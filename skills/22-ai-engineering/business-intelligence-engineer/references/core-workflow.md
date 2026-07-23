# Core Workflow — Full Implementation

<!-- STANDARD: 3min -->

### Phase 1 (~25 min): Semantic Layer Design

#### dbt Metrics with MetricFlow

```yaml
# models/semantic_layer/metrics/revenue.yml
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
        type_params:
          time_granularity: day
      - name: order_status
        type: categorical
    measures:
      - name: revenue
        agg: sum
        expr: net_revenue_amount
      - name: order_count
        agg: count
        expr: order_id

metrics:
  - name: net_revenue
    description: Total net revenue after discounts and refunds
    type: simple
    label: Net Revenue
    type_params:
      measure: revenue

  - name: net_revenue_mom_growth
    description: Month-over-month net revenue growth rate
    type: ratio
    label: Revenue MoM Growth
    type_params:
      numerator: net_revenue
      denominator: net_revenue
      numerator_offsets:
        month_offset: 0
      denominator_offsets:
        month_offset: -1
```

#### LookML Explores

```yaml
# orders.explore.lkml
explore: orders {
  label: "Order Analytics"
  from: fct_orders

  join: dim_customers {
    sql_on: ${orders.customer_id} = ${dim_customers.customer_id} ;;
    type: left_outer
    relationship: many_to_one
  }

  join: fct_order_lines {
    sql_on: ${orders.order_id} = ${fct_order_lines.order_id} ;;
    type: left_outer
    relationship: one_to_many
  }
}

# orders.view.lkml
view: fct_orders {
  sql_table_name: analytics.fct_orders ;;

  dimension: order_id { type: number primary_key: yes sql: ${TABLE}.order_id ;; }
  dimension: order_date { type: date sql: ${TABLE}.order_date ;; }
  dimension_group: created { type: time timeframes: [date, week, month, quarter, year] sql: ${TABLE}.created_at ;; }

  measure: net_revenue { type: sum sql: ${TABLE}.net_revenue_amount ;; value_format_name: usd }
  measure: order_count { type: count }
  measure: average_order_value { type: number sql: ${net_revenue} / NULLIF(${order_count}, 0) ;; value_format_name: usd }
}
```

#### Universal Semantic Layer Principles

- **MetricFlow** (dbt): code-first, version-controlled, git-friendly — best for dbt shops
- **LookML** (Looker): GUI + code hybrid, strong permission model, embedded analytics — best for Looker
- **Cube.js**: open-source, headless BI, REST/GraphQL API, caching layer — best for custom apps
- **Principles**: metrics defined once, used everywhere; dimensions drillable across metrics; time-over-time comparisons built into semantic layer, not dashboard-level calculations

### Phase 2 (~25 min): Self-Serve Dashboard Architecture

#### Tool Selection

| Tool | Best For | Pricing Model | Governance |
|------|----------|---------------|------------|
| Looker | Enterprise, embedded analytics | Per-user, expensive | Strong — LookML, folders, permissions |
| Metabase | Mid-market, simplicity | Open-source or hosted | Moderate — collections, permissions |
| Lightdash | dbt-native, developer-first | Open-source or cloud | Strong — dbt as source of truth |
| Holistics | Data modeling, governed self-serve | Per-user, mid-range | Strong — semantic modeling layer |
| Streamlit | Custom data apps, ML dashboards | Free, self-hosted | Custom — code-level |
| Preset (Superset) | Large-scale, FOSS | Open-source or cloud | Moderate — roles, datasets |

#### Governed Self-Service Model

