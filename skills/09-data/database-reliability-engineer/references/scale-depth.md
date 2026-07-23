# Scale Depth

<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
- **What changes**: DBRE = you're also the backend developer and DevOps. Single database instance, nightly pg_dump backup to S3. Monitoring: database alerts go to your phone. HA: accept downtime for patching. Connection pool: app-level only.
- **What to skip**: Replication. Automated failover. PITR. Connection pooling middleware. Multi-AZ. DR site. Fleet management. Sharding. Read replicas.
- **Coordination**: Self-contained. Monitor via cloud provider dashboard.
- **Cost**: $20-50/month (managed small instance). Free tier often sufficient.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Primary + 1 read replica (or 1-2 async replicas). Automated backups with WAL archiving (PITR possible). Connection pool: PgBouncer or app-level pool with max limits. Monitoring: basic dashboard + alerts. HA: manual failover with runbook. Schema migrations: versioned migrations with expand-contract for non-trivial changes.
- **What to skip**: Multi-AZ auto-failover (if using managed, it's included). Sharding. Read/write split routing layer. DR site (backups to different region enough). Fleet management automation.
- **Coordination**: Coordinate with backend developers on slow queries. Share migration plans before execution. Weekly review of database metrics.
- **Cost**: $100-500/month (managed with read replica + backup storage).

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: HA: auto-failover (Patroni + etcd, or managed Multi-AZ). Read replicas: 2+ for load distribution + failover candidates. PITR with 1-minute granularity. Connection pooling: PgBouncer/ProxySQL with read/write split. Monitoring: per-query performance, SLO dashboards, replication lag alerts. DR site: warm standby in different region. Schema migrations: strict expand-contract, no locking DDL in production. Fleet management: standardized provisioning and monitoring.
- **What to skip**: Full sharding (use vertical scaling + read replicas until they fail). Multi-master replication (complexity rarely justified). Real-time cross-region replication (async adequate for most).
- **Coordination**: Bi-weekly schema review with backend team. Monthly capacity review with DevOps. Quarterly DR failover drill with incident response team.
- **Cost**: $1K-5K/month (managed HA + replicas + backup + DR). Add $500-2K/month for self-hosted tooling.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multiple database clusters per service, some sharded (Vitess, Citus). Multi-region active-active or active-passive with sub-minute failover. Full observability: query performance, lock contention, bloat, vacuum, replication, and capacity in unified dashboard. Database change management: CI/CD pipeline with automated migration safety checks (linter for locking DDL, long-running queries). Fleet management at scale: 50+ instances, standardized tooling, self-service provisioning for teams. Cost optimization: reserved instances, storage tiering, archival automation. Runbooks for 20+ failure scenarios.
- **What's full production**: Database reliability as a platform service — teams request databases via API/Terraform, get monitoring/backup/HA by default. Chaos engineering for databases: automated failover drills. Anomaly detection: ML-based query performance and storage forecasting. Database load testing in CI/CD pipeline.
- **Coordination**: Database architecture review board (bi-weekly). Cross-team schema compatibility checks. Monthly FinOps review. Quarterly multi-region DR test.
- **Cost**: $10K-100K+/month depending on scale. Reserved instances save 30-50%. Data transfer costs dominate multi-region setups.

### Transition Triggers
- **Solo → Small**: >100 users. First paying customers. Downtime costs real money (>$100/hr). Manual backup restore too slow.
- **Small → Medium**: >10K users. Read replica needed. Replication lag causing data inconsistencies. Connection pool exhaustion.
- **Medium → Enterprise**: >1M users. Compliance requirements (SOC 2, HIPAA). Multiple teams with shared database dependencies. Single instance cannot scale vertically.
