# Project Management Frameworks

> **Author:** Sandeep Kumar Penchala

A comprehensive reference for project management methodologies, templates, and tools. Companion to the [Project Manager SKILL.md](../SKILL.md).

---

## 1. Methodology Selection

### Decision Matrix by Project Type

| Methodology | Best For | Team Size | Project Duration | Requirements |
|---|---|---|---|---|
| **Scrum** | Product development with evolving requirements | 3–9 per team | 1+ months | Product Owner available; cross-functional team |
| **Kanban** | Continuous delivery, ops, support, maintenance | Any | Ongoing | Stable priorities; flow-based work |
| **Scrumban** | Teams transitioning from Scrum needing flexibility | 3–9 | Ongoing | Mature Scrum practices + WIP limits |
| **Waterfall** | Regulatory compliance, construction, fixed-scope | Any | 3–12 months | Requirements fully known upfront |
| **Shape Up** | Product teams wanting 6-week cycles | 2–4 per cycle | 6 weeks | Senior ICs; appetite-based scoping |

### Methodology Selector Flowchart
```
Is scope fixed and fully known?
  ├─ Yes → Waterfall
  └─ No → Is work continuous and event-driven?
           ├─ Yes → Kanban
           └─ No → Does team benefit from timeboxed iterations?
                    ├─ Yes → Scrum (or Scrumban if hybrid needed)
                    └─ No → Shape Up
```

---

## 2. Project Charter Template

```markdown
# Project Charter: [Project Name]

## Problem Statement
[1–2 paragraphs describing the problem and why it matters now]

## Scope
### In Scope
- [Deliverable 1]
- [Deliverable 2]

### Out of Scope
- [Explicitly excluded item 1]
- [Explicitly excluded item 2]

## Success Criteria (SMART)
1. [Specific, Measurable, Achievable, Relevant, Time-bound goal]
2. [Goal 2]

## Stakeholders
| Name | Role | Interest | Influence (H/M/L) |
|---|---|---|---|
| [Name] | Executive Sponsor | Budget + strategic alignment | H |
| [Name] | Product Owner | Feature requirements | H |
| [Name] | Engineering Lead | Technical feasibility | M |

## Key Risks
| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| [Risk 1] | M | H | [Mitigation strategy] |

## Timeline & Milestones
| Phase | Dates | Key Deliverables |
|---|---|---|
| Discovery | Week 1–2 | Requirements doc, architecture plan |
| Build Sprint 1 | Week 3–4 | MVP features |
| UAT | Week 5 | User acceptance sign-off |
| Launch | Week 6 | Production deployment |

## Budget
| Category | Estimate | Notes |
|---|---|---|
| Engineering (4 devs × 6 weeks) | $XX,XXX | Internal cost |
| Infrastructure | $X,XXX | Cloud + tools |

## Approvals
- [ ] Executive Sponsor: ___________ Date: _______
- [ ] Engineering Lead: ___________ Date: _______
```

---

## 3. Risk Management

### Risk Register Template

| ID | Risk Description | Category | Probability (1–5) | Impact (1–5) | Score | Trigger | Mitigation | Contingency | Owner |
|---|---|---|---|---|---|---|---|---|---|
| R01 | Key engineer leaves mid-project | Resource | 3 | 5 | 15 | Resignation notice | Cross-train; document tribal knowledge | Contract backup freelancer | EM |
| R02 | Third-party API deprecation | Technical | 2 | 4 | 8 | Deprecation announcement | Abstract integration behind interface | Negotiate extended support window | Tech Lead |
| R03 | Scope creep from stakeholder requests | Scope | 4 | 3 | 12 | >3 unplanned features proposed | Change control process; steering committee | Escalate to sponsor for prioritization | PM |

### Probability × Impact Matrix

```
     IMPACT ──►
     1 (Negligible)  2 (Minor)  3 (Moderate)  4 (Major)  5 (Critical)

P  5 │  Med    High   High   Critical  Critical
R  4 │  Low    Med    High   High      Critical
O  3 │  Low    Med    Med    High      High
B  2 │  Low    Low    Med    Med       High
A  1 │  Low    Low    Low    Low       Med

Critical (15–25): Escalate to steering committee; active daily monitoring
High (10–14): Mitigation plan with weekly review
Medium (5–9): Monitor; plan contingency
Low (1–4): Accept; periodic review
```

### Mitigation vs Contingency
- **Mitigation:** Proactive action to reduce probability or impact (e.g., load testing before launch)
- **Contingency:** Reactive plan if risk materializes (e.g., rollback plan if deployment fails)
- **Budget rule:** Mitigation cost should be ≤ Risk Score × $Impact

---

## 4. Stakeholder Management

### RACI Matrix

| Task | Executive Sponsor | Product Owner | Engineering Lead | Design Lead | QA Lead |
|---|---|---|---|---|---|
| Approve budget | A | C | C | I | I |
| Define requirements | C | A/R | C | C | I |
| Design UI | I | C | I | R | I |
| Implement features | I | C | A/R | C | I |
| Test & validate | I | C | C | C | R |
| Launch approval | A | R | C | C | C |

**R** = Responsible (does the work) | **A** = Accountable (signs off) | **C** = Consulted (input needed) | **I** = Informed (kept in loop)

### Stakeholder Map: Power vs Interest

```
     INTEREST ──►
     Low                High

P   High │ Keep Satisfied    │ Manage Closely       │
O        │ (Executive)       │ (Product Owner, EM)  │
W   ─────┼───────────────────┼──────────────────────┤
E   Low  │ Monitor           │ Keep Informed        │
R        │ (Peripheral dept) │ (End users, support) │
```

### Communication Plan Template

