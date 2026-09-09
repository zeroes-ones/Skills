#!/usr/bin/env python3
"""Deterministic executor for examples/payments-api-ship/payments-api-ship.yaml.

Stand-in for agentic node content (an LLM running each node's SKILL.md). This module answers
for every node so scripts/workflow-runner.py is testable headless, mirroring what the skills'
Core Workflow + Verification would actually produce:

  - spec/architect/backend      : pass (design work converges)
  - code-reviewer/security-rwtr : pass on round 1 (audits clean for the demo)
  - fixer                       : pass (rework is applied when the loop asks)
  - qa                          : fails until its 4th run, then passes  -- this is what makes
                                  the loop exhaust once, hit the identify-agent gate, reroute a
                                  bounded window (channel first), and finally converge.
  - identify-agent-gate         : ctx.mode == "identify" -> reroute to the first untried pool
                                  member (deterministic content leg; repo_checks.py does the same)
  - release-gate (human)        : approve

Scenario control (env):
  PAYMENTS_SCENARIO=happy     qa passes on run 4  -> one agent reroute, then human approval
  PAYMENTS_SCENARIO=exhaust   qa never passes     -> reroute budget spent, escalates to the
                              human gate with the escalation report
"""

import os

_SCENARIO = os.environ.get("PAYMENTS_SCENARIO", "happy").strip().lower()
_QA_PASS_AT = 4 if _SCENARIO == "happy" else 10 ** 6


def _qa(node_id, state, ctx):
    runs = state.setdefault("fields", {}).get("qa_runs", 0) + 1
    state["fields"]["qa_runs"] = runs
    ok = runs >= _QA_PASS_AT
    return {"status": "done",
            "verdict": "pass" if ok else "changes_requested",
            "summary": ("checkout suite green after run %d" % runs) if ok
                       else ("flaky e2e on checkout (run %d)" % runs),
            "evidence": ["qa-run-%d" % runs],
            "diagnostics": ["checkout-e2e"] if not ok else []}


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
    if node_id == "qa":
        return _qa(node_id, state, ctx)
    if node_id == "fixer":
        return {"status": "done", "verdict": "pass",
                "summary": "applied review findings", "evidence": ["fixer:%s" % ctx.get("pass")]}
    if node_id == "release-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "release manager approved ship", "evidence": ["gate:human-approve"]}
    return {"status": "done", "verdict": "pass",
            "summary": "%s converged" % node_id, "evidence": [node_id]}


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    print(execute_node("qa", {"fields": {}}, {"pass": 1}))
