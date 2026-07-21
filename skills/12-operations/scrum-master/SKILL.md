---
name: scrum-master
description: Sprint planning, daily standups, retrospectives, backlog refinement, velocity tracking, burndown charts, team health, impediment removal, agile metrics.
author: Sandeep Kumar Penchala
type: operations
status: stable
version: "1.0.0"
updated: 2026-07-21
tags:
  - scrum-master
token_budget: 4000
output:
  type: "code"
  path_hint: "./"
---
# Scrum Master

Agile delivery leadership system for guiding Scrum teams from forming through high-performance. Covers all Scrum ceremonies, metrics-driven continuous improvement, impediment removal, and scaling frameworks.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

What are you trying to do?
├── Sprint planning → Start at "Sprint Facilitation" under Sub-Skills
├── Daily standup facilitation → Go to "Sprint Facilitation" under Sub-Skills
├── Running a retrospective → Jump to "Team Health & Psychological Safety" then "references/retrospective-formats.md"
├── Backlog refinement → Go to "Backlog Refinement Coaching" under Sub-Skills
├── Velocity tracking & burndown charts → Jump to "Agile Metrics & Diagnostics" under Sub-Skills
├── Team health check → Go to "Team Health & Psychological Safety" under Sub-Skills
├── Removing impediments → Jump to "Impediment Removal" under Sub-Skills
└── Don't know where to start? → Start at "Sprint Facilitation"

**Do not read the entire skill.** Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never estimate for the team.** Estimates come from the people doing the work, never from the scrum master.
- **Retrospective action items need owners and deadlines.** Action items without accountability don't get done.
- **Velocity is for planning, not performance evaluation.** Using velocity to compare teams or individuals destroys trust.
- **The scrum master serves the team, not manages it.** Facilitate, coach, and remove impediments — don't assign work.
- **Always surface impediments early.** A blocked team member for 2 days is a sprint risk.
- **Admit what you don't know.** If a scaling framework (LeSS/Nexus/SAFe) is unfamiliar territory, say so.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Establishing or resetting Scrum practices for a new or underperforming team
- Coaching a team through sprint planning — effective story decomposition, estimation, sprint goal crafting
- Facilitating retrospectives that produce actionable, tracked improvement experiments
- Diagnosing delivery bottlenecks through agile metrics: velocity variance, cycle time, cumulative flow, escaped defects
- Protecting the team from external interference while maintaining stakeholder transparency
- Scaling Scrum across multiple teams with LeSS, SAFe, or Nexus
- Onboarding a team to Scrum from waterfall or ad-hoc processes
- Improving Product Owner and Development Team collaboration on backlog health and refinement

## Decision Trees

### Scrum vs Kanban vs Scrumban
```
                     ┌──────────────────────────────┐
                     │ START: Which agile framework?  │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Work arrives predictably in     │
                    │ batches (features, epics) vs    │
                    │ continuous flow (tickets, bugs)?│
                    └────┬──────────────────────┬───┘
                         │ Batches             │ Continuous
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Team needs     │    │ Need predictable │
                    │ regular        │    │ delivery         │
                    │ ceremony       │    │ cadence (e.g.,   │
                    │ cadence for    │    │ release every    │
                    │ alignment?     │    │ sprint)?         │
                    └──┬────────┬───┘    └──┬──────────┬────┘
                       │YES     │NO        │YES       │NO
                  ┌────▼───┐ ┌─▼──────┐ ┌─▼──────┐ ┌─▼──────────┐
                  │Scrum   │ │Scrumban│ │Scrumban│ │Pure Kanban │
                  │2-week  │ │Sprints │ │Sprints+│ │WIP limits, │
                  │sprints,│ │+ WIP   │ │Kanban  │ │continuous  │
                  │all     │ │limits, │ │metrics │ │flow, CFD   │
                  │ceremonies│ │fewer   │ │        │ │metrics     │
                  └────────┘ │ceremon.│ └────────┘ └────────────┘
                             └────────┘
```
**When to choose Scrum:** Predictable batched work, team needs regular alignment — full ceremonies (sprint planning, daily scrum, review, retro), 2-week cadence, defined sprint goal.
**When to choose Kanban:** Continuous inflow (support tickets, ops), no natural sprint boundary — WIP limits, cycle time, cumulative flow diagram (CFD), no fixed iterations.
**When to choose Scrumban:** Mix of planned features + unplanned work — retain sprint structure with WIP limits, fewer ceremonies, use CFD + burndown metrics.

