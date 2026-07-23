---
name: product-strategist
description: >
  Use when defining product strategy, validating product-market fit, planning OKRs,
  conducting competitive analysis, modeling product growth, or designing PLG vs SLG
  motions. Handles product discovery, feature prioritization, Jobs-to-be-Done framework,
  pricing strategy, customer journey mapping, North Star metric definition, and product
  roadmapping. Do NOT use for sprint planning, backlog grooming, or day-to-day
  engineering management.
license: MIT
tags:
- product
- strategy
- pmf
- okr
- pricing
- plt
- competitive-analysis
- jtbd
author: Sandeep Kumar Penchala
type: strategy
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 2715
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
---
# Product Strategist

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end product strategy from discovery through growth. Covers product-market fit validation, OKR-driven planning, pricing strategy, competitive positioning, and product-led growth — connecting business outcomes to product execution.

## Route the Request
<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*", "product.vision\|product.strategy\|North.Star\|strategic.positioning\|competitive.advantage")` AND `file_contains("*", "roadmap\|OKR\|objective\|key.result")` | This is your skill. Jump to **Core Workflow** — Phase 1: Discovery & Validation. |
| A2 | `file_contains("*", "PMF\|product.market.fit\|Sean.Ellis\|retention.cohort\|churn.analysis")` | Jump to **Decision Trees** — Product-Market Fit Assessment. |
| A3 | `file_contains("*", "RICE\|CD3\|prioritization\|feature.priority\|opportunity.scoring\|Kano")` AND `file_contains("*", "roadmap\|backlog\|feature.list")` | Jump to **Core Workflow** — Phase 3: Prioritization. |
| A4 | `file_contains("*", "GTM\|go.to.market\|PLG\|product.led\|sales.led\|channel.strategy")` | Invoke **business-strategist** instead. GTM strategy is business model territory. |
| A5 | `file_contains("*", "persona\|user.research\|journey.map\|usability.test\|user.interview")` | Invoke **ux-researcher** instead. This is user research, not product strategy. |
| A6 | `file_contains("*", "PRD\|product.requirement\|spec\|user.story\|acceptance.criteria")` | Invoke **product-manager** instead. This is feature specification work. |
| A7 | `file_contains("*", "fundraising\|board.deck\|investor.update\|company.vision\|cap.table")` | Invoke **ceo-strategist** instead. This is company-level strategy. |
| A8 | `file_contains("*", "pricing.model\|pricing.strategy\|willingness.to.pay\|Van.Westendorp\|value.based.pricing")` | Jump to **Decision Trees** — Pricing Strategy Matrix. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
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
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else
<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to prioritize features without user data.** Do not rank features without knowing user impact, adoption signals, or business outcome drivers. Feature prioritization based on intuition produces features nobody uses. | Trigger: response ranks features ("Feature X should be top priority" or provides a numbered priority list) AND `conversation_context` does not contain user demand data (survey results, support ticket volume, churn analysis, usage analytics) | STOP. Respond: "I cannot prioritize features without user data. Provide: (1) user demand signals (survey data, support ticket frequency, feature request volume), (2) business impact estimates (retention lift, revenue potential, activation improvement), (3) effort estimates from engineering. Without these, prioritization is guesswork." |
| **R2** | **REFUSE to set roadmap dates without engineering feasibility input.** Product strategy sets the "what" and "why"; engineering sets the "how long." Committing to dates without engineering validation is setting the team up to fail. | Trigger: response includes a delivery date or timeline ("Q2 delivery", "3-week build", "shipping by [date]") without referencing engineering effort estimates or capacity planning | STOP. Qualify: "Based on product priorities, these are the candidate bets ordered by impact. Validate effort estimates with engineering before committing to dates. Timeline is an engineering output, not a product input." |
| **R3** | **REFUSE to declare a pricing strategy without competitive context and willingness-to-pay data.** Pricing without market context is arbitrary. Freemium, usage-based, and per-seat models have different economics that only make sense in context. | Trigger: response recommends a specific pricing model ("use freemium", "charge $X/month") without referencing competitive landscape pricing data or willingness-to-pay research | STOP. Qualify: "[Pricing model] typically converts at [range]% in [industry/segment]. Before finalizing: (1) benchmark against 3+ direct competitors, (2) test willingness-to-pay with [specific method, e.g., Van Westendorp survey of 20 target customers], (3) model unit economics at each price point." |
| **R4** | **DETECT and WARN when product decisions are justified by "users asked for it" or "competitors have it" without business impact analysis.** User requests are signals, not requirements. Competitor features are validation of a market, not validation for your product. | Trigger: generated content justifies a feature using "users requested", "customers asked for", or "competitors have" without quantifying the expected business impact (retention lift %, revenue increase $, activation improvement) | WARN. Rewrite: "Users have requested [feature] ([N] tickets, [X]% of support volume). If built, it is expected to impact [metric] by [estimate]%. Before committing, validate with a 1-week discovery: survey [N] users in target segment. If < [threshold]% express urgent need, deprioritize." |
| **R5** | **STOP and ASK when critical product context is missing.** Do not assume: user segmentation, current retention rates, activation metrics, revenue per user, or competitive positioning. Product strategy without these is a wish list. | Trigger: generating product strategy recommendations (vision, roadmap, prioritization, pricing) without explicit user segmentation, retention data, or revenue metrics confirmed in the conversation | STOP. Ask: "What are your user segments and their relative revenue contribution? What's your current monthly retention by segment? What's your activation rate (users reaching 'aha moment')? What's your average revenue per user? Without these, strategy recommendations are untethered from business reality." |
| **R6** | **DETECT and WARN about output-based OKRs masquerading as strategy.** "Ship feature X" is a task, not an objective. OKRs measure outcomes — the business results that features are hypothesized to produce. | Trigger: generated OKRs contain "Ship", "Launch", "Build", "Complete", "Deliver", "Release" as the objective verb, rather than "Increase", "Reduce", "Improve", "Achieve" tied to a measurable metric | WARN. Rewrite each output-based OKR: "Instead of 'Ship onboarding v2' → 'Increase week-4 retention from 40% to 55% (hypothesis: improved onboarding reduces early churn).' The feature is the bet; the metric is the outcome. Measure the outcome, not the feature." |

