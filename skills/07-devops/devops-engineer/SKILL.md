---
name: devops-engineer
description: Infrastructure as Code, GitOps, CI/CD strategy, deployment patterns, secret management, service mesh, progressive delivery, cost optimization, and disaster recovery. Triggered by terraform,
  pulumi, ansible, infrastructure, platform, deployment, blue-green, canary, secrets, service mesh, DR, FinOps.
author: Sandeep Kumar Penchala
type: devops
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- devops-engineer
token_budget: 4000
chain:
  consumes_from:
  - backend-developer
  - chaos-engineer
  - ci-cd-builder
  - cloud-architect
  - database-reliability-engineer
  - docker-kubernetes
  - fullstack-developer
  - incident-responder
  - migration-architect
  - networking-engineer
  - observability-engineer
  - performance-engineer
  - platform-engineer
  - qa-engineer
  - release-manager
  - security-engineer
  - system-architect
  feeds_into:
  - chaos-engineer
  - ci-cd-builder
  - database-reliability-engineer
  - docker-kubernetes
  - finops-engineer
  - migration-architect
  - mlops-engineer
  - monorepo-manager
  - observability-engineer
  - platform-engineer
  - release-manager
  - security-engineer
  - security-reviewer
  - site-reliability-engineer
output:
  type: code
  path_hint: ./
---
# DevOps Engineer

Design, automate, and operate resilient multi-cloud infrastructure and delivery pipelines. This skill
covers the full lifecycle: Infrastructure as Code (Terraform/Pulumi patterns), GitOps with Argo CD,
secret management (Vault, external-secrets), infrastructure testing (Terratest, OPA, Checkov), cost
optimization (FinOps), disaster recovery (RPO/RTO design, 3-2-1 backup, failover automation), service
mesh (Istio/Linkerd), and progressive delivery (canary, blue-green, feature flags).

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Write infrastructure as code (Terraform/Pulumi) → Jump to "Core Workflow" — Phase 1 (IaC)
├── Set up CI/CD or deployment pipelines → Invoke `ci-cd-builder` skill instead
├── Configure secrets management (Vault, SOPS) → Jump to "Core Workflow" — Phase 3 (Secrets)
├── Manage Kubernetes or container infrastructure → Invoke `docker-kubernetes` skill instead
├── Set up release management → Invoke `release-manager` skill instead
├── Need reliability and SLO framework → Invoke `site-reliability-engineer` skill instead
├── Build an internal developer platform → Invoke `platform-engineer` skill instead
├── Set up monitoring and observability → Jump to "Core Workflow" — Phase 5 (Observability)
├── Plan a deployment strategy (canary, blue-green) → Go to "Decision Trees" — Deployment Strategy
├── Design cloud infrastructure → Invoke cloud-architect skill instead
├── Respond to an incident → Invoke incident-responder skill instead
└── Not sure? → Describe the problem in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never apply terraform without reviewing the plan.** Always run `terraform plan` and inspect every resource change before `apply`. A typo in a `count` or `for_each` can destroy production.
- **Infrastructure changes need rollback plans.** Every IaC change must have a documented rollback: can you `terraform apply` the previous commit? Is state versioned? Are there data plane changes that can't be rolled back?
- **Never expose secrets in state files.** Terraform state contains all resource attributes in plaintext. Use encrypted backends, treat state files as secrets, and never commit them to version control.
- **Always consider blast radius.** A single Terraform workspace managing 500 resources across 3 environments is a disaster. Use smaller state files, separate workspaces, and explicit dependencies. If you can `destroy` it with one command, it's too big.
- **Always think about the operator on call at 3 AM.** The runbook for "increase capacity" shouldn't be "run terraform, wait 45 minutes, and pray." Build auto-scaling, self-healing, and operational simplicity into the infrastructure.
- **Admit what you don't know.** If a cloud provider's Terraform provider has a known bug or a resource's behavior changed between versions, say so and check the provider changelog.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Provisioning or refactoring cloud infrastructure with Terraform or Pulumi across multi-account architectures
- Designing and implementing GitOps workflows with Argo CD/Flux for Kubernetes fleet management
- Architecting multi-region, active-active, or pilot-light disaster recovery topologies
- Building progressive delivery pipelines: canary analysis, blue-green, feature-flagged rollouts
- Implementing service mesh (Istio, Linkerd) for mTLS, traffic splitting, circuit breaking
- Designing secrets management: Vault dynamic secrets, external-secrets operator, rotation automation
- Establishing FinOps practices: tagging governance, reserved/savings plans, spot instance strategy
- Enforcing policy as code: OPA/Checkov in CI pipelines, Sentinel in TFC/E, drift detection
- Migrating from click-ops → IaC, or push-based CD → GitOps pull-based reconciliation

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### IaC Tool: Terraform vs Pulumi vs CDK
```
                     ┌──────────────────────────┐
                     │ START: Choose IaC tool     │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Team primarily writes in    │
                    │ TypeScript/Python/Go?       │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Multi-cloud │   │ Terraform HCL   │
                    │ needed?     │   │ (industry        │
                    └────┬────────┘   │ standard, largest│
                         │ YES    NO  │ community)      │
                    ┌────▼────┐ ┌▼───┴──────────────┐
                    │ Pulumi  │ │ AWS-only? → CDK    │
                    │ (real    │ │ GCP-only? → Pulumi │
                    │  code,   │ │ Otherwise → TF     │
                    │  multi-  │ └────────────────────┘
                    │  cloud)  │
                    └──────────┘
```
**When to choose Terraform:** Largest community, HCL acceptable, multi-cloud or AWS-dominant, >3 team members. **When to choose Pulumi:** Multi-cloud + real programming languages needed, team already writes TypeScript/Python, need unit-testable infra code. **When to choose CDK:** AWS-only, TypeScript/Python shop, want high-level constructs, CloudFormation under the hood acceptable.

