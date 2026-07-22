---
name: incident-responder
description: Incident response plans, on-call procedures, postmortems, runbooks, escalation policies, communication templates, and blameless SRE culture. Triggered by incident, on-call, postmortem, runbook,
  escalation, SRE, blameless.
author: Sandeep Kumar Penchala
type: security
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- incident-responder
token_budget: 4000
chain:
  consumes_from:
  - chaos-engineer
  - compliance-officer
  - crisis-response-manager
  - observability-engineer
  - security-engineer
  - security-reviewer
  - site-reliability-engineer
  feeds_into:
  - compliance-officer
  - devops-engineer
  - security-engineer
output:
  type: code
  path_hint: ./
---
# Incident Responder

Manage the full incident lifecycle: preparation, detection, response, recovery, and learning.
This skill provides battle-tested patterns for on-call rotations, incident command,
communication during outages, blameless postmortems, runbook automation, and building
a culture of reliability.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Active incident happening now → Jump to "Core Workflow > Phase 2 (Containment)"
├── Write a postmortem → Go to "Core Workflow > Phase 4 (Learn & Postmortem)"
├── Create a runbook → Jump to "Core Workflow > Phase 1 (Prepare)" then "Sub-Skills > runbook-automation"
├── Set up on-call rotation → Go to "Core Workflow > Phase 1 (Prepare)"
├── Design escalation policy → Jump to "Core Workflow > Phase 1 (Prepare)"
├── Write incident communication template → Go to "Core Workflow > Phase 3 (Communication)"
├── Need security-specific containment → Invoke `security-engineer` skill instead
├── Need compliance reporting for breach → Invoke `compliance-officer` skill instead
├── Need observability and alerting → Invoke `observability-engineer` skill instead
├── Need reliability framework → Invoke `site-reliability-engineer` skill instead
└── Don't know where to start? → Follow "Core Workflow" sequentially: Detect → Contain → Resolve → Learn
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces. Incidents are high-stakes, time-sensitive, and information-sparse — rigid advice applied blindly makes things worse.

- **Every incident is different — playbooks are starting points, not scripts.** A runbook for "database connection timeout" may be the wrong response if the actual cause is a network partition, a kernel bug, or an active attack. Use playbooks as investigation frameworks, not step-by-step instructions to execute without thinking.
- **Never assume root cause without evidence.** The first hypothesis in an incident is usually wrong. Symptoms are often misleading — a CPU spike could be a traffic surge, a runaway query, a crypto miner, or a monitoring bug. State your hypothesis explicitly as a hypothesis and describe what evidence would confirm or disprove it.
- **Communication timing matters.** Premature external disclosure before you understand scope and impact can trigger unnecessary panic, regulatory reporting obligations, and loss of customer trust. Conversely, delaying too long erodes credibility. Recommend communication checkpoints aligned with incident severity and known facts — not speculation.
- **Preserve evidence before remediation.** Forensic artifacts — memory dumps, disk images, logs, network captures — are destroyed by remediation actions. Restarting a compromised instance, dropping a database connection, or rotating credentials before capturing evidence means you lose the ability to determine root cause. Always recommend an evidence preservation step before remediation steps.
- **Admit when you need more information to assess severity.** A vague "the site is down" could be a SEV1 customer-facing outage or a SEV4 staging environment blip. Without understanding blast radius, user impact, and duration, you cannot reliably recommend a response posture. Ask the clarifying questions before prescribing escalation.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Designing an incident response program from scratch or maturing an existing one
- Setting up on-call rotations, escalation policies, and alert routing in PagerDuty/OpsGenie
- Creating operational runbooks for known failure modes with automated remediation
- Running an incident as Incident Commander (IC) or serving in a support role
- Writing blameless postmortems and tracking action items to prevent recurrence
- Establishing incident severity levels (SEV1–SEV4) with clear definitions and response SLAs
- Designing communication templates for stakeholder updates during incidents
- Implementing SRE practices: error budgets, toil reduction, and reliability targets

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Incident Severity Classification
```
                     ┌──────────────────────────┐
                     │ START: Declare incident  │
                     └───────────┬──────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ Is customer-facing service          │
              │ completely unavailable?             │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ > 50% of users   │  │ Is core functionality│
        │ affected?        │  │ degraded or data at  │
        └──┬───────────┬───┘  │ risk?                │
           │ YES       │ NO   └──┬───────────────┬───┘
           ▼           ▼        │ YES           │ NO
      ┌────────┐ ┌──────────┐   ▼               ▼
      │ SEV1   │ │ SEV2     │ ┌────────┐  ┌───────────┐
      │Page all │ │Page on-  │ │ SEV2   │  │ SEV3/SEV4 │
      │hands    │ │call      │ │Page on-│  │Ticket,    │
      │5 min ack│ │15 min ack│ │call    │  │next       │
      └────────┘ └──────────┘ └────────┘  │business   │
                                          │day        │
                                          └───────────┘
```
**When to declare SEV1:** Complete outage of core product. Data loss or corruption confirmed. Security breach with active exploitation. PagerDuty alerts all engineering.  
**When SEV3/SEV4:** Cosmetic issue, non-blocking, workaround available. Affects < 5% of users. No data risk. Create ticket, address in next sprint.

