# Agent Delegation Protocol

Reference for multi-agent-orchestration SKILL.md — capability-based routing and handoff chains.

## Task Decomposition Algorithm

```
Input: task_description, complexity_score, domain_tags
  │
  ├── complexity_score < 3.0: Direct route to single agent
  │
  └── complexity_score >= 3.0:
      ├── Extract subtasks by domain boundary
      ├── Order by dependency graph (topological sort)
      └── Assign each subtask to best-capability agent
```

## Capability Manifest Format

```yaml
manifest:
  version: "1.0"
  agents:
    - id: "frontend-architect"
      capabilities: ["react", "next.js", "typescript", "a11y"]
      context_window: 128000
      avg_latency_ms: 1200
      p95_latency_ms: 2400
      cost_per_1k_tokens: 0.003
      max_concurrent_tasks: 3

    - id: "backend-architect"
      capabilities: ["fastapi", "postgres", "redis", "auth"]
      context_window: 200000
      avg_latency_ms: 900
      p95_latency_ms: 1800
      cost_per_1k_tokens: 0.005
      max_concurrent_tasks: 2
```

## Capability Matching

```python
def match_agent(task: dict, manifest: list[dict]) -> str:
    scores = []
    for agent in manifest:
        overlap = set(task["required_capabilities"]) & set(agent["capabilities"])
        score = len(overlap) / len(task["required_capabilities"])
        scores.append((score, agent["id"]))
    scores.sort(reverse=True)
    if scores[0][0] >= 0.8:
        return scores[0][1]  # Strong match
    elif scores[0][0] >= 0.5:
        return scores[0][1]  # Partial match — enrich context
    return "generalist"  # No match — log coverage gap
```

## Handoff Data Structure

```python
from dataclasses import dataclass
from hashlib import sha256
import json, time

@dataclass
class Handoff:
    source: str
    target: str
    task: dict
    state_snapshot: dict
    depth: int
    max_depth: int = 5
    timestamp: float = time.time()
    handoff_hash: str = ""

    def __post_init__(self):
        payload = json.dumps(self.state_snapshot, sort_keys=True)
        self.handoff_hash = sha256(payload.encode()).hexdigest()[:16]

    def validate(self) -> bool:
        if self.depth >= self.max_depth:
            return False
        expected = sha256(
            json.dumps(self.state_snapshot, sort_keys=True).encode()
        ).hexdigest()[:16]
        return self.handoff_hash == expected
```

## Fallback Chain Configuration

```yaml
fallback:
  retry_policy:
    max_attempts: 3
    backoff: exponential  # 1s, 2s, 4s
    warm_context: true  # Retry 1 with same context
    clean_context: true # Retry 2 with fresh context

  fallback_agents:
    - id: "generalist"
      capability_threshold: 0.3  # Wide but shallow match
    - id: "human-escalation"
      condition: "task.budget > 5000 or task.criticality == 'P0'"
      sla_response_minutes: 15