### GitOps vs Push-Based CD
```
                     ┌──────────────────────────┐
                     │ START: Deployment strategy │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Kubernetes-based workloads  │
                    │ AND >3 services?            │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ GitOps      │   │ Push-based CD   │
                    │ (Argo CD /  │   │ (GitHub Actions │
                    │ Flux)       │   │ deploy step or  │
                    │             │   │ AWS CodeDeploy) │
                    └─────────────┘   └────────────────┘
```
**When to choose GitOps:** K8s-native, >3 services, need drift detection and auto-remediation, >5 engineers deploying independently. **When to choose Push-Based:** Non-K8s workloads (Lambda, ECS), <3 services, simpler pipeline, don't need drift detection.

### Secrets Management Approach
```
                     ┌──────────────────────────┐
                     │ START: Secrets strategy    │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ >50 secrets across >5       │
                    │ services with rotation need?│
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ HashiCorp   │   │ Cloud-native:   │
                    │ Vault +     │   │ AWS Secrets     │
                    │ External    │   │ Manager / GCP   │
                    │ Secrets Op  │   │ Secret Manager  │
                    │ (dynamic    │   │ + CI/CD env vars│
                    │  secrets)   │   └────────────────┘
                    └─────────────┘
```
**When to choose Vault:** >50 secrets, dynamic database credentials needed, multi-cloud, auto-rotation with TTL, audit logging required. **When to choose Cloud-Native:** <50 secrets, single cloud, no dynamic secrets needed, simpler operational model, rotation via Lambda/Cloud Functions.

### Progressive Delivery Strategy
```
                     ┌──────────────────────────┐
                     │ START: Safe production     │
                     │ rollout                   │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Need metrics-based          │
                    │ automated rollback?         │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Canary +    │   │ Blue-Green:     │
                    │ Argo        │   │ instant cutover │
                    │ Rollouts /  │   │ with manual     │
                    │ Flagger     │   │ verification    │
                    └─────────────┘   └────────────────┘
```
**When to choose Canary:** Error budget >0.1%, need gradual traffic shift (5%→50%→100%), metrics-based rollback, >10 deploys/week. **When to choose Blue-Green:** Instant rollback required (<1 min), simpler to reason about, can afford 2× infrastructure, <5 deploys/week.

