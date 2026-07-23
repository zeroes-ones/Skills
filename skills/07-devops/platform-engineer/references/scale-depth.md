# Scale Depth

<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
- **What changes**: No IDP needed. Document patterns in a README. Single Terraform repo. Manual onboarding.
- **Overkill**: Backstage, scaffolding tools, ephemeral environments, platform APIs, scorecards.
- **Coordination**: You are the platform. No coordination overhead.
- **Cost**: $0 beyond cloud infrastructure costs.
- **Transition trigger**: Second developer joins; onboarding friction becomes visible (> 1 week to first deploy).

### Small (2-10 people, 100-10K users)
- **What changes**: Shared Terraform modules in a monorepo. Templated CI/CD (reusable workflows). `cookiecutter` scaffolding for new services. One shared dev AWS account. Runbooks in a wiki.
- **Overkill**: Developer portal, Backstage, platform APIs, formal SLAs, NPS surveys, ephemeral per-PR environments (use shared staging).
- **Coordination**: Platform changes via PR review. Monthly platform sync (30 min). Shared Slack channel.
- **Cost**: ~$200-500/month for shared dev infrastructure. Platform engineer is part-time role (20% of senior engineer).
- **Transition trigger**: 3+ services with divergent patterns emerge; onboarding > 3 days; first "I didn't know that existed" moment.

### Medium (10-50 people, 10K-1M users)
- **What changes**: Dedicated platform team (2-4 engineers). Backstage or Port deployed. Golden path templates with policy guards. Ephemeral per-PR environments for key services. Platform CLI. Scorecards with tech health metrics. Self-service infrastructure catalog (Terraform modules with JSON schema validation).
- **Overkill**: Full platform-as-product with PM, multi-platform-team topology, formal deprecation SLAs, plugin marketplace.
- **Coordination**: Platform team runs weekly office hours. Quarterly developer NPS survey. Cross-team platform RFCs for major changes. Monthly platform review with engineering leadership.
- **Cost**: $300-500K/year (2-4 engineers). Backstage hosting ~$500-1,000/month. Ephemeral env cloud costs ~$2-5K/month.
- **Transition trigger**: >50 engineers, multiple business units, compliance audit requirements; platform team becomes bottleneck.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multiple platform teams (2-3) with PMs. Platform Product Manager with roadmap. Published platform SLAs (99.9% availability). Developer Relations function. Plugin marketplace for internal tools. Automated compliance in golden paths. Multi-cloud platform support. Dedicated platform SRE rotation. Brownfield migration service offering.
- **What's full production**: Platform NPS dashboard, adoption rate metrics, cost-per-developer tracking, quarterly platform summit, internal conference talks.
- **Coordination**: Platform PM runs quarterly planning. Monthly stakeholder review. Weekly platform team standups. Bi-weekly cross-platform-team sync. Developer advisory board (quarterly).
- **Cost**: $1.5-3M/year (6-12 engineers + PM + DevRel). Portal hosting $5-15K/month. Ephemeral env costs $20-50K/month. Tooling licenses $50-100K/year.
- **Transition trigger**: Platform team becomes bottleneck for >20% of requests; >3 business units with divergent platform needs; developer NPS declining.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | devops-engineer | Infrastructure building blocks (IaC modules, clusters) |
| **This** | platform-engineer | IDP, golden paths, developer portal, self-service APIs |
| **After** | docker-kubernetes | Containerized workloads deployed via platform golden paths |

Common chains:
- **Chain**: devops-engineer → platform-engineer → docker-kubernetes — Infrastructure primitives become self-service; developers deploy containers through golden paths
- **Chain**: cloud-architect → platform-engineer → observability-engineer — Cloud architecture informs platform design; platform provides standard observability across all services