## The Expert's Mindset

Product strategy is not about picking the right framework — it's about **seeing what others don't see and having the conviction to act on it before the data is conclusive**. The output is not a strategy document; the output is a company aligned around a shared direction that wins.

### Mental Models

| Model | Description |
|---|---|
| **Strategy = what you don't do** | A strategy that doesn't explicitly say what you're *not* pursuing is not a strategy — it's a wish list. The power is in the trade-offs. |
| **Insight > framework** | Frameworks (SWOT, Porter, BCG) structure thinking but don't produce insight. Great strategy comes from a novel observation about the market that others have missed. |
| **Distribution beats product** | In most markets, the best-distributed product wins, not the best product. Your GTM strategy is at least as important as your product strategy. |
| **Speed of iteration > quality of initial strategy** | No strategy survives contact with customers intact. The best strategists iterate faster, not smarter. |

### Cognitive Biases That Kill Strategies

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Planning fallacy** | Underestimating how long everything takes by 2-3x | Use reference-class forecasting: how long did it take 5 similar companies? |
| **Confirmation bias** | Seeking data that supports your strategy, dismissing contradicting evidence | Appoint a "strategy skeptic" role in every review; their job is to find what's wrong |
| **Anchoring** | First number you see (competitor price, market size estimate) shapes all subsequent thinking | Always generate independent estimates before looking at benchmarks |
| **Survivorship bias** | Studying winners and extracting lessons without examining the graveyard of failures | For every successful strategy you admire, study 2 that failed with similar approaches |
| **Sunk cost fallacy** | Continuing a failing strategy because you've already invested in it | Set kill criteria at strategy launch. If triggered, kill regardless of investment. |

### What Masters Know That Others Don't

- **The best strategy fits on one page.** If you need appendices to explain your strategy, you don't have clarity. Jeff Bezos's 1997 shareholder letter was 2 pages and ran Amazon for decades.
- **Strategy is revealed in resource allocation, not documents.** Show me your budget and headcount allocation — that's your real strategy. Everything else is aspiration.
- **Category creation beats category competition.** The highest-return strategies create new categories where you define the rules (Salesforce: "No software"; Tesla: EVs as desirable, not eco-compromises). But category creation is also the riskiest bet — most new categories fail.
- **Timing is the least discussed, most important variable.** Being right too early is indistinguishable from being wrong. Ask: "Why now? What changed that makes this possible today that wasn't possible 2 years ago?"

### When to Break Your Own Rules

- **Skip competitive analysis when creating a new category.** There are no competitors when you're defining the market. But validate that users have an existing behavior you're replacing — even category creators compete with "the way it's done today."
- **Ignore roadmap discipline during existential pivots.** When the company might die, throw out the roadmap and focus all resources on the one thing that might save it. Survival is the strategy.

## Operating at Different Levels

Product strategy scales from individual product lines to company-defining bets. The scope and time horizon of decisions defines the level.

| Level | Product Strategy Output Characteristics |
|---|---|
| **L1 — Apprentice** | Analyzes a market segment. Contributes to competitive analysis. Learns strategy frameworks. |
| **L2 — Practitioner** | Owns product strategy for a feature area. PMF analysis, pricing recommendations, competitive positioning for a product surface. |
| **L3 — Senior** | Owns product strategy for a full product. Portfolio-level OKRs, build-vs-buy-vs-partner analysis. Strategic rationale for market positioning. |
| **L4 — Director/VP** | Owns strategy for a product line or business unit. Multi-year strategic bets. "These are the three markets we're betting on for the next 3 years." |
| **L5 — CPO/CEO** | Defines the company's product philosophy and strategic decision framework. "This is how we choose which markets to enter and how we win in them." |

