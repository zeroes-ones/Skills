---
name: system-architect
description: >
  Use when designing system architectures, making architecture decisions, modeling
  with C4, writing ADRs, evaluating microservices vs monolith trade-offs, or planning
  capacity. Handles scalability patterns, event-driven architecture, deployment
  topology design, trade-off analysis, capacity planning, and architecture governance.
  Do NOT use for hands-on coding, detailed API design, or infrastructure provisioning.
license: MIT
tags:
- architecture
- system-design
- c4
- adr
- scalability
- microservices
- event-driven
author: Sandeep Kumar Penchala
type: architecture
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  consumes_from:
  - cto-advisor
  - product-manager
  - security-engineer
  - staff-engineer
  feeds_into:
  - algorithmic-trader
  - api-designer
  - backend-developer
  - cloud-architect
  - cto-advisor
  - database-designer
  - devops-engineer
  - hardware-architect
  - idea-to-spec
  - migration-architect
  - networking-engineer
  - security-engineer
  - staff-engineer
  - technical-program-manager
---

# System Architect
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Design and evaluate system architectures through structured modeling, trade-off analysis, and architectural decision records. This skill covers end-to-end architecture from requirements to deployment topology, including C4 modeling (Context, Container, Component, Code), Architecture Decision Records (ADRs), scalability patterns, and capacity planning.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("architecture-decision-record*.md")` OR `file_exists("adr/")` OR `file_contains("*.md", "## ADR \| Architecture Decision Record\|## Decision")` | ADRs exist. Jump to **Core Workflow** — Phase 3 (ADR Writing & Review). |
| A2 | `file_contains("*", "C4\|Context.Diagram\|Container.Diagram\|structurizr\|plantuml.*container")` | Architecture diagrams exist. Jump to **Core Workflow** — Phase 4 (C4 Diagrams). |
| A3 | `file_contains("*", "microservice\|event.driven\|CQRS\|event.sourcing\|saga\|DDD.bounded.context")` AND NOT `file_contains("*", "monolith\|modular.monolith")` | Microservices/DDD architecture. Jump to **Decision Trees** — Monolith vs Microservices + **Anti-Patterns** (microservices at small scale). |
| A4 | `file_contains("*", "monolith\|modular.monolith\|single.deployable")` AND `file_contains("*", "migrat.*microservice\|split.*service\|extract.*service")` | Monolith-to-microservices migration. Jump to **Decision Trees** — Scalability Decision Tree. |
| A5 | `file_contains("*", "SLO\|SLI\|error.budget\|availability.*99\.\|latency.*p\d{2}")` | SLO/SLI concerns. Jump to **Core Workflow** — Phase 5 (SLO Architecture). |
| A6 | `file_contains("*", "capacity.plan\|load.test\|scale.*estimate\|QPS.*\d+\|throughput.*\d+")` | Capacity planning. Jump to **Core Workflow** — Phase 5 (Capacity Planning). |
| A7 | `file_contains("*", "build.vs.buy\|vendor.*select\|SaaS.*vs.*build\|platform.*decision")` | Build-vs-buy or vendor selection. Invoke **cto-advisor** instead. |
| A8 | `file_contains("*", "API.*design\|OpenAPI\|GraphQL\|gRPC\|REST.*contract")` AND NOT `file_contains("*", "system.*architect\|architecture.*decision")` | Pure API design without architecture context. Invoke **api-designer** instead. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── DESIGN something new
│   ├── Greenfield system → Start at "Decision Trees > Monolith vs Microservices"
│   ├── New service in existing system → Go to "Architecture Styles Decision Matrix"
│   └── API or integration → Invoke api-designer skill instead
├── EVALUATE or decide
│   ├── Choose between architectures → Start at "Decision Trees"
│   ├── Review an existing architecture → Go to "Core Workflow > Phase 2"
│   └── Build vs Buy decision → Invoke cto-advisor skill
├── DOCUMENT
│   ├── Write an ADR → Jump to "Core Workflow > Phase 3"
│   └── Create C4 diagrams → Jump to "Core Workflow > Phase 4"
├── SCALE or fix
│   ├── System under load → Go to "Scale Depth" section
│   ├── Refactoring legacy → Jump to references/complexity-cost-model.md
│   └── Capacity planning → Jump to "Core Workflow > Phase 5"
├── Need technology strategy and build-vs-buy → Invoke cto-advisor skill instead
├── Need product requirements and roadmap → Invoke product-manager skill instead
├── Need deep security architecture → Invoke security-engineer skill instead
├── Need API contract design → Invoke api-designer skill instead
├── Need database schema design → Invoke database-designer skill instead
├── Need network topology design → Invoke networking-engineer skill instead
└── Don't know where to start? → Describe the problem in plain language and I'll route you
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to recommend architecture without NFR context.** Before suggesting microservices or monolith, you must know: peak QPS, P95 latency budget, availability target (99.9%? 99.99%?), data volume, and team size. Architecture without quantified requirements is fashion, not engineering. | Trigger: producing an architecture recommendation (monolith/microservices/event-driven/CQRS) without citing specific NFR numbers: QPS, latency budget (ms), availability target (%), data volume, or team size | STOP. Ask: "Before recommending: What's your peak QPS? What's the P95 latency budget? What availability target do you need (99.9% = 8.76h downtime/year, 99.99% = 52min/year)? How many engineers will build and operate this? Architecture without quantified requirements is guessing — and guessing at architecture level costs millions." |
| **R2** | **REFUSE to present a single "right" answer without alternatives.** Every architecture decision is a tradeoff. Present at minimum 2 options with explicit pros, cons, and the context in which each wins. The architect's job is to illuminate the tradeoff space, not pick winners by personal preference. | Trigger: output contains exactly 1 architecture recommendation with no alternatives section, no tradeoff table, no "Alternatives Considered" heading | STOP. Insert: "**Alternatives Considered:** At minimum, present: Option A (recommended) vs Option B (next best). For each: rationale, tradeoffs, when B would be preferred. Architecture decisions without alternatives are opinions, not engineering. The right answer for a 5-person startup is wrong for a 500-person enterprise." |
| **R3** | **DETECT and WARN about architecture proposals without diagrams.** Start every architecture discussion with a C4 Context or Container diagram. A picture exposes assumptions that prose hides — missing connections, implicit dependencies, and gaps in understanding. Prose-only architecture is incomplete by definition. | Trigger: architecture proposal, ADR, or review output exceeds 500 words about system structure without including or referencing a diagram (C4, sequence, deployment, or data flow diagram) | WARN. Insert: "**Diagram Required:** Add a C4 Context diagram showing: users, external systems, the system boundary, and data flows. Use PlantUML C4 (`@startuml !include <C4/C4_Container>`), Mermaid, or Structurizr DSL. A 500-word architecture description without a diagram is a shared hallucination — every reader pictures something different." |
| **R4** | **REFUSE to recommend microservices for a team of fewer than 20 engineers on a greenfield project.** Microservices trade development speed for organizational scaling. A 5-person team with 15 services spends more time on deployment pipelines, monitoring dashboards, and inter-service debugging than on features. Start with a modular monolith and extract services only when proven necessary. | Trigger: recommending microservices architecture for a greenfield project with < 20 engineers, or a team where engineer:service ratio is < 3:1 | STOP. Reframe: "A modular monolith is the correct default for teams under 20 engineers. Benefits: 1 deploy pipeline, 1 codebase, 0 network latency between modules, simple debugging, simple transactions. Extract a service when: (1) that module has proven independent scaling needs, (2) its bounded context is stable, (3) a dedicated team will own it. Microservices are organizational scaling — you pay the cost upfront for a benefit you may never need." |
| **R5** | **DETECT and WARN about event-driven architecture without dead-letter queues.** Every event consumer without a DLQ is a silent data-loss incident waiting to happen. When the consumer is down, events are published into the void — unrecoverable, untraceable, invisible until a customer complains. | Trigger: proposing event-driven, pub/sub, or message-queue architecture without mentioning DLQ (dead-letter queue), message replay, or poison message handling for every consumer | WARN. Insert: "**DLQ Required:** Every event consumer must have: (1) Dead-Letter Queue with configurable `maxReceiveCount`, (2) alert on DLQ depth > 0, (3) message inspection UI, (4) replay mechanism, (5) retention policy (minimum 7 days). Without DLQ, a brief consumer outage = permanent data loss. Customers discover missing data before your monitoring does." |
| **R6** | **STOP and WARN about synchronous inter-service calls without timeouts, circuit breakers, retries, and bulkheads.** One slow downstream service saturates all request threads → cascading failure across the entire system. Every synchronous dependency is a bet that the downstream will respond within your timeout — and that bet must have a circuit breaker. | Trigger: proposing inter-service HTTP/gRPC calls without configuring: `timeout` (p95×2, max 30s), `circuit_breaker` (open at 50% error rate), `retry` (max 3, exponential backoff + jitter), `bulkhead` (separate thread pool) | STOP. Insert: "**Resilience Required:** Every sync call must configure: `timeout = p95_latency × 2` (max 30s), circuit breaker open at 50% error rate with 30s half-open probe, retries: max 3 with exponential backoff (100ms, 200ms, 400ms) + jitter (±25%), bulkhead: dedicated thread pool per downstream. Without these: 1 slow dependency = all users affected. This is the #1 cause of cascading production failures." |

## The Expert's Mindset

<!-- DEEP: 10+min — how masters think, not just what they do -->

### The Mental Model Shift
Competent architects design systems that meet requirements. Masters design systems that **degrade gracefully under conditions nobody predicted.** The shift: stop designing for the happy path and start designing for the failure modes. A system that works at 1000 QPS is not complete until you know what happens at 10,000 QPS, during a region outage, under a DDoS attack, and when the intern accidentally drops a production table. Architecture is the art of bounding blast radius.

### Cognitive Biases That Kill Systems
| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Resume-driven architecture** | Choosing the technology stack based on what looks good on LinkedIn rather than what the problem needs | Every technology choice must cite a measured requirement: "We need Kafka because we have 50K msg/sec with strict ordering" — not "Kafka is industry standard." |
| **Complexity-as-sophistication** | Adding microservices, event sourcing, and CQRS to a system with 3 developers and 100 users | Complexity is a cost, not a credential. The best architect is the one who solves the problem with the fewest moving parts. Add complexity only when the cost of not adding it exceeds the cost of managing it. |
| **Greenfield myopia** | Designing the perfect system assuming it will be built from scratch — ignoring the 10 existing services, 3 databases, and 2 message queues it must integrate with | Start every design with an integration map. What already exists? What must this system talk to? Greenfield systems are rare; brownfield systems are reality. |

### What Architecture Masters Know That Others Don't
- **Every component is a liability, not just an asset.** A microservice costs: infrastructure, deployment pipeline, monitoring, on-call rotation, documentation, onboarding time. Before adding a new service, ask: "What existing service can absorb this responsibility?" The best component is the one you don't build.
- **Architecture is about coupling management.** The primary job of architecture is to arrange components so that the things that change together are close together, and things that change independently are far apart. Conway's Law is not a metaphor — your org chart will become your architecture. Design both together.
- **Every architecture decision has a shelf life.** The perfect architecture for a 5-person startup is wrong for a 50-person company. The perfect architecture for 50 people is wrong for 500. Design for your current reality plus one growth stage. Beyond that, you're optimizing for a future that may never arrive.

### When to Break Your Own Rules
- **Skip the ADR for reversible decisions.** If the decision can be changed in a week with minimal blast radius, it doesn't need a formal record. ADRs are for irreversible or high-cost-reversal decisions: database choice, language choice, service boundaries. Library choice within a service? Just document in the README.
- **Ship a monolith to prove the market, then split.** If you're pre-PMF, optimize for speed of learning, not scalability. A monolith that can be refactored in a month is better architecture than microservices that took 6 months to build for a product nobody wants.

## Operating at Different Levels

Architecture decisions compound — a decision made at L2 has L4 consequences. Understanding level expectations ensures the right depth for the problem at hand.

| Level | Architecture Output Characteristics |
|---|---|
| **L1 — Apprentice** | Learns architecture patterns. Reads ADRs. Can diagram an existing system and explain the trade-offs already made. |
| **L2 — Practitioner** | Produces architecture for a single service or bounded context. Evaluates trade-offs with guidance. Writes clear, decision-focused ADRs. |
| **L3 — Senior** | Designs multi-service systems. Makes build-vs-buy and monolith-vs-microservices decisions with defensible rationale. Architecture RFCs that stand up to peer review. |
| **L4 — Staff** | Sets architecture standards for the organization. Defines technology radar, architecture principles, and governance. "This is what we mean by 'well-architected' here." |
| **L5 — Principal** | Creates architecture methodologies adopted across the industry. "Here's a new way to reason about distributed system design." |

**Usage**: Say "as an L4 architect, review the system design for..." Default: **L3** (multi-service design, independent architectural decisions).

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Designing a new system or service from scratch
- Evaluating microservices vs monolith vs modular monolith trade-offs
- Creating C4 architecture diagrams or Architecture Decision Records (ADRs)
- Planning event-driven architectures (Kafka, RabbitMQ, SNS/SQS, EventBridge)
- Capacity planning and scalability modeling (QPS, latency budgets, data volume)
- Refactoring legacy systems (strangler fig, anti-corruption layer)
- Cloud-native deployment topology design (Kubernetes, serverless, hybrid)
- Multi-tenancy strategy design (database-per-tenant, schema-per-tenant, shared)

## Decision Trees

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Monolith vs Microservices
```
                     ┌──────────────────────────┐
                     │ START: Greenfield system  │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Team <20 engineers AND     │
                    │ single tech stack?         │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Modular     │   │ Independent     │
                    │ Monolith    │   │ deploy + scale  │
                    │             │   │ needed per      │
                    │             │   │ domain?         │
                    └─────────────┘   └────┬────────┬───┘
                                           │ YES    │ NO
                                      ┌────▼────┐ ┌▼──────────┐
                                      │ Extract  │ │ Modular   │
                                      │ one      │ │ Monolith  │
                                      │ bounded  │ │ first      │
                                      │ context  │ └────────────┘
                                      │ at a time│
                                      └──────────┘
