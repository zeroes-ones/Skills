---
name: data-engineer
description: ETL/ELT pipelines, data architecture (medallion/data mesh/lakehouse), data modeling (star/snowflake/data vault), dbt/Airflow/Spark/Kafka, data quality (Great Expectations/WAP), data governance, streaming (Kafka/Flink), and performance optimization. Triggered by ETL, data warehouse, Spark, Airflow, Kafka, data pipeline, data modeling, data quality, CDC, data mesh.
author: Sandeep Kumar Penchala
---

# Data Engineer

Build robust, scalable, and reliable data pipelines and platforms. This skill covers the full data
engineering lifecycle: architecture design (medallion, data mesh, lake vs warehouse vs lakehouse),
ETL/ELT patterns (batch, micro-batch, streaming, CDC), dimensional modeling (star schema, data vault
2.0, SCD types), pipeline reliability (idempotency, checkpointing, DLQ, backfill), data quality
frameworks (Great Expectations, WAP pattern, data contracts), performance optimization (partitioning,
clustering, materialized views), governance (catalog, lineage, PII, GDPR), and stream processing
(Kafka, Flink, exactly-once semantics).

## When to Use

- Designing end-to-end data pipelines: ingestion → transformation → storage → serving layers
- Building or migrating a data warehouse (Snowflake, BigQuery, Redshift) or lakehouse (Databricks, Delta Lake)
- Architecting the data platform: medallion layers, medallion-to-mesh evolution
- Designing data models: star schema, data vault 2.0, OBT, SCD Type 0-7
- Implementing batch processing with Apache Spark or streaming with Kafka/Flink
- Orchestrating complex DAGs with Apache Airflow, Dagster, or Prefect
- Establishing data quality frameworks: Great Expectations, WAP pattern, data contracts
- Implementing data governance: catalog (DataHub/Amundsen), lineage, PII masking, GDPR right-to-erasure
- Building real-time analytics with Kafka Streams, Flink, or Spark Structured Streaming

## Core Workflow

### Phase 1: Data Architecture Design

1. **Source Inventory** — Catalog every data source:
   - Transactional databases (PostgreSQL, MySQL, MongoDB) → CDC via Debezium
   - SaaS APIs (Stripe, Salesforce, Zendesk) → Fivetran or Airbyte
   - Event streams → Kafka or Kinesis
   - File uploads → S3/GCS with S3 event notifications
   - Third-party data → SFTP, S3 cross-account, vendor APIs

2. **Architecture Pattern Decision**:

   ```
   How many domain teams? How many data sources?
   ├─ < 5 sources, 1 team → Centralized data warehouse
   │   └─ ELT: Fivetran/Airbyte → Snowflake/BigQuery → dbt
   ├─ 5-20 sources, 3-5 domain teams → Data lakehouse with medallion architecture
   │   └─ Bronze (raw S3/GCS) → Silver (Delta/Iceberg) → Gold (warehouse)
   └─ 20+ sources, 5+ autonomous teams → Data mesh
       └─ Federated governance, domain-owned data products
   ```

3. **Medallion Architecture** — The standard layering pattern:

   | Layer | Storage | Write Pattern | PII | Retention |
   |---|---|---|---|---|
   | **Bronze** | Object store (Parquet/Avro) | Append-only | Raw (yes) | 30-90 days |
   | **Silver** | Delta Lake / Iceberg | Merge/Upsert | Masked/Tokenized | 1-3 years |
   | **Gold** | Warehouse or Delta | Overwrite/Incremental | Fully anonymized | Per business need |

4. **Warehouse / Lakehouse Selection**:

   | Platform | Best For | Key Feature |
   |---|---|---|
   | **Snowflake** | SQL-heavy analytics, BI | Compute/storage separation, zero-copy cloning, data sharing |
   | **BigQuery** | Serverless analytics, petabyte scale | Auto-scaling, pay-per-query, BI Engine |
   | **Databricks** | Lakehouse, Spark + SQL + ML | Delta Lake, Unity Catalog, collaborative notebooks |
   | **Redshift** | AWS-native, predictable workloads | RA3 nodes, AQUA acceleration, Spectrum for S3 queries |

