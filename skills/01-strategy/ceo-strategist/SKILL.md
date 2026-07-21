---
name: ceo-strategist
description: Fundraising strategy, organizational design, equity allocation, cap table management, board governance, and business model validation. Use when planning fundraising, designing org structure, evaluating equity splits, or navigating company-building decisions.
author: Sandeep Kumar Penchala
---

# CEO Strategist

Executive-level strategy for company formation, fundraising, organizational design, and governance. Think like a founder/CEO making resource-constrained decisions under uncertainty.

## When to Use

- Fundraising strategy: when to raise, how much, from whom
- Organizational design: team structure by stage and size
- Equity and cap table planning: founder splits, employee option pools, dilution modeling
- Board governance: composition, meeting cadence, fiduciary duties
- Business model validation and pivoting decisions
- M&A evaluation: buy-side and sell-side strategy
- Company-building through MVP → Growth → Scale phases

## Sub-Skills

When this skill is invoked, drill into these specialized areas as needed:

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `fundraising-strategy` | Raising any round (pre-seed → Series C+) | This file — Fundraising sections |
| `board-management` | Board meetings, governance, investor relations | This file — Equity & Cap Table section |
| `org-design` | Hiring first 10, scaling to 100, 500+ | This file — Organization Design section |
| `competitive-strategy` | Market entry, pivot, defending competitors | `references/` (see business-strategist) |
| `crisis-management` | PR crisis, security breach, down round, co-founder conflict | This file — Anti-Patterns section |
| `m-and-a-strategy` | Acquiring or being acquired | `references/` (create as needed) |
| `vision-to-execution` | Translating 5-year vision to quarterly OKRs | This file — MVP-to-Scale section |

## Decision Trees

### Fundraising: Should You Raise VC?

```
Are you solving a venture-scale problem? (TAM > $1B?)
├── NO → Don't raise VC. Bootstrap, angel, or revenue finance.
│         VC requires 10x+ return. $50M exit = failure for VC.
└── YES → Can you grow 3x+ year-over-year?
    ├── NO → Don't raise VC. Growth equity or strategic investors.
    └── YES → Is the market timing right? (category is hot?)
        ├── NO → Wait. Raise when you have momentum.
        └── YES → Raise. But only what you need for 18-24 months.
```

### When NOT to Raise VC
- [ ] TAM < $1B (VCs need massive outcomes to return their fund)
- [ ] You want to run a lifestyle business ($1-5M ARR, profitable)
- [ ] You can reach profitability within 12 months on existing cash
- [ ] You're in a niche market that won't grow beyond $50M
- [ ] You value full control over company direction
- [ ] Your growth rate is <20% YoY (VCs want 3x+)

### Organization Design by Team Size

| Team Size | Structure | Management Layers | Key Hire | Monthly Burn (US) |
|-----------|----------|-------------------|----------|-------------------|
| **1-5** (MVP) | Everyone does everything. No managers. | 0 | Founding engineer | $40K-80K |
| **5-15** (Seed) | 1-2 functional leads. CEO still product. | 0-1 | First sales hire | $80K-150K |
| **15-30** (Series A) | Functional teams: eng, product, GTM. | 1-2 | VP Engineering or Head of Sales | $200K-400K |
| **30-80** (Series B) | Departments with directors. CEO delegates. | 2-3 | CFO/COO | $500K-1.2M |
| **80-200** (Series C+) | VPs with directors under them. COO runs ops. | 3-4 | CPO, CRO | $1.5M-4M |

## MVP-to-Scale Progression

| Phase | Fundraising | Valuation Driver | Monthly Cost |
|-------|------------|-----------------|--------------|
| **Pre-Seed** ($500K-2M) | Angel/accelerator | Team quality, market size | $30K-60K/mo |
| **Seed** ($2-5M) | Seed funds, angels | Early traction, PMF signals | $80K-150K/mo |
| **Series A** ($8-20M) | Tier 1/2 VCs | Revenue growth rate, retention | $200K-400K/mo |
| **Series B** ($20-50M) | Growth funds | Efficient growth, unit economics | $500K-1M/mo |
| **Series C+** ($50M+) | Late-stage, PE | Path to profitability, market leadership | $1.5M+/mo |

## Fundraising Cost by Round