### Disaster Recovery Topology
```
                     ┌──────────────────────────┐
                     │ START: DR architecture     │
                     └────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ RPO <1 min AND monthly      │
                    │ revenue >$1M at risk?       │
                    └────┬──────────────────┬────┘
                         │ YES              │ NO
                    ┌────▼────────┐   ┌─────▼──────────┐
                    │ Active-     │   │ Backup & Restore│
                    │ Active with │   │ (RPO 1-24hr,    │
                    │ multi-region│   │ RTO 1-4hr,      │
                    │ DB (3-5×     │   │ 1.1× cost)      │
                    │ cost)       │   └────────────────┘
                    └─────────────┘
```
**When to choose Active-Active:** RPO <1 min, >$1M/month revenue at risk, 99.99% SLA, budget for 3-5× cost. **When to choose Backup & Restore:** RPO 1-24hr acceptable, <$100K/month revenue at risk, cost-sensitive, 99.5% SLA adequate.

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Discovery & Infrastructure Audit
1. **Inventory & Classification** — Catalog every resource across accounts/projects. Identify snowflake servers, untagged resources, and resources not managed by IaC. Use `aws resourcegroupstaggingapi`, `gcloud asset search-all-resources`, or cloud asset inventory tools.
2. **Architecture Mapping** — Diagram network topology (VPC peering, transit gateway, PrivateLink), data flows, and service dependencies. Document environment topology: dev → staging → UAT → production → DR.
3. **Maturity Assessment** — Evaluate IaC coverage (%), CI/CD adoption, observability posture, incident response process. Score 1-5 on each DORA capability.
4. **Security & Compliance Constraints** — Map regulatory requirements (SOC2, HIPAA, PCI-DSS, GDPR) to infrastructure controls: network segmentation, encryption requirements, data residency, audit logging.

### Phase 2 (~30 min): Infrastructure as Code Design
1. **Tool Selection Matrix**

   | Factor | Terraform | Pulumi | CDK (AWS/Bicep) |
   |---|---|---|---|
   | Ecosystem breadth | ★★★★★ 3,000+ providers | ★★★ Growing, Terraform bridge | ★ AWS/Azure native only |
   | Language flexibility | HCL only | TypeScript, Python, Go, C#, Java | TypeScript, Python, Java, .NET |
   | State management | Self-managed (S3, GCS) or TFC | Pulumi Cloud or self-managed | Cloud-native (CloudFormation) |
   | Testing | Terratest, `terraform test` | Standard test frameworks | CDK assertions, fine-grained |
   | **Best when** | Broad multi-cloud, ops teams | Developer-owned infra, complex logic | Single-cloud, AWS/Azure-native shops |

2. **Repository Structure** — Separate repos per bounded context; never monolithic "infra" repo:
   ```
   infra-networking/     # VPCs, subnets, peering, transit gateway, DNS
   infra-security/       # IAM, KMS, SCPs, security groups, WAF
   infra-compute/        # EKS, ECS, Lambda, ASGs
   infra-data/           # RDS, DynamoDB, ElastiCache, S3 policies
   ```
   Within each repo: `modules/`, `environments/{dev,staging,prod}/`, `global/`

3. **Remote State** — Per-environment, per-component state with locking:
   ```
   s3://org-terraform-state/prod/us-east-1/networking/terraform.tfstate
   s3://org-terraform-state/prod/us-east-1/compute/terraform.tfstate
   ```
   State encryption via KMS; access logged via CloudTrail; alerts on unauthorized reads.

4. **Module Design** — Small, composable, single-purpose. Versioned by git tag (never `main` branch). Every module exports: ARN/ID, endpoint, security group.

5. **Secrets in IaC** — Never in plaintext `.tfvars`. Patterns:
   - `data "aws_secretsmanager_secret_version"` at plan time
   - HashiCorp Vault dynamic database credentials with lease TTL
   - SOPS + age/KMS for encrypted-in-git secrets (decrypted by CI)
   - `sensitive = true` on all secret variables

6. **Policy as Code Pipeline**:
   ```
   pre-commit → terraform fmt -check → terraform validate → checkov/OPA scan → plan → apply
   ```
   High/critical violations block apply. Drift detection: `terraform plan` on cron every 6 hours → alert on non-empty diff.

### Phase 3 (~20 min): GitOps & Deployment Architecture
1. **GitOps Agent Selection** — Argo CD for enterprise (UI, SSO, multi-tenancy, ApplicationSets); Flux for lightweight, OCI-native, Kustomize-first teams.

2. **Application Patterns**:
   - **App of Apps** — Bootstrap Application that discovers child Applications from Git
   - **ApplicationSet** — Template-based multi-cluster/multi-tenant with list, cluster, git, PR generators
   - **PR Generator** — Ephemeral preview environments per pull request, auto-teardown on close

3. **Sync Policy Configuration**:
   ```yaml
   syncPolicy:
     automated:
       prune: true       # Delete resources removed from Git
       selfHeal: true    # Revert manual changes within 5s
     syncWindows:        # Blackout during maintenance
       - schedule: "0 2 * * 1"  # Monday 2 AM
         duration: 2h
         kind: deny
   ```


**What good looks like:** `terraform plan` produces no unexpected changes. CI/CD pipeline deploys to staging in under 10 minutes and production in under 15. Rollback completes in under 5 minutes. All secrets are managed through a vault — zero plaintext credentials in repo.

