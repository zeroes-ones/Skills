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
| Team proposes microservices for a greenfield project with <10 engineers | Run the "Should We Microservice?" checklist. If team <20, DB CPU <50%, single tech stack, revenue <$20M ARR, deploy <daily → reject microservices. Start with a modular monolith with clear bounded contexts enforced by code structure | Microservices add network latency, deployment complexity, and debugging overhead. The default for <20 engineers should always be a monolith — extract services only when you can prove independent deploy/scale is required |
| Architecture diagram hasn't been updated in 6+ months — new team members draw their own on whiteboards during onboarding | Schedule a 2-hour "diagram day" to update C4 Context and Container diagrams. Add to PR template: "Does this change affect any C4 diagram? If yes, update it." Make diagrams part of the Definition of Done for architecture-affecting work | Outdated architecture diagrams are worse than no diagrams — they create false confidence. When fire breaks out, the wrong diagram leads incident response in the wrong direction, wasting critical minutes |
| ADR is proposed with a single option presented as "the obvious choice" — no alternatives considered | Reject the ADR and require at least 2 rejected alternatives with documented tradeoffs for each. An ADR without rejected alternatives is a preference, not a reasoned decision | The value of an ADR isn't the choice — it's the context around why alternatives were rejected. Two years later, when constraints have changed, knowing why you chose X over Y and Z is what enables informed reconsideration instead of guessing |
| Production incident reveals an event was published but never consumed — data silently lost with no alert | Audit every event subscription: does it have a dead-letter queue? Implement DLQ for all subscriptions, add message persistence with replay capability, monitor DLQ depth with alerts, and add end-to-end tracing for all event flows | Event-driven without DLQ is fire-and-forget with amnesia. Lost messages in production are invisible until a customer complains — by then the trust is gone and the data is unrecoverable |
| P95 latency doubled after extracting a new service — "we split it to make it faster" | Measure the latency budget per hop BEFORE extraction. Every network hop adds 50-200ms. If the split violates the latency budget, merge services back or use async messaging (events/queues) instead of sync REST | Distributed systems are slower than monolithic ones — always quantify before splitting. Extract with distributed tracing already in place, not after the fact. Latency is a feature users feel; don't trade it away for architectural purity |
| Security review finds hardcoded credentials in source code — 6 months after they were committed and the repo has been cloned by 15 engineers | Add secret scanning to CI immediately (Trivy, Semgrep, GitGuardian). Rotate all exposed credentials within 24 hours. Implement secrets management (Vault/AWS Secrets Manager) as a non-negotiable architectural requirement enforced at the platform level | A single hardcoded credential in source code can cost millions in breach remediation. Secrets should never touch a developer's editor or version control — inject at runtime via secrets manager or CI/CD pipeline |
| Team of 5 engineers operating 15 microservices — every deploy requires coordination across 3 teams and takes 3 days | Consolidate into a modular monolith with clear bounded contexts. One deploy, one repo, one team. If a service handles <100 req/s, it's a library, not a service — merge it back. Run the consolidation as a dedicated architectural initiative | The operational cost of a microservice (CI/CD pipeline, monitoring, on-call rotation, deployment coordination) is constant regardless of throughput. Many tiny services multiply operational burden without any scaling benefit |
| New external dependency introduced without architecture review — "we'll document it later, we needed it for the sprint" | Add architecture fitness functions in CI: no new service dependencies without an ADR, no circular module dependencies, no breaking API changes, no HIGH/Critical CVEs. Automate the architecture review, don't schedule it — the CI pipeline is your enforcement mechanism | Architecture degrades one un-reviewed decision at a time. Fitness functions in CI catch drift before it becomes debt. A dependency not reviewed is a decision not tracked — and a future outage with no documented rationale |

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
|-----------------|---------------------|
| Choosing microservices for a greenfield 5-person team "so we're ready to scale" — 15 services, 3-day deploys, debugging requires tracing across 5 service boundaries | Start with a modular monolith. Extract services only when: (1) bounded contexts are clearly proven, (2) independent scaling is measured as needed, (3) team topology aligns with service boundaries. Microservices are a cost paid upfront for a benefit you may never need |
| Designing for hypothetical scale — optimizing for 1M concurrent users when you have 100 | Design for 10x current load, not 10,000x. A single well-tuned Postgres + Redis can handle 10K req/s. Premature optimization adds complexity without value. Measure first, scale second |
| Using event sourcing for every write operation — even simple user profile updates become event-sourced sagas with replays and projections | Use event sourcing only when you need: immutable audit trail (compliance), temporal queries (what was the state at time T?), or complex multi-step event-driven workflows. For standard CRUD, a relational database with an append-only history table is simpler, faster, and easier to debug |
| Sharing a single database across multiple services — "it's faster than API calls and we trust each other's schema changes" | Each service owns its data exclusively. Services communicate via well-defined APIs, never by reading each other's tables directly. A shared database creates tight coupling: a schema migration in Service A silently breaks Service B's queries |
| Deploying to production without circuit breakers — "our dependencies are reliable, they never go down" | Every external dependency needs a circuit breaker, configurable timeout, retry policy with backoff, and graceful fallback. Assume every dependency can and will fail at the worst possible time. Circuit breakers prevent cascading failures from one slow service taking down the entire system |
| Treating the architecture diagram as a one-time deliverable — generated for the design review and never opened again | Architecture diagrams are living documents updated with every significant change. Add "update C4 diagrams if affected" to the Definition of Done. Outdated architecture docs are misinformation — they guide incident response to the wrong root cause during outages |
| Expressing non-functional requirements as adjectives — "the system must be fast, scalable, and secure" | Express NFRs as measurable SLOs: "P95 checkout latency <200ms, availability ≥99.95%, recover from single-AZ failure within 5 minutes." Vague adjectives are impossible to verify, test, or alert on. SLOs are specific, monitorable, and enforceable in CI and production |

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
