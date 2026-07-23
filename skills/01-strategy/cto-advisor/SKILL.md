---
name: cto-advisor
description: >
  Use when evaluating build-vs-buy decisions, designing engineering organizations,
  governing architecture, performing technical due diligence, selecting vendors, or
  managing innovation portfolios. Handles technology strategy, team topologies,
  architecture governance frameworks, technical debt assessment, due diligence
  checklists, and vendor evaluation matrices. Do NOT use for hands-on coding, code
  review, or infrastructure provisioning.
license: MIT
tags:
- strategy
- technology
- architecture
- engineering-management
- due-diligence
- vendor
- build-vs-buy
author: Sandeep Kumar Penchala
type: strategy
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 4000
chain:
  consumes_from:
  - director-engineering
  - engineering-manager
  - security-engineer
  - system-architect
  - vp-engineering
  feeds_into:
  - ceo-strategist
  - director-engineering
  - system-architect
  - vp-engineering
---

# CTO Advisor
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Strategic technology leadership: build-vs-buy decisions, engineering organization design,
architecture governance, technical due diligence, innovation management, and vendor
evaluation. Every section is a decision-making framework, not abstract advice.

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*", "build.vs.buy\|make.vs.buy\|build.or.buy\|procurement.decision\|vendor.selection")` AND `file_contains("*", "TCO\|cost.comparison\|5.year\|total.cost")` | This is your skill. Jump to **Decision Trees** — Build vs Buy. |
| A2 | `file_contains("*", "engineering.org\|team.structure\|team.topologies\|stream.aligned\|platform.team\|reporting.structure")` AND `file_contains("*", "hiring\|headcount\|career.ladder\|levels")` | Jump to **Core Workflow** — Phase 2: Engineering Org Design. |
| A3 | `file_contains("*", "architecture.governance\|architecture.review\|ARB\|RFC\|ADR\|decision.record")` AND `file_contains("*", "standard\|principle\|guideline\|policy")` | Jump to **Core Workflow** — Phase 3: Architecture Governance. |
| A4 | `file_contains("*", "tech.debt\|technical.debt\|refactor\|modernization\|legacy")` AND `file_contains("*", "prioritize\|principal\|interest\|cost.of.delay")` | Jump to **Decision Trees** — Tech Debt Prioritization. |
| A5 | `file_contains("*", "due.diligence\|technical.due.diligence\|acquisition\|M&A.*tech\|code.audit")` | Jump to **Core Workflow** — Phase 4: Technical Due Diligence. |
| A6 | `file_contains("*", "system.design\|microservice\|monolith\|event.driven\|C4\|architecture.pattern")` AND `file_contains("*", "scalability\|throughput\|latency\|capacity")` | Invoke **system-architect** instead. This is detailed architecture design. |
| A7 | `file_contains("*", "team.management\|hiring.engineer\|performance.review\|engineering.manager\|1:1")` AND NOT `file_contains("*", "architecture\|tech.debt\|build.vs.buy")` | Invoke **engineering-manager** instead. This is team management, not technology strategy. |
| A8 | `file_contains("*", "security.review\|threat.model\|pentest\|vulnerability\|OWASP\|compliance.SOC")` | Invoke **security-engineer** instead. This is security-specific work. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Make a build-vs-buy decision → Jump to "Decision Trees > Build vs Buy"
├── Design an engineering org
│   ├── Team structure → Go to "Core Workflow > Phase 2: Engineering Org Design"
│   └── Career ladders & hiring → Go to "Phase 2" + "Scale Depth"
├── Set architecture governance → Start at "Core Workflow > Phase 3: Architecture Governance"
├── Choose an architecture pattern → Jump to "Decision Trees > Architecture Pattern Selection"
├── Prioritize tech debt → Jump to "Decision Trees > Tech Debt Prioritization"
├── Evaluate a vendor → Jump to "Decision Trees > Vendor Selection" + "Phase 6: Vendor Evaluation"
├── Run technical due diligence → Go to "Core Workflow > Phase 4: Technical Due Diligence"
├── Manage innovation → Jump to "Core Workflow > Phase 5: Innovation Management"
├── Need system architecture or detailed design? → `system-architect`
├── Need engineering team management or hiring? → `engineering-manager`
├── Need security review or threat modeling? → `security-engineer`
├── Need company vision or fundraising strategy? → `ceo-strategist`
└── Don't know where to start? → Run "Core Workflow > Phase 1: Technology Strategy"
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to recommend a technology without understanding context.** Do not say "use Kubernetes" without knowing team size, current infrastructure, and scale requirements. Technology choice is context-dependent, not universally "best." | Trigger: response recommends a specific technology ("use [X]") AND `conversation_context` does not contain team_size, current_stack, AND expected_load within the conversation | STOP. Respond: "Before I recommend a technology, I need context. What's your current stack? How many engineers on the team? What's your expected load (QPS, data volume, users)? What's your deployment environment?" |
| **R2** | **REFUSE to present an architecture decision without tradeoffs.** Every "use X" recommendation must include at minimum one downside of X and one alternative Y with its conditions. If you cannot articulate the downsides, you do not understand the problem. | Trigger: generated content contains a technology recommendation AND within 300 characters no mention of "tradeoff\|downside\|alternative\|however\|but\|risk" | STOP. Append: "**Tradeoffs:** [X] trades off [downside]. The alternative is [Y], which is better if [condition]. You're choosing [X] because [reason], and you accept the cost of [downside]." |
| **R3** | **REFUSE to declare tech debt "critical" without quantifying impact.** "This tech debt is killing you" is not analysis. Quantify: "This tech debt slows feature delivery by an estimated [X] sprints per quarter." | Trigger: generated content labels tech debt "critical" or "urgent" without including an estimated time/cost impact (sprint delay, incident frequency, onboarding time) | STOP. Insert quantification: "This tech debt is critical because: [measurable symptom — e.g., 'deploys take 4 hours instead of 15 minutes'], costing [estimate — e.g., '~2 engineer-weeks per quarter in deploy time']. If unmeasurable, flag for measurement before prioritization." |
| **R4** | **DETECT and WARN when technology decisions are not tied to business outcomes.** Architecture recommendations must connect to cost, time-to-market, reliability, or team productivity. "Modern" or "best practice" are not valid justifications. | Trigger: generated content advocates for a technology using "modern" or "best practice" as the primary justification, without referencing a business metric (cost, revenue, time-to-market, reliability SLA, team velocity) | WARN. Rewrite: "Adopting [X] is expected to [business outcome: reduce cloud costs by Y%, accelerate deploy frequency from Z to W, improve uptime from A% to B%]. The cost is [migration effort, learning curve, tooling investment]." |
| **R5** | **STOP and ASK when critical architecture context is missing.** Do not assume: current scale (QPS, data volume), team expertise, deployment environment, or existing architecture constraints. Architectures designed without these are fiction. | Trigger: generating architecture recommendations that reference scale ("supports 10K QPS"), team capability ("your team can operate Kubernetes"), or environment ("deploy to AWS") without explicit confirmation of those details in the conversation | STOP. Ask: "What's your current and projected scale (QPS, data volume)? What's your team's expertise with the technologies under consideration? What's your deployment environment (AWS/Azure/GCP/on-prem)?" |
| **R6** | **DETECT and WARN when build-vs-buy analysis lacks TCO comparison.** Building in-house always looks cheaper in Year 1 and more expensive by Year 3. TCO must span 3-5 years including maintenance, onboarding, and opportunity cost. | Trigger: build-vs-buy recommendation is made without a 3-5 year TCO model covering: development cost, maintenance cost, onboarding cost for new hires, opportunity cost of engineers building commodity features | WARN. Append: "**TCO note:** In-house build likely costs [estimate] over 3 years (dev + maintenance + onboarding + opportunity cost). The vendor costs [estimate] over the same period. The crossover point is typically Year [N]. Verify these estimates with your actual engineering costs before deciding." |

