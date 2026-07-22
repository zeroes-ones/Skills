---
name: product-marketing-manager
description: >-
  Product marketing management for digital health and health tech companies — launch management with T1/T2/T3 tiering, launch checklists, cross-functional coordination, and post-launch retrospectives; competitive positioning with competitive matrices, win/loss analysis, battle cards, and differentiation strategy for health tech; clinical value propositions with outcomes-based messaging, clinical evidence integration, provider/HCP messaging, and patient-facing positioning; patient segment targeting with persona-based messaging for newly diagnosed, chronic management, caregiver, and pediatric parent segments at each journey stage; healthcare professional (HCP) messaging covering clinical workflow value, EHR integration benefits, outcomes data, and CME-eligible education; pharma partnership positioning with real-world evidence value propositions, patient recruitment messaging, and data partnership narratives; sales enablement including pitch decks, one-pagers, competitive battle cards, objection handling guides, and ROI calculators; product messaging architecture with core narrative, key messages by audience, proof points, and messaging hierarchy; market intelligence covering win/loss interviews, competitive monitoring, and analyst relations (Gartner, KLAS). Use when planning a health tech product launch, defining competitive positioning, creating clinical value propositions, enabling sales with health-focused collateral, or building product messaging architecture for regulated healthcare markets.
author: Sandeep Kumar Penchala
type: creative
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - product-marketing
  - go-to-market
  - clinical-value-proposition
  - healthcare-messaging
  - competitive-positioning
  - launch-management
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
chain:
  consumes_from:
    - product-strategist
    - marketing-manager
    - business-strategist
  feeds_into:
    - sales-engineer
    - demand-generation
    - content-strategist
---
# Product Marketing Manager (Health Tech PMM)

Bridge product and market — translate clinical capabilities into compelling value propositions, position health products against competitors with evidence, equip sales with clinical proof, and orchestrate launches that resonate with patients, providers, and payers alike.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

What are you trying to do?
├── Plan a product launch → Jump to "Core Workflow > Phase 1: Product Launches"
├── Build competitive positioning → Jump to "Core Workflow > Phase 2: Competitive Positioning"
├── Create a clinical value proposition → Jump to "Core Workflow > Phase 3: Clinical Value Propositions"
├── Target specific patient segments → Go to "Core Workflow > Phase 4: Patient Segment Targeting"
├── Message to healthcare professionals → Jump to "Core Workflow > Phase 5: HCP Messaging"
├── Position for pharma partnerships → Jump to "Core Workflow > Phase 6: Pharma Partnership Positioning"
├── Build sales enablement materials → Go to "Core Workflow > Phase 7: Sales Enablement"
├── Define messaging architecture → Jump to "Core Workflow > Phase 8: Messaging Architecture"
├── Gather market intelligence → Jump to "Core Workflow > Phase 9: Market Intelligence"
└── Don't know where to start? → Run "Core Workflow > Phase 1"

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never make clinical claims without evidence.** Every claim about patient outcomes, clinical efficacy, or health improvements must cite specific evidence: "Our digital therapeutic improved HbA1c by 1.2 points in a 500-patient RCT (NEJM, 2024)." Never: "Our product improves health outcomes."
- **Never position against competitors without documentation.** Battle cards and competitive matrices must cite public sources, win/loss interview data, or analyst reports. Never claim "competitor X can't do Y" without verifying the current state of their product.
- **Never promise ROI without a model.** Healthcare ROI claims require transparent calculation methodology. "Customers typically see 3:1 ROI within 18 months based on reduced readmission rates and staff time savings" with a linked calculator that shows the math. Never: "You'll save millions."
- **Always segment messaging by audience.** The same clinical evidence must be narrated differently for a chief medical officer (outcomes, workflow impact), a practice manager (reimbursement, efficiency), and a patient (quality of life, ease of use). One-size-fits-all messaging doesn't work in healthcare.
- **Always build launch tiers with explicit criteria.** Not every feature release is a T1 launch. Define T1/T2/T3 by: market impact, competitive urgency, revenue potential, sales readiness, and cross-functional dependencies.
- **Admit what you don't know.** If a question requires specific market data (TAM for a niche therapeutic area, competitor win rates in a specific region), say so and prescribe the research needed to get the answer.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Planning a product launch for a health tech product (T1/T2/T3 tiering, checklist, retro)
- Building a competitive matrix and differentiation strategy in the healthcare market
- Crafting clinical value propositions with outcomes-based messaging
- Creating persona-based messaging for different patient segments and journey stages
- Developing HCP-facing messaging about clinical workflow, EHR integration, and outcomes
- Positioning for pharma partnerships with real-world evidence and patient recruitment narratives
- Building sales enablement collateral: pitch decks, one-pagers, battle cards, objection handlers
- Defining product messaging architecture with core narrative, key messages, and proof points
- Running win/loss analysis and monitoring competitive landscape

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Launch Tier Decision Tree

