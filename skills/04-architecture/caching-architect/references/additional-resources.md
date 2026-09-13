# Additional Resources — Caching Architect

> Deep knowledge loaded on demand. `SKILL.md` holds the decisions and rules (R1–R6, the three
> decision trees); the extended material lives here and in the sibling reference files.

## Reference file map

| File | Covers |
|---|---|
| [`invalidation-catalogue.md`](invalidation-catalogue.md) | Every refresh strategy — write-through, write-behind, explicit invalidate, event-driven, TTL-only, versioned keys, stale-while-revalidate, cache-aside, refresh-ahead — with its cost and the case it fails in |
| [`staleness-and-ttl.md`](staleness-and-ttl.md) | The TTL-to-acceptable-error arithmetic, and why a staleness budget must be owned rather than chosen by feel |
| [`stampede-defences.md`](stampede-defences.md) | The 33× miss-multiplier worked through, what a single-flight actually saves, the XFetch early-expiry formulation, and why the cold state sets the origin's sizing |
| [`key-schema-and-cardinality.md`](key-schema-and-cardinality.md) | The separator dimensions, cardinality as a capacity decision, keys as a security boundary, and the collision property test |
| [`coherence-models.md`](coherence-models.md) | The five inter-layer models (single-writer, TTL-ordered, event-propagated, version-stamped, read-through), and the precedence + propagation rule each requires |
| [`measurement.md`](measurement.md) | Hit rate by key class rather than in aggregate, the hot-key skew the aggregate hides, and the reversibility check for any TTL or size change |
| [`failure-narratives.md`](failure-narratives.md) | Five anonymised production failures — the TTL-as-strategy, the tenant-less key, the deploy-flush storm, the ping-ponging layers, and the sticky negative — each with the rule it justifies |
| [`verification-recipes.md`](verification-recipes.md) | The six checks from SKILL.md's Verification section as runnable procedures |
| [`sources.md`](sources.md) | Every claim traced to a source, tagged by strength, with the "explicitly not claimed" boundary |
| [`related-reading.md`](related-reading.md) | The skills this one consumes from and feeds into, and what each relationship is for |

## Extended example

`examples/backtest/README.md` runs a cache-design programme against a stated scenario, with the
arithmetic shown and every figure provenance-tagged.

## Source material

Eviction policies, invalidation APIs and TTL rounding differ per cache product and version. Confirm
the installed version's behaviour before citing it as fact — see `sources.md`.

## Verification harness

`scripts/verify-skill.sh` asserts this skill's own invariants: that all six ground rules are present,
that TTL is treated as a backstop rather than an invalidation strategy, that a key schema separates
on every dimension the value depends on, that a stampede defence is paired with an origin-shed
threshold, that a staleness budget is declared and owned, that layered caches declare both precedence
and propagation, and that every tuning change is judged on measured origin load. Run it before
relying on the skill's output.
