#!/usr/bin/env python3
"""goal-to-graph.py — describe a goal, get a runnable spec-to-ship graph.

Turns a one-line client goal into a validated workflow manifest + a deterministic executor:
the graph runs skill-nodes, iterates a bounded fix-verify loop until verification passes
(exhaustion escalates to a kind: agent gate for bounded reroutes), and ends at a HUMAN
release/close gate once everything is green.

Output manifest passes `scripts/validate-workflows.py` (Safe-YAML subset: single-line
descriptions, condition vocabulary, escalation arcs for reachability). Planning skill layer
(which skills, which order) is delegated to the repo's own planner skills
(workflow-graph-authoring, iterative-task-execution, multi-agent-orchestration); this script
is the executable that materializes their plan as a runnable graph.

Usage:
    python3 scripts/goal-to-graph.py \
        --goal "Build me a booking SaaS MVP with auth and payments" \
        --name booking-mvp --kind build --size m --fix-rounds 3 \
        --out examples/goal-to-ship/booking-mvp

Kinds: build | ui | api | db | support
Sizes: xs | s | m | l | xl | xxl   (budget max_steps scaling)

Output: <out>/<name>.yaml  and  <out>/<name>_executor.py
Run it:
    python3 scripts/workflow-runner.py --manifest <out>/<name>.yaml \\
        --executor <out>/<name>_executor.py --state /tmp/<name>.json
"""

import argparse
import os
import re
import sys

# skill by kind (main deliverable node)
BUILD_SKILL = {
    "build": "backend-developer",
    "ui": "frontend-developer",
    "api": "backend-developer",
    "db": "backend-developer",
}
BUDGET = {"xs": 30, "s": 40, "m": 60, "l": 90, "xl": 120, "xxl": 160}
KINDS = set(BUILD_SKILL) | {"support"}

HANDOFF = ("status, summary, artifacts, decisions, open_questions, "
           "verification_evidence, context, budget, next")


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    return s or "goal-ship"


def _q(s):
    return '"%s"' % s.replace('"', "'")


def emit_manifest(name, kind, size, fix_desc):
    budget = BUDGET.get(size, 60)
    skill = BUILD_SKILL.get(kind, "backend-developer")
    loop_nodes = "build, verify" if kind != "support" else "fix, verify"
    gate_id = "release-gate" if kind != "support" else "close-gate"
    gate_desc = ("Human release approval: ship to production once the bounded fix-verify "
                 "loop converges (or review the escalation report when automation exhausted)."
                 if kind != "support"
                 else "Human month-close review of SLA and hours vs the retainer bucket.")
    start = "spec" if kind != "support" else "intake"
    payload = "  handoff-v1:\n    - " + "\n    - ".join(HANDOFF.split(", "))

    if kind == "support":
        nodes = (
            "nodes:\n"
            "  - id: intake\n    skill: customer-support-engineer\n    outputs: [ticket-bucket]\n"
            "  - id: fix\n    skill: backend-developer\n    inputs: [ticket-bucket]\n    outputs: [fix-attempt]\n"
            "  - id: verify\n    skill: qa-engineer\n    inputs: [ticket-bucket, fix-attempt]\n    outputs: [verify-report]\n"
        )
        edges = (
            "edges:\n"
            "  - from: intake\n    to: fix\n    when: intake.status == done\n    payload: handoff-v1\n"
            "  - from: verify\n    to: %s\n    when: verify.status == done\n    payload: handoff-v1\n" % gate_id
        )
    else:
        nodes = (
            "nodes:\n"
            "  - id: spec\n    skill: idea-to-spec\n    outputs: [spec]\n"
            "  - id: build\n    skill: %s\n    inputs: [spec]\n    outputs: [deliverable]\n" % skill
            + "  - id: verify\n    skill: qa-engineer\n    inputs: [deliverable]\n    outputs: [qa-report]\n"
        )
        edges = (
            "edges:\n"
            "  - from: spec\n    to: build\n    when: spec.status == done\n    payload: handoff-v1\n"
            "  - from: build\n    to: verify\n    when: build.status == done\n    payload: handoff-v1\n"
            "  - from: verify\n    to: %s\n    when: verify.status == done\n    payload: handoff-v1\n" % gate_id
        )

    gates = (
        "gates:\n"
        "  - id: identify-agent-gate\n"
        "    type: gate\n"
        "    kind: agent\n"
        "    pool: [%s]\n"
        "    max_reroutes: 3\n"
        "    escalate_to: %s\n"
        "    requires: [verify-report, deliverable]\n"
        "    description: %s\n"
        "  - id: %s\n"
        "    type: gate\n"
        "    kind: human\n"
        "    description: %s\n" % (loop_nodes, gate_id,
                                   _q("Pre-human triage: on loop exhaustion, identify which "
                                      "channel leads the next bounded window (bounded reroutes); "
                                      "then escalate to the human gate."),
                                   gate_id, _q(gate_desc))
    )
    loop = (
        "loops:\n"
        "  - id: fix-verify-loop\n"
        "    nodes: [%s]\n"
        "    exit_when: verify.verdict == pass\n"
        "    max_iterations: 2\n"
        "    escalate_to: identify-agent-gate\n"
        "    convergence:\n"
        "      window: 2\n"
        "      require_delta: true\n" % loop_nodes
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
        "end: [%s]\n" % (name, _q(fix_desc), payload, budget, start, nodes, gates, edges,
                         loop, gate_id)
    )
    # order: nodes, gates, edges, loops (gates before edges is cosmetic; validator parses keys)
    return manifest


