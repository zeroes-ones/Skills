# Database Operations

> **Author:** Sandeep Kumar Penchala

Production database operations patterns covering backup strategies, replication, high availability, connection pooling, query performance, vacuum management, monitoring, and disaster recovery. These practices support the database-reliability-engineer skill's mission of data durability and availability.

## Backup Strategies

### Backup Types and RPO/RTO

| Strategy | RPO | RTO | Storage Cost | Restore Complexity |
|----------|-----|-----|-------------|-------------------|
| Full backup (nightly) | Up to 24h | Hours | High (large + daily) | Low (single restore) |
| Full + Incremental | Minutes (with WAL) | 30-60 min | Medium | Medium (full + chain of incrementals) |
| Continuous WAL archiving | Seconds | 5-15 min | Medium (compressed WAL) | Medium (replay WAL to point-in-time) |
| Streaming replica + backups | Near-zero | < 30s (promote replica) | Higher (replica server) | Low (promote replica) |
| Multi-region replica | Near-zero | < 1min (DNS failover) | High (full copy in another region) | Low (switch traffic) |

### PostgreSQL Backup Commands

```bash
# Full backup
pg_dump -h localhost -U postgres -Fc mydb > mydb_full_$(date +%Y%m%d).dump

# Continuous WAL archiving (postgresql.conf)
archive_mode = on
archive_command = 'test ! -f /archive/%f && cp %p /archive/%f'

# Point-in-time recovery (PITR)
# recovery.conf / postgresql.auto.conf
restore_command = 'cp /archive/%f %p'
recovery_target_time = '2026-07-21 14:03:00 UTC'

# Verify backup can be restored (CRITICAL — schedule this)
pg_restore --list mydb.dump | head -20    # Check backup contents
pg_restore -h test-host -d mydb_test mydb.dump   # Test restore to staging
```

### Backup Schedule Template

```
Production critical (RPO < 5min):
  - Continuous WAL archiving to S3/GCS
  - Nightly full backup (retain 30 days)
  - Weekly backup verification (restore to staging + integrity check)

Production standard (RPO < 1hr):
  - Hourly incremental + WAL archiving
  - Daily full backup (retain 14 days)
  - Monthly backup verification

Non-production (RPO < 24hr):
  - Daily full backup (retain 7 days)
```

## Replication

### Async vs Sync

| Mode | Write Latency | Data Loss Risk | Use Case |
|------|-------------|---------------|----------|
| Async | No added latency | Seconds of WAL lag (can lose) | Read replicas, reporting |
| Sync | Waits for replica confirm | Zero data loss | High-durability requirements |
| Sync (remote_write) | Waits for local, async remote | WAN latency risk | Multi-region with local sync |

### Streaming Replication Setup

```ini
# Primary (postgresql.conf)
wal_level = replica
max_wal_senders = 5
wal_keep_size = 1024              # MB — keep WAL for lagging replicas

# Standby
primary_conninfo = 'host=primary port=5432 user=replicator password=secret'
```

### Logical Replication (Selective)

```sql
-- Publisher (source)
CREATE PUBLICATION orders_pub FOR TABLE orders, order_items;

-- Subscriber (target)
CREATE SUBSCRIPTION orders_sub
CONNECTION 'host=source dbname=mydb user=replicator password=secret'
PUBLICATION orders_pub;
```

### Failover Procedure

```bash
# 1. Verify standby is caught up
psql -h standby -c "SELECT pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn();"
# LSNs should match or be very close

# 2. Promote standby to primary
pg_ctl promote -D /var/lib/postgresql/data
# Or: touch /var/lib/postgresql/data/standby.signal → remove → restart

# 3. Update application connection string / DNS
# 4. Rebuild old primary as new standby
```

## High Availability

### HA Architecture Comparison

| Solution | Failover Time | Complexity | Cost | Best For |
|----------|-------------|-----------|------|----------|
| Patroni + etcd | < 30s | Medium | 3 nodes + etcd | Self-managed PostgreSQL |
| RDS Multi-AZ | 60-120s | Zero (managed) | 2x compute | AWS workloads |
| Cloud SQL HA | 60-120s | Zero (managed) | 2x compute | GCP workloads |
| pg_auto_failover | < 30s | Low-Medium | 3+ nodes | Simpler than Patroni |

### Patroni Configuration

```yaml
# patroni.yml
scope: mydb
name: postgresql-0
restapi:
  listen: 0.0.0.0:8008
  connect_address: postgresql-0.mydb:8008
etcd:
  hosts: etcd-0:2379,etcd-1:2379,etcd-2:2379
bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576    # 1 MB max lag for failover
    postgresql:
      use_pg_rewind: true
      parameters:
        wal_level: replica
        hot_standby: "on"
        wal_keep_size: 1024
postgresql:
  listen: 0.0.0.0:5432
  connect_address: postgresql-0.mydb:5432
  data_dir: /var/lib/postgresql/data
  pgpass: /tmp/pgpass
```

## Connection Pooling

### PgBouncer Pool Modes

| Mode | Description | When to Use |
|------|------------|-------------|
| Session | One server connection per client session | When using prepared statements, temp tables, `SET` |
| Transaction | Server connection released after each transaction | **Default recommendation** — best balance |
| Statement | Server connection released after each statement | Only for auto-commit, read-only workloads |

### PgBouncer Sizing

```ini
[pgbouncer]
pool_mode = transaction
default_pool_size = 25         # Per-user pool (25 per user/db combo)
max_client_conn = 500          # Max incoming clients
reserve_pool_size = 5          # Extra connections for bursts
reserve_pool_timeout = 3       # Seconds to wait for reserve pool
```

```
Sizing formula:
  total_app_connections = app_instance_count * pool_size_per_instance
  pg_pool_size = total_app_connections / average_concurrency_factor
  pg_pool_size <= (CPU_cores * 2) — never exceed this
```

