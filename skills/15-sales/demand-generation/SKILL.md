---
name: demand-generation
description: >
  Use when building paid acquisition campaigns, designing lead scoring models, optimizing
  conversion rates, or implementing ABM programs. Handles paid acquisition (Google, LinkedIn,
  Meta ads), email marketing automation, lead scoring and nurturing, MQL to SQL handoff,
  attribution modeling (first-touch, multi-touch, U-shaped), CAC optimization, landing page CRO,
  webinar programs, ABM for enterprise, and marketing operations (HubSpot, Marketo, Pardot).
  Do NOT use for product positioning, brand strategy, or content creation.
license: MIT
tags:
  - demand-generation
  - paid-acquisition
  - lead-scoring
  - attribution
  - abm
  - cro
  - email-marketing
  - hubspot
author: Sandeep Kumar Penchala
type: sales
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  consumes_from:
    - marketing-manager
    - analytics-engineer
    - growth-engineer
  feeds_into:
    - sales-engineer
    - marketing-manager
    - revops-manager
  alternatives:
    - content-strategist
---

# Demand Generation (Demand Gen / Growth Marketing)
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Own the pipeline engine: paid acquisition across Google/LinkedIn/Meta, email marketing automation, lead scoring, MQL→SQL handoff, attribution modeling, CAC optimization, landing page CRO, webinar programs, ABM for enterprise, and marketing operations (HubSpot/Marketo/Pardot).

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.csv", "UTM\|utm_source\|utm_medium\|campaign\|Campaign Name")` OR `file_contains("*.xlsx", "CAC\|Cost Per Lead\|CPL\|ROAS\|pipeline influenced")` OR `file_contains("*.docx", "lead scoring\|MQL\|SQL\|nurture sequence")`  | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.xlsx", "brand awareness\|positioning\|messaging\|competitive analysis\|launch plan")` OR `file_contains("*.pptx", "Brand Deck\|Messaging Framework\|positioning statement")`  | Invoke **marketing-manager** instead. This is brand & positioning work. |
| A3 | `file_contains("*.csv", "SEO\|organic traffic\|keyword rank\|backlink\|content calendar")` OR `file_contains("*.docx", "content strategy\|blog calendar\|editorial plan")`  | Invoke **content-strategist** instead. This is content & SEO work. |
| A4 | `file_contains("*.xlsx", "A/B test\|experiment\|variant\|statistical significance\|conversion rate")` AND `file_contains("*.csv", "control group\|treatment group\|hypothesis")`  | Invoke **growth-engineer** instead. This is experimentation infrastructure. |
| A5 | `file_contains("*.csv", "pipeline forecast\|closed-won\|ARR\|churn\|renewal")` AND `file_contains("*.xlsx", "revenue\|bookings\|quota\|attainment")`  | Invoke **revops-manager** instead. This is revenue operations. |
| A6 | `file_contains("*.xlsx", "ad creative\|Ad Copy\|headline variant\|CTR\|impressions")` AND `file_contains("*.csv", "Google Ads\|LinkedIn Ads\|Meta Ads\|campaign performance")`  | Jump to **Decision Trees** — Paid Channel Selection. |
| A7 | `file_contains("*.csv", "lead\|Lead Source\|lead status\|Lifecycle Stage")` AND `file_contains("*.docx", "lead scoring model\|scoring criteria\|point threshold")`  | Jump to **Decision Trees** — Lead Scoring Design. |
| A8 | `file_contains("*.xlsx", "attribution\|Attribution Model\|first-touch\|multi-touch\|U-shaped\|W-shaped")` | Jump to **Decision Trees** — Attribution Model Selection. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Launch paid acquisition (Google/LinkedIn/Meta ads) → Go to "Decision Trees > Paid Channel Selection"
├── Build email marketing automation & nurture sequences → Jump to "Core Workflow > Phase 3"
├── Design lead scoring & MQL→SQL handoff → Go to "Decision Trees > Lead Scoring Design"
├── Set up attribution modeling → Jump to "Decision Trees > Attribution Model Selection"
├── Optimize CAC (cost per acquisition) → Go to "Core Workflow > Phase 4"
├── Build an ABM program for enterprise → Go to "Core Workflow > Phase 5"
├── Need campaign positioning & messaging → Invoke `marketing-manager` skill instead
└── Not sure where to start? → Start at "Core Workflow > Phase 1"
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to spend a dollar on paid acquisition without a tracking plan.** If you can't measure ad impression → click → landing page → form fill → CRM → closed-won, you're buying vanity metrics. UTM hygiene is non-negotiable. | Trigger: generated campaign plan includes ad spend > $0 AND `grep -rn "UTM\|utm_source\|utm_medium\|tracking plan\|conversion tracking" *.csv *.docx` returns 0 results for that campaign | STOP. Respond: "I need a tracking plan before any ad spend. Share your UTM taxonomy, conversion tracking setup (Google Ads pixel, LinkedIn Insight Tag), and CRM integration status. I won't allocate budget without closed-loop attribution." |
| **R2** | **REFUSE to define MQL and SQL criteria without sales and marketing sign-off in writing.** If both teams disagree on what a "qualified lead" is, the handoff breaks and pipeline numbers are fiction. | Trigger: generated lead scoring model defines MQL/SQL thresholds AND `file_contains("*.docx\|*.pdf", "signed.*MQL\|MQL.*signed\|agreed.*lead scoring")` returns 0 results | STOP. Respond: "MQL/SQL definitions must be signed by sales and marketing leadership. Share the signed agreement or I'll generate a draft for joint review. No scoring model goes live without dual sign-off." |
| **R3** | **REFUSE to optimize for leads alone when pipeline and revenue are the actual goals.** 500 MQLs that convert to 3 opportunities is a targeting failure, not a volume success. | Trigger: generated report or dashboard uses "Leads Generated" as the North Star metric AND `grep -rn "pipeline\|Pipeline Influenced\|closed-won\|revenue" *.xlsx *.csv` returns < 2 pipeline metrics | STOP. Replace primary KPI with "Pipeline Revenue Influenced" and "Cost Per Opportunity." Add secondary metrics: MQL→SQL conversion %, SQL→Opportunity %, Cost Per Closed-Won $. Leads alone are a vanity metric — refuse to optimize exclusively for them. |
| **R4** | **STOP and require holdout groups on all email nurture sequences.** If you can't measure incremental lift vs a control group that receives nothing, you don't know if nurture is adding value or just annoying people who would have bought anyway. | Trigger: generated email nurture plan sequences emails to 100% of a segment AND `grep -rn "holdout\|control group\|incremental lift\|10%" *.csv *.docx` returns 0 results | STOP. Insert 10% holdout requirement: "Split segment into 90% treatment (receives nurture) and 10% holdout (receives nothing). Measure incremental lift in pipeline and revenue at 90 days. Nurture that can't beat 'do nothing' should be killed." |
| **R5** | **REFUSE to report attribution without stating the model and its limitations.** "Campaign X drove $500K" is meaningless without methodology. Different models produce wildly different numbers. | Trigger: generated report states revenue/pipeline attributed to a campaign AND `grep -rn "attribution model\|Attribution Model\|first-touch\|multi-touch\|U-shaped\|lookback" *.docx *.xlsx` returns 0 in the same report | STOP. Insert attribution disclaimer: "Reported using [U-shaped] attribution model with a [90-day] lookback window. Multi-touch models distribute credit differently than first-touch or last-touch. Attribution is directional — use for budget allocation, not as absolute truth." |
| **R6** | **DETECT and WARN about paid campaigns without creative testing cadence.** Running a single ad creative indefinitely guarantees creative fatigue, rising CPL, and diminishing returns. | Trigger: generated campaign plan has ad spend allocated to a channel AND `grep -rn "creative test\|A/B test\|variant\|ad rotation" *.xlsx *.csv` returns 0 for that channel | WARN: Add minimum creative testing requirement: "Launch with ≥5 ad variants per channel. Kill variants after $500 spend if CTR < 2× channel average. Replace killed variants weekly. Never run a single creative for more than 14 days without refresh." |
| **R7** | **DETECT and WARN about ABM programs without a sales follow-up SLA.** Marketing warms the account but sales doesn't follow up within 48 hours — the engagement signal decays and ABM investment is wasted. | Trigger: generated ABM plan includes account-level engagement tactics AND `grep -rn "SLA\|follow-up\|48 hour\|response time\|sales commitment" *.docx` returns 0 | WARN: Insert sales SLA clause: "Sales commits to 48-hour follow-up on all ABM engagement signals. If SLA breached, ABM program pauses until sales capacity is restored. Signal decay is exponential — after 48 hours, 80% of intent is lost." |

## The Expert's Mindset

Master demand generations understand that strategy is not about predicting the future — it's about **being less wrong than the competition, faster**.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Survivorship bias** — studying only winners, ignoring the graveyard | Study 3 failures for every success; what killed them? |
| **Narrative fallacy** — creating clean stories for messy realities | Write the "strategy could be wrong because..." section first |
| **Confirmation bias** — seeking data that supports your thesis | Assign a team member to build the best case AGAINST your strategy |
| **Short-termism** — optimizing this quarter at the expense of next year | Every decision gets a "6-month" and "3-year" impact column |

### What Masters Know That Others Don't
- **The bottleneck is always one thing.** Find it. Fix it. Then find the next one.
- **Strategy = what you say NO to.** If your strategy doesn't exclude anything, it's not a strategy.
- **Timing beats brilliance.** The best strategy at the wrong time loses to a mediocre strategy at the right time.

### When to Break Your Own Rules
- **Bet the company when the asymmetry is right.** If downside = $1M and upside = $1B, the math doesn't care about your process.
- **Ignore the data when you're creating a new category.** By definition, there's no data for something that doesn't exist yet.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Initiative | Execute a defined strategic initiative with clear metrics |
| **L2** | Product line / function | Define strategy for a product line; own outcomes |
| **L3** | Business unit | Set multi-year strategy for a business unit; allocate resources across competing priorities |
| **L4** | Company | Define company-wide strategy; make existential trade-off decisions |
| **L5** | Industry | Shape industry dynamics; create new market categories |

**Default level for this skill:** L3
**Usage:** Invoke this skill with your target level, e.g., "as an L3 demand generation, develop..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->

- Launching or scaling paid acquisition across Google Ads, LinkedIn Ads, or Meta Ads
- Building or rebuilding email marketing automation with lead nurturing sequences
- Designing a lead scoring model and formalizing the MQL→SQL handoff between marketing and sales
- Setting up attribution modeling to understand which channels and campaigns drive pipeline
- Diagnosing high CAC or low conversion rates at specific funnel stages
- Running a landing page CRO program — A/B testing headlines, CTAs, forms, and social proof
- Building an account-based marketing (ABM) program targeting 50-500 named enterprise accounts
- Launching a webinar or virtual event series as a demand generation engine
- Evaluating or migrating marketing automation platforms (HubSpot, Marketo, Pardot, ActiveCampaign)

## Decision Trees

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Paid Channel Selection

```
                              ┌──────────────────────────────┐
                              │ START: Which paid channels?   │
                              └────────────┬─────────────────┘
                                           │
                         ┌─────────────────▼─────────────────┐
                         │ What are you selling & to whom?   │
                         └────┬──────────────┬───────────────┘
                              │              │
                   ┌──────────▼────┐  ┌──────▼────────────┐
                   │ B2B SaaS      │  │ B2C / Consumer    │
                   │ (ACV > $5K)   │  │ (ACV < $500)      │
                   └──────┬────────┘  └──────┬────────────┘
                          │                  │
               ┌──────────▼──────┐  ┌────────▼────────────┐
               │ Primary:        │  │ Primary:             │
               │ LinkedIn Ads    │  │ Meta Ads + Google    │
               │ + Google Search │  │ Display + TikTok     │
               │ (high-intent)   │  │ (broad reach)        │
               │                 │  │                      │
               │ Secondary:      │  │ Secondary:           │
               │ Review sites    │  │ Google Search        │
               │ (G2/Capterra),  │  │ (intent capture),    │
               │ content         │  │ YouTube, influencer  │
               │ syndication,    │  │                      │
               │ podcast/        │  │                      │
               │ newsletter      │  │                      │
               │ sponsorships    │  │                      │
               └─────────────────┘  └──────────────────────┘