4. **Deployment Strategy Decision Tree**:
   ```
   Need zero-downtime deploy?
   ├─ Rolling update (Kubernetes default) — Good enough for stateless services
   ├─ Blue-Green — Full duplicate environment, instant rollback, 2x resource cost
   │   └─ Best for: Stateful services, database schema changes, critical releases
   ├─ Canary — Incremental traffic shift with automated analysis
   │   └─ Best for: High-traffic services, risk-averse organizations
   └─ Feature Flags — Decouple deploy from release
       └─ Best for: Continuous delivery, A/B testing, kill switches
   ```

5. **Progressive Delivery with Argo Rollouts**:
   ```yaml
   strategy:
     canary:
       steps:
         - setWeight: 10    # 10% to canary
         - pause: {duration: 5m}
         - analysis:        # Automated metric check
             templates:
               - templateName: error-rate-check
         - setWeight: 50
         - pause: {duration: 10m}
         - setWeight: 100   # Full promotion (or rollback on analysis failure)
   ```

6. **Deployment Gates** — Each environment promotion requires:
   - Smoke tests passing (critical path synthetic transactions)
   - Security scan passing (container CVE threshold, SAST gate)
   - SLO error budget > 50% remaining (automated: block if budget exhausted)
   - Manual approval for production (environment protection rules)

### Phase 4 (~15 min): Secret Management Lifecycle
1. **Hierarchy** — Vault as root of trust → cloud-native secret managers (AWS Secrets Manager, GCP Secret Manager) → Kubernetes Secrets via external-secrets operator or Vault Secrets Operator.

2. **Dynamic Secrets** — No static database credentials. Vault generates ephemeral credentials per application instance with lease TTL:
   ```hcl
   vault write database/roles/app-role \
     db_name=postgres-prod \
     creation_statements="CREATE USER \"{{name}}\" WITH PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
     default_ttl="1h" \
     max_ttl="24h"
   ```

3. **Rotation Automation** — Every secret must have a rotation schedule:
   | Secret Type | Rotation Frequency | Method |
   |---|---|---|
   | Database credentials | 7 days | Vault dynamic secrets or AWS RDS automatic rotation |
   | API keys | 30 days | Vault KV v2 with metadata-driven rotation script |
   | TLS certificates | 90 days | cert-manager with Let's Encrypt; auto-renew at 30-day remaining |
   | Service account keys | 90 days | Automated rotation pipeline; validate new key before revoking old |

4. **Kubernetes Secrets** — Encrypt at rest in etcd (`EncryptionConfiguration`). Never in plaintext manifests. External Secrets Operator syncs from cloud secret managers to Kubernetes Secrets:
   ```yaml
   apiVersion: external-secrets.io/v1beta1
   kind: ExternalSecret
   metadata:
     name: db-credentials
   spec:
     refreshInterval: 1h
     secretStoreRef:
       name: aws-secrets-manager
       kind: ClusterSecretStore
     target:
       name: db-credentials
     data:
       - secretKey: DB_PASSWORD
         remoteRef:
           key: /prod/myapp/db
           property: password
   ```

### Phase 5 (~25 min): Service Mesh Architecture
1. **Istio vs Linkerd Decision**:

   | Factor | Istio | Linkerd |
   |---|---|---|
   | Complexity | High — 10+ CRDs, Envoy sidecar | Low — purpose-built Rust proxy |
   | Features | Traffic splitting, fault injection, rate limiting, authorization (JWT/OAuth), WASM plugins | mTLS, retries, timeouts, circuit breaking, tap |
   | Resource overhead | ~150MB/sidecar | ~30MB/sidecar |
   | Multi-cluster | Native multi-cluster mesh | Multi-cluster via service mirroring |
   | **Best when** | Complex routing, multi-protocol, enterprise governance | Simplicity, low overhead, Kubernetes-only |

2. **mTLS Enforcement**:
   ```yaml
   # Istio PeerAuthentication — strict mTLS mesh-wide
   apiVersion: security.istio.io/v1beta1
   kind: PeerAuthentication
   metadata:
     name: default
     namespace: istio-system
   spec:
     mtls:
       mode: STRICT
   ```

3. **Traffic Splitting for Canary**:
   ```yaml
   apiVersion: networking.istio.io/v1beta1
   kind: VirtualService
   metadata:
     name: myapp
   spec:
     hosts:
       - myapp
     http:
       - route:
           - destination:
               host: myapp-stable
               subset: v1
             weight: 90
           - destination:
               host: myapp-canary
               subset: v2
             weight: 10
   ```

