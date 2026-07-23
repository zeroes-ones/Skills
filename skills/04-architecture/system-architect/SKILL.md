---
name: system-architect
description: System design, architecture decisions, scalability patterns, C4 modeling, ADRs, microservices vs monolith trade-offs, capacity planning, and event-driven architectures. Triggered by system
  design, architecture, scalability, C4, ADR, microservices, monolith, event-driven, capacity planning.
author: Sandeep Kumar Penchala
type: architecture
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- system-architect
token_budget: 4000
output:
  type: code
  path_hint: ./
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

Design and evaluate system architectures through structured modeling, trade-off analysis, and architectural decision records. This skill covers end-to-end architecture from requirements to deployment topology, including C4 modeling (Context, Container, Component, Code), Architecture Decision Records (ADRs), scalability patterns, and capacity planning.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── DESIGN something new
│   ├── Greenfield system → Start at "Decision Trees > Monolith vs Microservices"
│   ├── New service in existing system → Go to "Architecture Styles Decision Matrix" in references/
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

These rules apply to *every* response this skill produces.

- **Never recommend architecture without NFR context.** Before suggesting microservices or monolith, ask: "What's the expected scale (QPS, DAU), latency budget (p95 < ?ms), and availability target (99.9%? 99.99%)?" Do not propose solutions without quantified requirements.
- **Always present tradeoffs, not one "right" answer.** Every architecture decision is a tradeoff. Present at least two options with pros/cons. Do not deliver a single recommendation without alternatives.
- **Diagrams before code.** Start every architecture discussion with a diagram (C4 Context or Container level). A picture exposes assumptions that prose hides. Do not dive into implementation details without a shared visual model.
- **Always write an ADR for irreversible decisions.** Technology choices, data store selections, and service boundaries get an Architecture Decision Record with context, options considered, and rationale.
- **Admit what you don't know.** If you haven't seen latency requirements, throughput expectations, compliance constraints, or team capabilities, say so and ask before architecting.

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

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
When this skill is invoked, drill into these specialized areas as needed:

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `architecture-assessment` | New project, acquisition, modernization | This file — Phase 1 & 2 |
| `c4-modeling` | Communicating architecture to different audiences | This file — Phase 2: Architecture Design |
| `adr-writing` | Every significant technical decision | This file — Phase 3: Trade-off Analysis |
| `scalability-design` | Growth planning, performance issues | This file — Scalability Decision Tree |
| `resilience-design` | Mission-critical, high-availability | This file — Phase 4: Resilience |
| `integration-architecture` | Multi-system, multi-vendor | This file — Communication Patterns |
| `data-architecture` | Data-heavy, analytics, compliance | `references/complexity-cost-model.md` |
| `security-architecture` | Compliance, threat modeling | `security-engineer` skill |

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

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Evolvable architecture**: Start with modular monolith; extract microservices only when bounded contexts are clear and independent scaling is needed.
- **Loose coupling, high cohesion**: Services communicate through well-defined APIs and events; avoid shared databases across services.
- **Design for failure**: Every dependency can fail — implement retries, circuit breakers, fallbacks, and dead-letter queues.
- **Observability from day one**: Distributed tracing (OpenTelemetry), structured logging, metrics (RED: Rate, Errors, Duration), health checks (liveness/readiness).
- **Infrastructure as Code**: Terraform/Pulumi/CloudFormation for all infrastructure; GitOps (ArgoCD/Flux) for deployment.
- **Security by design**: Defense in depth, zero-trust networking, least-privilege IAM, encryption at rest and in transit, secrets management (Vault/Secrets Manager).
- **Cost awareness**: Model cloud costs early (compute, data transfer, storage, managed services); architect for cost optimization (spot instances, auto-scaling, serverless where appropriate).

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|---|---|
| Designing an event-driven architecture without dead-letter queues and message replay — orders silently lost during a brief consumer outage | Every event consumer gets a DLQ with alerting on depth >0. Messages in DLQ must be inspectable, replayable, and have a retention policy (7-30 days). Without DLQ, a consumer outage means permanent data loss — customers discover missing orders, not your monitoring dashboard |
| Sharing a single database across multiple services to "keep things simple" — Service A adds a column, Service B's queries break | Each service owns its data store exclusively. Services communicate through APIs or events, never through direct database access. A shared database creates the worst kind of coupling: the schema becomes the API, and every schema change requires cross-team coordination — defeating the purpose of independent deployability |
| Using synchronous HTTP calls for every inter-service communication without timeouts, circuit breakers, or bulkheads | Configure per-call timeouts (p95 latency × 2, max 30s), circuit breakers (open at 50% error rate, half-open after 30s with a single probe), retries (max 3 with exponential backoff + jitter), and bulkheads (separate thread pools per downstream). Without these, one slow downstream saturates all request threads — cascading failure across the entire system |
| Implementing saga orchestration without compensating transactions — "we'll handle failures manually if they happen" | Every saga step needs a defined compensating action (undo). For an order checkout saga: reserve inventory → charge payment → ship order. If shipping fails, you must refund payment AND release inventory. Without compensations, partial failures leave the system in an inconsistent state that requires manual database surgery to fix |
| Adopting CQRS without defining the eventual consistency window — users see stale data for minutes after updates | Define and document the acceptable staleness window (e.g., "read models are consistent within 2 seconds of write"). Monitor replication lag and alert when it exceeds the SLA. Design the UX to handle staleness: disable edit buttons until the read model catches up, or show a "saving..." indicator with optimistic UI updates. CQRS without staleness handling is a UX regression, not an architectural improvement |
| Building a BFF (Backend for Frontend) that becomes a monolithic gateway aggregating all logic — defeating the purpose of client-specific APIs | Keep BFFs thin: they aggregate and transform data from downstream services, never contain business logic. If the BFF starts implementing validation, authorization, or workflow logic, it has become a new monolith. Extract business logic into dedicated services; let the BFF do only protocol translation and payload shaping for its specific client type |
| Deploying a service mesh (Istio/Linkerd) without enabling distributed tracing and authorization policies | Service mesh without mTLS enforcement and tracing is just infrastructure overhead costing 50-100MB per pod. Configure day one: (a) mTLS in STRICT mode, (b) AuthorizationPolicy to allow only known service identities, (c) distributed tracing at 10% sampling, (d) retry budgets, (e) circuit breaker at 50% error rate. A mesh that only routes is a wasted deployment — the value is in security and observability, not the proxy |
| Choosing microservices for a greenfield 5-person team "so we're ready to scale" — 15 services, 3-day deploys, debugging requires tracing across 5 service boundaries | Start with a modular monolith. Extract services only when: (1) bounded contexts are clearly proven, (2) independent scaling is measured as needed, (3) team topology aligns with service boundaries. Microservices are a cost paid upfront — per-service CI/CD pipelines, monitoring dashboards, on-call rotations — for a scaling benefit you may never need |