```
┌────────────────────────────────────────────────────────────────┐
│ Governed Self-Service Architecture                              │
├────────────────────────────────────────────────────────────────┤
│                         LAYER 1: LOCKED                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Semantic Layer (dbt / LookML / MetricFlow)              │   │
│  │  ────────────────────────────────────────                │   │
│  │  Metrics: defined by BI team, locked for editing         │   │
│  │  Dimensions: defined by BI team, governed joins          │   │
│  │  ⚠️  Users CANNOT create new metric definitions           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                             ↕                                    │
│                         LAYER 2: GUIDED                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Exploration Layer                                       │   │
│  │  ────────────────────────────────────────                │   │
│  │  Saved Explores: BI team creates starting points         │   │
│  │  Field picker: users combine locked metrics/dimensions   │   │
│  │  Filters: users apply any filter within governed fields  │   │
│  │  ✅ Users CAN explore, filter, visualize, save            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                             ↕                                    │
│                         LAYER 3: FREE                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Personal Analysis Layer                                 │   │
│  │  ────────────────────────────────────────                │   │
│  │  Personal dashboards: users create own visualizations    │   │
│  │  Personal collections: organized by user/team            │   │
│  │  Shared only with explicit approval                      │   │
│  │  ✅ Users CAN create personal dashboards, NOT new metrics │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

#### Dashboard Review Gates

- **Tier 1 — Board/Investor** (every number must be verified): peer review + stakeholder sign-off + reconciliation check
- **Tier 2 — Operational** (numbers inform daily decisions): peer review + automated freshness check
- **Tier 3 — Exploratory** (WIP, may have caveats): "DRAFT" label, creator's name, last updated date

### Phase 3 (~25 min): Board Reporting

#### Investor KPIs

1. **Annual Recurring Revenue (ARR)**:
   - **Definition**: total annualized value of active subscriptions at a point in time
   - **Calculation**: SUM(monthly_recurring_revenue × 12) or SUM(annual_contract_value)
   - **Nuance**: exclude one-time fees, professional services, usage overage unless contractual
   - **Visualization**: ARR over time with expansion (new + upsell) minus contraction (churn + downgrade)

2. **Net Revenue Retention (NRR)**:
   - **Definition**: % of revenue retained from existing customers, including expansion
   - **Calculation**: (beginning ARR − churn − downgrade + expansion) / beginning ARR
   - **Benchmarks**: >120% excellent, 100–120% good, <100% concerning
   - **Board question this answers**: "Are we growing even without new customers?"

3. **LTV/CAC Ratio**:
   - **Definition**: lifetime value of customer vs cost to acquire them
   - **Calculation**: (ARPU × gross margin %) / (monthly churn rate) ÷ CAC
   - **Benchmarks**: >3× healthy, <1× unsustainable
   - **Nuance**: LTV should use gross margin, not revenue; CAC should be fully loaded (marketing + sales + SDR compensation)

4. **Magic Number**:
   - **Definition**: sales efficiency — how much revenue each dollar of sales/marketing generates
   - **Calculation**: (current quarter ARR − previous quarter ARR) × 4 / previous quarter S&M spend
   - **Benchmarks**: >0.75 invest more, 0.5–0.75 maintain, <0.5 investigate
   - **Board question this answers**: "Should we pour more fuel on the fire, or fix the engine?"

5. **Operational Metrics**:
   - **Burn Multiple**: net burn / net new ARR — efficiency of growth spend
   - **Rule of 40**: revenue growth rate + profit margin — should sum to ≥40%
   - **CAC Payback Period**: CAC / (ARPU × gross margin) — months to recover acquisition cost

#### Report Architecture

```sql
-- Example: monthly board snapshot table
CREATE TABLE analytics.board_metrics_monthly (
    report_month DATE,
    metric_name VARCHAR,
    metric_value NUMERIC,
    metric_unit VARCHAR,
    prior_month_value NUMERIC,
    prior_year_value NUMERIC,
    mom_change_pct NUMERIC,
    yoy_change_pct NUMERIC,
    target_value NUMERIC,
    target_variance_pct NUMERIC,
    data_freshness_ts TIMESTAMP,
    reconciliation_status VARCHAR -- 'VERIFIED', 'PENDING', 'FLAGGED'
);
```

### Phase 4 (~25 min): Clinical Outcomes Analytics

#### Patient-Reported Outcome (PRO) Trends

1. **PRO instruments** — standardized questionnaires measuring patient health status:
   - **PROMIS-29**: physical function, anxiety, depression, fatigue, sleep, pain, social roles
   - **PHQ-9**: depression severity (score 0–27; ≥10 indicates moderate depression)
   - **GAD-7**: anxiety severity (score 0–21; ≥10 indicates moderate anxiety)
   - **EQ-5D-5L**: health-related quality of life across 5 dimensions

2. **Trend analysis**:
   - **Clinically meaningful change**: not just statistical significance — does the change exceed the minimal clinically important difference (MCID)?
   - PHQ-9 MCID: 5 points; GAD-7 MCID: 4 points; PROMIS Physical Function: 3–5 T-score points

3. **Treatment adherence patterns**:
   - Medication possession ratio (MPR): days supply dispensed / days in period
   - Proportion of days covered (PDC): days covered / days in period
   - Adherence threshold: PDC ≥0.80 considered adherent
   - **Analytics**: cohort by condition, adherence trend over time, adherence drop-off after month N

#### Quality-of-Life Indices

- **QALY (Quality-Adjusted Life Year)**: years of life × quality weight (0 = death, 1 = perfect health)
- **DALY (Disability-Adjusted Life Year)**: years lost to premature death + years lived with disability
- **Dashboard**: trend of QALY/DALY by condition cohort, pre/post intervention comparison

### Phase 5 (~25 min): Pharma Partner Reporting

#### Real-World Evidence (RWE) Dashboards

1. **Patient population analytics:**
   - Demographics: age distribution, gender, geography, comorbidities
   - Treatment patterns: first-line therapy → second-line → third-line (Sankey diagram)
   - Persistence: time on therapy before discontinuation (Kaplan-Meier curve)
   - Switching: % patients switching from Drug A to Drug B within N months

2. **De-identification requirements:**
   - **HIPAA Safe Harbor**: remove 18 identifiers (names, dates more specific than year, ZIP codes <20K population, etc.)
   - **Expert Determination**: statistician certifies re-identification risk is "very small"
   - **Minimum cell size**: suppress counts <11 (or per partner agreement; CMS uses <11)
   - **K-anonymity**: each record indistinguishable from at least K other records (K ≥ 5 typical)

3. **Data export compliance:**
   - No raw PHI in exports — aggregated only
   - Partner-specific data filtered by contract scope
   - Export audit log: who, what, when, for which partner
   - Encryption at rest and in transit for all exports

### Phase 6 (~20 min): Data Modeling for BI

#### Star Schema Design

```
                    ┌──────────────────┐
                    │   dim_patients    │
                    │──────────────────│
                    │ patient_key (PK)  │
                    │ patient_id (NK)   │
                    │ age_group         │
                    │ gender            │
                    │ region            │
                    │ insurance_type    │
                    │ first_visit_date  │
                    └────────┬─────────┘
                             │
    ┌──────────────────┐    │    ┌──────────────────┐
    │   dim_providers  │    │    │    dim_dates     │
    │──────────────────│    │    │──────────────────│
    │ provider_key (PK)│    │    │ date_key (PK)     │
    │ provider_id (NK) │    │    │ full_date         │
    │ specialty        │    │    │ year, quarter     │
    │ practice_type    │    │    │ month_name        │
    └────────┬─────────┘    │    │ is_holiday        │
             │              │    └────────┬──────────┘
             │              │             │
             ▼              ▼             ▼
        ┌────────────────────────────────────────┐
        │              fct_encounters             │
        │────────────────────────────────────────│
        │ encounter_key (PK)                      │
        │ patient_key (FK)                        │
        │ provider_key (FK)                       │
        │ encounter_date_key (FK)                 │
        │ encounter_type                          │
        │ primary_diagnosis_code                  │
        │ billed_amount                           │
        │ allowed_amount                          │
        │ patient_responsibility                  │
        └────────────────────────────────────────┘