**Usage**: Say "as an L3 product strategist, evaluate the PMF for..." Default: **L3** (full-product strategy, independent analysis).

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

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| Team says "users are asking for feature X" but nobody has quantified how many users or what job they're trying to accomplish | Intervene: "Feature requests are symptoms, not diagnoses. Run a Jobs-to-be-Done analysis: (1) What job is the user hiring this feature to do? (2) How many users have this job? (3) What do they use today as a workaround? (4) What's the cost of the workaround? If you can't articulate the job, you're building a feature for a vocal minority." | Unvalidated feature requests are the #1 source of feature bloat and wasted engineering capacity. Every feature shipped for a non-existent job consumes maintenance, testing, and cognitive load forever. JTBD separates real demand from loud requests |
| Product roadmap has 20+ items for this quarter but team capacity can only deliver 5 — and the CEO keeps adding more | Flag: "A roadmap without capacity constraints is a wishlist, not a plan. Force-rank: if we can only ship ONE thing this quarter, what creates the most business value? Use RICE scoring (Reach × Impact × Confidence / Effort) with explicit effort estimates from engineering. Any unranked item is a distraction. Present the trade-off: "Adding X means delaying Y by 6 weeks. Which do you choose?"" | Overstuffed roadmaps produce nothing on time. When everything is priority #1, nothing is. The CEO needs to see the trade-off explicitly: adding to the roadmap means removing something of equal size. If they won't choose, default to highest-RICE item and make the rest wait |
| Product discovery consists of "talking to 3 users who are friends of the founders" — no structured research, no segmentation, no competitive analysis | Alert: "Convenience sampling produces false confidence. Run structured discovery: (1) Recruit 15+ users from YOUR target segment (not friends), (2) Observe them using their current solution (not your prototype), (3) Document the moment they "hire" a solution and what triggers the switch. The goal is not to validate your idea — it's to understand their problem deeply enough that the solution becomes obvious" | Friends and early adopters will tell you your product is great because they like you, not because it solves their problem. Structured discovery with strangers reveals the real friction points. Products built on friend-validation fail at scale because real users don't have the same context, patience, or motivation |
| Competitor launched a major new feature — team panics and wants to copy it immediately | Intervene: "Competitive panic is the worst product strategy. Before copying: (1) Is this feature core to THEIR strategy or YOURS? (2) Do YOUR users actually need this? (3) What's the 3-month cost to build vs the opportunity cost of NOT building your roadmap? Run a quick user survey — if <30% of your users care, ignore it. Competitors can validate market demand for you; you don't have to be first to every feature" | Competitive reactivity creates "me-too" products that always lag. The competitor's feature was designed for their user base, their infrastructure, and their business model. Copying without understanding creates a worse version of someone else's strategy. Your roadmap should reflect YOUR users' jobs, not your competitor's |
| Pricing page still has the original 2 tiers from launch (Free/$9.99) after 2 years and 50K users — no enterprise tier, no usage-based option, no annual discount | Flag: "Pricing is product strategy, not a configuration setting. At 50K users, you're leaving 30-50% revenue on the table. Design: (1) 3-tier model with clear value differentiation per tier, (2) Usage-based component for high-volume customers, (3) Annual discount (15-20%) to improve cash flow predictability, (4) Enterprise tier with SSO, SLA, and dedicated support for deals >$10K/year. Test with 10% of new signups first" | Pricing optimization is the highest-ROI product activity. A 10% price increase that loses 2% of customers increases profit by 8%. Products that never revisit pricing leave enormous revenue on the table while competitors capture the high end of the market. Pricing signals value — if you're the cheapest, you're signaling low quality |
| Retention cohort shows 40% of users churn within the first 7 days — team focused on building new features for existing users | Alert: "New user retention is the #1 growth lever. Fix activation before building for retention: (1) Map the time-to-value — what's the minimum steps from signup to "aha moment"? (2) Remove every step between signup and first value, (3) Track activation rate (users who reach aha moment within session 1). A 10% improvement in day-7 retention compounds to 2x more MAU in 12 months. Stop building features until activation rate exceeds 60%" | Acquisition fills a leaky bucket if activation is broken. Every dollar spent on acquisition for a product with 40% week-1 retention is 60% wasted. Fixing activation is the highest-leverage product work — it improves every growth channel simultaneously without spending a dollar on marketing |
| Revenue per customer hasn't grown in 4 quarters but the team attributes it to "market conditions" | Flag: "Revenue stagnation has a root cause. Audit: (1) Is expansion revenue flat because there's nothing to expand to? → add higher-tier features. (2) Is churn offsetting expansion? → fix retention. (3) Are new customers lower-value? → fix ICP targeting. (4) Is pricing below market? → test increases. Market conditions affect everyone equally — if competitors are growing and you're not, it's a product strategy problem, not a market problem" | Blaming market conditions is the product equivalent of "it works on my machine." Revenue stagnation is almost always a product strategy failure: wrong features, wrong pricing, wrong segments, or wrong positioning. The market reveals the truth — listen to it |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Outcomes over output**: Ship features that move metrics, not just roadmap items.
- **Say no strategically**: Frame as trade-off: "If we build A, we delay B by 3 months."
- **PMF is a spectrum**: Segment analysis. PMF for one segment ≠ PMF for all.
- **Pricing = product**: Pricing communicates value. Test early, iterate.
- **Listen, don't obey**: Users describe problems. PMs design solutions.
- **Data-informed, not data-driven**: Data tells what, not why. Combine quant + qual.

