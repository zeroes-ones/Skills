# Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Observability = PaaS built-in logs + metrics. No custom dashboards. No alerts (check manually). No tracing. No structured logging. Debug via `console.log` + PaaS log viewer.
- **What to skip**: Prometheus. Grafana. OpenTelemetry. Structured logging. SLOs. Alerting. Dashboards. Log aggregation. Distributed tracing.
- **Coordination**: You check logs when something breaks. No coordination needed.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Structured logging (JSON). Log aggregation (Papertrail/Logtail or cloud-native). Uptime monitoring (Pingdom/Checkly). Basic alerting (uptime + error rate via email/Slack). RED metrics hand-rolled or framework built-in. One dashboard with key metrics.
- **What to skip**: Prometheus + Grafana (use managed). Distributed tracing. SLOs. Error budgets. On-call rotation tooling beyond PagerDuty basics.
- **Coordination**: Alerts go to shared Slack channel. Weekly check on error trends. On-call rotation via calendar.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Full observability stack (Prometheus + Grafana + Loki + Tempo). OpenTelemetry for distributed tracing. Structured logging with trace correlation IDs. SLOs defined for critical journeys. Alertmanager with severity routing. Dashboards as code (Grafana in Terraform/Grafonnet). RED + USE metrics. On-call with PagerDuty + runbooks. RUM for frontend (if applicable).
- **What to skip**: AIOps/Anomaly detection. Full data warehouse for observability. Dedicated observability team (embed in platform team).
- **Coordination**: Observability weekly review with platform team. Monthly SLO review. Quarterly alert tuning. Incident post-mortems.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Observability platform team. Centralized observability with multi-tenancy. Error budget policies enforced. Chaos engineering with observability validation. AIOps for anomaly detection. Cost attribution for observability data. Log sampling and retention policies. Compliance audit trails. Observability as a product (self-service dashboards, alert configuration). Synthetic monitoring. Business KPI dashboards.
- **What's full production**: Observability center of excellence. Self-service observability platform. Automated runbook linking. Incident analysis automation. Observability data lifecycle management.
- **Coordination**: Observability platform team weekly. Monthly SLO + error budget review with service owners. Quarterly observability strategy review.

### Transition Triggers
- **Solo → Small**: First time you can't debug a production issue because logs are missing.
- **Small → Medium**: >3 services with inter-service calls. First incident where you couldn't trace root cause without distributed tracing.
- **Medium → Enterprise**: 10+ services with SLO commitments. Multi-team on-call. Compliance requires audit trails.