## When Monolith Wins

Scalability ceiling of a well-built modular monolith: **100K-1M DAU, 50+ engineers.**

```
Team < 20 engineers? → Monolith.
DB CPU < 50% sustained? → Monolith.
Single technology stack? → Monolith.
Revenue < $20M ARR? → Monolith.
Deploying < daily? → Monolith.
All features in one bounded context? → Monolith.

Check 3+ boxes? Don't even think about microservices.
```

Shopify ran a monolith past 1M merchants. GitHub: monorepo to 30M+ users.

## Architecture Fitness Functions

Automated tests verifying architecture doesn't degrade — run in CI:

| Category | What to Test | Example Threshold |
|----------|-------------|-------------------|
| **Coupling** | No circular deps between modules | `import-linter` / `madge` |
| **Cohesion** | Module size ≤ 500 lines | Custom script |
| **Performance** | P95 latency ≤ 200ms for critical paths | k6 / Locust |
| **API compatibility** | No breaking OpenAPI changes | `openapi-diff` |
| **Security** | No hardcoded keys, no HIGH CVEs | Trivy / Semgrep |

## Scalability Decision Tree

```
DB CPU > 70% sustained?
├── YES → Add read replicas → Still high? → Shard by tenant.
└── NO → Don't shard.

P95 latency > 200ms?
├── YES → Profile → Add cache (Redis) → Optimize queries → Make async.
└── NO → You're fine.

CI > 15 minutes?
├── YES → Parallelize tests → Split into smaller jobs → Consider service extraction.
└── NO → Ship features.

>2 teams colliding in same codebase?
├── YES → Extract one bounded context at a time.
└── NO → Keep the monolith.

Service handles < 100 req/s? → It's a library, not a service. Merge back.
Cache hit rate < 50%? → Remove the cache. It's adding latency.
```

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Architecture = a single monolith on a PaaS (Vercel, Railway, Render). No C4 diagrams. No ADRs. No microservices. Database = one managed Postgres. Decisions = you make them and document in a `decisions.md`.
- **What to skip**: Microservices. Event-driven architecture. C4 modeling. ADR templates. Capacity planning. FMEA. Multi-region. Service mesh. Kubernetes.
- **Coordination**: You are the architect + developer. No coordination needed.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Monolith with clear module boundaries. C4 Context + Container diagrams. Lightweight ADRs for key decisions. Managed services for infra (RDS, S3, SQS). Simple observability (logs + metrics + basic alerts). Capacity estimation for 6 months.
- **What to skip**: Microservices (module boundaries in monolith are enough). Event sourcing. CQRS. Service mesh. Formal SLOs (>99.5% is fine). Multi-cloud. Chaos engineering.
- **Coordination**: Architecture discussion in weekly eng sync. ADRs in shared repo. Quarterly architecture review (2 hours).

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Modular monolith or first microservices (3-5 services max). C4 all four levels. Formal ADR process with templates. Event-driven for async boundaries. SLOs defined (99.9% target). Capacity planning with growth modeling. FMEA for critical paths. Observability: tracing + metrics + structured logging + dashboards. Circuit breakers and retry policies.
- **What to skip**: Full microservices (>10 services without dedicated platform team). Multi-cloud. Active-active multi-region. Formal architecture review board.
- **Coordination**: Monthly architecture review. ADRs with async comment period (3 days). Quarterly capacity planning review. Bi-weekly tech lead sync.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Microservices with platform team. Architecture review board with formal governance. C4 + UML for complex domains. Architecture fitness functions in CI. Multi-region active-active or warm standby. Formal SLOs with error budgets. Chaos engineering program. Capacity planning with financial modeling. Dedicated architecture team.
- **What's full production**: Architecture governance framework. Technology radar with lifecycle management. Annual architecture strategy. Cross-BU architecture alignment. M&A architecture integration playbook.
- **Coordination**: ARB bi-weekly. Architecture strategy quarterly with CTO. Cross-team architecture sync monthly. Incident post-mortem architecture review per incident.

