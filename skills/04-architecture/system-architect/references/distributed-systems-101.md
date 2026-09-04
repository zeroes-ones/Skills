# Distributed Systems 101 — Fallacies, Consistency, and the Hard Parts

> Original explainer for interview prep and learning. [research-source: title-only]

## What it is

Distributed systems = multiple machines cooperating over a network to act like one system. The network is the defining constraint: it is slow, unreliable, and insecure — and no component can trust another's clock, memory, or fate. Every hard problem in the field flows from that one fact.

## The 8 fallacies (know these cold)

1. The network is reliable.
2. Latency is zero.
3. Bandwidth is infinite.
4. The network is secure.
5. Topology doesn't change.
6. There is one administrator.
7. Transport cost is zero.
8. The network is homogeneous.

Interview value: when a design "just works," name which fallacy it is quietly assuming.

## Core problems and the vocabulary to discuss them

| Problem | What it is | Canonical answers |
|---|---|---|
| **Partial failure** | A call may fail, hang, or return garbage — you can't tell which | Timeouts, retries with backoff + jitter, circuit breakers, idempotency |
| **Clock skew** | No shared "now"; NTP drift breaks ordering by timestamp | Lamport clocks, vector clocks, hybrid logical clocks, or "don't rely on time" |
| **Ordering** | Total order is expensive; causal order is the useful minimum | Sequence numbers per partition, causal consistency, single-writer per key |
| **Consensus** | Getting N nodes to agree despite failures | Paxos, Raft, Zab; note the leader election cost |
| **Exactly-once** | Is impossible in general (network) | At-least-once + idempotent consumers; dedupe keys |
| **Split brain** | Two leaders both accepting writes | Quorum sizes, fencing tokens, lease expiry |
| **Replication lag** | Read-your-writes may fail on followers | Read-from-leader for critical reads, version vectors |

## Consistency models (low to high, cost rising)

- **Eventual** — replicas converge given quiescence. Cheap; feeds, likes.
- **Causal** — causally related ops ordered. Good default for social.
- **Read-your-writes / session** — user sees own writes. UX-critical.
- **Linearizable (strong)** — every op appears atomic at one instant. Needed for money, locks, leader election. Costs latency and availability (CAP tension).

## CAP — the correct way to state it

Under a network partition you must choose **consistency** (all nodes see the same latest write) or **availability** (every request gets a response). It is *not* "pick 2 of 3 always" — when there's no partition you can have both. Real systems choose per-operation: payments → CP; profile views → AP.

## Common interview systems that exercise these ideas

- **Chat:** ordering (per-conversation sequence), delivery (at-least-once + dedupe), presence (heartbeats, no trust of "offline").
- **Distributed cache / leader election:** Raft-style consensus, fencing to prevent stale leaders writing.
- **Distributed counter / likes:** CRDT or sharded counters with eventual merge; read path tolerates staleness.
- **Multi-region active-active:** conflict resolution policy (LWW, per-field, CRDT) is the design crux.

## Anti-patterns

- ❌ Assuming a single "now" or single source of truth across regions without saying how writes reconcile.
- ❌ Claiming "exactly-once delivery" — say "at-least-once + idempotent consumer" instead.
- ❌ Ignoring retry storms: retries without jitter synchronized by client timeouts become cascading failure.
- ❌ Designing for strong consistency everywhere (costly) when the product only needs session or causal.

## Deliberate-practice drills

1. **Fallacy audit:** take any past design and mark which of the 8 fallacies it assumed; redesign the assumption away.
2. **Consistency matrix:** for chat, cart, payments, likes, feed — state the required model and the cheapest way to get it.
3. **Failure injection:** simulate a 2s network blip on every call in a design; trace timeout → retry → queue → dead-letter.
4. **CAP argument:** for 3 systems, state the partition behavior precisely ("during a partition we serve stale reads but never lose writes").
5. **Clock problem:** design a "last-write-wins by timestamp" feature and then break it with clock skew; fix with version vectors.

## References
- See also in this repo: system-design-101.md, consistent-hashing.md, microservices-patterns.md
- `event-driven-architect` SKILL.md for queues/eventing details
- `system-architect` SKILL.md for C4/ADR/capacity planning
