# Support Operations Guide

> **Author:** Sandeep Kumar Penchala

A comprehensive guide to building and scaling customer support engineering operations. Companion to the [Customer Support Engineer SKILL.md](../SKILL.md).

---

## 1. Support Tiers

### Tier Structure

| Tier | Role | Handles | Escalation Criteria |
|---|---|---|---|
| **L1: Triage** | Support Associate | Password resets, billing inquiries, FAQs, account setup | Issue requires technical investigation; > 10 min resolution |
| **L2: Technical** | Support Engineer | Configuration, API usage, debugging integration issues, performance | Bug confirmed; requires code change; > 2 hour resolution |
| **L3: Engineering** | Software Engineer | Bug fixes, hotfixes, feature requests requiring code | Root cause identified by L2; fix planned in sprint |
| **L4: Escalation** | Engineering Manager | Critical outages, major incidents, executive escalations | Business-critical; SLA breach imminent |

### Escalation Flow
```
Customer → L1 (Triage)
              ├─ Resolved (80% of tickets)
              └─ Escalate → L2 (Technical)
                                ├─ Resolved (15% of tickets)
                                └─ Escalate → L3 (Engineering)
                                                  ├─ Resolved (4% of tickets)
                                                  └─ Escalate → L4 (Critical / 1%)
```

### Ticket Deflection (L0 / Self-Service)
- Knowledge base articles surfaced in search
- Chatbot for common questions (integration with docs)
- Community forum for peer support
- In-app help tooltips and guided tours
- **Target:** 40%+ of inquiries resolved without human interaction

---

## 2. SLA Framework

### Standard SLA by Severity

| Severity | Definition | First Response | Resolution Target | Coverage |
|---|---|---|---|---|
| **Critical (Sev1)** | Service down; data loss; security breach | < 15 min | < 4 hours | 24/7/365 |
| **High (Sev2)** | Major feature broken; no workaround; revenue impact | < 1 hour | < 8 business hours | 24/7 or business hours |
| **Medium (Sev3)** | Partial feature impact; workaround exists | < 4 business hours | < 3 business days | Business hours |
| **Low (Sev4)** | Cosmetic; feature request; documentation gap | < 1 business day | < 10 business days | Business hours |

### Severity Classification Guide
```yaml
critical_indicators:
  - Production system completely unavailable
  - Data corruption or loss (any amount)
  - Security vulnerability actively exploited
  - Payment processing failure (all transactions)

high_indicators:
  - Core feature unavailable for all users
  - No viable workaround exists
  - SLA breach risk for customer's own SLAs
  - Performance degradation > 50% baseline

medium_indicators:
  - Feature unavailable for subset of users
  - Viable workaround documented and shared
  - Non-blocking integration issue

low_indicators:
  - UI cosmetic issue
  - Documentation error or gap
  - Feature request or enhancement
  - "Nice to have" configuration question
```

