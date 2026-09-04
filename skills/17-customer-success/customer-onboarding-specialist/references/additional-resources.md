# Additional Resources — customer-onboarding-specialist

> Deep knowledge loaded on demand. Playbook templates, health-score design, and reference material.

## Playbook Templates

### One-Page Success Plan (fill at kickoff)
| Field | Content |
|-------|---------|
| Customer & segment | Acme Corp — Enterprise (ACV $180K) |
| Business goals (their words) | Reduce manual reporting time by 50% across 3 teams |
| Success metrics (their numbers) | 3 teams live by day 60; reporting time down 50% by day 90 |
| First value event | First automated report delivered to their exec team |
| Target time-to-value | 45 days |
| Milestones (owner, date) | Day 7 SSO done; Day 21 first data sync; Day 45 value event |
| Executive sponsor / champion | CTO (sponsor) / Ops lead (champion) |
| Risks | Data migration complexity; sponsor availability |
| Definition of done | Value event reached + repeated; adoption at target; customer self-sufficient |

### Health Score Design (weighted)
| Input | Weight | Red | Yellow | Green |
|-------|--------|-----|--------|-------|
| Value events reached | 40% | 0 events | 1 event | 2+ events / repeated |
| Adoption vs milestones | 25% | >2 behind | 1 behind | On/above pace |
| Usage trend (30d) | 15% | Down >50% | Down 10-50% | Flat or up |
| Sponsor engagement | 10% | Unreachable | Low | Active |
| Support sentiment | 10% | Escalations, P1s | Some friction | Healthy |

### Risk Triggers & 48-Hour Playbook
| Trigger | First action (within 48h) |
|---------|---------------------------|
| No value event by day 30 | Interview users; find the friction; re-scope to smaller value slice |
| Usage drop >50% over 2 weeks | Contact; re-anchor on success plan; re-train champion; set next value date |
| Sponsor departure | Notify account-manager; re-secure sponsor; re-confirm priorities |
| Unresolved P1 support issue | Escalate support; keep customer informed; protect the value event |
| Missed kickoff commitments | Re-plan with owners; escalate if the customer side is not resourcing |

## War Stories

- **The $200K account that churned "successfully":** Onboarding completed every checklist item in 60 days. The customer quietly never used the core workflow — the team logged in, attended trainings, and then went back to their old tool. Churn surfaced at month 9 renewal. Lesson: checklist-complete onboarding without a reached value event is the most expensive kind of failure; it looks healthy until renewal.
- **The security review that doubled TTV:** Every enterprise deal slipped 5-6 weeks because SSO and security review started after implementation planning. Fixing it took one change: start security day one, in parallel, with a two-sided owner. TTV dropped by a month across the segment. Lesson: the longest pole sets time-to-value — know which step it is before you start.
- **The handoff that restarted the account:** A CSM inherited a customer with no artifact and spent a month re-learning the account. The account stalled; expansion slipped a quarter. Fix: the handoff artifact (health, adoption, risks, success plan) is a hard gate before any transition. Lesson: context is the handoff; the meeting is just the ceremony.

## Reference Material

- Gainsight / ChurnZero / Catalyst — health-score and journey-orchestration patterns
- SaaS metrics references — time-to-value, activation rate, early-churn correlation studies
- Product-led growth onboarding patterns — in-product checklists, empty states, activation emails
- Customer-success playbooks — segment-based onboarding depth and handoff standards
