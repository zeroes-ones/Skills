# Data Modeling Guide

> **Author:** Sandeep Kumar Penchala

Production data modeling patterns covering dimensional modeling, dbt best practices, data quality testing, incremental models, data lineage, performance optimization, documentation, and governance. These practices support the analytics-engineer skill's data transformation and modeling discipline.

## Dimensional Modeling

### Star Schema

```
┌─────────────────────────────────────────────────────────┐
│                    Fact Table                            │
│  order_facts                                            │
│  ┌──────────────────────────────────────────────────┐   │
│  │ order_id (PK) | customer_key (FK) | date_key (FK)│   │
│  │ product_key (FK) | quantity | revenue | discount  │   │
│  └──────────────────────────────────────────────────┘   │
│         │              │                │               │
│    ┌────▼────┐   ┌─────▼──────┐   ┌─────▼──────┐       │
│    │Customer │   │Date        │   │Product     │       │
│    │Dimension│   │Dimension   │   │Dimension   │       │
│    └─────────┘   └────────────┘   └────────────┘       │
└─────────────────────────────────────────────────────────┘

Fact:    Business event/transaction (quantitative, additive measures)
Dimension: Contextual attributes (who, what, where, when) — for filtering & grouping
```

### Slowly Changing Dimensions (SCD)

| Type | Strategy | Example | When to Use |
|------|----------|---------|-------------|
| 0 | Retain original | Birth date | Immutable attributes |
| 1 | Overwrite | Fix typo in `customer_name` | No history needed |
| 2 | Add new row + effective dates | `customer_address` changes | Full history required |
| 3 | Add previous value column | `previous_address` col | Track only last change |
| 4 | Separate history table | `customer_address_history` | When dimension is wide |
| 6 | Hybrid (1 + 2 + 3) | Most flexible | Complex requirements |

```sql
-- SCD Type 2 implementation in dbt
{{
  config(
    materialized='snapshot',
    strategy='timestamp',
    updated_at='updated_at',
    unique_key='customer_id'
  )
}}
SELECT customer_id, name, email, address, updated_at
FROM {{ source('raw', 'customers') }}
-- dbt snapshot adds: dbt_valid_from, dbt_valid_to, dbt_scd_id
```

## dbt Best Practices

### Project Structure

```
my_dbt_project/
├── models/
│   ├── staging/           # 1:1 with source tables; light cleanup, rename
│   │   ├── stg_customers.sql
│   │   ├── stg_orders.sql
│   │   └── sources.yml
│   ├── intermediate/       # Joins, aggregations; may not be exposed
│   │   └── int_order_items_enriched.sql
│   └── marts/             # Business-facing models
│       ├── finance/
│       │   ├── fct_orders.sql
│       │   └── dim_customers.sql
│       └── marketing/
│           └── fct_campaign_performance.sql
├── tests/                 # Custom generic tests
├── macros/                # Reusable Jinja macros
├── analyses/              # One-off analysis queries
└── dbt_project.yml
```

### Materialization Choices

| Materialization | When to Use | Refresh |
|----------------|-------------|---------|
| `view` | Lightweight transforms, always fresh, no storage | Every query |
| `table` | Expensive transforms, queried frequently | `dbt run` rebuilds |
| `incremental` | Large tables (> 1M rows), append-only or upsert | Only new/changed rows |
| `ephemeral` | Intermediate CTE — not exposed, cleaner code | Inlined in dependent models |

```sql
-- incremental model with merge strategy
{{
  config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='sync_all_columns'
  )
}}

SELECT order_id, customer_id, order_date, total_amount
FROM {{ ref('stg_orders') }}
{% if is_incremental() %}
WHERE order_date >= (SELECT MAX(order_date) FROM {{ this }})
{% endif %}
```

## Data Quality Testing

### dbt Built-in Tests

```yaml
# models/staging/sources.yml — schema tests
version: 2
models:
  - name: stg_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: customer_id
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'shipped', 'delivered', 'cancelled']
              quote: true
      - name: total_amount
        tests:
          - dbt_utils.expression_is_true:
              expression: ">= 0"
    tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns:
            - order_id
            - order_date
```

### Custom Generic Tests

```sql
-- tests/generic/test_not_negative.sql
{% test not_negative(model, column_name) %}
SELECT {{ column_name }}
FROM {{ model }}
WHERE {{ column_name }} < 0
{% endtest %}

-- Usage in schema.yml:
--  - name: total_amount
--    tests:
--      - not_negative
```

## Incremental Models

### Late-Arriving Data Handling

```sql
-- Handle late-arriving data by looking back N days
{{
  config(
    materialized='incremental',
    unique_key='event_id',
    incremental_strategy='merge'
  )
}}

SELECT ...
FROM {{ ref('stg_events') }}
{% if is_incremental() %}
WHERE event_date >= (SELECT MAX(event_date) FROM {{ this }}) - INTERVAL '3 DAYS'
-- Reprocess last 3 days to catch late arrivals
{% endif %}
```

