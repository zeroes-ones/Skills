# 21-Concept Curriculum — System Design Interview Prep

> Deep reference for `system-design-interview-prep`. Maps all 21 concepts to their owning
> skill's explainer (authored original content — research-source: title-only) plus the drill
> angle for each. Load the owning skill's reference when you need the full explainer.

## How to use this map

1. Pick the concept cluster for your target (see Decision Trees in the SKILL.md).
2. Open the owning skill's reference for the full explainer (concept → why → trade-offs → interview framing → drills).
3. Drill the concept aloud (teach-back + one design micro-question) and log it with a rubric score.

## The 21 concepts

| # | Concept | Owning skill + reference file | Interview angle to drill |
|---|---------|-------------------------------|--------------------------|
| 1 | System Design 101 | `system-architect` → `references/system-design-101.md` | 8-step framework; scale estimation; trade-off axes |
| 2 | Microservices Patterns | `system-architect` → `references/microservices-patterns.md` | When to split; gateway; circuit breaker; outbox; strangler fig |
| 3 | How DNS Works | `networking-engineer` → `references/dns-deep-dive.md` | Lookup path; record types; TTL strategy for failover |
| 4 | How JWT Works | `secure-api-design` → `references/jwt-tokens.md` | Lifecycle; verification; alg-confusion; revocation; JWT vs sessions |
| 5 | How HTTPS Works | `networking-engineer` → `references/https-in-practice.md` | TLS handshake; certificates; forward secrecy; termination |
| 6 | API Design Best Practices | `api-designer` → `references/api-design-best-practices.md` | Resources; errors; pagination; status codes; REST vs gRPC |
| 7 | Redis Use Cases | `database-designer` → `references/redis-use-cases.md` | Cache/sessions/rate-limit/leaderboard/locks; stampede; eviction |
| 8 | Distributed Systems 101 | `system-architect` → `references/distributed-systems-101.md` | 8 fallacies; consistency models; CAP; partial failure |
| 9 | How Message Queues Work | `event-driven-architect` → `references/message-queues.md` | Delivery semantics; ordering; consumer lag; DLQ |
| 10 | How WebSockets Work | `event-driven-architect` → `references/websockets-realtime.md` | Handshake; scaling with registry + pub/sub; reconnect/resume |
| 11 | Frontend System Design | `frontend-developer` → `references/frontend-system-design.md` | Rendering strategy; state classification; performance budgets |
| 12 | Password Storage | `secure-api-design` → `references/password-storage.md` (+ deep: `cryptography/references/hashing-and-passwords.md`) | Salted memory-hard KDFs; why not encryption; breach framing |
| 13 | Modular Monolith | `system-architect` → `references/modular-monolith.md` (+ `when-monolith-wins.md`) | Bounded-context modules; enforced boundaries; extraction |
| 14 | Saga Design Pattern | `event-driven-architect` → `references/saga-pattern.md` | Choreography vs orchestration; compensations; idempotency |
| 15 | Microservices Lessons From Netflix | `system-architect` → `references/netflix-microservices-lessons.md` | Chaos; statelessness; regional isolation; observability |
| 16 | Consistent Hashing | `system-architect` → `references/consistent-hashing.md` | Ring placement; virtual nodes; remapping storms |
| 17 | Idempotent APIs | `api-designer` → `references/idempotency.md` | Idempotency keys; stored-response replay; effectively-once |
| 18 | How RPC Works | `api-designer` → `references/rpc-and-grpc.md` | Stubs; IDL; deadlines; HTTP/2; RPC vs REST |
| 19 | API Versioning | `api-designer` → `references/versioning-cost-analysis.md` (existing) | Strategies; costs; deprecation; additive changes |
| 20 | Bloom Filters | `database-designer` → `references/bloom-filters.md` | Probabilistic membership; false positives; cache-penetration gates |
| 21 | Service Discovery | `networking-engineer` → `references/dns-and-service-discovery.md` | Registration/resolution; DNS vs registry vs mesh |

## Practice-bank question → concept map

| Classic question | Concepts it exercises |
|---|---|
| URL shortener | system-design-101, API design, idempotency (collision), consistent hashing |
| Rate limiter | Redis, distributed-systems (consistency), bloom filters (optional) |
| Chat app | WebSockets, message queues, saga (not needed), distributed systems (ordering) |
| News feed | distributed-systems, microservices, consistent hashing, Redis (cache/fan-out) |
| Notification system | message queues, idempotency (delivery), WebSockets |
| Payment flow | idempotency, saga, JWT/HTTPS, API design, password storage (auth) |
| Distributed cache | consistent hashing, Redis, bloom filters, service discovery |
| Search autocomplete | bloom filters, Redis (sorted sets/trie), consistent hashing |
| Video streaming | distributed-systems (CDN), DNS, HTTPS, message queues |
| Design Uber | WebSockets, distributed-systems (geo), consistent hashing, message queues |
| Realtime collab editor | WebSockets, distributed-systems (CRDT/ordering), service discovery |

## Drill log template

| Date | Concept / question | Difficulty | Clarify /25 | Scale /10 | Design /40 | Trade-offs /15 | Failure /10 | One fix for next time |
|---|---|---|---|---|---|---|---|---|

## 4-week quick plan (interview in ~1 month)

- **Week 1:** framework fluency — concepts 1, 8, 6; easy bank questions (URL shortener, rate limiter).
- **Week 2:** data + transport — concepts 7, 20, 16, 3, 5, 10; medium bank (chat, notification).
- **Week 3:** architecture + APIs — concepts 2, 9, 14, 13, 17, 18, 19; medium bank (news feed, payment).
- **Week 4:** security + mocks — concepts 4, 12, 21 (+ 15, 11 for track); 2-3 timed mocks with rubric.
