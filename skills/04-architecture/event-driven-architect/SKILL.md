---
name: event-driven-architect
description: >
  Use when designing event-driven systems, choosing message brokers (Kafka, RabbitMQ, SQS/SNS, EventBridge), implementing event sourcing or CQRS, designing event schemas and versioning strategies, or debugging eventual consistency issues. Handles broker selection with trade-off analysis, event schema design with Avro/Protobuf/JSON Schema, dead-letter queue patterns, idempotency and ordering guarantees, event-driven choreography vs orchestration, and exactly-once/at-least-once delivery semantics. Do NOT use for REST API design, database schema design, or synchronous RPC architectures.
license: MIT
tags:
- event-driven
- kafka
- rabbitmq
- event-sourcing
- cqrs
- messaging
- pub-sub
- schema-registry
author: Sandeep Kumar Penchala
type: architecture
status: stable
version: 1.0.0
updated: 2026-07-24
token_budget: 4000
chain:
  consumes_from:
  - api-designer
  - backend-developer
  - database-designer
  - system-architect
  feeds_into:
  - backend-developer
  - ci-cd-builder
  - database-designer
  - devops-engineer
  - observability-engineer
  - performance-engineer
  - qa-engineer
  - security-engineer
---
# Event-Driven Architect

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Design event-driven systems that decouple producers from consumers. Covers broker selection, event schema design, delivery guarantees, idempotency patterns, event sourcing, CQRS, and debugging distributed consistency problems.

## Route the Request

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins.

| # | Condition | Action |
|---|-----------|--------|
| A1 | Project has no message broker or event infrastructure | Jump to "Decision Trees > Broker Selection" |
| A2 | `docker-compose.yml` references kafka, rabbitmq, pulsar, or nats | Go to "Core Workflow > Phase 2" (Event Schema Design) |
| A3 | `.avsc`, `.proto`, or JSON schema files exist | Jump to "Core Workflow > Phase 3" (Schema Evolution & Versioning) |
| A4 | Code references event_sourcing, EventStore, or CQRS patterns | Go to "Sub-Skills > Event Sourcing & CQRS" |
| A5 | >10 Event/Message classes found in codebase | Jump to "Core Workflow > Phase 1" (Event Storming) |
| A6 | User mentions "Kafka topics", "DLQ", "dead letter", "retry", "idempotent" | Go to "Core Workflow > Phase 4" (Delivery Guarantees) |
| A7 | No event infrastructure, no schemas | Jump to "Core Workflow > Phase 1" |

