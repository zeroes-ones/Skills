# Analytics Setup

## Data Marts (Gold Layer)

Four dbt models in the `marts/` directory serve as the single source of truth for all dashboards:

**product_metrics**: Daily aggregates — active services (count by org, by type), template executions (count, success rate, avg duration), plugin installs, feature adoption (% of orgs using each plugin). Key metric: **Activation Rate** — % of signups that execute their first template within 7 days (currently 68%).

**team_metrics**: Per-team activity — services per team, deployment frequency, incident count, MTTR (Mean Time to Resolution aggregated from PagerDuty), on-call load (alerts per engineer per week). Enables team-level productivity dashboards for engineering managers.

**billing_metrics**: Stripe-derived — MRR (Monthly Recurring Revenue, currently $42,300), churn rate (monthly, by plan tier), expansion revenue, trial conversion rate (14-day trial → paid, currently 23%). Includes invoice-level detail for finance reconciliation.

**growth_metrics**: Acquisition funnel — website visitors → signups → organization created → first template execution → 3+ executions in 7 days → paid conversion. Tracks source attribution (organic, paid, referral, DevRel events).

## Metric Definitions (Standardized)

| Metric | Definition | Calculation | Refresh |
|--------|-----------|-------------|---------|
| DAU | Daily Active Users | Distinct `user_id` with any Rudderstack event in 24h UTC | Daily |
| Activation | User executed first template | `COUNT(DISTINCT user_id) WHERE first template_execution event` | Daily |
| Engaged User | 3+ template executions in 7 rolling days | Rolling window count ≥ 3 | Daily |
| Service Health Score | % of services with status "healthy" | `healthy_count / total_services * 100` | Hourly |
| Time-to-First-Deployment | Signup → template execution | `MIN(template_execution.timestamp) - user.created_at` | Daily |

All definitions published in `docs/metrics.md` as the organizational data dictionary.

## Metabase Dashboards

Metabase deployed on EKS (internal-only, VPN access), connected to Snowflake via a read-only service account.

**Product Overview Dashboard** (audience: product team, leadership): DAU trend (30-day line chart), template executions by type (stacked bar), plugin installs by plugin (horizontal bar), activation funnel (cohort table), feature adoption matrix. Updated every 4 hours.

**Executive Dashboard** (audience: CEO, CTO, board): MRR trend + forecast, logo churn, NPS (quarterly survey, current score: 42), team-level deployment frequency, top-line error rate. One-page view designed for weekly leadership review. Updated daily.

**Engineering Dashboard** (audience: engineering managers): Deployment frequency per service (DORA metric), change failure rate (template execution failures / total executions), p95 API latency (per endpoint), incident count and MTTR. Pulls from product_metrics and team_metrics marts. Updated hourly.

## Access Control

Metabase permissions synced with Google Workspace groups: `engineering@orchestra.dev` (all dashboards), `product@orchestra.dev` (product + growth), `exec@orchestra.dev` (executive dashboard only), `finance@orchestra.dev` (billing metrics only). Row-level security implemented in dbt models via the `org_id` filter clause — each query includes `WHERE org_id = {{ current_org() }}` except for aggregate-only marts.
