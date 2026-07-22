---
name: director-engineering
description: 'Director of Engineering: org design, team topology, strategy translation, managing managers, cross-functional leadership, budget planning, EM development, and scaling engineering organizations
  for 20-50 engineers. Triggered by org design, team structure, reorg, capacity planning, budget, engineering strategy, cross-team delivery, managing managers, succession planning, executive communication.'
author: Sandeep Kumar Penchala
type: leadership
status: stable
version: 1.0.0
updated: 2026-07-22
chain:
  consumes_from:
  - cto-advisor
  - engineering-manager
  - hr-manager
  - product-manager
  - recruiting
  - technical-program-manager
  - vp-engineering
  feeds_into:
  - cto-advisor
  - engineering-manager
  - recruiting
  - vp-engineering
tags:
- director-engineering
- org-design
- team-topology
- strategy-translation
- managing-managers
- cross-functional-leadership
- budget-planning
- engineering-culture
token_budget: 5000
output:
  type: document
  path_hint: ./
---

# Director of Engineering

Organizational leadership at scale. You translate business strategy into engineering
organization design. You manage managers, not ICs. Your job is organizational
leverage — building systems (hiring, career ladders, delivery processes) that scale
across teams. Every section is a decision framework, not abstract advice.

## Route the Request
<!-- QUICK: 30s — pick your path, skip the rest -->

What are you trying to do?
├── Org design problem (structure, team boundaries, ownership)?
│   └── Jump to "Core Workflow > Phase 1: Org Design"
├── Cross-team delivery problem?
│   ├── Roadmap negotiation → Director + technical-program-manager
│   └── Jump to "Core Workflow > Phase 2: Strategy Translation"
├── Budget or headcount planning?
│   └── Jump to "Decision Trees" + "Best Practices > Budget Planning"
├── Individual IC performance issue?
│   └── DELEGATE to engineering-manager skill
├── EM performance or development?
│   └── Jump to "Core Workflow > Phase 3: EM Development"
├── Technical strategy across teams?
│   └── DELEGATE to staff-engineer + cto-advisor skills
├── Executive communication or stakeholder management?
│   └── Jump to "Core Workflow > Phase 4: Cross-Functional Leadership"
├── Considering a reorg?
│   └── Jump to "Decision Trees > When to Split" BEFORE acting
├── Vendor/platform decision at org scale?
│   └── Jump to "Decision Trees > Build vs Buy vs Partner"
└── Don't know where to start?
    └── Run all 4 phases of "Core Workflow" sequentially

Do not read the entire skill. Follow the route above.

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

1. **You manage the system that manages the work.** If you're in every decision,
   your org has a single point of failure. Build the system — hiring standards,
   delivery cadences, escalation paths — then trust your EMs to operate it. If
   you can't take a two-week vacation without things breaking, you haven't built
   the system yet.

2. **Hire and develop great EMs.** Your EMs are your multipliers. A great EM
   amplifies 6-8 engineers; a weak EM drags them all down. Invest disproportionately
   in EM hiring, onboarding, and development. No other activity gives higher
   organizational leverage.

3. **Team topology is your primary design tool.** Wrong boundaries create more
   problems than wrong code. Teams aligned to the wrong axis produce working
   software that doesn't add up to a working product. Conway's law is a design
   constraint you must actively manage.

4. **Speak the language of the business.** Revenue, cost, risk, time-to-market are
   your vocabulary, not just tech debt and latency. "Refactoring the API layer"
   is a cost center. "Reducing time-to-market by 40%" is a competitive advantage.

5. **Culture is what you tolerate.** If you tolerate toxic brilliance, that's your
   culture. If you tolerate EMs who blame their teams for failures, that's your
   culture. Culture isn't what you write on the wiki — it's the worst behavior
   you consistently let slide.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->

- **Org design and restructuring** — teams are growing beyond healthy span of control, cross-team coordination is the #1 delivery blocker, or the company is entering a new strategic phase that requires reorganizing engineering teams.
- **Managing managers** — you have EMs reporting to you who need coaching, development, and performance management. This skill covers EM 1:1 cadence, peer group facilitation, and succession planning.
- **Strategy translation** — the company has set annual OKRs and you need to translate them into engineering team-level goals with realistic capacity plans and negotiated roadmaps with product.
- **Cross-functional leadership** — engineering is not a trusted partner in the organization, product/design/engineering triads are not operating effectively, or executive stakeholders don't understand engineering's value.
- **Budget and headcount planning** — the annual planning cycle is starting and you need to build an engineering budget model, justify headcount requests, and present investment tiers to leadership.
- **Vendor and platform decisions at org scale** — you need to evaluate a build-vs-buy decision that affects multiple teams, or a major platform tool replacement that requires cross-team coordination.

