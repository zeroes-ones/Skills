# Five Agent Topology Patterns

Reference for multi-agent-orchestration SKILL.md — detailed topology specifications.

## 1. Supervisor Topology

**Structure:** Central controller delegates tasks to worker agents, collects results, arbitrates conflicts.

```
         ┌──────────────┐
         │  SUPERVISOR  │
         │  (Router +   │
         │   Arbiter)   │
         └──┬──┬──┬──┬──┘
            │  │  │  │
     ┌──────┘  │  │  └──────┐
     ▼         ▼  ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│ Agent A│ │ Agent B│ │ Agent C│
└────────┘ └────────┘ └────────┘
```

**Strengths:** Clear ownership, simple debugging, predictable routing.
**Weaknesses:** Supervisor bottleneck at scale, single point of failure.
**Best for:** 3-12 agents, latency < 200ms/delegation, sequential pipelines.

## 2. Hierarchical Topology

**Structure:** Tree of sub-orchestrators, each owning a domain-specific agent group.

```
         ┌──────────────┐
         │    ORCH      │
         └──┬────────┬──┘
            │        │
    ┌───────┘        └───────┐
    ▼                        ▼
┌──────────┐            ┌──────────┐
│Sub-Orch 1│            │Sub-Orch 2│
└──┬───┬───┘            └──┬───┬───┘
   │   │                   │   │
   ▼   ▼                   ▼   ▼
┌──┐ ┌──┐             ┌──┐ ┌──┐
│A │ │B │             │C │ │D │
└──┘ └──┘             └──┘ └──┘
```

**Strengths:** Scales to 30+ agents, natural domain isolation, context-boundary enforcement.
**Weaknesses:** Deep chains increase latency, state serialization overhead at each level.
**Best for:** Complex decomposition across domains, 5-30 agents.

## 3. Peer-to-Peer Topology

**Structure:** Agents communicate directly via messages, no central coordinator.

```
┌────────┐ message ┌────────┐
│ Agent A│────────▶│ Agent B│
│        │◀────────│        │
└────────┘         └────────┘
     │                  │
     │    ┌────────┐    │
     └───▶│ Agent C│◀───┘
          └────────┘
```

**Strengths:** No SPOF, horizontal scaling, reduced coordination latency.
**Weaknesses:** Message ordering challenges, harder to debug, no global consistency.
**Best for:** Independent verification, async workflows, AutoGen GroupChat.

## 4. Debate Topology

**Structure:** Proposer and Critic iteratively refine, Arbiter checks convergence.

```
┌──────────┐ critique ┌──────────┐
│Proposer  │─────────▶│ Critic   │
│Agent     │◀─────────│ Agent    │
└──────────┘ revision └──────────┘
     │                      │
     └──────────┬───────────┘
                ▼
         ┌──────────────┐
         │  ARBITER     │
         └──────────────┘
```

**Strengths:** Adversarial validation, catches blind spots, high-quality final output.
**Weaknesses:** Indefinite refinement risk, high token cost, latency additive.
**Best for:** Architecture decisions, security review, high-stakes planning.
**Convergence guard:** max_rounds=5, improvement_threshold=0.05, stagnation_rounds=2.

## 5. Swarm Topology

**Structure:** Identical agents self-assign from shared task queue; emergent specialization.

```
┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐
│ A │ │ B │ │ C │ │ D │ │ E │
└─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘
  │      │      │      │      │
  └──────┴──┬───┴──────┴──────┘
            ▼
    ┌──────────────┐
    │ SHARED TASK  │
    │    QUEUE     │
    └──────────────┘
```

**Strengths:** Massively parallel, self-organizing, fault-tolerant (agent failure absorbed).
**Weaknesses:** Duplicate work possible, load balancing challenges, role convergence slow.
**Best for:** Parallel exploration, OpenAI Swarm, 10-100+ identical agents.

## Selection Matrix

| Factor | Supervisor | Hierarchical | P2P | Debate | Swarm |
|--------|-----------|-------------|-----|--------|-------|
| Agent count | 3-12 | 5-30 | 2-10 | 2-3 | 10-100+ |
| Latency tolerance | Low | Medium | Low | High | Any |
| Consistency need | Strong | Strong | Eventual | N/A | Best-effort |
| Human oversight | Low | Medium | Low | High | Low |