```
**When to choose Monolith:** <20 engineers, <$20M ARR, single tech stack, deploy <daily, DB CPU <50%. Shopify ran a monolith past 1M merchants. **When to extract microservices:** Independent deploy/scale proven needed, >2 teams colliding in same codebase, >50 engineers, CI >15 min.

### Synchronous vs Asynchronous Communication
```
                     ┌──────────────────────────┐
                     │ START: Service A needs    │
                     │ data/action from Service B│
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Caller needs immediate     │
                    │ response to proceed?       │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Sync (REST/ │   │ Event-driven    │
                    │ gRPC) +     │   │ (Kafka/SQS) +   │
                    │ circuit     │   │ eventual        │
                    │ breaker     │   │ consistency OK  │
                    └─────────────┘   └────────────────┘
```
**When to choose Sync:** Request-response needed within <200ms, user waiting on result, strong consistency required. **When to choose Async:** Fire-and-forget, >500ms processing, need retry/backpressure, decouple service lifecycles, eventual consistency acceptable.

### Caching Strategy
```
                     ┌──────────────────────────┐
                     │ START: P95 latency >200ms │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Same data requested >10×   │
                    │ per second with same key?  │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Add cache   │   │ Optimize query  │
                    │ layer:      │   │ or add index    │
                    │ Redis for   │   │ first           │
                    │ hot data    │   └────────────────┘
                    └────┬────────┘
                         │
                    ┌────▼────────┐
                    │ Monitor hit  │
                    │ rate — drop  │
                    │ cache if     │
                    │ <50%         │
                    └──────────────┘
