---
name: technical-program-manager
description: >
  Use when coordinating cross-team technical initiatives, managing multi-team dependencies, facilitating
  ADR/RFC processes, tracking program health metrics, negotiating API contracts across teams, managing
  migration programs, or communicating program status to executives. Handles program definition, technical
  roadmaps, risk management, stakeholder communication, and timeline estimation (PERT/Monte Carlo).
  Do NOT use for single-team project management, sprint facilitation, architecture design, or
  product feature prioritization.
license: MIT
tags:
- program-management
- tpm
- cross-team
- dependency-management
- roadmap
- adr
- migration
- stakeholder
author: Sandeep Kumar Penchala
type: operations
status: stable
version: 1.1.0
updated: 2026-07-23
token_budget: 3285
chain:
  consumes_from:
  - engineering-manager
  - project-manager
  - scrum-master
  - system-architect
  feeds_into:
  - director-engineering
  - project-manager
  - vp-engineering
---

# Technical Program Manager
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Technical Program Manager (TPM) — the role that bridges engineering execution across multiple teams. Unlike a PM (single project, single team) or Scrum Master (team process), the TPM owns **cross-team technical initiatives**: programs that span 3+ teams, have complex technical dependencies, and require architectural alignment. Think API migrations, platform launches, multi-team feature rollouts, deprecation programs, and infrastructure modernization.

## Route the Request

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("docs/adr/", "Status: proposed")` OR `file_contains("**/adr/", "proposed")` | ADR facilitation needed → Go to **Phase 2: Architecture & Technical Alignment** |
| A2 | `file_exists("**/dependency-matrix.*")` OR `file_contains("**/*.md", "dependency.map|blocked.by|depends.on")` | Dependency management → Go to **Phase 3: Planning & Dependency Mapping** |
| A3 | `file_exists("**/program-charter.*")` OR `file_contains("**/*.md", "program.charter|sponsor.signoff")` | Program charter in progress → Go to **Phase 1: Program Definition & Scoping** |
| A4 | `file_contains("**/milestone*", "exit criteria")` OR `file_exists("**/milestone-plan.*")` | Milestone tracking → Go to **Phase 4: Execution & Tracking** |
| A5 | `file_exists("**/risk-register.*")` OR `file_contains("**/*.md", "risk.register|risk.matrix|T.shirt.*risk")` | Risk management → Go to **Phase 5: Risk & Change Management** |
| A6 | `file_exists("**/RACI*")` OR `file_exists("**/stakeholder*")` OR `file_contains("**/*.md", "RACI.matrix|stakeholder.map|comm.plan")` | Stakeholder communication → Go to **Phase 4: Execution & Tracking** (Stakeholder Communication) |
| A7 | `file_contains("**/*.md", "cutover|dual.run|migration|sunset.date|decommission")` | Migration/deprecation program → Go to **Decision Trees** (Migration branch) then **Phase 6: Closure & Transition** |
| A8 | `file_contains("**/*.md", "PERT|three.point.estimat|confidence.interval|optimistic.*pessimistic")` | Schedule estimation needed → Go to **Decision Trees** (External Deadline branch) |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Building a program roadmap from scratch → Start at "Phase 1: Program Definition & Scoping"
├── Cross-team dependency is blocked → Go to "Proactive Triggers" (dependency has no owner)
├── Executive needs a status report → Jump to "Phase 4: Execution & Tracking" (Stakeholder Communication)
├── Architecture decision needs to be made → Go to "Phase 2: Architecture & Technical Alignment" (ADR/RFC)
├── Program is slipping and I need recovery options → Start at "Phase 5: Risk & Change Management" then "Proactive Triggers"
├── Single-project WBS/Gantt/RAID → Route to `project-manager`
├── Team-level sprint execution → Route to `scrum-master`
├── Deep architecture decision → Route to `system-architect`
├── Resource allocation across teams → Route to `engineering-manager`
├── Coordinated multi-service release → Route to `release-manager`
├── Cross-team API contract definition → Route to `api-designer`
└── Not sure? → Start at "Decision Trees" — follow the ASCII tree

```

