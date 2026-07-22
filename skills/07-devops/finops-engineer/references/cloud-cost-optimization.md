# Cloud Cost Optimization

> **Author:** Sandeep Kumar Penchala

Actionable FinOps patterns for compute optimization, storage tiering, data transfer reduction, Kubernetes cost allocation, tagging strategy, anomaly detection, and multi-cloud discount negotiation. These practices operationalize the finops-engineer skill's FinOps lifecycle.

## Compute Optimization

### Rightsizing Decision Matrix

| Situation | Action | Savings Potential |
|-----------|--------|-------------------|
| CPU < 30% avg, memory < 40% avg over 14 days | Downsize instance by 1 tier | 30-50% |
| CPU > 70% avg sustained | Upsize or add replicas | Avoids performance degradation |
| Burst pattern (peak at 9am, idle at night) | Use autoscaling + schedule | 40-60% |
| Steady predictable workload | Reserved Instance or Savings Plan | 30-72% |

### Reserved Instances vs Savings Plans

| Option | Discount | Term | Flexibility | Best For |
|--------|----------|------|------------|----------|
| Standard RI (1yr) | ~40% | 1 or 3 years | Locked to instance family + region | Stable, predictable workloads |
| Convertible RI (1yr) | ~30% | 1 or 3 years | Can change family, OS, tenancy | Evolving workloads |
| Compute Savings Plan | ~30% | 1 or 3 years | Any region, family, OS — just compute | Modern, flexible architecture |
| EC2 Instance Savings Plan | ~40% | 1 or 3 years | Specific family, any region | Known instance families |
| Spot Instances | 60-90% | None — can be reclaimed | None — 2-min warning | Fault-tolerant, stateless, batch |

```python
# Savings Plan recommendation calculator
def savings_plan_analysis(ondemand_monthly: float, coverage_pct: float = 0.70):
    """Recommend Savings Plan commitment based on steady-state usage."""
    p99_hourly = ondemand_monthly / 730
    # Target 70% coverage (remainder is variable/spot)
    commitment = p99_hourly * coverage_pct
    # Compute SP: ~30% discount; EC2 SP: ~40% discount
    compute_sp = commitment * 0.70 * 730
    ec2_sp = commitment * 0.60 * 730
    return {"commitment_hourly": round(commitment, 2), "compute_sp_monthly": round(compute_sp, 2), "ec2_sp_monthly": round(ec2_sp, 2)}
```

## Storage Tiering

```
Access Pattern → Tier → Cost (per GB/month, approx) → Retrieval
─────────────────────────────────────────────────────────────
Frequent access       → S3 Standard         $0.023        Immediate
Infrequent (1x/month) → S3 Standard-IA      $0.0125       Immediate + fee
Unknown/changing      → S3 Intelligent-Tiering  Auto      Immediate
Rare (quarterly)      → S3 Glacier Instant  $0.004        Immediate
Archive (yearly)      → S3 Glacier Flexible $0.0036       1-5 min to hours
Compliance (7+ years) → S3 Glacier Deep     $0.0018       12-48 hours
```

### S3 Lifecycle Policy

```json
{
  "Rules": [
    {
      "Id": "TransitionToIA",
      "Status": "Enabled",
      "Filter": { "Prefix": "logs/" },
      "Transitions": [
        { "Days": 30, "StorageClass": "STANDARD_IA" },
        { "Days": 90, "StorageClass": "GLACIER_INSTANT_RETRIEVAL" }
      ],
      "Expiration": { "Days": 365 }
    },
    {
      "Id": "DeleteIncompleteUploads",
      "Status": "Enabled",
      "Filter": {},
      "AbortIncompleteMultipartUpload": { "DaysAfterInitiation": 7 }
    }
  ]
}
```

## Data Transfer Costs

```
Highest → Lowest cost:
  1. Internet egress ($0.05-0.09/GB)        ← Avoid; use CDN
  2. Inter-region ($0.01-0.02/GB)           ← Minimize; replicate only if needed
  3. Inter-AZ ($0.01/GB each way)           ← Colocate services in same AZ
  4. Intra-AZ (free)                        ← Prefer this

Minimization strategies:
  - CDN in front (CloudFront/Cloudflare) reduces origin egress
  - PrivateLink/VPC endpoints for AWS service access (avoid NAT gateway)
  - Colocate services that talk heavily in same AZ
  - Compress payloads (gzip/brotli at API gateway)
  - Cache aggressively at every layer
```

### Data Transfer Cost Estimation

```
Monthly transfer cost for a typical microservice (1 TB out):
  CDN (cached):       0 TB origin egress × $0    = $0
  Direct internet:    1 TB × $0.09/GB             = ~$90
  Cross-region sync:  500 GB × $0.02/GB           = ~$10
  Inter-AZ chatter:   200 GB × $0.01/GB × 2 ways  = ~$4
  Total estimate: ~$104/month
```