### Escalation Trigger
```
                     ┌────────────────────────────┐
                     │ START: Should we escalate? │
                     └─────────────┬──────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Incident unresolved after target time?   │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ SEV1 > 30 min?   │    │ Continue current     │
        │ SEV2 > 2 hours?  │    │ response. Reassess   │
        └──┬───────────┬───┘    │ at next check-in.    │
           │ YES       │ NO    └──────────────────────┘
           ▼           ▼
    ┌────────────┐ ┌──────────────┐
    │ Escalate   │ │ Set 30-min   │
    │ to EM →    │ │ check-in.    │
    │ Director   │ │ Escalate if  │
    │ → VP → CTO │ │ still stale. │
    └────────────┘ └──────────────┘
```
**When to escalate:** SEV1 not contained within 30 minutes. Customer data potentially exposed. Decision needed beyond IC authority (external comms, legal exposure).  
**When to hold:** Progress is being made. Mitigation is active and working. ETA to resolution is credible and within SLA.

### Postmortem Depth
```
                     ┌───────────────────────────┐
                     │ START: Postmortem depth?  │
                     └───────────┬───────────────┘
                                 │
              ┌──────────────────▼──────────────────┐
              │ SEV1 or SEV2?                       │
              └────┬────────────────────┬───────────┘
                   │ YES                │ NO
                   ▼                    ▼
        ┌──────────────────┐  ┌──────────────────────┐
        │ Full postmortem: │  │ Light postmortem:    │
        │ Timeline, 5-Whys,│  │ Summary, timeline,   │
        │ action items,    │  │ 1-2 action items.    │
        │ readout to execs │  │ No exec readout.     │
        │ within 48 hours  │  └──────────────────────┘
        └──────────────────┘
```
**When full postmortem required:** Customer data loss or exposure. Revenue loss > $10K. Regulatory notification triggered. Mean time to resolve > 4 hours.  
**When light postmortem suffices:** SEV3 with quick resolution. Known failure mode with existing runbook. No user impact or < 1% user impact.