```
Scope of change?
├── New product category or major platform release → T1 Launch
│   ├── Full launch plan: PR, analyst briefings, sales training, customer event, demand gen campaign
│   └── Timeline: 8-12 weeks prep, 4-week sustain
├── Major new feature or new market entry → T2 Launch
│   ├── Targeted launch: press release, sales enablement, webinar, targeted demand gen
│   └── Timeline: 4-6 weeks prep, 2-week sustain
├── Feature enhancement or integration → T3 Launch
│   ├── Light launch: blog post, sales update, email to existing customers, social
│   └── Timeline: 1-2 weeks prep, 1-week sustain
└── Bug fix or minor update → No launch. Release notes only.
```

### Competitive Response Decision Tree

```
Competitor announced [feature/claim]?
├── Is it directly comparable to our offering?
│   ├── YES → Does it claim superiority over us?
│   │   ├── YES → Fast-track battle card update + sales enablement within 48 hours
│   │   └── NO → Monitor. Update competitive matrix within 1 week.
│   └── NO → No immediate action. Note for quarterly competitive review.
└── Is it a new market entrant?
    ├── YES → Complete competitive analysis within 2 weeks. Brief leadership.
    └── NO → Categorize for quarterly review.
```

**What good looks like:** A sales rep opens the battle card in a prospect meeting and finds the exact objection handler they need in under 10 seconds. A provider reads your value proposition and nods — it speaks directly to their workflow pain. An analyst at Gartner or KLAS cites your positioning accurately in their report. A competitor's launch triggers your response playbook, and sales has updated materials within 48 hours.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~25 min): Product Launches

Orchestrate launches that coordinate product, sales, marketing, and clinical teams.

1. **Launch tiers**:
   - **T1 (Platform/Category)**: New product category, major platform release, FDA clearance/approval. Full orchestration: PR, analyst briefings, sales training, customer event, demand gen campaign, thought leadership. 8-12 week prep.
   - **T2 (Major Feature/Market)**: Significant new feature, entry into new market segment, integration with major partner. Targeted plan: press release, sales enablement deck, webinar, targeted demand gen. 4-6 week prep.
   - **T3 (Feature/Update)**: Feature enhancement, new integration, minor market expansion. Light plan: blog post, sales one-pager update, email to customers, social. 1-2 week prep.
2. **Launch checklist**: Messaging locked (2 weeks before), sales trained (1 week before), demand gen assets ready (1 week before), PR/AR briefed (3 days before), support team ready (launch day), monitoring dashboard live (launch day), post-launch retro scheduled (2 weeks after).
3. **Cross-functional coordination**: Product (feature freeze date, known issues), Engineering (deployment schedule, rollback plan), Sales (training, comp plan alignment), CS (support docs, escalation path), Clinical (evidence package, KOL briefings), Regulatory (claims review, disclaimer approval), Legal (terms updates, privacy review).
4. **Post-launch retrospective**: What worked (keep), what didn't (fix), what we'd do differently (learn). Metrics: pipeline generated, win rate change, NPS impact, support ticket volume, analyst coverage.

### Phase 2 (~25 min): Competitive Positioning

Build defensible differentiation based on evidence, not opinion.

1. **Competitive matrix**: Map competitors on axes that matter to buyers. For health tech: clinical evidence strength, EHR integration depth, regulatory clearances, data security certifications, workflow impact, total cost of ownership, implementation time, customer satisfaction (KLAS rating).
2. **Win/loss analysis**: Interview every won and lost deal. Standardize: why they were looking, who they evaluated, why they chose (us/them), what almost lost/won it. Aggregate quarterly. Feed insights to product, sales, and marketing.
3. **Battle cards**: One card per competitor. Sections: competitor overview (1 line), their strengths (be honest), their weaknesses (be specific), our differentiation (evidence-backed), objection handlers (3-5 per competitor), trap-setting questions (3-5 to ask prospects), win stories (2-3 named or anonymous).
4. **Differentiation strategy for health tech**: Lead with clinical outcomes when you have peer-reviewed evidence. Lead with workflow efficiency when clinical parity. Lead with patient experience when both are parity. Never lead with "we're cheaper" in healthcare — that signals lower quality.
5. **Positioning statement formula**: For [target healthcare audience] who [pain point], [product name] is the [category] that [primary benefit]. Unlike [competitor alternative], we [unique differentiator] as demonstrated by [evidence].

