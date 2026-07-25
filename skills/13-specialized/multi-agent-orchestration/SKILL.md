---
name: multi-agent-orchestration
description: Use when designing multi-agent systems with specialized micro-agents, selecting topology patterns (supervisor/hierarchical/peer-to-peer/debate/swarm) for task execution, implementing typed shared state with LangGraph TypedDict checkpoints or CrewAI Pydantic task outputs, configuring agent delegation protocols with capability-based routing and fallback chains, resolving conflicts between agents via voting/supervisor-override/consensus/escalation, or instrumenting observability across agent-to-agent handoffs. Handles 5 topology patterns (Supervisor for centralized task routing with clear ownership, Hierarchical for complex decomposition with domain-specific sub-agents, Peer-to-Peer for independent verification with message passing, Debate for adversarial refinement with critic-agent feedback loops, Swarm for emergent specialization with role self-organization), typed shared state architecture (LangGraph TypedDict with checkpoint-based persistence for graph-node state transitions, CrewAI Pydantic BaseModel for structured task output contracts, AutoGen ConversableAgent message-bus for event-driven coordination), agent delegation protocol (task decomposition by complexity/domain, capability matching against agent skill manifest, handoff routing with explicit state serialization per agent-handoff-protocol, fallback chain configuration with N-retry and escalation timeout), state synchronization across sequential agent calls (checkpoint-based LangGraph with conditional edges, message-bus event sourcing for replay, shared-memory with distributed lock for write-after-read safety), conflict resolution strategies (simple majority voting for low-stakes decisions, supervisor override for deadline-pressure, consensus threshold with 2/3 quorum for architecture choices, escalation path to human-in-the-loop for budget-exceeding decisions), and failure mode prevention (hallucination cascade detection via inter-agent consistency check, state corruption guard with cryptographic hash of handoff payload, infinite delegation loop prevention via max-depth counter and cycle detection). Do NOT use for single-agent workflow design (use agent-handoff-protocol), LLM prompt engineering (use llm-engineer), distributed systems design (use system-architect), or microservices orchestration (use devops-engineer).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: framework
status: stable
version: 1.0.0
updated: 2026-07-24
tags: [multi-agent, orchestration, langgraph, crewai, autogen, state-synchronization, topology]
token_budget: 4700
chain:
  consumes_from:
    - agent-handoff-protocol
    - system-architect
    - llm-engineer
  feeds_into:
    - agent-eval-pipeline
    - backend-developer
    - platform-engineer
---

# Multi-Agent Orchestration

## Route the Request
Route multi-agent design through the topology patterns in Section 3 and decision trees in Section 11. If < 3 agents, use Section 11 for simple delegation. If ≥ 3 agents, use full topology + typed state from Sections 3-4.

## Ground Rules — Read Before Anything Else
Never let agents share mutable state without a typed schema. Never delegate without explicit success/failure contracts. Never run agents without observability instrumentation. Never exceed 3 delegation hops — use flat topologies. State corruption in multi-agent systems costs $100K+ per incident.

### Anti-Hallucination Ground Rules
- **Admit uncertainty**: If you are unsure about any API, version, configuration, or domain-specific fact, state "I am not certain about X — consult [authoritative source]" rather than guessing.
- **Flag your knowledge cutoff**: State "My training data ends in [date]. Verify current documentation for any version-specific details or newly released features."
- **Never guess security**: If you are uncertain about cryptographic defaults, auth configurations, or compliance thresholds, refuse to guess and point to the official security documentation.
- **VERIFIED**: Mark all definitive claims with **[VERIFIED]** when confirmed by documentation. Mark uncertain claims with **[BEST-KNOWN]** and provide the citation path to verify.

## 
## The Expert's Mindset
You design agent systems assuming every handoff will fail. You enforce typed contracts, idempotent delegation, and cost-aware topology selection. You treat agent output as stochastic — never deterministic.

## Operating at Different Levels
- **2-3 agents:** Simple supervisor or sequential topology
- **5-10 agents:** Hierarchical with typed state and LangGraph
- **10-50+ agents:** Swarm with CrewAI/AutoGen, cost-optimized routing
- **Cross-team:** Federation with agent-handoff-protocol handoff contracts

