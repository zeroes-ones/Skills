---
name: project-manager
description: Technical project management specialist. Project planning (WBS, Gantt charts), risk management (RAID logs), stakeholder communication, resource allocation, budget tracking, milestone management, status reporting, and project postmortems. PMBOK and agile-hybrid methodologies.
author: Sandeep Kumar Penchala
type: operations
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - project-manager
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
---
# Technical Project Manager

Technical project management covering initiation through closure. Work breakdown structures (WBS), dependency mapping, critical path analysis, risk management (RAID logs), stakeholder communication plans, budget tracking, resource leveling, milestone management, status reporting cadence, and project postmortems.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

What are you trying to do?
├── Project planning (WBS, Gantt) → Start at "Project Planning & Scheduling" under Sub-Skills
├── Risk management (RAID log) → Go to "RAID Log Management" under Sub-Skills
├── Stakeholder communication → Jump to "Stakeholder Communication" under Sub-Skills
├── Resource allocation → Go to "Resource Allocation" under references/
├── Budget tracking → Jump to "Earned Value Management (EVM)" under Sub-Skills
├── Milestone management & status reporting → Go to "Project Recovery" and "Stakeholder Communication"
├── Running a postmortem → Jump to "Postmortem" section in Core Workflow
└── Don't know where to start? → Start at "Project Planning & Scheduling"

**Do not read the entire skill.** Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never commit to dates without team input.** Dates decided in isolation will slip.
- **Risk register needs mitigation plans, not just identification.** Every risk needs an owner and a response strategy.
- **Status reports must surface blockers, not just progress.** Green status hiding red risks is a project killer.
- **Stakeholder communication should be proactive, not reactive.** Bad news early beats bad news late.
- **Always track dependencies with buffer.** Cross-team dependencies slip — plan for it.
- **Admit what you don't know.** If estimates are rough or key stakeholders haven't committed, say so.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Starting a new project that needs structured planning (initiation phase)
- Project slipped deadlines or scope creeping — need replanning
- Multiple stakeholders with misaligned expectations
- Need a risk management framework (RAID log)
- Project spans 3+ teams with interdependent deliverables
- Preparing for a gate review or steering committee presentation
- Running a project postmortem/retrospective
- Evaluating project health with objective metrics (EVM, SPI, CPI)
- Resource conflicts across multiple projects
- Need a communication plan (who gets what info, when, how)
- **Use `/scrum-master` instead** when: The team needs coaching on agile practices, sprint ceremonies are dysfunctional, impediments need removal, or team health needs improvement. Scrum-master is about *how* the team works — facilitation, coaching, process improvement.
- **Use `/technical-program-manager` instead** when: You need to coordinate across multiple teams, manage cross-team dependencies, drive a program with a fixed timeline and multiple workstreams. TPM handles scope that spans teams; PM handles scope within a single project.

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Methodology Selection: Waterfall vs Agile vs Hybrid
```
                     ┌──────────────────────────┐
                     │ START: Project methodology? │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Requirements well-understood,   │
                    │ unlikely to change (>80%        │
                    │ confidence in scope)?           │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Deliverable is│    │ Deliverable is   │
                    │ physical/     │    │ software AND     │
                    │ construction? │    │ team co-located  │
                    └──┬────────┬───┘    │ or async-capable?│
                       │YES     │NO      └──┬──────────┬────┘
                  ┌────▼───┐ ┌─▼────────┐   │YES       │NO
                  │Waterfall│ │Hybrid:   │ ┌─▼──────┐ ┌─▼──────────┐
                  │(critical│ │planning  │ │Scrum/  │ │Agile        │
                  │path,    │ │milestones│ │Kanban  │ │framework    │
                  │phase    │ │+ agile   │ │based on│ │with async   │
                  │gates)   │ │delivery  │ │team size│ │ceremonies   │
                  └─────────┘ │sprints   │ │+ cadence│ └─────────────┘
                              └──────────┘ └─────────┘
```
**When to choose Waterfall:** Physical/construction deliverables, regulatory phase-gate requirements, fixed-price contracts with clear scope — critical path method, milestone-driven.
**When to choose Hybrid:** Fixed scope + evolving implementation — waterfall planning/milestones with agile delivery sprints. Good for heavily regulated software.
**When to choose Agile/Scrum:** Software with evolving requirements, co-located or async-capable team — 2-week sprints, backlog refinement, working software increments.

