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

### Delivery Guarantees

```
                      +--------------------------+
                      | START: Delivery semantic   |
                      +------------+-------------+
                                   |
                     +-------------+-------------+
                     | Is data loss acceptable?    |
                     | (metrics, logs, analytics)  |
                     +----+------------------+----+
                          | YES              | NO
                     +----+--------+   +-----+----------+
                     | At-most-once |   | Duplicates MUST   |
                     | (fire/forget,|   | NEVER cause harm? |
                     |  no retry)   |   +--+---------------+
                     +-------------+      | YES        NO
                                     +----+----+ +----+-------+
                                     | At-least-| | Exactly-once|
                                     | once +   | | (idempotent |
                                     | idempot- | | producer +  |
                                     | ency key | | transactional|
                                     | on every | | consumer,    |
                                     | event    | | Kafka trans- |
                                     +----------+ | actions or   |
                                                  | Outbox)      |
                                                  +-------------+
```

### Schema Compatibility Strategy

```
                      +--------------------------+
                      | START: Schema change type  |
                      +------------+-------------+
                                   |
                     +-------------+-------------+
                     | Adding optional field or    |
                     | new event type?             |
                     +----+------------------+----+
                          | YES              | NO
                     +----+--------+   +-----+----------+
                     | BACKWARD      |   | Removing required |
                     | compatible:   |   | field or changing |
                     | deploy         |   | type?            |
                     | consumers      |   +--+---------------+
                     | first, then    |      | YES
                     | producers      | +----+---------+
                     +-------------+   | FULL compat:   |
                                       | NEW event type |
                                       | + coexistence  |
                                       | migration      |
                                       | period (N      |
                                       | releases)      |
                                       +---------------+
```

### Partition Key Selection

```
                      +--------------------------+
                      | START: Choose partition    |
                      | key for topic              |
                      +------------+-------------+
                                   |
                     +-------------+-------------+
                     | Need strict ordering per    |
                     | entity (order, account)?    |
                     +----+------------------+----+
                          | YES              | NO
                     +----+--------+   +-----+----------+
                     | Key = entity  |   | Need even load    |
                     | ID (order_id, |   | distribution?     |
                     | account_id)   |   +--+---------------+
                     | Risk: hot     |      | YES
                     | partition if  | +----+---------+
                     | single entity | | Key = user_id  |
                     | dominates     | | or round-robin |
                     +-------------+ | if ordering     |
                                     | not required    |
                                     +----------------+
```

### Idempotency Strategy

```
                      +--------------------------+
                      | START: Idempotency needed  |
                      +------------+-------------+
                                   |
                     +-------------+-------------+
                     | Consumer performs DB write  |
                     | as part of processing?      |
                     +----+------------------+----+
                          | YES              | NO
                     +----+--------+   +-----+----------+
                     | Use DB unique  |   | Purely side-    |
                     | constraint on  |   | effect (email,  |
                     | idempotency    |   | push, webhook)? |
                     | key + INSERT   |   +--+---------------+
                     | ON CONFLICT    |      | YES
                     | DO NOTHING     | +----+---------+
                     +-------------+   | Redis SETNX +  |
                                       | TTL (24h) to   |
                                       | deduplicate    |
                                       | before acting  |
                                       +---------------+
```
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