4. **Circuit Breaking** — Prevent cascading failures:
   ```yaml
   apiVersion: networking.istio.io/v1beta1
   kind: DestinationRule
   metadata:
     name: payment-service
   spec:
     host: payment-service
     trafficPolicy:
       connectionPool:
         tcp:
           maxConnections: 100
         http:
           http1MaxPendingRequests: 50
           maxRequestsPerConnection: 10
       outlierDetection:
         consecutive5xxErrors: 5
         interval: 30s
         baseEjectionTime: 60s
         maxEjectionPercent: 50
   ```

5. **Fault Injection** — Chaos testing in production:
   ```yaml
   http:
     - fault:
         delay:
           percentage:
             value: 10
           fixedDelay: 5s
         abort:
           percentage:
             value: 5
           httpStatus: 500
   ```

### Phase 6 (~25 min): Cost Optimization (FinOps)
1. **Tagging Governance** — Every resource tagged with `cost_center`, `environment`, `service`, `managed_by`. Enforced via SCP or OPA policy (block resource creation without tags).

2. **Commitment Discounts**:
   | AWS | GCP | Azure | Coverage Target |
   |---|---|---|---|
   | Reserved Instances (1y/3y) | Committed Use Discounts | Reserved VM Instances | 60-80% of stable baseline |
   | Savings Plans (Compute) | — | Savings Plan for Compute | 60-80% of compute spend |
   | Spot Instances | Preemptible VMs | Spot VMs | 20-40% of stateless workloads |

3. **Idle Resource Detection**:
   ```sql
   -- Cloudability / CloudHealth / custom query: find unattached resources
   SELECT resource_id, resource_type, monthly_cost
   FROM cloud_inventory
   WHERE last_access_time < NOW() - INTERVAL '30 days'
     AND resource_status = 'available'
   ORDER BY monthly_cost DESC;
   ```

4. **Rightsizing Automation** — Weekly analysis: identify over-provisioned instances (CPU < 20%, memory < 30% over 7d) → recommend downgrade. Identify under-provisioned instances → recommend upgrade.

5. **Anomaly Detection** — Monitor daily spend per cost center; alert on +20% deviation from 7-day rolling average.

### Phase 7 (~25 min): Disaster Recovery Implementation
1. **RPO/RTO Definition** — Business Impact Analysis → tiered classification:
   | Tier | RPO | RTO | Pattern | Example |
   |---|---|---|---|---|
   | Tier 0 — Mission Critical | < 1 min | < 15 min | Active-active multi-region | Payment API, Auth |
   | Tier 1 — Business Critical | < 15 min | < 1 hour | Pilot light + read replicas | Customer-facing apps |
   | Tier 2 — Important | < 1 hour | < 4 hours | Backup & restore | Internal tools |
   | Tier 3 — Non-Critical | < 24 hours | < 48 hours | Cold restore | Dev/staging |

2. **3-2-1 Backup Rule** — 3 copies, 2 different media, 1 off-site. Cloud-native: production + replica + cross-region snapshot. Object Lock for ransomware immutability.

3. **Failover Automation** — Terraform parameterized by `dr_active` boolean. Pipeline: verify replication health → promote replicas → scale compute → flip DNS → validate synthetic transactions.

4. **DR Testing Cadence** — Tabletop monthly, component failover quarterly, full regional failover annually. Measure actual RTO/RPO vs targets; every exercise generates postmortem action items.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | cloud-architect | Cloud architecture design and service selection |
| **This** | devops-engineer | Infrastructure as Code, GitOps workflows, deployment automation |
| **After** | ci-cd-builder | Pipeline that deploys the provisioned infrastructure |

Common chains:
- **Chain**: cloud-architect → devops-engineer → ci-cd-builder — Architecture becomes IaC; CI/CD pipeline automates infrastructure deployment
- **Chain**: system-architect → devops-engineer → site-reliability-engineer — System design drives infrastructure provisioning; SRE defines reliability targets for the deployed system

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
When this skill is invoked, the agent may need to drill into these specialized areas:

