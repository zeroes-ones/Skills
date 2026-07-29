# Deal Desk Operations Reference

## CPQ (Configure-Price-Quote) Workflow

### Quote-to-Close Stages

```
Discovery
  ↓ (AE qualifies opportunity, identifies budget, timeline, champion)
Configuration
  ↓ (AE builds quote: products, seats, term, discounts)
Pricing Committee (if discount >AE authority)
  ↓ (VP/CFO review based on approval matrix)
Approval
  ↓ (All required approvers sign off, CPQ system records approval chain)
Proposal
  ↓ (Formal proposal sent: product, pricing, terms, ROI summary)
Negotiation
  ↓ (Contract terms, legal review, redlines)
Close
  ↓ (Signed MSA + Order Form, PO received, invoice sent)
```

### CPQ Tools Comparison

| Tool | Best For | Pricing | Key Feature |
|------|----------|---------|------------|
| **Salesforce CPQ** | Salesforce-native teams, complex product bundles | $75-$150/user/month | Guided selling, approvals, DocuSign integration |
| **DealHub** | Mid-market, fast deployment | $40-$80/user/month | Interactive quotes, e-sign, usage-based pricing |
| **PandaDoc** | SMB-mid, document-centric sales | $19-$49/user/month | Proposal automation, content library |
| **Configure One** | Manufacturing, highly configurable products | Custom quote | Complex product configuration rules |
| **Custom (spreadsheets)** | Early stage (<10 enterprise deals) | Cost of errors | None — high error rate |

## Approval Matrix Design

### Tiered Approval Structure

```
Deal Value Tiers:
  <$25K ACV → AE authority
  $25K-$100K → VP Sales + Deal Desk review
  $100K-$500K → VP Sales + CFO
  $500K-$1M → VP Sales + CFO + CEO
  >$1M → Board notification (informational, not approval)

Discount Tiers (cross product of deal value):
  <10% → AE authority
  10-25% → VP Sales
  25-40% → CFO
  >40% → CEO
```

### Approval Trigger Matrix

| Trigger | Reviewer | SLA |
|---------|----------|-----|
| Custom MSA terms (non-standard) | Legal | 72hr |
| Custom SLA (above 99.9%) | CTO/VP Eng | 48hr |
| Data residency (new region) | CISO/VP Eng | 1 week |
| Payment terms >Net-45 | CFO | 48hr |
| MFN clause request | CFO + CEO | 1 week |
| IP indemnification (broad) | Legal + CTO | 72hr |
| Source code escrow | CTO + Legal | 1 week |

## Deal Desk SLAs

| Deal Priority | Definition | Quote Turnaround | Approval Turnaround | Escalation |
|-------------|-----------|-----------------|-------------------|-----------|
| **Standard** | New business, no time pressure | 48hr | 72hr | Deal desk manager after 72hr |
| **Priority** | Competitive deal, Q-end | 24hr | 48hr | VP Sales after 48hr |
| **Strategic** | Logo acquisition, must-win | 4hr | 24hr | CEO/CRO after 24hr |

## Deal Desk Metrics

### KPIs to Track

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Quote-to-close time | <30 days | 30-60 days | >60 days |
| Approval cycle time | <48hr | 48-96hr | >96hr |
| Quote accuracy (no revisions) | >90% | 80-90% | <80% |
| Discount rate (average) | <15% | 15-25% | >25% |
| Deal desk touches per deal | <2 | 2-4 | >4 |
| Win rate (enterprise) | >25% | 15-25% | <15% |

### Deal Desk Health Dashboard

```
Weekly Pulse:
  - Deals in approval: [count]
  - Deals stalled >48hr: [count] ← INVESTIGATE
  - Average discount this month: [%]
  - Deals requiring >2 revisions: [count] ← Process issue
  - ACV average this quarter: [$]
  - Pipeline coverage (this quarter): [ratio] (target: 3x)
```

## Special Pricing Programs

### Non-Profit / Education Pricing

| Program | Discount | Requirements |
|---------|----------|-------------|
| Non-profit | 25-50% off list | 501(c)(3) or equivalent verification |
| Education (K-12) | 30-50% off list | .edu email or accreditation |
| Higher Education | 20-40% off list | .edu email, academic use only |
| Government | GSA schedule or equivalent | Government purchase order |
| Startup program | 50-90% off Year 1, ramps to list | <$10M funding, <50 employees |

### Competitive Displacement Program

```
Standard: Up to 25% additional discount to displace competitor
Requirements:
  1. Active competitor contract (invoice proof)
  2. Contract end date within 6 months
  3. Commit to multi-year term (2+ years)
  4. Case study participation (after 6 months)
  5. Migration costs absorbed by customer
```
