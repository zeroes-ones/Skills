# Cloud Architect - Cloud Cost Optimization

Complete cloud cost optimization playbook with specific savings targets and startup free tier maximization.

---

## Cost Optimization Decision Tree

```
Monthly cloud bill > $5K?
├── YES → Have you purchased commitment discounts?
│   ├── NO → Buy RI/SP for steady-state workloads. Savings: 40-60%.
│   └── YES → Are you using spot/preemptible for stateless workloads?
│       ├── NO → Migrate 20-40% to spot. Savings: 70-90%.
│       └── YES → Have you right-sized ALL instances?
│           ├── NO → Run Compute Optimizer. Savings: 20-40%.
│           └── YES → Are you using tiered storage?
│               ├── NO → Move cold data to glacier/deep archive. Savings: 60-80% on storage.
│               └── YES → Audit data transfer costs.
└── NO → Are you maximizing free tier?
    ├── NO → See free tier strategy below. Target: $0/mo.
    └── YES → Monitor. Set $100 budget alert.
```

---

## Commitment Discounts Calculator

### AWS Reserved Instances / Savings Plans

| Workload Pattern | Commitment Type | Savings | Risk |
|-----------------|----------------|---------|------|
| Always-on, 24/7/365 | 3-year All Upfront RI | 62% | High — locked in |
| Always-on, flexible region | 1-year Compute Savings Plan | 28-35% | Low — applies across regions/families |
| Steady state, known AZ | 1-year Standard RI | 40% | Medium — resellable on marketplace |
| Bursty, unpredictable | No commitment | 0% | None |

### Breakeven: Should You Buy a Reservation?

```
Formula: reservation_savings > (monthly_cost × commitment_months × risk_of_change)

Example: EC2 m6i.xlarge on-demand = $190/mo
1-year RI All Upfront = $1,361/yr ($113/mo) — saves 40%
Annual savings = ($190 - $113) × 12 = $924

If there's a 30% chance you'll migrate off AWS in 6 months:
Expected cost = ($1,361 × 0.3) + ($1,361 × 0.7) = $1,361
Expected on-demand = $190 × 12 = $2,280
Savings: $919 → BUY the RI even with 30% risk of migration.
```

**Rule of thumb:** If workload runs > 70% of the time, buy 1-year commitment. If > 90%, buy 3-year.

---

## Spot Instance Strategy

| Workload | Spot Viability | Savings |
|----------|---------------|---------|
| CI/CD runners | ✅ Perfect | 70-90% |
| Batch processing | ✅ Perfect | 70-90% |
| Dev/staging environments | ✅ Good (shut down nights/weekends) | 70-90% |
| Stateless web tier (with fallback) | ⚠️ Possible (need on-demand fallback pool) | 50-70% |
| Stateful databases | ❌ Never | — |
| Mission-critical single instances | ❌ Never | — |

### Spot Diversification Pattern
```yaml
# Kubernetes: mix spot + on-demand with priority expander
apiVersion: karpenter.sh/v1beta1
kind: NodePool
spec:
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
        # Karpenter prioritizes spot, falls back to on-demand
```

**Max safe spot allocation:** 40% of total compute. Keep 60% on-demand/RI to survive spot termination waves.

---

## Right-Sizing Methodology

### Weekly Rightsizing Audit

```sql
-- AWS: Find over-provisioned EC2 instances
SELECT instance_id, instance_type,
    AVG(cpu_utilization) as avg_cpu,
    AVG(mem_utilization) as avg_mem
FROM cloudwatch_metrics
WHERE period_days = 14
    AND avg_cpu < 20
    AND avg_mem < 40
GROUP BY instance_id;
-- Action: Downgrade by 1-2 sizes. Save 30-50%.
```

### Right-Sizing Targets
| Resource | Target Utilization | Over-Provisioned If | Under-Provisioned If |
|----------|-------------------|--------------------|--------------------|
| CPU | 50-70% | <30% avg over 14d | >85% sustained |
| Memory | 60-80% | <40% avg over 14d | >90% sustained |
| Disk IOPS | 50-70% of provisioned | <20% avg | >80% sustained |
| Database connections | 60-80% of max | <30% avg | >85% peak |

---

## Serverless Cost Traps

| Trap | Why | Fix |
|------|-----|-----|
| **Lambda timeout too long** | 30s timeout × 100 invocations = 3,000 GB-seconds wasted | Set timeout to P99 × 2. Profile and reduce. |
| **Lambda memory overallocation** | 10240MB for simple CRUD = 10× cost of 512MB | Start at 512MB; increase only if CPU-bound. |
| **API Gateway + Lambda cold starts** | 100ms cold start = 10× latency, users wait, more concurrent invocations | Use provisioned concurrency for latency-sensitive endpoints. |
| **DynamoDB on-demand vs provisioned** | On-demand = 7× more expensive per operation at steady state | Switch to provisioned with auto-scaling after 30 days of predictable traffic. |
| **CloudFront → S3 origin (no caching)** | Every request hits S3 = high origin fetch cost | Set `CachePolicy` with appropriate TTL. |
| **NAT Gateway × many AZs** | $32/AZ/month × 3 AZs = $96/month just for NAT | Use VPC endpoints (free) for S3/DynamoDB; single NAT with multi-AZ routing if budget matters. |
| **Unused provisioned concurrency** | $0.000004167/GB-s reserved, 24/7 = $/month even with 0 invocations | Only provision for latency-critical paths; let cold starts handle the rest. |