```

#### Slowly Changing Dimensions (SCDs)

| SCD Type | Behavior | Use Case | Implementation |
|----------|----------|----------|---------------|
| Type 0 | Never changes | Birth date, original source | Preserve original value |
| Type 1 | Overwrite | Spelling corrections | UPDATE in place |
| Type 2 | Track history | Subscription tier, address | Add new row with effective/expiry dates |
| Type 3 | Track previous value | Territory reassignment | Add `previous_value` column |
| Type 6 | Hybrid (1+2+3) | Complex tracking | Current flag + previous + original |

#### Snapshots vs Incrementals

- **Snapshots**: capture full state at point in time (`dbt snapshot`); use for SCD Type 2
- **Incrementals**: append/merge new records since last run; use for fact tables, event streams
- **Decision rule**: if you need to answer "what did this look like on date X?", use snapshots; if you only need current state and recent deltas, incrementals suffice

### Phase 7 (~25 min): ETL for BI

#### dbt Transformation Patterns

```yaml
# dbt_project.yml
models:
  bi_reporting:
    staging:        # 1:1 with source tables, light cleaning
      +materialized: view
      +schema: staging
    intermediate:   # joins, aggregations, business logic
      +materialized: ephemeral
      +schema: intermediate
    marts:          # final tables consumed by BI tools
      +materialized: table
      +schema: marts

