---
name: think-troublemaker
description: Make trouble on purpose — throw deliberately unreasonable provocations at a problem (reversals, exaggerations, wishful thinking, escapes, random entry), mine each one with lateral-thinking movement until it yields practical ideas, then red-team both the strongest new idea and the current plan with a symmetric pre-mortem, with each step run by its own agent. Use this whenever the user wants provocations, a devil's advocate, a pre-mortem, a red team, or lateral thinking, or types "play devil's advocate", "poke holes in this", "how does this fail?", "red-team our plan", "what's the craziest thing we could do", or "make trouble". Reach for it the moment a team is converging too comfortably on one plan or the safe option is treated as risk-free, even when nobody asks for anything provocative. Not for inventorying and judging the assumptions behind a problem (that is think-rebel), not for a routine risk register, and not for a multi-role session (that is think-different).
---

# The Troublemaker

*The only thing you can't do is ignore them.*

Teams kill strange ideas before they've had a chance to go anywhere, and spare their current plan the scrutiny they give every new one. The Troublemaker does both things polite teams avoid: it says the unreasonable thing on purpose, then attacks — the new idea and the status quo alike. The whole point is **productive** trouble: a provocation is a stepping stone, not a proposal, and its value is where you can move from it, not whether it's right. And the attack is symmetric, because staying put is a plan too, and it can fail.

## The brief

Every `think-*` role works from the same three-part brief, so roles can hand off to each other:

- **CHALLENGE** — the problem or goal in one sentence, in the user's words.
- **CONTEXT** — facts, constraints, audience, the current plan (the status quo the red-teamer will attack), and any files or paths worth reading.
- **PRIOR** — the `## Handoff` blocks from earlier roles or steps, verbatim (empty when run standalone).

If `think-different` invoked you, the brief arrives ready — use it as-is. Standalone, build it from the conversation; ask one question only if the challenge itself is unclear, since the agents can work around thin context but can't recover a missing problem. A missing current plan is fine — the red-teamer treats "keep doing what we do today" as the status quo.

## The mechanics

Each step is one agent. Run them in order — each consumes the previous step's `## Handoff`. Spawn each with the Agent tool, `subagent_type` set to the agent name, in the foreground (the next step needs its output). Pass the brief plus the previous step's full output in the prompt.

1. **Provoke** → `think-troublemaker-provocateur`. Pass the brief. It returns 10–15 "Po:" provocations, each labelled with its technique (reversal, exaggeration, distortion, wishful thinking, escape, random entry) and the taken-for-granted it attacks. If they read like sensible suggestions, it self-censored — send it back once to push further.
2. **Mine for movement** → `think-troublemaker-movement-miner`. Pass the brief + the provocateur's output. It moves forward from each provocation (extract the principle, focus on the difference, simulate moment to moment, find the positive, find where it would make sense), returns concrete ideas traced to their provocation, drops the barren ones, and names the strongest idea. Expect a third to half to be barren; if none are, it's softening provocations instead of moving from them.
3. **Red-team both sides** → `think-troublemaker-red-teamer`. Pass the brief (with the current plan in CONTEXT) + the miner's output. It pre-mortems the strongest idea and the status quo — "it's 18 months later and it failed; why?" — grading every failure **kill**, **wound**, or **scratch** on one scale, with a hardening move for each, and says which side is more survivable.
4. **Deliver the trouble (you, not an agent).** Show the 1–3 best mined ideas with the provocations they came from, lay the two pre-mortems side by side, and give a verdict — switch, hybrid, or stay — with the hardening moves that make it survivable.

**Why this shape:** one agent asked to "be provocative" either judges its provocations before speaking them or produces absurdities and stops there. Separating generation from movement protects provocations long enough to move; separating movement from attack lets the miner be generous and the red-teamer ruthless. And a red team that only attacks the new idea is a bodyguard for the status quo — attacking both sides is what makes the trouble worth listening to.

## Output

```markdown
## The Troublemaker's report
**Challenge:** <one sentence>

**Provocations that moved:** <3–5 lines, each "Po: <provocation> (<technique>) → <the idea it became>">

**Ideas worth the trouble:**
1. **<idea>** — from <provocation>. The move: <who does what, differently>. Why it matters: <payoff>.
2. …

**Pre-mortem, both sides** (18 months on, it failed — why?):
| Severity | Strongest idea: <name> | Status quo: <plan> |
|----------|------------------------|--------------------|
| Kill | <failure → hardening move, or "none"> | <failure → hardening move, or "none"> |
| Wound | … | … |
| Scratch | … | … |

**Verdict:** <switch / hybrid / stay — and the hardening moves that make it survivable>

**First piece of trouble:** <the cheapest test of the biggest kill risk, startable this week>

## Handoff
- <3–7 bullets: the strongest idea and its origin, kill risks on each side with hardening moves, the verdict, and anything a next role must respect>
```

## Gotchas

- **A provocation is not a proposal.** "Po: the restaurant pays the customer" isn't advice — it's a place to move from. Don't trim the provocateur's list before the miner sees it, and don't show raw provocations to the user as ideas; judging at the provocation stage kills exactly the ones that would have moved furthest.
- **The status quo gets attacked too.** If the user names no plan, write down "keep doing what we do today" and pass it in CONTEXT anyway. Without the second pre-mortem, troublemaking turns into an elaborate list of reasons never to change — and quiet failures like erosion and opportunity cost never get priced.
- **Severity has to be earned, on one scale.** A kill ends the plan even with competent execution; most failures are wounds. If one side collects all the kills and the other all the scratches, the red-teamer graded preferences rather than failures — rerun it.
- **Agent types load at session start.** If `think-troublemaker-*` isn't an available `subagent_type` (for example the files were added mid-session), read `.claude/agents/<agent-name>.md`, strip the frontmatter, and pass the body as the prompt to a `general-purpose` agent with the brief appended — the mechanics stay identical.

## Going deeper

- **`evals/evals.json` + `evals/trigger-eval.json`** — the output-quality and description-trigger evals; drive them with `/meta-skill-creator-local` when tuning this skill or its description.
