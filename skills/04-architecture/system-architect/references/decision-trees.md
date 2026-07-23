# Decision Trees for system-architect

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
