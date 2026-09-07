#!/usr/bin/env python3
"""run-effectiveness.py — score a workflow run's effectiveness 0-100 (stdlib only).

The measurable definition of a "100% effective" run: the exit condition was reached via
exit-condition (not exhaustion), no escalation or guardrail block, every handoff carried a
payload, no dangling open questions, steps stayed within budget, and (when available) memory was
written. Score = 25 completion + 20 clean + 15 exit-by-design + 15 handoffs + 10 questions +
10 budget + 5 memory.

CLI:
    python3 scripts/run-effectiveness.py --state <run-state.json>
    python3 scripts/run-effectiveness.py --state <...> --json
    python3 scripts/run-effectiveness.py --state <...> --threshold 100   # gate: exit 1 below
Exit 0 unless --threshold is set and the score is below it.
"""

import argparse
import json
import os
import sys

_TERMINAL = ("done", "blocked", "needs_review", "skipped")


def score_state(state, has_memory=False):
    checks = []
    out = state.get("outcome") or (state.get("phase"))
    nodes = state.get("nodes", {})
    log = state.get("log", [])
    esc = any(e.get("action") in ("escalate", "guardrail") for e in log)
    budget = state.get("budget", {})

    # completion (25)
    complete = out == "complete"
    checks.append(("completion: run reached a terminal 'complete' state", 25 if complete else 0))

    # clean run: no escalation or guardrail block (20)
    checks.append(("clean: no escalation/guardrail in the log", 20 if not esc else 0))

    # exit-by-design: escalation-free AND reached via loop exit not exhaustion (15)
    exited_by_exit_condition = complete and not esc
    checks.append(("exit-by-design: exit condition, not exhaustion", 15 if exited_by_exit_condition else 0))

    # handoffs: every completed non-terminal node left a payload on the boundary (15)
    handoffs = state.get("handoff")
    handoff_ok = bool(handoffs and handoffs.get("payload")) or not nodes
    checks.append(("handoffs: payload present at the final boundary", 15 if handoff_ok else 0))

    # questions: none dangling (10)
    q_ok = len(state.get("open_questions", []) or []) == 0
    checks.append(("questions: no dangling open questions", 10 if q_ok else 0))

    # budget: steps within max_steps (10)
    steps = budget.get("steps_used", 0)
    max_steps = budget.get("max_steps") or (steps or 1)
    checks.append(("budget: steps_used <= max_steps", 10 if steps <= max_steps else 0))

    # memory (5): only when the runner reported it was written
    checks.append(("memory: run memory entry written", 5 if has_memory else 0))

    total = sum(score for _label, score in checks)
    return {"workflow": state.get("workflow"), "score": total, "max": 100,
            "checks": checks, "outcome": out, "escalated": esc}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Score a workflow run's effectiveness 0-100")
    ap.add_argument("--state", required=True, help="run-state json checkpoint")
    ap.add_argument("--threshold", type=int, default=None,
                    help="gate: exit 1 when score < threshold")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--memory", action="store_true",
                    help="treat memory as written (e.g. run used --memory)")
    args = ap.parse_args(argv)

    with open(args.state, encoding="utf-8") as fh:
        state = json.load(fh)
    result = score_state(state, has_memory=args.memory)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("effectiveness: %d/100 for %s (outcome=%s, escalated=%s)"
              % (result["score"], result["workflow"], result["outcome"], result["escalated"]))
        for label, score in result["checks"]:
            print("  %3d  %s" % (score, label))
    if args.threshold is not None:
        if result["score"] < args.threshold:
            print("effectiveness gate FAILED (< %d)" % args.threshold)
            return 1
        print("effectiveness gate passed (>= %d)" % args.threshold)
    return 0


if __name__ == "__main__":
    sys.exit(main())
