# Architecture Styles Decision Matrix

author: Sandeep Kumar Penchala

## Overview

Choosing an architecture style is the highest-impact technical decision you'll make. The wrong choice costs millions in rework; the right choice enables velocity for years. This guide provides a concrete decision framework — no "it depends" without explaining what it depends on and exactly how to decide.

## The Architecture Spectrum

```
Simplicity ◀──────────────────────────────────────────────▶ Scalability
Monolith ── Modular Monolith ── SOA ── Microservices ── Event-Driven ── Serverless
```

**Core principle**: Start as simple as possible, add complexity only when the data proves you need it. Premature distribution is the root of much architecture evil.

## Decision Matrix: When to Use Each Style

### Modular Monolith

| Factor | Threshold | Why |
|--------|-----------|-----|
| Team size | 1–15 engineers | Single deployable, single codebase. No coordination overhead. |
| QPS | < 5,000 req/s | A well-tuned monolith on modern hardware handles this easily. |
| Deployment frequency | < 5/day | No need for independent service deployments. |
| Data complexity | Single database, < 50 tables | One DB schema is manageable with discipline. |
| Organizational structure | Single team or 2–3 closely collaborating | Conway's Law: one team = one deployable. |

**When to choose**:
- You're building a new product and domain boundaries are unclear
- Time-to-market is the primary constraint
- Team is co-located or in similar time zones
- Domain logic is highly interconnected (few true bounded contexts)

**Implementation pattern**:
```
src/
├── orders/          # Module: everything orders-related
│   ├── api/         #   HTTP handlers, DTOs
│   ├── domain/      #   Business logic, entities, value objects
│   ├── db/          #   Repository, migrations
│   └── events/      #   Events this module publishes
├── catalog/         # Module: everything catalog-related
│   ├── api/
│   ├── domain/
│   ├── db/
│   └── events/
├── shared/          # Cross-cutting: logging, auth, config
└── Main.kt / main.go / main.py  # Composition root
```

**Module rules**:
1. Modules communicate ONLY through public interfaces (not direct DB access)
2. Module A cannot import Module B's internal packages
3. Shared kernel (`shared/`) contains only truly cross-cutting code
4. Each module owns its database tables — no cross-module JOINs in code
5. Module-to-module calls go through an in-process event bus or direct interface calls

**How to enforce**:
- **Python**: Use `__init__.py` with explicit exports; lint with `import-linter`
- **Go**: Use `internal/` directory per module + `go-mod` architecture tests
- **Node.js/TypeScript**: Use ESLint `import/no-restricted-paths` + Nx module boundaries
- **Java/Kotlin**: Use ArchUnit tests (`classes().that().resideInAPackage("..orders..").should().onlyAccessClassesThat()...`)

### Microservices

| Factor | Threshold | Why |
|--------|-----------|-----|
| Team size | 15+ engineers, 3+ teams | Independent teams need independent deployables. |
| QPS | > 5,000 req/s, spiky | Independent scaling per service. |
| Deployment frequency | Multiple times/day per team | Independent deploy cycles. |
| Data complexity | Multiple bounded contexts, > 50 tables | Separate DB per service prevents coupling. |
| Organizational structure | Multiple autonomous teams | Conway's Law: independent teams = independent services. |

**Readiness checklist — DO NOT adopt microservices unless you check ALL of these**:
- [ ] You have identified at least 3 clear bounded contexts with minimal coupling between them
- [ ] You have a platform team (or equivalent) to handle infrastructure, CI/CD, observability
- [ ] You have implemented (or are committed to) distributed tracing before the second service goes live
- [ ] You accept that network calls will fail and have circuit breakers, retries, and timeouts in place
- [ ] You have a plan for distributed data (eventual consistency, saga pattern, or 2PC)
- [ ] You have a deployment pipeline that can deploy any service independently
- [ ] You have API versioning and backward compatibility policies documented
- [ ] You have 15+ engineers — otherwise the coordination overhead of microservices exceeds the benefits
- [ ] You have a plan for integration testing across service boundaries
- [ ] You have a strategy for shared code (libraries, not shared databases)

