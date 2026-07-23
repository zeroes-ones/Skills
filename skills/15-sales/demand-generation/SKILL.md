---
name: demand-generation
description: Paid acquisition (Google/LinkedIn/Meta ads), email marketing automation, lead scoring & nurturing, MQL→SQL handoff, attribution modeling (first-touch, multi-touch, U-shaped), CAC optimization, landing page optimization & CRO, webinar programs, ABM for enterprise, marketing ops (HubSpot/Marketo/Pardot).
author: Sandeep Kumar Penchala
type: sales
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - demand-generation
  - demand-gen
  - growth-marketing
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
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

Design nurture sequences, not email blasts. Architecture: (1) Welcome sequence (3 emails over 7 days) — triggered on first conversion. Email 1: deliver the asset. Email 2: social proof + case study. Email 3: soft CTA (demo, trial, assessment), (2) Behavioral triggers — pricing page visit → case study email within 1 hour, feature page visit → product demo video, high engagement → sales alert, inactivity (30 days no click) → re-engagement drip (subject: "Still interested?"), (3) Newsletter (bi-weekly) — curated content, product updates, customer stories. Segment by persona so CTOs don't get end-user content, (4) Re-engagement — 3-email sequence for dormant leads. Email 1: "We miss you" + value. Email 2: "Last chance" + offer. Email 3: "Confirm you want to stay" — no click = unsubscribe. Always run a 10% holdout group on nurture sequences. Measure: open rate >20%, CTR >3%, unsubscribe <0.5% per send, conversion rate from nurture >5%.

<!-- DEEP: 10+min -->

### Phase 4 (~30 min): CAC Optimization

Calculate CAC per channel: total channel spend / customers acquired from that channel (using your chosen attribution model). Benchmark: LTV:CAC ratio > 3:1, CAC payback < 12 months. Optimization levers: (1) Creative — test 5+ ad variants per platform, kill underperformers after $500 spend, scale winners, (2) Targeting — narrow by job title, company size, industry, intent signals (G2 category page visits, competitor brand searches), use lookalike audiences from your best customers, (3) Landing page CRO — A/B test headline, hero image, CTA copy, form length, social proof placement, (4) Offer — test ebook vs. benchmark report vs. assessment vs. demo. High-intent offers (demo, trial, assessment) produce fewer leads but higher conversion to SQL, (5) Channel mix — shift spend toward channels with lowest CAC and highest LTV, not just lowest CPL. A $200 CPL channel that converts 20% to SQL beats a $50 CPL channel that converts 2%.

<!-- DEEP: 10+min -->

### Phase 5 (~45 min): ABM + Webinar Programs

**ABM (Account-Based Marketing):** Identify 50-500 target accounts (named list, not segments). Tier them: Tier 1 (1:1, 10-50 accounts — personalized gifts, executive outreach, custom content), Tier 2 (1:few, 50-200 accounts — industry-specific content, direct mail, semi-personalized ads), Tier 3 (1:many, 200-500 accounts — programmatic ads, email sequences, personalized landing pages by industry). For each tier: define the account plan (key contacts, engagement plan, content assets, success metrics). Measure: account engagement score, pipeline created from target accounts, deal velocity for ABM-sourced vs. non-ABM, average deal size uplift. Target: ABM accounts should have 2x pipeline velocity and 30% higher ACV than non-ABM.

**Webinar/Virtual Event Playbook:** (1) Topic selection — solve a specific pain, not a product pitch. "How [Role] at [Company Type] Reduced [Metric] by [X]%." (2) Speaker — customer + your expert. Customer stories convert 3x better than vendor-only. (3) Promotion — email to your list 3x: 2 weeks before, 1 week before, day before. LinkedIn ads targeting job title + industry for net-new. Partner co-promotion for reach extension. (4) During — polls every 10 minutes (engagement + data capture), Q&A throughout (not just at end), demo in last 10 minutes only, (5) Post-webinar — send recording + slides within 24 hours. No-show sequence: "We missed you — here's the recording." Attendee sequence: "Thanks for attending — here's the next step" (case study, trial, assessment). Measure: registration rate, attendance rate (>35% is good), on-demand views, pipeline created within 30 days.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -- these rules encode years of wasted ad spend, broken attribution, and nurture sequences that annoyed everyone -->

