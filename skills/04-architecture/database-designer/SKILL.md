---
name: database-designer
description: 'Schema design, normalization/denormalization, indexing strategies, database migrations, SQL vs NoSQL selection, query optimization, data modeling, and performance tuning. Trigger: database
  design, schema, indexing, migrations, normalization, SQL, NoSQL, data modeling, query optimization.'
author: Sandeep Kumar Penchala
type: architecture
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- database-designer
token_budget: 4000
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - api-designer
  - backend-developer
  - idea-to-spec
  - system-architect
  feeds_into:
  - api-designer
  - backend-developer
  - data-engineer
  - database-reliability-engineer
  - fullstack-developer
  - migration-architect
  - performance-engineer
---
# Database Designer

Design efficient, scalable, and maintainable database schemas across relational and NoSQL paradigms. This skill covers logical and physical data modeling, normalization levels, indexing strategies, migration management, query performance optimization, and database technology selection based on access patterns and consistency requirements.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Design a new schema from scratch → Start at "Decision Trees > SQL vs NoSQL Database Selection"
├── Normalize or denormalize an existing schema → Jump to "Core Workflow > Phase 2 (Normalization & Denormalization)"
├── Design an indexing strategy → Go to "Core Workflow > Phase 3 (Indexing Strategy)"
├── Plan a database migration → Jump to "Core Workflow > Phase 4 (Migration Planning)"
├── Choose between relational, document, or graph → Start at "Decision Trees > SQL vs NoSQL" then "Data Modeling Patterns"
├── Optimize a slow query → Go to "references/query-optimization-guide.md"
├── Model time-series or event data → Jump to "Data Modeling > Time-Series & Event Sourcing"
├── Need the overall system architecture first → Invoke system-architect skill instead
├── Need API design that this schema supports → Invoke api-designer skill instead
├── Need backend implementation using this schema → Invoke backend-developer skill instead
├── Need to build data pipelines (ETL/ELT) → Invoke data-engineer skill instead
├── Need database reliability and operations → Invoke database-reliability-engineer skill instead
└── Don't know where to start? → Describe your data and access patterns and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never recommend without knowing access patterns.** Schema design depends on how you query the data. Always ask: "What queries run most often? At what volume?" Do not design tables without knowing the queries.
- **Migrations must be reversible.** Every `up` migration needs a tested `down`. Do not ship a migration without a rollback path — expand-contract for zero-downtime changes.
- **Don't optimize prematurely without query plans.** Never add an index because it "seems right." Run `EXPLAIN ANALYZE` first, add the index, then verify the query plan improved. Do not index by intuition.
- **Always consider data growth.** A schema that works at 10K rows may collapse at 10M. Estimate growth trajectory and design accordingly.
- **Admit what you don't know.** If you haven't seen the query patterns, data volume estimates, or consistency requirements, say so and ask before designing.

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
<!-- DEEP: 10+min -->
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
<!-- DEEP: 10+min -->
1. Use `EXPLAIN ANALYZE` to profile slow queries.
2. Identify table scans (`Seq Scan` on large tables), N+1 queries, missing indexes, stale statistics.
3. **Rewrite queries**: Replace correlated subqueries with JOINs or `LATERAL`, use `WHERE EXISTS` instead of `IN` for large sets, avoid `SELECT *`, add `LIMIT` where appropriate.
4. **Connection pooling**: PgBouncer (transaction mode) or built-in pool (HikariCP for JVM, `asyncpg` pool for Python).
5. **Read replicas**: Route read queries to replicas; accept replication lag for non-critical reads.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | system-architect | Data flow diagrams, storage requirements, consistency/availability tradeoffs |
| **This** | database-designer | Schema designs, indexing strategies, migration plans, query optimization |
| **After** | backend-developer | Implements repository layer, ORM models, query patterns per schema |

Common chains:
- **Greenfield data model**: system-architect → database-designer → backend-developer — Architecture defines data boundaries, DB design creates the schema, backend codes the access layer
- **API-driven schema**: api-designer → database-designer → database-reliability-engineer — API resources define data shape, DB designs for those access patterns, DBRE ensures reliability at scale

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

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | Bounded context map, data ownership boundaries, multi-tenancy model, scaling strategy | Before designing the logical data model; ensures schema aligns with service topology |
| `api-designer` | Access patterns (read/write ratios), query patterns, expected QPS, pagination strategy | Before designing tables and indexes; query patterns drive schema design |
| `backend-developer` | ORM/framework constraints, connection pooling requirements, transaction boundary needs | Before finalizing schema for ORM compatibility and query construction patterns |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `backend-developer` | ERD, schema DDL, indexing strategy, migration scripts (up + down), query performance baselines | Backend can't implement data access layer without schema — blocked development |
| `data-engineer` | Read replica access patterns, CDC configuration, schema compatibility contract, data freshness SLAs | ETL pipelines break on schema drift; BI reports go stale |
| `database-reliability-engineer` | Instance sizing requirements, connection pool settings, backup/RPO-RTO targets, HA topology | Database may be provisioned incorrectly — performance incidents in production |
| `api-designer` | Query complexity feedback, N+1 risk flags, response shape constraints from data model | API endpoints may be designed that the database can't support efficiently |