## The Expert's Mindset

The CTO's job is not to pick the best technology — it's to **ensure technology serves business outcomes, to build an engineering organization that can execute, and to make technical decisions that compound positively over time**. The output is not a tech stack recommendation; the output is an engineering organization that delivers predictably at increasing scale.

### Mental Models

| Model | Description |
|---|---|
| **Technology is a means, not an end** | Every technical decision must trace to a business outcome: revenue, cost, speed, or risk reduction. If you can't draw that line, the decision is a hobby, not a strategy. |
| **Build vs. buy is a capability decision, not a cost decision** | Don't compare license cost to build cost. Compare: can you maintain this indefinitely? Does it differentiate you? Is it core to your business? Only build what differentiates. |
| **Technical debt is a financial instrument** | You're borrowing against future velocity. Like financial debt, it can be strategic (ship faster now, pay later) or reckless (no plan to repay). The CTO's job is to manage the debt portfolio. |
| **Your architecture is your org chart** | Conway's Law is real: systems mirror communication structures. If you want a different architecture, you may need a different team structure. |

### Cognitive Biases in Technology Leadership

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Shiny object syndrome** | Adopting new technology because it's exciting, not because it solves a real problem | Require a written rationale: "What problem does this solve? What's the alternative? What's the migration cost? What's the exit plan?" |
| **Not-invented-here** | Building everything internally when mature solutions exist | For every build decision, ask: "Is this core to our differentiation? If not, why are we building it?" |
| **Sunk cost in technology** | Continuing to invest in a failing platform because you've already spent millions | Set explicit "migrate or kill" criteria at adoption. Review annually. |
| **Recency bias in architecture** | Over-correcting for the last incident (e.g., adding microservices everywhere after one monolith problem) | Look at 12-month patterns, not the last fire. Don't architect for the last war. |

