# Invalidation Catalogue — what actually refreshes a cached copy

> Every strategy below names which of the three questions it answers — *when* the copy is refreshed
> (Decision Tree 1), *what* a miss does (Tree 2), *which layer wins* (Tree 3). The cost column is why
> R1 refuses "TTL only": each row buys correctness with a different currency.

---

## The invalidation catalogue

| Strategy | Refreshes when | Cost | Fails when |
|----------|---------------|------|-----------|
| **Write-through** | The writer writes both store and cache | Write latency; the cache is on the write path | The write to cache fails but the store succeeds and is not retried → permanent divergence |
| **Write-behind** | The writer updates cache, store async later | Durability window; loss on crash | Treated as a cache when it is actually a buffered data store |
| **Explicit invalidate on write** | The writer deletes/updates the known key | Requires the writer to derive every key it affects | The writer cannot enumerate affected keys (range queries, secondary indexes) → silent stale entries |
| **Event-driven (CDC / pub-sub)** | A change event invalidates subscribers | Broker availability becomes a dependency; at-least-once delivery | The event is lost and nothing bounds the error duration → this is why the TTL safety net stays |
| **TTL only** | Nothing refreshes; the entry ages out | Bounded-but-real staleness; miss storm at expiry | Used as the *strategy* rather than the backstop (R1) — the single most common production cache bug |
| **Versioned key namespace** | A schema or shape change bumps the namespace version | Old keys become garbage until evicted | Bumped without a plan to reclaim memory, or *not* bumped on a shape change → stale records read forever |
| **Stale-while-revalidate** | Serves the old value, refreshes in background | Staleness is deliberate and bounded; a background fetch | The background refresh fails and the stale value keeps being served past the budget without alerting |
| **Cache-aside (lazy fill)** | The reader loads on miss and fills | Miss latency on the reader's path; no single owner | Every caller implements it → keys, TTLs, and invalidation drift per call site |
| **Refresh-ahead** | Predicts expiry and refreshes before it | Wasted work if access is not actually periodic | Access is not periodic; the prediction warms entries nobody reads |

**Reading the table.** The correct answer to "what is our invalidation strategy?" is almost never a
single row. The production-safe shape is *explicit or event-driven invalidation for correctness,
plus a TTL as a bound on the failure case when the event is lost* — that pairing is exactly what R1
demands be written down.