| Round | Typical Raise | Dilution | Legal Cost | Time to Close |
|-------|-------------|----------|-----------|---------------|
| Pre-Seed (SAFE) | $500K-2M | 10-20% (cap dependent) | $5K-15K | 4-8 weeks |
| Seed (Priced) | $2-5M | 15-25% | $30K-60K | 8-12 weeks |
| Series A | $8-20M | 18-25% | $60K-120K | 12-16 weeks |
| Series B | $20-50M | 15-20% | $100K-200K | 12-16 weeks |
| Series C | $50M+ | 10-15% | $200K-400K | 12-20 weeks |

**Fundraising math:** A successful fundraise takes 3-6 months full-time for CEO. At $200K/year opportunity cost, a 4-month raise costs $67K in lost CEO time PLUS legal costs.

## Equity & Cap Table

### Option Pool Sizing
| Stage | Pool Size | Notes |
|-------|-----------|-------|
| Pre-Seed | 10-15% | Larger pool = less dilution at next round |
| Seed | 10-15% | Refresh pool before priced round |
| Series A | 15-20% | VCs will require this; refresh pre-money |
| Series B+ | 10-15% | Ongoing refresh for key hires |

### Employee Equity by Role (Seed/Series A)
| Role | Equity Range |
|------|-------------|
| CTO (co-founder) | 10-30% (4-year vest, 1-year cliff) |
| VP Engineering (#1-5 hire) | 1-3% |
| Senior Engineer (#5-20) | 0.2-0.5% |
| Engineer (#20+) | 0.05-0.2% |
| VP Sales | 0.5-2% |
| Head of Product | 0.5-1.5% |

## Cross-Skill Coordination

The CEO sits at the center of all strategic decisions. Coordination failures here cascade into every function — product builds the wrong thing, engineering builds it wrong, sales sells to the wrong market.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **CTO Advisor** | Build vs buy, tech strategy, architecture decisions, hiring plan | Engineering capacity, technical feasibility, cost of technical debt |
| **Product Strategist** | Product roadmap, PMF assessment, pivot decisions | Market signals, resource constraints, strategic trade-offs |
| **Business Strategist** | Fundraising, market entry, pricing, GTM | Unit economics, TAM/SAM/SOM, revenue projections, cash runway |
| **Legal Advisor** | Fundraising (term sheets, SAFE/equity), IP strategy, compliance, co-founder agreements | Deal terms, regulatory exposure, data privacy obligations |
| **Board/Investors** | Quarterly board meetings, fundraising updates, major pivots | Financials, KPIs, risks, capital allocation, hiring progress |
| **VP Sales / CRO** | Revenue targets, GTM strategy, compensation, territory design | Quota attainment, pipeline health, win/loss analysis, pricing feedback |
| **Head of People / HR** | Culture, hiring plan, org design, compensation philosophy | Burnout signals, retention risks, diversity metrics, leadership gaps |
| **Finance / CFO** | Budgeting, runway management, financial modeling, fundraise preparation | Burn rate, cash out date, revenue forecast, headcount plan |
| **Marketing Lead** | Brand positioning, launch strategy, demand gen | ICP definition, messaging, channel performance, competitive positioning |
| **Operations** | Process scaling, vendor management, facilities, compliance | Operational bottlenecks, cost drivers, automation opportunities |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Fundraising round opening | CTO Advisor, Business Strategist, Legal Advisor, Finance | Due diligence prep, data room, financial modeling, term sheet negotiation |
| Pivot decision | CTO Advisor, Product Strategist, Board | Architecture replanning, roadmap overhaul, investor communication |
| Co-founder departure/conflict | Legal Advisor, Board, Head of People | Equity implications, leadership gap, team morale, retention risk |
| Cash running below 6 months runway | Finance, Board, CTO Advisor | Emergency fundraising, cost cutting, hiring freeze decisions |
| Major customer loss (>10% revenue) | VP Sales, Product Strategist, Board | Churn analysis, product gaps, competitive threat response |
| Acquisition offer received | Legal Advisor, Board, CTO Advisor, Finance | Due diligence, valuation, integration feasibility, cap table analysis |
| Regulatory/legal threat | Legal Advisor, Board, All functional leads | Risk assessment, PR strategy, operational changes, board communication |
| Key hire (VP-level) accepted/rejected | All functional leads, Board | Org chart changes, onboarding plan, backup strategy |

### Escalation Path

```
Board level (existential risk: runway < 3mo, lawsuit, co-founder exit, acquisition offer)
  └── CEO handles directly. No delegation. Board convened within 48 hours.

Executive level (strategic: pivot, fundraising, major customer loss)
  └── CEO + relevant C-level (CTO, CFO, CRO). Decision within 1 week. Board informed.

Functional level (tactical: org change, process issue, vendor decision)
  └── Functional lead handles. CEO informed via weekly sync. No escalation needed.
```

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Fix |
|-------------|---------------|-----|
| **Raising too much too early** | High valuation = high expectations. $50M Series A with $500K ARR → impossible to grow into valuation. Down round risk. | Raise 18-24 months runway. Let valuation follow traction. |
| **Equal founder split (50/50)** | Ignores contribution asymmetry. Gridlock when founders disagree. | Use dynamic split: vesting over 4 years with cliff. Weight by contribution (idea, capital, time, network). |
| **Hiring executives too early** | VP Sales at 5 people doesn't sell — there's nothing to sell. VP Engineering at 3 engineers micromanages. | Functional leads until 15+ people. First exec hire at 25-30 people. |
| **Over-hiring before PMF** | Burn rate increases geometrically. Runway halves every 3 months at 20-person team. | Stay under 10 people until you have PMF. Outsource non-core. |
| **Board of 5 with no independent** | Founders outnumbered by investors = loss of control in tough decisions. | Board of 3: 2 founders, 1 investor. Add independent at Series A. |

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: You are the CEO, CFO, and COO. Fundraising = friends & family or bootstrapping. Org design = just you + maybe a co-founder. Board = informal advisory chats.
- **What to skip**: Venture capital entirely. Cap table software. Formal board meetings. 409A valuations. Org charts.
- **Coordination**: None needed. Talk to customers directly.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Pre-seed/Seed fundraising begins. Simple cap table on Carta/Pulley. Board of 3 (2 founders + 1 lead investor). First hires — generalists who wear multiple hats. 409A for option pricing.
- **What to skip**: Series A prep. Independent board members. Executive hires (stay functional leads). Complex option structures.
- **Coordination**: Weekly all-hands (30 min). Monthly board updates (1-pager). Bi-weekly 1:1s with each report.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Series A/B fundraising ($5M-$30M). Independent board member. First exec hires (VP Eng at 25+, VP Sales at 30+). Department structure emerges. Employee option pool at 15-20%. Performance review cycles.
- **What to skip**: Series C prep at <$10M ARR. Multi-class share structures. Full C-suite (CFO/COO can wait).
- **Coordination**: Quarterly board meetings with full deck. Monthly leadership offsite. Bi-weekly department leads sync.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Series C+ ($30M+). Professional board (5-7 members, majority independent). Full C-suite. Audit committee. Compensation committee. SOX readiness at IPO path. Multi-class shares for founder control. Secondary sales for employee liquidity.
- **What's full production**: Quarterly board with formal packages. Annual shareholder meeting. 409A every 12 months. D&O insurance. Investor relations function.
- **Coordination**: Formal board calendar. Quarterly earnings-style updates. Annual strategy offsite.

### Transition Triggers
- **Solo → Small**: You have paying customers and cannot build + sell + support alone anymore. Revenue > $50K ARR.
- **Small → Medium**: You're hiring specialists (not just generalists). Burn rate requires institutional capital. Revenue > $2M ARR.
- **Medium → Enterprise**: Board demands independent governance. IPO/liquidity event within 24 months. Revenue > $20M ARR.

## Production Checklist

- [ ] Cap table modeled with dilution at each round (use Carta/Pulley)
- [ ] 18-24 month runway modeled with hiring plan and burn rate
- [ ] Board composition planned with independent director identified
- [ ] Employee option pool sized correctly for hiring plan
- [ ] Fundraising materials: pitch deck, financial model, data room
- [ ] Investor pipeline: 30+ target investors per round
- [ ] Org chart designed for next 2 phases (MVP → Growth → Scale)
- [ ] Key person risk mitigated: no single employee is irreplaceable
- [ ] Founder agreement signed: vesting, IP assignment, decision rights
- [ ] 409A valuation completed for option pricing

## References

- Related: `cto-advisor`, `business-strategist`, `product-manager`
- Books: Venture Deals (Feld & Mendelson), The Hard Thing About Hard Things (Horowitz), High Growth Handbook (Gil)
