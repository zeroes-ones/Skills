# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Reliability Architecture Design

1. **Define SLOs — not just "highly available"**
   - Input: Business requirements from product owner
   - Output: SLO document: RPO (data loss tolerance), RTO (recovery time), availability target (99.9% / 99.95% / 99.99%)
   - RPO = 0 means sync replication, RPO = 5min means async with aggressive WAL archiving
   - Availability math: 99.9% = 8.76h downtime/year, 99.99% = 52.6min/year. Be explicit.

2. **Design HA topology**
   - PostgreSQL: Patroni + etcd (or Consul) for auto-failover. Minimum 3 nodes for quorum.
   - MySQL: InnoDB Cluster (Group Replication) or Orchestrator for topology management
   - Cloud-managed: RDS Multi-AZ, Cloud SQL HA, AlloyDB — hands-off but understand failover latency
   - Input: SLOs, traffic patterns, region topology. Output: HA architecture diagram + failover runbook.

3. **Design DR topology**
   - Cross-region replication: async streaming (or logical replication for selective tables)
   - DR site: warm standby (replica running, takes traffic in minutes) vs cold (restore from backup, hours)
   - Decision driver: RTO < 15min → warm standby. RTO < 4hrs → cold standby is acceptable.
   - Test: run DR failover exercise quarterly. Document actual RPO/RTO achieved vs target.

4. **Provision with future capacity**
   - Storage: provision 2x current usage. Monitor growth rate, not absolute.
   - IOPS: baseline from `pg_stat_statements` or `performance_schema`. Add 50% headroom.
   - Connections: PgBouncer pool size = (CPU cores × 2-4). Application pool size = 10-20 per process.
   - Anti-pattern: provisioning for "worst case" day 1 — scale up based on data, not guesses.

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Query Performance & Index Strategy

5. **Identify slow queries — systematic, not anecdotal**
   - PostgreSQL: `pg_stat_statements` — top queries by total_time, mean_time, calls, shared_blks_read
   - MySQL: `performance_schema.events_statements_summary_by_digest`
   - RDS: Performance Insights provides per-query metrics without query
   - Input: database statistics. Output: ranked list of optimization candidates with estimated impact.

6. **Analyze query execution plans**
   - `EXPLAIN (ANALYZE, BUFFERS)` for representative parameters
   - Look for: Seq Scan on large tables (>10K rows), nested loop with large inner, high memory estimates
   - Hash join vs nested loop: hash join wins for large datasets but uses more memory
   - Input: slow query. Output: execution plan analysis + optimization recommendation.

7. **Index strategy — deliberate, not reactive**
   - Every index must serve at least one specific query. Add index → measure improvement → keep or drop.
   - Composite index column order: equality filters → range filters → sort columns. Most selective first.
   - Covering indexes: `INCLUDE (col1, col2)` avoids heap fetches for index-only scans
   - Partial indexes: `WHERE status = 'active'` — smaller, faster for well-defined subsets
   - When NOT to index: tables < 1000 rows, columns with < 2 distinct values, write-heavy tables (>100 writes/s)
   - Input: query patterns. Output: index creation DDL with justification.

8. **Query rewriting techniques**
   - CTE (WITH) vs subquery: CTEs are optimization fences in PostgreSQL <12. Subqueries can be optimized as part of parent.
   - `WHERE EXISTS` over `IN` for large subquery results. `LATERAL` joins for top-N-per-group.
   - Avoid function calls on indexed columns: `WHERE date_trunc('day', created_at) = '2024-01-01'` → `WHERE created_at >= '2024-01-01' AND created_at < '2024-01-02'`.

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Maintenance & Operations

9. **Vacuum strategy (PostgreSQL) — the non-negotiable**
   - Autovacuum must be ON. Tune: `autovacuum_vacuum_scale_factor = 0.01` (not default 0.2) for large tables
   - Monitor: dead tuple ratio (`pg_stat_user_tables.n_dead_tup / n_live_tup`). Alert: > 10%
   - Anti-wraparound vacuum: monitor `age(datfrozenxid)`. Alert at 200M, critical at 1B.
   - Manual `VACUUM FULL` only when bloat is severe and during maintenance windows. It rewrites the table with exclusive lock.

