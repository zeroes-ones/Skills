---
name: business-strategist
description: Business model design, go-to-market strategy, financial modeling, pricing strategy, and growth planning. Use when designing business models, creating go-to-market plans, modeling financials, evaluating pricing, or planning market expansion.
author: Sandeep Kumar Penchala
type: strategy
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - business-strategist
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
---
# Business Strategist

Design and validate business models, craft go-to-market strategies, build financial models, and plan sustainable growth. Think like a COO/CFO/Head of Strategy combined.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

What are you trying to do?
├── Design a business model → Jump to "Decision Trees > Pricing Model Selection"
├── Plan a go-to-market launch
│   ├── Choosing channels → Jump to "Decision Trees > GTM Channel Strategy"
│   └── Market entry → Go to "Decision Trees > Market Entry Decision"
├── Build financial projections
│   ├── Revenue model & unit economics → Go to "Core Workflow > Phase 3"
│   └── Fundraising prep → Jump to "Decision Trees > Fundraising Readiness"
├── Set pricing strategy → Start at "Decision Trees > Pricing Model Selection"
├── Plan growth & market expansion
│   ├── Scaling up → Go to "Scale Depth"
│   └── Channel/partnership strategy → Jump to "Key Frameworks"
└── Don't know where to start? → Run "Core Workflow > Phase 1: Business Model Design"

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never invent market sizing numbers.** If actual TAM/SAM/SOM data isn't provided, use "industry estimates suggest" with a source and a range. Do NOT say "your TAM is $4.2B" — you don't know their specific market segment or geography.
- **Never present competitor claims as verified facts.** Competitor revenue, market share, or growth rates are estimates unless cited from public filings. Say "public reports estimate..." or "Crunchbase data suggests..." — never "Competitor X has 32% market share."
- **Never project financials without stating assumptions.** Every revenue forecast, burn rate calc, or runway estimate must be prefixed with: "Assuming [growth rate], [pricing], and [retention], the model shows..." If the user doesn't provide these inputs, ask for them.
- **Always recommend validation against primary data.** Every business model or GTM recommendation should include: "Test this against [specific data source]" — e.g., "Test pricing willingness-to-pay with 10 target customers before finalizing."
- **Admit what you don't know.** If a question requires current market conditions, real-time competitor pricing, or regulatory/compliance details that change frequently, say so and tell the user where to find it.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Business model canvas design and validation
- Go-to-market strategy and launch planning
- Financial modeling: revenue forecasting, unit economics, runway
- Pricing strategy: tiered, usage-based, freemium, enterprise
- Market expansion and internationalization planning
- Partnership and channel strategy
- Cost optimization and operational efficiency
- Fundraising preparation and investor materials

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Pricing Model Selection
```
                     ┌──────────────────────────┐
                     │ START: New pricing model? │
                     └────────────┬─────────────┘
                                  │
               ┌──────────────────▼──────────────────┐
               │ Is your product self-serve or       │
               │ sales-assisted?                     │
               └────┬─────────────────────┬──────────┘
                    │ Self-serve         │ Sales-assisted
          ┌─────────▼─────────┐  ┌───────▼──────────┐
          │ Does value scale   │  │ ACV > $10K?      │
          │ with usage?        │  └──┬──────────┬────┘
          └──┬──────────┬──────┘     │ YES       │ NO
             │ YES      │ NO         ▼           ▼
             ▼          ▼        ┌────────┐ ┌──────────┐
        ┌─────────┐ ┌────────┐  │Per-seat │ │Tiered     │
        │Usage-   │ │Tiered/ │  │+        │ │flat with  │
        │based    │ │Freemium│  │platform │ │add-ons    │
        └─────────┘ └────────┘  │fee      │ └──────────┘
                                └────────┘
```
**When to choose Usage-based:** Product value directly correlates with API calls, data processed, or compute consumed. CAC payback < 12 months at median usage.  
**When to choose Tiered/Flat:** Predictable value delivery per customer. Buyers need budget predictability. Implementation cost is similar regardless of usage volume.

### GTM Channel Strategy
```
                     ┌────────────────────────┐
                     │ START: Which GTM motion?│
                     └───────────┬────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ What is your ACV?                   │
              └────┬──────────┬──────────┬──────────┘
                   │ <$500    │ $500-10K │ >$10K
                   ▼          ▼          ▼
            ┌──────────┐ ┌──────────┐ ┌──────────────┐
            │ PLG +    │ │ Sales-   │ │ Enterprise    │
            │ Content  │ │ Assisted │ │ Sales +       │
            │ Marketing│ │ + Content│ │ Outbound SDR  │
            └──────────┘ └──────────┘ └──────────────┘
```
**When to choose PLG/Content:** Self-serve onboarding exists. Product demonstrates value in < 15 minutes. CAC target < $200.  
**When to choose Enterprise Sales:** Requires procurement, security review, or executive approval. Implementation takes > 2 weeks. ACV justifies > $1K CAC.

