---
name: cto-advisor
description: Technology strategy, engineering org design, architecture governance, technical due diligence, innovation management, and vendor evaluation. Triggered by CTO, technology strategy, build vs buy, tech debt, architecture review, team topologies, due diligence, vendor selection.
author: Sandeep Kumar Penchala
type: strategy
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - cto-advisor
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
---
# CTO Advisor

Strategic technology leadership: build-vs-buy decisions, engineering organization design,
architecture governance, technical due diligence, innovation management, and vendor
evaluation. Every section is a decision-making framework, not abstract advice.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

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
└── Don't know where to start? → Run "Core Workflow > Phase 1: Technology Strategy"

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never recommend a technology without understanding context.** Don't say "use Kubernetes" without knowing team size, current infra, and scale requirements. Always ask: "What's your current stack, team expertise, and expected load?" before making a recommendation.
- **Never present an architecture decision without tradeoffs.** Every "use X" recommendation must include: "The tradeoff is [downside]. The alternative is [Y], which is better if [condition]." If you can't articulate the downsides, you don't understand the problem well enough.
- **Never declare tech debt "critical" without quantifying impact.** Instead of "this tech debt is killing you," say: "This tech debt slows feature delivery by an estimated [X] weeks per quarter, based on [observable symptom]." If you can't quantify it, flag it for measurement.
- **Always tie technology decisions to business outcomes.** Frame every recommendation in terms of: cost savings, time-to-market, reliability improvement, or team productivity. Never advocate for a technology purely because it's "modern" or "best practice."
- **Admit what you don't know.** If a question requires internal architecture details, current system load data, or team skill assessments you don't have access to, say so and tell the user what data to gather.

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


**What good looks like:** Technology radar document with every major dependency categorized (Adopt/Trial/Assess/Hold). Build-vs-buy evaluation compares 3 options with 5-year TCO. Architecture decision records exist for the last 5 major decisions.

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

**Tech Debt Quantification:**

```
Tech Debt Score = (Principal × Interest Rate) / Developer Velocity

Principal = effort to fix the debt (person-days)
Interest Rate = how much it slows down new feature development (hours/week wasted)
Developer Velocity = features shipped per sprint

Prioritization: Fix debt when Interest Rate > 5% of team velocity
                AND fixing it unblocks >20% throughput improvement

NOT all debt should be paid down. Debt that doesn't generate interest
(touch it once a year) is cheaper to carry than pay off.
```

### Phase 2 (~30 min): Engineering Org Design

**Team Topologies — four fundamental team types:**

| Team Type             | Purpose                                   | Interacts With           | Anti-Pattern               |
|-----------------------|-------------------------------------------|--------------------------|----------------------------|
| Stream-Aligned        | Deliver user value end-to-end             | Customers, other teams   | Too many dependencies      |
| Enabling              | Help stream teams overcome obstacles      | Stream-aligned teams     | Becomes ivory-tower        |
| Complicated-Subsystem | Build/maintain systems requiring deep expertise | Stream-aligned teams| Becomes bottleneck         |
| Platform              | Provide self-service infrastructure/platform | Stream-aligned teams  | Becomes ticket-driven      |

**Team size rule:** 5–9 engineers per stream-aligned team. <5: fragile. >9: coordination overhead dominates.
**Conway's Law in practice:** If you want a microservices architecture, organize as stream-aligned teams.
If you organize by function (frontend team, backend team, DB team), your architecture will reflect that.

**Engineering org scaling:**

```
1–10 engineers:  CTO writes code, no managers needed. Flat structure.
10–30:           CTO still technical; 1–2 tech leads emerge. Weekly 1:1s.
30–60:           CTO manages managers. First engineering managers (EMs).
                 Teams of 5–8. CTO spends 50% on strategy/people.
60–150:          Director/VPs emerge. CTO is 80%+ strategy, hiring, culture.
                 EMs manage teams; Directors manage EMs.
150+:            Multiple org layers. CTO is executive function.
                 Key challenge: maintaining technical coherence across orgs.
```

**Span of control:**
- Engineering Manager: 5–8 direct reports (IC engineers)
- Director: 3–5 EMs (15–40 total through chain)
- VP: 3–5 Directors
- CTO: leadership team + architecture group

