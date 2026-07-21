---
name: incident-responder
description: Incident response plans, on-call procedures, postmortems, runbooks, escalation policies, communication templates, and blameless SRE culture. Triggered by incident, on-call, postmortem, runbook, escalation, SRE, blameless.
author: Sandeep Kumar Penchala
---

# Incident Responder

Manage the full incident lifecycle: preparation, detection, response, recovery, and learning.
This skill provides battle-tested patterns for on-call rotations, incident command,
communication during outages, blameless postmortems, runbook automation, and building
a culture of reliability.

## When to Use

- Designing an incident response program from scratch or maturing an existing one
- Setting up on-call rotations, escalation policies, and alert routing in PagerDuty/OpsGenie
- Creating operational runbooks for known failure modes with automated remediation
- Running an incident as Incident Commander (IC) or serving in a support role
- Writing blameless postmortems and tracking action items to prevent recurrence
- Establishing incident severity levels (SEV1–SEV4) with clear definitions and response SLAs
- Designing communication templates for stakeholder updates during incidents
- Implementing SRE practices: error budgets, toil reduction, and reliability targets

## Core Workflow

### Phase 1: Incident Response Program Design
1. Define incident severity levels with clear, objective criteria:
   - **SEV1**: critical user-facing outage, data loss/corruption, security breach — page immediately, all-hands response.
   - **SEV2**: major feature degradation, significant latency — page on-call, resolve within 2 hours.
   - **SEV3**: minor feature impairment, partial degradation — create ticket, resolve within 24 hours.
   - **SEV4**: cosmetic issue, non-user-facing — address in next sprint.
2. Establish response SLAs: time to acknowledge (5 min for SEV1), time to engage (15 min), time to mitigate (varies).
3. Define incident roles and responsibilities:
   - **Incident Commander (IC)**: owns the incident, makes decisions, delegates tasks, communicates to stakeholders.
   - **Operations Lead (OL)**: investigates and implements mitigation; leads the technical response.
   - **Communications Lead (CL)**: drafts and sends stakeholder updates; manages the status page.
   - **Scribe**: documents the timeline of events, decisions, and actions in the incident channel/tool.
4. Set up incident channels: dedicated Slack/Teams channel per incident, war-room bridge (Zoom/Meet), and a status page.
5. Choose tooling: PagerDuty or OpsGenie for alerting and scheduling; FireHydrant or incident.io for incident management.

### Phase 2: On-Call and Escalation
1. Design on-call rotations with primary and secondary responders; avoid single points of failure.
2. Implement follow-the-sun rotations for global teams; balance on-call load fairly across the team.
3. Define escalation policies: if primary doesn't acknowledge within 5 minutes, escalate to secondary; if unresolved after 30 minutes, escalate to engineering manager.
4. Compensate on-call fairly: pay for on-call time and incident response; don't burn out your responders.
5. Protect on-call sleep: tune alerts to page only on user-impacting symptoms (SLO burn rate), not noisy infrastructure alerts.
6. Run on-call handoffs: outgoing on-call summarizes open incidents and known issues to incoming on-call.

### Phase 3: Incident Response Execution
1. **Declare the incident**: IC activates the incident channel, announces severity, and assigns roles.
2. **Triage**: OL assesses the blast radius, impact duration, and identifies potential causes (recent deploys, config changes, dependency failures).
3. **Mitigate, don't debug**: the goal is to restore service — rollback, scale up, fail over, feature-flag off; root cause analysis comes later.
4. **Communicate**: CL sends updates every 30 minutes (or at defined intervals) with: what's happening, what's impacted, what we're doing, estimated resolution.
5. **Escalate if needed**: if the incident isn't contained within the expected time, IC escalates to senior leadership and broader teams.
6. **Resolve**: once service is restored and monitoring confirms recovery, IC declares resolution, noting time and impact.

### Phase 4: Postmortem and Learning
1. Schedule the postmortem within 48 hours while memories are fresh; make attendance optional but encouraged.
2. Write a blameless postmortem document:
   - **Summary**: what happened, impact (duration, users affected, revenue loss), detection method.
   - **Timeline**: minute-by-minute log from detection to resolution, including decisions and communications.
   - **Root Causes**: contributing factors (process, technical, human) — use "Five Whys" or fault-tree analysis.
   - **What Went Well**: call out good decisions to reinforce positive behavior.
   - **What Went Wrong**: gaps in monitoring, runbooks, testing, or process.
   - **Action Items**: specific, assigned, time-bound improvements with severity (P0–P2).
3. Track action items in the team's backlog; review during sprint planning; don't let them rot.
4. Share postmortems broadly to spread learnings across the organization.
5. Hold postmortem readouts for SEV1/SEV2 incidents with leadership and cross-functional stakeholders.

### Phase 5: Continuous Improvement
1. Maintain a library of runbooks for all known failure modes; review and practice quarterly.
2. Conduct game days and chaos engineering experiments: inject failures in a controlled way to test response readiness.
3. Measure incident metrics and trend over time: MTTD (detect), MTTA (acknowledge), MTTR (resolve), number of SEV1s per quarter.
4. Use error budgets to drive reliability investments: when the budget is exhausted, freeze feature launches and prioritize reliability work.
5. Reduce toil: identify manual steps during incidents and automate them — runbook automation, auto-rollback, self-healing.

