# Microservices Lessons From Netflix — What Production Scale Actually Taught Us

> Original explainer for interview prep and learning. [research-source: title-only]

## Why Netflix is the canonical case study

Netflix runs hundreds of microservices on AWS serving tens of millions of devices, and it has *published* what went wrong and how it fixed it — which makes it the safest real-world example in interviews. The lessons are about **operational reality**, not architecture diagrams.

## Lesson 1 — Failure is the default state; design for it

Netflix's mantra: "assume everything fails" (see the 8 fallacies). They built **Chaos Monkey** (kill instances randomly in prod) and later **Chaos Kong** (kill an entire AWS region) to *prove* the system survives. The lesson: you cannot design reliability by hoping; you must **rehearse failure** until degradation is boring.

Interview takeaway: name chaos engineering and why it exists — "we test that our redundancy actually works by breaking it on purpose in production."

## Lesson 2 — Loose coupling and asynchronous communication

Services don't call each other in long synchronous chains for core flows; events and queues decouple producers from consumers. A failure in one service must not cascade. Netflix's architecture pushes **events** (via its own message infrastructure, formerly SQS-based) so each service can fail, retry, and recover independently.

## Lesson 3 — Stateless services, state pushed to the edges

Compute is kept **stateless** so any instance can serve any request (scale = add instances). State lives in purpose-built stores (Cassandra for availability, EV cache, S3 for blobs). Statelessness is what makes autoscaling and instance churn safe.

## Lesson 4 — Regional isolation and graceful degradation

Multiple AWS regions, each able to run independently. When one region degrades, traffic shifts and the UI **degrades gracefully** (fewer recommendations, no hard crash). Interview gold: "the product has a designed degraded mode" — every dependency has a fallback.

## Lesson 5 — Observability is a first-class system

Metrics, logs, and distributed tracing across hundreds of services with **correlation IDs**; without it you cannot debug a request that touched 15 services. Netflix runs its own tracing (and open-sourced much of the stack). You can't operate what you can't trace.

## Lesson 6 — Independent deployability is the point

Teams deploy their own services independently, dozens of times a day. This is the *organizational* payoff of microservices — and the reason Netflix could scale engineering orgs, not just traffic. If you don't get independent deploys, you have a distributed monolith with extra cost.

## Lesson 7 — Data ownership and polyglot persistence

Each service owns its data and picks the store that fits (Cassandra for availability at scale, but not for everything). No shared database. Persistence choice follows the access pattern.

## What NOT to copy (the honest part)

- Netflix's scale justifies complexity that a startup would drown in. Its *principles* (assume failure, stateless compute, degrade gracefully, observe everything) transfer; its *topology* (hundreds of services, chaos at region scale) does not.
- Chaos engineering in production requires mature observability and runbooks first — start with chaos in staging.

## Interview answer skeleton

"Netflix's published lessons: assume every component fails and rehearse failure (Chaos Monkey/Kong); keep services stateless and push state to purpose-built stores; decouple with events so failures don't cascade; isolate regions and degrade gracefully; make observability a first-class system with correlation IDs. The transferable principle is operational design, not the topology — a startup should keep the principles and stay modular-monolith until splitting pays."

## Deliberate-practice drills

1. **Apply to a small system:** which Netflix lessons apply to a 3-service startup app, and which are overkill?
2. **Degradation drill:** define the degraded mode for every dependency in a video-streaming-style design.
3. **Chaos drill:** write a chaos-test plan for a staging environment: what to kill, what to assert, how to roll back.
4. **Trace drill:** sketch the correlation-ID flow for a request crossing 5 services with async hops.
5. **Interview drill:** answer "you added a 6th service and pager load doubled — what do the Netflix lessons say?" (coupling + observability + deployability).

## References
- See also: microservices-patterns.md, distributed-systems-101.md (this repo)
- `system-architect` SKILL.md — ADRs, capacity, deployment model
- `observability-engineer` SKILL.md — tracing, SLOs, alerting
- `chaos-engineer` (13-specialized) — chaos methodology and runbooks