### Sprint Length Decision
```
                     ┌──────────────────────────────┐
                     │ START: Sprint duration?        │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Requirements change frequently  │
                    │ (stakeholders want flexibility)  │
                    │ AND team is experienced?         │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ 1-week sprint │    │ Team new to      │
                    │ for fast      │    │ Scrum (<6 months)│
                    │ feedback.     │    │ OR work is       │
                    │ Risk: overhead │    │ complex (needs   │
                    │ of ceremonies │    │ spikes + deep    │
                    │ per sprint.   │    │ design)?         │
                    └───────────────┘    └──┬──────────┬────┘
                                           │YES       │NO
                                      ┌────▼────┐ ┌──▼──────────┐
                                      │3-4 week │ │2-week sprint │
                                      │sprint   │ │(default for  │
                                      │for      │ │most teams)   │
                                      │complex  │ │Balance of    │
                                      │work     │ │feedback +    │
                                      └─────────┘ │ceremony cost │
                                                  └──────────────┘
```
**When to choose 1-week:** Experienced team, volatile requirements, fast feedback needed — cost: ceremony overhead ~15% of sprint time.
**When to choose 2-week:** Default for most teams — balances feedback frequency with ceremony overhead (~10%), validates assumptions every 10 business days.
**When to choose 3-4 week:** New Scrum team or inherently complex work (research spikes, deep technical design) — more time to produce meaningful increment, less ceremony overhead.

### Retrospective Health Diagnosis
```
                     ┌──────────────────────────────┐
                     │ START: Retrospectives not      │
                     │ producing value?               │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Same issues surface sprint      │
                    │ after sprint — "Groundhog Day"  │
                    │ retro?                          │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Action items   │    │ Team disengaged  │
                    │ not completed  │    │ (quiet, phones,  │
                    │ or tracked?    │    │ laptops out)?    │
                    └──┬────────┬───┘    └──┬──────────┬────┘
                       │YES     │NO        │YES       │NO
                  ┌────▼───┐ ┌─▼───────┐ ┌─▼──────┐ ┌─▼──────────┐
                  │Implement│ │Issues are│ │Change  │ │Format is   │
                  │action   │ │systemic  │ │format: │ │fine —      │
                  │tracking │ │(outside  │ │silent  │ │investigate │
                  │board    │ │team      │ │writing, │ │why issues  │
                  │with     │ │control): │ │1-on-1  │ │not being   │
                  │owner +  │ │escalate  │ │check-  │ │raised      │
                  │deadline │ │to mgmt   │ │ins,    │ │(psycho-    │
                  └─────────┘ └──────────┘ │start-  │ │logical     │
                                           │stop-cont│ │safety?)    │
                                           │nue     │ └────────────┘
                                           └────────┘
```
**When to implement action tracking:** Same issues recurring — create visible action board with owner + deadline per item, review at start of each retro, escalate if >2 sprints stale.
**When to escalate:** Issues are systemic/organizational — team can't fix alone. Escalate with data (e.g., "3 sprints blocked by procurement SLAs").
**When to change format:** Disengagement — try silent writing, start-stop-continue, 4Ls (liked/learned/lacked/longed), or 1-on-1 check-ins to rebuild psychological safety.

