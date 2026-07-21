---
name: product-strategist
description: Product strategy, product-market fit, OKR planning, product discovery, competitive analysis, pricing strategy, product growth modeling, PLG vs SLG strategy, feature prioritization, product operations, customer journey mapping, Jobs-to-be-Done framework, product roadmapping, product metrics. Trigger: product strategy, PMF, OKR, product discovery, competitive analysis, pricing, PLG, product-led growth, JTBD, North Star metric, product roadmap.
author: Sandeep Kumar Penchala
---

# Product Strategist

End-to-end product strategy from discovery through growth. Covers product-market fit validation, OKR-driven planning, pricing strategy, competitive positioning, and product-led growth — connecting business outcomes to product execution.

## When to Use

- Validating product-market fit for a new product or feature
- Setting up OKRs cascading from company strategy to team execution
- Pricing strategy: freemium, usage-based, tiered, per-seat, hybrid
- Competitive analysis and market positioning
- Choosing PLG vs SLG go-to-market approach
- Prioritizing features: RICE, Kano, Cost of Delay, Opportunity Scoring
- Customer journey mapping and Jobs-to-be-Done analysis
- North Star metric definition and product metrics framework

## Decision Trees

### Product-Market Fit Assessment

```
Retention: 40%+ "very disappointed" without product? (Sean Ellis test)
├── YES → Organic growth > 50% of signups?
│   ├── YES → Revenue pulling from customers?
│   │   ├── YES → PMF confirmed. Scale.
│   │   └── NO → PMF weak. Pricing/value mismatch.
│   └── NO → Emerging PMF. Double down on delighted segment.
└── NO → No PMF. Interview users. Pivot or iterate.
```

### Go-to-Market Model Selection

```
Average deal size (ACV)?
├── < $500 → PLG: self-serve, free tier, viral loops
├── $500-$5K → PLG + Sales hybrid: PQL → sales assist
├── $5K-$50K → SLG with product assist: demo-driven
└── > $50K → Enterprise sales: high-touch, MSA, procurement
```

### Pricing Strategy Matrix

| Model | Best For | Conversion | Examples |
|-------|----------|------------|----------|
| Freemium | B2C, PLG tools | 2-5% | Spotify, Notion, Figma |
| Usage-based | API, infra, AI | Variable | AWS, Twilio, OpenAI |
| Per-seat | B2B SaaS, collab | Predictable | Slack, Jira, GitHub |
| Tiered | SMB-Enterprise | Segmented | HubSpot, Intercom |
| Hybrid | Complex products | Maximized | Datadog, Snowflake |

## Core Workflow

### Phase 1: Discovery & Validation

1. **Problem validation**: Vitamin or painkiller? Talk to 20+ target users.
2. **JTBD**: Functional job + emotional job + social job. "People don't want a drill, they want a hole."
3. **Competitive landscape**: Direct competitors, indirect, substitutes. Win/loss analysis.
4. **Opportunity sizing**: TAM → SAM → SOM. Top-down + bottom-up.
5. **Value proposition**: For [customer] who [problem], [product] is a [category] that [benefit]. Unlike [alternatives], we [differentiator].

### Phase 2: Strategy & Planning

1. **Vision (3-5yr) → Strategy (12-18mo) → Tactics (quarterly)**
2. **OKRs**: Objectives (qualitative, inspiring). KRs (quantitative, outcome-based). NOT output-based.
3. **Roadmap**: Now → Next → Later. Theme-based, tied to objectives.
4. **North Star metric**: Single metric capturing core value. Supporting: AARRR or HEART.

### Phase 3: Prioritization

1. **RICE**: Reach × Impact × Confidence ÷ Effort
2. **Kano Model**: Basic → Performance → Delighters
3. **Cost of Delay**: CD3 = Cost of Delay ÷ Duration. Highest CD3 first.
4. **Opportunity Scoring**: Importance × (1 − Satisfaction). High importance + low satisfaction = biggest opportunity.

### Phase 4: Growth & Optimization

1. **Growth loops**: Identify bottleneck in Acquisition → Activation → Retention → Revenue → Referral. Optimize.
2. **PLG**: Time-to-value < 5 min. PQL scoring for sales handoff.
3. **Pricing optimization**: Value metric research. Willingness-to-pay studies.
4. **Retention**: Cohort analysis. Identify "aha moment". Drive users there faster.