## Decision Trees
<!-- STANDARD: 3min -->

### When Do I Split a Team?

```
Is the team > 8 people (including EM)?
├── Yes → Do any of these also apply?
│   ├── Delivery cadence slowing despite healthy team
│   ├── Team has two distinct domains of ownership
│   ├── Standups take > 15 minutes
│   ├── EM can't do meaningful 1:1s with everyone weekly
│   └── Code ownership in one area blocks the other
│   → If 2+ signals: SPLIT. If only size: consider, but act soon.
└── No → Is the team responsible for different business capabilities?
    ├── Yes → Does splitting reduce coordination? → SPLIT
    └── No → KEEP. Add capacity within the team.
```

Readiness test: After splitting, will each team have a clear charter, a capable
EM, and work > 80% independent? If any is "no," you're creating two broken teams.

### Build vs Buy vs Partner for a Capability

```
Is this capability core to competitive differentiation?
├── Yes → BUILD. Own it. Staff it properly.
│   └── "Core" means customers choose you because of it, not "we use it a lot."
└── No → Is there a mature vendor product?
    ├── Yes → TCO ≤ building + maintaining in-house?
    │   ├── Yes → BUY. Don't build undifferentiated infrastructure.
    │   └── No → Payback < 18 months? → BUILD. Otherwise → re-evaluate scope.
    └── No → Strategic partner for co-development?
        ├── Yes → PARTNER. Share risk, retain roadmap influence.
        └── No → BUILD minimally. Plan to replace if vendor emerges.
```

Anti-patterns: Building your own CI/CD, custom auth when OSS standards exist,
building a CRM unless CRM is literally your product.

## Core Workflow
<!-- STANDARD: 3min -->

### Phase 1: Org Design

**Goal:** Every team has a clear charter, healthy span of control, and ownership
boundaries that minimize cross-team dependencies.

**Step 1: Map the System Architecture**
Start with target architecture, not the people. Identify subsystems, bounded
contexts, interfaces. Team boundaries should mirror these.

**Step 2: Apply Conway's Law**
For each bounded context: which team owns it end-to-end? Where do inter-team
interfaces map to well-defined APIs? Teams owning pieces of two bounded
contexts? → Red flag. Split or reassign.

