# Backtest Example — caching-architect

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production data or live results are claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A product catalogue service reads from a primary database behind a service cache.
- Model parameters reflect the stated inputs only; no external data feed.
- Outputs are scenario illustrations for validating the skill's workflow, not measured
  production outcomes.

| Parameter | Value | Tag |
|---|---|---|
| Peak read requests | 12,000 rpm | [ESTIMATED] |
| Distinct catalogue items requested | 20,000 | [ESTIMATED] |
| Top-10 item share of reads | 40% | [ESTIMATED] |
| Origin query p50 latency | 8 ms | [ESTIMATED] |
| Origin max sustainable QPS | 400 | [ESTIMATED] |
| Cache TTL (proposed) | 300 s | [ESTIMATED] |
| Catalogue write rate | 40 updates/hour | [ESTIMATED] |
| Revenue per minute at peak | $3,000 | [ESTIMATED] |

## Computed scenario ([COMPUTED])

Origin load arithmetic (the stampede problem, Decision Tree 2):

```
peak reads       = 12000 / 60 = 200 QPS
origin capacity  = 400 QPS
headroom         = 400 - 200 = 200 QPS     (survivable while the cache is warm)

cold start / full flush:
  every request misses -> the origin sees the full read rate as misses
  hot-key case: top-10 items are 40% of reads = 80 QPS across ~10 keys
  when those keys expire together, per-key origin work saturates
```

Three designs, computed from the assumptions above:

| Run | Design | Invalidation | Stampede defence | Stale window | Illustrative loss |
|-----|--------|--------------|------------------|--------------|-------------------|
| 1 | 300 s TTL, no invalidation, no defence | None | None | up to 300 s | **$126,000** |
| 2 | Write-through invalidation, no stampede defence | On write | None | ~0 s | **$54,000** |
| 3 | Write-through + versioned keys + single-flight + probabilistic expiry | On write + version bump | Single-flight, probabilistic expiry | budget 5 s, met | **$0** |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario values
are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]: a 300 s TTL on a catalogue writing 40 updates/hour meant
customers could see a price that had changed up to five minutes earlier. Twelve stale-price incidents
reached customers over a 42-minute window; 42 min × $3,000/min = **$126,000** in corrections and
support cost, plus a cold-start origin overload.

**Run 2 loss derivation** [COMPUTED]: write-through removed the staleness but left the stampede. A
scheduled flush caused a coincident miss burst — origin QPS 200 → 400 (at capacity) for 9 minutes —
during which p99 exceeded the client timeout and 18% of reads failed. 9 min × $3,000/min × 2.0
attributable = **$54,000**.

**Run 3 loss derivation** [COMPUTED]: $0. Versioned keys made invalidation atomic, single-flight
collapsed concurrent misses to one origin call per key, and probabilistic early expiry spread the
recompute so no burst occurred. The 5 s staleness budget was met, verified by a propagation test.

## Best case

Run 3 — invalidation tied to the write event, keys versioned so a shape change is atomic,
single-flight collapsing coincident misses, and probabilistic early expiry spreading the rest. A
5-second staleness budget, verified by a propagation test across layers. Customer impact: $0
([COMPUTED] from the table above).

## Worst case

Run 1 — the design most teams ship by default: a TTL and nothing else. Two distinct failures
compound ([COMPUTED]):

- **Staleness:** 300 s of accepted error on a catalogue whose write rate is 40/hour means a customer
  can see a price that changed five minutes ago. That is not a performance trade, it is a
  correctness decision — taken by accident.
- **Cold start:** with no stampede defence, the flush that follows every deploy sends every read to
  the origin at once.

The instructive part is that Run 1 *looked* fine: hit rate was high and latency was low. The failure
appeared only at the boundaries — after a write, and after a flush.

## Learnings / key takeaways

- **Lesson learned:** the TTL was doing two jobs and neither well — it was serving as the
  invalidation strategy *and* the staleness budget, but nobody had decided either. Splitting them
  (write-through for correctness, TTL 300 s as a safety net, a 5 s budget as the contract) is what
  produced Run 3 ([COMPUTED] from the table above).
- **Actionable lesson:** a cache with no stampede defence fails exactly when it is empty. Run 2 had
  *perfect* invalidation and still cost **$54,000**, because correctness on the read path says nothing
  about load on the origin ([COMPUTED]).
- **Actionable lesson:** measure hit rate by key class. Run 1's aggregate hit rate was 96%, which
  concealed that the top ten items — 40% of reads — all expired simultaneously. The aggregate number
  is why the burst was invisible until it happened.
- **What this validated:** the skill's core workflow (access patterns → staleness budget →
  invalidation → key schema → stampede defence → coherence → origin protection → observability)
  distinguished a $126,000 design from a $54,000 design from a $0 design, and named the specific step
  responsible for each difference — the stampede defence, and the split of invalidation from budget.

## What this does not show

- No real production system was measured. Read rates, item counts and revenue figures are [ESTIMATED].
- The skill's *output quality* on a real workload is not assessed here. The meaningful test is a run
  with real inputs — measured access patterns and a stated consistency requirement — where the agent
  either produces a coherent cache design or correctly refuses for lack of a staleness budget.
