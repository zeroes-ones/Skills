# Cost-per-Done — Tracking Successful-Task Cost

## The Metric

```
$/done = total_cost(task_type) / successful_tasks(task_type)
```

Track $/done, not $/request. A cheap payload that fails and retries on the expensive path can be 12% MORE expensive per done while looking 40% cheaper per call.

## Why It Matters

The correctness cliff: the cheapest request is the one that produces the wrong answer, because it must be re-run with more context and more turns. Optimization that lowers $/request but raises the failure rate is a net loss.

## Measurement

- Log per request: task_type, cost (from usage fields), success (boolean), retry_chain.
- Roll up per task type: total cost / successful tasks.
- Report retry rate per endpoint; alert on rising retry rate (the retry tax).

## The Retry Tax

| Scenario | $/request | Success | $/done |
|----------|----------:|--------:|-------:|
| Baseline | $0.10 | 95% | $0.105 |
| "Optimized" | $0.06 | 82% | $0.073 |
| After retry tax (18% retry on expensive path) | $0.06 | 82% | **$0.087+** |

A cheap path with a low success rate and an expensive fallback erodes the win.

## Optimization Decision Rule

An optimization ships only if:
1. $/done improved (not just $/request), AND
2. retention/success metrics are flat or better.

If $/request fell but $/done is flat or worse → investigate the failure mode; do not ship.

## Reporting

Every optimization report includes: $/request before/after, $/done before/after, success rate, retention score. A report missing $/done is incomplete (Ground Rule R6).
