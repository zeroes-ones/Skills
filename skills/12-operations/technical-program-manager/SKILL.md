---
name: technical-program-manager
description: "Technical Program Manager (TPM) for cross-team technical initiatives. Program definition, multi-team dependency mapping, technical roadmaps, stakeholder communication (RACI, dashboards), risk management, ADR/RFC process, program health metrics, resource negotiation, change management, timeline estimation (PERT/Monte Carlo), API contract negotiation, migration program management. [KEYWORDS: technical program manager, TPM, cross-team initiative, program management, dependency management, technical roadmap, multi-team coordination]"
author: Sandeep Kumar Penchala
type: operations
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - technical-program-manager
token_budget: 3285
output:
  type: "code"
  path_hint: "./"
---
# Technical Program Manager

Technical Program Manager (TPM) — the role that bridges engineering execution across multiple teams. Unlike a PM (single project, single team) or Scrum Master (team process), the TPM owns **cross-team technical initiatives**: programs that span 3+ teams, have complex technical dependencies, and require architectural alignment. Think API migrations, platform launches, multi-team feature rollouts, deprecation programs, and infrastructure modernization.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

What are you trying to do?
├── Building a program roadmap → Start at "Roadmap & Milestone Planning" under Sub-Skills
├── Cross-team coordination → Go to "Dependency Management" under Sub-Skills
├── Managing dependencies across teams → Jump to "Dependency Management" under Sub-Skills
├── Tracking a cross-team initiative → Go to "Program Scoping" then "Roadmap & Milestone Planning"
├── Executive reporting → Jump to "Stakeholder Communication" under Sub-Skills
├── Resource planning across programs → Go to "Risk & Change Management" under Sub-Skills
├── Managing program-level risk → Jump to "Risk & Change Management" under Sub-Skills
└── Don't know where to start? → Start at "Program Scoping"

**Do not read the entire skill.** Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never coordinate across teams without clear ownership per deliverable.** Every dependency needs a named owner and committed date.
- **Dependency management needs buffer — things will slip.** Plan 20-30% buffer on cross-team dependencies.
- **Executive reporting must be honest about risks, not optimistic for comfort.** Red status today beats a surprise failure next month.
- **Always run an RFC or ADR for cross-cutting technical decisions.** Verbal agreements between teams don't survive turnover.
- **Stakeholder communication should match the audience.** C-suite needs summaries; engineering teams need technical detail.
- **Admit what you don't know.** If a team's architecture or capacity is unclear, escalate and clarify before committing.

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
### Phase 1 (~15 min): Program Definition & Scoping

1. **Problem Statement** — One paragraph: what problem exists, who it affects, why it matters now. Output: 3-sentence doc.
2. **Success Criteria** — Measurable outcomes (not deliverables). "P95 latency < 200ms" not "build caching layer." Output: 3-5 OKRs or KPIs.
3. **Stakeholder Map** — Power-interest grid. Identify: sponsor, decision-makers, contributors, informed. Output: RACI matrix.
4. **Scope Definition** — What's IN, what's OUT, what's a known unknown. Output: scope document (1 page).
5. **Program Charter** — Combines #1-4 + timeline estimate + resource ask. Output: charter doc for sponsor sign-off.

### Phase 2 (~30 min): Architecture & Technical Alignment

1. **Technical Design Review (TDR)** — If solution is ambiguous: gather senior engineers from all affected teams. Facilitate, don't dictate. Output: 1-3 architecture options with trade-offs.
2. **Architecture Decision Record (ADR)** — Document architectural choice, context, alternatives considered, consequences. Output: ADR in repo (see references/adr-template.md).
3. **RFC Process** — If change affects public APIs or cross-team contracts: write RFC, circulate, collect feedback (1-2 weeks), decide. Output: approved RFC.
4. **API Contract Definition** — For any cross-team integration: OpenAPI spec, gRPC proto, or event schema. Contract first, implement second. Output: versioned contract artifact.

### Phase 3 (~20 min): Planning & Dependency Mapping

