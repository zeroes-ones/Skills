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

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Model for access patterns, not for "purity"**: Denormalize when read performance matters more than write simplicity.
- **UUIDs over auto-increment IDs** for distributed systems: UUIDv7 (time-ordered) for primary keys to avoid hot spots.
- **Soft deletes with caution**: `deleted_at` simplifies recovery but complicates every query (add `WHERE deleted_at IS NULL`). Consider archiving to separate tables instead.
- **Separate read and write models**: CQRS pattern for high-scale systems with disparate read/write patterns.
- **Connection management**: Set appropriate pool sizes (CPU cores * 2-4 for OLTP), statement timeouts, idle-in-transaction timeouts.
- **Regular maintenance**: `VACUUM ANALYZE`, index rebuilds, statistics updates, bloat monitoring.

## Anti-Patterns
<!-- QUICK: 90s -- 4-column machine-checkable format. Every anti-pattern has a grep to find it and a lint/prevention config. -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Designing indexes by intuition without running `EXPLAIN ANALYZE` | Run `EXPLAIN (ANALYZE, BUFFERS)` on every query in staging with production-like data volumes. Verify index scans actually occur | `grep -rn 'CREATE INDEX\|CREATE UNIQUE INDEX' migrations/ \| grep -v 'EXPLAIN\|explain\|query.plan'` — indexes without EXPLAIN evidence | CI check: `scripts/verify-indexes.sh` — for each new index, require EXPLAIN output showing the index is used before merge |
| Using `SELECT *` in production code against wide tables | Explicitly list columns. `SELECT *` breaks on schema changes, fetches unused blobs, and prevents index-only scans | `grep -rn 'SELECT \*\|select \*' src/ \| grep -v 'COUNT(\*)\|count(\*)\|EXISTS\|test\|\.spec\|\.test'` — production SELECT * occurrences | ESLint rule: `no-restricted-syntax` with pattern `SELECT *`. Pre-commit hook: `scripts/check-select-star.sh` blocks commits with new SELECT * |
| Running migrations without a tested rollback path — "we tested up, we'll figure out down if needed" | Every `up` migration must have a `down` tested in CI. Use expand-contract for destructive changes across multiple release cycles | `find migrations/ -name '*.up.sql' \| while read f; do down="${f/.up.sql/.down.sql}"; [ ! -f "$down" ] && echo "MISSING: $down"; done` — missing down migrations | CI gate: `scripts/check-migration-pairs.sh` — fails if any .up.sql lacks a .down.sql. Dev environment: run `down` then `up` as integration test |
| Relying on application-level constraints instead of database constraints | Add `NOT NULL`, `CHECK`, `UNIQUE`, and `FOREIGN KEY` at the database level. App validation is bypassed by background jobs, direct DB, data migrations | `grep -rn 'validates.*presence\|validates.*format\|validates.*uniqueness\|validate.*required' app/ \| grep -v 'null:\s*false\|CHECK\|UNIQUE'` — app validations without DB constraints for same columns | Lint rule: `scripts/check-constraint-alignment.sh` — for every `validates :presence` or `required: true` in app code, verify corresponding `NOT NULL` in schema |
| Opening a new database connection per request without pooling | Use PgBouncer (transaction mode) for Postgres, or ORM pool with `pool_size = (cores * 2) + 1`. Set `idle_in_transaction_session_timeout` | `grep -rn 'new Client\|new Pool\|createConnection\|connect()' src/ \| grep -v 'pool\|Pool\|MAX_CONNECTIONS\|pool_size'` — connection creation outside pool | CI check: `scripts/check-connection-pool.sh` — verifies connection pool configured with max size, idle timeout, and leak detection |
| Storing monetary values as `FLOAT`/`DOUBLE` | Use `NUMERIC(19,4)` or `DECIMAL` for exact decimal arithmetic. Store in smallest unit (cents) as `BIGINT` for integer-only ops | `grep -rn 'FLOAT\|DOUBLE\|float\|double.*amount\|price\|balance\|salary\|revenue\|cost\|fee\|payment\|charge' migrations/` — float columns for money | Pre-commit lint: `scripts/check-money-columns.sh` — blocks any `FLOAT`/`DOUBLE` column named `amount`, `price`, `balance`, `fee`, `payment`, `revenue`, `cost`, `salary`, `charge`, `refund` |
| Not monitoring connection pool saturation, replication lag, and slow queries | Deploy alerts: connection pool >70%, replication lag >5s, slow queries >500ms. These three signals catch 90% of database incidents before users notice | `grep -L 'pool.*utilization\|replication.*lag\|slow.*query.*alert\|pg_stat' monitoring/*` — no database-specific monitoring | Monitoring template: `templates/db-monitoring.yml` — deploys Grafana dashboard with pool, lag, slow queries. Run `scripts/check-db-monitoring.sh` in CI |
| Using application-level JOINs (N+1 pattern) instead of database JOINs | Write a single query with `JOIN` and proper indexes. Use ORM eager loading (`include`, `preload`, `joins`) or write the SQL | `grep -rn '\.each\|\.forEach\|for.*of\|\.map' src/ \| grep -v '\.includes\|\.preload\|\.eager\|\.join'` — loops that may be N+1 | Lint: `eslint-plugin-n-plus-one` or `bullet` gem in dev. Detect by monitoring: queries-per-request > 20 triggers alert |

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


