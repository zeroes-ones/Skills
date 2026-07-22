---
name: marketing-manager
description: Product marketing, positioning, messaging, competitive analysis, launch management, buyer persona development, sales enablement (battle cards, pitch decks), analyst relations (Gartner, Forrester),
  pricing & packaging strategy, campaign briefs, brand-to-demand connection.
author: Sandeep Kumar Penchala
type: sales
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- marketing-manager
- product-marketing
- pmm
token_budget: 3900
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - bizdev-manager
  - business-strategist
  - content-strategist
  - demand-generation
  - devrel-advocate
  - growth-engineer
  - partnerships-manager
  - product-marketing-manager
  - product-strategist
  - revops-manager
  - seo-specialist
  feeds_into:
  - bizdev-manager
  - brand-guidelines
  - demand-generation
  - product-marketing-manager
  - revops-manager
  - sales-engineer
  alternatives:
  - growth-engineer
---
# Marketing Manager (Product Marketing Manager / PMM)

Own product positioning, messaging, and go-to-market launches. Translate product capabilities into buyer-relevant narratives, arm sales with battle cards and pitch decks, manage analyst relations, and ensure every campaign starts from differentiated positioning — not generic category claims.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

```
What are you trying to do?
├── Position a new product or feature → Jump to "Core Workflow > Phase 1: Positioning & Messaging"
├── Plan a product launch → Go to "Core Workflow > Phase 2: Launch Management"
├── Build sales enablement materials → Jump to "Core Workflow > Phase 3: Sales Enablement"
├── Run competitive analysis → Go to "Decision Trees > Competitive Analysis Type"
├── Develop buyer personas → Jump to "Decision Trees > Persona Development"
├── Set pricing & packaging → Go to "Decision Trees > Pricing & Packaging Strategy"
├── Manage analyst relations → Jump to "Core Workflow > Phase 5: Analyst Relations"
├── Write a campaign brief → Go to "Core Workflow > Phase 4: Campaign Brief"
├── Need campaign execution across paid channels → Invoke `demand-generation` skill
├── Need partnership deal structure / JBP → Invoke `bizdev-manager` skill
├── Need product roadmap for launch timing → Invoke `product-strategist` skill
├── Need content assets for campaigns → Invoke `content-strategist` skill
├── Need product-level launch execution → Invoke `product-marketing-manager` skill
└── Not sure where to start? → Start at "Core Workflow > Phase 1"
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never write positioning without a differentiated insight.** If your message could appear on a competitor's website with the logo swapped, it's not positioning — it's category description. Every positioning statement must pass the "logo swap test."
- **Always anchor pricing to value delivered, not cost-plus.** Your cost to build has zero relationship to what a buyer will pay. Pricing communicates value. Underpricing is as damaging as overpricing — it signals "we don't believe in our value either."
- **Never launch without a "why now" narrative.** A launch without urgency is a press release nobody reads. "New feature X" is not news. "New feature X because [market shift / customer pain that just became acute]" is news.
- **Always validate messaging with actual buyers before scaling.** Your internal team is not your target audience. Test positioning with 5-10 real prospects or customers. If they don't lean forward, iterate.
- **Admit when you lack competitive intel.** Analyst reports, win/loss data, and primary competitive research are prerequisites. If you don't have them, say so and specify what to collect first.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->

- A product or feature needs positioning, messaging, and a go-to-market launch plan
- Sales team is losing deals and needs updated battle cards, pitch decks, and competitive rebuttals
- The company needs a pricing and packaging review — current model isn't capturing value
- A Gartner Magic Quadrant or Forrester Wave evaluation is approaching — need analyst briefing prep
- Buyer personas are stale or based on assumptions — need research-driven persona refresh
- A new market segment or vertical is being entered — need segment-specific positioning
- Brand awareness is strong but demand isn't converting — need brand-to-demand connection strategy
- Competitor just raised $50M or launched a major feature — need competitive response strategy

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Competitive Analysis Type

```
                              ┌──────────────────────────────┐
                              │ START: What competitive       │
                              │ analysis do you need?         │
                              └────────────┬─────────────────┘
                                           │
                         ┌─────────────────▼─────────────────┐
                         │ What is the purpose?              │
                         └────┬──────────────┬───────────────┘
                              │              │
                    ┌─────────▼──────┐  ┌────▼──────────────┐
                    │ Sales/Deal use │  │ Strategic/Product  │
                    │ (battle cards, │  │ (roadmap,          │
                    │ objection      │  │ positioning,       │
                    │ handling)      │  │ market entry)      │
                    └────┬───────────┘  └────┬───────────────┘
                         │                   │
              ┌──────────▼──────┐   ┌────────▼──────────────┐
              │ Competitive     │   │ Full Competitive       │
              │ Battle Card     │   │ Landscape Analysis    │
              │ Format:         │   │ Format:               │
              │ • Their strength│   │ • Market share est.   │
              │ • Their weakness│   │ • Feature comparison  │
              │ • Our positioning│  │ • G2/Capterra analysis│
              │ • Trap questions │   │ • Win/loss patterns  │
              │ • Proof points  │   │ • Pricing comparison  │
              │ • Customer      │   │ • Strategic           │
              │   evidence      │   │   recommendations     │
              └─────────────────┘   └───────────────────────┘
