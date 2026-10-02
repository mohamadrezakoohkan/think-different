<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img alt="think different — a toolkit for the crazy ones" src="assets/logo.svg" width="520">
  </picture>
</p>

<p align="center"><strong>The misfits, rebels, and troublemakers — as a team you can call on from Claude Code.</strong></p>

---

**Think Different** gives a problem to the people who see things differently. Each of the "crazy ones" is a **role**: a Claude Code skill with its own way of seeing. The Rebel breaks inherited rules, the Misfit steals mechanisms from distant fields, and the Round Peg asks whether the hole is the wrong shape. Every step inside a role is a dedicated **agent** that does exactly one thing, so no single pass collapses into the obvious answer.

Point it at a product, a process, a strategy, or a plan. It convenes the right roles, passes the brief between them, and hands back **one unconventional idea worth pursuing**, along with what it breaks, what could kill it, and the first move to test it this week.

> The round peg is the logo for a reason: when the peg won't fit, question the hole.

## The cast

| Role | Skill | What it does |
|---|---|---|
| The Round Peg | `think-round-peg` | Reframes the problem itself |
| The Seer | `think-seer` | Finds anomalies, absences, and weak signals |
| The Rebel | `think-rebel` | Puts inherited rules on trial and breaks the dead ones |
| The Misfit | `think-misfit` | Transplants mechanisms from distant domains |
| The Troublemaker | `think-troublemaker` | Provokes, then pre-mortems both the new idea and the status quo |
| The Explorer | `think-explorer` | Maps the solution space and plans cheap probes into the white space |
| The Inventor | `think-inventor` | Invents mechanisms that escape trade-offs |
| The Imaginer | `think-imaginer` | Paints the future, then works backward to today |
| The Healer | `think-healer` | Traces human pain to its root cause and designs a remedy that does no harm |
| The Creator | `think-creator` | Picks one idea, prototypes it, and edits it to its essence |
| The Inspirer | `think-inspirer` | Finds the belief underneath and tells it as a story |
| **The orchestrator** | `think-different` | Picks the right roles, runs them in order, and synthesizes the result |

## Run it

**You need** [Claude Code](https://claude.com/claude-code) (CLI, desktop app, or IDE extension).

### In this repo

Clone it and open Claude Code inside the folder. The skills and agents in `.claude/` load automatically.

```bash
git clone https://github.com/mohamadrezakoohkan/think-different.git
```

```bash
cd think-different && claude
```

### In every project

Copy the skills and agents into your user-level Claude Code folders:

```bash
mkdir -p ~/.claude/skills ~/.claude/agents
```

```bash
cp -R .claude/skills/think-* ~/.claude/skills/
```

```bash
cp .claude/agents/think-*.md ~/.claude/agents/
```

### Ask

Describe the problem in plain language, or call a skill by name:

| You say | What runs |
|---|---|
| `Think different about our onboarding — every proposal is "send more emails".` | `think-different` picks an arc of roles |
| `/think-different the moonshot arc on insulin pens` | a preset arc (short, breakthrough, moonshot, human, strategy, full) |
| `Which of our pricing assumptions are actually real?` | `think-rebel` |
| `How would someone outside our industry solve warehouse routing?` | `think-misfit` |
| `Poke holes in this launch plan.` | `think-troublemaker` |
| `/think-creator pick one of these five ideas and make it real` | `think-creator` |
| `Use the think-rebel-rule-excavator agent on our hiring process.` | one agent, standalone |

**Get better results** by giving context:
- Paste or point to files (agents can read your repo).
- Say what decision this feeds.
- Name the current plan, which the Troublemaker treats as the status quo to attack.
- For the Inspirer, name the format you want (pitch, memo, manifesto).

## What to expect

### A full session

1. **The arc, up front.** For example: *"Round Peg → Misfit → Creator — everyone in your field proposes the same fix."* Redirect it here if it's wrong.
2. **A checkpoint after each role.** You get two or three lines on what that role found and what it passes on.
3. **One synthesis at the end:**

```markdown
# Think Different: <your challenge>
**Arc:** Round Peg → Misfit → Creator — <why this arc>

**The different idea:** <concrete enough to act on>
**What it breaks:** <the convention it defies, and why that's OK>
**Why it might work:** <the mechanism, traced to the role that found it>
**What would kill it:** <the top risk, and the cheapest test>
**First move (this week):** <the smallest action that starts it>

**Also surfaced:** <runner-ups, with the role that produced each>
**The safe option, for contrast:** <the conventional answer, kept separate>
```

### A single role

Each role ends with its own deliverable, followed by a `## Handoff` block that another role can pick up:

| Role | You get |
|---|---|
| Round Peg | A new problem statement, a wildcard framing, and what the original frame hid |
| Seer | 1–3 insights, each an observation that would change the decision |
| Rebel | The rules that hold, the rules to break, and a first act of rebellion |
| Misfit | Ranked transplants from distant domains and a first graft |
| Troublemaker | Mined ideas, side-by-side pre-mortems, and a switch / hybrid / stay verdict |
| Explorer | A map of where everyone clusters, the open white space, and the cheapest probe |
| Inventor | Up to three how-it-works mechanisms, each with a test that could kill it |
| Imaginer | A vision, a dated path back to today, and which "impossibles" are only unprecedented |
| Healer | A prescription aimed at the root cause, with a do-no-harm check and a first dose |
| Creator | One chosen idea, a prototype edited to its essence, and the kill list |
| Inspirer | The finished piece, the belief underneath it, and an honest read on how it will land |

### Good to know

- **Depth costs runs.** Each role runs three agents (the Inspirer up to four), some of them in parallel. The default short arc is about nine agent runs; the full arc is about 33. Ask for "the full treatment" when the stakes justify it.
- **Your project files are never edited.** Agents only read files and search the web. The Creator returns its prototype inline and writes a file only when you ask for one.
- **It asks at most one question,** and only when the problem itself is unclear. Thin context is fine.
- **Hard limits stay intact.** Law, safety, and ethics are treated as load-bearing and are never "broken".
- **Research roles use the web when it's available.** The Seer, Explorer, and Misfit agents, among others, search the web; without access they work only from the context you give them.

## Contributing

After editing anything in `.claude/`, run the validator. It checks naming, structure, and evals, and confirms that the wiring graph in [`CLAUDE.md`](CLAUDE.md) still matches the files:

```bash
python3 scripts/validate.py --root .
```

---

<sub>Inspired by the 1997 "Think Different" campaign and its tribute to the crazy ones. An independent project, not affiliated with or endorsed by Apple Inc.</sub>
