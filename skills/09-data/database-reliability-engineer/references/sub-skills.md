# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `ha-architecture` | Designing high availability: auto-failover, quorum, split-brain prevention | Patroni, etcd, multi-AZ, failover testing, quorum design, witness nodes |
| `replication-strategy` | Setting up replication: async, sync, semi-sync, logical, cross-region | RPO/RTO tradeoffs, replication lag monitoring, conflict resolution, failover procedures |
| `query-optimization` | Slow queries, performance degradation, scaling bottlenecks | EXPLAIN ANALYZE, index design, query rewriting, statistics, plan caching, hint usage |
| `connection-pooling` | Connection exhaustion, serverless connection storms, multi-app access | PgBouncer, ProxySQL, pool sizing, transaction vs session mode, read/write split routing |
| `backup-recovery` | Backup strategy, PITR setup, disaster recovery planning | WAL-G, PgBackRest, XtraBackup, backup validation, restore drills, PITR procedures |
| `sharding-design` | Scaling beyond single instance, multi-tenant isolation | Range/hash/directory sharding, Vitess/Citus, resharding, cross-shard query handling |
| `migration-strategy` | Schema changes, data migrations, zero-downtime requirements | Expand-contract, online DDL (gh-ost, pt-online-schema-change), backfill, dual-write |
| `fleet-management` | Managing many databases at scale, standardization, self-service | Terraform, Ansible, configuration management, provisioning automation, lifecycle management |
