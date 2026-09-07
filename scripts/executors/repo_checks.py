#!/usr/bin/env python3
"""repo_checks.py — deterministic executor that runs THIS repo's own quality gates as graph nodes.

Dogfooding example: the workflow layer running the Skills repo itself. Each node id maps to a
real repo validator; the executor returns {status, verdict, evidence, summary} from the actual
exit code + last output line, so the engine's loops/handoffs/gates operate on genuine check
results (no LLM needed for the demo; an agent executor is the drop-in for content nodes).

Node ids: workflow-validation | skill-lints | golden-evals
"""

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _run(args):
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    tail = (proc.stdout or "").strip().splitlines()
    return proc.returncode, (tail[-1] if tail else proc.stderr.strip()[:200])


def execute_node(node_id, state, ctx):
    if node_id == "start-check":
        return {"status": "done", "verdict": "pass",
                "summary": "kicking off repo quality gates",
                "evidence": ["start"]}
    if node_id == "release-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "repo quality gates green - release approved",
                "evidence": ["gate:all-pass"]}
    if node_id == "workflow-validation":
        code1, msg1 = _run(["python3", "scripts/validate-workflows.py", "--selftest"])
        code2, msg2 = _run(["python3", "scripts/validate-workflows.py", "--all"])
        ok = code1 == 0 and code2 == 0
        msg = "%s | %s" % (msg1, msg2)
    elif node_id == "skill-lints":
        code, msg = _run(["python3", "scripts/lib/lint-workflow.py", "--all"])
        ok = code == 0
        msg = "lint-workflow: %s" % msg
    elif node_id == "golden-evals":
        code, msg = _run(["bash", "scripts/eval-skill.sh", "--all"])
        ok = code == 0
        msg = "eval-skill: %s" % msg
    else:
        return {"status": "blocked", "verdict": "unknown-node",
                "summary": "no check bound to node %r" % node_id}
    return {"status": "done",
            "verdict": "pass" if ok else "changes_requested",
            "evidence": ["rc:%s" % (0 if ok else 1)],
            "summary": (msg or "")[:400]}


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    print(json.dumps(execute_node("workflow-validation", {}, {}), indent=1))