| Sub-Skill | When to Use |
|-----------|-------------|
| `iac-design` | Provisioning or refactoring infrastructure with Terraform, Pulumi, CDK, or Crossplane |
| `gitops-implementation` | Managing Kubernetes deployments via ArgoCD or Flux with sync policies and health checks |
| `secret-management` | Centralizing credentials, certificates, and API keys with Vault, external-secrets, or sealed-secrets |
| `disaster-recovery` | Designing RPO/RTO targets, backup strategies, and automated failover for business continuity |
| `service-mesh` | Implementing mTLS, traffic management, and observability with Istio, Linkerd, or Cilium |
| `progressive-delivery` | Safe deployment patterns: canary, blue-green, feature flags, and automated rollback |

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `cloud-architect` | Landing zone architecture, networking design, IAM role specifications, cost models | Before provisioning infrastructure or selecting cloud services |
| `system-architect` | Service topology, deployment architecture, non-functional requirements | Before designing infrastructure topology or deployment patterns |
| `backend-developer` | Container resource limits, health check endpoints, migration scripts, environment variables | Before configuring service deployments or resource allocations |
| `security-engineer` | Vault/Secrets Manager architecture, security group design, Pod Security Standards, audit logging requirements | Before implementing secrets management or network policies |
| `ci-cd-builder` | Deploy step design, environment promotion gates, rollback automation, artifact storage | Before integrating infrastructure with deployment pipelines |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `ci-cd-builder` | Infrastructure deployment specs, environment configs, Terraform apply orchestration | CI/CD can't deploy — pipelines blocked |
| `docker-kubernetes` | Cluster provisioning, Helm repo management, GitOps integration, node configuration | Containers have nowhere to run — platform unavailable |
| `release-manager` | Infrastructure change risk assessment, migration rollback plan, environment availability | Releases can't proceed without environment readiness |
| `site-reliability-engineer` | Alerting setup, runbook automation, deploy pipeline integration, error budget checks | SRE can't measure or enforce reliability without infrastructure integration |
| `platform-engineer` | Infrastructure building blocks, IaC modules, cluster templates for golden paths | Platform has no foundation — developers can't self-serve |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
<!-- DEEP: 10+min -->
- **Immutable infrastructure** — Replace, never patch. New AMI/container image for every change. Baking config into golden AMIs defeats the purpose — inject at deploy time.
- **Drift detection on schedule** — `terraform plan` every 6 hours. Alert on non-empty plan. Classify drift: benign (tag mismatch), suspicious (security group opened), critical (unauthorized IAM change → page on-call).
- **Least-privilege pipelines** — OIDC federation, no static credentials. Separate IAM roles for plan (read-only) vs apply (write). Short-lived tokens with audience restriction.
- **Secrets: zero-trust model** — Assume compromise. Dynamic credentials with TTL, just-in-time access, automatic rotation. Audit log on every secret access.
- **GitOps single source of truth** — No `kubectl apply` from laptops. Git repo defines desired state; Argo CD/Flux reconciles. Manual changes auto-reverted within 5 seconds (`selfHeal: true`).
- **Cost-awareness from day one** — Tag every resource. Set budget alerts at 50%, 80%, 100% of monthly forecast. Weekly cost reviews; monthly FinOps meeting with service owners.
- **DR is a continuous practice, not a document** — Run DR tests on schedule. Measure recovery time, not just "it worked." Automate the failover — manual runbooks fail under pressure.

## Infrastructure Cost per User at Scale

| Users | Monthly Infra Cost | Cost Per User | Dominant Cost |
|-------|-------------------|---------------|---------------|
| 0-1K | $50-200 | $0.05-0.20 | Fixed-cost (always-on instances) |
| 1K-10K | $500-2K | $0.05-0.20 | Compute + managed DB |
| 10K-100K | $2K-10K | $0.02-0.10 | Bandwidth + DB + caching |
| 100K-1M | $10K-50K | $0.01-0.05 | Multi-region + observability + support |
| 1M+ | $50K-200K+ | $0.01-0.05 | Everything — optimize relentlessly |

**Target:** Infrastructure cost should be < 10% of revenue at all stages.

## When Managed Services Save Money

### Managed vs Self-Hosted: Breakeven Calculator

```
Self-hosting cost = engineer_salary × fraction_of_time_on_ops + server_cost
Managed cost = service_monthly_fee

Breakeven happens when: service_monthly_fee < engineer_salary × ops_time_fraction
```

