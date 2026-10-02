"""Validate the Think Different skills and agents against the house conventions
and against the machine-readable graph in CLAUDE.md.

Dependency-free: Python standard library only. Every check is path/regex/JSON based.

Usage:
    python3 scripts/validate.py --root .
    python3 scripts/validate.py --root . --quiet     # violations only

Exit codes: 0 clean, 1 violations, 2 usage error (missing dirs, unparseable graph).

Checks:
    skill-*   SKILL.md frontmatter (name, description), name == dir, single-line
              description of 700-1024 chars, section order, Handoff, fallback gotcha
    agent-*   agent frontmatter (name, description, tools), name == filename,
              description <= 500 chars starting "Step <n> of the <role> skill.",
              allowed tools, section order, Handoff in Output Format
    evals-*   evals.json skill_name == name, eval keys; trigger-eval.json balance
    graph-*   graph roles == skill dirs, graph agents == agent files == agents named
              in each SKILL.md, step numbers match descriptions, web flag matches
              tools, par groups have >= 2 members, arcs/feeds/defer name real skills
"""
import argparse
import json
import re
import sys
from pathlib import Path

ORCHESTRATOR = "think-different"
ALLOWED_TOOLS = {"Read", "Grep", "Glob", "WebSearch", "WebFetch"}
BASE_TOOLS = {"Read", "Grep", "Glob"}
ROLE_SECTIONS = ["## The brief", "## The mechanics", "## Output", "## Gotchas", "## Going deeper"]
AGENT_SECTIONS = ["## Role", "## Inputs", "## Process", "## Output Format", "## Guidelines"]


def build_parser():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--root", required=True, help="repository root")
    p.add_argument("--quiet", action="store_true", help="print violations only")
    return p


def parse_frontmatter(text):
    """Return (keys, values, body) or (None, reason, None)."""
    if not text.startswith("---\n"):
        return None, "no leading ---", None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, "unterminated frontmatter", None
    keys, values = [], {}
    for line in text[4:end].split("\n"):
        m = re.match(r"^([a-z_]+):\s?(.*)$", line)
        if not m:
            return None, f"non key-value line (multi-line value?): {line[:40]!r}", None
        keys.append(m.group(1))
        values[m.group(1)] = m.group(2)
    return keys, values, text[end + 5:]


def check_order(body, sections, label, errs):
    pos = -1
    for s in sections:
        i = body.find("\n" + s)
        if i == -1:
            errs.append(f"{label}: missing section '{s}'")
        elif i < pos:
            errs.append(f"{label}: section '{s}' out of order")
        else:
            pos = i


def load_graph(root):
    text = (root / "CLAUDE.md").read_text()
    m = re.search(r"<!-- graph:begin -->\s*```json\n(.*?)\n```\s*<!-- graph:end -->", text, re.S)
    if not m:
        raise ValueError("graph block not found between <!-- graph:begin/end --> markers")
    return json.loads(m.group(1))


def check_evals(skill_dir, name, errs):
    try:
        data = json.loads((skill_dir / "evals" / "evals.json").read_text())
        if data.get("skill_name") != name:
            errs.append(f"evals-name {name}: skill_name mismatch")
        evals = data.get("evals", [])
        if len(evals) < 2:
            errs.append(f"evals-count {name}: fewer than 2 evals")
        for e in evals:
            missing = {"id", "prompt", "expected_output", "files", "expectations"} - set(e)
            if missing:
                errs.append(f"evals-keys {name}: eval {e.get('id')} missing {sorted(missing)}")
    except (OSError, ValueError) as exc:
        errs.append(f"evals-json {name}: {exc}")
    try:
        arr = json.loads((skill_dir / "evals" / "trigger-eval.json").read_text())
        pos = sum(1 for q in arr if q.get("should_trigger") is True)
        neg = sum(1 for q in arr if q.get("should_trigger") is False)
        if pos < 12 or neg < 4:
            errs.append(f"evals-trigger {name}: {pos} true / {neg} false")
        return pos, neg
    except (OSError, ValueError) as exc:
        errs.append(f"evals-trigger {name}: {exc}")
        return 0, 0


def check_skills(skills_dir, role_names, errs, report):
    """Validate every skill; return {skill: set(agent names referenced in its body)}."""
    referenced = {}
    for name in role_names + [ORCHESTRATOR]:
        d = skills_dir / name
        f = d / "SKILL.md"
        if not f.exists():
            errs.append(f"skill-missing {name}: SKILL.md not found")
            continue
        text = f.read_text()
        keys, values, body = parse_frontmatter(text)
        if keys is None:
            errs.append(f"skill-frontmatter {name}: {values}")
            continue
        if keys != ["name", "description"]:
            errs.append(f"skill-frontmatter {name}: keys {keys}")
        if values.get("name") != d.name:
            errs.append(f"skill-name {name}: name != directory")
        dlen = len(values.get("description", ""))
        if not 700 <= dlen <= 1024:
            errs.append(f"skill-description {name}: length {dlen} (want 700-1024)")
        if not body.lstrip().startswith("# "):
            errs.append(f"skill-sections {name}: body does not start with an H1")
        if name != ORCHESTRATOR:
            check_order(body, ROLE_SECTIONS, f"skill-sections {name}", errs)
            if "## Handoff" not in body:
                errs.append(f"skill-handoff {name}: output template lacks ## Handoff")
            if "general-purpose" not in body:
                errs.append(f"skill-fallback {name}: missing agent-fallback gotcha")
        referenced[name] = set(re.findall(rf"`({re.escape(name)}-[a-z-]+)`", body))
        pos, neg = check_evals(d, name, errs)
        report.append(f"{name:22} desc={dlen:4}  lines={len(text.splitlines()):3}  triggers={pos}+/{neg}-")
    return referenced


