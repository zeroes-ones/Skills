#!/usr/bin/env python3
"""Deterministic executor for examples/production-incident/production-incident.yaml.

Stand-in for agentic node content. Scenario control (env):
  INCIDENT_SCENARIO=stable   telemetry goes green on its 3rd run -> one agent-gate reroute,
                             then the human incident commander confirms stabilization.
  INCIDENT_SCENARIO=sev      telemetry never goes green -> bounded reroutes, then escalation
                             to the human commander (declare / rollback decision).
"""

import os

_SCENARIO = os.environ.get("INCIDENT_SCENARIO", "stable").strip().lower()
_GREEN_AT = 3 if _SCENARIO == "stable" else 10 ** 6


def _telemetry(node_id, state, ctx):
    runs = state.setdefault("fields", {}).get("tel_runs", 0) + 1
    state["fields"]["tel_runs"] = runs
    ok = runs >= _GREEN_AT
    return {"status": "done",
            "verdict": "green" if ok else "degraded",
            "summary": ("checkout error rate back to baseline (run %d)" % runs) if ok
                       else ("error rate still elevated: %s (run %d)"
                             % ("5xx spike on checkout", runs)),
            "evidence": ["tel-run-%d" % runs],
            "diagnostics": ["checkout-5xx"] if not ok else []}


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
    if node_id == "triage":
        return {"status": "done", "verdict": "sev-2",
                "summary": "declared SEV-2: checkout checkout 5xx spike, checkout scope bounded",
                "evidence": ["alert:checkout-5xx", "scope:checkout-api"]}
    if node_id == "telemetry":
        return _telemetry(node_id, state, ctx)
    if node_id == "fix":
        return {"status": "done", "verdict": "pass",
                "summary": "applied mitigation (canary scale-up + retry backoff)",
                "evidence": ["fix:%s" % ctx.get("pass")]}
    if node_id == "commander-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "incident commander confirmed stabilization; postmortem scheduled",
                "evidence": ["gate:commander-approved"]}
    return {"status": "done", "verdict": "pass",
            "summary": "%s converged" % node_id, "evidence": [node_id]}


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    print(execute_node("telemetry", {"fields": {}}, {"pass": 1}))