## When to Use
Use when designing multi-agent systems with 3+ collaborating agents, debugging agent state corruption, optimizing multi-agent costs, or scaling from prototype to production agent swarms.

## Decision Trees
See Section 11 (Decision Trees) for structured topology selection, state management, delegation mode, and cost optimization decisions.

## Core Workflow
Topology selection → typed state schema → agent delegation contracts → state synchronization → observability → cost optimization → failure mode testing.

## Cross-Skill Coordination
- **agent-handoff-protocol:** State serialization and handoff contracts
- **context-compaction-strategies:** Token budget management across agents
- **agent-eval-pipeline:** Multi-agent behavioral evaluation
- **mcp-management:** Shared MCP server configuration

## Proactive Triggers
- "add another agent" → Ask: What topology? What state contract?
- "agents disagree" → Surface: Conflict resolution pattern (Section 7)
- "agent costs rising" → Audit: Delegation loops, hallucination cascades


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "multi-agent-orchestration",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like
All agents share typed state via LangGraph/Pydantic. Every delegation has idempotency and timeout. Full OpenTelemetry traces across agent boundaries. Cost per task is measured and optimized. Zero silent state corruption.

## Deliberate Practice
Design a 5-agent hierarchical topology for a code review pipeline. Implement typed shared state in LangGraph with Pydantic schemas. Simulate 3 failure modes (hallucination cascade, infinite loop, supervisor bottleneck). Build a cost dashboard tracking tokens-per-task across agents.

## References
See the References section at the end of this skill and references/ directory for deep-dive reference files on LangGraph, CrewAI, AutoGen, and swarm patterns.

## 1. Problem Statement

Multi-agent systems fail silently without deliberate orchestration. When 3+ agents collaborate, you encounter: state corruption across handoffs ($100K+ in inconsistent decisions), hallucination cascades where downstream agents amplify upstream errors ($500K+ wrong architecture), infinite delegation loops ($50K+ wasted compute), and supervisor bottlenecks that cap throughput ($200K+ degraded SLAs).

This skill provides the architecture, protocols, and failure mode prevention to build production multi-agent systems across LangGraph 0.2+, CrewAI 0.30+, AutoGen 0.4+, and OpenAI Swarm.

**Portability target:** All patterns work with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI.

## 2. Quick Reference Card

| Concern | LangGraph | CrewAI | AutoGen |
|---------|-----------|--------|---------|
| State model | TypedDict + checkpoint | Pydantic BaseModel | Message-bus dict |
| Topology | Graph edges | Hierarchical crew | ConversableAgent group |
| Sync mechanism | Channel-based + checkpoint | Sequential task output | Publish/subscribe |
| Delegation | Conditional edges | Task delegation | handoff() method |
| Conflict resolution | Custom reducer | Manager LLM | GroupChat selector |
| Trace/audit | LangSmith/LangFuse | CrewAI telemetry | AutoGen runtime log |

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

## 5. Agent Delegation Protocol

### 5.1 Task Decomposition

```
Input Task
    │
    ├── Complexity < threshold? ──yes──▶ Single agent
    │
    └── Complexity >= threshold?
            │
            ├── Domain = frontend? ──▶ Frontend specialist
            ├── Domain = backend?  ──▶ Backend specialist
            ├── Domain = data?     ──▶ Data specialist
            └── Cross-cutting?     ──▶ Orchestrator decomposes
```

### 5.2 Capability Manifest

```yaml
agents:
  - id: frontend-specialist
    capabilities: [react, next.js, tailwind, accessibility]
    context_window: 128k
    avg_latency_ms: 1200
    cost_per_1k_tokens: 0.003
  - id: backend-specialist
    capabilities: [fastapi, postgres, redis, auth]
    context_window: 200k
    avg_latency_ms: 900
    cost_per_1k_tokens: 0.005
```

### 5.3 Handoff Protocol

```python
from dataclasses import dataclass
from hashlib import sha256
import json

@dataclass
class AgentHandoff:
    source_agent: str
    target_agent: str
    task: dict
    state_snapshot: dict
    delegation_depth: int
    max_depth: int = 5
    handoff_id: str = ""

    def __post_init__(self):
        payload = json.dumps(self.state_snapshot, sort_keys=True)
        self.handoff_id = sha256(payload.encode()).hexdigest()[:16]

    def is_valid(self) -> bool:
        return self.delegation_depth < self.max_depth
```