- UTM hygiene is the foundation of all measurement. Enforce UTM parameters on every outbound link. Use `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` consistently. One missing parameter corrupts attribution for an entire campaign.
- Test ad creative in batches of 5 — kill anything with CTR <0.5% after $500 spend per platform. The best creative often isn't your first guess. Budget 20% of spend for testing.
- Never send identical nurture to everyone who downloads the same asset. Segment by persona, industry, and behavior. A CTO and a marketing manager downloading the same ebook need different follow-up.
- Lead scoring decays over time: a pricing page visit 6 months ago is not the same signal as one yesterday. Apply a 30-day recency decay: score reduces by 50% every 30 days of inactivity.
- MQL→SQL conversion rate <10% means either your scoring model is too generous or sales isn't following up. Audit 50 MQLs: why weren't they accepted or rejected? The answer tells you what to fix.
- Attribution windows matter enormously. A 30-day lookback credits very different channels than a 90-day. Pick one, document it, and don't change it quarter-to-quarter — consistency matters more than precision.
- Email nurture open rates are inflated by Apple Mail Privacy Protection. Look at click rate and conversion rate as primary metrics, not open rate. Open rate is directional at best.
- Holdout groups (10%) on every nurture sequence are non-negotiable. If the nurture doesn't produce statistically significant lift vs. doing nothing, kill it and redirect the effort.
- Use incrementality testing for paid channels: geo-holdout tests (ads in Region A, no ads in comparable Region B) tell you whether paid is creating demand or capturing demand that would have converted organically.
- Marketing automation migrations are more expensive than they appear. Budget 3x the platform cost for implementation, data migration, and training. A rushed migration corrupts data and breaks attribution for months.

