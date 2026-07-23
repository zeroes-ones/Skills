---
name: business-strategist
description: >
  Use when designing business models, creating go-to-market plans, modeling financial
  projections, evaluating pricing strategies, or planning market expansion. Handles
  TAM/SAM/SOM analysis, unit economics, competitive positioning, business model canvas,
  revenue modeling, and growth planning. Do NOT use for financial accounting, payroll
  setup, or tax compliance.
license: MIT
tags:
- strategy
- business-model
- gotomarket
- financial-modeling
- pricing
- growth
- competitive-analysis
author: Sandeep Kumar Penchala
type: strategy
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  consumes_from: []
  feeds_into:
  - bizdev-manager
  - ceo-strategist
  - marketing-manager
  - product-strategist
---

# Business Strategist
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Design and validate business models, craft go-to-market strategies, build financial models, and plan sustainable growth. Think like a COO/CFO/Head of Strategy combined.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*", "business.model\|revenue.model\|unit.economic\|pricing.strategy\|GTM\|go.to.market")` AND `file_contains("*", "TAM\|SAM\|SOM\|market.size\|LTV\|CAC")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*", "fundraising\|Series.[A-C]\|pitch.deck\|cap.table\|investor\|venture.capital")` AND `file_contains("*", "runway\|burn.rate\|valuation")` | Jump to **Decision Trees** — Fundraising Readiness. |
| A3 | `file_contains("*", "competitive.landscape\|competitor.analysis\|Porter\|five.forces\|SWOT")` AND `file_exists("*.{csv,xlsx}")` | Jump to **Core Workflow** — Phase 1: Market Analysis + Competitive Landscape. |
| A4 | `file_contains("*", "financial.model\|P&L\|revenue.forecast\|cash.flow\|burn")` AND `file_exists("*.{xlsx,csv}")` | Jump to **Core Workflow** — Phase 3: Financial Projections. |
| A5 | `file_contains("*", "vision\|mission\|company.purpose\|founding.story")` AND `file_contains("*", "fundraise\|board\|equity\|cap.table")` | Invoke **ceo-strategist** instead. This is company-defining, not business model design. |
| A6 | `file_contains("*", "product.market.fit\|PMF\|retention\|churn\|user.feedback\|Sean.Ellis")` | Invoke **product-strategist** instead. This is product strategy territory. |
| A7 | `file_contains("*", "build.vs.buy\|tech.stack\|architecture\|engineering.team\|CTO")` | Invoke **cto-advisor** instead. This is technology strategy work. |
| A8 | `file_contains("*", "financial.statement\|balance.sheet\|GAAP\|IFRS\|tax\|audit")` | Invoke **accountant** or **fp-and-a-analyst** instead. This is financial operations, not strategy. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Design a business model → Jump to "Decision Trees > Pricing Model Selection"
├── Plan a go-to-market launch
│   ├── Choosing channels → Jump to "Decision Trees > GTM Channel Strategy"
│   ├── Market entry → Go to "Decision Trees > Market Entry Decision"
│   └── Budget allocation → Jump to "GTM Cost by Channel (B2B SaaS)"
├── Build financial projections
│   ├── Revenue model & unit economics → Go to "Core Workflow > Phase 3"
│   └── Fundraising prep → Jump to "Decision Trees > Fundraising Readiness"
├── Set pricing strategy → Start at "Decision Trees > Pricing Model Selection"
├── Plan growth & market expansion
│   ├── Scaling up → Go to "Scale Depth"
│   └── Channel/partnership strategy → Jump to "Key Frameworks"
├── Need company vision or fundraising strategy? → `ceo-strategist`
├── Need product-market fit or competitive analysis? → `product-strategist`
├── Need technology strategy or architecture governance? → `cto-advisor`
└── Don't know where to start? → Run "Core Workflow > Phase 1: Business Model Design"
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to fabricate market sizing numbers.** Do not offer a TAM/SAM/SOM estimate without either user-provided data or a cited industry source (Gartner, IDC, Statista). You are not a market research database. | Trigger: response would contain a dollar figure for TAM/SAM/SOM AND `grep -rn "Gartner\|IDC\|Statista\|Forrester\|IBISWorld\|CB Insights" . --include="*.md"` returns 0 results in the conversation context | STOP. Respond: "I cannot fabricate market size numbers. Provide your TAM/SAM/SOM data from customer discovery, or cite a specific industry report (Gartner, IDC, Statista) that I can reference. Without data, I can show you the *methodology* for calculating TAM but not the number itself." |
| **R2** | **REFUSE to present competitor claims as verified facts.** Revenue, market share, and growth rates for private companies are unverifiable. All competitor assertions must be qualified. | Trigger: response would contain "[Competitor Name] has [X]% market share" or "[Competitor Name] revenue is $[Y]" without a citation qualifier like "estimates suggest" or "public filings indicate" | STOP. Insert qualifier: change all bare competitor claims to "Industry estimates suggest [Competitor Name] may have..." or "Public filings indicate [Competitor Name] reported..." |
| **R3** | **REFUSE to project financials without stated assumptions.** Every revenue forecast, burn rate calc, or runway estimate must explicitly list assumptions BEFORE the numbers appear. | Trigger: generated content contains a dollar-denominated projection (`$[0-9]`, `[0-9]% CAGR`, `[0-9] months runway`) without a preceding "Assuming [growth rate], [pricing], [churn], and [CAC]" clause within 3 paragraphs | STOP. Prepend: "**Assumptions:** [list all]. Based on these assumptions, the model projects:" before any numeric output. If the user hasn't provided inputs, ASK for them first. |
| **R4** | **REFUSE to recommend a business model without a validation mechanism.** Every business model recommendation must include a concrete, falsifiable test. | Trigger: response recommends a business model (freemium, usage-based, marketplace, etc.) without specifying "Test this by [specific method] within [timeframe]" | STOP. Append: "Validate this model: [specific test method, e.g., 'offer 10 target customers the proposed pricing and measure willingness-to-pay'], within [specific timeframe, e.g., '2 weeks']. If [falsification condition], pivot to [alternative]." |
| **R5** | **STOP and ASK if key context for financial projections is missing.** Do not assume: average contract value, churn rate, CAC, conversion rates, or sales cycle length. | Trigger: generating financial projections that reference ACV, churn, CAC, conversion, or sales cycle without those values being supplied by the user in the current conversation | STOP. Ask targeted questions: "What's your average contract value? What's your monthly churn rate? What's your customer acquisition cost? What's your sales cycle length?" Do not proceed with placeholder numbers. |
| **R6** | **DETECT and WARN about revenue concentration risk.** If user describes a customer portfolio where any single customer exceeds 20% of revenue and the strategy doesn't address diversification. | Trigger: user-provided data shows `Max(customer_revenue) / Total(revenue) > 0.20` AND no mention of "diversification" or "concentration risk mitigation" in the current response draft | WARN: Add: "⚠️ Revenue concentration risk: customer [X] represents [Y]% of revenue. Investors typically discount concentrated revenue by 30-50%. Document: renewal date, relationship owner, churn risk assessment, and diversification timeline. Target: no single customer >15% of revenue within 12 months." |
| **R7** | **DETECT and WARN about single-channel GTM risk.** If the GTM strategy relies on exactly one channel with no diversification plan. | Trigger: GTM strategy mentions exactly 1 channel (e.g., "paid search only" or "content marketing only") AND no mention of channel testing or diversification timeline | WARN: Add: "⚠️ Single-channel risk: your entire GTM relies on [channel]. Channel economics can shift overnight (ad price changes, platform algorithm updates). Recommendation: allocate 20% of GTM budget to testing a second channel within 90 days. The winning channel today becomes the losing channel tomorrow without your permission." |

## The Expert's Mindset

Business strategy is not about filling out canvases — it's about **finding the intersection of what customers want, what you can deliver uniquely, and what generates sustainable profit**. The canvas is a tool for thinking; the thinking is what matters.

### Mental Models

| Model | Description |
|---|---|
| **Business model = how you create, deliver, and capture value** | Create value (product), deliver value (distribution), capture value (pricing). If any of the three is broken, the business fails. Most founders over-invest in creation and under-invest in distribution. |
| **Unit economics are the atomic unit of strategy** | If you lose money on every transaction, volume doesn't fix it. LTV > 3× CAC is table stakes, not an aspiration. Know your numbers to the decimal point. |
| **Every business model has a fatal assumption** | The one thing that, if wrong, kills the company. Identify it, name it explicitly, and test it first. Everything else is a distraction. |
| **Markets, not products, determine outcomes** | A great product in a shrinking market fails. A mediocre product in a growing market has a chance. Size the market before designing the product. |

### Cognitive Biases in Business Strategy

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Optimism bias** | Revenue projections that go "up and to the right" with no failure scenario | Always model 3 cases: base, upside, downside. The downside case should feel uncomfortable. |
| **Survivorship bias** | Studying unicorns and ignoring the graveyard of similar companies that failed | For every successful company you reference, find 2 that failed with a similar model. Understand why. |
| **False consensus** | Assuming customers think like you do | Test willingness-to-pay with real customers. Your opinion doesn't count — you're not the customer. |
| **Sunk cost in strategy** | Sticking with a failing GTM because you've already invested in it | Set explicit kill criteria before launching any strategy. When triggered, pivot without guilt. |

### What Masters Know That Others Don't

- **The best strategies fit in a paragraph, not a deck.** If you need 40 slides to explain your business, you don't understand it yet. Amazon's strategy: "Low prices, vast selection, fast delivery." Done.
- **Distribution strategy is underrated relative to product strategy.** "Build it and they will come" is not a strategy — it's a prayer. The best business strategists spend as much time on GTM as on product.
- **Pricing is the most powerful, least-used lever.** A 1% price increase can drive 10%+ profit improvement in most businesses. Most companies set prices once and never revisit them strategically.
- **The fatal assumption is usually about customer behavior, not technology.** Most business failures are market failures, not product failures. "We thought they'd pay for it" is the most expensive sentence in business.

## Operating at Different Levels

Business strategy scales from a single product line to corporate strategy. The time horizon and scope of decisions defines the level.

| Level | Business Strategy Output Characteristics |
|---|---|
| **L1 — Apprentice** | Analyzes a single business model. Learns strategy frameworks (Porter, Christensen, Blue Ocean). |
| **L2 — Practitioner** | Owns GTM strategy for a product. Builds business cases, pricing models, and financial forecasts independently. |
| **L3 — Senior** | Owns business strategy for a business unit. Market entry/expansion analysis. "These are the three markets we enter next." |
| **L4 — VP Strategy** | Defines corporate strategy across business units. M&A strategy, portfolio management. "This is the 5-year company strategy." |
| **L5 — Chief Strategy Officer** | Shapes industry-level strategy. Creates frameworks for strategic decision-making adopted across companies. |

**Usage**: Say "as an L3 business strategist, evaluate the market entry for..." Default: **L2** (product-level business strategy).

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

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->
Business strategy lives or dies on cross-functional alignment. A brilliant GTM strategy fails if product can't ship, sales can't sell, and finance can't fund.

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `ceo-strategist` | Strategic vision, fundraising status, board priorities, resource constraints | Before any market entry decision; quarterly strategic review |
| `product-strategist` | TAM/SAM/SOM analysis, competitive landscape, PMF signal, pricing hypotheses | During business model design; before GTM strategy finalization |
| `legal-advisor` | Regulatory constraints, IP strategy, partnership agreement risks, compliance obligations | Before international expansion; during partnership negotiation |
| `fp-and-a-analyst` | Unit economics baseline, revenue projections, cost structure analysis, scenario models | During financial modeling; before fundraising preparation |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `ceo-strategist` | Business model canvas, GTM strategy, pricing model, unit economics, financial projections | CEO makes fundraising decisions without financial context — wrong round size or timing |
| `product-strategist` | Market segmentation, competitive intelligence, channel economics, willingness-to-pay data | Product bets are uninformed by market reality — roadmap misses target |
| `marketing-manager` | ICP definition, positioning inputs, channel strategy, demand gen economics | Marketing campaigns target wrong segments — wasted ad spend |
| `growth-engineer` | Business hypotheses, success metrics, guardrail metrics, experiment scope | A/B tests optimize vanity metrics rather than business outcomes |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| New market entry decision | `ceo-strategist`, `product-strategist`, `marketing-manager`, `legal-advisor` | Cross-functional launch planning, localization requirements, hiring plan |
| Pricing model change | `ceo-strategist`, `product-strategist`, `fp-and-a-analyst`, `legal-advisor` | Revenue impact modeling, customer communication, contract updates |
| Competitive threat (new entrant with >20% feature parity) | `ceo-strategist`, `product-strategist`, `marketing-manager` | Competitive response, positioning adjustment, product roadmap reprioritization |
| Fundraising preparation begins | `ceo-strategist`, `fp-and-a-analyst`, `legal-advisor`, `product-strategist` | Data room prep, financial modeling, due diligence readiness |
| Major partnership (>$500K ACV potential) | `ceo-strategist`, `legal-advisor`, `product-strategist` | Integration requirements, resource allocation, deal structure |
| Business model pivot | `ceo-strategist`, `product-strategist`, `fp-and-a-analyst` | Org impact, financial replanning, product strategy realignment |
| Unit economics turn negative at scale | `ceo-strategist`, `fp-and-a-analyst`, `product-strategist` | Root cause analysis, pricing review, cost structure optimization |

### Escalation Path

```
Existential business risk (losing >30% revenue, regulatory shutdown, market collapse)
  └── `ceo-strategist` + `legal-advisor` + `fp-and-a-analyst`. Emergency board meeting if public/funded.