### 5.4 Fallback Chain

```
Primary agent (capability match)
    │
    ├── Success (latency < 2s)? ──▶ Return result
    │
    └── Timeout/Failure?
            │
            ├── Retry 1 (same agent, warm context)
            ├── Retry 2 (same agent, clean context)
            │
            └── Retries exhausted?
                    │
                    ├── Fallback agent (wider capability)
                    │       │
                    │       └── Success? ──▶ Return with "degraded" flag
                    │
                    └── Fallback fails?
                            │
                            └──▶ Escalate to Human-in-the-Loop
```

## 6. State Synchronization Strategies

| Strategy | Mechanism | Consistency | Latency | When |
|----------|-----------|-------------|---------|------|
| Checkpoint | LangGraph MemorySaver/SqliteSaver | Strong (serialized at edge) | +50ms | Sequential pipelines |
| Event-sourcing | AutoGen message-bus replay | Eventual (replayable) | +10ms | Async coordination |
| Shared-memory | Redis/Memcached with distributed lock | Locked read-after-write | +5ms | Parallel agent pools |

**Synchronization protocol:**

```python
def sync_after_handoff(from_agent: str, to_agent: str, state: AgentState):
    state["handoff_hash"] = sha256(json.dumps(state).encode()).hexdigest()[:16]
    state["delegation_depth"] += 1
    if state["delegation_depth"] > state.get("max_depth", 5):
        raise DelegationDepthExceeded(state["delegation_depth"])
    checkpointer.put(state["handoff_hash"], deepcopy(state))
    return state
```

## 7. Conflict Resolution Patterns

### 7.1 Resolution Ladder

```
DISAGREEMENT DETECTED
    │
    ├── Step 1: Simple Majority Vote ──▶ Resolved? ──▶ Continue
    │   │
    │   └── Deadlock?
    │
    ├── Step 2: Weighted Vote (senior agents 2x)
    │   │
    │   └── Deadlock?
    │
    ├── Step 3: Supervisor Override
    │   │
    │   └── Budget > threshold?
    │
    └── Step 4: Human-in-the-Loop
            │
            └── Escalate with full context + options
```

### 7.2 Resolution Strategies

| Strategy | Agent Count | Latency | Risk Profile |
|----------|------------|---------|-------------|
| Simple majority (≥3 agents) | 3+ | Low | Low-medium |
| 2/3 consensus quorum | 3+ | Medium | Low |
| Supervisor override | Any | Low (biased) | Medium-high |
| Weighted voting | 3+ | Medium | Medium |
| Human escalation | Any | High | Lowest |

```python
def resolve(agents: list, threshold: float = 0.5) -> str:
    votes = Counter(a.propose() for a in agents)
    total = len(agents)
    for option, count in votes.most_common():
        if count / total >= threshold:
            return option
    return escalate_to_human(votes)
```

## 8. Observability & Instrumentation

### 8.1 What to Measure

| Metric | Instrument | Threshold |
|--------|-----------|-----------|
| Inter-agent latency | handoff_start → handoff_end | < 500ms P95 |
| Delegation depth | depth counter per chain | ≤ 5 |
| State hash drift | compare hashes pre/post handoff | Must match |
| Hallucination score | cross-agent consistency check | < 0.3 divergence |
| Token consumption / agent | per-agent token counter | Budget per task |
| Idle agent time | last_active timestamp | Evict if > 30s idle |

### 8.2 Decision Audit Trail

```python
from langfuse import Langfuse

trace = Langfuse().trace(name=f"multi-agent:{task_id}")
for handoff in handoff_chain:
    span = trace.span(
        name=f"handoff:{handoff.source}→{handoff.target}",
        metadata={
            "depth": handoff.depth,
            "state_hash": handoff.hash,
            "latency_ms": handoff.latency_ms
        }
    )
    span.end()
```

## 9. Failure Modes & Prevention

### 9.1 Hallucination Cascade

**Pattern:** Agent A hallucinates → Agent B uses hallucinated output → Agent C amplifies → cascading wrong decisions.

**Detection:**