```
**When to add cache:** Same key hit >10×/sec, p95 >200ms with optimized queries, data changes <1×/min, cache hit rate projected >70%. **When to remove cache:** Hit rate <50%, invalidation logic >50 lines, cache-induced bugs >1 per sprint — the cache is hurting more than helping.

### Multi-Region Deployment Strategy
```
                     ┌──────────────────────────┐
                     │ START: Global user base    │
                     │ needs <100ms latency       │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ 99.99% SLA contractually    │
                    │ required AND DAU >100K?     │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Active-     │   │ Warm standby    │
                    │ Active (DB  │   │ + DNS failover  │
                    │ multi-master│   │ (RTO <15 min,   │
                    │ or Spanner) │   │ RPO <5 min)     │
                    └─────────────┘   └────────────────┘
```
**When to choose Active-Active:** 99.99% SLA contractual, DAU >100K globally, can afford multi-master DB complexity ($500K+/yr). **When to choose Warm Standby:** 99.9% SLA, DAU <100K, RTO 15 min acceptable, want DR without multi-master complexity.

### CQRS & Event Sourcing Decision
```
                     ┌──────────────────────────┐
                     │ START: Complex domain with │
                     │ high read/write disparity  │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Need full audit trail AND  │
                    │ read:write ratio >100:1?   │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Event       │   │ CQRS without    │
                    │ Sourcing +  │   │ Event Sourcing: │
                    │ CQRS        │   │ separate read   │
                    │             │   │ models via       │
                    │             │   │ materialized     │
                    │             │   │ views           │
                    └─────────────┘   └────────────────┘