### Risk Response Strategy
```
                     ┌──────────────────────────┐
                     │ START: Risk response?       │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Probability × Impact score      │
                    │ HIGH (>15 on 5×5 matrix)?      │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Can we avoid   │    │ Medium risk      │
                    │ the risk       │    │ (5-15)?          │
                    │ entirely by    │    └──┬──────────┬────┘
                    │ changing plan? │       │YES       │NO (Low)
                    └──┬────────┬───┘  ┌────▼────┐ ┌──▼──────────┐
                       │YES     │NO    │Mitigate:│ │Accept +     │
                  ┌────▼───┐ ┌─▼────────┐│reduce P │ │monitor only:│
                  │Avoid:  │ │Can we     ││or I with│ │log in RAID, │
                  │change  │ │transfer?  ││concrete │ │no active    │
                  │scope,  │ └──┬────┬───┘│actions  │ │mitigation   │
                  │tech, or│    │YES │NO  │+ owners │ └─────────────┘
                  │approach│ ┌──▼──┐┌▼────┐└─────────┘
                  └────────┘ │Trans-││Miti-│
                              │fer:  ││gate: │
                              │insure││build │
                              │ance, ││con-  │
                              │vendor││tingen-│
                              │SLA   ││cy plan│
                              └──────┘└──────┘
```
**When to Avoid:** High risk, viable alternative approach — change technology, scope, or delivery plan to eliminate the risk entirely (strongest response).
**When to Transfer:** Financial or liability risk that can be insured or contracted away — insurance, vendor SLA, fixed-price contract with penalty clauses.
**When to Mitigate:** Can reduce probability (add testing, prototyping) or impact (contingency budget, fallback plan) — always assign an owner and deadline.
**When to Accept:** Low impact or low probability — document in RAID log, monitor triggers, no active mitigation unless threshold crossed.

### Stakeholder Communication Escalation
```
                     ┌──────────────────────────────┐
                     │ START: Who needs what comms?   │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Executive sponsor or steering   │
                    │ committee member?               │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │High-level:    │    │ Directly blocked  │
                    │Status on 1    │    │ or dependent on   │
                    │page: RAG,     │    │ deliverables?     │
                    │milestones,    │    └──┬──────────┬────┘
                    │key risks,     │       │YES       │NO
                    │decisions needed│  ┌────▼────┐ ┌─▼──────────┐
                    │Frequency:      │  │Detailed │ │FYI only:   │
                    │monthly or      │  │status:  │ │broadcast   │
                    │at gate reviews │  │task-level│ │channel,    │
                    └────────────────┘  │blockers,│ │newsletter  │
                                        │dependen-│ │or wiki     │
                                        │cies     │ │update      │
                                        └─────────┘ └────────────┘
```
**When to send Executive-level comms:** Sponsor/steering committee — 1-page RAG status, milestone vs plan, top 3 risks, decisions needed. Monthly or at gate reviews.
**When to send Detailed comms:** Team leads, dependent teams, blockers — task-level status, dependencies, timeline changes. Weekly or per sprint.
**When to send General comms:** Wider org, indirect stakeholders — project newsletter, wiki update, Slack broadcast. Optional consumption, no action required.