### Phase 3 (~25 min): Clinical Value Propositions

Translate clinical capabilities into messages that drive decisions.

1. **Outcomes-based messaging**: Lead with the clinical outcome, not the feature. "Reduce 30-day readmissions by 40%" not "Automated discharge planning module." Every outcome claim needs a citation: internal study, published RCT, customer case study, or analyst report.
2. **Clinical evidence integration**: Tier your evidence:
   - **Gold**: Peer-reviewed RCT published in top-tier journal
   - **Silver**: Peer-reviewed study, real-world evidence analysis
   - **Bronze**: Customer case study with named institution
   - **Supporting**: Internal analysis, white paper, KOL endorsement
   - Never use "studies show" without naming the study.
3. **Provider/HCP messaging**: Focus on clinical workflow. "See the full patient picture in one screen — labs, meds, notes, and our AI risk score — without leaving your EHR." Time savings, decision support, documentation burden reduction. Avoid "innovative" — providers hear this as "unproven."
4. **Patient-facing positioning**: Focus on quality of life and ease. "Spend less time managing your condition and more time living." Emphasize safety ("your data is protected"), simplicity ("set up in 5 minutes"), and support ("real clinicians available 24/7").
5. **Payer/employer positioning**: Focus on cost and population health. "Average $4,200 savings per enrolled member per year through reduced ER visits and hospitalizations." ROI model required.

### Phase 4 (~20 min): Patient Segment Targeting

Meet patients where they are — in their diagnosis, their journey, and their life.

1. **Persona-based messaging**:
   - **Newly diagnosed**: Address fear and uncertainty. "You just found out you have [condition]. Here's what to expect — and how we help." Educational, reassuring, not overwhelming.
   - **Chronic management**: Address fatigue and routine. "Managing [condition] is a marathon, not a sprint. We help you stay on track without it taking over your life." Practical, encouraging, habit-building.
   - **Caregiver**: Address burden and vigilance. "Caring for someone with [condition] is demanding. We help you coordinate care, track symptoms, and stay informed — so you can focus on being there." Supportive, practical.
   - **Pediatric parent**: Address anxiety and advocacy. "Watching your child manage [condition] is hard. We help you track what matters, communicate with their care team, and make informed decisions." Empowering, thorough.
2. **Journey-stage messaging**:
   - **Awareness**: "There's a better way to manage [condition]." Educational content, condition-specific.
   - **Consideration**: "See how [product] helps people like you." Case studies, testimonials, comparison tools.
   - **Decision**: "Start improving your [outcome] in [timeframe]." Trial, demo, ROI calculator.
   - **Onboarding**: "You're all set. Here's your first step." Guided setup, quick win.
   - **Advocacy**: "Share your story. Help others like you." Referral, review, community.

### Phase 5 (~20 min): Healthcare Professional (HCP) Messaging

Speak the language of clinicians — evidence, workflow, outcomes.

1. **Clinical workflow value**: Quantify time impact. "Our AI-assisted documentation reduces charting time by 35% — that's 90 minutes back in your day." Map to specific EHR workflows (Epic, Cerner, Meditech). Name the integration points.
2. **EHR integration benefits**: "Bi-directional sync with Epic means patient data flows automatically. No double entry. No missing information." List specific EHRs and integration depth (FHIR API, SMART on FHIR, embedded app, SSO).
3. **Outcomes data**: Show before/after with statistical significance. "Practices using [product] saw a 28% reduction in HbA1c non-control rates (p < 0.001, n=12,000 patients across 47 practices)." Peer-reviewed citation required.
4. **CME-eligible education**: Position product training as continuing education. "Earn 2.0 CME credits while learning how [product] fits into your clinical workflow." Partner with accredited CME providers.
5. **Clinical decision support positioning**: "Our CDS is assistive, not directive. You make the final call — we surface the relevant data, guidelines, and risk scores." Never position AI as replacing clinical judgment.