1. **Work Breakdown** — Each team breaks down their scope into epics/stories. TPM validates cross-team consistency. Output: per-team backlog.
2. **Dependency Map** — For each dependency: type (technical, resource, external), owner team, blocking team, committed date, buffer. Output: dependency matrix or graph.
3. **Critical Path Analysis** — Identify the longest chain of dependent work. This is your schedule bottleneck. Output: critical path diagram.
4. **Milestone Plan** — 5-8 program-level milestones with dates, entry/exit criteria, and responsible teams. Output: milestone timeline.
5. **Resource Negotiation** — Per team: how many engineers, what skills, for how long. Resolve conflicts with engineering managers. Output: staffing plan.
6. **Risk Register** — Technical risks (scalability, data integrity), schedule risks (dependency delays), resource risks (key person dependency), organizational risks (reorgs, priority changes). Mitigation for each. Output: risk register with T-shirt sizing.

### Phase 4 (~15 min): Execution & Tracking

1. **Program Cadence** — Weekly: TPM sync with team leads (30 min). Bi-weekly: stakeholder status. Monthly: program review with sponsor. Output: meeting calendar.
2. **Dependency Tracking** — Weekly check: are dependencies on track? If any slips >3 days, trigger escalation. Output: dependency status dashboard.
3. **Program Health Dashboard** — Metrics: milestone progress (on-track/at-risk/blocked), risk score (weighted probability × impact), burndown/velocity, team health. Output: dashboard (Notion/Linear/Jira).
4. **Decision Log** — Every significant decision: date, context, options, decision, rationale, dissenting views. Output: decision log (linked to ADRs).
5. **Stakeholder Communication** — Weekly: 1-page exec summary (top 3 wins, top 3 risks, decisions needed). Monthly: program review presentation. Output: status reports.
6. **Technical Debt Tracking** — Maintain program-level tech debt register. Negotiate repayment windows between feature work. Output: tech debt backlog with priority.

### Phase 5 (~25 min): Risk & Change Management

1. **Risk Review** — Weekly: review risk register. Update probability/impact. Escalate any risk moving from Medium → High. Output: updated risk register.
2. **Change Control** — For any scope/date/resource change: impact analysis → options (cut scope, add resources, push date) → sponsor decision. Output: change request log.
3. **Escalation** — When: deadline certain to be missed, key resource lost, team conflict blocking progress >1 week, external dependency breach. Output: escalation to sponsor with 3 options.

### Phase 6 (~25 min): Closure & Transition

1. **Program Closure** — All success criteria met? All migrations complete? Old systems decommissioned? Output: closure checklist signed.
2. **Postmortem** — What went well, what went wrong, what to do differently next program. Output: postmortem doc + action items.
3. **Knowledge Transfer** — ADRs, runbooks, operational docs handed to owning teams. Output: handoff document.
4. **Metrics Retrospective** — Planned vs actual: timeline, resources, quality. Output: metrics summary for future estimation.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
The TPM is the central coordination point for multi-team technical programs. Unlike the PM (who coordinates within a project), the TPM coordinates *across* projects, teams, and sometimes organizations.

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

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, < 2 teams)
- **What changes**: No formal program. You ARE the program. Lightweight dependency tracking in a todo list.
- **What's overkill**: RACI, formal ADRs, program dashboards, milestone plans, PERT estimation, dedicated program reviews.
- **Coordination needs**: Async updates in Slack. Bi-weekly check-in with stakeholder. No cross-team ceremonies.
- **Cost implications**: $0 tools. Time cost: 2-4 hours/week on program overhead.
- **Transition trigger to Small**: Adding a second team OR an external dependency OR a fixed deadline >1 month out.

### Small (2-10 people, 3-5 teams)
- **What changes**: Formal dependency map. Weekly TPM sync (30 min). Written status updates. Risk register (top 10).
- **What's overkill**: Program dashboards, dedicated program manager tooling, formal change control board, PERT/Monte Carlo estimation (use three-point estimates instead).
- **Coordination needs**: Weekly sync with all team leads. Bi-weekly stakeholder update (1-page). Dependency tracking spreadsheet.
- **Cost implications**: $0-200/year. Time cost: 8-12 hours/week. Shared spreadsheet or GitHub Projects for tracking.
- **Transition trigger to Medium**: 5+ teams OR 20+ cross-team dependencies OR 3+ concurrent programs OR external regulatory deadline.

### Medium (10-50 people, 5-15 teams)
- **What changes**: Full program management. RACI for every workstream. Formal ADR process. Program dashboard. Weekly dependency review. Dedicated TPM (full-time). Change control process. PERT estimation for critical path.
- **What's overkill**: Monte Carlo simulation (use PERT), dedicated program management office (PMO), portfolio-level tracking, earned value management.
- **Coordination needs**: TPM runs weekly dependency sync (all team leads). Bi-weekly program review with sponsor. Monthly steering committee. Program dashboard auto-updated. Decision log maintained.
- **Cost implications**: $500-5K/year on tools (Linear/Notion/Jira Premium). Time cost: full-time TPM + fractional support from team leads.
- **Transition trigger to Enterprise**: 15+ teams OR 3+ concurrent programs sharing resources OR >$1M program budget OR C-level sponsor OR enterprise compliance requirements.

### Enterprise (50+ people, 15+ teams, multiple programs)
- **What changes**: Program Management Office (PMO) or portfolio TPM team. Resource capacity planning tools (Float, Resource Guru). Formal phase-gate reviews. Monte Carlo simulation for schedule confidence. Earned value management. Standardized charter/RFC/ADR templates. Executive dashboard with portfolio view.
- **What's overkill**: Nothing is overkill at this scale, but avoid process for process's sake — every artifact must have a consumer.
- **Coordination needs**: TPM team meets weekly for portfolio sync. Monthly program reviews with CTO/VP-level sponsors. Quarterly steering committee with CEO. Dedicated integration team for cross-program coordination.
- **Cost implications**: $20K-100K/year on tools + dedicated TPM headcount (1 TPM per 2-3 programs). Time cost: 3-5 full-time TPMs.
- **Key risk**: Conway's Law — program structure mirrors org structure. Re-org may be needed before program re-plan.

### Transition Triggers Summary

| From → To | Trigger |
|-----------|---------|
| Solo → Small | Second team joins OR external dependency appears OR fixed deadline >1 month |
| Small → Medium | 5+ teams OR 20+ dependencies OR 3+ concurrent programs |
| Medium → Enterprise | 15+ teams OR portfolio-level resource sharing OR C-level sponsor |
| Enterprise → Medium | Program concludes, postmortem done, ongoing ownership handed to platform team |


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | project-manager | Project schedule, resource plan, RAID log, stakeholder map |
| **This** | technical-program-manager | Program roadmap, cross-team dependency map, ADRs, executive reports |
| **After** | scrum-master | Sprint plans per team, backlog refinement, velocity tracking |

Common chains:
- **Chain**: project-manager → technical-program-manager → scrum-master — Individual project plans are integrated into a multi-team program; scrum masters drive sprint-level execution.
- **Chain**: ceo-strategist → technical-program-manager → release-manager — Strategic initiative gets program-level orchestration; release manager coordinates the launch.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| **Program Scoping** | New program initiation. Ambiguous problem space. Multiple stakeholders with conflicting priorities. | Define problem statement, success criteria, scope boundaries, stakeholder map, program charter. |
| **Dependency Management** | Cross-team initiative with 5+ inter-team dependencies. External vendor/API dependencies. | Map dependencies by type (technical, resource, external). Track owners, committed dates, buffers. Weekly dependency review. |
| **Technical Design Review Facilitation** | Solution architecture is ambiguous. Multiple valid approaches exist. Teams disagree on technical direction. | Schedule TDR, invite senior engineers from all affected teams, facilitate option generation and trade-off analysis, drive to ADR. |
| **ADR & RFC Process** | Architecture decision cross-cuts teams. Public API or contract change. Build-vs-buy decision. | Write ADR (context, decision, alternatives, consequences). RFC for public contracts. Circulate 1-2 weeks. Decide and communicate. |
| **Roadmap & Milestone Planning** | Program spans >2 months. Multiple teams with sequenced deliverables. External commitments with dates. | Create milestone timeline (5-8 milestones). Define entry/exit criteria per milestone. Track progress weekly. |
| **Stakeholder Communication** | >3 stakeholder groups with different information needs. C-level sponsor. External stakeholders. | RACI for decisions. Weekly 1-page exec summary. Monthly program review. Self-serve dashboard for status. |
| **Risk & Change Management** | High-uncertainty program. Fixed external deadline. Novel technology. Resource-constrained. | Risk register with T-shirt sizing (L/M/S), probability, impact, mitigation. Change control: impact analysis → options → decision. |
| **API Contract Negotiation** | Teams need to agree on API contracts. Migration from one API version to another. Event schema changes spanning teams. | Contract-first approach. OpenAPI/gRPC/AsyncAPI specs. Versioning strategy. Deprecation policy. Contract testing. |
| **Migration Program Management** | System deprecation. Platform migration. Data migration. Dual-run transition. | Define: cutover criteria, rollback plan, data verification, sunset date. Track: % traffic on new system. Sunset old system only after 100% migration. |
| **Program Health & Metrics** | Sponsor asks "are we on track?" Need objective program health data. | Metrics: milestone progress (on-track/at-risk/blocked), risk score, burndown/velocity, dependency health, team satisfaction. Dashboard auto-updated weekly. |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **TPM ≠ PM + technical knowledge**: A TPM manages technical *alignment* across teams, not project tasks within a team. If you're updating Jira tickets, you're doing PM work, not TPM work.
- **Contract first, implement second**: Before Team A builds an integration with Team B, agree on the API contract (OpenAPI spec, event schema, gRPC proto). Version it. Both teams build against the contract. This is the single highest-leverage TPM practice.
- **ADR before implementation, not after**: Architecture Decision Records capture *why* a decision was made. Without them, 6 months later no one remembers why Redis was chosen over Memcached and the program pays for it again.
- **Dependency map is your program's skeleton**: If you can't draw the dependency graph, you don't understand the program. Every dependency must have: owner team, blocking team, committed date, buffer. If a dependency has no owner, it WILL slip.
- **Bad news ages like milk**: If a critical path dependency slips, escalate within 24 hours. A 3-day slip caught early is a scope negotiation. A 3-week slip caught late is a crisis.
- **One decision-maker per decision**: RACI is not optional at scale. Every decision in the decision log must have exactly one "A" (Accountable). "Everyone agrees" without a named decider = no one decides.
- **Program health is a lagging indicator of dependency health**: If all dependencies are on track, the program is on track. Track dependency health obsessively. Program health dashboards that don't include dependency status are lying to you.
- **Dual-run everything for migrations**: Never cut over in one big-bang. Old system and new system run in parallel. Ramp traffic gradually. Verify data consistency. Have a rollback path. Sunset only when new system reaches 100% for 1 full cycle.
- **Estimate with uncertainty, communicate with confidence intervals**: "Q3" is not a date. "Q3 with 80% confidence" is. Use PERT: (optimistic + 4×most-likely + pessimistic) ÷ 6. Share the range, not a single date.
- **The TPM's output is decisions, not documents**: Every artifact (charter, ADR, status report, risk register) exists to drive a decision. If no decision is being made, stop producing the artifact.


### Error Decoder

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Project misses deadline consistently | No buffer for unknowns | Add 20% schedule buffer for every phase. Track actual vs estimated to calibrate future planning. |
| Stakeholder disengaged | Updates don't answer their questions | Executive updates: progress toward milestones, blocking issues, decisions needed. Not activity reports. |
| Team demotivated | Retrospectives without action | Every retro must produce at least one action item with an owner. Track follow-through. |
| Scope keeps growing | No change control process | Formal change request: cost/impact assessment, approval gate, backlog vs current sprint decision. |
| Documentation nobody reads | Written for completeness, not task completion | Diátaxis framework: Tutorials (learning), How-to guides (tasks), Reference (facts), Explanation (understanding). |
| Customer churn repeats same issue | Symptoms addressed, root cause ignored | Five Whys on every recurring ticket. Escalate systemic issues, don't just reply to each report. |
| Cross-team meeting with no outcome | No written agenda or decision log | Every meeting must have: agenda shared 24h before, decision log during, summary sent within 1h of end. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Program charter written and signed by sponsor with clear success criteria (measurable OKRs/KPIs)
- [ ] **[S2]**  Stakeholder map complete with RACI for all major decisions
- [ ] **[S3]**  Scope defined: what's IN, what's OUT, what's a KNOWN UNKNOWN
- [ ] **[S4]**  Technical Design Review completed (if architecture ambiguous); ADRs published
- [ ] **[S5]**  API contracts defined and versioned for all cross-team integrations
- [ ] **[S6]**  Dependency map complete: every dependency has owner team, blocking team, committed date, buffer
- [ ] **[S7]**  Critical path identified with buffer (25-30% for fixed-date programs)
- [ ] **[S8]**  Milestone plan established: 5-8 milestones with entry/exit criteria
- [ ] **[S9]**  Resource plan confirmed with all engineering managers — no over-allocations >120%
- [ ] **[S10]**  Risk register initialized with ≥10 risks, T-shirt sized, with mitigation plans
- [ ] **[S11]**  Change control process documented and socialized to all teams
- [ ] **[S12]**  Program cadence established: weekly TPM sync, bi-weekly stakeholder update, monthly review
- [ ] **[S13]**  Program health dashboard live with milestone progress, dependency status, risk score
- [ ] **[S14]**  Decision log started — every significant decision recorded with rationale
- [ ] **[S15]**  Escalation path defined with triggers and named decision-makers
- [ ] **[S16]**  Communication plan: exec summary template, stakeholder update cadence, self-serve dashboard
- [ ] **[S17]**  Technical debt register maintained with repayment windows negotiated
- [ ] **[S18]**  If migration program: dual-run strategy, cutover criteria, rollback plan, sunset date defined
- [ ] **[S19]**  Program closure criteria defined (all success criteria met, old systems decommissioned, knowledge transferred)
- [ ] **[S20]**  Postmortem scheduled at program midpoint and program closure

## References
<!-- QUICK: 30s -- links to deeper reading -->
- **Internal**: `references/adr-template.md` — Architecture Decision Record template with sections: context, decision, alternatives considered, consequences, status.
- **Internal**: `references/program-charter-template.md` — Program charter template: problem statement, success criteria, scope, stakeholders, timeline, resource ask.
- **Internal**: `references/dependency-map-template.md` — Dependency tracking spreadsheet template with columns: ID, type, description, blocking team, dependent team, committed date, buffer, status, escalation.
- **Internal**: `references/status-report-template.md` — 1-page weekly exec summary template: top 3 wins, top 3 risks, decisions needed, milestone progress.
- **External**: [Google TPM Guide](https://www.youtube.com/watch?v=VLOhKkHGjBg) — Google's approach to Technical Program Management
- **External**: [PERT Estimation Technique](https://en.wikipedia.org/wiki/Program_evaluation_and_review_technique) — Three-point estimation for schedule uncertainty
- **External**: [Architecture Decision Records (ADR)](https://adr.github.io/) — ADR format and best practices
- **External**: [RACI Matrix Guide](https://www.projectmanager.com/blog/raci-chart-made-easy) — RACI for cross-team decision accountability
- **External**: [Conway's Law](https://martinfowler.com/bliki/ConwaysLaw.html) — System design mirrors communication structures
- **External**: [Writing Effective RFCs](https://rust-lang.github.io/rfcs/) — Rust's RFC process as a model for technical decision-making