```
**B2B LinkedIn:** Target by job title, company size, industry. Lead-gen forms (pre-filled) outperform landing page redirects by 3-5x on conversion. Expect CPL $50-200. Use for: top-of-funnel awareness + mid-funnel lead gen.

**B2B Google Search:** Bid on competitor names, category terms, pain-point queries. High intent — these prospects are actively searching. Expect CPC $5-50 for SaaS. Use for: bottom-of-funnel capture.

**B2C Meta/TikTok:** Creative is everything — test 5+ video variants per audience. Broad targeting + strong creative outperforms hyper-targeted + weak creative. Expect CPM $5-20.

### Attribution Model Selection

```
                              ┌──────────────────────────────┐
                              │ START: Which attribution       │
                              │ model to use?                 │
                              └────────────┬─────────────────┘
                                           │
                         ┌─────────────────▼─────────────────┐
                         │ How many touches before purchase? │
                         └────┬──────────────┬───────────────┘
                              │              │
                    ┌─────────▼────┐  ┌──────▼──────────────┐
                    │ 1-3 touches  │  │ 4+ touches,          │
                    │ (SMB, short  │  │ long cycle            │
                    │ cycle)       │  │ (Enterprise)          │
                    └──────┬───────┘  └──────┬───────────────┘
                           │                 │
                ┌──────────▼──────┐  ┌────────▼────────────┐
                │ First-Touch or  │  │ Multi-Touch:         │
                │ Last-Touch      │  │ U-Shaped or W-Shaped │
                │                 │  │                      │
                │ Simple,         │  │ U-Shaped: 40% first  │
                │ directional.    │  │ touch, 40% lead      │
                │ Good enough for │  │ creation, 20% split  │
                │ direct response.│  │ across middle touches│
                │                 │  │                      │
                │ Limitations:    │  │ W-Shaped: 30% first  │
                │ Over-credits    │  │ touch, 30% lead      │
                │ one touch.      │  │ creation, 30% opp    │
                └─────────────────┘  │ creation, 10% split  │
                                    └──────────────────────┘
