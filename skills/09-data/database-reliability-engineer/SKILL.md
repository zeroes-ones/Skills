---
name: database-reliability-engineer
description: Database reliability architecture (HA, DR, RPO/RTO), replication and sharding strategies, query optimization, index strategy, connection pooling, backup/recovery, migration with zero downtime, multi-tenant design, and database fleet management. Triggered by DBRE, database reliability, database operations, database scaling, query optimization, sharding, replication, database HA, database DR, database backup.
author: Sandeep Kumar Penchala
type: data
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - database-reliability-engineer
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
---
# Database Reliability Engineer (DBRE)

Ensure databases are reliable, performant, scalable, and recoverable. This skill applies SRE principles
to database systems — treating databases as reliability-critical infrastructure that requires
proactive engineering rather than reactive administration. Covers HA/DR architecture (RPO/RTO design),
replication strategies (async, semi-sync, sync, logical), sharding and partitioning design, connection
pooling (PgBouncer, ProxySQL, RDS Proxy), query optimization and index strategy, vacuum and maintenance
operations, backup and PITR, monitoring and alerting, capacity planning, zero-downtime migration
strategies, multi-tenant design, data archival and lifecycle management, database security, fleet
management at scale, and cost optimization.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Design high availability → Jump to "Sub-Skills > ha-architecture"
├── Disaster recovery planning → Go to "Sub-Skills > backup-recovery"
├── Replication strategy → Jump to "Sub-Skills > replication-strategy"
├── Query optimization → Go to "Sub-Skills > query-optimization"
├── Index strategy → Jump to "Best Practices" then "Sub-Skills > query-optimization"
├── Backup and recovery → Go to "Sub-Skills > backup-recovery"
├── Zero-downtime migration → Jump to "Sub-Skills > migration-strategy"
├── Need schema design → Invoke database-designer skill instead
├── Need infrastructure monitoring → Invoke site-reliability-engineer skill instead
└── Don't know where to start? → Start at "Decision Trees" for RPO/RTO-based architecture selection
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read First

These rules apply to *every* response this skill produces. Database changes are high-risk, irreversible, and affect production data — advice given without operational context can cause data loss or extended downtime.

- **Never recommend a migration or schema change without verifying backup status.** A failed migration without a verified, recent backup means data loss. Every schema change, data migration, or major configuration change recommendation must explicitly state: "Verify that a tested, recent backup exists before proceeding."
- **Performance advice without query plans is guessing.** Two queries with identical output can have wildly different execution plans depending on indexes, statistics freshness, table bloat, and planner configuration. Always recommend running `EXPLAIN (ANALYZE, BUFFERS)` (PostgreSQL) or equivalent before accepting any performance diagnosis or optimization recommendation.
- **Every production change needs an explicit rollback plan.** State this for every recommendation that touches a production database. Include what the rollback looks like (e.g., "reverse this migration with `rails db:rollback`", "restore from pre-change snapshot"), how long it takes, and what data loss or downtime it entails. If you can't describe the rollback, the change isn't ready for production.
- **Connection pool sizing depends on actual workload, not formulas.** The formula `connections = ((core_count * 2) + effective_spindle_count)` is a starting point, not an answer. Actual connection requirements depend on query latency distribution, transaction duration, application concurrency model, and connection overhead. Recommend measuring under realistic load before sizing pools.
- **Admit when you need to see the actual data.** Generalized advice about normalization, denormalization, indexing strategy, and partitioning becomes dangerous without understanding data volume, access patterns, and growth rate. When the recommendation depends on these factors, ask for them rather than assuming a "typical" workload.

## When to Use

- You need to design a high-availability database architecture with clear RPO and RTO targets
- You are choosing a replication strategy (synchronous, async, semi-sync, logical) for multi-region DR
- A production query is slow and you need to analyze execution plans, add indexes, or rewrite the query
- You need to set up connection pooling (PgBouncer, ProxySQL, RDS Proxy) to handle high connection counts
- You are planning a sharding or partitioning strategy to scale writes beyond a single database instance
- You need to implement backup and point-in-time recovery (PITR) with tested restore procedures
- You are running a zero-downtime schema migration and need an expand-contract or online schema change tool
- You are managing a fleet of 10+ databases and need standardized monitoring, maintenance, and lifecycle automation

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Replication Strategy Decision