### Phase 6 (~20 min): Pharma Partnership Positioning

Position your health tech product as a strategic asset for pharmaceutical partners.

1. **Real-world evidence (RWE) value prop**: "Generate real-world data on treatment patterns, adherence, and outcomes across 50,000+ patients in therapeutic area X. Accelerate your Phase IV and post-market surveillance requirements."
2. **Patient recruitment messaging**: "Identify and engage eligible patients for your clinical trials from our community of [N] patients with [condition]. Typical time-to-first-enrollment reduced by 40%."
3. **Data partnership narratives**: "Co-develop digital biomarkers for early detection of [condition]. Our longitudinal dataset spans [X] years, [Y] million data points, across [Z] diverse patient populations." Be explicit about data rights, privacy, and patient consent.
4. **Therapy companion app positioning**: "Extend the value of your therapy beyond the pill. Our digital companion improves adherence by [X]% and captures patient-reported outcomes between visits."
5. **Compliance guardrails**: All pharma messaging must comply with FDA guidance on drug promotion, PhRMA Code, and Sunshine Act reporting. Flag all pharma-facing content for legal/regulatory review.

### Phase 7 (~20 min): Sales Enablement

Arm sales teams with the content, evidence, and tools to win healthcare deals.

1. **Pitch deck**: Problem slide (the clinical/business pain) → Solution slide (how we solve it) → Evidence slide (proof it works) → Differentiation slide (why us) → ROI slide (the math) → Call to action. 10 slides max. Customizable per persona (provider, payer, pharma, employer).
2. **One-pagers**: One per product per audience. Front: value proposition, key outcomes, differentiators. Back: evidence summary, customer logos, implementation overview. Must be leave-behind quality.
3. **Competitive battle cards**: Phase 2 output. Format: one competitor per card, 2-page max, updated quarterly at minimum. Fast-track update within 48 hours of competitive announcement.
4. **Objection handling guides**: Top 20 objections per product. Each: objection as stated by prospect → what's behind it (real concern) → response framework → evidence to support. "It's too expensive" → "We understand budget pressure. Customers typically see payback in [X] months. Here's a calculator we can walk through together."
5. **ROI calculators**: Interactive tool. Input: practice size, patient volume, current readmission rate, current staff hours. Output: projected savings, time reclaimed, payback period. All assumptions documented and adjustable. Must pass clinical and financial review.
6. **Customer proof library**: 5-10 named case studies with measurable outcomes. 3-5 video testimonials. 10+ quotes organized by persona and use case. Always get customer approval before using in sales.

### Phase 8 (~20 min): Product Messaging Architecture

Build the hierarchy that keeps every communication on-message.

1. **Core narrative**: The one-paragraph story of why your product exists. "For the 34 million Americans managing diabetes, the gap between doctor visits is where health is won or lost. [Product] bridges that gap with continuous glucose monitoring, AI-powered insights, and real-time care team access — turning the 8,760 hours between annual checkups into a continuous care experience."
2. **Key messages by audience**:
   - Patients: "Take control of your health — on your terms."
   - Providers: "Practice at the top of your license with AI that handles the routine."
   - Payers: "Bend the cost curve with proven population health outcomes."
   - Pharma: "Accelerate evidence generation with real-world data at scale."
3. **Proof points**: 3-5 per key message. Each: claim → evidence → source → recency. "Reduce readmissions (claim): 40% reduction in 30-day all-cause readmissions (evidence): published in JAMA Internal Medicine, 2024 (source), confirmed in follow-up 2025 study (recency)."
4. **Messaging hierarchy**: Core narrative (1 paragraph) → Platform messages (3-5) → Product messages (per product) → Feature messages (per key feature) → Proof points. Every level must ladder up to the one above. No orphan messages.
5. **Message testing**: Test key messages with each audience. Measure: recall (can they repeat it?), relevance (does it speak to their problem?), differentiation (do they see us as unique?), credibility (do they believe it?).

### Phase 9 (~20 min): Market Intelligence

Know the market better than anyone else.