def emit_executor(name, kind, fix_rounds, size):
    gate_id = "release-gate" if kind != "support" else "close-gate"
    if kind == "support":
        extra = (
            '    if node_id == "intake":\n'
            '        return {"status": "done", "verdict": "pass",\n'
            '                "summary": "monthly ticket bucket triaged",\n'
            '                "evidence": ["intake"]}\n'
            '    if node_id == "fix":\n'
            '        return {"status": "done", "verdict": "pass",\n'
            '                "summary": "fixes applied",\n'
            '                "evidence": ["fix-" + str(ctx.get("pass"))]}\n'
        )
    else:
        extra = (
            '    if node_id == "spec":\n'
            '        return {"status": "done", "verdict": "pass",\n'
            '                "summary": "spec + acceptance criteria for the goal",\n'
            '                "evidence": ["spec"]}\n'
            '    if node_id == "build":\n'
            '        return {"status": "done", "verdict": "pass",\n'
            '                "summary": "deliverable implemented",\n'
            '                "evidence": ["build-" + str(ctx.get("pass"))]}\n'
        )
    template = (
        '#!/usr/bin/env python3\n'
        '"""Deterministic executor generated by scripts/goal-to-graph.py for @@NAME@@.\n'
        'verify fails until run @@PASS_AT@@, so the fix-verify loop exhausts once, the\n'
        'identify-agent gate reroutes a bounded window, verification passes, and the HUMAN\n'
        '@@GATE_ID@@ gate approves once ready. Override with FIX_ROUNDS=<n> when running.\n'
        '"""\n'
        'import os\n'
        '\n'
        '_PASS_AT = int(os.environ.get("FIX_ROUNDS", "@@PASS_AT@@"))\n'
        '\n'
        'def _verify(node_id, state, ctx):\n'
        '    runs = state.setdefault("fields", {}).get("verify_runs", 0) + 1\n'
        '    state["fields"]["verify_runs"] = runs\n'
        '    ok = runs >= _PASS_AT\n'
        '    return {"status": "done",\n'
        '            "verdict": "pass" if ok else "changes_requested",\n'
        '            "summary": ("verification green on run %d" % runs) if ok\n'
        '                       else ("verification failed on run %d" % runs),\n'
        '            "evidence": ["verify-%d" % runs],\n'
        '            "diagnostics": [] if ok else ["regression"]}\n'
        '\n'
        'def execute_node(node_id, state, ctx):\n'
        '    if node_id == "verify":\n'
        '        return _verify(node_id, state, ctx)\n'
        '@@EXTRA@@'
        '    if node_id == "@@GATE_ID@@":\n'
        '        return {"status": "done", "verdict": "approved",\n'
        '                "summary": "human approved (goal complete)",\n'
        '                "evidence": ["gate-@@GATE_ID@@"]}\n'
        '    return {"status": "done", "verdict": "pass",\n'
        '            "summary": node_id + " converged", "evidence": [node_id]}\n'
        '\n'
        'if __name__ == "__main__":  # pragma: no cover\n'
        '    print(execute_node("verify", {"fields": {}}, {"pass": 1}))\n'
    )
    return (template
            .replace("@@NAME@@", name)
            .replace("@@PASS_AT@@", str(fix_rounds))
            .replace("@@GATE_ID@@", gate_id)
            .replace("@@EXTRA@@", extra))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--goal", required=True, help="client goal, one line")
    ap.add_argument("--name", required=True, help="manifest slug / folder name")
    ap.add_argument("--kind", default="build", choices=sorted(KINDS))
    ap.add_argument("--size", default="m", choices=sorted(BUDGET))
    ap.add_argument("--fix-rounds", type=int, default=3, help="verification pass round")
    ap.add_argument("--out", default="examples/goal-to-ship/generated",
                    help="output directory (created)")
    args = ap.parse_args(argv)

    name = slugify(args.name)
    fix_desc = "%s (auto-generated graph, size %s, %s). Bounded fix-verify loop until " \
               "verification passes; exhaustion reroutes via a kind: agent gate; a human " \
               "release gate approves once ready." % (args.goal.strip(), args.size, args.kind)
    out_dir = args.out
    os.makedirs(out_dir, exist_ok=True)
    manifest_path = os.path.join(out_dir, name + ".yaml")
    executor_path = os.path.join(out_dir, name + "_executor.py")
    with open(manifest_path, "w", encoding="utf-8") as fh:
        fh.write(emit_manifest(name, args.kind, args.size, fix_desc))
    with open(executor_path, "w", encoding="utf-8") as fh:
        fh.write(emit_executor(name, args.kind, args.fix_rounds, args.size))
    os.chmod(executor_path, 0o755)
    print("wrote %s" % manifest_path)
    print("wrote %s" % executor_path)
    print("\nRun it:")
    print("  python3 scripts/workflow-runner.py --manifest %s \\" % manifest_path)
    print("      --executor %s --state /tmp/%s.json" % (executor_path, name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
