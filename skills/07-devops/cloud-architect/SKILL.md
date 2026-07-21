---
name: cloud-architect
description: AWS, Azure, GCP architecture design, landing zones, multi-cloud strategy, cost optimization, IAM, networking, and serverless. Triggered by cloud, AWS, Azure, GCP, architecture, landing zone, multi-cloud, serverless, IAM, Well-Architected.
author: Sandeep Kumar Penchala
---

# Cloud Architect

Design secure, scalable, cost-optimized cloud architectures across AWS, Azure, and GCP. Covers
landing zone design, multi-account/ multi-project governance, networking topologies, IAM strategy,
managed service selection, serverless patterns, and the Well-Architected Framework.

## When to Use

- Designing greenfield cloud architecture or migrating on-premises workloads to the cloud
- Setting up a cloud landing zone with multi-account (AWS Organizations) or multi-project (GCP resource hierarchy) isolation
- Architecting networking: VPC design, transit gateway, hub-and-spoke, private link, Cloud Interconnect
- Designing IAM: least-privilege roles, workload identity, resource-based policies, permission boundaries
- Selecting managed services (RDS vs. self-managed DB, ECS vs. EKS, Cloud Run vs. GKE) with trade-off analysis
- Performing Well-Architected Framework reviews and implementing recommendations
- Implementing FinOps: cost allocation tags, budgets, reserved instances, savings plans, anomaly detection
- Architecting for multi-region DR with RPO/RTO targets and automated failover

## Core Workflow

### Phase 1: Discovery and Requirements
1. Gather business requirements: user base, expected throughput, data residency constraints, compliance regime.
2. Define RPO (Recovery Point Objective) and RTO (Recovery Time Objective) for each workload tier.
3. Inventory existing workloads: compute, databases, storage, DNS, identity providers, third-party integrations.
4. Identify constraints: latency budgets between services, egress costs, data sovereignty, vendor lock-in tolerance.
5. Select cloud provider(s) based on feature parity, team expertise, existing commitments, and geographic presence.

### Phase 2: Landing Zone and Governance
1. Design the organization structure: AWS OUs/accounts per environment and workload; GCP folders/projects; Azure management groups/subscriptions.
2. Implement a security account/project for centralized logging, audit trails (CloudTrail, Audit Logs), and security tooling.
3. Establish networking foundation: hub VPC/VNet with inspection (firewall, IDS/IPS), spoke VPCs for workloads, transit gateway for inter-VPC routing.
4. Configure IP address management (IPAM): non-overlapping CIDR blocks across all VPCs, regions, and on-premises networks.
5. Define IAM strategy: SSO via identity provider (Okta, Azure AD), permission sets based on job function, break-glass roles for emergencies.
6. Implement Service Control Policies (AWS) or Organization Policies (GCP) to deny high-risk actions organization-wide.
7. Automate account/project provisioning with Terraform or custom Control Tower/Azure Landing Zone accelerator.

### Phase 3: Workload Architecture
1. Choose compute: containers (EKS, GKE, AKS) for microservices; serverless (Lambda, Cloud Run, Azure Functions) for event-driven; VMs for lift-and-shift.
2. Design data tier: relational (RDS, Cloud SQL), NoSQL (DynamoDB, Firestore), caching (ElastiCache, Memorystore), object storage (S3, GCS).
3. Architect for high availability: multi-AZ deployments within a region; multi-region with DNS failover (Route 53, Cloud DNS) or global load balancers.
4. Implement service discovery: CloudMap, Consul, or Kubernetes native DNS; use private API endpoints (PrivateLink, Private Service Connect) for intra-VPC traffic.
5. Design CI/CD integration: OIDC-based authentication from pipelines to cloud APIs; immutable infrastructure deployments.
6. Select appropriate managed services and justify trade-offs: RDS vs. self-managed PostgreSQL on EC2 — consider backup, patching, scaling overhead.

### Phase 4: Cost Optimization (FinOps)
1. Tag all resources with `Environment`, `Service`, `Team`, `CostCenter`; enforce tagging with SCPs or policy.
2. Set budgets with alerts at 50%, 80%, and 100% thresholds; configure anomaly detection in AWS Cost Explorer or GCP Billing.
3. Purchase reserved instances or savings plans for stable baseline workloads; use spot/preemptible instances for fault-tolerant batch jobs.
4. Right-size underutilized resources using Compute Optimizer or Recommender services.
5. Implement data lifecycle policies: transition infrequently accessed objects to colder storage tiers; auto-delete after retention period.
6. Review egress costs: prefer PrivateLink/Private Service Connect over NAT Gateway for service-to-service traffic; use CloudFront/CDN to reduce origin egress.

