---
name: analytics-engineer
description: dbt patterns, metric layers, BI architecture, data modeling for analytics, A/B testing and experimentation, SQL optimization, data visualization, and self-service analytics (Looker/Metabase/Lightdash). Triggered by analytics, dbt, Looker, Metabase, A/B test, metric layer, event tracking, SQL optimization, dashboard.
author: Sandeep Kumar Penchala
---

# Analytics Engineer

Bridge raw data and actionable business insight. This skill covers dbt project design and patterns
(model layers, incremental models, snapshots, macros, tests), metric definition (semantic models,
metric types, time dimensions), BI architecture (semantic layer vs direct query, caching, row-level
security), data modeling for analytics (wide tables vs star schema, pre-aggregation, denormalization),
experimentation (A/B test design, sample size, statistical significance, SRM), SQL optimization
(CTEs vs subqueries, window functions, query plans, materialization), and data visualization
principles (chart selection, dashboard design, data storytelling).

## When to Use

- Designing a dbt project: model layering (staging → intermediate → marts), incremental strategies, snapshot design
- Defining a company-wide metric layer: single source of truth for "DAU," "Revenue," "Churn Rate"
- Building self-service BI with Looker, Metabase, Lightdash, or Superset for non-technical stakeholders
- Designing and analyzing A/B tests with statistical rigor: power analysis, CUPED, SRM checks
- Optimizing slow SQL queries: CTE vs subquery tradeoffs, window functions, query plan reading
- Designing event tracking: naming conventions, property design, identity resolution
- Creating data visualizations that tell a story: chart selection, dashboard architecture, data storytelling
- Migrating from "Excel hell" or legacy BI to a modern analytics stack

## Core Workflow

### Phase 1: dbt Project Design & Patterns

1. **Project Structure** — The standard layered approach:
   ```
   models/
   ├── staging/        # stg_stripe__payments.sql — 1:1 with source, rename + cast
   │                   #   Config: materialized='view' (cheap, always fresh)
   ├── intermediate/   # int_order_payments.sql — business logic, multi-source joins
   │                   #   Config: materialized='table' or 'ephemeral' (CTE)
   └── marts/          # fct_orders.sql — business-facing, single source of truth
                       #   Config: materialized='table' or 'incremental'
   ```

2. **Materialization Decision Matrix**:

   | Strategy | When | Pros | Cons |
   |---|---|---|---|
   | **View** | Simple transforms, always-current data | Zero storage, always fresh | Recomputes on every query |
   | **Table** | Complex joins, dashboard source tables | Fast queries, snapshotable | Must be rebuilt/re-run |
   | **Incremental** | Large fact tables (>100M rows), append-mostly | Fast builds, low cost | Complex logic, late data handling |
   | **Ephemeral** | Reusable CTEs, not queried directly | No storage, composable | Re-computed per downstream model |
   | **Snapshot** | SCD Type 2 dimensions | Tracks history automatically | Storage grows over time |

3. **Incremental Model Pattern**:
   ```sql
   {{
       config(
           materialized='incremental',
           unique_key='event_id',
           partition_by={'field': 'event_date', 'data_type': 'date'},
           on_schema_change='sync_all_columns'
       )
   }}
   SELECT * FROM {{ source('events', 'product_events') }}
   {% if is_incremental() %}
   WHERE event_date >= (SELECT MAX(event_date) FROM {{ this }})
   {% endif %}
   ```

4. **Snapshot (SCD Type 2) Strategy**:
   ```sql
   {% snapshot customer_dimension %}
   {{ config(target_schema='marts', unique_key='customer_id', strategy='check', check_cols=['plan_type', 'region', 'status']) }}
   SELECT * FROM {{ ref('stg_customers') }}
   {% endsnapshot %}
   -- dbt automatically adds: dbt_valid_from, dbt_valid_to, dbt_scd_id
   ```

5. **dbt Tests — The Minimum Viable Suite**:
   ```yaml
   models:
     - name: fct_orders
       columns:
         - name: order_id
           tests: [unique, not_null]
         - name: customer_id
           tests: [not_null, {relationships: {to: ref('dim_customers'), field: 'customer_id'}}]
         - name: amount
           tests: [not_null, {dbt_utils.accepted_range: {min_value: 0.01}}]
         - name: status
           tests: [not_null, {accepted_values: {values: ['pending', 'completed', 'cancelled']}}]
   ```