## Anti-Patterns
<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Optimizing for lead volume over lead quality — celebrating 500 MQLs while pipeline is flat | Gate content with qualifying form fields (company size, role, timeline). Add open-text "biggest challenge" field. Measure MQL→SQL conversion as primary quality metric. Tighten targeting to ICP criteria. | `grep -rn "Lead Volume\|MQL count\|lead goal\|leads generated" *.xlsx *.csv \| grep -v "pipeline\|SQL\|opportunity\|conversion"` → finds lead-volume dashboards without pipeline correlation | Dashboard template: primary KPI is "Pipeline Revenue Influenced." Lead volume is secondary. Auto-flag if lead volume is rising but pipeline is flat for 2 consecutive months. |
| Running paid ads without UTM enforcement — 80% of pipeline shows as "Direct" or "Other" in attribution | Enforce UTM parameters on every outbound link via a UTM builder tool. Audit active campaign URLs weekly. Add UTMs to CRM automation for retroactive classification. No URL goes live without validated UTMs. | `grep -rn "utm_source" *.csv *.xlsx \| wc -l` → must exceed 90% of campaign URLs. `grep -rn "Direct\|Other\|\(none\)" *.csv -c` → these should be < 10% of pipeline attribution | UTM builder Chrome extension enforced for team. CRM auto-tags "Direct" pipeline with timestamp and landing page for retroactive UTM classification. Weekly audit: URLs without UTMs → auto-email campaign owner. |
| Sending identical nurture sequences to all personas — CTO gets same email as marketing coordinator | Segment nurture by persona, industry, and behavior. The CTO gets technical proof points; the marketing manager gets ROI and efficiency messaging. Different pain points require different follow-up. | `grep -rn "nurture\|Nurture Sequence\|email automation" *.docx *.csv -l \| xargs grep -L "persona\|segment\|industry\|role-based"` → finds nurture plans without persona segmentation | Marketing automation platform: each nurture sequence requires persona assignment before activation. Single-sequence-for-all → gate blocks activation. Audit: if >80% of contacts receive same sequence, auto-flag. |
| Ignoring email deliverability until domain lands in spam — recovery takes months | Monitor bounce rate (<2%), spam complaint rate (<0.1%), and domain reputation weekly. Pause sends and run list verification at first warning sign. Warm up new domains with most-engaged segment over 2-4 weeks. | `grep -rn "bounce rate\|spam complaint\|deliverability\|domain reputation" *.csv *.xlsx \| wc -l` → must return weekly monitoring reports. Zero reports → deliverability is unmonitored | Marketing ops: weekly deliverability report auto-generated. Bounce >2% OR spam >0.1% → auto-pause sends, trigger list verification. Domain warm-up script enforced for new sending domains. |
| Relying on open rates as primary email metric post-Apple MPP — celebrating 40% open rates that are inflated | Use click rate and conversion rate as primary email metrics. Open rate is directional at best. The only metric that matters: did the recipient take the intended action? | `grep -rn "open rate\|Open Rate\|email opens" *.csv *.xlsx -l \| xargs grep -L "click rate\|conversion rate\|CTR\|click-through"` → finds email reports prioritizing opens over clicks | Email dashboard template: click rate and conversion rate are primary columns. Open rate moved to secondary tab with warning: "⚠️ Directional only — inflated by Apple Mail Privacy Protection." |
| Running ABM without sales alignment on follow-up — marketing warms the account, sales ignores the signal | Marketing and sales jointly plan account outreach. Sales commits to 48-hour follow-up SLA on engagement signals. If SLA breached, ABM program pauses until sales capacity is restored. | `grep -rn "ABM\|account-based" *.docx *.pptx -l \| xargs grep -L "SLA\|follow-up\|48 hour\|sales commitment\|sales alignment"` → finds ABM plans without sales SLA | ABM program gate: "Sales SLA Signed" checkbox required before program activation. CRM automation: engagement signal triggers 48-hour countdown. Breach → auto-notify VP Sales + pause program. |
| Changing attribution models mid-year — shifting from first-touch to multi-touch invalidates all trend analysis | Pick one attribution model, document it, and lock it for 12 months. Consistency matters more than precision. Run alternative models side-by-side for internal learning, but plan and budget against the locked model. | `grep -rn "attribution model\|Attribution Model" *.docx *.xlsx \| sort \| uniq` → check if multiple models appear within 12-month period. Different models in same quarter → unstable attribution | Attribution model version-locked in BI tool config. Model change requires VP Marketing + VP RevOps dual approval. Auto-log every model change with timestamp and approver. |
| Treating CRO as one-off A/B tests instead of continuous program — no compounding learning, flat conversion rate | Run continuous CRO: hypothesis backlog → prioritized by potential impact → test → learn → repeat. Each test builds on last. Target 1-2 meaningful tests per month with documented learnings. | `grep -rn "A/B test\|experiment\|variant" *.csv *.xlsx \| wc -l` → count test records in trailing 6 months. < 6 tests → CRO is episodic, not continuous | CRO program template: hypothesis backlog sheet, monthly test calendar, decision log. Auto-flag if <2 tests/month for 3 consecutive months. Test results auto-archived to knowledge base. |


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

## Scale Depth: Solo → Small → Medium → Enterprise
<!-- DEEP: 10+min -- how this skill changes as the company grows -->

### Solo
Founder content + LinkedIn posts, organic outreach. Build awareness, get first leads. Founder is the brand; no budget; content and hustle. Focus on establishing initial market presence through personal networks and low-cost channels.

### Small Team
Paid ads (Google/LinkedIn), email sequences, landing pages. Generate pipeline predictably, prove CAC. First paid channels; basic nurture sequences; lead scoring starts. A dedicated demand gen person or agency runs structured campaigns with measurable ROI.

### Medium Team
Multi-channel ABM, marketing ops stack, attribution. Target ICP precisely, optimize funnel. Account-based plays; HubSpot/Marketo; multi-touch attribution; SDR team. Dedicated specialists per channel with documented playbooks and automated reporting.

### Enterprise
Global demand gen team, multi-region campaigns, brand + demand. Scale pipeline globally, build category. Regional teams; $1M+ campaign budgets; brand awareness + demand capture. ABM at scale across hundreds of accounts with predictive routing and custom attribution models.

