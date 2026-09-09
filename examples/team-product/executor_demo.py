#!/usr/bin/env python3
"""Deterministic executor for examples/team-product/team-product.yaml.

TEAM_SCENARIO=clean    qa passes on its 3rd run -> one agent-gate reroute, team lead approves,
                       release-manager deploys.
TEAM_SCENARIO=blocked  qa never passes -> bounded reroutes, then the human prod gate reviews.
"""

import os

_SCENARIO = os.environ.get("TEAM_SCENARIO", "clean").strip().lower()
_QA_PASS_AT = 3 if _SCENARIO == "clean" else 10 ** 6


def _verify(node_id, state, ctx):
    runs = state.setdefault("fields", {}).get("qa_runs", 0) + 1
    state["fields"]["qa_runs"] = runs
    ok = runs >= _QA_PASS_AT
    return {"status": "done",
            "verdict": "pass" if ok else "changes_requested",
            "summary": ("end-to-end suite green (run %d)" % runs) if ok
                       else ("integration gap between api and ui (run %d)" % runs),
            "evidence": ["verify-run-%d" % runs],
            "diagnostics": [] if ok else ["integration"]}


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
    if node_id == "verify":
        return _verify(node_id, state, ctx)
    if node_id == "spec":
        return {"status": "done", "verdict": "pass",
                "summary": "PRD + acceptance criteria for the release", "evidence": ["spec"]}
    if node_id == "architect":
        return {"status": "done", "verdict": "pass",
                "summary": "system design with api/ui contracts", "evidence": ["arch"]}
    if node_id in ("backend", "frontend"):
        return {"status": "done", "verdict": "pass",
                "summary": "%s track delivered" % node_id, "evidence": [node_id]}
    if node_id == "fixer":
        return {"status": "done", "verdict": "pass",
                "summary": "integration fixes applied", "evidence": ["fixer:%s" % ctx.get("pass")]}
    if node_id == "prod-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "team lead approved the production release",
                "evidence": ["gate:prod-approved"]}
    if node_id == "deploy":
        return {"status": "done", "verdict": "pass",
                "summary": "release-manager: production deploy executed",
                "evidence": ["deploy:prod"]}
    return {"status": "done", "verdict": "pass",
            "summary": "%s converged" % node_id, "evidence": [node_id]}


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    print(execute_node("verify", {"fields": {}}, {"pass": 1}))