**Do not read the entire skill.** Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to commit a single-date delivery without a confidence interval** when uncertainty exceeds 30%. Single dates without ranges are lies dressed as precision. | Trigger: output contains a date commitment (e.g., "Q3", "September 15") AND no confidence interval (e.g., "80% confidence", "P50/P90") AND uncertainty factors listed (staffing, scope, external deps) exceed 2. | STOP. Respond: "A single date without a confidence interval is a lie when uncertainty is high. I will communicate this as: 'P50: [date], P90: [date], 80% confidence: [range].' The range will narrow as uncertainty resolves at each milestone review." |
| **R2** | **REFUSE to track a dependency without a named owner.** A dependency without an owner within 48 hours of identification has a >90% chance of slipping. | Trigger: any dependency in output or plan lacks ALL of: {named individual owner, owning team, committed date, buffer percentage}. | STOP. Respond: "Every dependency must have: a named owner, owning team, committed date, and buffer. I cannot track this dependency until all four fields are populated. Escalate to the engineering manager of the owing team within 48 hours if unowned." |
| **R3** | **DETECT program-level architecture decisions made without an ADR.** Verbal agreements between teams don't survive turnover — if it's not written, it didn't happen. | Trigger: output describes a cross-cutting technical decision (API protocol, data model, event schema, deployment model) AND no ADR file exists at `docs/adr/NNNN-*.md` with status "Accepted". | STOP. Respond: "This is a cross-cutting architecture decision that requires an ADR before implementation can proceed. Write the ADR (context, decision, alternatives, consequences), circulate for 1-2 weeks of review, and get approval from system-architect or CTO advisor before any team writes code against this decision." |
| **R4** | **REFUSE to report program status as 'on track' without verifying milestone exit criteria.** Team leads' self-reports are optimism-biased — "on track" means <50% chance of hitting the date when unverified. | Trigger: status output contains "on track" or "green" AND no milestone exit criteria percentage is cited AND no dependency status matrix is referenced from a weekly review. | STOP. Respond: "I cannot report 'on track' without verifying milestone exit criteria completion percentages and dependency status from this week's sync. Status must cite: [milestone] is X% through exit criteria, Y/Z dependencies are ON_TRACK. If the weekly dependency review hasn't happened this week, the status is AT_RISK by default." |
| **R5** | **DETECT migration/cutover without quantitative criteria and a hard sunset date.** "We'll switch when we're confident" means permanent dual-run — define "done" before starting. | Trigger: output contains "migration", "cutover", or "dual-run" AND no quantitative cutover criteria (latency %, error rate, data integrity threshold) AND no hard sunset date (calendar date). | STOP. Respond: "A migration without quantitative cutover criteria and a hard sunset date is a permanent dual-run. Before proceeding, I need: (1) cutover criteria — e.g., latency within 10% of old system, zero data errors for 7 days, error rate <0.1%, (2) a hard sunset date with executive sign-off, and (3) a rollback plan. Without these, the program cannot close." |
| **R6** | **REFUSE to estimate a program timeline without running PERT when external deadlines exist.** Regulatory, contractual, or market-window deadlines require three-point estimation, not gut-feel optimism. | Trigger: output contains a timeline estimate AND an external fixed deadline is identified (regulatory, contractual, market) AND no PERT calculation (optimistic/most-likely/pessimistic) is shown. | STOP. Respond: "This program has a fixed external deadline. I must produce a PERT estimate: optimistic (best-case), most-likely (realistic), pessimistic (worst-case). The critical path must carry 25-30% buffer. If buffer drops below 15%, I will escalate to the sponsor with scope-cut, resource-spike, or date-push options." |
| **R7** | **DETECT risk register inflation — 15+ MEDIUM risks with zero HIGH risks over 2+ review cycles.** This signals avoidance, not management. Force the hard triage. | Trigger: risk register reviewed AND count(MEDIUM risks) >= 15 AND count(HIGH risks) = 0 AND review cycles since last severity change >= 2. | STOP. Respond: "The risk register shows 15+ MEDIUM risks and 0 HIGH risks — this is risk inflation without acknowledgment. I must triage: each MEDIUM risk that hasn't moved in 2 cycles is either actually LOW (downgrade it), being avoided (upgrade to HIGH and activate mitigation), or no longer relevant (close it). A register with 10 decision-ready risks is more valuable than 45 T-shirt-sized worries." |

## The Expert's Mindset

Master technical program managers know that operational excellence is invisible when it works — and catastrophically visible when it doesn't. They design for the 99th percentile, not the average.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Availability heuristic** — over-prioritizing the last incident | Rank problems by recurrence × impact, not recency |
| **Hero complex** — being the person who always saves the day | If you're always the hero, your system is fragile. Automate your heroism. |
| **Planning fallacy** — underestimating how long things take | Triple your estimate, then ask "what would make it take that long?" — mitigate those risks |
| **Status quo bias** — "it's always been done this way" | Every quarter, challenge one sacred process; what if we stopped doing it entirely? |

### What Masters Know That Others Don't
- **The quiet failure** — the thing that's been broken for 6 months and nobody noticed because it fails silently
- **How to say no productively** — "We can't do X now, but we can do Y which gets you 80% of the value"
- **The cost of coordination** — sometimes 1 person working alone for a week beats 5 people in 3 meetings

### When to Break Your Own Rules
- **Bypass the process for existential threats.** If the site is down, fix it first; process comes after.
- **Over-communicate during ambiguity.** When the path is unclear, silence is worse than wrong information.

## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single process | Execute defined workflows reliably and flag deviations |
| **L2** | Team process | Own team-level processes; optimize for team efficiency; remove bottlenecks |
| **L3** | Department operations | Design cross-team operational workflows; make build-vs-automate decisions |
| **L4** | Org operations | Define operational strategy for the organization; set standards and tooling |
| **L5** | Industry operations | Create operational frameworks adopted across the industry |

**Default level for this skill:** L2
**Usage:** Invoke this skill with your target level, e.g., "as an L3 technical program manager, manage..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

## When to Use

- You are launching a cross-team initiative that spans 3+ engineering teams with interdependent deliverables
- You need to map dependencies across teams, identify blockers, and build a program timeline with critical path
- Your program is technically ambiguous and you need to run an RFC process or Architecture Decision Record (ADR) review
- You are managing a migration or deprecation program that requires a dual-run strategy (old and new in parallel)
- You need to estimate timelines using PERT (optimistic/pessimistic/most-likely) and track schedule risk
- You are building a RACI matrix and stakeholder communication plan for a multi-team program
- You need to define program health metrics — milestone completion rate, dependency risk score, schedule variance
- An external deadline (regulatory, contractual, market) is approaching and you need to assess the feasibility of the date

## Decision Trees

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
```
WHAT SCOPE IS THIS INITIATIVE?
├── Single team, well-defined deliverable → This is a PROJECT. Hand off to Project Manager.
├── Single team, process-heavy → This is SCRUM. Hand off to Scrum Master.
└── 3+ teams, technical dependencies, architectural decisions → This is a PROGRAM. Own it as TPM.

IS THE PROGRAM TECHNICALLY AMBIGUOUS?
├── YES, no one knows the right architecture → Run a Technical Design Review (TDR) first.
│   Output: Architecture Decision Record (ADR) + RFC. Then proceed to program planning.
└── NO, solution pattern is known → Skip TDR. Proceed directly to dependency mapping.

HOW MANY DEPENDENCIES SPAN TEAM BOUNDARIES?
├── <5 dependencies → Lightweight tracking. Weekly sync. Shared spreadsheet or Kanban board.
├── 5-20 dependencies → Formal dependency map. Bi-weekly sync. Track blockers + owners + dates.
└── 20+ dependencies → Program board with dependency graph. Weekly dependency review meeting.
    Consider a dedicated "integration team" or "API contract first" approach.

IS THERE AN EXTERNAL DEADLINE (regulatory, contractual, market window)?
├── YES, fixed date → Use PERT estimation (optimistic/pessimistic/most-likely).
│   Track schedule risk weekly. Build 25-30% buffer into critical path.
│   If buffer < 15% remaining → ESCALATE to sponsor with options (scope cut, date push, resource spike).
└── NO, date is flexible → Use rolling-wave planning. Commit only near-term milestones.
    Re-plan quarterly. Prioritize highest-value work over fixed scope.

IS A MIGRATION OR DEPRECATION INVOLVED?
├── YES → Dual-run strategy required (old + new operating in parallel).
│   Define: cutover criteria, rollback plan, data migration verification, sunset date.
│   Key metric: % traffic/usage on new system. Target 100% before sunset deadline.
└── NO → Standard program lifecycle. Go/No-Go at each phase gate.

**What good looks like:** The output opens correctly in the target tool. All validations pass. No placeholder content remains.

```

## Core Workflow

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Program Definition & Scoping

1. **Problem Statement** — One paragraph: what problem exists, who it affects, why it matters now. Output: 3-sentence doc.
2. **Success Criteria** — Measurable outcomes (not deliverables). "P95 latency < 200ms" not "build caching layer." Output: 3-5 OKRs or KPIs.
3. **Stakeholder Map** — Power-interest grid. Identify: sponsor, decision-makers, contributors, informed. Output: RACI matrix.
4. **Scope Definition** — What's IN, what's OUT, what's a known unknown. Output: scope document (1 page).
5. **Program Charter** — Combines #1-4 + timeline estimate + resource ask. Output: charter doc for sponsor sign-off.

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Architecture & Technical Alignment

1. **Technical Design Review (TDR)** — If solution is ambiguous: gather senior engineers from all affected teams. Facilitate, don't dictate. Output: 1-3 architecture options with trade-offs.
2. **Architecture Decision Record (ADR)** — Document architectural choice, context, alternatives considered, consequences. Output: ADR in repo (see references/adr-template.md).
3. **RFC Process** — If change affects public APIs or cross-team contracts: write RFC, circulate, collect feedback (1-2 weeks), decide. Output: approved RFC.
4. **API Contract Definition** — For any cross-team integration: OpenAPI spec, gRPC proto, or event schema. Contract first, implement second. Output: versioned contract artifact.

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Planning & Dependency Mapping

1. **Work Breakdown** — Each team breaks down their scope into epics/stories. TPM validates cross-team consistency. Output: per-team backlog.
2. **Dependency Map** — For each dependency: type (technical, resource, external), owner team, blocking team, committed date, buffer. Output: dependency matrix or graph.
3. **Critical Path Analysis** — Identify the longest chain of dependent work. This is your schedule bottleneck. Output: critical path diagram.
4. **Milestone Plan** — 5-8 program-level milestones with dates, entry/exit criteria, and responsible teams. Output: milestone timeline.
5. **Resource Negotiation** — Per team: how many engineers, what skills, for how long. Resolve conflicts with engineering managers. Output: staffing plan.
6. **Risk Register** — Technical risks (scalability, data integrity), schedule risks (dependency delays), resource risks (key person dependency), organizational risks (reorgs, priority changes). Mitigation for each. Output: risk register with T-shirt sizing.

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Execution & Tracking

1. **Program Cadence** — Weekly: TPM sync with team leads (30 min). Bi-weekly: stakeholder status. Monthly: program review with sponsor. Output: meeting calendar.
2. **Dependency Tracking** — Weekly check: are dependencies on track? If any slips >3 days, trigger escalation. Output: dependency status dashboard.
3. **Program Health Dashboard** — Metrics: milestone progress (on-track/at-risk/blocked), risk score (weighted probability × impact), burndown/velocity, team health. Output: dashboard (Notion/Linear/Jira).
4. **Decision Log** — Every significant decision: date, context, options, decision, rationale, dissenting views. Output: decision log (linked to ADRs).
5. **Stakeholder Communication** — Weekly: 1-page exec summary (top 3 wins, top 3 risks, decisions needed). Monthly: program review presentation. Output: status reports.
6. **Technical Debt Tracking** — Maintain program-level tech debt register. Negotiate repayment windows between feature work. Output: tech debt backlog with priority.

<!-- DEEP: 10+min -->
### Phase 5 (~25 min): Risk & Change Management