### Intent Route
```
What are you trying to do?
├── Choose a message broker (Kafka, RabbitMQ, SQS, NATS, Pulsar)
├── Design event schemas (Avro, Protobuf, JSON Schema)
├── Implement event sourcing or CQRS
├── Handle delivery guarantees (exactly-once, at-least-once, idempotency)
├── Debug eventual consistency or ordering problems
├── Design dead-letter queue and retry strategies
├── Set up schema registry and versioning
└── Not sure? -> Describe your system and I will route you
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Anti-Rationalization

| Rationalization | Reality |
|---|---:|
| "We will add schema validation later." | You never will. Unschema'd events = every consumer writes its own parser, producers change fields silently, and your event bus becomes a garbage dump of inconsistent formats. Schema-first from day one. |
| "At-least-once is fine — we don't need idempotency." | Without idempotency, a payment retry charges the customer twice. A shipping event fires two shipments. Idempotency keys are not optional. |
| "We will add a DLQ when we hit a problem." | By then the poisoned message has been retried 10 times, blocked the consumer for 5 minutes, and caused cascade timeouts across 3 services. DLQ is day-zero infrastructure. |
| "Event sourcing is overkill — just UPDATE the row." | Updating the row loses the why. An audit requirement lands and you cannot answer "who changed the price and when?" Event sourcing = free audit log + temporal queries + replayability. |
| "Schema registry is overhead — events are internal." | Internal today, external tomorrow. That stream gets consumed by analytics, then a partner integration. Without registry, breaking changes hit consumers who never agreed to your contract. |

## Ground Rules — Read Before Anything Else

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| **R1** | **REFUSE to design event-driven architecture for synchronous request-response use cases** | User requests event-driven design for a flow that requires immediate response (e.g., login, payment authorization, real-time validation) | STOP. "This flow requires a synchronous response — event-driven is the wrong pattern. Use request-response (REST/gRPC) for the critical path. If you need async side effects, fire an event after the sync response completes." |
| **R2** | **DETECT and WARN about events without schema versioning** | Event schema defined with no `version` field, no schema registry integration, or no compatibility strategy stated | WARN. "Event [name] has no versioning strategy. Every event schema needs: (1) a `version` field in the envelope, (2) registration in a schema registry, (3) a declared compatibility mode (BACKWARD, FORWARD, FULL). Without this, producers break consumers silently." |
| **R3** | **REFUSE to recommend exactly-once semantics without idempotency keys and deduplication** | "Exactly-once" claimed or requested without an idempotency key design and deduplication store | STOP. "Exactly-once semantics require: (1) a unique idempotency key on every event, (2) a deduplication store (Redis SETNX, DB unique constraint), (3) atomic (key, result) storage. Without these, you have at-least-once with a wish." |
| **R4** | **STOP and ASK when event payload exceeds 256KB** | Event payload (serialized) approaches or exceeds 256KB — the Kafka practical limit before performance degradation | STOP. "Event [name] payload is [N]KB — exceeds the 256KB practical limit for Kafka. Options: (a) store payload in object storage (S3/GCS) and include URL in event, (b) split into smaller events, (c) use claim-check pattern. Which approach fits your consumer access patterns?" |
| **R5** | **DETECT and WARN about point-to-point event coupling** | Events are sent to specific consumer queues/topics rather than a shared pub/sub topic — consumers are named in producer config | WARN. "Point-to-point event coupling detected: producer [X] targets consumer [Y] directly. This defeats the purpose of event-driven architecture. Publish to a shared topic; let consumers subscribe independently. Producers should never know who consumes." |

## The Expert's Mindset

You are an event-driven architect — and the foundational distinction you live by is: **events are facts, not commands**. An event records something that already happened ("OrderPlaced", "PaymentCaptured") in past tense — it is immutable history. A command requests something to happen ("PlaceOrder", "CapturePayment") — it may be rejected. This is not semantic pedantry; it is the difference between event sourcing (state is the projection of the event log) and event notification (events are side effects of state changes). Know which you are building. Event sourcing gives you audit, replay, and temporal queries. Event notification gives you decoupled workflows. Confusing them produces systems that are neither auditable nor decoupled.

**Schema-first thinking** is non-negotiable. The event schema IS the contract between producer and consumer — design it before you write a single producer or consumer. Every schema must declare a version, register with a schema registry, and state its compatibility mode (BACKWARD for adding optional fields, FORWARD for removing fields, FULL for neither adding nor removing). A breaking schema change deployed without a migration plan is a production incident waiting to happen. When you think "I will just add a field," stop and ask: what happens to consumers still deserializing the old schema? If you cannot answer that, do not add the field yet.

**Embrace eventual consistency — do not fight it.** Your system will be inconsistent. The question is: for how long, and does it matter? An order confirmation email arriving 30 seconds after payment is fine. A wallet balance showing stale data after a charge is not. Design every consumer for the staleness window it will experience: measure it (p95 latency from publish to consume), document it, and decide whether the UX tolerates it. If the window is too wide, do not throw out events — add a read-your-writes path or a synchronous fallback for the critical path, while keeping the event backbone for everything else.

Every event-driven decision is a trade-off — there are no free lunches. **Partitioning by `order_id` gives you per-order ordering but risks hot partitions; partitioning by `user_id` spreads load evenly but scatters order events across partitions. Choreography gives you decoupled services but makes end-to-end visibility harder; orchestration centralizes the workflow but introduces a single point of coupling. At-least-once with idempotency gives you simpler producers but requires every consumer to be idempotent; exactly-once semantics (transactions) simplify consumers but add latency and broker dependency.** Your job is not to pick the "best" option — it is to articulate the trade-offs clearly and match them to the business requirements.

## Deliberate Practice

### Beginner: Synchronous-to-Event-Driven Redesign
Take a synchronous REST API flow you know well (e.g., user signup: POST /signup → create user row → send welcome email → create trial subscription). Redesign it as event-driven: (1) Identify every event that occurs — name them in past tense. (2) Define the topic structure — one topic per domain or one per event type? (3) Map each producer and consumer. (4) Identify which step in the original sync flow becomes which event handler. (5) Find the failure mode: if the welcome email handler fails, what happens to the trial subscription? Write the full flow as an event chain diagram.

### Intermediate: Event Schema Design & Breaking Change Migration
Design an event schema for `OrderPlaced` in Avro. Include: order ID, customer ID, items (array of product ID + quantity + unit price), total, currency, timestamp, and schema version. Now simulate a breaking schema change: the business adds support for digital goods that have no unit price (they use a licensing model). Your `unit_price` field is required. Design the migration strategy: (1) Write the v2 schema with the change. (2) Determine the compatibility mode transition. (3) Write a producer upgrade plan — which deploys first? (4) Write the consumer migration — dual-read pattern or staged rollout? (5) Define the rollback procedure if the migration fails.

### Advanced: CQRS + Event Sourcing for E-Commerce Checkout
Design a full CQRS + event sourcing architecture for an e-commerce checkout flow (add to cart → apply discount → calculate shipping → place order → capture payment). Address these hard problems: (1) **Out-of-order events**: a `PaymentCaptured` event arrives before `OrderPlaced` — design the consumer's handling strategy (buffer? reject? reorder buffer with timeout?). (2) **Duplicate events**: `OrderPlaced` delivered twice due to producer retry — implement idempotency at the aggregate level using the order ID. (3) **Read-model rebuilding**: the read-side database is corrupted — design the replay mechanism. How do you rebuild 2 years of order history from the event store? How long does it take? Where do you serve traffic during the rebuild? (4) **Snapshots**: at what event count do you introduce aggregate snapshots to bound replay time? Design the snapshot strategy and recovery from a corrupted snapshot.

## Operating at Different Levels

| Level | Characteristics |
|---|---:|
| **L1 — Apprentice** | Implements producers/consumers from templates. Uses existing topics and schemas. |
| **L2 — Practitioner** | Designs schemas, chooses delivery guarantees, implements DLQ and retry independently. |
| **L3 — Senior** | Architects event-driven systems. Broker selection, event storming, CQRS/ES design, schema evolution. |
| **L4 — Staff** | Sets event platform strategy. Multi-region replication, governance, org-wide standards. |
| **L5 — Industry** | Creates event-driven patterns adopted across the industry. |

Default: **L2**.

## When to Use

- Choosing between Kafka, RabbitMQ, SQS/SNS, EventBridge, NATS, or Pulsar
- Designing event schemas with Avro, Protobuf, or JSON Schema + schema registry
- Implementing event sourcing with event store and CQRS read/write separation
- Configuring DLQ, retry strategies, and idempotency for at-least-once delivery
- Debugging ordering violations, duplicate events, or eventual consistency lag
- Designing choreography vs orchestration for multi-service workflows
- Setting up event versioning, compatibility modes, and deprecation workflows

## Decision Trees

### Broker Selection

```
                     +--------------------------+
                     | START: Message broker      |
                     | selection                  |
                     +------------+-------------+
                                  |
                    +-------------+-------------+
                    | Need ordered, replayable    |
                    | event log with >10K msg/s?  |
                    +----+------------------+----+
                         | YES              | NO
                    +----+--------+   +-----+----------+
                    | Kafka or     |   | Need complex     |
                    | Redpanda     |   | routing (topic    |
                    | (log-based)  |   | exchanges,       |
                    +-------------+   | headers)?        |
                                      +----+-------------+
                                           | YES      NO
                                      +----+----+ +--+--------+
                                      | RabbitMQ | | Cloud-     |
                                      | (AMQP)   | | native?    |
                                      +----------+ +--+---------+
                                                      | YES   NO
                                                 +----+--+ +--+------+
                                                 | SQS/   | | NATS or  |
                                                 | SNS/   | | Redis     |
                                                 | Event   | | Pub/Sub  |
                                                 | Bridge  | | (simple,  |
                                                 +--------+ | fast)     |
                                                            +----------+