6. **Macros for DRY Code**:
   ```sql
   -- macros/cents_to_dollars.sql
   {% macro cents_to_dollars(column_name, precision=2) %}
   ROUND({{ column_name }} / 100.0, {{ precision }})
   {% endmacro %}
   -- Usage: {{ cents_to_dollars('amount_cents') }} AS amount_dollars
   ```

### Phase 2: Metric Layer & Semantic Models

1. **Metric Definition Framework** — The single source of truth:

   | Metric Type | Example | Definition |
   |---|---|---|
   | **Simple** | Revenue | `SUM(order_amount)` — direct aggregation |
   | **Ratio** | Conversion Rate | `COUNT(DISTINCT purchasers) / COUNT(DISTINCT visitors)` |
   | **Cumulative** | MTD Revenue | `SUM(revenue) FOR month TO DATE` |
   | **Derived** | ARPU | `Revenue / Active Users` |

2. **Semantic Model** — Define once, use everywhere:
   ```yaml
   # dbt Semantic Layer / MetricFlow
   semantic_models:
     - name: orders
       model: ref('fct_orders')
       entities:
         - name: order_id
           type: primary
         - name: customer_id
           type: foreign
       dimensions:
         - name: order_date
           type: time
           type_params: {time_granularity: day}
         - name: status
           type: categorical
       measures:
         - name: revenue
           agg: sum
           expr: order_amount
         - name: order_count
           agg: count
           expr: order_id

   metrics:
     - name: monthly_revenue
       type: simple
       label: Monthly Revenue
       type_params:
         measure: revenue
   ```

3. **Metric Governance** — Prevent the "five definitions of DAU" problem:
   ```
   Metric Registry (Git-based):
   metrics/
   ├── revenue.yaml         # One canonical definition
   ├── active_users.yaml    # DAU, WAU, MAU — with date dimension
   ├── churn_rate.yaml      # Formula: (lost_customers / start_customers) × 100
   └── conversion_rate.yaml # Funnel step N+1 / Funnel step N
   ```

### Phase 3: BI Architecture

1. **BI Tool Decision**:

   | Tool | Model Layer | Version Control | Best For |
   |---|---|---|---|
   | **Looker** | LookML (git-based) | Native | Engineering-heavy, complex data models |
   | **Metabase** | GUI-based | Limited (export/import) | Business users, quick setup |
   | **Lightdash** | dbt-native | Git (dbt repo) | dbt-centric teams |
   | **Superset** | SQL Lab + Virtual Datasets | Limited | OSS, complex viz |

2. **Semantic Layer vs Direct Query**:
   ```
   Semantic Layer (Looker/Lightdash):
   ✅ Consistent metric definitions across all dashboards
   ✅ Row-level security enforced at the semantic layer
   ✅ Query optimization (aggregate awareness, caching)
   ❌ Upfront investment in model definition

   Direct Query (Metabase/Superset):
   ✅ Fast to build — SQL editor to dashboard in minutes
   ❌ Metric definitions duplicated across dashboards
   ❌ RLS must be implemented at DB level or per-question
   ```

3. **Caching Strategy**:
   - Looker: `persist_for` parameter — cache query results for N hours
   - dbt: materialized tables (pre-computed) vs views (live)
   - BI Engine (BigQuery): in-memory acceleration for Looker
   - dbt incremental: rebuild only new partitions

4. **Row-Level Security (RLS)**:
   ```yaml
   # Looker LookML — restrict by user attribute
   access_filter:
     field: orders.region
     user_attribute: allowed_regions

   # BigQuery — policy tag
   CREATE ROW ACCESS POLICY region_filter ON fct_orders
   GRANT TO ("group:analysts@company.com")
   FILTER USING (region = SESSION_USER());
   ```

### Phase 4: A/B Testing & Experimentation

