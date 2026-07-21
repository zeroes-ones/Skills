---
name: database-designer
description: Schema design, normalization/denormalization, indexing strategies, database migrations, SQL vs NoSQL selection, query optimization, data modeling, and performance tuning. Trigger: database design, schema, indexing, migrations, normalization, SQL, NoSQL, data modeling, query optimization.
author: Sandeep Kumar Penchala
type: architecture
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - database-designer
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
---
# Database Designer

Design efficient, scalable, and maintainable database schemas across relational and NoSQL paradigms. This skill covers logical and physical data modeling, normalization levels, indexing strategies, migration management, query performance optimization, and database technology selection based on access patterns and consistency requirements.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Designing a new database schema for a greenfield application
- Choosing between SQL (PostgreSQL, MySQL) and NoSQL (MongoDB, DynamoDB, Cassandra, Redis)
- Normalizing or denormalizing existing schemas for performance or consistency
- Designing indexing strategies for query performance optimization
- Planning database migrations with zero-downtime strategies (expand-contract)
- Data modeling for specific access patterns (OLTP vs OLAP, time-series, graph, full-text search)
- Auditing and optimizing slow queries (EXPLAIN ANALYZE, query plan analysis)
- Designing sharding, partitioning, or replication topologies

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### SQL vs NoSQL Database Selection
```
                     ┌──────────────────────────┐
                     │ START: New data store     │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Schema known upfront,      │
                    │ needs ACID transactions?   │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ PostgreSQL  │   │ Schema evolves   │
                    │ (default)   │   │ rapidly or nested│
                    └─────────────┘   │ documents?      │
                                      └────┬────────┬───┘
                                           │ YES    │ NO
                                      ┌────▼────┐ ┌▼──────────┐
                                      │ MongoDB │ │ Key-Value  │
                                      │         │ │ (Redis/    │
                                      │         │ │ DynamoDB)  │
                                      └─────────┘ └────────────┘
```
**When to choose PostgreSQL:** Structured data, complex JOINs/aggregations, >90% of use cases — start here unless a specific NoSQL advantage is clear. **When to choose MongoDB:** Rapidly evolving schema, deeply nested JSON documents, no cross-document JOINs needed. **When to choose Key-Value:** Simple GET/SET access patterns, p99 latency <5ms required, caching/session store.

### When to Add an Index
```
                     ┌──────────────────────────┐
                     │ START: Query runs >50ms   │
                     │ p95 on production         │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ EXPLAIN shows Seq Scan     │
                    │ on table >10K rows?        │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Add index   │   │ Query is fine — │
                    │ on filtered │   │ check for N+1   │
                    │ columns     │   │ or app-side     │
                    └────┬────────┘   │ issues          │
                         │            └────────────────┘
                    ┌────▼────────┐
                    │ Verify with  │
                    │ EXPLAIN after│
                    │ (target: <5ms│
                    │  Index Scan) │
                    └──────────────┘
```
**When to add index:** Seq Scan on >10K rows, query runs >100× per minute, filtered column cardinality >100 distinct values. **When NOT to add index:** Table <1K rows, write-heavy table (>100 writes/sec) where read:write ratio <10:1, column with <10 distinct values.

### Normalize to 3NF vs Denormalize
```
                     ┌──────────────────────────┐
                     │ START: Data modeling      │
                     │ decision point            │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Read:Write ratio > 100:1   │
                    │ AND read latency >20ms?    │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Denormalize │   │ Normalize to    │
                    │ specific    │   │ 3NF — data      │
                    │ column(s)   │   │ integrity first │
                    └─────────────┘   └────────────────┘
```
**When to denormalize:** Read:write >100:1, read p95 >20ms, denormalized column is small (<100 bytes), <1% of writes trigger the denormalized update. **When to keep 3NF:** Read:write <10:1, write correctness critical (financial data), data changes must propagate instantly.

### Online vs Maintenance-Window Migration
```
                     ┌──────────────────────────┐
                     │ START: Schema change on   │
                     │ production table >1M rows │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Adding nullable column     │
                    │ or new index?              │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Online —     │   │ Adding NOT NULL │
                    │ safe, <1s    │   │ with DEFAULT?   │
                    │ lock         │   └────┬────────┬───┘
                    └──────────────┘        │ YES    │ NO
                                       ┌────▼────┐ ┌▼──────────┐
                                       │ Expand- │ │ Maintenance│
                                       │ Contract│ │ window (off│
                                       │ (multi-  │ │ -peak, <1h)│
                                       │ step)    │ └────────────┘
                                       └──────────┘
```
**When to use Expand-Contract:** NOT NULL + DEFAULT on >1M rows, column rename/drop, type change. Steps: add nullable → backfill → set NOT NULL → add DEFAULT → drop old. **When maintenance window is acceptable:** Off-peak traffic <10% of peak, RTO <1hr acceptable, table <1M rows.

