# LangGraph Mapping — multi-agent-review-graph

Illustrative translation of `examples/workflow-runtime/multi-agent-review-graph.yaml` into
LangGraph (StateGraph + typed state). Reference code, not a repo dependency: LangGraph is not
installed in this environment, so `graph.py` is reviewed, not executed. The mapping follows the
table in WORKFLOW-SYSTEM.md §6.

## Concept mapping

| Manifest concept | LangGraph element |
|------------------|-------------------|
| `nodes` (skills) | Graph nodes calling the skill prompt via the executor |
| `parallel: reviewers` | Parallel fan-out with a reducer on shared state; here modeled as sequential calls in one node for simplicity, matching the stdlib runner |
| `review-verdict` | Aggregate node reading the three reviewer verdicts from state |
| `review-fix-loop` + `exit_when` | Cycle with a conditional edge: on pass → `fixer` exit route; on fail + budget → back to reviewers; on fail + exhausted → `release_gate` (interrupt) |
| `release-gate` (human) | `interrupt_before` for human approval |
| `payloads: handoff-v1` | Typed state fields the payload keys map to |
| run-state + budgets | `langgraph.checkpoint.memory.MemorySaver` + explicit counters in state |

## The graph in words

1. Entry → `reviewers_node` runs code/security/qa reviewers (sequentially here; a real deployment
   fans out with `Send`/`Command` or parallel branch merges).
2. → `aggregate_node` computes join-all verdict.
3. Conditional edge from aggregate:
   - verdict `pass` → final route to the human gate (approval interrupt) then END.
   - verdict `changes_requested` and `passes < 3` → increment `passes`, route back to reviewers.
   - verdict `changes_requested` and `passes == 3` → route straight to the human gate as an
     *escalation* (with the exhaustion logged).
4. `fixer` runs between aggregate and the next review pass only when changes were requested —
   in LangGraph the fixer is a node on the loop-back path, mirroring the manifest's member order.

The key difference from the stdlib runner: LangGraph makes the *graph structure* the control flow
(cycles + conditional edges), so suppression of member edges during passes is automatic — there are
no stray parallel edges to suppress; the cycle is explicit.

## State schema sketch (typed)

```python
from typing import TypedDict, Annotated, List


def append_unique(a: List[dict], b: List[dict]) -> List[dict]:
    return a + [x for x in b if x not in a]


class ReviewState(TypedDict):
    code_verdict: str
    security_verdict: str
    qa_verdict: str
    aggregate_verdict: str
    findings: Annotated[List[dict], append_unique]   # disjoint writers, merged append-unique
    passes: int
    max_passes: int
    escalated: bool
    gate_approved: bool
```

Every field has one writer at a time (the manifest's write-ownership rule): reviewers write only
their own verdict + findings; the aggregate writes `aggregate_verdict`; the runner/graph writes
`passes`.

## Checklist when porting a manifest to LangGraph

| # | Check |
|---|-------|
| ☐ | One typed state per manifest; each field maps to one manifest `outputs`/`fields` writer |
| ☐ | Loop → explicit cycle; exit condition → conditional edge that can reach END |
| ☐ | `max_iterations` → counter in state checked on every loop-back edge |
| ☐ | Human gate → `interrupt_before`; requires-listed artifacts exist before the interrupt |
| ☐ | Payload registry keys → typed state fields; no ad-hoc fields added |
| ☐ | Escalation path mirrors `escalate_to` exactly (same target as the happy path where possible) |
| ☐ | Checkpointing on (MemorySaver/SqliteSaver) so runs resume per run-state R6 |