```python
def detect_cascade(outputs: list[dict], threshold: float = 0.3) -> bool:
    for i in range(1, len(outputs)):
        consistency = cosine_similarity(
            embed(outputs[i-1]["claim"]),
            embed(outputs[i]["claim"])
        )
        if consistency < threshold:
            return True  # Cascade detected — halt and verify
    return False
```

**Prevention:** Inter-agent consistency check after every handoff. If consistency < 0.7, inject verification step before continuing.

### 9.2 State Corruption Across Handoffs

**Pattern:** Agent A mutates shared state → Agent B reads stale value → decision based on wrong state.

**Prevention:**

```python
def verify_state_integrity(handoff: AgentHandoff) -> bool:
    expected_hash = handoff.handoff_id
    actual_hash = sha256(
        json.dumps(handoff.state_snapshot, sort_keys=True).encode()
    ).hexdigest()[:16]
    return expected_hash == actual_hash
```

### 9.3 Infinite Delegation Loop

**Pattern:** Agent A → B → C → A (cycle) or unbounded depth recursion.

**Detection:**

```python
visited = set()
def delegate(current: str, target: str, state: dict):
    edge = (current, target)
    if edge in visited:
        raise InfiniteLoopError(f"Cycle detected: {edge}")
    if state["delegation_depth"] >= MAX_DEPTH:
        raise DelegationDepthExceeded(state["delegation_depth"])
    visited.add(edge)
    state["delegation_depth"] += 1
```

### 9.4 Debate Topology Indefinite Refinement

**Pattern:** Proposer and Critic iteratively "improving" past optimal without convergence check.

**Prevention:** Configure convergence guards:

```python
DEBATE_CONFIG = {
    "max_rounds": 5,
    "improvement_threshold": 0.05,  # 5% delta minimum
    "stagnation_rounds": 2,         # Halt after 2 rounds with no improvement
}
```

## 10. Cost Optimization

### 10.1 Parallel vs Sequential Decision

```
All tasks ready?
    │
    ├── Independent tasks ──▶ Execute in parallel
    │   └── Cost: sum(individual) + fan-out overhead
    │
    └── Dependent tasks ──▶ Sequential with completion gates
        └── Cost: sum(individual) + context-passing overhead
```

### 10.2 Idle Agent Eviction

```python
import time

class AgentPool:
    def __init__(self, idle_timeout: int = 30):
        self.agents = {}
        self.last_active = {}
        self.idle_timeout = idle_timeout

    def evict_idle(self):
        now = time.time()
        for agent_id, last in list(self.last_active.items()):
            if now - last > self.idle_timeout:
                self.agents.pop(agent_id, None)
                self.last_active.pop(agent_id, None)
```

### 10.3 Context Reuse

Reuse agent context when same agent handles sequential related tasks — avoids re-loading system prompts and domain context ($0.002-$0.01 saved per handoff).

## 11. Decision Trees

### 11.1 Decision Tree: Topology Selection

```
Task characteristics?
    │
    ├── Single domain, clear owner ──▶ SUPERVISOR
    │
    ├── Multiple domains, deep hierarchy ──▶ HIERARCHICAL
    │
    ├── Independent verification needed ──▶ PEER-TO-PEER
    │
    ├── High-stakes, adversarial validation ──▶ DEBATE
    │
    └── Massively parallel, emergent roles ──▶ SWARM
```

### 11.2 Decision Tree: State Persistence

```
Consistency requirement?
    │
    ├── Strong (seq. pipeline) ──▶ Checkpoint (LangGraph MemorySaver)
    │
    ├── Eventual (async agents) ──▶ Event-sourcing (AutoGen message-bus)
    │
    └── Real-time (parallel pool) ──▶ Shared-memory + distributed lock
```

### 11.3 Decision Tree: Agent Delegation Routing

```
Task received
    │
    ├── Extract: domain, complexity, dependencies
    │
    ├── Query capability manifest
    │   │
    │   ├── Exact match? ──▶ Route to specialist
    │   ├── Partial match? ──▶ Route with context enrichment
    │   └── No match? ──▶ Generalist agent + log coverage gap
    │
    ├── Set timeout (P95 latency + 2x buffer)
    │
    └── Timeout triggered?
        ├── Retry (same agent, warm context)
        └── Fallback chain escalation
```

