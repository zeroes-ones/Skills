# Database Selection Decision Tree

## Decision Flow

```
Need to store data
  │
  ├─ Data is highly relational, ACID required?
  │   ├─ Yes → Relational DB (PostgreSQL, MySQL)
  │   │   ├─ Need full-text search? → PostgreSQL (built-in tsvector)
  │   │   ├─ Need horizontal scale writes? → CockroachDB, Vitess
  │   │   └─ Simple CRUD, single region? → PostgreSQL (default choice)
  │   │
  │   └─ No → Continue ↓
  │
  ├─ Data is document-oriented, schema flexible?
  │   ├─ Yes → MongoDB, Couchbase
  │   └─ No → Continue ↓
  │
  ├─ Data is time-series (metrics, events)?
  │   ├─ Yes → TimescaleDB (PostgreSQL extension), InfluxDB
  │   └─ No → Continue ↓
  │
  ├─ Need graph traversals (social, recommendations)?
  │   ├─ Yes → Neo4j, Amazon Neptune
  │   └─ No → Continue ↓
  │
  ├─ Key-value cache with TTL?
  │   ├─ Yes → Redis, Memcached
  │   └─ No → Continue ↓
  │
  ├─ Full-text search engine?
  │   ├─ Yes → Elasticsearch, Meilisearch
  │   └─ No → Continue ↓
  │
  ├─ Event streaming / message queue?
  │   ├─ Yes → Kafka, Redis Streams, RabbitMQ
  │   └─ No → Continue ↓
  │
  ├─ Blob / file storage?
  │   ├─ Yes → S3, Cloud Storage, MinIO
  │   └─ No → Continue ↓
  │
  └─ Analytical / OLAP workloads?
      ├─ Yes → ClickHouse, BigQuery, Snowflake, DuckDB
      └─ No → PostgreSQL (polyglot persistence — one DB for most needs)
```

## PostgreSQL: The Default Choice

PostgreSQL is the recommended default for most applications because:
- ACID compliance with strong consistency
- JSONB for document flexibility when needed
- Full-text search with tsvector
- Extensions: PostGIS (geo), TimescaleDB (time-series), pgvector (embeddings)
- Excellent tooling and ecosystem
- Free, open-source, battle-tested

## When NOT to Use PostgreSQL

| Use Case | Better Alternative |
|----------|-------------------|
| High write throughput (>50K writes/sec) | Cassandra, DynamoDB |
| Graph-heavy queries | Neo4j |
| Full-text at massive scale (>10M docs) | Elasticsearch |
| Real-time analytics on billions of rows | ClickHouse |
| Global multi-region writes | CockroachDB, Spanner |

## Multi-Database Architecture

Modern applications often use multiple databases:
```
PostgreSQL (primary OLTP) + Redis (cache/sessions) + Elasticsearch (search) + S3 (files)
```

**Rules:**
1. PostgreSQL is the source of truth
2. Redis is cache only — can be rebuilt from PostgreSQL
3. Elasticsearch is search index — can be reindexed from PostgreSQL
4. S3 is for blobs — metadata (path, size, type) in PostgreSQL