5. **Orchestration Selection**:
   - **Airflow**: Complex DAGs, rich ecosystem, 2,000+ providers. Best for enterprise.
   - **Dagster**: Software-defined assets, asset lineage, type safety. Best for observable pipelines.
   - **Prefect**: Dynamic workflows, Pythonic API, easy local dev. Best for developer experience.
   - **dbt Cloud**: SQL transformations only, zero-infra. Best for analytics engineering teams.

### Phase 2: Data Modeling

1. **Modeling Approach Decision**:

   | Pattern | Structure | Best When | Weakness |
   |---|---|---|---|
   | **Star Schema** | Fact + Dimension tables | BI, self-service analytics, predictable queries | Not flexible for ad-hoc exploration |
   | **Data Vault 2.0** | Hub + Link + Satellite | Enterprise DW, audit trail, source system integration | Complex to query (needs views on top) |
   | **One Big Table (OBT)** | Wide denormalized table | Performance-critical, simple dimensional model (3-5 dims) | Explodes with SCD Type 2 history |

2. **Star Schema Design Process**:
   ```
   1. Identify business process → "Order Fulfillment"
   2. Declare grain → "One row per order line item"
   3. Design dimensions → Date, Customer, Product, Warehouse
   4. Design facts → quantity_ordered, unit_price, discount, line_total
   5. Add surrogate keys to all dimensions (never join on natural keys)
   ```

3. **Slowly Changing Dimensions (SCD)** — The complete decision tree:

   | Type | Behavior | Example |
   |---|---|---|
   | **Type 0** | Retain original. Never change. | Date of birth |
   | **Type 1** | Overwrite. No history. | Correcting a typo |
   | **Type 2** | Add new row. Full history. | Customer address over time |
   | **Type 3** | Add column for previous value. | Department: `current_dept` + `previous_dept` |
   | **Type 4** | Separate history table. | High-frequency stock prices |

   **SCD Type 2 with dbt snapshots:**
   ```sql
   {% snapshot customer_snapshot %}
   {{ config(target_schema='silver', unique_key='customer_id', strategy='timestamp', updated_at='updated_at') }}
   SELECT * FROM {{ source('bronze', 'customers') }}
   {% endsnapshot %}
   ```

4. **Partitioning Strategy** — The single biggest performance lever:
   - **Partition column**: Date (most queries filter by date). Medium cardinality (100-10K partitions).
   - **Anti-pattern**: Partitioning by `user_id` or `order_id` (millions of tiny partitions).
   - **Clustering**: High-cardinality filter columns (e.g., `region`, `product_category`).
   - **Iceberg**: Partition evolution without rewriting data.

### Phase 3: Pipeline Implementation

1. **Ingestion Pattern Selection**:

   | Pattern | Latency | Tooling | Best For |
   |---|---|---|---|
   | **Full Load** | Hours-Days | Fivetran, Airbyte | Small datasets, initial loads |
   | **Incremental** | Minutes-Hours | dbt incremental, Airflow | Most batch use cases |
   | **CDC** | Seconds | Debezium + Kafka | Database replication |
   | **Streaming** | Milliseconds-Seconds | Kafka + Flink | Real-time analytics, fraud detection |
   | **Micro-batch** | 1-5 min | Spark Structured Streaming | Near-real-time, late data handling |

2. **dbt Transformation Patterns**:
   ```
   models/
   ├── staging/       # stg_orders.sql — 1:1 with source, rename + type cast
   ├── intermediate/  # int_order_payments.sql — business logic, joins
   └── marts/         # fct_orders.sql — business-facing, single source of truth
   ```

   **Incremental model pattern:**
   ```sql
   {{ config(materialized='incremental', unique_key='order_id', on_schema_change='sync_all_columns') }}
   SELECT * FROM {{ source('raw', 'orders') }}
   {% if is_incremental() %}
   WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
   {% endif %}
   ```

