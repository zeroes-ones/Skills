# LangGraph Typed State Patterns

Reference for multi-agent-orchestration SKILL.md — LangGraph 0.2+ TypedDict state management.

## TypedDict State Definition

```python
from typing import TypedDict, Annotated, Sequence
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[str], operator.add]
    current_task: str
    agent_outputs: dict[str, str]
    decision_log: list[dict]
    delegation_depth: int
    handoff_hash: str
```

## Channel-Based State Updates

LangGraph uses channels with reducers to control state mutation:

| Reducer | Behavior | Use Case |
|---------|----------|----------|
| `operator.add` | Append to sequence | Message history |
| `default_reducer` | Overwrite value | Current task, routing keys |
| Custom reducer | Merge logic | Agent outputs, decision logs |

## Checkpointer Configuration

### MemorySaver (Development)
```python
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
graph.compile(checkpointer=checkpointer)
```

### SqliteSaver (Production)
```python
from langgraph.checkpoint.sqlite import SqliteSaver
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
```

### Checkpoint Strategy
- Checkpoint after every agent handoff — never accumulate 3+ mutations without checkpoint.
- Use `config["configurable"]["thread_id"]` for session isolation.
- Verify handoff hash before accepting state from previous agent.

## Conditional Edges for Routing

```python
from typing import Literal

def router(state: AgentState) -> Literal["agent_a", "agent_b", "END"]:
    if state["delegation_depth"] >= 5:
        return "END"
    return state.get("next_agent", "END")

graph.add_conditional_edges(
    "supervisor",
    router,
    {"agent_a": "agent_a", "agent_b": "agent_b", "END": END}
)
```

## Node-to-Node State Flow

```
┌─────────┐  state_snapshot  ┌─────────┐
│ Agent A │─────────────────▶│ Agent B │
│ (write) │                  │ (read)  │
└─────────┘                  └─────────┘
     │                            │
     └──────────┬─────────────────┘
                ▼
         ┌──────────────┐
         │  CHECKPOINT  │
         │  (Saver)     │
         └──────────────┘
```

## State Serialization Contract

Every node must:
1. Read state via `state["key"]` (TypedDict access)
2. Return updated state dict: `return {"key": new_value}`
3. Never mutate shared state in-place — return new dict
4. Include `handoff_hash` verification on receipt

## Gotcha: State Drift

3+ sequential nodes modifying state without intermediate checkpoints → drift.
**Fix:** Insert checkpoint node between every 2 computational nodes in long chains.