```
**Battle Card use:** AE is going into a deal where Competitor X is named. They need: "Here's what they'll say. Here's how you respond. Here's the trap question to ask."

**Landscape Analysis use:** You're entering a new market, launching a new product, or preparing for an analyst briefing. You need: "Here's everyone in the space, where they play, where we win, where we don't."

### Persona Development

```
                              ┌──────────────────────────────┐
                              │ START: New persona needed?    │
                              └────────────┬─────────────────┘
                                           │
                         ┌─────────────────▼─────────────────┐
                         │ Do you have primary research       │
                         │ (10+ interviews with this role)?   │
                         └────┬──────────────────────────┬───┘
                              │ NO                        │ YES
                              ▼                           ▼
                      ┌──────────────┐          ┌──────────────────────┐
                      │ STOP.        │          │ Build persona:        │
                      │ Commission   │          │ 1. Day-in-the-life    │
                      │ 10-15        │          │    narrative          │
                      │ customer/    │          │ 2. Goals & metrics    │
                      │ prospect     │          │    they're measured on│
                      │ interviews   │          │ 3. Pain points ranked │
                      │ before       │          │    by severity        │
                      │ building.    │          │ 4. Buying triggers    │
                      │ Assumptions  │          │ 5. Information sources│
                      │ become       │          │ 6. Objections they    │
                      │ stereotypes. │          │    raise              │
                      └──────────────┘          │ 7. Preferred channels │
                                                │ 8. "Jobs to be done"  │
                                                └──────────────────────┘
```
**Research before personas:** Never build personas from internal assumptions. Interview 10-15 people in the target role. Ask: "Walk me through yesterday. What was your biggest frustration? How are you measured? What did you research last? Who do you ask for advice on purchases like this?"

**Valid persona:** "VP of Engineering at 200-500 person SaaS company. Measured on: velocity, uptime, cost. Pain: developer onboarding takes 6 weeks. Trigger: board mandated 30% faster time-to-market. Reads: Hacker News, Stratechery, CTO Craft newsletter. Objection: 'We could build this internally.'"

### Pricing & Packaging Strategy

```
                              ┌──────────────────────────────┐
                              │ START: New pricing strategy?  │
                              └────────────┬─────────────────┘
                                           │
                         ┌─────────────────▼─────────────────┐
                         │ What's the primary purchase unit? │
                         └────┬──────────────┬───────────────┘
                              │              │
                   ┌──────────▼────┐  ┌──────▼────────────┐
                   │ User/Seat     │  │ Usage/Volume      │
                   │ based         │  │ based             │
                   └──────┬────────┘  └──────┬────────────┘
                          │                  │
               ┌──────────▼──────┐  ┌────────▼────────────┐
               │ 1. Per-seat +   │  │ 1. Freemium tier    │
               │    platform fee │  │    (free up to X)   │
               │ 2. Tiered seats │  │ 2. Good-Better-Best │
               │    (Pro/Ent)    │  │    tiers by volume  │
               │ 3. Feature-based│  │ 3. Overage charges  │
               │    upsells      │  │    or auto-upgrade  │
               └─────────────────┘  └─────────────────────┘
