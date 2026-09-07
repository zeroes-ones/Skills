#!/usr/bin/env python3
"""
skill-sli-report.py — per-workflow SLIs from run-state checkpoints (stdlib only).

Frontier B4/L4 (M3, BEYOND-LOOPS-GRAPHS.md): treat agent workflows like distributed systems.
Given a directory of run-state checkpoints, report SLIs per workflow:

    runs             checkpoints seen
    complete         outcomes recorded 'complete' with no escalation/guardrail in the log
    escalated        runs with an escalate or guardrail log action (silent-stop / blocked)
    escalation_rate  escalated / runs
    avg_steps        mean budget.steps_used (cost proxy)
    guardrail_blocks runs with a 'guardrail' log action

Optional quality gate: --gate-escalation 0.5 exits 1 when any workflow's escalation rate is at or
above the threshold, so CI can fail when reliability degrades. Deterministic; cost/latency slots
come from real executors later.

Usage:
    python3 scripts/skill-sli-report.py --dir examples/workflow-runtime/state
    python3 scripts/skill-sli-report.py --dir <states> --gate-escalation 0.5
    python3 scripts/skill-sli-report.py --dir <states> --json
"""

import argparse
import json
import os
import sys


def _load_states(directory):
    states = []
    for root, _dirs, files in os.walk(directory):
        for f in sorted(files):
            if f.endswith(".json"):
                path = os.path.join(root, f)
                try:
                    with open(path, encoding="utf-8") as fh:
                        state = json.load(fh)
                except (OSError, ValueError):
                    continue
                if isinstance(state, dict) and state.get("workflow"):
                    states.append((path, state))
    return states


def _escalated(state):
    return any(e.get("action") in ("escalate", "guardrail") for e in state.get("log", []))


def report(states):
    per = {}
    for path, state in states:
        wf = state["workflow"]
        agg = per.setdefault(wf, {"runs": 0, "complete": 0, "escalated": 0,
                                  "guardrail_blocks": 0, "steps": []})
        agg["runs"] += 1
        steps = state.get("budget", {}).get("steps_used", 0)
        agg["steps"].append(steps)
        esc = _escalated(state)
        if esc:
            agg["escalated"] += 1
        else:
            agg["complete"] += 1
        if any(e.get("action") == "guardrail" for e in state.get("log", [])):
            agg["guardrail_blocks"] += 1
    rows = []
    for wf in sorted(per):
        a = per[wf]
        rate = a["escalated"] / a["runs"] if a["runs"] else 0.0
        avg_steps = (sum(a["steps"]) / len(a["steps"])) if a["steps"] else 0
        rows.append({"workflow": wf, "runs": a["runs"], "complete": a["complete"],
                     "escalated": a["escalated"],
                     "escalation_rate": round(rate, 2),
                     "avg_steps": round(avg_steps, 1),
                     "guardrail_blocks": a["guardrail_blocks"]})
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description="Per-workflow SLIs from run-state checkpoints")
    ap.add_argument("--dir", required=True, help="directory of run-state *.json checkpoints")
    ap.add_argument("--gate-escalation", type=float, default=None,
                    help="fail (exit 1) if any workflow escalation rate >= this threshold")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    states = _load_states(args.dir)
    rows = report(states)
    if not states:
        print("no run-state checkpoints found in %s" % args.dir)
        return 2
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        header = "%-32s %5s %6s %9s %10s %8s" % (
            "workflow", "runs", "done", "escalated", "esc_rate", "avg_steps")
        print(header)
        for r in rows:
            print("%-32s %5d %6d %9d %10.2f %8.1f" % (
                r["workflow"], r["runs"], r["complete"], r["escalated"],
                r["escalation_rate"], r["avg_steps"]))
    if args.gate_escalation is not None:
        bad = [r["workflow"] for r in rows
               if r["escalation_rate"] >= args.gate_escalation]
        if bad:
            print("SLI gate FAILED (escalation >= %.2f): %s" % (args.gate_escalation, ", ".join(bad)))
            return 1
        print("SLI gate passed (escalation < %.2f for all workflows)" % args.gate_escalation)
    return 0


if __name__ == "__main__":
    sys.exit(main())