### Business Hours vs 24/7
- **Business Hours:** 9am–6pm, Mon–Fri (in customer's timezone or follow-the-sun)
- **24/7:** On-call rotation; PagerDuty/Opsgenie; escalation policy with 5-min ack SLA
- **Hybrid:** Business hours for L1/L2; 24/7 on-call for Critical severity only (bypasses L1)

---

## 3. Ticket Management

### Platform Comparison

| Platform | Best For | Key Feature | Pricing |
|---|---|---|---|
| **Zendesk** | Enterprise; multi-channel (email, chat, phone) | Robust triggers, macros, SLA automation | $19–$150/agent/mo |
| **Intercom** | SaaS; in-app messaging; proactive outreach | Product tours, bots, rich customer profiles | $29–$139/seat/mo |
| **Linear** | Engineering-first; tight GitHub integration | Speed, keyboard shortcuts, issue tracking | Free–$14/user/mo |
| **GitHub Issues** | Open source; developer community | Native code linking, public visibility | Free |
| **Help Scout** | Small teams; simple, email-first | No portal branding; Beacon widget | $20–$65/user/mo |

### Ticket Template (Required Fields)
```yaml
ticket_template:
  title: "[Concise summary of the issue]"
  severity: Critical | High | Medium | Low
  environment:
    product_version: string
    deployment: SaaS | Self-hosted | Preview
    browser_os: string  # if UI issue
  description: |
    ## Steps to Reproduce
    1. [Step 1]
    2. [Step 2]
    3. [Observed behavior]

    ## Expected Behavior
    [What should have happened]

    ## Actual Behavior
    [What actually happened; include error messages, screenshots]

    ## Impact
    [How many users affected? Workaround exists? Revenue impact?]

  attachments: [logs, screenshots, HAR files, screen recordings]
  customer_id: string
  plan_tier: Free | Pro | Enterprise
```

### Ticket States & Workflow
```
New → Triaged → In Progress → Pending Customer → Resolved → Closed
                  ↓                    ↑
                Blocked ───────────────┘
                  ↓
              Escalated → [L2/L3/L4 workflow]
```

- **Pending Customer:** Waiting on customer response; auto-close after 7 days of inactivity
- **Resolved:** Solution provided; auto-close after 72 hours if no follow-up
- **Closed:** Final state; no further updates (can be reopened by customer)

---

## 4. Knowledge Base Structure

### Content Hierarchy
```
Knowledge Base
├── Getting Started
│   ├── Quickstart Guide
│   ├── Account Setup
│   └── Core Concepts
├── Troubleshooting
│   ├── Common Error Messages (and how to fix them)
│   ├── Connectivity Issues
│   └── Performance Troubleshooting
├── How-To Guides
│   ├── Integrations (by tool: Slack, Jira, GitHub)
│   ├── Advanced Configurations
│   └── Migration Guides
├── Reference
│   ├── API Reference
│   ├── Configuration Reference
│   └── Glossary
├── FAQ
│   ├── Billing & Plans
│   ├── Security & Compliance
│   └── Technical FAQs
└── Community Forum (link out)
```

### Article Template
```markdown
# [Symptom or Question] — [Brief Resolution]

## Problem
[What the customer sees; exact error message; when it happens]

## Cause
[Root cause — technical or configuration]

## Solution
[Step-by-step resolution]

### Step 1: [Action]
```bash
command to run
```
[What this does and what to verify]

### Step 2: [Action]

## Verification
[How to confirm the fix worked]

## If This Doesn't Work
- [Alternative solution 1]
- [Contact support with: logs, version, environment]

## Applies To
- Version: X.Y.Z+
- Plan: All / Pro / Enterprise

## Related Articles
- [Related issue 1]
- [Related issue 2]
```

---

## 5. Debugging Workflow

### Standard Debug Process
```
1. REPRODUCE  → Can we reliably trigger the issue?
                  ├─ Yes → Continue
                  └─ No → Request exact steps + environment from customer

2. ISOLATE    → What changed? (Recent deploy, config change, new data)
                  ├─ Narrow by: time window, affected users, region, feature flag
                  └─ Use: split testing (50% traffic), canary analysis

3. DIAGNOSE   → What's the root cause?
                  Tools: logs (Kibana/Datadog), traces (Jaeger/Honeycomb), metrics (Grafana)
                  Method: hypothesis → test → confirm or reject

4. RESOLVE    → Apply fix; verify in staging; deploy; confirm with customer

5. DOCUMENT   → Write KB article; add to runbook; share with team

6. PREVENT    → Add monitoring alert; add test case; fix root cause in code
```

### Debugging Toolkit
```yaml
tools:
  logging: Kibana, Datadog Logs, Papertrail
  tracing: Jaeger, Honeycomb, Lightstep
  metrics: Grafana, Datadog, New Relic
  error_tracking: Sentry, Rollbar
  session_replay: LogRocket, FullStory (for UI issues)
  api_debug: Postman, Insomnia, curl
  database: Direct read-replica access; EXPLAIN ANALYZE
  feature_flags: LaunchDarkly, Flagsmith (check if flag controls affected code)
```

---

## 6. Customer Communication

### Status Page
- **Tool:** Atlassian Statuspage, Better Uptime, or self-hosted
- **Must include:** Current status per component (Operational / Degraded / Down)
- **Incident history:** Last 30 days publicly visible
- **Subscribe:** Email/SMS/webhook notifications for updates

### Incident Communication Template
```markdown
## [Incident Title] — Investigating
**Posted:** [Timestamp] | **Status:** Investigating
We are investigating reports of [symptom]. Affected customers may experience [impact].
Next update in: 30 minutes.

---

## [Incident Title] — Identified
**Posted:** [Timestamp] | **Status:** Identified
The issue has been traced to [root cause]. We are [action being taken].
ETA for resolution: [timestamp].

---

## [Incident Title] — Monitoring
**Posted:** [Timestamp] | **Status:** Monitoring
A fix has been deployed. We are monitoring to confirm resolution.
Affected period: [start] to [end] UTC.

---

## [Incident Title] — Resolved
**Posted:** [Timestamp] | **Status:** Resolved
The issue is resolved. [Brief description of fix].
A full postmortem will be published within 5 business days.
```

### RCA (Root Cause Analysis) Publication
```markdown
# Postmortem: [Incident Title]
**Date:** [Date] | **Duration:** [X hours Y minutes] | **Severity:** Critical/High

## Summary
[2–3 sentence summary: what happened, impact, root cause]

## Timeline (UTC)
| Time | Event |
|---|---|
| 14:32 | Monitoring alert fired: P99 latency > 5s |
| 14:34 | On-call engineer acknowledged |
| 14:45 | Identified: connection pool exhaustion from new deploy |
| 14:52 | Rollback initiated |
| 15:02 | Service restored |

## Root Cause
[Detailed technical explanation]

## Impact
- [X] customers affected
- [Y] minutes of [degraded service / full outage]
- [Z] failed transactions

## Action Items
| Action | Owner | Deadline | Status |
|---|---|---|---|
| [Action 1] | [Name] | [Date] | [Status] |
```

---

## 7. Support Metrics

### Key Metrics Dashboard

| Metric | Target | Formula | Tool |
|---|---|---|---|
| **CSAT** (Customer Satisfaction) | > 90% | % of "good"/"great" ratings on post-resolution survey | Zendesk Explore |
| **CES** (Customer Effort Score) | < 3 (1–7 scale) | "How easy was it to resolve your issue?" (1 = very easy) | Post-ticket survey |
| **FRT** (First Response Time) | < target by severity | Time from ticket creation to first human response | Ticketing platform |
| **ART** (Average Resolution Time) | < target by severity | Time from creation to "Resolved" status | Ticketing platform |
| **Ticket Volume** | Monitor trend | Total tickets per week / month | Ticketing platform |
| **Escalation Rate** | < 5% | % of tickets escalated from L1 → L2+ | Ticketing platform |
| **KB Deflection Rate** | > 40% | % of searches that end without creating a ticket | Analytics + KB search |
| **One-Touch Resolution** | > 60% | % of tickets resolved with a single reply | Ticketing platform |

### Weekly Support Report Template
```markdown
# Support Report — Week of [Date]

## Volume
- New tickets: [N] (↑/↓ X% WoW)
- Resolved: [N]
- Backlog: [N]

## SLA
- Critical: [N] tickets, [X]% within SLA
- High: [N] tickets, [X]% within SLA
- Overall SLA adherence: [X]%

## Customer Satisfaction
- CSAT: [X]% (target > 90%)
- CES: [X.X] (target < 3.0)

## Top Issues This Week
1. [Issue 1] — [N] tickets — KB article: [draft/published]
2. [Issue 2] — [N] tickets — Bug filed: [link]

## Team
- Agents available: [N]
- Avg tickets/agent/day: [N]
```

---

## 8. Support Engineering Career Ladder

| Level | Title | Experience | Key Skills | Scope |
|---|---|---|---|---|
| **L1** | Associate Support Engineer | 0–2 years | Product knowledge, communication, triage | Ticket resolution (L1); knowledge base contributions |
| **L2** | Support Engineer | 2–5 years | Debugging, APIs, SQL, scripting | Complex issues (L2); tooling improvements; mentoring L1 |
| **L3** | Senior Support Engineer | 5–8 years | Systems thinking, code contributions, incident command | Cross-team collaboration; runbook ownership; L3 escalation |
| **L4** | Staff Support Engineer | 8+ years | Architecture, product strategy, process design | Product improvement initiatives; tooling strategy; team leadership |
| **L5** | Principal Support Engineer | 10+ years | Industry expertise, organizational influence | Multi-product strategy; industry advocacy; executive escalation |

### Skills by Level

```yaml
L1_Associate:
  technical:
    - Read and understand API documentation
    - Reproduce reported bugs using provided steps
    - Basic log analysis (search for error messages)
  soft:
    - Empathetic customer communication
    - Accurate ticket documentation
    - Knowing when to escalate

L2_Engineer:
  technical:
    - Write and execute SQL queries for investigation
    - Use debugging tools (browser dev tools, curl, Postman)
    - Read application code to trace issues
    - Write simple scripts to reproduce/validate issues
  soft:
    - De-escalate frustrated customers
    - Mentor L1 team members
    - Write clear KB articles and runbooks

L3_Senior:
  technical:
    - Contribute code fixes (bug fixes, small features)
    - Design monitoring and alerting for support use cases
    - Lead incident response as Incident Commander
    - Perform root cause analysis for complex issues
  soft:
    - Influence product roadmap with support data
    - Train engineering teams on supportability
    - Present at team all-hands and customer briefings

L4_Staff:
  technical:
    - Drive architectural changes to reduce support burden
    - Design support tooling and automation strategy
    - Cross-product debugging and integration expertise
  soft:
    - Define support engineering strategy
    - Partner with product and engineering leadership
    - External thought leadership (conferences, blogs)
```

---

## 9. Runbook Template

```markdown
# Runbook: [Scenario Name]
**Owner:** [Team/Name] | **Last Updated:** [Date] | **Severity:** Critical/High/Medium

## Symptom
- Alert name: [e.g., "API P99 Latency > 2s"]
- Dashboard link: [URL]
- What customers report: "[User-facing symptom]"

## Prerequisites
- Access to: [systems, dashboards, tools]
- Permissions: [required roles or access levels]

## Diagnosis Steps
### Step 1: Verify scope
```sql
-- Check affected customers/regions
SELECT region, COUNT(*) FROM errors
WHERE timestamp > NOW() - INTERVAL '15 minutes'
GROUP BY region;
```

### Step 2: Check recent changes
```bash
# List recent deployments
kubectl rollout history deployment/api-server
```

### Step 3: Check system health
- [Dashboard link 1]: Check [metric]; expected range: [X–Y]
- [Dashboard link 2]: Check [metric]; threshold: [value]

## Resolution Steps
### If root cause is [Scenario A]:
1. [Action 1]: `command to execute`
2. [Action 2]: [Manual step]
3. Verify: [How to confirm resolution]

### If root cause is [Scenario B]:
1. [Action 1]
2. [Action 2]

## Rollback
If resolution fails or causes further issues:
1. `revert_command_here`
2. Notify: #incident-response Slack channel

## Escalation Path
| After | Escalate To | Contact |
|---|---|---|
| 15 min without diagnosis | L2 On-Call | @l2-oncall in Slack; PagerDuty |
| 30 min without resolution | Engineering Manager | @em-oncall; Phone: [number] |
| 60 min (Critical only) | VP Engineering | Phone: [number] |

## Post-Incident
- [ ] Create incident ticket with timeline
- [ ] Schedule postmortem (within 5 business days for Critical)
- [ ] Update this runbook with lessons learned
- [ ] Add new monitoring alert if gap identified

## Related Runbooks
- [Related scenario 1](link)
- [Related scenario 2](link)
```

---

*Support engineering is not just ticket resolution — it's the bridge between customers and product. Invest in processes, metrics, and career growth to build a high-performing support organization.*
