# Scale Depth: Solo → Small → Medium → Enterprise

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
