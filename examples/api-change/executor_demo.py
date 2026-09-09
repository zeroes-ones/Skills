#!/usr/bin/env python3
"""Deterministic executor for examples/api-change/api-change.yaml."""


def execute_node(node_id, state, ctx):
    if node_id == "contract":
        return {"status": "done", "verdict": "pass",
                "summary": "v2 contract: cursor pagination + error model; versioning plan",
                "evidence": ["spec:api-v2"]}
    if node_id == "backend":
        return {"status": "done", "verdict": "pass",
                "summary": "implemented v2 endpoints behind version header",
                "evidence": ["impl:api-v2"]}
    if node_id == "secure":
        return {"status": "done", "verdict": "pass",
                "summary": "auth + rate limits applied; no new exposure",
                "evidence": ["secure:api-v2"]}
    if node_id == "qa":
        return {"status": "done", "verdict": "pass",
                "summary": "contract tests green (pagination, errors, auth)",
                "evidence": ["qa:api-v2"]}
    if node_id == "accept-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "client accepted the API change", "evidence": ["gate:accepted"]}
    return {"status": "done", "verdict": "pass",
            "summary": "%s converged" % node_id, "evidence": [node_id]}


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    print(execute_node("qa", {}, {}))
