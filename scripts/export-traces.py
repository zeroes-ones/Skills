#!/usr/bin/env python3
"""
export-traces.py — export a workflow run-state checkpoint as OTel-shaped spans (stdlib only).

Frontier B4 (BEYOND-LOOPS-GRAPHS.md): run-state is already a trace — this exporter turns a
checkpoint into OTel-inspired span records so any span pipeline (Langfuse/Phoenix/Grafana Tempo)
can ingest agent-run telemetry. Stable naming is part of the contract:

    session span : session.<workflow>            (one per run)
    node span    : workflow.<workflow>.node.<id> (one per executed node, incl. gates)

Attributes are stable keys: status, verdict, evidence, iterations, and (where present) step.
Cost/tokens are executor-reported: the runner accumulates `usage` from each node into run-state and
this exporter surfaces it per span and rolled up on the session span. `usage_reported` /
`cost_measured` distinguish "spent nothing" from "not measured" — an unmeasured run must never be
read as a free one. Latency remains a placeholder (0) until a real executor reports it. Sampling
policy is 100% for escalations/guardrail trips (the state log's 'escalate'/'guardrail' actions),
default otherwise.

Usage:
    python3 scripts/export-traces.py --state examples/workflow-runtime/state/happy-run-state.json
    python3 scripts/export-traces.py --state ... --json   # single JSON array instead of JSONL
Exit code 0.
"""

import argparse
import hashlib
import json
import sys


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _esc(tag):
    return tag.replace("<", "_").replace(">", "_").replace(" ", "_")


def export(state):
    """Return a list of span dicts for one run-state checkpoint."""
    workflow = state.get("workflow", "run")
    spans = []
    session_id = "session.%s" % _esc(workflow)
    spans.append({
        "name": session_id,
        "kind": "SESSION",
        "span_id": _sha(session_id + ":" + state.get("manifest_sha", "")),
        "parent_span_id": None,
        "attributes": {
            "workflow": workflow,
            "manifest_sha": state.get("manifest_sha"),
            "phase": state.get("phase"),
            "outcome_steps": state.get("budget", {}).get("steps_used", 0),
            "iterations": state.get("budget", {}).get("iterations", {}),
            "created": state.get("created"),
            "updated": state.get("updated"),
            # run-level cost rollup (executor-reported). `cost_measured` false means the
            # executor reported nothing — the run's cost is UNKNOWN, not zero.
            "cost_usd": (state.get("budget", {}).get("cost") or {}).get("cost_usd"),
            "tokens_in": (state.get("budget", {}).get("cost") or {}).get("tokens_in", 0),
            "tokens_out": (state.get("budget", {}).get("cost") or {}).get("tokens_out", 0),
            "cost_measured": (state.get("budget", {}).get("cost") or {}).get("measured", False),
            "max_cost_usd": (state.get("budget") or {}).get("max_cost_usd"),
        },
        "sampled": True,
    })
    escalate_steps = {e.get("step") for e in state.get("log", [])
                      if e.get("action") in ("escalate", "guardrail")}
    for nid, rec in sorted(state.get("nodes", {}).items()):
        span_name = "workflow.%s.node.%s" % (_esc(workflow), _esc(nid))
        sampled = bool(escalate_steps) or rec.get("status") in ("blocked", "needs_review")
        spans.append({
            "name": span_name,
            "kind": "SPAN",
            "span_id": _sha(span_name + ":" + nid),
            "parent_span_id": _sha(session_id + ":" + state.get("manifest_sha", "")),
            "attributes": {
                "node": nid,
                "status": rec.get("status"),
                "verdict": rec.get("verdict"),
                "evidence": rec.get("evidence") or [],
                "iterations": rec.get("iterations", 0),
                "latency_ms": 0,   # reported by the executor in real deployments
                # executor-reported usage (None when the executor reported nothing, so an
                # unreported span is distinguishable from a genuinely free one)
                "tokens_in": (rec.get("cost") or {}).get("tokens_in"),
                "tokens_out": (rec.get("cost") or {}).get("tokens_out"),
                "tokens": (((rec.get("cost") or {}).get("tokens_in") or 0)
                           + ((rec.get("cost") or {}).get("tokens_out") or 0)),
                "cost_usd": (rec.get("cost") or {}).get("cost_usd"),
                "usage_reported": (rec.get("cost") or {}).get("reported", False),
            },
            "sampled": sampled,
        })
    return spans


def main(argv=None):
    ap = argparse.ArgumentParser(description="Export a workflow run-state as OTel-shaped spans")
    ap.add_argument("--state", required=True, help="run-state json checkpoint")
    ap.add_argument("--json", action="store_true", help="emit one JSON array")
    args = ap.parse_args(argv)

    with open(args.state, encoding="utf-8") as fh:
        state = json.load(fh)
    spans = export(state)
    if args.json:
        print(json.dumps(spans, indent=2))
    else:
        for s in spans:
            print(json.dumps(s, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
