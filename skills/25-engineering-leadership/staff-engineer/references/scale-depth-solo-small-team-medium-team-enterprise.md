# Scale Depth: Solo → Small Team → Medium Team → Enterprise

<!-- DEEP: 10+min -->
<!-- STANDARD: 2min — how the role changes as the org grows -->

### Solo (1 person, 0-100 users)
- **What changes**: No staff engineer role. Everyone is an IC doing everything. The concept doesn't
  apply — there's no "across teams" when there's one team.
- **What to skip**: Everything. Come back when you have 3+ teams.
- **Coordination**: N/A.

### Small Team (1-2 teams, 100-10K users)
- **What changes**: First staff engineer is often the most senior IC who naturally bridges backend,
  frontend, and infrastructure. Role is informal — you're "the person who figures out the hard
  stuff." RFCs are lightweight (1-2 pages). Design reviews happen at the whiteboard. No formal
  office hours; just be approachable.
- **What to skip**: Formal decision frameworks (socialize them in person). Quarterly health reports
  (weekly engineering sync covers it). External brand building (focus on internal impact first).
- **Coordination**: Weekly 1:1 with CTO. Pair-program with every engineer at least once a month.
  One shared `decisions.md` file for ADRs.

### Medium Team (5-10 teams, 10K-1M users)
- **What changes**: You now focus on 3-5 teams, not all of them. RFC process is formal (template,
  comment period, design review). Office hours are scheduled. You have a defined EM counterpart for
  each team. Mentoring shifts to tech leads — you help them grow into staff-level thinking. Start
  external visibility: one conference talk per year.
- **What to skip**: Organization-wide architecture governance (that's the CTO's domain). Vendor
  evaluation (unless deeply technical). Hiring decisions (consult, don't decide).
- **Coordination**: Bi-weekly 1:1 with CTO. Weekly sync with each EM. Monthly design review with
  all tech leads. Async RFC process. Formal ADR repository. Quarterly technical health report.

### Enterprise (10+ teams, 1M+ users, multiple staff engineers)
- **What changes**: You are one of several staff engineers, each with a domain (platform, product
  architecture, data, security). You coordinate with each other through a staff engineering forum
  (bi-weekly). You likely have a Principal Engineer above you setting org-wide technical strategy.
  Your scope narrows but deepens. External visibility is expected — conferences, open-source,
  industry working groups.
- **What to skip**: Trying to understand every team's codebase (impossible, focus on your domain).
  Attending every design review (send a delegate). Being the escalation point for everything (that's
  what the Principal Engineer is for).
- **Coordination**: Staff engineering forum (bi-weekly). Monthly 1:1 with CTO/Principal Engineer.
  Quarterly domain strategy review. Formal mentorship program. Published decision frameworks
  maintained as living documents. Annual external impact report.
