# Routing Economics

A routing miss is the largest single line in a session budget, and it looks like a quality bug instead.

## Why a miss costs double

```
correct route : load right skill  → do the work        (1× )
routing miss  : load wrong skill  → do the work anyway (2×+)
```

The wrong skill consumes budget, and the work is then redone — often with a second skill loaded. The cost is the wrong load plus the redo, and it is paid in the same session.

## Measuring precision

- Build a held-out set of task descriptions with the correct skill labelled.
- Measure **rank-1** (did the right one load first), not just top-N.
- Track must-not violations: a skill loading on a prompt it explicitly disclaims.
- Re-measure whenever the corpus or the listing changes.

## Levers

| Lever | Effect |
|---|---|
| Negative routing from `Do NOT use` clauses | Prevents adjacent-skill false positives |
| Shorter, discriminative descriptions | Reduces collisions between siblings |
| Distinct trigger vocabulary per skill | Raises rank-1 |
| Embedding/rerank | Needed once lexical matching plateaus |

## Failure modes

- **Routing treated as quality only.** The cost is invisible until attributed.
- **Rank-1 unmeasured.** Top-N hides the miss rate that matters.
- **Unbounded cost variance.** Wildly varying session cost is usually varying routing.
- **Listing growth ignored.** Each added skill makes every routing decision harder.
- **Lexical matching pushed past its ceiling.** At scale it plateaus; the plateau looks like inconsistency.
- **Must-not violations tolerated.** They are the same error as a miss, with more confidence.