```
What are your RPO and RTO requirements?
├── RPO = 0, RTO < 60s (no data loss tolerated)
│   ├── Single region                        → Synchronous replication (Patroni + etcd, Galera)
│   │   └── Cost: +30-50% write latency. At least 3 nodes for quorum.
│   └── Multi-region                         → Sync within region + async cross-region
│       └── Accepts cross-region failover is manual (RPO may be >0 for region loss)
│
├── RPO < 1s, RTO < 5min (minimal data loss)
│   ├── PostgreSQL                            → Async streaming replication + WAL archiving
│   │   └── `synchronous_commit = remote_write` for near-sync with better perf
│   └── MySQL                                 → Semi-sync replication
│       └── `rpl_semi_sync_master_wait_for_slave_count = 1`
│
├── RPO < 1min, RTO < 30min (tolerate some loss)
│   ├── PostgreSQL                            → Async streaming + WAL-G/PgBackRest with 1min archive_timeout
│   └── MySQL                                 → Async replication + binlog backup every 5min
│
└── RPO < 1hr (cost-optimized)
    └── Either engine                         → Async replication + periodic pg_dump/mysqldump
        └── Consider if the business can truly tolerate this before choosing
```

### Sharding Strategy Decision

```
Sharding trigger: single instance can't handle load after optimizing queries + caching + read replicas?
├── Data model is tenant-isolated (SaaS, multi-tenant)
│   ├── <100 tenants, simple queries          → Schema-per-tenant on a larger instance
│   ├── 100-1000 tenants, moderate load        → Database-per-tenant on pooled instances
│   └── 1000+ tenants, high isolation needed   → Citus or Vitess with tenant as shard key
│
├── Data has a natural partition key (customer_id, org_id, timestamp)
│   ├── Time-series, append-heavy              → Time-based range partitioning (native PostgreSQL/MySQL)
│   │   └── Archive old partitions to cheaper storage
│   ├── Random access, grows unbounded         → Hash sharding (Vitess, Citus, application-level)
│   │   └── Rebalancing cost: O(N/M) data movement when adding shards
│   └── Geo-distributed users                  → Directory-based sharding by region/user location
│       └── Adds routing layer complexity but minimizes cross-region latency
│
└── No natural partition key, cross-shard queries required
    └── Reconsider sharding. Try: read replicas, caching, vertical scaling, specialized databases.
        Cross-shard JOINs and transactions are the #1 source of sharding regret.
```

### Connection Pooling Decision

```
Database engine and client pattern?
├── PostgreSQL
│   ├── Long-lived app servers (Python, Java, Go services)
│   │   ├── < 50 concurrent connections → Built-in connection pool (HikariCP, asyncpg pool)
│   │   ├── 50-500 connections → PgBouncer (transaction mode)
│   │   └── 500+ connections → PgBouncer + read/write split with HAProxy or pgpool-II
│   │
│   └── Serverless / Lambda (ephemeral connections) → RDS Proxy or PgBouncer with short timeouts
│       └── Prevents connection storm from cold starts
│
├── MySQL
│   ├── Simple applications → Built-in pooling (HikariCP, mysql2 pool)
│   ├── Complex routing (read/write split, sharding-aware) → ProxySQL
│   └── AWS RDS → RDS Proxy (IAM auth, TLS, serverless-friendly)
│
└── Managed cloud DB (RDS, Cloud SQL, AlloyDB)
    └── Check managed proxy offering first (RDS Proxy, Cloud SQL Auth Proxy)
        └── Reduces operational burden; built-in IAM + secret rotation
```

### Backup Strategy Decision

