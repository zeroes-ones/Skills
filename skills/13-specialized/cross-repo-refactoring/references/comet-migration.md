# Comet-Style Migration: The Three-Phase Framework

## The Metaphor

```
HEAD (New API) ← COMET (Consumers migrating) ← TAIL (Old API)
```

The comet represents consumers in transit from old to new. The framework ensures that at no point is a consumer left without a working API.

## Phase 1: Comet Creation (Deploy HEAD)

1. Add the new API alongside the old API in the same release
2. Mark old API as deprecated (compile-time annotation + runtime warning)
3. Instrument old API with a usage counter per consumer
4. Announce deprecation with timeline to all consumer teams
5. Gate: HEAD deployed and stable, TAIL counter reporting

## Phase 2: Comet Traversal (Migrate Consumers)

1. Prioritize consumers by call volume (highest first)
2. For each consumer: migrate, merge, deploy, verify TAIL counter = 0
3. Track progress: % consumers migrated, % call sites migrated
4. Gate: TAIL usage < 5% of baseline for 30 consecutive days
5. Escalation: unmaintained repos → engineering manager

## Phase 3: Comet Removal (Remove TAIL)

1. Confirm TAIL counter = 0 for 30 days
2. Remove old API code
3. Bump MAJOR version (semver: breaking change)
4. Deploy and monitor for 1 week
5. If errors: revert, investigate missed consumer, extend timeline

## Timeline Estimation

| Factor | Impact |
|--------|--------|
| Consumer count | +1 week per consumer for manual migration |
| Codemod coverage | -80% time if >90% automatable |
| Slowest deploy cycle | Minimum deprecation window = cycle × 3 |
| Unmaintained repos | +2-4 weeks per repo (context loading) |
| External consumers | +3-6 months (cannot force migration) |
