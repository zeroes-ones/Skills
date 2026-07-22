---
name: incident-classification-matrix
description: SEV1-SEV5 classification with concrete criteria per industry (SaaS, FinTech, HealthTech), war room protocol, and communication templates per audience.
author: Sandeep Kumar Penchala
---

# Incident Classification Matrix

Concrete, objective criteria for classifying incident severity across industries. Includes war
room protocols, communication templates per audience, and escalation procedures that work
in real incidents — not just in policy documents.

## 1. Severity Classification — Universal Framework

### 1.1 The Five Levels

| Level  | Name            | Definition                                                      | Page?  | Response SLA              |
|--------|-----------------|-----------------------------------------------------------------|--------|---------------------------|
| SEV1   | Critical        | Complete service outage, data loss/corruption, security breach  | YES    | Acknowledge <5 min, Engage <15 min |
| SEV2   | Major           | Core feature broken for majority of users, significant degradation | YES | Acknowledge <15 min, Engage <30 min |
| SEV3   | Minor           | Feature partially impaired, workaround exists, limited users    | NO     | Acknowledge <1 hr, Engage <4 hrs    |
| SEV4   | Low             | Cosmetic issue, non-blocking, no user impact                    | NO     | Acknowledge <4 hrs, Engage <24 hrs  |
| SEV5   | Informational   | Future risk, proactive maintenance, capacity concern            | NO     | Ticket in next sprint               |

### 1.2 The Three Questions for Classification

For any incident, ask these three questions in order. Stop when the answer is clear:

```
Q1: Is user data at risk of loss, corruption, or unauthorized access?
    YES → SEV1 (security breach or data integrity incident)

Q2: Are users completely unable to use a core product function?
    YES → Is it >50% of users? → SEV1
           Is it <50% of users? → SEV2

Q3: Is there a workaround that users can reasonably follow?
    NO → SEV2
    YES → Is the workaround documented and accessible?
        YES → SEV3
        NO → SEV2 (treat as SEV2 until workaround is published)
```

## 2. Industry-Specific Classification

### 2.1 SaaS / B2B Software

| Scenario                                      | Severity | Rationale                                        |
|-----------------------------------------------|----------|--------------------------------------------------|
| Login completely broken for all users         | SEV1     | Users cannot access product at all               |
| Payment processing failing, users can't upgrade| SEV1    | Revenue-impacting + user-blocking                 |
| Core feature (e.g., search) returning errors   | SEV2     | Core workflow broken                             |
| Dashboard loading >30 seconds for all users    | SEV2     | Significant degradation of primary interface     |
| Export feature broken for enterprise tier      | SEV2     | Contractual SLA may be violated                  |
| Minor UI bug on settings page                  | SEV4     | Non-blocking, visible but functional workaround   |
| Typo on marketing landing page                 | SEV4     | No product impact                                |
| SSL certificate expiring in 7 days             | SEV3     | Proactive — will become SEV1 if unresolved       |
| Third-party integration intermittently failing | SEV2     | Depends on % of users affected and criticality    |

