# Incident Response Plan

## Severity Levels

| Level | Definition | Response | Notification |
|-------|-----------|----------|--------------|
| P1 — Critical | Platform unavailable, data loss, security breach active | Page on-call engineer immediately. 5-minute acknowledgment SLA. | Internal: #incident-critical Slack channel. Customer: status.orchestra.dev banner + email to affected orgs within 15 minutes. |
| P2 — High | Core feature degraded (catalog unavailable, template execution failing >50%) | Page on-call during business hours (9am–6pm ET Mon–Fri). Off-hours: escalate only if duration exceeds 30 minutes. | Internal: #incident-high Slack channel. Customer: status page update within 30 minutes. |
| P3 — Medium | Non-core feature degraded, single-user impact, workaround exists | Auto-create Linear ticket. Team triages within 4 business hours. | Internal: #eng-alerts Slack channel. Customer: no proactive notification; visible in status page history. |
| P4 — Low | Cosmetic issues, minor bugs with workaround | Added to team backlog. Triaged during weekly grooming. | No proactive notification. |

## Escalation Path

1. **On-Call Engineer** (primary): 5-minute P1 acknowledgment window. If no response, auto-escalate.
2. **Team Lead** (secondary): Paged if primary doesn't acknowledge within 5 minutes.
3. **CTO** (tertiary): Paged for P1 incidents exceeding 30 minutes without resolution, or any confirmed security breach.

On-call rotation: 1-week shifts, 2 engineers per shift (primary + shadow). Shadow handles P3/P4 triage and learns incident process. Rotation managed in PagerDuty with Opsgenie as backup.

## Communication Templates

**Internal — Incident Declared (Slack)**: Includes: incident commander name, severity, affected component, start time, incident channel link, and a brief description (2 sentences max). Pinned to #incident-{severity} channel.

**Customer — Status Page (status.orchestra.dev)**: Template: "We are investigating {issue description}. Affected: {components}. Next update in {time} minutes." Automated from PagerDuty incident creation via webhook.

**Postmortem (Confluence)**: Required for all P1 and P2 incidents. Sections: timeline (UTC), impact assessment (users affected, duration, data loss), root cause (5 Whys), resolution, action items (assigned, due date). Published within 5 business days. Shared with affected enterprise customers on request.

## Tabletop Exercises

**Exercise 1 — Data Breach Scenario (June 15, 2026)**: Simulated unauthorized access to the `template_executions` table via a leaked API key. Team walked through detection (CloudTrail alert → PagerDuty), containment (revoke key, rotate all credentials, enable WAF blocking mode), eradication (audit audit logs for 90 days of access), and recovery (notify affected customers, publish postmortem). **4 findings**: CloudTrail alert had 12-minute delay (reduced to 2 minutes), key rotation playbook was outdated (updated), no pre-written customer notification template for data breach (created), and on-call didn't have direct DB access for forensic queries (added read-only console access with break-glass procedure).

**Exercise 2 — Multi-Region API Outage (July 2, 2026)**: Simulated us-east-1 regional failure. Team walked through detection (Route53 health check failure), mitigation (DNS failover to eu-west-1), and recovery (promote read replica, verify data consistency). **2 findings**: DNS TTL of 300 seconds caused 5-minute propagation delay (reduced to 60 seconds for health check records), and the failover runbook referenced a deprecated Aurora CLI command (updated to current AWS CLI syntax).
