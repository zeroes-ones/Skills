# Cost Calibration — Loaded Rates, Bug Costs, Maintenance Overhead

> **NOTE:** For dynamic, invocation-time rate research, use `scripts/calculate-roi.sh --auto-research`.
> This file documents the baseline assumptions and methodology.

## Loaded Developer Cost by Region (2024 Baseline)

"Loaded" = salary + benefits (30%) + equipment/office (20%) + management overhead (15%) ≈ 2× base salary.

| Region | Hourly Rate | Annual Loaded | Basis |
|--------|------------|---------------|-------|
| US SF/NYC | $275/hr | ~$550K | FAANG-tier, top-of-market |
| US Other Metro | $175/hr | ~$350K | Major tech hubs (Austin, Seattle, Denver) |
| US Remote | $125/hr | ~$250K | Distributed workforce |
| Western Europe | $150/hr | ~$300K | London, Berlin, Amsterdam |
| Eastern Europe | $80/hr | ~$160K | Warsaw, Prague, Bucharest |
| India | $60/hr | ~$120K | Bangalore, Hyderabad, Pune |
| Southeast Asia | $45/hr | ~$90K | Singapore, Bangkok, Manila |
| Australia | $160/hr | ~$320K | Sydney, Melbourne |
| Canada | $140/hr | ~$280K | Toronto, Vancouver |
| Latin America | $65/hr | ~$130K | Mexico City, São Paulo, Buenos Aires |

**CPI Adjustment:** Rates compound at ~3% annually from 2024 baseline. Use `--auto-research` flag for current-year adjustment.

## Typical Bug Costs (Annualized)

| Bug Severity | Cost Range | Example |
|-------------|------------|---------|
| P0 — Full outage | $50K–$500K+/hour | Checkout broken, auth down |
| P1 — Major feature broken | $10K–$50K/day | Search returning empty, payments degraded |
| P2 — Minor feature broken | $1K–$5K/week | Admin panel glitch, edge case form error |
| P3 — Cosmetic | $100–$1K/year | Misaligned button, wrong shade of blue |

## Maintenance Overhead

| Change Type | Annual Maintenance | Basis |
|------------|-------------------|-------|
| New feature | 15–20% of build cost/year | Ongoing bug fixes, dependency updates |
| Refactor | 5–10% of build cost/year | Reduced if simplifying, increased if adding abstraction |
| Migration | 20–30% of build cost/year | Dual-run period, compatibility shims |
| Optimization | 2–5% of build cost/year | Performance regressions from future changes |

## Cloud Cost Factors

| Resource | Approximate Cost | Notes |
|----------|-----------------|-------|
| Database read replica | $150–$500/month | AWS RDS, depending on instance size |
| Redis/ElastiCache | $70–$300/month | Cache layer to reduce DB pressure |
| Lambda execution | $0.20/1M requests | Plus compute time |
| S3 storage | $0.023/GB/month | Standard tier |
| Data transfer (egress) | $0.09/GB | First 10TB, decreases with volume |
| Idle EC2 instance | $35–$700/month | t3.medium to c5.4xlarge |

## ROI Formula

```
ROI = (Annual_Value − Annual_Maintenance_Cost) / Development_Cost

Where:
  Annual_Value = Traffic_Impact_Value + Bug_Prevention_Value + Revenue_Impact
  Development_Cost = Dev_Hours × Hourly_Rate + Risk_Premium + Cloud_Cost
  Risk_Premium = Migration_Changes × 0.15 + API_Changes × 0.10 + Infra_Changes × 0.20
```

**Gate thresholds:**
- TRIVIAL: Cost < $500 → auto-pass
- MODERATE: Cost < $5,000 → quick analysis required
- MAJOR: Cost ≥ $5,000 → full business case required

**Decision rule:** If Annual_Value > Development_Cost AND payback < 24 months → PROCEED. Else → BORDERLINE (human decision). If payback > 36 months → STOP.