```
**Pricing validation checklist:**
- [ ] Van Westendorp Price Sensitivity Meter survey with 100+ target buyers
- [ ] Competitive pricing indexed — are you premium, parity, or discount?
- [ ] Unit economics verified: CAC payback < 12 months at target price point
- [ ] Willingness-to-pay interview: "At what price would you consider this too expensive? Too cheap?"
- [ ] 3-tier pricing (Good-Better-Best) with a "most popular" anchor
- [ ] Annual discount ≥ 15% vs monthly — incentivize commitment
- [ ] Enterprise tier with "Contact Sales" — price opacity for $50K+ deals

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->

<!-- DEEP: 10+min -->

### Phase 1 (~45 min): Positioning & Messaging

Positioning is the single sentence that defines who you're for, what you do, and why you're different. Start with the positioning template: "For [target buyer] who [pain/need], [Product] is the [category] that [key benefit/differentiator]. Unlike [competitors], we [unique advantage]." Test it against the logo-swap test. Then build the messaging house: (1) Umbrella value prop — one sentence, (2) 3 Pillars — each pillar has a headline, 2-3 proof points, and a customer story, (3) Tagline — memorable, 5-7 words, (4) Boilerplate — 100-word company description. Validate with 5-10 target buyers: "In your own words, what does this company do?" If they can't articulate it clearly, iterate. Document the final messaging in a single source of truth — the messaging document that every team references.

<!-- DEEP: 10+min -->

### Phase 2 (~90 min): Launch Management

Define the launch tier: Tier 1 (company-defining — all hands, major PR, analyst tour, customer event), Tier 2 (significant feature — blog, email, social, sales enablement), Tier 3 (minor update — changelog, in-app notification). Build a launch plan with: (1) Launch narrative & key messages, (2) Target audience segments with channel plan, (3) Asset checklist: blog post, press release, pitch deck update, battle card update, demo update, website update, social posts, customer email, (4) Timeline with owner per asset and dependencies called out, (5) Internal comms: Slack announcement, all-hands slot, sales training session, (6) Success metrics: awareness (press mentions, social reach), engagement (blog views, demo requests), pipeline ($ influenced within 30/60/90 days). Hold a launch readiness review 1 week before: every asset reviewed, every owner confirmed, every dependency green. Post-launch retro within 2 weeks: what worked, what didn't, pipeline impact.

<!-- DEEP: 10+min -->

### Phase 3 (~30 min): Sales Enablement

Sales enablement means: when an AE opens their laptop Monday morning, they have everything they need to sell effectively. Build and maintain: (1) Pitch deck — 10-12 slides max, problem-forward not product-forward, 1 data point per slide, strong close with CTA, (2) Battle cards — 1 per competitor, updated quarterly, format: their strengths (be honest), their weaknesses (with evidence), our positioning (reframe, don't trash), trap questions to ask, trap questions they'll ask, customer evidence (logos, quotes, case study links), (3) One-pagers — 1 per use case or vertical, hook at top, 3 bullets on value, customer logo row, CTA, (4) Discovery questions — 10 questions per buyer persona to uncover pain, (5) ROI calculator — simple inputs, credible outputs, vetted by finance, (6) Competitive displacement kit — for when competitor is the incumbent: migration guide, TCO comparison, "why switch" deck. Train sales: 30-minute lunch-and-learn on every new asset. Record it. Track asset usage: what's being opened, what's gathering digital dust.

<!-- DEEP: 10+min -->

### Phase 4 (~30 min): Campaign Brief

Write campaign briefs that demand generation can execute without back-and-forth. Structure: (1) Campaign objective — one sentence. "Generate 200 MQLs in financial services segment within 90 days." (2) Target audience — specific persona, segment, pain trigger. (3) Core message — the one thing we want them to remember. (4) Offer — what value are we providing in exchange for their attention/contact info? (5) Channel mix — which channels, why, budget allocation per channel. (6) Asset requirements — what needs to be built (landing page, ebook, webinar, ads, email sequences). (7) Success metrics — MQL target, MQL→SQL conversion target, pipeline target, CAC target. (8) Timeline — launch date, campaign duration, key milestones. (9) Handoff checklist — what demand gen needs from you before they can start. Review the brief with the demand generation lead before locking it. A bad brief creates 3 rounds of revision and a delayed launch.

<!-- DEEP: 10+min -->

### Phase 5 (~45 min): Analyst Relations

Analyst relations (AR) is a long game, not a deal-sprint. Strategy: (1) Identify the 2-3 analyst firms that matter for your category (Gartner, Forrester, IDC — but also category-specific analysts). (2) Build relationships with the analysts who cover your space — quarterly check-ins, not just evaluation-time panic. Share roadmap directionally, customer wins, market observations. (3) For Magic Quadrant / Forrester Wave evaluations: start 6 months before the research cycle begins. Align your product roadmap messaging to the evaluation criteria. Brief the analyst on your vision, not just your features. Submit responses that are concise, evidence-backed, and customer-validated. (4) Customer references for analysts: hand-pick 3-5 reference customers who will say you're strategic, not tactical. Prepare them with a briefing doc. (5) Post-evaluation: regardless of placement, publish a response. If you placed well, amplify. If not, acknowledge the feedback and share your plan. Analysts reward transparency. Track: analyst mentions, report placements, inquiry volume, and deal influence from analyst references.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -- these rules encode years of positioning failures, launch disasters, and analyst snubs -->

- Run the "logo swap test" on every positioning statement: if a competitor can say the same thing by swapping their name for yours, rewrite it. Differentiated positioning is irreplaceable.
- Every launch asset must have one owner and one deadline. Co-ownership means no ownership. Track on a single spreadsheet or project board visible to all stakeholders.
- Never build a battle card without win/loss data. Your opinion of why you win is likely wrong. Interview 5 won deals and 5 lost deals against each competitor. The patterns will surprise you.
- Pricing changes that increase revenue per customer by >15% need a 90-day communication runway. Surprise price increases trigger churn. Grandfather existing customers for 12 months minimum.
- Analyst briefings are presentations to a jury, not a product demo. Lead with market vision, customer evidence, and momentum. Product features come last. Analysts evaluate your strategy, not your UI.
- Segment your messaging by persona but maintain a single brand voice. A CTO and a VP of Sales should both recognize the same company — they just hear different parts of the story.
- The "why now" of a launch is more important than the "what." Every launch must answer: "Why should anyone care about this today?" If you can't answer it, it's not ready to launch.
- Maintain a swipe file of competitor marketing — their homepage, pricing page, latest blog posts, job listings (hiring patterns reveal strategy). Review monthly. You'll spot shifts before they happen.
- Use the "messaging house" framework consistently: Umbrella → Pillars → Proof Points. If a message doesn't ladder up to a pillar, it's clutter. Cut it.
- Campaign briefs that are approved in one review cycle save 2 weeks of launch delay. Invest time in the brief — it's the blueprint demand gen follows. Ambiguity in the brief = waste in execution.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Product Manager** | Feature launches, roadmap alignment, competitive gaps | Product capabilities, roadmap timeline, beta customer access, feature priorities |
| **Business Strategist** | Market entry, pricing strategy, GTM planning | TAM/SAM/SOM data, business model, revenue targets, market segmentation |
| **Demand Generation** | Campaign execution, paid media, lead gen programs | Campaign briefs, target audience, messaging, asset requirements, MQL targets. **Decision gate:** Does campaign messaging pass logo-swap test? → launch ready. **Artifact:** campaign brief with positioning framework. |
| **Content Strategist** | Content marketing assets, blog, ebooks, webinars | Messaging framework, buyer personas, campaign themes, SEO keywords. **Decision gate:** Does content map to a specific buyer journey stage? → publish. **Artifact:** content calendar with persona-to-asset mapping. |
| **Sales Engineer** | Battle cards, demo narratives, competitive positioning | Win/loss data, technical differentiators, customer evidence, objection patterns. **Decision gate:** Is battle card updated within 2 weeks of competitor launch? → sales-ready. **Artifact:** battle card + demo narrative script. |
| **UX Researcher** | Persona research, messaging validation, buyer behavior | Research findings, persona insights, buyer journey mapping |
| **CEO Strategist** | Company positioning, major launches, pricing changes | Strategic narrative, investor messaging, company-level positioning |
| **Growth Engineer** | Messaging A/B tests, landing page CRO, conversion optimization | Variant messaging, hypothesis, experiment results, conversion data |
| **BizDev Manager** | Co-marketing agreements, partner GTM campaigns | Partner positioning, co-branding guidelines, joint campaign briefs. **Decision gate:** Is partner brand compatible (no conflicting positioning)? → co-market. **Artifact:** co-marketing agreement + joint campaign plan. |
| **Product Strategist** | Product vision, market category definition, competitive landscape | Category-level positioning, buy-vs-build analysis, market timing. **Decision gate:** Is the product in an existing category or creating a new one? → positioning strategy diverges. **Artifact:** category analysis + positioning recommendation. |
| **Product Marketing Manager** | Product-level launch execution, feature-level messaging | Feature briefs, launch checklists, sales enablement for specific products. **Decision gate:** Is product-level messaging derivative of company positioning? → aligned. **Artifact:** product launch kit (messaging, battle cards, demo assets). |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Competitor raises $50M+ or launches major feature that threatens positioning | CEO Strategist, Product Manager, Sales Engineer | Competitive response strategy; messaging update within 1 week |
| Launch asset misses deadline that cascades into launch delay | All launch stakeholders, VP of Marketing | Launch date recalibration; expectation reset |
| Messaging tests poorly with target buyers (<30% comprehension or recall) | Product Manager, Content Strategist, Demand Generation | Stop campaign spend; fix messaging before scaling |
| Pricing change causes >5% churn in the first 60 days | CEO Strategist, Product Manager, Customer Success | Pricing rollback or adjustment; customer retention intervention |
| Analyst evaluation places company lower than expected | CEO Strategist, VP Sales, Product Manager | Response strategy; factual error check; customer reference mobilization |

### Escalation Path

```
Positioning/GTM strategic conflict → CEO Strategist + VP Product. Decision within 1 week.
Competitive threat requiring repositioning → CEO Strategist + VP Sales + Product Manager. Response within 2 weeks.
Pricing change with >$1M revenue impact → CEO Strategist + CFO. Board visibility required.
Analyst evaluation outcome materially negative → CEO Strategist + VP Product + Board. Formal response within 48 hours.
```

### Cross-skills Integration

```bash
# Chain: product-manager → marketing-manager → demand-generation
# New feature launch: PM defines feature → PMM positions, builds launch assets → Demand gen executes campaign