**Step 3: Validate Span of Control**
EM:IC ratio: 1:5 to 1:8. Director:EM ratio: 1:4 to 1:6. No team < 4 without
specific reason. No team > 10 (EM can't manage beyond this).

**Step 4: Write Team Charters**
One-pager per team: what they own, what they don't own, who their customers
are, mission in one sentence.

**Step 5: Identify Coordination Costs**
Draw lines between teams that coordinate to ship features. If a feature touches
4+ teams, boundaries are wrong. Revisit Step 1.

**Outputs:** Org chart with charters, ownership matrix, coordination map.

### Phase 2: Strategy Translation

**Goal:** Company strategy translated into team-level OKRs with realistic
capacity plans.

**Step 1: Absorb Company Strategy**
Start with company OKRs. Ask CEO/VP: "If we only accomplish one thing this
year, what must it be?"

**Step 2: Translate to Engineering OKRs**
Cascade method:
```
Company OKR: Launch in EU by Q3
  → KR: EU data residency (Infra team, Q2)
  → KR: EU payment providers (Payments team, Q2)
  → KR: i18n for DE, FR, ES (Platform + Product, Q2-Q3)
```

**Step 3: Capacity Planning**
Total weeks = (team size × weeks) × 0.7-0.8 factor. Subtract on-call,
interviews, PTO, management overhead, and KTLO (bugs, incidents, minor
improvements). Remaining = strategic capacity. If < OKR demands: descope,
hire, or renegotiate.

**Step 4: Roadmap Negotiation with Product**
Present capacity reality: "We have X weeks. The roadmap needs Y. Let's
prioritize together." For each ask: "If we do this, what drops?" Never say
"we'll figure it out."

**Outputs:** Team-level OKRs, capacity plan, negotiated roadmap.

### Phase 3: EM Development

**Goal:** Every EM is growing, every team has succession, calibration is fair.

**Step 1: EM 1:1 Cadence**
Weekly 1:1 with each EM. Non-negotiable. Recurring questions:
- "Who on your team is ready for more responsibility?"
- "What's the hardest part of your job right now?"
- "If you left tomorrow, who could replace you?"

**Step 2: EM Peer Group**
Bi-weekly EM forum: share challenges, cross-team coordination happens here,
you facilitate. EMs learn from each other, not just from you.

**Step 3: Performance Calibration**
Quarterly calibration: stack-rank across teams, calibrate on impact not
activity, identify high-potential ICs and EMs for succession. Document
decisions.

**Step 4: Succession Planning**
For each EM role (including yours): who steps in within 24 hours? Bench:
Ready now → Ready in 6 months → Ready in 12-18 months. If "ready now" is
empty, you have work to do.

**Outputs:** EM growth plans, calibration document, succession bench.

### Phase 4: Cross-Functional Leadership

**Goal:** Engineering is a trusted partner, not a service organization.

**Step 1: Product/Design/Engineering Triad**
Regular triad meeting: Product says what customers need, Design says how, you
say what's feasible when and at what cost. Disagree here, present unified plan
everywhere else.

**Step 2: Stakeholder Management Map**
Identify everyone who can say "no" to your org: exec team, product leaders,
dependent teams, compliance/legal/security. For each: what do they care about,
what's their perception, what do they need to hear this quarter?

**Step 3: Executive Communication**
Quarterly strategy memo (see Best Practices #2): what we delivered (business
impact), what's coming (why it matters), risks, what you need from leadership,
team health.

**Step 4: Metrics That Matter to Business**
Report time-to-market instead of velocity, customer-facing uptime instead of
incident count, cost per active user instead of headcount, feature adoption
rate instead of story points.

**Outputs:** Quarterly strategy memo, stakeholder map, triad operating rhythm.

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

<!-- NEIGHBORS: Director-level decisions cascade across org boundaries — coordinate on design, not just execution -->

| Skill | Decision Gate | Strategic Handoff Artifacts |
|---|---|---|
| `vp-engineering` | Multi-org strategy, major investments, reorgs across director boundaries — alignment needed before committing resources | Strategic alignment memo, resource advocacy brief, org-wide capacity model |
| `engineering-manager` | Team execution, IC performance, hiring pipeline, delivery tracking — escalate systemic patterns, not individual issues | Team health scorecards, risk registers, succession bench, delivery trend data |
| `cto-advisor` | Build vs buy at org scale, technology bets, due diligence for platform decisions — architecture governance gate | Trade-off framing documents, technology radar updates, build-vs-buy recommendation memos |
| `hr-manager` | Performance management framework, compensation calibration, employee relations for EM+ level | Calibration data, PIP documentation, engagement survey analysis by team |
| `product-manager` | Roadmap negotiation, customer discovery, prioritization — capacity reality must drive roadmap commits | Capacity model, negotiated roadmap, feature-vs-investment allocation |
| `technical-program-manager` | Cross-team delivery, dependency tracking, org-wide timelines — dependency maps drive org design decisions | Dependency maps, RAID logs, delivery status dashboards, cross-team risk registers |
| `recruiting` | EM+ hiring pipeline, offer strategy, employer brand — pipeline health feeds org design capacity planning | Pipeline metrics, comp benchmarks, process quality audits, time-to-fill by level |

**Org design handoff protocol:**
- **Quarterly reorg assessment:** Every quarter, review coordination cost data with `vp-engineering` — if 3+ teams touch most features, org boundaries need redesign
- **Architecture governance:** `cto-advisor` + `staff-engineer` review all cross-team RFCs; director ensures team charters reflect architectural boundaries
- **Strategic planning cadence:** Quarterly strategy memo to `vp-engineering` → cascaded to `engineering-manager` → reflected in team OKRs within 2 weeks
- **Succession planning:** `hr-manager` reviews bench strength quarterly; director owns EM succession with ready-now names for every EM role

| Skill | When to Involve | What You Need |
|---|---|---|
| **vp-engineering** | Multi-org strategy, major investments, reorgs across VP boundaries | Strategic alignment, air cover, resource advocacy |
| **engineering-manager** | Team execution, IC performance, hiring, delivery tracking | Team health data, risk flags, succession candidates |
| **staff-engineer** | Cross-team architecture, technical strategy, tech debt | Architecture assessments, RFC facilitation |
| **cto-advisor** | Build vs buy at scale, technology bets, due diligence | Trade-off framing, not just recommendations |
| **ceo-strategist** | Company strategy shifts, market changes | Business context for allocation decisions |
| **product-manager** | Roadmap negotiation, customer discovery, prioritization | Customer impact rationale |
| **technical-program-manager** | Cross-team delivery, dependency tracking, timelines | Dependency maps, risk registers, delivery status |
| **recruiting** | Hiring pipeline, offer strategy, employer brand | Pipeline metrics, comp benchmarks, process quality |
| **fp-and-a-analyst** | Budget modeling, headcount planning, vendor TCO | Financial models, scenario analysis, budget tracking |

## Best Practices
<!-- DEEP: 10+min -->

### 1. Team Topology Design
Per Team Topologies: **Stream-aligned** (70-80% of teams, own a business domain),
**Platform** (internal acceleration tools), **Enabling** (temporary, new tech
adoption), **Complicated-subsystem** (deep specialization). Start stream-aligned.
Extract platform only when duplication pain exceeds maintenance cost. Don't let
every team call itself a platform team.

### 2. Writing Strategy Memos
Structure: (1) Executive Summary — 3 sentences the CEO reads. (2) Last Quarter's
Results — business impact, not feature list. (3) This Quarter's Plan — 3-5
priorities, measurable outcomes. (4) Team Health — hiring, attrition, engagement.
(5) Risks & Asks — what could fail, what you need. (6) Appendix: Metrics Dashboard.
If your CEO can't understand it, rewrite it.

### 3. Running EM Staff Meetings
Weekly, 60-90 min: 0-10 min wins, 10-30 min strategic deep dive, 30-50 min
cross-team coordination, 50-60 min decisions. Never use for status — status goes
async. The meeting is for discussion, decisions, and team cohesion.

### 4. Managing Reorgs Without Destroying Morale
**Before:** written rationale, defined end state, pre-brief affected people 1:1.
**During:** over-communicate, protect IC focus (they keep shipping), acknowledge
cost honestly. **After:** no structural changes for 6 months, retrospect with
EMs at 30/60/90 days.

### 5. Budget Planning
(1) Strategic headcount: engineers at what levels to deliver strategy. (2) Cost
model: loaded cost = salary × 1.25-1.4 + infrastructure + SaaS + T&E. (3)
Scenarios: what at 80% budget? at 120%? (4) Vendor review: renewals,
consolidation, underused contracts. (5) Present as investment tiers: Tier 1
(KTLO, must fund) → Tier 2 (growth) → Tier 3 (acceleration, fund if possible).

### 6. Vendor and Platform Decisions at Scale
Form committee (you + EMs + staff engineer + procurement). Define criteria before
looking at vendors. Score independently, discuss. Run POC with real workload.
Document rationale — protects you when the vendor gets acquired.

### 7. Incident Review Culture
Your role: ensure blameless reviews producing systemic fixes. Never "who caused
this?" — ask "what in our system allowed this?" Track action items (> 90%
completion). Share learnings across teams. If you're in a bridge call and not
the commander, stay quiet.

