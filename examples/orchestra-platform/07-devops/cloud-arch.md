# Cloud Architecture — Orchestra Platform

## Provider & Core Services

Orchestra runs on **AWS**, selected for its mature Kubernetes ecosystem, managed database offerings, and compliance certifications. The core service footprint:

| Service | Purpose |
|---|---|
| **EKS** | Container orchestration for all microservices |
| **RDS Aurora PostgreSQL** | Primary relational database (multi-AZ) |
| **ElastiCache Redis** | Session state, job queues, rate limiting |
| **S3** | Template artifact storage, log archives, backups |
| **CloudFront** | CDN for static assets and template previews |
| **Route53** | DNS with latency-based routing and health checks |
| **KMS** | Envelope encryption for all data at rest |
| **WAF** | OWASP Top 10 protection, rate-based rules for API endpoints |

## Multi-Account Structure

Three isolated AWS accounts enforce blast-radius containment:

- **dev** — sandbox environment. Engineers have broad access. Spot instances used aggressively. No customer data permitted.
- **staging** — pre-production mirror. Same topology as prod but at reduced scale. Synthetic data only. Used for integration testing and demos.
- **prod** — isolated production account. MFA required for all console access and destructive API calls. Changes require a reviewed PR merged by a second engineer.

## Compute (EKS)

Production EKS runs across **3 availability zones** with a mixed-instance strategy:

- **On-demand** for all prod workloads and core system components (`kube-system`, monitoring, ingress controllers). Guarantees availability during spot interruptions.
- **Spot instances** in dev and non-critical staging workloads to reduce cost by ~60%.
- **Cluster Autoscaler** configured with node group priorities — spot ASGs scale first, on-demand fills gaps.
- Kubernetes version: **1.30** (tracking EKS extended support window).

## Networking

Each VPC spans 3 AZs with **public and private subnets per AZ**. Application workloads reside exclusively in private subnets. Internet-bound traffic routes through NAT gateways (one per AZ for resilience). **VPC endpoints** for S3 and DynamoDB eliminate NAT gateway costs for AWS API calls and reduce attack surface.

## IAM & Access Control

**IRSA** (IAM Roles for Service Accounts) maps Kubernetes service accounts to IAM roles with least-privilege policies. Each microservice receives a dedicated role scoped to its exact needs — e.g., the template engine can read from a single S3 bucket prefix only. **No IAM policy in production uses wildcard resources**. Cross-account access uses role chaining with external IDs.

## Disaster Recovery

| Asset | Strategy | RPO | RTO |
|---|---|---|---|
| RDS Aurora | Multi-AZ with automated backups every 5 min | 15 min | 5 min |
| S3 (templates) | Cross-region replication to us-west-2 | 15 min | N/A |
| EKS cluster state | Velero backups to S3, scheduled every 6 hours | 6 hours | 2 hours |

## Cost Model

Estimates are estimates. Actual costs depend on usage patterns, data transfer, and reserved instance timing.

| Stage | Monthly Estimate |
|---|---|
| MVP (dev + staging + prod) | **$3,500/month** |
| 100 customers | **$12,500/month** |

The primary cost drivers at scale are RDS Aurora (IOPS-heavy workloads) and data transfer between services. Reserved instances and Savings Plans are targeted for adoption after the 6-month usage baseline is established.
