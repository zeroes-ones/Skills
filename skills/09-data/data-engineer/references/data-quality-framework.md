# Data Quality Framework — Production Field Manual

## Table of Contents
1. [Data Quality Dimensions](#data-quality-dimensions)
2. [Great Expectations (GX) Framework](#great-expectations-gx-framework)
3. [WAP Pattern (Write-Audit-Publish)](#wap-pattern-write-audit-publish)
4. [Data Contracts](#data-contracts)
5. [dbt Testing Framework](#dbt-testing-framework)
6. [Quality Monitoring & Alerting](#quality-monitoring--alerting)

---

## Data Quality Dimensions

| Dimension | Definition | Test | Failure Impact |
|---|---|---|---|
| **Completeness** | Are all expected records present? | `COUNT(*) >= threshold`, null rate < X% | Missing data in reports |
| **Uniqueness** | Are duplicates absent? | Primary key uniqueness | Double-counting revenue |
| **Freshness** | Is data up-to-date? | `MAX(updated_at) >= NOW() - SLA` | Stale dashboards |
| **Accuracy** | Does data reflect reality? | Values within expected range, referential integrity | Wrong business decisions |
| **Consistency** | Is data consistent across systems? | Cross-system reconciliation | Conflicting reports |
| **Validity** | Does data conform to schema/format? | Regex pattern match, enum values | Pipeline failures |
| **Timeliness** | Is data available when needed? | `pipeline_end_time - SLA_trigger_time < SLA` | Delayed decisions |
| **Lineage** | Can we trace data origin? | End-to-end lineage for every field | Untrusted data, debugging hell |

---

## Great Expectations (GX) Framework

### Architecture

```
Data Source → GX Checkpoint → Validation Results → Data Docs (HTML) → Alerting
              │
              ├── Expectation Suite (declarative, version-controlled)
              │   ├── expect_column_values_to_not_be_null
              │   ├── expect_column_values_to_be_unique
              │   ├── expect_column_values_to_be_in_set
              │   ├── expect_column_values_to_be_between
              │   ├── expect_table_row_count_to_be_between
              │   └── expect_column_pair_values_A_to_be_greater_than_B
              │
              └── Checkpoint (binds suite to data source + actions)
```

### Expectation Suite Example

```python
import great_expectations as gx

context = gx.get_context()

# Create expectations for orders table
suite = context.suites.add(
    gx.ExpectationSuite(name="orders_quality_suite")
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id")
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(column="order_id")
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="amount",
        min_value=0.01,
        max_value=1000000.00
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="status",
        value_set=["pending", "confirmed", "shipped", "delivered", "cancelled", "refunded"]
    )
)

suite.add_expectation(
    gx.expectations.ExpectTableRowCountToBeBetween(
        min_value=100,
        max_value=10000000
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        column_A="delivered_at",
        column_B="created_at",
        or_equal=True
    )
)

# Validate
checkpoint = context.checkpoints.add(
    gx.Checkpoint(
        name="orders_checkpoint",
        validations=[
            {
                "batch_request": {
                    "datasource_name": "orders_db",
                    "data_asset_name": "public.orders",
                },
                "expectation_suite_name": "orders_quality_suite",
            }
        ],
    )
)

results = checkpoint.run()
if not results["success"]:
    context.build_data_docs()
    # Send alert: Slack, PagerDuty, email
```

### CI Integration

```yaml
# GitHub Actions — run GX validations on PR
- name: Data Quality Check
  run: |
    great_expectations checkpoint run orders_checkpoint
    if [ $? -ne 0 ]; then
      echo "Data quality checks failed. See Data Docs for details."
      exit 1
    fi
```

---

## WAP Pattern (Write-Audit-Publish)

### The Pattern

```
┌─────────┐     ┌─────────┐     ┌──────────┐
│  WRITE   │────▶│  AUDIT   │────▶│ PUBLISH  │
│          │     │          │     │          │
│ Write to │     │ Run GX/  │     │ Swap/    │
│ staging  │     │ dbt tests│     │ expose   │
│ table    │     │ on staging│    │ to users │
└─────────┘     └─────────┘     └──────────┘
                     │
                     ▼ (audit fails)
                ┌─────────┐
                │  ALERT   │
                │  + ABORT │
                └─────────┘
```

### dbt + WAP Implementation

```sql
-- Step 1: WRITE — built model in staging schema
-- models/marts/fct_daily_revenue.sql
{{ config(materialized='table', schema='staging') }}
SELECT ... FROM ...

-- Step 2: AUDIT — dbt test on staging version
-- tests/assert_revenue_positive.sql
SELECT * FROM {{ ref('fct_daily_revenue', v='staging') }}
WHERE revenue < 0

-- Step 3: PUBLISH — swap schemas if audit passes
-- In post-hook:
ALTER SCHEMA analytics.fct_daily_revenue SWAP WITH staging.fct_daily_revenue;
```

### WAP Pipeline in Airflow

```python
@task
def write_to_staging(**context):
    run_dbt_model('fct_daily_revenue', schema='staging')

@task
def audit_staging(**context):
    results = run_dbt_tests('fct_daily_revenue', schema='staging')
    if not results.success:
        send_alert("Data quality audit failed for fct_daily_revenue")
        raise AirflowException("Audit failed — publication blocked")

@task
def publish_to_production(**context):
    swap_schema('fct_daily_revenue', from_schema='staging', to_schema='analytics')
    log_publication('fct_daily_revenue', version='v2.3.1')

write_to_staging() >> audit_staging() >> publish_to_production()
```

---

## Data Contracts

### Contract Between Producer and Consumer

```yaml
# data_contracts/orders_v2.yaml
data_contract:
  name: orders_v2
  owner: checkout-team
  description: "Order events emitted by Checkout Service"
  schema:
    - field: order_id
      type: string
      nullable: false
      description: "Unique order identifier"
      pattern: "^ord_[a-z0-9]{16}$"
    - field: customer_id
      type: string
      nullable: false
    - field: amount
      type: decimal(10,2)
      nullable: false
      constraints:
        min: 0.01
        max: 1000000.00
    - field: currency
      type: string
      nullable: false
      enum: ["USD", "EUR", "GBP", "JPY"]
    - field: status
      type: string
      nullable: false
      enum: ["pending", "confirmed", "shipped", "delivered", "cancelled", "refunded"]
    - field: created_at
      type: timestamp
      nullable: false

  slo:
    freshness: "5 minutes"
    completeness: "99.9%"
    uniqueness: "order_id"

  change_policy:
    additive_changes: "24h notice"    # Adding optional fields
    breaking_changes: "30 days notice, 2 deprecation warnings"  # Removing/renaming fields
    contact: "#checkout-data-eng"
```

### Contract Enforcement in CI

```yaml
# GitHub Actions — validate data contract on schema changes
- uses: datacontract/cli-action@v1
  with:
    contract: data_contracts/orders_v2.yaml
    server: production
    # Validates: schema compatibility, freshness SLO, completeness SLO
```

### Schema Evolution Rules

```
Add optional field:
  ✅ Backward compatible — consumers ignore unknown fields
  ✅ Forward compatible — producer adds field; consumers can upgrade later
  Notice: 24 hours

Add required field with default:
  ✅ Backward compatible — default fills in for old consumers
  ⚠️ Requires consumer awareness — default may not be semantically correct
  Notice: 7 days

Remove field:
  🚫 Breaking change — consumers expecting field will fail
  Process: Deprecate (mark optional) → 30 days → Remove
  Notice: 30 days, 2 deprecation warnings

Change field type:
  🚫 Breaking change — e.g., string → integer
  Process: Add new field with new type → migration period → remove old field
  Notice: 30 days

Rename field:
  🚫 Breaking change — equivalent to remove old + add new
  Process: Add new field → dual-write for 30 days → remove old field
  Notice: 30 days
```

---

## dbt Testing Framework

### Built-in Tests

```yaml
# models/marts/schema.yml
version: 2

models:
  - name: fct_orders
    description: "Order fact table — one row per order"
    columns:
      - name: order_id
        description: "Primary key"
        tests:
          - unique
          - not_null

      - name: customer_id
        description: "Foreign key to dim_customers"
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id

      - name: amount
        description: "Order total in base currency (USD)"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0.01
              max_value: 1000000.00

      - name: status
        tests:
          - not_null
          - accepted_values:
              values: ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled', 'refunded']
              quote: true
```

### Custom Generic Tests

```sql
-- tests/generic/assert_positive_values.sql
{% test assert_positive_values(model, column_name) %}
SELECT {{ column_name }}
FROM {{ model }}
WHERE {{ column_name }} < 0
{% endtest %}

-- Use it:
# schema.yml
columns:
  - name: amount
    tests:
      - assert_positive_values
```

### Singular Tests (One-Off Assertions)

```sql
-- tests/assert_order_dates_consistent.sql
SELECT order_id
FROM {{ ref('fct_orders') }}
WHERE shipped_at < created_at
   OR delivered_at < shipped_at
-- Returns rows that violate the assertion; test fails if any rows returned
```

### dbt Test Severity

```yaml
# dbt_project.yml
tests:
  +severity: warn  # Default: fail on error

models:
  +severity: error  # Override: fail on all test failures for models

# In schema.yml:
columns:
  - name: amount
    tests:
      - not_null:
          severity: error    # Fail pipeline
      - accepted_range:
          min_value: 0.01
          severity: warn     # Warn but don't fail
```

---

## Quality Monitoring & Alerting

### Freshness Monitoring

```sql
-- dbt source freshness
sources:
  - name: stripe
    freshness:
      warn_after: {count: 4, period: hour}
      error_after: {count: 12, period: hour}
    loaded_at_field: _etl_loaded_at
    tables:
      - name: payments
```

```bash
# Run freshness checks on schedule
dbt source freshness

# Alert if stale
if [ $? -ne 0 ]; then
  curl -X POST https://hooks.slack.com/... \
    -d '{"text": "⚠️ dbt source freshness check FAILED: Stripe payments data is stale"}'
fi
```

### Anomaly Detection on Row Counts

```sql
-- dbt test — row count within 3 standard deviations of 7-day average
{% test row_count_anomaly(model, lookback_days=7, threshold_stddev=3) %}
WITH recent_counts AS (
  SELECT
    DATE(loaded_at) AS load_date,
    COUNT(*) AS row_count
  FROM {{ model }}
  WHERE loaded_at >= CURRENT_DATE - INTERVAL '{{ lookback_days }}' DAY
  GROUP BY 1
),
stats AS (
  SELECT
    AVG(row_count) AS avg_count,
    STDDEV(row_count) AS stddev_count
  FROM recent_counts
)
SELECT
  (SELECT COUNT(*) FROM {{ model }} WHERE DATE(loaded_at) = CURRENT_DATE) AS todays_count,
  avg_count,
  stddev_count
FROM stats
WHERE todays_count < avg_count - ({{ threshold_stddev }} * stddev_count)
   OR todays_count > avg_count + ({{ threshold_stddev }} * stddev_count)
{% endtest %}
```

### Quality Score Dashboard

```
Metric: Data Quality Score = (Passed Tests / Total Tests) × 100

Per table:
  - Completeness: % of required columns with null rate < 1%
  - Uniqueness: % of PK columns passing uniqueness test
  - Freshness: % of tables within freshness SLA
  - Accuracy: % of referential integrity checks passing

Aggregate: Weighted average across all critical tables
Alert: Score drops below 95% → P2 Slack alert
       Score drops below 90% → P1 PagerDuty
```

### Quality Alert Routing

```yaml
# Alert configuration
data_quality_alerts:
  freshness_breach:
    severity: P2
    channel: "#data-alerts"
    message: "Source {source} has not updated in {hours}h"

  uniqueness_failure:
    severity: P1
    channel: "#data-alerts"
    pagerduty: true
    message: "Duplicate primary keys in {table}.{column} — revenue reports may be inflated"

  null_rate_spike:
    severity: P2
    channel: "#data-alerts"
    condition: "null_rate > 2% AND null_rate > (7d_avg * 3)"
    message: "Null rate spike in {table}.{column}: {rate}% vs avg {avg}%"

  referential_integrity_failure:
    severity: P1
    channel: "#data-alerts"
    pagerduty: true
    message: "Orphan records in {table}.{column} — {count} FK values not found in parent"
```

---

## Production Hardening Checklist

- [ ] Data quality dimensions defined per dataset: completeness, uniqueness, freshness, accuracy, consistency
- [ ] Great Expectations suites (or equivalent) version-controlled in Git
- [ ] WAP pattern implemented for critical datasets — audit before publish
- [ ] Data contracts defined for producer-consumer boundaries with change policies
- [ ] dbt tests on every model: unique, not_null, relationships, accepted_values at minimum
- [ ] Source freshness checks running on schedule with alert on breach
- [ ] Row count anomaly detection on all fact tables
- [ ] Quality score dashboard with overall + per-table scores
- [ ] Quality alerts routed to #data-alerts (P2) and PagerDuty (P1)
- [ ] Schema registry (Confluent/AWS Glue) tracking schema versions and compatibility
- [ ] Lineage tracking (dbt docs, DataHub, Marquez) from source to dashboard
- [ ] Runbooks for quality failure remediation: backfill process, schema evolution playbook, PII incident response
