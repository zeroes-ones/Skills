---
name: multi-agent-orchestration
description: >
  Use when designing multi-agent systems, selecting topology patterns
  (supervisor/hierarchical/peer-to-peer/debate/swarm), implementing typed shared state with
  LangGraph or CrewAI, configuring agent delegation with capability-based routing, resolving
  inter-agent conflicts, or instrumenting observability across agent handoffs. Handles 5 topology
  patterns (Supervisor, Hierarchical, Peer-to-Peer, Debate, Swarm), typed shared state (LangGraph
  checkpoints, CrewAI outputs, AutoGen message-bus), delegation protocol (task decomposition,
  capability matching, handoff routing, fallback chains), state sync (checkpoint, event sourcing,
  shared memory), conflict resolution (voting, override, consensus, HITL escalation), and failure
  prevention (hallucination cascade detection, state corruption guards, loop prevention). Do NOT use
  for single-agent workflows (use agent-handoff-protocol), LLM prompt engineering (use
  llm-engineer), distributed systems (use system-architect), or microservices orchestration (use
  devops-engineer).
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

### Operational Ground Rules

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R2** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

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

## Error Recovery

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Agent loop without a turn limit — two agents enter a negotiation pattern where Agent A asks "Are you done?", Agent B replies "Almost, one more thing," and they repeat 500 times until hitting the token limit. Half the context window is "Almost, one more thing." | $10K-$30K in wasted API costs per incident when a multi-agent conversation consumes $200 in tokens without producing output. Over a month of development iterations, this happens 5-10 times. | Set a hard maximum turn count (default: 20). Implement a convergence detector: if the last 3 turns don't produce new, actionable information, terminate the conversation and escalate. Log turn count and token usage per agent conversation as KPIs. |
| Agent delegates to another agent without passing sufficient context — Agent A says "Fix the auth bug in the user service" but doesn't pass the stack trace, the failing test case, or the git blame for the last change. Agent B starts from scratch, re-discovers the bug, and arrives at a different fix that reintroduces an older regression. | $15K-$40K per incident in redundant investigation time plus regression risk. The fix is worse than the original because the second agent lacked the context the first one had. | Implement a context pass-through protocol: every delegation message must include (1) the original problem statement, (2) what's already been tried, (3) log/error output, (4) relevant file paths with line numbers, and (5) the hypothesized root cause. Never delegate with less than these five elements. |
| Parallel agents operate on the same file without coordination — Agents A, B, and C each read `config.yaml`, each modify it differently, each write it back. Only the last write survives. The changes from A and B are silently lost. | $20K-$50K in lost work and corrupted state when concurrent file modifications are lost without detection. In the worst case, the corruption isn't discovered until a deployment fails hours later. | Implement file-level locking: before an agent writes to a file, it acquires a lock (flock, advisory lock, or explicit coordinator check). If lock is held by another agent, wait or escalate. Prefer sequential phases that operate on non-overlapping files. Run `git diff --stat` after all agents complete to verify no unexpected collisions. |
| Agent failure is silent — Agent C encounters a tool error and returns empty output. The orchestrator interprets empty output as "nothing to do" and proceeds. Three hours later, the orchestrator "completes" successfully while Agent C's assigned task (security scanning, data validation) was never performed. | $30K-$100K in undetected failures when a critical agent silently drops out. If the security scan agent fails silently, code ships un-scanned. If the data validation agent fails silently, corrupt data propagates. | Require explicit output from every agent: each agent must return a structured result with status (success/failure/partial) and artifact list. Orchestrator validates that every expected agent produced a result. Empty output = failure, not success. Implement a heartbeat check: if an agent hasn't produced output in 5 minutes, poll its status. |

## Verification Guardrails

Run these checks before declaring work complete. ALL must pass.

| # | Guardrail | Check |
|---|-----------|-------|
| V1 | Output matches specification | Compare generated output against the requirements stated at the start. Every explicit requirement must have a corresponding deliverable. |
| V2 | No broken references or links | All file references must resolve. Run `grep -oP '\]\([^)]+\)' [output] | while read link; do [ -f "$link" ] || echo "BROKEN: $link"; done`. |
| V3 | All validations pass where applicable | Run any existing test suite or verification script. `bash scripts/validate-skills.sh` if in this repository. |
| V4 | No placeholder or TODO content remains | `grep -ri 'TODO\|FIXME\|PLACEHOLDER' [output]` must return empty. |
| V5 | Error states handled | Verify error paths produce clear messages, not silent failures or stack traces. |
| V6 | Edge cases considered | Empty input, max/min values, concurrent access, boundary conditions handled or documented as out-of-scope. |
| V7 | Performance within budget | If constraints specified, verify compliance. If not, verify no unbounded loops or quadratic blowup. |
| V8 | Anti-patterns from Gotchas section avoided | Re-read Gotchas section. Verify none of the listed anti-patterns appear in the output. |