### Sharding Decision
```
                     ┌──────────────────────────┐
                     │ START: DB approaching     │
                     │ capacity limits           │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Read replicas and vertical │
                    │ scaling already exhausted? │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ >10TB data  │   │ Add replicas or │
                    │ OR >10K     │   │ scale up first  │
                    │ writes/sec? │   └────────────────┘
                    └────┬────────┘
                         │ YES
                    ┌────▼────────┐
                    │ Shard —      │
                    │ budget $500K │
                    │ + 6mo + 2    │
                    │ DBREs        │
                    └──────────────┘
```
**When to shard:** Data >10TB, writes >10K/sec sustained, read replicas maxed out (5+), vertical scaling ceiling hit (r6i.8xlarge). **When NOT to shard:** <1TB data, <5K writes/sec, can add read replicas, team <5 engineers — sharding costs $500K+/year.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Requirements Analysis & Technology Selection
1. **Identify access patterns**: Read-heavy vs write-heavy, query shapes (point lookups, range scans, aggregations, joins, full-text search), expected QPS and data volume.
2. **Define consistency requirements**: Strong consistency (ACID) vs eventual consistency (BASE), conflict resolution strategy (LWW, CRDTs, application-level merging).
3. **Choose database type**:
   - **Relational (PostgreSQL/MySQL)**: Complex joins, transactions, structured data, reporting. Default choice unless specific NoSQL need exists.
   - **Document (MongoDB)**: Flexible schema, nested/denormalized documents, rapid iteration, JSON-native workflows.
   - **Key-Value (Redis/DynamoDB)**: Simple access patterns, ultra-low latency, caching, session storage.
   - **Wide-Column (Cassandra/ScyllaDB)**: High write throughput, time-series, append-only, known query patterns.
   - **Graph (Neo4j/Amazon Neptune)**: Highly connected data, relationship traversal, recommendation engines.
   - **Search (Elasticsearch/OpenSearch)**: Full-text search, faceted navigation, log analytics.
   - **Time-Series (TimescaleDB/InfluxDB)**: Metrics, IoT sensor data, monitoring, financial tick data.

### Phase 2 (~30 min): Logical & Physical Data Modeling
1. **Entity-Relationship Modeling**: Identify entities, attributes, relationships (1:1, 1:N, M:N), and cardinality constraints.
2. **Normalization**: Apply 1NF (atomic values), 2NF (no partial dependencies), 3NF (no transitive dependencies). Stop at 3NF for OLTP; BCNF/4NF only for complex cases.
3. **Denormalization**: Intentionally duplicate data for read performance. Common in CQRS read models, reporting tables, and NoSQL design. Document each denormalization decision.
4. **Data types**: Use the most specific type (`UUID` not `VARCHAR(36)`, `TIMESTAMPTZ` not `TIMESTAMP`, `NUMERIC(19,4)` for money, `INET` for IP addresses). Leverage domain-specific types: `JSONB` in PostgreSQL for semi-structured data, `ltree` for hierarchical paths, `PostGIS` for geospatial.
5. **Constraints**: `NOT NULL` by default, `CHECK` constraints for business rules, `UNIQUE` on natural keys, `FOREIGN KEY` where referential integrity matters.

### Phase 3 (~20 min): Indexing Strategy
1. **Analyze query patterns**: Extract all queries from application code; order by frequency and latency sensitivity.
2. **Covering indexes**: Index includes all columns needed by a query, avoiding heap lookups. PostgreSQL: `CREATE INDEX idx_orders_user_status ON orders(user_id, status) INCLUDE (amount, created_at)`.
3. **Partial indexes**: Index only relevant rows: `CREATE INDEX idx_active_subscriptions ON subscriptions(user_id) WHERE status = 'active'`.
4. **Composite index column order**: Equality filters first, then range filters, then sort columns. Most selective first.
5. **Avoid over-indexing**: Each index costs storage and write performance. Monitor unused indexes (`pg_stat_user_indexes.idx_scan = 0`) and drop them.
6. **Full-text search indexes**: `GIN` indexes for `tsvector` in PostgreSQL; Elasticsearch for advanced search features.

