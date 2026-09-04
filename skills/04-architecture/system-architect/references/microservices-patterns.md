# Microservices Patterns — When to Split, How to Keep It Safe

> Original explainer for interview prep and learning. [research-source: title-only]

## What it is

Microservices = many small, independently deployable services, each owning one business capability and its data. The *patterns* are the reusable answers to the recurring problems this creates: how to decompose, how services find and call each other, how failures stay contained, and how data stays consistent across service boundaries.

## When microservices actually pay (and when they don't)

Choose microservices when the *driver* is organizational or operational:
- **Team autonomy** — 2-pizza teams shipping independently (Conway's law: architecture mirrors org).
- **Independent scaling** — one capability has different load characteristics.
- **Change isolation** — a hot, fast-moving capability shouldn't require redeploying everything.
- **Polyglot / tech isolation** — a genuine need for a different runtime (rare; usually not the real reason).

Choose a **monolith first** when the team is small, the domain is cohesive, or the scaling driver is absent — see `when-monolith-wins.md` and the modular-monolith doc in this repo. Most teams should start modular-monolith and extract services as pain appears.

## The pattern catalog (know the name + the problem it solves)

| Pattern | Problem it solves | Notes |
|---|---|---|
| **Decompose by business capability / bounded context** | What goes in which service | DDD bounded contexts are the best seam |
| **API gateway / BFF** | Client talks to N services | Aggregation, auth, routing; avoid turning it into a monolith-in-disguise |
| **Service discovery** | How does A find B's address? | Client-side (registry) vs server-side (LB); see dns-and-service-discovery.md |
| **Config server / externalized config** | Config changes without redeploy | Versioned, auditable, secret-managed |
| **Circuit breaker** | Stop calling a failing service | Fail fast, trip/open/half-open states |
| **Retry with backoff + jitter** | Transient failures | Never retry storms on a dying service |
| **Bulkhead** | One slow consumer doesn't starve others | Per-dependency thread pools/connection pools |
| **Saga** | Distributed transaction without 2PC | Choreography vs orchestration — see saga-pattern.md |
| **Outbox pattern** | Atomic DB write + event publish | Write event to same DB tx; relay publishes |
| **Event-driven / async communication** | Decouple, absorb spikes | See event-driven-architect SKILL.md |
| **Strangler fig** | Incrementally replace a monolith | Route by URL/feature; migrate slice by slice |
| **Observability (logs/metrics/traces)** | You can't debug what you can't see | Correlation IDs across services |

## Data ownership rules (the part people get wrong)

1. **Each service owns its data.** No sharing a database table across services — shared DBs silently recreate the monolith's coupling.
2. **No direct DB access to another service's store.** All access through the owner's API/events.
3. **Cross-service consistency is eventual** via sagas/outbox, not distributed transactions.
4. **Read-model / CQRS** is the escape hatch when a service needs data owned elsewhere — subscribe to events, build a local projection.

## Failure containment — the interview must-have

- Assume every downstream can fail, hang, or return garbage.
- **Timeouts everywhere**, circuit breakers on hot paths, bulkheads per dependency.
- Define **fallback behavior** per dependency (cache, default, degrade).
- **Retry storms kill systems**: add jitter; use exponential backoff; cap retries.
- Test it: chaos — kill a service and watch the system degrade, not collapse.

## Anti-patterns

- ❌ **Distributed monolith:** many services + shared DB + synchronous call chains = a monolith that's harder to operate.
- ❌ Splitting by technical layer (one "UI service", one "DB service") instead of business capability.
- ❌ Choreographing sagas with no way to see the whole flow (orchestration + tracing needed).
- ❌ Introducing microservices for "scalability" with a 10-person team and no scaling pain.

## Deliberate-practice drills

1. **Decomposition drill:** take a monolith domain (e.g., e-commerce) and draw bounded contexts; justify each service boundary with a team/change driver.
2. **Failure drill:** for a 6-service order flow, trace what happens when each single service dies; name the containment pattern used.
3. **Saga drill:** design an order → payment → inventory saga in both choreographed and orchestrated forms; compare failure handling.
4. **Strangler drill:** plan a 3-phase migration of one monolith module with a rollback at each phase.
5. **Interview role-play:** "your checkout calls 5 services — how do you keep it fast and available?" Answer with gateway + async + circuit breakers + fallbacks.

## References
- See also: saga-pattern.md, dns-and-service-discovery.md (this repo)
- `system-architect` SKILL.md — microservices-vs-monolith decision, C4
- `event-driven-architect` SKILL.md — queues, outbox, event schema versioning
- Modular monolith as the pragmatic middle: modular-monolith.md
