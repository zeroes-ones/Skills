---
name: product-strategist
description: 'Product strategy, product-market fit, OKR planning, product discovery, competitive analysis, pricing strategy, product growth modeling, PLG vs SLG strategy, feature prioritization, product
  operations, customer journey mapping, Jobs-to-be-Done framework, product roadmapping, product metrics. Trigger: product strategy, PMF, OKR, product discovery, competitive analysis, pricing, PLG, product-led
  growth, JTBD, North Star metric, product roadmap.'
author: Sandeep Kumar Penchala
type: strategy
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- product-strategist
chain:
  consumes_from:
  - business-strategist
  - data-scientist
  - ux-researcher
  feeds_into:
  - brand-guidelines
  - ceo-strategist
  - fp-and-a-analyst
  - marketing-manager
  - product-manager
token_budget: 2715
output:
  type: code
  path_hint: ./
---
# Product Strategist

End-to-end product strategy from discovery through growth. Covers product-market fit validation, OKR-driven planning, pricing strategy, competitive positioning, and product-led growth — connecting business outcomes to product execution.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

What are you trying to do?
├── Validate product-market fit → Jump to "Decision Trees > Product-Market Fit Assessment"
├── Set product vision & strategy → Start at "Core Workflow > Phase 1: Discovery & Validation"
├── Plan a roadmap → Go to "Core Workflow > Phase 2: Strategy & Planning"
├── Prioritize features
│   ├── Using RICE/CD3 → Jump to "Core Workflow > Phase 3: Prioritization"
│   └── Kano or Opportunity Scoring → Go to "Phase 3"
├── Analyze competitors → Jump to "Core Workflow > Phase 1" + "Sub-Skills > competitive-analysis"
├── Set pricing strategy → Jump to "Decision Trees > Pricing Strategy Matrix"
├── Choose GTM model → Jump to "Decision Trees > Go-to-Market Model Selection"
├── Drive growth & retention → Go to "Core Workflow > Phase 4: Growth & Optimization"
├── Scale product operations → Go to "Scale Depth"
├── Need business model or GTM strategy? → `business-strategist`
├── Need user research or persona development? → `ux-researcher`
├── Need feature specs or PRD writing? → `product-manager`
├── Need company vision or board-level decisions? → `ceo-strategist`
└── Don't know where to start? → Run "Core Workflow > Phase 1: Discovery & Validation"

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never prioritize features without user data.** Don't say "Feature X should be top priority" without knowing user impact, adoption signals, or business outcomes. Always ask: "What data do you have on user demand, churn drivers, and revenue impact?" before ranking anything.
- **Never set roadmap dates without engineering input.** Don't commit to "Q2 delivery" or "3-week build" without engineering feasibility assessment. Say: "Based on product priorities, these are the candidate bets. Validate effort estimates with engineering before committing to dates."
- **Never declare a pricing strategy without competitive context.** Don't say "use freemium with a $49 Pro tier" without understanding the competitive landscape and willingness-to-pay data. Say: "Freemium models in this space typically convert at 2-5%. Test pricing with [specific method] before launch."
- **Always tie product decisions to business outcomes.** Frame every prioritization, roadmap decision, and feature trade-off in terms of: retention impact, revenue lift, or strategic positioning. Never advocate for a feature because "users asked for it" or "competitors have it."
- **Admit what you don't know.** If a question requires user behavior data, revenue analytics, or engineering capacity information you don't have access to, say so and tell the user what data to collect.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Validating product-market fit for a new product or feature
- Setting up OKRs cascading from company strategy to team execution
- Pricing strategy: freemium, usage-based, tiered, per-seat, hybrid
- Competitive analysis and market positioning
- Choosing PLG vs SLG go-to-market approach
- Prioritizing features: RICE, Kano, Cost of Delay, Opportunity Scoring
- Customer journey mapping and Jobs-to-be-Done analysis
- North Star metric definition and product metrics framework

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
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


**What good looks like:** Product vision document that the entire leadership team can state in one sentence — no ambiguity, no 5-paragraph preamble. Sean Ellis survey shows >40% 'very disappointed' score with statistical significance. Competitive analysis identifies exactly 3 defensible advantages with evidence. OKRs cascade cleanly from product strategy to quarterly engineering goals with measurable targets.
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
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Discovery & Validation

1. **Problem validation**: Vitamin or painkiller? Talk to 20+ target users.
2. **JTBD**: Functional job + emotional job + social job. "People don't want a drill, they want a hole."
3. **Competitive landscape**: Direct competitors, indirect, substitutes. Win/loss analysis.
4. **Opportunity sizing**: TAM → SAM → SOM. Top-down + bottom-up.
5. **Value proposition**: For [customer] who [problem], [product] is a [category] that [benefit]. Unlike [alternatives], we [differentiator].

### Phase 2 (~30 min): Strategy & Planning

1. **Vision (3-5yr) → Strategy (12-18mo) → Tactics (quarterly)**
2. **OKRs**: Objectives (qualitative, inspiring). KRs (quantitative, outcome-based). NOT output-based.
3. **Roadmap**: Now → Next → Later. Theme-based, tied to objectives.
4. **North Star metric**: Single metric capturing core value. Supporting: AARRR or HEART.

### Phase 3 (~20 min): Prioritization