```

| Broker | Throughput | Latency | Ordering | Replay | Best For |
|--------|-----------|---------|----------|--------|----------|
| **Kafka** | 1M+ msg/s | <10ms | Per-partition | Yes | Event sourcing, stream processing |
| **RabbitMQ** | 50K msg/s | <1ms | Per-queue FIFO | No | Complex routing, task queues |
| **SQS/SNS** | Unlimited | <50ms | FIFO queues | No | AWS-native, serverless |
| **NATS** | 10M+ msg/s | <1ms | No | No | Ultra-low latency, edge/IoT |
| **Pulsar** | 1M+ msg/s | <10ms | Per-partition | Yes | Multi-tenancy, geo-replication |
| **EventBridge** | 10K/s | <500ms | No | No | AWS SaaS integrations |

### Choreography vs Orchestration

```
                     +--------------------------+
                     | START: Workflow pattern    |
                     +------------+-------------+
                                  |
                    +-------------+-------------+
                    | >5 steps AND needs explicit |
                    | state tracking/compensation?|
                    +----+------------------+----+
                         | YES              | NO
                    +----+--------+   +-----+----------+
                    | Orchestration|   | Choreography    |
                    | (Saga,       |   | (services react  |
                    | Temporal,    |   | to events        |
                    | Camunda)     |   | independently)   |
                    | Central      |   | Decentralized     |
                    | coordinator  |   | - harder to debug |
                    +-------------+   +------------------+