```
**Recommended default:** U-Shaped attribution with a 90-day lookback window. 40% credit to first touch, 40% to lead creation touch, 20% evenly across middle touches. State the model explicitly in every report.

**When to use data-driven attribution:** >50 conversions/month per channel, machine learning can assign fractional credit based on actual influence patterns. Requires significant data volume.

### Lead Scoring Design

```
                              ┌──────────────────────────────┐
                              │ START: Build lead scoring     │
                              └────────────┬─────────────────┘
                                           │
                         ┌─────────────────▼─────────────────┐
                         │ Scoring dimensions?               │
                         └────┬──────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
    ┌─────────────────┐ ┌──────────┐ ┌──────────────────┐
    │ Demographic Fit │ │ Behavior │ │ Engagement       │
    │ (Explicit)      │ │ (Implicit)│ │ (Recency/Depth) │
    ├─────────────────┤ ├──────────┤ ├──────────────────┤
    │ Job title: +15  │ │Pricing   │ │Website visit <7d │
    │ (target role)   │ │page visit│ │: +10             │
    │                 │ │: +20     │ │                  │
    │ Job title: +5   │ │Case study│ │Email click <14d  │
    │ (adjacent role) │ │download  │ │: +10             │
    │                 │ │: +15     │ │                  │
    │ Company size    │ │Demo      │ │Multiple visits   │
    │ in ICP: +10     │ │request:  │ │>3 pages: +15     │
    │                 │ │+30       │ │                  │
    │ Industry fit:   │ │Webinar   │ │No activity >30d  │
    │ +10             │ │attended │ │: -15             │
    │                 │ │: +10     │ │                  │
    │ Negative:       │ │          │ │Unsubscribed:     │
    │ Student: -30    │ │          │ │-50              │
    │ Competitor: -20 │ │          │ │                  │
    │ Personal email: │ │          │ │                  │
    │ -10             │ │          │ │                  │
    └─────────────────┘ └──────────┘ └──────────────────┘
