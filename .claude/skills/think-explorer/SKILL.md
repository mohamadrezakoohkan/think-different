---
name: think-explorer
description: Explore the solution space — choose the dimensions that decide the outcome, place existing solutions and workarounds on them to show where everyone clusters, scout the empty regions and why each one is empty, then plan cheap probes ranked by learning per cost, with each step run by its own agent. Use this whenever the user wants to map a landscape, see all the options or alternatives, find white space or an unserved niche, draw a competitive map, or test a direction cheaply before committing, or asks "what's out there?", "where's the gap?", "map the market", or "how could we test this cheaply?". Reach for it the moment someone is about to pick a direction without seeing the territory, even when they never say "white space". Not for blind spots or anomalies (that is think-seer), not for inventing a mechanism (that is think-inventor), not for picking one idea and prototyping it (that is think-creator), and not for a multi-role session (that is think-different).
---

# The Explorer

*They explore.*

Most teams choose a direction after glancing at three competitors — then discover the territory was bigger, stranger, and more crowded than they thought. The Explorer maps the whole solution space first, finds the regions nobody occupies, and sends cheap probes before anyone commits. The whole point is **the axes**: a map drawn on the dimensions everyone already competes on only shows the white space everyone already sees, and a gap that's empty because it's impossible is a trap, not an opportunity.

## The brief

Every `think-*` role works from the same three-part brief, so roles can hand off to each other:

- **CHALLENGE** — the problem or goal in one sentence, in the user's words.
- **CONTEXT** — facts, constraints, audience, and any files or paths worth reading.
- **PRIOR** — the `## Handoff` blocks from earlier roles or steps, verbatim (empty when run standalone).

If `think-different` invoked you, the brief arrives ready — use it as-is. Standalone, build it from the conversation; ask one question only if the challenge itself is unclear, since the agents can work around thin context but can't recover a missing problem.

## The mechanics

Each step is one agent. Run them in order — each consumes the previous step's `## Handoff`. Spawn each with the Agent tool, `subagent_type` set to the agent name, in the foreground (the next step needs its output). Pass the brief plus the previous step's full output in the prompt.

1. **Map the territory** → `think-explorer-territory-mapper`. Pass the brief. It returns the candidate dimensions it weighed, the 2–3 axes it chose and why they decide the outcome, 10–20 existing solutions, substitutes, and workarounds placed on them, and where they cluster. If the chosen axes could be pasted into any industry's pitch deck (price vs quality, simple vs powerful), send it back once for axes tied to this challenge's outcome.
2. **Scout the frontier** → `think-explorer-frontier-scout`. Pass the brief + the mapper's output. It returns the empty regions and the adjacent possible, each diagnosed as **tried-and-failed**, **impossible**, **overlooked**, or **newly viable**, with what could live in the open ones, the traps marked, and the top 3 regions picked.
3. **Plan the expeditions** → `think-explorer-expedition-planner`. Pass the brief + the scout's output. For each top region it returns a falsifiable hypothesis, the smallest experiment, cost and time, and a go/no-go signal set in advance — ranked by learning per cost.
4. **Deliver the map (you, not an agent).** Lead with the axes and the crowd so the user sees why the white space is white, present the open regions alongside the traps, and end with the top-ranked probe, in the output shape below.

**Why this shape:** one agent asked to "find the white space" draws the industry's usual 2×2, points at the empty corner, and calls it an opportunity. Splitting the steps forces a deliberate choice of axes before anyone looks for gaps, an honest diagnosis of every gap before anyone gets excited, and lets the planner spend its whole effort on making the first step cheap instead of cheering for the destination.

## Output

```markdown
## The Explorer's map
**Challenge:** <one sentence>

**The axes that matter:** <axis A> × <axis B> (× <axis C>) — <why these decide the outcome, and which conventional axes were set aside>

**Where everyone clusters:** <the crowded region, who's in it, and why they converge>

**White space worth exploring:**
1. **<region>** — empty because <tried-and-failed / overlooked / newly viable, with the reason>. What could live there: <concrete offering or approach>.
2. …

**Traps (empty for a reason):** <regions ruled impossible or still failing, one line each>

**First expedition:** <the top-ranked probe — hypothesis, experiment, cost/time, go/no-go signal — startable this week>

## Handoff
- <3–7 bullets: the axes, the chosen white space and why it's open, the first probe and its go/no-go signal, and the traps any next role must avoid>
```

## Gotchas

- **The industry's axes produce the industry's map.** Price vs quality is where every competitor already looks, so every gap on it is either taken or empty for a reason. The axes worth mapping on are usually an outcome the user cares about that the market doesn't compete on — if the mapper's axes are generic, rerun it before scouting.
- **Empty is not the same as open.** A region can be empty because physics, law, or unit economics forbid it, or because someone tried and died there. Impossible regions are traps; tried-and-failed ones are worth a probe only if the scout names what changed since the failure. Only overlooked and newly viable regions are fresh ground.
- **A probe that can't fail isn't a probe.** "Launch and see how people react" confirms whatever you hoped. Every probe needs its go/no-go threshold written down before it runs — if either outcome leads to the same decision, send the planner back.
- **Don't hand the mapper the gap you're hoping for.** Pass only the brief. If the prompt also says "we think the opening is X", the mapper picks axes that make X look empty and the whole map bends around it.
- **Agent types load at session start.** If `think-explorer-*` isn't an available `subagent_type` (for example the files were added mid-session), read `.claude/agents/<agent-name>.md`, strip the frontmatter, and pass the body as the prompt to a `general-purpose` agent with the brief appended — the mechanics stay identical.

## Going deeper

- **`evals/evals.json` + `evals/trigger-eval.json`** — the output-quality and description-trigger evals; drive them with `/meta-skill-creator-local` when tuning this skill or its description.
