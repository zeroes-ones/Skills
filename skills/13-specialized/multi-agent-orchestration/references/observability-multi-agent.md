# Observability for Multi-Agent Systems

Reference for multi-agent-orchestration SKILL.md — tracing, audit, and latency instrumentation.

## Instrumentation Layers

```
┌──────────────────────────────────────┐
│         BUSINESS METRICS             │
│  Task completion rate, cost/task     │
├──────────────────────────────────────┤
│         AGENT-LEVEL TRACING          │
│  Per-handoff spans, decision logs    │
├──────────────────────────────────────┤
│         INFRASTRUCTURE               │
│  CPU, memory, token consumption      │
└──────────────────────────────────────┘
```

## LangFuse Integration

```python
from langfuse import Langfuse
import time

langfuse = Langfuse()

def trace_handoff(source: str, target: str, task_id: str):
    trace = langfuse.trace(name=f"orchestration:{task_id}")

    span = trace.span(
        name=f"handoff:{source}→{target}",
        metadata={
            "source_agent": source,
            "target_agent": target,
            "delegation_depth": state["delegation_depth"],
            "state_hash": state["handoff_hash"],
            "latency_ms": 0  # Filled on end
        }
    )

    start = time.time()
    # ... agent execution ...
    span.update(metadata={"latency_ms": (time.time() - start) * 1000})
    span.end()
```

## Key Metrics Dashboard

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| Inter-agent latency P95 | Span duration | > 500ms |
| Delegation depth | State counter | >= 5 |
| Handoff hash mismatch | StateGuard | Any occurrence |
| Hallucination cascade score | Similarity check | < 0.7 |
| Token consumption / agent | LLM response | Budget per task |
| Idle agent duration | last_active timestamp | > 30s |
| Debate round count | Round counter | >= max_rounds |

## Decision Audit Trail

Every handoff must record:

```python
audit_entry = {
    "timestamp": time.isoformat(),
    "handoff_id": handoff_hash,
    "source_agent": source,
    "target_agent": target,
    "task": task_summary,
    "decision": agent_output,
    "confidence": confidence_score,
    "state_snapshot_hash": state_hash,
    "delegation_depth": depth,
    "latency_ms": elapsed_ms
}
```

## Alert Configuration

```yaml
alerts:
  - name: InfiniteLoopDetected
    condition: InfiniteLoopError raised
    severity: P1
    channel: pagerduty

  - name: DelegationDepthExceeded
    condition: depth >= max_depth
    severity: P2
    channel: slack + pagerduty

  - name: HallucinationCascade
    condition: consistency_score < 0.5 across 2+ handoffs
    severity: P1
    channel: pagerduty

  - name: StateCorruption
    condition: handoff_hash_mismatch
    severity: P0
    channel: pagerduty + halt_pipeline

  - name: HighLatency
    condition: P95 inter-agent latency > 500ms for 5min
    severity: P3
    channel: slack