### Market Entry Decision
```
                     ┌──────────────────────────┐
                     │ START: Enter new market?  │
                     └───────────┬──────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Is existing market saturated        │
              │ (growth < 15% YoY)?                 │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌────────────────────┐
        │ Adjacent market  │  │ Deepen penetration │
        │ expansion        │  │ in current market   │
        └──────────────────┘  └────────────────────┘
```
**When to expand:** Current market share > 30% OR TAM in adjacent market > 2x current. Can repurpose > 60% of existing tech/sales motion.  
**When to deepen:** Current market share < 15%. CAC is trending down. Unit economics improving with scale.

### Fundraising Readiness
```
                     ┌──────────────────────────┐
                     │ START: Time to fundraise? │
                     └───────────┬──────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Revenue growing > 15% MoM           │
              │ for 3+ consecutive months?          │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ Fundraise now.   │  │ Extend runway. Fix   │
        │ LTV/CAC > 3x?    │  │ growth engine first. │
        │ Gross margin>70%?│  │ Revisit in 6 months. │
        └──────────────────┘  └──────────────────────┘
```
**When to fundraise:** > 6 months runway remaining. Clear use of funds tied to milestones. Strong founder-market fit narrative.  
**When to wait:** < 4 months runway (emergency mode — bridge round). Growth is flat. Missing key hires needed to deploy capital effectively.


### Cross-skills Integration

This skill in a typical workflow chain:

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | idea-to-spec | Validated problem statement, target market hypothesis, initial TAM estimate |
| **This** | business-strategist | Business model canvas, GTM plan, pricing strategy, financial model, unit economics |
| **After** | product-manager | Consumes GTM strategy and pricing model to build feature requirements and launch plan |

Common chains:
- **New venture**: idea-to-spec → business-strategist → product-manager — Problem validation → business model → execution plan
- **Fundraising prep**: business-strategist → ceo-strategist — Financial model + GTM → investor narrative + pitch deck
- **Growth planning**: business-strategist → growth-engineer — Unit economics + channel strategy → growth experiments + A/B tests
- **Pricing overhaul**: product-strategist → business-strategist → financial-modeling — Pricing hypothesis → pricing strategy + tiering → revenue projections

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
When this skill is invoked, drill into these specialized areas as needed:

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `business-model-design` | New product, pivot, new market entry | This file — Business Model Canvas workflow |
| `unit-economics` | Fundraising, pricing, profitability analysis | This file — Unit Economics by Business Model |
| `gtm-strategy` | Launch, expansion, new vertical | This file — GTM Cost by Channel |
| `market-sizing` | Fundraising, new market entry | This file — Market Sizing Shortcuts |
| `pricing-strategy` | Launch, enterprise tier, international | This file — Pricing Models section |
| `partnership-strategy` | Channel sales, integrations, platform plays | `references/` (create as needed) |

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Business Model Design
1. Complete Business Model Canvas: value prop, customer segments, channels, revenue streams, key resources, key activities, key partners, cost structure
2. Identify riskiest assumptions and design experiments to validate
3. Model unit economics: CAC, LTV, gross margin, payback period
4. Size the market: TAM, SAM, SOM with bottom-up validation
5. Map competitive positioning on key dimensions

### Phase 2 (~30 min): Go-to-Market Strategy
1. Define target customer profile and ideal customer profile (ICP)
2. Design customer acquisition funnel with conversion targets
3. Select distribution channels with rationale
4. Create pricing and packaging strategy
5. Build sales motion: self-serve, sales-assisted, PLG, enterprise

### Phase 3 (~20 min): Financial Planning
1. Build 3-year financial model: revenue, costs, headcount, cash
2. Model scenarios: base, optimistic, pessimistic
3. Define key metrics and milestones for each phase
4. Calculate funding requirements and dilution impact
5. Create board/investor reporting package

## Key Frameworks

**Business Model Canvas** — 9 building blocks for business model design.

**Pirate Metrics (AARRR)** — Acquisition, Activation, Retention, Revenue, Referral.

**Three Horizons** — Horizon 1 (core), Horizon 2 (emerging), Horizon 3 (future).

