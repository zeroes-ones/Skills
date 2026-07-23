# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): dbt Project Design & Patterns

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


**What good looks like:** dbt project with model documentation, tests, and lineage. BI dashboard loads in under 5 seconds. All metrics have definitions documented in a shared glossary. Data freshness meets SLA for every report. No hard-coded table references in SQL — all ref()'d.

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

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Metric Layer & Semantic Models

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

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): BI Architecture

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

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): A/B Testing & Experimentation

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

<!-- DEEP: 10+min -->
### Phase 5 (~25 min): SQL Optimization

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

<!-- DEEP: 10+min -->
### Phase 6 (~25 min): Data Visualization & Storytelling

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