### Project Health Assessment
```
                     ┌──────────────────────────────┐
                     │ START: Is the project healthy? │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ SPI (Schedule Performance      │
                    │ Index) < 0.85 OR CPI (Cost     │
                    │ Performance Index) < 0.85?     │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ RED: Immediate│    │ SPI/CPI 0.85-0.95│
                    │ Corrective    │    │?                 │
                    │ Action:       │    └──┬──────────┬────┘
                    │ - Root cause  │       │YES       │NO
                    │ - Recovery    │  ┌────▼────┐ ┌───▼──────────┐
                    │   plan        │  │AMBER:   │ │GREEN:        │
                    │ - Stakeholder │  │Course-  │ │Monitor only. │
                    │   notification│  │correct  │ │Celebrate if   │
                    │ - Escalate if │  │before it │ │SPI/CPI > 1.0 │
                    │   >2 weeks    │  │hits RED  │ │— ahead of    │
                    └───────────────┘  └─────────┘ │plan.         │
                                                   └──────────────┘
```
**When RED (SPI/CPI < 0.85):** >15% behind schedule or over budget — immediate root cause analysis, recovery plan with specific dates, stakeholder escalation, increased monitoring frequency.
**When AMBER (SPI/CPI 0.85-0.95):** 5-15% off plan — course correct now with specific actions, don't wait for RED. Adjust resource allocation or re-baseline.
**When GREEN (SPI/CPI > 0.95):** On or ahead of plan — continue monitoring, celebrate ahead-of-plan performance, but verify metrics aren't gamed.

### Resource Conflict Resolution
```
                     ┌──────────────────────────────┐
                     │ START: Resource conflict       │
                     │ between projects?              │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Both projects have same         │
                    │ strategic priority from         │
                    │ sponsor/portfolio?              │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │Capacity-based│    │ Lower priority   │
                    │Split:         │    │ project yields.  │
                    │% allocation   │    │ Re-plan with     │
                    │agreed with    │    │ remaining        │
                    │both sponsors. │    │ capacity. If     │
                    │If not feasible│    │ blocking higher  │
                    │→ escalate to  │    │ priority →       │
                    │portfolio      │    │ escalate to      │
                    │governance     │    │ portfolio for    │
                    └───────────────┘    │ decision.        │
                                         └──────────────────┘
```
**When to capacity-split:** Equal priority — agree % allocation with both sponsors (e.g., 60/40), document impact on both timelines, review monthly. Escalate to portfolio if not feasible.
**When to yield:** Unequal priority — lower priority project adjusts plan, higher priority proceeds. Escalate to portfolio governance for formal decision if contested.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Initiation & Planning

1. **Project charter**: Problem statement, business case, success criteria, constraints, assumptions
2. **Stakeholder analysis**: Power-interest grid, communication preferences, RACI for key decisions
3. **Work breakdown structure (WBS)**: Decompose deliverables into work packages (8-80 hour rule)
4. **Dependency mapping**: Mandatory, discretionary, external, internal dependencies
5. **Critical path analysis**: Longest path through dependencies; zero-float activities
6. **Resource plan**: Who does what, availability, skill gaps, resource leveling
7. **Schedule baseline**: Gantt chart with milestones, dependencies, and buffer
8. **Budget**: Bottom-up estimation, contingency reserve (10-20%), management reserve
9. **Communication plan**: Stakeholder → information need → format → frequency → owner
10. **Risk register (RAID)**: Risks, Assumptions, Issues, Decisions — T-shirt sizing (L/M/S), probability, impact, mitigation

### Phase 2 (~30 min): Execution & Monitoring

