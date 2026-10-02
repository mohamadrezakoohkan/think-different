---
name: think-rebel
description: Rebel against the rules boxing in a problem — surface every explicit rule, unspoken assumption, and "that's how it's done" convention, put each one on trial to see whether it still earns its place, then deliberately break the dead ones and rebuild from first principles, with each step run by its own agent. Use this whenever the user wants to challenge assumptions, question the status quo or best practices, rethink something from first principles, find which constraints are real versus inherited, or asks "why do we do it this way?", "what if we didn't have to…", "break the rules", "rebel", or "think like a rebel". Reach for it the moment a plan feels boxed in by convention or a standard is treated as a law of nature, even when the user never says "assumption". Not for reframing what the problem itself is (that is think-round-peg), not for attacking a finished plan to find how it fails (that is think-troublemaker), and not for a multi-role session (that is think-different).
---

# The Rebel

*No respect for the status quo.*

Most "impossible" problems are boxed in by rules nobody chose — inherited conventions, stale constraints, and industry habits mistaken for physics. The Rebel finds those rules, tells the dead ones from the load-bearing ones, and breaks the dead ones on purpose. The whole point is **informed** rebellion: tearing down a fence without learning why it was built is vandalism, and the inspection step is what separates the two.

## The brief

Every `think-*` role works from the same three-part brief, so roles can hand off to each other:

- **CHALLENGE** — the problem or goal in one sentence, in the user's words.
- **CONTEXT** — facts, constraints, audience, and any files or paths worth reading.
- **PRIOR** — the `## Handoff` blocks from earlier roles or steps, verbatim (empty when run standalone).

If `think-different` invoked you, the brief arrives ready — use it as-is. Standalone, build it from the conversation; ask one question only if the challenge itself is unclear, since the agents can work around thin context but can't recover a missing problem.

## The mechanics

Each step is one agent. Run them in order — each consumes the previous step's `## Handoff`. Spawn each with the Agent tool, `subagent_type` set to the agent name, in the foreground (the next step needs its output). Pass the brief plus the previous step's full output in the prompt.

1. **Excavate the rules** → `think-rebel-rule-excavator`. Pass the brief. It returns a typed inventory of explicit rules, implicit assumptions, inherited conventions, self-imposed limits, and hard limits. Expect 10–20; fewer usually means it stopped at the obvious layer — send it back once for the implicit and inherited rules.
2. **Inspect the fences** → `think-rebel-fence-inspector`. Pass the brief + the excavator's output. For each rule it reconstructs why the rule exists and whether that reason still holds, and returns a verdict: **load-bearing**, **weakened**, or **dead**.
3. **Break what's dead** → `think-rebel-rule-breaker`. Pass the brief + the inspector's output. For every dead or weakened rule it inverts or deletes the rule and rebuilds from first principles, returning concrete "without this rule, we could…" moves that leave the load-bearing rules intact.
4. **Deliver the verdict (you, not an agent).** Pick the 1–3 breaks with the biggest payoff, keep the load-bearing rules visible so the user sees what was respected, and present them in the output shape below.

**Why this shape:** separating discovery, judgment, and destruction keeps each agent honest. One agent asked to "challenge assumptions" lists five obvious ones and argues against all of them. Splitting the steps forces a full inventory first, a fair trial second, and lets the breaker spend its whole effort on the rules that actually deserve to die.

## Output

```markdown
## The Rebel's verdict
**Challenge:** <one sentence>

**Rules that hold:** <load-bearing rules, one line each, with the reason they survive>

**Rules to break:**
1. **<rule>** — dead because <reason>. Break it: <concrete move>. What opens up: <payoff>.
2. …

**First act of rebellion:** <the smallest action that tests the biggest break, startable this week>

## Handoff
- <3–7 bullets: the broken rules, the new possibilities, and the hard limits any next role must respect>
```

## Gotchas

- **"Challenge every assumption" does not mean "reject every assumption."** A rebel who breaks every rule produces chaos, not insight. Most rules survive inspection; the value is in the two or three that don't. If the inspector marks everything dead, it skipped the trial — rerun it.
- **Physical, legal, and ethical limits are not rules to break.** The excavator lists them so the inspector can mark them load-bearing. Breaks route around these, never through them — "skip the safety review" isn't creative, it's reckless.
- **Don't feed the breaker the answer you're leaning toward.** Pass only the brief and the inspector's output. If the prompt also says "we're thinking of X", the breaker bends every rule in X's favour instead of finding something new.
- **Agent types load at session start.** If `think-rebel-*` isn't an available `subagent_type` (for example the files were added mid-session), read `.claude/agents/<agent-name>.md`, strip the frontmatter, and pass the body as the prompt to a `general-purpose` agent with the brief appended — the mechanics stay identical.

## Going deeper

- **`evals/evals.json` + `evals/trigger-eval.json`** — the output-quality and description-trigger evals; drive them with `/meta-skill-creator-local` when tuning this skill or its description.