### Transition Triggers
- **Solo → Small Team:** Marketing spend exceeds $10K/month and pipeline from paid channels reaches 20% of total pipeline.
- **Small Team → Medium Team:** Marketing-sourced pipeline exceeds $5M/quarter or the company targets named accounts with ABM.
- **Medium Team → Enterprise:** Operating in 3+ regions with $10M+ ARR, or requiring dedicated attribution and ops infrastructure to manage multi-channel complexity.


## What Good Looks Like
<!-- QUICK: 30s -- concrete success description -->

Every paid channel has a documented CAC and LTV:CAC ratio >3:1. MQL→SQL conversion rate >15% and stable quarter-over-quarter. Attribution model is documented (U-shaped, 90-day lookback) and consistently applied across all reports. Email nurture sequences have <0.5% unsubscribe rate and >3% CTR. Landing pages convert >3% from paid traffic. Lead scoring model validated quarterly against actual closed-won data — high-scoring leads convert at >2x the rate of medium-scoring leads. ABM program generates >30% higher ACV than non-ABM. Pipeline dashboard updates daily with no data gaps. Marketing-sourced pipeline consistently hits >40% of total pipeline.

## Error Decoder
<!-- DEEP: 5min -- each entry includes a console-string matcher for automatic recovery loops -->

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `grep -rn "MQL\|Marketing Qualified" *.csv *.xlsx \| awk -F',' '{sum+=$2} END {print sum}'` shows high MQL volume; `grep -rn "SQL\|Sales Qualified\|Opportunity" *.csv \| wc -l` < 10% of MQL count | 500 MQLs generated this quarter. Sales accepted 12. Pipeline from marketing is below target and sales blames marketing for "sending garbage." | Forms are too easy — ebook gates with name + email, no qualification. Target audience is too broad. MQL definition is based on activity (downloaded content) not fit (ICP match). | Add qualifying form fields: company size, role, timeline. Add "biggest challenge" open-text — quality responses = quality leads. Tighten targeting to ICP. Redefine MQL to require both activity AND fit signals. | 1. Audit MQL→SQL conversion by source: `grep "Lead Source" *.csv \| sort \| uniq -c` 2. For sources with <10% conversion: tighten targeting or kill 3. Add BANT-lite form fields: company size, role, timeline 4. Set MQL definition: Activity (content download/event) + Fit (ICP match) = MQL. One without the other = Lead 5. Monthly: if MQL→SQL <15%, auto-escalate to demand gen lead |
| `grep -rn "UTM\|utm_source" *.csv *.xlsx \| wc -l` < 50% of `grep -rn "Direct\|Other\|\(none\)" *.csv \| wc -l` → more pipeline attributed to Direct than to tracked campaigns | CEO asks "which marketing channel drives the most pipeline?" You can't answer because 80% of pipeline is "Direct" or "Other." Attribution is broken and budget allocation is guesswork. | UTM parameters are missing or inconsistent across campaigns. Links in emails, ads, and social posts don't carry tracking. CRM cannot map deals back to campaigns. | Audit all active campaign URLs. Implement UTM builder tool with mandatory fields. Add UTMs to CRM automation. Retroactively classify Direct traffic by timestamp and landing page. Campaigns without valid UTMs are paused until fixed. | 1. Audit: `grep -rn "utm" *.csv \| awk -F',' '{print $NF}' \| sort \| uniq -c` — count URLs with vs without UTMs 2. Build UTM taxonomy document: utm_source, utm_medium, utm_campaign, utm_content as required fields 3. Implement UTM builder tool (Google Sheets template or dedicated tool) 4. Weekly: `scripts/utm-audit.sh` — auto-email campaign owners for URLs missing UTMs 5. CRM: auto-classify "Direct" leads using timestamp + landing page to nearest campaign |
| `grep -rn "CPL\|Cost Per Lead\|cost per lead" *.xlsx \| awk -F',' '{if($2 > 200) print}'` returns campaigns with CPL > $200; `grep -rn "pipeline\|Pipeline Generated" *.csv \| awk -F',' '{if($2 == 0) print}'` shows zero pipeline | LinkedIn CPL is $200+ with zero pipeline to show for it. CFO is asking why marketing is burning cash with no ROI. | Targeting is correct but creative doesn't resonate, OR landing page doesn't match ad promise. Message-match score is low — ad promises one thing, landing page delivers another. | Test ad creative variants. Measure message-match score: does landing page headline repeat ad's promise? Test LinkedIn lead-gen forms (on-platform) vs landing page redirects — forms typically convert 3-5x better. Kill underperforming variants after $500 spend. | 1. Compute message-match score: compare ad headline to landing page H1 using `diff <(echo "$ad_headline") <(echo "$lp_h1")` 2. If < 80% match → rewrite landing page to match ad promise 3. A/B test: form-fill vs landing page redirect 4. Set kill threshold: $500 spend without >1 SQL → pause 5. Weekly: auto-flag campaigns with CPL > 2× channel average |
| `grep -rn "bounce\|Bounce Rate\|spam\|Spam Complaint" *.csv \| awk -F',' '{if($2 > 2) print}'` → bounce > 2%; `grep -rn "deliverability\|domain health\|reputation" *.xlsx \| wc -l` → 0 monitoring reports | Email domain suddenly lands in spam. Open rates drop from 25% to 3% overnight. All nurture sequences are now dead. Recovery will take months. | List hygiene degraded silently — high bounce rate, spam complaints accumulating, or sending to unengaged addresses for too long. Domain reputation tanked and ISPs blacklisted the sending IP. | Immediately pause all sends. Run list through email verification service. Remove addresses with >90 days no engagement. Warm up domain over 2-4 weeks starting with most-engaged segment (opened/clicked in last 30 days). Implement sunset policy for unengaged contacts. | 1. Check: `grep "deliverability" *.csv \| tail -30` — review last 30 days of deliverability metrics 2. If bounce > 2% OR spam > 0.1%: immediate pause 3. Run list verification: `scripts/verify-email-list.sh contact-list.csv` 4. Remove >90-day unengaged + hard bounces 5. Warm-up plan: send to most-engaged 1K contacts day 1, double daily for 14 days 6. Resume normal sends only when reputation score > 90 |
| `grep -rn "attribution\|Attribution Model" *.docx *.xlsx \| sort \| uniq -c \| awk '{if($1>1) print}'` → multiple different attribution models referenced in same quarter | Marketing team reports Campaign X drove $500K. Sales reports Campaign X drove $80K. CFO doesn't trust any marketing numbers. Budget allocation is frozen because nobody agrees on which channel is working. | Different teams are using different attribution models — marketing uses first-touch (gives them credit), sales uses last-touch (gives them credit), finance uses something else. No single source of truth. | Pick one attribution model, document methodology, and lock for 12 months. Recommended: U-shaped attribution with 90-day lookback. Run alternative models side-by-side for learning, but plan and budget against the locked model. All reports must state methodology. | 1. Audit: `grep -rn "attribution\|first.touch\|last.touch\|multi.touch" *.docx *.xlsx` — catalog all models in use 2. Select single model: U-shaped, 90-day lookback as default 3. Configure in BI/CRM: lock model for 12 months 4. Add methodology disclaimer to all pipeline reports 5. Run alt models in separate tab — flagged "For Internal Learning Only — Not for Planning" |

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | UTM parameters enforced on every outbound link — utm_source, utm_medium, utm_campaign, utm_content all present | `grep -rn "utm_source\|utm_medium\|utm_campaign" *.csv *.xlsx \| wc -l` → must be ≥ 90% of total campaign URLs tracked | UTM builder template enforced. Weekly: `scripts/utm-audit.sh` — emails campaign owners for URLs without validated UTMs |
| **[S2]** | Attribution model documented, version-locked for 12 months — U-shaped with 90-day lookback recommended | `grep -rn "attribution model\|Attribution Model\|U-shaped\|first-touch\|multi-touch" *.docx` → must return exactly 1 model + methodology doc | BI tool config: attribution model version-locked. Change requires VP Marketing + VP RevOps dual approval |
| **[S3]** | Lead scoring model defined, implemented in marketing automation, and validated quarterly against closed-won data | `grep -rn "lead scoring\|Lead Scoring\|scoring criteria\|point threshold\|MQL threshold" *.docx *.csv` → must return scoring criteria + quarterly validation report | Quarterly: `scripts/validate-lead-scoring.sh` — correlates scores with closed-won conversion. Auto-flag if correlation < 0.3 |
| **[S4]** | MQL definition signed by sales and marketing leadership — reviewed quarterly for quality drift | `grep -rn "MQL definition\|MQL.*signed\|agreed.*MQL" *.docx *.pdf` → must return signed doc with both signatures | CRM gate: MQL definition document must have "Signed: Sales Leader + Marketing Leader" metadata. Quarterly review calendar invite auto-generated |
| **[S5]** | CAC calculated per channel monthly — LTV:CAC > 3:1, payback period < 12 months | `grep -rn "CAC\|Cost Per Acquisition\|LTV:CAC\|payback period" *.xlsx` → must return per-channel CAC breakdown with LTV:CAC ratio | Monthly: `scripts/compute-cac.sh` pulls spend from ad platforms + pipeline from CRM. Auto-flag channels with LTV:CAC < 2:1 |
| **[S6]** | Pipeline dashboard: leads, MQLs, SQLs, opportunities, pipeline value — updates daily with automated data refresh | `curl -s "https://dashboard.internal/api/pipeline/health" \| jq .last_refresh` → must be < 24 hours ago | Dashboard data pipeline: daily CRM sync. Auto-alert if refresh fails 2 consecutive days |
| **[S7]** | Email nurture sequences have 10% holdout groups — incremental lift measured quarterly for every active sequence | `grep -rn "holdout\|control group\|10%\|incremental lift" *.csv *.xlsx` → must return holdout group definition + lift report per sequence | Marketing automation: holdout group auto-assigned on sequence activation. Quarterly lift report auto-generated. Zero-lift sequences → auto-flag for kill review |
| **[S8]** | Email list hygiene: bounce rate < 2%, spam complaint rate < 0.1%, unsubscribes honored within 24 hours | `grep -rn "bounce\|spam complaint\|unsubscribe" *.csv \| awk -F',' '{if($2>2) print "FAIL"; else print "PASS"}'` → must return PASS for all metrics | Weekly deliverability report auto-generated. Bounce >2% OR spam >0.1% → auto-pause sends, trigger list verification |
| **[S9]** | Ad platform conversion tracking verified — data flowing from Google Ads + LinkedIn to CRM, not just platform-reported metrics | `grep -rn "conversion tracking\|Conversion Tracking\|pixel\|Insight Tag" *.csv *.xlsx` → must show CRM-attributed conversions matching ad platform reports within 20% tolerance | Monthly: `scripts/verify-conversion-tracking.sh` — compares ad platform reported conversions to CRM pipeline. > 20% discrepancy → auto-escalate |
| **[S10]** | Landing pages: load time < 3 seconds mobile (Lighthouse score > 80), forms ≤ 5 fields, message-match score > 80% | `npx lighthouse https://landing.example.com --only-categories=performance --chrome-flags="--headless" \| jq .categories.performance.score` → must return > 0.80 | CI: `lighthouse` in deploy pipeline with performance budget. PageSpeed score < 80 → deploy blocked. Message-match audit script auto-scores ad → landing page coherence |
| **[S11]** | Ad creative testing cadence: ≥ 5 variants active per channel, underperformers killed after $500 spend with no pipeline | `grep -rn "ad variant\|creative test\|ad rotation" *.csv \| awk -F',' '{print NF}'` → must show ≥ 5 active variants per channel | Ad platform automation: launch with 5+ variants. $500 spend trigger: auto-pause variants with 0 SQL pipeline. Weekly: if < 5 active variants → auto-alert to refresh creative |
| **[S12]** | ABM program: named account list published, account engagement scoring active, sales follow-up SLA signed at ≤ 48 hours | `grep -rn "ABM\|named account\|engagement score\|SLA\|follow-up" *.csv *.docx \| wc -l` → must return ≥ 3 artifacts: account list, scoring model, signed SLA | ABM program gate: all 3 artifacts required before activation. CRM: engagement signal triggers 48h countdown. Breach → auto-notify VP Sales + pause program |