### Runbook Automation Priority
```
                     ┌──────────────────────────────┐
                     │ START: Which runbooks to     │
                     │ automate first?              │
                     └─────────────┬────────────────┘
                                   │
              ┌────────────────────▼────────────────────┐
              │ Has this incident occurred > 2x in     │
              │ the last quarter?                       │
              └────┬──────────────────────┬─────────────┘
                   │ YES                  │ NO
                   ▼                      ▼
        ┌──────────────────┐    ┌──────────────────────┐
        │ Automate now.    │    │ Is manual resolution │
        │ P0: Build self-  │    │ error-prone (> 5    │
        │ healing or 1-    │    │ manual steps)?      │
        │ click runbook.   │    └──┬───────────────┬───┘
        └──────────────────┘       │ YES           │ NO
                                   ▼               ▼
                            ┌────────────┐  ┌──────────────┐
                            │ Automate   │  │ Document +   │
                            │ within 2   │  │ review       │
                            │ sprints    │  │ quarterly    │
                            └────────────┘  └──────────────┘
```
**When to automate immediately:** Recurring incident (> 2x/quarter). Resolution requires > 10 minutes of human time. Error rate in manual resolution > 10%.  
**When documentation suffices:** Incident occurred once and root cause was permanently fixed. Resolution is simple (restart service, scale up). Annual recurrence expected.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Incident Response Program Design
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

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): On-Call and Escalation
1. Design on-call rotations with primary and secondary responders; avoid single points of failure.
2. Implement follow-the-sun rotations for global teams; balance on-call load fairly across the team.
3. Define escalation policies: if primary doesn't acknowledge within 5 minutes, escalate to secondary; if unresolved after 30 minutes, escalate to engineering manager.
4. Compensate on-call fairly: pay for on-call time and incident response; don't burn out your responders.
5. Protect on-call sleep: tune alerts to page only on user-impacting symptoms (SLO burn rate), not noisy infrastructure alerts.
6. Run on-call handoffs: outgoing on-call summarizes open incidents and known issues to incoming on-call.

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Incident Response Execution
1. **Declare the incident**: IC activates the incident channel, announces severity, and assigns roles.
2. **Triage**: OL assesses the blast radius, impact duration, and identifies potential causes (recent deploys, config changes, dependency failures).
3. **Mitigate, don't debug**: the goal is to restore service — rollback, scale up, fail over, feature-flag off; root cause analysis comes later.
4. **Communicate**: CL sends updates every 30 minutes (or at defined intervals) with: what's happening, what's impacted, what we're doing, estimated resolution.
5. **Escalate if needed**: if the incident isn't contained within the expected time, IC escalates to senior leadership and broader teams.
6. **Resolve**: once service is restored and monitoring confirms recovery, IC declares resolution, noting time and impact.

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Postmortem and Learning
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

<!-- DEEP: 10+min -->
### Phase 5 (~25 min): Continuous Improvement
1. Maintain a library of runbooks for all known failure modes; review and practice quarterly.
2. Conduct game days and chaos engineering experiments: inject failures in a controlled way to test response readiness.
3. Measure incident metrics and trend over time: MTTD (detect), MTTA (acknowledge), MTTR (resolve), number of SEV1s per quarter.
4. Use error budgets to drive reliability investments: when the budget is exhausted, freeze feature launches and prioritize reliability work.
5. Reduce toil: identify manual steps during incidents and automate them — runbook automation, auto-rollback, self-healing.


### Cross-skills Integration
```bash
# Infrastructure reliability → Incident response → Security containment → Compliance reporting
/site-reliability-engineer && /incident-responder && /security-engineer
/observability-engineer && /incident-responder && /compliance-officer
# SRE provides infrastructure context. Security handles threat containment. Compliance manages reporting obligations.
```

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
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

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `observability-engineer` | Dashboard links, metric trends, anomaly detection signals, log query assistance, trace analysis | Before declaring incident severity or launching war room investigation |
| `security-engineer` | Detection rule context, IoCs, forensic tooling access, containment recommendations, threat intelligence | Before classifying as security incident or engaging threat response |
| `site-reliability-engineer` | Incident severity classification, communication templates, postmortem ownership, runbook procedures | Before activating incident command roles or escalating |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `security-engineer` | Incident scope, affected systems, blast radius assessment, containment status | Security team operates blind — threat can spread unchecked |
| `compliance-officer` | Breach classification, regulatory clock start time, evidence chain of custody | Regulatory notification deadlines missed — legal liability |
| `devops-engineer` | Infrastructure incident context, recent deploy log, change timeline, rollback assessment | DevOps can't contain infrastructure failures — outage extends |