### Phase 4 (~15 min): Migration Management
1. **Expand-Contract pattern** for zero-downtime schema changes:
   - **Expand**: Add new column/table (non-breaking).
   - **Migrate**: Backfill data, dual-write during transition.
   - **Contract**: Remove old column/table after all reads have moved.
2. **Versioned migrations**: Use Flyway, Alembic (Python), golang-migrate, or Prisma Migrate. Never apply ad-hoc schema changes.
3. **Migration safety rules** (for PostgreSQL):
   - Adding nullable column: safe.
   - Adding column with DEFAULT + NOT NULL: unsafe on large tables (rewrites entire table). Use multi-step: add nullable, backfill in batches, set NOT NULL, set DEFAULT.
   - Renaming column: unsafe (breaks existing code). Use expand-contract.
   - Dropping column/table: only after verifying zero references.
4. **Rollback planning**: Every migration must have a tested rollback path.

### Phase 5 (~25 min): Query Optimization
1. Use `EXPLAIN ANALYZE` to profile slow queries.
2. Identify table scans (`Seq Scan` on large tables), N+1 queries, missing indexes, stale statistics.
3. **Rewrite queries**: Replace correlated subqueries with JOINs or `LATERAL`, use `WHERE EXISTS` instead of `IN` for large sets, avoid `SELECT *`, add `LIMIT` where appropriate.
4. **Connection pooling**: PgBouncer (transaction mode) or built-in pool (HikariCP for JVM, `asyncpg` pool for Python).
5. **Read replicas**: Route read queries to replicas; accept replication lag for non-critical reads.


### Cross-skills Integration
The preceding skill in the chain documents output format requirements. The following skill in the chain expects that format. Run them sequentially:
```bash
#[previous-skill] && #[this-skill] && #[next-skill]
```
Document the output contract explicitly so consuming skills know what to expect.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
When this skill is invoked, drill into these specialized areas as needed:

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `schema-design` | New project, new feature | This file — Phase 2: Schema Design |
| `query-optimization` | Slow queries, scaling issues | This file — Phase 3 + Index Strategy section |
| `migration-strategy` | Schema changes, zero-downtime | This file — Phase 1: Migration Planning |
| `multi-tenancy` | SaaS, B2B | This file — Phase 2: Schema Design patterns |
| `backup-recovery` | DR planning, compliance | This file — Production Checklist section |
| `database-selection` | New project, scaling event | This file — When Postgres is All You Need |

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Database design touches every layer of the stack. A schema mistake cascades into application bugs, performance incidents, and migration pain — coordination prevents this.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **System Architect** | New service data needs, CQRS/event sourcing, multi-tenancy model | Data model, access patterns, consistency requirements, read/write ratios, scaling strategy |
| **API Designer** | API endpoints that query or mutate data, N+1 risks, response shape | Query patterns, expected QPS, pagination strategy, field-level access, response size budgets |
| **Backend Developer** | ORM usage, query construction, migration tooling, connection management | Schema design, migration scripts, query review, connection pool settings, transaction boundaries |
| **Performance Engineer** | Slow queries, index optimization, connection pool sizing, read replica routing | Query execution plans, hot queries, workload patterns (OLTP/OLAP), cache hit rates |
| **DevOps / Platform Engineer** | Database provisioning, backup/recovery, DR planning, monitoring | Instance sizing, HA configuration, backup schedule, RPO/RTO, monitoring thresholds |
| **Security Engineer** | Data classification, encryption (at rest, in transit), PII handling, audit logging | Sensitive data identification, encryption strategy, column-level access, data retention policy |
| **Data Engineer / Analytics** | ETL/ELT pipelines, data warehouse, BI integration, CDC | Read replica access, change data capture, schema compatibility, impact of schema changes on pipelines |
| **Migration Architect** | Database migration (expand-contract, dual-write, backfill) | Schema evolution plan, data migration scripts, consistency verification, rollback strategy |
| **Chaos Engineer** | Database failure injection (primary failure, replica lag, connection exhaustion) | Failure modes, recovery procedures, blast radius, steady-state metrics |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Schema migration planned (new table, column change, index change) | Backend Developers, API Designer, Data Engineer | Impact on queries, API responses, ETL pipelines; migration strategy (online, maintenance window) |
| Query performance degradation (p95 > 2x baseline, new sequential scan on large table) | Performance Engineer, Backend Lead, System Architect | Root cause (missing index, stats stale, data volume), fix priority, query rewrite or new index |
| Database approaching capacity (storage >70%, connections >70%, replication lag growing) | DevOps, System Architect, Performance Engineer | Scaling strategy: vertical, read replicas, sharding, archiving |
| Breaking schema change required (column rename, type change, table restructure) | All consuming services, API Designer, Data Engineer | Expand-contract migration plan, compatibility window, deprecation timeline |
| Data corruption or integrity issue detected | Security Engineer, DevOps, All consuming services | Severity assessment, point-in-time recovery, affected rows/tables, root cause |
| New data classification (PII, PCI, HIPAA compliance requirement) | Security Engineer, DevOps, Legal | Encryption, access control, audit logging, retention policy, data residency |
| Database technology evaluation (considering new DB for specific workload) | System Architect, DevOps, Performance Engineer | Evaluation criteria, benchmark results, migration complexity, operational readiness |

