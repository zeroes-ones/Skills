# Google ADK Patterns

> Agent Development Kit (ADK) — Google's open-source agent framework, available in Python,
> TypeScript, Go, Java and Kotlin. Included here because the framework matrix is otherwise
> LangChain-centric; the concepts map onto the same topology and state decisions.
> Version note: ADK 2.0 added graph workflows. Verify the API against the installed version before
> relying on these shapes — they are reference code, not a repo dependency.

---

## Core agent

```python
from google.adk import Agent
from google.adk.tools import google_search

agent = Agent(
    name="researcher",
    model="gemini-flash-latest",
    instruction="You help users research topics thoroughly.",
    tools=[google_search],
)
```

The `tools` list is the action space. Its width is a measured surface — see the
tool-overload rule in `agentic-complexity-ladder` (R7) rather than widening it by default.

## Sequential / loop / parallel workflows (the prebuilt shapes)

ADK ships template workflow agents that mirror the canonical rungs directly:

| This library's shape | ADK prebuilt |
|---|---|
| Prompt chain (Rung 2) | Sequential workflow agent |
| Loop with `exit_when` | Loop workflow agent |
| Parallel fan-out + join (Rung 4) | Parallel workflow agent |
| Routing (Rung 3) | Agent routing / conditional edges |

Use a prebuilt workflow agent before reaching for the graph API — the same "simplest rung that
works" discipline the ladder enforces.

## Graph workflows (ADK 2.0) — the bounded graph

```python
from google.adk import Workflow
from google.adk.workflow import node

def router(node_input: str):
    # classify, then emit a route
    return Event(route=["BUG"])

response_bug = node(lambda _ctx, _in: message("Handling bug..."), name="response_bug")

root_agent = Workflow(
    name="routing_workflow",
    edges=[
        ("START", process_message, router),
        (router, {
            "BUG": response_bug,
            "CUSTOMER_SUPPORT": response_support,
            "LOGISTICS": response_logistics,
        }),
    ],
)
```

This is the direct equivalent of a routing graph: a node emits a route, and a dict of edges
dispatches to the matching handler.

## Concept mapping — manifest → ADK

| Canonical concept | ADK |
|---|---|
| Manifest | `Workflow` (graph) or a prebuilt workflow agent |
| Node (skill) | A node function/agent inside `edges`, or a workflow agent |
| Edge `when:` | A router node emitting `route=[...]`; dict-dispatch edges |
| Loop with `exit_when` | Loop workflow agent, or a cycle in the graph with a route out |
| Parallel + join | Parallel workflow agent; `NewJoinNode` for explicit fan-in (Go) |
| Gate (human) | Human-input graph step |
| Run-state | Session state + events; context compression and memory |
| Guardrail at an edge | Callbacks (`before_agent`, `after_model`) and plugins |

## Language surface differences

ADK's graph API differs by language — check the installed SDK's docs rather than assuming parity:

- **Python/TypeScript**: `Workflow` + `edges` with route dicts; the samples above.
- **Go v2**: `workflow.NewFunctionNode` / `NewAgentNode` for nodes, `workflow.Chain` /
  `Concat` with `[]workflow.Edge`, `workflowagent.New` to wrap it. Conditional routing uses
  `workflow.StringRoute` / `IntRoute` / `BoolRoute` matched against `event.Routes`; fan-in uses
  `workflow.NewJoinNode`.
- **Java / Kotlin**: `LlmAgent.builder()` for single agents; graph support tracks the 2.0 line.

## Context and memory — where ADK is opinionated

ADK's stated design is that context is assembled rather than concatenated: sessions, memory, tool
outputs and artifacts are kept as structured state, older turns are summarised, and irrelevant
events are filtered. That is the same separation this library's `context-compaction-strategies`
and `agent-handoff-protocol` argue for — worth reading alongside them when choosing what crosses a
node boundary.

## Safety and evaluation surfaces

- **Callbacks and plugins** are the guardrail hook point (per-edge policy maps here).
- **Evaluation** ships criteria, user simulation and custom metrics — the ADK analogue of the
  golden-eval and judge-calibration discipline in `agent-eval-pipeline`.
- **A2A protocol** is ADK's agent-to-agent wire format; relevant when the topology spans separate
  deployments rather than a single graph.

## Known limitations (from the ADK docs)

- Some third-party integrations are **not** compatible with graph-based workflows.
- Graph workflows are newer than the template workflow agents; when a prebuilt shape fits, it is
  the lower-risk choice.

## Sourcing

Fetched from the official ADK documentation (`adk.dev`, `adk.dev/graphs/`) — verify against the
installed version, since ADK's graph API is a 2.0 addition and the multi-language surfaces differ.