```
**When to choose Event Sourcing:** Financial/audit systems, full history required by regulation, complex state transitions, event replay needed. **When to choose CQRS-only:** Read:write >100:1, read-side query complexity high, no audit trail requirement, materialized views sufficient.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | cto-advisor | Business strategy, build-vs-buy decisions, technology radar |
| **This** | system-architect | C4 diagrams, ADRs, scalability models, deployment topology, trade-off analysis |
| **After** | api-designer | Consumes system boundaries and service topology to design API contracts |

Common chains:
- **Business to architecture**: cto-advisor → system-architect → api-designer — Strategy defines constraints, architecture designs the system, API formalizes service contracts
- **Product to operations**: product-manager → system-architect → devops-engineer — Product defines requirements, architect designs for scale and reliability, DevOps implements infrastructure

## Core Workflow

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Requirements & Constraints Gathering
1. Identify functional requirements (use cases, user journeys, data flows).
2. Capture non-functional requirements: availability (e.g., 99.99%), latency (p50/p95/p99), throughput (QPS), data consistency, compliance (SOC2, GDPR, HIPAA).
3. Document constraints: budget, team size, technology mandate, existing ecosystem, vendor lock-in posture.
4. Define Service Level Objectives (SLOs) and error budgets.

### Phase 2 (~30 min): Architecture Design & Modeling
<!-- DEEP: 10+min -->
1. **C4 Context Diagram**: System boundaries, external actors (users, third-party APIs, partner systems), data flows.
2. **C4 Container Diagram**: Deployable units (web app, API gateway, microservices, databases, message brokers, caches), communication protocols (REST, gRPC, async messaging).
3. **C4 Component Diagram** (for complex containers): Internal component structure, ports & adapters, hexagonal architecture boundaries.
4. **Data Architecture**: Storage selection (relational, document, graph, time-series, columnar), data partitioning, replication strategy, caching layers (Redis, CDN, in-memory).
5. **Communication Patterns**: Synchronous (REST/gRPC/GraphQL) vs asynchronous (event choreography, orchestration with Saga, pub/sub, CQRS, event sourcing).
6. **Deployment Topology**: Kubernetes (pod anti-affinity, HPA, cluster autoscaling, Istio service mesh) vs serverless (AWS Lambda, Cloud Run) vs traditional VMs.

### Phase 3 (~20 min): Trade-off Analysis & Decision Records
1. Write ADRs in a structured format: Title, Status (Proposed/Accepted/Deprecated/Superseded), Context, Decision, Consequences.
2. Evaluate each architectural decision against: scalability, complexity, cost, team expertise, operational burden, vendor lock-in.
3. Document rejected alternatives with rationale.
4. Maintain an architecture decision log in the repository (`docs/adr/`).

### Phase 4 (~15 min): Scalability & Capacity Planning
1. Estimate traffic: peak QPS, daily active users, data ingestion rate, read/write ratio.
2. Calculate latency budgets: break down end-to-end latency into service-level budgets.
3. Model data growth: storage requirements (1y/3y projection), hot/warm/cold tiering.
4. Design scaling strategy: vertical vs horizontal, stateless vs stateful, database read replicas, sharding key selection.
5. Identify bottlenecks: single points of failure, contention points, cascading failure risks.
6. Plan for resilience: circuit breakers, retries (with exponential backoff + jitter), bulkheads, timeouts, graceful degradation, chaos engineering.

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `cto-advisor` | Technology strategy, build-vs-buy decisions, budget constraints, organizational context | Before making irreversible architectural decisions (language, database, monolith vs microservices) |
| `product-manager` | Product requirements, feature roadmap, user personas, NFRs (latency/availability/throughput) | Before translating product needs into architecture; ensures business alignment |
| `security-engineer` | Threat model, compliance requirements (SOC2/HIPAA/GDPR), trust boundaries, encryption standards | Before designing data flows, IAM, or service communication patterns |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `api-designer` | Bounded context map, API principles, versioning strategy, communication patterns (REST/GraphQL/gRPC) | API design proceeds without bounded context clarity — cross-service contract conflicts |
| `database-designer` | Data ownership boundaries, multi-tenancy model, consistency requirements, scaling strategy | Database schema designed without service topology alignment — costly refactors |
| `networking-engineer` | Service topology, communication patterns, latency budgets, capacity projections | Network topology built without understanding service dependencies — security and latency issues |
| `backend-developer` | Service boundaries, technology stack decisions, inter-service contracts, deployment topology | Backend implemented against wrong service boundaries — architectural drift |
| `devops-engineer` | Infrastructure requirements (compute/networking/storage), scaling patterns, observability needs | Infrastructure provisioned without understanding architecture — over/under-provisioning |
| `cto-advisor` | Architecture options with tradeoff analysis, technical risk assessment, cost projections | CTO makes strategic decisions without architectural feasibility input |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| ADR (Architecture Decision Record) published | All engineering leads, CTO, Product | Key decisions affecting API, data, infrastructure, or developer workflows |
| New service or bounded context identified | API Designer, Database Designer, DevOps | API contract, database, infrastructure, CI/CD pipeline provisioning needed |
| Technology stack change | CTO, All engineering leads, DevOps, Security | Skill requirements, migration plan, operational readiness, security review |
| Architecture review finds scalability ceiling | CTO, DevOps, Performance Engineer | Capacity planning, scaling strategy, timeline before ceiling hit |
| Build-vs-buy decision needed | CTO, Product, Finance, Security | Options analysis, TCO (3yr), integration complexity, compliance implications |

### Escalation Path

```
Architecture emergency (data corruption, cascading failure, security breach from arch flaw)
  └── System Architect + CTO + Security + DevOps + affected teams. War room. Fix or rollback within hours.