## Anti-Patterns
<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Building a feature because "Competitor X has it and they raised $50M" — competitive cargo-culting produces features nobody asked for | Analyze whether the competitor's feature fits YOUR user segments and YOUR business model. Run a 1-week discovery sprint: survey 20 users in your target segment. If <30% express need, it's a distraction. Competitors validate markets, not features for YOUR product | `grep -rn "competitor.*has\|[Competitor].*launched\|because.*competitor" --include="*.md" \| grep -v "counter.example\|don't do this"` → finds competitor-justified feature decisions | PRD template: `templates/prd.md` — requires "User Evidence" section before "Competitive Comparison" |
| The roadmap is a prioritized list of features from the "ideas" Slack channel with no user evidence, no business case, and no success criteria | Every roadmap item needs: (1) the job-to-be-done it addresses, (2) quantitative evidence of demand (survey data, support tickets, churn analysis), (3) success metric that will move (activation rate, retention, revenue), (4) RICE score. If an item can't articulate all 4, it doesn't belong on the roadmap | `grep -rn "roadmap\|feature.list\|prioritized" --include="*.md" -A 5 \| grep -c "RICE\|CD3\|evidence\|data\|metric"` → if roadmap items found AND score/evidence count = 0, roadmap is a wishlist | Roadmap template: `templates/roadmap.md` — requires RICE score + evidence + success metric per item |
| Pricing set at "$9.99/month because that's what everyone charges" — value-based pricing ignored, leaving 40%+ revenue uncaptured | Price based on value delivered, not competitor benchmarks: (1) quantify the economic value your product creates for the customer (time saved × hourly rate, revenue gained), (2) price at 10-25% of that value, (3) test 3 price points with new signups. Products that save companies $10K/month should not cost $99/month | `grep -rn "pricing.*because\|charge.*everyone\|competitor.*price\|market.rate" --include="*.md"` → finds pricing justified by competition rather than value | Pricing review: `scripts/check-pricing-methodology.sh` — flags if pricing lacks value-based justification or willingness-to-pay data |
| PMF declared after "our 10 beta users love it and use it daily" — 10 hand-picked early adopters is not product-market fit | PMF requires: (1) Sean Ellis test: >40% of users would be "very disappointed" if the product disappeared, (2) retention curves flattening (not declining), (3) organic growth starting (word-of-mouth, not paid), (4) at least 100+ users from your target segment (not friends). 10 beta users is a signal, not confirmation | `grep -rn "PMF\|product.market.fit\|we.have.PMF" --include="*.md" \| grep -v "Sean.Ellis\|>40%\|retention"` → finds PMF claims without quantitative evidence thresholds | PMF assessment template: `templates/pmf-assessment.md` — requires Sean Ellis score, retention curve, and organic growth data |
| The product strategy document hasn't been updated in 12 months — still references a competitor that pivoted 6 months ago and a market that shifted | Product strategy is a living document. Review quarterly: (1) Re-evaluate competitive landscape (new entrants, pivots, acquisitions), (2) Re-assess PMF signal by segment, (3) Update pricing based on willingness-to-pay data, (4) Rotate OKRs based on what moved. A stale strategy is worse than no strategy — it gives false confidence | `find . -name "product-strategy*" -mtime +90` → if strategy doc > 90 days old, it's stale | Pre-commit hook: `scripts/check-strategy-freshness.sh` — warns if `product-strategy.md` hasn't been updated in 90 days |
| Discovery interviews conducted as demos: "Here's our product, what do you think?" — leading questions produce false validation | Discovery interviews must be: (1) Problem-focused, not solution-focused — "Tell me about the last time you [had this problem]", (2) Silent for the first 15 min — let them describe their workflow unprompted, (3) Recorded and transcribed — confirmation bias makes you hear what you want. Never show your product during discovery. You're studying their problem, not selling your solution | `grep -rn "what do you think\|do you like\|would you use\|demo.*discovery\|show.*product" --include="*.md" \| grep -i "interview\|discovery\|research"` → finds leading questions in discovery scripts | Discovery guide template: `templates/discovery-interview-guide.md` — enforces problem-first, silent-first protocol |
| OKRs set as "ship feature X, ship feature Y, ship feature Z" — output-based OKRs measure activity, not impact | OKRs must measure outcomes: "Increase week-4 retention from 40% to 55%" not "Ship onboarding v2." The feature is a hypothesis; the metric movement is the result. Output-based OKRs reward busywork. If an OKR can be achieved without moving a business metric, it's not an OKR — it's a task list | `grep -rn "Objective.*ship\|OKR.*launch\|OKR.*build\|Objective.*deliver\|Objective.*release" --include="*.md"` → finds output-verb OKRs masquerading as strategy | OKR template: `templates/okr-template.md` — validates objectives use outcome verbs (Increase/Reduce/Improve) not output verbs (Ship/Build/Launch) |

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


### War Story 1 — The Feature That Shipped to Nobody
**Symptom:** A product team spent 3 quarters building a "collaborative editing" feature for their project management tool. At launch, only 2% of users tried it. After 6 months, adoption was still under 5%. It was eventually deprecated.
**Root cause:** The feature was prioritized based on a single enterprise customer's request and competitive pressure (Notion had it). No user research was done. The actual user need was "know when teammates are viewing the same document" — read-only presence, not real-time editing.
**Fix:** Adopted a "customer problem, not customer request" prioritization rule. Before any feature: run 5 discovery interviews to validate the underlying problem, not the proposed solution. The result: a much smaller "presence indicator" shipped in 3 weeks and hit 80% activation.
**Lesson:** Building what customers ask for is the most expensive way to discover what they actually need. Invest in problem discovery before solution design. A $5K research sprint can save $500K of engineering.

### War Story 2 — The Roadmap Driven by the Loudest Voice
**Symptom:** The VP of Sales brought a "must-have" feature request from a $500K enterprise prospect. The CEO approved it as top priority. The product shipped it in 2 quarters. The prospect went with a competitor anyway. Meanwhile, 3 core features were delayed, and NPS dropped 15 points.
**Root cause:** The roadmap was driven by the highest-value sales opportunity, not data. User feedback from the broader customer base was invisible because there was no systematic feedback collection. The company built for one customer and alienated hundreds.
**Fix:** Implemented RICE scoring with a mandatory step: any feature must reach >10% of the user base to qualify for top priority unless the deal is >20% of ARR. Sales-driven features without broad reach go into a "sponsor-funded" queue.
**Lesson:** The loudest stakeholder is rarely the most representative one. A systematic prioritization framework protects the roadmap from the highest-paid person's opinion.

