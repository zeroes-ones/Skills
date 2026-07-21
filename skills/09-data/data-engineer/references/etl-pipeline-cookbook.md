# ETL/ELT Pipeline Cookbook — Production Field Manual

## Table of Contents
1. [Ingestion Pattern Decision Tree](#ingestion-pattern-decision-tree)
2. [Batch ETL/ELT Patterns](#batch-etelet-patterns)
3. [Stream Processing Patterns](#stream-processing-patterns)
4. [CDC (Change Data Capture)](#cdc-change-data-capture)
5. [Orchestration Framework Selection](#orchestration-framework-selection)
6. [Pipeline Reliability Patterns](#pipeline-reliability-patterns)
7. [Backfill & Late-Arriving Data](#backfill--late-arriving-data)

---

## Ingestion Pattern Decision Tree

```
Data freshness requirement?
├─ Real-time (seconds) → Streaming
│   ├─ High throughput (>10K msg/s) → Kafka + Flink or Spark Streaming
│   ├─ Moderate throughput → Kafka + Kafka Streams or Kinesis + Lambda
│   └─ Change Data Capture from DB → Debezium + Kafka
│
├─ Near real-time (minutes) → Micro-batch
│   ├─ Spark Structured Streaming (trigger every 1-5 min)
│   ├─ Airflow with short schedule_interval (every 5 min)
│   └─ dbt Cloud job triggered on source freshness
│
└─ Batch (hours/days) → ETL/ELT
    ├─ Simple, low-volume → Fivetran, Airbyte, Stitch (managed connectors)
    ├─ Complex transformations → dbt + Airflow orchestration
    └─ Petabyte-scale → Spark on EMR/Dataproc/Databricks
```

---

## Batch ETL/ELT Patterns

### ELT (Extract, Load, Transform) — The Modern Standard

```
Extract: SaaS API → Fivetran/Airbyte → Raw data in warehouse (Snowflake/BigQuery)
Load:    Raw tables in staging schema
Transform: dbt models → Staging → Intermediate → Marts

Why ELT?
1. Push compute to the warehouse (scalable, cost-effective)
2. Raw data preserved for reprocessing
3. Transformations are SQL — accessible to analysts
4. dbt provides testing, documentation, lineage
```

### dbt Project Structure

```
my_dbt_project/
├── models/
│   ├── staging/           # 1:1 with source tables
│   │   ├── stg_payments.sql
│   │   └── stg_orders.sql
│   ├── intermediate/      # Joins, aggregations, reusable
│   │   └── int_order_payments.sql
│   └── marts/             # Business-facing
│       ├── finance/
│       │   └── fct_daily_revenue.sql
│       └── marketing/
│           └── fct_campaign_performance.sql
├── tests/                 # Custom data tests
│   └── assert_positive_amounts.sql
├── macros/                # Reusable Jinja macros
│   └── generate_schema_name.sql
├── seeds/                 # Static CSV reference data
│   └── country_codes.csv
├── snapshots/             # SCD Type 2 tracking
│   └── customer_history.sql
└── dbt_project.yml
```

### Incremental Models in dbt

```sql
{{
    config(
        materialized='incremental',
        unique_key='order_id',
        partition_by={'field': 'order_date', 'data_type': 'date'},
        on_schema_change='sync_all_columns'  # Add new columns automatically
    )
}}

SELECT
    order_id,
    customer_id,
    order_date,
    amount,
    status,
    updated_at
FROM {{ source('raw', 'orders') }}

{% if is_incremental() %}
WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}
```

### ETL Pattern — When to Transform Before Loading

```
Use ETL (not ELT) when:
1. PII must be masked/anonymized before it hits the warehouse
2. Data volume reduction is critical (summarize at edge before loading)
3. Compliance requires data to never touch cloud storage raw
4. Multi-source joins are needed pre-warehouse (legacy systems)

Typical ETL stack: Spark on EMR → processed data → S3 → COPY into Snowflake
```

---

## Stream Processing Patterns

### Kafka Architecture — Production Configuration

```yaml
# Topic configuration
orders-topic:
  partitions: 12            # Based on throughput: target < 10MB/s per partition
  replication_factor: 3     # HA: tolerate 2 broker failures
  retention.ms: 604800000   # 7 days (standard)
  retention.bytes: 107374182400  # 100GB per partition (safety cap)
  cleanup.policy: delete    # Or compact for changelog topics
  min.insync.replicas: 2   # Durability: acks=all requires 2 ISRs

# Producer configuration
acks: all                   # Wait for all in-sync replicas
enable.idempotence: true    # Exactly-once semantics
compression.type: snappy    # Balance CPU vs compression ratio
linger.ms: 5                # Batch more messages before sending
batch.size: 16384           # 16KB batches

# Consumer configuration
enable.auto.commit: false   # Manual offset commit (exactly-once)
isolation.level: read_committed  # Only read committed transactions
max.poll.records: 500       # Control batch size
```

### Exactly-Once Semantics

```
Level 0: At-most-once — Fire and forget; messages may be lost (not recommended)
Level 1: At-least-once — Retry on failure; duplicates possible (most common)
Level 2: Exactly-once (idempotent producer) — Kafka deduplicates within session
Level 3: Exactly-once (transactions) — Atomic writes across multiple topics
Level 4: End-to-end exactly-once — Idempotent consumer writes + deduplication

For end-to-end exactly-once:
1. Kafka: enable.idempotence=true, transactional.id set, acks=all
2. Consumer: deduplicate by message key + timestamp in sink
3. Sink: upsert/merge (not append) using unique key
4. Flink: checkpointing + two-phase commit
```

### Windowing in Stream Processing

| Window Type | Description | Use Case |
|---|---|---|
| **Tumbling** | Fixed-size, non-overlapping | "Revenue per hour" |
| **Sliding** | Fixed-size, overlapping | "Moving average of last 5 minutes, every 1 minute" |
| **Session** | Dynamic, gap-based | "User session (30 min inactivity gap)" |
| **Global** | Single window per key | "Total lifetime customer value" |

```sql
-- Flink SQL — tumbling window
SELECT
  TUMBLE_START(order_time, INTERVAL '1' HOUR) AS window_start,
  COUNT(*) AS order_count,
  SUM(amount) AS revenue
FROM orders
GROUP BY TUMBLE(order_time, INTERVAL '1' HOUR);

-- Session window (30 min gap)
SELECT
  SESSION_START(event_time, INTERVAL '30' MINUTE) AS session_start,
  user_id,
  COUNT(*) AS events
FROM user_events
GROUP BY user_id, SESSION(event_time, INTERVAL '30' MINUTE);
```

### Watermarking — Handling Late Data

```sql
-- Flink SQL — watermark on event_time, allow 5 min lateness
CREATE TABLE orders (
  order_id STRING,
  amount DECIMAL,
  event_time TIMESTAMP(3),
  WATERMARK FOR event_time AS event_time - INTERVAL '5' MINUTE
) WITH (
  'connector' = 'kafka',
  ...
);

-- Events older than watermark are dropped (or sent to side output)
```

---

## CDC (Change Data Capture)

### Debezium Architecture

```
PostgreSQL → Debezium Connector (Kafka Connect) → Kafka Topic → Consumer (Sink)
              │                                       │
              │  Reads WAL (Write-Ahead Log)          │  Schema Registry (Avro)
              │  Captures: INSERT, UPDATE, DELETE     │
```

### Debezium Configuration

```json
{
  "name": "postgres-orders-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres-prod",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "${SECRET:debezium-db-password}",
    "database.dbname": "orders_db",
    "database.server.name": "orders_pg",
    "table.include.list": "public.orders,public.order_items",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_orders",
    "publication.autocreate.mode": "filtered",
    "key.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "transforms.unwrap.drop.tombstones": false
  }
}
```

### CDC Message Format (Debezium)

```json
{
  "before": null,
  "after": {
    "order_id": "ord_123",
    "customer_id": "cust_456",
    "amount": 99.99,
    "status": "completed",
    "updated_at": "2026-07-21T14:32:00Z"
  },
  "source": {
    "version": "2.7.0.Final",
    "connector": "postgresql",
    "name": "orders_pg",
    "ts_ms": 1750427520000,
    "snapshot": "false",
    "db": "orders_db",
    "schema": "public",
    "table": "orders",
    "txId": 589234,
    "lsn": 237892340
  },
  "op": "c",  // c=create, u=update, d=delete, r=read (snapshot)
  "ts_ms": 1750427521000
}
```

### SCD Type 2 from CDC

```sql
-- dbt snapshot using CDC stream as source
{%
    config(
        target_schema='silver',
        unique_key='order_id',
        strategy='timestamp',
        updated_at='updated_at',
    )
%}
SELECT 
  after.order_id AS order_id,
  after.customer_id AS customer_id,
  after.amount AS amount,
  after.status AS status,
  after.updated_at AS updated_at
FROM {{ source('cdc', 'orders_cdc') }}
WHERE op != 'd'  -- Exclude deletes (or handle tombstone records)
```

---

## Orchestration Framework Selection

| Framework | Best For | Key Strength | Weakness |
|---|---|---|---|
| **Apache Airflow** | Complex DAGs, rich ecosystem, mature | 2000+ providers, extensible, battle-tested | Requires dedicated infra, steep learning curve |
| **Dagster** | Software-defined assets, observability | Asset lineage, type-safe, I/O management | Smaller ecosystem, newer |
| **Prefect** | Dynamic workflows, Pythonic | Dynamic DAG generation, easy local dev | Less mature than Airflow |
| **dbt Cloud** | SQL transformations only | Zero-infra, managed, CI/CD built-in | SQL-only, limited non-warehouse tasks |
| **Argo Workflows** | Kubernetes-native, containerized | Each step is a container, YAML-defined | Heavy for small teams, K8s required |

### Airflow DAG — Production Pattern

```python
from airflow.decorators import dag, task
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime, timedelta

@dag(
    dag_id='orders_pipeline',
    schedule='@hourly',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    default_args={
        'owner': 'data-engineering',
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
        'email_on_failure': True,
        'email': ['data-alerts@company.com'],
    },
    tags=['production', 'orders'],
)
def orders_pipeline():

    @task.sensor(poke_interval=60, timeout=3600)
    def wait_for_source() -> bool:
        """Check if upstream data is ready."""
        return check_s3_prefix_exists('s3://raw/orders/dt={{ ds }}')

    extract = SnowflakeOperator(
        task_id='extract_orders',
        sql='sql/extract_orders.sql',
    )

    @task
    def validate_row_counts(**context):
        source_count = get_s3_object_count(...)
        target_count = get_snowflake_row_count(...)
        if source_count != target_count:
            raise ValueError(f"Row count mismatch: {source_count} vs {target_count}")

    transform = SnowflakeOperator(
        task_id='transform_orders',
        sql='dbt run --select marts.orders+',
    )

    test = SnowflakeOperator(
        task_id='test_orders',
        sql='dbt test --select marts.orders+',
    )

    wait_for_source() >> extract >> validate_row_counts() >> transform >> test

orders_pipeline()
```

---

## Pipeline Reliability Patterns

### Idempotency — The Cardinal Rule

```
Pipeline must produce same result whether run once or N times.

✅ Patterns:
1. INSERT OVERWRITE — Replace entire partition (atomic, idempotent)
2. MERGE/UPSERT — Update existing, insert new (deduplication by key)
3. DELETE + INSERT in transaction — Delete old, insert new atomically

❌ Anti-patterns:
1. INSERT INTO without deduplication key
2. CREATE TABLE AS SELECT without DROP IF EXISTS
3. Append-only without downstream deduplication
```

```sql
-- ✅ MERGE pattern (idempotent)
MERGE INTO silver.orders AS target
USING (
  SELECT * FROM bronze.orders_raw
  WHERE dt = '{{ ds }}'
) AS source
ON target.order_id = source.order_id
WHEN MATCHED AND source.updated_at > target.updated_at THEN
  UPDATE SET amount = source.amount, status = source.status, updated_at = source.updated_at
WHEN NOT MATCHED THEN
  INSERT (order_id, customer_id, amount, status, updated_at, dt)
  VALUES (source.order_id, source.customer_id, source.amount, source.status, source.updated_at, source.dt);
```

### Dead Letter Queue Pattern

```
Normal flow:
  Kafka → Stream Processor → Sink (warehouse)

Error flow:
  Kafka → Stream Processor → DLQ Topic (bad messages) → Alert → Manual investigation → Replay

DLQ message:
{
  "original_message": {...},
  "error": "JSON parse error: unexpected character at line 14",
  "error_timestamp": "2026-07-21T14:32:00Z",
  "retry_count": 3,
  "source_topic": "orders-v1",
  "source_partition": 4,
  "source_offset": 123456
}
```

### Checkpointing — Resume from Failure

```python
# Spark Structured Streaming — checkpoint directory
df.writeStream \
  .format("delta") \
  .option("checkpointLocation", "s3://checkpoints/orders_pipeline/") \
  .outputMode("append") \
  .trigger(processingTime="1 minute") \
  .start("s3://silver/orders/")

# On restart: Spark reads checkpoint, resumes from last committed offset
```

---

## Backfill & Late-Arriving Data

### Backfill Strategies

| Scenario | Strategy | Example |
|---|---|---|
| New column added | Backfill historical partitions | `INSERT OVERWRITE gold.fct_orders PARTITION (dt) SELECT ..., new_column FROM ...` |
| Bug fix in transformation | Truncate + re-run from Silver | `TRUNCATE TABLE gold.fct_orders; dbt run --full-refresh --select fct_orders` |
| Missing historical data | Parallel backfill by date range | Airflow backfill: `airflow dags backfill -s 2025-01-01 -e 2026-01-01 orders_pipeline` |
| Source data corrected | Merge corrections into Silver, propagate to Gold | `MERGE INTO silver.orders ... WHERE updated_at > last_run` |

### Airflow Backfill Command

```bash
# Backfill all dates from Jan 1 to Jun 30, 2026
airflow dags backfill \
  --start-date 2026-01-01 \
  --end-date 2026-06-30 \
  --reset-dagruns \
  --rerun-failed-tasks \
  orders_pipeline

# ⚠️ Always test on a dev environment first
# ⚠️ Set max_active_runs=1 to avoid overwhelming downstream
```

### Late-Arriving Data Window

```python
# Flink — define allowed lateness for window
stream
  .keyBy(_.orderId)
  .window(TumblingEventTimeWindows.of(Time.hours(1)))
  .allowedLateness(Time.minutes(30))  # Accept data up to 30 min late
  .sideOutputLateData(lateOutputTag)   # Route later data to side output
  .aggregate(...)

# dbt — handle late data in incremental models
SELECT * FROM source
WHERE order_date >= '{{ ds }}' - INTERVAL '3 days'  # 3-day lookback
  AND updated_at > (SELECT MAX(updated_at) FROM {{ this }})
```

---

## Production Hardening Checklist

- [ ] All pipelines are idempotent — safe to re-run without data duplication
- [ ] Merge/upsert strategy defined for every ingestion pipeline
- [ ] Dead letter queues configured for streaming pipelines with replay mechanism
- [ ] Checkpointing enabled for stateful stream processors
- [ ] Schema registry in use for all Kafka topics; schema evolution with compatibility rules
- [ ] Backfill process documented and tested for each pipeline
- [ ] Late-arriving data window defined and handled (not silently dropped)
- [ ] Pipeline alerting: freshness check (data hasn't arrived by SLA), row count anomaly, null rate spike
- [ ] Runbooks exist for top 5 pipeline failure modes
- [ ] Cost monitoring: warehouse credits, Spark cluster hours, Kafka storage
