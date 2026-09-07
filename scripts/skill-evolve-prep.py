#!/usr/bin/env python3
"""
skill-evolve-prep.py — collect failure traces from run-states into a draft-inbox (stdlib only).

Frontier B3 (BEYOND-LOOPS-GRAPHS.md): the trace -> candidate step of self-improvement. This
script scans workflow run-state checkpoints and, for every run that shows an escalation, a
guardrail block, or a blocked/needs_review node, emits one DRAFT candidate record into the
inbox. A candidate is NOT a promoted change: it is the auditable raw material (source run,
failed nodes, evidence, escalation log) that a later distiller + verifier-gated promotion would
use (replay against the recorded trajectories, pass golden evals, only then promote).

CLI:
    python3 scripts/skill-evolve-prep.py --state FILE [--state FILE ...]
    python3 scripts/skill-evolve-prep.py --dir DIR            # scan *.json recursively
    python3 scripts/skill-evolve-prep.py --state FILE --out inbox.json

Exit 0. Prints a summary; --out writes the candidates array to a file.
"""

import argparse
import hashlib
import json
import os
import sys

BLOCKING_ACTIONS = ("escalate", "guardrail")
BAD_STATUSES = ("blocked", "needs_review")


def _is_failure(state):
    """True when the run-state reflects a failure worth distilling from."""
    phase = state.get("phase")
    if phase == "escalated":
        return True
    if any(e.get("action") in BLOCKING_ACTIONS for e in state.get("log", [])):
        return True
    if any(rec.get("status") in BAD_STATUSES for rec in state.get("nodes", {}).values()):
        return True
    return False


def candidate_from_state(path, state):
    """Build one draft-inbox candidate from a failing run-state."""
    source = state.get("workflow", "run")
    digest = hashlib.sha256(open(path, encoding="utf-8").read().encode()).hexdigest()[:12]
    failed_nodes = [
        {"id": nid, "status": rec.get("status"), "verdict": rec.get("verdict"),
         "evidence": rec.get("evidence") or []}
        for nid, rec in sorted(state.get("nodes", {}).items())
        if rec.get("status") in BAD_STATUSES or rec.get("verdict") == "guardrail-blocked"]
    escalations = [
        {"step": e.get("step"), "action": e.get("action"), "detail": e.get("detail")}
        for e in state.get("log", []) if e.get("action") in BLOCKING_ACTIONS]
    return {
        "candidate_id": "%s-%s" % (source, digest),
        "source_run": os.path.basename(path),
        "workflow": source,
        "manifest_sha": state.get("manifest_sha"),
        "failed_nodes": failed_nodes,
        "escalations": escalations,
        "open_questions": state.get("open_questions", []),
        "hypothesis": None,        # filled by the distiller step
        "promoted": False,         # promotion is verifier-gated (replay + golden evals)
        "trace_ref": path,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Collect failure traces into a self-improvement inbox")
    ap.add_argument("--state", action="append", default=[], help="run-state checkpoint(s)")
    ap.add_argument("--dir", help="directory scanned recursively for run-state *.json")
    ap.add_argument("--out", help="write candidates array to this file")
    ap.add_argument("--json", action="store_true", help="print candidates as JSON")
    args = ap.parse_args(argv)

    paths = list(args.state)
    if args.dir:
        for root, _dirs, files in os.walk(args.dir):
            for f in files:
                if f.endswith(".json"):
                    paths.append(os.path.join(root, f))

    candidates = []
    skipped = 0
    for path in sorted(paths):
        try:
            with open(path, encoding="utf-8") as fh:
                state = json.load(fh)
        except (OSError, ValueError):
            skipped += 1
            continue
        if not isinstance(state, dict) or "workflow" not in state:
            skipped += 1
            continue
        if _is_failure(state):
            candidates.append(candidate_from_state(path, state))

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(candidates, fh, indent=2, default=str)
    if args.json:
        print(json.dumps(candidates, indent=2, default=str))
    print("inbox: %d candidate(s) from %d run-state(s) (%d skipped)"
          % (len(candidates), len(paths), skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