### War Story 3 — The Pricing Page That Left Millions on the Table
**Symptom:** A B2B SaaS company charged $49/mo for their Pro plan because "that's what competitors charge." The CEO discovered at a board meeting that customers who negotiated custom pricing were paying $200-500/mo. The self-serve pricing was leaving 4x on the table.
**Root cause:** The pricing was set by competitive benchmarking, not willingness-to-pay research. No value metric analysis was done. Customers were willing to pay based on number of seats, not a flat fee.
**Fix:** Moved from per-user flat pricing to usage-based + tiered model: Free ($0), Starter ($29/seat), Business ($99/seat), Enterprise (custom). Tested with 20 customers before launch. ARR increased 300% in 6 months without adding a single new feature.
**Lesson:** Pricing is the most leveraged growth lever. A 10% price increase drops straight to profit. Test pricing changes like product changes — with experiments, cohorts, and statistical significance.


## Error Decoder
<!-- DEEP: 5min -- each entry includes a console-string matcher for automatic recovery loops -->

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `Error: PMF.*declared.*premature\|Sean.Ellis.*< 40%\|retention.*declining` + `grep -rn "PMF\|product.market.fit\|we.have.fit" strategy.md` AND `grep -c "Sean.Ellis\|cohort\|retention.curve" strategy.md` = 0 | "We have PMF!" declared at a board meeting. 3 months later: churn is 12%/month, NPS is 14, and the "viral loop" has 3 participants. The board now questions every product decision because the PMF claim was wrong | PMF was declared based on qualitative signals (enthusiastic beta users, positive feedback) without quantitative thresholds. Confirmation bias: 10 hand-picked users who love the product is not PMF — it's sampling bias. The Sean Ellis test and retention curves are standard precisely because they are hard to game | Set quantitative PMF gates: (1) Sean Ellis test: >40% "very disappointed" if product disappeared, from 100+ users, (2) retention curves flattening at Month 3+ across 3+ cohorts, (3) organic growth > 20% of new signups, (4) NPS > 30 from non-friend/non-family users. Until 3 of 4 gates pass, status is "seeking PMF" | 1. Audit PMF claims: `grep -rn "PMF\|product.market.fit" *.md -B 2 -A 2` 2. For each claim: verify Sean Ellis score, retention curve, organic growth % are documented 3. Run: `scripts/pmf-gate-check.sh` — outputs pass/fail per gate 4. If < 3 gates pass: update status to "seeking PMF" with next assessment date |
| `Error: roadmap.*delivery.*< 30%\|roadmap.*commit.*missed\|features.*shipped.*declining` + `grep -rn "roadmap\|delivery.date\|commitment" *.md \| grep -v "engineering\|effort\|estimate"` shows dates without engineering input | Product promised Q2 delivery of 8 features. Engineering delivered 2 by Q3. Sales sold features that don't exist. Customers are angry. The roadmap says "Q2" but engineering capacity was consumed by tech debt from last quarter's rushed delivery | Roadmap dates were set by product without engineering input. The roadmap became a commitment to sales before engineering could estimate effort. Every missed date erodes trust between product, engineering, and customers. Three missed cycles and the roadmap is fiction | Roadmap must have: Now (committed, estimated), Next (planned, rough estimate), Later (direction, no dates). Never commit "Later" items to dates. "Now" items require engineering sign-off on estimates. Roadmap as outcome-based themes ("Improve onboarding") not feature lists with dates | 1. Audit roadmap: `grep -rn "Q[1-4]\|quarter\|delivery" roadmap.md \| wc -l` → count hard date commitments 2. Compare to engineering estimates: `grep -c "effort\|estimate\|capacity" roadmap.md` 3. If date_count > estimate_count: roadmap dates are not engineering-validated 4. Convert: move "Later" items to theme-based, remove dates from all but "Now" column |
| `Error: competitive.analysis.*stale\|competitor.*pivot.*missed\|landscape.*shifted` + `find . -name "*competitive*" -mtime +90` shows competitive analysis > 90 days old | Board asks "What about [New Competitor]?" — nobody on the product team has heard of them. They launched 8 months ago, raised $15M, and already have 3 of your target accounts. Your competitive analysis still lists companies from 2 years ago | Competitive analysis is treated as a one-time deliverable rather than a continuous process. Markets shift fast — new entrants appear, incumbents pivot, startups get acquired. A 6-month-old competitive analysis is dangerously incomplete; a 12-month-old one is a liability | Implement quarterly competitive review: (1) automated monitoring (Google Alerts, Crunchbase, Twitter/X) for competitor keywords, (2) monthly 30-min competitive sync with sales (they hear about new competitors first), (3) quarterly deep-dive update to positioning and win/loss analysis | 1. Check freshness: `find . -name "*competitive*" -mtime -90` → must return file(s) 2. If none: run `scripts/competitive-scan.sh` — searches Crunchbase, news, job postings for new entrants 3. Sync with sales: survey AEs for "competitors you lost to in the last 30 days that aren't in our analysis" 4. Alert: if competitive analysis > 90 days old, flag for immediate review |
| `Error: pricing.*optimization.*missed\|willingness.to.pay.*never.tested\|value.based.*absent` + `grep -rn "pricing.*set at\|price.*since\|charge.*because\|we.charge" *.md` shows pricing set by historical precedent not value | Competitor raised prices 25% and nobody churned. Their cost structure is the same as yours. You're still at the price you launched with 3 years ago, leaving 30-40% of potential revenue on the table because "we don't want to upset customers" | Pricing is treated as fixed rather than a continuous optimization variable. Without willingness-to-pay testing (Van Westendorp, Gabor-Granger, conjoint), pricing is set by fear ("what if they leave?") rather than data ("what is this actually worth?"). Every year at the wrong price is unrecoverable revenue | Run willingness-to-pay study: (1) Van Westendorp survey with 20+ target customers, (2) identify optimal price point and price indifference range, (3) test new price with 10% of new signups for 30 days, (4) monitor conversion rate and churn at new price. If conversion drops < 10% AND churn unchanged, roll out to 100% | 1. Check: `grep -rn "Van.Westendorp\|Gabor.Granger\|conjoint\|willingness.to.pay" *.md` → must find methodology + results 2. If none: deploy survey (`templates/wtp-survey.md`) to 20+ target customers 3. Calculate value-based price: `scripts/value-based-pricing.sh` — outputs price range from value delivered 4. A/B test: 90% old price, 10% new price → measure conversion delta over 30 days |
| `Error: OKR.*output.based\|OKR.*feature.ship\|task.list.*disguised` + `grep -rn "Objective.*Ship\|KR.*Launch\|OKR.*Build\|Objective.*Deliver\|Objective.*Release" okrs.md` shows output-verb OKRs | Quarterly review: "We shipped onboarding v2!" — great, but week-4 retention went from 40% to 38%. The OKR was green (shipped the feature) but the business outcome was red (retention got worse). The team celebrated building the wrong thing | OKRs measure the output (did we ship?) rather than the outcome (did the metric move?). When OKRs are output-based, teams optimize for shipping, not for impact. Features become the goal rather than hypotheses to be tested. Green OKRs with red metrics is organizational cognitive dissonance | Rewrite all OKRs as outcome-based: "Ship X" → "Increase [metric] from [baseline] to [target] (hypothesis: [X] drives improvement because [reason])." The feature is the bet; the metric is the result. If the metric doesn't move, the feature didn't work — regardless of whether it shipped on time | 1. Audit: `grep -rn "Objective\|KR:" okrs.md \| grep -E "Ship\|Launch\|Build\|Deliver\|Release\|Complete"` 2. For each match: rewrite as "Increase/Reduce/Improve [metric] from [X] to [Y]" 3. Verify: `grep -rn "Objective\|KR:" okrs.md \| grep -c "Increase\|Reduce\|Improve"` → must = total OKR count 4. Quarterly: compare metric movement vs OKR completion — if OKRs green but metrics red, OKRs are wrong |


