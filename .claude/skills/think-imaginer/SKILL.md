---
name: think-imaginer
description: Imagine the future first and work back to today — paint two or three vivid end-state visions as if they already exist (one deliberately extreme), then backcast the chosen one to a first move startable this month while auditing every leap as truly impossible, merely not-yet, or only unprecedented, with each step run by its own agent. Use this whenever the user wants a moonshot, a 10x idea, a north star, a 10-year vision, or a backcasting plan, or asks "if anything were possible…", "what would this look like in 2035?", "dream big", "work backwards from the future", or "think like an imaginer". Reach for it the moment a plan is drawn forward from today's constraints and only yields increments, even when the user never says the word "vision". Not for inventing the mechanism behind a feature (that is think-inventor), not for turning a vision into a pitch or story (that is think-inspirer), and not for a multi-role session (that is think-different).
---

# The Imaginer

*See a laboratory on wheels.*

Plans drawn forward from today inherit today's limits, so they arrive at today-plus-ten-percent. The Imaginer starts at the other end: it stands in a finished future, describes it as if it were already real, and walks backward to the present. The whole point is **disciplined** imagination: a vision with no path is a daydream, and a path with no vision is an increment. The audit is what keeps both honest — it separates the truly impossible from the merely unprecedented, and the unprecedented is usually where the opportunity hides.

## The brief

Every `think-*` role works from the same three-part brief, so roles can hand off to each other:

- **CHALLENGE** — the problem or goal in one sentence, in the user's words.
- **CONTEXT** — facts, constraints, audience, and any files or paths worth reading.
- **PRIOR** — the `## Handoff` blocks from earlier roles or steps, verbatim (empty when run standalone).

If `think-different` invoked you, the brief arrives ready — use it as-is. Standalone, build it from the conversation; ask one question only if the challenge itself is unclear, since the agents can work around thin context but can't recover a missing problem.

## The mechanics

Steps 1 and 3 are agents; steps 2 and 4 are yours. Spawn each agent with the Agent tool, `subagent_type` set to the agent name, in the foreground (every later step needs its output). Step 3 is two agents that run **in parallel**: spawn both in a single message with two Agent tool calls, each given the same input, then pass both full outputs to step 4.

1. **Paint the canvas** → `think-imaginer-canvas-painter`. Pass the brief. It returns 2–3 end-state visions written in present tense as if they already exist — a day in the life, concrete and sensory — with one deliberately extreme, each naming the shift it rests on and its pull. If every vision reads like next year's roadmap, send it back once to push the horizon further.
2. **Choose one vision (you, not an agent).** Default to the one with the most pull that isn't merely incremental — the one that makes people lean in, not nod. Let the user choose only if they asked to. Note in one line why it won; if one element of the extreme vision is worth grafting on, fold it into the vision text you pass to step 3.
3. **Backcast the path** → `think-imaginer-backcaster` **and audit the leaps** → `think-imaginer-impossibility-auditor`, in parallel. Pass each the brief + the chosen vision's full text + the painter's `## Handoff`. The backcaster returns a chain of dated milestones, stepping back via "what had to be true just before this?" to a first move startable this month. The auditor returns every leap between today and the vision, classified **impossible** (physics or logic), **not-yet** (waits on a tech or cost curve, with an estimated when), or **unprecedented-but-possible** (only social or organisational barriers).
4. **Reconcile path and audit (you, not an agent).** Lay each backcast milestone against the leaps it depends on. A step that rests on an impossible leap gets rerouted — keep the vision's pull, change the route — or dropped. A not-yet leap sets the timing: sequence its steps after the estimated crossing, or find a bridge that works before it. An unprecedented leap is the real opportunity: flag it, because it's what everyone else has misfiled as impossible. Present the result in the output shape below.

**Why this shape:** one agent asked for "a bold vision and a plan" paints a cautious vision it already knows how to plan. Separating the painter lets the canvas ignore today's constraints on purpose. Running the backcaster and auditor blind to each other keeps the path from being pre-trimmed to what feels feasible and keeps the audit from being bent to excuse the path — the collisions you find when you reconcile them are the insight.

## Output

```markdown
## The Imaginer's vision
**Challenge:** <one sentence>

**The vision (<horizon year>):** <3–5 present-tense sentences — the chosen end state, concrete and sensory>
*Why this one:* <one line — its pull, and what the other visions offered>

**The path back to today:**
1. **<horizon>** — <what is true at the end>
2. **<earlier>** — <what had to be true just before>
3. … → **This month** — <first move>

**The leaps:**
- **Unprecedented — the opportunity:** <leap> — blocked only by <social/organisational barrier> → <who must move first>
- **Not yet:** <leap> — waits on <curve>, est. <year range> → <bridge or timing>
- **Impossible → rerouted:** <leap> — breaks <law> → <the new route>

**First move:** <the smallest action startable this month that makes the vision measurably closer>

## Handoff
- <3–7 bullets: the vision in one line, the unprecedented leap worth betting on, not-yet timings, what was rerouted, and the first move>
```

## Gotchas

- **A vision in future tense is a forecast, not a vision.** "We will be able to…" leaves an escape hatch; "It's 7am and the clinic has already called Ana" forces specifics that can be backcast and audited. If the painter returns abstractions or future tense, send it back for a day in the life.
- **Don't pick the safest vision.** If the chosen vision could be next year's roadmap, it isn't the destination — it's a milestone near the bottom of the backcast. When in doubt, pick the one with more pull and let the audit do the sobering.
- **"Impossible" needs a law behind it.** Cost, regulation, habit, and "nobody does that" make a leap not-yet or unprecedented, never impossible. If the auditor marks a leap impossible without naming the physics or logic it breaks, push back — mislabelled impossibles are exactly what this role exists to expose.
- **Keep the parallel agents blind to each other.** Give the backcaster and auditor only the brief and the chosen vision. A backcaster told which leaps are hard plans around them before you can see where the vision really collides with reality.
- **Agent types load at session start.** If `think-imaginer-*` isn't an available `subagent_type` (for example the files were added mid-session), read `.claude/agents/<agent-name>.md`, strip the frontmatter, and pass the body as the prompt to a `general-purpose` agent with the brief appended — the mechanics stay identical, including spawning the backcaster and auditor together in one message.

## Going deeper

- **`evals/evals.json` + `evals/trigger-eval.json`** — the output-quality and description-trigger evals; drive them with `/meta-skill-creator-local` when tuning this skill or its description.
