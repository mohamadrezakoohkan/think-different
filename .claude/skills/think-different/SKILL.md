---
name: think-different
description: Run a Think Different session on any problem, product, strategy, or decision by convening the crazy ones — eleven role skills such as the Misfit, Rebel, and Round Peg, each running its own agents — choosing the right arc of roles, carrying one shared brief between them, and synthesizing the single unconventional idea worth pursuing. Use this whenever the user asks to think differently, think outside the box, get unconventional or crazy ideas, break out of conventional thinking, run an innovation or creative session, find a breakthrough, rethink something end to end, or says "think different", "here's to the crazy ones", or "which lens should I use?". Reach for it whenever the user wants a genuinely fresh take but hasn't named one specific lens, even if they only say "help me rethink this". Not for a single named lens (invoke that think-* role directly, e.g. think-rebel or think-misfit), and not for routine planning, factual questions, or ordinary code changes.
---

# Think Different

*Here's to the crazy ones.*

Thinking differently isn't one move — it's a cast. Each crazy one sees a problem through a different lens: the Misfit borrows from elsewhere, the Rebel breaks inherited rules, the Round Peg questions the hole itself. This skill is the toolmaker: it doesn't generate ideas itself. It chooses which roles to convene and in what order, carries the brief between them, and protects the most different idea from being sanded down at the end. Every role is a skill; every step inside a role is an agent.

## The cast

| Role skill | Manifesto line | What it does | Reach for it when… |
|---|---|---|---|
| `think-round-peg` | the round pegs | Reframes the problem itself | It might be the wrong problem; fixes keep not sticking |
| `think-seer` | sees things differently | Finds anomalies, absences, weak signals | There's data but no insight; something feels off |
| `think-rebel` | no respect for the status quo | Breaks dead inherited rules | Boxed in by "how it's done" |
| `think-misfit` | the misfits | Transplants mechanisms from distant domains | Everyone in the field proposes the same thing |
| `think-troublemaker` | the troublemakers | Provokes, then red-teams | The team agreed too fast; the plan feels safe |
| `think-explorer` | they explore | Maps the space, finds white space | Nobody knows what else is out there |
| `think-inventor` | they invent | Invents new mechanisms | A technical trade-off blocks every option |
| `think-imaginer` | they imagine | Paints a future and backcasts | Stuck in incrementalism; needs a moonshot |
| `think-healer` | they heal | Pain → root cause → humane remedy | People are hurting: complaints, churn, burnout |
| `think-creator` | they create | Converges and prototypes one idea | Too many ideas, nothing real |
| `think-inspirer` | they inspire | Distils the truth and tells the story | The idea exists but nobody cares yet |

## The procedure

1. **Build the brief.** Every role consumes the same three parts:
   - **CHALLENGE** — the problem or goal in one sentence, in the user's words.
   - **CONTEXT** — facts, constraints, audience, and any files or paths worth reading.
   - **PRIOR** — starts empty; accumulates each role's `## Handoff` block.

   Ask one question only if the challenge itself is unclear — every role can work around thin context, none can recover a missing problem.

2. **Choose the arc.** Default to the **short arc**: `think-round-peg` → *one breaker* → `think-creator`, picking the breaker from the "Reach for it when…" column that best matches the user's situation. Use a preset instead when the situation clearly calls for it, and go to the full arc only when the user asks for a deep session:

   | Arc | Roles, in order | Use when |
   |---|---|---|
   | Short (default) | Round Peg → *breaker* → Creator | Most requests |
   | Breakthrough | Round Peg → Rebel → Misfit → Troublemaker → Creator | Mature field, everyone stuck in the same groove |
   | Moonshot | Imaginer → Rebel → Inventor → Creator → Inspirer | The ask is 10x, not 10% |
   | Human | Healer → Seer → Round Peg → Inventor → Creator | The problem is people suffering |
   | Strategy | Seer → Explorer → Misfit → Troublemaker → Creator | Choosing where to play |
   | Full | Round Peg, Seer → Rebel, Misfit, Troublemaker → Explorer, Inventor, Imaginer, Healer → Creator, Inspirer | The user explicitly asks for everything |

   State the arc and why in one line before starting, so the user can redirect cheaply.

3. **Run each role in turn.** Invoke it with the Skill tool, passing the brief with PRIOR holding every earlier role's `## Handoff` block — the handoffs only, not the full outputs. After each role, print a 2–3 line checkpoint (what it found, what it hands on) and keep going. Pause for the user only when a role's output forks the direction in a way the brief can't settle.

4. **Synthesize (you, not a role).** Pick the one idea with the most distance from the conventional answer that still survives the evidence, and present it in the output shape below. Put runner-ups and the safe option in their own lines rather than blending them into the winner.

**Why this shape:** each role is narrow on purpose, so the arc is where breadth comes from — and a short arc of three roles that hand off cleanly beats eleven roles that each skim. Starting with the Round Peg in most arcs is deliberate: a brilliant answer to the wrong question is the most expensive failure, and it's cheap to check first. Ending with the Creator forces the session to produce something tangible instead of a pile of possibilities.

## Output

```markdown
# Think Different: <challenge in a few words>
**Arc:** <role → role → role> — <one line on why this arc>

**The different idea:** <one paragraph — concrete enough to act on>
**What it breaks:** <the convention or assumption it defies, and why that's OK here>
**Why it might work:** <the mechanism or evidence, traced to which role surfaced it>
**What would kill it:** <the top risk, and the cheapest way to test it>
**First move (this week):** <the smallest action that starts it>

**Also surfaced:** <2–3 runner-up ideas, one line each, with the role that produced each>
**The safe option, for contrast:** <the conventional answer, one line>
```

## Gotchas

- **More roles is not more different.** Running all eleven by default produces an averaged, exhausted output and ~33 agent runs. Each role should be in the arc because the situation calls for it — default to the short arc and earn every addition.
- **Pass handoffs, not transcripts.** PRIOR carries each role's `## Handoff` block only. Full outputs bloat context and anchor later roles on earlier phrasing, so every role converges on the first role's idea.
- **Synthesis drifts back to safe.** At the end, the conventional answer looks reassuringly reasonable next to the crazy ones, and blending them produces a compromise nobody would fight for. Keep the different idea whole, and show the safe option separately so the contrast is the user's choice to make.
- **Don't run a role's agents yourself.** Invoke the role skill and let it spawn its own agents — the role skill knows its step order, parallelism, and what each agent needs. Calling the agents directly skips the role's synthesis step.
- **Agent types load at session start.** If a role's `think-*` agents aren't available as `subagent_type`s (for example the files were added mid-session), the role skill falls back to reading `.claude/agents/<agent-name>.md` and running it through a `general-purpose` agent — let it; the arc doesn't change.

## Going deeper

- **`evals/evals.json` + `evals/trigger-eval.json`** — the output-quality and description-trigger evals; drive them with `/meta-skill-creator-local` when tuning this skill or its description.
