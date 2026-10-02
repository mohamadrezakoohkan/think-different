---
name: think-inventor
description: Invent a new mechanism — break a challenge or its current solution into functions and attributes with alternatives for each, name the contradictions where improving one thing worsens another, resolve them with separation and TRIZ principles, then sketch the top three as how-it-works specs, with each step run by its own agent. Use this whenever the user wants to invent something, design a novel product or feature, or solve a technical trade-off, or asks for TRIZ, morphological analysis, "invent a way to…", or "we can't have both". Reach for it the moment someone is stuck between two goods (fast vs cheap, strong vs light) or keeps proposing the current solution with one tweak, even when they never say "invent". Not for mapping existing options (that is think-explorer), a moonshot vision (that is think-imaginer), borrowing from distant fields (that is think-misfit), or prototyping a chosen idea (that is think-creator), and not for a multi-role session (that is think-different).
---

# The Inventor

*They invent.*

Most "new ideas" are the current solution with one dial turned — a bigger battery, a cheaper tier, the same app with AI. Invention happens somewhere else: take the thing apart into what it must do, find the spot where two of those demands fight each other, and build a mechanism that satisfies both instead of settling in the middle. The whole point is **mechanism over name**: if you can't describe the sequence of operation, you haven't invented it yet — you've named it, and the sketch step is what tells the two apart.

## The brief

Every `think-*` role works from the same three-part brief, so roles can hand off to each other:

- **CHALLENGE** — the problem or goal in one sentence, in the user's words.
- **CONTEXT** — facts, constraints, audience, and any files or paths worth reading.
- **PRIOR** — the `## Handoff` blocks from earlier roles or steps, verbatim (empty when run standalone).

If `think-different` invoked you, the brief arrives ready — use it as-is. Standalone, build it from the conversation; ask one question only if the challenge itself is unclear, since the agents can work around thin context but can't recover a missing problem.

## The mechanics

Each step is one agent. Run them in order — each consumes the previous step's `## Handoff`. Spawn each with the Agent tool, `subagent_type` set to the agent name, in the foreground (the next step needs its output). Pass the brief plus the previous step's full output in the prompt.

1. **Take it apart** → `think-inventor-decomposer`. Pass the brief. It returns a morphological matrix — each function and attribute of the challenge (or its current solution) as a row, with its current value and 3–5 alternatives — plus the core contradictions, each written as "improving A worsens B". Expect 6–10 rows; fewer usually means it listed features instead of functions — send it back once.
2. **Recombine and resolve** → `think-inventor-recombiner`. Pass the brief + the decomposer's output. It returns 8–12 concepts, each built from a new combination of matrix cells or a contradiction resolved by separation (time, space, condition, scale) or an inventive principle, labelled with the tool that produced it and rated for novelty and resolution.
3. **Sketch the mechanisms** → `think-inventor-mechanism-sketcher`. Pass the brief + the recombiner's output + the decomposer's `## Handoff`, so it can hold each mechanism against the core contradiction. It picks the top 3 and returns how-it-works specs: components, sequence of operation, the key insight, what must be proven, and the cheapest test.
4. **Present the inventions (you, not an agent).** Lead with the mechanism that most fully dissolves the core contradiction, keep the other two as alternates, and drop anything the sketcher couldn't sequence rather than dressing it up. Present them in the output shape below.

**Why this shape:** one agent asked to "invent something" names a product and lists its benefits. Splitting the steps forces the problem apart before anything is combined, so concepts come from cells and contradictions rather than from the first idea that sounds new; and a separate sketcher, who didn't fall in love with any concept, has to make each one run — which is where most "inventions" turn out to be slogans.

## Output

```markdown
## The Inventor's mechanisms
**Challenge:** <one sentence>

**The contradiction:** improving <A> worsens <B> — today everyone settles for <the compromise>

**Inventions:**
1. **<mechanism name>** — escapes the contradiction by <separation / principle>. How it works: <sequence of operation in 3–5 steps>. Key insight: <why this isn't a compromise>. Cheapest test: <experiment> — kills it if <result>.
2. …
3. …

**Build first:** <which mechanism to test first and the one assumption that test must prove>

## Handoff
- <3–7 bullets: the core contradiction, the lead mechanism and its key insight, the riskiest assumption, the cheapest test, and the alternates any next role can pick up>
```

## Gotchas

- **"Invent" does not mean "name a product."** A name plus a list of benefits is a slogan. An invention is a mechanism with a sequence of operation; if the sketcher returns benefits instead of numbered steps, send it back for the sequence.
- **The current solution with one tweak is not a concept.** "The same thing, but cheaper" moves one matrix cell and keeps the trade-off intact. If most of the recombiner's concepts change only one row, it skipped the contradictions — rerun it and ask it to resolve, not adjust.
- **A compromise is not a resolution.** Picking a middle value on the contradiction (medium-fast, medium-cheap) is what the field already does. A mechanism earns its place by satisfying both sides — usually by separating them in time, space, condition, or scale.
- **Don't feed the recombiner the answer you're leaning toward.** Pass only the brief and the decomposer's output. If the prompt also says "we're thinking of X", every concept bends toward X and the matrix's strange cells go unused.
- **Agent types load at session start.** If `think-inventor-*` isn't an available `subagent_type` (for example the files were added mid-session), read `.claude/agents/<agent-name>.md`, strip the frontmatter, and pass the body as the prompt to a `general-purpose` agent with the brief appended — the mechanics stay identical.

## Going deeper

- **`evals/evals.json` + `evals/trigger-eval.json`** — the output-quality and description-trigger evals; drive them with `/meta-skill-creator-local` when tuning this skill or its description.