## Sub-Skills

When this skill is invoked, the agent may need to drill into these specialized areas:

| Sub-Skill | When to Use |
|-----------|-------------|
| `incident-detection` | Setting up monitoring, alerting rules, SIEM configuration, and anomaly detection |
| `incident-triage` | First response: severity classification, war room activation, and initial impact assessment |
| `containment-strategy` | Active incident response: isolation, access revocation, and kill-switch activation |
| `forensics` | Post-containment investigation: evidence collection, chain of custody, and timeline reconstruction |
| `rca-methodology` | Root cause analysis using 5-Whys, Ishikawa diagrams, fault tree analysis, and contributing factors |
| `postmortem` | Writing blameless postmortems with action items, tracking, and organizational learning |
| `tabletop-exercises` | Designing and facilitating incident scenarios, running game days, and after-action reviews |

## Cross-Skill Coordination

Incident responders must activate and coordinate a cross-functional war room. They direct developers to fix, DevOps to contain, security to investigate, communications to inform stakeholders, and leadership to manage external perception.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Security Engineer** | Security incidents, threat investigation | Detection rule context, IoCs, forensic tooling access, containment recommendations, threat intelligence |
| **DevOps Engineer** | Infrastructure incidents, deployment failures | Recent deploy log, infrastructure change timeline, rollback capability assessment, access for investigation |
| **Backend/Frontend Developer** | Service-specific incidents, code-level bugs | Service architecture context, recent code changes, known failure modes, SME expertise |
| **Observability Engineer** | Alert correlation, metric investigation | Dashboard links, metric trends, anomaly detection signals, log query assistance, trace analysis |
| **Compliance Officer** | Data breach, regulatory triggering events | Breach classification (PII/PHI exposure?), regulatory notification clock start, evidence preservation requirements |
| **Legal Advisor** | Customer data exposure, liability assessment | Legal obligations, communication constraints, external statement review |
| **Communications Lead (CL)** | All SEV1/SEV2 incidents | Status page updates, customer emails, internal stakeholder messages, media handling if applicable |
| **CTO/VP Engineering** | Prolonged SEV1, major customer impact | Situation briefs, resource requests, escalation decisions, external communication approval |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| SEV1 declared | All roles above + affected teams | War room activation; assign IC, OL, CL, Scribe |
| Incident not contained within 30 minutes | Engineering Manager | Escalation; additional resources may be needed |
| Incident not contained within 2 hours | VP Engineering, CTO | Executive visibility; external communication decision |
| Data breach confirmed (PII, PHI, financial data) | Compliance Officer, Legal Advisor | Regulatory clock starts; notification obligations assessed |
| Media/social media attention on incident | Communications Lead, CTO, PR | Reputation management; prepared statement required |
| Postmortem published | All involved teams + broader engineering | Organizational learning; action item assignment |

### Escalation Path

```
SEV1 — No acknowledgement in 5 min? → Secondary on-call → EM → Director → VP → CTO
Security breach confirmed? → CISO + CTO immediately
Customer data exposed? → CISO + Legal + CTO immediately
Regulatory notification required? → Compliance Officer → Legal → CEO
```

## Best Practices

- **Blameless culture is non-negotiable**: focus on systems and processes, not individuals. "You didn't cause this; the system allowed it to happen."
- **Delegate the IC role widely**: every engineer should run at least one incident to build organizational resilience.
- **Pre-write communication templates**: have templates for SEV1, SEV2, security incidents, and scheduled maintenance.
- **Page on symptoms, not causes**: "checkout error rate > 1%" is actionable; "CPU > 80%" is not necessarily.
- **Practice makes prepared**: run tabletop exercises quarterly and full game days twice a year.
- **Post-incident review of alert quality**: after every SEV1/SEV2, ask: was the page actionable? Should it have fired earlier?

## Production Checklist

- [ ] Incident severity levels defined (SEV1–SEV4) with clear, objective criteria and response SLAs
- [ ] On-call rotations configured with primary/secondary, escalation policies, and fair compensation
- [ ] Incident management tooling in place (PagerDuty, incident.io, FireHydrant) and tested
- [ ] Communication templates ready for SEV1/SEV2 incidents, security breaches, and scheduled maintenance
- [ ] Status page configured and updated automatically or via communications lead
- [ ] At least 5 runbooks documented for top failure modes; automation for the top 3
- [ ] Blameless postmortem template adopted; all SEV1/SEV2 incidents result in a postmortem within 48 hours
- [ ] Action item tracking integrated with the engineering backlog; overdue items escalated
- [ ] Incident metrics tracked (MTTD, MTTA, MTTR) with quarterly trend review
- [ ] Game day or chaos engineering exercise conducted within the last 6 months

## References

- Google SRE Book (Chapters 11–14): https://sre.google/
- PagerDuty Incident Response Documentation: https://response.pagerduty.com/
- Atlassian Incident Management Handbook: https://www.atlassian.com/incident-management
- Howie Guide to Postmortems: https://postmortems.io/
- Chaos Engineering Principles: https://principlesofchaos.org/
