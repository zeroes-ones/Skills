# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **One source of truth for metrics** — Define in dbt semantic layer or metric registry. Never duplicate `revenue = SUM(amount)` across 5 dashboards.
- **Stage → Intermediate → Mart** — Never expose raw source tables to end users. Stage for cleanliness, intermediate for business logic, marts for consumption.
- **Test data, not code** — dbt `unique`, `not_null`, `relationships` tests on every model. Custom tests for business rules (`revenue >= 0`).
- **Pre-aggregate for dashboards** — A dashboard that queries 500M rows on every load is broken. Use incremental models, materialized tables, or BI cache.
- **Pre-register experiments** — Document hypothesis, metrics, and sample size before launching. Never cherry-pick significant results from 50 metrics.
- **Segment by default** — Every dashboard should allow filtering by platform, region, plan tier, and user cohort.
- **Document metric definitions** — "Is 'active user' someone who opened the app or made a purchase?" Put the answer in the dashboard description.