1. **Win/loss interviews**: Monthly cadence. Interview both won and lost deals within 2 weeks of decision. Standard question set. Aggregate findings quarterly. Share anonymized insights with product, sales, and exec leadership.
2. **Competitive monitoring**: Track competitor product updates, funding announcements, leadership changes, pricing changes, customer wins/losses, analyst mentions, patent filings. Weekly digest for leadership, monthly deep-dive for product marketing.
3. **Analyst relations (Gartner, KLAS)**:
   - **Gartner**: For payer/employer/enterprise health IT. Maintain vendor briefing cadence (annual minimum). Respond to Magic Quadrant and Market Guide surveys. Provide customer references.
   - **KLAS**: For provider-facing health IT. Encourage customer participation in KLAS surveys. Respond to KLAS reports. Address negative findings publicly and transparently.
   - **Other**: Forrester (digital health), Chilmark (clinical AI), CB Insights (startup coverage).
4. **Conference intelligence**: HIMSS, HLTH, CHIME, J.P. Morgan Healthcare. Track competitor presence, messaging, and announcements. Debrief within 1 week.
5. **Advisory board insights**: Customer advisory board feedback, KOL perspectives, clinical advisory panel input. Document and share with product and strategy teams.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->

Product marketing is the connective tissue between product, sales, and market. Know when to coordinate:

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Product Strategist** | Launch planning, market entry, pricing | Product vision, roadmap timing, strategic priorities, market sizing |
| **Marketing Manager** | Campaign planning, brand alignment | Positioning framework, messaging hierarchy, campaign briefs, brand guidelines |
| **Business Strategist** | Market entry, partnership strategy, pricing | TAM/SAM/SOM, unit economics, channel strategy, partnership rationale |
| **Sales Engineer** | Battle cards, demos, objection handling | Product capabilities, technical differentiation, demo scripts, competitive differentiators |
| **Demand Generation** | Campaign execution, lead nurturing | Target personas, key messages, content assets, campaign themes, conversion goals |
| **Content Strategist** | Content marketing, thought leadership | Messaging architecture, proof points, customer stories, content calendar inputs |
| **CEO Strategist** | Company narrative, market positioning | Corporate strategy, fundraising narrative, board presentation support |
| **Product Manager** | Feature launches, roadmap communication | Feature value props, release timing, beta program opportunities, customer feedback |
| **UX Researcher** | Persona development, message testing | Segment insights, pain points, journey maps, message comprehension results |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Competitor launches directly competing feature | Product Strategist, Sales Engineer, CEO Strategist | Strategic response, sales enablement update |
| Win/loss trend shift (>10% change) | Product Manager, Business Strategist, Sales Engineer | Product gaps or messaging failures |
| Analyst report mentions us (positive or negative) | CEO Strategist, Marketing Manager, Product Strategist | Market perception impact |
| Major customer win or loss | Sales Engineer, CEO Strategist, Product Strategist | Proof point or churn signal |
| Launch readiness gate (2 weeks before) | All cross-functional leads | Go/no-go decision |
| New clinical evidence published | Content Strategist, Sales Engineer, Demand Generation | Messaging refresh, content creation |
| Regulatory clearance received | CEO Strategist, Marketing Manager, Legal Advisor | Claims expansion, launch acceleration |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Lead with outcomes, not features**: Healthcare buyers care about results. Every message should answer: "What happens for the patient/provider after they use this?"
- **Anchor differentiation in evidence**: In healthcare, "unique" without proof is noise. Every differentiator needs a citation.
- **Segment messaging ruthlessly**: The CMO of a health system and the parent of a child with asthma speak different languages. Same product, different story.
- **Update competitive intelligence continuously**: Healthcare moves fast — M&A, new entrants, regulatory changes. Quarterly battle card updates are the minimum.
- **Train sales on the "why," not just the "what"**: Anyone can read a feature list. Sales needs to understand the clinical rationale so they can handle any objection.
- **Respect regulatory boundaries**: Never claim what your clearance doesn't cover. FDA 510(k) clearance for "blood glucose monitoring" does not authorize "diabetes treatment" claims.

## MVP vs Growth vs Scale

| Concern | MVP (Pre-launch) | Growth (Post-launch) | Scale (Market Leader) |
|---------|-----------------|----------------------|----------------------|
| Launches | One T1 launch plan | T1/T2 cadence | Multi-product launch calendar |
| Competitive | 5-competitor matrix, 3 battle cards | Win/loss program, 10+ battle cards | Competitive intelligence function |
| Proof points | Customer case studies (2-3) | Published evidence, KOL endorsements | Peer-reviewed RCTs, KLAS ranking |
| Messaging | Core narrative + 3 key messages | Full messaging hierarchy | Multi-audience, multi-product architecture |
| Sales enablement | Pitch deck, one-pager | Battle cards, ROI calculator, objection guides | Continuous enablement, certification |
| Market intel | Analyst briefing (annual) | Win/loss monthly, competitive weekly | Dedicated CI analyst, conference coverage |
| Segments | 1-2 patient personas | 4-5 personas with journey mapping | Dynamic personalization, predictive targeting |
| Pharma positioning | Initial partnership narrative | RWE value prop, patient recruitment deck | Co-development proposals, data licensing |