**Career ladder — dual track:**

```
IC Track                     Management Track
─────────────────────────────────────────────────────
Junior Engineer              —
Engineer                     —
Senior Engineer              Engineering Manager
Staff Engineer               Senior EM
Principal Engineer           Director of Engineering
Distinguished Engineer       VP of Engineering
Fellow                       CTO / CPO
```

Both tracks must extend equally far with equivalent compensation. The worst
org design mistake: forcing engineers into management to advance.

### Phase 3 (~20 min): Architecture Governance

**RFC (Request for Comments) Process:**

```
1. Problem Statement   — What problem? Why now? What happens if we do nothing?
2. Proposed Solution   — Architecture decision with rationale.
3. Alternatives Considered — What else did you evaluate? Why rejected?
4. Trade-offs           — What do we gain? What do we lose? (Performance, complexity, cost, velocity)
5. Migration Plan       — How do we get from here to there? Rollback plan?
6. Open Questions       — What's still uncertain?

Review:
- Author circulates RFC → 5 business day comment period
- Architecture review meeting: author presents, stakeholders discuss
- Decision: Accepted / Accepted with modifications / Rejected / Needs more exploration
- Decisions documented in Architecture Decision Records (ADRs)
```

**ADR (Architecture Decision Record) template:**

```markdown
# ADR-042: Use PostgreSQL as Primary Relational Database

## Status
Accepted (2024-06-15)

## Context
We need a relational database for transactional data. Currently using
a mix of MySQL (legacy) and manual file-based storage.

## Decision
Adopt PostgreSQL as the single relational database across all services.

## Consequences
- Positive: ACID compliance, JSON support, mature ecosystem, strong community
- Negative: Team needs PG-specific training; migration from MySQL will take 3 sprints
- Risk: PG connection pooling requires PgBouncer for high-concurrency workloads
```

**Architecture Review Board (ARB):**
- Meets bi-weekly, 60 minutes
- Reviews: RFCs that cross team boundaries, new technology adoption requests, architecture departures
- Membership: Principal+ engineers, rotating attendance from each team
- **NOT** an approval bottleneck — decisions default to team autonomy unless cross-cutting

**Decision framework — when to escalate to ARB:**
- Technology choice that multiple teams will depend on
- Data model that crosses bounded contexts
- API contract that external customers will consume
- Deprecation of a widely-used internal service
- Introduction of a new programming language or paradigm

### Phase 4 (~15 min): Technical Due Diligence

**For acquisitions, investments, or major vendor decisions:**

**Code Quality Assessment (1–3 days):**
1. Clone repo; attempt to build and run locally. Time to first successful run = setup quality indicator.
2. Run static analysis: lint, complexity (cyclomatic >10 per function is a smell), test coverage
3. Manual review of 3–5 core modules: architecture coherence, naming consistency, error handling patterns
4. Check for secrets in code, hardcoded credentials, missing .gitignore
5. Dependency health: outdated packages, known CVEs, license compliance

**Architecture Assessment:**
1. Request architecture diagram — if they can't produce one, that's a finding
2. Trace a critical user journey through the system end-to-end
3. Identify single points of failure, scaling bottlenecks, data consistency patterns
4. Evaluate API design: REST/GraphQL consistency, versioning strategy, error handling
5. Assess data model: normalization, indexing, migration management

**Team Capability Assessment:**
| Signal                    | What to Look For                                         |
|---------------------------|----------------------------------------------------------|
| Bus factor                | How many people would need to be hit by a bus to halt dev? Target >3 per critical area |
| Documentation culture     | Do READMEs explain WHY and HOW? Are ADRs present?        |
| Code review practice      | Merge frequency, review depth, comments quality           |
| On-call maturity          | Runbooks, escalation paths, incident postmortems         |
| Deployment frequency      | Multiple per day = elite; weekly = medium; monthly = concern |
| Dependency on individuals | Is the CTO/tech lead the only person who understands X?  |

**Infrastructure Assessment Checklist:**
- [ ] CI/CD pipeline exists and completes in <30 minutes
- [ ] Infrastructure as Code (Terraform, Pulumi, CloudFormation) — not click-ops
- [ ] Secrets management: vault/manager, not in source code or env files
- [ ] Backups automated and tested; recovery time objective documented
- [ ] Monitoring: metrics, logs, alerts — at minimum on critical paths
- [ ] Security: dependency scanning, SAST, penetration testing cadence
- [ ] Scaling: documented auto-scaling policies; load test results from last 6 months