### 8. Diversity and Inclusion at Org Level
**Pipeline:** sourcing strategies, bias-checked job descriptions. **Retention:**
track by demographic — differentials signal cultural issues. **Promotion:** audit
rates by demographic. **Inclusion:** measure psychological safety. **Accountability:**
include D&I metrics in quarterly strategy memo.

## Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Low morale, trust eroded after frequent restructuring | Reorg used as solution for unclear strategy or weak EMs. Reorging rearranges deck chairs instead of fixing underlying problems. | Diagnose before reorging: is strategy clear? Are EMs effective? Require "non-reorg alternatives considered" in any reorg proposal. | If you can't list three things you tried first, don't reorg. Reorgs fix org structure, not strategy gaps or weak management. |
| Director works 60-hour weeks, ICs report directly undermining EMs | Trust deficit in EMs. Bypassed them, making them weaker and yourself overloaded. Became a super-EM instead of building the management system. | Stop all skip-levels except quarterly structured ones. Tell each EM "I've been too involved. Here's what I need to step back from." Coach or replace weak EMs. | If >15% of your calendar is with ICs, you're in super-EM territory. Your leverage comes through EMs, not around them. |
| Team is happy but not delivering. No loud complaints yet output lags. | Conflict avoidance kept underperforming EM too long. Harmony became the goal instead of an enabler of high performance. | Conduct hard conversations. PIP the underperforming EM. Push back on roadmap with data. High-performing teams debate constructively. | Ask peers and your manager quarterly: "Where am I avoiding conflict?" Harmony without performance is just polite mediocrity. |
| Architecture mirrors org chart including bad parts. Cross-cutting concerns are inconsistent. | Teams designed around people and history, not target architecture. Conway's law operated unchecked. | Start from target architecture. Redraw boundaries around bounded contexts. Accept that moving people is necessary. | Every team charter must map to architecture decisions, not historical accidents. Let architecture drive org design, not the reverse. |
| Exec team doesn't understand engineering's value. Budget questioned. Engineering is first to cut. | Communicated in engineering language. Reported activity, not outcomes. No narrative connecting engineering work to company success. | Write quarterly strategy memos. Translate all initiatives into business impact language. Build relationships with CFO, not just CTO/VP. | If a non-technical exec can't explain your org in 30 seconds, your narrative is broken. Speak outcomes, not output. |

