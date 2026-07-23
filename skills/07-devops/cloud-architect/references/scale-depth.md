# Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Cloud = one AWS/GCP/Azure account. No IaC (console or click-ops). Default VPC. Managed services for everything (RDS, S3, Lambda). No IAM beyond root + admin. No cost optimization. No multi-region.
- **What to skip**: IaC (Terraform/CDK). Multi-account. Custom VPC. IAM roles. Reserved instances. Cost budgets. WAF. CloudTrail.
- **Coordination**: You are the cloud admin. No coordination needed.

### Small Team (2-10 people, 100-10K users)
- **What changes**: IaC for infrastructure (Terraform). Separate dev + prod accounts (or resource groups). IAM roles (not root). Managed services for database, cache, queue. Cost budgets with alerts. Basic networking (VPC, subnets, NAT). CloudTrail enabled.
- **What to skip**: Multi-account organization (2 accounts is enough). Transit Gateway. Service Control Policies. Reserved Instances (start with on-demand). Multi-region.
- **Coordination**: Cloud changes via IaC PRs. Monthly cost review. Infrastructure access via IAM roles.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Multi-account strategy (AWS Organizations). IAM with SSO + permission boundaries. Custom VPC with private subnets. Transit Gateway for VPC peering. Reserved Instances / Savings Plans (compute). CloudFront CDN. WAF for edge security. CloudTrail centralized. Cost optimization: tagging, budgets, anomaly detection.
- **What to skip**: Multi-cloud (one is enough). Service mesh. Multi-region active-active (warm standby is fine). Dedicated cloud team.
- **Coordination**: Cloud architecture review monthly. FinOps review bi-weekly. IAM access review quarterly. Infrastructure RFC for major changes.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multi-account with AWS Organizations/Control Tower. SCPs + permission boundaries. Service mesh. Multi-region active-active. Multi-cloud (AWS + GCP/Azure). Dedicated cloud platform team. Full FinOps practice. Centralized logging + monitoring. Compliance automation (SOC 2, PCI DSS, HIPAA). Cloud security posture management (CSPM). Infrastructure as product.
- **What's full production**: Cloud center of excellence. Self-service infrastructure catalog. Automated compliance guardrails. Cloud financial operations dashboard. Well-Architected reviews continuous.
- **Coordination**: Cloud platform team weekly. FinOps monthly. Architecture review board monthly. Quarterly Well-Architected review.

### Transition Triggers
- **Solo → Small**: Second developer needs cloud access. First cost surprise >$500/month.
- **Small → Medium**: 3+ teams with separate cloud needs. First compliance audit. >$5K/month cloud spend.
- **Medium → Enterprise**: Multi-region required. Regulatory compliance. >$50K/month cloud spend.