10. **MySQL maintenance**
    - InnoDB: `ANALYZE TABLE` for stale statistics. `OPTIMIZE TABLE` for fragmented tables.
    - Purge lag: `SHOW ENGINE INNODB STATUS` — check history list length. Lag > 10K impacts query performance.
    - Buffer pool hit rate: should be > 99%. If < 95%, increase `innodb_buffer_pool_size`.

11. **Scheduled maintenance windows**
    - Monthly: REINDEX on heavily-updated indexes (concurrent where possible)
    - Monthly: update table statistics (`ANALYZE`)
    - Quarterly: validate backups — actually restore the latest backup to a staging instance
    - Quarterly: DR failover drill — measure actual RPO/RTO vs targets

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Backup, Recovery & Migration

12. **Backup verification — the backup that isn't tested doesn't exist**
    - Weekly: automated restore test of latest backup to ephemeral instance
    - Verify: row counts match, recent data present, no corruption
    - Input: backup files. Output: backup validation report

13. **PITR recovery drill**
    - Scenario: "recover orders table to state 2 hours ago"
    - Process: restore base backup → replay WAL/binary logs to target time → extract data
    - Input: backup + WAL archives. Output: recovered data validated + time-to-recover recorded

14. **Zero-downtime migration — expand-contract pattern**
    - **Expand**: Add new column/table. Dual-write: app writes to both old and new schema.
    - **Backfill**: Populate new schema with historical data in batches (1000 rows, 100ms sleep between)
    - **Verify**: Data consistency check between old and new. Row counts, checksums.
    - **Switch**: App reads from new schema. Keep dual-write for 1 release cycle.
    - **Contract**: Drop old column/table after confirming no reads remain.
    - Input: migration requirements. Output: migration runbook + rollback plan.

15. **Schema change safety rules**
    - Adding nullable column: safe. Instant on PostgreSQL 11+.
    - Adding column with DEFAULT + NOT NULL: unsafe on large tables (rewrites entire table). Use: add nullable → backfill → set NOT NULL → set DEFAULT.
    - Renaming column: unsafe. Use expand-contract: add new column → dual-write → migrate reads → drop old.
    - Dropping column/table: only after weeks of monitoring showing zero references.

<!-- DEEP: 10+min -->
### Phase 5 (~25 min): Monitoring, Capacity & Fleet Management

16. **Essential monitoring metrics**
    - **Latency**: p50, p95, p99 query duration. Alert: p95 > 2x baseline.
    - **Throughput**: queries/sec, connections active/idle. Alert: connections > 80% pool capacity.
    - **Replication lag**: bytes behind (PostgreSQL), seconds behind (MySQL). Alert: > 5s or growing.
    - **Errors**: deadlocks, connection timeouts, statement timeouts. Alert: any sustained increase.
    - **Storage**: disk usage % + growth rate. Alert: > 75% or > 7 days until full at current growth rate.
    - **Bloat**: dead tuples ratio (PostgreSQL), fragmentation (MySQL). Alert: > 10%.

17. **Capacity planning — data-driven, not calendar-driven**
    - Track: storage growth rate (GB/week), connection growth, IOPS trend, replication lag trend
    - Forecast: when will current instance hit 70% of any limit? Plan upgrade 1 month before.
    - Input: 90-day metrics history. Output: capacity forecast with upgrade timeline and cost estimate.

18. **Fleet management — treat databases as cattle, not pets**
    - Every database: source-controlled schema (migration files), configuration in Git, backup verified
    - Standardize: same PostgreSQL extensions, same autovacuum tuning, same monitoring dashboard
    - Automation: Terraform/Pulumi for provisioning, Ansible for config management, CI/CD for migrations
    - Anti-pattern: SSH into production to run ad-hoc queries. Use read replicas or staging.
