# Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: DevOps = PaaS (Vercel/Railway/Render). No IaC. No containers. No CI/CD pipeline. Manual deploy via git push. Monitoring = built-in PaaS dashboard. Secrets in `.env` (or platform env vars).
- **What to skip**: Terraform/Pulumi. Docker. Kubernetes. CI/CD pipelines. GitOps. Observability stack (Prometheus/Grafana). Secrets management (Vault). Infrastructure monitoring.
- **Coordination**: You are ops + dev. No coordination needed.

### Small Team (2-10 people, 100-10K users)
- **What changes**: IaC for infrastructure (Terraform). Docker for consistent environments. CI/CD with test + deploy. Managed services for database, cache, queue. Basic monitoring (logs + uptime + basic metrics). Secrets in CI/CD secrets manager. Staging environment.
- **What to skip**: Kubernetes. GitOps. Service mesh. Full observability (just logs + uptime + basic metrics). Multi-region. Self-hosted anything.
- **Coordination**: DevOps tasks shared among developers. Weekly infra review. PagerDuty for production alerts (rotating).

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Dedicated DevOps/SRE (1-2 people). Kubernetes or ECS. GitOps (Argo CD/Flux). Full observability (Prometheus + Grafana + Loki + Tempo). IaC per environment with state isolation. Secrets management (Vault or cloud KMS). CI/CD with security scanning. Auto-scaling. Blue-green deployments. SLOs defined.
- **What to skip**: Multi-cloud. Service mesh. Chaos engineering. Dedicated platform team.
- **Coordination**: DevOps weekly planning. Monthly infrastructure review. On-call rotation (follow-the-sun if needed).

### Enterprise (50+ people, 1M+ users)
- **What changes**: Platform engineering team (3+ engineers). Internal developer platform (Backstage). Multi-cloud infrastructure. Service mesh (Istio/Linkerd). Full GitOps. Secrets management with rotation. Chaos engineering. Multi-region active-active. SLOs with error budgets. FinOps practice. Compliance automation. Capacity planning.
- **What's full production**: Developer platform as a product. Self-service infrastructure. Automated compliance. Cost optimization dashboard. Platform engineering metrics (DORA + platform adoption).
- **Coordination**: Platform team weekly. Monthly infrastructure review. Quarterly capacity planning. On-call with escalation paths.

### Transition Triggers
- **Solo → Small**: Second developer. PaaS limitations hit (cost or features).
- **Small → Medium**: 3+ services. Manual deploys causing issues. First production incident at 3 AM.
- **Medium → Enterprise**: 10+ services with cross-team ownership. Multi-region or compliance required. >50 engineers.
