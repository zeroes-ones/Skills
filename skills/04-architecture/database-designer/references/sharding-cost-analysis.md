# Sharding Cost Analysis

**Sharding increases complexity cost by 3-5×. Justify it:**

| Sharding Trigger | Threshold | Alternative First |
|-----------------|-----------|-------------------|
| DB CPU > 70% | Add read replicas | 3-5 replicas handle most read-heavy workloads |
| Write throughput > 5K/sec | Vertical scale (r6i.8xlarge) | $2K/month vs $100K+ in sharding complexity |
| > 10TB data | Partitioning + archiving | Partition by date, archive cold partitions to S3 |
| Multi-tenancy at scale | Database-per-tenant | Simpler than sharding; isolate noisy neighbors |

**Sharding cost:** 3-6 months initial build + 1-2 dedicated DBREs at $180K/year each + application-level routing complexity. Minimum $500K/year overhead.
