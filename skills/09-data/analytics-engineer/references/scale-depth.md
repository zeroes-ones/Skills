# Scale Depth

<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
One analyst/analytics engineer running dbt on a free tier warehouse (BigQuery sandbox, Snowflake trial). No orchestration; dbt Cloud free tier schedules. BI tool: Metabase open-source or Looker Studio free. Manual data quality checks. Metrics in dbt marts; no semantic layer needed. No A/B testing infrastructure beyond SQL queries in notebooks. Cost: $0-200/month. Overkill: data catalog, semantic layer, Airbyte/Fivetran, CI/CD, staging environments.

### Small (2-10 people, 100-10K users)
Dedicated analytics engineer. dbt Cloud team plan or self-hosted with Airflow. BI: Looker/Metabase with shared dashboards. Start A/B testing framework (SQL + statistical functions). Data quality: dbt tests + elementary for anomaly detection. Metric governance with dbt docs. CI/CD: lint + test on PRs. Cost: $500-3K/month. Overkill: full semantic layer, feature store, real-time dashboards.

### Medium (10-50 people, 10K-1M users)
Analytics engineering team (2-3). Semantic layer (dbt Semantic Layer or Cube) for centralized metric governance. Multi-environment: dev/staging/prod with CI/CD. Data catalog (DataHub/Amundsen). Automated A/B testing with SRM checks, CUPED, sequential testing (Eppo/Statsig integration). Certified metrics with lineage tracking. Embedded analytics for product. Cost: $5K-20K/month. Overkill: data mesh (stay centralized unless domain count > 10).

### Enterprise (50+ people, 1M+ users)
Distributed analytics engineering pods aligned to domains. Federated semantic layer with global metric registry. Real-time operational dashboards. Automated metric anomaly detection with Slack/PagerDuty integration. Data product lifecycle management: beta → GA → deprecated. Cross-domain metric consistency enforcement. Multi-region BI deployment. FinOps: warehouse cost attribution to domains. Cost: $30K-200K+/month.

### Transition Triggers
| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | 3+ BI consumers across different teams | Set up dbt Cloud team plan; formalize metric taxonomy; introduce CI/CD |
| Small → Medium | Metric disagreement across teams; >20 dashboards | Implement semantic layer (dbt SL/Cube); add data catalog; build A/B testing framework |
| Medium → Enterprise | 10+ domain teams needing self-service analytics | Adopt federated semantic layer; implement data product lifecycle; cross-domain governance |