### What Masters Know That Others Don't

- **The best CTOs say no to 90% of technology requests.** Every "yes" to a new language, framework, or service is a permanent operational cost. The default answer is: "Let's solve this with what we already have." Only say yes when the existing stack truly cannot solve the problem.
- **Hiring bar is the most compounding technical decision you make.** A great engineer hired today makes the next hire easier (they attract other great engineers). A mediocre engineer hired today makes the next hire harder. Never compromise on the bar to fill a seat faster.
- **The CTO's technical depth must evolve with scale.** At 10 people, you should be the best IC on the team. At 100 people, you should be the best architect. At 1,000 people, you should be the best organizational designer. The skills that got you here won't get you there.
- **Platform teams are underinvested.** A 5-person platform team that makes 100 engineers 20% more productive delivers the equivalent of 20 additional engineers. Most CTOs underinvest in internal platform because it's not customer-facing.

## Operating at Different Levels

CTO effectiveness is deeply tied to company stage. The skills that make a great 10-person CTO differ from what makes a great 500-person CTO.

| Level | CTO Output Characteristics |
|---|---|
| **L1 — First-time CTO** | Learns technology leadership at scale. Needs frameworks for build-vs-buy, org design, and tech debt prioritization. |
| **L2 — Seed CTO (10-30)** | Hands-on technical leader. Sets initial tech stack, hiring bar, and engineering culture. Writes code while building the team. |
| **L3 — Growth CTO (30-150)** | Manages managers. Sets architecture strategy, tech org structure, and technical due diligence for fundraising. |
| **L4 — Scale CTO (150-1000+)** | Runs a multi-hundred person engineering org. Technology vision, platform strategy, M&A technical assessment. "This is our 3-year technical direction." |
| **L5 — Industry CTO** | Defines technology philosophies adopted across the industry. Board-level technology strategy for public companies. |

**Usage**: Say "as a growth-stage CTO, help me design the engineering org for..." or calibrate by company size. Default: **Growth CTO** (30-150 engineers, managing managers).

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Making build-vs-buy decisions for critical infrastructure or product components
- Designing or restructuring engineering organizations: team design, reporting structures, career ladders
- Establishing architecture governance: RFC processes, architecture review boards, decision frameworks
- Evaluating a startup's technology for investment, acquisition, or partnership
- Quantifying and prioritizing technical debt reduction
- Managing innovation: hackathons, research time, innovation funnels
- Running vendor evaluations: RFIs, RFPs, proof-of-concept design, TCO modeling

