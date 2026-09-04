# System Design 101 — Core Concepts & Interview Framing

> Original explainer for interview prep and learning. [research-source: title-only]

## What it is

System design is the discipline of turning a fuzzy product requirement into a concrete architecture: components, data flow, storage, scale targets, and failure behavior — before writing code. In interviews it tests whether you can *reason about trade-offs under constraints*, not whether you can recite a stack.

## Why it matters

- Every production system eventually hits scale, reliability, or team boundaries — the architecture decides how gracefully.
- Interviewers use it to probe seniority: juniors name technologies; seniors name *decision criteria* and *failure modes*.
- A good design is boring and survivable: obvious components, explicit contracts, and known weak points.

## The interview framework (use this structure)

1. **Clarify requirements** — functional (what does it do?) and non-functional (DAU, latency, availability, consistency needs, read/write ratio, data size).
2. **Estimate scale** — QPS, storage, bandwidth, cache size. Round numbers; state assumptions out loud (e.g., "assume 10M DAU, 10% peak concurrency").
3. **Define the API** — the contract is the skeleton of the design.
4. **Design the data model** — entities, storage engine choice, indexes, partitioning.
5. **High-level architecture** — clients → edge/load balancer → services → data stores; draw the happy path.
6. **Drill into the interesting 20%** — the interviewer usually cares about one hard part (feed fan-out, chat ordering, idempotent payments). Go deep there.
7. **Address failure & scale** — redundancy, caching, queues, backpressure, monitoring.
8. **Summarize trade-offs** — what you chose, what you gave up, what you'd revisit.

## Core building blocks to know cold

| Block | What it solves | Watch out |
|---|---|---|
| Load balancer | Distribution, health checks | Sticky vs stateless; L4 vs L7 |
| Cache (CDN, Redis) | Read latency, hot data | Stale reads, cache stampede, eviction |
| Message queue | Decoupling, spikes, retries | Ordering, exactly-once illusions, backpressure |
| Database + index | Durable storage, query | Index write overhead, hot partitions |
| Replication / sharding | Availability / scale | Consistency lag, cross-shard queries |
| Object storage (S3-style) | Blobs, static assets | Not a database — no strong consistency guarantees in all modes |

## Key trade-offs table (memorize the axes, not the answers)

| Axis | Options | Typical driver |
|---|---|---|
| Consistency | Strong → eventual | Financial vs feed/social |
| Availability | 9s targets | Business cost of downtime |
| Read vs write optimized | Cache/denormalize vs normalize | Read:write ratio |
| Sync vs async | Request/response vs queue/event | Latency vs decoupling |
| Monolith vs microservices | Single deployable vs many | Team size, change isolation |

## Interview anti-patterns

- ❌ Jumping to a technology ("we'll use Kafka") before requirements/estimates.
- ❌ Designing a Google-scale system for a 10K-user app — match ambition to the stated scale.
- ❌ Ignoring failure: a design with no redundancy, retry, or degradation story is incomplete.
- ❌ Memorizing one architecture (e.g., the classic "pastebin/URL shortener") and forcing every question into it.

## Deliberate-practice drills

1. **Whiteboard 3 systems from memory** — URL shortener, chat app, news feed — using the 8-step framework in under 30 minutes each.
2. **Scale drill:** for each, compute QPS/storage/cache size and justify every assumption with a sanity check.
3. **Trade-off drill:** for each design, state 3 things you deliberately gave up and when you'd reverse the choice.
4. **Failure drill:** pick one component per design and describe degradation if it dies at peak.
5. **Interview role-play:** answer "what happens if this service is down?" for every service you drew.

## References
- Full architecture guidance, C4, ADRs: `system-architect` SKILL.md + its `references/`
- Related concepts in this repo: distributed-systems-101.md, consistent-hashing.md, microservices-patterns.md
- When a monolith is the right answer: when-monolith-wins.md