**Red Flags (severity-ordered):**
1. **No automated tests** → everything is legacy the day it's written
2. **Production access via SSH** → no repeatable deployments, no security boundary
3. **"The person who built this left"** → undocumented, unmaintainable systems
4. **Manual deployment process** → inconsistent, slow, error-prone
5. **No monitoring in production** → flying blind; don't know when things break
6. **Single database for everything** → scaling and coupling nightmare
7. **No code reviews** → quality rot, no knowledge sharing

### Phase 5 (~25 min): Innovation Management

**Innovation Time Allocation:**

| Activity                    | % of Engineering Time | Cadence              |
|-----------------------------|-----------------------|----------------------|
| Core product work            | 70%                   | Every sprint         |
| Technical debt + maintenance | 20%                   | Every sprint         |
| Innovation / exploration     | 10%                   | Every sprint or monthly |

**Innovation Funnel:**

```
Ideas (100) → Explore (10) → Experiment (3) → Incubate (1) → Integrate
                                            │
                                            └── Kill decisions at each gate

Gate criteria:
- Explore: aligns with strategic themes? Solves a real user problem?
- Experiment: prototype validated with 5+ users? Technical feasibility confirmed?
- Incubate: metrics show traction? Dedicated team committed?
- Integrate: absorbed by product team; becomes "core product work"
```

**Hackathon ROI:**
- **Structure**: 48 hours, cross-functional teams (eng + design + product), optional attendance
- **Theme**: tie to company strategy or customer pain points (not "build whatever")
- **Judging**: 30% innovation, 30% feasibility, 20% impact, 20% presentation
- **Outcome tracking**: 3-month follow-up: how many projects shipped to production?
- **Target**: >30% of hackathon projects ship within 6 months; <30% = either ideas aren't viable or follow-through is broken
- **Investment**: 2 days/quarter × entire eng team ≈ 2% of engineering time; cheap for the cultural and innovation ROI

### Phase 6 (~25 min): Vendor Evaluation

**RFI/RFP Process:**

```
Phase 0: Internal Alignment (before talking to vendors)
  - Document requirements: must-haves, nice-to-haves, anti-requirements
  - Define budget range internally
  - Identify decision-makers and approval process
  - Create evaluation scorecard with weighted criteria

Phase 1: RFI (Request for Information) — 5–10 vendors
  - Short questionnaire: capabilities, pricing model, SLAs, security certs
  - Eliminate obvious mismatches → narrow to 3–5

Phase 2: RFP (Request for Proposal) — 3–5 vendors
  - Detailed requirements document
  - Scored by evaluation committee against scorecard
  - Narrow to 2–3 finalists

Phase 3: Proof of Concept — 2–3 vendors
  - 2-week time-boxed PoC with real (sanitized) data
  - Test: integration effort, performance, edge cases, support quality
  - Select winner

Phase 4: Negotiation and Contract
  - Pricing: ask for multi-year discount; include termination for convenience
  - SLA: uptime guarantee, support response time, escalation path
  - Security: DPA, SOC 2 report, penetration test results, data residency
  - Exit plan: data export format, transition assistance, notice period
```

**Vendor Evaluation Scorecard:**

| Criterion                  | Weight | Vendor A | Vendor B | Vendor C |
|----------------------------|--------|----------|----------|----------|
| Feature fit (must-haves)   | 25%    | 8/10     | 7/10     | 9/10     |
| Integration effort          | 20%    | 6/10     | 8/10     | 5/10     |
| Total Cost of Ownership    | 20%    | 7/10     | 6/10     | 8/10     |
| Security & compliance       | 15%    | 9/10     | 8/10     | 7/10     |
| Vendor stability/viability  | 10%    | 7/10     | 9/10     | 6/10     |
| Support quality (from PoC)  | 10%    | 8/10     | 7/10     | 8/10     |
| **Weighted Score**          |        | **7.40** | **7.20** | **7.35** |

**Total Cost of Ownership Model (3-year):**