## Error Decoder
<!-- DEEP: 10+min -- 5-column format with grep matches and auto-recovery loops -->

| 🖥️ Console Match (grep) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|--------------------------|---------|-----------|-----|----------------------|
| `grep -iP '(lock.*timeout\|ACCESS.EXCLUSIVE\|could.not.acquire.*lock\|waiting.for.*lock\|deadlock)' logs/db-errors.log` | Production database locked up for 20+ minutes during deployment — all queries blocked | Migration added `ALTER TABLE X ADD COLUMN Y TEXT NOT NULL DEFAULT 'value'` — DB rewrites entire table holding ACCESS EXCLUSIVE lock | Kill stuck migration. Use expand-contract: add nullable column → backfill in 10K batches → `ALTER COLUMN SET NOT NULL`. Test on staging copy of production data first | 1. Check `pg_stat_activity` for blocking query. 2. If migration is blocking: `SELECT pg_cancel_backend(pid)` or `pg_terminate_backend(pid)`. 3. Restore from replica if data corrupted. 4. Rewrite migration: ADD COLUMN (nullable) → batched UPDATE → SET NOT NULL. 5. Test migration time on staging clone. 6. Set `lock_timeout = '5s'` for all migrations |
| `grep -iP '(seq.scan\|sequential.scan.*rows=\d{6,}\|Seq.Scan.*cost)' logs/db-errors.log` | Dashboard query times out at 60+ seconds — sequential scan on multi-million-row table | Missing index on JOIN/FILTER column. Query planner chooses Seq Scan because no usable index exists, scanning 10M+ rows | `CREATE INDEX CONCURRENTLY idx_name ON table(column)`. Run `EXPLAIN ANALYZE` to verify index is used. Query drops from 60s to < 100ms | 1. Identify slow query from `pg_stat_statements` or slow query log. 2. Run `EXPLAIN (ANALYZE, BUFFERS) [query]`. 3. Look for `Seq Scan on large_table (rows=10000000)`. 4. Identify filter/JOIN columns without indexes. 5. `CREATE INDEX CONCURRENTLY idx_...` (non-blocking). 6. Re-run EXPLAIN — must show Index Scan or Bitmap Index Scan. 7. Verify query time improvement |
| `grep -iP '(float.*precision\|rounding.*error\|numeric.*overflow\|0\.30000000000000004\|decimal.*mismatch)' logs/db-errors.log` | Financial reports off by pennies/cents — cumulative rounding errors across thousands of transactions | Monetary values stored as `FLOAT`/`DOUBLE` instead of `NUMERIC(19,4)` or `BIGINT` (cents). Floating-point arithmetic is inexact by design | `ALTER TABLE X ALTER COLUMN amount TYPE NUMERIC(19,4)`. Recalculate historical balances. Add `CHECK (amount >= 0)` constraint | 1. Audit all tables with columns named `amount`, `price`, `balance`, `fee`, `payment`, `revenue`, `cost`. 2. For each FLOAT/DOUBLE: `ALTER COLUMN TYPE NUMERIC(19,4) USING (amount::numeric)`. 3. For integer-only ops: convert to `BIGINT` storing cents. 4. Recalculate all aggregate balances with `SUM(amount::numeric)`. 5. Add CHECK constraints. 6. Run financial reconciliation to verify totals match |
| `grep -iP '(connection.*refused\|too.many.clients\|remaining.connection.slots.*reserved\|pool.*exhausted\|no.*connections.available)' logs/db-errors.log` | Application throws "too many clients" or "connection refused" — database unreachable | Connection pool exhausted. App opens new connections without pooling, or connections leak due to missing `idle_in_transaction_session_timeout` | Set pool max = `(cores * 2) + 1` (for direct Postgres) or `(cores * 4)` (for PgBouncer). Set `idle_in_transaction_session_timeout = 30000`. Add pool monitoring at 70% | 1. Check `pg_stat_activity` for idle-in-transaction connections. 2. `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle in transaction' AND age(now(), state_change) > '5 min'`. 3. Configure PgBouncer in transaction mode. 4. Set `pool_size` and `idle_timeout`. 5. Add Grafana alert: pool utilization > 70%. 6. Add application-side connection timeout + retry with backoff |
| `grep -iP '(could.not.rollback\|down.migration.*fail\|column.*does.not.exist.*rollback\|cannot.undo)' logs/db-errors.log` | Migration rollback fails — data lost because rollback tries to re-add a dropped column but can't recover the data | Destructive migration (DROP COLUMN) deployed without a tested rollback. PITR is disaster recovery, not a rollback strategy | Restore from PITR to point before migration. Implement expand-contract: never drop columns in a single migration; deprecate first, drop after 2 release cycles | 1. Stop all writes. 2. Restore from PITR to timestamp before migration. 3. Extract lost data from PITR restored instance. 4. Replay safe portion of migration. 5. Implement expand-contract for future DROPs. 6. Add CI check: no DROP COLUMN without `deprecated_since` comment and 2-release waiting period |
| `grep -iP '(N\+1\|n.plus.1\|hundreds.of.queries\|thousands.of.queries\|query.per.request.*\d{3,})' logs/db-errors.log` | Page load fires 200+ database queries — response time > 5 seconds under normal load | N+1 pattern: app fetches parent records, then loops and fetches child records one at a time instead of using JOIN or eager loading | Replace loop+query pattern with single JOIN query or ORM eager loading (`include`, `preload`, `joins`). 200 queries → 1 query. Response time drops from 5s to < 200ms | 1. Enable query logging in dev: log every query with duration. 2. Load the page — count queries. If > 20 queries per request: N+1 likely. 3. Find the loop: `grep -rn '\.each\|\.forEach\|for.*of'` in the controller/handler. 4. Inside the loop: find database calls. 5. Replace with `Model.findAll({ include: [ChildModel] })` or `SELECT ... LEFT JOIN ...`. 6. Re-count queries — must be 1-3 per request |


