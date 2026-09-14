# Slicing Patterns

## Vertical vs horizontal

| | Vertical (correct) | Horizontal (failure mode) |
|---|---|---|
| Slice 1 | UI → service → store, demoable end-to-end | All the models |
| Slice 2 | Add one capability to that path | All the services |
| Integration risk | Retired in slice 1 | Deferred to the final week |
| Demo | Every slice | The last day, maybe |

## The walking skeleton

A walking skeleton is the thinnest end-to-end path that runs. It is not a prototype and not throwaway: every later slice thickens it. If slice 1 does not cross every layer, the slicing is horizontal.

## Foundation tasks

A layer of "all the models first" is a smell. A single foundation task is legitimate when a named consumer requires it. The test:

- One task? Acceptable.
- A sequence of same-kind tasks with no demo between them? That is a layer — re-slice.

## Right-sizing

A task is right-sized when its outcome is demonstrable in one sitting. Signals it is too large:

- The description contains "and" joining two outcomes
- You cannot state the acceptance criteria in one sentence
- The verification step would need its own plan

## Slicing a migration

Order: dual-write or flag → backfill (with reconciliation) → cutover → observe → remove old path → delete flag. Each is its own task with its own verification.