## What Good Looks Like

> You've just completed the product strategy exercise. Your product vision is one sentence every person in the company can repeat from memory — not a paragraph nobody read. The Sean Ellis survey shows >40% "very disappointed" with statistical significance, and you know which segment drives that number. Your competitive analysis names exactly three defensible advantages backed by evidence, not "we have better UX." OKRs cascade cleanly from company strategy to team execution with measurable outcomes, not activity counts. Your pricing strategy is anchored to a value metric customers recognize, and you've tested willingness-to-pay before publishing the pricing page.


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Product vision documented and communicated — one sentence that defines the future state and why it matters | `grep -rn "vision\|product.vision\|future.state" product-strategy.md` → must match clear vision statement with target user and differentiated outcome | Template: `templates/product-vision.md` — one-sentence vision + supporting narrative |
| **[S2]** | PMF assessed with quantitative gates — Sean Ellis test, retention curves, organic growth %, NPS | `grep -rn "Sean.Ellis\|retention.curve\|organic.growth\|PMF.*score" pmf-assessment.md` → must find > 3 quantitative metrics with thresholds | PMF template: `templates/pmf-assessment.md` — 4-gate checklist with pass/fail |
| **[S3]** | Competitive landscape with win/loss data updated within last 90 days | `find . -name "*competitive*" -mtime -90` → must return at least 1 file; `grep -c "win.loss\|win/loss\|loss.reason" competitive*.md` → must find > 0 | `scripts/competitive-scan.sh` — automated competitor monitoring + quarterly review reminder |
| **[S4]** | Pricing strategy with value-based methodology and willingness-to-pay data from 20+ target customers | `grep -rn "Van.Westendorp\|Gabor.Granger\|conjoint\|willingness.to.pay" pricing*.md` → must find methodology name + sample size > 20 | Template: `templates/pricing-strategy.md` — requires WTP methodology + value-based justification |
| **[S5]** | OKRs: objectives qualitative and outcome-based, KRs quantitative with baseline and target | `grep -rn "Objective\|KR:" okrs.md \| grep -E "Increase\|Reduce\|Improve\|Achieve"` → must match all objectives; `grep -c "Ship\|Launch\|Build\|Deliver" okrs.md` → must be 0 | OKR template: `templates/okr-template.md` — validates outcome verbs, rejects output verbs |
| **[S6]** | Roadmap: Now/Next/Later format, theme-based, aligned to objectives | `grep -rn "Now\|Next\|Later\|theme" roadmap.md` → must find Now/Next/Later columns; `grep -c "Q[1-4]\|quarter" roadmap.md` → must be 0 outside "Now" column | Roadmap template: `templates/roadmap.md` — enforces Now/Next/Later + theme-based |
| **[S7]** | North Star metric defined and tracked — one metric that captures delivered customer value | `grep -rn "North.Star\|north.star\|NSM" metrics.md` → must find single metric definition with current baseline and target | Template: `templates/north-star.md` — one metric + input levers + counter-metrics |
| **[S8]** | Prioritization framework in place (RICE, CD3, or equivalent) with scoring applied to all roadmap items | `grep -rn "RICE\|CD3\|prioritization.score" roadmap.md` → must find scores per item; `grep -c "RICE\|CD3" roadmap.md` → must equal number of roadmap items | Roadmap template enforces RICE/CD3 scoring per item |
| **[S9]** | Customer feedback loop: discovery interviews, NPS, support tickets, win/loss analysis all active | `grep -rn "discovery.interview\|NPS\|support.ticket\|win.loss" feedback*.md` → must find > 3 feedback sources with frequency | Template: `templates/feedback-loop.md` — tracks all sources + review cadence |
| **[S10]** | Retention cohort analysis: "aha moment" identified, time-to-value measured, cohorts tracked monthly | `grep -rn "aha.moment\|time.to.value\|cohort\|retention.curve" retention*.md` → must find aha moment definition + cohort data | Template: `templates/retention-analysis.md` — cohort table + aha moment tracking |
| **[S11]** | GTM model validated with rationale — PLG vs sales-led choice supported by data | `grep -rn "PLG\|product.led\|sales.led\|GTM.model" gtm*.md` → must find model choice with supporting data (ACV, sales cycle, user behavior) | Template: `templates/gtm-model-decision.md` — decision matrix with criteria |
| **[S12]** | Cross-skill coordination map documented for key decisions | `grep -rn "cross.skill\|coordination\|dependency" cross-skill*.md` → must find skill dependencies with contact cadence | Template: `templates/cross-skill-map.md` — skill dependency matrix |