1. **Experiment Design Process**:
   ```
   1. Hypothesis: "Adding one-click checkout increases conversion by 5%"
   2. Primary metric: Conversion rate (purchases / visitors)
   3. Guardrail metrics: Revenue per user (shouldn't drop), Page load time (shouldn't rise)
   4. Sample size calculation: α=0.05, β=0.2 (80% power), MDE=5%
   5. Randomization unit: User ID (hashed, consistent across sessions)
   6. Duration: [calculated from sample size ÷ daily traffic]
   7. Analysis: 2-sample z-test for proportions, t-test for continuous metrics
   ```

2. **Sample Size Calculator** (for proportions):
   ```python
   from scipy import stats

   def sample_size_proportion(p_baseline, mde, alpha=0.05, power=0.8):
       z_alpha = stats.norm.ppf(1 - alpha / 2)
       z_beta = stats.norm.ppf(power)
       p_alt = p_baseline * (1 + mde)
       p_pooled = (p_baseline + p_alt) / 2
       n = (z_alpha * (2 * p_pooled * (1 - p_pooled))**0.5 +
            z_beta * (p_baseline * (1 - p_baseline) + p_alt * (1 - p_alt))**0.5)**2 / (p_alt - p_baseline)**2
       return int(n)

   # Baseline 10% conversion, 5% relative lift (→ 10.5%), 80% power
   # Result: ~50,000 users per variant
   ```

3. **Statistical Analysis**:
   ```
   For proportions (conversion rate):  z-test for 2 proportions
   For continuous (revenue per user): Welch's t-test (unequal variance)
   For non-normal (time to purchase): Mann-Whitney U test
   For multiple metrics:              Bonferroni/Holm correction or multivariate test

   Key rule: Pre-register primary metric BEFORE experiment starts.
   Never: "Let's check 30 metrics and report significant ones."
   ```

4. **CUPED (Variance Reduction)**:
   ```sql
   -- Use pre-experiment data to reduce variance
   WITH pre_experiment AS (
     SELECT user_id, AVG(metric_value) AS pre_avg
     FROM user_metrics
     WHERE date BETWEEN '2026-07-01' AND '2026-07-14'  -- 2 weeks pre-experiment
     GROUP BY 1
   )
   SELECT
     variant,
     AVG(metric_value - θ * pre_avg) AS cuped_adjusted_metric  -- θ = covariance / variance
   FROM experiment_results
   JOIN pre_experiment USING (user_id)
   GROUP BY 1;
   -- CUPED can reduce required sample size by 50%+
   ```

5. **SRM Check (Sample Ratio Mismatch)**:
   ```sql
   -- Expected: 50/50 split. Check with chi-squared test.
   SELECT
     variant,
     COUNT(*) AS users,
     COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS ratio
   FROM experiment_assignments
   GROUP BY 1;
   -- If p < 0.01: SRM detected — STOP experiment, investigate assignment bug
   ```

6. **Experiment Decision Framework**:
   ```
   Significant positive + Guardrails OK       → SHIP
   Significant positive + Guardrail degraded  → INVESTIGATE (tradeoff analysis)
   Not significant at required duration       → INCONCLUSIVE (extend or discard)
   Significant negative                       → DISCARD (document learning)
   SRM detected                                → INVALID (fix bug, re-randomize)
   ```

### Phase 5: SQL Optimization

1. **CTE vs Subquery Decision**:
   ```sql
   -- ✅ CTE: Readable, reusable, self-documenting
   WITH monthly_revenue AS (
     SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS revenue
     FROM orders GROUP BY 1
   ),
   monthly_growth AS (
     SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_revenue
     FROM monthly_revenue
   )
   SELECT *, (revenue - prev_revenue) / prev_revenue * 100 AS growth_pct
   FROM monthly_growth;

   -- ✅ Subquery: Simple, one-off filter
   SELECT * FROM orders WHERE customer_id IN (SELECT customer_id FROM vip_customers);

   -- ❌ Anti-pattern: Deeply nested subqueries (hard to read, same performance as CTE)
   ```

2. **Window Functions** — Smarter aggregations:
   ```sql
   -- Running total
   SUM(revenue) OVER (PARTITION BY region ORDER BY order_date ROWS UNBOUNDED PRECEDING)

   -- Percentile rank
   PERCENT_RANK() OVER (PARTITION BY category ORDER BY revenue)

   -- Moving average (7-day)
   AVG(revenue) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
   ```