```
**Scoring thresholds:** Score >50 = MQL (handoff to sales). Score 30-50 = Nurture (keep in marketing). Score <30 = Long-term nurture or discard.

**Validation:** Run a correlation analysis quarterly. Are high-scoring leads actually converting at higher rates? If not, your scoring model is broken. Adjust weights based on actual closed-won data, not hunches.

### CRO: Landing Page Funnel Leak Diagnosis

```
                              ┌──────────────────────────────┐
                              │ START: Which stage to fix?    │
                              └────────────┬─────────────────┘
                                           │
                         ┌─────────────────▼─────────────────┐
                         │ >70% bounce from LP without        │
                         │ any action?                        │
                         └────┬──────────────────────────┬───┘
                              │ YES                       │ NO
                              ▼                           ▼
                      ┌──────────────┐          ┌──────────────────────┐
                      │Top-of-funnel │          │ >60% drop between     │
                      │CRO:          │          │ form view → submit?   │
                      │Headline,     │          └──┬──────────────┬────┘
                      │hero image,   │             │ YES          │ NO
                      │above-fold    │             ▼              ▼
                      │value prop,   │    ┌──────────────┐ ┌──────────────┐
                      │page speed,   │    │ Form Friction│ │ Post-Convert │
                      │mobile UX     │    │ CRO:         │ │ CRO:         │
                      └──────────────┘    │ Reduce fields│ │ Thank-you    │
                                          │ to ≤5, add   │ │ page CTA,   │
                                          │ social proof │ │ nurture      │
                                          │ near CTA,    │ │ sequence,    │
                                          │ auto-fill,   │ │ sales follow │
                                          │ remove phone │ │ -up timing   │
                                          │ if not needed│ └──────────────┘
                                          └──────────────┘
