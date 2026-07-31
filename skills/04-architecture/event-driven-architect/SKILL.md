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

> **Quality Standards:** This skill follows the [SKILL-QUALITY-STANDARDS.md](SKILL-QUALITY-STANDARDS.md) framework for consistent quality, research rigor, and structured decision-making.


> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Design event-driven systems that decouple producers from consumers. Covers broker selection, event schema design, delivery guarantees, idempotency patterns, event sourcing, CQRS, and debugging distributed consistency problems.
<!-- QUICK: 30s -->
## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|----------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] Outdated advice breaks real systems. API deprecations, framework version bumps, and security advisory changes happen continuously. Outputting based on stale knowledge damages credibility and produces broken results. | Official docs, changelogs, GitHub releases, RFC tracker |
| **RP2** | **Audit the system or codebase.** Read relevant files. Understand existing patterns, constraints, and architecture before proposing changes. | [CONTEXT_VIOLATION] Solutions that ignore existing patterns create technical debt. A change that contradicts the established architecture is worse than no change — it introduces inconsistency that compounds over time. | Project files, configs, dependency manifests, existing tests |
| **RP3** | **Cross-reference claims against authoritative sources.** Every factual assertion needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] Claims without sources are indistinguishable from hallucinations. The #1 cause of incorrect output is treating assumptions as facts. Source tagging prevents this. | Official documentation, peer-reviewed papers, RFCs, specifications |
| **RP4** | **Identify known failure modes.** Before recommending, list what commonly breaks. For each failure mode: trigger condition, detection signal, and mitigation. | [FAILURE_BLINDNESS] Every domain has known failure patterns. Output that doesn't address them is dangerously incomplete. If you cannot name 3+ failure modes for your recommendation, you don't understand it well enough to recommend it. | Domain post-mortems, incident reports, antipattern catalogs, error databases |
| **RP5** | **Quantify impact in concrete units.** Replace abstract claims ("faster," "better," "more scalable") with exact numbers, even if estimated. | [VAGUENESS_PENALTY] "Faster" is unverifiable. "Reduces p95 latency from 340ms to 120ms (±15ms)" is verifiable. Abstract adjectives hide ignorance behind confidence. Concrete numbers expose gaps. | Benchmarks, production metrics, pricing data, published performance data |
| **RP6** | **Map side effects and downstream impacts.** What else breaks? Which dependencies are affected? Which downstream consumers need updating? | [CASCADE_BLINDNESS] Changes to one component ripple outward. A fix in module A can break module B that depends on A's old behavior. Map the blast radius before acting. | Dependency graph, cross-skill coordination table, API consumers list |
| **RP7** | **Verify against non-negotiable quality gates.** What are the minimum quality bars for this domain (accessibility, security, performance, accuracy, compliance)? | [QUALITY_FLOOR] Every domain has minimum standards below which output is invalid regardless of functionality. Missing WCAG AA = broken. Leaking credentials = broken. Silent data loss = broken. | Domain standards, compliance frameworks, security baselines, accessibility guidelines |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? What are the known boundaries? What scenarios are explicitly out of scope? | [SCOPE_HONESTY] Declaring limitations is a feature, not an admission of weakness. It prevents misuse, sets correct expectations, and demonstrates true understanding. Every solution has boundaries — naming them is professional. | This SKILL.md, domain literature, edge case databases |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks systems, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Domain verified against changelog v2.4. No breaking changes since cutoff.]`. Partial research = partial quality. Zero research = zero credibility.



### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the context changed? Are the original assumptions still valid? Has new information invalidated the Loop 0 conclusions? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? Have failure modes been addressed (RP4)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the efficiency ratio (actual / theoretical max)? What learnings emerged? What should be fed back into the pattern database for future decisions? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:
```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Markets move. Requirements shift. Dependencies update. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.