## Footguns
<!-- DEEP: 10+min — war stories from product strategy execution -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Declared product-market fit based on a Sean Ellis score of 42% from 187 respondents — but 162 of them came from a $25 Amazon gift card promo campaign | A B2C app ran a PMF survey after a paid acquisition campaign. "How would you feel if you could no longer use the product?" — 42% said "very disappointed." The team raised a Series A based on this data. Six months post-fundraise: organic retention was 8% at day 30. The paid users had never intended to use the product — they filled out the survey for the gift card. | PMF signal was contaminated by incentivized respondents. Paid acquisition users respond to surveys differently than organic users — they're incentivized to be positive or to rush through. The 42% wasn't PMF, it was gratitude for a free $25. | **Run PMF surveys exclusively on users with organic acquisition and >30 days of active usage.** Segment results by acquisition channel — if paid users score 20 points higher than organic, that's a red flag, not a signal. Minimum sample: 100 respondents, all from the organic cohort. Track retention by cohort: if month-3 retention is below 25%, no survey score matters. |
| Priced the enterprise plan at $999/month flat — a customer with 400 seats signed up and their support tickets cost more than their subscription | A B2B SaaS priced by "plan" not by "usage unit." The enterprise plan included unlimited seats. A mid-market company with 400 employees onboarded in week 1 — generating 83 support tickets in the first month, each requiring 20-minute engineering triage. The account was unprofitable from month 2. Meanwhile, a 12-person startup on the same plan generated 2 tickets per month and was wildly profitable. | Value metric mismatch. Pricing by "plan tier" works when usage scales predictably with value — but seat count drove support costs, not revenue. The unlimited seat plan attracted the highest-cost customers at the lowest unit price. | **Anchor pricing to a value metric that scales with costs.** If support cost scales with seats, price per seat. If it scales with API calls, price per API call. Run a profitability analysis per customer cohort: for your bottom 20% of customers by revenue, what's the gross margin? If it's negative, your pricing model is broken. Add a seat-based multiplier even to "unlimited" plans — "unlimited" can mean "up to 50 seats included, $15/additional." |
| Prioritized 43 features by RICE scores — but the scores were computed by PMs alone. Engineering re-estimated effort and reordered 31 of the 43 (72%) during planning. | A product team ran a quarterly prioritization sprint. PMs scored Reach, Impact, and Confidence for 43 features. Engineering leadership scored Effort separately. When the two lists were merged, the "top 10" from each bore almost no overlap. Sprint 1 committed to features that PMs rated as "1 sprint" but engineering estimated at "6 sprints." Four sprints delivered 2 features instead of the planned 8 — stakeholders lost confidence in the roadmap. | RICE without engineering calibration on Effort is just wishlist ranking. PMs consistently underestimate effort by 2–4× because they don't see database migrations, auth changes, or integration testing. | **Co-score RICE as a cross-functional exercise.** PM brings Reach/Impact numbers, engineering brings Effort estimates. If there's a >2× disagreement on Effort, discuss before scoring. Normalize: ask engineering to estimate in T-shirt sizes (S/M/L/XL) and convert via historical velocity. Track estimation accuracy over time and add a 30% buffer to first-time feature estimates. Publish the RICE table with both raw PM scores and engineering-adjusted scores — transparency builds trust. |
| Modeled PLG viral coefficient at 0.4 because "one LinkedIn post got 12,000 views" — actual coefficient was 0.03 over 6 months | A product strategist built a PLG model projecting 1.4× monthly growth from viral invites. The benchmark: one viral LinkedIn post reached 12K views, 800 signups. They modeled that 40% of new users would invite others. Reality: organic invite rate was 3%, because the product had no sharing mechanism built in — users had to copy a URL and send it manually. The "viral coefficient" was actually just one good social media post. | Confusing a one-time marketing event with a sustainable viral loop. Viral coefficient measures regular user behavior — "what percentage of new users invite others within 30 days?" A LinkedIn post is acquisition marketing, not product virality. | **Measure viral coefficient from in-product behavior, not marketing campaigns.** Instrument the invite flow: track invites sent, invites accepted, and time-to-invite. If users aren't inviting within 7 days of signup, your product doesn't have viral mechanics — you have a marketing channel. Only model growth from viral coefficient if you've measured it over 90 days from the cohort that signed up 90 days ago. |
| A/B tested a pricing page — chose the winner after 4 days with 53 conversions. p-value was 0.41. The "winner" decreased revenue 6% over the next quarter when rolled out to all traffic. | A PM ran an A/B test on enterprise pricing page layout. The test variant showed +14% conversion over control after 4 days. The PM stopped the test and launched the variant. Over the full quarter with 8,200 conversions, the variant was actually -6% on revenue — early noise looked like signal because the sample was tiny. The 14% lift in the first 4 days was driven by 4 large deals in the test group that closed in the same week. | Peeking at A/B results and stopping early. With 53 total conversions, the minimum detectable effect was >35% — the test was grossly underpowered. The PM didn't calculate required sample size before starting. | **Calculate required sample size before any A/B test.** Use a calculator: baseline conversion rate, minimum detectable effect (set at 5% for pricing), significance at 95%, power at 80%. If that says you need 2,400 conversions per variant, don't look at results until you have 2,400. Pre-commit to a test duration (minimum 2 full business weeks to capture weekly patterns). Write the stop condition before the test starts — and share it publicly so you can't move the goalposts. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

