# Redis Use Cases — What It's Actually For (and Not For)

> Original explainer for interview prep and learning. [research-source: title-only]

## What Redis is

Redis is an in-memory, single-threaded data store with a rich data-type vocabulary (strings, hashes, lists, sets, sorted sets, streams) and sub-millisecond operations. Because it holds data in RAM, it is fast but **not a durability-first database** — its job is serving hot data fast, not being the system of record.

## The canonical use cases (ranked by how often they actually appear)

| Use case | Why Redis | Data type | Watch out for |
|---|---|---|---|
| **Cache** | Sub-ms reads, TTL built in | Strings/hashes | Cache stampede, eviction policy, stale reads |
| **Session store** | Fast read/write, TTL expiry = logout | Strings/hash with TTL | Size, cluster consistency |
| **Rate limiting** | Atomic increment + expire | Counter with TTL | Sliding-window vs fixed-window accuracy |
| **Leaderboards / rankings** | Sorted sets (`ZADD`, `ZRANGE`) | Sorted set | Tie-breaking, size |
| **Distributed locks** | `SET key val NX PX` | String | Lock expiry vs long work (renewal/fencing) — see notes |
| **Message queue / pub-sub** | Lightweight fan-out | List/Stream/PubSub | At-least-once, consumer groups, durability |
| **Counters / analytics** | Atomic `INCR` | String | Hot-key contention on one counter |
| **Geospatial** | Nearby queries | Geo sets | Accuracy vs DB spatial index |
| **Rate-burst / circuit state / feature flags** | Fast shared state | String/hash | Consistency expectations across nodes |

## Interview-critical subtleties

- **It's in-memory.** Everything can be lost on restart unless persistence (RDB/AOF) is on — and even then, Redis is a *cache/accelerator of record*, not the record. If data loss is unacceptable, the source of truth lives elsewhere (DB) and Redis is the hot layer.
- **Single-threaded execution** — commands are atomic and fast, which is why `INCR` and `SET NX` are safe — but one slow command (large `KEYS`, huge `SORT`) blocks everything. Never run `KEYS *` in production.
- **Cache stampede / thundering herd:** a hot key expires and 1,000 requests all miss to the DB. Fixes: **request coalescing/locking** (one process refreshes, others wait), **early recompute** (refresh before TTL ends), **jittered TTL**, or **stale-while-revalidate**.
- **Eviction policies:** `allkeys-lru` vs `volatile-ttl` vs `noeviction` — choose by whether you can tolerate evicting any key or only TTL'd ones.
- **Distributed locks are subtle:** a lock that expires while the holder is still working lets two holders run. Real fixes: **renewal** (Redisson watchdog) or **fencing tokens** (compare against a monotonically increasing value before the critical section). Know this in interviews — "SET NX PX" alone is not a robust lock.
- **Cluster / sharding:** Redis Cluster shards keys by hash slot; multi-key operations only work within a slot (use hash tags). Client-side caching (Redis 6) reduces network round trips.

## Choosing "is Redis right?" (interview filter)

1. Is the access pattern **hot** (high read rate, low tolerance for DB latency)? → cache layer yes.
2. Does the data need to **survive** a node restart with no loss? → keep source of truth elsewhere.
3. Do you need **atomic counters / sorted sets / TTL** semantics cheaply? → Redis is the natural fit.
4. Is it the *system of record*? → probably the wrong tool (use a real DB; Redis as accelerator).

## Interview answer skeleton

"Redis is an in-memory store with atomic, typed operations — I use it for caching, sessions, rate limiting, leaderboards, and lightweight pub-sub. The rules: it's an accelerator, not the system of record, so the source of truth lives in a durable DB; I design against stampedes with locking/early recompute; and if I use it for distributed locks I add renewal or fencing, because a plain SET NX PX lease can expire under a slow holder."

## Anti-patterns

- ❌ Treating Redis as the primary database (data loss on restart is "by design").
- ❌ `KEYS *` / unbounded scans in production (single-thread block).
- ❌ Naive `SET NX PX` distributed locks without renewal/fencing.
- ❌ No stampede protection on hot cache keys.
- ❌ Wrong eviction policy for the workload (evicting the only copy of a session).

## Deliberate-practice drills

1. **Design drill:** cache layer for a product catalog with per-item TTLs and stampede protection — draw the read path.
2. **Lock drill:** implement a distributed lock; then break it with a slow holder and fix with fencing tokens.
3. **Rate-limit drill:** fixed-window vs sliding-window limiter in Redis — write both, compare accuracy/cost.
4. **Leaderboard drill:** top-100 with ties using sorted sets — write `ZADD`/`ZRANGE`/`ZREVRANK` correctly.
5. **Interview drill:** "why is Redis fast?" — answer single-threaded + in-memory + event loop, and the one thing that makes it slow.

## References
- See also: bloom-filters.md, system-design-101.md (this repo)
- `database-designer` SKILL.md — cache strategies, denormalization
- `performance-engineer` SKILL.md — caching and latency budgets