```
**When to optimize above-fold:** Bounce >70%. Fix within 48 hours. Test headline + hero + CTA as a triad.

**When to optimize form:** >60% drop form → submit. Reduce to ≤5 fields. Every field costs ~10% conversion.

## Core Workflow

<!-- QUICK: 30s -- scan phase titles to understand the process -->

<!-- DEEP: 10+min -->

### Phase 1 (~20 min): Pipeline Modeling & Target Setting

Build a reverse funnel from revenue target: Revenue target → Pipeline needed (at close rate X) → SQLs needed (at SQL→Opp rate Y) → MQLs needed (at MQL→SQL rate Z) → Leads needed (at Lead→MQL rate W). Example: $2M quarterly revenue target. Avg deal size $50K = 40 closed deals. Close rate 25% = 160 opportunities. SQL→Opp rate 60% = 267 SQLs. MQL→SQL rate 15% = 1,780 MQLs. Lead→MQL rate 10% = 17,800 leads. Now allocate across channels: organic %, paid %, email %, events %, partner %. Track actuals vs. plan weekly. Reforecast monthly.

<!-- DEEP: 10+min -->

### Phase 2 (~60 min): Marketing Operations Setup

Marketing ops is the infrastructure: choose your platform (HubSpot for SMB/mid-market, Marketo for enterprise, Pardot if Salesforce-native required). Set up: (1) Tracking — UTM parameters enforced on every outbound link, form submissions captured with source data, cookie-based tracking for anonymous visitors, first-touch and last-touch fields populated at conversion, (2) Lead lifecycle stages — Visitor → Lead → MQL → SQL → Opportunity → Customer → Evangelist, with automated stage transitions based on scoring and actions, (3) Email automation — nurture sequences triggered by behavior (content download → related nurture track, pricing page visit → sales outreach alert), (4) List hygiene — bounce management, unsubscribe compliance, deduplication, suppression lists, (5) Attribution — U-shaped model as default, campaign influence tracking, ROI dashboards by channel, (6) Reporting — weekly pipeline dashboard: leads by channel, MQL volume, MQL→SQL rate, SQL→Opp rate, pipeline created, CAC by channel, LTV:CAC ratio.

<!-- DEEP: 10+min -->

### Phase 3 (~45 min): Email Marketing & Nurture

Design nurture sequences, not email blasts. Architecture: (1) Welcome sequence (3 emails over 7 days) — triggered on first conversion. Email 1: deliver the asset. Email 2: social proof + case study. Email 3: soft CTA (demo, trial, assessment), (2) Behavioral triggers — pricing page visit → case study email within 1 hour, feature page visit → product demo video, high engagement → sales alert, inactivity (30 days no click) → re-engagement drip (subject: "Still interested?"), (3) Newsletter (bi-weekly) — curated content, product updates, customer stories. Segment by persona so CTOs don't get end-user content, (4) Re-engagement — 3-email sequence for dormant leads. Email 1: "We miss you"

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Marketing Manager** | Campaign briefs, positioning, personas, messaging for ads | Approved messaging, target personas, asset briefs, launch timelines. **Decision gate:** Does campaign brief pass logo-swap test? → launch ready. **Artifact:** campaign brief doc + messaging framework. |
| **Analytics Engineer** | Attribution models, data pipelines, dashboards | Tracking requirements, event taxonomy, attribution methodology, data quality. **Decision gate:** Is attribution model locked for 12 months? → report consistently. **Artifact:** attribution model doc + UTM taxonomy. |
| **Sales Engineer** | MQL→SQL handoff quality, lead qualification feedback | Lead quality feedback, conversion rates by channel, content preferences. **Decision gate:** Is MQL→SQL conversion > 15%? → handoff process healthy. **Artifact:** MQL quality scorecard + handoff SLA report. |
| **Growth Engineer** | Landing page CRO, A/B testing infrastructure, experiment design | Experiment results, CRO hypotheses, technical feasibility of landing page changes. **Decision gate:** Is CRO experiment statistically significant (p < 0.05)? → ship winner. **Artifact:** A/B test results + implementation spec. |
| **Content Strategist** | Content assets for nurture, offers for campaigns | Asset briefs, content calendar, SEO-validated topics, target keywords. **Decision gate:** Does content asset have a CTA with measurable conversion? → campaign-ready. **Artifact:** asset brief + performance benchmarks. |
| **SEO Specialist** | Organic/content synergy, keyword-driven paid campaigns | Keyword data, organic landing page performance, paid-organic cannibalization checks. **Decision gate:** Is paid cannibalization < 10% of organic traffic? → budget efficient. **Artifact:** keyword overlap report. |
| **Customer Success Manager** | Customer stories for webinars, reference logos for landing pages | Customer advocates, NPS data, churn signals that indicate targeting or messaging issues. **Decision gate:** Is NPS > 30 for reference customers? → safe to feature. **Artifact:** customer advocacy roster. |
| **Business Strategist** | CAC targets, LTV models, budget allocation, ROI reporting | Revenue targets, unit economics, growth targets, budget constraints. **Decision gate:** Is LTV:CAC > 3:1 for each channel? → budget allocation sound. **Artifact:** channel-level unit economics dashboard. |
| **RevOps Manager** | Pipeline analytics, forecasting, attribution integration | Campaign-attributed pipeline data, conversion rates by channel. **Decision gate:** Is campaign pipeline > 40% of total pipeline? → demand gen is primary growth engine. **Artifact:** pipeline attribution report by campaign. |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| CAC increases >30% month-over-month on any channel | Marketing Manager, Analytics Engineer, Business Strategist | Channel efficiency at risk; may need pause, creative refresh, or targeting change |
| MQL→SQL conversion drops below 10% for >2 weeks | Sales Engineer, Marketing Manager | Scoring model or sales follow-up broken; pipeline forecast at risk |
| Email domain reputation drops (bounce >2%, spam complaint >0.1%) | Marketing Manager | Deliverability crisis; pause sends, audit list hygiene, warm domain |
| Landing page conversion drops below 2% (from ad traffic) | Growth Engineer, Marketing Manager | CRO audit; test headline, offer, form, page speed |
| Attribution tracking breaks (UTMs missing, cookie consent change) | Analytics Engineer, Marketing Manager | All spend data becomes unreliable; fix before launching new campaigns |
| Pipeline gap >30% of target at mid-quarter | Marketing Manager, Sales Engineer, Business Strategist | Emergency pipeline generation; surge campaigns, event acceleration, lead list activation |

### Escalation Path

```
CAC exceeds target by >50% for >30 days → Business Strategist + VP Marketing. Channel pause or restructure.
Attribution/data pipeline failure >48 hours → Analytics Engineer + VP Marketing. Revenue reporting blind spot.
Marketing automation platform outage >4 hours → Platform vendor + VP Marketing + Sales Ops. Lead processing halted.
MQL quality crisis (sales rejects >50% of MQLs) → Sales leadership + Marketing Manager. Scoring reset + joint review.
```

### Cross-skills Integration

```bash
# Chain: marketing-manager → demand-generation → sales-engineer
# Campaign execution: PMM provides positioning → Demand gen executes across channels → SE receives qualified MQLs

