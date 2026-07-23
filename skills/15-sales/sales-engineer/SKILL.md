---
name: sales-engineer
description: Technical demos, proof-of-concept design, RFP responses, technical qualification with MEDDIC/BANT/SPICED frameworks, competitive positioning, objection handling, demo environment management,
  and technical win rate optimization. Use when preparing technical sales engagements.
author: Sandeep Kumar Penchala
type: sales
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- sales-engineer
- solutions-engineer
- presales
token_budget: 3800
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - backend-developer
  - bizdev-manager
  - demand-generation
  - marketing-manager
  - partnerships-manager
  - product-manager
  - product-marketing-manager
  - revops-manager
  feeds_into:
  - account-manager
  - customer-success-manager
  - product-manager
  - revops-manager
  alternatives:
  - bizdev-manager
---
# Sales Engineer (Solutions Engineer / Presales)

Own the technical side of the sales cycle: discover with MEDDIC/BANT/SPICED, design proofs-of-concept that close, deliver demos that map to pain, write RFP responses that score, and build demo environments that never fail during a call.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

```
What are you trying to do?
├── Prepare a technical demo → Jump to "Core Workflow > Phase 3: Demo Design"
├── Design a proof-of-concept (PoC) → Go to "Decision Trees > PoC Design Decision"
├── Respond to an RFP/RFI → Jump to "Core Workflow > Phase 4: RFP Response"
├── Qualify a deal technically → Go to "Decision Trees > Discovery Framework Selection"
├── Handle a competitive objection → Jump to "Decision Trees > Competitive Objection Handling"
├── Build or maintain a demo environment → Go to "Core Workflow > Phase 2: Demo Env Management"
├── Position against a competitor → Start at "Core Workflow > Phase 5"
├── Need product roadmap / feature scoping → Invoke `product-manager` skill
├── Need custom integration / API development → Invoke `backend-developer` skill
├── Need deal structure / partnership model → Invoke `bizdev-manager` skill
├── Need revenue analytics / pipeline metrics → Invoke `revops-manager` skill
└── Not sure where to start? → Start at "Core Workflow > Phase 1: Discovery"
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never demo a feature you haven't personally walked through in the last 24 hours.** Stale demos lose deals. If something broke overnight, find it before the prospect does.
- **Always tie every feature shown to a pain point discovered in discovery.** Demo without pain mapping is a feature tour — prospects forget it within 24 hours. Say: "You mentioned [pain X]. Here's how we solve that. Let me show you."
- **Never answer a question you don't know the answer to during a live interaction.** Say: "That's a great question. Let me verify with engineering and I'll have a detailed answer by end of day tomorrow." Then actually follow up. Guessing kills credibility.
- **Always qualify out before qualifying in.** A bad-fit deal in pipeline wastes SE cycles, inflates forecast, and damages the relationship with the AE when it eventually falls through. Use BANT or MEDDIC — and mean it.
- **Never trash competitors.** Say: "[Competitor] is strong in [area]. Our customers typically choose us when [differentiator] is critical." Prospects respect honesty; they smell fear.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->

- An AE has a qualified opportunity and needs a technical demo to advance to the next stage
- A prospect requests a proof-of-concept with specific success criteria before committing
- An RFP lands with 150+ questions and a 5-day deadline — needs technical sections filled
- A competitor is named in a deal and the AE needs a positioning/objection-handling playbook
- The demo environment is unreliable — blank screens, stale data, broken integrations during calls
- Technical win rate is below 30% — need to diagnose where in the cycle deals are lost
- A new product feature needs to be translated into a demo narrative with discovery questions

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Discovery Framework Selection: MEDDIC vs BANT vs SPICED

```
                              ┌──────────────────────────────────┐
                              │ START: Which discovery framework? │
                              └────────────────┬─────────────────┘
                                               │
                         ┌─────────────────────▼─────────────────────┐
                         │ What's the ACV range?                     │
                         └────┬──────────────┬──────────────┬────────┘
                              │ <$10K ACV   │ $10K-100K   │ >$100K ACV
                              ▼             ▼              ▼
                      ┌───────────┐  ┌────────────┐  ┌───────────────┐
                      │ BANT      │  │ SPICED     │  │ MEDDIC        │
                      │ Budget    │  │ Situation  │  │ Metrics       │
                      │ Authority │  │ Pain       │  │ Economic Buyer│
                      │ Need      │  │ Impact     │  │ Decision Crit │
                      │ Timeline  │  │ Champion   │  │ Decision Proc │
                      │           │  │ Economic   │  │ Identify Pain  │
                      │           │  │ Decision   │  │ Champion       │
                      └───────────┘  └────────────┘  └───────────────┘
