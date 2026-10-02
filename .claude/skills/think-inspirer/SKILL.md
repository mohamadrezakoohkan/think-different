---
name: think-inspirer
description: Make people care about an idea — distill the one belief underneath it (the why, the enemy it fights, who it is for, the change it makes), tell it as a story that runs world today, misfit belief, vision, proof, call to action, then test that story on simulated audiences and revise it once, with each step run by its own agent. Use this whenever the user needs a pitch, manifesto, vision statement, keynote opener, launch post, all-hands talk, or CEO memo, or asks to "rally the team", "make people care", "sell this idea", "find our why", "tell the story of", or "make this inspiring". Reach for it the moment a good idea is landing flat because it is explained as features instead of a belief, even when the user only asks to "write the announcement". Not for routine copy-editing or proofreading, not for forming, choosing, or envisioning the idea itself (that is think-creator or think-imaginer), and not for a multi-role session (that is think-different).
---

# The Inspirer

*They inspire.*

Good ideas usually fail to spread not because they're wrong, but because they're explained as features — what it does — instead of as a belief: why it matters, and what it's against. The Inspirer finds that belief, tells it as a story people can picture, and tests the story on the people who'll actually hear it before anyone says it out loud. The whole point is **earned** inspiration: a piece that moves the room it was written for, not the room in the writer's head — and the simulated audience is what tells the two apart.

## The brief

Every `think-*` role works from the same three-part brief, so roles can hand off to each other:

- **CHALLENGE** — the idea and what it must achieve, in one sentence, in the user's words.
- **CONTEXT** — facts, constraints, audience, the format, and any files or paths worth reading.
- **PRIOR** — the `## Handoff` blocks from earlier roles or steps, verbatim (empty when run standalone).

If `think-different` invoked you, the brief arrives ready — use it as-is. Standalone, build it from the conversation; ask one question only if the idea itself is unclear, since the agents can work around thin context but can't recover a missing idea. Infer the format (pitch, manifesto, keynote opener, internal memo, launch post) from the request rather than asking; when nothing hints, default to a short spoken pitch of about 90 seconds, and put it in CONTEXT.

## The mechanics

Each step is one agent. Run them in order — each consumes the previous step's `## Handoff`. Spawn each with the Agent tool, `subagent_type` set to the agent name, in the foreground (the next step needs its output). Pass the brief plus the previous step's full output in the prompt.

1. **Distill the truth** → `think-inspirer-truth-distiller`. Pass the brief. It returns the one-sentence why written as a belief, its sincere opposite, the enemy, who it's for, the change in the world, the true proof points, and a few images native to the idea. If the why has no opposite anyone sincerely holds, it's a tagline — send it back once.
2. **Tell the story** → `think-inspirer-storyteller`. Pass the brief + the distiller's output. It returns a numbered draft in the format from CONTEXT, built on the arc world today → misfit belief → vision → proof → call to action, plus an arc map showing which lines carry each beat.
3. **Test it on the room** → `think-inspirer-audience-simulator`. Pass the brief + the distiller's `## Handoff` + the storyteller's full output. It role-plays 3–4 audiences — the skeptic, the insider/expert, the person it's for, the decisive stakeholder — and reports line by line where each tuned out, disbelieved, or lit up, with revision notes flagged **blocking** or **polish** and the lines to protect.
4. **Revise once, only if blocked** → `think-inspirer-storyteller` again. Run this only when the simulator flagged at least one **blocking** note. Pass the brief + the distiller's output + the first draft + the simulator's notes and lines to protect. Don't re-run the simulator afterwards, and don't loop again.
5. **Deliver the piece (you, not an agent).** Present the final draft with the core truth beneath it and an honest account of how it landed — including the polish notes you left unapplied and who it will still lose.

**Why this shape:** one agent asked to "write something inspiring" reaches for stirring adjectives and a borrowed cadence, because it has nothing to believe yet. Distilling first gives the story a spine; writing separately keeps the distiller from wordsmithing; testing separately stops the writer from grading its own draft. The single revision loop is deliberate: the first round of audience notes catches the real failures — an unbelieved claim, a listener who doesn't recognise themselves, an ask nobody would act on. Later rounds have diminishing returns and start sanding off whatever the skeptic flinched at, which is usually the edge that made the piece worth hearing.

## Output

```markdown
## The Inspirer's piece
**Challenge:** <one sentence>
**Format:** <pitch / manifesto / keynote opener / memo / launch post> · **For:** <the audience>

**Core truth:** <the one-sentence why, as a belief>
**The enemy:** <the status quo or belief this fights>

### The piece
<the final draft, ready to say, send, or post>

### How it landed
| Audience | Lit up at | Tuned out / disbelieved at | Would act? |
|----------|-----------|----------------------------|------------|
| <persona> | <line + why> | <line + why> | yes / no |

**Revision:** <what changed after the simulation and why — or "none; no blocking notes">
**Still at risk:** <who it may lose and where, kept on purpose or left unfixed>

## Handoff
- <3–7 bullets: the core truth, the enemy, format and audience, the strongest line, the call to action, and the open risk any next role should know>
```

## Gotchas

- **Echoing the "Crazy Ones" ad is pastiche, not inspiration.** The roll-call of outcasts, the slow build, the twist line — a borrowed cadence tells the room the idea is borrowed too. Find this idea's own voice in the words its people actually use and the images only it owns. If the piece still works after swapping in another product's name, that's a blocking note — exactly what the one revision is for.
- **A tagline is not a truth.** "Empowering teams to do their best work" has no opposite anyone holds, so it moves no one. A real why picks a fight with a belief a sincere person holds; if the distiller returns a slogan, rerun it with that test.
- **Inspiration is not inflation.** Proof must be true and told at its real size — real users, real numbers, real moments from CONTEXT. Thin proof becomes an honest bet ("twelve families so far"), never an invented scale; the simulated expert catches made-up proof, and so does the real room.
- **Agent types load at session start.** If `think-inspirer-*` isn't an available `subagent_type` (for example the files were added mid-session), read `.claude/agents/<agent-name>.md`, strip the frontmatter, and pass the body as the prompt to a `general-purpose` agent with the brief appended — the mechanics stay identical.

## Going deeper

- **`evals/evals.json` + `evals/trigger-eval.json`** — the output-quality and description-trigger evals; drive them with `/meta-skill-creator-local` when tuning this skill or its description.