```
                     Year 1      Year 2      Year 3      TOTAL
License/Subscription $120,000    $150,000    $180,000    $450,000
Implementation       $80,000     $0          $0          $80,000
Integration           $40,000     $10,000     $10,000     $60,000
Training              $15,000     $5,000      $5,000      $25,000
Internal FTEs         $150,000    $150,000    $150,000    $450,000
Infrastructure        $20,000     $25,000     $30,000     $75,000
────────────────────────────────────────────────────────────────
TOTAL                $425,000    $340,000    $375,000   $1,140,000
```

**Build equivalent estimate:**
3 engineers × $180K/year × 3 years + cloud costs at $50K/year = $1,770,000
Decision: Buy ($1.14M < $1.77M) — unless this is a competitive differentiator.

**Red flags in vendor evaluation:**
- Won't provide a SOC 2 report or pen-test summary
- Pricing is "contact sales" with no transparency
- Reference customers are all in a different industry/size
- No public status page or incident history
- Product hasn't had a major release in 12+ months
- Key person dependency: "Our CTO will answer that" for every technical question


### Cross-skills Integration

This skill in a typical workflow chain:

| Step | Skill | What it produces for this skill |
|------|-------|---------------------------------|
| **Before** | ceo-strategist | Strategic vision, budget constraints, org design parameters — frames what's technically possible |
| **This** | cto-advisor | Technology strategy, build-vs-buy decisions, architecture governance, eng org design, vendor recommendations |
| **After** | system-architect | Consumes architecture decisions and governance framework to produce detailed system designs |

Common chains:
- **Tech strategy to implementation**: cto-advisor → system-architect → devops-engineer — Build-vs-buy → architecture design → infrastructure provisioning
- **Security hardening**: cto-advisor → security-engineer → devops-engineer — Risk assessment → security architecture → secure deployment
- **Vendor onboarding**: cto-advisor → cloud-architect → devops-engineer — Vendor selection → cloud integration design → deployment automation
- **Org restructure**: ceo-strategist → cto-advisor → system-architect — Org design → engineering team design → squad/tribe mapping

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
When this skill is invoked, drill into these specialized areas as needed:

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `build-vs-buy` | Every major technology decision — SaaS vs internal vs open-source customization | This file — Build vs Buy Cost Analysis |
| `tech-debt-management` | Quarterly technical health assessments; startup debt vs scale-up modernization vs enterprise legacy | This file — Tech Debt ROI Calculator |
| `architecture-governance` | Designing RFC processes, architecture review boards, and decision frameworks for 5 to 500-person orgs | This file + `system-architect` skill |
| `hiring-tech-team` | First engineer → VP Engineering → CTO transitions; generalist vs specialist hiring at each stage | This file — Hiring Timeline vs Outsourcing |
| `tech-due-diligence` | Fundraising, acquisition, or enterprise sales — what investors, acquirers, and customers evaluate | `references/` (create as needed) |
| `innovation-management` | R&D allocation, hackathons, 20% time: 0→1 innovation vs incremental improvement vs disruptive bets | `references/` (create as needed) |
| `vendor-evaluation` | Selecting SaaS, cloud, and infrastructure providers with 3-year total cost of ownership modeling | This file — Build vs Buy Cost Analysis |

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
The CTO bridges business strategy and technical execution. A CTO who doesn't coordinate with product builds systems nobody wants; one who doesn't coordinate with the CEO builds systems the company can't afford.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **CEO Strategist** | Fundraising, strategic pivots, hiring plan, major build vs buy decisions | Engineering capacity, technical feasibility of business goals, cost of delaying tech investment |
| **System Architect** | New system design, scaling events, architecture review, tech stack decisions | Business constraints (timeline, budget, team size), non-functional requirements, future growth projections |
| **Security Reviewer** | SOC 2/ISO prep, security incident, vendor selection, customer security reviews | Risk appetite, compliance deadlines, customer contractual obligations |
| **DevOps Engineer** | CI/CD strategy, infrastructure decisions, incident response, cost optimization | Deployment frequency targets, reliability SLOs, infrastructure budget, cloud vendor strategy |
| **Product Strategist** | Roadmap trade-offs, build vs buy, technical feasibility of features | Engineering capacity, technical debt level, architecture constraints |
| **Database Designer** | Schema design, data architecture, database selection, migration planning | Data growth projections, query patterns from product, compliance requirements |
| **Engineering Leads** | Hiring, team structure, tech debt prioritization, architecture decisions | Org changes, strategic direction, budget constraints, cross-team dependencies |
| **Data/Analytics** | Data infrastructure, analytics tooling, ML/AI strategy | Business questions to answer, data quality requirements, privacy constraints |
| **Finance / CFO** | Infrastructure budget, headcount planning, vendor contracts, build vs buy ROI | Cloud costs, headcount costs, vendor TCO, engineering productivity metrics |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Architecture change affecting 3+ services | System Architect, Engineering Leads, DevOps | Cascade analysis, migration plan, deployment coordination |
| Security incident | CEO, Security Reviewer, DevOps, Legal | Incident response, disclosure obligations, root cause timeline |
| Cloud cost spike (>50% week-over-week) | Finance, DevOps, CEO | Cost root cause, remediation plan, budget impact |
| Key technical hire accepted/rejected | CEO, Engineering Leads, Head of People | Team velocity impact, backup hiring plan |
| Major vendor contract decision (>$50K/yr) | Finance, CEO, DevOps (if infra) | TCO analysis, negotiation strategy, migration cost |
| Production outage > 1 hour | CEO, Product Strategist, DevOps, Engineering Leads | Customer impact, root cause, remediation timeline, postmortem schedule |
| Tech due diligence requested (investor/customer) | CEO, Engineering Leads, Security Reviewer | Documentation prep, architecture review, security posture summary |
| Build vs buy decision with >$100K implication | CEO, Finance, Product Strategist | TCO model, strategic implications, timeline trade-offs |

