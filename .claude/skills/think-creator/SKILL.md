---
name: think-creator
description: Create one real thing out of a pile of ideas — converge the pool on a single sharp idea with an explicit kill list, build the smallest tangible prototype that makes it real enough to react to (a spec, mock, landing copy, code sketch, or storyboard), then edit it down to its essence, with each step run by its own agent. Use this whenever the user has too many ideas and must pick one, wants an idea made tangible, asks for a prototype, mock, or MVP, or wants something cut to the essentials, including "pick one and make it real", "which of these should we build?", "what's the MVP?", or "simplify this". Reach for it the moment a brainstorm has produced more options than anyone can act on, even when the user never says the word prototype. Not for generating new ideas (that is think-inventor, think-misfit, or think-troublemaker), not for pitching or storytelling (that is think-inspirer), not for production code, and not for a multi-role session (that is think-different).
---

# The Creator

*They create.*

Ideas are cheap; what's scarce is one idea someone has committed to and made real enough to judge. The Creator takes a pool of ideas, chooses one with conviction, makes it tangible, then takes things away until only the idea remains. The whole point is **commitment without compromise**: the easy move is to blend the five best ideas into one safe concept nobody objects to and nobody wants. The converger protects the sharp edge, and the editor makes sure the prototype didn't sand it off.

## The brief

Every `think-*` role works from the same three-part brief, so roles can hand off to each other:

- **CHALLENGE** — the problem or goal in one sentence, in the user's words.
- **CONTEXT** — facts, constraints, audience, and any files or paths worth reading.
- **PRIOR** — the `## Handoff` blocks from earlier roles or steps, verbatim (empty when run standalone). For the Creator, PRIOR is the idea pool.

If `think-different` invoked you, the brief arrives ready — use it as-is. Standalone, build it from the conversation and put the ideas the user listed into PRIOR as the pool; ask one question only if the challenge itself is unclear or there are no ideas to converge on, since the agents can work around thin context but can't recover a missing problem — or a missing pool.

## The mechanics

Each step is one agent. Run them in order — each consumes the previous step's `## Handoff`. Spawn each with the Agent tool, `subagent_type` set to the agent name, in the foreground (the next step needs its output). Pass the brief plus the previous step's full output in the prompt.

1. **Converge on one idea** → `think-creator-converger`. Pass the brief (PRIOR carries the pool). It clusters the pool, scores each cluster on distinctiveness, value, and feasibility, and returns ONE idea with its sharp edge named, the bet it rests on, and an explicit kill list. If it returns a blend of several ideas or kills without reasons, it compromised — send it back once to choose.
2. **Make it tangible** → `think-creator-prototyper`. Pass the brief + the converger's output. It picks the one medium that fits (one-page spec, text or HTML mock, landing-page copy, code sketch, storyboard), builds the moment where the sharp edge is felt first, and returns the artifact inline — agents are read-only, so nothing is written to disk.
3. **Edit to the essence** → `think-creator-editor`. Pass the brief + the prototyper's full output + the converger's `## Handoff` (so it knows which edge to protect). It cuts everything the idea doesn't need, returns the edited artifact with a cut list and a reason per cut, and checks that the core idea and its sharp edge survived.
4. **Present the work (you, not an agent).** Show the one idea, the edited artifact in full, the kill list, and the cut list in the output shape below. Keep the artifact inline; write it to a file only if the user asks for one.

**Why this shape:** choosing, making, and cutting pull against each other, and one agent asked to do all three hedges on each — it picks the safest idea, builds everything it can think of, and never cuts what it just made. Splitting the steps forces a real choice with a written kill list first, a concrete artifact second, and an editor who neither chose nor built the thing and so has no attachment to any part of it.

## Output

```markdown
## The Creator's work
**Challenge:** <one sentence>

**The one idea:** <one sentence> — sharp edge: <the distinctive property that was protected>

**Why this one:** <one or two lines — how it scored and why it beat the runner-up>

**Killed:** <each killed idea, one line, with its specific reason; mark any `parked`>

**The prototype:**
<the edited artifact, in full>

**Cut in the edit:** <what was removed and why, one line each>

**Show it to:** <who reacts first, and the reaction that would confirm or kill the bet>

## Handoff
- <3–7 bullets: the chosen idea and its sharp edge, what the prototype is, what was killed, and the bet a reaction to the prototype should settle>
```

## Gotchas

- **No idea pool means no Creator run — yet.** If PRIOR is empty and the user listed no ideas, don't let the converger invent a pool; it will pick its own favourite and call it a decision. Ask the user for their candidate ideas, or suggest a generating role first (`think-inventor`, `think-misfit`, `think-troublemaker`) or `think-different` for the full arc.
- **The "best of all worlds" hybrid is not convergence.** Merging the top three ideas feels safe and almost always yields a concept with no edge. The converger may graft one specific element from a killed idea, but only if it sharpens the winner; if the chosen idea reads like a committee wrote it, send it back.
- **The prototype is for reacting to, not for shipping.** Even for software, the prototyper returns a sketch — a mock, interfaces with stubs, a spec — never production code. If the user wants it built for real, that is a separate engineering task after this skill.
- **An editor who cuts the core idea has failed, not simplified.** If the survival check says the sharp edge is weaker or gone, restore the cut that carried it and keep the rest of the edit — essence means the idea with nothing else, not nothing.
- **Agent types load at session start.** If `think-creator-*` isn't an available `subagent_type` (for example the files were added mid-session), read `.claude/agents/<agent-name>.md`, strip the frontmatter, and pass the body as the prompt to a `general-purpose` agent with the brief appended — the mechanics stay identical.

## Going deeper

- **`evals/evals.json` + `evals/trigger-eval.json`** — the output-quality and description-trigger evals; drive them with `/meta-skill-creator-local` when tuning this skill or its description.
