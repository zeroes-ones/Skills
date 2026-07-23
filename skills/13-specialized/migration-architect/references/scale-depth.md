# Scale Depth

<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person) → Small (2-10) → Medium (10-50) → Enterprise (50+)

| Dimension | Solo | Small | Medium | Enterprise |
|-----------|------|-------|--------|------------|
| **Migration Scope** | 1 database, <10 tables, <1GB | 1 codebase, 1 DB, <50 tables | 5-20 services, multiple DBs | 50+ services, multi-region, multi-DB |
| **Tooling** | ORM auto-migrate, raw SQL | Framework-based (Flyway/Alembic/Prisma) | Online schema change (gh-ost/pgroll) + CDC | Blue-green DB deploys + automated drift detection |
| **Testing** | Manual apply, verify, roll back | CI: apply up → test → roll back → test | Prod-scale clone testing + perf regression | Automated migration testing with synthetic traffic |
| **Risk Management** | Maintenance window acceptable | Expand-Contract for zero-downtime | Feature flags + canary per migration phase | Multi-region gradual rollout + auto-rollback on anomaly |
| **Rollback** | Manual script per migration | Documented rollback per phase | Automated rollback tested in CI | Instant feature-flag disable + data sync reversal |
| **Coordination** | Developer owns migration end-to-end | 1 backend specialist reviews | Migration architect + DB team | Dedicated migration team with runbook and stakeholder comms |

### Transition Triggers

| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | Paying users who would notice >1s downtime | Add versioned migrations, Expand-Contract for schema changes, CI validation |
| Small → Medium | Database >50GB or >5 services | Online schema change tools, CDC for data migration, automated rollback testing |
| Medium → Enterprise | Multi-region, >50 services, regulatory compliance | Blue-green deployments, automated drift detection, migration runbook with stakeholder comms |