## Cross-Skill Coordination
- **agent-handoff-protocol:** State serialization and handoff contracts
- **context-compaction-strategies:** Token budget management across agents
- **agent-eval-pipeline:** Multi-agent behavioral evaluation
- **mcp-management:** Shared MCP server configuration

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | System context, integration points, architectural constraints | Before specialized implementation — understand the system it fits into |

## Proactive Triggers
- "add another agent" → Ask: What topology? What state contract?
- "agents disagree" → Surface: Conflict resolution pattern (Section 7)
- "agent costs rising" → Audit: Delegation loops, hallucination cascades

## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Supervisor agent delegates to sub-agent → sub-agent delegates back to supervisor with "I need more context" → supervisor delegates again → infinite loop burns $500 in API tokens in 8 minutes before timeout kills the pipeline | No cycle detection. Supervisor and sub-agent both have delegation as their default escalation path. When a sub-agent is uncertain, it delegates "up" — which is back to the supervisor, who delegates "down" to another sub-agent who might also delegate back. No max-depth counter | Implement max delegation depth (default: 3). Track delegation chain: agent ID → agent ID → agent ID. Reject delegation if the target agent is already in the current chain. Add a "resolve or escalate to human" terminal state — if max depth reached, the current agent must produce a best-effort answer, not delegate further | Delegation without cycle detection is an infinite money-burning machine. Every agent in the chain must know the full delegation path and refuse to create cycles. The max-depth counter is the circuit breaker — when it trips, the agent must produce output, not delegate again |
| Peer-to-peer topology: Agent A and Agent B disagree on architecture decision. Both escalate to "decide by consensus" but there's no tiebreaker — only 2 peers. Both post "waiting for consensus" and the pipeline hangs indefinitely | P2P topology requires an odd number of peers or a tiebreaker. With exactly 2 peers, a disagreement creates deadlock. No timeout on consensus — the pipeline just waits. No escalation path from peer-level deadlock to a supervisor or human | Always use odd-numbered peer groups (3, 5). Define a consensus timeout: if no agreement after 3 rounds of debate, escalate to supervisor agent or human-in-the-loop. P2P with 2 agents is not a topology — it's a deadlock architecture. Minimum viable peer group is 3 | Peer-to-peer with an even number of peers is a design bug. Every disagreement becomes a deadlock. The topology must define: how are ties broken? What's the timeout? Who escalates? Without these answers, P2P is just a distributed hang |
| TypedDict state: Agent B modifies `results.summary` field. Agent A depends on `results.summary` being in the format it wrote. Agent B's modification changes the data type from `List[str]` to `str`. Agent A's next invocation crashes with `AttributeError: 'str' object has no attribute 'append'` | Shared mutable state with no write protection. TypedDict defines the schema but doesn't prevent an agent from writing a value that breaks another agent's expectations. Agent A assumes it "owns" the `summary` field; Agent B doesn't know about this assumption because there's no field ownership model | Define field ownership in the state schema: each field has an `owner` agent and `readers` list. Readers can read but not write. Implement immutable snapshots: agents receive a frozen copy of state, not a mutable reference. Changes are collected and merged after the agent completes. Validate state schema after every agent invocation — reject state that doesn't match the contract | Shared mutable state without ownership is the root of all multi-agent bugs. TypedDict defines the shape but not the access control. Every field needs: who writes it, who reads it, and what happens when a non-owner writes it (reject with error). Schema validation after every agent turn is not optional |
| Swarm topology with 8 agents → 3 agents become idle, never assigned work. The swarm self-organizes around the first 5 agents that claim tasks; the other 3 wait for tasks that never arrive. Total cost is 8 agents' worth of tokens for 5 agents' worth of work | Swarm self-organization without load balancing. Agents claim tasks on a first-come basis. Fast-starting agents claim multiple tasks; slow-starting agents get none. No mechanism to redistribute work from overloaded to idle agents. Idle agents still consume resources | Implement work stealing: idle agents poll for unclaimed tasks and also poll for "overloaded agent" signals. Set per-agent task caps: no agent can claim more than N concurrent tasks. Add a swarm coordinator that monitors task distribution and reassigns if imbalance exceeds 2:1. Track agent utilization — idle agents should be spun down, not left polling | Swarm topology without load balancing is just paying for idle compute. Self-organization optimizes for speed, not fairness — the first agents to claim tasks get all the work. Work stealing and task caps are the minimum fairness mechanisms. An idle agent that's not contributing should be decommissioned, not left burning tokens |
| Hallucination cascade: Agent 1 fabricates an API endpoint (`/api/v2/users/bulk-delete`). Agent 2 builds a client library with that endpoint. Agent 3 writes integration tests. Agent 4 deploys to staging. The endpoint doesn't exist — it was hallucinated. Entire pipeline produces working code for a non-existent API | No inter-agent fact verification. Each agent trusts the previous agent's output as ground truth. Agent 1's hallucination propagates through the chain because no agent independently verifies external facts. The pipeline optimizes for internal consistency, not external correctness | Implement verification checkpoints: agents that consume external API descriptions must verify them against actual API specs or live endpoints. Cross-validation: when Agent 2 receives an API endpoint from Agent 1, it must call `GET /api/v2/openapi.json` to verify the endpoint exists. Consensus check: if 2+ agents independently resolve the same fact and disagree, flag for human review | A hallucination in a single-agent system produces wrong output. In a multi-agent system, it produces a cascade of wrong outputs that all agree with each other — internally consistent, externally false. Verification checkpoints between agents are the only defense against hallucination propagation |
| Conflict resolution with majority vote: 5 agents vote on architecture decision. Result: 2 for option A, 2 for option B, 1 abstains ("insufficient context"). Pipeline hangs waiting for a majority that will never come. Timeout kills the pipeline with no decision and no fallback | Voting requires a majority threshold but the pipeline didn't define what happens when no majority is reached. 5 agents with 3 options is a common deadlock scenario. No tiebreaker, no timeout escalation, no "supervisor override" fallback | Define a decision ladder: (1) Unanimous → decide. (2) 2/3 supermajority → decide. (3) Simple majority with tiebreaker → supervisor agent decides. (4) No majority after timeout → escalate to human. Set a per-decision timeout: 3 debate rounds or 10 minutes. The pipeline must never hang — it must always produce a decision or an escalation | Voting systems need tiebreakers. The failure mode of majority voting with even numbers is not "bad decision" — it's "no decision." Every voting mechanism must define the fallback when the vote fails: supervisor override, human escalation, or default-to-safest-option. A hung pipeline is worse than a suboptimal decision |

## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
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
<!-- COMPRESSED: Full 166 lines extracted to references/3-five-agent-topology-patterns.md -->

### 3.1 Supervisor (Central Controller)

```
                  ┌──────────────┐
                  │  SUPERVISOR  │
...
> 📎 **Full content (166 lines):** [references/3-five-agent-topology-patterns.md](references/3-five-agent-topology-patterns.md)

## 4. Typed Shared State Architecture
<!-- COMPRESSED: Full 57 lines extracted to references/4-typed-shared-state-architecture.md -->

### 4.1 LangGraph TypedDict (Checkpoint-Based)

```python
from typing import TypedDict, Annotated, Sequence
from langgraph.checkpoint.memory import MemorySaver
...
> 📎 **Full content (57 lines):** [references/4-typed-shared-state-architecture.md](references/4-typed-shared-state-architecture.md)

## 5. Agent Delegation Protocol
<!-- COMPRESSED: Full 81 lines extracted to references/5-agent-delegation-protocol.md -->

### 5.1 Task Decomposition

```
Input Task
    │
...
> 📎 **Full content (81 lines):** [references/5-agent-delegation-protocol.md](references/5-agent-delegation-protocol.md)

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
<!-- COMPRESSED: Full 69 lines extracted to references/9-failure-modes-prevention.md -->

### 9.1 Hallucination Cascade

**Pattern:** Agent A hallucinates → Agent B uses hallucinated output → Agent C amplifies → cascading wrong decisions.

**Detection:**
...
> 📎 **Full content (69 lines):** [references/9-failure-modes-prevention.md](references/9-failure-modes-prevention.md)

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
