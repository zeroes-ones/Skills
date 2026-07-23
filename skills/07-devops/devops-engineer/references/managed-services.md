# When Managed Services Save Money

### Managed vs Self-Hosted: Breakeven Calculator

```
Self-hosting cost = engineer_salary × fraction_of_time_on_ops + server_cost
Managed cost = service_monthly_fee

Breakeven happens when: service_monthly_fee < engineer_salary × ops_time_fraction
```

| Service | Self-Hosted Cost | Managed Cost | Breakeven |
|---------|-----------------|--------------|-----------|
| **PostgreSQL** | $500/month server + $5K/month ops time (25% of $200K eng) = $5,500/mo | RDS: $300-2K/month | **Always managed** unless extreme scale |
| **Kubernetes** | $2K/month nodes + $10K/month ops (50% of $240K eng) = $12K/mo | EKS: $73/cluster + $2K nodes | Managed saves $10K/month at small scale |
| **Kafka** | $3K/month servers + $8K/month ops = $11K/mo | MSK/Confluent: $2K-8K/month | Breakeven at 5 brokers |
| **Redis/ElastiCache** | $500/month server + $2K/month ops = $2,500/mo | ElastiCache: $200-1K/month | **Always managed** |
| **CI/CD** | $3K/month Jenkins infra + $5K/month = $8K/mo | GitHub Actions: $200/month | **Never self-host CI** under 1K eng |

**Rule:** Self-host only when managed service costs > 2× the engineer cost to run it OR you need features managed services don't offer.