## Decision Trees

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Build vs Buy
```
                     ┌────────────────────────┐
                     │ START: Build or Buy?   │
                     └───────────┬────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Is this a competitive differentiator │
              │ for your core product?              │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ Can you hire and │  │ Is there a mature     │
        │ retain the talent│  │ vendor with < 20%     │
        │ in-house?        │  │ market share risk?    │
        └──┬───────────┬───┘  └──┬───────────────┬────┘
           │ YES       │ NO      │ YES           │ NO
           ▼           ▼         ▼               ▼
      ┌────────┐ ┌──────────┐ ┌──────┐    ┌───────────┐
      │ BUILD  │ │BUY +     │ │ BUY  │    │ BUILD      │
      │        │ │customize │ │      │    │ (no good   │
      │        │ │wrapper   │ │      │    │  vendor)   │
      └────────┘ └──────────┘ └──────┘    └───────────┘
```
**When to BUILD:** It's core IP that creates competitive moat. Team has domain expertise. Time-to-market > 6 months is acceptable. Total cost of build < 3x annual license cost over 3 years.  
**When to BUY:** Commodity infrastructure (auth, payments, monitoring, CI/CD). Vendor switching cost is manageable (< 3 months migration). Build would divert > 30% of engineering from product work.

### Architecture Pattern Selection
```
                     ┌──────────────────────────────┐
                     │ START: Monolith or Services?  │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Team size > 20 engineers?               │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ Do 2+ teams need │    │ Modular monolith.    │
        │ independent      │    │ Deploy as single     │
        │ deploy cadences? │    │ unit. Fast iteration.│
        └──┬───────────┬───┘    └──────────────────────┘
           │ YES       │ NO
           ▼           ▼
    ┌────────────┐ ┌──────────────┐
    │ Micro-     │ │ Monorepo     │
    │ services   │ │ with         │
    │ per domain │ │ modular      │
    └────────────┘ │ packages     │
                   └──────────────┘
```
**When to choose Microservices:** 3+ teams with independent release cycles. Different scaling requirements per component. Polyglot persistence is needed.  
**When to choose Modular Monolith:** < 20 engineers. Single deployment pipeline is adequate. Data consistency across domains is critical. Premature distribution adds latency and <!-- DEEP: 10+min -->
debugging complexity.

### Tech Debt Prioritization
```
                     ┌────────────────────────────┐
                     │ START: Prioritize tech debt │
                     └─────────────┬──────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Does this debt block a critical feature │
              │ or cause > 1 SEV1/quarter?              │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ P0: Fix this     │    │ Does it slow feature │
        │ sprint. Allocate │    │ delivery by > 30%?   │
        │ 20% capacity.    │    └──┬───────────────┬───┘
        └──────────────────┘       │ YES           │ NO
                                   ▼               ▼
                            ┌────────────┐  ┌──────────────┐
                            │ P1: Fix    │  │ P2: Fix when │
                            │ within 4   │  │ touching the │
                            │ weeks      │  │ file anyway  │
                            └────────────┘  └──────────────┘
```
**When to fix immediately (P0):** Security vulnerability with known exploit. Data corruption risk. Prevents shipping revenue-generating feature.  
**When to defer (P2):** Legacy code that works reliably. Module slated for replacement within 6 months. No customer-facing impact.

### Vendor Selection
```
                     ┌──────────────────────────┐
                     │ START: Evaluate vendor   │
                     └───────────┬──────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Does vendor SOC 2 / ISO 27001       │
              │ + serve > 100 customers at scale?   │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ POC in 2 weeks:  │  │ REJECT or wait for   │
        │ test critical    │  │ maturity. Too risky   │
        │ path + failure   │  │ for production use.   │
        │ modes            │  └──────────────────────┘
        └──┬───────────────┘
           │
           ▼
    ┌──────────────────────────┐
    │ Pricing < 15% of feature │
    │ budget? Lock-in risk     │
    │ reversible in 3 months?  │
    └──┬───────────────────┬───┘
       │ YES               │ NO
       ▼                   ▼
  ┌─────────┐        ┌──────────────┐
  │ PROCEED │        │ Negotiate or │
  │         │        │ find alt     │
  └─────────┘        └──────────────┘
```
**When to proceed:** Vendor passes security review, POC succeeds on critical path, pricing fits budget, and data migration OUT is feasible.  
**When to reject:** Vendor < 2 years old with < 50 customers. No SOC 2 or equivalent. Proprietary data format with no export API. Key-person dependency (single maintainer).

## Core Workflow

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Technology Strategy

**Build vs Buy Framework:**