## When NOT to Product Market

```
Pre-PMF product with < 10 customers? → Founder does PMM. Learn from early customers directly.
Single buyer persona (e.g., only D2C patients)? → Demand generation covers enough. PMM overhead not justified.
Launching a minor feature update? → Product manager writes the blog post. PMM focuses on T2+ launches.
No clinical differentiation? → Focus on product differentiation first. PMM amplifies, doesn't create.
```

### Cross-skills Integration

This skill in a typical workflow chain:

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | product-strategist | Product vision, PMF assessment, competitive landscape, pricing strategy, roadmap |
| **Before** | marketing-manager | Brand positioning, campaign strategy, budget allocation, channel mix |
| **Before** | business-strategist | Market entry strategy, TAM analysis, partnership framework, revenue model |
| **This** | product-marketing-manager | Launch plans, competitive positioning, clinical value props, messaging architecture, sales enablement |
| **After** | sales-engineer | Receives battle cards, pitch decks, objection handlers — translates into demos and POCs |
| **After** | demand-generation | Receives target personas, key messages, content assets — executes campaigns |
| **After** | content-strategist | Receives messaging hierarchy, proof points, customer stories — creates content calendar |

Common chains:
- **Strategy to market**: product-strategist → product-marketing-manager → demand-generation — Strategy → positioning → campaigns
- **Product to sales**: product-manager → product-marketing-manager → sales-engineer — Features → messaging → enablement
- **Evidence to narrative**: clinical-informatics-specialist → product-marketing-manager → content-strategist — Clinical data → value prop → thought leadership
- **Launch orchestration**: product-strategist + marketing-manager → product-marketing-manager → sales-engineer + demand-generation + content-strategist

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `launch-management` | Planning T1/T2/T3 launches | Phase 1 |
| `competitive-positioning` | Building competitive matrices, battle cards | Phase 2 |
| `clinical-value-props` | Crafting outcomes-based messaging | Phase 3 |
| `patient-segmentation` | Persona-based messaging | Phase 4 |
| `hcp-messaging` | Provider-facing communication | Phase 5 |
| `pharma-partnerships` | Positioning for pharma collaborations | Phase 6 |
| `sales-enablement` | Building pitch decks, one-pagers, ROI tools | Phase 7 |
| `messaging-architecture` | Defining messaging hierarchy | Phase 8 |
| `market-intelligence` | Win/loss, competitive monitoring, analyst relations | Phase 9 |

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 PMM, pre-launch startup)
- **What changes**: You do everything. Core narrative + pitch deck + 3 battle cards. Launch = blog post + sales email. Win/loss = you do the calls. No analyst relations yet.
- **What to skip**: Launch tiers (everything is T1 when you're launching your first product), formal win/loss program, analyst relations, dedicated CI, ROI calculator (use a spreadsheet).
- **Coordination**: Weekly founder sync. Monthly customer interview debrief.

### Small Team (2-3 PMMs, 1-3 products)
- **What changes**: Launch tiers emerge. Competitive matrix for 5-10 competitors. Formal win/loss monthly. Analyst briefing annual. ROI calculator built. 2-3 persona segments. Sales enablement = pitch deck + one-pagers + battle cards.
- **What to skip**: Full messaging hierarchy (core narrative + key messages is enough), continuous CI monitoring (quarterly is fine), dedicated pharma positioning.
- **Coordination**: Weekly product marketing sync. Monthly competitive review. Quarterly analyst prep.

### Medium Team (4-10 PMMs, multi-product portfolio)
- **What changes**: Product marketing function with specialization (competitive, analyst, enablement, pharma). Full messaging hierarchy. Continuous CI. Formal win/loss program with external interviewer. Gartner + KLAS engagement. Multi-audience messaging architecture. ROI calculator per product. Sales certification program.
- **What to skip**: AI-assisted CI (manual at this scale), real-time messaging personalization.
- **Coordination**: Weekly product marketing team meeting. Bi-weekly sales enablement review. Monthly competitive deep-dive. Quarterly analyst roadshow.

### Enterprise (10+ PMMs, global product lines)
- **What changes**: Dedicated PMM per product line. CI team with AI monitoring. Analyst relations function. Global launch coordination across regions. Sales enablement platform with certification. Dynamic messaging personalization. Pharma partnership team. Conference intelligence function.
- **What's full production**: PMM ops. Messaging automation. Continuous message testing. Board-level competitive reports. Global launch calendar management.
- **Coordination**: Daily CI briefing. Weekly global launch sync. Bi-weekly sales enablement council. Monthly executive competitive briefing. Quarterly board market update.

### Transition Triggers
- **Solo → Small**: Second product launch, >$2M ARR, first competitor targets you directly
- **Small → Medium**: >5 products, >$10M ARR, enterprise sales motion, first analyst coverage
- **Medium → Enterprise**: Global markets, >$50M ARR, public company analyst scrutiny, pharma partnership deals

### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Sales ignores battle cards | Cards are too long, outdated, or not trusted | Cut to 2 pages, update within 48 hours of competitive change, co-create with top reps |
| Launch falls flat (low pipeline) | Messaging not tested, sales not trained, demand gen not aligned | Test key messages with target audience pre-launch, mandate sales training completion, align campaigns to launch timing |
| Win rate declining | Competitive gap opened, messaging stale, or market shifted | Run urgent win/loss analysis (last 20 deals), update battle cards, refresh messaging with new evidence |
| Analyst report misrepresents product | Insufficient briefing, wrong analyst contacted, no evidence package provided | Schedule corrective briefing, provide evidence package with citations, offer customer references |
| Pharma partners disengage | Value prop too generic, no RWE to share, compliance concerns | Build specific RWE dataset proposal, engage regulatory early, create co-development narrative with mutual KPIs |
| Messaging inconsistency across channels | No messaging hierarchy, no review process, content teams working in silos | Build and socialize messaging architecture, implement message review gate, hold quarterly messaging alignment session |

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->

- [ ] **[PM1]** Launch tier (T1/T2/T3) assigned with documented rationale
- [ ] **[PM2]** Launch checklist completed with cross-functional sign-off from Product, Sales, CS, Clinical, Regulatory
- [ ] **[PM3]** Post-launch retrospective scheduled and metrics baseline captured
- [ ] **[PM4]** Competitive matrix built for top 5+ competitors with evidence citations
- [ ] **[PM5]** Battle cards updated within last quarter with verified claims
- [ ] **[PM6]** Clinical value proposition cites specific evidence (study name, journal, year, outcome)
- [ ] **[PM7]** Core narrative + key messages defined for each target audience (patients, providers, payers, pharma)
- [ ] **[PM8]** Messaging hierarchy documented: core narrative → platform → product → feature → proof points
- [ ] **[PM9]** Patient personas defined with journey-stage messaging for each
- [ ] **[PM10]** Sales enablement package complete: pitch deck, one-pagers, battle cards, objection guide, ROI calculator
- [ ] **[PM11]** Win/loss program running with monthly interviews and quarterly aggregate reporting
- [ ] **[PM12]** Competitive monitoring cadence established with weekly digest for leadership
- [ ] **[PM13]** Analyst relations maintained: annual Gartner/KLAS briefing, responsive to report inquiries
- [ ] **[PM14]** All marketing claims reviewed by Legal and Regulatory; clinical claims validated by Clinical team

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Obviously Awesome](https://www.amazon.com/dp/1999023005) — April Dunford (positioning)
- [Product Marketing Misunderstood](https://www.amazon.com/dp/0578768082) — Richard King
- [Crossing the Chasm](https://www.amazon.com/dp/0062292986) — Geoffrey Moore
- [Made to Stick](https://www.amazon.com/dp/1400064287) — Chip & Dan Heath (messaging)
- [Loved](https://www.amazon.com/dp/1119704598) — Martina Lauchengco (product marketing)
- [Gartner Digital Health Research](https://www.gartner.com/en/industries/healthcare) — Gartner
- [KLAS Research](https://klasresearch.com/) — KLAS (healthcare IT rankings)
- [Chilmark Research](https://www.chilmarkresearch.com/) — Healthcare AI and analytics
- [Product Marketing Alliance](https://www.productmarketingalliance.com/) — PMM resources and certification