## What Good Looks Like

> Every query in the application is backed by an index that makes it run in single-digit milliseconds, and `EXPLAIN ANALYZE` output confirms index-only scans on every critical path — no sequential scans hiding in production. The schema is normalized to 3NF with deliberate, documented denormalizations where read performance demands it, and no one has ever said "we'll fix the schema later" in a code review. Migrations apply in under 30 seconds with zero downtime via expand-contract patterns, and rollback plans are practiced, not theorized. Connection pools are sized so peak Black Friday traffic never exhausts them, and slow-query logs are empty for days at a time. Backups run on schedule, restores are exercised quarterly, and the team can answer "what was the state of this row at 3:14 PM last Tuesday?" because point-in-time recovery just works.

## Production Checklist
<!-- QUICK: 30s -- all items are machine-verifiable. Every item gets a validation command and auto-fix path. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **S1** | Database technology selected with documented rationale (SQL vs NoSQL, specific engine) | `grep -cP '(rationale\|decision.*record\|why.*chose\|chosen.*because)' db-decision.md` — must return >= 1 | Template: `templates/database-selection-adr.md` — architecture decision record with data model, access patterns, consistency requirements, and alternatives considered |
| **S2** | Entity-relationship diagrams (ERDs) created and peer-reviewed | `file db-diagram.{svg,png,pdf,drawio}` — must exist. `grep -cP 'reviewed\|approved' erd-review.md` — must have review sign-off | Generate ERD from schema: `npx schemaspy -t pgsql -host localhost -db mydb -o docs/erd`. Or export from DBeaver/Prisma |
| **S3** | Schema normalized to 3NF with deliberate, documented denormalizations | `grep -cP 'denormaliz\|materialized.view\|cache.table\|aggregate.table\|precomputed' schema-docs.md` — every denormalization must be documented with justification | Run `scripts/check-normalization.sh` — flags tables with transitive dependencies (non-3NF). Template: `templates/denormalization-justification.md` for each intentional denormalization |
| **S4** | Indexing strategy aligned with all critical query patterns (EXPLAIN output reviewed) | `grep -cP 'Index.Scan\|Index.Only.Scan\|Bitmap.Index.Scan' explain-plans/*.txt` — every critical query must show index usage | Run `scripts/verify-indexes.sh` — for each query in `queries/*.sql`, run EXPLAIN and verify index usage. Report missing indexes |
| **S5** | Migration framework in place with expand-contract for production changes | `find migrations/ -name '*.down.sql' \| wc -l` must match `find migrations/ -name '*.up.sql' \| wc -l` | `scripts/check-migration-pairs.sh` — fails CI if any .up.sql lacks .down.sql. Template: `templates/migration-expand-contract.md` |
| **S6** | Connection pooling configured with appropriate limits and timeouts | `grep -cP 'pool.*size\|max_connections\|connection_timeout\|idle_in_transaction' config/database.{yml,yaml,toml,env}` — must have pool config | Template: `templates/pgbouncer.ini` or ORM pool config. Defaults: pool=20, idle_timeout=10s, idle_in_transaction_timeout=30s |
| **S7** | Backup strategy defined (WAL archiving, PITR, daily snapshots) with tested restore | `grep -cP 'backup\|WAL.archiv\|PITR\|snapshot\|restore.*test' backup-plan.md` — >= 3 | Template: `templates/backup-strategy.md`. Run `scripts/test-restore.sh` in CI — restores latest backup to ephemeral instance and runs smoke tests |
| **S8** | Encryption at rest (TDE/KMS) and in transit (TLS 1.3) configured | `grep -cP 'ssl\|tls\|encrypt\|KMS\|TDE\|pg_hba.*scram-sha-256' config/database.{yml,yaml,toml,env}` — >= 2 | Run `scripts/check-db-encryption.sh` — verifies TLS enabled, scram-sha-256 auth, and KMS key configured for managed DB |
| **S9** | Monitoring dashboards for slow queries, connection counts, replication lag, disk usage | `curl -s -o /dev/null -w '%{http_code}' <grafana-db-dashboard-url>` must return 200 | Deploy `templates/db-monitoring.yml` — Grafana dashboard with: slow queries, pool utilization, replication lag, disk %, deadlocks, index hit ratio |
| **S10** | Data retention and archival policy documented and automated | `grep -cP 'retention\|archive\|purge\|TTL\|delete.after' data-lifecycle.md` — >= 2 | Template: `templates/data-lifecycle-policy.md`. Cron jobs: `scripts/archive-and-purge.sh` for each table with TTL policy |

