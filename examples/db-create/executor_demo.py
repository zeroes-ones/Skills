#!/usr/bin/env python3
"""Deterministic executor for examples/db-create/db-create.yaml."""


def execute_node(node_id, state, ctx):
    if node_id == "schema":
        return {"status": "done", "verdict": "pass",
                "summary": "schema v1 + forward/backward migration plan for the module",
                "evidence": ["schema:v1"]}
    if node_id == "schema-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "schema reviewed and approved", "evidence": ["gate:schema-ok"]}
    if node_id == "impl":
        return {"status": "done", "verdict": "pass",
                "summary": "wrote migrations + rollback; ran against staging copy",
                "evidence": ["impl:migrations"]}
    if node_id == "qa":
        return {"status": "done", "verdict": "pass",
                "summary": "data-integrity tests green on migrated staging DB",
                "evidence": ["qa:migrations"]}
    if node_id == "release-gate":
        return {"status": "done", "verdict": "approved",
                "summary": "approved to apply migrations to production",
                "evidence": ["gate:release-ok"]}
    return {"status": "done", "verdict": "pass",
            "summary": "%s converged" % node_id, "evidence": [node_id]}


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    print(execute_node("qa", {}, {}))