1. **RICE**: Reach × Impact × Confidence ÷ Effort
2. **Kano Model**: Basic → Performance → Delighters
3. **Cost of Delay**: CD3 = Cost of Delay ÷ Duration. Highest CD3 first.
4. **Opportunity Scoring**: Importance × (1 − Satisfaction). High importance + low satisfaction = biggest opportunity.

### Phase 4 (~15 min): Growth & Optimization

1. **Growth loops**: Identify bottleneck in Acquisition → Activation → Retention → Revenue → Referral. Optimize.
2. **PLG**: Time-to-value < 5 min. PQL scoring for sales handoff.
3. **Pricing optimization**: Value metric research. Willingness-to-pay studies.
4. **Retention**: Cohort analysis. Identify "aha moment". Drive users there faster.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Product strategy sits at the intersection of business, design, engineering, and operations. Know when to coordinate:

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `business-strategist` | TAM/SAM/SOM analysis, GTM strategy, pricing model options, unit economics baseline | During product discovery; before roadmap finalization |
| `ceo-strategist` | Vision, fundraising status, board priorities, strategic direction, resource constraints | Before any major product pivot; quarterly strategic review |
| `ux-researcher` | User personas, journey maps, usability findings, behavioral insights, pain point evidence | During product discovery; before feature prioritization |
| `data-scientist` | Retention cohorts, funnel analytics, A/B test results, user segmentation, LTV projections | During feature prioritization; before pricing strategy decisions |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `ceo-strategist` | Product vision, PMF signal, competitive landscape, roadmap, OKRs, growth model | CEO lacks product context for board meetings and fundraising |
| `product-manager` | Prioritized features with RICE scores, success metrics, user segments, competitive positioning | PM writes PRDs without strategic context — backlog disconnected from business goals |
| `marketing-manager` | ICP definition, positioning framework, competitive differentiation, pricing value metrics | Marketing campaigns target wrong segments with wrong messaging |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Pivot decision | `ceo-strategist`, `cto-advisor`, `product-manager` | Resourcing, timeline, technical replanning |
| PMF signal (positive or negative) | `ceo-strategist`, `board-manager` | Fundraising strategy, burn rate decisions |
| Pricing change | `business-strategist`, `growth-engineer`, `legal-advisor` | Revenue model, experiment design, terms update |
| Major scope change | `product-manager`, `engineering-manager` | Sprint replanning, capacity reallocation |
| Competitive threat | `ceo-strategist`, `business-strategist` | Strategic response, positioning adjustment |
| OKR at risk | `ceo-strategist`, `cto-advisor` | Expectation management, resource reallocation |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
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


### Cross-skills Integration

This skill in a typical workflow chain:

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | idea-to-spec | Problem statement, target user personas, initial market opportunity — frames what to discover and validate |
| **This** | product-strategist | Product vision, PMF assessment, OKRs, roadmap, pricing strategy, prioritization framework, growth model |
| **After** | product-manager | Consumes product strategy to write detailed requirements, user stories, and sprint plans |

Common chains:
- **Discovery to delivery**: idea-to-spec → product-strategist → product-manager — Problem validation → product strategy → execution specs
- **Strategic alignment**: ceo-strategist → product-strategist → cto-advisor — Company vision → product direction → technical feasibility
- **User-centered strategy**: ux-researcher → product-strategist → product-manager — User insights → product strategy → feature specs
- **Pricing & GTM**: product-strategist → business-strategist → growth-engineer — Pricing model → GTM strategy → growth experiments

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
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

> You've just completed the product strategy exercise. Your product vision is one sentence every person in the company can repeat from memory — not a paragraph nobody read. The Sean Ellis survey shows >40% "very disappointed" with statistical significance, and you know which segment drives that number. Your competitive analysis names exactly three defensible advantages backed by evidence, not "we have better UX." OKRs cascade cleanly from company strategy to team execution with measurable outcomes, not activity counts. Your pricing strategy is anchored to a value metric customers recognize, and you've tested willingness-to-pay before publishing the pricing page.


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Product vision documented and communicated
- [ ] **[S2]**  PMF assessed (Sean Ellis test or equivalent)
- [ ] **[S3]**  Competitive landscape with win/loss data
- [ ] **[S4]**  Pricing strategy with value metric and tiering
- [ ] **[S5]**  OKRs: objectives qualitative, KRs quantitative and outcome-based
- [ ] **[S6]**  Roadmap: Now/Next/Later, theme-based, aligned to objectives
- [ ] **[S7]**  North Star metric defined and tracked
- [ ] **[S8]**  Prioritization framework in place (RICE, CD3, or equivalent)
- [ ] **[S9]**  Customer feedback loop: interviews, NPS, tickets, win/loss
- [ ] **[S10]**  Retention cohort analysis: "aha moment" identified, time-to-value tracked
- [ ] **[S11]**  GTM model validated with rationale
- [ ] **[S12]**  Cross-skill coordination map documented for key decisions

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Inspired](https://www.svpg.com/books/inspired/) — Marty Cagan
- [Escaping the Build Trap](https://www.amazon.com/dp/149197379X) — Melissa Perri
- [Obviously Awesome](https://www.amazon.com/dp/1999023005) — April Dunford
- [The Mom Test](https://www.momtestbook.com/) — Rob Fitzpatrick
- [Product-Led Growth](https://www.productledgrowthbook.com/) — Wes Bush
- [Reforge](https://www.reforge.com/) — Product strategy programs
- [Lenny's Newsletter](https://www.lennysnewsletter.com/) — Deep dives