### 11.4 Decision Tree: Conflict Resolution Escalation

```
Disagreement detected (N agents, K opinions)
    │
    ├── N >= 3 and simple majority exists? ──▶ Majority vote → RESOLVED
    │
    ├── N >= 3 but no majority?
    │   ├── Weighted vote (seniority x2) → RESOLVED if majority
    │   └── Still deadlocked? → Step 3
    │
    ├── N < 3 or deadlocked?
    │   ├── Supervisor override → DECIDED (logged as override)
    │   └── Budget > threshold? → Human escalation
    │
    └── Human escalation:
        ├── Present: options, agent reasoning, vote distribution
        └── Human decision → Record for future training
```

### 11.5 Decision Tree: Infinite Loop Detection

```
Handoff A → B initiated
    │
    ├── Check: (A, B) in visited edges?
    │   └── YES → HALT. Raise InfiniteLoopError. Log cycle path.
    │
    ├── Check: delegation_depth >= MAX_DEPTH?
    │   └── YES → HALT. Raise DelegationDepthExceeded.
    │               Escalate to human with full chain.
    │
    ├── Record edge (A, B) in visited set
    ├── Increment delegation_depth
    └── Proceed with handoff
```

### 11.6 Decision Tree: Parallel vs Sequential Execution

```
Task batch received: [T1, T2, T3, T4]
    │
    ├── Dependency graph analysis
    │   │
    │   ├── T1, T2 are independent? ──▶ Execute in parallel
    │   │
    │   ├── T3 depends on T1? ──▶ Wait for T1 completion gate
    │   │
    │   └── T4 depends on T2, T3? ──▶ Wait for both completion gates
    │
    ├── Parallel execution: fan-out to available agents
    │   └── Cost: max(individual_latency) + fan_out_overhead
    │
    └── Sequential execution: chain with state passing
        └── Cost: sum(individual_latency) + N * handoff_overhead
```

## 12. Ground Rules

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|-------------------|-------------------|
| 1 | No mutable state passed across agent boundaries | `type(state_arg) in (dict, list)` detected in handoff | Deep-copy state; pass serialized snapshot with hash |
| 2 | No delegation beyond max-depth | `delegation_depth >= MAX_DEPTH` or cycle detected | HALT chain; escalate to human with full trace |
| 3 | No agent output accepted without consistency check | `consistency_score < 0.7` between sequential outputs | Inject verification step; re-run with cross-reference |
| 4 | No supervisor computation — routing only | `supervisor_node.complexity > O(1)` or latency > 200ms | Extract computation to worker agent; supervisor routes only |
| 5 | No debate without convergence guard | `debate_rounds >= max_rounds` or `delta < threshold` for 2 rounds | HALT debate; arbiter selects best candidate |
| 6 | No handoff without state hash verification | `handoff.source_hash != handoff.target_received_hash` | Reject handoff; replay from last verified checkpoint |
| 7 | No idle agents beyond timeout | `time.now() - agent.last_active > IDLE_TIMEOUT` | Evict agent from pool; re-instantiate if needed |
| 8 | No parallel execution of dependent tasks | Dependency graph has edge between tasks in parallel batch | Sequentialize; insert completion gate |

## 13. Gotchas

1. **Supervisor bottleneck ($200K+ in degraded throughput):** Single agent routing all tasks hits latency ceiling at ~50 concurrent agents. Mitigation: Partition by domain with multiple supervisors or use hierarchical fan-out.

2. **Checkpoint state drift ($100K+ in inconsistent decisions):** 3+ sequential agents mutate shared TypedDict without checkpoint between mutations. Mitigation: Checkpoint after every handoff; verify handoff hash on receipt.

3. **Infinite delegation loop ($50K+ compute waste):** Agent A → B → C → A cycle with no detection. Mitigation: `visited` edge set + `delegation_depth` counter; halt at depth 5 or cycle.

4. **Debate indefinite refinement ($30K+ token costs):** Two agents iteratively "improving" past optimal. Mitigation: `max_rounds=5`, `improvement_threshold=0.05`, stagnation detection at 2 rounds.

