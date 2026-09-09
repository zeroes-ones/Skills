#!/usr/bin/env python3
"""Deterministic executor for examples/strangler-migration/strangler-migration.yaml.

Stand-in for agentic node content. Scenario control (env):
  MIGRATION_SCENARIO=clean     qa passes on its 3rd run -> one agent-gate reroute, then the
                               human plan-gate and cutover-gate both approve.
  MIGRATION_SCENARIO=blocked   qa never passes -> bounded reroutes, then escalation to the
                               human cutover gate (do-not-cut-over review).
"""

import os

_SCENARIO = os.environ.get("MIGRATION_SCENARIO", "clean").strip().lower()
_QA_PASS_AT = 3 if _SCENARIO == "clean" else 10 ** 6


def _verify(node_id, state, ctx):
    runs = state.setdefault("fields", {}).get("qa_runs", 0) + 1
    state["fields"]["qa_runs"] = runs
    ok = runs >= _QA_PASS_AT
    return {"status": "done",
            "verdict": "pass" if ok else "changes_requested",
            "summary": ("parity suite green for migrated slice (run %d)" % runs) if ok
                       else ("legacy parity gap on edge cases (run %d)" % runs),
            "evidence": ["verify-run-%d" % runs],
            "diagnostics": ["parity-gap"] if not ok else []}


def execute_node(node_id, state, ctx):
    if ctx and ctx.get("mode") == "identify":
        pool = ctx.get("pool") or []
        if not pool:
            return {"status": "done", "verdict": "human",
                    "summary": "no corrective channels left", "evidence": ["identify:none"]}
        cand = pool[0]
        return {"status": "done", "verdict": "reroute", "next": cand,
                "summary": "identified %s as the channel to lead the next window" % cand,
                "evidence": ["identify:%s" % cand]}
    if node_id == "analyze":
        return {"status": "done", "verdict": "pass",
                "summary": "strangler plan: slice 3 = checkout; 2 calls, 1 table, route in gateway",
                "evidence": ["plan:checkout-slice"]}
    if node_id == "plan-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "architecture owner approved the migration plan",
                "evidence": ["gate:plan-approved"]}
    if node_id == "verify":
        return _verify(node_id, state, ctx)
    if node_id == "implement":
        return {"status": "done", "verdict": "pass",
                "summary": "implemented checkout slice behind gateway flag",
                "evidence": ["implement:%s" % ctx.get("pass")]}
    if node_id == "cutover-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "release owner approved cutover to the new slice",
                "evidence": ["gate:cutover-approved"]}
    if node_id == "docs-engineer":
        return {"status": "done", "verdict": "pass",
                "summary": "published API reference for the new slice",
                "evidence": ["docs:api-reference"]}
    if node_id == "deprecation-engineer":
        return {"status": "done", "verdict": "pass",
                "summary": "sunset plan: legacy endpoint deprecation notice + removal date",
                "evidence": ["deprecation:sunset-plan"]}
    return {"status": "done", "verdict": "pass",
            "summary": "%s converged" % node_id, "evidence": [node_id]}


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    print(execute_node("verify", {"fields": {}}, {"pass": 1}))