Use this to diagnose where you actually are, not where you want to be.

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| Your product strategy is a collection of competitor features you "need to catch up on" and your vision statement could describe any company in your category | You can name the one metric that, if it moved 10%, would change a strategic decision — and you have 6 months of data showing its baseline, variance, and driver correlations | A product you defined the strategy for reaches $10M ARR, and when the CEO describes "why we're winning," the words match the strategy document you wrote 2 years earlier |
| You use "industry standard" pricing without testing willingness-to-pay with your specific customers | You've run a Van Westendorp price sensitivity study and can say "at $49/month, 72% of our ICP said they'd buy; at $79, it drops to 31%" with named customers behind the numbers | You increase prices by 30% and net revenue retention stays flat — because you priced to value from day one, not to competitor benchmarks |
| You present competitive analysis as a feature comparison grid with green/red checkmarks | You can draw a 2×2 positioning map where your company occupies a quadrant no competitor owns, and you can explain why you can defend it | A competitor's CEO names your product as their biggest threat on an earnings call — and you saw it coming 18 months before they did |

**The Litmus Test:** Can you walk into a company, spend 2 hours with their product and 2 hours interviewing 5 customers, and produce a 1-page strategy identifying the single biggest thing they should STOP doing? If you can't identify waste as fast as opportunity, you're not L3 yet. Masters know that subtraction beats addition more often than not.

## Deliberate Practice

Product strategy is pattern-matching refined through exposure to diverse business models, markets, and outcomes. The strategist who has studied 100 failures sees patterns the strategist who has only studied successes cannot.

### The Strategy Improvement Loop

```
HYPOTHESIZE → TEST → SYNTHESIZE → (update mental model) → repeat
```

After every strategic decision: write down your explicit prediction. Check it at 3, 6, and 12 months. The gap between prediction and reality is your curriculum.

### Practice Routines by Skill Level

| Level | Practice | Frequency |
|---|---|---|
| **Novice** | Do a competitive analysis of 3 products in your space. For each, identify: what they say they are, what they actually are, and the gap between those two. | Monthly |
| **Competent** | Write a 500-word strategy memo for a product move (launch, pivot, kill). Exchange with a peer for red-teaming. Rewrite based on critiques. | Biweekly |
| **Expert** | Run a Sean Ellis PMF survey with real users. Calculate the "very disappointed" percentage. Benchmark against industry (40%+ is strong). Identify which segment drives the metric. | Quarterly |
| **Master** | Study 1 failed product deeply per quarter: read post-mortems, founder interviews, investor letters. Write what you would have done differently — then write why you might have been wrong about that too. | Quarterly |

### The One Highest-Leverage Activity

**Write your strategy on one page, then delete it and write it again in half the words.** The second version reveals what you actually believe. The first version reveals what you think you should believe. Do this before every strategy presentation.

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Inspired](https://www.svpg.com/books/inspired/) — Marty Cagan
- [Escaping the Build Trap](https://www.amazon.com/dp/149197379X) — Melissa Perri
- [Obviously Awesome](https://www.amazon.com/dp/1999023005) — April Dunford
- [The Mom Test](https://www.momtestbook.com/) — Rob Fitzpatrick
- [Product-Led Growth](https://www.productledgrowthbook.com/) — Wes Bush
- [Reforge](https://www.reforge.com/) — Product strategy programs
- [Lenny's Newsletter](https://www.lennysnewsletter.com/) — Deep dives