| Service | Self-Hosted Cost | Managed Cost | Breakeven |
|---------|-----------------|--------------|-----------|
| **PostgreSQL** | $500/month server + $5K/month ops time (25% of $200K eng) = $5,500/mo | RDS: $300-2K/month | **Always managed** unless extreme scale |
| **Kubernetes** | $2K/month nodes + $10K/month ops (50% of $240K eng) = $12K/mo | EKS: $73/cluster + $2K nodes | Managed saves $10K/month at small scale |
| **Kafka** | $3K/month servers + $8K/month ops = $11K/mo | MSK/Confluent: $2K-8K/month | Breakeven at 5 brokers |
| **Redis/ElastiCache** | $500/month server + $2K/month ops = $2,500/mo | ElastiCache: $200-1K/month | **Always managed** |
| **CI/CD** | $3K/month Jenkins infra + $5K/month = $8K/mo | GitHub Actions: $200/month | **Never self-host CI** under 1K eng |

**Rule:** Self-host only when managed service costs > 2× the engineer cost to run it OR you need features managed services don't offer.

## Self-Hosting Breakeven Calculator

```
Monthly cost to self-host = (server_cost + backup_cost + monitoring_cost) + 
                           (engineer_salary / 12 × ops_time_fraction × team_size)

Example: Self-hosting PostgreSQL
Server: r6i.xlarge = $190/month
Backup + monitoring: $50/month
Ops time: 25% of 1 engineer @ $200K/year = $4,167/month
TOTAL: $4,407/month

RDS equivalent: db.r6i.xlarge Multi-AZ = $780/month
Savings: $3,627/month by using managed.

Self-hosting only wins when:
- You need 10+ dedicated servers → bulk hardware savings > engineer cost
- You have < 1% ops overhead (automated everything, zero-touch)
- You need features no cloud provider offers
```

## Scale Depth: Solo → Small → Medium → Enterprise

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


### Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Staging tests pass — production deploy fails with database connection error | Staging used a t3.micro RDS instance with 100 max connections. Production used a db.r6g.xlarge with 1000 max connections. The application's connection pool was configured for staging's limit. | Never hardcode environment-specific values. All environment-specific configuration must come from environment variables. Use the same configuration structure across environments — only the values differ. Run integration tests in an environment as close to production as possible. | Environment parity is the foundation of reliable deployments. Every difference between staging and production is a class of untestable bugs. |
| Deployment broke because app expected `DATABASE_URL` but IaC only exported `DB_URL` | Environment variables were defined by two different teams (app and infrastructure) with no shared naming convention. Both teams independently chose different variable names. | Define a shared environment variable schema that both application and infrastructure teams agree on. Publish the schema as a document and validate it in CI. Use a `.env.example` file as the single source of truth for variable names. | Naming inconsistency between infrastructure and application code is one of the most common deployment failures. A shared schema turns a silent mismatch into a loud validation error. |
| Terraform destroy accidentally deleted the production RDS instance | A developer ran `terraform destroy` in what they thought was the staging workspace. The workspace selector was set to `prod` from a previous session. | Implement blast radius controls: use separate AWS accounts per environment with SCPs blocking cross-account access. Enable deletion protection on all production databases. Require multi-factor authentication for destroy operations. Never use the same Terraform state file for multiple environments. | A single `terraform destroy` can end your career. Production infrastructure must be protected by multiple layers of defense: account isolation, deletion protection, and human approval gates. |
| Canary analysis showed no errors — 5 minutes after full rollout, all requests failing | Canary analysis compared p95 latency against the stable version, but the canary was configured with 100% traffic during testing so there was no "stable" baseline. | Canary analysis must compare against a live control group receiving old version traffic. At minimum: keep 10-20% of traffic on the old version during the analysis window. Use statistical significance testing, not simple threshold comparison. | Canary without a control group isn't a canary — it's a risky rollout with monitoring. Always maintain a baseline for comparison. |
| Vault dynamic credentials stopped working — all services lost database access simultaneously | Vault's database secret engine TTL was set to 1 hour with a maximum lease TTL of 1 hour. After exactly 1 hour, all credentials expired simultaneously and every application tried to renew at the same time, overwhelming Vault. | Set renewal TTL to stagger across services (not all at T-0). Add a buffer period (renew at 50% of TTL, not 100%). Tune Vault's rate limiting for peak renewal load. Monitor Vault's lease expiration rate — a spike is a pre-incident signal. | Synchronous credential rotation creates thundering herd problems. Always stagger renewal times and add headroom for the peak load. |


## What Good Looks Like

