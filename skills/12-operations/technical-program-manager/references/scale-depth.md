# Scale Depth

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
