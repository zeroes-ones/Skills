# Cost Optimization for Multi-Agent Systems

## Token Cost Model
- **Agent initialization:** Fixed cost per agent start (~500-2K tokens)
- **Per-turn cost:** Input + output tokens per agent turn
- **Coordination overhead:** Supervisor turn cost × number of delegations
- **Merge cost:** Tokens to aggregate and validate results

## Optimization Strategies

### 1. Minimize Agent Count
Each additional agent adds fixed init cost + coordination overhead.
Optimal: 3-5 agents for most tasks.

### 2. Batch Delegations
Instead of agent-per-subtask, batch related sub-tasks to same agent.
Reduces init cost from N× to 1×.

### 3. State Pruning
Remove irrelevant context before passing to sub-agents.
Use context-compaction-strategies to reduce token waste.

### 4. Early Termination
If agent output reaches quality threshold early, stop.
Don't use max_turns if convergence happens at turn 3.

### 5. Shared Context Cache
Agents in same topology share immutable context.
Avoid re-sending same background information.

## Cost Comparison
| Topology | Agents | Init | Per-Turn | Total (10 turns) |
|----------|--------|------|----------|------------------|
| Single agent | 1 | 2K | 4K | 42K |
| Pipeline (4) | 4 | 8K | 4K | 48K |
| Fan-out (4+merge) | 5 | 10K | 16K | 170K |
| Hierarchical (1+3) | 4 | 8K | 16K | 168K |