### Impediment Escalation Triage
```
                     ┌──────────────────────────────┐
                     │ START: Team blocked by          │
                     │ impediment?                    │
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ Can the team resolve it         │
                    │ themselves within 24 hours?     │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ Team self-    │    │ Impediment is    │
                    │ resolves.     │    │ cross-team       │
                    │ SM monitors   │    │ dependency?      │
                    │ but doesn't    │    └──┬──────────┬────┘
                    │ intervene.    │       │YES       │NO
                    └───────────────┘  ┌────▼────┐ ┌──▼──────────┐
                                       │SM       │ │Organizational│
                                       │facilitates│ │blocker:     │
                                       │cross-team│ │SM escalates │
                                       │resolution│ │to leadership│
                                       │meeting   │ │with business │
                                       └──────────┘ │impact data  │
                                                    └─────────────┘
```
**When team self-resolves:** Impediment within team's span of control — SM observes and coaches but doesn't do it for them. Builds team autonomy.
**When SM facilitates cross-team:** Dependency on another team — SM schedules and facilitates resolution meeting, tracks action items, follows up daily.
**When SM escalates to leadership:** Organizational blocker (procurement, hiring, policy) — SM escalates with quantified business impact data, not just frustration.

### Scaling Framework Selection (LeSS vs SAFe vs Nexus)
```
                     ┌──────────────────────────────┐
                     │ START: Which scaling framework?│
                     └────────────┬─────────────────┘
                                  │
                    ┌─────────────▼─────────────────┐
                    │ 2-8 teams working on same       │
                    │ product, co-located or          │
                    │ timezone-aligned?               │
                    └────┬──────────────────────┬───┘
                         │ YES                  │ NO
                    ┌────▼──────────┐    ┌──────▼──────────┐
                    │ LeSS (2-8     │    │ 5+ teams across   │
                    │ teams) or     │    │ multiple products, │
                    │ Nexus (3-9    │    │ need portfolio    │
                    │ teams) —      │    │ management,       │
                    │ lightweight,  │    │ compliance, and   │
                    │ single product│    │ enterprise        │
                    │ backlog       │    │ governance?       │
                    └───────────────┘    └──┬──────────┬────┘
                                           │YES       │NO
                                      ┌────▼────┐ ┌──▼──────────┐
                                      │SAFe     │ │Stay with    │
                                      │Full     │ │coordinated  │
                                      │with ART,│ │Scrum of     │
                                      │PI       │ │Scrums —     │
                                      │Planning,│ │don't        │
                                      │RTE role │ │over-framework│
                                      └─────────┘ └─────────────┘
```
**When to choose LeSS/Nexus:** Single product, 2-9 teams, co-located — LeSS (minimalist), Nexus (Scrum.org). Keep it simple; avoid SAFe overhead for single product.
**When to choose SAFe:** Enterprise with 5+ teams across multiple products/programs, need portfolio management, compliance, executive visibility — ART, PI Planning, RTE role.
**When to choose Scrum of Scrums:** 3-5 teams, no enterprise governance needed — lightweight coordination with ambassador from each team meeting 2-3×/week.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Team Formation & Foundations

1. **Team Chartering** — Purpose, norms, Definition of Ready (DoR), Definition of Done (DoD), roles clarified.
2. **Backlog Establishment** — User story format, ordered by value (WSJF for complex prioritization), relative sizing (Fibonacci), top 2-3 sprints refined.
3. **Sprint Cadence** — 2 weeks standard. Fixed ceremony schedule. Protect the rhythm.

### Phase 2 (~30 min): Ceremony Facilitation

1. **Sprint Planning** (4hr for 2-week sprint) — What: PO presents sprint goal, team pulls PBIs. How: decompose PBIs into tasks (≤8hrs each). Commit to sprint goal, not individual PBIs.
2. **Daily Scrum** (15 min) — Team coordination, not status report. Walk board right-to-left.
3. **Backlog Refinement** (10% of capacity) — Weekly. Review, split, estimate, add acceptance criteria.
4. **Sprint Review** (1hr/week of sprint) — Collaborative inspection of increment + backlog adaptation.
5. **Sprint Retrospective** (1.5hr for 2-week sprint) — Gather data → generate insights → decide 1-3 improvement experiments → close.

### Phase 3 (~20 min): Metrics, Impediments & Scaling

