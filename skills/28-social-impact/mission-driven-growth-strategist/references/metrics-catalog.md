# Mission-Driven Growth Metrics Catalog

## KPI Library

### Impact Metrics (Depth)

| Metric | Formula | IRIS+ Code | Benchmark | Dashboard |
|---------|---------|-----------|-----------|-----------|
| Beneficiary Outcome Achievement Rate | % of beneficiaries achieving target outcome / total served | Custom | N/A (org-specific) | Monthly by program |
| Depth Score | Average magnitude of change on primary outcome indicator | Custom | Baseline vs target | Quarterly |
| Beneficiary Net Promoter Score (bNPS) | % Promoters - % Detractors | N/A | >30 is good, >50 is excellent | Quarterly |
| Quality-Adjusted Life Years (QALYs) | Years of life × health utility weight | N/A | Cost/QALY < GDP per capita = cost-effective | Annually |
| Multi-Dimensional Poverty Index Change | Change in MPI score pre/post | PI2828 proxy | 10%+ reduction meaningful | Annually |
| SROI Ratio | Social value ($) / Investment ($) | Custom | >$3:1 is strong | Annually |

### Reach Metrics (Breadth)

| Metric | Formula | IRIS+ Code | Benchmark | Dashboard |
|---------|---------|-----------|-----------|-----------|
| Client Individuals Reached | Unique individuals served in period | PI4060 | YoY growth target | Monthly |
| Client Individuals: Female | Unique female clients | PI8330 | Depends on target population | Monthly |
| Client Individuals: Poor | Unique clients below poverty line | PI2828 | Depends on mission | Monthly |
| Geographic Coverage | # of communities/regions served | Custom | Expansion plan | Quarterly |
| Program Completion Rate | % of enrolled beneficiaries completing program | Custom | >80% target | Monthly |

### Organizational Health Metrics

| Metric | Formula | Benchmark | Dashboard |
|---------|---------|-----------|-----------|
| Grant Dependency Ratio | Grant revenue / Total revenue | Target <50% by year 5 | Quarterly |
| Earned Revenue Ratio | Earned revenue / Total revenue | Target >25% by year 5 | Quarterly |
| Revenue Diversification Index | Herfindahl-Hirschman Index of funding sources | <2,500 (moderately concentrated) | Quarterly |
| Fundraising Efficiency | Fundraising cost / Funds raised | <$0.25 per $1 raised (nonprofit standard) | Annually |
| Program Efficiency | Program spend / Total spend | >75% (nonprofit) or mission-aligned (social enterprise) | Quarterly |
| Runway (months) | Cash / Monthly burn | >12 months target, >6 months minimum | Monthly |
| Blended Cost of Capital | Weighted average cost across all capital sources | Compare to returns generated | Annually |

### Mission Fidelity Metrics

| Metric | Formula | Trigger Threshold | Dashboard |
|---------|---------|------------------|-----------|
| Target Beneficiary Revenue % | Revenue from target beneficiaries / Total | <60% triggers review | Quarterly |
| Mission-Aligned Program % | Spend on ToC-aligned programs / Total program spend | <80% triggers review | Quarterly |
| Beneficiary Depth Trend | Depth score this period vs prior period | >10% decline triggers review | Quarterly |
| Staff Mission Alignment | % staff who can articulate ToC / Total | <70% triggers review | Annually |
| Partner Mission Alignment | % partners who meet mission criteria | <80% triggers review | Annually |

### Systems Change Metrics

| Metric | Definition | Measurement Method | Timeframe |
|---------|-----------|-------------------|-----------|
| Policy Changes Influenced | # of laws, regulations, policies changed | Policy tracking database | Annually |
| Sector Standards Shifted | # of organizations adopting new practices | Sector survey or industry data | 2-3 years |
| Narrative Change | Media mentions, public discourse shift | Media analysis, social listening | Quarterly |
| Field Building | # of organizations replicating model | Replication tracking | Annually |
| Power Shift | Beneficiaries in decision-making roles | Governance tracking | Annually |

## Dashboard Design

### Board Dashboard (Quarterly)

```
┌─────────────────────────────────────────────────────────┐
│ MISSION FIDELITY DASHBOARD — Q3 2026                     │
├─────────────────────────────────────────────────────────┤
│ IMPACT                   │ ORGANIZATIONAL HEALTH         │
│ ● Beneficiaries: 12,450  │ ● Grant dependency: 42%       │
│ ● Outcome rate: 73%      │ ● Earned revenue: 28%         │
│ ● bNPS: 42               │ ● Runway: 14 months           │
│ ● SROI: $3.80 : $1       │ ● Revenue growth: 18% YoY     │
├─────────────────────────────────────────────────────────┤
│ MISSION FIDELITY         │ FLAGS                        │
│ ● Target beneficiary %: 78%│ ● Grant dependency ↓ (good) │
│ ● Beneficiary depth: +5%  │ ● Target beneficiary % ←     │
│ ● Program alignment: 88%  │   (watch: below 80% trigger) │
└─────────────────────────────────────────────────────────┘
```

### Impact Investor Dashboard (Quarterly)

| IRIS+ Metric | Target | Actual | Status |
|-------------|--------|--------|--------|
| PI4060 — Client Individuals | 15,000 | 12,450 | 🟡 83% |
| PI3687 — Jobs Created | 50 | 47 | 🟢 94% |
| PI8330 — Female Clients | 60% | 64% | 🟢 Above |
| PI2828 — Poor Clients | 70% | 68% | 🟡 97% |
| OI5411 — CO2 Reduced (t) | 500 | 420 | 🟡 84% |

### Fundraising Dashboard (Monthly)

```
FUNDING FUNNEL — October 2026
├── Pipeline: $4.2M across 18 opportunities
│   ├── Grants: $1.8M (6 applications)
│   ├── Impact Investment: $1.5M (4 conversations)
│   ├── Earned Revenue: $600K (5 contracts)
│   └── Government: $300K (3 RFPs)
├── Closed: $1.1M this quarter
│   ├── Win rate: 45%
│   └── Avg time to close: 4.2 months
└── At Risk: $800K (2 opportunities stalled >6 months)
```

## Formulas Reference

### SROI Calculation

```
SROI = Σ (Outcome quantity × Financial proxy × (1 - Deadweight - Attribution - Displacement)) / Total investment

Where:
- Deadweight: % of outcome that would have happened anyway
- Attribution: % of outcome attributable to others
- Displacement: % of outcome that displaced other positive outcomes
- Drop-off: % reduction in outcome persistence each year
```

### Revenue Diversification (HHI)

```
HHI = Σ (Revenue share of source i)²

Interpretation:
- <1,500: Unconcentrated (healthy)
- 1,500-2,500: Moderately concentrated (monitor)
- >2,500: Highly concentrated (actively diversify)
```

### Beneficiary Net Promoter Score (bNPS)

```
bNPS = % Promoters (score 9-10) - % Detractors (score 0-6)

Question: "On a scale of 0-10, how much has [program] improved your [life area]?"

Benchmarks:
- >50: Excellent (beneficiaries are advocates)
- 30-50: Good (satisfied beneficiaries)
- <30: Needs improvement (passive or detractors)
```
