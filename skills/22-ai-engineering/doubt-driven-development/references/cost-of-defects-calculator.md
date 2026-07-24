# Cost of Defects Calculator

## When Is Doubt-Driven Development Worth the Investment?

Doubt-driven development adds 15-45 minutes per PR in review overhead. Whether this
investment is justified depends on the cost of defects in your domain.

## Defect Cost Curves by Industry

| Industry | Avg Cost per Production Defect | Doubt-Driven ROI Threshold |
|---|---|---|
| **Healthtech (patient-facing)** | $50K-$500K (regulatory, liability, patient harm) | Any PR touching patient data or clinical logic |
| **Fintech (transactions)** | $25K-$250K (financial loss, compliance, audit) | Any PR touching money movement or ledger |
| **E-commerce (checkout)** | $10K-$100K (lost revenue, oversell, chargebacks) | PRs touching payment, inventory, or cart |
| **Infrastructure/SaaS** | $5K-$50K (downtime, SLA violation, customer churn) | PRs touching auth, data plane, or multi-tenancy |
| **Internal tools** | $500-$5K (lost productivity, manual workaround) | PRs > 200 lines with data mutation |
| **Marketing website** | $100-$1K (minor UX issue, quick fix) | Not worth it — use standard review |

## Break-Even Analysis

```
Cost of doubt-driven review = (review_time_hours × engineer_hourly_rate) + (API costs)

Example: 200-line PR, 12 claims extracted, 28 doubt cycles
  Review time: 45 min (0.75h)
  Engineer rate: $150/h (fully loaded)
  API costs (cross-model): $5
  Total cost: $117.50

Break-even defect cost: $117.50 / (probability of catching defect × effectiveness)
  If adversarial review catches 30% more defects than standard review:
  Break-even = $117.50 / 0.30 = $391.67

A single defect with cost > $392 justifies the doubt-driven review.
```

## ROI Calculator

```
ROI = (DEFECTS_PREVENTED × AVG_DEFECT_COST) - (PRs_REVIEWED × REVIEW_COST_PER_PR)

Example: Fintech team, 50 PRs/month, 20% touch critical paths
  PRs receiving doubt-driven review: 10/month
  Defects caught per 10 PRs: 3 (30% discovery rate × 10 PRs)
  Avg defect cost: $75K
  Value of defects prevented: $225K/month
  Cost of reviews: 10 × $117.50 = $1,175/month
  ROI: ($225,000 - $1,175) / $1,175 = 190x return
```

## When Doubt-Driven Development LOSES Money

### Scenario 1: Low-Defect-Cost Domain
Internal dashboard PR, defect cost ~$500.
- Review cost: $117.50
- Break-even: must catch defect in 24% of reviews
- Reality: internal dashboards have ~5% discovery rate
- **Verdict:** Do not use. Standard review is sufficient.

### Scenario 2: Trivial Changes
Log-level change, 3 lines. Defect cost: near zero.
- Review cost: $15 (quick scan only)
- Break-even: effectively infinite (defect cost approaches $0)
- **Verdict:** Do not use. Even quick scan is overkill.

### Scenario 3: Prototype Code
Throwaway prototype, no production deployment.
- Cost of ANY defect in prototype: $0 (by definition, it's throwaway)
- Review cost: $117.50
- **Verdict:** Do not use. Zero-value activity.

## Cost Escalation Factors

These factors multiply the cost of a defect. Use them to estimate impact:

| Factor | Multiplier | Example |
|---|---|---|
| **Data loss or corruption** | 10x | Deleted customer records → $50K → $500K |
| **Security breach** | 20x | Exposed PII → $25K → $500K (regulatory fines + notification) |
| **Regulatory violation** | 15x | HIPAA violation → $10K → $150K (per violation) |
| **Revenue interruption** | 5x/hour | 4h e-commerce outage → $10K/h → $40K |
| **Reputation damage** | 2-10x | Public incident → churn, negative press, trust erosion |
| **Cascading failure** | 3-8x | Bug in shared library → affects 4 services |

## Quick Decision Matrix

| Code Change Type | Defect Cost Estimate | Use Doubt-Driven? |
|---|---|---|
| Auth middleware | $50K-$500K | **YES — mandatory** |
| Payment processing | $25K-$250K | **YES — mandatory** |
| Database migration (destructive) | $20K-$200K | **YES — mandatory** |
| LLM output delivery | $10K-$100K | **YES — recommended** |
| New API endpoint | $5K-$50K | **YES — if > 50 lines** |
| Bug fix (critical path) | $5K-$25K | **YES — doubt the fix AND surrounding code** |
| Refactoring (no behavior change) | $1K-$10K | **Quick scan — extract behavior-preservation claims** |
| Dependency update (minor) | $500-$5K | **Quick scan — extract changelog claims** |
| UI text change | $100-$500 | **NO — standard review** |
| Log line addition | $50-$200 | **NO — standard review** |
| Comment update | $0-$50 | **NO — skip review** |
