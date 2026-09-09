#!/usr/bin/env python3
"""Deterministic executor for examples/add-feature/add-feature.yaml."""


def execute_node(node_id, state, ctx):
    if node_id == "scope":
        return {"status": "done", "verdict": "pass",
                "summary": "feature spec + acceptance criteria: export-to-PDF on invoices",
                "evidence": ["spec:export-pdf"]}
    if node_id == "build":
        return {"status": "done", "verdict": "pass",
                "summary": "implemented export-to-PDF behind existing layout",
                "evidence": ["build:export-pdf"]}
    if node_id == "qa":
        return {"status": "done", "verdict": "pass",
                "summary": "feature tests green + no regression on invoice flow",
                "evidence": ["qa:export-pdf"]}
    if node_id == "accept-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "client accepted the feature", "evidence": ["gate:accepted"]}
    return {"status": "done", "verdict": "pass",
            "summary": "%s converged" % node_id, "evidence": [node_id]}


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    print(execute_node("qa", {}, {}))