1. **Daily ops**: Standup attendance (observe, don't run), unblocking, dependency tracking
2. **Weekly status**: Progress against milestones, SPI/CPI, top 3 risks, blocked items, decisions needed
3. **RAID log review**: Weekly review, aging analysis, escalation triggers
4. **Change control**: Scope change requests (SCR) → impact analysis → CCB review → approve/reject
5. **Burndown/burnup**: Track earned value vs planned value
6. **Stakeholder updates**: Tailored by audience (executive summary vs detailed technical)

### Phase 3 (~20 min): Closure & Postmortem

1. **Project closure checklist**: All deliverables accepted, contracts closed, resources released
2. **Lessons learned**: What went well, what went wrong, what to do differently
3. **Postmortem report**: Timeline, metrics (planned vs actual), root causes, action items
4. **Knowledge transfer**: Documentation, runbooks, architecture decisions archived
5. **Celebration**: Acknowledge the team. Seriously — it matters for retention.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Project management is the hub — coordinating product, engineering, design, QA, DevOps, stakeholders, and business. The PM doesn't do the work; the PM ensures the right people talk to each other at the right time.

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Product Strategist** | Roadmap, scope changes, prioritization | Feature priorities, MVP scope, trade-off decisions, stakeholder expectations |
| **CTO Advisor / Engineering Lead** | Architecture decisions, tech debt, capacity | Engineering capacity, technical risks, build vs buy recommendations |
| **Scrum Master** | Sprint execution, impediments, team health | Sprint goals, velocity trends, blocked items, team capacity changes |
| **UX Designer** | Design deliverables, user research timeline | Design handoff dates, research findings that affect scope, prototype reviews |
| **Frontend/Backend Dev Leads** | Estimation, technical risks, dependency identification | Feasibility input, sequencing constraints, spike results |
| **QA Lead** | Test planning, acceptance criteria, release readiness | Test environment needs, regression scope, defect triage priorities |
| **DevOps / Infrastructure** | Environments, deployments, CI/CD pipeline | Environment availability, deployment schedule, infrastructure dependencies |
| **Security Reviewer** | Security review gates, penetration testing | Security review SLA, findings that block release, remediation priorities |
| **Data/Analytics** | Metrics instrumentation, reporting requirements | Event tracking needs, dashboard readiness, success metric baselines |
| **Business Strategist / Stakeholders** | Business milestones, budget, ROI expectations | Status against business case, budget burn rate, milestone achievement |
| **Legal Advisor** | Contractual obligations, compliance gates | Delivery obligations, SLA commitments, regulatory milestones |
| **Vendor / External Partners** | Third-party deliverables, API integrations | External dependency status, contract deliverables, integration timelines |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Critical path delayed by >1 week | Stakeholders, Product Strategist, All Team Leads | Delivery date impact; replanning required |
| Resource loss (key person leaves, reallocated, or unavailable >2 weeks) | Engineering Lead, Stakeholders | Capacity impact; timeline or scope adjustments needed |
| Scope change request from stakeholder | Product Strategist, Engineering Lead | Impact analysis needed before approval; trade-off decision |
| Risk probability escalates from Medium to High | Stakeholders, Affected Team Leads | Mitigation activation; may require contingency budget |
| External dependency misses committed date | Affected Team Leads, Stakeholders | Schedule impact cascade; escalation to vendor management |
| Budget burn rate exceeds plan by >15% | Stakeholders, Finance | Overrun risk; corrective action or re-baseline needed |
| Major milestone achieved (or missed) | All Stakeholders, All Teams | Celebration or course correction; visibility critical for trust |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Project no longer viable (business case invalidated) | **CEO Strategist** + Sponsor + Portfolio Governance | Stop-work decision; resource reallocation |
| Stakeholder conflict blocking progress for >1 week | **Sponsor** or Steering Committee | Resolution authority beyond PM's influence |
| Vendor breach of contract or non-delivery | **Legal Advisor** + Procurement + Sponsor | Contractual remedy; may require legal action |
| Regulatory/compliance deadline at risk of being missed | **Legal Advisor** + Regulatory Specialist + Sponsor | Regulatory exposure; may require external notification |
| >20% budget or schedule overrun without recovery path | **Sponsor** + Portfolio Governance + Finance | Re-baseline or termination decision; executive approval required |

## Scale Depth
<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
One person managing 1-3 small projects part-time. Tools: Google Sheets + Notion for tracking, Slack for comms. No formal RAID log — issues tracked in a doc. No EVM; simple milestone tracking. Communication: async updates, no stakeholder meetings beyond weekly check-in. Cost: $0-100/month. Overkill: MS Project, Jira Advanced Roadmaps, portfolio dashboards, formal gate reviews.

### Small (2-10 people, 10-100 users)
Dedicated PM or tech lead wearing PM hat. Tools: Jira/Linear + Confluence/Notion. RAID log maintained. Basic EVM: SPI/CPI on major deliverables. Weekly status reports to stakeholders. Gate reviews for major milestones. Risk register with owners and mitigation plans. Cost: $100-500/month (tools). Overkill: PMO, formal portfolio governance, resource management software.

### Medium (10-50 people, 100-10K users)
1-3 PMs or PMO lead. Tools: Jira Advanced Roadmaps, MS Project, Smartsheet. EVM across all workstreams. Portfolio-level RAID log with cross-project dependencies. Formal stage-gate process with steering committee. Resource capacity planning. Vendor management process. Cost: $2K-10K/month. Overkill: dedicated PMO department, enterprise PPM (Planview, Clarity).

### Enterprise (50+ people, 10K+ users)
PMO (3-10+). Enterprise PPM: Planview, ServiceNow PPM, Clarity. Portfolio governance with stage-gate, benefits realization tracking. Resource management across all projects. Strategic alignment scoring. Vendor performance management. PM methodology training and coaching. Cost: $20K-200K+/month.

### Transition Triggers
| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | 3+ concurrent projects with cross-team dependencies | Add Jira/Linear for tracking; implement RAID log; start weekly stakeholder reporting |
| Small → Medium | 5+ concurrent projects, shared resource pool, or portfolio budget >$500K | Add PPM tool; implement stage-gate governance; hire dedicated PM(s) |
| Medium → Enterprise | 10+ projects, multi-department resource conflicts, or regulatory oversight | Establish PMO; implement enterprise PPM; add portfolio governance board |


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | product-manager | Prioritized product backlog, roadmap, and feature requirements |
| **This** | project-manager | WBS, project schedule, RAID log, status reports, resource plan |
| **After** | scrum-master | Sprint plans, backlog refinement, team velocity tracking |

Common chains:
- **Chain**: product-manager → project-manager → scrum-master — Product vision becomes a structured project plan; the scrum master executes sprints against it.
- **Chain**: ceo-strategist → project-manager → technical-program-manager — Strategic initiative gets project-level planning; handed off to TPM for cross-team execution.

## What Good Looks Like

> When project management is applied perfectly, every project has a clear charter with defined success criteria, the critical path is known and actively managed, risks are identified before they become issues, stakeholders receive the right information at the right cadence without information overload, resource constraints are surfaced early with trade-off options, and projects complete within the communicated timeline and budget — not through heroics but through disciplined execution.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| **Project Planning & Scheduling** | New project initiation or major re-plan | WBS, Gantt charts, critical path method — MS Project, Smartsheet, Jira Advanced Roadmaps |
| **RAID Log Management** | Any project with >2 stakeholders or >1 month duration | Risks, Assumptions, Issues, Dependencies — tracked in spreadsheet or Jira/Confluence with owners and review cadence |
| **Earned Value Management (EVM)** | Budget >$100K or sponsor requires objective progress metrics | SPI (schedule), CPI (cost), EAC (estimate at completion) — calculate from planned vs actual vs earned |
| **Stakeholder Communication** | 3+ stakeholder groups with different information needs | RACI matrix, communication plan (who, what, when, how), steering committee decks, status dashboards |
| **Vendor & Procurement Management** | External vendors delivering project components | RFP/RFQ process, SOW review, SLA monitoring, milestone acceptance, invoice verification |
| **Risk Management** | High-uncertainty projects or regulated environments | Probability × Impact matrix, Monte Carlo simulation, risk response strategies (avoid/transfer/mitigate/accept), contingency reserves |
| **Agile/Scrum PM** | Software projects with evolving requirements | Sprint planning facilitation, backlog grooming, velocity tracking, Scrum of Scrums for multi-team coordination |
| **Project Recovery** | Project >15% behind schedule or >20% over budget | Root cause analysis, recovery plan (crash/fast-track/re-scope), stakeholder re-alignment, increased governance frequency |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Plan for the plan to be wrong**: No plan survives contact with reality. Build 15-20% buffer.
- **RAID log is your second brain**: If it's not in the RAID log, it doesn't exist
- **Status reports are pull, not push**: Dashboard where stakeholders self-serve; don't email PDFs
- **Escalate early, not when it's on fire**: Bad news does not age well. The sooner escalated, the more options available.
- **One decision-maker per decision**: RACI avoids the "everyone agrees but nothing happens" trap
- **Milestones over tasks for external comms**: Stakeholders care about "payment module live," not 47 subtasks
- **Risk identification is everyone's job**: A quiet PM doesn't catch risks; an engineering team speaking up catches them
- **Postmortems are blameless**: Focus on process failures, not individual mistakes

## MVP vs Growth vs Scale

| Phase | Scope | Team Size | Project Management Approach |
|-------|-------|-----------|---------------------------|
| **MVP (0→1)** | 1 project, 1-5 people, 2-week cycles | Solo PM or tech lead doubling as PM | GitHub Projects or Linear + Notion. No Gantt charts. No formal RAID log. One status update/week in Slack. Milestones: "launched," "not launched yet." |
| **Growth (1→10)** | 3-5 concurrent projects, 5-20 people | 1 PM or fractional PM | Proper WBS for projects >1 month. RAID log (Google Sheets). Weekly status reports. Gantt for complex dependency chains. Jira/Asana with timeline view. |
| **Scale (10→N)** | 10+ concurrent projects, 50+ people, multi-team programs | PMO or multiple PMs | Portfolio-level tracking. Earned value management. Resource capacity planning tools (Float/Resource Guru). Standardized charter templates. Formal phase-gate reviews. Executive dashboard. |

## Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| Project tracking | GitHub Projects (free) or Trello (free) | Jira ($7.75/user/mo) or Linear ($8/user/mo) | >10 contributors or need dependency visualization |
| Gantt charts | Mermaid Gantt in markdown (free) | TeamGantt ($24/mo) or Smartsheet ($7/user/mo) | Stakeholders demand visual timelines or >50 tasks |
| RAID log | Google Sheets template (free) | Jira Risk Management or dedicated tool | >5 projects or need dashboard aggregation |
| Status reporting | Markdown in shared repo (free) | Notion ($8/user/mo) or Confluence ($6/user/mo) | Need permission control or non-technical stakeholders |
| Resource planning | Google Sheets (free) | Float ($6/user/mo) or Resource Guru ($4/user/mo) | >20 people to manage across >5 projects |
| Time tracking | Toggl Track (free up to 5 users) | Harvest ($12/user/mo) | >5 people tracking or need billable hours reporting |
| Stakeholder comms | Slack channel + weekly message (free) | Loom ($12/mo) for async video updates | >10 stakeholders or need async video walkthroughs |
| Portfolio mgmt | Google Sheets dashboard (free) | Monday.com ($9/user/mo) or Wrike ($9.80/user/mo) | >5 concurrent projects or need roll-up reporting |

**Annual tool budget by phase:** MVP: $0. Growth: $500-2K. Scale: $5K-30K.

## Scalability Decision Tree

```
How long is the project?
├── <2 weeks → TODO list in GitHub Issues. No Gantt, no WBS. Just a checklist with owners.
└── 2 weeks to 2 months → WBS + dependency map + weekly status. Google Sheets sufficient.
    └── >2 months → Full plan with Gantt, RAID, communication plan, phase gates.

How many people involved?
├── 1-3 → Async status updates in Slack. Lightweight planning.
├── 3-10 → Weekly sync (30 min max). RAID log. Written status updates.
└── 10+ → Structured communication plan. Different info for execs vs team vs stakeholders.

Are there external dependencies (other teams, vendors, APIs)?
├── YES → Dependency tracking becomes critical. Flag external deps in RAID with owner + due date.
│   External dependencies are the #1 cause of project delays.
└── NO → Internal alignment is simpler. Focus on sequencing, not negotiation.

Is the budget >$50K or is there a contract with penalties?
├── YES → Formal change control, earned value tracking, regular financial reporting.
└── NO → Lightweight budget tracking. Check monthly not weekly.

Are stakeholders asking for "more visibility"?
├── YES → Create a self-serve dashboard. Don't send more emails. Stakeholders pull, not PM push.
└── NO → Current communication is sufficient. Don't create reports nobody reads.
```


**What good looks like:** Project charter signed by sponsor. WBS decomposed to tasks under 80 hours. RAID log reviewed weekly. Status report sent on schedule with milestones, risks, and decisions needed. Project completes within 10% of estimated timeline.

## When NOT to Use This Skill (Overkill)

- **2-person project lasting 1 week**: A Slack DM and a shared todo list is the plan. Formal WBS, Gantt charts, and RAID logs for a 5-day 2-person effort are overhead, not help.
- **The project is "exploratory" or research**: You can't plan research. You can plan time-boxed spikes. Don't create a WBS for "investigate why the database is slow."
- **Solo founder building an MVP**: You are your own stakeholder, resource, and approver. Ship fast. The only project management you need is "what's the most important thing to build next?"
- **The team is highly experienced and ships consistently without process**: Don't fix what isn't broken. If things slip predictably, apply process surgically to the pain point, not the whole project.
- **You're the bottleneck — the PM is doing all tracking while the team overruns anyway**: The problem isn't planning. It's trust, capacity, or skill. Process won't fix it.
- **The project is a recurring operational activity ("monthly billing run")**: That's a runbook, not a project. Automate it. Don't Gantt-chart recurring ops.

## Token-Efficient Workflow

```
# Step 1: Project health check
python3 scripts/project_health.py --project-id PROJECT --output json
# Returns: {
#   "spi": 0.85, "cpi": 1.05, "critical_path_slippage_days": 4,
#   "risks_high_open": 2, "risks_aging_30d": 1,
#   "blocked_tasks": 3, "stakeholder_nps": 7,
#   "milestones_on_track": 5, "milestones_total": 7
# }

# Step 2: Decision tree
# spi < 0.8 → Schedule compression (fast-tracking or crashing)
# cpi > 1.1 → Under budget (re-allocate or early delivery)
# critical_path_slippage_days > 0 → Focus ONLY on critical path recovery
# risks_high_open > 0 → Top priority: mitigation actions this week
# stakeholder_nps < 6 → Communication plan failing. Fix.
# blocked_tasks > 3 → SWAT unblocking session

# Step 3: Status report — auto-generate from data
python3 scripts/gen_status.py --project-id PROJECT > status_$(date +%Y-%m-%d).md
# 1-page markdown: milestones, top risks, blocked items, decisions needed

# Step 4: Verify RAID freshness
python3 scripts/raid_audit.py --project-id PROJECT --stale-threshold-days 14
# Exit 0 = all items reviewed within 14 days. Exit 1 = stale items found.
```

**Principle:** `project_health.py` reads from the project tracker (Jira/Linear/GitHub issues), computes SPI/CPI, checks milestone dates, and outputs a JSON snapshot. Agent reads 1 JSON file, applies the decision tree, and generates exactly 1 action. No reading task lists into agent context.


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
- [ ] **[S1]**  Project charter approved with clear success criteria
- [ ] **[S2]**  WBS created with work packages decomposed to <80 hours each
- [ ] **[S3]**  Dependency map complete with critical path identified
- [ ] **[S4]**  RAID log initialized with at least 10 identified risks
- [ ] **[S5]**  Stakeholder analysis complete with communication preferences mapped
- [ ] **[S6]**  Schedule baseline established with milestones and buffer
- [ ] **[S7]**  Budget approved with contingency reserve (10-20%)
- [ ] **[S8]**  Communication plan defined (who gets what info, when, how)
- [ ] **[S9]**  Change control process documented and socialized
- [ ] **[S10]**  Status report template ready (dashboard or document format)
- [ ] **[S11]**  Escalation path defined with triggers
- [ ] **[S12]**  Resource allocation confirmed (no over-allocations >120%)
- [ ] **[S13]**  Kickoff meeting held with all stakeholders
- [ ] **[S14]**  Project retrospective/postmortem scheduled at 2-4 week cadence

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [PMBOK Guide (7th Edition)](https://www.pmi.org/pmbok-guide-standards/foundational/pmbok)
- [Atlassian Project Management Guide](https://www.atlassian.com/project-management)
- [Linear Method](https://linear.app/method)
- [Shape Up: Basecamp's Project Methodology](https://basecamp.com/shapeup)
- [Google Project Management Certificate](https://www.coursera.org/professional-certificates/google-project-management)
- [Earned Value Management (EVM) — DoD Guide](https://www.dau.edu/acquipedia/pages/ArticleDetails.aspx?aid=71c4e37a-5e2b-4d85-8bc5-35b7753e7191)
- [RACI Matrix Guide](https://www.projectmanager.com/blog/raci-chart-made-easy)
- [How to Run a Project Postmortem — Atlassian](https://www.atlassian.com/team-playbook/plays/project-retrospective)