| Stakeholder Group | Information Need | Format | Frequency | Owner |
|---|---|---|---|---|
| Executive Sponsor | Status (RAG), budget, milestones | 1-page dashboard + 15-min call | Bi-weekly | PM |
| Core Team | Tasks, blockers, decisions | Standup + sprint board | Daily + sprint cadence | Scrum Master |
| Extended Stakeholders | Highlights, key decisions, timeline | Email newsletter | Monthly | PM |
| End Users | Release notes, training | In-app notification + wiki | Per release | Product |

---

## 5. Project Tracking

### Burndown Chart
Tracks remaining work against the sprint/iteration timeline.
```
Work Remaining (Story Points)
  │
40│╲
30│  ╲___
20│      ╲___  ← Ideal burndown
10│          ╲___  ← Actual (above line = behind)
 0│______________╲___
      Day 1    Day 5    Day 10
```

### Burnup Chart
Tracks completed work vs total scope (shows scope creep).
```
Work (Story Points)
  │                    ╱ Total Scope (creeping up = scope creep)
50│              ╱─────
40│         ╱────
30│    ╱────          ← Completed
20│╱───
  │___________________
      Sprint 1  Sprint 2  Sprint 3
```

### Velocity Tracking
- **Velocity:** Average story points completed per sprint (last 3–5 sprints)
- **Use for:** Capacity planning, NOT performance evaluation
- **Anti-pattern:** Pressuring team to "increase velocity"

### Cumulative Flow Diagram

```
Tickets
  │
  │  Backlog ──────────────────────────
  │       ╲
  │        ╲  In Progress ─────────────
  │         ╲     ╲
  │          ╲     ╲  Review ──────────
  │           ╲     ╲    ╲
  │            ╲     ╲    ╲  Done ─────
  │_____________________________________
              Time
```
- Widening "In Progress" band → bottleneck
- Widening "Backlog" → scope creep
- Narrow "Done" band → low throughput

---

## 6. Meeting Cadence

| Meeting | Duration | Frequency | Participants | Purpose |
|---|---|---|---|---|
| **Daily Standup** | 15 min | Daily | Delivery team | Sync, not solve |
| **Sprint Planning** | 2 hrs / week of sprint | Per sprint | Team + PO | Commit to sprint scope |
| **Backlog Refinement** | 1–2 hrs | Weekly or mid-sprint | Team + PO | Groom upcoming stories |
| **Sprint Review** | 1 hr / week of sprint | End of sprint | Team + stakeholders | Demo working software |
| **Retrospective** | 90 min | End of sprint | Team only | Continuous improvement |
| **Stakeholder Update** | 30 min | Bi-weekly | PM + sponsors | Status, risks, decisions |
| **Steering Committee** | 60 min | Monthly | Executives | Strategic direction, budget |

---

## 7. Project Closure

### Post-Mortem Template

```markdown
# Post-Mortem: [Project Name]
**Date:** [Date] | **Facilitator:** [Name] | **Attendees:** [List]

## Project Summary
- **Goal:** [One-line objective]
- **Timeline:** [Planned vs Actual]
- **Budget:** [Planned vs Actual]
- **Key Metric:** [Target vs Actual]

## What Went Well (Keep Doing)
1. [Item] — Owner: [Name]
2. [Item]

## What Didn't Go Well (Start Doing Differently)
1. [Item] — Root cause: [Cause] — Proposed fix: [Fix] — Owner: [Name]
2. [Item]

## Systemic Root Causes
| Issue | Root Cause | Category (Process/Tech/People) | Preventative Action |
|---|---|---|---|

## Lessons Learned
1. [Actionable insight that applies to future projects]

## Action Items
| ID | Action | Owner | Deadline |
|---|---|---|---|
| AI-01 | [Action] | [Name] | [Date] |
```

### Knowledge Transfer Checklist
- [ ] Architecture Decision Records (ADRs) committed to repo
- [ ] Runbooks updated with deployment/rollback procedures
- [ ] Monitoring dashboards handed off to on-call team
- [ ] API documentation published
- [ ] Stakeholder sign-off obtained
- [ ] Access permissions transferred or revoked
- [ ] Retrospective completed and action items logged
- [ ] Project folder archived (decisions, contracts, wireframes)

---

## 8. PM Tools Comparison

| Tool | Best For | Team Size | Key Strength | Weakness | Pricing |
|---|---|---|---|---|---|
| **Jira** | Enterprise; regulated industries | 50+ | Customizable workflows, compliance | Heavy; steep learning curve | $8.15–$16/user/mo |
| **Linear** | Engineering-first startups | 5–100 | Speed, keyboard-driven, GitHub integration | Limited non-engineering use | Free–$14/user/mo |
| **Asana** | Cross-functional (marketing, ops) | 10–500 | Timeline view, portfolios | Overkill for pure engineering | Free–$25/user/mo |
| **Notion** | All-in-one wiki + PM | 3–50 | Docs + databases, flexible | No native sprint tracking | Free–$18/user/mo |
| **Monday.com** | Visual, non-technical teams | 10–200 | Colorful dashboards, automations | Pricey at scale | $9–$19/user/mo |
| **GitHub Projects** | Open source; GitHub-native | 3–50 | Integrated with code/issues | Basic feature set | Free–enterprise |

### Selection Heuristic
- **Pure engineering team + speed → Linear**
- **Multi-department + compliance → Jira**
- **Wiki-heavy + flexible → Notion**
- **Open source + GitHub-native → GitHub Projects**
- **Visual dashboards + automations → Monday.com**

---

*Select the methodology and tools that fit your team's context, not the latest trend. The best framework is the one your team actually uses consistently.*
