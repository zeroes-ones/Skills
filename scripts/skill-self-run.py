#!/usr/bin/env python3
"""skill-self-run.py — make ANY eligible skill self-run with handoff-and-continue.

Reads a skill's own `chain.consumes_from` (BACK direction) and generates a validated workflow
manifest + deterministic executor that, when run:

  [back]  prereqs (handoff chain) -> main-skill
  [loop]  main-skill repeats until its Verification passes (exit_when: main.verdict == pass);
          exhaustion reroutes via a kind: agent gate (bounded)
  [end]   continues forward to a HUMAN accept gate with the evidence trail.

Up/down/diagonal context (framework rules, references, cross-skill coordination) is loaded by
the executor/agent inside the main node — the engine owns ordering, loops, handoffs, budgets,
gates. Any skill with Core Workflow + Verification is a valid node (repo audit ~300/303).

Usage:
    python3 scripts/skill-self-run.py --skill code-reviewer --prereqs 2 --fix-rounds 3 \
        --out examples/self-run/code-reviewer

    python3 scripts/workflow-runner.py \
        --manifest <out>/<skill>.yaml \
        --executor <out>/<skill>_executor.py --state /tmp/<skill>.json
"""

import argparse
import os
import re
import sys

SKILLS_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "skills")
BUDGET = {"xs": 30, "s": 50, "m": 80, "l": 120}
HANDOFF = ("status, summary, artifacts, decisions, open_questions, "
           "verification_evidence, context, budget, next")


def find_skill(skill_name):
    for domain in sorted(os.listdir(SKILLS_ROOT)):
        p = os.path.join(SKILLS_ROOT, domain, skill_name, "SKILL.md")
        if os.path.isfile(p):
            return p
    return None


def frontmatter(text):
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


def parse_chain(fm):
    """Return (consumes, feeds) name lists from a YAML-ish chain block (no PyYAML needed)."""
    consumes, feeds = [], []
    section = None
    for line in fm.splitlines():
        s = line.strip()
        if s == "consumes_from:":
            section = "c"
            continue
        if s == "feeds_into:":
            section = "f"
            continue
        if s.startswith("- "):
            if section == "c":
                consumes.append(s[2:].strip())
            elif section == "f":
                feeds.append(s[2:].strip())
        elif s and not s.startswith(("-", "examples:", "#")):
            if not s.startswith(("consumes_from:", "feeds_into:", "examples:", "name:",
                                 "description:", "license:", "tags:", "author:", "type:",
                                 "status:", "version:", "updated:", "token_budget:")) and \
                    section in ("c", "f"):
                section = None
    return consumes, feeds


def _q(s):
    return '"%s"' % s.replace('"', "'")


def emit(name, skill_name, prereq_names, fix_desc, budget):
    payload = "  handoff-v1:\n    - " + "\n    - ".join(HANDOFF.split(", "))
    n = len(prereq_names)
    start = prereq_names[0] if n else "main"

    nodes = ["nodes:"]
    for pid in prereq_names:
        nodes.append("  - id: %s\n    skill: %s\n    outputs: [%s-output]" % (pid, pid, pid))
    nodes.append("  - id: main\n    skill: %s\n    outputs: [result]" % skill_name)

    gates = (
        "gates:\n"
        "  - id: identify-agent-gate\n"
        "    type: gate\n    kind: agent\n"
        "    pool: [main]\n"
        "    max_reroutes: 3\n"
        "    escalate_to: accept-gate\n"
        "    requires: [result]\n"
        "    description: %s\n"
        "  - id: accept-gate\n"
        "    type: gate\n    kind: human\n"
        "    requires: [result]\n"
        "    description: %s\n"
        % (_q("Pre-human triage: on self-loop exhaustion, reroute the main channel (bounded); "
              "then escalate to the human gate."),
           _q("Human accepts the result once the skill's Verification passes (or reviews the "
              "escalation report when automation exhausted)."))
    )

    edges = ["edges:"]
    for i in range(n):
        src = prereq_names[i]
        dst = prereq_names[i + 1] if i + 1 < n else "main"
        edges.append("  - from: %s\n    to: %s\n    when: %s.status == done\n"
                     "    payload: handoff-v1" % (src, dst, src))
    edges.append("  - from: main\n    to: accept-gate\n    when: main.status == done\n"
                 "    payload: handoff-v1")

    loop = (
        "loops:\n"
        "  - id: self-loop\n"
        "    nodes: [main]\n"
        "    exit_when: main.verdict == pass\n"
        "    max_iterations: 2\n"
        "    escalate_to: identify-agent-gate\n"
        "    convergence:\n"
        "      window: 2\n"
        "      require_delta: true"
    )
    manifest = (
        "name: %s\n"
        "version: \"1.0.0\"\n"
        "description: %s\n"
        "payloads:\n%s\n"
        "budget:\n"
        "  max_steps: %d\n"
        "start: %s\n"
        "%s\n"
        "%s\n"
        "%s\n"
        "%s\n"
        "end: [accept-gate]\n" % (name, _q(fix_desc), payload, budget, start,
                                  "\n".join(nodes), gates, "\n".join(edges), loop)
    )
    return manifest