5. **Hallucination cascade ($500K+ wrong architecture):** Agent B acts on Agent A's hallucinated output, compounding error across chain. Mitigation: Inter-agent consistency check with embedding similarity threshold.

6. **Missing human-in-the-loop ($250K+ unauthorized spend):** Budget-exceeding decisions auto-executed without escalation. Mitigation: Budget gate before any decision > $threshold; require human approval.

7. **State corruption on concurrent writes ($75K+ data inconsistency):** Multiple agents write to shared state without distributed lock. Mitigation: WAL (write-ahead log) or Redis distributed lock on shared state segments.

8. **Context window overflow on long chains ($20K+ truncated decisions):** Delegation chain N > 5 agents, each appending to message history → context overflow. Mitigation: Summarize state at each handoff; pass structured state, not raw messages.

## 14. Quick Start / Implementation Checklist

**Phase 1 — Design (Day 1)**
- [ ] Select topology pattern (use Decision Tree 11.1)
- [ ] Define TypedDict/Pydantic/Message schema for shared state
- [ ] Create capability manifest for all agents
- [ ] Set max_depth and timeout thresholds

**Phase 2 — Core (Day 2-3)**
- [ ] Implement handoff protocol with cryptographic hash
- [ ] Implement delegation routing with capability matching
- [ ] Configure checkpointer (LangGraph) or message-bus (AutoGen)
- [ ] Add depth counter and cycle detection

**Phase 3 — Safety (Day 3-4)**
- [ ] Implement conflict resolution ladder (vote → override → escalation)
- [ ] Add inter-agent consistency checks
- [ ] Configure debate convergence guards
- [ ] Set up human-in-the-loop escalation for budget decisions

**Phase 4 — Production (Day 4-5)**
- [ ] Instrument with LangFuse/LangSmith spans per handoff
- [ ] Add idle agent eviction
- [ ] Implement parallel execution with completion gates
- [ ] Set up PagerDuty alert on InfiniteLoopError or DelegationDepthExceeded

## Anti-Rationalization

| When you think... | Actually verify... |
|---|---|
| "My 2-agent system doesn't need topology selection" | 2 agents still need handoff protocol and state sync — choosing Supervisor vs Peer-to-Peer changes failure mode profile |
| "I'll just use dict for state; TypedDict is overkill" | Untyped dicts cause silent key errors on handoff → $100K+ downstream decisions on wrong data |
| "Infinite loops won't happen in my 3-agent flow" | Cycle detection is not optional — 3-agent cycle A→B→C→A is the most common loop topology |
| "Consensus will just emerge naturally" | Unstructured multi-agent discussion without resolution protocol → $50K+ in unproductive token consumption |
| "I don't need observability for 4 agents" | Without per-handoff tracing, debugging cross-agent errors is NP-hard — you can't reconstruct who said what |

---

## References

Detailed patterns in **references/**:
- [five-agent-topologies.md](references/five-agent-topologies.md) — Supervisor/Hierarchical/Peer/Debate/Swarm with diagrams
- [langgraph-typed-state-patterns.md](references/langgraph-typed-state-patterns.md) — TypedDict, checkpoints, conditional edges
- [crewai-pydantic-task-outputs.md](references/crewai-pydantic-task-outputs.md) — Structured output contracts
- [agent-delegation-protocol.md](references/agent-delegation-protocol.md) — Capability matching, routing, fallbacks
- [state-synchronization-strategies.md](references/state-synchronization-strategies.md) — Checkpoint vs event-sourcing vs shared-memory
- [conflict-resolution-patterns.md](references/conflict-resolution-patterns.md) — Voting, override, consensus, escalation
- [failure-mode-prevention.md](references/failure-mode-prevention.md) — Hallucination cascade, state corruption, loops
- [observability-multi-agent.md](references/observability-multi-agent.md) — Agent-level tracing, latency, audit trail
- [cost-optimization-reference.md](references/cost-optimization-reference.md) — Parallel/sequential costing, eviction patterns
- [swarm-advanced-patterns.md](references/swarm-advanced-patterns.md) — OpenAI Swarm advanced routing patterns

---

*Version 1.0.0 | Author: Sandeep Kumar Penchala | License: MIT | Built on LangGraph 0.2+, CrewAI 0.30+, AutoGen 0.4+*