1. **Agile Metrics** — Velocity (3-sprint rolling avg), Sprint Burndown, Cumulative Flow Diagram (CFD), Cycle Time, Escaped Defects, Team Health, Sprint Goal Success Rate.
2. **Impediment Removal** — External and internal impediments. Maintain impediment log. Track resolution time.
3. **Scaling** — Nexus (3-9 teams), LeSS (up to 8 teams, single backlog), SAFe (if organizational mandate). Goal: minimize cross-team dependencies.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- The Scrum Master is a coach, not a secretary. Teach, don't do.
- Sprint goals, not sprint backlogs, are the commitment.
- Protect the retrospective — never cancel it.
- WIP limits reduce cycle time: WIP = team size / 2.
- Velocity is for team forecasting, not management performance review.
- Daily scrum is team-to-team coordination, not status report to SM/PO.
- Healthy backlog has top 2-3 sprints refined to task level.

## MVP vs Growth vs Scale

| Phase | Team Size | Priority | Scrum Approach |
|-------|-----------|----------|---------------|
| **MVP (0→1)** | 1-3 devs | Ship fast, learn faster | Kanban over Scrum. 1-week cycles. No formal ceremonies — async standup in Slack. Retro = 15 min at end of cycle. DoD: "deployed + doesn't crash." No story points — just break work into small tasks. |
| **Growth (1→10)** | 3-15 devs, SM may be rotating role or tech lead | Predictability + continuous improvement | Full Scrum: 2-week sprints, all ceremonies timeboxed, story points + velocity, backlog refinement weekly, retros with action items. |
| **Scale (10→N)** | 15+ devs, dedicated SMs (1 per 1-2 teams) | Cross-team alignment, scaling | Scaling framework (Nexus/LeSS/SAFe). Scrum of Scrums, cross-team refinement, integrated increment, shared DoD. Program-level metrics. |

**MVP rule:** Don't Scrum before you need it. A team of 3 doing daily standups, sprint planning, reviews, and retros for a 1-week cycle is ceremony overhead eating 20% of dev time. Kanban + 1 retro/week is enough.

## Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| Scrum board | GitHub Projects / Linear (free) / Trello (free) | Jira Software ($7.75/user/mo) | >10 people, need advanced reporting, or enterprise requirements |
| Retrospectives | Google Docs + Miro free (3 boards) | Miro Team ($8/user/mo) or Parabol ($6/user/mo) | Remote team >5 or need structured retro formats with voting |
| Sprint reports | Jira/GitHub built-in velocity chart (free) | ActionableAgile ($15/user/mo) | Need CFD, Monte Carlo forecasting, or flow metrics |
| Agile coaching | Internal champion reads Scrum Guide + blogs | Professional coach ($150-300/hr) | Team stuck, persistent dysfunction, or scaling to 3+ teams |
| Team health | Google Forms pulse survey, 1 question | Officevibe ($4/user/mo) or CultureAmp | >3 teams or need anonymized trend data |

**Annual Scrum tool budget by phase:** MVP: $0. Growth: $500-5K. Scale: $10K-100K.

## Scalability Decision Tree

```
Is your team size >7 people?
├── YES → Split into 2 teams. Optimal size: 5-7. Don't scale one team to 12.
└── NO → Single team is fine.

Are sprints consistently finishing with >30% carryover?
├── YES → <!-- DEEP: 10+min -->
Root cause: overcommitment? scope creep? unplanned work? Fix the cause.
└── NO → Carryover <20% is healthy.

Is velocity variance >30% sprint-over-sprint?
├── YES → Inconsistent sizing, team changes, scope changes. Stabilize.
└── NO → Stable enough for forecasting. Use 3-sprint rolling average.

Is cycle time >5 days for "ready to done" on average?
├── YES → Bottleneck. Check CFD. Apply WIP limits at constraint.
└── NO → Cycle time is healthy.

Are retro action items being completed?
├── YES → Improvement loop working.
└── NO → Reduce to 1 action item. Track visibly. Build the habit.

Do you have >3 teams on the SAME product?
├── YES → Cross-team coordination needed. Nexus or LeSS. Single Product Backlog.
└── NO → No scaling framework needed.
```