3. **Query Plan Reading** — Identify bottlenecks:
   ```
   Look for in query plan:
   - Full table scan (no partition filter) → Add WHERE clause or partition filter
   - Broadcast join (small table sent to all nodes) → Check if table is unexpectedly large
   - Shuffle (data movement between nodes) → Co-locate join keys or bucket by join key
   - Spill to disk → Increase memory or reduce data per node

   Snowflake: Use QUERY_PROFILE in Snowsight
   BigQuery: Execution details → Slot time, shuffle bytes
   PostgreSQL: EXPLAIN ANALYZE
   ```

4. **Materialization Strategy**:
   ```sql
   -- dbt: choose materialization based on access pattern

   -- Views: Always fresh, cheap storage, recomputed on query
   --   Best: Staging models, small datasets

   -- Tables: Pre-computed, fast queries, takes storage
   --   Best: Dashboard sources, complex joins queried 100x/day

   -- Incremental: Append-only, partition-aware
   --   Best: Fact tables, event streams, daily aggregations
   ```

### Phase 6: Data Visualization & Storytelling

1. **Chart Selection Framework**:

   | Relationship | Chart Type | Example |
   |---|---|---|
   | **Comparison** | Bar chart, column chart | Revenue by region |
   | **Change over time** | Line chart, area chart | DAU over 90 days |
   | **Distribution** | Histogram, box plot | Order value distribution |
   | **Part-to-whole** | Stacked bar, treemap, pie (≤ 5 segments) | Revenue by product |
   | **Correlation** | Scatter plot, bubble chart | Ad spend vs revenue |
   | **Ranking** | Horizontal bar (sorted) | Top 10 products |
   | **Geospatial** | Choropleth map | Revenue by country |

2. **Dashboard Architecture**:
   ```
   Level 1 (Top):  KPI cards — 3-5 key metrics (Revenue, DAU, Conversion Rate, Churn)
                   Trend sparklines, % change vs previous period
   Level 2 (Mid):  Trend charts — Daily/weekly/monthly views, segmented by channel/region
   Level 3 (Bottom): Drill-down tables — Top/bottom performers, outliers, details
   ```

3. **Data Storytelling Checklist**:
   - [ ] Title answers the question: not "Revenue Chart" but "Revenue grew 15% YoY driven by APAC expansion"
   - [ ] Annotations explain anomalies: "July dip: 3-day payment outage"
   - [ ] Color is intentional: one highlight color, grayscale for everything else
   - [ ] Y-axis starts at zero for bar charts (unless showing small changes)
   - [ ] Time on X-axis is consistent: daily, weekly, monthly — not mixed

## Best Practices

- **One source of truth for metrics** — Define in dbt semantic layer or metric registry. Never duplicate `revenue = SUM(amount)` across 5 dashboards.
- **Stage → Intermediate → Mart** — Never expose raw source tables to end users. Stage for cleanliness, intermediate for business logic, marts for consumption.
- **Test data, not code** — dbt `unique`, `not_null`, `relationships` tests on every model. Custom tests for business rules (`revenue >= 0`).
- **Pre-aggregate for dashboards** — A dashboard that queries 500M rows on every load is broken. Use incremental models, materialized tables, or BI cache.
- **Pre-register experiments** — Document hypothesis, metrics, and sample size before launching. Never cherry-pick significant results from 50 metrics.
- **Segment by default** — Every dashboard should allow filtering by platform, region, plan tier, and user cohort.
- **Document metric definitions** — "Is 'active user' someone who opened the app or made a purchase?" Put the answer in the dashboard description.

## Cross-Skill Coordination