## Production Checklist
<!-- STANDARD: 3min -->

| ID | Check | Status |
|---|---|---|
| DE1 | Org chart documented with team charters for every team | ☐ |
| DE2 | EM:IC ratio between 1:5 and 1:8 for all teams | ☐ |
| DE3 | Director:EM ratio between 1:4 and 1:6 | ☐ |
| DE4 | Career ladder current and published for all engineering roles | ☐ |
| DE5 | Annual budget and headcount plan approved by FP&A | ☐ |
| DE6 | Team health metrics collected quarterly (engagement, safety) | ☐ |
| DE7 | Cross-team architecture forum meets bi-weekly or monthly | ☐ |
| DE8 | Succession plan documented for each EM role (ready-now name) | ☐ |
| DE9 | Quarterly strategy memo written and presented to exec team | ☐ |
| DE10 | Stakeholder NPS measured (product, design, dependent teams) | ☐ |
| DE11 | Incident review action items tracked, completion > 90% | ☐ |
| DE12 | Promotion rate audited by demographic, no significant differentials | ☐ |
| DE13 | Vendor contract renewals calendar with 90-day review trigger | ☐ |
| DE14 | EM peer group meets bi-weekly with documented learnings | ☐ |

## Scale Depth
<!-- DEEP: 10+min -->

### Solo (0-10 users, 1 person)
**Description:** Leads a single team, still hands-on with code
**When to use:** Early-stage company where director also codes; small team needs technical leadership
**Approach:** Balance IC work with team management; set technical direction while writing code; mentor junior engineers directly

### Small Team (10-100 users, 2-5 teams)
**Description:** Manages 2-3 teams (15-25 engineers), no longer has a direct team; impact measured through EM success
**When to use:** Organization growing beyond single team; need dedicated management layer; EMs need coaching and support
**Approach:** Org design and structure; EM development and coaching; learn influence without authority with product, design, exec team. Start with Phase 1 (Org Design) + Phase 3 (EM Development).

### Medium Team (100-10K users, 5-8 teams)
**Description:** Manages 5-8 teams (40-80 engineers), may have directors or senior EMs reporting
**When to use:** Org design is primary lever — systems of teams, not individual teams; heavy exec relationships and budget strategy
**Approach:** Multi-quarter planning; budget strategy; exec relationships (Phase 4); build trust with directs and let them manage their teams; avoid trying to maintain same depth with every team

### Enterprise (10K+ users, 20+ teams)
**Description:** Manages other directors, span of 80-200+ engineers; multi-year horizons for strategy and people
**When to use:** Responsible for engineering P&L; calendar 60%+ external (exec team, board, customers, partners)
**Approach:** Multi-year strategic planning; executive stakeholder management; engineering budget and P&L ownership; partner with fp-and-a-analyst; board-level communication

### Transition Triggers
- Move from Solo to Small Team when: Organization grows beyond a single team; need for dedicated EM layer becomes clear; IC-to-manager transition complete
- Move from Small Team to Medium Team when: Managing 5+ teams; need for org design at systems level; director-level reports join the organization
- Move from Medium Team to Enterprise when: Managing other directors; P&L responsibility; span exceeds 80 engineers; multi-year strategy becomes primary focus

## What Good Looks Like
<!-- STANDARD: 3min -->

Every team knows what success looks like and how it connects to company goals.
EMs grow into directors — the best retention is a clear growth path. Reorgs are
rare because initial design was right; when they happen, they're strategic, not
reactive. Teams self-organize because boundaries are clear. You spend most of your
time on future-state strategy, not firefighting — you built a system that handles
the fires. In executive meetings, you're sought for business perspective, not
asked to justify headcount. Your EMs say "working here made me a better leader"
— and they mean it.