```
**BANT** — Transactional deals, SMB. Gateway check: does this deal have budget, authority, need, and timeline? 5-minute qualification.

**SPICED** — Mid-market ($10K-100K ACV). Focuses on champion building and economic buyer identification. Ask: "Who else needs to see the value of this?"

**MEDDIC** — Enterprise ($100K+ ACV). Deep discovery across 6 axes. Each letter is a gate: if you can't score 4+ on MEDDIC, the deal is at risk. Track MEDDIC score in the CRM after every call.

### MEDDIC Qualification Scoring

```
For each MEDDIC element, score 0-3 (0 = unknown/absent, 3 = strongly present):

M - Metrics: Can the prospect quantify the pain? e.g., "We lose $15K/week on manual reconciliation."
    3 = Specific dollar/time impact quantified
    2 = Directional pain acknowledged
    1 = Vague "we need to be better"
    0 = "Everything is fine" → Not a real deal

E - Economic Buyer: Do you have access to the person with budget authority?
    3 = Met EB, they're actively engaged
    2 = EB identified, meeting scheduled
    1 = EB identified, no meeting
    0 = No idea who signs checks → High risk

D - Decision Criteria: Do you know the formal and informal criteria?
    3 = Formal RFP/evaluation matrix shared, we know weightings
    2 = Some criteria known, gaps remain
    1 = Vague "we evaluate on best value"
    0 = No criteria shared → Flying blind

D - Decision Process: Do you know the steps, who's involved, and timeline?
    3 = Documented process with dates and names: "Legal review (2 weeks), then security (1 week), then VP approval, PO by March 15."
    2 = Process known but timeline vague
    1 = "We'll figure it out"
    0 = No process shared → Deal stall risk

I - Identify Pain: Is the pain acute and tied to a business outcome?
    3 = Pain is costing money/revenue/reputation — executive mandate to fix
    2 = Pain acknowledged but competing priorities
    1 = Nice-to-have
    0 = No pain → Not a real opportunity

C - Champion: Do you have an internal advocate with influence who will fight for you?
    3 = Champion is actively selling internally; has slides + ROI built
    2 = Champion is bought in but hasn't mobilized others
    1 = Contact is friendly but passive
    0 = No champion → Someone else's deal
```

**Go/No-Go Threshold:** Score < 12 → Do not commit SE cycles beyond initial discovery. Score 12-14 → Engage with caution; focus on improving weak MEDDIC elements. Score 15-18 → Full engagement; green-lit for PoC/demo investment.

### PoC Design Decision

```
                              ┌──────────────────────────────┐
                              │ START: Prospect requests PoC  │
                              └────────────┬─────────────────┘
                                           │
                         ┌─────────────────▼─────────────────┐
                         │ Is the PoC solving a real pain    │
                         │ (not just "show us it works")?    │
                         └────┬──────────────────────────┬───┘
                              │ NO                        │ YES
                              ▼                           ▼
                      ┌──────────────┐          ┌──────────────────────┐
                      │ Decline PoC. │          │ Can you scope it to   │
                      │ Offer         │          │ < 2 weeks of effort? │
                      │ reference     │          └──┬──────────────┬────┘
                      │ calls and     │             │ YES          │ NO
                      │ recorded demo │             ▼              ▼
                      └──────────────┘    ┌──────────────┐ ┌──────────────┐
                                          │ Scoped PoC   │ │ Not a PoC —  │
                                          │ with success │ │ this is       │
                                          │ criteria,    │ │ implementation│
                                          │ timeline,    │ │ consulting.   │
                                          │ mutual       │ │ Scope as a    │
                                          │ success plan │ │ paid pilot or │
                                          │              │ │ walk away.    │
                                          └──────────────┘ └──────────────┘
