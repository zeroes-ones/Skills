## 3. Five Agent Topology Patterns

### 3.1 Supervisor (Central Controller)

```
                  ┌──────────────┐
                  │  SUPERVISOR  │
                  │  (Router +   │
                  │   Arbiter)   │
                  └──┬──┬──┬──┬──┘
                     │  │  │  │
              ┌──────┘  │  │  └──────┐
              ▼         ▼  ▼         ▼
         ┌────────┐ ┌────────┐ ┌────────┐
         │ Agent A│ │ Agent B│ │ Agent C│
         │(Code)  │ │(Review)│ │(Test)  │
         └────────┘ └────────┘ └────────┘
```

**Use when:** Task routing needs clear ownership; latency < 200ms per delegation; 3-12 agents.

**Anti-pattern:** Supervisor becomes bottleneck — delegate only routing, never computation.

**LangGraph implementation:**

```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

class SupervisorState(TypedDict):
    messages: list
    next_agent: str
    task_result: dict

def supervisor_router(state: SupervisorState) -> Literal["coder", "reviewer", "tester", "END"]:
    if state["task_result"].get("done"):
        return "END"
    return state["next_agent"]

graph = StateGraph(SupervisorState)
graph.add_node("supervisor", supervisor_node)
graph.add_node("coder", coder_node)
graph.add_node("reviewer", reviewer_node)
graph.add_node("tester", tester_node)
graph.add_conditional_edges("supervisor", supervisor_router, {
    "coder": "coder", "reviewer": "reviewer",
    "tester": "tester", "END": END
})
```

### 3.2 Hierarchical (Tree Delegation)

```
                   ┌──────────────┐
                   │    ORCH      │
                   │  (Planner)   │
                   └──┬────────┬──┘
                      │        │
              ┌───────┘        └───────┐
              ▼                        ▼
        ┌──────────┐            ┌──────────┐
        │Sub-Orch 1│            │Sub-Orch 2│
        │(Frontend)│            │(Backend) │
        └──┬───┬───┘            └──┬───┬───┘
           │   │                   │   │
      ┌────┘   └────┐         ┌────┘   └────┐
      ▼             ▼         ▼             ▼
   ┌──────┐    ┌──────┐   ┌──────┐    ┌──────┐
   │React │    │CSS   │   │API   │    │DB    │
   │Agent │    │Agent │   │Agent │    │Agent │
   └──────┘    └──────┘   └──────┘    └──────┘
```

**Use when:** Complex decomposition across domains; sub-orchestrators own context boundaries; 5-30 agents.

**Key rule:** Each sub-orchestrator serializes state before passing up — never pass mutable references across tree levels.

### 3.3 Peer-to-Peer (Message Passing)

```
    ┌────────┐    message     ┌────────┐
    │ Agent A│───────────────▶│ Agent B│
    │(Design)│◀───────────────│(Build) │
    └────────┘    response    └────────┘
         │                          │
         │    ┌────────┐           │
         └───▶│ Agent C│◀──────────┘
              │(Verify)│
              └────────┘
```

**Use when:** Independent verification; horizontal scaling; no single point of coordination.

**AutoGen implementation:**

```python
from autogen import ConversableAgent, GroupChat, GroupChatManager

designer = ConversableAgent("designer", system_message="Design architecture")
builder = ConversableAgent("builder", system_message="Build implementation")
verifier = ConversableAgent("verifier", system_message="Verify correctness")

groupchat = GroupChat(
    agents=[designer, builder, verifier],
    messages=[],
    speaker_selection_method="round_robin",
    max_round=12
)
manager = GroupChatManager(groupchat)
```

### 3.4 Debate (Adversarial Refinement)

```
    ┌──────────┐    critique    ┌──────────┐
    │Proposer  │───────────────▶│ Critic   │
    │Agent     │◀───────────────│ Agent    │
    └──────────┘    revision    └──────────┘
         │                           │
         └─────────┬─────────────────┘
                   ▼
            ┌──────────────┐
            │  ARBITER     │
            │ (Convergence │
            │   Check)     │
            └──────────────┘
```

**Use when:** High-stakes architectural decisions; adversarial validation; diminishing-returns detection required.

**Key rule:** Always configure `max_debate_rounds` (default 5) and `improvement_threshold` (0.05 delta). Without these, two agents will iteratively "improve" past optimal ($30K+ token waste).

### 3.5 Swarm (Emergent Specialization)

```
    ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
    │ A │  │ B │  │ C │  │ D │  │ E │   <- identical agents
    └─┬─┘  └─┬─┘  └─┬─┘  └─┬─┘  └─┬─┘
      │       │       │       │       │
      └───────┴───┬───┴───────┴───────┘
                  ▼
          ┌──────────────┐
          │ SHARED TASK  │
          │    QUEUE     │
          └──────────────┘
```

**Use when:** Parallel exploration; identical agents self-assign subtasks; 10-100+ agents.

**OpenAI Swarm implementation:**

```python
from swarm import Swarm, Agent

def transfer_to_database(): return database_agent
def transfer_to_frontend(): return frontend_agent

orchestrator = Agent(
    name="Orchestrator",
    instructions="Route based on task domain",
    functions=[transfer_to_database, transfer_to_frontend]
)
client = Swarm()
response = client.run(agent=orchestrator, messages=[{"role": "user", "content": task}])
```