## Cross-Skill Coordination

Product strategy sits at the intersection of business, design, engineering, and operations. Know when to coordinate:

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **CEO Strategist** | Fundraising, pivot decisions, org changes | Product roadmap implications, resource needs, revenue projections |
| **CTO Advisor** | Build vs buy, tech debt vs features | Technical feasibility, engineering capacity, architecture constraints |
| **Business Strategist** | Market entry, pricing, GTM | TAM/SAM/SOM, unit economics, channel strategy |
| **UX Researcher** | Discovery, usability testing | Problem hypotheses, user segments, research questions |
| **UI/UX Designer** | Feature design, prototypes | User stories, acceptance criteria, design constraints |
| **System Architect** | Scalability planning, new services | Growth projections, traffic estimates, data volume forecasts |
| **Frontend/Backend Dev** | Feature estimation, trade-offs | Prioritized backlog, acceptance criteria, technical constraints |
| **QA Engineer** | Acceptance criteria, test planning | User scenarios, edge cases, expected behavior |
| **Growth Engineer** | Experimentation, A/B tests | Hypothesis design, success metrics, experiment scope |
| **Legal Advisor** | Terms, privacy, compliance | Data collection purposes, consent requirements, regulatory constraints |
| **Security Reviewer** | Data handling, auth flows | PII classification, access patterns, threat surfaces from new features |
| **Project Manager** | Roadmap, capacity, dependencies | Priorities, timeline estimates, cross-team dependencies |
| **Data/Analytics** | Metrics, tracking, dashboards | What to measure, event taxonomy, reporting needs |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Pivot decision | CEO Strategist, CTO Advisor, Project Manager | Resourcing, timeline, technical replanning |
| PMF signal (positive or negative) | CEO Strategist, Board | Fundraising strategy, burn rate decisions |
| Pricing change | Business Strategist, Growth Engineer, Legal | Revenue model, experiment design, terms update |
| Major scope change | Project Manager, Engineering leads | Sprint replanning, capacity reallocation |
| Competitive threat | CEO Strategist, Business Strategist | Strategic response, positioning adjustment |
| OKR at risk | CEO Strategist, CTO Advisor | Expectation management, resource reallocation |

## Best Practices

- **Outcomes over output**: Ship features that move metrics, not just roadmap items.
- **Say no strategically**: Frame as trade-off: "If we build A, we delay B by 3 months."
- **PMF is a spectrum**: Segment analysis. PMF for one segment ≠ PMF for all.
- **Pricing = product**: Pricing communicates value. Test early, iterate.
- **Listen, don't obey**: Users describe problems. PMs design solutions.
- **Data-informed, not data-driven**: Data tells what, not why. Combine quant + qual.

## MVP vs Growth vs Scale

| Concern | MVP (Pre-PMF) | Growth (Post-PMF) | Scale (Market Leader) |
|---------|--------------|-------------------|----------------------|
| Discovery | 20+ user interviews | NPS, surveys, analytics | Behavioral data + predictive |
| Roadmap | 1 quarter, themes | 3 quarters, themes | 4-6 quarters, OKR cascade |
| Pricing | 2 tiers (Free+Pro) | 3-4 tiers + enterprise | Multi-product, bundling |
| Metrics | Retention + Sean Ellis | North Star + AARRR | LTV/CAC + expansion MRR |
| Prioritization | Intuition + requests | RICE + Cost of Delay | CD3 + portfolio optimization |
| GTM | Founder-led + self-serve | PLG + light sales | Multi-channel |
| Team | PM + designer + 2-3 eng | PM per squad (5-8 eng) | Group PM + PMs per line |
| Coordination | Daily founder sync | Weekly cross-functional | Monthly steering + quarterly board |

## When NOT to Product Manage

```
Pre-PMF with < 5 users? → Founder IS the PM. No dedicated PM needed.
Solo developer building for yourself? → Dogfooding IS product management.
< 10 engineers + strong PMF? → Engineer as rotating product owner.
Agency building for clients? → Client = PM. You execute.
```

