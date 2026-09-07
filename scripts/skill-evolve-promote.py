#!/usr/bin/env python3
"""
skill-evolve-promote.py — closed, verifier-gated self-improvement loop (stdlib only).

Frontier B3 (BEYOND-LOOPS-GRAPHS.md): from a FAILING run-state, distill a change candidate,
replay it against the same workflow with the proposed patch, and PROMOTE only when the replay
verifier passes; otherwise REJECT with the evidence. Every promotion is auditable: it links the
source failing run, the distilled remedy, and the verification result.

The generic contract is: a failing run (e.g., a loop exhausting at max_iterations) implies a
calibration remedy. This pipeline proves the mechanism end-to-end on the flagship review graph:

    baseline : max_iterations=3, convergence at pass 5  -> exhausts (the failure being distilled)
    accepted : max_iterations=6                          -> converges at pass 5 (verifier pass)
    rejected : max_iterations=4                          -> still exhausts (verifier fail)

Usage:
    python3 scripts/skill-evolve-promote.py \
      --state examples/workflow-runtime/state/exhaust-run-state.json \
      --manifest examples/workflow-runtime/multi-agent-review-graph.yaml \
      --executor examples/workflow-runtime/executors/review_board.py \
      --loop review-fix-loop --field max_iterations --value 6 \
      --pass-at 5 --ledger /tmp/evolve-ledger.jsonl
Exit 0 when the replay verifier passes (candidate promoted); 1 when it fails (candidate rejected).
"""

import argparse
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from lib import safe_yaml  # noqa: E402


def _load_module(path, modname):
    spec = importlib.util.spec_from_file_location(modname, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_runner_module():
    return _load_module(os.path.join(ROOT, "scripts", "workflow-runner.py"), "workflow_runner")


def distill(state, path):
    """Raw-material candidate from a failing run-state (mirrors skill-evolve-prep.py)."""
    digest = hashlib.sha256(open(path, encoding="utf-8").read().encode()).hexdigest()[:12]
    escalations = [
        {"step": e.get("step"), "action": e.get("action"), "detail": e.get("detail")}
        for e in state.get("log", []) if e.get("action") in ("escalate", "guardrail")]
    return {
        "candidate_id": "%s-%s" % (state.get("workflow", "run"), digest),
        "workflow": state.get("workflow"),
        "source_run": os.path.basename(path),
        "phase": state.get("phase"),
        "escalations": escalations,
        "remedy": None,
        "verification": None,
        "promoted": False,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Distill + verifier-gated promote pipeline")
    ap.add_argument("--state", required=True, help="failing run-state checkpoint")
    ap.add_argument("--manifest", required=True, help="workflow manifest (yaml)")
    ap.add_argument("--executor", required=True, help="executor module path")
    ap.add_argument("--loop", required=True, help="loop id to patch (e.g. review-fix-loop)")
    ap.add_argument("--field", default="max_iterations", help="loop field to patch")
    ap.add_argument("--value", type=int, required=True, help="proposed value")
    ap.add_argument("--pass-at", type=int, required=True,
                    help="convergence round used by the replay executor (REVIEW_PASS_AT)")
    ap.add_argument("--ledger", help="append promotion/rejection entries (JSONL)")
    ap.add_argument("--json", action="store_true", help="print the full result as JSON")
    args = ap.parse_args(argv)

    with open(args.state, encoding="utf-8") as fh:
        failing = json.load(fh)
    candidate = distill(failing, args.state)
    if failing.get("phase") != "escalated" and not any(
            e.get("action") in ("escalate", "guardrail") for e in failing.get("log", [])):
        candidate["verification"] = {"verdict": "rejected",
                                     "reason": "source run-state shows no failure to distill"}
        print(json.dumps(candidate, indent=2, default=str) if args.json
              else "rejected: source run-state shows no failure to distill")
        return 1

    # 1) apply the proposed patch to the manifest
    text = open(args.manifest, encoding="utf-8").read()
    manifest = safe_yaml.parse(text)
    patched = False
    for lp in manifest.get("loops") or []:
        if lp.get("id") == args.loop:
            lp[args.field] = args.value
            patched = True
    if not patched:
        print("no loop %r found in %s" % (args.loop, args.manifest))
        return 2

    # 2) replay under the deterministic convergence scenario
    os.environ["REVIEW_PASS_AT"] = str(args.pass_at)
    runner_mod = _load_runner_module()
    executor = _load_module(args.executor, "workflow_executor")
    state = runner_mod.fresh_state(manifest, text, 100)
    r = runner_mod.Runner(manifest, executor, state, 100)
    summary = r.run()

    ok = (summary.get("outcome") == "complete"
          and not any(e.get("action") in ("escalate", "guardrail") for e in state.get("log", [])))
    candidate["remedy"] = {"workflow": manifest.get("name"), "loop": args.loop,
                           "field": args.field, "old": 3, "new": args.value,
                           "rationale": "loop exhausted its budget; budget from history +1"}
    candidate["verification"] = {
        "verdict": "promoted" if ok else "rejected",
        "replayed_outcome": summary.get("outcome"),
        "iterations": summary.get("iterations", {}).get(args.loop),
        "steps_used": summary.get("steps_used"),
        "escalation_free": ok,
        "replay_env": {"REVIEW_PASS_AT": args.pass_at},
    }
    candidate["promoted"] = ok
    candidate["verified_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    if args.ledger:
        with open(args.ledger, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(candidate, sort_keys=True, default=str) + "\n")

    if args.json:
        print(json.dumps(candidate, indent=2, default=str))
    else:
        v = candidate["verification"]
        print("candidate %s -> %s (replay %s, iterations=%s)"
              % (candidate["candidate_id"], v["verdict"], v["replayed_outcome"],
                 v.get("iterations")))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
