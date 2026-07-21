---
name: system-architect
description: "System design, architecture decisions, scalability patterns, C4 modeling, ADRs, microservices vs monolith trade-offs, capacity planning, and event-driven architectures. Triggered by system design, architecture, scalability, C4, ADR, microservices, monolith, event-driven, capacity planning."
author: Sandeep Kumar Penchala
type: architecture
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - system-architect
token_budget: 2006
output:
  type: "code"
  path_hint: "./"
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
└── Don't know where to start? → Describe the problem in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

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
<!-- QUICK: 30s -- table of who to talk to when -->
System architecture is the skeleton everything hangs on. Decisions ripple across every team — coordination isn't optional, it's the job.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **CTO Advisor** | Technology strategy, major architectural decisions, build-vs-buy | Architecture options with tradeoff analysis, technical risk assessment, cost projections |
| **API Designer** | Service boundaries, API contracts, communication patterns | Bounded contexts, API principles (REST/GraphQL/gRPC), versioning strategy, error handling standards |
| **Database Designer** | Data architecture, persistence layer, caching strategy | Data model, access patterns, consistency requirements, read/write ratios, multi-tenancy model |
| **Security Engineer** | Threat modeling, auth architecture, compliance (SOC2, HIPAA, GDPR) | Architecture diagrams, data flow, trust boundaries, encryption requirements, IAM design |
| **DevOps / Platform Engineer** | Infrastructure design, CI/CD, observability, deployment strategy | Architecture requirements (compute, networking, storage), scaling patterns, monitoring needs |
| **Performance Engineer** | Scalability modeling, bottleneck analysis, capacity planning | Traffic projections, latency budgets, throughput requirements, architecture choices that affect perf |
| **Frontend Lead / Mobile Lead** | Client architecture, BFF pattern, API contract, real-time requirements | BFF design, GraphQL schema, WebSocket/SSE architecture, offline support, client-side caching |
| **Product Manager** | Feasibility assessment, technical constraints, build-vs-buy | What's architecturally possible, complexity cost, options with tradeoffs in business terms |
| **Chaos Engineer** | Resilience design, failure mode analysis, blast radius containment | Architecture weak points, dependency graph, failure modes, steady-state definition |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| ADR (Architecture Decision Record) published | All engineering leads, CTO, Product | Key decisions affecting API surface, data model, infrastructure, or developer workflows |
| New service or bounded context identified | API Designer, Database Designer, DevOps | API contract, database design, infrastructure provisioning, CI/CD pipeline |
| Technology stack change (new language, framework, database, message broker) | CTO, All engineering leads, DevOps, Security | Skill requirements, migration plan, operational readiness, security review |
| Architecture review finds scalability ceiling (e.g., DB at 70% capacity) | CTO, DevOps, Performance Engineer | Capacity planning, scaling strategy, timeline before ceiling hit |
| Build-vs-buy decision needed (e.g., auth service, search, payments) | CTO, Product, Finance, Security | Options analysis, TCO (3yr), integration complexity, compliance implications |
| Cross-cutting concern discovered (auth, logging, monitoring, error handling) | All service teams, API Designer | Standardization needed — centralize or federate, pattern documentation |
| Production incident with architectural root cause | CTO, DevOps, affected teams, Chaos Engineer | Postmortem, architectural fix priority, resilience pattern addition |

### Escalation Path

```
Architecture emergency (data corruption, cascading failure, security breach from arch flaw)
  └── System Architect + CTO + Security + DevOps + affected teams. War room. Fix or rollback within hours.

Architecture decision that blocks multiple teams or changes core assumptions
  └── System Architect + CTO + all affected leads. ADR within 1 week. Tradeoff analysis required.

Architecture guidance, review, or approval for team-level design
  └── System Architect reviews, team implements. No escalation needed. ADR if decision affects other teams.
```

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Evolvable architecture**: Start with modular monolith; extract microservices only when bounded contexts are clear and independent scaling is needed.
- **Loose coupling, high cohesion**: Services communicate through well-defined APIs and events; avoid shared databases across services.
- **Design for failure**: Every dependency can fail — implement retries, circuit breakers, fallbacks, and dead-letter queues.
- **Observability from day one**: Distributed tracing (OpenTelemetry), structured logging, metrics (RED: Rate, Errors, Duration), health checks (liveness/readiness).
- **Infrastructure as Code**: Terraform/Pulumi/CloudFormation for all infrastructure; GitOps (ArgoCD/Flux) for deployment.
- **Security by design**: Defense in depth, zero-trust networking, least-privilege IAM, encryption at rest and in transit, secrets management (Vault/Secrets Manager).
- **Cost awareness**: Model cloud costs early (compute, data transfer, storage, managed services); architect for cost optimization (spot instances, auto-scaling, serverless where appropriate).

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


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `relation "..." does not exist` | Migration not run or wrong database | `npx prisma migrate dev` or check `DATABASE_URL` |
| `deadlock detected` | Concurrent transactions in wrong order | Enforce consistent lock ordering; use `NOWAIT` where appropriate |
| `connection pool exhausted` | Too many concurrent connections | Increase pool size; add connection timeout; check for leaked connections |
| `414 URI Too Long` | Request URI exceeds server limit | Use POST for data-heavy requests; paginate `?filter=` params |


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