def check_agents(agents_dir, errs, report):
    """Validate every agent file; return {agent: (description, tools)}."""
    agents = {}
    for path in sorted(agents_dir.glob("*.md")):
        stem = path.stem
        text = path.read_text()
        keys, values, body = parse_frontmatter(text)
        if keys is None:
            errs.append(f"agent-frontmatter {stem}: {values}")
            continue
        if keys != ["name", "description", "tools"]:
            errs.append(f"agent-frontmatter {stem}: keys {keys}")
        if values.get("name") != stem:
            errs.append(f"agent-name {stem}: name != filename")
        desc = values.get("description", "")
        if not 200 <= len(desc) <= 500:
            errs.append(f"agent-description {stem}: length {len(desc)} (want 200-500)")
        tools = {t.strip() for t in values.get("tools", "").split(",") if t.strip()}
        if not tools <= ALLOWED_TOOLS or not BASE_TOOLS <= tools:
            errs.append(f"agent-tools {stem}: {sorted(tools)}")
        if not re.search(r"^# .+ Agent$", body, re.M):
            errs.append(f"agent-sections {stem}: missing '# ... Agent' H1")
        check_order(body, AGENT_SECTIONS, f"agent-sections {stem}", errs)
        if "## Handoff" not in body.split("## Output Format", 1)[-1]:
            errs.append(f"agent-handoff {stem}: Output Format lacks ## Handoff")
        agents[stem] = (desc, tools)
        report.append(f"  {stem:44} desc={len(desc):3}  tools={','.join(sorted(tools))}")
    return agents


def check_graph(graph, referenced, agents, errs):
    roles = graph.get("roles", {})
    all_skills = set(roles) | {ORCHESTRATOR}
    graph_agents = set()
    for role, spec in roles.items():
        role_agents, groups = set(), {}
        for step in spec.get("steps", []):
            if step.get("by") == "main":
                continue
            a = step.get("agent")
            role_agents.add(a)
            if step.get("par"):
                groups.setdefault(step["par"], []).append(a)
            if a not in agents:
                errs.append(f"graph-agent {role}: {a} has no agent file")
                continue
            desc, tools = agents[a]
            first_n = min(s["n"] for s in spec["steps"] if s.get("agent") == a)
            if not re.match(rf"Step {first_n} of the {re.escape(role)} skill[.,]", desc):
                errs.append(f"graph-step {a}: description should start 'Step {first_n} of the {role} skill.'")
            if bool(step.get("web")) != ("WebSearch" in tools):
                errs.append(f"graph-web {a}: web flag {bool(step.get('web'))} != tools {sorted(tools)}")
        for gid, members in groups.items():
            if len(members) < 2:
                errs.append(f"graph-par {role}: group '{gid}' has a single member")
        if role in referenced and referenced[role] != role_agents:
            errs.append(f"graph-sync {role}: SKILL.md names {sorted(referenced[role] ^ role_agents)} differently from graph")
        for target in spec.get("feeds", []):
            if target not in all_skills:
                errs.append(f"graph-feeds {role}: unknown skill {target}")
        for target in spec.get("defer", {}).values():
            for t in target.split("|"):
                if t not in all_skills:
                    errs.append(f"graph-defer {role}: unknown skill {t}")
        graph_agents |= role_agents
    for stem in sorted(set(agents) - graph_agents):
        errs.append(f"graph-orphan {stem}: agent file not in graph")
    orch = graph.get("orchestrator", {})
    for arc, seq in orch.get("arcs", {}).items():
        for r in seq:
            if r != "$breaker" and r not in roles:
                errs.append(f"graph-arc {arc}: unknown role {r}")
    for r in orch.get("breaker_by_situation", {}).values():
        if r not in roles:
            errs.append(f"graph-breaker: unknown role {r}")


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root)
    skills_dir, agents_dir = root / ".claude/skills", root / ".claude/agents"
    if not skills_dir.is_dir() or not agents_dir.is_dir():
        print("usage error: --root must contain .claude/skills and .claude/agents")
        return 2
    try:
        graph = load_graph(root)
    except (OSError, ValueError) as exc:
        print(f"usage error: cannot load graph from CLAUDE.md ({exc})")
        return 2

    errs, report = [], []
    role_names = list(graph.get("roles", {}))
    on_disk = {p.name for p in skills_dir.iterdir() if p.is_dir()}
    for extra in sorted(on_disk - set(role_names) - {ORCHESTRATOR}):
        errs.append(f"graph-orphan {extra}: skill directory not in graph")
    referenced = check_skills(skills_dir, role_names, errs, report)
    agents = check_agents(agents_dir, errs, report)
    check_graph(graph, referenced, agents, errs)
    diff_body = (skills_dir / ORCHESTRATOR / "SKILL.md").read_text()
    for role in role_names:
        if f"`{role}`" not in diff_body:
            errs.append(f"skill-cast {ORCHESTRATOR}: cast table missing {role}")

    if not args.quiet:
        print("\n".join(report))
        print(f"\nskills={len(role_names) + 1} agents={len(agents)}")
    if errs:
        print("\nVIOLATIONS:\n- " + "\n- ".join(errs))
        return 1
    print("OK — no violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