```
Can this be a competitive differentiator?
├── YES → Does building give us a moat that buying doesn't?
│   ├── YES → BUILD (invest heavily)
│   └── NO  → Can we customize an off-the-shelf solution?
│       └── YES → BUY + customize
│
└── NO → Is there a mature, well-supported solution available?
    ├── YES → BUY (don't reinvent the wheel)
    └── NO  → Is the market nascent but strategically adjacent?
        ├── YES → BUILD (first-mover advantage possible)
        └── NO  → WAIT (let the market mature, then buy)
```


**What good looks like:** Technology radar document published and reviewed with the engineering team — every major dependency has a clear Adopt/Trial/Assess/Hold rating with written rationale. The last 3 build-vs-buy decisions are documented with 5-year TCO, alternatives considered, and accepted tradeoffs. A new CTO can read the radar and understand why every technology choice was made within an afternoon.

**Build-vs-buy cost comparison (5-year TCO):**

| Cost Factor               | Build                     | Buy (SaaS)          |
|----------------------------|---------------------------|---------------------|
| Initial build              | 3–6 engineers × 6–12 mo  | 0                   |
| Annual maintenance         | 2–3 engineers ongoing    | Annual license      |
| Infrastructure              | Cloud + ops               | Included            |
| Opportunity cost            | Engineers NOT on product  | 0                   |
| Integration cost            | Designed for your stack   | May need adapters   |
| Upgrade/migration cost      | You own it                | Vendor-driven       |
| Vendor lock-in              | None                      | High                |
| Customization flexibility   | Unlimited                 | Limited by API/config|
| **Rule of thumb**           | Build if it IS the product| Buy everything else |

**Technology Radar:**

Maintain a living document that classifies technologies into four rings:
- **Adopt**: proven, safe, widely used — default choice (e.g., PostgreSQL, React, AWS)
- **Trial**: promising, used in production by some teams — actively evaluate (e.g., Rust for perf-critical, Temporal for workflows)
- **Assess**: worth exploring, not yet production-ready in your context — spike/experiment (e.g., WebAssembly, DuckDB)
- **Hold**: proceed with caution — legacy, deprecated, or over-hyped (e.g., MongoDB for relational data, hand-rolled auth)

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->
The CTO bridges business strategy and technical execution. A CTO who doesn't coordinate with product builds systems nobody wants; one who doesn't coordinate with the CEO builds systems the company can't afford.

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `ceo-strategist` | Strategic vision, budget constraints, fundraising status, org design parameters, hiring budget | Before annual tech strategy planning; during build-vs-buy decisions >$100K |
| `system-architect` | Architecture decision records (ADRs), system design proposals, tech stack evaluations, scalability assessments | During architecture review board meetings; before approving new platform choices |
| `engineering-manager` | Team velocity data, tech debt backlog, hiring pipeline status, capacity allocation, skill gap analysis | During quarterly engineering planning; before team restructuring |
| `security-engineer` | Threat models, vulnerability reports, SOC 2/ISO progress, incident postmortems, security roadmap | During security incident response; before customer security review commitments |
| `vp-engineering` | Cross-team dependencies, engineering OKRs, resource conflicts, delivery risk flags | During portfolio-level prioritization; before major resource reallocation |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `ceo-strategist` | Technical feasibility assessment, engineering capacity forecast, cost of delay for tech investments, build-vs-buy recommendations | CEO commits to impossible timelines or overinvests in wrong technology |
| `vp-engineering` | Technology strategy, architecture governance framework, innovation budget, vendor evaluation results | Engineering teams operate without strategic direction — misaligned investments |
| `director-engineering` | Architecture principles, tech radar (Adopt/Trial/Assess/Hold), tech debt prioritization framework, RFC process design | Teams make inconsistent technology choices — fragmentation and duplicated effort |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Architecture change affecting 3+ services | `system-architect`, `engineering-manager`, `vp-engineering` | Cascade analysis, migration plan, deployment coordination |
| Security incident | `ceo-strategist`, `security-engineer`, `vp-engineering`, `legal-advisor` | Incident response, disclosure obligations, root cause timeline |
| Cloud cost spike (>50% week-over-week) | `fp-and-a-analyst`, `vp-engineering`, `ceo-strategist` | Cost root cause, remediation plan, budget impact |
| Key technical hire accepted/rejected | `ceo-strategist`, `engineering-manager`, `hr-manager` | Team velocity impact, backup hiring plan |
| Major vendor contract decision (>$50K/yr) | `fp-and-a-analyst`, `ceo-strategist`, `vp-engineering` | TCO analysis, negotiation strategy, migration cost |
| Production outage > 1 hour | `ceo-strategist`, `product-strategist`, `vp-engineering`, `engineering-manager` | Customer impact, root cause, remediation timeline, postmortem schedule |
| Tech due diligence requested (investor/customer) | `ceo-strategist`, `engineering-manager`, `security-engineer` | Documentation prep, architecture review, security posture summary |
| Build vs buy decision with >$100K implication | `ceo-strategist`, `fp-and-a-analyst`, `product-strategist` | TCO model, strategic implications, timeline trade-offs |

