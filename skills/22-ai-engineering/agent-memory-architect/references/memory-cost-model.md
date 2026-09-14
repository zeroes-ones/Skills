# Memory Cost Model

Memory is not free: it occupies window share on every turn it is injected.

## The cost

```
cost per session ≈ injected_memory_tokens × turns_injected × price_per_token
benefit          = avoided re-derivation + avoided repeat failures
```

Both sides must be estimated before memory is worth building.

## When memory pays

- The task class recurs across sessions.
- Re-derivation is expensive (research, exploration, long analysis).
- A prior failure would be repeated without the record.

## When memory does not pay

- One-off tasks. The read never happens.
- Cheap re-derivation. The store costs more than the redo.
- Memory that no query returns. Pure cost.

## Budgeting the share

Cap memory as a share of the window. The cap forces the ranking decision once, deliberately, instead of letting overflow decide which entries survive.

## Failure modes

- **Cost never compared to benefit.** The store is assumed to help.
- **Injection on every turn.** Memory injected unconditionally pays on every turn regardless of relevance.
- **Uncapped growth.** The share grows until the task is crowded out.
- **Measuring writes, not reads.** Writes are cheap to count and prove nothing.
- **Benefit assumed.** No with/without comparison means the value is unknown.
- **Ignoring the null result.** A store that changes nothing should be deleted, not kept "in case".
