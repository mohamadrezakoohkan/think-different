---
name: think-misfit
description: Look at a problem through an outsider's eyes — map how insiders frame and solve it, strip the challenge to its structural core and raid distant domains (nature, history, games, logistics, medicine) that already solved the same shape of problem, then transplant their mechanisms home and rank them by distance from orthodoxy times plausibility, with each step run by its own agent. Use this whenever the user wants analogies, cross-industry inspiration, biomimicry, fresh or outsider eyes, or asks "how would X solve this?", "what can we steal from other fields", "who else has solved this", or "think like a misfit". Reach for it the moment a team only benchmarks its competitors or every idea sounds like the field's own playbook, even when the user never says the word "analogy". Not for questioning rules and assumptions (that is think-rebel), not for reframing what the problem itself is (that is think-round-peg), and not for a multi-role session (that is think-different).
---

# The Misfit

*Here's to the crazy ones. The misfits.*

Insiders solve problems with the field's own toolbox, so they keep arriving at the same answers. The Misfit doesn't belong to the field, and that is the advantage: it asks who, far away, has already solved the same *shape* of problem — an ant colony, a pit crew, a medieval guild — and carries the mechanism home. The whole point is **transplanting mechanisms, not borrowing labels**: "be the Uber of X" copies a brand, while a misfit move copies how something actually works, and the consensus map is what proves the move is genuinely far from where insiders already look.

## The brief

Every `think-*` role works from the same three-part brief, so roles can hand off to each other:

- **CHALLENGE** — the problem or goal in one sentence, in the user's words.
- **CONTEXT** — facts, constraints, audience, and any files or paths worth reading.
- **PRIOR** — the `## Handoff` blocks from earlier roles or steps, verbatim (empty when run standalone).

If `think-different` invoked you, the brief arrives ready — use it as-is. Standalone, build it from the conversation; ask one question only if the challenge itself is unclear, since the agents can work around thin context but can't recover a missing problem.

## The mechanics

Each step is one agent, spawned with the Agent tool, `subagent_type` set to the agent name. Steps 1 and 2 are independent — spawn them **in parallel**: a single message with two Agent tool calls, both in the foreground, each given the brief. Step 3 waits for both and receives both full outputs in its prompt.

1. **Map the consensus** → `think-misfit-consensus-mapper`. Pass the brief. It returns the insider orthodoxy: the dominant frame, the canonical solutions (including what competitors and neighbouring industries do), the shared vocabulary, what the field treats as unthinkable, and its blind side. This map is the ruler step 3 measures distance with.
2. **Raid distant domains** → `think-misfit-domain-raider` (in parallel with step 1). Pass the brief only. It strips the challenge to a structural core with the domain nouns removed, raids 4–6 distant domains that solved that structure, and extracts each one's mechanism. If most raids come from one family or from an industry next door, send it back once for farther domains.
3. **Transplant and rank** → `think-misfit-transplanter`. Pass the brief + the consensus mapper's and the domain raider's full outputs. It translates each mechanism concretely into the home domain, names the tissue rejection (what must adapt for it to take), and ranks transplants by distance-from-orthodoxy × plausibility.
4. **Deliver the find (you, not an agent).** Pick the 1–3 transplants with the best combined score, show the orthodoxy each one departs from, and present them in the output shape below.

**Why this shape:** one agent asked for "analogies" names the nearest competitor or a famous company and stops. Mapping the consensus separately gives the transplanter a ruler, so "distance" means distance from what insiders actually do rather than from what feels novel. Running the raider in parallel keeps it blind to the field's vocabulary — searching in the field's own words only leads back to the field. And a separate transplanter can be strict about whether a mechanism survives the move instead of falling for the story that found it.

## Output

```markdown
## The Misfit's find
**Challenge:** <one sentence>
**Structural core:** <the challenge with domain nouns stripped — the shape being solved>

**The orthodoxy:** <how insiders frame and solve it, 2–3 lines, plus what they treat as unthinkable>

**Transplants:**
1. **<mechanism> from <distant domain>** — how it works there: <one line>. At home: <concrete change — who does what differently>. Tissue rejection: <what must adapt>. Distance: high / med / low · Plausibility: high / med / low.
2. …

**First graft:** <the smallest experiment that tests the top transplant, startable this week>

## Handoff
- <3–7 bullets: the top transplants, the orthodoxy each departs from, the adaptations they need, and any constraint a next role must respect>
```

## Gotchas

- **"Be the Uber of X" is a label, not a mechanism.** Surface analogies copy a business's name or category; a transplant needs the moving parts — who does what, triggered by what, and why it produces the result. A label carries no instructions, so it can't be adapted or tested; if a raid can't say how the thing works causally, discard it.
- **A neighbour is not a misfit.** Borrowing from a direct competitor or an adjacent industry is benchmarking, and the consensus map already contains it. If a raided domain shares the challenge's vocabulary, customers, or competitors, it's too close — that's why the raider strips the nouns before it searches.
- **Don't feed the raider your favourite analogy or the consensus map.** Pass only the brief. A prompt that says "we were thinking of airline yield management" anchors every raid to it, and the field's vocabulary steers searches back home — this is why steps 1 and 2 run in parallel rather than in sequence.
- **Distance without plausibility is a party trick.** The most exotic transplant is rarely the best; the ranking multiplies the two, so a moderately distant graft that will take beats a wild one that won't. If every top pick is low plausibility, the transplanter skipped the tissue-rejection check — rerun it.
- **Agent types load at session start.** If `think-misfit-*` isn't an available `subagent_type` (for example the files were added mid-session), read `.claude/agents/<agent-name>.md`, strip the frontmatter, and pass the body as the prompt to a `general-purpose` agent with the brief appended — the mechanics, including the parallel first two steps, stay identical.

## Going deeper

- **`evals/evals.json` + `evals/trigger-eval.json`** — the output-quality and description-trigger evals; drive them with `/meta-skill-creator-local` when tuning this skill or its description.