### Idempotency for Incremental Models

```sql
-- Merge strategy ensures idempotency — safe to re-run
{{
  config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    merge_update_columns=['status', 'total_amount', 'updated_at']
  )
}}

SELECT
  order_id,
  customer_id,
  status,
  total_amount,
  CURRENT_TIMESTAMP AS updated_at
FROM {{ ref('stg_orders') }}
```

## Data Lineage

### dbt DAG

```bash
# Generate and view lineage graph
dbt docs generate
dbt docs serve

# Check model dependencies
dbt ls --select +fct_orders       # All ancestors of fct_orders
dbt ls --select fct_orders+       # All descendants of fct_orders

# Check what will run
dbt ls --select state:modified+   # Modified models and downstream
```

### Column-Level Lineage

```yaml
# dbt 1.5+ — column-level lineage via semantic models
semantic_models:
  - name: orders
    defaults:
      agg_time_dimension: order_date
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
    measures:
      - name: total_revenue
        agg: sum
        expr: total_amount
      - name: order_count
        agg: count_distinct
        expr: order_id
```

## Performance Optimization

### Query Profiling

```sql
-- Identify slow models (Snowflake/BigQuery/Redshift)
-- Check dbt run results
SELECT
  node_id,
  execution_time,
  rows_affected,
  bytes_processed
FROM {{ ref('dbt_run_results') }}
ORDER BY execution_time DESC
LIMIT 10;
```

### Materialization Selection Guide

```
Model used by 1-2 downstream models, always-fresh needed      → view
Model used by 10+ downstream models, queried hourly            → table
Model has > 10M rows, only new data matters                    → incremental
Model is intermediate step, not queried directly               → ephemeral
```

### Partition Pruning

```sql
-- BigQuery: partition by date for cost efficiency
{{
  config(
    materialized='table',
    partition_by={'field': 'event_date', 'data_type': 'date'},
    cluster_by=['event_type']
  )
}}

-- Snowflake: clustering key
{{
  config(
    materialized='table',
    cluster_by=['customer_id', 'event_date']
  )
}}
```

## Documentation

### Model Descriptions

```yaml
# models/marts/finance/schema.yml
version: 2
models:
  - name: fct_orders
    description: >
      Fact table containing one row per order. Grain: order_id.
      Revenue is in USD. Excludes test orders (customer_type = 'test').
      Freshness: updated hourly, < 15 min lag from source.
    columns:
      - name: order_id
        description: "Unique identifier for each order. Surrogate key."
        tests: [unique, not_null]
      - name: total_revenue_usd
        description: "Order total in USD after discounts, before tax. Excludes shipping."
      - name: is_first_order
        description: "TRUE if this is the customer's first order (lifetime)."
```

### Source Freshness

```yaml
# models/staging/sources.yml
sources:
  - name: raw
    database: production
    schema: public
    freshness:
      warn_after: { count: 6, period: hour }
      error_after: { count: 24, period: hour }
    loaded_at_field: ingested_at
    tables:
      - name: orders
      - name: customers
```

```bash
# Check freshness in CI
dbt source freshness
```

## Governance

### Data Contracts

```yaml
# contract for fct_orders
models:
  - name: fct_orders
    config:
      contract:
        enforced: true
    columns:
      - name: order_id
        data_type: integer
        constraints:
          - type: not_null
          - type: primary_key
      - name: total_revenue_usd
        data_type: numeric(18,2)
      - name: order_date
        data_type: date
```

### Schema Versioning

```
Strategy: Never break downstream consumers without migration path.

Breaking changes:
  1. Create new model version (e.g., fct_orders_v2) alongside existing
  2. Announce deprecation timeline (e.g., 30 days)
  3. Migrate consumers to v2
  4. Remove v1 after all consumers migrated

Non-breaking changes (additive only):
  1. Add column → safe; add to model, re-run
  2. Widen data type → safe (INT → BIGINT)
  3. Rename column → BREAKING; use new column + deprecate old
  4. Remove column → BREAKING; use contract enforcement
```

### Deprecation Policy

```yaml
# model deprecation announcement
models:
  - name: fct_orders_v1
    description: "⚠️ DEPRECATED — will be removed 2026-09-01. Migrate to fct_orders_v2."
    meta:
      deprecation_date: "2026-09-01"
      replacement_model: "fct_orders_v2"
```

### Data Catalog

```
Every model MUST have:
  ✅ Description (what it represents; grain)
  ✅ Column descriptions (what each column means)
  ✅ Owner (team or individual responsible)
  ✅ Freshness SLA (how often updated; max acceptable lag)
  ✅ Access level (public, internal, restricted, pii)

Expose via:
  dbt docs (open-source)
  Data catalogs: Atlan, Alation, DataHub, Amundsen
```

This data modeling guide implements the analytics-engineer skill's layered approach — staging → intermediate → marts — with dbt as the transformation engine, quality tests at every layer, and governance built into the model definitions, not bolted on after.
