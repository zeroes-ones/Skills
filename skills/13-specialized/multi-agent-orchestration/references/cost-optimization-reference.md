# Cost Optimization for Multi-Agent Systems

Reference for multi-agent-orchestration SKILL.md — parallel execution, eviction, context reuse.

## Cost Model

```
Total Cost = Σ(agent_cost × tokens × calls) + coordination_overhead + idle_cost
```

### Per-Agent Cost Tracking

```python
from dataclasses import dataclass, field

@dataclass
class AgentCostTracker:
    agent_id: str
    total_tokens: int = 0
    total_calls: int = 0
    total_cost: float = 0.0
    idle_seconds: float = 0.0
    last_active: float = 0.0

    def record_call(self, tokens: int, cost_per_1k: float):
        self.total_tokens += tokens
        self.total_calls += 1
        self.total_cost += (tokens / 1000) * cost_per_1k
```

## 1. Parallel vs Sequential Execution

```
Task batch: [T1, T2, T3, T4]
    │
    ├── Dependency graph: T1→T3, T2→T4
    │
    ├── Wave 1 (parallel): [T1, T2]
    │   Cost: max(2 * avg_latency) = 1.2s
    │
    ├── Wave 2 (parallel): [T3, T4]
    │   Cost: max(2 * avg_latency) = 1.2s
    │
    └── Total: 2.4s vs sequential: 4.8s (50% savings)
```

```python
def schedule_tasks(tasks: list, deps: dict) -> list[list]:
    """Topological sort into parallel waves."""
    waves = []
    remaining = set(tasks)
    while remaining:
        wave = [t for t in remaining
                if all(d in completed for d in deps.get(t, []))]
        waves.append(wave)
        completed.update(wave)
        remaining -= set(wave)
    return waves
```

## 2. Idle Agent Eviction

```python
import time, threading

class AgentPoolManager:
    def __init__(self, idle_timeout: int = 30):
        self.pool = {}
        self.last_active = {}
        self.idle_timeout = idle_timeout
        self._start_eviction_loop()

    def _start_eviction_loop(self):
        def evict():
            while True:
                now = time.time()
                for aid in list(self.pool):
                    if now - self.last_active.get(aid, 0) > self.idle_timeout:
                        cost = self.pool[aid].total_cost
                        idle = now - self.last_active[aid]
                        log_eviction(aid, cost, idle)
                        del self.pool[aid]
                time.sleep(10)
        threading.Thread(target=evict, daemon=True).start()
```

## 3. Context Reuse

Reuse agent context when same agent handles sequential related tasks:

```python
class ContextCache:
    def __init__(self, ttl: int = 300):
        self.cache = {}  # agent_id → (context, timestamp)
        self.ttl = ttl

    def get_or_load(self, agent_id: str, context_loader):
        if agent_id in self.cache:
            ctx, ts = self.cache[agent_id]
            if time.time() - ts < self.ttl:
                return ctx  # Cache hit — save $0.002-$0.01
        ctx = context_loader()
        self.cache[agent_id] = (ctx, time.time())
        return ctx
```

## 4. Cost-Optimal Agent Selection

```python
def select_cost_optimal(task: dict, agents: list[dict]) -> str:
    candidates = []
    for agent in agents:
        overlap = set(task["capabilities"]) & set(agent["capabilities"])
        score = len(overlap) / len(task["capabilities"])
        est_cost = task["est_tokens"] * agent["cost_per_1k_tokens"] / 1000
        candidates.append({
            "id": agent["id"],
            "score": score,
            "est_cost": est_cost,
            "efficiency": score / max(est_cost, 0.0001)
        })
    candidates.sort(key=lambda c: c["efficiency"], reverse=True)
    return candidates[0]["id"]
```

## Optimization Checklist

- [ ] Parallelize independent subtasks — expect 40-60% latency reduction
- [ ] Evict idle agents after 30s — reclaim memory and avoid idle API costs
- [ ] Cache agent context for sequential calls — save $0.002-$0.01 per handoff
- [ ] Select agents by cost-efficiency, not just capability match
- [ ] Set per-task token budgets; alert at 80% consumption
- [ ] Track cost-per-task to identify expensive agent patterns