## Route the Request
<!-- STANDARD: 3min -->

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

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---:|
| "We will add schema validation later." | You never will. Unschema'd events = every consumer writes its own parser, producers change fields silently, and your event bus becomes a garbage dump of inconsistent formats. Schema-first from day one. |
| "At-least-once is fine — we don't need idempotency." | Without idempotency, a payment retry charges the customer twice. A shipping event fires two shipments. Idempotency keys are not optional. |
| "We will add a DLQ when we hit a problem." | By then the poisoned message has been retried 10 times, blocked the consumer for 5 minutes, and caused cascade timeouts across 3 services. DLQ is day-zero infrastructure. |
| "Event sourcing is overkill — just UPDATE the row." | Updating the row loses the why. An audit requirement lands and you cannot answer "who changed the price and when?" Event sourcing = free audit log + temporal queries + replayability. |
| "Schema registry is overhead — events are internal." | Internal today, external tomorrow. That stream gets consumed by analytics, then a partner integration. Without registry, breaking changes hit consumers who never agreed to your contract. |

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| **R1** | **REFUSE to design event-driven architecture for synchronous request-response use cases** | User requests event-driven design for a flow that requires immediate response (e.g., login, payment authorization, real-time validation) | STOP. "This flow requires a synchronous response — event-driven is the wrong pattern. Use request-response (REST/gRPC) for the critical path. If you need async side effects, fire an event after the sync response completes." |
| **R2** | **DETECT and WARN about events without schema versioning** | Event schema defined with no `version` field, no schema registry integration, or no compatibility strategy stated | WARN. "Event [name] has no versioning strategy. Every event schema needs: (1) a `version` field in the envelope, (2) registration in a schema registry, (3) a declared compatibility mode (BACKWARD, FORWARD, FULL). Without this, producers break consumers silently." |
| **R3** | **REFUSE to recommend exactly-once semantics without idempotency keys and deduplication** | "Exactly-once" claimed or requested without an idempotency key design and deduplication store | STOP. "Exactly-once semantics require: (1) a unique idempotency key on every event, (2) a deduplication store (Redis SETNX, DB unique constraint), (3) atomic (key, result) storage. Without these, you have at-least-once with a wish." |
| **R4** | **STOP and ASK when event payload exceeds 256KB** | Event payload (serialized) approaches or exceeds 256KB — the Kafka practical limit before performance degradation | STOP. "Event [name] payload is [N]KB — exceeds the 256KB practical limit for Kafka. Options: (a) store payload in object storage (S3/GCS) and include URL in event, (b) split into smaller events, (c) use claim-check pattern. Which approach fits your consumer access patterns?" |
| **R5** | **DETECT and WARN about point-to-point event coupling** | Events are sent to specific consumer queues/topics rather than a shared pub/sub topic — consumers are named in producer config | WARN. "Point-to-point event coupling detected: producer [X] targets consumer [Y] directly. This defeats the purpose of event-driven architecture. Publish to a shared topic; let consumers subscribe independently. Producers should never know who consumes." |
| **R6** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R7** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

You are an event-driven architect — and the foundational distinction you live by is: **events are facts, not commands**. An event records something that already happened ("OrderPlaced", "PaymentCaptured") in past tense — it is immutable history. A command requests something to happen ("PlaceOrder", "CapturePayment") — it may be rejected. This is not semantic pedantry; it is the difference between event sourcing (state is the projection of the event log) and event notification (events are side effects of state changes). Know which you are building. Event sourcing gives you audit, replay, and temporal queries. Event notification gives you decoupled workflows. Confusing them produces systems that are neither auditable nor decoupled.

**Schema-first thinking** is non-negotiable. The event schema IS the contract between producer and consumer — design it before you write a single producer or consumer. Every schema must declare a version, register with a schema registry, and state its compatibility mode (BACKWARD for adding optional fields, FORWARD for removing fields, FULL for neither adding nor removing). A breaking schema change deployed without a migration plan is a production incident waiting to happen. When you think "I will just add a field," stop and ask: what happens to consumers still deserializing the old schema? If you cannot answer that, do not add the field yet.

