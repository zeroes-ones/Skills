# Best Practices

<!-- DEEP: 10+min -->

1. **Design the semantic layer for governance, not just convenience**: Every metric in the semantic layer should have exactly one definition, one owner, and one review date. MetricFlow/LookML files should be in version control with the same rigor as production code. Treat metric definition changes with the same review process as API contract changes — they affect every downstream consumer.

2. **Optimize queries at the aggregation layer, not the visualization layer**: Dashboard slowness usually traces to unoptimized SQL in the semantic layer, not the BI tool. Pre-aggregate large fact tables at the granularity stakeholders actually query (daily, not per-transaction). Use incremental materialization with unique keys. Profile every metric's query performance before exposing it in a dashboard.

3. **Design dashboards for scan time, not build time**: An executive should be able to understand the key takeaway from a dashboard in under 10 seconds. Put the most important metric top-left. Use sparklines for trends, not full time-series. Color-code: green for on-track, red for off-track, grey for "not applicable this period." Remove anything that doesn't answer a specific business question.

4. **Model data for self-serve success, not just analyst convenience**: Self-serve fails when users need to understand 17 joins to answer a simple question. Build wide, denormalized exploration tables with clear column names, descriptions, and relationships. Pre-join common paths. Document every column with a plain-English description and example value. If a business user can't understand the schema in 5 minutes, it's not self-serve ready.

5. **Standardize the stakeholder intake process with a brief, not a meeting**: Require every dashboard request to specify: the business question, the decision it informs, the audience, the refresh cadence needed, and how the stakeholder will know the dashboard is working. This brief becomes the acceptance criteria. Reject requests that say "I'll know it when I see it."

6. **Govern metric definitions with a decision log, not tribal knowledge**: When two teams disagree on how ARR or NRR is calculated, the tiebreaker must be a written decision with a rationale, not the loudest voice in the room. Maintain a metric decision log (what was decided, why, when, by whom). When the metric is inevitably questioned again, point to the log — don't re-litigate.

7. **Define data freshness SLAs per domain, not globally**: Clinical outcomes data may need <1 hour freshness. Board metrics may tolerate 24 hours. Exploratory sandboxes may tolerate 1 week. Each domain gets an SLA, and dashboards prominently display the last refresh timestamp. Stakeholders should never wonder "is this data from today or last quarter?"

8. **Design embedded analytics as a product, not a feature**: Customer-facing analytics need SSO, row-level security, rate limiting, white-labeling, export compliance, and SLA-backed availability. Plan for tenant isolation from day one — a slow query from one customer's dashboard should never degrade another customer's experience. Pre-compute tenant-specific aggregates. Monitor per-tenant performance and set usage quotas.
