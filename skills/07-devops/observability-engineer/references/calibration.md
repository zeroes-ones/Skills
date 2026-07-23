# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You "monitor" production by SSHing into servers and running `tail -f /var/log/syslog` — you've never configured a metrics pipeline | Every service auto-instruments with OpenTelemetry, metrics go to Prometheus, logs to Loki, traces to Tempo — and you can navigate between all three in Grafana using Exemplars | You've reduced mean time to detection (MTTD) from 45 minutes to 90 seconds for 95% of production incidents, proven by comparing incident timelines before and after your observability overhaul |
| Your alerts fire for conditions that don't require action — "CPU > 70%" with no recovery playbook. Your on-call rotation has a 40% burnout rate | Every alert has a runbook with a specific action. Your alert signal-to-noise ratio is > 80%. The on-call rotation has a < 15% burnout rate because alerts are rare and actionable | You've designed a service level objective framework where every team has SLOs with error budgets, and those error budgets drive real decisions: freeze features when budget burns too fast, accelerate when budget is healthy |
| You add `console.log('here')` to debug production issues and deploy it — you've never used a log aggregation system | All production logs are structured (JSON), ingested into a centralized system, and searchable within 5 seconds of emission. You've never `kubectl exec`-ed into a pod to read logs | You've built a self-service observability platform: any team can add a new service and get dashboards, alerts, and SLOs provisioned automatically from a GitOps template — no ticket required, SLI definitions generated from OpenAPI specs |

**The Litmus Test:** Can you receive a P0 page, open a single Grafana dashboard, and within 90 seconds identify: (a) which service is failing, (b) whether it's a code bug or infrastructure issue, (c) the exact deployment or config change that triggered it, and (d) a link to the offending PR — all without opening a terminal?