### Phase 5: Security and Compliance
1. Encrypt data at rest with KMS/Cloud KMS customer-managed keys; encrypt data in transit with TLS 1.2+.
2. Implement VPC Flow Logs, DNS query logging, and S3 access logging for network forensics.
3. Use AWS Config, Azure Policy, or GCP Security Command Center for continuous compliance monitoring.
4. Establish incident response runbooks specific to cloud attack vectors: compromised credentials, exposed buckets, cryptomining.
5. Conduct regular Well-Architected Framework reviews and penetration tests.

## Sub-Skills

When this skill is invoked, drill into these specialized areas as needed:

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| `landing-zone-design` | Setting up multi-account (AWS Organizations), multi-project (GCP), or management groups (Azure) | This file — Phase 1: Account Structure |
| `cloud-networking` | Designing VPCs, transit gateways, hub-and-spoke topologies, PrivateLink, and hybrid connectivity | This file — Phase 2: Networking |
| `iam-design` | Architecting least-privilege IAM with SSO, permission boundaries, SCPs, and workload identity | This file — Phase 3: IAM |
| `cost-optimization` | Implementing FinOps: tagging, budgets, RIs/savings plans, spot instances, and anomaly detection | `references/cloud-cost-optimization.md` |
| `managed-service-selection` | Choosing between managed and self-managed services with TCO and operational trade-off analysis | This file — Best Practices section |
| `multi-cloud-strategy` | Architecting across AWS, Azure, and GCP with abstraction layers and provider-agnostic patterns | This file — Multi-Cloud vs Single-Cloud Cost |
| `serverless-architecture` | Designing event-driven systems with Lambda, Cloud Run, or Azure Functions — cold starts, scaling, costs | This file — Serverless Cost Traps |

## Cross-Skill Coordination

Cloud architects design the foundational infrastructure that all services run on. They coordinate with every engineering team for workload placement, DevOps for implementation, security for hardening, and finance for cost governance.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **DevOps Engineer** | Infrastructure provisioning, IaC implementation | Architecture diagrams, Terraform module design, landing zone requirements, deployment pipeline integration |
| **Backend Developer** | Service deployment, managed service selection | Workload characteristics (CPU/memory/I/O profile), managed vs self-managed trade-off analysis, latency budgets |
| **Security Engineer** | IAM design, network security, encryption, compliance | Least-privilege IAM roles, VPC security group design, KMS key policies, compliance control mapping to cloud services |
| **Docker/Kubernetes Specialist** | Cluster architecture, node management, service mesh | EKS/GKE/AKS configuration, node group design, cluster autoscaler, CNI plugin selection |
| **Data Engineer** | Data storage architecture, analytics infrastructure | RDS vs Redshift vs Snowflake trade-offs, Spark on EMR vs Glue vs Databricks, streaming (Kinesis vs MSK) |
| **Observability Engineer** | Cloud-native monitoring, logging infrastructure | CloudWatch/Cloud Monitoring setup, centralized logging architecture, cost monitoring dashboards |
| **CI/CD Builder** | Cloud auth for pipelines, deployment integration | OIDC provider setup, IAM roles for GitHub Actions/GitLab CI, artifact storage (ECR, Artifact Registry) |
| **Compliance Officer** | Data residency, compliance certification scope | Region restrictions, encryption requirements, audit trail completeness, compliance evidence from cloud APIs |
| **Finance/Business** | Cloud budget, FinOps, commitment discounts | Cost allocation tags, RI/SP recommendations, budget alert thresholds, monthly cloud spend review |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| New AWS/GCP/Azure service being evaluated for production | DevOps, Security Engineer, Affected teams | Security review, cost modeling, operational readiness assessment |
| Cloud provider outage or degradation | DevOps, Incident Responder, All service owners | Impact assessment; failover activation if multi-region |
| Architecture decision record (ADR) proposed | All engineering stakeholders | Review and comment before acceptance |
| Cost anomaly >50% of monthly forecast | DevOps, Finance, Affected team | Immediate investigation; resource cleanup or budget increase |
| Security finding from cloud posture management (AWS Config, Security Command Center) | Security Engineer, DevOps | Remediation; may indicate misconfiguration or compromise |
| RI/SP commitment decision (>$10K/yr) | Finance, CTO | Purchase approval; budget allocation |

### Escalation Path