## Query Performance

### pg_stat_statements Analysis

```sql
-- Top 10 queries by total time
SELECT
  queryid,
  LEFT(query, 100) AS query_preview,
  calls,
  ROUND(total_exec_time::numeric, 2) AS total_ms,
  ROUND(mean_exec_time::numeric, 2) AS avg_ms,
  ROUND((shared_blks_hit::numeric / NULLIF(shared_blks_hit + shared_blks_read, 0)) * 100, 1) AS cache_hit_pct,
  rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

### auto_explain for Slow Queries

```ini
# postgresql.conf
shared_preload_libraries = 'auto_explain'
auto_explain.log_min_duration = 1000   # Log plans for queries > 1s
auto_explain.log_analyze = on          # Include actual timings
auto_explain.log_buffers = on          # Include buffer usage
auto_explain.log_nested_statements = on
```

### Index Advisor (HypoPG)

```sql
-- Install HypoPG extension
CREATE EXTENSION hypopg;

-- Create hypothetical index (not actually built)
SELECT * FROM hypopg_create_index('CREATE INDEX ON orders(customer_id, status)');

-- Check if the hypothetical index would be used
EXPLAIN SELECT * FROM orders WHERE customer_id = 42 AND status = 'shipped';
-- Look for "Index Scan using <hypo_index>" — if present, create the real index
```

## Vacuum Management

### Autovacuum Tuning

```ini
# postgresql.conf — aggressive autovacuum for write-heavy workloads
autovacuum_max_workers = 4              # Default 3; increase for many tables
autovacuum_naptime = 30s                # Default 1min; wake up more often
autovacuum_vacuum_scale_factor = 0.05   # Default 0.2; vacuum sooner (5% dead tuples)
autovacuum_vacuum_threshold = 100       # Minimum dead tuples before vacuum
autovacuum_vacuum_cost_limit = 2000     # Default 200; allow more aggressive vacuum
```

### Transaction ID Wraparound Prevention

```sql
-- Monitor wraparound risk
SELECT
  datname,
  age(datfrozenxid) AS xid_age,
  ROUND(100.0 * age(datfrozenxid) / 2000000000, 2) AS pct_to_wraparound
FROM pg_database
WHERE age(datfrozenxid) > 100000000
ORDER BY age(datfrozenxid) DESC;

-- CRITICAL: If approaching 2 billion, VACUUM FREEZE immediately
-- AUTOMATIC: PostgreSQL forces autovacuum_freeze_max_age (default 200M)
```

### Bloated Table Detection

```sql
-- Check for table bloat (dead tuples not yet reclaimed)
SELECT
  schemaname || '.' || relname AS table,
  n_dead_tup,
  n_live_tup,
  ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 1) AS dead_pct,
  last_vacuum, last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

## Monitoring

### Key PostgreSQL Metrics

```sql
-- Cache hit ratio (should be > 99%)
SELECT
  sum(blks_hit) * 100.0 / NULLIF(sum(blks_hit) + sum(blks_read), 0) AS cache_hit_ratio
FROM pg_stat_database;

-- Dead tuples
SELECT relname, n_dead_tup, n_live_tup FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 10;

-- Replication lag (in bytes)
SELECT
  client_addr,
  pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes,
  state
FROM pg_stat_replication;

-- Connection count by state
SELECT state, count(*) FROM pg_stat_activity GROUP BY state;

-- Long-running queries (> 5 min)
SELECT pid, now() - query_start AS duration, LEFT(query, 150)
FROM pg_stat_activity
WHERE state != 'idle' AND query_start < now() - interval '5 minutes'
ORDER BY duration DESC;
```

### Monitoring Dashboard Cheat Sheet

```
Metric              | Alert When                  | Dashboard Panel
--------------------|-----------------------------|-------------------
Cache Hit Ratio     | < 95%                       | Gauge (99% target)
Dead Tuples %       | > 20% of total rows         | Line chart
Replication Lag     | > 100 MB or > 30s           | Line chart (bytes + seconds)
Active Connections  | > 80% of max_connections   | Line chart
Long-Running Queries| > 5 min duration            | Table
XID Wraparound      | > 1 billion age             | Gauge (below 1B)
Transaction Rate    | Drop to 0 (may be outage)   | Line chart
```

## Disaster Recovery

### Multi-Region Failover

```yaml
# DNS failover with health checks
# Route 53 configuration
PrimaryEndpoint:
  Region: us-east-1
  HealthCheckId: primary-db-health
  Weight: 100  # All traffic to primary
SecondaryEndpoint:
  Region: eu-west-1
  HealthCheckId: standby-db-health
  Weight: 0    # No traffic unless primary fails
  Failover: PRIMARY  # Active when primary health check fails
```

### Recovery Testing Schedule

```
Weekly:    Verify WAL archiving — check latest WAL in archive
Monthly:   Restore latest full backup to staging + replay WAL → validate
Quarterly: Full DR failover test — promote standby, run app against it
Annually:  Chaos test — kill primary during business hours, measure failover
```

### DR Runbook (Abbreviated)

```bash
# 1. Detect failure — alert fires or manual observation
# 2. Decide: promote standby or restore from backup?
#    Promote standby if lag < 10s; restore from backup otherwise
# 3. Execute failover
pg_ctl promote -D /var/lib/postgresql/data  # On standby
# 4. Update DNS / connection strings
# 5. Verify: can the app connect and serve traffic?
# 6. Rebuild old primary as new standby
# 7. Postmortem: what caused the failure?
```

These database operations patterns implement the database-reliability-engineer skill's core mandate: data is never lost, always available, and recoverable within defined RPO/RTO targets — verified through regular testing, not hope.