```
Recovery requirements?
├── PITR required (recover to any point in time)
│   ├── PostgreSQL → WAL archiving (WAL-G, PgBackRest) + periodic base backups
│   │   └── Base backup: daily. WAL archive: continuously. Retention: 7-30 days.
│   └── MySQL → Binary log streaming + periodic full backups (XtraBackup)
│       └── Full backup: daily. Binlog retention: >= 2 full backup cycles.
│
├── Daily recovery point acceptable, < 1hr restore
│   └── Logical backup (pg_dump, mysqldump) + WAL/binlog for gap filling
│       └── Compress and encrypt. Test restore monthly.
│
└── DR / cross-region
    └── Physical backup replicated to secondary region (WAL-G with S3 cross-region replication)
        └── Warm standby in DR region if RTO < 15min. Cold standby if RTO < 4hrs.

**What good looks like:** The output opens correctly in the target tool. All validations pass. No placeholder content remains.

```

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
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

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
DBREs sit at the intersection of infrastructure, application, and data. Schema changes break applications,
replication lag breaks dashboards, and connection exhaustion causes outages. Coordination prevents these.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Backend Developer** | Schema migrations, query patterns, N+1 queries, connection management | Migration safety review, query optimization recommendations, connection pool sizing, ORM configuration |
| **Database Designer** | Schema design decisions, normalization tradeoffs, index strategy | Access patterns, query frequency, expected data volume, SCD requirements |
| **DevOps Engineer** | Infrastructure provisioning, backup scheduling, monitoring setup | Instance sizing, replication topology, backup retention, monitoring thresholds, Terraform/Pulumi configs |
| **Observability Engineer** | Database monitoring, alerting rules, SLO dashboards | Connection metrics, query performance metrics, replication lag, deadlock counts, storage forecasts |
| **Data Engineer** | ETL/ELT pipeline impact, CDC setup, read replica access | Replication slot management, WAL disk usage from stuck replication slots, query impact on primary performance |
| **Security Engineer** | Encryption, access control, audit logging, PII handling | Encryption at rest/transit configuration, IAM integration, audit logging requirements, column-level access |
| **Incident Responder** | Database outages, replication failures, data corruption | Runbooks, escalation procedures, rollback procedures, failover decision trees |
| **Chaos Engineer** | Database failure injection, failover testing, connection exhaustion | Failure mode documentation, steady-state metrics, blast radius definition, recovery procedures |
| **Cost Optimization (FinOps)** | Instance right-sizing, reserved instances, storage tiering | Utilization metrics, growth forecasts, managed vs self-hosted cost comparisons |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| Schema migration that locks table for > 1s | Backend Developer, DevOps Engineer | Potential production impact; schedule during low-traffic window |
| Replication lag > 10s or growing | Backend Developer, Data Engineer, Observability | Read replicas serving stale data; CI/CD pipeline may need pausing |
| Connection pool > 80% capacity | Backend Developer, DevOps Engineer | Imminent connection exhaustion; scale pool or add instances |
| Storage > 75% or < 7 days remaining | DevOps Engineer, Data Engineer | Provision additional storage or archive data before outage |
| Backup failure (any) | DevOps Engineer, Incident Responder (if consecutive) | Backup gap extends RPO; investigate immediately |
| Deadlock rate spike | Backend Developer | Application transaction design issue; update ordering problem |
| Vacuum wraparound approaching (PostgreSQL) | DevOps Engineer | Critical — database will shut down if not resolved; escalate immediately |

### Escalation Path

