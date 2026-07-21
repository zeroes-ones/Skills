# SRE Practices — Orchestra Platform

## Error Budget Policy

Orchestra's primary SLO is **99.9% monthly availability**, yielding an error budget of **43.8 minutes per month**. Error budget burn is tracked in real-time via a Grafana dashboard that fires alerts at specific thresholds:

| Burn Rate | Budget Consumed | Action |
|---|---|---|
| 25% (11 min) | Advisory notice to on-call | Review recent changes, prepare rollback |
| 50% (21.9 min) | **Freeze all deployments** | No production changes until budget recovers; exception process requires CTO approval |
| 80% (35 min) | **Mandatory postmortem** | Blameless postmortem within 48 hours; action items tracked in Jira |

If the error budget is fully consumed before month-end, all non-emergency changes are blocked until the budget resets on the first of the next month.

## Toil Automation

Four manual processes have been eliminated through automation:

| Process | Before | After | Annual Time Saved |
|---|---|---|---|
| Environment provisioning | 45 min (manual Terraform + ArgoCD setup) | 5 min (self-service CLI tool) | ~120 hours |
| SSL certificate renewal | Manual cert request + deployment | Auto-renew via cert-manager + Let's Encrypt | ~12 hours |
| Database backup verification | Manual restore test (monthly) | Automated restore test with alert on failure | ~24 hours |
| User offboarding | 6 manual steps across AWS, GitHub, and IdP | 1 Jira ticket → automated deprovisioning workflow | ~36 hours |

Cumulative toil reduction: **~192 engineering-hours per year** redirected to feature work and reliability improvements.

## On-Call Rotation

Follow-the-sun rotation across three geographic zones:

```
US East (9AM–5PM ET)  →  US West (9AM–5PM PT)  →  EU (9AM–5PM CET)
```

- **3 engineers** in rotation, week-long shifts
- PagerDuty handles escalation: **engineer → team lead (15 min) → CTO (30 min)**
- No engineer is on-call for more than one week per month
- Post-on-call compensation: the following Friday off (no meetings, no sprint work)

## Capacity Planning

A rolling **6-month capacity forecast** is updated weekly, driven by:

- Customer growth rate (current: 15% month-over-month)
- Per-tenant resource consumption trends (CPU, memory, storage)
- Seasonality adjustments based on usage patterns

Auto-scaling policies are tuned to respond before saturation:
- **Horizontal Pod Autoscaler**: scale out at CPU > 70% for 5 minutes
- **Cluster Autoscaler**: provision new nodes when pods are pending for > 2 minutes
- **RDS storage auto-scaling**: enabled with 20% headroom threshold

Weekly capacity review is a standing 30-minute meeting with engineering leads.

## Runbooks

Twelve runbooks cover common incident scenarios. Each runbook follows a standardized template: symptom description, diagnostic commands, remediation steps, escalation criteria, and post-resolution verification. Key runbooks:

- Database failover (RDS Aurora)
- Redis memory pressure (> 80% used)
- API latency spike (p95 > 1 second)
- Template execution timeout (> 30 seconds)
- Ingress controller failure
- Certificate expiration alert
- PagerDuty notification failure fallback

All runbooks are stored in the `orchestra-runbooks` repository and linked from every Alertmanager alert.

## Postmortem Culture

Orchestra follows a **blameless postmortem** process. To date:

- **5 postmortems** completed (incidents that consumed > 10% of error budget)
- **23 action items** generated — 18 completed, 5 in progress
- **Average time to action item resolution**: 12 days

Each postmortem includes a timeline, contributing factors, what went well, what went wrong, and graded action items by priority. Postmortems are shared company-wide (not just engineering) to build organizational resilience awareness.