**SaaS-specific guardrails:**
- If any enterprise customer with >$100K ACV reports an issue → minimum SEV2
- If status page is down during an incident → escalate to SEV1 (customers can't check status)
- Data export/portability broken → SEV2 minimum (regulatory risk under GDPR)

### 2.2 FinTech / Payments

| Scenario                                      | Severity | Rationale                                        |
|-----------------------------------------------|----------|--------------------------------------------------|
| Payment processing down completely            | SEV1     | Revenue halt + regulatory risk                  |
| Incorrect amounts being charged               | SEV1     | Financial loss + legal liability + reputational  |
| Settlement/reconciliation delayed >4 hours    | SEV1     | Regulatory reporting violation possible          |
| Unauthorized transaction detected              | SEV1     | Security breach — immediate containment          |
| KYC/AML check service unavailable             | SEV2     | Blocks new user onboarding but existing OK       |
| Real-time fraud detection degraded            | SEV1     | Financial risk escalates with every transaction  |
| Statement generation delayed                  | SEV2     | Customer-facing, but not blocking transactions   |
| Exchange rate feed stale >15 minutes          | SEV1     | Incorrect conversions → financial liability      |
| API latency >2 seconds for payment endpoint   | SEV2     | User experience degraded, may cause timeouts     |

**FinTech-specific guardrails:**
- Any incident involving incorrect money movement → SEV1, immediate containment
- Regulatory reporting deadlines missed → SEV1 + compliance officer must be notified
- PCI DSS control failure → SEV1, engage security team immediately
- Trading/pricing system anomaly → SEV1, halt trading if automated

### 2.3 HealthTech / Healthcare

| Scenario                                      | Severity | Rationale                                        |
|-----------------------------------------------|----------|--------------------------------------------------|
| Patient data exposed or accessed unauthorized  | SEV1     | HIPAA breach — 60-day notification clock starts  |
| Clinical decision support returning wrong recs | SEV1     | Patient safety risk                              |
| EHR (Electronic Health Record) unavailable     | SEV1     | Clinical workflows blocked; patient care impact  |
| Telehealth video/audio down                    | SEV1     | Patient appointments cannot proceed              |
| Lab results delayed >2 hours                   | SEV2     | Clinical decision delays                         |
| Prescription renewal portal down               | SEV2     | Patient access to medication blocked             |
| Appointment scheduling unavailable             | SEV3     | Inconvenience, phone scheduling still works      |
| Analytics dashboard stale (not real-time)      | SEV4     | No patient impact                                |
| Medical device data streaming interrupted      | SEV1     | Loss of patient monitoring data                  |

**HealthTech-specific guardrails:**
- Any incident with potential patient safety impact → SEV1 immediately
- PHI exposure → SEV1, begin HIPAA breach notification assessment within 1 hour
- FDA-reportable device malfunction → SEV1 + regulatory team engaged
- "When in doubt, page it out" — err on the side of over-response for clinical systems

## 3. War Room Protocol

### 3.1 Activation

**Who declares:** The first responder who identifies the incident, OR the on-call engineer receiving the alert.

**How to declare:**
1. Post in `#incidents` Slack channel with `/incident` command (or manual message)
2. The command/action automatically:
   - Creates a dedicated channel `#inc-{date}-{brief-description}`
   - Creates a PagerDuty incident
   - Posts to status page (if SEV1/SEV2 — pre-filled template)
   - Starts a Zoom/Meet war room bridge

**Template for declaration message:**
```
🚨 INCIDENT DECLARED 🚨

Severity: SEV[1/2]
Title: [One-line description of what's broken]
Impact: [What users see / what's affected]
Detection: [How we found out — alert, customer report, internal]
Incident Commander: @name
Operations Lead: @name
Communications Lead: @name

War room: [Zoom/Meet link]
Channel: #inc-YYYY-MM-DD-shortname
Status page: [link]
```

### 3.2 Roles and Responsibilities

| Role        | Responsibilities                                                                 | Who                            |
|-------------|-----------------------------------------------------------------------------------|--------------------------------|
| **Incident Commander (IC)** | Owns the incident. Makes all decisions. Delegates tasks. Communicates to leadership. Does NOT fix the problem. | Senior engineer, EM, or director on rotation |
| **Operations Lead (OL)** | Leads technical investigation and mitigation. Coordinates engineers debugging. Reports findings to IC. | On-call engineer or SME for affected system |
| **Communications Lead (CL)** | Drafts and sends all stakeholder communications. Manages status page. Shields IC and OL from inbound questions. | Engineering manager, TPM, or product manager |
| **Scribe** | Documents everything: timeline, actions taken, decisions, hypotheses tested. Posts updates in channel. | Any available engineer; rotating role |

**IC Commandments:**
1. **Mitigate first, investigate later.** The goal is to restore service. Root cause comes in the postmortem.
2. **Delegate everything.** IC does not touch a keyboard. If the IC is also debugging, there is no commander.
3. **State your mental model.** "I believe the database is overloaded because of a query change at 14:30. OL, can you check the query performance dashboard?"
4. **Set time expectations.** "We'll reconvene in 15 minutes. OL, by then I want the query plan analysis."
5. **Escalate early.** If the incident isn't contained in 30 minutes, notify your manager. If not contained in 1 hour, notify the VP/director. Don't wait.

### 3.3 Incident Timeline — What Happens When

```
T+0:00   Alert fires / issue detected
T+0:05   On-call acknowledges, begins triage
T+0:10   Severity determined. If SEV1/SEV2 → declare incident, open war room
T+0:15   IC assigned. Roles assigned. Status page updated (SEV1).
T+0:30   First stakeholder update sent by CL
T+1:00   If unresolved → escalate to engineering manager
T+2:00   If unresolved → escalate to VP/Director
T+4:00   If unresolved → escalate to CTO. Consider external support.
Every 30 min: CL sends status updates
At resolution: IC declares incident resolved. CL sends final update.
T+48 hrs: Postmortem scheduled
```

### 3.4 War Room Cadence

| Time Since Declaration | Action                                             |
|------------------------|----------------------------------------------------|
| 0 min                  | Open war room. IC briefs on what's known.          |
| 15 min                 | OL reports findings. IC updates mental model.      |
| 30 min                 | Decision point: rollback? scale up? failover?       |
| 45 min                 | IC decides: escalate? bring in more SMEs?          |
| Every 30 min thereafter| Full sync. IC: "This is what we know, this is what we're doing, this is what we need." |
| Resolution             | IC: "Service is restored. We're monitoring for 30 min before closing." |
| +30 min post-resolution| IC: "Monitoring confirms recovery. Incident resolved at [time]. Postmortem in 48 hrs." |

## 4. Communication Templates

### 4.1 Customer-Facing (Status Page / Email)

**Initial notification (SEV1, first 15 minutes):**
```
Subject: [SEV1] [Service] experiencing issues

We are currently investigating reports of [brief symptom: e.g., "elevated error rates on login"].
Users may experience [what users see].

Our engineering team is actively investigating and we will provide an update within 30 minutes.

We apologize for the disruption.
```

**Update (every 30 minutes):**
```
Subject: UPDATE: [SEV1] [Service] — [Time since start]

[What we know now]
We have identified [cause, if known] and are [mitigation action in progress].
Users are currently [what users experience now — same, better, worse].

Estimated resolution: [if known, with caveat; if not, say "We do not have an ETA yet"]
Next update: [time, typically 30 min from now]
```

**Resolution:**
```
Subject: RESOLVED: [SEV1] [Service] — Service restored

[Service] is now operating normally. The issue was resolved at [time].

Total impact duration: [X hours, Y minutes]
What happened: [1–2 sentence summary]
What we're doing: [1 sentence on follow-up — e.g., "We are conducting a full postmortem and will share findings within 5 business days."]

We sincerely apologize for the disruption. If you continue to experience issues, please contact support at [email/link].
```

### 4.2 Internal Stakeholder (Slack / Email)

**Initial (first 5 minutes after declaration):**
```
@channel 🚨 SEV1 INCIDENT: [Brief Title]

What: [One line on what's broken]
Impact: [User impact scope]
War room: [link]
Incident Commander: @ic_name
Status page: [link]
Next update: 30 minutes

Please do NOT DM the IC or OL for updates — follow #inc-YYYY-MM-DD-shortname.
```

**Status update (every 30 minutes):**
```
@here INCIDENT UPDATE — [Title] — T+[time]

Status: [Investigating / Mitigating / Monitoring / Resolved]
Current situation: [2–3 sentences]
Actions taken: [What we did in last 30 min]
Next steps: [What we're doing next]
Users affected: [% or count]
Revenue impact (if known): [estimated]
Next update: [time]
```

### 4.3 Executive Update (for SEV1 lasting >1 hour)

```
To: CTO, VP Eng, CPO
Subject: Executive Update — SEV1 [Title] — T+[time]

Situation: [1 paragraph — what, impact, current state]
Actions: [Bullet list of actions taken and planned]
Timeline: [Key events since detection]
Customer communication: [Status page updated Y/N, last update time]
Escalation: [Who's engaged, what help needed]
ETA: [If known, with confidence level: high/medium/low]
```

### 4.4 Postmortem Announcement

```
Subject: Postmortem: [Incident Title] — [Date]

A postmortem for the [severity] incident on [date] affecting [service] has been published.

Summary:
- Duration: [X hours, Y minutes]
- Impact: [What users experienced]
- Root cause: [1–2 sentence summary]

Read the full postmortem: [link]

Action items have been filed and will be tracked in [tracking system]. Questions? Join the postmortem readout on [date/time].
```

## 5. Escalation Policy

### 5.1 Escalation Path

```
Level 1: Primary On-Call Engineer
  │ ─ if no ack in 5 min ──▶
  ▼
Level 2: Secondary On-Call Engineer (different timezone ideally)
  │ ─ if no ack in 10 min ──▶
  ▼
Level 3: Engineering Manager on duty
  │ ─ if no ack in 15 min ──▶
  ▼
Level 4: Director of Engineering
  │ ─ if no ack in 20 min ──▶
  ▼
Level 5: VP Engineering / CTO
```

### 5.2 When to Escalate During an Active Incident

| Trigger                                           | Escalate To               |
|---------------------------------------------------|----------------------------|
| Incident not acknowledged within 5 minutes        | Next tier in on-call path  |
| Incident not contained within 30 minutes          | Engineering Manager        |
| Incident not contained within 1 hour              | Director of Engineering    |
| Incident not contained within 2 hours             | VP Engineering             |
| Incident not contained within 4 hours             | CTO                        |
| Data breach or security incident                   | CISO + CTO immediately     |
| Customer data exposed                              | CISO + Legal + CTO immediately |
| >10% of revenue at risk                           | VP + CTO immediately       |
| Media / social media attention                     | PR/Comms + CTO immediately |
| Regulator contact / inquiry                        | Legal + CTO immediately    |

## 6. After-Action: Handoff and Stand-Down

### 6.1 Handoff Template

If an incident spans shifts, the outgoing IC briefs the incoming IC:

```markdown
# Incident Handoff: [Title]
- Incident channel: #inc-YYYY-MM-DD-shortname
- Severity: SEV[X]
- Declared: [time] by [name]
- Current status: [Investigating/Mitigating/Monitoring]

## What We Know
[Current understanding of the problem]

## What We've Done
[Bulleth list of actions taken, with times]

## What We're Doing Now
[Current active investigation/mitigation threads]

## What We Haven't Tried Yet
[Ideas that are worth pursuing but haven't been explored]

## Key Contacts
- Previous IC: [name, phone]
- Previous OL: [name, phone]
- Escalation so far: [who has been notified]
```

### 6.2 Resolution Criteria

An incident is RESOLVED when ALL of these are true:
- [ ] Service is restored to pre-incident functionality
- [ ] Monitoring confirms normal operation for 30 minutes
- [ ] No active customer reports of the issue
- [ ] Status page updated to "Resolved"
- [ ] Postmortem scheduled (within 48 hours for SEV1, within 1 week for SEV2)
- [ ] Runbook updated with findings from this incident
- [ ] War room stand-down announced in incident channel

## References

- PagerDuty Incident Response: https://response.pagerduty.com/
- Atlassian Incident Management: https://www.atlassian.com/incident-management
- Google SRE — Managing Incidents: https://sre.google/sre-book/managing-incidents/
- Incident Command System (NIMS): https://www.fema.gov/emergency-managers/nims
