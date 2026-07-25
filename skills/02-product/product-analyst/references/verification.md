## Verification

| # | Check | Pass Condition | Fix If Failing |
|---|-------|---------------|----------------|
| **V1** | North Star decomposes to input metrics | Every team can name the input metric they own and how it connects to North Star | Run a metric-mapping workshop: North Star → input metrics → team ownership. Any orphan metric is either miscategorized or irrelevant. |
| **V2** | Every experiment has pre-registered sample size | Sample size calculation (baseline, MDE, alpha, power) documented BEFORE test launch in experiment tracker | Block experiment launch until sample size is calculated and documented. Use a launch checklist template. |
| **V3** | Retention measured by cohort, not aggregate | Cohort table shows 3+ sequential weekly cohorts with confidence bands | If only aggregate retention exists, build the cohort query. It needs: user acquisition timestamp, retention event timestamp, cohort size. |
| **V4** | Funnel identifies highest-impact bottleneck | Bottleneck = step with max(drop_size × reachable_users × fixability_score) | If funnel shows drops but no bottleneck analysis, rank steps by: absolute drop size, then apply qualitative fixability scoring. |
| **V5** | Counter-metrics exist for every KPI | For every input metric, a counter-metric is defined and monitored on the same dashboard | Audit each KPI: "If we optimize this to 2x, what breaks?" Define that as the counter-metric. No KPI ships without its counter. |
| **V6** | Tracking plan validates in CI | Event payload schema checked against taxonomy on every PR. Schema drift alert fires if production events deviate. | Add JSON Schema validation of event payloads to CI pipeline. Set up production event sampling that compares payloads to taxonomy. |
| **V7** | Dashboard tiles trace to decisions | Every tile on every dashboard completes: "When [metric] crosses [threshold], we [action]." | Review dashboards quarterly. Remove tiles that fail this test. Redesign dashboard with decision-first layout. |
| **V8** | Segmentation uses behavior, not just demographics | At minimum: power users, core users, casual users, at-risk users are defined with event-based criteria | Define segments by usage frequency + recency in the last 28 days. Power: top 10% frequency. Core: 50-90th percentile. Casual: 10-50th. At-risk: <10th percentile AND >14 days since last visit. |