**Blue Ocean Strategy Canvas** — Visualize competitive factors and differentiation.

**Pricing Models**: Cost-plus, value-based, competitive, freemium, usage-based, tiered.

## Unit Economics by Business Model

| Business Model | CAC Range | LTV Expectation | LTV/CAC Target | Gross Margin |
|---------------|-----------|----------------|----------------|-------------|
| **B2B SaaS (SMB)** | $200-500 | $2K-10K | >3x | 70-85% |
| **B2B SaaS (Enterprise)** | $5K-50K | $50K-500K | >4x | 70-85% |
| **B2C Subscription** | $5-50 | $100-500 | >3x | 60-80% |
| **Marketplace** | $10-100 (per side) | $500-5K | >4x | 40-60% |
| **E-commerce** | $20-80 | $200-1K | >3x | 30-50% |
| **PLG / Freemium** | $1-10 (free user) | $200-2K (converted) | >5x | 80-90% |

**Red flags:** LTV/CAC < 1.5 = dying. CAC payback > 18 months = cash flow problem.

## GTM Cost by Channel (B2B SaaS)

| Channel | CAC | Time to First Customer | Best For |
|---------|-----|----------------------|----------|
| **Content/SEO** | $50-200 | 6-12 months | Long-term, PLG, SMB |
| **Paid search (Google/LinkedIn)** | $300-1K | 1-4 weeks | Immediate pipeline |
| **Outbound sales (SDR)** | $500-2K | 2-8 weeks | Enterprise, ACV > $10K |
| **Partnerships** | $100-500 | 3-9 months | Ecosystem plays |
| **Community** | $20-100 | 6-18 months | Developer tools, niche |
| **Events/Conferences** | $1K-5K | 1-4 weeks | Enterprise, brand building |

**Channel mix by stage:** MVP = founder-led sales + content. Growth = paid + outbound + partnerships. Scale = all channels with attribution.

## Market Sizing Shortcuts

```
TAM (Total Addressable Market) = Number of potential customers × Annual contract value
SAM (Serviceable Addressable Market) = TAM × geographic/segment filter (usually 10-30%)
SOM (Serviceable Obtainable Market) = SAM × realistic market share Year 3 (usually 1-5%)

Quick TAM checks:
- B2B SaaS: # companies in target segment × average software spend/category
- Consumer: # users × ARPU benchmark for category
- Marketplace: GMV of comparable incumbents × 10% disruption target

Red flag: If your SOM < $20M, VC path is dead. Bootstrap or lifestyle.
Healthy: SOM > $100M with clear path to $1B TAM.
```


**What good looks like:** Business model canvas with 10+ customer interviews validating each assumption — you know which bets are confirmed and which are still risky. Unit economics show LTV/CAC > 3 at scale with a clear path to get there. Beachhead segment identified where you can own 30%+ of a $20M+ TAM within 18 months. The strategy document is 3 pages, not 30.
## Financial Modeling Best Practices

- Bottom-up > top-down: build from unit assumptions, not market percentages
- Always model 3 scenarios: base, optimistic, pessimistic
- Separate fixed vs. variable costs
- Include headcount plan with fully-loaded cost
- Model cash runway, not just P&L
- Document all assumptions explicitly

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Business strategy lives or dies on cross-functional alignment. A brilliant GTM strategy fails if product can't ship, sales can't sell, and finance can't fund.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **CEO Strategist** | Fundraising, pivot, market entry, major pricing changes | Strategic options with financial implications, risk/reward scenarios, resource requirements |
| **Product Strategist** | Product-market fit assessment, pricing, competitive positioning | Market data, competitive intelligence, customer segmentation, willingness-to-pay research |
| **Legal Advisor** | Terms of service, partnership agreements, international expansion, regulatory strategy | Business model requirements, risk tolerance, deal structure preferences |
| **Finance / CFO** | Financial modeling, fundraising, budget allocation, unit economics | Revenue projections, cost structure, market assumptions, sensitivity ranges |
| **Growth Engineer** | Experimentation roadmap, PLG funnel, A/B testing | Business hypotheses to test, success metrics, guardrail metrics |
| **Sales / CRO** | GTM strategy, territory design, pricing, sales compensation | ICP definition, competitive win/loss data, customer objections, channel economics |
| **Marketing Lead** | Positioning, messaging, demand gen, brand strategy | Market research, segmentation, competitive landscape, channel performance |
| **Data/Analytics** | Market analysis, customer segmentation, LTV modeling, forecasting | Business questions, data requirements, analysis priorities |
| **Partnerships / BD** | Channel partnerships, platform integrations, strategic alliances | Partnership economics, integration requirements, co-marketing strategy |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| New market entry decision | CEO, Product, Marketing, Sales, Legal, Finance | Cross-functional launch planning, localization requirements, hiring plan |
| Pricing model change | CEO, Product, Sales, Finance, Legal | Revenue impact modeling, customer communication, contract updates |
| Competitive threat (new entrant with >20% feature parity) | CEO, Product, Marketing, Sales | Competitive response, positioning adjustment, product roadmap reprioritization |
| Fundraising preparation begins | CEO, Finance, Legal, Product | Data room prep, financial modeling, due diligence readiness |
| Major partnership (>$500K ACV potential) | CEO, Legal, Product, Engineering | Integration requirements, resource allocation, deal structure |
| Business model pivot | CEO, Product, Finance, All functional leads | Org impact, financial replanning, product strategy realignment |
| Unit economics turn negative at scale | CEO, Finance, Product, Sales | Root cause analysis, pricing review, cost structure optimization |