# Chain: analytics-engineer → demand-generation → growth-engineer
# Data-driven optimization: Analytics builds attribution model → Demand gen optimizes channel mix → Growth engineer tests CRO changes

# Chain: demand-generation → growth-engineer
# Conversion optimization: Demand gen identifies funnel leaks → Growth engineer builds and runs A/B tests
```

## Proactive Triggers

<!-- QUICK: 30s -- when to proactively notify stakeholders -->

| Trigger | Notify | Why |
|---------|--------|-----|
| CAC increases >30% month-over-month on any paid channel | Marketing Manager, Business Strategist, Analytics Engineer | Channel efficiency crisis; may need creative refresh, targeting change, or channel pause before budget is wasted |
| MQL→SQL conversion drops below 10% for 2+ consecutive weeks | Sales Engineer, Marketing Manager, RevOps Manager | Scoring model broken or sales follow-up degraded; pipeline forecast at risk; joint marketing-sales audit required |
| Email domain reputation warning (bounce >2% or spam complaint >0.1%) | Marketing Manager, Analytics Engineer | Deliverability crisis imminent; pause all sends, audit list hygiene, and warm domain before full blacklist occurs |
| Attribution tracking breaks (UTM pipeline failure, cookie consent change, CRM sync error) | Analytics Engineer, Marketing Manager, RevOps Manager | All spend data becomes unreliable; fix attribution pipeline before launching any new campaigns — flying blind on spend |
| Pipeline gap exceeds 30% of quarterly target at mid-quarter | Marketing Manager, Sales Engineer, Business Strategist, RevOps Manager | Emergency pipeline generation required; surge campaigns, event acceleration, lead list activation, and SDR blitz |
| Landing page conversion drops below 2% from paid traffic (sustained >1 week) | Growth Engineer, Marketing Manager | CRO emergency; test headline, offer, form length, page speed. Every day below threshold burns ad budget with no return |
| Competitor launches aggressive paid campaign targeting your branded keywords or ICP | Marketing Manager, Business Strategist | Brand CPC inflation and share-of-voice loss; competitive response strategy needed within 48 hours |
| Nurture sequence holdout test shows no statistically significant lift vs. control after 90 days | Marketing Manager, Content Strategist | Nurture is burning effort for zero incremental pipeline; kill the sequence and redirect resources to higher-ROI activities |

## What Good Looks Like

<!-- QUICK: 30s -- concrete success description -->

Every paid channel has a documented CAC and LTV:CAC ratio >3:1. MQL→SQL conversion rate >15% and stable quarter-over-quarter. Attribution model is documented (U-shaped, 90-day lookback) and consistently applied across all reports. Email nurture sequences have <0.5% unsubscribe rate and >3% CTR. Landing pages convert >3% from paid traffic. Lead scoring model validated quarterly against actual closed-won data — high-scoring leads convert at >2x the rate of medium-scoring leads. ABM program generates >30% higher ACV than non-ABM. Pipeline dashboard updates daily with no data gaps. Marketing-sourced pipeline consistently hits >40% of total pipeline.

## Deliberate Practice

```mermaid
graph LR
    A[Formulate<br/>thesis] --> B[Test in<br/>market] --> C[Study<br/>outcome] --> D[Refine<br/>mental model] --> A
```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Write a strategy memo for a past business event; compare your reasoning to what actually happened | Monthly |
| **Competent** | Write 3 strategies for the same goal with different constraints; debate which wins | Quarterly |
| **Expert** | Reverse-engineer a competitor's strategy from public information; validate against their next move | Quarterly |
| **Master** | Board-level strategy for a company in a different industry; present to a peer CEO for feedback | Semi-annually |

**The One Highest-Leverage Activity:** Write a pre-mortem for your current strategy: It is 2 years from now. Our strategy failed. Why?

## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)

