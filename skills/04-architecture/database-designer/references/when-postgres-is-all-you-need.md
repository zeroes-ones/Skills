# When Postgres is All You Need

```
Need full-text search? → Postgres built-in tsvector + GIN index (good to 1M docs).
Need caching? → Postgres UNLOGGED tables + materialized views (good to 10K QPS).
Need message queue? → Postgres SKIP LOCKED (PGMQ / 1K msg/sec).
Need time-series? → Postgres partitioning + TimescaleDB extension (good to 1B rows).
Need JSON documents? → Postgres JSONB with GIN indexes (good to 10M documents).
Need graph queries? → Postgres recursive CTEs (good to 100K nodes).

The only reasons to leave Postgres:
- > 10TB data with simple key-value access → DynamoDB/Cassandra
- > 10K writes/sec sustained → Cassandra/ScyllaDB
- > 100M graph traversals → Neo4j
- Global multi-region with < 10ms writes → CockroachDB/Spanner
```