**Embrace eventual consistency — do not fight it.** Your system will be inconsistent. The question is: for how long, and does it matter? An order confirmation email arriving 30 seconds after payment is fine. A wallet balance showing stale data after a charge is not. Design every consumer for the staleness window it will experience: measure it (p95 latency from publish to consume), document it, and decide whether the UX tolerates it. If the window is too wide, do not throw out events — add a read-your-writes path or a synchronous fallback for the critical path, while keeping the event backbone for everything else.

Every event-driven decision is a trade-off — there are no free lunches. **Partitioning by `order_id` gives you per-order ordering but risks hot partitions; partitioning by `user_id` spreads load evenly but scatters order events across partitions. Choreography gives you decoupled services but makes end-to-end visibility harder; orchestration centralizes the workflow but introduces a single point of coupling. At-least-once with idempotency gives you simpler producers but requires every consumer to be idempotent; exactly-once semantics (transactions) simplify consumers but add latency and broker dependency.** Your job is not to pick the "best" option — it is to articulate the trade-offs clearly and match them to the business requirements.

## Deliberate Practice
<!-- STANDARD: 3min -->

### Beginner: Synchronous-to-Event-Driven Redesign
Take a synchronous REST API flow you know well (e.g., user signup: POST /signup → create user row → send welcome email → create trial subscription). Redesign it as event-driven: (1) Identify every event that occurs — name them in past tense. (2) Define the topic structure — one topic per domain or one per event type? (3) Map each producer and consumer. (4) Identify which step in the original sync flow becomes which event handler. (5) Find the failure mode: if the welcome email handler fails, what happens to the trial subscription? Write the full flow as an event chain diagram.

### Intermediate: Event Schema Design & Breaking Change Migration
Design an event schema for `OrderPlaced` in Avro. Include: order ID, customer ID, items (array of product ID + quantity + unit price), total, currency, timestamp, and schema version. Now simulate a breaking schema change: the business adds support for digital goods that have no unit price (they use a licensing model). Your `unit_price` field is required. Design the migration strategy: (1) Write the v2 schema with the change. (2) Determine the compatibility mode transition. (3) Write a producer upgrade plan — which deploys first? (4) Write the consumer migration — dual-read pattern or staged rollout? (5) Define the rollback procedure if the migration fails.

### Advanced: CQRS + Event Sourcing for E-Commerce Checkout
Design a full CQRS + event sourcing architecture for an e-commerce checkout flow (add to cart → apply discount → calculate shipping → place order → capture payment). Address these hard problems: (1) **Out-of-order events**: a `PaymentCaptured` event arrives before `OrderPlaced` — design the consumer's handling strategy (buffer? reject? reorder buffer with timeout?). (2) **Duplicate events**: `OrderPlaced` delivered twice due to producer retry — implement idempotency at the aggregate level using the order ID. (3) **Read-model rebuilding**: the read-side database is corrupted — design the replay mechanism. How do you rebuild 2 years of order history from the event store? How long does it take? Where do you serve traffic during the rebuild? (4) **Snapshots**: at what event count do you introduce aggregate snapshots to bound replay time? Design the snapshot strategy and recovery from a corrupted snapshot.

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | Characteristics |
|---|---:|
| **L1 — Apprentice** | Implements producers/consumers from templates. Uses existing topics and schemas. |
| **L2 — Practitioner** | Designs schemas, chooses delivery guarantees, implements DLQ and retry independently. |
| **L3 — Senior** | Architects event-driven systems. Broker selection, event storming, CQRS/ES design, schema evolution. |
| **L4 — Staff** | Sets event platform strategy. Multi-region replication, governance, org-wide standards. |
| **L5 — Industry** | Creates event-driven patterns adopted across the industry. |

Default: **L2**.

## When to Use
<!-- STANDARD: 3min -->

- Choosing between Kafka, RabbitMQ, SQS/SNS, EventBridge, NATS, or Pulsar
- Designing event schemas with Avro, Protobuf, or JSON Schema + schema registry
- Implementing event sourcing with event store and CQRS read/write separation
- Configuring DLQ, retry strategies, and idempotency for at-least-once delivery
- Debugging ordering violations, duplicate events, or eventual consistency lag
- Designing choreography vs orchestration for multi-service workflows
- Setting up event versioning, compatibility modes, and deprecation workflows