Architecture decision that blocks multiple teams or changes core assumptions
  └── System Architect + CTO + all affected leads. ADR within 1 week. Tradeoff analysis required.

Architecture guidance, review, or approval for team-level design
  └── System Architect reviews, team implements. No escalation needed. ADR if decision affects other teams.
```


**What good looks like:** Architecture Review Board signs off with zero unresolved critical findings. C4 diagrams (Context → Container → Component → Code) are accurate and up-to-date — a new team member traces the system's data flow from ingress to persistence in under 10 minutes. ADRs for the last 5 major decisions are written, reviewed, and merged. The architecture sketch passes the 'explain to a new hire in 5 minutes' test.

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| Designing the communication backbone between 5+ microservices | Before choosing REST or gRPC for everything, propose an event bus (Kafka/NATS/SQS) for asynchronous boundaries and gRPC for synchronous hot paths. Map each service pair to sync/async based on latency budget: <50ms → gRPC, >200ms tolerance → async events. Discuss event schema evolution (Avro/Protobuf with schema registry) and dead-letter queues per consumer | Synchronous call chains create distributed monoliths: Service A calls B calls C calls D — a failure in D times out A after cascading through 3 retries. Events decouple services temporally, but without schema governance and DLQ, you trade tight coupling for silent data loss. The sync/async boundary is the most consequential architectural decision after monolith-vs-microservices |
| Team proposes microservices for a greenfield project with <10 engineers | Run the "Should We Microservice?" checklist. If team <20, DB CPU <50%, single tech stack, revenue <$20M ARR, deploy <daily → reject microservices. Start with a modular monolith with clear bounded contexts enforced by code structure | Microservices add network latency (50-200ms per hop), deployment complexity (N pipelines instead of 1), and debugging overhead (distributed tracing required). The default for <20 engineers should always be a monolith — extract services only when independent deploy/scale is provably required |
| Splitting a monolith into microservices for the first time | Before extracting any service, propose defining the bounded context with these questions: Does this context have independent deploy cadence? Independent scaling needs? A separate team? If fewer than 2 "yes" answers, keep it in the monolith. Discuss the strangler fig pattern: route new endpoints to the service, leave existing traffic on the monolith, migrate incrementally | Premature extraction creates "distributed spaghetti": services that share databases, have chatty APIs, and deploy together. The first extraction sets the pattern for all future ones — get the bounded context wrong and you're refactoring service boundaries for years. A strangler fig migration takes 3-6 months; a big-bang rewrite takes 12-24 and often fails |
| Designing a system that needs to serve both web and mobile clients with different data needs | Before creating a single unified API, propose a BFF (Backend for Frontend) pattern: one API layer per client type. Web BFF aggregates 10 endpoints into one dashboard response; mobile BFF returns lean payloads with sparse fieldsets. Discuss whether the BFFs are separate services or gateway configuration layers. Never let the mobile client pull the same payload as the web dashboard | Web dashboards need 50 aggregated fields; mobile list views need 5 flat fields. A single API serving both forces the mobile client to download 45 unused fields on every request — burning battery, bandwidth, and rendering time. BFFs isolate client-specific concerns, but too many BFFs (one per client version) become maintenance overhead — find the balance at client type granularity |
| Proposing CQRS (Command Query Responsibility Segregation) for a new domain | Before implementing separate read/write stores, quantify the read/write asymmetry: if reads outnumber writes <10:1, CQRS is premature. If reads are 100:1 with complex aggregations, propose CQRS with event-driven projection: writes go to a normalized store, CDC streams to a denormalized read store (materialized views, Elasticsearch). Discuss eventual consistency window and its UX implications | CQRS solves a specific problem: read patterns and write patterns are so different that optimizing one store for both creates a mediocre compromise. It does NOT solve "we have a lot of reads" — read replicas solve that. CQRS introduces eventual consistency: a user updates their profile and might see the old profile for 2 seconds. Make sure the product team accepts that before you build it |
| Choosing between orchestration (Saga orchestrator) and choreography (event-driven) for a distributed transaction spanning 4+ services | Before picking a pattern, evaluate failure complexity: orchestration centralizes the workflow (easy to reason about, single point of failure), choreography distributes it (resilient, hard to debug). Propose orchestration for business-critical flows (order checkout, payment settlement) where compensating transactions must be explicit. Propose choreography for reactive data propagation (cache invalidation, search index updates). Discuss saga compensation: every step needs an undo action | Orchestration without compensating transactions is a distributed transaction with no rollback. Choreography without correlation IDs is a mystery when something breaks — 4 services emitted events, which one failed? Saga patterns need both: an orchestrator that knows the sequence, and compensating actions that undo partial progress. Test the failure of step 3 of 5 — does the system reach a consistent state? |
| Designing multi-region failover for a system with 99.99% availability target | Before implementing active-active, propose quantifying the cost: inter-region data transfer ($0.02/GB), cross-region replication lag (typically 500ms-2s), and conflict resolution strategy (last-write-wins vs CRDTs). Discuss whether 99.99% justifies active-active (4+ regions) or whether a warm standby with 5-minute RTO achieves the same SLO at 40% of the cost. Document the failover runbook and test it quarterly | Active-active multi-region is the most expensive architectural decision you can make — not just infra costs, but operational complexity. Conflict resolution for multi-master writes is an unsolved problem for most domains. Many teams pay for active-active but run active-standby because they never resolved write conflicts. Be honest about whether you actually need writes in multiple regions |
| Planning the observability stack (service mesh + APM + tracing) for a distributed system | Before selecting tools, propose the three pillars with specific instrumentation: (1) distributed tracing with OpenTelemetry — propagate trace context across ALL service boundaries (HTTP, gRPC, message queues, DB calls), sample at 10% for success, 100% for errors; (2) structured logging with correlation IDs — every log line has `trace_id` and `span_id`; (3) RED metrics (Rate, Errors, Duration) per endpoint per service. Discuss SLO-based alerting: alert on error budget burn rate | Observability bolted on after incidents is useless — you can't add tracing during an outage. Without propagated trace context, a 5-second P99 latency spike is a mystery: is it service A's DB query? Service B's network call? Service C's serialization? Distributed tracing answers in one query. Without it, you're grep'ing logs across 10 services at 3 AM |

## What Good Looks Like

> Every stakeholder — from the junior developer to the CTO — can look at the C4 diagrams and understand how the system fits together without asking "what does this arrow mean?" Architecture Decision Rec

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.


## Deliberate Practice

<!-- DEEP: 10+min — how to improve, not just what you do -->

### The Architecture Improvement Loop
1. **Post-mortem an incident** — Take a real production incident. Draw the architecture diagram as it existed when the incident happened. Mark every component that failed.
2. **Identify the systemic gap** — Was it a missing circuit breaker? Single point of failure? Cascading failure? Missing observability?
3. **Design the fix and model the blast radius** — If you add this pattern, what new failure modes does it introduce?
4. **Repeat quarterly** — Incidents are free architecture lessons. Each one exposes a weakness in your mental model of the system.

### Practice Routines
| Skill Level | Practice | Frequency | Expected Result |
|-------------|----------|-----------|-----------------|
| Novice → Competent | Take an existing system (open source or at work) and draw its C4 diagrams without looking at docs. Then compare with reality. | Monthly | Develops the ability to see architecture from behavior, not just documentation |
| Competent → Expert | Design the same system 3 different ways: monolith, microservices, event-driven. Write ADRs for each. Compare: which is simpler? Which handles failure better? | Quarterly | Internalizes that architecture is tradeoffs, not absolutes — can articulate why one pattern fits a context |
| Expert → Master | Post-mortem a famous outage (GitHub, AWS, Cloudflare). Design the fix. Then read what they actually did. Compare your solution to theirs. | Quarterly | Develops calibration — can assess whether your solution matches the industry's best |

### The One Thing
**Redesign a system you built 2 years ago using what you know now.** Would you make the same decisions? If yes: you haven't grown enough. If no: write down why. Your old architectures are a record of your thinking at that time. Revisiting them is the fastest way to see your own growth.

## Gotchas

- **C4 Container diagram vs. deployment diagram**: Containers in C4 are runtime processes (a web app, a database), NOT Docker containers. Showing Docker containers as C4 containers conflates the deployment view with the runtime view. Docker is infrastructure detail — it belongs in C4 level 4, not level 2.
- **Event-driven architectures** make debugging order-dependent bugs nearly impossible without correlation IDs. If Service A emits event E1, B reacts with E2, C reacts with E3 — and C sees E3 before E1's side effect — the bug reproduces only under specific race conditions. Every event must carry a `correlationId` and `causationId`.
- **Microservice data ownership**: If Service A owns `users` and Service B needs `user.email`, B should NOT query A's database directly. But if B calls A's API for every email, latency spikes. The real answer is a materialized view or event-carried state transfer — decisions that must be made at architecture time, not implementation time.
- **ADR (Architecture Decision Record)** titles must state the decision, not the topic. "ADR-003: Database" is useless months later. "ADR-003: Use PostgreSQL with Citus for tenant-isolated multi-tenancy" tells you what was decided.
- **Capacity planning with percentiles**: "Average response time 200ms" means 50% of requests are below 200ms, but 1% might be 5 seconds. P95, P99, and P99.9 matter more than average. Architect for the P99, not the mean.


## References
- **Architecture Fitness Functions**: See [architecture-fitness-functions.md](references/architecture-fitness-functions.md)
- **When Monolith Wins**: See [when-monolith-wins.md](references/when-monolith-wins.md)