**What good looks like:** Incident timeline documented with all decisions and actions. Root cause identified and confirmed. Containment completed within SLA (SEV1 < 1 hour). Post-mortem published within 48 hours with action items, owners, and due dates.

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Incident response = you get an alert on your phone. You fix it. No on-call rotation. No severity levels. No postmortems. No runbooks. Monitoring = basic health checks. Alerting = maybe a Slack notification.
- **What to skip**: On-call rotation. Escalation policies. Severity classification (SEV1–SEV4). Incident commander role. Postmortem process. Runbook automation. Status page. Game days.
- **Coordination**: You are the entire response team. Direct fix, no coordination overhead.

### Small Team (2-10 people, 100-10K users)
- **What changes**: On-call rotation (primary/secondary). Basic severity levels (SEV1–SEV3). PagerDuty/OpsGenie with escalation policies. Postmortems for SEV1s. 3-5 runbooks for common failures. Status page (manual updates). Incident channel in Slack/Teams. Basic alerting (uptime, error rate, latency).
- **What to skip**: Dedicated incident commander training for all engineers. War room bridge (use Slack huddle). Game days. Error budgets. SRE practices. External communications lead.
- **Coordination**: On-call handoff at rotation change. SEV1 postmortem within 1 week shared with team. Monthly incident review (15 min).

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Formal incident response program. SEV1–SEV4 severity with objective criteria. Dedicated incident management tooling (incident.io, FireHydrant). Automated status page updates. Runbook library with 10+ documented scenarios. Game days twice a year. Postmortem for all SEV1/SEV2 (< 48 hours). Incident metrics tracked (MTTD, MTTA, MTTR). Error budgets with feature freeze gates. Communication templates for all severity levels.
- **What to skip**: Full chaos engineering program. Dedicated incident response team (on-call rotation across engineering). External communications firm on retainer.
- **Coordination**: Quarterly game day. Monthly incident metric review. Postmortem readouts for SEV1/SEV2 with leadership. Weekly on-call health check (burnout monitoring).

### Enterprise (50+ people, 1M+ users)
- **What changes**: Dedicated incident response team or SRE organization. Chaos engineering program with regular production experiments. Automated runbook remediation (self-healing). Incident response as a service across business units. Regulatory incident reporting pipelines (GDPR 72-hour, PCI DSS). Executive incident communication protocols. External communications firm on retainer. Incident simulation with cross-functional teams (engineering, legal, PR, support). Continuous improvement via incident analysis ML/trending.
- **What's full production**: Incident response platform with automated workflows. SLO-based alerting (burn rate, not threshold). Postmortem action tracking integrated with engineering backlog. Real-time incident dashboards for executive visibility. Quarterly board-level reliability reporting.
- **Coordination**: Weekly SRE/incident response sync. Monthly cross-business-unit incident review. Quarterly reliability review with CTO. Annual incident response maturity assessment.

### Transition Triggers
| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| **Solo → Small** | Second engineer joins. First incident you couldn't fix because you were asleep. | Add on-call rotation + basic severity levels + postmortem template. |
| **Small → Medium** | > 2 SEV1s per quarter. Customers notice downtime before you do. > 10K users. | Formal severity classification, dedicated incident tooling, game day program, error budgets. |
| **Medium → Enterprise** | Multiple business units with independent services. Regulatory compliance (GDPR, PCI DSS). Public incident covered by media. | Dedicated SRE/IR team, chaos engineering, automated remediation, regulatory notification pipeline. |

## What Good Looks Like