```
**When to do a PoC:** Clear success criteria defined, < 2 weeks effort, deal size justifies investment (>5:1 return), champion identified, and mutual success plan signed by both sides.

**When to refuse a PoC:** No success criteria, scope creep risk ("we'll figure it out as we go"), no champion, deal ACV < 5× SE cost, or the PoC is being used to beat up the incumbent for a better price.

### Competitive Objection Handling

```
                              ┌──────────────────────────────┐
                              │ START: Competitor objection   │
                              └────────────┬─────────────────┘
                                           │
                         ┌─────────────────▼─────────────────┐
                         │ Competitor claim: "They say they   │
                         │ do X, we can't do X."             │
                         └────┬──────────────────────────┬───┘
                              │ We CAN do X              │ We CANNOT do X
                              ▼                          ▼
                      ┌──────────────┐          ┌──────────────────────┐
                      │ Acknowledge: │          │ Reframe: "Most of our│
                      │ "Great catch.│          │ customers who needed │
                      │ We can do X. │          │ X actually solved it │
                      │ Let me show  │          │ more effectively with│
                      │ you how and  │          │ Y + Z. Here's a case │
                      │ share a case │          │ study showing 40%    │
                      │ study."      │          │ better outcome."     │
                      └──────────────┘          └──────────────────────┘
