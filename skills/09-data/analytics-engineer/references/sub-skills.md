# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| **dbt Data Modeling** | Building or refactoring data transformation pipelines | dbt (Core or Cloud), dimensional modeling, Kimball star schema, medallion architecture |
| **Metric Layer Design** | Defining company-wide KPIs, single source of truth for "DAU" or "Revenue" | dbt Semantic Layer, Cube, LookML — centralized metric definition with lineage |
| **A/B Test Design & Analysis** | Running experiments to measure product changes | Power analysis, CUPED, SRM checks, sequential testing — Eppo, Statsig, or SQL-based framework |
| **SQL Performance Tuning** | Queries exceeding 30s or consuming excessive warehouse credits | EXPLAIN plans, partitioning/clustering, CTE optimization, warehouse sizing |
| **Self-Service BI Enablement** | Non-technical stakeholders need ad-hoc data access | Looker, Metabase, Lightdash, Superset — governed self-service with certified metrics |
| **Event Tracking Design** | Defining what user actions to capture and how | Tracking plans, Snowplow, Segment, RudderStack — schema validation, identity resolution |
| **Data Storytelling** | Communicating insights to drive decisions | Visualization principles, narrative structure, dashboard architecture, executive summaries |
| **Data Quality & Observability** | Proactive detection of data issues before stakeholders notice | dbt tests, elementary, Great Expectations, Monte Carlo — freshness, volume, schema anomaly checks |
