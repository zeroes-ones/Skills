# Saga Design Pattern — Distributed Transactions Without 2PC

> Original explainer for interview prep and learning. [research-source: title-only]

## The problem it solves

A business operation (order → payment → inventory → shipping) spans multiple services, each owning its own database. You cannot use a single ACID transaction across them, and two-phase commit (2PC) is operationally fragile (coordinator = single point of failure, locks held during uncertainty). The saga pattern models the operation as a **sequence of local transactions**, each with a **compensating action** that undoes it if a later step fails.

## Two coordination styles (know both)

**Choreography** — each service publishes events; the next service reacts.
- `OrderService` creates order → emits `OrderCreated` → `PaymentService` charges → emits `PaymentCharged` → `InventoryService` reserves → …
- Failure: a step throws → it emits a failure event → previous services run their compensations.
- Pros: no central coordinator, loose coupling. Cons: flow is implicit across events; hard to see/reason about the whole saga; tricky to extend and debug.

**Orchestration** — a central `OrderSaga` coordinator tells each service what to do and calls compensations on failure.
- Coordinator: "charge payment" → "reserve inventory" → "confirm" → on any failure "refund payment" / "release inventory".
- Pros: flow visible in one place, easy to add steps, easy to test. Cons: coordinator can become a god-object / bottleneck.

**Recommendation:** orchestration for anything non-trivial — visible, testable, and easier to operate. Use choreography only for simple, fire-and-forget chains.

## Compensating actions (the real design work)

| Step | Action | Compensation |
|---|---|---|
| Charge payment | Debit card/account | Refund / reverse charge |
| Reserve inventory | Hold stock | Release reservation |
| Send email | Send | (None needed — or send a correction) |
| Book flight/hotel | Book | Cancel (may incur fees — model them) |

Rules:
1. Every step that can fail after a side effect needs a compensation.
2. Compensations must be **idempotent** (running twice = running once) and **reliable** (retried until success, or dead-lettered).
3. Not all steps are compensable at zero cost — cancellation fees, partial refunds. Model the cost; don't pretend it's free.
4. Sagas give **eventual consistency**: there is a window where the order is "partially done." Decide what the user sees in that window (e.g., "processing") and how reconciliation (a sweeper) fixes anything stuck.

## Failure & recovery mechanics

- Track saga state durably (DB table or outbox) so a crash mid-saga can resume — never keep saga state only in memory.
- Use an **outbox pattern** so the local transaction and its event are atomic (write event in same DB tx; a relay publishes it).
- Idempotency keys on every step so retries from timeouts/duplicates don't double-charge.
- Dead-letter + alert: if a compensation keeps failing, stop retrying silently — page a human.

## Interview answer skeleton

"A saga is a sequence of local transactions with compensating actions, because cross-service ACID (or 2PC) is fragile. I'd orchestrate it with a central coordinator that persists state and calls compensations in reverse on failure; each step is idempotent and events go out via the outbox so the local write and the event are atomic. The trade-off is eventual consistency — there's a window of partial completion, so I design the UX for it and run a reconciliation sweeper."

## Anti-patterns

- ❌ Reaching for 2PC "because we need transactions" — the coordinator is a SPOF and locks are costly; sagas are the distributed answer.
- ❌ Steps without compensations (or compensations that silently fail) — you get stuck orders and manual fixes.
- ❌ No saga state persistence — a crash mid-flow orphans the order.
- ❌ Choreography for a 5-step saga with no visibility — you can't answer "where is this order stuck?"

## Deliberate-practice drills

1. **Build a saga:** order → payment → inventory → shipping; write both choreographed and orchestrated versions.
2. **Failure drill:** inject a failure at each step; list the exact compensations run and their idempotency keys.
3. **Compensation drill:** design the refund/release for a system with non-refundable third-party fees (e.g., flight + hotel).
4. **Recovery drill:** the saga coordinator crashes after step 2 — design resume-from-durable-state.
5. **Interview drill:** answer "how do you keep an order flow consistent across 5 services?" with saga + outbox + idempotency.

## References
- See also: message-queues-and-events.md (this repo)
- `event-driven-architect` SKILL.md — outbox, event schema versioning, eventual consistency
- microservices-patterns.md (this repo) — where sagas sit in the pattern catalog