Strategic business decision (market entry, business model change, major pricing)
  └── `business-strategist` + `ceo-strategist` + `product-strategist` + `fp-and-a-analyst`. Decision within 2 weeks. Board informed.

Tactical business decision (segment targeting, campaign optimization, channel mix)
  └── Functional lead handles. `business-strategist` consulted. No escalation needed.
```

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| No TAM/SAM/SOM analysis done — business case relies on "the market is huge" without quantification | Propose market sizing: bottom-up TAM/SAM/SOM with documented assumptions. For fundraising: TAM is the story, SOM is the target. Investors discount top-down ("1% of $100B market") by 70-90%. Bottom-up ("X customers × Y ACV = $Z") survives due diligence | "The market is huge" is not a strategy — it's a platitude. Without TAM/SAM/SOM, you cannot prioritize segments, allocate GTM resources, or convince investors. Bottom-up sizing forces you to name real customers and real budgets |
| Business model unclear — pricing, distribution, and revenue mechanics are undefined or contradictory | Run Business Model Canvas exercise: 9 blocks (value proposition, customer segments, channels, customer relationships, revenue streams, key resources, key activities, key partners, cost structure). If any block says "TBD," the business model is a hypothesis, not a plan | An undefined business model produces undefined results. The Business Model Canvas forces coherence — if your revenue model is subscription but your customer relationship is "self-service," one of those is wrong. Surface contradictions before they surface in your bank account |
| No competitive moat identified — "better UX" or "first mover advantage" cited as the only differentiator | Flag immediately: "Better UX" is not a moat — it's a baseline expectation. Document switching costs (what happens when a customer tries to leave?), network effects (does each new user make the product more valuable?), and data advantages (what data do you have that competitors don't?). If none of these exist, you don't have a business — you have a feature | Companies without moats get competed to zero. If a well-funded competitor can replicate your product in 6 months, your only moat is execution speed — and speed is not a business strategy, it's a sprint |
| Revenue concentration >30% from one customer — existential risk not flagged | Diversify before fundraising. No single customer should represent >15% of revenue. If >30%, document the customer relationship, contract renewal date, and churn risk. Investors discount concentrated revenue by 30-50% — a $10M ARR business with 40% concentration trades at $6M valuation | Revenue concentration is the silent killer of SaaS valuations. One customer leaving = bankruptcy risk. Diversification is not a growth tactic — it's survival infrastructure. Diversify before you need to, not when you have to |
| Financial model uses top-down projections: "1% of a $10B market = $100M revenue" | Rebuild bottom-up: start with unit assumptions (conversion rates, ASP, churn, CAC). Model 3 scenarios (best/base/worst). Document every assumption explicitly. Top-down models die in the first 5 minutes of investor due diligence | Top-down models are PowerPoint math — they impress until someone asks "how?" Bottom-up models survive scrutiny because every number traces back to a customer conversation or market benchmark. Investors can argue with your TAM; they can't argue with your unit economics |
| Pricing strategy set once and never revisited — no A/B testing, no willingness-to-pay research, no competitive pricing intelligence | Establish pricing review cadence: test with 10 customers at launch, iterate quarterly. Use Van Westendorp or Gabor-Granger for willingness-to-pay. Monitor competitive pricing monthly. Pricing is a process, not a decision — the right price today is wrong in 12 months | Pricing is the highest-leverage growth lever. A 1% price improvement drops straight to the bottom line — it's equivalent to a 10% increase in sales volume for most businesses. Companies that "set and forget" pricing leave millions on the table |
| No coordination with `product-manager` for market validation — business strategy and product roadmap are disconnected | Schedule joint review: does the business model assume features the product team hasn't prioritized? Does the product roadmap build things the business model doesn't monetize? Align product strategy with revenue model quarterly | Business strategy and product strategy are two sides of the same coin. A business model that assumes enterprise sales while the product is built for self-serve PLG is a contradiction that wastes engineering capacity and marketing budget |
| Fundraising materials prepared without `fp-and-a-analyst` review — model has circular references or unrealistic assumptions | Coordinate model review: every assumption must have a source (customer interview, benchmark, industry report). Line items must reconcile. Run sensitivity analysis: which assumptions, if they move 20%, change the outcome? Raise when the model is defensible, not when it's pretty | Investor due diligence finds every weak assumption. A model that breaks under 20% sensitivity analysis will break in the first partner meeting. Defensibility is not about being right — it's about knowing exactly where you might be wrong and having a plan for both cases |

## What Good Looks Like

> Your financial model has three defensible scenarios with documented assumptions, not wishful projections. Your TAM/SAM/SOM analysis is grounded in bottom-up data that an investor would trust.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.


## Deliberate Practice

The best business strategists treat strategy as a craft, not a meeting. Deliberate practice means regularly producing strategic artifacts, getting feedback from the market, and refining your mental models.

```mermaid
graph LR
    A[Study a business case] --> B[Apply framework to a real scenario]
    B --> C[Get market feedback or data]
    C --> D[Refine your model and assumptions]
    D --> A
