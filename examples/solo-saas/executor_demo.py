#!/usr/bin/env python3
"""Deterministic executor for examples/solo-saas/solo-saas.yaml.

SOLO_SCENARIO=clean    qa passes on run 2 -> one bounded window, human go-live approves.
SOLO_SCENARIO=blocked  qa never passes -> loop exhausts and escalates STRAIGHT to the human
                       go-live gate (no specialist pool at solo scale): the solo dev decides.
"""

import os

_SCENARIO = os.environ.get("SOLO_SCENARIO", "clean").strip().lower()
_QA_PASS_AT = 2 if _SCENARIO == "clean" else 10 ** 6


def _qa(node_id, state, ctx):
    runs = state.setdefault("fields", {}).get("qa_runs", 0) + 1
    state["fields"]["qa_runs"] = runs
    ok = runs >= _QA_PASS_AT
    return {"status": "done",
            "verdict": "pass" if ok else "changes_requested",
            "summary": ("smoke + core flow green (run %d)" % runs) if ok
                       else ("found %d issues to fix (run %d)" % (3 if runs == 1 else 1, runs)),
            "evidence": ["qa-run-%d" % runs],
            "diagnostics": [] if ok else ["core-flow"]}


def execute_node(node_id, state, ctx):
    if node_id == "qa":
        return _qa(node_id, state, ctx)
    if node_id == "spec":
        return {"status": "done", "verdict": "pass",
                "summary": "one-page spec: landing page + core flow on a $5 VPS",
                "evidence": ["spec:v1"]}
    if node_id == "build":
        return {"status": "done", "verdict": "pass",
                "summary": "built the MVP (auth, core flow, sqlite)",
                "evidence": ["build:%s" % ctx.get("pass")]}
    if node_id == "go-live-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "solo dev approved go-live", "evidence": ["gate:go-live"]}
    return {"status": "done", "verdict": "pass",
            "summary": "%s converged" % node_id, "evidence": [node_id]}


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    print(execute_node("qa", {"fields": {}}, {"pass": 1}))
