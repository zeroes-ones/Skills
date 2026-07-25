## 4. Typed Shared State Architecture

### 4.1 LangGraph TypedDict (Checkpoint-Based)

```python
from typing import TypedDict, Annotated, Sequence
from langgraph.checkpoint.memory import MemorySaver
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[str], operator.add]  # Append-only
    current_task: str
    agent_outputs: dict[str, str]  # Agent -> output mapping
    decision_log: list[dict]       # Audit trail
    delegation_depth: int          # Max-depth counter
    handoff_hash: str              # Cryptographic hash of last handoff

checkpointer = MemorySaver()
graph.compile(checkpointer=checkpointer)
```

**Checkpoint rule:** Checkpoint after every agent handoff — never let 3+ sequential mutations accumulate without persistent snapshot.

### 4.2 CrewAI Pydantic (Task Output Schema)

```python
from pydantic import BaseModel, Field
from crewai import Task

class ArchitectureDecision(BaseModel):
    component: str = Field(description="System component name")
    decision: str = Field(description="Chosen approach")
    rationale: str = Field(description="Why this approach")
    alternatives_considered: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)

task = Task(
    description="Design database schema",
    expected_output="ArchitectureDecision Pydantic model",
    output_pydantic=ArchitectureDecision
)
```

### 4.3 AutoGen Message Bus (Event-Driven)

```python
from autogen import ConversableAgent

agent_a = ConversableAgent("agent_a", llm_config={"config_list": [...]})

agent_a.send(
    message={"type": "handoff", "task": {...}, "state_hash": "sha256:abc123"},
    recipient=agent_b,
    request_reply=True
)
```