### Escalation Path

```
Existential technical risk (data loss, security breach, extended outage)
  └── `cto-advisor` + `ceo-strategist` + `legal-advisor`. Incident commander appointed. All-hands if >4 hours.

Strategic technical decision (architecture platform choice, major build vs buy)
  └── `cto-advisor` + `system-architect` + `engineering-manager`. `ceo-strategist` informed. Decision within 2 weeks.

Tactical technical decision (tooling, framework version, CI pipeline change)
  └── `engineering-manager` handles. `cto-advisor` informed via weekly 1:1. No escalation needed.
```

## Proactive Triggers

<!-- STANDARD: 5min — scenarios where CTO should intervene BEFORE disaster -->

| Trigger | Action | Why |
|---------|--------|-----|
| Team proposes building auth/payments/email infrastructure from scratch | Intervene: "Auth, payments, and email are solved problems. Unless they are your core differentiator, buying saves 6-12 months of engineering and eliminates entire classes of security liability. Auth0/Clerk for auth, Stripe for payments, Resend/SendGrid for email. Redirect engineering effort to your moat." | Build-vs-buy errors in commoditized infrastructure are the most expensive early-stage mistakes. Building auth in-house means your team now owns OWASP auth vulnerabilities, password reset flows, MFA enrollment, session management, and SOC 2 audit scope — none of which differentiate your product |
| A team lead says "we'll refactor it later" for the third sprint in a row without tracking tech debt | Flag: "Technical debt without quantification is just wishful thinking. Model it as: principal (effort to fix) × interest rate (velocity drag per sprint). If interest exceeds 10% of team velocity, it must be scheduled. Create a tech-debt-backlog.md with principal + interest rate for each item" | Unquantified technical debt compounds silently. A 2-day refactor deferred for 8 sprints becomes a 3-week migration because the code has accumulated 12 dependent features. The interest-rate framework makes the cost visible to non-technical stakeholders |
| Engineering team growing from 8 to 15 without org structure changes | Alert: "At 8 people, everyone can talk to everyone. At 15, you need stream-aligned teams with clear ownership boundaries. Without this, you get: (1) distributed monoliths as team A accidentally breaks team B's code, (2) decision paralysis because everything needs cross-team consensus, (3) Conway's Law working against you. Define team boundaries NOW, before the next 3 hires" | Conway's Law is the silent architecture killer. Every organization that scales without intentional team boundaries produces a system architecture that mirrors its communication chaos. Fixing this retroactively requires re-architecting BOTH the org chart AND the codebase |
| CTO spending >50% of time on hands-on coding instead of strategy and people | Warn: "Your highest-leverage activities are: (1) architecture decisions that affect all teams, (2) hiring and retaining senior engineers, (3) build-vs-buy decisions with $100K+ TCO impact, (4) board/investor technology communication. Individual coding contributions at this stage have 10x less impact than a single architecture decision. Delegate the PRs; own the RFCs" | The CTO role transitions from builder to multiplier at ~10 engineers. A CTO writing features while the team lacks an architecture governance process is optimizing for personal satisfaction over organizational impact. The best CTOs write code that other engineers would never think to write — frameworks, platforms, decision records, not CRUD endpoints |
| Company evaluating 5+ SaaS tools without a vendor evaluation framework | Intervene: "Ad-hoc vendor selection leads to tool sprawl, integration nightmares, and budget overruns. Implement a weighted scorecard: (1) functional fit [30%], (2) TCO over 5 years [25%], (3) integration complexity with existing stack [20%], (4) vendor viability/roadmap [15%], (5) security/compliance posture [10%]. Every vendor over $10K/year must pass this gate" | Without a framework, vendor selection becomes a beauty contest won by the best sales team. Engineering teams end up maintaining 15 different SaaS integrations, each with its own auth, webhooks, and SLA — creating a fragile dependency chain that fails in unpredictable ways |
| No RFC process exists and architecture decisions are made in Slack threads that disappear | Flag: "Architecture decisions made in ephemeral communication channels are undiscoverable, unreviewable, and unaccountable. Implement: (1) RFC template with context, decision, alternatives considered, consequences, (2) async review period (3-5 days), (3) decision recorded as ADR in the repo. The process should be lightweight — a 2-page document, not a 20-page treatise" | The cost of a bad architecture decision isn't felt until 6-12 months later, when the person who made it may have left the company. ADRs create institutional memory. Without them, every new hire asks "why did we build it this way?" and nobody has the answer |
| Production incident occurs and there's no incident commander or escalation path | Intervene immediately: "Define: (1) incident severity levels (SEV1: customer data loss, SEV2: degraded service, SEV3: minor), (2) incident commander role rotates weekly, (3) escalation: 15min without resolution → CTO, 1hr → CEO, (4) post-mortem within 48hrs (blameless). Write this as incidents.md and share with the entire engineering team today" | Without an incident process, every outage becomes a scramble where the loudest person directs the response. Blameless post-mortems separate system failures from individual mistakes. Companies without incident processes either over-escalate (CEO paged for a partial CDN outage) or under-escalate (data breach goes unreported for 72 hours) |

