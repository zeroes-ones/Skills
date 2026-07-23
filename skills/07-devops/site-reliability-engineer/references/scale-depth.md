# Scale Depth

<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
- **What changes**: No formal SRE. You are the SRE. Monitor with UptimeRobot or healthchecks.io. Get paged via PagerDuty free tier. Manual incident response. No SLOs — just "is it up?"
- **Overkill**: SLO/SLI framework, error budgets, formal incident roles, capacity planning, chaos engineering, postmortem docs.
- **Coordination**: You handle everything. No coordination needed.
- **Cost**: $0-30/month (monitoring + paging).
- **Transition trigger**: First user-impacting incident you didn't notice for > 1 hour. Paying users depend on availability.

### Small (2-10 people, 100-10K users)
- **What changes**: Define 2-3 SLIs per service. Set basic SLOs (99.9% availability). Simple alerting (CPU > 80%, 5xx > 1%). On-call rotation (weekly). Blameless postmortems for SEV1 only. Toil tracking via rough estimates. No capacity planning — react to growth.
- **Overkill**: Multi-window burn rate alerting, formal error budget policy, chaos engineering, dedicated SRE role, capacity forecasting models.
- **Coordination**: On-call handoff between engineers. Weekly reliability standup (10 min). Postmortem shared in team channel.
- **Cost**: $100-500/month (monitoring, paging, on-call stipends). SRE is shared responsibility, no dedicated headcount.
- **Transition trigger**: > 2 SEV1 incidents/month; MTTR > 2 hours; on-call burnout becoming visible.

### Medium (10-50 people, 10K-1M users)
- **What changes**: Dedicated SRE team (2-4). Full SLO framework with multi-window burn rate alerts. Error budget policy integrated with deploys. Toil measurement and automation program. Capacity planning with quarterly forecasts. Incident commander training. Chaos engineering gamedays (quarterly). Production readiness reviews.
- **Overkill**: Multi-region active-active SLOs, dedicated SRE for every product team, enterprise incident management platform, formal reliability engineering budget.
- **Coordination**: SRE embedded in product teams (1 SRE per 2-3 teams). Monthly SLO review with product owners. Quarterly capacity review. Postmortems shared org-wide.
- **Cost**: $600K-1.2M/year (2-4 SREs). Monitoring/paging $2-5K/month. Gameday tooling $500-2K/month.
- **Transition trigger**: > 50 engineers, multiple customer-facing services, contractual SLAs with customers, compliance audit requirements.

### Enterprise (50+ people, 1M+ users)
- **What changes**: SRE organization with multiple models (embedded + consulting + platform). Formal error budget governance committee. Full chaos engineering program with automated experiments. Capacity planning with ML-based forecasting. Dedicated incident management function. Reliability engineering roadmap as product. Reliability North Star metrics at company level. Progressive delivery with automated canary analysis.
- **What's full production**: Automated error budget enforcement in CD pipelines. Continuous verification in production. Dedicated SRE training program. Published reliability reports for customers. Reliability SLOs in sales contracts.
- **Coordination**: SRE leadership team weekly. Monthly reliability review with CTO. Quarterly capacity and budget review. Cross-team SRE sync bi-weekly.
- **Cost**: $3-8M/year (10-25 SREs across teams). Enterprise monitoring/paging $15-50K/month. Chaos engineering platform $5-10K/month.
- **Transition trigger**: > 200 engineers, multi-product portfolio, 99.99%+ contractual obligations, public company reliability reporting.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | observability-engineer | Metrics, dashboards, alerts, and SLO instrumentation |
| **This** | site-reliability-engineer | Error budget management, toil reduction, incident response |
| **After** | incident-responder | Incident triage and resolution using SRE-defined runbooks |

Common chains:
- **Chain**: observability-engineer → site-reliability-engineer → incident-responder — Observability data feeds error budgets; incidents are managed with established processes
- **Chain**: devops-engineer → site-reliability-engineer → chaos-engineer — Infrastructure is deployed; SRE validates reliability; chaos experiments test resilience under failure