3. **Pipeline Reliability Requirements**:
   - **Idempotency** — Re-running produces same result. Use MERGE/UPSERT, never INSERT INTO without dedup.
   - **Checkpointing** — Resume from last committed offset. Spark: `checkpointLocation`. Flink: savepoints.
   - **Dead Letter Queue** — Bad messages → DLQ topic → alert → manual investigation → replay.
   - **Backfill** — `INSERT OVERWRITE` partitions for historical corrections.

4. **Streaming with Kafka + Flink**:
   ```yaml
   # Kafka topic config
   orders-topic:
     partitions: 12
     replication_factor: 3
     min.insync.replicas: 2
     retention.ms: 604800000  # 7 days

   # Exactly-once semantics:
   # Producer: enable.idempotence=true, acks=all
   # Consumer: manual commit, deduplicate by key
   # Flink: checkpointing + two-phase commit
   ```

5. **Late-Arriving Data Handling**:
   - Watermark = event_time - max_lateness_window (e.g., 5 min)
   - Events older than watermark → side output (not dropped)
   - dbt incremental: 3-day lookback window `WHERE order_date >= '{{ ds }}' - INTERVAL '3 days'`

### Phase 4: Data Quality

1. **Quality Dimensions** — Validate every pipeline output against:

   | Dimension | Test | Example |
   |---|---|---|
   | **Completeness** | Not null, row count bounds | `order_id` never null, row count within 3σ of 7-day avg |
   | **Uniqueness** | Primary key unique | No duplicate `order_id` |
   | **Freshness** | Max timestamp within SLA | `MAX(updated_at) >= NOW() - 1 hour` |
   | **Accuracy** | Values in range, referential integrity | `amount > 0`, FK resolves in `dim_customers` |
   | **Consistency** | Cross-system reconciliation | Row count matches source system |

2. **WAP Pattern (Write-Audit-Publish)** — The gold standard for critical pipelines:
   ```
   Write → Staging table
   Audit → Run dbt tests + GX expectations on staging
   Publish → Swap schemas (atomic) or expose to consumers
   Fail → Alert + abort (consumers never see bad data)
   ```

3. **Data Contracts** — Producer-consumer agreements:
   ```yaml
   data_contract:
     name: orders_v2
     schema:
       - field: order_id | type: string | nullable: false
       - field: amount | type: decimal(10,2) | constraints: {min: 0.01, max: 1000000.00}
     slo:
       freshness: "5 minutes"
       completeness: "99.9%"
     change_policy:
       breaking_changes: "30 days notice, 2 deprecation warnings"
   ```

4. **dbt Testing** — Minimum test coverage per model:
   - `unique` on primary key
   - `not_null` on all required fields
   - `relationships` on all foreign keys
   - `accepted_values` on all enums/status fields
   - Custom: positive amounts, date consistency (`shipped_at > created_at`)

### Phase 5: Governance & Operations

1. **Data Catalog** — Amundsen, DataHub, or Atlan:
   - Every dataset tagged with: owner, domain, sensitivity classification, refresh cadence, SLA
   - Lineage tracked end-to-end: source → Bronze → Silver → Gold → BI dashboard
   - Discovery: business glossary mapping "Monthly Revenue" to `analytics.fct_monthly_revenue.revenue`

2. **Access Control**:
   - Column-level masking: PII columns (`email`, `phone`) → `NULL` or hash for unauthorized roles
   - Row-level security: `WHERE tenant_id = CURRENT_TENANT()` for multi-tenant data
   - Role-based: `analyst_read` (SELECT on Gold), `engineer_write` (Silver bronze only), `admin_all`

3. **GDPR / CCPA Right to Erasure**:
   ```sql
   -- Soft delete: anonymize PII, retain aggregate analytics value
   UPDATE silver.customers
   SET
     email = 'deleted_' || customer_id || '@anonymized.local',
     name = 'Deleted User',
     phone = NULL,
     address = NULL,
     is_deleted = true,
     deleted_at = NOW()
   WHERE customer_id = 'cust_789';

   -- Hard delete: remove from all layers (Bronze → Gold) within 30 days
   -- But retain in encrypted archive for legal hold if required
   ```

