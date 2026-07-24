# Swarm Advanced Patterns

Reference for multi-agent-orchestration SKILL.md — OpenAI Swarm routing and emergent specialization.

## Core Swarm Pattern

```python
from swarm import Swarm, Agent

def transfer_to_agent_b():
    return agent_b

agent_a = Agent(
    name="Agent A",
    instructions="Handle frontend tasks. Transfer backend to Agent B.",
    functions=[transfer_to_agent_b]
)

agent_b = Agent(
    name="Agent B",
    instructions="Handle backend tasks only.",
)

client = Swarm()
response = client.run(
    agent=agent_a,
    messages=[{"role": "user", "content": "Build API endpoint"}],
    context_variables={"project": "ecommerce"}
)
```

## Emergent Specialization Pattern

Agents self-organize by claiming tasks from shared queue:

```
┌───┐ ┌───┐ ┌───┐ ┌───┐
│ A │ │ B │ │ C │ │ D │  ← Identical agents
└─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘
  │      │      │      │
  └──────┴──┬───┴──────┘
            ▼
    ┌──────────────┐
    │ TASK QUEUE   │
    │ [T1, T2, T3] │
    └──────────────┘
```

```python
import queue, threading

task_queue = queue.Queue()
for task in tasks:
    task_queue.put(task)

def agent_worker(agent_id: str):
    while not task_queue.empty():
        try:
            task = task_queue.get(timeout=1)
            result = execute(agent_id, task)
            results[task["id"]] = result
            task_queue.task_done()
        except queue.Empty:
            break

threads = [threading.Thread(target=agent_worker, args=(f"agent-{i}",))
           for i in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

## Load Balancing Strategies

| Strategy | Mechanism | Best For |
|----------|-----------|----------|
| Round-robin | Sequential assignment | Uniform task difficulty |
| Least-busy | Assign to agent with fewest active tasks | Variable task complexity |
| Capability-weighted | Route by agent specialization score | Heterogeneous agents |
| Random-with-backoff | Random + retry on failure | Fault tolerance |

## Context Propagation

```python
context_variables = {
    "project": "ecommerce",
    "architecture": "microservices",
    "constraints": ["budget_500k", "timeline_6mo"],
    "shared_state_hash": "abc123"
}

response = client.run(
    agent=orchestrator,
    messages=[{"role": "user", "content": task}],
    context_variables=context_variables
)

# Each agent in swarm receives same context_variables
# Agent can update via: context_variables["decision"] = "X"
```

## Anti-Patterns

1. **Duplicate work:** Multiple agents claiming same task. Use queue with atomic `.get()`.
2. **Starvation:** Slow agents hold tasks indefinitely. Use `timeout` on queue get.
3. **Context bloat:** Passing full project context to every agent. Pass only relevant subset.
4. **Missing convergence:** Swarm exploring infinitely. Set `max_tasks_per_agent` and `global_timeout`.
