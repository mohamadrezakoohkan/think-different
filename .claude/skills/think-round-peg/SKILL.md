---
name: think-round-peg
description: Reframe the problem itself rather than polishing solutions — audit it as stated to expose the smuggled-in solution, the hidden stakeholder and metric, and any XY problem, generate "How might we…" reframings with named levers, then judge them for fidelity to the real need and deliver a new problem statement plus a wildcard framing, with each step run by its own agent. Use this whenever the user wonders if they are solving the right problem, feels every solution is wrong, wants a problem statement or how-might-we questions, or says "are we solving the right problem?", "what is the real problem here", "reframe this", "is this an XY problem", or "we need an app that…". Reach for it the moment a request arrives with its solution already baked in, even when the user never says "reframe". Not for inventorying and breaking assumptions (that is think-rebel), not for tracing the root cause of user pain (that is think-healer), and not for a multi-role session (that is think-different).
---

# The Round Peg

*The round pegs in the square holes.*

Many stuck problems aren't stuck because the solutions are weak — they're stuck because the problem was stated wrong. A request arrives with its answer already welded in ("we need an app that…"), aimed at one stakeholder, measured by one number, on one timescale, and every idea gets sanded down to fit that hole. The Round Peg questions the hole instead of the peg. The whole point is **faithful** reframing: a new frame must still serve the need underneath the original. A reframe that's clever but abandons the real need is a dodge, not an insight, and the judging step exists to catch it.

## The brief

Every `think-*` role works from the same three-part brief, so roles can hand off to each other:

- **CHALLENGE** — the problem or goal in one sentence, in the user's words. Keep their exact phrasing here; the smuggled-in solution usually hides in the wording.
- **CONTEXT** — facts, constraints, audience, and any files or paths worth reading.
- **PRIOR** — the `## Handoff` blocks from earlier roles or steps, verbatim (empty when run standalone).

If `think-different` invoked you, the brief arrives ready — use it as-is. Standalone, build it from the conversation; ask one question only if the challenge itself is unclear, since the agents can work around thin context but can't recover a missing problem.

## The mechanics

Each step is one agent. Run them in order — each consumes the previous step's `## Handoff`. Spawn each with the Agent tool, `subagent_type` set to the agent name, in the foreground (the next step needs its output). Pass the brief plus the previous steps' full output in the prompt.

1. **Audit the frame** → `think-round-peg-frame-auditor`. Pass the brief. It returns the stated problem dissected into a frame card — smuggled-in solution, whose problem it is, success metric, timescale, scope boundary, unit, and the square hole it's forced into — plus an XY-problem check and the underlying need in one solution-free sentence. If the challenge names a product, feature, or tool and the auditor reports "no smuggled-in solution", send it back once; that is its most common miss.
2. **Generate reframes** → `think-round-peg-reframer`. Pass the brief + the auditor's output. It returns 8–12 "How might we…" framings, each tagged with its lever (zoom out, zoom in, flip stakeholder, change metric, change timescale, invert the goal, remove the embedded solution, change the unit, make it someone else's problem). If most framings lean on one or two levers, send it back once for breadth.
3. **Judge the frames** → `think-round-peg-frame-judge`. Pass the brief + the auditor's output + the reframer's output — the judge needs the auditor's underlying need to score fidelity. It scores every framing (and the original, as a control) on leverage, fidelity, and actionability, rejects dodges, and returns one primary, one wildcard, the new problem statement, and what the original frame excluded.
4. **Deliver the new problem (you, not an agent).** Put the new problem statement first and the original beside it so the user sees what moved, name the wildcard, list what the original frame hid, and suggest the cheapest way to test the new frame. Stop at the problem — solving it belongs to the user or the next role.

**Why this shape:** one agent asked to "reframe this" either paraphrases the problem in fancier words or jumps straight to solutions. Auditing first drags the frame into the open — you can't swap a frame you can't see. Generating with named levers forces real breadth instead of five synonyms. Judging separately lets the reframer be wild while the judge holds every framing to the underlying need; no single agent can diverge freely and police fidelity at the same time.

## Output

```markdown
## The Round Peg's reframe
**New problem statement:** How might we <verb> <for whom> so that <outcome tied to the real need>?
**Solved when:** <the new success metric>

**Original problem:** <the challenge as given, verbatim>
**What moved:** <lever used, and what the new frame lets in that the old one shut out>
**Real need it still serves:** <the underlying need, one line>

**Wildcard framing:** How might we …? — lever: <lever>. Worth a look if <condition>.

**What the original frame hid:**
- <smuggled-in solution, excluded stakeholder, metric, or timescale — one line each>

**Test the frame:** <the cheapest check that this is the right problem — one person to ask, one number to pull — doable this week>

## Handoff
- **New problem statement:** <verbatim — later roles should work on this, not the original>
- Real need it must keep serving: <one line>
- Wildcard framing: <verbatim>
- Smuggled-in solution: <set aside / kept as one option among many / confirmed as right>
- <1–3 bullets: stakeholders, metrics, or limits any next role must respect>
```

## Gotchas

- **"Reframe" does not mean "rephrase."** A frame only moved if it changes what counts as an answer — if every solution to the original also solves the new one, nothing happened. If the reframer's list reads like synonyms, send it back with the lever list.
- **A clever reframe that drops the real need is a dodge.** "Cut appointment wait times" → "make the wait feel useful" is a reframe; → "stop taking appointments" abandons the patients. The judge treats fidelity as a gate, not a weight; never promote a low-fidelity framing to primary because it's exciting — the wildcard may be bolder, never less faithful.
- **Exposing the smuggled-in solution isn't killing it.** Setting it aside lets other answers compete; sometimes the original frame wins the judging. Report that honestly — a confirmed frame is a real result, and it beats a forced reframe.
- **Agent types load at session start.** If `think-round-peg-*` isn't an available `subagent_type` (for example the files were added mid-session), read `.claude/agents/<agent-name>.md`, strip the frontmatter, and pass the body as the prompt to a `general-purpose` agent with the brief appended — the mechanics stay identical.

## Going deeper

- **`evals/evals.json` + `evals/trigger-eval.json`** — the output-quality and description-trigger evals; drive them with `/meta-skill-creator-local` when tuning this skill or its description.