### Serverless vs Container Breakeven

```
Lambda: $0.0000166667 per GB-second + $0.20 per 1M requests
Fargate: $0.04048 per vCPU-hour + $0.004445 per GB-hour

Breakeven (constant load): Lambda is cheaper up to ~50 req/sec continuous.
Above 50 req/sec constant → Fargate/ECS is cheaper.

Spiky workload (1K rpm for 5 min, idle 55 min):
Lambda: 1K × 5 min × 0.5GB × $0.0000166667 × 12 cycles/hr = ~$0.50/hr
Fargate: 0.25 vCPU × $0.04048/hr = $0.01/hr (idle!) → $0.24/day minimum
→ Lambda wins for spiky workloads even at high peaks.
```

---

## Free Tier Maximization (Startup Playbook)

### Target: $0/month for MVP (0-1K users)

| Service | Free Tier | How to Stay Free |
|---------|----------|-----------------|
| **AWS Lambda** | 1M requests, 400K GB-seconds/month | Use for all compute. 128MB functions. |
| **AWS DynamoDB** | 25GB storage, 25 RCU/WCU | Use on-demand mode, single table design. |
| **AWS S3** | 5GB storage, 20K GET requests | Compress assets. Use CloudFront for caching (1TB free transfer). |
| **AWS CloudFront** | 1TB transfer, 10M requests/month | CDN everything. |
| **Vercel** | 100GB bandwidth, 6K build minutes | Frontend hosting. Pro at $20/mo when you need. |
| **PlanetScale** | 5GB storage, 1B row reads | MySQL-compatible, no ops. |
| **Supabase** | 500MB DB, 2GB bandwidth | Postgres + auth + storage. |
| **Cloudflare** | Unlimited DDoS, CDN, DNS | Put everything behind Cloudflare. |
| **GitHub Actions** | 2000 min/month (private) | CI/CD for free. |
| **Sentry** | 5K errors/month | Error monitoring. |

### $0 to $50/month Progression

| Users | Compute | Database | Frontend | Monthly |
|-------|---------|----------|----------|---------|
| 0-100 | Lambda free tier | DynamoDB free tier | Vercel free | $0 |
| 100-1K | Lambda free tier | Supabase free | Vercel free | $0-10 |
| 1K-5K | Lambda free tier | Supabase Pro ($25) | Vercel Pro ($20) | $45 |
| 5K-50K | ECS Fargate + Lambda | RDS t3.small ($35) | Vercel Pro | $80-200 |
| 50K-500K | Fargate/EKS | RDS m6i.xlarge ($250) | CloudFront + S3 | $500-2K |

---

## Multi-Cloud vs Single-Cloud Cost Analysis

### Single-Cloud (AWS Only)
| Advantage | Savings |
|-----------|---------|
| Higher commitment discounts (concentrated spend) | 5-15% |
| No data transfer costs between clouds | $0.02-0.12/GB saved |
| Lower engineering overhead (one toolchain) | $50K-100K/year in eng time |
| Easier compliance (one environment to audit) | Reduced audit cost |

### Multi-Cloud (AWS + GCP)
| Advantage | Savings |
|-----------|---------|
| Leverage GCP's lower compute costs (20-30% cheaper than AWS) | 20-30% on compute |
| Use GCP credits ($100K+ free for startups) | Immediate $100K |
| Avoid vendor lock-in | Hard to quantify |
| Best-of-breed services (BigQuery > Redshift for analytics) | Performance gains |

### Multi-Cloud Hidden Costs
| Cost | Impact |
|------|--------|
| Egress between clouds | $0.02-0.12/GB. 10TB/month = $200-1,200/month |
| Engineering complexity | Need engineers who know both clouds — $20K+ salary premium |
| Compliance overhead | SOC 2 across 2 clouds = 2 audits = double cost |
| Latency between clouds | 20-50ms penalty for cross-cloud calls |

**Verdict:** For companies under $50M ARR, single-cloud + multi-region is usually optimal. Multi-cloud makes sense above $100M ARR or when GCP/Azure offer $100K+ in credits.

---

## Monthly Cost Audit Checklist

Run this monthly:
- [ ] Purchased RI/SP coverage for stable workloads (>70% coverage target)
- [ ] Spot instance adoption for stateless workloads (>30% target)
- [ ] Right-sized any instances with <30% CPU for 14 days
- [ ] Deleted unattached EBS volumes, elastic IPs, idle load balancers
- [ ] Lifecycle policies on S3 buckets (transition to IA after 30 days, archive after 90)
- [ ] RDS instances using Reserved, not on-demand
- [ ] NAT Gateways consolidated (1 per region, not 1 per AZ)
- [ ] Unused provisioned concurrency cleaned up
- [ ] Budget alerts configured at 80%/100% threshold
- [ ] Free tier utilization maximized (every new account = new free tier)