def emit_executor(skill_name, fix_rounds, prereq_names):
    extra = ""
    for pid in prereq_names:
        extra += ('    if node_id == "%s":\n'
                  '        return {"status": "done", "verdict": "pass",\n'
                  '                "summary": "prerequisite %s satisfied",\n'
                  '                "evidence": ["%s"]}\n' % (pid, pid, pid))
    template = (
        '#!/usr/bin/env python3\n'
        '"""Deterministic executor generated by scripts/skill-self-run.py for @@SKILL@@.\n'
        'Prerequisites pass; the main skill fails until run @@PASS_AT@@ so the self-loop\n'
        'exhausts once, the identify-agent gate reroutes a bounded window, the skill\u2019s\n'
        'Verification passes, and the HUMAN accept gate approves. Override FIX_ROUNDS=n.\n'
        '"""\n'
        'import os\n'
        '\n'
        '_PASS_AT = int(os.environ.get("FIX_ROUNDS", "@@PASS_AT@@"))\n'
        '\n'
        'def _main(node_id, state, ctx):\n'
        '    runs = state.setdefault("fields", {}).get("main_runs", 0) + 1\n'
        '    state["fields"]["main_runs"] = runs\n'
        '    ok = runs >= _PASS_AT\n'
        '    return {"status": "done",\n'
        '            "verdict": "pass" if ok else "changes_requested",\n'
        '            "summary": ("Verification passed on run %d" % runs) if ok\n'
        '                       else ("Verification failed on run %d" % runs),\n'
        '            "evidence": ["run-%d" % runs],\n'
        '            "diagnostics": [] if ok else ["self-check"]}\n'
        '\n'
        'def execute_node(node_id, state, ctx):\n'
        '    if node_id == "main":\n'
        '        return _main(node_id, state, ctx)\n'
        '@@EXTRA@@'
        '    if node_id == "accept-gate":\n'
        '        return {"status": "done", "verdict": "approved",\n'
        '                "summary": "human accepted (skill complete)",\n'
        '                "evidence": ["gate-accepted"]}\n'
        '    return {"status": "done", "verdict": "pass",\n'
        '            "summary": node_id + " converged", "evidence": [node_id]}\n'
        '\n'
        'if __name__ == "__main__":  # pragma: no cover\n'
        '    print(execute_node("main", {"fields": {}}, {"pass": 1}))\n'
    )
    return (template
            .replace("@@SKILL@@", skill_name)
            .replace("@@PASS_AT@@", str(fix_rounds))
            .replace("@@EXTRA@@", extra))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--skill", required=True, help="skill name (must exist under skills/)")
    ap.add_argument("--prereqs", type=int, default=2,
                    help="how many chain.consumes_from prereqs to run first (back direction)")
    ap.add_argument("--fix-rounds", type=int, default=3)
    ap.add_argument("--size", default="m", choices=sorted(BUDGET))
    ap.add_argument("--out", default="examples/self-run",
                    help="output directory (created)")
    args = ap.parse_args(argv)

    path = find_skill(args.skill)
    if not path:
        print("skill not found: %s" % args.skill, file=sys.stderr)
        return 2
    text = open(path, encoding="utf-8").read()
    fm = frontmatter(text)
    consumes, feeds = parse_chain(fm)
    prereqs = []
    for c in consumes:
        if c == args.skill or c in prereqs:
            continue
        if find_skill(c):
            prereqs.append(c)
        if len(prereqs) >= max(0, args.prereqs):
            break
    name = args.skill
    desc = ("Self-running graph for skill %r: run %d prerequisite(s) (back), then the skill "
            "loops until its Verification passes (exit_when: main.verdict == pass; exhaustion "
            "reroutes via a kind: agent gate), then hands off to a human accept gate."
            % (args.skill, len(prereqs)))
    os.makedirs(args.out, exist_ok=True)
    manifest_path = os.path.join(args.out, name + ".yaml")
    executor_path = os.path.join(args.out, name + "_executor.py")
    with open(manifest_path, "w", encoding="utf-8") as fh:
        fh.write(emit(name, args.skill, prereqs, desc, BUDGET[args.size]))
    with open(executor_path, "w", encoding="utf-8") as fh:
        fh.write(emit_executor(args.skill, args.fix_rounds, prereqs))
    os.chmod(executor_path, 0o755)
    print("wrote %s" % manifest_path)
    print("wrote %s" % executor_path)
    print("backtrace prereqs: %s" % (prereqs or "(none — start at main)"))
    print("\nRun it:")
    print("  python3 scripts/workflow-runner.py --manifest %s \\" % manifest_path)
    print("      --executor %s --state /tmp/%s.json" % (executor_path, name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
