# Optimization Methodology

### The Loop

```
Measure → Profile → Identify Bottleneck → Optimize → Verify → Repeat
```

1. **Measure**: Establish a baseline — what is the current latency/throughput/size?
2. **Profile**: Drill into _why_ — what function, query, or resource is the bottleneck?
3. **Identify bottleneck**: Pinpoint the single constraint limiting performance.
4. **Optimize**: Apply the targeted fix (not speculative optimization).
5. **Verify**: Run the same measurement again — did it improve? By how much? Did anything else degrade?
6. **Repeat**: The bottleneck usually moves to the next constraint.

### Amdahl's Law

`speedup = 1 / ((1 - P) + (P / S))` where P = proportion that can be improved, S = speedup factor.

If you can only optimize 50% of the execution time, the maximum speedup is 2x — even if you make that 50% infinitely fast. This means: **measure the proportion first**. Optimizing 80% of execution is worth 5x; optimizing 5% is never worth the effort.

### Pareto Principle (80/20 Rule)

80% of performance issues come from 20% of the code. Focus on the hot paths — the 20% that serves 80% of requests. Don't inline utility functions that run once per user session while pagination queries are doing sequential scans.

### Common Anti-Patterns

- **Premature optimization** (Knuth): "The real problem is that programmers have spent far too much time worrying about efficiency in the wrong places and at the wrong times."
- **Optimizing without measuring**: You don't know what's slow until you measure. Intuition is frequently wrong.
- **Optimizing the wrong thing**: Making a function 10x faster that runs 0.1% of the time saves nothing. Always optimize what matters to users — not what looks satisfying.
- **Vendor lock without profiling**: Adding Redis because "it's fast" when the bottleneck is a missing index on `users.email`. Layer in complexity only when needed.
- **Confusing micro-optimization with architecture**: Switch statement vs if-else doesn't matter when you're doing a sequential scan over 10M rows.
