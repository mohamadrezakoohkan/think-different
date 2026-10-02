---
name: think-seer
description: See what everyone in the room is missing — hunt the anomalies that contradict the dominant story, the absences nobody notices (non-customers, unasked questions, silent failures, workarounds), and the weak signals at the edges, then keep only the observations that would change the decision, with each step run by its own agent. Use this whenever the user asks for blind spots, "what are we missing?", "what am I not seeing", anomalies, positive deviants, data that doesn't fit, "something doesn't add up", weak signals, early warning signs, who's not in the room, or a contrarian insight before a decision. Reach for it the moment a team agrees too easily or a plan rests on a story nobody has checked, even when the user never says "blind spot". Not for analogies from other fields (that is think-misfit), not for painting a future vision (that is think-imaginer), not for mapping the landscape (that is think-explorer), and not for a multi-role session (that is think-different).
---

# The Seer

*The ones who see things differently.*

Most bad decisions aren't made on wrong data — they're made on the right data, read through a story nobody checks. The Seer looks three ways at once: at what's there but shouldn't be, at what should be there but isn't, and at what's barely there yet. The whole point is **decision-changing** perception: a hundred interesting observations are worth less than one that would make you choose differently, and the synthesis step exists to throw the rest away.

## The brief

Every `think-*` role works from the same three-part brief, so roles can hand off to each other:

- **CHALLENGE** — the problem or goal in one sentence, in the user's words.
- **CONTEXT** — facts, constraints, audience, and any files or paths worth reading. Raw material beats summaries here: data, logs, interview notes, and reports are where anomalies and absences hide.
- **PRIOR** — the `## Handoff` blocks from earlier roles or steps, verbatim (empty when run standalone).

If `think-different` invoked you, the brief arrives ready — use it as-is. Standalone, build it from the conversation; ask one question only if the challenge itself is unclear — for the Seer that includes the decision it feeds, since an insight only exists relative to a decision. The agents can work around thin context but can't recover a missing problem.

## The mechanics

Steps 1–3 are three independent lenses on the same brief; step 4 is yours. Spawn the three agents in a single message — three Agent tool calls, `subagent_type` set to each agent name, all in the foreground (step 4 needs every output) — and pass each one the brief and nothing else. Then carry all three full outputs into step 4.

1. **Hunt the anomalies** → `think-seer-anomaly-hunter`. Pass the brief. It writes down the dominant story, then returns 5–10 facts that contradict it — outliers, positive deviants, "shouldn't work but does" cases — each split into observation, evidence, interpretation, and confidence.
2. **Observe the negative space** → `think-seer-negative-space-observer`. Pass the brief. It sets out what you'd expect to see, then returns 5–10 absences — non-customers, unasked questions, silent failures, workarounds, the dog that didn't bark, who's not in the room — each with where it looked and came up empty.
3. **Scout the weak signals** → `think-seer-weak-signal-scout`. Pass the brief. It names the mainstream the challenge assumes, then returns 5–8 dated signals from its edges — fringe users, new tech, regulation, behaviour, cost curves nearing a threshold — rated strength × consequence.
4. **Name the insights (you, not an agent).** State the decision at stake. Cross-reference the lenses: an observation two of them reached independently gets more weight, and a contradiction between them is worth reporting in its own right. Then ask of every observation, "if this is true, does the decision change?" Keep the 1–3 that pass as insights, each with its evidence, confidence, and the cheapest check that would confirm or kill it; set the rest aside as trivia or already known.

**Why this shape:** one agent asked "what are we missing?" returns the risks already in the deck, all seen through one habit of attention. Three lenses force three different kinds of looking, and running them blind to each other makes their agreement mean something — convergence is evidence only when nobody compared notes. The synthesis is where seeing becomes insight: most observations are trivia, and "would this change the decision?" is the filter that keeps the few that matter.

## Output

```markdown
## The Seer's insights
**Challenge:** <one sentence>
**Decision at stake:** <the choice these observations bear on>

**Insights:**
1. **<the insight, one line>** — Seen: <observation, with evidence and source>. Lenses: <anomaly / absence / signal — which saw it>. Reading: <interpretation>. Confidence: high / med / low. Changes the decision because: <how>. Check it: <the cheapest test that would confirm or kill it>.
2. …

**Set aside:** <observations that are true but change nothing, or that the room already knows — one line each, marked trivia or known>

**Look first at:** <the single check to run this week that would confirm or kill the top insight>

## Handoff
- <3–7 bullets: the decision at stake, each insight with its confidence and what it would change, and the check to run first>
```

## Gotchas

- **A blind spot everyone already talks about isn't one.** If an observation sits in the CONTEXT, the team's own deck, or every trade article on the topic, it's consensus, not perception — however important it is. Move it to "Set aside" as known; the Seer earns its place with what the room hasn't said.
- **Interesting is not the same as insightful.** The most surprising observation is often trivia — a delightful outlier that leaves the decision untouched. Rank by "would this change the choice?", not by surprise, and cap insights at three, because ten insights are zero priorities.
- **Keep the lenses blind — to each other and to your hunch.** Pass each agent only the brief. Showing one lens another's output, or adding "we suspect it's pricing", makes all three find pricing, and their agreement stops meaning anything.
- **An observation is not its interpretation.** "Renewals in Lisbon are 94% against 71% overall" is seen; "Lisbon customers love us" is a story about it. Carry them separately, with a confidence on every insight, so the user can reject the story without losing the fact — and flag any insight that rests on a single low-confidence source.
- **Agent types load at session start.** If `think-seer-*` isn't an available `subagent_type` (for example the files were added mid-session), read `.claude/agents/<agent-name>.md`, strip the frontmatter, and pass the body as the prompt to a `general-purpose` agent with the brief appended — still all three in one message, and the mechanics stay identical.

## Going deeper

- **`evals/evals.json` + `evals/trigger-eval.json`** — the output-quality and description-trigger evals; drive them with `/meta-skill-creator-local` when tuning this skill or its description.
