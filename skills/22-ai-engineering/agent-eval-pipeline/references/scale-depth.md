# Scale Depth — Agent Evaluation Pipeline

## Single Agent (1 agent, 1 team)
**Eval scope:** Test pyramid for one agent. 200 unit cases, 50 integration scenarios, 20 E2E scenarios, 50 gotchas.
**Infrastructure:** Docker Compose on developer machine or single CI runner. Pre-merge: <5 min. Nightly: <30 min.
**Metrics:** Per-dimension scores with CIs. PR comments. Drift alerts to team Slack.
**Cost:** $200-500/month in LLM judge API calls.

## Agent Team (3-10 agents, 1-3 teams)
**Eval scope:** Per-agent test pyramids. Shared gotcha library. Cross-agent regression detection (agent A's change shouldn't break agent B).
**Infrastructure:** CI matrix build. Parallel eval containers. Shared Docker registry for eval images. Centralized results database.
**Metrics:** Per-agent dashboards. Cross-agent drift correlation. Team-level eval health (false-positive rate, time-to-detection).
**Cost:** $1,000-3,000/month. Tiered judging: cheap for pre-merge, expensive for nightly.

## Platform (10-50 agents, 5-15 teams)
**Eval scope:** Self-service eval platform. Teams author scenarios, platform executes. Standardized judge calibration. Mandatory gotcha scenarios per agent type.
**Infrastructure:** Eval-as-a-service with REST API. Kubernetes cluster for eval execution. Multi-tenant isolation. Results data warehouse.
**Metrics:** Platform-level SLOs: eval availability >99.5%, pre-merge p95 latency <5 min, false-positive rate <2%. Per-team cost attribution.
**Cost:** $5,000-15,000/month. Volume discounts on judge API calls. Spot/preemptible instances for nightly evals.

## Enterprise (50+ agents, 15+ teams, multiple products)
**Eval scope:** Federated eval platform. Team autonomy with enterprise governance. Compliance-mandated eval for regulated agents (healthcare, finance, legal). Agent marketplace with eval certification.
**Infrastructure:** Multi-region eval execution. Disaster recovery for eval data. SOC 2 compliance for eval platform. SSO/RBAC for eval access.
**Metrics:** Enterprise eval scorecard. Agent quality index (composite across all agents). Eval ROI: cost of eval platform vs cost of undetected regressions. Executive dashboard.
**Cost:** $20,000-50,000/month. Dedicated eval infrastructure team. Custom judge models for domain-specific evaluation.