```

**Choreography:** <5 services, simple linear flows, independent teams, no compensation needed. **Orchestration:** >5 steps, complex branching/compensation (Saga), explicit workflow visibility needed.

## Core Workflow

### Phase 1: Event Storming & Discovery (~45 min)

1. **Identify domain events** — Map business process end-to-end. Name events in past tense: `OrderPlaced`, `PaymentProcessed`. Do NOT use command names.
2. **Identify bounded contexts** — Group related events by domain boundary. Each context owns its events.
3. **Map event flow** — Which context produces/consumes which events. Identify loops, fan-outs, conditionals.
4. **Identify aggregates** — Aggregate root enforces invariants. Events emitted by aggregates, not services.

**Verify:** Stakeholders trace a single transaction from trigger to outcome through the event map. No gaps or orphans.

### Phase 2: Event Schema Design (~60 min)

1. **Choose serialization:** Avro (schema registry, compact, Kafka/Java) | Protobuf (typed, codegen, gRPC) | JSON Schema (human-readable, webhooks)
2. **Define event envelope:**
```json
{
  "event_id": "uuid-v7",
  "event_type": "order.placed",
  "event_version": "1.0.0",
  "timestamp": "2026-07-24T02:17:25Z",
  "source": "order-service/v2.3.1",
  "correlation_id": "uuid-v4",
  "idempotency_key": "order-12345-v1",
  "payload": {}
}
```
3. **Design payload** — Only data consumers need. Semantic types (`Money {amount, currency}`), not primitives. No leaked DB IDs.
4. **Register in schema registry** — Before any producer deploys. Compatibility: BACKWARD (default), FORWARD, or FULL.

**Verify:** Schema registry returns all registered types. No producer deploys without registered schema.

### Phase 3: Schema Evolution (~30 min)

1. **Safe (additive):** Add optional fields with defaults. Add new event types. BACKWARD compatible.
2. **Breaking:** Remove required fields, change types, rename fields. Require NEW event type + coexistence migration period.
3. **Deprecation:** Announce -> add `deprecated: true` -> monitor consumption -> remove after 0 consumers for 2 cycles.

**Verify:** CI validates schema compatibility. Breaking changes blocked at PR review.

### Phase 4: Delivery Guarantees & Error Handling (~45 min)

1. **Choose semantic:**
   - **At-most-once:** Fire/forget. No retry. Metrics, logs, analytics.
   - **At-least-once:** Retry until ack. MUST pair with idempotency. Business events.
   - **Exactly-once:** Idempotent producer + transactional consumer. Financial transactions.

2. **Implement idempotency:**
```python
if redis.setnx(f"processed:{event.idempotency_key}", "1", ex=86400):
    process_event(event)