```
**Golden rule:** Never say "we have that on the roadmap." Say: "That's on our roadmap for Q3. In the meantime, here's how our customers solve it today — and here's the recorded conversation with our VP of Product explaining why we're building it the way we are."

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->

<!-- DEEP: 10+min -->

### Phase 1 (~30 min): Technical Discovery

Run MEDDIC or BANT discovery with the prospect. Start with open-ended pain questions: "Walk me through your current process. Where does it break? What does that cost you?" Document every pain point with a quantifier — dollars, hours, errors, churn. Identify the technical evaluators (who will test the product) separately from the economic buyer (who signs). Ask: "What would a successful evaluation look like? If we nail this, what happens next?" Map the decision process: who, what gates, when. End discovery with a summary email: "Here's what I heard. Did I get it right? If so, I'll tailor the demo to these 3 priorities."

<!-- DEEP: 10+min -->

### Phase 2 (~20 min): Demo Environment Management

Maintain at least 3 demo environments: (1) "Clean" — empty/default state for first demos, (2) "Real-ish" — populated with realistic data, dashboards showing activity, integration connectors configured, (3) "Vertical-specific" — tailored to healthcare/fintech/e-commerce with domain-relevant data. Environment checklist before every demo: all integrations connected, latest version deployed, no error toast on login, all charts render, search returns results, user flow works end-to-end. Use automation: scheduled health checks that run the critical path daily at 6 AM and email if anything fails. Have a fallback plan: recorded walkthrough ready if environment fails during the call.

<!-- DEEP: 10+min -->

### Phase 3 (~45 min): Demo Design & Delivery

Build a 3-act demo narrative: Act 1 — "Here's your world today" (show the pain). Act 2 — "Here's what it could be" (show the solution solving the exact pain they described). Act 3 — "Here's why it's different" (differentiator walk). Start with the outcome, not the login screen. Never do a point-and-click feature tour — every click answers a pain point they disclosed. Prepare 2-3 "pattern interrupt" moments: unexpected value that makes them lean forward. Schedule the demo for 45 minutes max; leave 15 minutes for questions. Send the prospect a "what to expect" email 24 hours before: "We'll cover [pain 1], [pain 2], [pain 3]. Come with questions." Record the demo and share within 2 hours. Follow up with a 1-page summary: "We showed X → Your pain Y → Outcome Z."

<!-- DEEP: 10+min -->

### Phase 4 (~60 min): RFP/RFI Response

Triage incoming RFP: score against ideal customer profile (ICP). Don't respond to every RFP — if it's vendor-written (designed for a competitor), decline with a polite "not a fit at this time." For RFPs worth pursuing: create a response matrix (question → answer owner → deadline). Use a response library: maintain a database of previous answers tagged by topic (security, integration, SLAs, architecture). Don't rewrite from scratch. For technical sections: include architecture diagrams, integration patterns, API documentation links, and relevant case studies. Every "yes" answer needs proof — "We support SSO" → "Attached: SAML 2.0 configuration guide, SOC 2 Type II report." Deadline buffer: submit 24 hours before the deadline, not at 11:59 PM. Errors caught late can't be fixed.

<!-- DEEP: 10+min -->

### Phase 5 (~30 min): Competitive Positioning

Map your product against top 3 competitors on a 2×2: X-axis = completeness of vision, Y-axis = ability to execute. Identify your unfair advantages — the capabilities competitors can't replicate in 12 months. Build a competitive battle card for each competitor: their strengths (be honest), their weaknesses (validated by customer evidence), your positioning (reframe, don't trash), trap questions they'll ask about you, and trap questions you ask about them. Example trap question: "How does [competitor] handle [edge case your product handles gracefully]?" Keep battle cards updated quarterly — competitors ship too, and stale competitive intel is worse than none.

<!-- DEEP: 10+min -->

### Phase 6 (~20 min): Technical Win Rate Optimization

Track technical win rate = (deals where you were technical evaluator's choice) / (total deals engaged). Target > 40% technical win rate. For every loss, run a 15-minute loss analysis: (1) What was the technical reason given? (2) What was the real reason (ask the AE, the champion, the evaluator)? (3) Did we lose on product, on process, or on politics? (4) What's the pattern across the last 3 losses? Common failure modes: demo didn't map to pain (fix: better discovery), PoC scope too large (fix: mutual success plan), no champion (fix: qualification), competitive trap sprung (fix: battle card refresh). Review win/loss patterns monthly with product management — product gaps that repeat across losses are roadmap input.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -- these rules encode years of lost deals and near-misses -->

- Record every demo and label it with the deal name, date, and outcome. Build a library of 10 "greatest hits" — 2-minute clips of moments where prospects leaned in.
- Maintain a personal knowledge base of "how to show X" for every major feature. Demo narratives, not feature specs. Updated weekly.
- Use the "Tell-Show-Tell" pattern: "We're going to show you [outcome]. [Demo the thing]. As you saw, this delivers [outcome] which means [business impact]."
- Always ask the "What happens next?" question at the end of every demo: "If this looks good, what are your next steps to evaluate and decide? Who else needs to see this?"
- Never go into a demo without knowing the top 3 pain points. If the AE won't tell you, run discovery yourself before the demo.
- Time-box PoCs ruthlessly: 2 weeks max, 3 success criteria max, mutually agreed success plan signed before starting, weekly check-ins, hard stop date.
- For RFP responses: maintain a "response vault" — a searchable database of past answers tagged by topic, industry, and competitor mentioned.
- Use the "parking lot" technique for off-topic questions during demos: "Great question — let me capture that and we'll cover it at the end so I can give it the attention it deserves."
- When you lose a deal, conduct the loss analysis within 48 hours while memory is fresh. Pattern-match across losses — one loss is data, two is a pattern, three is a systemic issue.
- Never demo on production. Ever. One wrong click, one real customer's data exposed, and the deal is dead — plus you've created a compliance incident.

## Anti-Patterns
<!-- STANDARD: 3min -- patterns that predictably fail -->

| Anti-Pattern | Why It Fails | Correct Approach |
|---|---|---|
| Running demos as feature tours instead of pain-solving narratives | "Looks great" is the most dangerous phrase in presales. The prospect enjoyed the show but doesn't know what to do next because you never connected features to their business impact | Use Tell-Show-Tell: state the outcome, demo the feature, connect to business impact. Map every feature shown to a quantifiable pain discovered in discovery. End with "What happens next?" |
| Starting a PoC without a signed mutual success plan | Without agreed scope and criteria, the PoC becomes an open-ended consulting project. Every stakeholder has a different definition of success and the evaluation drifts indefinitely | PoC must have ≤3 success criteria defined before starting, signed by both parties, 2-week max timeline, weekly check-ins, and a hard stop date. No signed plan = no PoC |
| Writing RFP responses with generic affirmations ("Yes, we support X") | Generic answers are indistinguishable from competitors' generic answers. Evaluators score you the same as everyone else — and the incumbent wins on relationship | Every "yes" in an RFP needs a proof point: implementation guide link, architecture diagram, case study with metrics. Specificity is the only way to differentiate in a procurement-driven evaluation |
| Assuming a technical win means a deal win | The engineering team loves your product but the economic buyer wasn't engaged. Technical win without business win = loss | MEDDIC "E" (Economic Buyer) and "C" (Champion) scores must be >7 before PoC starts. Arm your champion with ROI data and internal-selling materials. The technical evaluator can't sign the check |
| Letting FUD sit unanswered for more than 24 hours | FUD has a 24-hour half-life. If you don't respond with evidence quickly, the prospect assumes the competitor's claim is true and your silence confirms it | Build competitive battle cards proactively. When FUD lands, respond with evidence within 24 hours — customer proof, third-party validation, or architecture explanation. Silence loses deals |
| Maintaining only one demo environment with no backup | When the demo environment fails during a live call, credibility evaporates. You can't recover the momentum and the deal stalls | Maintain at least 3 demo environments: Clean (pristine), Realistic (data-rich), and Vertical-specific. Run daily automated health checks. Always have a recorded backup walkthrough ready |
| Conducting loss analysis weeks after the deal closes | Memory fades, details blur, and the real reason for the loss gets replaced by convenient narratives. Patterns across losses go undetected | Complete loss analysis within 48 hours of deal outcome. Interview the AE, the champion, and the evaluator. Track patterns across losses monthly — one loss is data, two is a pattern, three is a systemic issue |
| Treating demo follow-up as optional or delayed | The prospect's enthusiasm decays rapidly. A demo with no follow-up within 2 hours loses momentum the AE can't recover | Send follow-up within 2 hours: recording link, 1-page summary of what was shown and how it maps to their pain, and clear next steps. The follow-up is the bridge from demo to decision |

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Product Manager** | Feature gaps identified across 3+ deals, roadmap questions in RFPs, competitive positioning | Win/loss analysis with product gap patterns, roadmap timeline requests, competitive feature parity gaps. **Decision gate:** Does product gap block > $500K pipeline? → roadmap escalation. **Artifact:** product gap impact report. |
| **Backend Developer** | PoC requires custom integration, API limitations hit during demo, architecture deep-dive needed | Technical requirements, integration specs, API capability questions |
| **Account Manager** | Deal stage advancement, AE alignment on discovery, qualification check | MEDDIC score, demo outcome, next steps, technical risk flags. **Decision gate:** Is MEDDIC "E" (Economic Buyer) score > 7? → deal qualified. **Artifact:** MEDDIC qualification sheet + demo outcome summary. |
| **Customer Success Manager** | Post-sale handoff, implementation expectations set during sales, PoC-to-production transition | Success criteria from PoC, promises made during demo, technical configuration details. **Decision gate:** Are PoC success criteria documented and signed by both parties? → handoff ready. **Artifact:** technical handoff document + success criteria sign-off. |
| **Business Strategist** | Market positioning changes, competitive landscape shifts, pricing objections | Competitor intelligence, win/loss trends, market messaging feedback |
| **Security Engineer** | Security questionnaires in RFPs, prospect security reviews, compliance certification requests | SOC 2 reports, penetration test results, architecture diagrams for security review |
| **Marketing Manager** | Battle card updates, case study requests from won deals, competitive messaging | Win stories, competitive positioning feedback, demo clips for sales enablement |
| **Legal Advisor** | Contract technical schedules, SLA commitments in RFP, data processing terms | Technical scope of commitments, feasibility of SLA terms, data handling workflows |
| **BizDev Manager** | Partner-sourced deals, channel co-sell opportunities, partner training needs | Partner deal registration, technical qualification for partner deals, partner capability gaps. **Decision gate:** Has partner completed technical certification? → co-sell enabled. **Artifact:** partner technical readiness scorecard. |
| **RevOps Manager** | Pipeline analytics, deal velocity, win rate trends, forecast accuracy | Deal-level data, stage duration, technical win/loss reasons, conversion rates by source. **Decision gate:** Is deal velocity within 20% of historical average? → forecast reliable. **Artifact:** deal inspection report + velocity analysis. |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Product gap blocks 3+ active deals | Product Manager + VP of Sales | Roadmap escalation; quantify revenue at risk |
| Competitor launches feature that eliminates our key differentiator | Product Manager + Marketing Manager + VP Sales | Competitive response needed within 1 week |
| Demo environment down during a call | AE on the deal + all SEs | Reputation damage control; switch to backup immediately |
| PoC success criteria not met by deadline | AE + Customer Success Manager | Expectation reset; no-deal or scope-change conversation |
| RFP response requires commitment we can't deliver (SLA, feature, cert) | Legal Advisor + Product Manager | Liability risk; negotiate alternative before submitting |

### Escalation Path

```
Product gap blocking >$500K pipeline → Product Manager + VP Product + VP Sales
Competitor displacement threat across multiple accounts → VP Sales + Marketing Manager + Product Manager
Demo environment instability >48 hours → Engineering Lead + DevOps + VP Sales
RFP commitment exceeds current capability → Legal Advisor + VP Product + CEO Strategist
```

### Cross-skills Integration

```bash
# Chain: product-manager → sales-engineer → customer-success-manager
# New feature launch: product-manager defines feature → sales-engineer builds demo + battle card → customer-success-manager receives post-sale handoff