# Incremental model
-- models/marts/fct_daily_encounters.sql
{{
  config(
    materialized='incremental',
    unique_key='encounter_id',
    on_schema_change='sync_all_columns'
  )
}}
SELECT * FROM {{ ref('stg_encounters') }}
{% if is_incremental() %}
WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}
```

#### Data Freshness SLAs

| Data Domain | Freshness SLA | Monitoring |
|-------------|--------------|------------|
| Board reports | 9 AM ET on report day | dbt source freshness |
| Operational dashboards | Hourly | Airflow/Dagster sensor |
| Clinical outcomes | Daily + 2 hours | Great Expectations |
| Pharma partner reports | Weekly (Monday 12 PM) | dbt Cloud job |
| Ad-hoc exploration | Stale after 24 hours | Warning only |

#### Testing Strategy

```yaml
# dbt tests in schema.yml
models:
  - name: fct_encounters
    columns:
      - name: encounter_id
        tests:
          - unique
          - not_null
      - name: patient_key
        tests:
          - not_null
          - relationships:
              to: ref('dim_patients')
              field: patient_key
      - name: billed_amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1000000
      - name: allowed_amount
        tests:
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: "{{ 2 * billed_amount }}"
```

### Phase 8 (~20 min): Embedded Analytics

#### Customer-Facing Dashboards

- **Pattern**: embed analytics directly in product using iframe, React component, or API
- **Tools**: Looker Embed, Metabase Embed, Cube.js, custom with chart library
- **Authentication**: JWT-based SSO, row-level security enforced at query time
- **Performance**: pre-aggregate common queries, cache heavily, limit date range to 12 months default

#### White-Label Reporting

- **Multi-tenant architecture**: separate schema per tenant OR row-level security on shared tables
- **Branding**: custom logos, colors, fonts per tenant
- **Export formats**: PDF (paginated), CSV (raw data), Excel (formatted), API (JSON)
- **Scheduling**: tenant-configured report delivery (email, Slack, webhook)

#### Data Export Compliance

- **Audit trail**: every export logged (user, tenant, report, timestamp, row count, format)
- **Data minimization**: export only data the user has permission to see
- **Retention**: auto-delete exports older than N days (configurable per tenant)
- **Encryption**: exports encrypted at rest; download links expire; watermark PDFs with "CONFIDENTIAL — [Tenant Name] — [Date]"
