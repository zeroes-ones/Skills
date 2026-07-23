# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You add indexes to every column in a slow query without checking whether the query planner actually uses them | You can `EXPLAIN ANALYZE` any slow query, identify whether the bottleneck is a missing index, a bad join order, or a table scan, and deploy a fix that reduces query time by 10× or more — confirmed by production metrics | A developer asks "why is this query slow?" and you diagnose the root cause in under 2 minutes without looking at the code, just from the query plan — and you're right 90% of the time |
| You design schemas by modeling "what the app needs right now" without thinking about what queries will run against it 12 months from now | You design schemas with 3-year query patterns in mind — you know which columns will be filtered, which will be sorted, and which will be joined — and the indexing strategy you define today still serves 80% of queries 2 years later | You lead a migration from one database technology to another (PostgreSQL → CockroachDB, MySQL → Vitess) with zero data loss, under 5 minutes of write downtime, and no application code changes beyond the connection string |
| You run migrations during business hours by clicking "Apply" in a GUI | Every migration is expand-contract: add the new column/schema (compatible), backfill data, switch reads, switch writes, remove old column — and each step is individually reversible | You contribute a performance improvement or bug fix to the PostgreSQL/MySQL/SQLite query optimizer, not just the application layer — you understand why the planner makes its decisions, not just what it decided |

**The Litmus Test:** Can you restore a production backup to a staging server, identify the 5 slowest queries by running `EXPLAIN ANALYZE` on each, and deploy fixes that improve each by at least 5× — all within 2 hours?