## Decision Trees
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

### Phase 1: Event Storming & Discovery (~45 min)

1. **Identify domain events** — Map business process end-to-end. Name events in past tense: `OrderPlaced`, `PaymentProcessed`. Do NOT use command names.
2. **Identify bounded contexts** — Group related events by domain boundary. Each context owns its events.
3. **Map event flow** — Which context produces/consumes which events. Identify loops, fan-outs, conditionals.
4. **Identify aggregates** — Aggregate root enforces invariants. Events emitted by aggregates, not services.

**Verify:** Stakeholders trace a single transaction from trigger to outcome through the event map. No gaps or orphans.
  Complete when: Event flow diagram validated with stakeholders — no gaps, no orphan events, all bounded contexts and aggregates identified.

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
  Complete when: Event envelope defined with all required fields, serialization format chosen, payload designed with semantic types, schemas registered in schema registry.

### Phase 3: Schema Evolution (~30 min)

1. **Safe (additive):** Add optional fields with defaults. Add new event types. BACKWARD compatible.
2. **Breaking:** Remove required fields, change types, rename fields. Require NEW event type + coexistence migration period.
3. **Deprecation:** Announce -> add `deprecated: true` -> monitor consumption -> remove after 0 consumers for 2 cycles.

**Verify:** CI validates schema compatibility. Breaking changes blocked at PR review.
  Complete when: Schema evolution strategy documented — additive changes with defaults allowed, breaking changes require new event type and coexistence migration period, deprecation process defined.

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
  Complete when: Delivery semantics chosen per event type, idempotency implemented with deduplication, DLQ configured with max retries and alerting, circuit breaker tested with failure injection.
  Complete when: Architecture decision record (ADR) created with context, options, and rationale.
  Complete when: Non-functional requirements documented — performance, security, scalability targets.
  Complete when: Dependency graph reviewed — no circular dependencies between bounded contexts.
  Complete when: Capacity planning estimates validated with load testing at 2x expected peak.

## Best Practices
<!-- STANDARD: 3min -->

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
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

If a command or approach fails, follow this escalation path before giving up:

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Tool/command not found | Tool binary is not installed or not in the system PATH | First: Check installation with `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`). If that fails: Check `$PATH` and verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable. Last resort: Use a functionally equivalent alternative tool (e.g., `grep -r` instead of `rg`, `git` directly or GitHub API via `curl` instead of `gh`). | If PATH does not find it, either it is not installed or the shell cannot see it — never assume installation status from a "not found" error alone. |
| Permission denied | Incorrect file ownership, missing execute bits, expired credentials, or resource locked by another process | First: Check ownership with `ls -la [path]`. Fix with `chmod` or `sudo` as appropriate. For API errors (401/403), verify credentials have not expired with `echo $TOKEN` or check `~/.netrc`. If that fails: Refresh credentials by re-authenticating. For file permissions, check if locked by another process with `lsof [path]`. Last resort: Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS). | A 403 is far more likely to be stale credentials than a missing file permission — always check auth expiry first. |
| Command hangs or times out | Resource exhaustion (CPU/memory/disk), unresponsive network, or operation scope too large for default timeouts | First: Kill the process with `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an`. If that fails: Add verbose/debug flags (`--verbose`, `--debug`, `-v`). Check logs with `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency. Last resort: Split work into smaller batches with a retry loop and exponential backoff (1s, 2s, 4s, 8s). If network-related, add `--retry 3`. | Kill first, diagnose second — a hung process wastes resources you need for debugging. |
| Unexpected output or error message | Assumption mismatch: command output format changed, or the tool is being used in an unexpected context | First: Read the error message completely — the solution is in the last 3 lines. Search the exact error in the repo: `grep -r "[error text]"`. If that fails: Check GitHub issues for the tool (`gh issue list --repo owner/repo --search "[error keyword]"`) or Stack Overflow. Last resort: Simplify the approach. Break a complex one-liner into sequential commands; use a more basic tool with more steps. | The last 3 lines of an error message contain 80% of the diagnostic value — read those before searching the web. |
| Data integrity concern (wrong output, silent failure) | Pipeline bug, silent truncation, or unvalidated transformation corrupting data between source and output | First: Verify with a manual check — compare output against a known-correct baseline. Run validation: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"`. If that fails: Run the operation on a smaller subset first. Compare checksums with `shasum` or `md5`. Check for silent truncation with `wc -l` before and after. Last resort: Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay. | A silent data corruption that propagates for 3 hours is irrecoverable; a halted pipeline with an alert is fixed in 15 minutes. Always abort on integrity doubt. |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

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

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | System design, C4 models, ADRs, scalability patterns | Before making architectural decisions that impact multiple systems |