## Footguns
<!-- DEEP: 10+min — war stories from production database systems -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Index on a `status` column with 3 values (pending/active/closed) — 98% of rows were "closed" so the query planner ignored the index and table-scanned 50M rows on every query | A task management system added an index on `tasks.status` to speed up "show me open tasks" queries. But after 3 years, 98% of the 50M rows had `status = 'closed'`. PostgreSQL's query planner looked at the histogram: "If I use the index, I'll still read 49M rows from the heap — faster to just sequential scan the table." The "open tasks" query took 8 seconds in production because the index was effectively useless for the dominant value. The team added 3 more indexes on the same column (partial, composite, expression) trying to fix it, bloating the database by 40GB. | Low-cardinality indexes degrade over time as data distribution changes. An index on a column with 3 values is useful when the values are evenly distributed. When one value dominates, the index becomes a liability — the planner ignores it but still maintains it on every write. The team never re-evaluated index effectiveness against current data distribution. | **Review index usage quarterly against current data distribution.** Query: `SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch FROM pg_stat_user_indexes`. If `idx_scan = 0` for 3+ months, the index is dead weight. For low-cardinality columns, use partial indexes: `CREATE INDEX ON tasks (created_at) WHERE status IN ('pending', 'active')`. This indexes only the 2% of rows you actually query, making it small, fast, and always used by the planner. |
| Foreign keys enforced in development but missing in production RDS — 1.2M orphaned rows accumulated over 11 months because the DBA created tables with `CREATE TABLE ... ENGINE=InnoDB` but forgot `FOREIGN KEY` clauses | A SaaS platform ran MySQL in dev with strict mode and foreign keys. The production RDS instance was provisioned via Terraform with a raw SQL migration. The DBA exported the schema from dev using `mysqldump --no-data` but the output was truncated at 65KB — everything after the `orders` table was missing. The RDS instance ran without FK constraints for 11 months. When the team ran a data cleanup script that `DELETE FROM users WHERE last_login < '2023-01-01'`, it succeeded — but left 1.2M orders, 340K invoices, and 8M log entries referencing deleted users. The analytics dashboard showed revenue from "User #0" for 6 months before anyone investigated. | Foreign keys were assumed present because "the migration ran successfully." Nobody verified with `SHOW CREATE TABLE` on the production instance. The Terraform module had `apply_immediately = false` so schema validation never ran against the actual RDS instance after provisioning. | **Validate schema integrity in production, not just in dev.** Run a post-deploy check: `SELECT TABLE_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_NAME IS NOT NULL` and compare against expected FKs. Add a CI check that runs `pt-online-schema-change --dry-run` against a production-sized clone. Never assume — verify with `SHOW CREATE TABLE` on the actual production instance after every migration. |
| Migration `ADD COLUMN last_login_at TIMESTAMP DEFAULT NOW()` on a 50M-row table locked all writes for 4 hours because PostgreSQL < 11 rewrites every row to fill the default value | A team added a `last_login_at` column to the `users` table (50M rows) with `ALTER TABLE users ADD COLUMN last_login_at TIMESTAMP DEFAULT NOW()`. On PostgreSQL 10.6, this triggered a full table rewrite — every row was copied to a new location on disk with the default value filled in. The `users` table was locked for writes (no logins, no signups, no password resets) for 4 hours. The migration started at 10:00 AM on a Monday. Support received 1,700 tickets before the migration completed. Management required all future migrations to be approved by a VP. Velocity cratered. | In PostgreSQL < 11, `ADD COLUMN ... DEFAULT` rewrites the entire table because the default value must be physically stored in each row. The team assumed "this is just adding a nullable column with a default — it'll be instant" based on experience with MySQL, where `ADD COLUMN` is metadata-only when the column is nullable. They never checked the PostgreSQL version or tested on a production-sized dataset. | **Always check your database version before writing migrations.** PostgreSQL 11+ supports instant `ADD COLUMN ... DEFAULT` for non-volatile defaults. If on < 11, split the migration: (1) `ALTER TABLE ADD COLUMN` (instant, nullable, no default), (2) backfill in batches of 10,000 with `UPDATE ... WHERE id IN (...) LIMIT 10000`, (3) `ALTER COLUMN SET DEFAULT` once backfill is complete. Test every migration on a production-sized anonymized clone before running against production. |
| Connection pool sized at 20 connections based on average load — a marketing email drove 500 concurrent users, the pool saturated, and every service returned `502 Bad Gateway` for 18 minutes | A B2C platform configured HikariCP with `maximumPoolSize: 20` — reasonable for their average of 15 concurrent requests. A Black Friday email campaign went out at 9:00 AM. Concurrent users spiked to 500 in 60 seconds. The connection pool saturated at 20 — 480 requests queued waiting for connections. The `connectionTimeout` was 30 seconds, so every queued request blocked for 30 seconds before failing. The application server's thread pool also saturated. New requests from unaffected services couldn't reach the health check endpoint. Recovery required restarting all 12 application instances. Lost revenue: estimated $47,000 in 18 minutes. | The pool was sized for the average, not the peak. No one calculated: `pool_size = (peak_qps × p95_query_ms) / 1000 × 1.5`. The connection timeout (30s) was orders of magnitude too high — a `502` after 3 seconds is a blip; a `502` after 30 seconds is an outage. No circuit breaker protected downstream services from the pool saturation. | **Size your connection pool for peak, not average.** Formula: `pool_size = (peak_qps × p95_query_ms) / 1000 × 1.5`. For 500 QPS with 50ms p95 queries: (500 × 50) / 1000 × 1.5 = 37.5 → set pool to 40. Set `connectionTimeout` to 3 seconds — fail fast, don't queue. Add a circuit breaker on the application side that trips when 80% of pool connections are in use and returns degraded responses. Load-test with the peak scenario before every major campaign. |
| Read replica lag exceeded 30 seconds during a nightly batch job — customers in Europe saw orders they placed 30 seconds ago disappear from their order history | A global e-commerce platform used a primary-write, replica-read topology. The primary was in us-east-1; a read replica in eu-west-1 served European traffic. A nightly analytics batch job ran `SELECT COUNT(*), SUM(amount) FROM orders WHERE ...` on the primary at 2:00 AM UTC. The query took 8 seconds and generated 2GB of WAL. The eu-west-1 replica fell 30 seconds behind applying WAL. European customers who placed orders and immediately viewed their order history saw... nothing. Their orders existed on the primary but hadn't replicated yet. Support received 140 "where is my order?" tickets. Three customers placed duplicate orders thinking the first one failed. | The read replica was treated as transparently consistent, but replication is asynchronous by default. No application-level logic handled replication lag. The batch job ran on the primary (generating WAL) instead of a dedicated analytics replica. No monitoring alerted on replica lag exceeding 5 seconds. | **Never assume read replicas are current.** Use `SHOW SLAVE STATUS` or `pg_stat_replication` to check `replay_lag` before routing reads to a replica. For read-your-own-writes: after a mutation, route the next N seconds of reads from that user session to the primary. Add an alert on replication lag > 5 seconds. Move analytics queries to a dedicated replica that doesn't serve user traffic, so batch jobs don't stall the replicas customers read from. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You add indexes to every column in a slow query without checking whether the query planner actually uses them | You can `EXPLAIN ANALYZE` any slow query, identify whether the bottleneck is a missing index, a bad join order, or a table scan, and deploy a fix that reduces query time by 10× or more — confirmed by production metrics | A developer asks "why is this query slow?" and you diagnose the root cause in under 2 minutes without looking at the code, just from the query plan — and you're right 90% of the time |
| You design schemas by modeling "what the app needs right now" without thinking about what queries will run against it 12 months from now | You design schemas with 3-year query patterns in mind — you know which columns will be filtered, which will be sorted, and which will be joined — and the indexing strategy you define today still serves 80% of queries 2 years later | You lead a migration from one database technology to another (PostgreSQL → CockroachDB, MySQL → Vitess) with zero data loss, under 5 minutes of write downtime, and no application code changes beyond the connection string |
| You run migrations during business hours by clicking "Apply" in a GUI | Every migration is expand-contract: add the new column/schema (compatible), backfill data, switch reads, switch writes, remove old column — and each step is individually reversible | You contribute a performance improvement or bug fix to the PostgreSQL/MySQL/SQLite query optimizer, not just the application layer — you understand why the planner makes its decisions, not just what it decided |

**The Litmus Test:** Can you restore a production backup to a staging server, identify the 5 slowest queries by running `EXPLAIN ANALYZE` on each, and deploy fixes that improve each by at least 5× — all within 2 hours?

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
<!-- QUICK: 30s -- links to deeper reading -->
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/) — Performance Tips, Index Types
- [Use the Index, Luke!](https://use-the-index-luke.com/) — Markus Winand
- [Database Migrations Done Right](https://www.brunton-spall.co.uk/post/2014/05/06/database-migrations-done-right/) — Michael Brunton-Spall
- [Designing Data-Intensive Applications (Chapters 2-3, 5-7)](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) — Martin Kleppmann
- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html) — PostgreSQL Official
- [MongoDB Schema Design Best Practices](https://www.mongodb.com/docs/manual/core/data-modeling-introduction/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
