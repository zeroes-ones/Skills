#!/usr/bin/env python3
"""Deterministic executor for examples/enterprise-platform/enterprise-platform.yaml.

ENTERPRISE_SCENARIO=clean    qa passes on its 3rd run -> one agent-gate reroute; compliance
                             gate and release board both approve; canary observed healthy.
ENTERPRISE_SCENARIO=blocked  qa never passes -> bounded reroutes, then the compliance gate
                             reviews instead of approving canary.
"""

import os

_SCENARIO = os.environ.get("ENTERPRISE_SCENARIO", "clean").strip().lower()
_QA_PASS_AT = 3 if _SCENARIO == "clean" else 10 ** 6


def _verify(node_id, state, ctx):
    runs = state.setdefault("fields", {}).get("qa_runs", 0) + 1
    state["fields"]["qa_runs"] = runs
    ok = runs >= _QA_PASS_AT
    return {"status": "done",
            "verdict": "pass" if ok else "changes_requested",
            "summary": ("full regression + integration green (run %d)" % runs) if ok
                       else ("regression failures after audit findings (run %d)" % runs),
            "evidence": ["verify-run-%d" % runs],
            "diagnostics": [] if ok else ["regression"]}


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
                "summary": "program spec + compliance scope", "evidence": ["spec"]}
    if node_id == "architect":
        return {"status": "done", "verdict": "pass",
                "summary": "platform architecture with trust boundary", "evidence": ["arch"]}
    if node_id == "implement":
        return {"status": "done", "verdict": "pass",
                "summary": "release candidate implemented", "evidence": ["implement"]}
    if node_id == "secure":
        return {"status": "done", "verdict": "pass",
                "summary": "security review: threat model + findings closed",
                "evidence": ["secure"]}
    if node_id == "compliance":
        return {"status": "done", "verdict": "pass",
                "summary": "compliance readiness: controls mapped to evidence",
                "evidence": ["compliance"]}
    if node_id == "fixer":
        return {"status": "done", "verdict": "pass",
                "summary": "integrated audit findings into the candidate",
                "evidence": ["fixer:%s" % ctx.get("pass")]}
    if node_id == "compliance-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "security + compliance approved canary",
                "evidence": ["gate:compliance-approved"]}
    if node_id == "deploy":
        return {"status": "done", "verdict": "pass",
                "summary": "release-manager: canary deployed (5%)", "evidence": ["deploy:canary"]}
    if node_id == "observe":
        return {"status": "done", "verdict": "pass",
                "summary": "canary healthy: error budget + latency nominal",
                "evidence": ["observe:canary-healthy"]}
    if node_id == "release-board-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "release board approved full rollout",
                "evidence": ["gate:board-approved"]}
    return {"status": "done", "verdict": "pass",
            "summary": "%s converged" % node_id, "evidence": [node_id]}


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    print(execute_node("verify", {"fields": {}}, {"pass": 1}))