```
Cloud provider outage affecting production? → DevOps → Incident Responder → CTO
Security control failure (open S3 bucket, public RDS)? → Security Engineer → Compliance Officer
Cost overrun threatening budget? → Finance → CTO
Architecture decision deadlock? → CTO Advisor
Cross-cloud migration decision? → CTO Advisor → CEO Strategist
```

## Best Practices

- **Account/project isolation**: separate production and non-production at the account level; never mix in a single VPC.
- **Infrastructure as Code from day one**: the console is for exploration only; all production changes go through IaC pipelines.
- **Least privilege IAM**: start with no permissions, add only what's needed; use IAM Access Analyzer to validate.
- **Design for failure**: assume any component can fail at any time; use circuit breakers, retries with backoff, and graceful degradation.
- **Region selection**: prioritize latency, data residency, service availability, and cost in that order.

## Is This Overkill? Checklist

| Scenario | Overkill Unless... |
|----------|-------------------|
| Multi-cloud for < $50M ARR | You have $100K+ in credits from GCP/Azure |
| Service mesh for < 10 services | You need strict mTLS for compliance |
| Multi-region active-active for < 100K DAU | 99.99% SLA is a contractual requirement |
| KMS with external HSM for < 100 secrets | You're in fintech/healthcare with regulatory mandate |
| Custom VPC with Transit Gateway for 1 app | You have on-prem hybrid connectivity requirements |
| Provisioned concurrency for all Lambdas | P99 latency > 500ms for customer-facing endpoints |

## Multi-Cloud vs Single-Cloud Cost

| Factor | Single-Cloud | Multi-Cloud |
|--------|-------------|-------------|
| Commitment discounts | 40-60% (concentrated spend) | 20-30% (spread across providers) |
| Egress costs | $0 (intra-cloud) | $200-1,200/month per 10TB cross-cloud |
| Engineer premium | Standard salary | +$20-50K for multi-cloud expertise |
| Compliance audit cost | 1× | 2× (per cloud) |
| Negotiated discounts | Higher (larger single bill) | Lower (smaller per-cloud bill) |
| **Verdict** | **Best for < $50M ARR** | **Consider at $100M+ ARR** |

## Serverless Cost Traps

| Trap | Impact | Fix |
|------|--------|-----|
| **Lambda Provisioned Concurrency idle** | $35/month per 1GB provisioned, even at 0 invocations | Reserve only for latency-critical paths |
| **DynamoDB On-Demand at steady state** | 7× more expensive per operation vs provisioned | Switch to provisioned + auto-scaling after 30d |
| **API Gateway no caching** | Every request hits backend | Enable API Gateway cache ($0.02/hr per GB) |
| **Lambda 10GB memory for simple CRUD** | 20× cost of 512MB | Start at 512MB; scale up only if CPU-bound |
| **NAT Gateway per AZ** | $32/AZ/month × 3 AZs = $96/mo wasted | 1 NAT + VPC endpoints for S3/DynamoDB |
| **CloudFront no caching policy** | Every request = origin fetch cost | Set CachePolicy with 1hr TTL for static content |

## Scale Depth: Solo → Small → Medium → Enterprise

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

## Production Checklist

- [ ] Multi-account/multi-project isolation with separate production and non-production environments
- [ ] Networking: non-overlapping CIDRs, private subnets for workloads, NAT Gateway for egress, VPC Flow Logs enabled
- [ ] IAM: SSO configured, no long-lived access keys, break-glass roles, permission boundaries enforced
- [ ] Encryption: data at rest with CMK, TLS 1.2+ in transit, S3 bucket policies block public access
- [ ] Logging: CloudTrail/Audit Logs enabled organization-wide, centralized to a security account
- [ ] Backups: automated backups for all data stores, cross-region replication for critical data, restore tested quarterly
- [ ] Cost: budgets set with alerts, tagging strategy enforced, RI/SP coverage for baseline workloads
- [ ] DR: RPO/RTO defined, failover runbook documented and tested, multi-region for tier-1 services
- [ ] Well-Architected Framework review completed within the last 6 months
- [ ] Incident response plan covers cloud-specific scenarios and is tested annually

## References

- [Cloud Cost Optimization Playbook](references/cloud-cost-optimization.md) — Commitment discounts, spot strategy, right-sizing, serverless cost traps, free tier maximization
- AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/
- Azure Well-Architected Framework: https://learn.microsoft.com/en-us/azure/well-architected/
- Google Cloud Architecture Framework: https://cloud.google.com/architecture/framework
- AWS Organizations Best Practices: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices.html
- FinOps Framework: https://www.finops.org/framework/