### Transition Triggers
- **Solo → Small**: Monolith codebase becomes unwieldy (>50K LOC). Need dedicated architecture decisions.
- **Small → Medium**: 3+ teams working in the same codebase causes merge conflicts. First service extraction justified (independent deploy + scale needs).
- **Medium → Enterprise**: 10+ services require platform team. Multi-region or compliance (SOC 2, HIPAA) required. >50 engineers.


## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Team of 5 with 15 microservices — every deploy took 3 days of coordination | Architecture chose microservices for a greenfield project with a 5-person team "to be scalable" | Consolidate into a modular monolith with clear bounded contexts. 1 deploy, 1 repo, 1 team. Result: deploy time dropped from 3 days to 15 minutes | **Microservices are a cost, not a benefit, for most projects.** Start with a modular monolith. Extract services only when you can prove independent deploy/scale is needed. The default for <20 engineers should always be a monolith |
| Critical user event notifications silently disappeared — orders were placed but customers never received confirmation | Event-driven system used a pub/sub model with no dead-letter queue. When the notification service was briefly down, 2,300 events were published into the void | Implement dead-letter queues (DLQ) for every subscription. Add message persistence with replay capability. Monitor DLQ depth with alerts. Add end-to-end tracing for all event flows | **Event-driven without DLQ is fire-and-forget with amnesia.** Every event subscription needs: DLQ, message retention, replay capability, and delivery monitoring. Lost messages in production are invisible until a customer complains — by then the trust is gone |
| Dashboard showed stale data for 8 hours after a critical price update | Wrong caching strategy: HTTP cache on CDN with 24-hour TTL for an endpoint where data changed hourly | Reduce CDN TTL to 1 hour for time-sensitive data. Add cache invalidation hook on data update. Implement stale-while-revalidate pattern. Add cache hit-rate monitoring with alert on unexpected patterns | **Cache TTL must match data freshness requirements, not convenience.** A cache that serves stale data is worse than no cache because it's silently wrong. Always measure and alert on cache hit rates. Stale data erodes user trust faster than a slow page load |
| After "Go to checkout," users saw items from another person's cart | Session affinity was configured on the load balancer but the shopping cart service used a shared in-memory cache without user-id scoping — two users on the same pod saw each other's data | Add user-id scope to all cache keys. Ensure shopping cart data is isolated per session. Add integration tests that simulate multiple concurrent users on the same instance | **Shared mutable state is the #1 source of data leakage bugs.** Every cache key must include user/tenant scope. Test with multiple concurrent users on the same instance — not just isolated single-user scenarios |
| P95 latency jumped from 200ms to 12s after migrating from monolith to 8 microservices | Each request that was once a single database query now crossed 5 service boundaries (REST calls between services), each adding 50-200ms overhead | Measure the actual latency budget per hop. Re-evaluate whether service boundaries are correct. Merge services that belong to the same bounded context. Add circuit breakers to prevent cascading delays | **Distributed systems are slower than monolithic ones — quantify before splitting.** Every network hop adds latency. Before splitting a monolith, measure the end-to-end latency budget and confirm the split won't violate it. Add distributed tracing before, not after, the split |


