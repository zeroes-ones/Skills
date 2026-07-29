# Enterprise Contract Negotiation Playbook

## Key Terms Reference

### Payment Terms

| Term | Standard Position | Fallback | Last Resort |
|------|------------------|----------|-------------|
| Billing cycle | Annual upfront | Semi-annual | Quarterly |
| Payment due | Net-30 | Net-45 | Net-60 |
| Late payment | 1.5% monthly interest | 1% monthly | — |
| Auto-renewal | Yes, with 60-day opt-out | Yes, with 90-day | Mutual opt-in |

### Price Protection

```
Standard: Price locked for initial term (1-3 years)
Renewal cap: Maximum 5-7% annual increase
True-up: Quarterly for usage-based; customer pays overage, no refund for underage

NEVER:
  - Unlimited price lock (>3 years)
  - No renewal cap (allows unlimited increases)
  - Rollover of unused committed volume (creates liability on balance sheet)
```

### Termination

| Type | Standard Position | Rationale |
|------|------------------|-----------|
| For convenience (customer) | 30-90 days written notice | Standard; limit to 90 days max |
| For convenience (vendor) | Not offered | You cannot terminate a paying customer for no reason |
| For cause (either) | 30 days to cure breach | Industry standard; longer = risk |
| For insolvency (either) | Immediate | Protects both parties |
| For change of control | Optional — triggers if competitor acquires customer | Protect IP access |

### Liability

```
Standard: Cap at fees paid in prior 12 months
Aggressive: Cap at fees paid in prior 24 months (for large strategic deals)
NEVER: Unlimited liability — unacceptable in any enterprise contract

Carve-outs from liability cap (uncapped):
  - IP infringement indemnification
  - Confidentiality breach
  - Gross negligence or willful misconduct
  - Payment obligations (customer must pay what they owe)
```

### Data Portability

```
Standard: Export in industry-standard format (CSV, JSON, PDF)
Timeline: 30 days post-termination to export data
Data deletion: 90 days post-termination, certified deletion confirmation
GDPR: Data Processing Agreement (DPA) with Standard Contractual Clauses (SCCs)

NEVER:
  - Proprietary export format only
  - Data held hostage ("pay to get your data")
  - Indefinite data retention without customer consent
```

## Red-Flag Contract Terms

| Term | Risk | Recommended Response |
|------|------|---------------------|
| **MFN (Most Favored Nation)** | Constrains all future pricing. Every deal references this one | Strike entirely. If unavoidable: scope to exact product, volume, geo, 12-month window |
| **Unlimited liability** | One incident could bankrupt the company | Cap at 12-24 months fees. Non-negotiable |
| **IP assignment** | Customer owns your product IP | License, never assign. "Customer owns their data; vendor owns the platform" |
| **Non-compete (broad)** | Can't sell to entire industry verticals | Narrow to direct competitive products only |
| **Indemnification (broad)** | You indemnify customer for all third-party claims | Limit to IP infringement claims only; exclude customer-modified scenarios |
| **Acceptance testing (open-ended)** | Customer can reject delivery indefinitely | 30-day acceptance period with specific, measurable criteria |
| **Right to audit (unlimited)** | Customer can audit your books anytime | Annual audit by mutually agreed third-party auditor, customer pays unless >5% discrepancy |
| **SLA with uncapped credits** | One bad month wipes out all revenue | Cap SLA credits at 25-50% of monthly fees |

## Negotiation Playbook

### Champion's Deck (Internal Selling Tool)

```
Slide 1: Executive Summary — "What you'll achieve with [Product]"
Slide 2: Current State — Pain points, costs, risks of status quo
Slide 3: Future State — With [Product]: quantified outcomes
Slide 4: ROI Summary — 3-year NPV, payback period, key assumptions
Slide 5: Implementation Timeline — Phased rollout, milestones, success criteria
Slide 6: Competitor Comparison — Why [Product] vs alternatives (not just features — outcomes)
Slide 7: Risk Mitigation — Security, compliance, data portability, SLA commitments
Slide 8: Customer Evidence — "Companies like yours achieved X" (logos, quotes)
Slide 9: Investment Summary — Total cost, payment terms, next steps
```

### Concession Plan

| You Can Give (Low Cost) | You Must Hold (High Cost) |
|------------------------|--------------------------|
| Payment terms (Net-45) | Price (discount beyond threshold) |
| Training credits | IP ownership |
| Extended support during transition | Liability cap |
| Executive sponsor access | MFN clauses |
| Product roadmap influence (advisory board) | Termination for convenience (vendor side) |
| Co-marketing / case study | Data ownership |
| Extended pilot period with clear criteria | SLA credits without cap |

### BATNA Framework

```
BATNA (Best Alternative To Negotiated Agreement):

1. What happens if this deal doesn't close?
   - Pipeline coverage: Do you have 3x pipeline for this quarter?
   - Revenue impact: $[X] gap in forecast
   - Strategic impact: No presence in [industry/geo]

2. Walk-away point:
   - Price floor: $[X] ACV (below this, deal is unprofitable)
   - Terms dealbreakers: MFN, unlimited liability, IP assignment
   - Red flags: More than 2 dealbreaker terms = walk

3. Strengthen your BATNA:
   - Parallel deals: Never negotiate only one deal at a time
   - Pipeline sufficiency: 3x quota coverage reduces desperation
   - Time pressure: End-of-quarter leverage works against you too
```

### Negotiation Timeline

| Week | Activity | Output |
|------|----------|--------|
| 1 | Discovery call, identify champion, understand budget cycle | Qualified opportunity |
| 2-3 | Technical validation, POC if needed, ROI quantification | ROI deck, technical win |
| 4-5 | Commercial proposal, pricing discussion, champion deck delivery | Verbal agreement on price |
| 6-8 | Legal review, MSA/DPA/SLA negotiation, security review | Redlines resolved |
| 9-10 | Procurement process, final approvals, PO issued | Signed contract |
| Ongoing | QBR setup, onboarding, CSM introduction | Customer success transition |