### Escalation Path

```
Existential business risk (losing >30% revenue, regulatory shutdown, market collapse)
  └── CEO + Business Strategist + Legal + Finance. Emergency board meeting if public/funded.

Strategic business decision (market entry, business model change, major pricing)
  └── Business Strategist + CEO + Product + Finance. Decision within 2 weeks. Board informed.

Tactical business decision (segment targeting, campaign optimization, channel mix)
  └── Functional lead handles. Business Strategist consulted. No escalation needed.
```

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
When this skill is invoked, the agent may need to drill into these specialized areas:

| Sub-Skill | When to Use |
|-----------|-------------|
| `business-model-design` | Designing or pivoting business models: SaaS, marketplace, subscription, transactional, freemium |
| `unit-economics` | Fundraising readiness, pricing analysis, and profitability modeling with CAC, LTV, and payback period |
| `gtm-strategy` | Launch, expansion, or new vertical entry: PLG vs sales-led vs channel vs community-led |
| `market-sizing` | Fundraising or new market entry: TAM/SAM/SOM methodology, bottom-up vs top-down analysis |
| `pricing-strategy` | Launch pricing, enterprise tiers, or international expansion: usage-based, per-seat, hybrid, freemium |
| `partnership-strategy` | Channel sales, integrations, platform plays: technical vs go-to-market vs strategic partnerships |

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Business model = Lean Canvas on a napkin. GTM = you doing sales, marketing, and support. Pricing = guess based on competitors. Market sizing = "big enough to matter." Financial model = revenue minus costs in a spreadsheet.
- **What to skip**: Formal TAM/SAM/SOM analysis. Multi-channel GTM strategy. Pricing consultants. Detailed financial models. Competitive intelligence tools.
- **Coordination**: Talk to 10 customers. That's your entire strategy process.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Business model canvas formalized. TAM/SAM/SOM estimated (bottom-up). Single GTM channel (usually PLG or founder-led sales). Simple pricing tiers (2-3). Unit economics tracked (LTV/CAC). 12-month financial model.
- **What to skip**: Multi-channel GTM (pick one and nail it). Pricing optimization (just test with customers). Formal competitive intelligence. 5-year financial projections.
- **Coordination**: Monthly strategy review with CEO. Weekly metrics review. Quarterly pricing review.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Business model stress-tested with data. Full TAM/SAM/SOM with bottom-up validation. 2-3 GTM channels with attribution. Pricing optimization with A/B testing. Regular competitive analysis. 3-year financial model with scenarios. Customer segmentation and ICP refinement.
- **What to skip**: TAM analysis for adjacent markets. International pricing. Channel partnerships program (unless proven). Dedicated strategy team.
- **Coordination**: Quarterly strategy offsite. Monthly GTM review. Bi-weekly pricing committee. Customer advisory board annually.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multi-product business model. Full market intelligence function. Omnichannel GTM with attribution. Dynamic pricing (usage-based, geography, segment). M&A strategy integration. Scenario planning with Monte Carlo. Investor-grade financial models. Dedicated strategy & ops team.
- **What's full production**: Annual strategic planning cycle. Quarterly board strategy review. Continuous competitive intelligence. Pricing science team. Market expansion playbooks. Strategic finance function.
- **Coordination**: Annual strategy cycle (Q3 planning, Q4 budget, Q1 kickoff). Quarterly board deck. Monthly business review (MBR). Weekly GTM standup.