### Escalation Path

```
Database emergency (data corruption, production data loss, cascading query failure)
  └── Database Designer + DevOps + System Architect + Backend Lead. War room. Point-in-time recovery or rollback within hours.

Schema migration that blocks 3+ teams or requires coordinated multi-service deploy
  └── Database Designer + System Architect + all affected team leads. Migration plan, compatibility window, rollback plan.

Routine schema change (new column, index addition, non-breaking type change)
  └── Database Designer reviews PR, team deploys with migration. No escalation needed.
```


**What good looks like:** ERD covering all entities with relationships and cardinalities. Indexing strategy covers the top 10 query patterns. Migration script with rollback for each change. Query plan analysis shows sequential scans eliminated for the critical path.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Model for access patterns, not for "purity"**: Denormalize when read performance matters more than write simplicity.
- **UUIDs over auto-increment IDs** for distributed systems: UUIDv7 (time-ordered) for primary keys to avoid hot spots.
- **Soft deletes with caution**: `deleted_at` simplifies recovery but complicates every query (add `WHERE deleted_at IS NULL`). Consider archiving to separate tables instead.
- **Separate read and write models**: CQRS pattern for high-scale systems with disparate read/write patterns.
- **Connection management**: Set appropriate pool sizes (CPU cores * 2-4 for OLTP), statement timeouts, idle-in-transaction timeouts.
- **Regular maintenance**: `VACUUM ANALYZE`, index rebuilds, statistics updates, bloat monitoring.

## When Postgres is All You Need

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

## Sharding Cost Analysis

**Sharding increases complexity cost by 3-5×. Justify it:**

| Sharding Trigger | Threshold | Alternative First |
|-----------------|-----------|-------------------|
| DB CPU > 70% | Add read replicas | 3-5 replicas handle most read-heavy workloads |
| Write throughput > 5K/sec | Vertical scale (r6i.8xlarge) | $2K/month vs $100K+ in sharding complexity |
| > 10TB data | Partitioning + archiving | Partition by date, archive cold partitions to S3 |
| Multi-tenancy at scale | Database-per-tenant | Simpler than sharding; isolate noisy neighbors |

**Sharding cost:** 3-6 months initial build + 1-2 dedicated DBREs at $180K/year each + application-level routing complexity. Minimum $500K/year overhead.

## Denormalization ROI Calculator

