# Agent Topology Patterns

## 1. Hierarchical Supervisor
```
Supervisor Agent
  ├── Worker Agent A
  ├── Worker Agent B
  └── Worker Agent C
```
- **Best for:** Complex tasks requiring coordination, uncertain sub-task boundaries
- **Overhead:** 1 extra hop (supervisor→worker→supervisor)
- **Failure mode:** Supervisor is single point of failure
- **Mitigation:** Supervisor timeout + auto-promote worker to supervisor

## 2. Sequential Pipeline
```
Agent A → Agent B → Agent C → Agent D
```
- **Best for:** Linear workflows with clear handoffs
- **Overhead:** Low (sequential, 1 active agent at a time)
- **Failure mode:** Step N failure blocks steps N+1 onward
- **Mitigation:** Checkpoint state after each step, enable restart

## 3. Parallel Fan-Out
```
        ┌── Agent B
Agent A ──┼── Agent C
        └── Agent D
        (merge back to A or supervisor)
```
- **Best for:** Independent sub-tasks, multi-perspective review
- **Overhead:** Merge cost proportional to agent count
- **Failure mode:** Merge logic complexity, partial results
- **Mitigation:** Timeout per agent, accept partial results

## 4. Peer-to-Peer Mesh
```
Agent A ↔ Agent B
  ↕        ↕
Agent C ↔ Agent D
```
- **Best for:** Collaborative problem-solving, debate/consensus
- **Overhead:** O(n²) communication, high token usage
- **Failure mode:** Circular conversations, no convergence
- **Mitigation:** Max rounds, convergence criteria

## 5. Hybrid (Hierarchical + Fan-Out)
```
Supervisor
  ├── Pipeline (A→B)
  └── Fan-Out [C, D, E] → Merge
```
- **Best for:** Complex real-world workflows
- **Overhead:** Moderate
- **Failure mode:** Compounding failures across sub-topologies
- **Mitigation:** Each sub-topology has independent failure handling