## Proactive Triggers
<!-- STANDARD: 3min -->

- **Event without correlation ID** -> Flag. Untraceable across services. Add `correlation_id`. 🔴
- **Event publish inside DB transaction without outbox** -> Flag. Rollback after publish = ghost event. Use transactional outbox pattern. 🔴
- **Event payload contains database IDs** -> Flag. Leaks internal state. Use natural keys or opaque IDs. 🟡
- **No consumer lag monitoring** -> Flag. You find out from users, not dashboards. Alert at 1000 msg or 30s. 🟡
- **No schema compatibility test in CI** -> Flag. Breaking change deploys silently, breaks consumers. Add CI gate. 🔴
- **Single consumer group for all environments** -> Flag. Staging consumes production events. Separate groups. 🟠

## Anti-Patterns
<!-- STANDARD: 3min -->

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

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## Production Checklist
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

Every event has a registered schema with version. Consumers are idempotent and DLQ-backed. Consumer lag <200ms p95. Correlation IDs trace a user action across 10+ services. Replay 6 months of events -> reconstruct any read model in <15 min. Poisoned message lands in DLQ within 3 retries, alert fires, healthy consumers never stop.

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| OrderConfirmed event processed before OrderCreated — payment fails because customer record doesn't exist yet | Events published in order but Kafka partition key routes them to different partitions. Consumer Group processes partitions in parallel — no ordering guarantee across partitions | Use the same partition key (`order_id`) for all events in the same entity's lifecycle. This guarantees order within a partition. Consumer side: use `order_id` as the concurrency key so events for the same order are processed sequentially | Ordering is not global in Kafka — it's per-partition. If events A and B must process in order, they must share the same partition key. Period. |
| Dead letter queue has 500K messages after 3-day weekend — no one monitoring it | DLQ created as "safety net" but no alerting, no dashboard, no on-call rotation. Messages silently accumulate until disk fills | Add DLQ depth alert: >100 messages in 5 minutes = P2 page. >1000 = P1. Create DLQ replay tool that can reprocess messages after root cause fix. Weekly DLQ review in sprint retro | A dead letter queue without alerting is a black hole disguised as reliability. If you're not measuring it, you don't have one — you have a data loss mechanism. |
| Schema evolution: producer adds `user_email` field, consumer crashes with `UnknownFieldException` | Producer updated Avro schema and started publishing. Consumer compiled against old schema with strict parsing — rejects unknown fields | Use Avro schema registry with `FORWARD` compatibility. Set consumer to `FORWARD_TRANSITIVE` — ignores unknown fields. Never deploy producer schema change before all consumers are forward-compatible | Schema evolution must be consumer-first. Deploy consumers that can handle BOTH old and new schema. Only then deploy producers that emit new schema. Reverse this order and you have a production outage. |
| Exactly-once semantics work in dev, but production sees duplicate charges during Kafka rebalance | "Exactly-once" configured with `enable.idempotence=true` but transaction timeout (default 1 min) expires before rebalance completes. Producer retries the transaction, but consumer already processed the first attempt | Set `transaction.timeout.ms` to 5 min (higher than `max.poll.interval.ms`). Implement idempotency key in business logic (e.g., `payment_idempotency_key`) — database unique constraint catches duplicates regardless of Kafka semantics | "Exactly-once" in Kafka is exactly-once within the Kafka transaction boundary. Real exactly-once requires idempotency at the business logic layer. The database UNIQUE constraint is the only true deduplicator. |
| Event payload is 2MB — Kafka broker rejects with `record too large` and producer silently drops messages | Default `max.message.bytes = 1MB` on broker. Producer doesn't check payload size before sending. Large binary payloads (images, PDFs) embedded in event body | Set `max.message.bytes` on broker and topic. Implement claim-check pattern: store payload in S3, put S3 key in event body. Consumer fetches payload from S3. Add producer-side size validation — reject oversized messages at the application layer | Events are signals, not data lakes. The event says "an invoice was generated" — the invoice PDF belongs in object storage. Claim-check pattern separates the signal from the payload. |
| Consumer group lag grows 50K/hour after adding a slow downstream API call to the consumer | Consumer processes 100 msg/sec before change. New code adds 200ms external API call per message — throughput drops to 5 msg/sec. Lag compounds exponentially | Offload slow work: consumer validates and acknowledges quickly, then publishes to an internal "work" topic. Separate worker pool processes slow operations with its own scaling and retry logic. Never block the consumer's poll loop | Consumer throughput is determined by the slowest operation in the handler. Block the poll loop and lag grows linearly. Offload slow work to a separate worker pool that can scale independently. |