```
For each denormalization: 
ROI = (read_latency_reduction_ms × reads_per_second × user_value_per_ms) - (write_penalty_ms × writes_per_second × write_cost_factor) - (storage_cost)

Example: Denormalizing `order_count` onto `users` table:
- Reads: 1000/s, latency down from 50ms to 5ms (45ms saved)
- Writes: 10/s, latency up from 10ms to 12ms (2ms penalty)
- Storage: 4 bytes × 1M users = 4MB — negligible
- ROI: (45ms × 1000 × 1000 reqs) - (2ms × 10 × 1000) = overwhelmingly positive

Denormalize when: read:write ratio > 100:1 and read latency > 20ms.
Do NOT denormalize when: read:write ratio < 10:1 (maintenance will kill you).
```

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Database = SQLite for dev, managed Postgres for production (Supabase/Railway). No ORM (raw SQL or lightweight query builder). Migrations = manual or simple migration tool. Backups = managed service handles it. No replication. No connection pooling beyond default.
- **What to skip**: Read replicas. Sharding. CQRS. Multi-tenancy design. PITR. Encryption-at-rest configuration. Monitoring dashboards.
- **Coordination**: You are the DBA + developer. Make schema changes whenever.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Managed Postgres with migration framework (Alembic, Prisma Migrate). ORM with escape hatches to raw SQL. Indexes on query patterns (EXPLAIN reviewed). Connection pooling (PgBouncer or built-in pool). Daily backups with PITR. Basic monitoring (slow query log, connection count).
- **What to skip**: Read replicas (unless >1000 QPS). Sharding. Multi-tenancy beyond row-level. Materialized views. CQRS. Database selection matrix (Postgres covers 95% of needs).
- **Coordination**: Schema changes reviewed in PR. Migration tested in staging before production. Weekly check on slow queries.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Read replicas for read-heavy workloads. Expand-contract migration pattern for zero-downtime. Index strategy with regular review. Materialized views for complex aggregations. Multi-tenancy design (row-level or schema-per-tenant). Monitoring dashboards (slow queries, replication lag, disk, connections). Backup + restore tested quarterly. Database selection matrix for specialized needs (search → Elasticsearch, cache → Redis).
- **What to skip**: Sharding (wait until >1TB or >10K writes/sec). CQRS with separate read/write stores (materialized views + replicas are enough). Multi-region active-active.
- **Coordination**: Schema change RFC for cross-team impact. Monthly query performance review. Quarterly backup restore test.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Dedicated DBA or database reliability team. Sharding strategy (when needed). Multi-region with failover. CQRS for high-scale domains. Data warehouse for analytics. Database CI/CD with automated migration testing. Encryption at rest + in transit + key rotation. Data retention and archival automation. Compliance audit trails (GDPR, HIPAA). Capacity planning with cost modeling.
- **What's full production**: Database reliability engineering (DRE). Automated failover testing. Chaos engineering for database. Annual capacity planning. Data governance framework.
- **Coordination**: Database reliability team weekly. Monthly capacity review. Quarterly DR test. Schema change governance board.

### Transition Triggers
- **Solo → Small**: Second developer making schema changes. Need migration framework to avoid conflicts.
- **Small → Medium**: Read load exceeds single instance capacity (>1000 QPS). First zero-downtime migration needed.
- **Medium → Enterprise**: >1TB data or >10K writes/sec. Multi-region or compliance (SOC 2, HIPAA, GDPR). >50 developers.


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `relation "..." does not exist` | Migration not run or wrong database | `npx prisma migrate dev` or check `DATABASE_URL` |
| `deadlock detected` | Concurrent transactions in wrong order | Enforce consistent lock ordering; use `NOWAIT` where appropriate |
| `connection pool exhausted` | Too many concurrent connections | Increase pool size; add connection timeout; check for leaked connections |
| `414 URI Too Long` | Request URI exceeds server limit | Use POST for data-heavy requests; paginate `?filter=` params |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Database technology selected with documented rationale for the choice
- [ ] **[S2]**  Entity-relationship diagrams (ERDs) created and peer-reviewed
- [ ] **[S3]**  Schema normalized to 3NF with deliberate, documented denormalizations
- [ ] **[S4]**  Indexing strategy aligned with all critical query patterns (EXPLAIN output reviewed)
- [ ] **[S5]**  Migration framework in place with expand-contract for production changes
- [ ] **[S6]**  Connection pooling configured with appropriate limits and timeouts
- [ ] **[S7]**  Backup strategy defined (WAL archiving, PITR, daily snapshots) with tested restore
- [ ] **[S8]**  Encryption at rest (TDE/KMS) and in transit (TLS 1.3) configured
- [ ] **[S9]**  Monitoring dashboards for slow queries, connection counts, replication lag, disk usage
- [ ] **[S10]**  Data retention and archival policy documented and automated

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/) — Performance Tips, Index Types
- [Use the Index, Luke!](https://use-the-index-luke.com/) — Markus Winand
- [Database Migrations Done Right](https://www.brunton-spall.co.uk/post/2014/05/06/database-migrations-done-right/) — Michael Brunton-Spall
- [Designing Data-Intensive Applications (Chapters 2-3, 5-7)](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) — Martin Kleppmann
- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html) — PostgreSQL Official
- [MongoDB Schema Design Best Practices](https://www.mongodb.com/docs/manual/core/data-modeling-introduction/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
