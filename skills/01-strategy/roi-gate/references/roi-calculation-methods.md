# ROI Calculation Methods
> Reference for `roi-gate` — loaded on demand for deep analysis

## Loaded Cost Estimation

Default loaded costs for ROI calculations. Verify against actual team costs.

| Region | Loaded Cost/Engineer-Hour | Loaded Cost/Engineer-Week | Notes |
|---|---|---|---|
| US (SF/NYC) | $200-$300 | $8,000-$12,000 | Includes salary + benefits + office + equipment |
| US (other metro) | $150-$200 | $6,000-$8,000 | |
| US (remote LCOL) | $100-$150 | $4,000-$6,000 | |
| Western Europe | $120-$180 | $4,800-$7,200 | |
| Eastern Europe | $60-$100 | $2,400-$4,000 | |
| India | $40-$80 | $1,600-$3,200 | |
| Southeast Asia | $30-$60 | $1,200-$2,400 | |

**Rule:** Always use the higher end of the range for ROI estimates. Being conservative about costs prevents
false-positive ROI decisions.

## Bug Cost Estimation

| Bug Severity | Investigation (hours) | Fix (hours) | Deploy/Verify (hours) | Total Cost (US metro) |
|---|---|---|---|---|
| Critical (SEV1) | 2-4 | 1-4 | 1-2 | $600-$1,500 |
| High (SEV2) | 1-2 | 1-2 | 0.5-1 | $375-$750 |
| Medium (SEV3) | 0.5-1 | 0.5-1 | 0.5 | $225-$375 |
| Low (SEV4) | 0.25 | 0.25-0.5 | 0.25 | $113-$188 |

**Cost of a bug in production:** Above + lost revenue + reputational damage + support tickets.
Use 3x the base cost for production bugs vs development bugs.

## Net Present Value (NPV) Calculation

```
NPV = ∑(Cash Flow_t / (1 + r)^t) - Initial Investment

Where:
- Cash Flow_t = Annual Benefit_t - Annual Cost_t
- r = discount rate (use 10% for software projects)
- t = year (1, 2, 3)

Example:
Year 1: ($50,000 benefit - $10,000 maintenance) / 1.10 = $36,364
Year 2: ($50,000 benefit - $10,000 maintenance) / 1.21 = $33,058
Year 3: ($50,000 benefit - $10,000 maintenance) / 1.331 = $30,053
Total PV of benefits: $99,475
Initial investment: $100,000
NPV: -$525 → Negative. Do not proceed.
```

## Risk Quantification

```
Risk Cost = Probability of Failure × Cost of Failure

Example risks:
- Migration breaks production: 5% × $50,000 = $2,500
- New library has critical bug: 2% × $10,000 = $200
- Data corruption during migration: 1% × $100,000 = $1,000
- Deployment fails, rollback needed: 10% × $2,000 = $200

Total risk cost: Sum of all quantified risks above

Never skip risk quantification. "It probably won't fail" is not a risk assessment.
```

## Dependency Maintenance Cost

```
Annual maintenance hours per dependency:
- Active (> 1 release/month): 4-8 hours/year (breaking changes, API changes)
- Stable (< 4 releases/year): 2-4 hours/year (security patches, compatibility)
- Sunsetting (< 2 releases/year): 1-2 hours/year (minimal updates, monitor for EOL)
- Abandoned: Do not add (or budget migration cost upfront)

3-year maintenance cost = Annual hours × loaded cost/hour × 3

Example: Adding React (active) — 6 hours/year × $150/hour × 3 years = $2,700
Example: Adding lodash (stable) — 3 hours/year × $150/hour × 3 years = $1,350
```

## Abstraction Overhead Calculation

```
Annual abstraction overhead per layer:
- Maintenance: 5-10 hours/year (interface changes, test updates)
- Onboarding: 2 hours × new hires/year
- Debugging overhead: 20% slowdown × hours spent debugging in this module/year
- Testing: N mock classes × 1 hour/year maintenance each

Example: Repository pattern with 5 DAOs, 5 mocks, 2 new hires/year
= 8 hours maintenance + 4 hours onboarding + 10 hours debugging + 5 hours mocks
= 27 hours/year × $150/hour = $4,050/year

Over 3 years: $12,150. This abstraction must deliver > $12,150 in value.
```

## Opportunity Cost Calculation

```
What is the team NOT building while doing this?

Opportunity cost = (estimated hours for this task) × (value per hour of best alternative)

If the team could be:
- Building a revenue-generating feature: $200-$500/hour
- Fixing customer-reported bugs: $100-$200/hour (reduced churn)
- Reducing tech debt that slows delivery: $50-$150/hour
- Doing nothing (unused capacity): $0/hour

Rule: If the opportunity cost is higher than the task's value, don't do the task.
A refactor that costs $50K prevents a $200K revenue feature. Do the feature.