4. **Pipeline Monitoring Dashboard**:
   - DAG-level: Status (success/failure/running), last run, next run, duration trend
   - Data-level: Row counts, freshness, null rates, partition sizes
   - Cost-level: Warehouse credits consumed, Spark cluster hours, Kafka storage

## Sub-Skills

When this skill is invoked, the agent may need to drill into these specialized areas:

| Sub-Skill | When to Use |
|-----------|-------------|
| `data-architecture` | Designing data platforms: medallion architecture, data mesh, lake vs warehouse vs lakehouse |
| `etl-pipeline` | Building ingestion and transformation: batch, micro-batch, streaming, and CDC pipelines |
| `schema-design-analytics` | Designing star schemas, snowflake schemas, data vaults, and slowly changing dimensions |
| `data-quality` | Implementing Write-Audit-Publish patterns, data contracts, and Great Expectations validation |
| `pipeline-reliability` | Production hardening: idempotency, checkpointing, dead-letter queues, and backfill strategies |
| `stream-processing` | Real-time data with Kafka: windowing, watermarking, exactly-once semantics, and consumer lag |
| `data-governance` | Cataloging with DataHub/Amundsen, lineage tracking, PII handling, and retention policies |

## Cross-Skill Coordination

Data engineers build the pipelines that feed analytics, ML, and product decisions. They coordinate with backend developers for data production, analytics engineers for transformation, ML engineers for feature stores, and DevOps for pipeline reliability.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Backend Developer** | Event schema design, CDC setup, webhook data sources | Event payload schemas, data freshness expectations, database change capture configuration, API rate limits |
| **Analytics Engineer** | Data model design, dbt transformation handoff | Raw data schemas, freshness SLAs, data dictionary, PII classification per column, partitioning strategy |
| **ML/AI Engineer** | Feature store population, training data pipelines | Feature computation schedules, point-in-time correctness requirements, historical backfill capabilities, embedding storage |
| **DevOps Engineer** | Pipeline infrastructure, Airflow/Dagster deployment | Compute requirements (Spark clusters, K8s pods), secret management for data source connections, monitoring and alerting setup |
| **Observability Engineer** | Pipeline monitoring, data quality alerting | Pipeline metrics (lag, row count, freshness), data quality check results, cost metrics for warehouse/Spark |
| **Security Engineer** | Data access controls, PII handling | Column-level access policies, encryption requirements, data masking for non-production, audit logging for data access |
| **Compliance Officer** | Data retention, right-to-deletion, cross-border transfers | Retention policy implementation, DSAR automation (data subject access), data residency enforcement, GDPR Article 30 records |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| Source schema change (new/removed column, type change) | Analytics Engineer, ML Engineer | Update downstream models; prevent pipeline breakage |
| Pipeline failure (data not delivered within SLA) | Analytics Engineer, ML Engineer, Observability | SLA breach; downstream dashboards/training jobs stale |
| PII discovered in non-PII-designated column | Security Engineer, Compliance Officer | Data classification update; access control review; potential breach assessment |
| Data quality check failure (null rate spike, row count anomaly) | Backend Developer (if source issue), Analytics Engineer | Root cause: source data bug or pipeline regression? |
| Major backfill required (>7 days of historical data) | Analytics Engineer, ML Engineer, DevOps | Compute cost estimate; coordination on backfill window |

### Escalation Path

```
Data pipeline down (production)? → DevOps Engineer → Incident Responder (if SEV2+)
PII exposure in data pipeline? → Security Engineer → Compliance Officer
Cross-team schema conflict? → System Architect → Data governance council
Pipeline cost overrun? → Cloud Architect (FinOps) → CTO Advisor
```

## Best Practices

