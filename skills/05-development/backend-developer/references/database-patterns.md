# Database Patterns

> **Author:** Sandeep Kumar Penchala

Production database patterns covering query optimization, migrations, connection pooling, transactions, caching, and data modeling. These patterns extend the backend-developer skill's database integration and performance tuning phases.

## Query Optimization

### Reading EXPLAIN Output

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 42 AND status = 'shipped';

-- Key fields to check:
-- Seq Scan          → BAD — full table scan; add an index
-- Index Scan        → OK — using index; check if index-only scan possible
-- Index Only Scan   → GOOD — no heap lookup needed (use covering indexes)
-- Bitmap Heap Scan  → OK for larger result sets; combines multiple indexes
-- Nested Loop       → OK for small inner sets; terrible for large joins
-- Hash Join         → GOOD for large equality joins
-- (cost=X..Y)       → X = startup cost, Y = total cost; focus on Y
-- (rows=N)          → Estimated vs actual rows — large mismatch = stale stats
```

### Index Selection Guide

| Query Pattern | Index Type | Example |
|--------------|-----------|---------|
| `WHERE col = ?` | B-tree on col | `CREATE INDEX idx_status ON orders(status);` |
| `WHERE col BETWEEN ? AND ?` | B-tree on col | Covers range queries |
| `WHERE col IN (?)` | B-tree on col | Covers IN clauses |
| `WHERE col ILIKE 'prefix%'` | B-tree (anchored) or GIN trigram | `CREATE INDEX idx_name ON users USING gin(name gin_trgm_ops);` |
| `WHERE col @> '{"key":"value"}'` (JSONB) | GIN | `CREATE INDEX idx_data ON events USING gin(data);` |
| `WHERE ST_DWithin(...)` (geo) | GiST | `CREATE INDEX idx_loc ON places USING gist(location);` |
| Multi-column: `WHERE a=? AND b=?` | Composite: `(a, b)` | Order matters — put equality first, range last |
| `ORDER BY col` | B-tree on col | Eliminates sort step |
| Covering: `SELECT a, b WHERE a=?` | `(a) INCLUDE (b)` | Index-only scan — no heap lookup |

### Query Plan Caching

```sql
-- PostgreSQL: check prepared statement hit rate
SELECT * FROM pg_prepared_statements;

-- Check plan cache efficiency
SELECT calls, total_exec_time / calls AS avg_ms, query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

## Migration Patterns

### Expand-Contract (Zero-Downtime)

```
Phase 1 — EXPAND: Add new column/table (non-breaking)
  ALTER TABLE users ADD COLUMN full_name TEXT;
  -- Deploy app that writes to both old and new columns

Phase 2 — MIGRATE: Backfill data
  UPDATE users SET full_name = first_name || ' ' || last_name WHERE full_name IS NULL;

Phase 3 — SWITCH: Switch reads to new column
  -- Deploy app that reads from new column

Phase 4 — CONTRACT: Remove old column
  ALTER TABLE users DROP COLUMN first_name, DROP COLUMN last_name;
```

### Dangerous Migration Checklist

| Operation | Risk | Mitigation |
|-----------|------|------------|
| `ALTER TABLE ... ADD COLUMN NOT NULL DEFAULT` | Table rewrite on old PG (< 11) | Add nullable first, backfill, set NOT NULL |
| `DROP COLUMN` | App still reading it | Expand-contract; never drop in same deploy |
| `RENAME COLUMN` | App references old name | Rename is instant but app must switch atomically |
| `ADD FOREIGN KEY` | Locks both tables | Add NOT VALID, validate later: `ALTER TABLE ... VALIDATE CONSTRAINT` |
| `CREATE INDEX` | Locks writes on old PG | Use `CONCURRENTLY`: `CREATE INDEX CONCURRENTLY` |

### Rollback Strategy

```sql
-- Every migration file should have a tested down migration
-- 001_add_email_to_users.up.sql
ALTER TABLE users ADD COLUMN email TEXT;

-- 001_add_email_to_users.down.sql
ALTER TABLE users DROP COLUMN email;
```

## Connection Pooling

### Pool Sizing Formula

```
connections = ((core_count * 2) + effective_spindle_count)

PostgreSQL:  Pool size = floor((cores * 2) / number_of_services)
             Max ~200 total connections (PG performs poorly beyond this)

Typical: 10-25 connections per service instance
```

### PgBouncer Configuration

```ini
[databases]
mydb = host=db.internal port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction           # transaction | session | statement
default_pool_size = 25            # Per-user pool size
max_client_conn = 500             # Max incoming client connections
server_idle_timeout = 600         # Drop idle server connections after 10m
client_login_timeout = 15         # Max time to authenticate
query_timeout = 30                # Max query execution time
```