**What good looks like:** Team velocity tracked for 5+ sprints with predictable range. Sprint goal achieved in 8 of 10 sprints. Retro produces action items tracked to completion. Impediments removed within 24 hours. Team health score > 4/5 in retro survey.

## When NOT to Use This Skill (Overkill)

- **Solo developer or pair programming**: Scrum for 1-2 people is absurd. Use Kanban.
- **Team of 3 building an MVP in 2 weeks**: Ceremonies consume more time than they save. Async check-ins. Skip planning. 1 retro at the end.
- **Pure operations/support team (no development)**: Scrum is for complex product development. Ops teams do better with Kanban.
- **Research team with unpredictable work**: Sprints assume you can estimate. If you can't, use Kanban with explicit policies.
- **Team already high-performing with a different process (Shape Up, Kanban, XP)**: Don't "fix" what works. The goal is delivering value, not doing Scrum.

## Token-Efficient Workflow

```
# Step 1: Sprint health check (query from issue tracker API)
python3 scripts/sprint_health.py --team backend --output json
# Returns: {"sprint":"W15","committed":34,"completed":28,"carryover":6,
#           "velocity_3sprint_avg":31,"cycle_time_p85":4.2,"retro_items_done":2}

# Step 2: Decision tree → action
# carryover > 20% → Overcommitted. Reduce commitment by average carryover.
# cycle_time_p85 > 5 days → Check CFD for bottleneck. Apply WIP limit.
# retro_items_done == 0 → Retros need focus. Pick 1 action. Track.

# Step 3: Generate retrospective data (pull metrics before retro)
python3 scripts/retro_data.py --team backend --sprint 15 --output markdown

# Step 4: Verify improvement
python3 scripts/sprint_health.py --team backend --compare-sprint 14 --output json
# Exit code 0 = metrics improved, 1 = worsened
```

**Principle:** `sprint_health.py` queries Linear/Jira API, returns JSON. Agent reads numbers, not narratives. Retro data auto-generated. Improvement tracked via exit codes.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
The Scrum Master is a servant-leader who enables the team, removes impediments, and facilitates agile ceremonies. Coordination is about protecting the team while keeping stakeholders informed.

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Product Owner / Product Strategist** | Backlog refinement, sprint planning, stakeholder alignment | Sprint goals, backlog health, velocity trends, value delivery metrics |
| **Project Manager** | Cross-team dependencies, timeline expectations, resource changes | Impediments spanning multiple teams, delivery forecasts, capacity changes |
| **Engineering Lead / Tech Lead** | Technical debt, architecture decisions, engineering practices | Tech debt backlog, refactoring needs, pairing/mentoring, code quality metrics |
| **UX Designer** | Sprint readiness, design handoff, usability testing | Design-ready stories before sprint start, research findings integration |
| **QA Engineer** | Definition of Done, test automation, regression strategy | Done criteria adherence, test coverage trends, defect patterns |
| **DevOps / Platform Team** | CI/CD pipeline health, deployment cadence, environment availability | Pipeline failures, deployment blockers, environment provisioning |
| **Other Scrum Masters** | Cross-team coordination, Scrum of Scrums, dependency management | Team dependencies, shared impediments, agile practice alignment |
| **HR / People Ops** | Team health, conflict resolution, professional development | Team morale signals, skill gaps, training needs, interpersonal dynamics |
| **Security Reviewer** | Security requirements in Definition of Done | Security acceptance criteria, threat modeling participation |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Sprint goal at risk (mid-sprint) | Product Owner, Project Manager, Stakeholders | Early expectation management; scope negotiation possible |
| Blocked impediment not resolved in 24 hours | Engineering Lead, Project Manager | Escalation needed; team throughput affected |
| Team velocity drops by >30% for 2 consecutive sprints | Product Owner, Engineering Lead, Project Manager | Systemic issue; root cause investigation required |
| Team health check shows declining trend (2+ consecutive drops) | Engineering Lead, HR/People Ops | Burnout, conflict, or disengagement risk; intervention needed |
| Inter-team dependency not met by commitment date | Other Scrum Master, Project Manager | Downstream sprint impact; escalation to dependency owner |
| Definition of Done not met for >20% of sprint items | Product Owner, Engineering Lead, QA | Quality crisis; root cause in estimation, skills, or technical debt |
| Retrospective action items not completed 2 sprints in a row | Engineering Lead, Team | Continuous improvement credibility at risk; process trust erodes |
| Stakeholder bypassing Scrum process (direct task assignment to devs) | Product Owner, Project Manager | Process integrity; undermines sprint commitment and prioritization |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Team dysfunction or interpersonal conflict affecting delivery >2 sprints | **Engineering Lead** + HR/People Ops | Mediation or team composition change needed; beyond Scrum Master facilitation |
| Product Owner unavailable or unresponsive for >1 sprint | **Product Strategist** + Project Manager | Backlog unrefined; team cannot plan without PO engagement |
| Organizational impediment blocking team (budget, procurement, policy) | **CTO Advisor** or VP Engineering + Project Manager | Authority beyond team level; systemic blocker |
| Agile transformation resistance from senior leadership | **Agile Coach** (external) + CTO Advisor | Cultural change requires executive sponsorship |
| Team consistently over-committing and burning out (utilization >110% for 4+ sprints) | **Engineering Lead** + HR + Project Manager | Sustainability crisis; capacity protection needed |

