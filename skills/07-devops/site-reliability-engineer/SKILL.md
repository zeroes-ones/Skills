---
name: site-reliability-engineer
description: SRE, site reliability, error budget, toil reduction, SLI, SLO, SLA, incident management, capacity planning, chaos engineering, reliability engineering. Works with Claude Code, Copilot CLI,
  Cursor, OpenClaw, Gemini CLI.
author: Sandeep Kumar Penchala
type: devops
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- site-reliability-engineer
token_budget: 3555
chain:
  consumes_from:
  - chaos-engineer
  - cloud-architect
  - database-reliability-engineer
  - devops-engineer
  - docker-kubernetes
  - networking-engineer
  - observability-engineer
  - performance-engineer
  - release-manager
  feeds_into:
  - chaos-engineer
  - incident-responder
  - observability-engineer
  - release-manager
output:
  type: code
  path_hint: ./
---
# Site Reliability Engineer (SRE)

Apply software engineering to operations problems. Define and measure reliability through SLIs and
SLOs, manage error budgets as decision-making frameworks, eliminate toil through automation, run
blameless incident analysis, and architect for resilience. Covers the full SRE practice: measurement,
budgeting, automation, incident response, capacity planning, and organizational models.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Define SLOs and SLIs for a service → Jump to "Core Workflow > Phase 1" (SLO/SLI Definition)
│   ├── Greenfield service (no data) → Go to "Decision Trees > SLO Target Selection"
│   └── Existing service with metrics → Start at "Core Workflow > Phase 1" — gather 4 weeks of data
├── Manage error budgets (exhausted, freeze features?) → Jump to "Core Workflow > Phase 2" (Error Budget Management)
├── Reduce toil through automation → Jump to "Core Workflow > Phase 3" (Toil Reduction)
├── Set up incident management / on-call → Jump to "Core Workflow > Phase 4" (Incident Management)
├── Capacity planning (when will we hit scaling limits?) → Jump to "Core Workflow > Phase 5" (Capacity Planning)
├── Run a chaos engineering experiment (GameDay) → Go to "Sub-Skills > chaos-engineering"
├── Need observability instrumentation → Invoke `observability-engineer` skill instead
├── Need incident response procedures → Invoke `incident-responder` skill instead
├── Need release coordination → Invoke `release-manager` skill instead
├── Need infrastructure automation → Invoke `devops-engineer` skill instead
└── Not sure where to start? → "Core Workflow > Phase 1" — you can't manage reliability you haven't measured
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never define SLO without user impact data.** An SLO for "99.9% availability" is arbitrary unless it's tied to when users actually notice degradation. Measure the user experience, not just system metrics.
- **Error budgets are a decision tool, not a metric.** An exhausted error budget means "stop shipping features and invest in reliability." If you ignore the budget and keep shipping, you don't have SRE — you have wishful thinking.
- **Toil must be measurable before it can be reduced.** Track time spent on manual, repetitive, automatable work. If you can't quantify toil, you can't justify the engineering investment to eliminate it.
- **On-call must be sustainable (no single point of failure).** Every service needs at least two on-call responders. Alert fatigue, burnout, and bus-factor-of-one are reliability risks, not HR problems.
- **Always run a blameless postmortem after every incident.** Focus on "what in the system allowed this to happen?" not "who caused this?" Every incident is a learning opportunity.
- **Admit what you don't know.** If you don't have access to production metrics, SLI data, or incident history, say so. SRE recommendations without data are just opinions.

## When to Use

- You need to define SLIs (latency, error rate, throughput) and set SLO targets for a production service
- Your error budget is exhausted and you need to decide whether to freeze features or accept risk
- You are setting up an on-call rotation, incident response process, and blameless postmortem culture
- You need to identify and automate repetitive operational toil — manual deploys, restarts, or config changes
- You are running a chaos engineering experiment (GameDay) to test system resilience under failure
- You need to build a capacity planning model to forecast when your service will hit its scaling limit
- You are redesigning a service for higher reliability — multi-region, active-active, graceful degradation
- You need to choose an SRE organizational model (embedded, consulting, or hybrid) for your team structure

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### 1. What Should Be an SLI?
```
Is this user-visible behavior?
├─ YES → SLI candidate
│   ├─ Can you measure it from the user's perspective?
│   │   ├─ YES → Define SLI
│   │   │   └─ Examples: request latency p95 from load balancer, error rate from application logs
│   │   └─ NO → Use proxy metric (e.g., queue depth for throughput, connection pool wait for saturation)
│   └─ SLI categories (USE + RED):
│       ├─ Latency: time to serve a request (p50, p95, p99)
│       ├─ Traffic: requests per second, concurrent connections
│       ├─ Errors: 5xx rate, timeout rate, dropped messages
│       └─ Saturation: CPU > 80%, memory > 85%, disk > 90%, connection pool exhausted
├─ NO → Internal operational metric (monitor but don't set SLO)
│   └─ Examples: deployment frequency, cache hit ratio, garbage collection pause time
└─ Edge case: Batch systems → measure freshness (data age) and throughput instead of latency
```

