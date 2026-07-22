# Data Architecture Patterns — Production Field Manual

## Table of Contents
1. [Medallion Architecture](#medallion-architecture)
2. [Data Mesh Principles](#data-mesh-principles)
3. [Lake vs Warehouse vs Lakehouse](#lake-vs-warehouse-vs-lakehouse)
4. [Schema Design Patterns](#schema-design-patterns)
5. [Slowly Changing Dimensions (SCD)](#slowly-changing-dimensions-scd)
6. [Partitioning & Clustering Strategy](#partitioning--clustering-strategy)

---

## Medallion Architecture

### The Three Layers

```
┌──────────────────────────────────────────────────────────────┐
│  BRONZE (Raw)                                                 │
│  ─────────────────                                            │
│  Source data ingested as-is, no transformation.               │
│  Format: Parquet, Avro, JSON (append-only)                    │
│  Purpose: Full fidelity, time travel, reprocessing            │
│  Retention: 30-90 days                                        │
├──────────────────────────────────────────────────────────────┤
│  SILVER (Cleansed)                                            │
│  ─────────────────                                            │
│  Deduplicated, validated, typed, joined.                      │
│  Format: Delta Lake / Parquet (merge-capable)                 │
│  Purpose: Single source of truth, self-serve analytics        │
│  Retention: 1-3 years                                         │
├──────────────────────────────────────────────────────────────┤
│  GOLD (Aggregated)                                            │
│  ─────────────────                                            │
│  Business-level aggregates, denormalized, ready for BI.       │
│  Format: Star schema / OBT, optimized for query               │
│  Purpose: Dashboards, ML features, reports                    │
│  Retention: As defined by business requirements               │
└──────────────────────────────────────────────────────────────┘
```

### Layer Design Rules

| Layer | Write Pattern | Read Pattern | PII Allowed? | Schema Enforcement |
|---|---|---|---|---|
| Bronze | Append-only | Ad-hoc debugging, reprocessing | Yes (raw) | None — schema on read |
| Silver | Merge/Upsert | Data analysts, data scientists | Masked/Tokenized | Schema on write — validated |
| Gold | Overwrite/Incremental | BI tools, dashboards, ML | No — fully anonymized | Strict — enforced by dbt tests |

### Bronze → Silver Transformation Checklist

```
- [ ] Deduplicate: remove duplicate rows by business key + timestamp
- [ ] Type casting: string → date, int → decimal, null → default
- [ ] Validation: required fields not null, enums within range, referential integrity
- [ ] Enrichment: join with reference data (currency conversion, geo lookup)
- [ ] PII handling: tokenize/hash/anonymize before Silver (GDPR/CCPA)
- [ ] Schema drift handling: add new columns, don't drop old ones
```

---

## Data Mesh Principles

### Four Principles

| Principle | Description | Implementation |
|---|---|---|
| **Domain Ownership** | Each domain owns its data end-to-end | Domain teams build + operate their data products |
| **Data as a Product** | Data is discoverable, addressable, trustworthy, self-describing | Data product = datasets + metadata + SLOs + ownership |
| **Self-Serve Platform** | Domain-agnostic infrastructure for building data products | Central platform: storage, catalog, orchestration, governance |
| **Federated Governance** | Global standards + local autonomy | Global: PII rules, retention. Local: schema, refresh cadence |

### Data Product Anatomy

```yaml
data_product:
  name: customer_orders
  domain: checkout
  owner: checkout-team@company.com
  description: "Enriched order data with customer and payment details"
  output_ports:
    - name: order_facts
      format: parquet
      schema_version: v2.1
      refresh_cadence: 5min
      slo:
        freshness: "5 minutes"
        completeness: "99.9%"
        correctness: "order_amount >= 0"
  input_ports:
    - name: raw_orders
      source: checkout_kafka_topic
    - name: customer_master
      source: crm.customer_data_product
  lineage: https://datahub.company.com/lineage/customer_orders
```

### When to Adopt Data Mesh

```
Team structure?
├─ Multiple autonomous product/domain teams → Data Mesh adds value
│   ├─ Already doing microservices? → Data Mesh aligns organizationally
│   └─ Planning to scale to 20+ data sources → Start with federated governance
└─ Single data team, < 10 data sources → Stick with centralized data platform
    └─ Revisit when organizational complexity grows
```

---

## Lake vs Warehouse vs Lakehouse

| Dimension | Data Lake | Data Warehouse | Data Lakehouse |
|---|---|---|---|
| **Storage** | Object store (S3, GCS, ADLS) | Proprietary (Snowflake, BigQuery, Redshift) | Object store + open table formats |
| **Data types** | Unstructured, semi-structured, structured | Structured + semi-structured (JSON variant) | All types |
| **Schema** | Schema-on-read | Schema-on-write | Schema-on-write (with evolution) |
| **ACID transactions** | No (filesystem semantics) | Yes (SQL transactions) | Yes (Delta Lake, Iceberg, Hudi) |
| **BI/analytics** | Via compute engine (Spark, Presto) | Native SQL engine | Native SQL via engine (Spark, Trino) |
| **ML/AI** | Good (direct file access) | Limited (SQL-only access) | Excellent (file + SQL access) |
| **Cost** | Low storage, variable compute | Higher storage, variable compute | Low storage, variable compute |
| **Performance** | Depends on engine + format | Highly optimized, proprietary | Highly optimized, open formats |
| **Best when** | Data science, raw data archival | Traditional BI, SQL-heavy analytics | End-to-end: BI + ML + streaming |

### Open Table Formats

| Format | Key Feature | Best For |
|---|---|---|
| **Delta Lake** | ACID transactions, time travel, schema enforcement & evolution | Databricks-native, Spark-heavy workloads |
| **Apache Iceberg** | Partition evolution, hidden partitioning, snapshot isolation | Multi-engine (Spark, Trino, Flink, Presto), cloud-agnostic |
| **Apache Hudi** | Record-level upserts/deletes, incremental queries, CDC support | Streaming ingestion, CDC pipelines |

---

## Schema Design Patterns

### Star Schema

```
        ┌─────────────┐
        │  dim_date    │
        │  ────────    │
        │  date_key PK │──────────────┐
        │  full_date   │              │
        │  year        │              ▼
        │  quarter     │    ┌──────────────────┐
        │  month       │    │  fct_orders       │
        └─────────────┘    │  ────────────     │
                           │  date_key FK      │
        ┌─────────────┐    │  customer_key FK  │◄───── ┌─────────────────┐
        │ dim_customer │    │  product_key FK   │◄───── │  dim_product     │
        │ ─────────── │───▶│  amount           │       │  ───────────     │
        │ cust_key PK  │    │  quantity         │       │  product_key PK  │
        │ name         │    │  discount         │       │  name            │
        │ segment      │    │  revenue          │       │  category        │
        │ region       │    └──────────────────┘       │  brand           │
        └─────────────┘                                 └─────────────────┘

Rule of thumb: Fact = "what happened"; Dimension = "who, what, where, when"
```

### Data Vault 2.0

```
Hub (business keys):
  hub_customer:  customer_id (hash), customer_nk (natural key), load_date, record_source

Link (relationships):
  link_order_customer: order_customer_id (hash), order_id FK, customer_id FK, load_date

Satellite (descriptive attributes):
  sat_customer_detail: customer_id FK, name, email, segment, load_date, load_end_date
  sat_customer_address: customer_id FK, street, city, zip, load_date, load_end_date

Key rules:
  - Hubs are insert-only (business keys never change)
  - Satellites track history via load_date/load_end_date (SCD Type 2)
  - Links track many-to-many relationships
  - No foreign key constraints at DB level; enforced in ETL
```

### One Big Table (OBT) — When & When Not

```
✅ Use OBT when:
  - Query performance > storage cost (denormalization duplicates data)
  - BI tool requires flat tables (Looker, Tableau explore)
  - Joins are the bottleneck in your query workload
  - You have a small number of dimensions (3-5) that don't change often

❌ Don't use OBT when:
  - You need SCD Type 2 history (OBT explodes with dimension changes)
  - Dimensions are wide (100+ columns) and shared across facts
  - Update frequency is high (every dimension change rewrites entire OBT)
  - You need strict referential integrity (OBT masks missing dimension keys)
```

---

## Slowly Changing Dimensions (SCD)

| Type | Behavior | When to Use | Example |
|---|---|---|---|
| **Type 0** | Retain original. No changes. | Immutable reference data | Date of birth, original transaction amount |
| **Type 1** | Overwrite old value. No history. | Corrections, unimportant changes | Fixing a typo in product name |
| **Type 2** | Add new row. Track history. | Most common — track all changes | Customer address, product price history |
| **Type 3** | Add column for previous value. | Limited history (1 version) | Department name: `current_dept` + `previous_dept` |
| **Type 4** | Separate history table. | High-frequency changes | Rapidly changing stock prices |
| **Type 5** | Type 1 + Type 4 hybrid | Complex, rarely used | — |
| **Type 6** | Type 1 + Type 2 + Type 3 hybrid | When you need current + all history + previous | Advanced — use dbt snapshots instead |
| **Type 7** | Dual surrogate keys | When you need both transaction-time and valid-time | Temporal databases |

### SCD Type 2 — dbt Snapshot

```sql
{% snapshot customer_snapshot %}
{{
    config(
        target_schema='silver',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='updated_at',
    )
}}
SELECT * FROM {{ source('bronze', 'customers') }}
{% endsnapshot %}

-- dbt automatically adds:
-- dbt_valid_from, dbt_valid_to (NULL for current), dbt_scd_id
```

### SCD Type 2 Query Patterns

```sql
-- Get current state (dbt_valid_to IS NULL = current)
SELECT * FROM customers_snapshot WHERE dbt_valid_to IS NULL;

-- As of a point in time
SELECT * FROM customers_snapshot
WHERE dbt_valid_from <= '2026-01-15'
  AND (dbt_valid_to > '2026-01-15' OR dbt_valid_to IS NULL);

-- Full history for a customer
SELECT * FROM customers_snapshot
WHERE customer_id = 'cust_123'
ORDER BY dbt_valid_from;
```

---

## Partitioning & Clustering Strategy

### Partition Column Selection

| Criteria | Good | Bad |
|---|---|---|
| Cardinality | Medium (100-10K partitions) | High (millions of tiny files) or Low (1 partition) |
| Query patterns | Frequently filtered (`WHERE date = '...'` ) | Rarely used in WHERE clauses |
| Write pattern | Append-mostly (date-based partitions) | Heavy updates across partitions |
| Partition size | 100MB - 50GB per partition | < 100MB (too many small files) or > 50GB (slow scans) |

### Multi-Level Partitioning

```sql
-- Snowflake
CREATE TABLE orders (
  order_id STRING,
  order_date DATE,
  region STRING,
  ...
)
CLUSTER BY (order_date, region);

-- BigQuery
CREATE TABLE orders (
  order_id STRING,
  order_date DATE,
  region STRING,
  ...
)
PARTITION BY order_date
CLUSTER BY region;

-- Spark / Delta Lake
CREATE TABLE orders (
  order_id STRING,
  order_date DATE,
  region STRING,
  ...
)
USING delta
PARTITIONED BY (order_date, region);
```

### Partition Evolution (Iceberg)

```sql
-- Change partitioning without rewriting data
ALTER TABLE orders
  REPLACE PARTITION FIELD (YEAR(order_date), region);

-- Hidden partitioning: queries don't need to filter on partition column
SELECT * FROM orders WHERE order_date = '2026-01-15'
-- Iceberg knows to only read the '2026/01' partition
```

---

## Performance Optimization Quick Reference

| Technique | What | When | Impact |
|---|---|---|---|
| **Partition pruning** | Skip irrelevant partitions | Filter on partition columns | 10-1000x fewer bytes scanned |
| **Clustering** | Co-locate related data | High-cardinality filter columns | 2-10x fewer blocks read |
| **Column pruning** | Read only queried columns | SELECT specific columns | 2-20x fewer bytes scanned (wide tables) |
| **Predicate pushdown** | Filter at storage layer | Parquet/ORC with row group stats | 2-100x fewer rows processed |
| **Materialized views** | Pre-compute aggregations | Frequently queried aggregations | 10-1000x faster (trade storage) |
| **Z-ordering** (Delta Lake) | Multi-dimensional clustering | Filter on 2+ columns simultaneously | 5-50x faster multi-column filters |
| **OPTIMIZE** / **VACUUM** | Compaction + cleanup | Small files problem (< 100MB) | 2-10x faster scans |