## Scale Depth

### Solo (1 person, 0-100 users)
One Scrum Master serving 1 team part-time (often a developer wearing SM hat). Ceremonies: daily scrum (15 min), sprint planning (2 hours/biweekly), review + retro (1.5 hours combined). Backlog: Product Owner manages in Jira/Linear. No formal scaling needed. Metrics: velocity (basic), sprint burndown. SM focuses on facilitation + impediment removal, light coaching. Cost: $0-200/month (Jira/Linear). Overkill: SAFe, LeSS, Nexus, dedicated SM, agile coaching, portfolio Kanban.

### Small (2-10 people, 100-10K users)
Dedicated Scrum Master for 1-2 teams. Ceremonies standardized with team working agreements. Metrics: velocity, sprint burndown, cycle time, escaped defects. Retrospectives produce tracked action items. Sprint goal consistently achieved (>70% sprint success rate). SM coaches PO on backlog refinement. Cost: $200-1K/month. Overkill: scaling framework, release train, PI Planning.

### Medium (10-50 people, 10K-1M users)
2-3 Scrum Masters or Agile Coaches. Scaling: LeSS or Nexus for 3-8 teams on same product. Metrics: cumulative flow, throughput, lead time, defect density. Cross-team dependency management via Scrum of Scrums. SM community of practice. Agile health assessments (Spotify Squad Health Check). SM coaches leadership on agile principles. Cost: $2K-10K/month. Overkill: SAFe unless enterprise governance demands it.

### Enterprise (50+ people, 10K+ users)
Agile Coaches + Scrum Masters across multiple ARTs (SAFe) or product groups. Release Train Engineer (RTE) for PI Planning. Enterprise agile metrics: flow efficiency, time-to-market, employee NPS. Portfolio Kanban linking strategy to execution. Center of Excellence for agile practices. Value stream mapping. Cost: $20K-150K+/month.

### Transition Triggers
| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | 2+ teams needing SM, or sprint success rate <60% | Dedicate SM; standardize ceremonies; implement action tracking from retros |
| Small → Medium | 3+ teams on same product, cross-team dependencies blocking sprints | Adopt LeSS/Nexus; implement Scrum of Scrums; add agile health assessments |
| Medium → Enterprise | 5+ products, portfolio governance required, or 50+ developers | Adopt SAFe (if enterprise); add RTE role; implement portfolio Kanban; establish CoE |


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | project-manager | Project schedule, RAID log, milestone plan, resource allocation |
| **This** | scrum-master | Sprint plans, retrospectives, backlog refinement, velocity metrics |
| **After** | backend-developer | Working software increments delivered each sprint |

