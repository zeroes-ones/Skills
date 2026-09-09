#!/usr/bin/env python3
"""Deterministic executor for examples/ui-change/ui-change.yaml."""


def execute_node(node_id, state, ctx):
    if node_id == "ui":
        return {"status": "done", "verdict": "pass",
                "summary": "redesigned checkout summary view (responsive, dark mode)",
                "evidence": ["ui:checkout-summary"]}
    if node_id == "review":
        return {"status": "done", "verdict": "pass",
                "summary": "review: no regressions, state handling clean",
                "evidence": ["review:ui-change"]}
    if node_id == "accept-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "client accepted the UI change", "evidence": ["gate:accepted"]}
    return {"status": "done", "verdict": "pass",
            "summary": "%s converged" % node_id, "evidence": [node_id]}


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    print(execute_node("ui", {}, {}))
