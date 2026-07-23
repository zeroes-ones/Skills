# Best Practices

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
