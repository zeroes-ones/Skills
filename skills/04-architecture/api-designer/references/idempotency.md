# How Idempotent APIs Work — Retry Without Double-Processing

> Original explainer for interview prep and learning. [research-source: title-only]

## The problem

Networks fail, clients time out, and the safest reaction is to retry. But retrying a `POST /payments` or `POST /orders` can charge twice or create two orders. An **idempotent API** guarantees that retrying the same request produces the same result as the first attempt — so retries become safe.

## What idempotency actually means

A request is idempotent if executing it N times has the same effect as executing it once. By HTTP semantics: `GET`, `PUT`, `DELETE` are naturally idempotent (same result each time); `POST` is *not* — it creates. Making `POST` safe is the job of the **idempotency key**.

## The idempotency-key pattern (know this precisely)

1. **Client generates a key** — a UUID (or meaningful hash) that identifies the logical operation, sent as `Idempotency-Key: <key>`.
2. **Server checks** — on arrival, look up the key.
   - **New key** → process the operation, store the request + response keyed by the idempotency key, return the result.
   - **Existing key, same request** → return the **stored response** (the original result), do NOT re-process.
   - **Existing key, different request** → return `422`/`409` (key reuse with different payload is a client bug).
3. **Concurrency** — two simultaneous requests with the same key must not both process: the check-and-store must be atomic (unique constraint on the key, or a lock/conditional insert).

## Where to store idempotency state

| Storage | Works for | Notes |
|---|---|---|
| DB table with **unique key constraint** | Most backends | Atomic; store request hash + response; clean up after TTL |
| Redis SETNX with TTL | High-throughput, low-state | Fast; design for eviction → a lost key after TTL could double-process (choose TTL > max retry window) |
| Outbox / event log | Event-driven | The key doubles as dedupe in consumers |

**Critical rules:**
- The **response must be cached and replayed** — a retry after a timeout must return the original 200 with the created resource ID, not "already exists" errors the client can't interpret.
- Key **TTL > the longest retry window** (e.g., 24h if clients retry for hours).
- The stored **request hash** detects key reuse with a different payload.
- Idempotency applies per logical operation, not per endpoint — a key identifies "charge this order once", not "this endpoint".

## Why at-least-once + idempotency = effectively-once

Brokers and networks deliver **at-least-once**; duplicates are normal. If every consumer/endpoint is idempotent, duplicates become harmless — this is how you get "effectively-once" without distributed-transaction magic. The pattern is everywhere: payment gateways (Stripe's Idempotency-Key), message consumers (dedupe by message ID), webhook handlers.

## Common failure modes (and the fixes)

- **Client regenerates the key per retry** → the server sees a new operation each time. Fix: key is created once per logical operation and reused on every retry.
- **Server restarts and loses the table** → in-memory-only idempotency = double-processing after restart. Fix: durable store.
- **Key TTL too short** → a very slow retry re-processes. Fix: TTL > max retry window.
- **Replay of the wrong response** → store the exact original response body/status.
- **Concurrent first requests race** → both process without an atomic guard. Fix: unique constraint / conditional insert.

## Interview answer skeleton

"To make POST retry-safe, the client sends an Idempotency-Key that identifies the logical operation. The server stores the key with a request hash and the original response under a unique constraint: a repeat of the same key returns the stored response without re-processing, a different payload on the same key is a 422, and the store is durable with a TTL longer than the retry window. Combined with at-least-once delivery, that gives effectively-once behavior."

## Anti-patterns

- ❌ Relying on "the client won't retry" — networks retry for you.
- ❌ Returning a fresh error on a replayed key instead of the original response.
- ❌ In-memory idempotency state (lost on restart).
- ❌ One key per attempt instead of per logical operation.
- ❌ Idempotency only on payments — apply it to any retryable write (orders, emails, webhook side effects).

## Deliberate-practice drills

1. **Flow drill:** write the sequence for charge → timeout → retry with the same key; show the stored-response replay.
2. **Concurrency drill:** two same-key requests arrive simultaneously — design the atomic guard and prove only one processes.
3. **Storage drill:** compare DB-unique-key vs Redis SETNX for a payments API; state the failure mode of each.
4. **Consumer drill:** design dedupe for a webhook/queue consumer so exactly one side effect happens per event.
5. **Interview drill:** "your payment endpoint double-charged after a retry — what happened and how do you fix it?" — answer with the key pattern and the atomic guard.

## References
- See also: api-design-best-practices.md, message-queues.md (this repo)
- `api-designer` SKILL.md — error modeling, retry semantics
- `backend-developer` SKILL.md — implementing idempotency