Analytics engineers build the metrics layer that drives business decisions. They coordinate with data engineers for raw data, product for metric definitions, ML engineers for feature data, and business stakeholders for reporting needs.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Data Engineer** | Raw data ingestion, pipeline health, schema changes | Source schema expectations, freshness SLAs, data quality issues, backfill requests, CDC event formats |
| **Product Strategist** | Metric definitions, North Star metric, experiment design | Metric taxonomy, event tracking specification, A/B test metric framework, dashboard requirements |
| **ML/AI Engineer** | Feature data, training datasets, model evaluation metrics | Feature computation in dbt, labeled dataset creation, model performance dashboards, prediction monitoring queries |
| **Backend Developer** | Event tracking implementation, API data sources | Event schema design, tracking SDK instrumentation, API response data shape for analytics ingestion |
| **Growth Engineer** | Experimentation metrics, activation tracking | A/B test metric definitions, statistical analysis queries, activation funnel instrumentation, cohort definitions |
| **Business Strategist** | Business KPIs, board reporting, investor metrics | Revenue definitions, CAC/LTV calculations, market segmentation queries, ARR/MRR reporting |
| **Data Governance** | Metric certification, data catalog, access controls | Metric documentation in catalog, certified vs experimental metric tagging, PII access policy for analytics data |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| Source data schema change (breaking) | Data Engineer | Update staging models; fix dbt transforms |
| Metric definition change (e.g., "active user" redefined) | Product Strategist, Business Strategist, Growth Engineer | All dashboards and experiments using old definition need update |
| Data quality test failure in production dbt run | Data Engineer, Affected stakeholders | Root cause investigation; downstream impact assessment |
| New tracking event proposed | Product Strategist, Backend Developer | Schema review; instrumentation effort estimation |
| Dashboard data stale (>24 hours) | Data Engineer | Pipeline health check; SLA breach |

### Escalation Path

```
Data pipeline broken (upstream)? → Data Engineer → DevOps Engineer
Metric disagreement across teams? → Product Strategist → Data governance council
Dashboard showing materially incorrect data? → Data Engineer → Affected stakeholders (immediate notification)
PII exposed in analytics layer? → Security Engineer → Compliance Officer
```

## Production Checklist

### dbt & Data Modeling
- [ ] dbt project structured: staging → intermediate → marts with consistent naming
- [ ] Materialization strategy documented per model type
- [ ] dbt tests on every model: unique, not_null, relationships, accepted_values minimum
- [ ] Custom tests for business logic: positive amounts, date consistency, logical invariants
- [ ] Snapshots (SCD Type 2) configured for slowly changing dimensions
- [ ] Source freshness checks running on schedule
- [ ] `dbt docs` generated and published; column-level descriptions complete

### Metrics & BI
- [ ] Metric layer defined — single source of truth for all KPIs
- [ ] Semantic models: entities, dimensions, measures documented
- [ ] BI tool configured: caching, row-level security, scheduled reports
- [ ] Executive dashboard (3-5 top-level KPIs) + Product dashboard (funnels, cohorts, segments)
- [ ] Dashboard load time < 5 seconds (materialized tables, aggregate awareness, BI cache)

### Experimentation
- [ ] A/B test design template: hypothesis, primary metric, guardrail metrics, sample size, duration
- [ ] Sample size calculator accessible to all product teams
- [ ] CUPED or equivalent variance reduction implemented
- [ ] SRM (Sample Ratio Mismatch) check on every experiment
- [ ] Experiment results repo: hypothesis, setup, results, decision, learnings
- [ ] Pre-registration enforced — no peeking or cherry-picking

### SQL & Performance
- [ ] Incremental models for tables > 100M rows
- [ ] Query plan reviewed for top 10 most-expensive queries
- [ ] Window functions used for running totals, moving averages, rankings (not self-joins)
- [ ] Materialized views or aggregate tables for frequently accessed aggregations
- [ ] CI pipeline: `dbt build --select state:modified+` — only build changed models

### Operations
- [ ] Data freshness monitoring with alerts on stale dashboards
- [ ] Analytics on-call rotation for critical pipeline failures
- [ ] BI tool usage analytics: which dashboards are viewed? Which are ignored (archive candidates)?
- [ ] Stakeholder training: self-service exploration, how to read an A/B test result, when to ask for help

## References

- dbt Best Practices: https://docs.getdbt.com/best-practices
- dbt Semantic Layer: https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-semantic-layer
- Looker LookML Best Practices: https://cloud.google.com/looker/docs/best-practices
- A/B Testing at Scale (Kohavi et al.): https://exp-platform.com/
- Amplitude Data Taxonomy Playbook: https://amplitude.com/data-taxonomy-playbook
- SQL Style Guide: https://www.sqlstyle.guide/
- The Visual Display of Quantitative Information (Tufte): https://www.edwardtufte.com/