> Infrastructure is fully codified, versioned, and reproducible — nothing is created by hand and nothing drifts. Deployments are zero-downtime with automated rollback on health check failure. Secrets are never in plaintext, never in environment variables, and always retrieved at runtime from a secrets manager. Monitoring, alerting, and logging are standardized across every service. The developer experience from commit to production is seamless: a single command provisions, deploys, and verifies. Mean time to recovery is measured in minutes, not hours, because every failure has a runbook.

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
### IaC & State
- [ ] **[S1]**  Remote state with encryption at rest + locking (S3+DynamoDB, GCS, Azure Blob)
- [ ] **[S2]**  State per environment per component (blast radius isolation)
- [ ] **[S3]**  All modules pinned by immutable git tag or commit SHA
- [ ] **[S4]**  Provider versions pinned (`~>` pessimistic constraint)
- [ ] **[S5]**  `terraform fmt -check` + `terraform validate` enforced in CI
- [ ] **[S6]**  Speculative plan posted as PR comment; apply requires human approval

### GitOps & Deployment
- [ ] **[S7]**  Argo CD/Flux deployed and managing all Kubernetes resources
- [ ] **[S8]**  `selfHeal: true` and `prune: true` for production applications
- [ ] **[S9]**  Sync windows defined for maintenance blackout periods
- [ ] **[S10]**  SSO (OIDC) enabled; RBAC configured per team
- [ ] **[S11]**  Progressive delivery configured (Argo Rollouts or Flagger) with automated analysis
- [ ] **[S12]**  Automated rollback on SLO breach or analysis failure

### Secrets & Security
- [ ] **[S13]**  No plaintext secrets in Git, `.tfvars`, or Kubernetes manifests
- [ ] **[S14]**  External Secrets Operator syncing from cloud secret manager
- [ ] **[S15]**  Vault dynamic secrets with lease TTL for databases
- [ ] **[S16]**  Secret rotation automated for all credential types
- [ ] **[S17]**  Kubernetes etcd encryption at rest configured
- [ ] **[S18]**  mTLS enforced mesh-wide (STRICT mode)

### Observability & Alerting
- [ ] **[S19]**  SLOs defined for all critical user journeys with error budgets
- [ ] **[S20]**  Multi-window burn-rate alerts configured and routed to PagerDuty
- [ ] **[S21]**  Golden signals dashboards (RED + USE) for every production service
- [ ] **[S22]**  Distributed tracing with trace_id in structured logs for correlation

### DR & Reliability
- [ ] **[S23]**  RPO/RTO defined per service tier, signed off by business stakeholders
- [ ] **[S24]**  3-2-1 backup rule applied to all Tier 0-2 data stores
- [ ] **[S25]**  Cross-region replication for databases and object storage
- [ ] **[S26]**  Failover automation scripted, tested, committed to Git
- [ ] **[S27]**  DR test conducted within last quarter; postmortem action items tracked
- [ ] **[S28]**  DNS TTL ≤ 60s for critical endpoints

### Cost & Operations
- [ ] **[S29]**  Tagging governance enforced at account/project level
- [ ] **[S30]**  Budget alerts configured at 50%/80%/100% thresholds
- [ ] **[S31]**  Idle resource detection running weekly
- [ ] **[S32]**  Spot/preemptible instances used for stateless workloads (20-40%)
- [ ] **[S33]**  Runbooks exist for all P1/P2 alerts with escalation paths
- [ ] **[S34]**  Blameless postmortem process established; action items tracked to completion

### Platform Engineering
- [ ] **[S35]**  Internal developer portal (Backstage, Port) for service catalog
- [ ] **[S36]**  Self-service infrastructure provisioning (TFC workspace per team, Backstage scaffolder)
- [ ] **[S37]**  Golden path templates for new services (CI pipeline + IaC + observability + on-call)
- [ ] **[S38]**  Service mesh in place for mTLS, observability, traffic management

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Terraform Patterns — Production Field Manual](references/terraform-patterns.md) — Module design, state management, drift detection, plan review, provider pinning
- [GitOps with Argo CD — Production Field Manual](references/gitops-argocd-guide.md) — Application patterns, sync policies, health checks, progressive delivery, multi-cluster
- [Disaster Recovery Playbook](references/disaster-recovery-playbook.md) — RPO/RTO methodology, 3-2-1 backup, failover automation, DR testing, communication templates
- Google SRE Book — Release Engineering: https://sre.google/
- Argo Rollouts Progressive Delivery: https://argoproj.github.io/argo-rollouts/
- HashiCorp Vault Dynamic Secrets: https://developer.hashicorp.com/vault/docs/secrets/databases
- Open Policy Agent: https://www.openpolicyagent.org/docs/latest/policy-language/
- FinOps Foundation: https://www.finops.org/framework/
- DORA Metrics: https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance
