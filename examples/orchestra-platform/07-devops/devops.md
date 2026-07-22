# Infrastructure as Code — Orchestra Platform

## Terraform

Orchestra's infrastructure is defined in **Terraform** across **25 modules** organized by domain:

| Domain | Modules |
|---|---|
| **Networking** | VPC, subnets, NAT gateways, VPC endpoints, transit gateway |
| **Compute** | EKS cluster, node groups, cluster autoscaler, IRSA roles |
| **Data** | RDS Aurora, ElastiCache, S3 buckets, backup policies |
| **Monitoring** | Prometheus stack, Grafana, Loki, Tempo, alertmanager |
| **Security** | KMS keys, WAF rules, security groups, IAM roles |

Remote state is stored in **S3** with **DynamoDB** for state locking, preventing concurrent `terraform apply` across CI runners. Each AWS account has its own state bucket. Module versions are pinned to specific git tags to prevent drift.

## GitOps with ArgoCD

Deployments follow a **GitOps** model using **ArgoCD**. Kubernetes manifests and Helm charts live in `orchestra-deploy`, the single source of truth for cluster state.

- **Apps-of-apps pattern** — a root ArgoCD application bootstraps all child applications (services, ingress, monitoring, certificates). Adding a new service is a single YAML file in the deploy repo.
- **Automated sync** polls the deploy repo every 3 minutes. Manual sync is available for urgent changes.
- **Prune and self-heal** enabled — drift from the desired state is auto-corrected.

## Secrets Management

Three tiers of secret storage:

| Tier | Tool | Use Case |
|---|---|---|
| **External** | AWS Secrets Manager | Database credentials, third-party API keys, Stripe secrets |
| **Internal** | HashiCorp Vault | Service-to-service auth tokens, internal encryption keys, short-lived database credentials |
| **GitOps** | Sealed Secrets | Encrypted secrets committed alongside manifests (e.g., ingress basic-auth, webhook tokens) |

External Secrets Operator syncs AWS Secrets Manager entries into Kubernetes secrets, refreshing automatically on rotation.

## Atlantis

**Atlantis** runs in a dedicated ECS task, triggered by PR comments:

- `atlantis plan` — runs `terraform plan` on PR open or when commented. Output is posted back as a PR comment.
- `atlantis apply` — runs `terraform apply` on merge to main. Requires plan approval by a second engineer for production.
- **Locking** prevents concurrent plans on the same directory. Locks auto-expire after 30 minutes of inactivity.

## Environment Promotion Flow

```
Push to main  →  dev (auto-deploy)
    │
    ▼
PR merge to staging  →  staging (auto-deploy)
    │
    ▼
Manual approval  →  prod (gated deploy)
```

## Core Principle

> **Never apply terraform without reviewing the plan. Infrastructure changes need rollback plans.**

Every `terraform apply` must have a documented rollback procedure in the PR description. For database changes, the rollback plan must account for schema migrations and data compatibility. For network changes, a connectivity smoke test validates routing before the deployment is considered complete.
