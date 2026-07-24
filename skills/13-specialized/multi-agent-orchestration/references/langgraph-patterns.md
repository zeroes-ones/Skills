# LangGraph Orchestration Patterns

## StateGraph Pattern
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class OrchestrationState(TypedDict):
    task: str
    results: Annotated[list, operator.add]
    next_agent: str
    turn_count: int

graph = StateGraph(OrchestrationState)
graph.add_node("supervisor", supervisor_node)
graph.add_node("worker_a", worker_a_node)
graph.add_node("worker_b", worker_b_node)
graph.add_conditional_edges("supervisor", router, {
    "worker_a": "worker_a",
    "worker_b": "worker_b",
    "done": END
})
graph.add_edge("worker_a", "supervisor")
graph.add_edge("worker_b", "supervisor")
```

## Conditional Routing
```python
def router(state: OrchestrationState) -> str:
    if state["turn_count"] > 10:
        return "done"
    if "security" in state["task"]:
        return "worker_a"
    return "worker_b"
```

## Sub-Graph Delegation
```python
subgraph = StateGraph(SubState).compile()
main_graph.add_node("delegated", subgraph)
```