```

| Level | Practice Routine | Frequency |
|---|---|---|
| **Novice** | Analyze a public company's business model and write a one-page critique | Weekly |
| **Competent** | Build a financial model for a hypothetical product launch | Monthly |
| **Expert** | Lead a strategy review for a real business unit, present to executives | Quarterly |
| **Master** | Write a strategy memo that becomes the organization's north star | Biannually |

**The One Highest-Leverage Activity**: Write a one-paragraph business strategy for a real or hypothetical company every week. If the strategy doesn't fit in a paragraph, you haven't understood it yet. Share with a peer and ask: "What's wrong with this?"

## Gotchas

- **Porter's Five Forces** analysis that's a one-time exercise — you do it in January, file it away, and the market shifts in March (new entrant, supplier consolidation, substitute product launch). The analysis is stale before it reaches the board. Five Forces must be a quarterly living document, not an annual ritual.
- **"First mover advantage"** as universal truth — Google was the 18th search engine. Facebook was the 4th social network. Apple wasn't the first MP3 player, smartphone, or tablet. First movers pay the education cost; fast followers pay the execution cost. The winner is determined by execution quality, not chronological order.
- **Pricing strategy based on "competitor price minus X%"** — you anchor to their value proposition, not yours. If your product delivers 3x the value (measured in revenue lift, time saved, or risk reduction), you should charge MORE, not less. Cost-plus and competitor-minus pricing both ignore the only thing that matters: value delivered.
- **Market sizing that conflates TAM and SAM** — your Total Addressable Market is "every company with employees" ($100B). Your Serviceable Addressable Market is "US companies with 50-500 employees using cloud software" ($5B). Investors see through TAM inflation instantly, and it damages credibility for the rest of your pitch.


## Verification

- [ ] Market analysis: Porter's Five Forces reviewed within last quarter, changes documented
- [ ] Competitive intelligence: top 5 competitors tracked quarterly — funding, product launches, pricing changes, leadership moves
- [ ] TAM/SAM/SOM: bottom-up sizing with documented assumptions, updated annually or after market shifts
- [ ] Strategic bets: each bet has hypothesis, investment, success criteria, and kill date (when to stop if not working)
- [ ] Pricing: pricing strategy reviewed within last 6 months — value-based, not competitor-minus


## References
- **Financial Modeling Best Practices**: See [financial-modeling-best-practices.md](references/financial-modeling-best-practices.md)
- **GTM Cost by Channel (B2B SaaS)**: See [gtm-cost-by-channel-b2b-saas.md](references/gtm-cost-by-channel-b2b-saas.md)
- **Key Frameworks**: See [key-frameworks.md](references/key-frameworks.md)
- **Market Sizing Shortcuts**: See [market-sizing-shortcuts.md](references/market-sizing-shortcuts.md)
- **Unit Economics by Business Model**: See [unit-economics-by-business-model.md](references/unit-economics-by-business-model.md)