### Connection Lifecycle

```python
# SQLAlchemy pool configuration
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://user:pass@host/db",
    pool_size=20,              # Persistent connections
    max_overflow=10,           # Temporary extras under load
    pool_recycle=3600,         # Recycle after 1hr (stale connection defense)
    pool_pre_ping=True,        # Verify connection before use (adds ~1ms overhead)
    connect_args={
        "options": "-c statement_timeout=30000",  # 30s query timeout
        "application_name": "my-service",
    }
)
```

## Transaction Patterns

### Isolation Level Selection

| Level | Protects Against | PostgreSQL Default? | Performance |
|-------|-----------------|---------------------|-------------|
| Read Uncommitted | Nothing useful | N/A (treated as Read Committed) | Best |
| Read Committed | Dirty reads | **YES — default** | Good |
| Repeatable Read | Non-repeatable reads | No (but PG has SI) | Moderate |
| Serializable | All anomalies | No | Worst |

### Optimistic Locking

```sql
-- Add version column for optimistic concurrency control
ALTER TABLE orders ADD COLUMN version INT DEFAULT 1;

-- Read
SELECT id, status, version FROM orders WHERE id = 123;

-- Write — only succeeds if no one else wrote
UPDATE orders SET status = 'shipped', version = version + 1
WHERE id = 123 AND version = 5;
-- If rows_affected = 0 → conflict; retry from read
```

### Distributed Transactions — Saga Pattern

```
Order Saga:
  1. Create Order       (Order Service)        ← success
  2. Reserve Inventory  (Inventory Service)    ← success
  3. Charge Payment     (Payment Service)      ← FAILS!
  4. Compensate: Cancel Inventory Reservation  (rollback step 2)
  5. Compensate: Cancel Order                  (rollback step 1)

Implementation: choreography (events) or orchestration (saga coordinator)
```

## Caching Strategies

| Strategy | Reads | Writes | Consistency | Best For |
|----------|-------|--------|-------------|----------|
| Cache-Aside | App checks cache, misses → DB, populates cache | App writes to DB, invalidates cache | Eventually consistent | Read-heavy, cache misses tolerable |
| Read-Through | Cache sits in front; transparently loads from DB | App writes to cache → cache writes DB | Eventually consistent | Simplifying app code |
| Write-Through | As read-through | Cache writes to DB synchronously | Stronger | Write-heavy, need consistency |
| Write-Behind | As read-through | Cache writes async to DB | Weakest | High write throughput, tolerable loss |

```python
# Cache-aside with Redis (Python)
import redis, json
from functools import wraps

r = redis.Redis(decode_responses=True)

def cached(ttl: int = 300):
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            key = f"cache:{fn.__name__}:{args}:{kwargs}"
            cached = r.get(key)
            if cached:
                return json.loads(cached)
            result = await fn(*args, **kwargs)
            r.setex(key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@cached(ttl=60)
async def get_user_orders(user_id: int):
    return await db.fetch_all("SELECT * FROM orders WHERE user_id = $1", user_id)
```

## Data Modeling Tradeoffs

| Decision | For Normalized | For Denormalized |
|----------|---------------|------------------|
| Write performance | ✅ Single source of truth | ❌ Update multiple copies |
| Read performance | ❌ JOINs needed | ✅ Single read, no joins |
| Storage | ✅ No duplication | ❌ Data duplicated |
| Consistency | ✅ Guaranteed | ❌ Eventual consistency risk |
| Query complexity | ❌ Complex queries | ✅ Simple queries |

### UUID vs Auto-Increment Primary Keys

| Property | UUID v4 | UUID v7 (time-sorted) | Auto-Increment BIGINT |
|----------|---------|----------------------|----------------------|
| Size | 16 bytes | 16 bytes | 8 bytes |
| Sortability | ❌ Random | ✅ Time-ordered | ✅ Sequential |
| Distributed generation | ✅ No coordination | ✅ No coordination | ❌ Needs central source |
| Index performance | ❌ Fragmented B-tree | ✅ Partially ordered | ✅ Perfect ordering |
| URL safety | ✅ Opaque | ✅ Opaque | ❌ Guessable |
| Recommendation | Legacy / external IDs | Modern default | Simple apps, single DB |

### When to Use Each

```
UUID v7 → Distributed systems, multi-tenant, exposed IDs, eventual sharding
Auto-Increment → Single database, internal only, size-constrained, sequential needed
ULID → Alternative to UUID v7 — 26 chars, sortable, URL-safe
```

These database patterns support the backend-developer skill's Phase 2 (Implementation) and Phase 4 (Deployment Readiness) — proper connection pooling, migration strategies, and cache-aside patterns ensure production reliability from day one.