## What Good Looks Like

> Every stakeholder — from the junior developer to the CTO — can look at the C4 diagrams and understand how the system fits together without asking "what does this arrow mean?" Architecture Decision Records capture the context, options considered, and trade-offs for every key decision, so the rationale behind choosing event sourcing over CRUD is still crystal clear two years and three team rotations later. Non-functional requirements are expressed as measurable SLOs, not vague adjectives: 99.95% availability with p99 latency under 200ms for the checkout path, backed by production telemetry that proves compliance. The failure mode analysis has been walked through with the whole team, and when the payment gateway actually went down during Black Friday, the circuit breaker opened in under 100ms, the dead-letter queue absorbed every message, and zero orders were lost — exactly as the runbook said.

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  C4 Context and Container diagrams created and reviewed
- [ ] **[S2]**  Architecture Decision Records documented for all key decisions
- [ ] **[S3]**  Non-functional requirements captured with measurable SLOs
- [ ] **[S4]**  Scalability model with peak QPS, latency budgets, and data growth projections
- [ ] **[S5]**  Failure mode analysis conducted (FMEA, fault tree, or chaos engineering plan)
- [ ] **[S6]**  Data storage strategy documented (primary store, cache, search, analytics)
- [ ] **[S7]**  Authentication, authorization, and secrets management strategy defined
- [ ] **[S8]**  Observability stack planned (tracing, metrics, logging, alerting)
- [ ] **[S9]**  Deployment and rollback strategy documented (blue-green, canary, rolling)
- [ ] **[S10]**  Capacity planning and cost estimation completed for 12-month horizon