**If you checked fewer than 8 items, stay with modular monolith.**

### The Distributed Monolith Danger

This is the worst of both worlds and the most common outcome of unprepared microservice adoption:

**Symptoms you have a distributed monolith**:
- Changing one "service" always requires changes in others
- Services share a database (or read each other's databases directly)
- Deployments are coordinated (must deploy A, B, and C together)
- You can't test a service without running 5 others
- Latency is worse than the monolith it replaced
- Debugging a request requires checking logs across 7 services

**How to escape**:
1. Consolidate coupled services back into larger services (reverse microservice)
2. Identify true bounded contexts using event storming
3. Introduce async communication between true contexts
4. Give each remaining service its own data store

### Event-Driven Architecture

| Factor | Threshold | Why |
|--------|-----------|-----|
| Communication pattern | Loose coupling required between domains | Services don't need immediate responses. |
| Data consistency | Eventual consistency acceptable | Events propagate state changes asynchronously. |
| Audit requirements | Full history of state changes needed | Event store = natural audit log. |
| Throughput | > 10,000 events/s | Dedicated event infrastructure handles this. |

**Event types**:
- **Domain Events**: "OrderPlaced", "PaymentReceived" — significant business state changes
- **Integration Events**: Translated domain events for external consumers, with different schema
- **Notification Events**: "EmailSent", "SMSDelivered" — side-effect notifications
- **Delta Events**: Contain only changed fields — "UserUpdated { email: new@email.com }"
- **State Transfer Events**: Full current state snapshot for cache population

**Broker selection**:
| Broker | Throughput | Latency | Message Ordering | Best For |
|--------|-----------|---------|------------------|----------|
| **Kafka** | 1M+ msg/s | ~2-5ms | Per-partition | Event sourcing, high-throughput streaming |
| **RabbitMQ** | ~50K msg/s | ~1ms | Per-queue | Complex routing, reliable delivery, DLQs |
| **SQS + SNS** | Unlimited | ~10-50ms | Best-effort | AWS-native, zero-ops |
| **Redis Streams** | ~100K msg/s | < 1ms | Per-stream | Lightweight, already-have-Redis scenarios |
| **NATS** | ~1M msg/s | < 1ms | Per-subject | Low-latency, simple topologies |

**Event schema evolution**:
1. **Never remove fields** — mark as deprecated, stop producing, remove after all consumers migrated
2. **Add fields as optional** — backward-compatible: old consumers ignore, use default
3. **Use schema registry** — Confluent Schema Registry (Avro), or JSON Schema versioned per topic
4. **Version events explicitly** — `order.placed.v1`, `order.placed.v2` as separate topics or use `type` field

**When NOT to use event-driven**:
- Simple CRUD with no cross-domain workflows → REST is simpler
- You need synchronous confirmation of cross-service actions → use request-response with saga orchestration
- Team has no experience with async patterns → the debugging complexity will kill velocity

### Serverless (FaaS)

| Factor | Threshold | Why |
|--------|-----------|-----|
| Traffic pattern | Spiky, unpredictable, or very low (< 100 req/day) | Pay-per-use economics win. |
| Execution time | < 15 minutes (AWS), < 60 min (GCP) | Platform limits. |
| Cold start tolerance | Can accept 200ms-2s cold starts | Provisioned concurrency mitigates but costs more. |
| State | Stateless functions, state externalized to DB/cache | No in-memory state between invocations. |

**When serverless is the right call**:
- Event processing pipelines (S3 upload → Lambda → DynamoDB)
- Scheduled jobs (cron replacement)
- Webhook handlers
- API backends with highly variable traffic (0 at night, 1000 at peak)
- Glue code between managed services

**When serverless is wrong**:
- Long-running processes (> 15 min)
- Consistent high throughput (cheaper on EC2/containers)
- WebSocket-heavy applications (use containers)
- GPU/ML inference (use dedicated instances)
- You need fine-grained control over the runtime environment

## Decision Algorithm

```
1. How many engineers? 
   < 15 → Modular Monolith (stop here)
   ≥ 15 → Continue

2. Can you identify 3+ bounded contexts with loose coupling?
   No → Modular Monolith (revisit in 6 months)
   Yes → Continue

3. Do you have platform/infra support (CI/CD, observability, service mesh)?
   No → Modular Monolith + invest in platform first
   Yes → Continue

4. Is your traffic spiky/unpredictable AND each request is short-lived?
   Yes → Serverless for compute, managed services for data
   No → Continue

5. Do you need cross-domain workflows with loose coupling AND audit trails?
   Yes → Event-Driven with microservices
   No → Microservices with sync communication (REST/gRPC) + async where needed
```

## Scale-Based Recommendations

### 0–1,000 users
- **Style**: Monolith (not even modular — single Django/Rails/Express app)
- **Infra**: Single VPS or PaaS (Railway, Render). One database. No cache.
- **Why**: You're proving product-market fit. Architecture doesn't matter yet. Speed matters.

### 1,000–100,000 users
- **Style**: Modular Monolith
- **Infra**: 2-3 app servers behind load balancer. Managed database with read replicas. Redis for cache. CDN for static assets.
- **Why**: You need reliability but not distributed complexity. Module boundaries give you migration paths.

### 100,000–1,000,000 users
- **Style**: Microservices (5-10 services) + async for cross-boundary workflows
- **Infra**: Kubernetes or ECS. Service mesh (Istio/Linkerd). Message broker. Distributed tracing mandatory.
- **Why**: Team scale demands independent deployability. Traffic demands independent scaling.

### 1,000,000+ users
- **Style**: Event-Driven with microservices (20-50+ services) + serverless for spiky workloads
- **Infra**: Multi-region Kubernetes. Kafka for events. Specialized databases per service. Full observability platform.
- **Why**: Scale demands specialization. Events decouple services across regions and teams.

## Anti-Patterns to Recognize and Avoid

1. **Premature Microservices**: Splitting before bounded contexts are clear. Result: distributed monolith, worse than the original.
2. **Nanomonolith**: Too many tiny services (1-2 endpoints each). Result: explosion of deployment units with no benefit.
3. **Serverless for Everything**: Wrapping every endpoint as a Lambda. Result: cold starts everywhere, impossible to debug.
4. **Event-Driven Everything**: Using events for simple request-response. Result: indirection that makes debugging a nightmare.
5. **Shared Database Across Services**: The #1 cause of microservice failure. Result: you can never deploy independently.

## Migration Strategies

### Strangler Fig Pattern
Replace monolith functionality incrementally:
1. Route new feature requests to new service
2. Existing functionality stays in monolith
3. Gradual feature parity — one endpoint at a time
4. When all traffic to a feature is in new service, remove from monolith

**Metrics to track during migration**:
- % of traffic served by new services vs monolith
- Latency comparison (monolith vs new service) for migrated endpoints
- Error rate comparison
- Developer velocity (time to ship a feature before vs after extraction)

### Feature Flags for Gradual Migration
```python
if feature_flag.is_enabled("new-order-service", user_id=request.user_id):
    return order_service.create_order(request)
else:
    return monolith.create_order(request)
```

This allows:
- Canary testing with 1% of users
- Instant rollback by flipping a flag
- A/B testing performance between old and new

## References
- [Building Microservices, 2nd Edition](https://samnewman.io/books/building_microservices_2nd_edition/) — Sam Newman
- [Fundamentals of Software Architecture](https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/) — Mark Richards & Neal Ford
- [Software Architecture: The Hard Parts](https://www.oreilly.com/library/view/software-architecture-the/9781492086888/) — Neal Ford et al.
- [Monolith to Microservices](https://samnewman.io/books/monolith-to-microservices/) — Sam Newman