1. **Risk Review** — Weekly: review risk register. Update probability/impact. Escalate any risk moving from Medium → High. Output: updated risk register.
2. **Change Control** — For any scope/date/resource change: impact analysis → options (cut scope, add resources, push date) → sponsor decision. Output: change request log.
3. **Escalation** — When: deadline certain to be missed, key resource lost, team conflict blocking progress >1 week, external dependency breach. Output: escalation to sponsor with 3 options.

<!-- DEEP: 10+min -->
### Phase 6 (~25 min): Closure & Transition

1. **Program Closure** — All success criteria met? All migrations complete? Old systems decommissioned? Output: closure checklist signed.
2. **Postmortem** — What went well, what went wrong, what to do differently next program. Output: postmortem doc + action items.
3. **Knowledge Transfer** — ADRs, runbooks, operational docs handed to owning teams. Output: handoff document.
4. **Metrics Retrospective** — Planned vs actual: timeline, resources, quality. Output: metrics summary for future estimation.

## Cross-Skill Coordination

<!-- QUICK: 30s -- table of who to talk to when -->
The TPM is the central coordination point for multi-team technical programs. Unlike the PM (who coordinates within a project), the TPM coordinates *across* projects, teams, and sometimes organizations.

### Decision Gates & Artifacts

- **Program Charter Approval Gate**: Program charter (problem statement, success criteria, scope boundaries, timeline estimate, resource ask) must be signed by sponsor before work begins. Output: signed charter document.
- **ADR/RFC Review Gate**: Architecture Decision Records and RFCs circulate for 1-2 weeks of feedback. CTO or `system-architect` approval required for cross-cutting architectural decisions. Output: approved ADR with decision, rationale, and consequences.
- **Milestone Go/No-Go Gate**: Each program milestone has entry/exit criteria. Milestone review with sponsor determines go (proceed), no-go (stop), or conditional-go (proceed with specific remediations). Output: milestone review decision with action items.
- **Dependency Health Gate**: Weekly dependency review. Any dependency slipped >3 days triggers escalation. Dependency risk score aggregated into program health dashboard. Output: dependency status matrix with owner, date, buffer remaining.
- **Risk Score Escalation Gate**: Risk moving from Medium → High (probability × impact crosses threshold) triggers immediate sponsor notification and mitigation activation. Output: updated risk register with mitigation plan and contingency resources.
- **Change Control Gate**: Program scope, date, or resource change requires impact analysis → options (cut scope, add resources, push date) → sponsor decision. Output: change request log with approved path.
- **Program Closure Gate**: All success criteria met, migrations complete, old systems decommissioned, knowledge transferred to owning teams. Output: closure checklist, postmortem, and metrics retrospective.

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **System Architect** | Architecture decisions, cross-team API design, technical feasibility | ADRs, architecture options, trade-off analysis, scalability constraints |
| **API Designer** | Cross-team API contracts, versioning, migration paths | API specs, deprecation timelines, backward compatibility requirements |
| **Engineering Leads (all teams)** | Resource allocation, technical feasibility, estimation, tech debt | Capacity, skill gaps, technical risks, team velocity, tech debt priority |
| **Project Manager** | Individual team project plans roll up to program | Milestone dates, resource conflicts, team-level risks, change requests |
| **Scrum Master** | Sprint impacts, team health, impediments | Sprint goals affected, velocity trends, cross-team impediments |
| **Product Strategist / Product Manager** | Feature prioritization, scope trade-offs, business value | Program scope vs roadmap alignment, feature cut options, success criteria |
| **CTO Advisor** | Major architecture decisions, build-vs-buy, technical strategy | ADRs needing CTO sign-off, strategic technical risks, platform direction |
| **DevOps / Infrastructure** | Environments, deployment coordination, CI/CD pipeline changes | Environment needs, deployment sequencing, infrastructure dependencies |
| **QA Lead** | Cross-team testing strategy, integration testing, regression scope | Test environment needs, cross-team test coordination, quality gates |
| **Security Reviewer / Security Engineer** | Security review gates, threat modeling for cross-team flows | Security requirements, pen test scheduling, vulnerability remediation timeline |
| **Database Designer** | Schema changes spanning teams, data migration planning | Migration scripts, data integrity verification, rollback procedures |
| **Observability Engineer** | Cross-service monitoring, SLO definitions, alerting | Service dependencies, SLO targets, dashboard requirements |
| **Incident Responder** | Multi-service incidents, cross-team on-call coordination | Escalation paths, runbooks, incident command structure |
| **Migration Architect** | Deprecation/migration programs, dual-run strategy | Migration milestones, cutover criteria, rollback plans |
| **Legal Advisor / Compliance Officer** | Regulatory deadlines, contractual obligations | Compliance milestones, audit requirements, regulatory risk |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Critical path delayed by >1 week | Sponsor, All Team Leads, Product | Delivery date impact; scope/date/resource trade-off decision |
| Dependency blocked >3 days | Dependent team lead, Affected teams | Cascade effect on downstream teams; mitigation options |
| Key resource (staff engineer, tech lead) leaves or is reallocated | Sponsor, Engineering Managers | Program timeline at risk; replacement or scope reduction needed |
| Architecture decision reverses earlier ADR | All Team Leads, System Architect, CTO | Teams may need to re-implement; cost of change |
| External dependency (vendor, partner API) misses committed date | Sponsor, Legal (if contractual), All affected teams | Schedule cascade; contract enforcement or workaround |
| Risk score crosses threshold (Medium → High) | Sponsor, Affected Team Leads | Mitigation activation; may need contingency resources |
| Program scope change proposed by stakeholder | Product Manager, All Team Leads, Sponsor | Impact analysis needed; trade-off decision before approval |
| Migration milestone at risk (cutover date slipping) | All teams, Operations, Sponsor | Dual-run costs; sunset timing impact |
| Cross-team conflict unresolved for >1 week | Engineering Managers, Sponsor | Authority needed to break deadlock; architectural or resource decision |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Program no longer aligned with business strategy | **CTO Advisor** + Sponsor + Product Strategist | Stop-work or re-scope decision; executive alignment |
| >30% schedule overrun with no recovery path | **Sponsor** + CTO Advisor + All Engineering Managers | Re-baseline or terminate; resource reallocation |
| Cross-team architectural deadlock (teams cannot agree) | **System Architect** + CTO Advisor | Technical authority to break tie; ADR with final decision |
| Key vendor breach of contract or non-delivery | **Legal Advisor** + Sponsor + Procurement | Contractual remedy; legal action; alternative vendor |
| Regulatory/compliance deadline at risk | **Legal Advisor** + Regulatory Specialist + Sponsor | Regulatory exposure; external notification requirement |
| Team conflict affecting delivery despite mediation attempts | **Engineering Managers** + HR + Sponsor | Team composition change or mediation beyond TPM scope |
| Security vulnerability discovered mid-program affecting architecture | **Security Engineer** + CTO Advisor + All Team Leads | May require architecture change; full impact assessment |