## Footguns
<!-- DEEP: 10+min — war stories from production architecture decisions -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Microservices split by noun (User Service, Order Service, Product Service) — every request needed data from 3+ services, and p99 latency jumped from 50ms to 2,400ms as the fan-out exploded | An e-commerce platform decomposed their monolith into microservices by database entity: `user-service`, `order-service`, `product-service`, `inventory-service`, `pricing-service`. The "Order Details" page required data from all 5. Under the monolith, it was one SQL query: 50ms. Under microservices, it was 5 sequential gRPC calls with service A calling B calling C: 2,400ms p99. The team then added a GraphQL federation layer to parallelize the calls — which added 3 more services (gateway, subgraph proxies). Total services: 11. P99 latency: 1,800ms. Still 36× worse than the monolith. The architecture was redesigned 18 months later at a cost of $1.2M in engineering time. | Services were split by data ownership (one service per database table) instead of by business capability (one service per user journey). The "entity-based decomposition" pattern creates distributed joins — every use case spans multiple services because business processes naturally involve multiple entities. The monolith was split along the wrong axis. | **Decompose by business capability, not by database entity.** An "Order Fulfillment" service owns orders, inventory, and shipping — not an "Order Service" that only owns the `orders` table. Use Domain-Driven Design event storming to find natural boundaries: which entities change together? Which are read together? If two entities are always queried in the same API call, they belong in the same service boundary. Validate: write the top 10 API calls in the new architecture and measure the number of inter-service calls each requires. If any requires > 2, redraw the boundaries. |
| Event-driven architecture with Kafka — but no dead letter queue configured, and 2.3M events were silently dropped over 17 days because the consumer deserialization failed on a new field added to the schema | A logistics platform adopted Kafka with an event-driven architecture. The `OrderShipped` event schema evolved: a new `carrier_tracking_url` field was added to the Avro schema. The `notification-service` consumer used an older schema version and couldn't deserialize events with the new field. The default Kafka consumer error handler was `LogAndContinue` — it logged a warning and skipped the message. For 17 days, 2.3M `OrderShipped` events were consumed, deserialization failed, and the events were silently dropped. 2.3M customers never received shipping confirmation emails. The support team noticed when "where is my order?" tickets spiked 400% week-over-week. | The consumer's error handling was "log and skip" — the worst possible choice for an event-driven system. Schema evolution happened unilaterally (producer added field, didn't coordinate with consumers). No dead letter queue captured failed events for replay. No monitoring existed for consumer lag or deserialization error rates. | **Every event consumer must have a dead letter queue (DLQ) and separate error handling for deserialization failures vs business logic failures.** Deserialization failures: stop the consumer, alert, page on-call — schema incompatibility means all subsequent messages will also fail. Business logic failures: retry with exponential backoff, then DLQ. Monitor: consumer lag, DLQ depth, deserialization error rate. For schema evolution: use a schema registry (Confluent, Apicurio) with compatibility checks. Never add a required field without coordinating with all consumers. |
| C4 diagrams drawn once during the initial architecture review — 18 months later, reality had diverged so completely that 3 of the 7 documented services no longer existed and 2 new critical services were undocumented | A startup's founding engineering team created C4 Container and Component diagrams during their Series A architecture review. They were beautiful: hand-drawn in Structurizr, peer-reviewed, exported to the engineering wiki. Eighteen months and 4 reorgs later, a new architect joined and asked for the system diagrams. The wiki showed 7 services. Reality had 9: 3 of the original 7 had been decommissioned, 2 new services had been built and were handling 40% of production traffic, and 1 service had been split into 3 but still appeared as a single box. The diagrams were worse than useless — they actively misled. An incident investigation was delayed by 45 minutes because the on-call engineer followed a diagram showing a dependency that had been removed 11 months prior. | Diagrams were treated as a one-time deliverable (produce and forget) instead of a living artifact that must evolve with the system. Nobody was accountable for keeping them current. The Structurizr DSL files lived in a separate repo that nobody touched after the initial review. New services were built without updating the diagrams because "that's architecture team work." | **Treat architecture diagrams as code that must pass CI.** Store diagrams in the same repo as the services they describe (e.g., `docs/architecture/`). Add a CI check: on every PR that adds or removes a service, fail if the C4 diagram isn't updated. Use Structurizr DSL or PlantUML — text-based formats that can be diff'd in code review. Run quarterly "architecture reviews" where the team walks the production infrastructure and updates the diagrams live. The rule: if a diagram can't be generated from production data, it's already stale. |
| "We'll scale horizontally later" — the single-write-master database became the bottleneck at 18 months, but by then the schema had 47 tables with deep foreign key chains that couldn't be sharded | A SaaS startup's CTO made the classic decision: "MySQL with a read replica. We'll shard when we hit 100K users." The schema grew organically: 47 tables with foreign keys spanning 4 levels deep. Queries routinely joined across 6 tables. At 80K users, the write master hit 80% CPU during peak hours. The team explored sharding — but with foreign keys crossing every proposed shard boundary, every major query would need distributed joins. The "just add Citus" migration couldn't work because Citus requires colocating joined tables on the same shard key. The "just add Vitess" migration required rewriting 40% of application queries. The fix: an emergency 3-month project to denormalize, add caches, and split read/write paths — while the database was melting down every afternoon. | "Scale later" decisions assume the schema won't accumulate complexity that makes scaling harder. Every foreign key, every cross-table join, every aggregate query becomes a sharding blocker. By 18 months, the schema had organically grown into a shape that made horizontal scaling nearly impossible without a rewrite. | **Design for sharding from day one, even if you don't implement it.** Pick a shard key for every major table. Avoid cross-shard foreign keys. Denormalize data that's read together into the same shard. Test: can you run your top 10 queries against a single shard without hitting another shard? If no, your sharding strategy is already broken. Run a "sharding drill" at 6 months and 12 months: provision 3 database instances, distribute data by your planned shard key, and measure how many queries fail or need rewriting. |
| Architecture Decision Record written and stored in Confluence — 18 months later, nobody could find it, and the team made the exact same mistake again because the original rationale was lost | An engineering team spent 2 weeks evaluating PostgreSQL vs CockroachDB for a new service. They wrote a 3-page ADR with benchmarks, tradeoffs, and the final decision (PostgreSQL with the caveat "revisit when we need multi-region writes"). The ADR was stored in Confluence under `/Engineering/Architecture/Decisions/2024-03-postgres-vs-cockroachdb`. Eighteen months later, needs changed: the service now needed multi-region writes. The new team (3 of 5 original members had left) spent 3 weeks re-evaluating databases from scratch, unaware the original ADR existed. They reached the same conclusion — except this time they chose CockroachDB, not knowing that the original team had ruled it out because of a specific stored procedure incompatibility that was still present. The migration to CockroachDB failed 6 weeks in when they hit the exact stored procedure bug the original team had documented. | ADRs are useless if they're not discoverable. Confluence is a document graveyard — content is written once and never found again. The team assumed "it's in Confluence, it's discoverable" — but Confluence search is notoriously bad for technical content, and nobody browses `/Engineering/Architecture/Decisions/` before making decisions. | **Store ADRs in the repository alongside the code they govern.** Directory: `docs/adr/0001-use-postgres-for-user-service.md`. Use a numbered, searchable format. Add a CI check: PRs that modify the architecture must reference an ADR or create one. Use `adr-tools` CLI to manage the decision log. At the top of every ADR: "Status: Superseded by ADR-0014" or "Status: Accepted — Revisit by 2025-06." The rule: a decision isn't final until it's in `docs/adr/` and the team has reviewed it in a PR. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You propose "use microservices" or "use a monolith" without asking "what are the top 5 queries this system must serve, and what are their latency budgets?" | You can design the same system as a monolith, microservices, and event-driven architecture — and articulate the specific tradeoffs of each with quantified estimates (latency, complexity, team topology, operational cost) | A CTO asks you "should we rewrite or refactor?" and you deliver a recommendation backed by production data, risk analysis, and a phased migration plan — and 12 months later the organization completed the transition on time and budget |
| You draw architecture diagrams in a visual tool (draw.io, Lucidchart) and export them as PNGs that can't be diff'd, versioned, or updated without redoing the entire diagram from scratch | Your architecture diagrams are generated from text-based DSL (Structurizr, PlantUML, C4-PlantUML) stored in the repo, diff'd in PRs, and regenerate on every commit — you haven't touched a visual diagram tool in 2 years | You post-mortem a major incident and 6 months later, your architectural recommendations have prevented the entire class of failure from recurring — and you can prove it with incident data showing a 70% reduction in related Sev1 events |
| You make architecture decisions alone and announce them in Slack — "we're moving to Kafka, starting next sprint" | Every architecture decision has an ADR with: context, options considered, tradeoffs, decision, consequences, and a revisit date — and it's approved by at least 2 senior engineers who weren't part of the evaluation | You're brought into a struggling project as an "architecture SWAT" — in 2 weeks, you diagnose the root architectural problem, propose a remediation that the team can implement in 3 months, and 6 months later the system is stable |

**The Litmus Test:** Can you receive a 2-page PRD for a system you've never seen, produce C4 Context + Container diagrams, 3 prioritized ADRs, a non-functional requirements document with quantified SLOs, and a 12-month cost projection — all in under 6 hours — and have the CTO approve it without requesting a single structural change?

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

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Complexity Cost Model](references/complexity-cost-model.md) — Complexity cost formula, monolith vs microservices cost comparison, architecture fitness functions
- [C4 Model](https://c4model.com/) — Simon Brown
- [Architecture Decision Records](https://adr.github.io/) — adr.github.io
- [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) — Martin Kleppmann
- [Building Microservices](https://www.oreilly.com/library/view/building-microservices-2nd/9781492034018/) — Sam Newman
- [System Design Interview](https://github.com/donnemartin/system-design-primer) — donnemartin/system-design-primer
- [The Twelve-Factor App](https://12factor.net/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
