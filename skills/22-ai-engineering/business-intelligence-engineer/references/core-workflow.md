## Core Workflow

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
| Lightdash |

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.