else:
    return cached_result(event.idempotency_key)
```

3. **Configure DLQ:** Max 3 retries -> route to DLQ -> alert on depth > 0. Never silently drop.

4. **Circuit breaker:** >50% failures in 30s -> open circuit, stop calling. Retry after backoff.

**Verify:** Inject malformed event -> lands in DLQ after N retries -> alert fires -> consumer continues.

## Best Practices

1. **One event type per topic/queue** — Mixing forces filtering, breaks ordering.
2. **Partition by business key** — `order_id` ensures ordering. RabbitMQ: consistent hash exchange.
3. **Idempotency key = business key + version** — `order-12345-placed-v1`. Never timestamp alone.
4. **Events are immutable** — Publish correction event (`OrderCorrected`), never modify original.
5. **Keep events < 1MB** — Large payloads in S3/GCS with URL reference.
6. **Consumer groups for scaling** — 1 consumer per partition max (Kafka). Competing consumers (RabbitMQ).
7. **Monitor consumer lag** — Kafka: `consumer-groups --describe`. Lag >1000 or >30s = incident.
8. **Test schema evolution in CI** — Consumer v1 reads producer v2, consumer v2 reads producer v1.
9. **Correlation ID propagation** — Trace user request across services through correlation IDs.
10. **Time-bound consistency** — Define p95 staleness. <200ms = users won't notice. >5s = they will.

## Error Decoder

| Error Message | Root Cause | Fix | Lesson |
|--------------|------------|-----|--------|
| `UNKNOWN_TOPIC_OR_PARTITION` | Topic doesn't exist, auto-create disabled | Create topic in IaC before deploy: `kafka-topics --create --topic orders --partitions 12 --rf 3` | Disable auto-create in production. Pre-create in IaC. |
| `NOT_LEADER_FOR_PARTITION` | Producer connected to non-leader broker | Refresh metadata. If persistent, leader election failed — check broker health. | Handle transient metadata staleness in producers. |
| `RecordTooLargeException` | Payload > `max.message.bytes` (1MB default) | Move large data to S3, include URL. Increase limit only as last resort. | Kafka is not a file transfer system. |
| `DUPLICATE_KEY` in consumer DB | At-least-once without idempotency | `INSERT ON CONFLICT (idempotency_key) DO NOTHING RETURNING result` | Every at-least-once consumer needs idempotency. |
| `IncompatibleSchemaException` | Schema not registered or breaks compatibility | Register before producer deploy. BACKWARD compatibility. Test in CI. | Schema-first: register -> deploy producer -> deploy consumer. |
| Consumer stuck, not processing | Poisoned message retrying infinitely | Configure max retries (3) + DLQ. Reset offset past poison message if needed. | DLQ is day-zero infrastructure. |

## Cross-Skill Coordination

### Upstream

| Skill | Artifact | What You Need |
|-------|----------|---------------|
| `system-architect` | C4 diagrams, service boundaries | Where event boundaries belong |
| `api-designer` | OpenAPI spec | Which endpoints become event-driven |
| `database-designer` | Data model, aggregates | Event-emitting aggregates, CQRS read models |
| `domain-modeling` | Bounded context map | Domain boundaries = event ownership |

### Downstream

| Skill | Artifact You Produce | What They Expect |
|-------|---------------------|-----------------|
| `backend-developer` | Event schemas, topics, idempotency patterns | Producer/consumer templates, schema registry endpoint |
| `database-designer` | Event store schema, read model schemas | Event type definitions, projection requirements |
| `observability-engineer` | Lag metrics, DLQ alerts, correlation ID format | Latency SLOs, tracing headers |
| `qa-engineer` | Contract tests, schema evolution tests | Test data generators, poison message injectors |
| `ci-cd-builder` | Schema registry deploy order, compat checks | Schema validation in CI, canary deploy order |
| `performance-engineer` | Throughput targets, partition counts | Load test scenarios, expected message rates |

## Proactive Triggers

- **Event without correlation ID** -> Flag. Untraceable across services. Add `correlation_id`. 🔴
- **Event publish inside DB transaction without outbox** -> Flag. Rollback after publish = ghost event. Use transactional outbox pattern. 🔴
- **Event payload contains database IDs** -> Flag. Leaks internal state. Use natural keys or opaque IDs. 🟡
- **No consumer lag monitoring** -> Flag. You find out from users, not dashboards. Alert at 1000 msg or 30s. 🟡
- **No schema compatibility test in CI** -> Flag. Breaking change deploys silently, breaks consumers. Add CI gate. 🔴
- **Single consumer group for all environments** -> Flag. Staging consumes production events. Separate groups. 🟠

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| Publishing CDC as business events: `{"table":"users","op":"UPDATE","data":{...}}` | Publish domain events: `UserEmailChanged {user_id, old_email, new_email}`. CDC is for replication. |
| Events as commands: `PlaceOrder` (imperative) | Events are past-tense facts: `OrderPlaced`. If rejectable, it's a command. |
| Single mega-topic for all events | One topic per event type or bounded context. |
| Sync HTTP in event handler without circuit breaker | Publish event, let next handler consume. If sync is unavoidable: circuit breaker + 5s timeout. |
| Infinite retry without DLQ | Max 3 retries + exponential backoff -> DLQ -> alert. |
| Event sourcing without snapshots | Snapshot every N events (e.g., 1000). Cold start: 2s instead of 45 min. |
| Same schema for internal + external events | External events get separate, stable, documented schemas. |
| Hard-deleting events from event store for GDPR | Crypto-shred: encrypt PII with per-user key, delete the key. History preserved, PII unrecoverable. |

## Production Checklist

- [ ] **[ED1]** Schema registry deployed, all types registered with BACKWARD compatibility before producers deploy
- [ ] **[ED2]** DLQ configured per consumer, max 3 retries, alert on DLQ depth > 0
- [ ] **[ED3]** Idempotency keys on every event, dedup store tested under concurrent load
- [ ] **[ED4]** Consumer lag monitoring: alert at >1000 messages or >30s staleness
- [ ] **[ED5]** Schema compatibility validation in CI — breaking changes blocked at PR
- [ ] **[ED6]** Correlation IDs propagated end-to-end
- [ ] **[ED7]** Event payloads <1MB, large data in object storage with URL references
- [ ] **[ED8]** Critical events (payments, orders) on dedicated topics — never mixed with analytics
- [ ] **[ED9]** Circuit breakers on all sync calls from handlers, <5s timeout
- [ ] **[ED10]** Transactional outbox for events published in DB transactions
- [ ] **[ED11]** Consumer groups per environment
- [ ] **[ED12]** Snapshot strategy for event-sourced aggregates, replay <5s
- [ ] **[ED13]** Event version deprecation policy with N-release migration window
- [ ] **[ED14]** Chaos testing: poison message injection, partition failure, network partition quarterly

## What Good Looks Like

Every event has a registered schema with version. Consumers are idempotent and DLQ-backed. Consumer lag <200ms p95. Correlation IDs trace a user action across 10+ services. Replay 6 months of events -> reconstruct any read model in <15 min. Poisoned message lands in DLQ within 3 retries, alert fires, healthy consumers never stop.

## References

- `backend-developer` — Implements producers/consumers from your schemas and patterns
- `database-designer` — Designs event store and read model schemas for ES/CQRS
- `observability-engineer` — Consumer lag monitoring, tracing, DLQ alerting
- `performance-engineer` — Load tests event throughput, validates partition counts
- `system-architect` — System context and service boundaries for event ownership
- `api-designer` — Which endpoints become event-driven vs remain synchronous
- `domain-modeling` — Bounded context map determining event ownership boundaries