### Transition Triggers
- **Solo → Small**: You have revenue and need specialists (marketing, sales). >$50K ARR.
- **Small → Medium**: Single-channel GTM saturates. Need second channel. Revenue >$2M ARR.
- **Medium → Enterprise**: Multi-product or multi-geography expansion. IPO preparation. Revenue >$20M ARR.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
1. **Model bottom-up, not top-down:** Build financial projections from unit assumptions (conversion rates, ASP, churn) — not by taking 1% of a billion-dollar market. Top-down models die in due diligence.
2. **TAM is a story, SOM is your target:** Investors care about TAM for narrative. Your GTM plan lives and dies on SOM — a realistic, bottom-up calculation of what you can capture in Year 1–3.
3. **LTV/CAC > 3 is table stakes, payback < 12 months is gold:** A business with 5x LTV/CAC but 24-month payback runs out of cash. Optimize for payback period, not just ratio.
4. **Pricing is a process, not a decision:** Launch with a hypothesis, test with 10 customers, iterate quarterly. The right price today is wrong in 12 months. Build pricing review into your operating cadence.
5. **One GTM channel at a time:** Founders try content + paid + outbound + partnerships simultaneously. Pick the channel with highest LTV/CAC at your stage. Saturate it before adding a second.
6. **Competitive moat = switching cost + network effects + data advantages:** "Better UX" is not a moat. Document why customers can't leave, why each new user makes the product more valuable, and what data you have that competitors don't.
7. **Revenue concentration > 30% from one customer = existential risk:** Diversify before fundraising. No single customer should represent more than 15% of revenue. Investors discount concentrated revenue by 30–50%.
8. **Fundraise when you have momentum, not when you need money:** The best time to raise is when you have 3+ months of 15%+ MoM growth, not when you have 3 months of runway. Desperation is visible and expensive.
9. **Document assumptions, review them monthly:** Every model has assumptions. Write them down explicitly. Review monthly — which assumptions held, which didn't, and what changed. This is how you build forecasting accuracy.
10. **Strategy without execution tracking is fiction:** Every strategic initiative needs an owner, a deadline, and a dashboard metric. Review weekly. A beautiful strategy document that nobody executes is worse than no strategy at all.


### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Market timing wrong | Product launched too early (no demand) or too late (crowded) | Run demand validation with 10+ paid pre-orders before building; use Wardley Map to time your entry |
| Team can't execute | Key hires missing, wrong incentives, no clear owner | Hire for the next 6 months' problems, not the last 6 months'; DRI model with written OKRs |
| Runway < 12 months | Burn rate exceeds plan, revenue slower than projected | Cut burn to 18-month runway immediately; model best/worst/realistic case scenarios |
| Investor pass | Pitch doesn't articulate defensible moat | Lead with TAM → problem → traction → team → ask. Your demo is not your pitch. |
| Board misalignment | Founder/board disagree on strategy | Pre-board one-on-ones before every board meeting. Surface disagreement in the room, not after. |
| Scaling prematurely | Growing team/features before PMF | Sean Ellis test: < 40% "very disappointed" if product disappeared → do not scale |
| Co-founder conflict | Roles, equity, or vision disagreement | Written founder agreement with vesting, roles, decision rights, and exit terms |


## What Good Looks Like

> You've just completed the business strategy exercise. Your financial model has three defensible scenarios with documented assumptions, not wishful projections. Your TAM/SAM/SOM analysis is grounded in bottom-up data that an investor would trust. The unit economics show LTV/CAC > 3 with a clear path to that ratio from day one. Your GTM plan names specific channels, budgets, and conversion targets — not "social media and word of mouth." Your pricing has been tested with real customers who said "that feels fair" rather than "I'd need to think about it." Every number in your model traces back to a customer conversation or market benchmark.


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Business model validated with customer discovery
- [ ] **[S2]**  Unit economics positive at scale (LTV/CAC > 3)
- [ ] **[S3]**  Go-to-market plan with channel strategy and budget
- [ ] **[S4]**  Financial model with 3 scenarios and documented assumptions
- [ ] **[S5]**  Pricing tested with target customers
- [ ] **[S6]**  Competitive landscape mapped and monitored
- [ ] **[S7]**  Key metrics dashboard defined
- [ ] **[S8]**  Fundraising materials ready (pitch deck, data room, model)
- [ ] **[S9]**  Risk register with mitigation strategies
- [ ] **[S10]**  90-day execution plan with owners and deadlines

## References
<!-- QUICK: 30s -- links to deeper reading -->
- Related: `ceo-strategist`, `product-manager`, `growth-engineer`
- Books: Business Model Generation (Osterwalder), Lean Startup (Ries), Obviously Awesome (Jantsch)
