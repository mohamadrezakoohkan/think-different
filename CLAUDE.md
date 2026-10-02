# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Claude Code toolkit for the goal "Think Different", with no application code. Each **role** from the "Crazy Ones" manifesto is one skill in `.claude/skills/think-<role>/`. Each **mechanic** (a step inside a role) is one subagent in `.claude/agents/think-<role>-<mechanic>.md`. `think-different` is the orchestrator: it picks an arc of roles and chains them. The authoritative wiring is the JSON graph below; the per-file prose (procedures, gotchas, output templates) lives in each `SKILL.md` and agent file.

## Commands

- **Validate everything:** `python3 scripts/validate.py --root .` (stdlib only; exit 0 clean, 1 violations, 2 usage). It checks naming, frontmatter, section order, description lengths, eval files, and that the graph below matches the skill and agent files on disk. Run it after any edit under `.claude/`.
- **Test one skill:** invoke it with a prompt from its `evals/evals.json` and check the output against that eval's `expectations`.
- **Full eval loop and description trigger-tuning:** `/meta-skill-creator-local` (the user's personal skill, not in this repo) on `evals/evals.json` + `evals/trigger-eval.json`.
- There is nothing to build and there are no dependencies.

## Graph

Schema:
- `contract`: rules shared by every node.
- `orchestrator`: how `think-different` chooses and runs arcs.
- `roles.<skill>.steps[]`: executed in `n` order.
  - `needs`: the inputs to put in the agent's prompt. `brief` = CHALLENGE+CONTEXT+PRIOR; `sN` = step N's full output; `sN.handoff` = only its `## Handoff` block.
  - `par`: a group id; steps sharing it are spawned together in ONE message.
  - `by:"main"`: a step the main thread does itself (never an agent).
  - `if` / `max_runs`: a conditional step.
  - `web`: the agent has WebSearch/WebFetch (absent = false).
- `defer`: request topics that belong to another skill.
- `feeds`: natural successor roles for chaining.
- An agent whose `needs` is exactly `["brief"]` is safe to spawn standalone. All others stop if their inputs are missing.

<!-- graph:begin -->
```json
{
  "schema": "think-graph/v1",
  "contract": {
    "brief": {"CHALLENGE": "one sentence, user's words", "CONTEXT": "facts, constraints, audience, file paths agents may Read", "PRIOR": "verbatim '## Handoff' blocks from earlier steps/roles; empty when standalone"},
    "agent_output_ends_with": "## Handoff",
    "role_output_ends_with": "## Handoff",
    "agents": "read-only (Read, Grep, Glob [+WebSearch, WebFetch]); return text inline; main thread writes files only on user request",
    "spawn": "Agent tool, subagent_type=<agent>, run_in_background=false; steps sharing a par group go in ONE message",
    "fallback": "if subagent_type unavailable: Read .claude/agents/<agent>.md, strip frontmatter, run body + brief via subagent_type=general-purpose",
    "nesting": "subagents cannot spawn subagents, so role skills (which spawn agents) must run in the main thread"
  },
  "orchestrator": {
    "skill": "think-different",
    "invokes": "role skills via Skill tool, sequentially, main thread; PRIOR accumulates each role's ## Handoff only",
    "default_arc": "short",
    "breaker_by_situation": {
      "data but no insight; something feels off": "think-seer",
      "boxed in by how it's done; industry standard treated as law": "think-rebel",
      "everyone in the field proposes the same thing": "think-misfit",
      "team agreed too fast; plan feels safe": "think-troublemaker",
      "nobody knows what else is out there": "think-explorer",
      "a technical trade-off blocks every option": "think-inventor",
      "stuck in incrementalism; needs a moonshot": "think-imaginer",
      "people are hurting: complaints, churn, burnout": "think-healer"
    },
    "arcs": {
      "short": ["think-round-peg", "$breaker", "think-creator"],
      "breakthrough": ["think-round-peg", "think-rebel", "think-misfit", "think-troublemaker", "think-creator"],
      "moonshot": ["think-imaginer", "think-rebel", "think-inventor", "think-creator", "think-inspirer"],
      "human": ["think-healer", "think-seer", "think-round-peg", "think-inventor", "think-creator"],
      "strategy": ["think-seer", "think-explorer", "think-misfit", "think-troublemaker", "think-creator"],
      "full": ["think-round-peg", "think-seer", "think-rebel", "think-misfit", "think-troublemaker", "think-explorer", "think-inventor", "think-imaginer", "think-healer", "think-creator", "think-inspirer"]
    },
    "arc_selection": "short unless the situation matches a preset; full only when the user explicitly asks for everything",
    "synthesis_out": "# Think Different: … (different idea, what it breaks, why it might work, what would kill it, first move, runner-ups, safe option kept separate)"
  },
  "roles": {
    "think-round-peg": {
      "job": "reframe the problem itself; expose smuggled-in solutions and XY problems",
      "defer": {"inventory/break assumptions": "think-rebel", "root cause of user pain": "think-healer"},
      "steps": [
        {"n": 1, "agent": "think-round-peg-frame-auditor", "needs": ["brief"], "out": "frame card, smuggled solution, XY check, underlying need"},
        {"n": 2, "agent": "think-round-peg-reframer", "needs": ["brief", "s1"], "out": "8-12 'How might we' framings tagged by lever"},
        {"n": 3, "agent": "think-round-peg-frame-judge", "needs": ["brief", "s1", "s2"], "out": "scored framings, primary + wildcard, new problem statement"},
        {"n": 4, "by": "main", "out": "## The Round Peg's reframe + ## Handoff (first bullet = new problem statement)"}
      ],
      "feeds": ["think-rebel", "think-misfit", "think-troublemaker", "think-seer", "think-explorer", "think-inventor", "think-healer", "think-creator"]
    },
    "think-seer": {
      "job": "perception: anomalies, absences, weak signals; keep only observations that change the decision",
      "defer": {"analogies from other fields": "think-misfit", "future vision": "think-imaginer", "landscape map": "think-explorer"},
      "steps": [
        {"n": 1, "agent": "think-seer-anomaly-hunter", "needs": ["brief"], "par": "lenses", "web": true, "out": "facts contradicting the dominant story"},
        {"n": 2, "agent": "think-seer-negative-space-observer", "needs": ["brief"], "par": "lenses", "web": true, "out": "meaningful absences"},
        {"n": 3, "agent": "think-seer-weak-signal-scout", "needs": ["brief"], "par": "lenses", "web": true, "out": "dated edge signals, strength x consequence"},
        {"n": 4, "by": "main", "out": "## The Seer's insights + ## Handoff", "note": "state the decision at stake; weight observations reached by 2+ lenses"}
      ],
      "feeds": ["think-explorer", "think-rebel", "think-round-peg", "think-misfit"]
    },
    "think-rebel": {
      "job": "find inherited rules, judge each, break the dead ones from first principles",
      "defer": {"reframe the problem": "think-round-peg", "attack a finished plan": "think-troublemaker"},
      "steps": [
        {"n": 1, "agent": "think-rebel-rule-excavator", "needs": ["brief"], "web": true, "out": "typed rule inventory (10-20)"},
        {"n": 2, "agent": "think-rebel-fence-inspector", "needs": ["brief", "s1"], "web": true, "out": "verdicts: load-bearing | weakened | dead"},
        {"n": 3, "agent": "think-rebel-rule-breaker", "needs": ["brief", "s2"], "out": "delete/invert breaks that respect load-bearing rules"},
        {"n": 4, "by": "main", "out": "## The Rebel's verdict + ## Handoff"}
      ],
      "feeds": ["think-misfit", "think-troublemaker", "think-inventor", "think-creator"]
    },
    "think-misfit": {
      "job": "outsider lens: transplant mechanisms from distant domains",
      "defer": {"rules/assumptions": "think-rebel", "reframe the problem": "think-round-peg"},
      "steps": [
        {"n": 1, "agent": "think-misfit-consensus-mapper", "needs": ["brief"], "par": "scan", "web": true, "out": "insider orthodoxy, taboos, blind side"},
        {"n": 2, "agent": "think-misfit-domain-raider", "needs": ["brief"], "par": "scan", "web": true, "out": "structural core + 4-6 distant-domain mechanisms", "note": "brief only; never pass the consensus map or a favourite analogy"},
        {"n": 3, "agent": "think-misfit-transplanter", "needs": ["brief", "s1", "s2"], "out": "transplants ranked distance x plausibility"},
        {"n": 4, "by": "main", "out": "## The Misfit's find + ## Handoff"}
      ],
      "feeds": ["think-troublemaker", "think-creator"]
    },
    "think-troublemaker": {
      "job": "provocation -> movement -> symmetric pre-mortem of new idea vs status quo",
      "defer": {"assumption inventory": "think-rebel"},
      "steps": [
        {"n": 1, "agent": "think-troublemaker-provocateur", "needs": ["brief"], "out": "10-15 'Po:' provocations by technique"},
        {"n": 2, "agent": "think-troublemaker-movement-miner", "needs": ["brief", "s1"], "out": "practical ideas mined from provocations"},
        {"n": 3, "agent": "think-troublemaker-red-teamer", "needs": ["brief", "s2"], "web": true, "out": "kill/wound/scratch pre-mortems for both sides", "note": "put the current plan in CONTEXT; absent = 'keep doing what we do today'"},
        {"n": 4, "by": "main", "out": "## The Troublemaker's report + verdict switch|hybrid|stay + ## Handoff"}
      ],
      "feeds": ["think-creator"]
    },
    "think-explorer": {
      "job": "map the solution space, diagnose white space, plan cheap probes",
      "defer": {"blind spots": "think-seer", "invent a mechanism": "think-inventor", "pick one and prototype": "think-creator"},
      "steps": [
        {"n": 1, "agent": "think-explorer-territory-mapper", "needs": ["brief"], "web": true, "out": "decisive axes + where existing solutions cluster"},
        {"n": 2, "agent": "think-explorer-frontier-scout", "needs": ["brief", "s1"], "web": true, "out": "empty regions diagnosed tried-and-failed | impossible | overlooked | newly viable"},
        {"n": 3, "agent": "think-explorer-expedition-planner", "needs": ["brief", "s2"], "out": "probes ranked by learning per cost"},
        {"n": 4, "by": "main", "out": "## The Explorer's map + ## Handoff"}
      ],
      "feeds": ["think-creator", "think-misfit", "think-inventor"]
    },
    "think-inventor": {
      "job": "new mechanisms via morphological matrix, contradictions, separation/TRIZ",
      "defer": {"map existing options": "think-explorer", "moonshot vision": "think-imaginer", "borrow from distant fields": "think-misfit", "prototype a chosen idea": "think-creator"},
      "steps": [
        {"n": 1, "agent": "think-inventor-decomposer", "needs": ["brief"], "out": "morphological matrix + core contradictions"},
        {"n": 2, "agent": "think-inventor-recombiner", "needs": ["brief", "s1"], "web": true, "out": "8-12 non-obvious concepts"},
        {"n": 3, "agent": "think-inventor-mechanism-sketcher", "needs": ["brief", "s2", "s1.handoff"], "out": "top-3 how-it-works specs + cheapest kill test"},
        {"n": 4, "by": "main", "out": "## The Inventor's mechanisms + ## Handoff"}
      ],
      "feeds": ["think-creator"]
    },
    "think-imaginer": {
      "job": "future-back: paint visions, backcast one, audit every leap",
      "defer": {"invent the mechanism": "think-inventor", "turn vision into a pitch": "think-inspirer"},
      "steps": [
        {"n": 1, "agent": "think-imaginer-canvas-painter", "needs": ["brief"], "out": "2-3 present-tense end-state visions, one extreme"},
        {"n": 2, "by": "main", "out": "one chosen vision (most pull, not incremental)"},
        {"n": 3, "agent": "think-imaginer-backcaster", "needs": ["brief", "s2", "s1.handoff"], "par": "path", "out": "milestone chain back to a first move this month"},
        {"n": 3, "agent": "think-imaginer-impossibility-auditor", "needs": ["brief", "s2", "s1.handoff"], "par": "path", "web": true, "out": "leaps: impossible | not-yet | unprecedented-but-possible"},
        {"n": 4, "by": "main", "out": "## The Imaginer's vision + ## Handoff", "note": "reroute steps resting on impossible leaps"}
      ],
      "feeds": ["think-rebel", "think-inventor", "think-inspirer", "think-creator"]
    },
    "think-healer": {
      "job": "human pain -> root cause -> humane remedy with do-no-harm check",
      "defer": {"reframe the problem": "think-round-peg", "invent a mechanism": "think-inventor", "open brainstorm": "think-different"},
      "steps": [
        {"n": 1, "agent": "think-healer-pain-cartographer", "needs": ["brief"], "web": true, "out": "pain map incl. hidden stakeholders, wants vs needs"},
        {"n": 2, "agent": "think-healer-root-cause-diagnostician", "needs": ["brief", "s1"], "out": "causal chains, highest-leverage root cause, evidence gaps"},
        {"n": 3, "agent": "think-healer-remedy-designer", "needs": ["brief", "s2", "s1"], "out": "3-5 remedies with do-no-harm checks"},
        {"n": 4, "by": "main", "out": "## The Healer's prescription + ## Handoff"}
      ],
      "feeds": ["think-inventor", "think-creator", "think-round-peg"]
    },
    "think-creator": {
      "job": "converge on one sharp idea, prototype it, edit to essence",
      "defer": {"generate new ideas": "think-inventor|think-misfit|think-troublemaker", "pitch/story": "think-inspirer"},
      "steps": [
        {"n": 1, "agent": "think-creator-converger", "needs": ["brief", "idea_pool"], "out": "ONE idea + kill list", "note": "idea_pool = PRIOR handoffs or a user-supplied list; if neither, ask or run a generator role first"},
        {"n": 2, "agent": "think-creator-prototyper", "needs": ["brief", "s1"], "out": "smallest tangible artifact, inline"},
        {"n": 3, "agent": "think-creator-editor", "needs": ["brief", "s2", "s1.handoff"], "out": "edited artifact + cut list"},
        {"n": 4, "by": "main", "out": "## The Creator's work + ## Handoff", "note": "artifact inline; write a file only if the user asks"}
      ],
      "feeds": ["think-inspirer", "think-troublemaker"]
    },
    "think-inspirer": {
      "job": "core truth -> story -> simulated audiences -> at most one revision",
      "defer": {"form, choose, or envision the idea": "think-creator|think-imaginer"},
      "steps": [
        {"n": 1, "agent": "think-inspirer-truth-distiller", "needs": ["brief"], "out": "one-sentence why (a belief), enemy, audience, proof points"},
        {"n": 2, "agent": "think-inspirer-storyteller", "needs": ["brief", "s1"], "out": "numbered draft in the CONTEXT format (default ~90s spoken pitch)"},
        {"n": 3, "agent": "think-inspirer-audience-simulator", "needs": ["brief", "s1.handoff", "s2"], "out": "line-level reactions, notes flagged blocking | polish"},
        {"n": 4, "agent": "think-inspirer-storyteller", "needs": ["brief", "s1", "s2", "s3"], "if": "s3 has >=1 blocking note", "max_runs": 1, "out": "revised draft"},
        {"n": 5, "by": "main", "out": "## The Inspirer's piece + ## Handoff"}
      ],
      "feeds": []
    }
  }
}
```
<!-- graph:end -->

## Orchestration protocol

1. **Route every request to the narrowest entry point that covers it:**
   - The user names a role or lens → that role skill.
   - A generic "think differently / unconventional / rethink this", or more than one lens is needed → `think-different`.
   - The request matches one role's `job` → that role skill. Use `defer` to break ties.
   - A narrow single-mechanic ask ("just list our assumptions") whose agent `needs` only `["brief"]` → spawn that agent directly.

   Prefer a skill over thinking it through ad hoc: the step separation is what stops one pass from collapsing into the obvious answer.
2. **Build the brief once and reuse it.** Put readable file paths in CONTEXT, since agents can Read, Grep, and Glob. After `think-round-peg` runs, set CHALLENGE to its new problem statement and move the original into CONTEXT, so every later role works on the reframed problem.
3. **Run a role only through its skill.** The skill owns step order, `par` groups, send-back checks (for example, "fewer than 10 rules → send the excavator back once"), and the `by:"main"` synthesis. Spawning a role's agents by hand skips all of that.
4. **Chain roles through handoffs, never through transcripts.** PRIOR receives only `## Handoff` blocks. Full outputs anchor later roles on earlier phrasing.
5. **Use parallelism only where the graph declares it** (`par`), and never across roles. Roles run sequentially in the main thread because they spawn agents, and subagents cannot spawn subagents. Never delegate a role skill to a subagent.
6. **Keep generator agents blind.** Don't pass your own leaning, favourite analogy, or "we're thinking of X" to raiders, breakers, recombiners, provocateurs, or the Seer lenses. Pass exactly what `needs` lists.
7. **Extend reach after a standalone role.** When a role finishes outside `think-different`, offer the most fitting `feeds` successor in one line (for example, Round Peg → a breaker; any generator → Creator; Creator → Inspirer). Run it only if the user wants to continue. If the user asked for an end-to-end outcome up front ("…and make it concrete"), switch to `think-different` instead of chaining by hand.
8. **Protect the different idea at every synthesis.** Keep the safe or conventional option as a separate line for contrast; never blend it into the winner.

## Editing invariants

- **Naming:** directory == `name` == `think-<role>` for skills; filename == `name` == `think-<role>-<mechanic>` for agents.
- **Skill frontmatter:** exactly `name`, `description`. The description is a single line of 700–1000 chars covering what it does, when to use it, a pushy nudge, and a negative boundary that names the adjacent `think-*` skills plus `think-different`.
- **Skill sections, in order:** H1 → epigraph → framing → `## The brief` → `## The mechanics` → `## Output` (template ending `## Handoff`) → `## Gotchas` (last item is always the agent-fallback gotcha) → `## Going deeper`.
- **Agent frontmatter:** exactly `name`, `description` (single line, ≤450 chars, beginning `Step <n> of the think-<role> skill.`), `tools`. No `model:` key.
- **Agent sections, in order:** `# … Agent` → `## Role` (including what it does NOT do) → `## Inputs` → `## Process` → `## Output Format` (ending `## Handoff`) → `## Guidelines`.
- **Adding, removing, or renaming a role or agent** means updating, together:
  - the role's `## The mechanics`
  - the graph above
  - the cast table and arcs in `think-different/SKILL.md`
  - the negative boundaries of adjacent skills
  - that role's `evals/`

  Then run the validator.
- **House authoring conventions** come from the user's personal skill `meta-skill-authoring-local`. Load it before restructuring a skill.