## Sub-Skills

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `product-discovery` | New product, pivot | Phase 1 |
| `okr-planning` | Quarterly planning | Phase 2 |
| `competitive-analysis` | Market entry, repositioning | Phase 1 |
| `pricing-strategy` | Monetization change | Decision Matrix |
| `plg-strategy` | B2B SaaS, self-serve | Phase 4 + GTM Tree |
| `roadmap-planning` | Stakeholder alignment | Phase 2 |
| `feature-prioritization` | Backlog management | Phase 3 |
| `customer-journey` | Onboarding, retention | Phase 4 |

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Product strategy = your gut + 5 customer conversations. Roadmap = a prioritized TODO list. "PMF" = people are paying and not churning. No OKRs, no North Star metric, no prioritization framework.
- **What to skip**: Formal OKRs. RICE/CD3 scoring. Win/loss analysis. NPS surveys. Retention cohort analysis.
- **Coordination**: You are product + engineering + design. Talk to customers weekly.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Product vision written down. Simple roadmap (Now/Next/Later). North Star metric identified. Basic OKRs (1-2 objectives per quarter). Customer feedback loop (interviews + NPS). PMF assessed with Sean Ellis test. Prioritization = value vs effort matrix.
- **What to skip**: Full RICE/CD3 (value vs effort is enough). Competitive win/loss program. Formal product ops. Product council.
- **Coordination**: Weekly product sync with engineering lead. Monthly roadmap review. Quarterly OKR planning. Customer interview debriefs.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Product vision + strategy doc. Theme-based roadmap with outcomes. Structured OKRs (company → team). RICE or CD3 prioritization. Win/loss analysis program. NPS + CSAT + retention cohorts. Dedicated PM per product area. Product ops function emerges. Beta program management.
- **What to skip**: Product portfolio management (unless multi-product). Formal product council (peer review is enough). Full-time product ops (shared with eng ops).
- **Coordination**: Bi-weekly product review. Monthly roadmap review with stakeholders. Quarterly OKR review. Product council monthly.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multi-product portfolio strategy. Product line management with P&L ownership. Full product ops function. Product council with formal gates. Advanced analytics (product-qualified leads, expansion revenue). Competitive intelligence team. Pricing science. Product-led growth team. M&A product integration playbook.
- **What's full production**: Annual product strategy cycle. Quarterly business review (QBR). Product portfolio review monthly. Product council bi-weekly. Win/loss continuous. Beta → GA lifecycle management.
- **Coordination**: QBR with exec team. Monthly product portfolio review. Bi-weekly product council. Weekly PLG metrics review.

### Transition Triggers
- **Solo → Small**: You need dedicated PM because you can't talk to customers + write specs + manage eng. >500 users.
- **Small → Medium**: Single PM can't cover all product areas. Need specialization. >10K users or second product line.
- **Medium → Enterprise**: Multiple product lines with P&L. IPO or acquisition requires formal product governance. >100K users.

## Production Checklist

- [ ] Product vision documented and communicated
- [ ] PMF assessed (Sean Ellis test or equivalent)
- [ ] Competitive landscape with win/loss data
- [ ] Pricing strategy with value metric and tiering
- [ ] OKRs: objectives qualitative, KRs quantitative and outcome-based
- [ ] Roadmap: Now/Next/Later, theme-based, aligned to objectives
- [ ] North Star metric defined and tracked
- [ ] Prioritization framework in place (RICE, CD3, or equivalent)
- [ ] Customer feedback loop: interviews, NPS, tickets, win/loss
- [ ] Retention cohort analysis: "aha moment" identified, time-to-value tracked
- [ ] GTM model validated with rationale
- [ ] Cross-skill coordination map documented for key decisions

## References

- [Inspired](https://www.svpg.com/books/inspired/) — Marty Cagan
- [Escaping the Build Trap](https://www.amazon.com/dp/149197379X) — Melissa Perri
- [Obviously Awesome](https://www.amazon.com/dp/1999023005) — April Dunford
- [The Mom Test](https://www.momtestbook.com/) — Rob Fitzpatrick
- [Product-Led Growth](https://www.productledgrowthbook.com/) — Wes Bush
- [Reforge](https://www.reforge.com/) — Product strategy programs
- [Lenny's Newsletter](https://www.lennysnewsletter.com/) — Deep dives
