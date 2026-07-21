# Communication Patterns

author: Sandeep Kumar Penchala

## Overview

Every distributed system is a network of communicating components. The communication pattern you choose determines your system's latency profile, failure modes, consistency guarantees, and debugability. This guide covers when to use synchronous vs asynchronous communication, which protocol to choose, and how to implement each pattern correctly.

## The Fundamental Choice: Sync vs Async

```
Need immediate response from another service?
├── YES → Synchronous (REST, gRPC, GraphQL)
│         Latency = sum of all service call latencies
│         Availability = product of all service availabilities
│         0.99 × 0.99 × 0.99 = 0.97 (3 nines → 2 nines!)
│
└── NO → Asynchronous (Events, Messages, Queues)
          Latency = independent per service
          Availability = independent per service
          Adds: eventual consistency complexity
```

### When Synchronous is Right
- User is waiting for a response (request-response cycle)
- The operation MUST succeed or fail atomically (payment + order creation)
- The calling service needs the result to continue processing
- The data is small and the called service is fast (< 50ms)

### When Asynchronous is Right
- The caller doesn't need an immediate result ("fire and forget" — send email, generate report)
- Multiple services need to react to the same event
- You want to decouple services from each other's availability
- The operation is long-running (> 500ms)
- You need to buffer requests during traffic spikes

## Synchronous Patterns

### REST (Representational State Transfer)

**Best for**: Public APIs, browser-to-server, cross-organization, caching-friendly reads.

**When to use over gRPC**:
- External/public APIs where HTTP tooling matters (curl, browser, Postman)
- You need HTTP caching (CDN, browser cache, proxy cache)
- Client diversity is high (mobile, web, third-party, curl scripts)
- Human-readable debugging is important

**When NOT to use**:
- High-throughput internal service-to-service (use gRPC)
- Streaming/bidirectional (use gRPC or WebSocket)
- Very large payloads (use gRPC with streaming)

**Implementation checklist**:
- [ ] Resource-oriented URLs: `/orders/{id}` not `/getOrder?id={id}`
- [ ] Consistent error format (RFC 7807 Problem Details)
- [ ] HATEOAS links for discoverability (at minimum, `self` link)
- [ ] ETag/If-None-Match for conditional requests and caching
- [ ] `Prefer: respond-async` header for long-running operations
- [ ] `Idempotency-Key` header for safe retries on mutations
- [ ] Proper HTTP status codes (201 for creation, 202 for accepted async, 409 for conflict)

### gRPC (gRPC Remote Procedure Call)

**Best for**: Internal service-to-service, high-throughput, strongly-typed contracts, polyglot environments.

**When to use over REST**:
- Internal microservice communication (> 100 req/s per service pair)
- You need streaming (server, client, or bidirectional)
- You want code-generated type-safe clients
- Bandwidth matters (protobuf is 3-10x smaller than JSON)
- You need built-in deadlines/cancellation propagation
- Polyglot environment with strong contract enforcement

