# Enterprise ROI Calculators

## Value Quantification Methodology

### The Value Stack

```
Tier 1: Direct Cost Savings
  |-- Labor: hours saved × fully-loaded hourly cost × # of users
  |-- Infrastructure: replaced systems, eliminated licenses
  |-- Efficiency: reduced process time, fewer errors, automation gains

Tier 2: Revenue Uplift
  |-- Increased conversion: % improvement × current revenue
  |-- Faster time-to-market: weeks saved × weekly revenue contribution
  |-- New revenue streams: enabled by product capabilities

Tier 3: Risk Reduction
  |-- Compliance fines avoided: GDPR ($20M or 4% global revenue), HIPAA ($50K-$1.5M/violation)
  |-- Downtime cost avoided: (hours × revenue/hour) × improvement in uptime
  |-- Security breach cost: average breach cost ($4.45M in 2023) × risk reduction %
```

### ROI Formula

```
ROI = (Value Generated - Total Cost) / Total Cost × 100%
Payback Period = Total Cost / Monthly Value Generated
3-Year NPV = Σ(Year 1-3 Value / (1 + discount_rate)^year) - Total Cost
```

## ROI Calculator Design

### Required Inputs (Customer-Facing)

| Input | Type | Default | Source |
|-------|------|---------|--------|
| Number of users | Integer | — | Customer provides |
| Average fully-loaded hourly cost | Currency | $75/hr (tech), $50/hr (general) | Industry benchmark |
| Hours saved per user per week | Decimal | — | Case study data |
| Current process cost (annual) | Currency | — | Customer provides OR industry benchmark |
| Current downtime hours/year | Decimal | — | Customer IT data |
| Cost per hour of downtime | Currency | $5,600/min (Gartner 2014, adjusted) | Industry benchmark |

### Calculator Outputs

| Output | Formula |
|--------|---------|
| Annual Labor Savings | users × hourly_cost × hours_saved_per_week × 52 |
| Annual Efficiency Gain | current_process_cost × efficiency_improvement_% |
| Annual Downtime Savings | downtime_hours × cost_per_hour × uptime_improvement_% |
| Total Annual Value | labor_savings + efficiency_gain + downtime_savings |
| Your Annual Price | [quoted price] |
| Net Annual Benefit | total_value - annual_price |
| ROI | (net_benefit / annual_price) × 100% |
| Payback Period (months) | (annual_price / monthly_value) |

### Defensibility Checklist

- [ ] All inputs have published sources (Bureau of Labor Statistics, Gartner, Forrester, internal case study)
- [ ] Customer can adjust all inputs — transparency builds trust
- [ ] Conservative defaults — better to underpromise and overdeliver
- [ ] Includes sensitivity analysis: "If hours saved is 20% less, ROI still 3.2x"
- [ ] CFO-ready: Can the customer's CFO reproduce these numbers?

## Benchmark Data Sources

| Source | Data Type | Cost | Best For |
|--------|-----------|------|----------|
| **Bureau of Labor Statistics** | Fully-loaded labor costs by occupation | Free | Labor savings calculations |
| **Gartner IT Key Metrics** | IT spending benchmarks, downtime costs | $30K+/year | IT efficiency, infrastructure ROI |
| **Forrester Total Economic Impact** | Commissioned ROI studies | $50K-$100K | Third-party validated ROI for enterprise sales |
| **IDC Business Value** | Sponsored ROI white papers | $30K-$60K | Technology-specific value quantification |
| **Internal customer survey** | Actual customer results | Cost of survey | Most credible, hardest to gather early |
| **Glassdoor / Levels.fyi** | Salary data for loaded cost | Free | Proxy for fully-loaded labor costs |
| **IBM/Ponemon Cost of Data Breach** | Breach cost benchmarks | Free (annual report) | Security ROI calculations |

## Value-Based Price Ceiling

```
Value-Based Price = Total Annual Value × Value Capture Rate

Value Capture Rate Guidelines:
  - 10%: Conservative, easily defensible, low churn risk
  - 20%: Balanced, industry standard
  - 30%: Aggressive, requires strong differentiation and proof
  - >30%: Customer sees net negative, expect pushback and churn
```

### Example

```
Customer saves $500K/year using your product
  → 10% capture: $50K/year — easy yes, you're leaving money on table
  → 20% capture: $100K/year — balanced, CFO can justify
  → 30% capture: $150K/year — aggressive, need strong proof points
  → 40% capture: $200K/year — customer questions if they should build in-house
```
