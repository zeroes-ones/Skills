"""Deterministic executor for examples/workflow-runtime/workflow.yaml.

Stand-in for agentic node content: instead of an LLM running a SKILL.md, this module answers for
every node so the engine (scripts/workflow-runner.py) is testable headless. The verdict logic here
mirrors what the boundary templates would produce:

- each reviewer runs verify-node discipline: it only returns verdict "pass" when its criteria are
  met (modeled by REVIEW_PASS_ROUND);
- review-verdict aggregates the three reviewer verdicts (join: all semantics);
- fixer acts only when the aggregate verdict is changes_requested; on pass it no-ops.

Scenario control: REVIEW_SCENARIO=happy (reviewers pass from round 3) or exhaust (they never
pass, so the loop hits max_iterations and escalates to release-gate).
"""

import os

SCENARIO = os.environ.get("REVIEW_SCENARIO", "happy").strip().lower()
_PASS_AT = os.environ.get("REVIEW_PASS_AT")
PASS_ROUND = int(_PASS_AT) if _PASS_AT is not None else {"happy": 3, "exhaust": 10**6}[SCENARIO]

REVIEWER_VERDICTS = {
    "code-reviewer": {"pass": "code is clean", "fail": "naming and dead code"},
    "security-reviewer": {"pass": "no vuln findings", "fail": "authz gap in service A"},
    "qa-engineer": {"pass": "suite green", "fail": "flaky e2e on checkout"},
}


def _findings_for(node_id, verdict, round_no):
    note = REVIEWER_VERDICTS[node_id].get(verdict, REVIEWER_VERDICTS[node_id]["fail"])
    return [{"node": node_id, "round": round_no, "verdict": verdict, "note": note}]


def execute_node(node_id, state, ctx):
    round_no = ctx.get("pass", 1)

    if node_id in REVIEWER_VERDICTS:
        verdict = "pass" if round_no >= PASS_ROUND else "changes_requested"
        note = REVIEWER_VERDICTS[node_id].get(verdict, REVIEWER_VERDICTS[node_id]["fail"])
        return {
            "status": "done",
            "verdict": verdict,
            "evidence": ["%s-review-%d" % (node_id, round_no)],
            "diagnostics": [verdict, note],
            "summary": "%s round %d: %s" % (node_id, round_no, verdict),
            "artifacts": [{"name": "%s-report" % node_id, "path": "artifacts/%s.md" % node_id,
                           "sha": "a1b2c3d4e5f6", "type": "doc"}],
        }

    if node_id == "review-verdict":
        reviews = {n: state["nodes"].get(n, {}).get("verdict")
                   for n in ("code-reviewer", "security-reviewer", "qa-engineer")}
        passed = all(v == "pass" for v in reviews.values())
        return {
            "status": "done",
            "verdict": "pass" if passed else "changes_requested",
            "evidence": ["aggregate-%d" % round_no],
            "diagnostics": ["%s" % reviews],
            "summary": "aggregate verdict round %d: %s" % (round_no, "pass" if passed else "changes"),
            "artifacts": [{"name": "aggregate-verdict", "path": "artifacts/verdict.md",
                           "sha": "deadbeef0001", "type": "doc"}],
        }

    if node_id == "fixer":
        aggregate = state["nodes"].get("review-verdict", {}).get("verdict")
        if aggregate == "pass":
            return {"status": "done", "verdict": "no-op",
                    "evidence": ["fixer-noop-%d" % round_no],
                    "summary": "no fixes required in round %d" % round_no}
        return {
            "status": "done",
            "verdict": "fixed",
            "evidence": ["fixer-pass-%d" % round_no],
            "diagnostics": ["applied fixes for round %d" % round_no],
            "summary": "fixer applied changes in round %d" % round_no,
            "artifacts": [{"name": "fix-report", "path": "artifacts/fix-report.md",
                           "sha": "feedcafe000%d" % round_no, "type": "doc"}],
        }

    if node_id == "release-gate":
        # Headless stand-in for the human gate: approve and record what was reviewed.
        return {"status": "done", "verdict": "approved",
                "evidence": ["human-approval"],
                "decisions": ["release approved at review-gate"],
                "summary": "release-gate approved (headless stand-in for human review)"}

    raise KeyError("unhandled node: %s" % node_id)