```
Database down / unreachable? → DevOps Engineer → Incident Responder (SEV1)
Replication completely broken? → DevOps Engineer → Incident Responder (SEV2)
Data corruption detected? → DevOps Engineer → Incident Responder → Security Engineer (if malicious)
Performance degradation affecting users? → Backend Developer → Observability → Incident Responder
Cost anomaly (5x normal spend)? → FinOps → Cloud Architect → CTO Advisor
Vacuum wraparound imminent? → DevOps Engineer → Incident Responder (SEV1 — database will shut down)
```

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
- **What changes**: DBRE = you're also the backend developer and DevOps. Single database instance, nightly pg_dump backup to S3. Monitoring: database alerts go to your phone. HA: accept downtime for patching. Connection pool: app-level only.
- **What to skip**: Replication. Automated failover. PITR. Connection pooling middleware. Multi-AZ. DR site. Fleet management. Sharding. Read replicas.
- **Coordination**: Self-contained. Monitor via cloud provider dashboard.
- **Cost**: $20-50/month (managed small instance). Free tier often sufficient.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Primary + 1 read replica (or 1-2 async replicas). Automated backups with WAL archiving (PITR possible). Connection pool: PgBouncer or app-level pool with max limits. Monitoring: basic dashboard + alerts. HA: manual failover with runbook. Schema migrations: versioned migrations with expand-contract for non-trivial changes.
- **What to skip**: Multi-AZ auto-failover (if using managed, it's included). Sharding. Read/write split routing layer. DR site (backups to different region enough). Fleet management automation.
- **Coordination**: Coordinate with backend developers on slow queries. Share migration plans before execution. Weekly review of database metrics.
- **Cost**: $100-500/month (managed with read replica + backup storage).

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: HA: auto-failover (Patroni + etcd, or managed Multi-AZ). Read replicas: 2+ for load distribution + failover candidates. PITR with 1-minute granularity. Connection pooling: PgBouncer/ProxySQL with read/write split. Monitoring: per-query performance, SLO dashboards, replication lag alerts. DR site: warm standby in different region. Schema migrations: strict expand-contract, no locking DDL in production. Fleet management: standardized provisioning and monitoring.
- **What to skip**: Full sharding (use vertical scaling + read replicas until they fail). Multi-master replication (complexity rarely justified). Real-time cross-region replication (async adequate for most).
- **Coordination**: Bi-weekly schema review with backend team. Monthly capacity review with DevOps. Quarterly DR failover drill with incident response team.
- **Cost**: $1K-5K/month (managed HA + replicas + backup + DR). Add $500-2K/month for self-hosted tooling.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multiple database clusters per service, some sharded (Vitess, Citus). Multi-region active-active or active-passive with sub-minute failover. Full observability: query performance, lock contention, bloat, vacuum, replication, and capacity in unified dashboard. Database change management: CI/CD pipeline with automated migration safety checks (linter for locking DDL, long-running queries). Fleet management at scale: 50+ instances, standardized tooling, self-service provisioning for teams. Cost optimization: reserved instances, storage tiering, archival automation. Runbooks for 20+ failure scenarios.
- **What's full production**: Database reliability as a platform service — teams request databases via API/Terraform, get monitoring/backup/HA by default. Chaos engineering for databases: automated failover drills. Anomaly detection: ML-based query performance and storage forecasting. Database load testing in CI/CD pipeline.
- **Coordination**: Database architecture review board (bi-weekly). Cross-team schema compatibility checks. Monthly FinOps review. Quarterly multi-region DR test.
- **Cost**: $10K-100K+/month depending on scale. Reserved instances save 30-50%. Data transfer costs dominate multi-region setups.

### Transition Triggers
- **Solo → Small**: >100 users. First paying customers. Downtime costs real money (>$100/hr). Manual backup restore too slow.
- **Small → Medium**: >10K users. Read replica needed. Replication lag causing data inconsistencies. Connection pool exhaustion.
- **Medium → Enterprise**: >1M users. Compliance requirements (SOC 2, HIPAA). Multiple teams with shared database dependencies. Single instance cannot scale vertically.


### Cross-skills Integration
```bash
# Schema design → Database reliability → Infrastructure reliability
/database-designer && /database-reliability-engineer && /site-reliability-engineer
# Data pipeline → Database operations → Deployment automation
/data-engineer && /database-reliability-engineer && /devops-engineer
# Database designers define schemas. DBREs ensure reliability at scale. SREs and DevOps handle infrastructure and deployment.
```

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `ha-architecture` | Designing high availability: auto-failover, quorum, split-brain prevention | Patroni, etcd, multi-AZ, failover testing, quorum design, witness nodes |
| `replication-strategy` | Setting up replication: async, sync, semi-sync, logical, cross-region | RPO/RTO tradeoffs, replication lag monitoring, conflict resolution, failover procedures |
| `query-optimization` | Slow queries, performance degradation, scaling bottlenecks | EXPLAIN ANALYZE, index design, query rewriting, statistics, plan caching, hint usage |
| `connection-pooling` | Connection exhaustion, serverless connection storms, multi-app access | PgBouncer, ProxySQL, pool sizing, transaction vs session mode, read/write split routing |
| `backup-recovery` | Backup strategy, PITR setup, disaster recovery planning | WAL-G, PgBackRest, XtraBackup, backup validation, restore drills, PITR procedures |
| `sharding-design` | Scaling beyond single instance, multi-tenant isolation | Range/hash/directory sharding, Vitess/Citus, resharding, cross-shard query handling |
| `migration-strategy` | Schema changes, data migrations, zero-downtime requirements | Expand-contract, online DDL (gh-ost, pt-online-schema-change), backfill, dual-write |
| `fleet-management` | Managing many databases at scale, standardization, self-service | Terraform, Ansible, configuration management, provisioning automation, lifecycle management |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Backup that isn't tested doesn't exist** — Automate weekly restore tests. The first time you test a restore should NOT be during an incident.
- **Connection pooling is mandatory, not optional** — Every PostgreSQL/MySQL instance serving >5 application instances needs PgBouncer or ProxySQL in front. Default max_connections is a trap.
- **Autovacuum must be aggressive on large tables** — Default `scale_factor = 0.2` is designed for 2005-era storage. Set to 0.01-0.05 for tables > 100GB. Monitor dead tuple ratio.
- **Index with purpose, not panic** — Every index must serve a specific, measured query. Review unused indexes monthly (`pg_stat_user_indexes.idx_scan = 0`) and drop them. Each index costs writes.
- **Never run locking DDL in production without review** — `ALTER TABLE ... ADD COLUMN DEFAULT ... NOT NULL` rewrites entire table. Use expand-contract: add nullable → backfill → set NOT NULL → set DEFAULT.
- **Replication lag is a leading indicator of trouble** — Lag grows before disks fill, before queries time out, before failover fails. Alert on lag > 5s. Investigate lag > 2s.
- **Monitor storage growth rate, not just absolute usage** — Knowing you're at 60% is useless without knowing you're consuming 5%/day. Calculate days-until-full and alert at 14 days.
- **PITR requires continuous WAL archiving** — If WAL archiving has a gap, PITR is incomplete. Monitor `pg_stat_archiver` for failures. Archive timeout ≤ 1min for RPO < 1min.
- **Fleet management scales through standardization** — Every database in your fleet should be provisioned identically (same extensions, same autovacuum settings, same backup schedule). Differences are bugs.
- **DR testing is quarterly, not optional** — If you haven't failed over to DR this quarter, you don't have DR. Record actual RPO/RTO and track improvement over time.


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Permission denied` | Missing file/system permissions | Use `chmod +x` or `sudo`; check user/group ownership |
| `command not found` | Required tool not installed | Install with `apt install`, `brew install`, or `npm install -g` |
| `File exists` | Output file already exists | Use `--force` flag or specify different output path |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  SLOs documented: RPO (data loss tolerance), RTO (recovery time target), availability target (99.9%+), with explicit downtime budget
- [ ] **[S2]**  HA topology designed and tested: auto-failover (Patroni, InnoDB Cluster, or managed HA), quorum prevents split-brain
- [ ] **[S3]**  Replication configured: streaming with appropriate sync level for RPO, WAL/binary log archiving continuous
- [ ] **[S4]**  Connection pooling deployed: PgBouncer/ProxySQL/RDS Proxy sized for peak connections + 50% headroom
- [ ] **[S5]**  Backup verified: weekly automated restore tests pass; PITR drill completed within last quarter
- [ ] **[S6]**  DR site tested: quarterly failover drill measures actual RPO/RTO against targets; runbook updated
- [ ] **[S7]**  Monitoring dashboard: query latency (p50/p95/p99), throughput, connections, replication lag, storage, bloat, errors
- [ ] **[S8]**  Alerts configured: replication lag > 5s, storage > 75%, connections > 80% pool, backup failure, deadlock spike, vacuum wraparound approaching
- [ ] **[S9]**  Query optimization: top 20 slow queries identified and indexed; unused indexes reviewed and dropped
- [ ] **[S10]**  Autovacuum tuned: scale_factor reduced for large tables; dead tuple ratio monitored; anti-wraparound alerting in place
- [ ] **[S11]**  Schema migrations safe: expand-contract for all changes; no locking DDL without explicit review; rollback plan for every migration
- [ ] **[S12]**  Capacity plan: 90-day growth trends tracked; upgrade timeline forecast 30 days before hitting 70% of any resource limit
- [ ] **[S13]**  Fleet standardized: all instances provisioned with identical configuration; database schemas in source control (migrations)
- [ ] **[S14]**  Runbooks exist for: primary failure, replication breakage, storage full, connection exhaustion, data corruption, backup restoration
- [ ] **[S15]**  Security: encryption at rest and in transit enabled; audit logging for sensitive data access; IAM-based access control; no shared superuser credentials

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [HA & DR Architecture Patterns](references/ha-dr-architecture.md) — Patroni, RPO/RTO design, failover topologies, split-brain prevention, DR site design
- [Query Optimization & Index Strategy](references/query-optimization.md) — EXPLAIN ANALYZE deep dive, index types, covering/partial indexes, query rewriting patterns
- [Backup & Recovery Runbook](references/backup-recovery.md) — WAL-G/PgBackRest, PITR procedures, backup validation, restore drills, corruption recovery
- [Migration & Expand-Contract Patterns](references/migration-strategies.md) — Zero-downtime schema changes, online DDL tools, backfill strategies, rollback procedures
- [Fleet Management at Scale](references/fleet-management.md) — Terraform/Pulumi provisioning, configuration standardization, lifecycle automation, cost optimization
- PostgreSQL Documentation — Chapter 25: Backup and Restore, Chapter 30: Reliability, Chapter 68: GiST/GIN/BRIN indexes
- MySQL Documentation — Chapter 7: Backup and Recovery, Chapter 17: InnoDB, Chapter 18: Replication
- Database Reliability Engineering (Campbell, Majors) — The SRE approach to databases
- https://www.citusdata.com/blog/ — Practical PostgreSQL at scale
- https://www.percona.com/blog/ — MySQL and MongoDB operations
