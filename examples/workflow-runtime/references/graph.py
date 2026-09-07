"""Illustrative LangGraph scaffold for examples/workflow-runtime/multi-agent-review-graph.yaml.

Reference only — LangGraph is NOT a dependency of this repo and is not installed in this
environment. This file mirrors the manifest's structure (nodes, loop, conditional exit,
escalation, human gate) so teams that adopt LangGraph can translate the canonical manifest
1:1. See references/langgraph-mapping.md for the concept mapping and porting checklist.

Run (in an environment with langgraph + langchain installed):
    python3 graph.py            # builds and prints the graph structure
"""

from typing import Annotated, List, TypedDict


def append_unique(a: List[dict], b: List[dict]) -> List[dict]:
    return a + [x for x in b if x not in a]


class ReviewState(TypedDict):
    code_verdict: str
    security_verdict: str
    qa_verdict: str
    aggregate_verdict: str
    findings: Annotated[List[dict], append_unique]
    fix_report: str
    passes: int
    max_passes: int
    escalated: bool
    gate_approved: bool


# ---- node bodies (thin wrappers around the manifest's executor contract) ----
def reviewers_node(state: ReviewState) -> dict:
    """Run code/security/qa reviewers. In a real deployment these fan out in parallel and each
    writes only its own fields; the manifest declares them as the `reviewers` parallel block."""
    from examples.workflow_runtime_executor_reference import review_verdict_for  # placeholder
    pass  # real content here comes from the skill executor (see executors/review_board.py)


def aggregate_node(state: ReviewState) -> dict:
    passed = (state["code_verdict"] == "pass" and state["security_verdict"] == "pass"
              and state["qa_verdict"] == "pass")
    return {"aggregate_verdict": "pass" if passed else "changes_requested"}


def fixer_node(state: ReviewState) -> dict:
    if state["aggregate_verdict"] == "pass":
        return {"fix_report": "no-op"}
    return {"fix_report": "fix-report.md"}  # applied changes for the next pass


def should_exit(state: ReviewState) -> str:
    if state["aggregate_verdict"] == "pass":
        return "gate"                      # exit_when satisfied -> human gate
    if state["passes"] >= state["max_passes"]:
        return "gate"                      # exhaustion -> escalate_to the same gate
    return "fixer"                         # iterate: run fixer then re-review


def build_graph():
    # Only exercised where langgraph is installed; import is deferred and optional.
    from langgraph.graph import StateGraph, START, END

    g = StateGraph(ReviewState)
    g.add_node("reviewers", reviewers_node)
    g.add_node("aggregate", aggregate_node)
    g.add_node("fixer", fixer_node)
    g.add_node("release_gate", lambda s: {"gate_approved": True})  # human interrupt in prod

    g.add_edge(START, "reviewers")
    g.add_edge("reviewers", "aggregate")
    g.add_conditional_edges("aggregate", should_exit,
                            {"fixer": "fixer", "gate": "release_gate"})
    g.add_edge("fixer", "reviewers")       # loop-back = one review-fix pass
    # Human approval node: use interrupt_before in production so a person reviews the
    # fix_report + verdict artifacts required by the manifest's release-gate declaration.
    g.add_edge("release_gate", END)
    return g.compile()


if __name__ == "__main__":  # pragma: no cover - optional demo
    try:
        graph = build_graph()
        print("graph built:", type(graph).__name__)
        print("structure: START -> reviewers -> aggregate "
              "->(pass|exhaust)-> release_gate -> END | ->(fail)-> fixer -> reviewers")
    except ImportError as exc:  # langgraph not installed here — expected
        print("langgraph not installed; scaffold verified structurally only. (%s)" % exc)
