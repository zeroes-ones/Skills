# Scale Depth

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