# Chain: business-strategist → marketing-manager → content-strategist
# Market entry: Business strategist defines GTM → PMM builds segment positioning → Content strategist creates assets

# Chain: marketing-manager → sales-engineer
# Sales enablement: PMM builds battle cards & pitch decks → SE uses in demos and provides feedback loop
```

## Scale Depth: Solo → Small → Medium → Enterprise
<!-- DEEP: 10+min -- how this skill changes as the company grows -->

### Solo
Founder does marketing — content, social, website. Build the brand from zero, find PMF messaging. No dedicated marketer; scrappy experiments; founder is the voice. Focus on learning which channels and messages resonate with the earliest customers.

### Small Team
Generalist marketer covers all channels, first campaigns. Establish marketing function, build pipeline. One person does content, email, social, events, and product marketing. Every campaign teaches something about the ICP and the channels that work.

### Medium Team
Specialist team (content, demand gen, product marketing, brand). Deepen each function, build scalable programs. Each channel has a dedicated owner; marketing ops formalized. Consistent messaging enforced across all touchpoints with documented playbooks.

### Enterprise
CMO + departments, multi-region, brand governance. Category leadership, global consistency. Marketing org of 50+; brand guidelines enforced globally; $5M+ budgets. Regional teams with localized messaging that still fits the global brand narrative.

### Transition Triggers
- **Solo → Small Team:** Marketing spend exceeds $5K/month or pipeline from marketing activities reaches 15% of total pipeline and can no longer be managed as a side job.
- **Small Team → Medium Team:** Marketing team exceeds 3 people and channel volume requires dedicated owners per function.
- **Medium Team → Enterprise:** Operating in 3+ regions or $50M+ ARR requires dedicated brand governance and regional marketing leadership.


## What Good Looks Like
<!-- QUICK: 30s -- concrete success description -->

Positioning passes the logo-swap test — no competitor can say the same thing. Messaging validated with 10+ target buyers with >80% comprehension and recall. Launch plan has one owner per asset, clear deadlines, and ships on time. Battle cards updated within 2 weeks of any competitor launch. Pricing validated with Van Westendorp survey (n > 100) and CAC payback < 12 months. Analyst briefings result in improved report placement or at minimum, factual accuracy. Campaign briefs approved in one review cycle. Sales team can articulate the positioning and top 3 differentiators without looking at a slide.

## Error Decoder
<!-- DEEP: 10+min -- each row is a real-world positioning or launch failure pattern -->

| Symptom | Root Cause | Fix | Lesson |
|---------|------------|-----|--------|
|---------|------------|-----|
| Launch generates zero pipeline after 30 days | Launch was a feature announcement, not a buyer-relevant narrative | Rewrite launch as "why now" + "what's in it for you." Add a compelling offer (assessment, trial, benchmark report) — pure announcements have 0% conversion. | A launch without a "why now" is a press release nobody reads. Every launch must answer "Why should anyone care about this today?" with urgency that drives action. |
| Sales team doesn't use the battle cards you built | Battle cards are too long or too generic — sales needs deal-time speed, not marketing essays | Rebuild as 1-pagers: 5 bullet points of "they say/you say," 3 trap questions, 1 kill line. Test with 3 AEs. If they don't use it spontaneously after 1 week, it's wrong. | Sales enablement assets that sit unused are worse than nonexistent — they wasted the time it took to build them. Test with 3 AEs before scaling. If they don't use it naturally, it's wrong. |
| Pricing page gets traffic but conversion is flat | Pricing doesn't communicate value differentiation — it's a commodity comparison | Add ROI content above the fold on the pricing page. Include "Why customers choose us at this price" section. A/B test showing value before price vs price first. | Pricing communicates value. If your pricing page lists features and prices without connecting them to outcomes, you're running a commodity comparison — and losing to whoever is cheapest. |
| Analyst report places you lower than expected despite feature parity | You briefed features, not strategy and vision. Analysts score vision and execution — features are table stakes. | Re-brief leading with market vision, customer momentum (logos, growth rate, NPS), and 12-month roadmap. Schedule quarterly touchpoints — not just evaluation-time panic. | Analyst briefings are not product demos — they are strategy presentations. Analysts evaluate your market vision and execution, not your feature list. Treat them as a jury, not an audience. |
| Messaging tests well internally but fails with buyers | Internal team is too close to the product — they fill gaps with product knowledge buyers don't have | Test with cold prospects, not existing customers. Their blank-slate reaction is what your website visitors experience. If they don't get it in 5 seconds, rewrite. | Your team knows too much to evaluate your own messaging. The blank-slate reaction of a cold prospect is the only test that matters. If they can't articulate what you do in 5 seconds, the message fails. |
| Competitor messaging shift blindsides your team | No competitive monitoring cadence — you're reacting to public launches, not anticipating them | Track competitor job listings (hiring patterns), pricing page changes (archive.org), and leadership blog posts monthly. Their strategy is visible 6 months before their launch. | Competitor strategy is visible 6 months before their launch — hiring patterns, pricing page changes, and job listings reveal everything. Monthly monitoring turns surprises into anticipated moves. |



## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
<!-- DEEP: 10+min -- each item references a standard born from a launch that went wrong -->

- [ ] **[S1]** Positioning statement passes the logo-swap test — no competitor can say the same thing
- [ ] **[S2]** Messaging validated with 10+ target buyers — >80% comprehension and recall
- [ ] **[S3]** Buyer personas built from primary research (10+ interviews), not internal assumptions
- [ ] **[S4]** Competitive battle cards exist for top 3 competitors — updated quarterly with win/loss data
- [ ] **[S5]** Pricing validated with Van Westendorp survey (n > 100) and CAC payback < 12 months
- [ ] **[S6]** Launch plan template includes: narrative, audience, asset checklist, timeline with owners, success metrics
- [ ] **[S7]** Every launch has a "why now" narrative — pure feature announcements are blocked
- [ ] **[S8]** Sales pitch deck is ≤12 slides, problem-forward, with 1 data point per slide
- [ ] **[S9]** ROI calculator is built, vetted by finance, and available to all AEs and SEs
- [ ] **[S10]** Analyst relations: quarterly touchpoints with top 3 analyst firms covering your category
- [ ] **[S11]** Campaign brief template includes: objective, audience, message, offer, channels, metrics, timeline
- [ ] **[S12]** Competitor monitoring cadence: monthly review of competitor website, pricing, job listings
- [ ] **[S13]** Message house documented in a single source of truth — every team references it
- [ ] **[S14]** Launch post-mortem completed within 2 weeks of every Tier 1 or Tier 2 launch
- [ ] **[S15]** Sales enablement asset usage tracked monthly — unused assets retired or rebuilt


## References

## References

- **product-manager** — for feature roadmap, capabilities, beta access, and competitive feature gaps
- **business-strategist** — for market analysis, GTM strategy, TAM/SAM/SOM, and pricing modeling
- **demand-generation** — for campaign execution, channel strategy, paid media, and lead generation
- **content-strategist** — for content marketing, blog, ebooks, webinars, and SEO-aligned messaging
- **sales-engineer** — for battle card validation, demo alignment, competitive positioning feedback
- **ux-researcher** — for buyer persona research, messaging validation studies, and buyer journey mapping
- _Obviously Awesome_ by April Dunford — for positioning methodology and the logo-swap test
- _Play Bigger_ by Al Ramadan et al. — for category design and market creation strategy
- _The Challenger Customer_ by Brent Adamson et al. — for B2B buying group dynamics and persona strategy
