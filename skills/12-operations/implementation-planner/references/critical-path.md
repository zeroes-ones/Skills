# Critical Path

The critical path is the longest chain of dependent tasks. It is the schedule. Everything else is
optimisation.

## Computing it

1. Build the DAG with durations (or your size unit).
2. For each task, earliest finish = max(earliest finish of all predecessors) + own duration.
3. The critical path is the chain ending at the largest earliest-finish.

```
T1(2) ──► T3(5) ──► T6(3)      chain length 10  ← critical path
T2(1) ──► T4(2) ──┘
T5(4) ──────────────┘
```

## Why it matters

Adding people to off-path work cannot shorten delivery. In the example above, putting two engineers
on T5 does not move the finish date; T6 still waits on T3.

The corollary: **the only way to shorten a plan is to shorten the critical path** — by splitting a
critical task, parallelising it, or removing a dependency from it.

## Reading the result

- **Slack** = how long a task can slip without moving the finish. On-path tasks have zero slack.
- A plan where almost everything is on the path is a plan with no parallelism — re-check the slicing.
- A plan where nothing is on the path usually means dependencies were not declared.

## Failure modes of critical-path analysis

- **Path never computed.** The schedule is unknowable, and effort is misapplied to off-path work.
- **Durations treated as facts.** Hour estimates are guesses; the *ordering* is the durable output, not the numbers.
- **Path ignored during execution.** A critical task slips silently because nobody marked it as critical.
- **Splitting off-path work.** Classic misallocation — the finish date does not move.