Common chains:
- **Chain**: project-manager → scrum-master → backend-developer — Project plan broken into sprints; the team delivers working increments.
- **Chain**: product-manager → scrum-master → qa-engineer — Backlog priorities become sprint goals; QA validates the sprint output.

## Sub-Skills

| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| **Sprint Facilitation** | Running sprint planning, daily scrum, review, and retrospective | Time-boxed facilitation, sprint goal crafting, capacity-based planning, visual boards (Miro, Jira) |
| **Backlog Refinement Coaching** | Backlog >2 sprints deep, stories lack clear acceptance criteria, or PO overwhelmed | INVEST criteria, story splitting patterns, 3-amigos sessions, estimation (story points, t-shirt sizing) |
| **Agile Metrics & Diagnostics** | Diagnosing delivery bottlenecks or reporting team health | Velocity trend, CFD, cycle time, throughput, escaped defects, sprint burndown — Jira, Linear, ActionableAgile |
| **Impediment Removal** | Systematic blockers slowing team velocity | Impediment log, escalation paths, cross-team facilitation, organizational blocker quantification in business impact |
| **Team Health & Psychological Safety** | Team engagement declining, conflict surfacing, or turnover rising | Retrospective formats (4Ls, sailboat, start-stop-continue), health checks, 1-on-1s, conflict mediation |
| **Scaling Scrum (LeSS/Nexus/SAFe)** | 3+ teams on same product or multi-team coordination needed | LeSS (2-8 teams, single product), Nexus (3-9 teams), SAFe (enterprise, 5+ products, PI Planning) |
| **Agile Transformation Coaching** | Organization transitioning from waterfall or ad-hoc to agile | Change management, leadership coaching, agile principles over practices, pilot teams, metrics-driven adoption |
| **DoR/DoD Facilitation** | Quality issues from unclear readiness or completion criteria | Definition of Ready (DoR) checklist, Definition of Done (DoD) with quality gates, team agreement, PO + team alignment |


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
- [ ] **[S1]**  Team charter established: purpose, norms, DoR, DoD, roles clarified and agreed
- [ ] **[S2]**  Product backlog exists with user stories, acceptance criteria, and relative size estimates
- [ ] **[S3]**  Sprint cadence fixed: sprint length, ceremony schedule
- [ ] **[S4]**  Sprint Planning produces a sprint goal, selected PBIs, and a task breakdown
- [ ] **[S5]**  Daily Scrums timeboxed at 15 minutes, focused on coordination toward sprint goal
- [ ] **[S6]**  Backlog Refinement occurs weekly (10% of capacity); top 2-3 sprints ready
- [ ] **[S7]**  Sprint Review demonstrates working increment; stakeholders provide feedback; backlog adapts
- [ ] **[S8]**  Sprint Retrospective produces 1-3 actionable improvement experiments tracked to completion
- [ ] **[S9]**  Agile metrics tracked: velocity (rolling avg), burndown, CFD, cycle time, escaped defects
- [ ] **[S10]**  Team health metric collected each sprint; declining trends addressed proactively
- [ ] **[S11]**  Impediment log maintained with resolution time tracked; systemic impediments escalated
- [ ] **[S12]**  DoD enforced: no PBI marked "Done" without meeting all DoD criteria
- [ ] **[S13]**  If multi-team: scaling framework selected; cross-team coordination operational
- [ ] **[S14]**  Retrospective action items integrated into sprint backlog and counted toward capacity

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Scrum Guide (Schwaber & Sutherland)](https://scrumguides.org/)
- [LeSS — Large-Scale Scrum](https://less.works/)
- [Nexus Guide](https://www.scrum.org/resources/nexus-guide)
- [SAFe Framework](https://scaledagileframework.com/)
- [Scrum.org — Evidence-Based Management](https://www.scrum.org/resources/evidence-based-management-guide)
- [Actionable Agile — Metrics for Predictability](https://actionableagile.com/)
