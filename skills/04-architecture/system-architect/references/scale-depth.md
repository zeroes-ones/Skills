# Scale Depth: Solo → Small → Medium → Enterprise

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
