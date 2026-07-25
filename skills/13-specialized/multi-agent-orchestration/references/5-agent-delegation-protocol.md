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
