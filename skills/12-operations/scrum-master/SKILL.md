---
name: scrum-master
description: Sprint planning, daily standups, retrospectives, backlog refinement, velocity tracking, burndown charts, team health, impediment removal, agile metrics.
author: Sandeep Kumar Penchala
---

# Scrum Master

Agile delivery leadership system for guiding Scrum teams from forming through high-performance. Covers all Scrum ceremonies, metrics-driven continuous improvement, impediment removal, and scaling frameworks.

## When to Use

- Establishing or resetting Scrum practices for a new or underperforming team
- Coaching a team through sprint planning — effective story decomposition, estimation, sprint goal crafting
- Facilitating retrospectives that produce actionable, tracked improvement experiments
- Diagnosing delivery bottlenecks through agile metrics: velocity variance, cycle time, cumulative flow, escaped defects
- Protecting the team from external interference while maintaining stakeholder transparency
- Scaling Scrum across multiple teams with LeSS, SAFe, or Nexus
- Onboarding a team to Scrum from waterfall or ad-hoc processes
- Improving Product Owner and Development Team collaboration on backlog health and refinement

## Core Workflow

### Phase 1: Team Formation & Foundations

1. **Team Chartering** — Purpose, norms, Definition of Ready (DoR), Definition of Done (DoD), roles clarified.
2. **Backlog Establishment** — User story format, ordered by value (WSJF for complex prioritization), relative sizing (Fibonacci), top 2-3 sprints refined.
3. **Sprint Cadence** — 2 weeks standard. Fixed ceremony schedule. Protect the rhythm.

### Phase 2: Ceremony Facilitation

1. **Sprint Planning** (4hr for 2-week sprint) — What: PO presents sprint goal, team pulls PBIs. How: decompose PBIs into tasks (≤8hrs each). Commit to sprint goal, not individual PBIs.
2. **Daily Scrum** (15 min) — Team coordination, not status report. Walk board right-to-left.
3. **Backlog Refinement** (10% of capacity) — Weekly. Review, split, estimate, add acceptance criteria.
4. **Sprint Review** (1hr/week of sprint) — Collaborative inspection of increment + backlog adaptation.
5. **Sprint Retrospective** (1.5hr for 2-week sprint) — Gather data → generate insights → decide 1-3 improvement experiments → close.

### Phase 3: Metrics, Impediments & Scaling

1. **Agile Metrics** — Velocity (3-sprint rolling avg), Sprint Burndown, Cumulative Flow Diagram (CFD), Cycle Time, Escaped Defects, Team Health, Sprint Goal Success Rate.
2. **Impediment Removal** — External and internal impediments. Maintain impediment log. Track resolution time.
3. **Scaling** — Nexus (3-9 teams), LeSS (up to 8 teams, single backlog), SAFe (if organizational mandate). Goal: minimize cross-team dependencies.

## Best Practices

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
├── YES → Root cause: overcommitment? scope creep? unplanned work? Fix the cause.
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

## Production Checklist

- [ ] Team charter established: purpose, norms, DoR, DoD, roles clarified and agreed
- [ ] Product backlog exists with user stories, acceptance criteria, and relative size estimates
- [ ] Sprint cadence fixed: sprint length, ceremony schedule
- [ ] Sprint Planning produces a sprint goal, selected PBIs, and a task breakdown
- [ ] Daily Scrums timeboxed at 15 minutes, focused on coordination toward sprint goal
- [ ] Backlog Refinement occurs weekly (10% of capacity); top 2-3 sprints ready
- [ ] Sprint Review demonstrates working increment; stakeholders provide feedback; backlog adapts
- [ ] Sprint Retrospective produces 1-3 actionable improvement experiments tracked to completion
- [ ] Agile metrics tracked: velocity (rolling avg), burndown, CFD, cycle time, escaped defects
- [ ] Team health metric collected each sprint; declining trends addressed proactively
- [ ] Impediment log maintained with resolution time tracked; systemic impediments escalated
- [ ] DoD enforced: no PBI marked "Done" without meeting all DoD criteria
- [ ] If multi-team: scaling framework selected; cross-team coordination operational
- [ ] Retrospective action items integrated into sprint backlog and counted toward capacity

## References

- [Scrum Guide (Schwaber & Sutherland)](https://scrumguides.org/)
- [LeSS — Large-Scale Scrum](https://less.works/)
- [Nexus Guide](https://www.scrum.org/resources/nexus-guide)
- [SAFe Framework](https://scaledagileframework.com/)
- [Scrum.org — Evidence-Based Management](https://www.scrum.org/resources/evidence-based-management-guide)
- [Actionable Agile — Metrics for Predictability](https://actionableagile.com/)
