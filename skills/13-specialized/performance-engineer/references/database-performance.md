# Database Performance

### Query Plan Analysis (EXPLAIN ANALYZE)

Reading a query plan from innermost to outermost:

- **Node types**:
  - **Sequential Scan**: Reads all rows — BAD on large tables. Fix: add index or add `LIMIT`.
  - **Index Scan**: Reads via index. Good. Single index lookup.
  - **Bitmap Heap Scan** + **Bitmap Index Scan**: Reads via index then fetches heap pages. Used for low-selectivity queries (many matching rows).
  - **Index Only Scan**: All needed data in the index, no heap fetch. Best case — add covering indexes.
- **Join methods**:
  - **Nested Loop**: For each outer row, probe inner. Good for small result sets or when inner side has an index.
  - **Hash Join**: Build hash table on one side, probe with other. Best for large, unsorted data sets.
  - **Merge Join**: Sort both sides then merge. Good for pre-sorted data (index order).
- **Key metrics**: `rows` (estimated) vs `actual rows` — mismatch >10x means stale statistics. `cost` — relative, not absolute. `buffers` — how many 8KB pages read.

### Index Optimization

- **Covering indexes**: Include all columns needed by a query in the index. PostgreSQL: `CREATE INDEX idx ON posts (author_id) INCLUDE (title, created_at)`. Enables index-only scans.
- **Composite index column order**: Put high-cardinality / high-selectivity columns first. `(user_id, status)` — user_id filters most rows, then status differentiates. Wrong order: `(status, user_id)` — status has few values, not selective.
- **Partial indexes**: Index only a subset of rows. Example: `CREATE INDEX idx_active_users ON users (email) WHERE active = true`. Smaller, faster.
- **Expression indexes**: Index on a function result. Example: `CREATE INDEX idx_lower_email ON users (LOWER(email))`. Enables `WHERE LOWER(email) = '...'`.
- **Write overhead**: Each index adds ~10-30% write overhead. Don't index columns you never query. Monitor `pg_stat_user_indexes` for unused indexes.

### Connection Pooling (Database)

- **PgBouncer**: Lightweight, dedicated PostgreSQL connection pooler. Three modes:
  - **Session pooling**: Connection assigned to client for entire session. Lowest overhead but uses most connections.
  - **Transaction pooling** (recommended for web apps): Connection returned to pool after each transaction. Requires no session-level state (`SET`, prepared statements).
  - **Statement pooling**: Connection returned after each statement. Even stricter — no session state at all.
- **Pool sizing**: `max_connections = (num_cores × 2) ÷ (avg_query_time ÷ avg_query_interval)`. Start at 20-30 per pooler, benchmark up.
- **Watch**: `server_idle_timeout` (close idle connections), `query_timeout` (kill stuck queries), `max_db_connections` (don't overwhelm the database).

### Read Replica Routing

- **Pattern**: Write to primary, read from replicas. Route at the application layer or via middleware (PgBouncer with replica config, ProxySQL).
- **Replication lag**: Monitor `pg_stat_replication` (PostgreSQL) or `SHOW SLAVE STATUS` (MySQL). Acceptable lag depends on use case — real-time dashboard vs historical reporting.
- **Stale read handling**: If your application cannot tolerate stale data, read-write splits must be aware: send critical reads to primary, use replica for analytics and reporting.
- **Load balancing**: Distribute read queries across replicas with health-aware round-robin. Remove unhealthy replicas from rotation automatically.

### Vacuum & Analyze (PostgreSQL)

PostgreSQL's MVCC means dead tuples accumulate on UPDATE/DELETE. Autovacuum reclaims this space.

- **Monitoring**: Check `n_dead_tup` in `pg_stat_user_tables`. If dead tuples exceed 20% of live tuples, autovacuum is falling behind.
- **Tuning**: Increase `autovacuum_vacuum_scale_factor` (default 0.2 = vacuum after 20% changed). For large tables, set it lower or use fixed thresholds.
- **When to intervene**: Run `VACUUM ANALYZE` manually after bulk updates. `VACUUM FREEZE` before long-running transactions to avoid transaction ID wraparound.
- **Bloated indexes**: `REINDEX INDEX idx_name CONCURRENTLY` — rebuilds index without blocking writes.