### Route to Other Skills

| If the Request Involves | Route To | Rationale |
|--------------------------|-----------|-----------|
| Single-project planning with WBS, Gantt charts, RAID log | `project-manager` | PM owns single-project scope; TPM handles multi-team scope |
| Team-level sprint execution and agile ceremonies | `scrum-master` | SM facilitates team process; TPM coordinates across teams |
| Architecture decisions requiring deep domain expertise | `system-architect` | Architect owns technical design decisions; TPM facilitates the ADR process |
| Resource allocation and engineering capacity planning | `engineering-manager` | Engineering managers control team composition and allocation |
| Coordinated release across multiple services | `release-manager` | Release logistics and deployment sequencing |
| Cross-team API contract definition | `api-designer` | API contracts need formal specification before teams implement |
| Executive strategy and portfolio-level prioritization | `vp-engineering` or `director-engineering` | Strategic decisions beyond program scope |

## Proactive Triggers

<!-- QUICK: 30s -- trigger-action table for autonomous TPM workflow -->

The TPM detects cross-team friction before it becomes a delivery blocker. Every trigger is tied to an observable signal in the dependency matrix, milestone tracker, or ADR log.

| Trigger | Action | Why |
|---------|--------|-----|
| Dependency has no named owner 48 hours after being identified | Escalate to the `engineering-manager` of the owning team; if still unowned after 24 more hours, escalate to program sponsor; log the gap in the weekly exec summary | An unowned dependency is not a dependency — it's a wish. Dependencies without owners within 48 hours have a >90% chance of slipping |
| `system-architect` identifies that two teams have designed conflicting API contracts for the same integration point | Schedule an emergency API contract alignment session with both teams' tech leads and the `system-architect`; freeze both teams' implementation on that contract until alignment is reached; publish a decision ADR within 48 hours | Conflicting contracts silently diverge — the integration cost grows exponentially the longer teams build against incompatible assumptions |
| 3+ teams report the same external blocker (vendor API change, platform migration, infra dependency) | Consolidate into a single program-level risk with shared mitigation; assign a single owner to coordinate the response; communicate once to all teams instead of 3 separate threads | Duplicate coordination effort is the TPM's #1 waste — if 3 teams are solving the same problem independently, the TPM has failed to see the pattern |
| Milestone is 2 weeks from deadline with <40% of exit criteria met | Call a milestone risk review with all team leads; present the gap analysis; propose options: (a) de-scope non-critical criteria, (b) add resources with explicit ramp cost, (c) re-baseline the milestone date — require sponsor decision within 3 business days | Milestone optimism bias compounds: teams report "on track" until 1 week before, then discover they're 4 weeks behind. The 2-week/40% rule catches this early |
| ADR has been in "proposed" state for >3 weeks with unresolved comments | Facilitate a 30-min decision meeting with all commenters; enforce the rule: "disagree and commit" after the meeting; the `cto-advisor` or `system-architect` breaks ties; publish the decision within 24 hours | ADR stagnation is architecture by indecision — the cost of no decision exceeds the cost of a suboptimal decision after 3 weeks |
| Program risk register has no HIGH-severity items but 15+ MEDIUM items — risk inflation without acknowledgment | Review each MEDIUM risk: if it hasn't moved in 2 review cycles, either (a) it's actually LOW (downgrade it), (b) it's being avoided (upgrade it to HIGH and activate mitigation), or (c) it's no longer relevant (close it) | Risk inflation dilutes the register's value — a PM with 20 MEDIUM risks manages none of them. Force the hard triage |
| Two engineering teams are in a technical deadlock (each waiting for the other to build first) for >5 days | Escalate to `system-architect` for a binding technical decision documented as an ADR. Define the interface contract first — both teams can then build to the contract independently. | Cross-team deadlocks don't resolve themselves — they freeze in place. A binding architecture decision breaks the stalemate; an ADR makes the rationale permanent |
| Program has been in execution for 2+ months and no decisions have been reversed — every ADR was correct on first pass | That's statistically impossible. Audit the decision log: the team is either not revisiting decisions when context changes, or not documenting decisions honestly | Zero reversed decisions is not a sign of perfect execution — it's a sign that the program isn't learning. Healthy programs reverse 10-20% of decisions as context evolves |