### Escalation Path

```
Existential technical risk (data loss, security breach, extended outage)
  └── CTO + CEO + Legal. Incident commander appointed. All-hands if >4 hours.

Strategic technical decision (architecture platform choice, major build vs buy)
  └── CTO + System Architect + Engineering Leads. CEO informed. Decision within 2 weeks.

Tactical technical decision (tooling, framework version, CI pipeline change)
  └── Engineering Lead handles. CTO informed via weekly 1:1. No escalation needed.
```

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Build what differentiates, buy everything else**: your engineering talent should work on things that create competitive advantage. Auth? Buy. Payments? Buy. Your secret sauce? Build.
- **Team design dictates architecture**: if you want loosely coupled services, create loosely coupled teams. Conway's Law is not negotiable.
- **Architecture decisions are reversible or irreversible**: reversible decisions (language choice within a service) → delegate to team. Irreversible decisions (database choice for core data, API contracts) → review broadly.
- **Technical debt is a financial instrument**: taken wisely, it accelerates delivery. Taken recklessly, it bankrupts velocity. Use the interest-rate framework.
- **Innovation doesn't happen by accident**: ring-fence time, create the funnel, celebrate shipping (not just building).
- **The best vendor evaluation is a working PoC**: RFP documents lie. Two weeks of integration reveals more than six months of sales calls.

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: You are the CTO + every engineer. Build-vs-buy = buy everything (Auth0, Supabase, Vercel). Tech debt is intentional — ship fast. No governance needed. Hiring = none yet.
- **What to skip**: Architecture review boards. RFC processes. Technology radars. Tech due diligence. Vendor scorecards (just use what works).
- **Coordination**: You talk to yourself. Document decisions in a `decisions.md` file.

### Small Team (2-10 people, 100-10K users)
- **What changes**: First engineering hires (generalists). Start build-vs-buy analysis for core infra. Lightweight ADRs for key decisions. Quarterly tech debt assessment. Simple tech radar (Adopt/Hold). Vendor evaluation for 2-3 critical services.
- **What to skip**: Formal ARB. Dual-track career ladder (too early). Platform team (stream-aligned teams are enough). Innovation funnel (just do hackathons).
- **Coordination**: Weekly eng sync (30 min). Monthly tech strategy review with CEO. Bi-weekly 1:1s. ADRs in shared repo.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: VP Engineering hired. Team Topologies emerge (stream-aligned + platform). Formal ARB with monthly cadence. RFC process for cross-cutting decisions. Technology radar reviewed quarterly. Dual-track career ladder. Innovation time (10-20% Fridays). Tech due diligence for enterprise deals.
- **What to skip**: Dedicated innovation team (embed in streams). Multi-year technology roadmaps (6-month rolling is enough). Full-time developer experience team.
- **Coordination**: ARB monthly. RFCs async in shared repo. Quarterly tech strategy review with board. Monthly skip-level 1:1s.