- **Idempotency first** — Every pipeline must produce identical output on re-run. Use MERGE, never bare INSERT.
- **ELT over ETL** — Load raw data first, transform in the warehouse. Raw data enables reprocessing and auditing.
- **Push compute to the warehouse** — Don't run Spark for aggregations that Snowflake/BigQuery can do 10x faster with 1/10th the code.
- **Test data, not just code** — Transformation unit tests (does the SQL produce the right shape?) + data quality tests (is the actual data in the right state?).
- **Schema evolution is inevitable** — Expect schemas to change. Use schema registries (Confluent, AWS Glue), Iceberg schema evolution, dbt `on_schema_change='sync_all_columns'`.
- **Small files kill performance** — Compact regularly: Delta `OPTIMIZE`, Iceberg `rewrite_data_files`, Spark `coalesce()`.
- **Partition before you cluster** — Partition pruning eliminates 99% of data before query execution. Cluster on high-cardinality columns within partitions.
- **Track lineage obsessively** — When a dashboard shows wrong numbers, you need to trace back through Gold → Silver → Bronze → Source in seconds, not hours.

## Production Checklist

### Architecture
- [ ] Data architecture documented: medallion layers (or mesh domains), storage, compute, and orchestration
- [ ] Medallion layers: Bronze (raw, append-only), Silver (cleansed, merge-capable), Gold (aggregated, BI-ready)
- [ ] Partitioning and clustering strategy defined for all large tables (> 1GB)
- [ ] Small file compaction scheduled (weekly minimum)

### Data Modeling
- [ ] Data model designed: star schema, data vault, or OBT — documented with ER diagrams
- [ ] Surrogate keys on all dimensions; natural keys used only for business lookup
- [ ] SCD strategy defined per dimension (most will be Type 2 via dbt snapshots)
- [ ] Data dictionary: every column documented (business meaning, type, constraints, source)

### Pipelines
- [ ] All pipelines are idempotent — safe to re-run without data duplication
- [ ] Merge/upsert strategy defined for every ingestion pipeline
- [ ] Dead letter queues with replay mechanism for streaming pipelines
- [ ] Checkpointing enabled for stateful stream processors
- [ ] Backfill process documented and tested
- [ ] Late-arriving data window defined and handled (not silently dropped)

### Data Quality
- [ ] dbt tests on every model: unique, not_null, relationships, accepted_values
- [ ] Custom data quality checks: positive amounts, date consistency, row count anomaly
- [ ] WAP pattern for critical datasets — audit before publish
- [ ] Source freshness checks running on schedule with alert on breach
- [ ] Quality score dashboard with per-table and aggregate scores

### Governance
- [ ] Data catalog deployed: DataHub, Amundsen, or Atlan
- [ ] Lineage tracked from source to dashboard
- [ ] PII identified, classified, and masked/anonymized in Silver and Gold
- [ ] Row-level security and column-level masking enforced
- [ ] GDPR/CCPA deletion process defined and tested
- [ ] Retention policies: auto-delete Bronze after N days, archive cold data

### Operations
- [ ] Pipeline monitoring dashboard: DAG health, data freshness, row count trends
- [ ] Alerting on: pipeline failure, freshness breach, quality test failure, row count anomaly
- [ ] Runbooks for top 5 pipeline failure modes with documented remediation
- [ ] Cost monitoring: warehouse credits, Spark cluster hours, Kafka storage
- [ ] DR: Cross-region backups for data warehouse, Kafka mirroring, schema versioning in Git

## References

- [Data Architecture Patterns — Production Field Manual](references/data-architecture-patterns.md) — Medallion, data mesh, lake vs warehouse, schema design, SCD, partitioning
- [ETL/ELT Pipeline Cookbook](references/etl-pipeline-cookbook.md) — Ingestion patterns, Kafka, CDC, Airflow/Dagster, idempotency, backfill
- [Data Quality Framework](references/data-quality-framework.md) — Great Expectations, WAP pattern, data contracts, dbt testing, quality monitoring
- dbt Best Practices: https://docs.getdbt.com/best-practices
- Apache Airflow Best Practices: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html
- Snowflake Data Engineering: https://docs.snowflake.com/en/user-guide/data-engineering
- Kafka: The Definitive Guide: https://www.confluent.io/resources/kafka-the-definitive-guide/
- Spark Performance Tuning: https://spark.apache.org/docs/latest/sql-performance-tuning.html
