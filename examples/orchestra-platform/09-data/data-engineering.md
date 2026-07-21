# Data Engineering

## Data Pipeline Architecture

The Orchestra platform generates operational and product telemetry that flows through a three-stage pipeline: ingestion (Airbyte), transformation (dbt), and serving (Snowflake). Event sources include PostgreSQL (application data), Rudderstack (user behavior events), and PagerDuty (incident data).

## Airbyte — Ingestion Layer

Airbyte Open Source deployed on EKS with a dedicated `t3.xlarge` node. Four connectors configured:

- **PostgreSQL → Snowflake**: Full CDC replication of 7 application tables (services, service_versions, templates, template_executions, plugins, plugin_configs, organizations) via logical replication. Sync interval: 5 minutes.
- **Rudderstack → Snowflake**: Event stream loaded every 15 minutes. Events include: `page_view`, `template_execution`, `plugin_install`, `feature_flag_exposure`, and `user_invitation`.
- **PagerDuty → Snowflake**: Incident and on-call schedule data synced hourly for reliability metrics.
- **Stripe → Snowflake**: Billing events (invoice created, payment succeeded, subscription changed) synced daily.

## dbt — Transformation Layer (18 Models)

dbt Core 1.8 with dbt-snowflake adapter. Models organized in a medallion architecture:

**Bronze (6 staging models)**: Raw data, minimal transformation. `stg_postgres__services`, `stg_postgres__template_executions`, `stg_rudderstack__events`, `stg_rudderstack__page_views`, `stg_pagerduty__incidents`, `stg_stripe__invoices`. These models add column aliases, cast types, and filter to relevant date ranges. Materialized as views for freshness.

**Silver (8 intermediate models)**: Cleaned, deduplicated, and joined. `int_services_enriched` joins services with owners and versions. `int_daily_template_metrics` aggregates template executions per day per organization. `int_user_activity_daily` deduplicates Rudderstack events and joins with organization metadata. Materialized as incremental tables with a 7-day lookback window.

**Gold (4 marts)**: Business-ready aggregates. See analytics documentation for mart definitions.

## Event Tracking — Rudderstack

Rudderstack JavaScript SDK v3 integrated into the Next.js app via a custom `AnalyticsProvider`. All events follow a standardized schema: `{ event, userId, orgId, properties: { ... }, context: { page, referrer, timestamp } }`. The `identify()` call fires on login and links the anonymous session to the authenticated user. Feature flag exposure events (`feature_flag_exposed`) are tracked to enable A/B test analysis. Rudderstack configured to route events to Snowflake (warehouse destination) and Amplitude (product analytics, planned Q4 2026).

## Data Quality — Great Expectations

12 expectations configured as a CI gate in the dbt pipeline:

- `expect_table_row_count_to_be_between` on `stg_rudderstack__events` (min: 1,000/day, alerts if event pipeline drops)
- `expect_column_values_to_not_be_null` on `service_id`, `org_id`, `template_id` across all staging models
- `expect_column_values_to_be_in_set` on `service_type` (must be one of: api, web, cron, pipeline, plugin)
- `expect_column_unique` on UUID primary key columns
- `expect_column_values_to_match_regex` on `version` (semver format validation)

Validation suite runs in CI after `dbt build`. Any failed expectation blocks the PR from merging. All 12 expectations currently passing with 100% success rate over the last 30 days.