## Kubernetes Cost Allocation

### Kubecost / OpenCost

```yaml
# OpenCost deployment (free, CNCF)
helm install opencost opencost/opencost \
  --set opencost.exporter.defaultClusterId=prod-cluster \
  --set opencost.ui.enabled=true
```

### Namespace/Team Chargeback

```
Kubecost provides:
  - Cost by namespace, deployment, pod, label
  - Cost efficiency (CPU/memory requested vs used)
  - Cost allocation by custom label (team, environment, cost-center)

Chargeback formula:
  Team cost = sum(pod costs labeled team=X)
  Efficiency score = resources_used / resources_requested
  Target: > 70% efficiency (30% waste is typical baseline)
```

## Tagging Strategy

### Mandatory Tags

| Tag Key | Example | Purpose | Enforcement |
|---------|---------|---------|-------------|
| `CostCenter` | `eng-platform-42` | Cost allocation/reporting | SCP — deny untagged resource creation |
| `Environment` | `prod` / `staging` / `dev` | Environment-specific rates | SCP — enforce allowed values |
| `Application` | `order-service` | Per-app cost tracking | SCP |
| `Owner` | `platform-team@company.com` | Accountability | SCP |
| `DataClassification` | `internal` / `confidential` / `pii` | Compliance, security | SCP |

### AWS SCP for Tag Enforcement

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RequireCostCenterTag",
      "Effect": "Deny",
      "Action": ["ec2:RunInstances", "rds:CreateDBInstance", "s3:CreateBucket"],
      "Resource": "*",
      "Condition": {
        "Null": { "aws:RequestTag/CostCenter": "true" }
      }
    }
  ]
}
```

## Cost Anomaly Detection

```yaml
# AWS Budget with anomaly detection
aws budgets create-budget \
  --account-id 123456789012 \
  --budget '{
    "BudgetName": "monthly-total",
    "BudgetLimit": {"Amount": "50000", "Unit": "USD"},
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST",
    "CostFilters": {},
    "CostTypes": {"IncludeRefund": false, "IncludeCredit": false}
  }' \
  --notifications-with-subscribers '[{
    "Notification": {"ComparisonOperator": "GREATER_THAN", "Threshold": 80, "ThresholdType": "PERCENTAGE"},
    "Subscribers": [{"SubscriptionType": "EMAIL", "Address": "finops@company.com"}]
  }]'
```

### Alert Thresholds

```
Budget alerts:
  - 50% → Informational (weekly digest)
  - 80% → Warning (email to team leads)
  - 100% → Critical (Slack + PagerDuty; freeze non-essential resources)

Anomaly detection:
  - Daily spend > 40% above expected → Investigate immediately
  - Hourly spike > 200% → Automated check (is it a deploy? expected traffic?)
```

## FinOps Lifecycle

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  INFORM ──→ OPTIMIZE ──→ OPERATE               │
│  (visibility)  (savings)   (governance)         │
│     │              │              │              │
│     ▼              ▼              ▼              │
│  tagging        rightsizing    continuous       │
│  dashboards     RI/SP buying   policy enforce   │
│  cost per team  spot adoption  anomaly alert    │
│  showback       arch changes   chargeback        │
│                                                 │
└─────────────────────────────────────────────────┘

Team responsibilities:
  INFORM:    FinOps analyst — build dashboards, tag compliance, cost visibility
  OPTIMIZE:  Engineering + FinOps — rightsizing, commitment purchasing, architecture
  OPERATE:   Engineering — continuous optimization, policy-as-code, automation
```

## Multi-Cloud Discount Levers

| Cloud | Enterprise Discount | Commitment | Key Lever |
|-------|-------------------|------------|-----------|
| AWS | EDP (Enterprise Discount Program) | 3yr with growth commitment | Total spend volume; multi-service commitment |
| Azure | MACC (Microsoft Azure Consumption Commitment) | 3yr fixed spend | Competitive displacement; Microsoft 365 bundling |
| GCP | CUD (Committed Use Discounts) | 1yr or 3yr | Spend-based CUDs (flexible, no instance lock-in) |

### Negotiation Tips

```
1. Total contract value > $500K/yr → 15-25% discount possible
2. Commit to growth (10-20% YoY) for better rates
3. Multi-year (3yr) gets best discounts — but locks you in
4. Competitive leverage: "AWS offered X; can Azure match?"
5. Bring cloud-agnostic architecture for genuine optionality (and leverage)
6. Negotiate professional services credits, training, and support tiers together
7. Review quarterly — cloud prices drop; renegotiate if market shifted
```

These cost optimization patterns operationalize the finops-engineer skill's Inform → Optimize → Operate lifecycle — turning cloud spend from a black box into a managed, continuously optimized resource.
