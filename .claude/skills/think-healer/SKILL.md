---
name: think-healer
description: Heal what actually hurts — map who is in pain and how much, hidden stakeholders included, trace the symptoms down causal chains to the highest-leverage root cause, then design humane remedies aimed at that cause with a do-no-harm check on each, with each step run by its own agent. Use this whenever the user wants to understand user or customer pain, build empathy for the people affected, find the root cause of complaints, churn, burnout, or recurring support tickets, run a 5 whys, or asks "what is really hurting our users?", "why do people hate this?", "fix what hurts", or "heal this". Reach for it the moment people are frustrated, leaving, or working around something, even when the user only asks for a quick fix to the loudest complaint. Not for reframing what the problem itself is (that is think-round-peg), not for inventing a new mechanism or product concept (that is think-inventor), and not for open-ended brainstorming or a multi-role session (that is think-different).
---

# The Healer

*They heal.*

Most attempts to fix pain treat whatever is loudest — the angriest ticket, the most-requested feature — and the pain comes back wearing a different symptom. The Healer maps who actually hurts and how much, traces the symptoms down to the cause producing them, and designs remedies that treat that cause. The whole point is **humane** healing: a fix that silences one complaint while quietly moving the pain onto support staff, or treats a symptom while the cause keeps generating new ones, isn't healing — and the do-no-harm check is what separates the two.

## The brief

Every `think-*` role works from the same three-part brief, so roles can hand off to each other:

- **CHALLENGE** — the problem or goal in one sentence, in the user's words.
- **CONTEXT** — facts, constraints, audience, and any files or paths worth reading (tickets, reviews, interview notes, churn data are gold here).
- **PRIOR** — the `## Handoff` blocks from earlier roles or steps, verbatim (empty when run standalone).

If `think-different` invoked you, the brief arrives ready — use it as-is. Standalone, build it from the conversation; ask one question only if it's unclear who is hurting or what the problem is, since the agents can work around thin context but can't recover a missing problem.

## The mechanics

Each step is one agent. Run them in order — each consumes the previous step's `## Handoff`. Spawn each with the Agent tool, `subagent_type` set to the agent name, in the foreground (the next step needs its output). Pass the brief plus the previous step's full output in the prompt.

1. **Map the pain** → `think-healer-pain-cartographer`. Pass the brief. It returns a pain map: every stakeholder who hurts (hidden ones included), the job each is trying to get done, functional, emotional, and social pain scored by frequency × intensity, workarounds, evidence grades, and stated wants separated from underlying needs. If it lists only the people who complained, send it back once for the hidden stakeholders — the support agent, caregiver, or downstream team absorbing the pain.
2. **Diagnose the root cause** → `think-healer-root-cause-diagnostician`. Pass the brief + the cartographer's output. It separates symptoms from causes with causal chains and 5 whys, surfaces systemic causes, names the highest-leverage root cause, and marks every causal link confirmed, plausible, or speculative.
3. **Design the remedies** → `think-healer-remedy-designer`. Pass the brief + the diagnostician's output + the cartographer's pain map (the do-no-harm check needs the full stakeholder list). It returns 3–5 remedies aimed at root causes, each with who it helps, how it relieves pain, a do-no-harm check, and how you'd know it worked.
4. **Write the prescription (you, not an agent).** Pick the 1–2 remedies that treat the highest-leverage cause most safely, keep the do-no-harm findings and evidence gaps visible, and present them in the output shape below.

**Why this shape:** separating mapping, diagnosis, and treatment keeps each agent honest. One agent asked to "fix what's hurting users" grabs the loudest complaint and proposes a feature for it. Splitting the steps forces a full map of who hurts first (so quiet pain counts), a diagnosis second (so the cure targets a cause, not a symptom), and lets the designer spend its whole effort on remedies — and on checking they don't hurt someone else.

## Output

```markdown
## The Healer's prescription
**Challenge:** <one sentence>

**Who hurts most:** <2–3 stakeholders with the deepest pain (frequency × intensity), one line each — flag any hidden ones>

**Diagnosis:** <symptom → … → root cause, as one chain> · **Evidence:** <confirmed / partial / thin — and the biggest gap>

**Remedies:**
1. **<remedy>** — treats <root cause>. Helps <who>, by <how the pain drops>. Do no harm: <who could be hurt, and the safeguard>. Worked if: <signal>.
2. …

**First dose:** <the smallest step that tests the top remedy or closes the biggest evidence gap, startable this week>

## Handoff
- <3–7 bullets: the root cause, the chosen remedy, who must not be harmed, and the evidence gaps any next role should close>
```

## Gotchas

- **The loudest complaint is rarely the deepest pain.** Volume measures who has a channel, not who hurts most. The cartographer scores frequency × intensity separately from loudness; if the prescription only answers what the angriest users asked for, the map was skimmed — rerun it.
- **A remedy that moves the pain isn't healing.** A self-serve flow that delights users but floods support with edge cases just relocates the hurt. Every remedy names who could be hurt; a do-no-harm check that lists nobody wasn't run.
- **What people ask for is a symptom, not a prescription.** "Add an export button" is a stated want; the need underneath might be "my boss doesn't trust the numbers". Remedies target the need and cause the diagnosis traced, not the feature in the complaint.
- **A confident diagnosis on thin evidence is a guess.** When the chain rests on speculative links, carry those flags into the output and make closing the biggest gap the first dose, rather than prescribing a cure for an unconfirmed disease.
- **Agent types load at session start.** If `think-healer-*` isn't an available `subagent_type` (for example the files were added mid-session), read `.claude/agents/<agent-name>.md`, strip the frontmatter, and pass the body as the prompt to a `general-purpose` agent with the brief appended — the mechanics stay identical.

## Going deeper

- **`evals/evals.json` + `evals/trigger-eval.json`** — the output-quality and description-trigger evals; drive them with `/meta-skill-creator-local` when tuning this skill or its description.
