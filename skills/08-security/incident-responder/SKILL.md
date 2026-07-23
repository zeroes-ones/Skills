---
name: incident-responder
description: >
  Use when responding to active incidents, designing on-call rotations, writing
  postmortems, creating runbooks, establishing escalation policies, or building
  incident communication templates. Handles incident command, detection and triage,
  containment and recovery, blameless postmortem facilitation, runbook automation,
  and on-call rotation design. Do NOT use for observability stack setup, CI/CD
  pipeline design, or security vulnerability assessment.
license: MIT
tags:
- incident
- on-call
- postmortem
- runbook
- escalation
- blameless
- response
- sre
author: Sandeep Kumar Penchala
type: security
status: stable
version: 1.1.0
updated: 2026-07-23
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
---
# Incident Responder

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Manage the full incident lifecycle: preparation, detection, response, recovery, and learning.
This skill provides battle-tested patterns for on-call rotations, incident command,
communication during outages, blameless postmortems, runbook automation, and building
a culture of reliability.

## Route the Request
<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains(".pagerduty/config.yml", "service")` or `file_exists("opsgenie.yml")` | Jump to "Core Workflow > Phase 2 (Containment)" — on-call tooling detected, assume active incident support |
| A2 | `file_exists("runbooks/", "postmortems/")` and `file_contains("runbooks/*.md", "severity")` | Go to "Core Workflow > Phase 1 (Prepare)" — runbook infrastructure exists, assess readiness |
| A3 | `file_exists("postmortems/")` and `file_contains("postmortems/*.md", "root.cause")` | Jump to "Core Workflow > Phase 4 (Learn & Postmortem)" — postmortem patterns detected |
| A4 | `file_contains(".github/ISSUE_TEMPLATE/incident.md", "severity")` or `file_exists("incident-response/playbooks/")` | Go to "Core Workflow > Phase 1 (Prepare)" — incident templates found, verify completeness |
| A5 | `file_contains("docker-compose.yml", "grafana")` or `file_contains("docker-compose.yml", "prometheus")` | Go to "Core Workflow > Phase 5 (Monitoring & Detection)" — observability stack detected, check alert coverage |
| A6 | `file_contains("terraform/", "pagerduty")` or `file_contains("terraform/", "opsgenie")` | Go to "Core Workflow > Phase 1 (Prepare)" — IaC-managed on-call detected, verify rotation config |
| A7 | `file_exists(".github/workflows/incident.yml")` or `file_exists(".github/workflows/postmortem.yml")` | Jump to "Core Workflow > Phase 4 (Learn & Postmortem)" — automated incident workflows detected |
| A8 | `file_contains("README.md", "incident")` or `file_exists("INCIDENT.md")` | Go to "Core Workflow > Phase 1 (Prepare)" — incident documentation exists, assess completeness |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

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
└── Not sure? → Describe the problem in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else
<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to prescribe remediation before evidence preservation.** Restarting a compromised instance, dropping connections, or rotating credentials destroys forensic artifacts | Trigger: `grep -rn "restart\|reboot\|rotate.credential\|drop.connection"` in proposed action + no preceding `grep -rn "preserve\|capture\|dump\|snapshot\|forensic"` | STOP. Respond: "Preserve evidence before remediation. Capture: memory dump, disk image, relevant logs, network flows. Only then execute remediation." |
| **R2** | **REFUSE to declare root cause without confirmed evidence.** The first hypothesis in an incident is usually wrong — a CPU spike could be traffic surge, runaway query, crypto miner, or monitoring bug | Trigger: response contains "root cause is" or "caused by" but `grep -c "hypothesis\|evidence\|confirm\|disprove"` < 1 in the response | STOP. Reword: "My current hypothesis is [X]. Evidence that would confirm: [A], [B]. Evidence that would disprove: [C]. Before acting, verify:" |
| **R3** | **REFUSE to recommend external communication without severity + blast-radius confirmation.** Premature disclosure triggers panic and regulatory obligations; delayed disclosure erodes trust | Trigger: response contains "notify customers\|status page update\|public disclosure\|press release" but no preceding statement of confirmed SEV level, blast radius, and user impact count | STOP. Respond: "Before external communication: (1) confirm SEV level, (2) quantify blast radius (% users affected), (3) identify impact type (data loss/availability/integrity). Only then recommend communication." |
| **R4** | **REFUSE to recommend "all-hands war room" for SEV3/SEV4 incidents.** Over-including people burns organizational incident response capacity and creates alert fatigue | Trigger: response contains "war room\|all hands\|full team" and severity context is SEV3, SEV4, or unconfirmed | STOP. Respond: "War room scale should match severity. SEV1: IC + comms lead + SMEs. SEV2: primary on-call + 1 expert. SEV3/SEV4: on-call responder alone. Do not escalate until severity is confirmed." |
| **R5** | **STOP and ASK when severity cannot be determined from available data.** "The site is down" could be SEV1 (customer-facing outage) or SEV4 (staging environment blip) | Trigger: request mentions incident symptoms but no SEV level, user-impact count, or blast radius is stated or inferable from context | STOP. Ask: "To assess severity: (1) What % of users are affected? (2) Is this production or staging? (3) Is there data loss/corruption? (4) Did the issue start suddenly or gradually?" |
| **R6** | **DETECT and WARN about runbook rot.** Runbooks referencing deprecated dashboards, retired services, or former team members waste precious minutes during incidents | Trigger: `grep -rn "last.updated\|last.reviewed" runbooks/*.md` returns dates > 90 days ago, or runbook mentions a service not found via `grep -rl "service.name" docker-compose* terraform/` | WARN: "Runbook [name] appears stale — last updated >90 days ago and/or references services not found in current infrastructure. Runbooks must be exercised quarterly. Verify before relying on this during an incident." |
| **R7** | **DETECT and WARN about undocumented incidents.** Incidents resolved without documentation cannot be trended, learned from, or prevented | Trigger: user describes a past incident but `grep -rl "postmortem\|incident.report\|after.action"` returns no matching file for the described event | WARN: "This incident appears undocumented. Every incident — even a 5-minute blip — must produce a timeline and root cause note. Create a postmortem now to capture key events while memory is fresh." |


## The Expert's Mindset

Master incident responders know that quality is not found — it is **engineered into the process**. They don't catch bugs; they make bugs uneconomical to produce.

| Cognitive Bias | Mitigation |
|----------------|------------|
| **Automation bias** — trusting tool output without verification | Every automated finding gets a human "sniff test" before action |
| **Perfect quality fallacy** — pursuing zero defects at infinite cost | Define explicit quality gates with economic thresholds; know when good enough is good enough |
| **Recency effect** — over-weighting the last failure you saw | Maintain a risk register ranked by probability × impact, not recency |
| **Normalization of deviance** — accepting degrading quality as the new normal | Trend your quality metrics; any downward slope triggers a review, not just threshold breaches |

### What Masters Know That Others Don't
- **Where the bodies are buried** — the 3 components most likely to fail and why
- **How to make quality self-service** — the best quality gate is the one developers run before they push
- **The economics of defects** — cost-to-fix grows 10x at each stage (dev → CI → staging → production)

### When to Break Your Own Rules
- **Ship it broken (with a flag).** Sometimes you need production data to understand the failure mode.
- **Skip the test for throwaway code.** If the code lives < 1 week, a manual check suffices.
## Operating at Different Levels

| Level | Scope | You... |
|-------|-------|--------|
| **L1** | Single test/review | Execute defined quality procedures; follow checklists |
| **L2** | Feature quality | Own quality for a feature area; write custom test strategies |
| **L3** | System quality | Design quality strategy for a system; define gates and thresholds; mentor |
| **L4** | Org quality | Define org-wide quality standards; make investment cases for quality tooling |
| **L5** | Industry quality | Create quality methodologies adopted across the industry |

**Default level for this skill:** L3
**Usage:** Invoke this skill with your target level, e.g., "as an L3 incident responder, review..."

For full level definitions, see `skills/00-framework/skill-levels/SKILL.md`.

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

## Proactive Triggers

| Trigger | Action | Rationale |
|---|---|---|
| No runbook exists for a critical service or component | Propose runbook creation; prioritize services with highest customer impact and lowest operational familiarity | An undocumented service in an incident is a blind spot — the team learns how it works while it's on fire |
| MTTR (Mean Time to Resolve) shows upward trend for 2+ quarters | Propose incident process audit: review recent postmortems for process gaps, alert design, and runbook effectiveness | Rising MTTR signals systemic degradation — either alerts are noisier, runbooks are stale, or on-call is overwhelmed |
| New service or dependency added to production without incident playbook | Flag for incident readiness review; ensure alerting, runbook, and escalation path exist before the service handles traffic | New services fail in novel ways — having no runbook guarantees extended MTTR on the first incident |
| Alert-to-noise ratio exceeds 30% (fewer than 1 in 3 alerts corresponds to real incidents) | Audit alerting rules; reduce threshold sensitivity; page on symptoms (user-facing error rate), not causes (CPU > 80%) | Alert fatigue causes responders to ignore real incidents — every false alarm erodes trust in the paging system |
| Postmortem action items not completed within 2 sprints | Escalate to engineering manager; action items with no owner or deadline are organizational debt that guarantees incident recurrence | Unresolved action items mean the same incident class will happen again — postmortems without follow-through are theater |
| No game day or chaos engineering exercise conducted in 6+ months | Schedule tabletop exercise for top failure mode; game days reveal stale runbooks and untested assumptions before production does | Runbooks that have never been exercised are documentation, not preparedness — the first execution during a real incident is too late |
| Compliance breach notification clock started (GDPR 72-hour, PCI DSS) | Activate compliance workflow; preserve evidence chain of custody; engage legal and communications | Regulatory deadlines are non-negotiable — every hour of delay increases legal and financial exposure |

**Service Interaction Designs:**

| Interaction | Design Detail |
|---|---|
| Incident ↔ Observability | Alert correlation: group related alerts into a single incident to reduce noise and reveal causal chains. Dashboard drill-down: incident commander's dashboard links directly to service dashboards, log explorers, and trace viewers for the affected time window. Anomaly detection triggers pre-incident investigation before alert threshold is breached. |
| Incident ↔ SRE | Post-mortem ownership: SRE owns postmortem process, action item tracking, and reliability improvement backlog. Error budget integration: incidents consume error budget; budget exhaustion triggers feature freeze. Runbook maintenance: SRE ensures runbooks are tested and updated quarterly. |
| Incident ↔ DevOps | Deployment freeze during SEV1: automated rollback capability verified before incident response begins. Infrastructure change log surfaced during incident triage — recent deployments are the #1 trigger. Secret rotation workflow activated automatically during security incidents. |
| Incident ↔ Security | Security incident classification overlay on SEV severity: SEV1 + security = immediate security engineer + CISO engagement. IoC sharing between incident response and threat detection. Forensic evidence preservation before remediation (snapshot impacted systems before restarting/rebuilding). |
| Incident ↔ Communications | Pre-written communication templates for SEV1, SEV2, security incidents, and scheduled maintenance. Status page auto-update from incident management tool. Customer-facing messaging approved and published within 15 minutes of confirmed impact. Executive briefing template for SEV1 with business impact summary. |

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

## Anti-Patterns
<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Hero culture: praising the engineer who resolved a SEV1 at 3 AM solo without following process — incentivizes bypassing IR procedures and burning out "heroes" | Build systems, not heroes. Every "heroic" save is a process failure. Require that every SEV1/SEV2 resolution follows documented runbook steps with an incident commander | `grep -rn "single.handedly\|hero\|solo\|alone.*resolved" postmortems/*.md` → finds hero-culture language in postmortems | Add a postmortem template check: `grep -c "incident.command\|IC.role\|runbook" postmortems/*.md` must be ≥ 2; CI rejects hero-language patterns |
| Blame-oriented postmortems: asking "who caused this?" instead of "what in our system allowed this?" — kills psychological safety, drives incidents underground | Every postmortem must be blameless by policy. Focus on systemic controls that would have prevented the incident regardless of individual actions | `grep -rn "\bwho\b.*caused\|human.error\|operator.error\|blame\|fault" postmortems/*.md` → flags blame-oriented language | Pre-commit hook: `grep -rli "human.error\|operator.error\|caused by.*person" postmortems/*.md` blocks commits; require "system allowed" phrasing |
| Runbook rot: writing runbooks once and never updating — references deprecated dashboards, retired services, or former team members | Runbooks exercised quarterly; updated within 1 sprint of any service change. Version-controlled with last-reviewed date in metadata | `grep -rn "last.reviewed" runbooks/*.md` → check dates; flag if > 90 days. `grep -rl "deprecated\|retired\|former" runbooks/` → flag stale references | CI job runs `runbook-staleness-check.sh` weekly: if last-reviewed > 90 days OR references services not in current infra, auto-create Jira ticket |
| Alert fatigue normalization: accepting "most alerts are noise" as fact — responders stop investigating, start acknowledging-without-reading | Monthly alert quality audit: every alert must be actionable. Kill or tune top 20% by volume. Any alert firing >10 times without true positive gets removed | `grep -rn "silenced\|acknowledged.*without\|noise\|false.positive"` in incident logs or chat transcripts → measures fatigue language. `curl -s pagerduty-api/alerts?status=acknowledged\&since=30d` → count ack-only resolutions | Alert quality dashboard with SLA: if alert fires >10 times in 7 days with zero true positives, auto-suppress and notify on-call lead. Quarterly "kill the top 20%" sprint |
| Postmortem theater: running the postmortem process but never completing action items — "we'll look into it" with no owner, deadline, or tracking | Every action item needs owner, due date, and escalation on overdue. Track in engineering backlog alongside feature work, not a separate silo | `grep -rn "will.look\|consider\|maybe\|later\|TODO" postmortems/*.md` → finds non-actionable follow-ups. `grep -c "owner:\|due:\|assignee:" postmortems/*.md` → checks ownership | CI postmortem linter: rejects postmortems where action-item-to-owner ratio < 1. Dashboard tracks overdue items; auto-escalate at due-date + 7 days |
| Silent incidents: incidents resolved without documentation because "it was a quick fix" — cannot trend, learn from, or prevent undocumented failures | Every incident — even a 5-minute blip — must produce a timeline and root cause note. Minimum: date, duration, symptom, resolution, root cause hypothesis | `grep -rn "resolved\|fixed\|hotfix\|rolled.back"` in chat/commits with no corresponding postmortem file within 48 hours → detects silent incidents | Alert-to-postmortem correlation: if PagerDuty alert fires and resolves but no postmortem PR appears in 48 hours, auto-create a lightweight incident record |
| On-call as dumping ground: assigning on-call only to junior engineers or one team while rest of engineering is unaccountable | On-call rotates across ALL engineers who ship to production. You build it, you carry the pager. Rotate IC role widely to build organizational resilience | `grep -rn "on.call\|oncall\|pager" .github/CODEOWNERS team.yml` → check rotation coverage; flag if only 1 team or only junior engineers listed | PagerDuty rotation coverage check: if any production service has < 3 on-call engineers, auto-escalate to EM. Quarterly rotation audit enforces minimum participation |
| All-hands war room for SEV2: pulling 15 people into an incident call for non-critical issues — burns organizational IR capacity | War rooms scale to severity: SEV1 → IC + comms lead + SMEs; SEV2 → primary on-call + 1 expert; SEV3/SEV4 → on-call alone | `grep -rn "war.room\|incident.call\|bridge"` in incident records + cross-reference SEV level → flag SEV2/SEV3 incidents with >5 participants | Incident tooling auto-creates channels scaled to severity. SEV3/SEV4 default to 2-person limit; adding beyond that requires SEV escalation approval |

## Error Decoder
<!-- DEEP: 5min -- each entry includes a console-string matcher for automatic recovery loops -->

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `grep -rn "Connection.*refused\|connection.*timeout\|ECONNREFUSED" /var/log/app/*.log` + `curl -s http://localhost:${PORT}/health` returns non-200 | Service unreachable — users report 502/503 errors. Monitoring dashboard shows red for the service but green for upstream dependencies | Database connection pool exhausted, upstream timeout not propagated, or network partition between service and data tier | 1. Check connection pool metrics (`SHOW PROCESSLIST` or equivalent). 2. If pool exhausted, increase pool size and add circuit breaker. 3. Verify network ACLs and security groups allow traffic on all required ports | 1. `grep -rn "ECONNREFUSED\|connection.*refused"` → identify affected service. 2. `curl -s health-endpoint` → confirm status. 3. Check pool metrics → identify bottleneck. 4. Apply fix (expand pool / restart with drain / fix network) → `curl -s health-endpoint` → 200 → monitor 5min |
| `grep -rn "OutOfMemoryError\|OOM\|memory.leak\|heap.space" /var/log/app/*.log` + `ps aux \| grep java` shows RSS > Xmx | Service crashes with OOM every 30-90 minutes after restart. Memory graph shows steady climb, not spike | Memory leak in application code (unclosed resources, growing cache, or unbounded collection), or heap configured too small for workload | 1. Capture heap dump before restart (`jmap -dump:live`). 2. Analyze with Eclipse MAT or similar. 3. Identify leak source (top retainers by size). 4. Apply fix and verify heap stabilizes over 4-hour soak | 1. `grep -rn "OOM\|heap"` → confirm memory pressure. 2. `jmap -dump:live,format=b,file=heap.hprof PID` → preserve evidence. 3. Restart service for immediate relief. 4. Analyze heap dump → fix leak → deploy → monitor heap 4hrs → flat = resolved |
| `grep -rn "Unauthorized\|401\|403\|access.denied\|invalid.token" /var/log/auth/*.log \| wc -l` > threshold + `grep -rn "brute.force\|multiple.failures"` matches | Spike in 401/403 responses — legitimate users locked out while attacker probes credentials. Auth service latency increasing | Credential stuffing attack, expired token signing key, or IAM policy change revoked legitimate access | 1. Check if spike is attack (same IPs, varied usernames) or misconfig (varied IPs, specific endpoints). 2. If attack: enable rate limiting, block source IPs. 3. If misconfig: audit recent IAM/secret rotation changes, revert if needed | 1. `grep -c "401" auth.log` → spike confirmed. 2. `grep -oP "src_ip=\S+" auth.log \| sort \| uniq -c \| sort -rn \| head` → identify attack pattern vs misconfig. 3. Apply rate limit / IP block or revert config. 4. `grep -c "401" auth.log` → count returns to baseline |
| `grep -rn "data.*exfil\|outbound.*transfer\|egress.*anomaly" /var/log/network/*.log` + `grep -rn "large.*upload\|bulk.*export" /var/log/app/*.log` | Unusual outbound data transfer from database-tier subnet to external IP — 500MB+ egress in 5 minutes. No scheduled backup or ETL job running | Data exfiltration via compromised credential, SQL injection with `INTO OUTFILE`, or insider threat running bulk export | 1. Isolate source host (network quarantine, not shutdown — preserve memory). 2. Capture network flows, process list, and active connections. 3. Identify exfiltration method and data scope. 4. Initiate breach notification if PII/PHI involved | 1. `tcpdump -i eth0 -w exfil.pcap host SOURCE_IP` → capture. 2. `iptables -A OUTPUT -s SOURCE_IP -j DROP` → isolate. 3. `ps aux \| grep SOURCE_IP` → identify process. 4. Assess data scope → breach notification if needed → rotate all credentials → forensic analysis |
| `grep -rn "disk.full\|no.space\|ENOSPC\|quota.exceeded" /var/log/syslog` + `df -h` shows /var or /data at 100% | Application returns 500 errors on write operations. Logs stopped writing. Database reports "no space left on device" | Log rotation failed (logrotate config error or daemon stopped), runaway log generation (DEBUG level in production), or unmonitored data growth | 1. Identify large files: `du -sh /var/log/* \| sort -rh \| head -10`. 2. Compress and archive old logs. 3. Fix log rotation config. 4. Add disk-space monitoring alert at 80% and 90% thresholds | 1. `df -h` → confirm disk full. 2. `du -sh /var/* \| sort -rh \| head -5` → find culprit. 3. `logrotate -f /etc/logrotate.conf` → force rotation. 4. `df -h` → confirm space recovered → fix rotation config → add monitoring alert |
| `grep -rn "certificate.*expired\|SSL.*error\|TLS.*handshake\|x509" /var/log/nginx/*.log` + `openssl s_client -connect HOST:443 \| openssl x509 -noout -dates` shows expired | All HTTPS endpoints returning ERR_CERT_DATE_INVALID in browsers. Internal service-to-service mTLS failing with TLS handshake errors | TLS certificate expired — no monitoring on certificate expiry dates. Auto-renewal (cert-manager, ACME) failed silently or was never configured | 1. Verify expiry: `openssl x509 -in cert.pem -noout -enddate`. 2. If production-down: issue emergency cert, deploy. 3. Root cause: verify auto-renewal cron/cert-manager is running. 4. Add expiry monitoring: alert at 30d, 14d, 7d, 3d, 1d | 1. `openssl s_client -connect HOST:443 2>&1 \| grep -A2 "Verify return code"` → confirm. 2. `certbot renew --force-renewal` or `kubectl delete certificate NAME` → trigger renewal. 3. `curl -sI https://HOST` → confirm 200. 4. `echo "\$(openssl x509 -enddate)" \| grep -q "expired"` → verify not expired |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Incident severity levels defined (SEV1–SEV4) with objective criteria and response SLAs | `grep -rn "SEV1\|SEV2\|SEV3\|SEV4\|severity.level\|response.SLA" policies/ incident-response/` → must return ≥ 4 severity definitions with time-based SLAs | Generate severity-levels.md template with SEV1–SEV4 definitions, examples per level, and PagerDuty-compatible SLA mapping |
| **[S2]** | On-call rotations configured with primary/secondary, escalation policies, and fair compensation | `curl -s -H "Authorization: Token token=${PD_TOKEN}" "https://api.pagerduty.com/schedules" \| jq '.schedules \| length'` → must return ≥ 1 schedule; `curl -s .../escalation_policies \| jq '. \| length'` → ≥ 1 | Run `pagerduty-oncall-bootstrap.sh` to create default rotation with 2 levels of escalation if none exist |
| **[S3]** | Incident management tooling in place (PagerDuty, incident.io, FireHydrant) and tested | `grep -rn "pagerduty\|incident.io\|firehydrant\|opsgenie" .github/ terraform/ docker-compose*` → must find integration config | Generate tooling integration checklist: webhook test to PagerDuty, auto-create Slack channel on incident declare, status page auto-update |
| **[S4]** | Communication templates ready for SEV1/SEV2, security breaches, and scheduled maintenance | `find templates/ postmortems/templates/ -name "*template*" -o -name "*communication*" \| wc -l` → must be ≥ 3 (SEV1, SEV2, security) | Generate comm-templates/ with: sev1-internal.md, sev1-customer.md, security-breach.md, maintenance.md — with fill-in sections |
| **[S5]** | Status page configured and updated automatically or via communications lead | `grep -rn "statuspage\|status.io\|atlassian.status\|cachet" terraform/ docker-compose*` → must find status page provider config | Generate status-page-integration.sh: webhook from monitoring → auto-update component status on incident declare/resolve |
| **[S6]** | At least 5 runbooks documented for top failure modes; automation for the top 3 | `find runbooks/ -name "*.md" \| wc -l` → ≥ 5. `grep -rl "automation\|auto.remediation\|script" runbooks/ \| wc -l` → ≥ 3 | Run `runbook-coverage-check.sh`: cross-reference last 12 months of incidents with existing runbooks; flag uncovered failure modes |
| **[S7]** | Blameless postmortem template adopted; all SEV1/SEV2 incidents result in postmortem within 48 hours | `grep -rn "blameless\|postmortem.template\|after.action" .github/ postmortems/` → template found. `find postmortems/ -name "*.md" -mtime -60 \| wc -l` → matches expected incident count | CI check: if PagerDuty incident resolved > 48 hours ago with no postmortem PR, auto-create draft postmortem from template |
| **[S8]** | Action item tracking integrated with engineering backlog; overdue items escalated | `grep -rn "action.item\|follow.up\|corrective" postmortems/*.md` and verify each has Jira/GitHub issue link → all action items must have external ticket ID | Postmortem linter CI: reject postmortems where action items lack `tracking:` field. Run `overdue-actions.sh` weekly to find items past due date |
| **[S9]** | Incident metrics tracked (MTTD, MTTA, MTTR) with quarterly trend review | `grep -rn "MTTD\|MTTA\|MTTR\|mean.time.to" dashboard/ metrics/` → must find metric definitions. `curl -s monitoring-api/incident-metrics?range=90d` → data exists | Generate incident-metrics-dashboard.json for Grafana: MTTD/MTTA/MTTR trend lines, incident count by severity, top failure modes |
| **[S10]** | Game day or chaos engineering exercise conducted within last 6 months | `grep -rn "game.day\|chaos.engineering\|tabletop\|gameday" postmortems/ runbooks/` and check date → must find exercise record within 180 days | Generate game-day-template.md with: scenario, runbook to test, success criteria, participant roles. Schedule recurring quarterly calendar event |
| **[S11]** | Log retention meets minimum 90 days for security-relevant logs; shipping to centralized SIEM/S3 with immutability | `grep -rn "retention.*days\|log.retention\|retention_days" terraform/ docker-compose*` → must be ≥ 90. `grep -rn "siem\|log.aggregation\|s3.*log\|loki\|elastic" terraform/` → destination configured | Generate log-retention-audit.sh: enumerate all log sources, check retention config, flag any < 90 days or not shipping to centralized store |
| **[S12]** | Alert quality audited monthly: every alert must be actionable; top 20% by volume killed or tuned quarterly | `curl -s pagerduty-api/alerts?since=30d \| jq 'group_by(.alert_key) \| map({key: .[0].alert_key, count: length}) \| sort_by(-.count)'` → review top 20% | Run `alert-quality-audit.sh` monthly: for top 20% alerts by volume, check true-positive rate; auto-suppress < 5% TPR alerts and notify on-call lead |

## Footguns
<!-- DEEP: 10+min — war stories from the incident command trenches -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Silenced a SEV1 alert as "known noisy alert" — it was a real data exfiltration that ran undetected for 4 hours while the on-call slept | A security monitoring alert fired at 2:14 AM for 8TB of outbound data from the primary database. The on-call engineer checked their phone, recognized the alert as a pattern they'd seen 3 times that week (all false positives from a backup job), and silenced it. At 6:30 AM, a customer reported their data on Pastebin. The alert was real — a compromised API key was exporting customer records. 94,000 records exfiltrated. | Alert fatigue: the backup job alert had fired 17 times in 7 days with no tuning. The team had normalized "that loud alert" as background noise. The silencing action had no secondary verification — one engineer, one decision, one click. | **Never let a single human silence a SEV1-class alert without a second review.** Require that any silenced P0/P1 alert auto-escalates to a secondary on-call after 15 minutes with the message: "Alert X was silenced by [name] at [time]. Confirm or escalate." Tune alert thresholds within 48 hours of the second false positive — every false positive trains the team to ignore real signals. Run a quarterly "alert audit": sort all alerts by volume, kill or tune the top 20%. |
| Postmortem blamed "human error" for the 5th consecutive incident — same S3 bucket misconfiguration caused 3 data leaks over 8 months because nobody fixed the root provisioning path | A Terraform module for S3 buckets defaulted to `acl = "private"` but had no `block_public_access` setting. Three separate incidents occurred where engineers copied the module, overrode `acl = "public-read"` for a specific use case, and leaked data. Each postmortem's corrective action was "retrained the engineer on S3 security." The fourth incident leaked 340,000 PII records to a public bucket. | The postmortem process treated each incident as an isolated human failure rather than a systemic control gap. The corrective action ("train the human") addressed the symptom, not the cause: the Terraform module allowed public ACLs without guardrails. | **After every incident, ask: "What control would have prevented this regardless of who was on call?"** If the answer is "training," you haven't found the root cause. For the S3 case: add an SCP that denies `s3:PutPublicAccessBlock` removal, add a `block_public_access = true` default in the module with a `prevent_destroy` lifecycle, and scan for public buckets every 15 minutes. Human error is a starting point for investigation, not a root cause. |
| Runbook said "notify CISO at 555-0127" — the CISO had left the company 8 months ago and the number was reassigned to an intern's desk phone | A ransomware attack encrypted the primary database at 11:00 PM Saturday. The IR runbook's escalation path listed the former CISO's direct line. The on-call left 3 voicemails over 90 minutes. The intern who now had that extension arrived Monday morning to find the messages. Meanwhile, the decision to pay the ransom (which required CISO authorization per policy) was delayed 9 hours while the CEO manually called board members to find the current CISO's number. | The runbook was a static document with no ownership. No one was responsible for verifying escalation contacts. The CISO's departure triggered HR offboarding (badge, email, laptop) but not IR runbook updates. | **Runbook contact verification is a quarterly automated job, not a manual task.** Script: for every phone number in every runbook, dial it and confirm a human answers who identifies themselves as the listed role. If verification fails, page the IR program owner. Rotate a "runbook owner" role weekly — that person is accountable for accuracy. Add a PagerDuty escalation policy that bypasses individual phone numbers entirely: "If SEV1 persists 30 minutes with no IC acknowledgement, auto-escalate to VP Engineering's mobile." |
| SEV1 declared but the comms lead was on a flight — Twitter filled with customer screenshots of the error page while the official status page still showed "All Systems Operational" | An API gateway failure at 2:00 PM EST caused all mobile apps to show "Service Unavailable." The incident commander declared SEV1 within 4 minutes and assembled the technical response team. The communications lead was on a 6-hour flight from SFO to JFK. Nobody else had the status page login credentials — they were in the comms lead's 1Password vault, which required the comms lead's master password for emergency access. For 95 minutes, customers saw "Operational" on the status page while staring at error messages. Twitter decided the narrative. | Single point of failure for customer communications. Status page access was treated as a comms tool, not an incident response tool. No backup comms lead, no shared emergency access procedure. | **The incident commander must be able to update the status page within 60 seconds of SEV1 declaration.** Store status page credentials in a shared emergency vault accessible to all on-call engineers (not just comms). Pre-write status page templates for the top 10 failure modes: "We are investigating reports of [symptom]. Affected: [service]. Next update: [time, 30 min from now]." Practice: in every game day, the first action is updating the status page — before any debugging begins. |
| Game day tested region failover perfectly — but the test used a synthetic workload of 10 RPS while production ran 12,000 RPS; real failover took 47 minutes because the warm-up scripts had never been tested at scale | The team ran quarterly region failover game days for 2 years. Every test passed with DNS cutover in under 90 seconds. When us-east-1 actually failed during a major AWS outage, the team flipped to us-west-2 and waited. The canary service started in 90 seconds. The main application took 47 minutes because connection pools needed to warm up across 800 pods, the CDN cache was cold for the new origin, and the read replica lag was 12 minutes because nobody had tested with production query volume. | The game day was designed to pass, not to find failure modes. The test data set was 100× smaller than production. Every test started from a clean, pre-warmed state. The success metric was "did DNS flip?" rather than "are users receiving 200s?" | **Game days must use production-scale traffic and measure the metric that matters: end-user 200s, not infrastructure health checks.** Run game days during business hours with a fraction of real traffic (canary users). Time every step of recovery from the user's perspective — the clock starts when the first real user sees an error. Every game day must have at least one surprise failure injected that the team wasn't told about. If your game day always passes, you're not trying hard enough to break things. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can fill out a postmortem template but your corrective actions are always "train the engineer" or "add more monitoring" | You've led 20+ SEV1 incidents as IC, and your postmortems have prevented entire classes of failures — not just the specific bug | Someone on a SEV1 call says "I calmed down when I heard your voice on the bridge" — and your organization's MTTR dropped 60% after you redesigned the incident response program |
| You need your runbook to respond to an incident — if the runbook is wrong or missing, you freeze | You can run an incident without a runbook because you understand the system architecture well enough to triage blind, and you're the one who updates the runbook after | You design the incident response program that scales across 50+ teams, and every team's SEV1 recovery time is under 15 minutes without you on the call |
| You've never run a blameless postmortem where the root cause was a process failure you designed | Your postmortems identify specific controls that would have prevented the incident, and you've personally implemented 10+ such controls that have never been triggered | A regulator reviews your incident response program during an enforcement action and cites it as a mitigating factor because your documentation demonstrated operational maturity beyond compliance requirements |

**The Litmus Test:** You're woken up at 3:00 AM by an alert you've never seen before. The runbook doesn't cover it. The on-call for the affected service isn't answering. Can you assess severity, assemble the right people, establish a comms cadence, and start containment within 10 minutes — without panicking? Masters have done this so many times that the first 10 minutes are muscle memory.

## Deliberate Practice

```mermaid
graph LR
    A[Test/Review] --> B[Find gap] --> C[Study<br/>root cause] --> D[Improve<br/>prevention] --> A
```

| Level | Practice | Frequency |
|-------|----------|-----------|
| **Novice** | Review your own work from 3 months ago; catalog everything you'd now flag | Monthly |
| **Competent** | Shadow a more senior reviewer; compare their findings to yours; study the delta | Weekly |
| **Expert** | Design a new quality gate; measure false positive/negative rates; tune for 6 months | Quarterly |
| **Master** | Create a training module that teaches others your quality intuition; measure their improvement | Quarterly |

**The One Highest-Leverage Activity:** Keep a "mistakes journal." Every time you miss something, write down: what you missed, why you missed it, and what rule would have caught it.

## References
<!-- QUICK: 30s -- links to deeper reading -->
- Google SRE Book (Chapters 11–14): https://sre.google/
- PagerDuty Incident Response Documentation: https://response.pagerduty.com/
- Atlassian Incident Management Handbook: https://www.atlassian.com/incident-management
- Howie Guide to Postmortems: https://postmortems.io/
- Chaos Engineering Principles: https://principlesofchaos.org/