# Chain: backend-developer → sales-engineer → account-manager
# Custom integration PoC: backend-developer builds integration → sales-engineer demos it → account-manager closes

# Chain: marketing-manager → sales-engineer
# Campaign launch: marketing-manager provides messaging/persona → sales-engineer builds demo tailored to campaign target
```

## Proactive Triggers
<!-- QUICK: 30s -- when to proactively notify stakeholders -->

| Trigger | Notify | Why |
|---------|--------|-----|
| Same product gap blocks 3+ active deals simultaneously | Product Manager, VP Sales, VP Product | Roadmap escalation required; quantify total revenue at risk across all affected deals. Pattern = systemic gap, not isolated objection |
| Competitor launches feature that eliminates a key differentiator | Product Manager, Marketing Manager, VP Sales | Competitive response needed within 1 week; battle card refresh, demo narrative update, and sales enablement before competitive losses accumulate |
| Demo environment is down or unstable during a scheduled call | AE on the deal, all SEs | Reputation damage control; switch to recorded backup immediately. Root cause the failure and implement preventive health checks before next demo |
| PoC success criteria are not met by the agreed deadline | AE, Customer Success Manager, RevOps Manager | Expectation reset required; either extend with revised scope, or have the no-deal conversation. Prolonging a failing PoC wastes SE time and damages credibility |
| RFP response requires a contractual commitment the product can't deliver (SLA, feature, certification) | Legal Advisor, Product Manager, VP Product | Liability risk; negotiate alternative language or decline the commitment before submission. A signed contract you can't fulfill is worse than a lost RFP |
| Technical win rate drops below 30% for 2 consecutive months | VP Sales, Product Manager, Marketing Manager | Systemic presales issue; audit recent losses for patterns. Possible causes: demo quality, competitive positioning gap, product gap, or qualification failure |
| MEDDIC "E" (Economic Buyer) score is <5 across 50%+ of active deals | VP Sales, RevOps Manager | Deals are unqualified — SE time is being wasted on opportunities that can't close. Tighten qualification gates before SE engagement |
| Customer reports critical bug or data issue discovered during a live PoC or demo | Product Manager, Engineering Lead, Customer Success Manager | Trust crisis with an active prospect; immediate engineering escalation. Transparency and speed of response determine whether the deal survives |

## Scale Depth: Solo → Small → Medium → Enterprise
<!-- DEEP: 10+min -- how this skill changes as the company grows -->

### Solo
Founder demos the product, answers technical questions. Close first deals, learn objections. Founder is the SE; no demo environment; every call is a learning opportunity. Focus on understanding what prospects care about technically and building demo narratives around those discovery insights.

### Small Team
1-2 SEs support all deals, build demo environments. Scale founder's technical selling ability. Dedicated SEs; reusable demo environments; first battle cards. The SE team builds demo environments that don't break and battle cards that actually help AEs.

### Medium Team
SE team organized by vertical/region, PoC management. Deep vertical expertise, win competitive deals. Vertical-specialized SEs; structured PoC process; RFx response team. SEs develop domain expertise that differentiates the company in competitive evaluations.

### Enterprise
Global SE organization, SE leadership, solution architect tiers. Support enterprise sales at scale, technical GTM. SE Directors; solution architects for strategic deals; SE career ladder; demo platform. SE function is a strategic revenue driver with career progression, specialized roles, and global coverage.

### Transition Triggers
- **Solo → Small Team:** Deal volume exceeds 5 technical evaluations/month and founder can no longer personally demo every opportunity.
- **Small Team → Medium Team:** SE team exceeds 5 people and deals require vertical specialization or dedicated PoC management.
- **Medium Team → Enterprise:** Sales organization exceeds 50 AEs across multiple geographies and requires SE leadership, solution architect tiers, and a formal career ladder.


## What Good Looks Like
<!-- QUICK: 30s -- concrete success description -->

Demo opens in 5 seconds, environment is at latest version, first screen maps to the prospect's #1 pain point exactly. The prospect says "that's exactly what we need" within the first 10 minutes. After the demo, the prospect can articulate 3 specific reasons they'd choose you — unprompted. RFP submitted 24 hours before deadline with zero errors. MEDDIC score updated in CRM within 1 hour of each call. Technical win rate trending above 40%. Loss analyses filed within 48 hours and pattern-matched across deals. Demo environment health checks pass every morning at 6 AM.

## Error Decoder
<!-- DEEP: 10+min -- every row is a real deal that was lost or saved. Each error is a pattern observed across 10+ deals. -->

| Symptom | Root Cause | Fix | Lesson |
|---------|------------|-----|--------|
|---------|------------|-----|
| Demo environment shows blank screen or 500 error | Integration token expired or service version mismatch | Run daily automated health checks. Keep a "demo restore" script that resets environment to known-good state in <5 min. Always have the recorded backup walkthrough ready. | A demo environment that fails during a call costs credibility that takes months to rebuild. Automated health checks are insurance against the most preventable deal-killer in presales. |
| Prospect says "looks great" after demo but deal stalls | Demo was a feature tour, not a pain-solving narrative | Revisit discovery. Did you map every feature shown to a quantifiable pain? Send follow-up: "Based on what we showed, here's the 3 ways we'd impact your business. What's the next step to validate?" | "Looks great" is the most dangerous phrase in presales. It means the prospect enjoyed the show but doesn't know what to do next — because you never connected features to their pain. |
| PoC fails on technical criteria at final review | Scope too large, success criteria too vague, no mutual plan | PoC must have ≤3 success criteria, defined before starting, signed by both parties. Weekly checkpoints catch drift early. Never start a PoC without a signed mutual success plan. | A PoC without signed success criteria is an open-ended consulting project masquerading as an evaluation. Without mutual sign-off on scope and criteria, every party has a different definition of success. |
| RFP loses on technical score despite feature parity | Responses were generic ("yes we support X") without proof points | Every "yes" in an RFP needs evidence: implementation guide link, architecture diagram, case study with metrics. Generic answers are indistinguishable from competitors' generic answers. | In RFPs, "yes" without evidence is indistinguishable from a lie. Every affirmative answer must be backed by a proof point — implementation guide, architecture diagram, or case study with metrics. |
| Technical evaluator loves product but deal goes to competitor anyway | Didn't reach the economic buyer or champion wasn't mobilized | MEDDIC "E" and "C" scores were low. Technical win without business win = loss. Engage economic buyer before PoC starts. Arm your champion with ROI data and internal-selling materials. | A technical win is not a deal win. The engineering team can love your product, but if the economic buyer doesn't see business value, you will lose to a competitor who connected features to outcomes. |
| Competitor FUD lands and prospect goes cold | No competitive battle card prepared for this competitor | Build battle cards proactively, not reactively. Train AEs on trap questions for each competitor. When FUD lands, respond with evidence within 24 hours — silence confirms FUD. | FUD has a 24-hour half-life. If you don't respond with evidence within one business day, the prospect assumes the FUD is true and you lose the competitive narrative. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
<!-- DEEP: 10+min -- each checklist item references a standard born from production failure -->

- [ ] **[S1]** Demo environment health check passes daily at 6 AM — all integrations connected, no errors, critical path walkable
- [ ] **[S2]** Demo environment restore script runs in < 5 minutes from any broken state
- [ ] **[S3]** Recorded backup demo exists for every major product area — usable when live environment fails
- [ ] **[S4]** MEDDIC score recorded in CRM for every opportunity after every SE interaction
- [ ] **[S5]** Demo narrative exists for every major feature — updated weekly, linked to discovery questions and pain mapping
- [ ] **[S6]** Competitive battle cards maintained for top 3 competitors — updated quarterly with trap questions and rebuttals
- [ ] **[S7]** RFP response library organized by topic with searchable tags — no answer written from scratch twice
- [ ] **[S8]** Every PoC has a signed mutual success plan with ≤3 success criteria, 2-week max timeline, and hard stop date
- [ ] **[S9]** Win/loss analysis completed within 48 hours of every deal outcome — patterns tracked monthly
- [ ] **[S10]** Technical win rate measured monthly — targets: >40% overall, >50% for enterprise deals
- [ ] **[S11]** Demo follow-up sent within 2 hours: recording link, 1-page summary, next steps
- [ ] **[S12]** At least 3 demo environments maintained: Clean, Realistic, and Vertical-specific
- [ ] **[S13]** Product gap log maintained — every gap identified during sales cycle logged with revenue impact estimate
- [ ] **[S14]** Pre-demo "what to expect" email sent 24 hours before every scheduled demo


## References

## References

- **product-manager** — for feature roadmap, product gap escalation, and competitive positioning input
- **backend-developer** — for PoC integration support, API capability deep-dives, and custom demo builds
- **customer-success-manager** — for post-sale handoff, implementation expectation alignment, PoC-to-production transition
- **marketing-manager** — for battle card maintenance, case study development, and sales enablement materials
- **account-manager** — for AE alignment, deal stage advancement, and qualification methodology
- **business-strategist** — for market positioning, competitive landscape analysis, and pricing objection handling
- _The Challenger Sale_ by Matthew Dixon & Brent Adamson — for insight-led selling methodology
- _Demonstrating to Win_ by Rob Rutenbar — for demo narrative design patterns
- MEDDIC framework by Dick Dunkel & John McMahon — for enterprise qualification methodology
