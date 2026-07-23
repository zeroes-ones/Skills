---
name: database-designer
description: >
  Use when designing database schemas, planning indexing strategies, normalizing or
  denormalizing data models, choosing between SQL and NoSQL, or optimizing query
  performance. Handles logical and physical data modeling, migration management,
  performance tuning, technology selection, and access pattern analysis. Do NOT use
  for implementing database code, configuring database servers, or designing API
  endpoints.
license: MIT
tags:
- database
- schema
- sql
- nosql
- indexing
- normalization
- migration
- performance
author: Sandeep Kumar Penchala
type: architecture
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
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
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Design efficient, scalable, and maintainable database schemas across relational and NoSQL paradigms. This skill covers logical and physical data modeling, normalization levels, indexing strategies, migration management, query performance optimization, and database technology selection based on access patterns and consistency requirements.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("schema.sql")` OR `file_exists("*.prisma")` OR `file_contains("package.json", "knex\|kysely\|drizzle\|typeorm\|sequelize")` | Schema exists. Jump to **Core Workflow** — Phase 2 (Normalization & Denormalization review). |
| A2 | `file_contains("schema.sql\|migrations/", "CREATE TABLE\|ALTER TABLE\|DROP TABLE")` AND `file_contains("*", "EXPLAIN\|query.plan\|slow.query")` | Schema changes with query concerns. Jump to **Decision Trees** — SQL vs NoSQL + Indexing Strategy. |
| A3 | `file_exists("migrations/")` AND `file_contains("migrations/*", "NOT NULL.*DEFAULT\|ADD.*COLUMN.*DEFAULT")` | Migrations with potential locking operations. Jump to **Anti-Patterns** — check for "NOT NULL with DEFAULT on large tables." |
| A4 | `file_contains("*", "shard\|partition\|horizontal.scale\|distributed\|citus\|vitess")` | Sharding/partitioning concerns. Jump to **Sharding Cost Analysis**. |
| A5 | `file_contains("*", "json\|jsonb\|document\|mongo\|couchbase\|document.store")` AND NOT `file_contains("*", "relational\|postgres\|mysql\|sqlite")` | Document store concerns. Jump to **Decision Trees** — SQL vs NoSQL Database Selection. |
| A6 | `file_contains("*", "denormaliz\|materialized.view\|precompute\|cache.table\|aggregate.table")` | Denormalization concerns. Jump to **Denormalization ROI Calculator**. |
| A7 | `file_contains("*", "time.series\|event.store\|append.only\|iot\|sensor\|clickhouse\|timescaledb")` | Time-series or event data. Jump to **Decision Trees** — Data Modeling > Time-Series Patterns. |
| A8 | `file_contains("*", "ETL\|ELT\|pipeline\|data.warehouse\|airflow\|dbt\|spark")` | This is data engineering / analytics engineering. Invoke **data-engineer** or **analytics-engineer** instead. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Design a new schema from scratch → Start at "Decision Trees > SQL vs NoSQL Database Selection"
├── Normalize or denormalize an existing schema → Jump to "Core Workflow > Phase 2 (Normalization & Denormalization)"
├── Design an indexing strategy → Go to "Core Workflow > Phase 3 (Indexing Strategy)"
├── Plan a database migration → Jump to "Core Workflow > Phase 4 (Migration Planning)"
├── Choose between relational, document, or graph → Start at "Decision Trees > SQL vs NoSQL" then "Data Modeling Patterns"
├── Optimize a slow query → Go to "references/query-optimization-guide.md"
├── Model time-series or event data → Jump to "Data Modeling > Time-Series & Event Sourcing"
├── Evaluate sharding or partitioning → Jump to "Sharding Cost Analysis"
├── Calculate denormalization trade-offs → Jump to "Denormalization ROI Calculator"
├── Need the overall system architecture first → Invoke system-architect skill instead
├── Need API design that this schema supports → Invoke api-designer skill instead
├── Need backend implementation using this schema → Invoke backend-developer skill instead
├── Need to build data pipelines (ETL/ELT) → Invoke data-engineer skill instead
├── Need database reliability and operations → Invoke database-reliability-engineer skill instead
└── Don't know where to start? → Describe your data and access patterns and I'll route you
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to design without access patterns.** Schema design depends on how you query the data — not how it looks on a whiteboard. A perfectly normalized schema that can't serve the top 3 queries is a failed design. Always ask: "What queries run most often? At what volume? What are the read-to-write ratios?" | Trigger: producing a schema design or table definition without documenting the top 3-5 query patterns (SELECTs with WHERE conditions, JOIN paths, expected frequency) that the schema must support | STOP. Ask: "Before designing: What are your top 3 queries? At what QPS? What are the most common JOIN paths? What's the expected data volume in 12 months? Schema design without access patterns is architecture without load assumptions — it will optimize for the wrong thing." |
| **R2** | **REFUSE to ship a migration without a tested rollback path.** Every `up` migration needs a corresponding `down` that has been tested in a staging environment with production-like data volumes. An untested rollback is a false sense of security — it will fail when you need it most. | Trigger: producing a migration file (SQL, Prisma, Alembic, Flyway) that contains `DROP`, `ALTER COLUMN ... TYPE`, or `ALTER TABLE ... DROP COLUMN` without a corresponding `down` migration defined in the same output | STOP. Require: "Every destructive migration (DROP, ALTER TYPE, DROP COLUMN) must include a tested `down` migration. Use expand-contract: add new column (nullable) → backfill in batches → switch reads → deprecate old column → drop in a follow-up migration after 2 release cycles." |
| **R3** | **DETECT and WARN about `NOT NULL ... DEFAULT` on large tables (> 1M rows).** This pattern holds an ACCESS EXCLUSIVE lock while rewriting the entire table — blocking all reads and writes for minutes to hours on production. This is the #1 cause of database outages during deployments. | Trigger: migration contains `ALTER TABLE ... ADD COLUMN ... NOT NULL DEFAULT` or `ALTER COLUMN ... SET NOT NULL` without a preceding batched backfill step | WARN. Rewrite: "This migration will lock [table] for the duration of a full table rewrite. Use: (1) ADD COLUMN nullable, (2) backfill in batches of 10K with `WHERE id > ? LIMIT 10000`, (3) `ALTER COLUMN SET NOT NULL` (instant on Postgres 11+ with a valid CHECK constraint). Test migration time on a staging copy of production data BEFORE deploying." |
| **R4** | **STOP and WARN about `SELECT *` in production code.** `SELECT *` breaks when columns are added/removed, fetches unused blobs over the wire, prevents index-only scans, and obscures which columns the application actually depends on. It is the root cause of ~15% of unexpected production schema-change incidents. | Trigger: code or query contains `SELECT *` or `SELECT t.*` in a non-ad-hoc context (i.e., inside application code, ORM default, or API handler) | WARN. Rewrite: "Replace `SELECT *` with explicit column list. This: (1) prevents breakage on schema changes, (2) enables index-only scans, (3) reduces network I/O, (4) documents which columns the application actually depends on. Run `scripts/detect-select-star.sh` to find all occurrences." |
| **R5** | **DETECT and WARN about missing database constraints when app-level validation exists.** App-level validation is bypassed by background jobs, direct DB access, data migrations, ORM `update_all`, and bugs. Every business rule enforced only in application code is a data corruption incident waiting to happen. | Trigger: schema has business-relevant columns (e.g., `amount`, `status`, `email`, `age`) without corresponding `CHECK`, `NOT NULL`, `UNIQUE`, or `FOREIGN KEY` constraints, but application code contains validation for those columns | WARN. Add: "Column [name] has app-level validation but no database constraint. Add: `CHECK ([condition])` at minimum. Database constraints are the last line of defense — they survive application bugs, ORM bypasses, and direct DB access forever. Application validation is a suggestion; database constraints are a guarantee." |
| **R6** | **REFUSE to recommend an index without `EXPLAIN` evidence.** Never add an index because it "seems right." Every index costs write performance and storage. The query planner may ignore it due to low cardinality, outdated statistics, or a better sequential scan plan. | Trigger: recommending `CREATE INDEX` or adding an index to a migration without showing `EXPLAIN (ANALYZE, BUFFERS)` output before and after the index | STOP. Require: "Run `EXPLAIN (ANALYZE, BUFFERS) [query]` on production-like data volumes. Show the plan before and after the index. Verify: (1) the index is actually used (Index Scan/Bitmap Index Scan, not Seq Scan), (2) query time improves measurably, (3) the index has acceptable write overhead. An unused index is dead weight — it slows every INSERT for zero read benefit." |

## The Expert's Mindset

<!-- DEEP: 10+min — how masters think, not just what they do -->

### The Mental Model Shift
Competent database designers model the data. Masters model **how the data will be accessed under load, at scale, for years.** The shift: stop thinking about entities and start thinking about queries. A perfectly normalized schema that requires 7 joins for every page load is wrong — not because normalization is wrong, but because it doesn't match the access pattern. The database exists to serve queries. Design from the queries backward to the schema, not from the entities forward.

### Cognitive Biases That Kill Databases
| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Normalization fundamentalism** | Normalizing to 5NF for every table — impeccable theory, 12-join queries in production | Normalize for write integrity. Denormalize for read performance. Know which queries are read-heavy and which are write-heavy before designing. |
| **Index cargo culting** | Adding indexes to every foreign key "because that's best practice" without running EXPLAIN ANALYZE on actual query patterns | Every index costs write performance and storage. Index the queries your application actually runs, not the ones it might run someday. Unused indexes are dead weight. |
| **ORM trust** | Assuming the ORM generates efficient queries — discovering at 5M rows that the "simple" `user.orders` generates 50,000 individual SELECTs | Always log and review generated SQL in development. Set a query count threshold per request — if any endpoint generates > 20 queries, investigate. ORMs are conveniences with sharp edges. |

### What Database Masters Know That Others Don't  
- **The query planner is a liar until proven otherwise.** `EXPLAIN ANALYZE` on production-sized data is the only truth. Estimated row counts, cost calculations, index suggestions — all approximations. Never trust a query plan on a 100-row dev database.
- **Migrations are the highest-risk operation in your system.** A migration that locks a table blocks all writes. A migration that fails mid-way leaves the schema in an unknown state. Always: test on a production-sized copy, use `lock_timeout`, batch large data changes, and have a tested rollback.
- **Connection pooling is not optional at scale.** A default PostgreSQL install allows 100 connections. With 20 application servers each opening 10 connections, you're at 200 — double the database's capacity. Use PgBouncer or built-in poolers. Connection count must be monitored and capped at the pooler level.

### When to Break Your Own Rules
- **Use a materialized view instead of denormalizing.** When you need read performance but want to keep the source schema normalized, a materialized view gives you the best of both: normalized source, denormalized query surface, and a refresh strategy you control.
- **Skip foreign keys in a high-write append-only table.** Foreign keys validate on every INSERT. For an event log or audit table receiving 10K writes/sec, FK validation becomes the bottleneck. Enforce referential integrity at the application layer for these extreme cases — document the tradeoff explicitly.

## Operating at Different Levels

Database design skill scales from single-table decisions to org-wide data strategy. The cost of a wrong decision scales with the data volume.

| Level | Database Design Output Characteristics |
|---|---|
| **L1 — Apprentice** | Designs tables from an entity model. Learns normalization, indexing basics. Writes correct migrations. |
| **L2 — Practitioner** | Designs schemas for a service independently. Chooses appropriate data types, constraints, and indexes. Handles migrations safely. |
| **L3 — Senior** | Designs the data architecture for a product. SQL vs NoSQL selection with trade-off analysis. Partitioning, replication, and performance strategy. |
| **L4 — Staff** | Sets data architecture standards for the organization. Database selection criteria, schema governance, data lifecycle policies. "This is how we model data here." |
| **L5 — Principal** | Creates data modeling methodologies adopted across the industry. "Here's a new way to think about data consistency at scale." |

**Usage**: Say "as an L3 database designer, design the schema for..." Default: **L2** (service-level schema design, independent execution).

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

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| Choosing an ORM for a new project | Before committing, map the ORM's query generation against your top 5 query patterns. Propose running `EXPLAIN ANALYZE` on ORM-generated queries for joins, aggregations, and pagination. Discuss N+1 detection tooling (e.g., `bullet` gem, `nplusone` for Django, Prisma's `relationLoadStrategy: "query"`) | ORMs generate queries you didn't write — LEFT JOINs where INNER JOINs suffice, implicit subqueries, and lazy-loaded relations that cause N+1 cascades. A `findAll({ include: { posts: { include: { comments: true } } } })` can generate 5000+ queries under load. Pre-select the ORM's escape hatch for raw SQL |
| Modeling a many-to-many relationship that will serve >100K associations per entity | Before creating a standard junction table, propose a denormalized approach: materialize the association as a JSONB array on the parent for read-heavy workloads, or use a separate optimized read model (Redis sorted set, Elasticsearch) for high-cardinality lookups. Discuss read/write ratio and query patterns before picking the physical model | Standard junction tables with `JOIN` + `GROUP_CONCAT` perform fine at 1K associations but collapse at 100K — index scans become table scans, and aggregations consume disproportionate memory. The right model depends on whether reads or writes dominate |
| Designing a database that will serve both OLTP (transactional) and OLAP (analytics/reporting) workloads | Propose separating read models: OLTP uses normalized Postgres, OLAP uses a read replica with materialized views or a dedicated columnar store (ClickHouse, Redshift). Discuss CDC (change data capture) to stream writes to the analytics store. Never let reporting queries compete with transaction locks | A `SELECT COUNT(*) GROUP BY date_trunc('hour', created_at)` on 50M rows holds locks that block order creation. Reporting queries scanning production tables are the #1 cause of unexplained latency spikes in OLTP systems. Separate the workloads before the first dashboard is built |
| Adding full-text search to a Postgres-backed application | Before reaching for Elasticsearch, evaluate Postgres `tsvector` + GIN index (good to ~1M documents, ~100ms queries). If >1M docs or sub-50ms latency needed, propose CDC pipeline from Postgres WAL → Elasticsearch/Meilisearch. Discuss reindexing strategy, synonym dictionaries, and relevance tuning | Postgres full-text search works surprisingly well at moderate scale, but `tsvector` columns need triggers/refresh on every write, GIN indexes have write amplification, and fuzzy matching is limited. Elasticsearch is 10x better at relevance but adds a second system to operate — know the crossover point |
| Configuring connection pooling across a microservices fleet | Before deploying, calculate total connections: `(pool_size_per_service × service_instances) + (background_jobs × workers)`. Propose PgBouncer transaction pooling (not session pooling) for >5 services. Set `idle_in_transaction_session_timeout` to 30s. Alert at 70% pool utilization with P95 | 10 services × 20 connections each × 3 instances = 600 connections. Postgres defaults to 100 max_connections — 500 connections get queued. Every service thinks "I only need 20" but the sum creates a denial-of-service on the database. Connection budgets are shared resources that need governance |
| Using Redis/Memcached as a cache layer in front of the database | Before adding cache, propose a read-through or write-through pattern with TTL based on data freshness requirements. Discuss cache invalidation strategy: TTL-based (simple), event-driven (accurate but complex), or write-through (consistent but higher write latency). Propose cache-hit-rate monitoring with stale-data alerts | A cache without an invalidation strategy serves stale data silently. `SETEX user:123 3600 {...}` works until a profile update happens and users see old names for an hour. Write-through ensures consistency; TTL-only accepts staleness — pick deliberately, not by accident |
| Designing a multi-tenant database schema | Before choosing shared-table vs schema-per-tenant vs database-per-tenant, propose evaluating: (a) tenant count (10 vs 10K), (b) isolation requirements (GDPR/HIPAA), (c) noisy-neighbor risk. Discuss connection pool routing — if database-per-tenant, how does the app route to the right pool? Discuss tenant-level backup/restore expectations | Row-level tenancy (`tenant_id` column + RLS) is simple but one tenant's heavy queries degrade all others. Database-per-tenant isolates perfectly but explodes connection counts (200 tenants × 10 connections = 2000 connections). The choice between "simple and shared" vs "isolated and complex" is a business decision masked as a technical one |

## What Good Looks Like

> Every query in the application is backed by an index that makes it run in single-digit milliseconds, and `EXPLAIN ANALYZE` output confirms index-only scans on every critical path — no sequential scans hiding in production. The schema is normalized to 3NF with deliberate, documented denormalizations where read performance demands it, and no one has ever said "we'll fix the schema later" in a code review. Migrations apply in under 30 seconds with zero downtime via expand-contract patterns, and rollback plans are practiced, not theorized. Connection pools are sized so peak Black Friday traffic never exhausts them, and slow-query logs are empty for days at a time. Backups run on schedule, restores are exercised quarterly, and the team can answer "what was the state of this row at 3:14 PM last Tuesday?" because point-in-time recovery just works.

## Deliberate Practice

<!-- DEEP: 10+min — how to improve, not just what you do -->

### The Database Improvement Loop
1. **Enable slow query logging in production** — Set `log_min_duration_statement` to 100ms. Review the top 10 slowest queries weekly.
2. **EXPLAIN ANALYZE the worst offender** — Is it a missing index? Bad join order? Table scan on a 50M-row table?
3. **Fix, deploy, verify the query plan improved** — The fix is not complete until EXPLAIN shows the expected plan on production data.
4. **Repeat weekly** — Query patterns change as the application evolves. Last month's fast query is this month's bottleneck.

### Practice Routines
| Skill Level | Practice | Frequency | Expected Result |
|-------------|----------|-----------|-----------------|
| Novice → Competent | Take a 50M-row dataset (public: NYC taxi data, GitHub archive). Write 10 queries. EXPLAIN ANALYZE each. Add indexes. Measure improvement | Monthly | Internalizes the relationship between indexes, query plans, and actual performance |
| Competent → Expert | Design a schema migration with zero downtime on a 100M-row table. Test on a copy. Measure lock duration, replication lag, and rollback time | Per major migration | Can execute complex migrations without blocking production — knows expand-contract patterns cold |
| Expert → Master | Contribute a query optimizer improvement to PostgreSQL, MySQL, or SQLite documentation. Explain a surprising query plan behavior in a blog post | Quarterly | Understands why the optimizer chose that plan, not just what plan it chose |

### The One Thing
**Restore last night's production backup to a staging server and run your application against it.** Not a synthetic dataset. Not a truncated copy. The real data, real volume, real distribution. Your queries that ran in 2ms on dev will show their true colors on 500GB of production data.

## References
- **Denormalization ROI Calculator**: See [denormalization-roi-calculator.md](references/denormalization-roi-calculator.md)
- **Sharding Cost Analysis**: See [sharding-cost-analysis.md](references/sharding-cost-analysis.md)
- **When Postgres is All You Need**: See [when-postgres-is-all-you-need.md](references/when-postgres-is-all-you-need.md)