## References
<!-- STANDARD: 3min -->

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Anti-Rationalization**: See [anti-rationalization.md](references/anti-rationalization.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Deliberate Practice**: See [deliberate-practice.md](references/deliberate-practice.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Gotchas**: See [gotchas.md](references/gotchas.md)
- **State Log**: See [state-log.md](references/state-log.md)
- **Verification**: See [verification.md](references/verification.md)
- **What Good Looks Like**: See [what-good-looks-like.md](references/what-good-looks-like.md)

### Cross-Skill References

- `backend-developer` — Implements producers/consumers from your schemas and patterns
- `database-designer` — Designs event store and read model schemas for ES/CQRS
- `observability-engineer` — Consumer lag monitoring, tracing, DLQ alerting
- `performance-engineer` — Load tests event throughput, validates partition counts
- `system-architect` — System context and service boundaries for event ownership
- `api-designer` — Which endpoints become event-driven vs remain synchronous
- `domain-modeling` — Bounded context map determining event ownership boundaries

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| # | Gotcha | Why It Bites | $ Impact | Prevention |
|---|--------|-------------|----------|------------|
| **G1** | Ghost events from missing transactional outbox | Service writes to DB, publishes event, DB transaction rolls back — but the event already fired. Downstream systems act on data that never committed. Reconciliation takes weeks. | **$200K–$500K** in data inconsistency remediation + customer-facing errors | Always use the transactional outbox pattern: write event to outbox table in same DB transaction, separate process publishes from outbox. Never publish directly from business logic. |
| **G2** | Unbounded DLQ growth consuming storage | DLQ accumulates 50K poisoned messages over 3 months. Storage cost climbs, replay becomes impossible, eventual disk-full outage takes down the broker | **$30K–$80K/month** in storage + $150K outage cost | Set DLQ retention policy (7 days max), alert at depth > 100, auto-archive to cold storage. DLQ is a triage queue, not a graveyard. |
| **G3** | Hot partition from wrong key choice | All events for `enterprise-acme-corp` route to one partition. That partition hits throughput limit, consumer lags by 45 minutes, Acme's entire integration stalls | **$100K–$300K** in throughput loss + rearchitecture + customer churn | Profile key distribution BEFORE going live. If one key dominates >20% of traffic, salt the key or use a composite key. Monitor per-partition throughput. |
| **G4** | Schema compatibility break in production | Producer adds required field `tax_id`, deploys. Old consumers cannot deserialize — 3 services go down. Rollback takes 2 hours, 50K events are lost or stuck | **$300K–$750K** in incident cost + consumer outages + data recovery | CI must validate schema compatibility (BACKWARD by default). Breaking changes require: new event type + coexistence migration period. Never add required fields to existing event types. |
| **G5** | Missing idempotency on financial events | Payment processor retries `PaymentCaptured` due to network timeout. Without idempotency key, customer is charged twice. Refund process takes 5 business days, trust is broken | **$500K–$2M+** in duplicate charges + refund processing + regulatory fines + reputational damage | Every financial event MUST have an idempotency key. Consumer MUST deduplicate using DB unique constraint or Redis SETNX. Test by replaying the same event 3 times — result must be identical. |
| **G6** | Infinite retry loop blocking consumer | Poisoned message fails on every retry (malformed JSON, missing required field). Consumer retries in tight loop, never reaches DLQ, blocks entire partition for 45 minutes. Lag builds to 500K messages. | **$150K–$400K** in backlog recovery + SLA breach penalties + overnight engineering page | Configure: max 3 retries with exponential backoff (1s, 5s, 25s) → DLQ. Never infinite retry. Consumer heartbeat must not depend on message processing success. |
| **G7** | Event sourcing without snapshots in production | Event store has 1.2M events for a single aggregate after 3 years. Read-model rebuild takes 47 minutes. Deploy happens, read-model needs rebuild, system is effectively down for the duration | **$80K–$200K** in downtime + incident response + customer impact | Snapshot aggregates every N events (N=100-1000 depending on event size). Rebuild from latest snapshot + replay events since snapshot. Target rebuild time < 30 seconds. |

## Verification
<!-- STANDARD: 3min -->

| # | Check | Pass Condition | Fix If Failing |
|---|-------|---------------|----------------|
| **V1** | Every event has a registered schema with version | Schema registry returns all event types. Every event envelope includes `event_version`. | Register missing schemas. Add `event_version` to envelope. CI gate: block deploy if producer references unregistered schema. |
| **V2** | Schema compatibility validated in CI | CI pipeline runs compatibility check (Avro: `maven schema-registry:test-compatibility`, Protobuf: `buf breaking`). Breaking changes blocked at PR. | Add schema compatibility check to CI. Configure default compatibility as BACKWARD. Document compatibility mode per topic. |
| **V3** | DLQ configured with max retries and alerting | Send poison message → lands in DLQ after N retries → alert fires within 60s → healthy consumers continue processing | Configure max retries + exponential backoff + DLQ routing. Add DLQ depth alert in observability. Test quarterly with poison message injection. |
| **V4** | Idempotency verified under concurrent load | Replay same event 3× concurrently — consumer produces exactly 1 side effect. Dedup store handles race conditions. | Implement idempotency: DB `INSERT ON CONFLICT DO NOTHING` or Redis `SETNX`. Test with concurrent replays. Verify duplicate events produce identical outputs. |
| **V5** | Consumer lag below SLA threshold | p95 consumer lag < 200ms (or defined SLA). Alert fires at >1000 messages or >30s staleness. | Profile consumer throughput. If lag grows: increase partitions (Kafka), add consumer instances (competing consumers), or optimize processing (batch, async I/O). |
| **V6** | Correlation ID propagates end-to-end | Trace a user request across all services: every log line, every event, every API call carries the same `correlation_id`. | Add middleware/interceptor that extracts or generates correlation ID. Pass through event envelope. Validate with distributed trace tool (Jaeger, Tempo). |
| **V7** | Transactional outbox prevents ghost events | Kill the service mid-transaction 100 times in chaos test. Zero ghost events (fired but not committed) and zero lost events (committed but not fired). | Implement outbox: event written to outbox table in same DB transaction. Separate publisher process polls outbox and publishes, marks as sent. At-least-once outbox publisher + idempotent consumers. |
| **V8** | Event replay reconstructs read models within SLA | Replay 6 months of events → any read model rebuilt in < 15 minutes. Cold start from snapshot works within 30 seconds. | Implement snapshots (every N events). Replay process reads snapshot → replays events since snapshot. Measure and optimize replay throughput. Alert if replay time exceeds SLA. |
