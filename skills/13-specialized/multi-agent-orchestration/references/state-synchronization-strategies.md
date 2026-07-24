# State Synchronization Strategies

Reference for multi-agent-orchestration SKILL.md — checkpoint, event-sourcing, shared-memory.

## Strategy Comparison

```
Consistency requirement?
    │
    ├── Strong (seq. pipeline) ──▶ CHECKPOINT
    │
    ├── Eventual (async agents) ──▶ EVENT-SOURCING
    │
    └── Real-time (parallel pool) ──▶ SHARED-MEMORY + LOCK
```

## 1. Checkpoint-Based (LangGraph)

```python
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string("state.db")
graph.compile(checkpointer=checkpointer)

# Invoke with thread_id for session isolation
result = graph.invoke(
    {"task": "design_schema"},
    config={"configurable": {"thread_id": "session-42"}}
)
```

**When:** Sequential pipelines, strong consistency, audit requirements.
**Cost:** +50ms per checkpoint write; storage ~1KB per snapshot.
**Gotcha:** Checkpoint every handoff — 3+ mutations without checkpoint → $100K+ drift.

## 2. Event-Sourcing (AutoGen Message Bus)

```python
from autogen import ConversableAgent

# Each message is an event — replayable
agent_a.send(
    message={"type": "state_update", "key": "schema_v2", "value": {...}},
    recipient=agent_b,
    request_reply=True
)

# Replay from event log
def replay_from(log: list[dict], target_state_index: int) -> dict:
    state = {}
    for event in log[:target_state_index + 1]:
        state[event["key"]] = event["value"]
    return state
```

**When:** Async agents, eventual consistency, debugging via replay.
**Cost:** +10ms per message; storage ~0.5KB per event.
**Gotcha:** Event log unbounded growth — configure TTL or snapshot compaction.

## 3. Shared-Memory (Redis/Memcached)

```python
import redis
r = redis.Redis()

# Write with distributed lock
with r.lock("agent_state:session-42", timeout=5):
    current = r.hgetall("agent_state:session-42")
    current["last_decision"] = json.dumps(decision)
    r.hset("agent_state:session-42", mapping=current)
```

**When:** Parallel agent pools, real-time coordination, low-latency reads.
**Cost:** +5ms for lock acquisition; Redis memory ~100KB per active session.
**Gotcha:** Write-after-read race — always use distributed lock. Without lock → $75K+ inconsistency.

## Decision Matrix

| Factor | Checkpoint | Event-Sourcing | Shared-Memory |
|--------|-----------|---------------|---------------|
| Consistency | Strong | Eventual | Locked (strong) |
| Latency overhead | +50ms | +10ms | +5ms |
| Replay/debug | Per-snapshot | Full event log | Not supported |
| Scale ceiling | 50 agents | 200+ agents | 100+ agents |
| Framework | LangGraph | AutoGen | Custom/Redis |
