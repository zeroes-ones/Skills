# Scale Depth: Solo → Small → Medium → Enterprise

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