### 2. SLO Target Selection
```
What's the reliability floor your users tolerate?
├─ Customer-facing API?
│   ├─ 99.9% availability (43 min downtime/month) — START HERE
│   ├─ 99.95% availability (21 min/month) — add when user complaints about slowness
│   └─ 99.99% availability (4.3 min/month) — only with multi-region active-active; costs 3-5x more
├─ Internal service?
│   ├─ 99.5% (3.6 hours/month) — acceptable for async, batch, admin tools
│   └─ 99.9% — if dependent services have tighter SLOs
├─ Background/async processing?
│   └─ Freshness SLO: "99% of records processed within 5 minutes"
└─ Rule: SLOs must be STRICTER than SLAs (contractual) — typically SLO = SLA × 2 margin
```

### 3. Error Budget Burn Rate Response
```
Error budget consumption rate decision:
├─ Burn rate < 1x (on track to finish budget within window)?
│   └─ Normal operations: deploy freely, take risks
├─ Burn rate 1-5x (exhausting budget faster than window)?
│   └─ Page on-call: investigate within 30 min, freeze risky deploys
├─ Burn rate 5-10x (will exhaust budget in 1/5 of window)?
│   └─ Immediate page + war room: stop all deploys, rollback if recent, escalate to SRE lead
├─ Burn rate > 10x (catastrophic)?
│   └─ Incident declared: all-hands, exec communication, focus solely on mitigation
└─ Multi-window alerting:
    ├─ Short window (1h): catch fast burns — "5% budget burned in 1 hour"
    └─ Long window (6h or 3d): catch slow leaks — "2% budget burned in 6 hours"
```

### 4. Toil: Automate or Accept?
```
Is the work manual AND repetitive AND automatable AND without enduring value AND scaling with growth?
├─ YES to all 5 → Toil: automate immediately
│   └─ Examples: manual log rotation, hand-crafted deploy steps, ticket-driven capacity requests
├─ Manual but infrequent (< 1x/month)?
│   └─ Accept (runbook): document and review quarterly — cost of automation > lifetime toil
├─ Manual but requires human judgment (cannot fully automate)?
│   └─ Augment: build tooling to assist, keep human in loop for decision
│   └─ Examples: approval workflows for production schema changes, incident commander role
└─ Toil budget rule: cap toil at 50% of each SRE's time; excess toil escalates to engineering manager
```

### 5. Incident Severity Classification
```
Is the incident user-visible?
├─ YES → Is the impact > 20% of users or revenue-critical?
│   ├─ YES → SEV1: critical, all-hands, exec comms, 30-min update cadence
│   └─ NO → SEV2: major, dedicated responders, 1-hour update cadence
├─ NO → Internal only?
│   ├─ YES → SEV3: minor, handled during business hours, no page
│   └─ NO → Noise: suppress alert, improve threshold
└─ Data integrity or security involved? → Auto-escalate one level

**What good looks like:** The output opens correctly in the target tool. All validations pass. No placeholder content remains.

```

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Reliability Measurement
1. **Define SLIs for each critical user journey**: identify 2-4 SLIs per service (latency, error rate, throughput, freshness).
   - Input: User journey map, architecture diagram, existing monitoring.
   - Output: SLI specification document with measurement method, data source, and aggregation window.
2. **Implement SLI measurement**: instrument with Prometheus metrics, structured logging, or synthetic probes.
   - Output: Grafana/Prometheus recording rules that compute SLIs over rolling windows (7d, 30d).
