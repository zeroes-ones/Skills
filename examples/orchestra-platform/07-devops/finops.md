# FinOps — Orchestra Platform

**Skill:** finops-engineer
**Input:** Cloud architecture, usage projections, pricing model

## Cost Model

### Infrastructure Cost Breakdown (Monthly)

| Resource | Dev ($) | Staging ($) | Prod ($) | Notes |
|----------|---------|-------------|----------|-------|
| EKS (3 clusters) | 215 | 435 | 870 | eksctl, 3 AZs |
| RDS Aurora (3 instances) | 180 | 360 | 720 | db.r6g.large, Multi-AZ prod |
| ElastiCache Redis | 60 | 120 | 240 | cache.m6g.large, cluster mode |
| EC2 (EKS worker nodes) | 280 | 560 | 1,120 | m6i.xlarge, spot in dev |
| S3 (artifacts, backups) | 40 | 80 | 160 | 500GB total, IA after 30 days |
| CloudFront + WAF | 30 | 60 | 120 | 2 distributions |
| Route53 + ACM | 10 | 10 | 20 | 3 hosted zones |
| NAT Gateway + data transfer | 50 | 100 | 200 | 3 AZs |
| Observability (Grafana Cloud) | 0 | 0 | 250 | 10K series, 30-day retention |
| **Subtotal** | **865** | **1,725** | **3,700** | |

**Total at MVP:** $6,290/month (dev + staging + prod)

### Scaling Projections

| Customer Count | Monthly Infra Cost | Cost/Customer/Month |
|---------------|-------------------|---------------------|
| 10 (beta) | $6,290 | $629 |
| 100 | $12,500 | $125 |
| 500 | $35,000 | $70 |
| 1,000 | $55,000 | $55 |
| 5,000 | $180,000 | $36 |

Unit economics improve with scale — shared infrastructure amortizes across customers.

## Savings Opportunities

### Reserved Instance Strategy

| Commitment | Savings | Annual Savings at 100 Customers |
|-----------|---------|-------------------------------|
| RDS 1-year, all upfront | 30% | $5,400 |
| ElastiCache 1-year, all upfront | 28% | $1,700 |
| EC2 Savings Plan 1-year | 32% | $9,200 |

**Total annual savings:** $16,300 (29% of compute costs)

### Waste Identified & Fixed

| Finding | Monthly Waste | Action |
|---------|---------------|--------|
| 5 unattached EBS volumes | $42 | Deleted, added lifecycle policy |
| 12 unused Elastic IPs | $43 | Released, limit to 5 per account |
| RDS instances not using Reserved Instances | $180 | Purchased 1-year RI |
| dev EKS cluster running 24/7 | $290 | Auto-stop nights/weekends (saves 65%) |

**Monthly savings from waste fix:** $390 average

## Cost Governance

- **Budget alerts:** $5K (dev), $8K (staging), $16K (prod) — alert at 80%
- **Tagging policy:** Every resource tagged with `team`, `service`, `environment`, `cost-center`
- **Monthly review:** First Monday, CTO + Engineering Lead + FinOps
- **Showback dashboard:** Per-team cost attribution in Grafana
- **Principle:** Never report savings without showing the calculation. Cost attribution must be transparent.
