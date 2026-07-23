# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
1. **Expand-Contract for every schema change:** Add → dual-write → backfill → switch reads → remove old. Never drop a column in the same deploy that adds its replacement.
2. **Test rollbacks before you need them:** Every migration must pass CI: apply up → run tests → roll back → run tests. If rollback can't be tested, it doesn't exist.
3. **Start with low-risk components first:** Migrate your least critical, least coupled service first. Learn from it. Don't start with the payment system.
4. **Batch data migration with checkpointing:** Process 1K-10K rows per batch with a sleep interval. Save checkpoint after each batch. A failed 100M-row migration must resume, not restart.
5. **Feature flags for every migration path:** Every new code path gets a flag. If something breaks, you disable the flag — not roll back a deploy. Flags toggle in seconds; deploys take minutes.
6. **Bake period scales with blast radius:** DB-only change → 24h bake. API migration → 48h. Full-stack → 72h minimum. Never decommission old system before bake completes.
7. **Monitor replication lag during migration:** Lag >2s → throttle or pause migration. The old system is your rollback — don't let it fall behind.
8. **Consistency verification is non-negotiable:** Row counts match. Checksums match. Business-level reconciliation queries pass. All three must pass before cutover.
9. **Never migrate and refactor simultaneously:** Either lift-and-shift (same logic, new platform) OR refactor-and-migrate (new logic). Doing both at once makes <!-- DEEP: 10+min -->
debugging impossible.
10. **Conduct a pre-mortem before every migration:** "The migration failed. What went wrong?" Write down the top 3 causes. Those are your rollback triggers and monitoring priorities.