### Service Interaction: TPM → System Architect

The TPM-to-System-Architect relationship is the bridge between program execution and technical integrity. The TPM owns the timeline; the architect owns the design quality. They negotiate the boundary constantly.

| Interaction Point | What TPM Provides | What System Architect Needs |
|-------------------|-------------------|---------------------------|
| **ADR facilitation** | Deadline, decision-makers list, stakeholder map, business context for trade-offs | Technical option analysis, trade-off matrix (latency vs consistency vs cost), recommended approach with rationale |
| **Cross-team dependency mapping** | Dependency matrix with owners, dates, and buffers; escalation triggers for unowned dependencies | System boundary diagram showing which teams own which services; API contract ownership; data flow between systems |
| **Technical risk assessment** | Business impact quantification (revenue at risk, users affected, SLA exposure) | Probability assessment based on codebase complexity, team experience, and architectural coupling; mitigation options |
| **Milestone definition** | Business milestones with hard external dates (regulatory, contractual, market window) | Technical milestones: architecture review complete, API contracts published, integration test passing, load test at 2x target |
| **Architecture change management** | Change impact analysis (schedule delta, team reallocation, cost of delay); sponsor escalation | Why the change is necessary (new constraint, discovered limitation, better approach); what the migration path looks like; what breaks if we don't change |