## What Good Looks Like

> Your technology radar is current and every team knows which technologies are Adopt, Trial, Assess, or Hold — nobody is stealth-adopting MongoDB "because the tutorial used it.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.


## Deliberate Practice

Great CTOs develop their judgment through structured exposure to technology and organizational problems across different contexts.

```mermaid
graph LR
    A[Audit a tech org/system] --> B[Diagnose: what's the bottleneck?]
    B --> C[Recommend strategy with trade-offs]
    C --> D[Observe implementation outcome]
    D --> A
```

| Level | Practice Routine | Frequency |
|---|---|---|
| **Novice** | Study a public company's engineering blog and write a one-page analysis of their tech strategy | Weekly |
| **Competent** | Do a mock build-vs-buy analysis for a realistic scenario | Monthly |
| **Expert** | Conduct a real org health assessment: team topology, delivery metrics, tech debt inventory | Quarterly |
| **Master** | Advise a portfolio company or startup through a strategic inflection point | Annually |

**The One Highest-Leverage Activity**: Audit one team's entire tech stack end-to-end each month — from CI/CD to production monitoring. Write a one-page assessment: what's working, what's the bottleneck, what should change in the next quarter. Share with the team lead.

## Gotchas

- **Build vs buy decision** based on first-year cost alone — building costs $200K (3 engineers × 6 months) and buying costs $50K/year. At year 3: build = $200K + $40K/year maintenance = $320K. Buy = $150K (with 20% annual price increase). But build also gives you control over roadmap, integration depth, and zero vendor lock-in. TCO not year-1.
- **Due diligence technical assessment** that reviews architecture diagrams and code quality — misses the #1 risk: key-person dependency. "What happens if your lead infrastructure engineer wins the lottery tomorrow?" If the answer is "we're in serious trouble," that's a material risk, regardless of code quality.
- **"Innovation lab" or "skunkworks"** as a team siloed from the main engineering org — they build cool prototypes that can't integrate with production systems. The prototypes demo beautifully to the board and then die because the main engineering team wasn't part of the process. Innovation must be embedded, not siloed.
- **"Move fast and break things"** applied to infrastructure decisions — choosing a database, message queue, or deployment platform requires 3-5 year commitments. Breaking things at the infrastructure layer means data migration, retraining, and service disruption. Fast iteration is for products, not platforms.


## References
- **Consequences**: See [consequences.md](references/consequences.md)
- **Context**: See [context.md](references/context.md)
- **Decision**: See [decision.md](references/decision.md)
- **Status**: See [status.md](references/status.md)
