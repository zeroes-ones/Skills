#!/usr/bin/env python3
"""Deterministic executor for examples/support-maintain/support-maintain.yaml.

SUPPORT_SCENARIO=clean    first fix pass passes -> month closes normally.
SUPPORT_SCENARIO=stuck    fixes never verify -> support-loop exhausts and escalates to the
                          human month-close gate (SLA/hours review, not silent absorption).
"""

import os

_SCENARIO = os.environ.get("SUPPORT_SCENARIO", "clean").strip().lower()
_STUCK = _SCENARIO == "stuck"


def _verify(node_id, state, ctx):
    runs = state.setdefault("fields", {}).get("verify_runs", 0) + 1
    state["fields"]["verify_runs"] = runs
    ok = not _STUCK
    return {"status": "done",
            "verdict": "pass" if ok else "changes_requested",
            "summary": ("all bucket tickets closed + regression green (run %d)" % runs) if ok
                       else ("fix regressed another area (run %d)" % runs),
            "evidence": ["verify-%d" % runs],
            "diagnostics": [] if ok else ["regression"]}


def execute_node(node_id, state, ctx):
    if node_id == "intake":
        return {"status": "done", "verdict": "pass",
                "summary": "monthly bucket: 12 tickets (9 bug, 2 config, 1 small change); SLA watch",
                "evidence": ["intake:12-tickets"]}
    if node_id == "verify":
        return _verify(node_id, state, ctx)
    if node_id == "fix":
        return {"status": "done", "verdict": "pass",
                "summary": "applied fixes for the bucket",
                "evidence": ["fix:%s" % ctx.get("pass")]}
    if node_id == "close-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "month closed: SLA met, hours within retainer, true-up none",
                "evidence": ["gate:month-close"]}
    return {"status": "done", "verdict": "pass",
            "summary": "%s converged" % node_id, "evidence": [node_id]}


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    print(execute_node("verify", {"fields": {}}, {"pass": 1}))
