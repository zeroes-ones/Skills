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
<!-- QUICK: 30s -- pick your path, skip the rest -->

```
What are you trying to do?
├── Launch paid acquisition (Google/LinkedIn/Meta ads) → Go to "Decision Trees > Paid Channel Selection"
├── Build email marketing automation & nurture sequences → Jump to "Core Workflow > Phase 3"
├── Design lead scoring & MQL→SQL handoff → Go to "Decision Trees > Lead Scoring Design"
├── Set up attribution modeling → Jump to "Decision Trees > Attribution Model Selection"
├── Optimize CAC (cost per acquisition) → Go to "Core Workflow > Phase 4"
├── Run landing page CRO → Jump to "Decision Trees > CRO: Funnel Leak Diagnosis"
├── Build an ABM program for enterprise → Go to "Core Workflow > Phase 5"
├── Set up marketing ops (HubSpot/Marketo/Pardot) → Jump to "Core Workflow > Phase 2"
├── Launch a webinar or virtual event program → Go to "Core Workflow > Phase 5 > Webinar Playbook"
├── Need campaign positioning & messaging → Invoke `marketing-manager` skill
├── Need CRO experiments / A/B testing infrastructure → Invoke `growth-engineer` skill
├── Need revenue forecasting / pipeline analytics → Invoke `revops-manager` skill
└── Not sure where to start? → Start at "Core Workflow > Phase 1"
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never spend a dollar on paid acquisition without a tracking plan.** If you can't measure from ad impression → click → landing page → form fill → CRM → closed-won, you're buying vanity metrics, not pipeline. UTM hygiene is non-negotiable.
- **Always define MQL and SQL criteria in writing, signed by sales and marketing leadership.** If both teams disagree on what a "qualified lead" is, the handoff breaks and pipeline numbers are fiction. Revisit quarterly.
- **Never optimize for leads alone — optimize for pipeline and revenue.** 500 MQLs that convert to 3 opportunities is a targeting failure, not a volume success. The North Star is pipeline revenue influenced, not leads generated.
- **Always run holdout tests on email nurture sequences.** If you can't measure incremental lift vs. a control group that receives nothing, you don't know if your nurture is adding value or just annoying people who would have bought anyway.
- **Never report attribution without stating the model and its limitations.** "Campaign X drove $500K" is meaningless without "using a U-shaped attribution model with a 90-day lookback window." Different models produce wildly different numbers. State your methodology.

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

### Phase 1 (~20 min): Pipeline Modeling & Target Setting

Build a reverse funnel from revenue target: Revenue target → Pipeline needed (at close rate X) → SQLs needed (at SQL→Opp rate Y) → MQLs needed (at MQL→SQL rate Z) → Leads needed (at Lead→MQL rate W). Example: $2M quarterly revenue target. Avg deal size $50K = 40 closed deals. Close rate 25% = 160 opportunities. SQL→Opp rate 60% = 267 SQLs. MQL→SQL rate 15% = 1,780 MQLs. Lead→MQL rate 10% = 17,800 leads. Now allocate across channels: organic %, paid %, email %, events %, partner %. Track actuals vs. plan weekly. Reforecast monthly.

### Phase 2 (~60 min): Marketing Operations Setup

Marketing ops is the infrastructure: choose your platform (HubSpot for SMB/mid-market, Marketo for enterprise, Pardot if Salesforce-native required). Set up: (1) Tracking — UTM parameters enforced on every outbound link, form submissions captured with source data, cookie-based tracking for anonymous visitors, first-touch and last-touch fields populated at conversion, (2) Lead lifecycle stages — Visitor → Lead → MQL → SQL → Opportunity → Customer → Evangelist, with automated stage transitions based on scoring and actions, (3) Email automation — nurture sequences triggered by behavior (content download → related nurture track, pricing page visit → sales outreach alert), (4) List hygiene — bounce management, unsubscribe compliance, deduplication, suppression lists, (5) Attribution — U-shaped model as default, campaign influence tracking, ROI dashboards by channel, (6) Reporting — weekly pipeline dashboard: leads by channel, MQL volume, MQL→SQL rate, SQL→Opp rate, pipeline created, CAC by channel, LTV:CAC ratio.

### Phase 3 (~45 min): Email Marketing & Nurture

Design nurture sequences, not email blasts. Architecture: (1) Welcome sequence (3 emails over 7 days) — triggered on first conversion. Email 1: deliver the asset. Email 2: social proof + case study. Email 3: soft CTA (demo, trial, assessment), (2) Behavioral triggers — pricing page visit → case study email within 1 hour, feature page visit → product demo video, high engagement → sales alert, inactivity (30 days no click) → re-engagement drip (subject: "Still interested?"), (3) Newsletter (bi-weekly) — curated content, product updates, customer stories. Segment by persona so CTOs don't get end-user content, (4) Re-engagement — 3-email sequence for dormant leads. Email 1: "We miss you" + value. Email 2: "Last chance" + offer. Email 3: "Confirm you want to stay" — no click = unsubscribe. Always run a 10% holdout group on nurture sequences. Measure: open rate >20%, CTR >3%, unsubscribe <0.5% per send, conversion rate from nurture >5%.

### Phase 4 (~30 min): CAC Optimization

Calculate CAC per channel: total channel spend / customers acquired from that channel (using your chosen attribution model). Benchmark: LTV:CAC ratio > 3:1, CAC payback < 12 months. Optimization levers: (1) Creative — test 5+ ad variants per platform, kill underperformers after $500 spend, scale winners, (2) Targeting — narrow by job title, company size, industry, intent signals (G2 category page visits, competitor brand searches), use lookalike audiences from your best customers, (3) Landing page CRO — A/B test headline, hero image, CTA copy, form length, social proof placement, (4) Offer — test ebook vs. benchmark report vs. assessment vs. demo. High-intent offers (demo, trial, assessment) produce fewer leads but higher conversion to SQL, (5) Channel mix — shift spend toward channels with lowest CAC and highest LTV, not just lowest CPL. A $200 CPL channel that converts 20% to SQL beats a $50 CPL channel that converts 2%.

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

## What Good Looks Like
<!-- QUICK: 30s -- concrete success description -->

Every paid channel has a documented CAC and LTV:CAC ratio >3:1. MQL→SQL conversion rate >15% and stable quarter-over-quarter. Attribution model is documented (U-shaped, 90-day lookback) and consistently applied across all reports. Email nurture sequences have <0.5% unsubscribe rate and >3% CTR. Landing pages convert >3% from paid traffic. Lead scoring model validated quarterly against actual closed-won data — high-scoring leads convert at >2x the rate of medium-scoring leads. ABM program generates >30% higher ACV than non-ABM. Pipeline dashboard updates daily with no data gaps. Marketing-sourced pipeline consistently hits >40% of total pipeline.

## Error Decoder
<!-- DEEP: 10+min -- each row is a real campaign that burned budget without pipeline -->

| Problem | Root Cause | Fix |
|---------|------------|-----|
| High lead volume but near-zero SQL conversion | Forms are too easy (ebook gate, no qualification) or targeting is too broad | Add qualifying form fields (company size, role, timeline). Add a "what's your biggest challenge?" open-text field — quality responses = quality leads. Tighten ad targeting to ICP criteria. |
| LinkedIn CPL is $200+ with no pipeline ROI | Targeting correct but creative doesn't resonate, or landing page doesn't match ad promise | Message-match score: does the landing page headline repeat the ad's headline promise? If not, fix it. Test lead-gen forms (on-LinkedIn) vs. landing page redirects — forms typically convert 3-5x better. |
| Email domain suddenly lands in spam (deliverability crash) | List hygiene degraded — high bounce rate, spam complaints, or sending to unengaged addresses | Immediately pause all sends. Run list through email verification service. Remove addresses with >90 days no engagement. Warm up domain over 2 weeks starting with most-engaged segment. |
| Attribution shows 80% of pipeline from "Direct" or "Other" | UTM parameters missing or inconsistent across campaigns | Audit all active campaign URLs. Implement UTM builder tool for the team. Add UTMs to CRM automation. Retroactively classify where possible using timestamp + landing page data. |
| Webinar registration is high but attendance <20% | Promotion-to-event gap too long or reminder sequence too weak | Shorten registration-to-event window to ≤14 days. Send reminder 1 week, 1 day, 1 hour before. Add calendar invite with "Add to Calendar" link in confirmation email. Offer on-demand within 24 hours for no-shows. |
| ABM program shows engagement but no pipeline after 6 months | Targeting accounts but not the right people within accounts, or no sales alignment on outreach | For each account: identify 5-10 key contacts. Sales and marketing jointly plan outreach. Marketing warms the account, sales opens the conversation. If sales isn't following up within 48 hours of an engagement signal, the program fails. |

### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Prospect goes dark after great demo | No clear next step with owner and timeline | Every demo must end with a specific next step: "If you agree X by Friday, I'll have the PoC ready by next Wednesday." No open-ended "let me know when you're ready." |
| Technical win, commercial loss | Sold to engineering champion who has no budget authority | Always identify the economic buyer by the second meeting. MEDDIC: find the Champion AND Economic Buyer before writing a PoC. Engineers love your product; budget holders love ROI — speak both languages. |
| RFP response rejected on pricing | Didn't uncover budget range before responding | Always ask: "Have you allocated a budget range for this initiative?" before writing a single page. If they won't share a range, the RFP is a price-discovery exercise — bid your standard price, not your best price. |
| POC runs 3 months, no deal | No timeline boundaries or exit criteria set upfront | POC agreement must include: duration (max 30 days), success criteria (3 measurable metrics), and a kill switch ("if criteria not met by day 25, POC ends"). Long POCs kill pipeline velocity. |
| Champion leaves mid-cycle | Only cultivated one internal advocate | Multi-thread from day one. Minimum 3 relationships per account: champion (wants your solution), economic buyer (controls budget), technical evaluator (validates feasibility). If one leaves, you still have coverage. |
| Competitive deal lost on a feature you actually have | Prospect didn't know your product had that capability | Build a competitive battlecard for every RFP. Map every competitor feature claim to your equivalent or better. Train your team quarterly — competitive positioning decays as products evolve. |
| Sales engineer over-engineering the POC | SE builds a production system instead of a proof-of-concept | POC scope: "works with your data, demonstrates the core value, can be thrown away." No custom integrations, no production-grade setup. If prospect asks for production, it's not a POC — it's a paid engagement. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
<!-- DEEP: 10+min -- each item references a standard born from a quarter where pipeline missed target -->

- [ ] **[S1]** UTM parameters enforced on every outbound link — utm_source, utm_medium, utm_campaign, utm_content
- [ ] **[S2]** Attribution model documented and consistently applied — U-shaped with 90-day lookback recommended
- [ ] **[S3]** Lead scoring model defined, implemented, and validated quarterly against closed-won conversion data
- [ ] **[S4]** MQL definition signed by sales and marketing leadership — reviewed quarterly for quality
- [ ] **[S5]** CAC calculated per channel monthly — LTV:CAC >3:1, payback <12 months
- [ ] **[S6]** Pipeline dashboard: leads, MQLs, SQLs, opportunities, pipeline value — updates daily
- [ ] **[S7]** Email nurture sequences have 10% holdout groups — incremental lift measured quarterly
- [ ] **[S8]** Email list hygiene: bounce <2%, spam complaint <0.1%, unsubscribes honored within 24 hours
- [ ] **[S9]** Google Ads + LinkedIn Ads conversion tracking verified — data flowing to CRM, not just ad platform reporting
- [ ] **[S10]** Landing pages: load time <3 seconds mobile, forms ≤5 fields, message-match score >80%
- [ ] **[S11]** Ad creative testing cadence: 5+ variants active per platform, underperformers killed after $500 spend
- [ ] **[S12]** ABM program: named account list, account engagement scoring, sales marketing SLA for follow-up
- [ ] **[S13]** Webinar program: promotion sequence defined, poll+CRO strategy, post-webinar follow-up automated
- [ ] **[S14]** Lead lifecycle stages defined and automated: Visitor → Lead → MQL → SQL → Opportunity → Customer
- [ ] **[S15]** Marketing ops platform data backup verified and GDPR/CAN-SPAM compliance confirmed

## Scale Depth
<!-- QUICK: 30s -- how this skill changes as the company grows -->

| Stage | Scope | Focus | Key Difference |
|-------|-------|-------|----------------|
| **Solo** | Founder content + LinkedIn posts, organic outreach | Build awareness, get first leads | Founder is the brand; no budget; content and hustle |
| **Startup** | Paid ads (Google/LinkedIn), email sequences, landing pages | Generate pipeline predictably, prove CAC | First paid channels; basic nurture sequences; lead scoring starts |
| **Scale-up** | Multi-channel ABM, marketing ops stack, attribution | Target ICP precisely, optimize funnel | Account-based plays; HubSpot/Marketo; multi-touch attribution; SDR team |
| **Enterprise** | Global demand gen team, multi-region campaigns, brand + demand | Scale pipeline globally, build category | Regional teams; $1M+ campaign budgets; brand awareness + demand capture |

## References

- **marketing-manager** — for campaign briefs, positioning, personas, messaging, and competitive intel
- **analytics-engineer** — for attribution modeling, data pipelines, event taxonomy, and dashboards
- **sales-engineer** — for MQL quality feedback, lead handoff process, and conversion optimization
- **growth-engineer** — for A/B testing infrastructure, CRO experiments, and landing page optimization
- **content-strategist** — for content assets, nurture sequence copy, and offer development
- **business-strategist** — for CAC targets, LTV models, budget planning, and revenue forecasting
- **seo-specialist** — for organic/content synergy, keyword-driven paid campaigns, paid-organic balance
- _Obviously Awesome_ by April Dunford — for positioning-informed campaign design
- HubSpot Academy (free certs: Inbound Marketing, Email Marketing, Marketing Automation)
- Google Ads Certification & LinkedIn Marketing Labs — for platform-specific best practices