## Footguns
<!-- DEEP: 10+min — war stories from demand generation and B2B pipeline -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Built a lead scoring model on "what felt right" — 90% of MQLs were unqualified, and by month 6, sales had permanently tuned out every marketing lead | A Series B SaaS company implemented Marketo lead scoring in Q1 2023. The marketing team assigned points based on intuition: +50 for "visited pricing page," +30 for "attended webinar," +15 for "opened 3 emails." Within 6 months, 90% of MQLs routed to sales were students, competitors, or job seekers — they had visited pricing to research a school project. Sales SDRs started auto-rejecting every MQL. The marketing-to-sales SLA was dead. | Lead scoring was never validated against closed-won data. The team didn't run a regression: "Which behaviors actually correlate with becoming a customer?" Pricing page visits were high-intent for buyers but also for every curious visitor. Webinar attendance was inflated by people who wanted the slide deck for free. | **Build lead scoring from your CRM data, not your imagination.** Export your last 200 closed-won deals and 2,000 closed-lost/disqualified leads. Run a logistic regression: which behaviors (page visits, content downloads, email clicks, demo requests) predict conversion? Weight scores by actual conversion rates. Revalidate quarterly — what predicted purchase in Q1 may not predict purchase in Q4. |
| Attributed 100% of pipeline to "last-click Google Ads" — cut content and events budget, then watched pipeline drop 40% because those channels were the actual source | A demand gen director presented a Q4 2023 attribution report showing Google Ads as 70% of pipeline. The "proof": last-click attribution in HubSpot. Based on this, the CEO cut the content team budget by 60% and canceled all event sponsorships for 2024. Pipeline dropped 40% by May. Investigation revealed that content was the first touch for 55% of deals — prospects read 3 blog posts, then Googled the company name and clicked a branded ad. Last-click gave the ad 100% credit for a journey content started. | Last-click attribution is the cheapest attribution model to implement and the most misleading. It systematically over-credits bottom-of-funnel channels (branded search, retargeting) and under-credits top-of-funnel channels (content, social, events) that create demand. | **Use a multi-touch attribution model (U-shaped or W-shaped) with a minimum 90-day lookback window.** U-shaped gives 40% credit to first touch, 40% to lead conversion touch, and 20% distributed across middle touches. Track "content-influenced pipeline" separately: any deal where the contact viewed ≥1 content piece before becoming an opportunity. Never make budget cuts based on single-touch attribution. |
| Spent $80K on Facebook ads targeting "CTOs at companies with 200-500 employees" — generated 3,000 leads, 0 qualified, because CTOs don't click Facebook ads for enterprise software | A demand gen manager at a DevOps startup convinced the CEO to allocate $80K to Facebook Lead Ads in Q2 2022. The targeting looked great on paper: job title = CTO, company size = 200-500. The campaign generated 3,000 leads at $26/lead — below the $50 target. But 0 leads became opportunities. Analysis revealed the leads were fake profiles using "CTO" as a vanity title, or real CTOs who clicked by accident while scrolling personal feeds. Nobody buys infrastructure software from a Facebook ad. | Platform-channel fit was never tested. The targeting capability existed ("CTO at mid-market company") but the context was wrong — Facebook is a personal social network, not a place where CTOs evaluate $50K/year DevOps tools. LinkedIn would have been the right platform; even then, content syndication or webinar ads would outperform lead gen forms. | **Test each channel with $5K before scaling.** Run a minimum viable campaign: define ICP, test 3 audiences, run for 2 weeks, measure not just leads but MQLs → SQLs → opportunities. If $5K generates 0 pipeline, the channel is wrong — don't spend $75K more "optimizing." Channel-platform fit matters more than creative optimization. A great Facebook ad to the wrong audience still produces zero pipeline. |
| Scaled LinkedIn spend from $15K/month to $90K/month without fixing the landing page — CAC went from $300 to $1,100 because the page had a 1.8% conversion rate | A Series C company hit their LinkedIn ROAS target at $15K/month spend and decided to scale. Over 6 months, they increased LinkedIn spend to $90K/month — 6×. But the landing page conversion rate was 1.8% (benchmark: 4-6% for B2B SaaS). At $15K/month, the 1.8% conversion produced enough pipeline to hit targets. At $90K/month, LinkedIn auction dynamics forced bids higher (same audience, more competition), CPC rose 40%, and the 1.8% conversion rate meant CAC went from $300 to $1,100 — above the $800 LTV:CAC ceiling. | The team optimized ad creative and audience targeting but never A/B tested the landing page. Scaling spend magnifies conversion rate problems — at low spend, a bad conversion rate is hidden; at high spend, it's fatal. The law of shitty click-through: as you scale, your marginal clicks come from less-qualified audiences, so conversion rate naturally drops unless you improve the page. | **Before scaling spend, optimize conversion rate to at least 4% on your primary landing page.** Run A/B tests on: headline (value prop vs pain point), form length (5 fields vs 3 fields vs progressive profiling), social proof placement (above fold vs below), and CTA language ("Get a Demo" vs "See How It Works"). Only scale budget when conversion rate is stable and CAC stays below 1/3 LTV at 3× current spend. |
| Ran a webinar program that generated 800 registrants per session — but 60% were no-shows and 30% of attendees were competitors, producing 4 qualified opportunities in 12 months | A demand gen team ran 18 webinars in 2023 averaging 800 registrations each — impressive numbers for board slides. But post-webinar analysis revealed: 60% no-show rate, 30% of attendees used competitor email domains, and only 4 of 14,400 registrants became opportunities. The team had optimized for registrations (easy to inflate with LinkedIn ads and "free" incentives) instead of pipeline. Total program cost: $180K in ad spend + production. Cost per opportunity: $45,000. | Vanity metrics drove the program. The team's OKR was "webinar registrations," not "webinar-attributed pipeline." The promotion strategy (broad LinkedIn ads + "free whitepaper for registering") attracted freebie-seekers, not buyers. | **Define webinar success as "qualified opportunities created within 30 days," not registrations.** Target promotion to named accounts (ABM) or lookalike audiences of existing customers — not broad job-title targeting. Require work email registration and filter out competitor domains at the form level. Post-webinar: SDRs call every attendee within 4 hours; automated nurture for no-shows. Run a 6-month holdout group to measure true incremental lift. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You report "leads generated" and "cost per lead" to the board — and get defensive when the CRO asks "how many became pipeline?" | You can look at a campaign that's been running for 2 weeks and say "this will produce $X in pipeline by end of quarter" — and be within 20% | You inherit a broken demand gen engine (CAC 3× target, sales ignores MQLs, attribution is single-touch) and within 6 months it's generating pipeline at <12-month CAC payback with multi-touch attribution the CFO trusts |
| You set lead scoring rules based on marketing team brainstorming rather than analyzing which behaviors actually correlate with closed-won deals | You've killed 3 campaigns this year that weren't working — and you made the call before month 2, not after burning 6 months of budget hoping they'd "optimize" | A CEO asks you "should we spend $500K on demand gen or sales headcount?" and you deliver a model with CAC, payback period, and capacity analysis per channel — and 12 months later the actual numbers are within 15% of your projection |
| You can't explain the difference between U-shaped and W-shaped attribution, and your reports use "last-click" because "that's what the tool defaults to" | Every campaign you launch has a holdout group, a pre-registered success metric, and a shut-off threshold — and you've never spent a dollar past the shut-off threshold | You build a demand gen engine at a company pre-revenue, and by month 18 it's generating 60% of new logo pipeline with a documented playbook that a new hire could execute |

**The Litmus Test:** Give a demand gen manager a $50K budget, an ICP, and 90 days. If they come back with >$150K in qualified pipeline AND can show you exactly which channels, campaigns, and audience segments drove it — with holdout group data proving incrementality — they're L3. If they come back with "3,500 leads" but can't trace a single one to pipeline, they're L1 regardless of years of experience.

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
