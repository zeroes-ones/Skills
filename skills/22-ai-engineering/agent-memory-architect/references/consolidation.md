# Consolidation, Supersession, Eviction

The manage half. All three run on a cadence; none happens by itself.

## Why not re-summarise

Summarising a summary drifts. Each pass distorts a little; after several, the store is confident about a history that did not happen. Consolidation must therefore **count**, not rewrite.

| Approach | Result |
|---|---|
| Re-summarise older entries into prose | Progressive drift; the store converges on plausible fiction |
| Count and index outcomes | Stable; tallies remain true as detail is dropped |

## The three operations

**Consolidate.** Keep the newest N raw. Fold older entries into one record carrying `entries_folded`, `outcome_tally`, and first/last timestamps. Detail is dropped; the answer to "has this worked before?" survives.

**Supersede.** When a newer entry contradicts an older one, keep both and mark the older superseded. The question "when did this change?" is often more valuable than the current value alone.

**Evict.** Drop entries that are unageable (no provenance), corrupted, or never returned by any query. Never-read entries are cost with no demonstrated return.

## Retention policy shape

```
raw window     : newest N entries (individually queryable)
consolidated   : older, counted, detail dropped
superseded     : retained, marked, excluded from default retrieval
evicted        : unageable, corrupt, or never read
```

## Failure modes

- **No consolidation.** Store grows; useful entries become unreachable.
- **Summary drift.** The store's history becomes fiction.
- **Overwrite instead of supersede.** Loses the change history.
- **No eviction.** Cost grows with no return; nothing is ever measured out.
- **Non-idempotent manage job.** Running consolidation twice corrupts the store.
- **Evicting on age alone.** An often-read old entry is more valuable than a never-read new one.