### Escalation Path

```
Database emergency (data corruption, production data loss, cascading query failure)
  └── Database Designer + DevOps + System Architect + Backend Lead. War room. Point-in-time recovery or rollback within hours.

Schema migration that blocks 3+ teams or requires coordinated multi-service deploy
  └── Database Designer + System Architect + all affected team leads. Migration plan, compatibility window, rollback plan.

Routine schema change (new column, index addition, non-breaking type change)
  └── Database Designer reviews PR, team deploys with migration. No escalation needed.
```


**What good looks like:** ERD covers all entities with named relationships and cardinalities. The 10 most expensive query patterns each have an EXPLAIN plan showing sequential scans eliminated by the chosen index strategy. Migration scripts have both up and down paths tested in CI. The schema survives a production load test at 2x peak QPS without connection pool exhaustion or lock contention.
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

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Production database locked up for 20 minutes during deployment | Migration added `ALTER TABLE orders ADD COLUMN status TEXT NOT NULL DEFAULT 'pending'` — PostgreSQL rewrote the entire 50M-row table, holding an ACCESS EXCLUSIVE lock | Kill the stuck migration, restore from replica. Use multi-step: add nullable column, backfill in batches (10K rows per batch), then `ALTER COLUMN SET NOT NULL` with `DEFAULT` | **Never add NOT NULL columns with DEFAULT in one step on large tables.** Always use expand-contract: add nullable, backfill in batches, set NOT NULL. Test migrations on a staging copy of production data first |
| Dashboard query timed out at 90 seconds every morning | Users table joined with orders table with no index on `orders.user_id` — sequential scan on 10M-row orders table | `CREATE INDEX idx_orders_user_id ON orders(user_id);` Query dropped to 12ms. Run `EXPLAIN ANALYZE` on all queries before deploying | **Every join column needs an index, not just primary keys.** Profile queries with `EXPLAIN ANALYZE` in CI before merging code. A missing index is the #1 cause of unexpected production slowdowns |
| Currency calculations were off by $0.01 after 10,000 transactions | Monetary values stored as `FLOAT` instead of `NUMERIC(19,4)` — floating point rounding errors accumulated | `ALTER TABLE transactions ALTER COLUMN amount TYPE NUMERIC(19,4);` Recalculate all historical balances. Add CHECK constraint `amount >= 0` | **Never use FLOAT/DOUBLE for monetary values.** Floating-point rounding errors compound over thousands of transactions. `NUMERIC(19,4)` for money, always. Add `CHECK` constraints at the database level for business rules |
| Production went down because connection pool was empty | Application was not releasing connections after database queries — 50 connections leaked per minute, pool of 100 exhausted in 2 minutes | Restart application servers to drain leaked connections. Add connection leak detection (set `idle_in_transaction_session_timeout` to 30s). Implement connection pool monitoring with P95 usage alert at 70% | **Connection pools need monitoring, timeouts, and leak detection.** Set statement timeout, idle-in-transaction timeout, and connection leak detection. Alert on pool usage before exhaustion |
| Migration rollback failed — data was lost irrecoverably | Migration removed a column, and the rollback migration tried to re-add it — but couldn't recover the dropped data | Restore from point-in-time recovery (PITR). Implement expand-contract pattern: never drop columns in a single migration; mark as deprecated, wait 2 release cycles, then drop | **Every destructive migration must have a tested rollback path.** Use expand-contract for all column drops. Never drop a column without verifying zero queries reference it. PITR is not a rollback strategy — it's disaster recovery |


## What Good Looks Like

> Every query in the application is backed by an index that makes it run in single-digit milliseconds, and `EXPLAIN ANALYZE` output confirms index-only scans on every critical path — no sequential scans hiding in production. The schema is normalized to 3NF with deliberate, documented denormalizations where read performance demands it, and no one has ever said "we'll fix the schema later" in a code review. Migrations apply in under 30 seconds with zero downtime via expand-contract patterns, and rollback plans are practiced, not theorized. Connection pools are sized so peak Black Friday traffic never exhausts them, and slow-query logs are empty for days at a time. Backups run on schedule, restores are exercised quarterly, and the team can answer "what was the state of this row at 3:14 PM last Tuesday?" because point-in-time recovery just works.

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