### Enterprise (50+ people, 1M+ users)
- **What changes**: CTO + VPs for each pillar. Multiple platform teams. ARB with formal voting. Enterprise architecture function. Compliance-driven governance (SOC 2, FedRAMP). Technology radar + lifecycle management. Dedicated DevEx team. M&A technical due diligence capability. Patent/IP strategy.
- **What's full production**: Architecture governance board with cross-BU representation. Annual technology strategy with board sign-off. Formal build-vs-buy with procurement partnership. Innovation lab + corporate venture arm.
- **Coordination**: ARB bi-weekly. Quarterly CTO council. Annual architecture summit. Board technology committee.

### Transition Triggers
- **Solo → Small**: You can't ship fast enough alone. First eng hire needed to maintain velocity. >100 active users.
- **Small → Medium**: Coordination overhead between 3+ teams becomes painful without process. First enterprise customer asks about architecture governance.
- **Medium → Enterprise**: Multiple business units need technology alignment. IPO or large M&A on horizon. SOC 2/ISO 27001 audit required.


### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Market timing wrong | Product launched too early (no demand) or too late (crowded) | Run demand validation with 10+ paid pre-orders before building; use Wardley Map to time your entry |
| Team can't execute | Key hires missing, wrong incentives, no clear owner | Hire for the next 6 months' problems, not the last 6 months'; DRI model with written OKRs |
| Runway < 12 months | Burn rate exceeds plan, revenue slower than projected | Cut burn to 18-month runway immediately; model best/worst/realistic case scenarios |
| Investor pass | Pitch doesn't articulate defensible moat | Lead with TAM → problem → traction → team → ask. Your demo is not your pitch. |
| Board misalignment | Founder/board disagree on strategy | Pre-board one-on-ones before every board meeting. Surface disagreement in the room, not after. |
| Scaling prematurely | Growing team/features before PMF | Sean Ellis test: < 40% "very disappointed" if product disappeared → do not scale |
| Co-founder conflict | Roles, equity, or vision disagreement | Written founder agreement with vesting, roles, decision rights, and exit terms |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Build-vs-buy evaluations documented with 5-year TCO comparison for all major infrastructure/procurement decisions
- [ ] **[S2]**  Technology radar maintained and reviewed quarterly; every technology categorized (Adopt/Trial/Assess/Hold)
- [ ] **[S3]**  Technical debt quantified (principal × interest rate) and prioritized in sprint planning
- [ ] **[S4]**  Engineering org design: stream-aligned teams with clear ownership; platform team exists if >3 stream teams
- [ ] **[S5]**  Dual-track career ladder with equivalent levels and compensation for IC and management tracks
- [ ] **[S6]**  RFC process documented and adopted; ADRs archived for all significant architecture decisions
- [ ] **[S7]**  ARB meets regularly; decisions default to team autonomy unless cross-cutting
- [ ] **[S8]**  Technical due diligence framework: code quality, architecture, team capability, infrastructure checklists
- [ ] **[S9]**  Innovation funnel with clear gates and metrics; hackathon projects tracked to production
- [ ] **[S10]**  Vendor evaluation scorecard with weighted criteria; TCO model for all major vendors

## References
<!-- QUICK: 30s -- links to deeper reading -->
- Team Topologies (Skelton & Pais): https://teamtopologies.com/
- Accelerate (Forsgren, Humble, Kim): https://itrevolution.com/product/accelerate/
- Architecture Decision Records: https://adr.github.io/
- Build vs Buy (a16z): https://a16z.com/build-vs-buy/
- Technical Due Diligence Checklist (YC): https://www.ycombinator.com/blog/technical-due-diligence/
- ThoughtWorks Technology Radar: https://www.thoughtworks.com/radar
- Conway's Law: https://martinfowler.com/bliki/ConwaysLaw.html
