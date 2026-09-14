# Task Plan Template

The output schema for a decomposition produced by `implementation-planner`.

## Task record

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Stable short id (`T3`) |
| `title` | yes | One deliverable, stated as a state change |
| `deliverable` | yes | The single artifact or observable outcome |
| `acceptance` | yes | What "done" looks like, testable |
| `verify` | yes | Command or check that proves it |
| `blocked_by` | yes | List of task ids that must complete first (may be empty) |
| `wave` | yes | Integer scheduling wave (0 = startable now) |
| `collision_surface` | yes | Files, schema, or shared resources this task touches |
| `size` | yes | `one-sitting` or `needs-split` |
| `risk` | no | `low` / `medium` / `high` — high risk is front-loaded |

## Graph notation

```
T1 ──► T3 ──► T6
T2 ──► T4 ──┘
T5 ──────────┘
```

- Arrow = blocking edge (`blocked_by`).
- Wave 0 = every task with an empty `blocked_by`.
- Critical path = the longest chain through the DAG.

## Wave layout

```
Wave 0 (parallel):  T1, T2, T5     collision surface: none checked
Wave 1 (parallel):  T3, T4         collision surface: T3/T4 both touch src/config.ts → SERIALISE
Wave 2:             T6             critical path: T1 → T3 → T6
```

## Forgotten-work block

Every plan carries these four explicitly or marks them `N/A` with a reason:

- **Migration / backfill** — with reconciliation criteria
- **Rollout** — flag or staged enablement
- **Rollback** — how to reverse
- **Cleanup** — flag removal, dead-path deletion