> An incident is declared, the on-call responder acknowledges within 90 seconds, and the incident commander opens a structured war room with pre-built communication channels within three minutes. Runbooks fire automatically based on alert signatures, status pages update without human intervention, and customer-facing messaging goes out within fifteen minutes of confirmed impact. The postmortem is blameless, published within 48 hours, and every action item is tracked to completion. Mean time to detect keeps dropping quarter over quarter because the monitoring surface grows faster than the alert noise.

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Blameless culture is non-negotiable**: focus on systems and processes, not individuals. "You didn't cause this; the system allowed it to happen."
- **Delegate the IC role widely**: every engineer should run at least one incident to build organizational resilience.
- **Pre-write communication templates**: have templates for SEV1, SEV2, security incidents, and scheduled maintenance.
- **Page on symptoms, not causes**: "checkout error rate > 1%" is actionable; "CPU > 80%" is not necessarily.
- **Practice makes prepared**: run tabletop exercises quarterly and full game days twice a year.
- **Post-incident review of alert quality**: after every SEV1/SEV2, ask: was the page actionable? Should it have fired earlier?


### Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|------------|-----|--------|
| Breach undetected for 6 months -- attacker had persistent access | No security monitoring (SIEM, EDR) deployed; no alerting on anomalous authentication patterns | Deploy SIEM with detection rules aligned to MITRE ATT&CK; enable EDR on all endpoints; monitor authentication logs for anomalous patterns | Without monitoring, you don't have incident response -- you have a post-mortem of how long the breach went unnoticed |
| Ransomware spread from one compromised desktop to entire server fleet | Containment was slow because incident commander hesitated to pull the network cable; no isolation runbook existed | Establish pre-approved isolation authority for IC; write and practice containment runbooks; automate host quarantine via EDR during incidents | Speed of containment determines blast radius -- hesitation during the first 15 minutes costs millions |
| Insider threat exfiltrated 50GB of source code over 3 months -- no alerts | Only monitored perimeter threats; no DLP, no UEBA, no anomalous data access detection | Implement DLP for outbound data patterns; deploy UEBA for anomalous user behavior; alert on bulk data access/download events | Insider threats need different signals than external attacks -- access patterns and data volumes reveal the insider that firewalls miss |
| Investigation stalled because key logs had already rotated off production servers | Log retention was set to 24 hours; no centralized log aggregation; forensic artifacts destroyed before investigation began | Set minimum 90-day log retention for security-relevant logs; ship logs to SIEM or S3 with immutability; preserve evidence before remediation | Forensic artifacts destroyed by remediation are lost forever -- always capture evidence before restarting, rotating, or rebuilding |
| Playbook not followed during active SEV1 -- team improvised, made the outage worse | Playbooks were out of date, nobody had practiced them, and the content was buried in a wiki nobody reads | Keep playbooks version-controlled in incident management tool; run tabletop exercises quarterly; embed runbooks in the tool so they surface during incidents | An unread playbook is theater -- it must be exercised, trusted, and surfaced at the moment of need |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Incident severity levels defined (SEV1–SEV4) with clear, objective criteria and response SLAs
- [ ] **[S2]**  On-call rotations configured with primary/secondary, escalation policies, and fair compensation
- [ ] **[S3]**  Incident management tooling in place (PagerDuty, incident.io, FireHydrant) and tested
- [ ] **[S4]**  Communication templates ready for SEV1/SEV2 incidents, security breaches, and scheduled maintenance
- [ ] **[S5]**  Status page configured and updated automatically or via communications lead
- [ ] **[S6]**  At least 5 runbooks documented for top failure modes; automation for the top 3
- [ ] **[S7]**  Blameless postmortem template adopted; all SEV1/SEV2 incidents result in a postmortem within 48 hours
- [ ] **[S8]**  Action item tracking integrated with the engineering backlog; overdue items escalated
- [ ] **[S9]**  Incident metrics tracked (MTTD, MTTA, MTTR) with quarterly trend review
- [ ] **[S10]**  Game day or chaos engineering exercise conducted within the last 6 months

## References
<!-- QUICK: 30s -- links to deeper reading -->
- Google SRE Book (Chapters 11–14): https://sre.google/
- PagerDuty Incident Response Documentation: https://response.pagerduty.com/
- Atlassian Incident Management Handbook: https://www.atlassian.com/incident-management
- Howie Guide to Postmortems: https://postmortems.io/
- Chaos Engineering Principles: https://principlesofchaos.org/
