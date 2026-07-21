# Database Reliability

## High Availability Setup

**RDS Aurora PostgreSQL 15.4** in Multi-AZ configuration across us-east-1a, us-east-1b, and us-east-1c. The primary writer instance runs on `db.r6g.xlarge` (4 vCPU, 32GB RAM) with a synchronous standby in a different AZ. Recovery Point Objective (RPO): 15 minutes (worst-case data loss from the last committed transaction before failure). Recovery Time Objective (RTO): 5 minutes (Aurora automatic failover to a read replica promoted to writer). Failover tested monthly via `aws rds failover-db-cluster` during a low-traffic window — last 4 tests all completed within 3.2 minutes.

## Read Replicas

Two read replicas (`db.r6g.large` each) serve different workloads:

- **Analytics Replica**: Dedicated to Metabase, dbt transformations, and ad-hoc data exploration. Isolated from application traffic to prevent analytical queries (some running 30+ seconds) from impacting the primary instance. Configured with `max_connections = 50`.
- **Failover Replica**: Idle standby with identical configuration to the primary, positioned in a third AZ (us-east-1c). Promoted automatically by Aurora if the primary and first standby both fail. Cross-region read replica in eu-west-1 deployed for the multi-region migration (see migration architecture doc).

## Connection Pooling — PgBouncer

PgBouncer 1.22 deployed as a sidecar container in each application pod. Configuration: transaction pooling mode (`pool_mode = transaction`), 200 total connections, `default_pool_size = 25`. EKS node-level PgBouncer daemonset considered but rejected — sidecar pattern provides better fault isolation (one misbehaving service doesn't starve others). Application connects to `localhost:6432` instead of the RDS endpoint. PgBouncer metrics (active connections, waiting clients, query duration) exported to Prometheus via the `pgbouncer_exporter`.

## Backup Strategy

**Automated Backups**: RDS automated backups with 30-day retention, daily snapshots taken at 03:00 UTC. Snapshots copied to a separate AWS account (disaster recovery account) using AWS Backup cross-account copy with vault lock (compliance requirement: backups immutable for 14 days).

**Point-in-Time Recovery**: WAL (Write-Ahead Log) archiving enabled, allowing PITR to any point within the 30-day backup window with 5-minute granularity. Recovery tested quarterly — last test (July 5, 2026) restored a database to a point 4 hours prior in 22 minutes.

**Logical Backups**: Weekly `pg_dump` of the `services`, `service_versions`, and `templates` tables to S3 as a last-resort recovery option independent of the Aurora proprietary format. Stored as gzipped SQL with SSE-KMS encryption. 90-day retention.

## Zero-Downtime Migration Plan

Database schema changes follow the expand-contract pattern in 4 phases:

1. **Expand (Add)**: Deploy a migration that adds new columns/tables with no application code changes. Existing queries ignore the new schema. No downtime.

2. **Dual-Write**: Deploy application code that writes to both old and new columns. Reads still use old columns. No downtime.

3. **Backfill & Switch Read**: Run a background job to backfill new columns from old data. Once verified, switch reads to new columns. No downtime.

4. **Contract (Remove)**: After confirming no code reads or writes to old columns (1 sprint of monitoring), deploy a migration dropping old columns. No downtime.

All migrations follow this pattern — no `ALTER TABLE` that requires an `ACCESS EXCLUSIVE` lock for more than 2 seconds. Long-running migrations (index creation, column backfills) use `CONCURRENTLY` or batched updates in 10,000-row chunks with 100ms sleep between batches.