3. **Set SLO targets**: based on user tolerance, dependencies, and business criticality (see Decision Tree #2).
   - Output: SLO document per service approved by product owner and engineering lead.
4. **Configure error budget burn rate alerts**: multi-window, multi-burn-rate alerting (see Decision Tree #3).
   - Output: Alerting rules in Prometheus/Alertmanager with clear runbook links.

### Phase 2 (~30 min): Error Budget Governance
1. **Establish error budget policy**: defines what happens at each burn rate threshold.
   - Output: Policy document linked from SLO dashboard, referenced in incident runbooks.
2. **Integrate error budget into release decisions**: deploy freeze when budget is critically depleted.
   - Output: CI/CD pipeline integration that checks budget before production deploys.
3. **Monthly SLO review**: review SLO attainment, error budget consumption, and adjust targets if needed.
   - Output: SLO review dashboard, action items for services that missed SLO.
4. **Quarterly SLO calibration**: tighten SLOs that were too loose, loosen SLOs that caused excessive toil without user benefit.
   - Output: Updated SLO targets with changelog and stakeholder sign-off.

### Phase 3 (~20 min): Toil Elimination
1. **Measure toil**: every SRE logs time against toil/non-toil categories for 2 weeks.
   - Output: Toil baseline as percentage of total SRE effort.
2. **Identify top toil sources**: sort by time-consumed × frequency.
   - Output: Ranked list of toil sources with estimated engineering effort to automate.
3. **Automate top toil**: apply toil elimination framework (see Decision Tree #4).
   - Output: Each automation reduces a toil bucket by > 80%; toil drops below 50% of SRE time.
4. **Prevent toil regression**: require automation design review for any new manual process exceeding 15 min/week.
   - Output: Toil dashboard tracking automation coverage and trends.

### Phase 4 (~15 min): Incident Management Lifecycle
1. **Detection**: monitoring alerts fire → on-call acknowledges within 5 minutes.
2. **Declaration**: incident commander declares severity (SEV1/2/3) within 10 minutes.
3. **Mitigation**: restore service first, root cause later. Rollback, scale, failover, or circuit-breaker activation.
4. **Communication**: status page update within 15 min of declaration; internal comms to stakeholders.
5. **Resolution**: service restored; verify with monitoring; incident commander declares resolved.
6. **Postmortem**: blameless postmortem within 48 hours (SEV1/2) or 1 week (SEV3).
   - Output: Postmortem doc with timeline, contributing factors, action items with owners and deadlines.
7. **Follow-through**: track action items to completion; share learnings org-wide.

### Phase 5 (~25 min): Capacity Planning
1. **Model demand**: forecast growth from business metrics (user growth, transaction volume, data ingestion rate).
   - Output: 12-month demand forecast with confidence intervals.
2. **Map capacity to demand**: translate forecast to compute, storage, network, and license requirements.
   - Input: Current utilization metrics, known scaling limits (e.g., RDS max connections, K8s node limits).
   - Output: Capacity plan with lead times and procurement triggers.
3. **Provision ahead of demand**: order/scale infrastructure when forecast + lead time crosses current capacity.
   - Output: Automated provisioning triggers; no capacity-related incidents.
4. **Review quarterly**: compare forecast vs. actual; tune model.
   - Output: Capacity planning review dashboard.

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `devops-engineer` | Alerting setup, runbook automation, deploy pipeline integration, error budget check infrastructure | Before defining SLO enforcement mechanisms or automating reliability gates |
| `observability-engineer` | SLI instrumentation, dashboards, burn rate alerts, synthetic monitoring | Before setting error budget thresholds or configuring alert policies |
| `cloud-architect` | Multi-region HA design, failover architecture, RPO/RTO targets, capacity forecasts | Before designing resilience patterns or capacity planning models |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `observability-engineer` | SLO definitions, burn rate alert formulas, error budget policy, alert severity calibration | Observability can't build meaningful alerts — everything becomes noise |
| `incident-responder` | Incident severity classification, communication templates, postmortem ownership, runbook procedures | Incidents have no structured response — chaos during outages |
| `release-manager` | Error budget status, deploy freeze recommendations, canary rollout gating, deploy risk assessment | Risky releases ship without guardrails — production instability |

## Scale Depth
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

## What Good Looks Like

> Every service has defined SLIs, SLOs, and error budgets that are reviewed quarterly with stakeholders. Error budget burn triggers automated policy actions — deployments freeze, reliability work gets prioritized, and the team aligns before the budget is exhausted. Incident retrospectives are blameless and produce actionable follow-ups completed within two weeks. The system meets its availability targets while the team maintains a sustainable operational load: on-call shifts are quiet, toil is under 50% of the team's time, and every repeated incident drives a permanent fix rather than a workaround.

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|---|---|---|
| `sli-slo-definition` | Defining reliability indicators and objectives for a new or existing service | Measurement methodology, data sources, aggregation windows, stakeholder negotiation |
| `error-budget-policy` | Designing governance around error budget consumption | Burn rate thresholds, policy automation, deploy gating, stakeholder communication |
| `toil-elimination` | Reducing operational toil through automation | Toil identification framework, automation ROI, toil budgeting, preventing regression |
| `incident-management` | Running the full incident lifecycle from detection to postmortem | Severity classification, commander role, communication templates, postmortem facilitation |
| `capacity-planning` | Forecasting demand and provisioning resources ahead of need | Demand modeling, headroom calculation, procurement triggers, cost optimization |
| `chaos-engineering` | Proactively testing system resilience through controlled experiments | Experiment design, blast radius, steady-state hypothesis, automated experimentation platforms |
| `production-readiness-review` | Assessing if a service meets reliability bar for production | PRR checklist, reliability patterns audit, operational maturity scoring |
| `progressive-delivery` | Canary, blue-green, and ring deployments with automated analysis | Deployment strategies, metrics-based promotion, automated rollback, risk scoring |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Hope is not a strategy**: every critical user journey needs an SLI. If you can't measure it, you can't manage it.
- **SLOs are a decision-making tool, not a report card**: use error budgets to decide when to ship features vs. invest in reliability — not to punish teams.
- **100% is the wrong target**: 100% reliability costs exponentially more and prevents innovation. Users don't notice the difference between 99.99% and 99.999% on a mobile connection.
- **Automate toil until it hurts (and then automate some more)**: every manual step is a future incident. SREs should spend > 50% of time on engineering work, not operations.
- **Blameless is not consequence-free**: postmortems should be blameless in tone but rigorous in action items. "Blameless" means "we all want to fix the system," not "nobody is accountable."
- **Alert on symptoms, not causes**: alert on "user-facing error rate > 1%" not "CPU > 80%." The latter is a <!-- DEEP: 10+min -->
debugging signal, not a user-impact signal.
- **Every alert must require human action**: if an alert fires and you can ignore it, it's noise — tune the threshold or remove it. Alert fatigue kills response times.
- **Runbooks before alerts**: never create an alert without a linked runbook. "Page first, figure it out later" is how SEV1s become SEV0s.
- **Capacity is a reliability concern**: running out of capacity is a self-inflicted outage. Plan for 2x peak and have elastic scaling as backup.
- **SRE is cultural, not a job title**: reliability is everyone's responsibility. SRE provides the framework, tooling, and expertise — but service owners own their SLOs.


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Permission denied` | Missing file/system permissions | Use `chmod +x` or `sudo`; check user/group ownership |
| `command not found` | Required tool not installed | Install with `apt install`, `brew install`, or `npm install -g` |
| `File exists` | Output file already exists | Use `--force` flag or specify different output path |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  SLIs defined for all critical user journeys (minimum: latency, error rate, throughput per service)
- [ ] **[S2]**  SLOs documented with stakeholder sign-off for each production service
- [ ] **[S3]**  Multi-window, multi-burn-rate alerting configured for all SLOs
- [ ] **[S4]**  Error budget policy documented and integrated with deploy pipeline (freeze when critically depleted)
- [ ] **[S5]**  On-call rotation established with clear escalation path and runbooks for every alert
- [ ] **[S6]**  Incident management process defined: commander role, severity levels, communication cadence, postmortem timeline
- [ ] **[S7]**  Blameless postmortem completed for all SEV1 and SEV2 incidents within 48 hours
- [ ] **[S8]**  Postmortem action items tracked to completion; > 90% closed within 30 days
- [ ] **[S9]**  Toil tracked and < 50% of SRE team time; top-3 toil sources have automation in progress
- [ ] **[S10]**  Capacity plan updated quarterly with 12-month forecast; no capacity-related incidents in past 6 months
- [ ] **[S11]**  Chaos engineering gameday conducted at least quarterly; findings tracked to remediation
- [ ] **[S12]**  Production readiness review completed for all new services before production traffic
- [ ] **[S13]**  SLO review conducted monthly; targets calibrated quarterly based on user feedback and error budget consumption
- [ ] **[S14]**  Reliability dashboard visible to all engineers with SLI status, error budget remaining, and incident history

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Google SRE Book](https://sre.google/books/) — Foundational SRE principles, SLI/SLO framework, toil elimination
- [SRE Workbook](https://sre.google/workbook/) — Practical implementation: SLOs, error budgets, incident response
- [Implementing Service Level Objectives](https://www.oreilly.com/library/view/implementing-service-level/9781492076803/) — Alex Hidalgo's practical guide to SLO implementation
- [DORA Metrics](https://dora.dev/) — Deployment frequency, lead time, MTTR, change failure rate
- [PagerDuty Incident Response](https://response.pagerduty.com/) — Incident commander training and process templates
- [Chaos Engineering](https://principlesofchaos.org/) — Principles of Chaos Engineering
- Internal: [../../domain/references/sre-patterns.md](../../domain/references/) — Detailed reliability patterns and anti-patterns