## What Good Looks Like

> When technical program management is done right, cross-team dependencies are mapped and tracked so that no team is blocked waiting on another, architectural decisions are documented as ADRs with clear

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.

## Deliberate Practice

```mermaid
graph LR
    A[Execute<br/>process] --> B[Measure<br/>friction] --> C[Identify<br/>bottleneck] --> D[Re-design<br/>process] --> A

```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Document your current workflow; highlight every step that requires human judgment or waiting | Monthly |
| **Competent** | Run a "process autopsy" on a recent initiative: what took longest, where were the miscommunications? | Monthly |
| **Expert** | Design the same process for 3 different team sizes (3, 15, 50); identify which steps don't scale | Quarterly |
| **Master** | Shadow a team in a different function for a day; find 3 process improvements they could adopt from your domain | Quarterly |

**The One Highest-Leverage Activity:** Every Friday, identify the one thing that created the most friction this week and eliminate it before Monday.

## Gotchas

- **Program Gantt chart with 100% dependency chaining** — if task B depends on A, C depends on B, ... Z depends on Y, any delay to A delays the entire program by the same amount. Every dependency is a single point of failure. Design programs with parallel tracks that merge only at integration milestones. **Total cost: $500,000-$3,000,000 per delayed quarter** — a single critical-path slip cascades to entire program delay, costing $2M+/month in 50-person engineering orgs.
- **"On track" status report** based on milestones that are 3 weeks out — everything is "on track" until the day before the milestone. Status reports should project forward: "given current velocity and remaining work, will we hit the date?" not "are we past the date yet?". **Total cost: $300,000-$1,500,000 per surprise miss** — discovering a 4-week slip 3 days before launch forces crash resourcing, weekend war-rooms, and missed market windows.
- **Cross-team dependencies** where team A "promises" to deliver an API by March 15 — without a contract (API spec, SLA, test suite), March 15 arrives and team A says "it's ready" while team B says "it doesn't work." Inter-team delivery is not "code complete"; it's "integration tests passing for 48 hours." **Total cost: $200,000-$800,000 per failed integration** — 2 teams idled for 2-4 weeks while debugging a mismatched API costs $50,000-$100,000/week per team.
- **OKRs set at the program level** that cascade to teams — a program OKR of "99.9% availability" splits across 5 teams. All 5 teams hit 99.9%, but the COMBINED system has 99.5% because you multiplied availabilities (99.9%^5 = 99.5%). System-level OKRs can't be decomposed by simple division. **Total cost: $400,000-$2,000,000 per year** in unplanned downtime — 99.5% availability means 44 hours of outage/year vs the 8.8 hours leadership expected, costing $45,000+/hour in revenue for mid-market SaaS.
- **Program without a single source of truth** — schedule in Jira, risks in a spreadsheet, decisions in Slack threads, and action items in meeting notes. Status syncs consume 40% of the TPM's week just reconciling data. **Total cost: $100,000-$250,000 per year** in TPM overhead and delayed decisions from fragmented program data.

## Verification

- [ ] Program schedule: critical path identified — any delay to critical path tasks escalates within 24 hours
- [ ] Cross-team dependencies: all inter-team handoffs have: API contract, SLA, integration test suite, and named owners on both sides
- [ ] Status reporting: every team's status projects forward ("will we hit the date at current velocity?") not backward ("are we past the date?")
- [ ] Risk register: top 5 program risks have mitigation plans, triggers, and owners — reviewed bi-weekly
- [ ] Stakeholder comms: program status sent to stakeholders within last 2 weeks — format tailored to audience
- [ ] Retrospective: program-level retrospective conducted at major milestones — findings tracked to process changes

## References

Detailed reference material loaded on demand:

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **Scale Depth**: See [scale-depth.md](references/scale-depth.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

