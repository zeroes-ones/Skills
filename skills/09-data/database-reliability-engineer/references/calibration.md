# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can run `SELECT`, `INSERT`, `UPDATE` but would freeze if `pg_stat_activity` shows 200 `idle in transaction` connections at 3:00 AM | You can recover a database from backup with PITR to a specific timestamp, and you've done it in a quarterly drill — not just read the docs | You get paged at 3 AM: "database is slow." Within 5 minutes looking at `pg_stat_activity`, `pg_locks`, and `vmstat`, you identify whether the problem is queries, infrastructure, or the application |
| You write `CREATE INDEX` without checking if a similar index already exists — or how much space the index will consume | You plan index changes with `EXPLAIN (ANALYZE, BUFFERS)`, estimate the size, check disk space, and schedule the creation during a low-traffic window | You can look at a database's `pg_stat_user_tables` and `pg_stat_user_indexes` and identify which 3 indexes are costing more than they're saving — and prove it with before/after metrics |
| You don't know what autovacuum is or why `n_dead_tup` matters until the database wraps around the transaction ID and shuts down in single-user mode | You've tuned autovacuum for your workload: `scale_factor` per-table, `cost_limit` per instance, and you monitor dead tuple ratios weekly | You design the database layer for a 200-service microservice architecture — and 12 months later, zero outages attributable to database configuration, connection management, or index strategy |

**The Litmus Test:** Someone hands you SSH access to a production PostgreSQL instance you've never seen. Can you produce a health assessment — connection saturation, query performance, replication status, backup freshness, vacuum health, disk forecast — with specific recommendations, in under 30 minutes? If you reach for a SaaS monitoring tool, you're not L3 yet.
