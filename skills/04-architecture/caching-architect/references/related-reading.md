# Related Reading — where this skill plugs into the library

> The skills this one consumes from and feeds into, and what each relationship is for.

---

## Related reading in this library

- `performance-engineer` — the measured latency and origin load that size the benefit and validate
  the hit-rate target
- `system-architect` — service topology and read/write paths, which determine where a cache may sit
  and what coherence it needs
- `database-designer` — schema and write paths, which determine what invalidation the writer can emit
- `resilience-pattern-engineer` — origin-side shedding, breakers and degradation for the worst-case
  miss burst; a cache can mask a failing dependency, but the runtime defence belongs there
- `capacity-planning-engineer` — headroom policy and sizing, which the key cardinality feeds into
- `site-reliability-engineer` — the staleness-budget and hit-rate SLIs that alert on freshness
  violations
- `observability-engineer` — hit rate by key class, miss bursts, and defence-activation metrics
- `docs/missing-skills-research.md` §3 (G2, G3) — why caching and capacity are the leading
  capacity-exhaustion root causes in the incident literature
