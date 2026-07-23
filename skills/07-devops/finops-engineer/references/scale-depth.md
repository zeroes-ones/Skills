# Scale Depth

<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person, 0-100 users)
- **What changes**: No FinOps practice. Check cloud bill monthly. Set billing alerts for $X/month threshold. Use free tier aggressively. No tagging, no RIs, no optimization beyond "did my bill spike?"
- **Overkill**: Tagging strategy, RIs/Savings Plans, cost allocation to teams, unit economics, FinOps lifecycle, carbon tracking, budget governance.
- **Coordination**: You pay the bill. No coordination needed.
- **Cost**: $0 beyond cloud services. Focus on staying in free tier.
- **Transition trigger**: Monthly bill exceeds $500 consistently; first surprise bill > 2x expected.

### Small (2-10 people, 100-10K users)
- **What changes**: Basic tagging (`Environment`, `Service`). Budget alerts at 80% and 100%. Monthly bill review. RI/SP for steady production (1-year, no upfront). Delete unattached EBS/disks monthly. S3 lifecycle policies for logs (30-day → IA, 90-day → delete). No spot instances yet.
- **Overkill**: Unit economics, formal FinOps governance, anomaly detection automation, carbon footprint tracking, Kubernetes cost optimization (unless running K8s at scale), provider negotiation.
- **Coordination**: One person reviews bill monthly. Shared dashboard visible to team. Cost discussed in monthly engineering sync (5 min).
- **Cost**: $0-200/month (cloud cost tools free tier). 30 min/month bill review time.
- **Transition trigger**: Monthly bill > $2K; > 50 resources running; first RI/SP purchase opportunity > $5K/year.

### Medium (10-50 people, 10K-1M users)
- **What changes**: Dedicated FinOps function (part-time, 20-50% of one engineer). Full tagging strategy with SCP enforcement. Budgets per team with alerts. RI/SP coverage 60-80% of compute. Spot for non-production (40%+). Right-sizing program (quarterly reviews). S3 lifecycle policies across all buckets. Anomaly detection enabled. Cost dashboards per team. Kubernetes cost allocation via kubecost. Monthly FinOps review.
- **Overkill**: Dedicated FinOps team, unit economics (unless SaaS with per-customer cost sensitivity), carbon tracking, provider EDP negotiation, formal chargeback.
- **Coordination**: Monthly FinOps review with engineering leads. Cost dashboards self-service for teams. Quarterly optimization sprint. Budget overruns escalate to engineering manager.
- **Cost**: $30-70K/year (part-time FinOps engineer). kubecost or equivalent $2-5K/year. Commitment management overhead ~5 hours/month.
- **Transition trigger**: Monthly bill > $20K; > 5 teams with independent cloud usage; first compliance audit requiring cost allocation evidence.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Dedicated FinOps team (1-3 people). FinOps lifecycle fully implemented. Multi-cloud cost management platform (CloudHealth, Cloudability, Vantage). Unit economics per product/customer. Chargeback or showback with detailed allocation. Formal cost governance with approval workflows. EDP/private pricing negotiation. Carbon-aware optimization. Automated waste elimination (nightly non-prod shutdown). Continuous right-sizing automation. Cost optimization integrated into CI/CD (cost estimate on PR). FinOps certified practitioners.
- **What's full production**: Real-time cost anomaly detection with automated response. Cost-per-feature measurement. Cloud provider business reviews quarterly. FinOps council with cross-functional membership. Published cost optimization scorecards. Carbon reduction targets integrated with cost optimization.
- **Coordination**: Weekly FinOps team sync. Monthly FinOps council (FinOps, finance, engineering leads, CTO). Quarterly business review with cloud providers. Budget governance integrated with procurement.
- **Cost**: $400K-1.2M/year (1-3 FinOps engineers + tools). Multi-cloud cost platform $30-100K/year. Expected savings 20-40% of cloud spend (ROI positive at > $1M/year cloud spend).
- **Transition trigger**: Monthly bill > $100K; multi-cloud environment; > 100 engineers; public company financial controls; customer-facing SaaS with per-tenant cost sensitivity.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | cloud-architect | Cloud architecture with cost estimates |
| **This** | finops-engineer | Cost analysis, optimization recommendations, savings projections |
| **After** | devops-engineer | Infrastructure changes implementing cost optimizations |

Common chains:
- **Chain**: cloud-architect → finops-engineer → devops-engineer — Architecture cost estimates are validated; optimization recommendations are implemented via IaC
- **Chain**: platform-engineer → finops-engineer → cto-advisor — Platform usage costs are analyzed; CTO receives cost-to-value analysis for strategic decisions
