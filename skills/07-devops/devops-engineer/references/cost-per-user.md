# Infrastructure Cost per User at Scale

| Users | Monthly Infra Cost | Cost Per User | Dominant Cost |
|-------|-------------------|---------------|---------------|
| 0-1K | $50-200 | $0.05-0.20 | Fixed-cost (always-on instances) |
| 1K-10K | $500-2K | $0.05-0.20 | Compute + managed DB |
| 10K-100K | $2K-10K | $0.02-0.10 | Bandwidth + DB + caching |
| 100K-1M | $10K-50K | $0.01-0.05 | Multi-region + observability + support |
| 1M+ | $50K-200K+ | $0.01-0.05 | Everything — optimize relentlessly |

**Target:** Infrastructure cost should be < 10% of revenue at all stages.
