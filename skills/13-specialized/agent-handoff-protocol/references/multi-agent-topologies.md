# Multi-Agent Topologies — 5 Patterns

## Topology Selection Guide

The topology determines how agents communicate, who makes decisions, and how conflicts resolve.
Choose based on pipeline complexity, trust level, and latency tolerance.

---

## 1. Supervisor Topology

```
         ┌─────────────┐
         │  Supervisor  │
         │   (oracle)   │
         └──┬───┬───┬──┘
       ┌────┘  │   └────┐
       ▼       ▼        ▼
   ┌──────┐┌──────┐┌──────┐
   │Agent1││Agent2││Agent3│
   └──────┘└──────┘└──────┘
```

**Best for:** Sequential pipelines with clear ordering (most handoff use cases)
**Pros:** Simple routing, single source of truth, easy debugging
**Cons:** Supervisor bottleneck, single point of failure
**Handoff format:** Supervisor serializes state, routes to next agent

---

## 2. Hierarchical Topology

```
        ┌──────────┐
        │   Root   │
        └──┬────┬──┘
      ┌────┘    └────┐
      ▼              ▼
  ┌───────┐      ┌───────┐
  │ Lead  │      │ Lead  │
  └──┬──┬─┘      └──┬──┬─┘
     │  │           │  │
```

**Best for:** Complex projects with sub-teams (e.g., frontend lead + backend lead)
**Pros:** Scales to large agent counts, parallel sub-pipelines
**Cons:** Handoff across branches requires explicit contract
**Handoff format:** Leads aggregate sub-agent state, pass to peer leads

---

## 3. Peer-to-Peer Topology

```
  ┌──────┐  ────→  ┌──────┐  ────→  ┌──────┐
  │Agent1│         │Agent2│         │Agent3│
  └──────┘  ←────  └──────┘  ←────  └──────┘
```

**Best for:** Collaborative workflows (design ↔ review ↔ implement)
**Pros:** No single point of failure, bidirectional feedback
**Cons:** State sync overhead, potential for circular dependencies
**Handoff format:** Each agent reads previous agent's state, appends own decisions

---

## 4. Debate Topology

```
  ┌──────┐     ┌──────────┐     ┌──────┐
  │AgentA│────→│ Arbiter  │←────│AgentB│
  └──────┘     └──────────┘     └──────┘
                    │
                    ▼
              ┌──────────┐
              │ Decision  │
              └──────────┘
```

**Best for:** High-stakes architecture decisions, security reviews
**Pros:** Multiple perspectives, documented dissent, higher quality decisions
**Cons:** 2-3x token cost, slower, requires arbiter agent
**Handoff format:** Both agents produce state, arbiter merges with conflict resolution

---

## 5. Swarm Topology

```
  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
  │Agent1│  │Agent2│  │Agent3│  │Agent4│
  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘
     └─────────┴─────────┴─────────┘
                    │
              ┌──────────┐
              │  Shared   │
              │  State    │
              └──────────┘
```

**Best for:** Parallel exploration (code review, multi-file analysis)
**Pros:** Maximum parallelism, diverse outputs, no ordering constraints
**Cons:** Merge conflicts, duplicate work, state consistency challenges
**Handoff format:** All agents write to shared state; final merge agent resolves conflicts

## Topology Decision Matrix

| Criterion | Supervisor | Hierarchical | Peer | Debate | Swarm |
|-----------|------------|--------------|------|--------|-------|
| Token efficiency | ★★★★ | ★★★ | ★★ | ★ | ★★ |
| Decision quality | ★★★ | ★★★★ | ★★★ | ★★★★★ | ★★ |
| Fault tolerance | ★ | ★★ | ★★★★ | ★★ | ★★★★★ |
| Audit trail | ★★★★★ | ★★★★ | ★★★ | ★★★★★ | ★★ |
| Latency | ★★★★ | ★★★ | ★★★ | ★ | ★★★★★ |