**When NOT to use**:
- Browser-to-server (gRPC-Web exists but has limitations)
- External partners (they won't adopt your protobuf)
- Simple CRUD with few consumers
- You can't handle protobuf build step in CI/CD

**Streaming patterns**:

1. **Unary** (1 request, 1 response): `rpc GetOrder(GetOrderRequest) returns (Order);`
   - Standard request-response. Most common.

2. **Server Streaming** (1 request, N responses): `rpc ListOrders(ListOrdersRequest) returns (stream Order);`
   - Use for: large result sets, real-time feeds, log streaming
   - Client reads until EOF

3. **Client Streaming** (N requests, 1 response): `rpc UploadFile(stream FileChunk) returns (UploadResult);`
   - Use for: file uploads, bulk operations, telemetry ingestion
   - Server processes all then responds

4. **Bidirectional Streaming** (N requests, M responses): `rpc Chat(stream Message) returns (stream Message);`
   - Use for: chat, collaborative editing, real-time games
   - Independent read/write streams

**Deadlines and timeouts (CRITICAL)**:
```
Every gRPC call MUST set a deadline. Without one:
- A hung server will keep the connection open indefinitely
- Client goroutines/threads will accumulate
- Eventually: cascading thread exhaustion

Rule of thumb: deadline = P99 latency × 3
If P99 is 100ms, deadline = 300ms
```

### GraphQL

**Best for**: Client-driven data fetching, multiple frontend clients (web, iOS, Android), complex nested data.

**When to use over REST**:
- Frontend teams need flexible queries (different screens, different data shapes)
- You have deeply nested/relational data (user → orders → items → product)
- Over-fetching is a real problem (mobile on slow networks)
- Multiple client types need different data from the same endpoint

**When NOT to use**:
- Simple CRUD with fixed data shapes (REST is simpler)
- Server-to-server communication (use gRPC)
- You can't invest in N+1 prevention, query complexity analysis, and depth limiting
- Caching is critical (GraphQL uses POST, which CDNs don't cache)

**Critical operational concerns**:
1. **N+1 prevention** (DataLoader): Batch and cache database calls within a single request. Without DataLoader, every nested field becomes a separate DB query.
2. **Query depth limiting**: `query { user { orders { items { product { reviews { author } } } } } }` — 6 levels deep, potential DoS. Limit to 5-7.
3. **Query complexity analysis**: Assign costs to fields. Reject queries with cost > threshold (e.g., 1000). Prevents `{ users { orders { items } } }` × 1000 users explosion.
4. **Rate limiting by complexity**: 100 simple queries/hour or 10 complex queries/hour per user.
5. **Persisted queries**: Store queries server-side, client sends hash. Prevents arbitrary query injection.

### WebSocket / SSE (Server-Sent Events)

**WebSocket** (bidirectional): Chat, live collaboration, real-time games
**SSE** (server→client only): Live feeds, notifications, progress updates

**Use when**: Client needs real-time updates pushed from server without polling.
**Skip when**: Polling every 5-30s is acceptable (far simpler to implement and debug).

## Asynchronous Patterns

### Message Queues (Point-to-Point)

One producer, one consumer. Exactly-once processing semantics (with idempotency).

**Use for**:
- Task distribution (image processing, report generation)
- Work queues (one task processed by exactly one worker)
- Load leveling (buffer between producer and consumer)

**Broker: RabbitMQ, SQS, ActiveMQ**

### Publish-Subscribe (Pub/Sub)

One producer, multiple consumers. Each consumer gets every message.

**Use for**:
- Notifications (order placed → email service + analytics service + inventory service)
- Cache invalidation (data changed → all cache instances invalidate)
- Cross-service state propagation

**Broker: Kafka, SNS+SQS, Redis Pub/Sub, NATS**

### Event Streaming (Kafka)

Immutable ordered log of events. Consumers track their own offset. Replay possible.

**Use for**:
- Event sourcing (rebuild state by replaying events)
- Audit trails (complete history of all state changes)
- Real-time analytics (process streams of events)
- Change Data Capture (CDC — database changes as event stream)

### The Saga Pattern

Distributed transactions without 2PC (Two-Phase Commit). A saga is a sequence of local transactions, each publishing an event that triggers the next step.

**Two implementation styles**:

**Choreography** (decentralized):
```
Order Service: "OrderPlaced" → Payment Service listens → "PaymentProcessed" 
→ Inventory Service listens → "StockReserved" → Shipping Service listens
```

- **Pros**: Loose coupling, no single point of failure
- **Cons**: Hard to understand the flow end-to-end, cyclic dependencies hard to spot

**Orchestration** (centralized):
```
Saga Orchestrator: 
  1. Tell Payment Service to process payment → wait for response
  2. Tell Inventory Service to reserve stock → wait for response
  3. Tell Shipping Service to create shipment → wait for response
```

- **Pros**: Clear flow, easy to understand, centralized error handling
- **Cons**: Orchestrator becomes a single point of coordination, can become a god object

**Compensating transactions**:
Every saga step needs a compensating action for rollback:
```
Step 1: Create Order      → Compensate: Cancel Order (set status = CANCELLED)
Step 2: Reserve Inventory → Compensate: Release Inventory
Step 3: Charge Payment    → Compensate: Refund Payment
Step 4: Create Shipment   → Compensate: Cancel Shipment
```

**Saga guarantees**:
- **Backward recovery**: If step N fails, execute compensating transactions for steps N-1, N-2, ..., 1
- **Forward recovery**: Retry step N until it succeeds (if failure is transient)
- **Idempotency**: EVERY saga step and compensating action MUST be idempotent

### Outbox Pattern

**Problem**: You update the database AND publish an event. If one fails without the other, you have inconsistency:
- DB updated, event NOT published → other services never know
- Event published, DB NOT updated → other services act on stale/nonexistent data

**Solution**: Use the database as the source of truth for events:

```sql
-- In the SAME transaction:
BEGIN;
  INSERT INTO orders (id, user_id, status, amount) VALUES (...);
  INSERT INTO outbox (id, aggregate_type, aggregate_id, event_type, payload) 
    VALUES (gen_random_uuid(), 'order', 'ord_123', 'OrderPlaced', '{"order_id": "ord_123", ...}');
COMMIT;
```

A separate process (Change Data Capture or poller) reads the outbox table and publishes to the message broker.

**Implementation options**:
1. **Debezium + Kafka Connect**: CDC on outbox table, auto-publish to Kafka
2. **Transactional outbox poller**: App thread polls outbox, publishes, marks as published
3. **PostgreSQL LISTEN/NOTIFY**: Trigger fires NOTIFY on outbox insert, listener publishes

## Protocol Selection Guide

| Protocol | Payload Size | Latency (P50) | Throughput | Streaming | Browser Support | Tooling |
|----------|-------------|---------------|------------|-----------|-----------------|---------|
| REST/JSON | Large | ~10-50ms | Moderate | No | Native | Excellent |
| gRPC/protobuf | Small (3-10x less) | ~2-10ms | High | Yes | gRPC-Web | Good |
| GraphQL/JSON | Very large (overfetch risk) | ~20-100ms | Moderate | Subscriptions | Native | Good |
| WebSocket | Variable | ~1-5ms (persistent) | High | Bidirectional | Native | Moderate |
| SSE | Variable | ~10-50ms | Moderate | Server→Client | Native | Simple |
| Kafka | Variable | ~2-5ms | Very High | Event stream | No | Complex |
| RabbitMQ | Variable | ~1ms | Moderate | Event stream | No | Good |

## Connection Management

### Connection Pooling
- **Database**: min=2, max=(CPU cores × 2) + effective_spindle_count. PgBouncer transaction mode for serverless/microservices.
- **HTTP clients**: Pool per destination host. Max connections = expected peak concurrent × 1.5. Idle timeout = keepalive timeout of server.
- **Redis**: Single connection per process is often enough (Redis is single-threaded). Pool if pipelining.

### Timeouts (Universal Best Practices)
```
Connect timeout: 3-5 seconds (establishing TCP connection)
Read timeout:    P99 latency × 3 (waiting for response)
Write timeout:   P99 latency × 2 (sending request body)
Idle timeout:    30-60 seconds (close idle connections to save server resources)
```

### Circuit Breaker Thresholds
```
Failure rate threshold: > 50% in 60s rolling window → OPEN
Half-open probe: After 30s, try 1 request → 
  Success → CLOSED (normal)
  Failure → OPEN (wait another 30s)
Minimum requests before evaluation: 10 (don't trip on first failure)
```

## Resilience Patterns Quick Reference

| Pattern | What it does | When to use |
|---------|-------------|-------------|
| **Retry with backoff** | Retry failed call with increasing delays | Transient failures (network blip, brief DB restart) |
| **Circuit Breaker** | Stop calling when failure rate exceeds threshold | Protecting yourself from a degraded dependency |
| **Bulkhead** | Limit concurrent calls to a dependency | Preventing one slow dependency from consuming all threads |
| **Timeout** | Abort call after deadline | Every call! Prevents resource exhaustion |
| **Fallback** | Return degraded/cached response on failure | Non-critical features if dependency is down |
| **Rate Limiter** | Limit requests per time window | Protecting yourself from being overwhelmed |
| **Load Shedding** | Reject excess requests at the edge | Server is overloaded — preserve capacity for critical paths |

## References
- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/) — Gregor Hohpe & Bobby Woolf
- [gRPC Deadlines](https://grpc.io/docs/guides/deadlines/)
- [Saga Pattern](https://microservices.io/patterns/data/saga.html) — Chris Richardson
- [Outbox Pattern](https://microservices.io/patterns/data/transactional-outbox.html) — Chris Richardson
