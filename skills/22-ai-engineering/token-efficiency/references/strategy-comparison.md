# Strategy Comparison — Cache vs Compress vs Route vs Distill

## The Four Strategies

| Strategy | What it does | Best when | Risk |
|----------|--------------|-----------|------|
| **Cache (stabilize)** | Freeze the prefix; repeated content billed at 1/10-1/25 | Content repeats across requests | Cache busting (byte drift) |
| **Compress** | Summarize/prune unique content | Content is unique per request | Information loss (retention) |
| **Route** | Send easy tasks to a cheaper model | Task difficulty varies widely | Wrong routing → quality drop + retries |
| **Distill** | Replace a large model with a fine-tuned smaller one | High-volume, stable task signature | Training + eval cost; drift over time |

## Selection Rule

1. **Cache if it repeats** — cheapest, lossless. If you can freeze the prefix, do that before anything else.
2. **Compress if it's unique** — only with a retention test >= 90%.
3. **Route if difficulty varies** — a confidence-threshold router with fallback to the expensive model.
4. **Distill only at scale** — a stable task, millions of calls, and a solid eval set. Distillation is a project, not a lever.

## ROI Comparison (worked, per 1M tokens)

| Strategy | Effective cost reduction | Setup cost | Time to value |
|----------|--------------------------|-----------|---------------|
| Cache | 90-96% on the cached portion | Low (freeze + flags) | Days |
| Compress | 50-80% on the compressed portion | Medium (retention suite) | Weeks |
| Route | 50-90% on routed traffic | Medium (router + evals) | Weeks |
| Distill | 80-95% on distilled traffic | High (training + evals) | Months |

## Combined Playbook

For a typical system: stabilize the prefix (cache), dedup/exclude (reduce), compress the unique tail (retention-gated), cap output, then route easy tasks down-tier. Distill only the single highest-volume stable task after the other levers are measured.

## Anti-Patterns

- **Distilling before caching** — paying a month of training to fix a cache misconfiguration.
- **Routing without a fallback** — cheap model errors silently cascade; always route with a confidence floor and expensive-model fallback.
- **Compressing cacheable content** — unique-tail compression applied to the repeated prefix (see budget-optimization.md).
