---
name: devops-engineer
description: Infrastructure as Code, GitOps, CI/CD strategy, deployment patterns,
  secret management, service mesh, progressive delivery, cost optimization, and disaster
  recovery. Triggered by terraform, pulumi, ansible, infrastructure, platform, deployment,
  blue-green, canary, secrets, service mesh, DR, FinOps.
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
  - hipaa-technical-implementation
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
------
# DevOps Engineer

Design, automate, and operate resilient multi-cloud infrastructure and delivery pipelines. This skill
covers the full lifecycle: Infrastructure as Code (Terraform/Pulumi patterns), GitOps with Argo CD,
secret management (Vault, external-secrets), infrastructure testing (Terratest, OPA, Checkov), cost
optimization (FinOps), disaster recovery (RPO/RTO design, 3-2-1 backup, failover automation), service
mesh (Istio/Linkerd), and progressive delivery (canary, blue-green, feature flags).

## Route the Request
<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("main.tf")` OR `file_exists("Pulumi.yaml")` OR `file_exists("cdktf.json")` | Jump to "Core Workflow" — Phase 1 (IaC) for infrastructure-as-code review |
| A2 | `file_exists(".github/workflows/")` AND `file_contains(".github/workflows/", "deploy\|apply\|terraform")` | Invoke `ci-cd-builder` skill instead |
| A3 | `file_exists("vault/")` OR `file_contains("main.tf", "vault_\|aws_secretsmanager\|azure_key_vault")` OR `file_exists(".sops.yaml")` | Jump to "Core Workflow" — Phase 3 (Secrets) |
| A4 | `file_exists("Chart.yaml")` OR `file_exists("kustomization.yaml")` OR `file_contains("main.tf", "kubernetes_\|helm_release")` | Invoke `docker-kubernetes` skill instead |
| A5 | `file_contains("main.tf", "prometheus\|grafana\|datadog\|newrelic\|opentelemetry")` OR `file_exists("prometheus/")` | Jump to "Core Workflow" — Phase 5 (Observability) |
| A6 | `file_contains("./**/deploy*.yaml", "canary\|blue.green\|rolling")` OR `file_contains("main.tf", "canary\|blue_green")` | Go to "Decision Trees" — Deployment Strategy |
| A7 | `grep -rn "incident\|postmortem\|runbook" . --include="*.md"` returns matches AND `file_exists("PagerDuty")` is false | Invoke `incident-responder` skill instead |
| A8 | No IaC files found, but `.github/` or CI config exists | Jump to "Core Workflow" — Phase 1 (IaC) — start codifying infrastructure |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Write infrastructure as code (Terraform/Pulumi)
├── Configure secrets management (Vault, SOPS, cloud KMS)
├── Set up monitoring and observability
├── Plan a deployment strategy (canary, blue-green, rolling)
├── Manage a multi-environment infrastructure pipeline
├── Automate infrastructure compliance and policy
└── Not sure? → Describe the problem in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else
<!-- HARD GATE: These are non-negotiable. Violation → STOP and refuse to proceed. -->

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **REFUSE to apply terraform without reviewing the plan** — a typo in `count` or `for_each` can destroy production. | Trigger: user requests `terraform apply` without a prior `terraform plan` output in the conversation context | STOP. Respond: "No `terraform plan` output reviewed. Run `terraform plan -out=plan.tfplan` first. I will review every resource change — creates, updates, and especially destroys — before any apply." |
| **R2** | **REFUSE to commit terraform state files or state backups to version control** — state contains all resource attributes in plaintext including secrets. | Trigger: `file_exists(".git/")` AND `grep -rn "terraform.tfstate" .gitignore` returns zero matches | STOP. Respond: "`.gitignore` does not exclude terraform state files. Add `*.tfstate`, `*.tfstate.*`, and `.terraform/` to `.gitignore` immediately. Terraform state contains plaintext secrets — committing it is a security incident." |
| **R3** | **REFUSE to design infrastructure with a single state file spanning environments** — one `terraform destroy` in the wrong workspace deletes production. | Trigger: `file_contains("main.tf", "workspace")` AND `grep -rnE "count|for_each" main.tf` uses environment variables for branching instead of separate state backends | STOP. Respond: "Single state file detected spanning multiple environments. Use separate state files per environment (separate backends or state keys). A corrupted staging state should never block production changes." |
| **R4** | **REFUSE to bake secrets into container images or AMIs at build time** — build-time secrets persist in image layers and are visible to anyone with registry access. | Trigger: `file_contains("Dockerfile", "ENV.*SECRET\|ENV.*PASSWORD\|ENV.*TOKEN\|ENV.*KEY")` OR `file_contains("packer*.json", "secret\|password\|token")` in plaintext | STOP. Respond: "Secret detected in [file:line] at build time. Secrets must be injected at runtime via a secrets manager (Vault, AWS Secrets Manager, External Secrets Operator). Build-time secrets persist in image layers forever." |
| **R5** | **STOP and ASK when GitOps is configured without `selfHeal: true` and `prune: true`** — manual `kubectl` changes create hidden drift that accumulates silently. | Trigger: `file_contains("argocd/", "selfHeal")` is false OR `file_contains("flux/", "prune")` is false in GitOps manifests | STOP. Ask: "GitOps detected without `selfHeal: true` and `prune: true`. Without self-heal, manual changes persist indefinitely. Without prune, orphaned resources accumulate. Enable both? (These settings are non-negotiable for production GitOps.)" |
| **R6** | **DETECT and WARN about long-lived static credentials for CI/CD** — static credentials are a single point of compromise; if leaked, attacker has permanent access. | Trigger: `grep -rnE "AWS_ACCESS_KEY_ID|AZURE_CLIENT_SECRET|GCP_SA_KEY|service.account.*key" .github/workflows/` returns matches AND OIDC is not configured | WARN: "Static cloud credentials detected in CI pipeline at [file:line]. Migrate to OIDC federation (GitHub Actions → AWS, GitLab → GCP) with short-lived tokens scoped per step. Rotate any existing static credentials immediately." |
| **R7** | **DETECT and WARN when disaster recovery exists only as documentation** — DR docs without automated testing are wishful thinking. | Trigger: `file_exists("dr-plan.md")` OR `file_exists("runbooks/")` AND `grep -rn "dr.*test\|failover.*test\|game.*day" . --include="*.md" --include="*.yml"` returns zero matches | WARN: "DR documentation exists but no automated DR tests detected. Run game days quarterly — measure RTO/RPO against targets. Docs alone never reveal: DNS changes not committed to Git, runbook steps referencing decommissioned tools, or missing cross-region IAM permissions." |

## The Expert's Mindset

DevOps is not about tools — it's about **reducing the time and friction between code written and code delivering value, safely**. The best infrastructure is boring, predictable, and uneventful. If your infrastructure is exciting, something is wrong.

### Mental Models

| Model | Description |
|---|---|
| **Infrastructure is cattle, not pets** | Every server, container, and resource must be replaceable without ceremony. If you name your servers, you're doing it wrong. If you can't terminate any instance without thinking, it's a pet. |
| **Every manual step is a future incident** | If a step requires a human to execute it, it will eventually be executed wrong, skipped, or executed by someone who doesn't understand it. Automate or eliminate. |
| **Simplicity is the ultimate sophistication** | The best infrastructure has the fewest moving parts that satisfy the requirements. Every additional service is an additional failure mode. Resist complexity that isn't buying proportionate reliability. |
| **The goal is not uptime — it's user happiness** | 99.9% uptime with happy users beats 99.999% uptime with a system so brittle nobody dares deploy on Fridays. Optimize for deployment frequency, not just availability. |

### Cognitive Biases That Cause Outages

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Overengineering bias** | Adding Kubernetes, service mesh, and GitOps for a 2-service app "just in case we scale" | Start with the simplest stack that meets current needs. Migrate when you have evidence, not fear. |
| **Automation theater** | Automating a process without understanding why it exists | Before automating, ask: "Should this process exist at all?" Automate the right thing, not the existing thing. |
| **Recency bias** | Over-weighting the last incident when designing reliability | Maintain an incident log and look at patterns over 6-12 months. The last outage may be a one-off. |
| **Normalization of deviance** | Accepting flaky deployments as normal: "It usually works on the third retry" | Treat every failure as anomalous until proven otherwise. A deployment that passes 95% of the time fails 5% of the time — that's unacceptable. |
| **Sunk cost in tooling** | Sticking with a tool because you've invested in it, even when it's the wrong fit | Every tool decision should have a "when would we migrate away?" answer. Set that threshold before adopting. |

### What Masters Know That Others Don't

- **The best infrastructure is boring.** You should be able to go on vacation and have nothing interesting happen. Excitement in infrastructure means incidents. Boredom means reliability.
- **Every alert should demand human action.** If an alert fires and the correct response is "acknowledge and close," delete the alert. Alert fatigue kills response time for real incidents.
- **MTTR (Mean Time to Recovery) matters more than MTBF (Mean Time Between Failures).** Systems will fail. Optimize for how fast you can detect, diagnose, and recover. A system that fails monthly but recovers in 30 seconds is more reliable than one that fails yearly but takes 4 hours to fix.
- **Runbooks that haven't been tested this quarter don't exist.** If you haven't executed the recovery procedure recently, it won't work when you need it. Test in production (with safety).

### When to Break Your Own Rules

- **Manual steps are acceptable in early-stage startups.** When you're shipping to 10 users, a manually-provisioned EC2 instance is fine. Automate when the manual process causes pain, not before.
- **Skip the full GitOps pipeline for internal tools.** The rigor needed for customer-facing production is not always needed for internal dashboards. Match process rigor to blast radius.

## Operating at Different Levels

DevOps skill manifests in the scope of infrastructure you own and the blast radius of your decisions.

| Level | DevOps Output Characteristics |
|---|---|
| **L1 — Apprentice** | Executes infrastructure changes from runbooks. Learns IaC, CI/CD patterns. Deploys with guidance. |
| **L2 — Practitioner** | Owns infrastructure for a service. Writes Terraform/Pulumi, builds CI/CD pipelines. Handles incidents independently. |
| **L3 — Senior** | Designs infrastructure for a product. Multi-account architecture, DR strategy, progressive delivery. Incident command. Trade-off analysis included. |
| **L4 — Staff/Principal** | Sets platform standards for the organization. "This is how all our services deploy, monitor, and recover." Infrastructure governance and FinOps strategy. |
| **L5 — Industry-level** | Creates DevOps methodologies adopted across the industry. "Here's a new approach to infrastructure reliability." |

**Usage**: Say "as an L3 DevOps engineer, design the deployment pipeline for..." Default: **L3** (product-level infrastructure, independent design).

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

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| `terraform plan` drift detected on a security group or IAM role | Investigate immediately and page on-call if the change is unauthorized. Drift on security-boundary resources often indicates a manual console change or a compromised credential. | Security group and IAM drift are the #1 indicators of misconfiguration or breach. Benign tag drift can wait; security drift cannot. |
| Argo CD reports `OutOfSync` on a production application for more than 5 minutes | Check if `selfHeal` is enabled and prune is configured. If sync is blocked by a resource conflict, resolve manually and root-cause why auto-sync failed. | Prolonged OutOfSync means the cluster's actual state diverges from Git — the entire premise of GitOps is broken. |
| Vault lease expiration rate spikes across multiple services simultaneously | Check for synchronized credential renewal — all services renewing at the same TTL boundary creates a thundering herd. Stagger renewal windows by adding jitter to each service's TTL. | Synchronous credential rotation can overwhelm Vault and cause a cascading auth failure across every service. |
| Cloud bill projected to exceed monthly budget by >20% mid-month | Run cost attribution report by tag, identify the top 3 spend drivers, and notify service owners. Check for orphaned resources (unattached EBS volumes, idle load balancers, abandoned NAT gateways). | Mid-month budget overruns don't self-correct. A $500 leak on day 10 becomes a $1,500 surprise by day 30. |
| Production deploy succeeded but error budget burn rate spiked within the rollout window | Trigger automated rollback using the deployment tool's rollback API. Do not investigate in production — roll back first, diagnose on staging. | Error budget burn during a rollout almost always correlates with the release. The safest action is rollback, then RCA. |
| A teammate runs `kubectl apply` directly on a production cluster managed by Argo CD/Flux | The manual change will be auto-reverted within the sync interval. Educate the teammate on GitOps workflow and verify `selfHeal: true` is configured. If the manual change was an emergency fix, it must be committed to Git immediately. | Manual `kubectl` on a GitOps cluster is an anti-pattern that causes confusion (who changed what?) and drift (the revert may surprise the operator). |
| Terraform state file grows beyond 100MB or `terraform plan` takes >10 minutes | Refactor state into smaller scoped workspaces — split by component (network, compute, data) or by service team. Large state files slow every plan/apply cycle and increase blast radius on state corruption. | State file bloat is a gradual degradation that silently erodes deployment velocity. A 200MB state file can turn a 30-second plan into a 10-minute blocking operation. |
| DNS TTL for critical endpoints is ≥300 seconds during a planned failover test | Reduce TTL to ≤60 seconds at least 1 TTL period before the failover window. DNS propagation delay with high TTL means clients cache stale IPs and can't reach the new endpoint during DR. | High DNS TTL is the silent killer of fast failover. A 300-second TTL means up to 5 minutes of client downtime even if your infrastructure fails over in 30 seconds. |

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

## Anti-Patterns
<!-- DEEP: 5min -- each anti-pattern includes machine-detectable patterns -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) | 🛡️ Auto-Prevent |
|-----------------|---------------------|--------------------------|-------------------|
| Running `terraform apply` from a local laptop against production state | All applies must run through CI/CD with plan posted as PR comment and human approval required | `grep -rn "terraform apply" .github/workflows/` returns zero matches AND `file_exists("main.tf")` → no CI-enforced apply, local-only risk | CI pipeline requirement: production state backend denies access except from CI service principal; `terraform apply` blocked outside CI |
| Using the same Terraform state file for staging and production with workspace switching | Use separate state files (or separate backends) per environment; `terraform destroy` in wrong workspace deletes production | `grep -rn "terraform.workspace\|workspace_key_prefix" main.tf` → workspace switching detected for env separation | `terraform validate` + CI check: if workspace switching used AND `backend` config same for prod/staging, block and require separate backends |
| Baking secrets into container images or AMIs at build time | Inject secrets at runtime via secrets manager (Vault, AWS Secrets Manager, External Secrets Operator) | `grep -rn "ENV.*SECRET\|ENV.*PASSWORD\|ENV.*TOKEN\|ENV.*KEY" Dockerfile` → finds build-time secrets in images | `hadolint` rule DL3044 + Trivy secret scan in CI blocking images with embedded credentials |
| Configuring GitOps without `selfHeal: true` and `prune: true` | Self-heal auto-reverts unauthorized changes; pruning removes resources deleted from Git | `grep -rn "selfHeal:" argocd/` shows `false` OR `grep -rn "prune:" flux/` shows `false` → disabled self-heal/prune | OPA/Gatekeeper policy: ArgoCD Application without `syncPolicy.automated.prune: true` → deny admission |
| Deploying a canary without a control group — sending 100% of traffic through the canary | Keep 10–20% of traffic on the stable version as baseline; compare canary metrics against live control group | `grep -rn "canary\|canaryWeight" k8s/` AND `grep -rn "stableWeight" k8s/` shows `canaryWeight: 100` → no control group | Argo Rollouts analysis template requiring `stableWeight > 0` for canary steps; CI validation of rollout manifests |
| Treating disaster recovery as a document that gets updated once a year | Run automated DR tests on schedule (monthly for tier-1); measure RTO/RPO against targets; game days expose gaps | `file_exists("dr-plan.md")` AND `grep -rn "dr.*test\|failover.*test\|game.*day" .github/workflows/` returns zero matches → DR doc without testing | Scheduled GitHub Actions workflow running DR failover test monthly; failed DR test → PagerDuty alert |
| Using long-lived static credentials for CI/CD pipelines instead of OIDC federation | Use OIDC federation (GitHub Actions → AWS, GitLab → GCP) with short-lived tokens scoped to each pipeline step | `grep -rnE "AWS_ACCESS_KEY_ID\|AZURE_CLIENT_SECRET\|GCP_SA_KEY" .github/workflows/` returns matches → static credentials in CI | `trufflehog` CI scan blocking static cloud credentials; repo-level OIDC configuration required for production environments |

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


## Error Decoder
<!-- DEEP: 5min -- each entry includes a console-string matcher for automatic recovery loops -->

| 🖥️ Console Match (grep pattern) | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| `grep -rn "DATABASE_URL\|DB_URL" . --include="*.tf" --include="*.env*" && grep -rn "DATABASE_URL\|DB_URL" app/ --include="*.ts" --include="*.js"` shows naming mismatch | Staging tests pass — production deploy fails with database connection error | Staging used t3.micro RDS (100 max connections); production used db.r6g.xlarge (1000 connections); app connection pool configured for staging's limit | Never hardcode environment-specific values; all env-specific config from environment variables; use same config structure across environments — only values differ | 1. Audit all env vars: `grep -rn "process\.env\." app/` 2. Compare staging vs production values 3. Standardize naming with `.env.example` as source of truth 4. Add CI validation that env var schema matches across environments |
| `grep -rn "DATABASE_URL" app/ && grep -rn "DB_URL" main.tf` returns both but no shared schema doc | Deployment broke because app expected `DATABASE_URL` but IaC exported `DB_URL` | Env vars defined by two different teams (app and infra) with no shared naming convention | Define shared env var schema that both teams agree on; publish as doc and validate in CI; use `.env.example` as single source of truth for variable names | 1. `grep -rn "process\.env\." app/ -o | sort -u` to list all env vars 2. Cross-reference with IaC exports 3. Create `.env.example` with documented naming 4. Add CI check: `diff <(grep -oP 'process\.env\.\K\w+' app/) <(grep -oP 'export \K\w+' main.tf)` |
| `grep -rn "terraform destroy" shell-history.txt 2>/dev/null && ls terraform.tfstate.d/` shows `prod/` directory | Terraform destroy accidentally deleted production RDS instance | Developer ran `terraform destroy` in what they thought was staging workspace; workspace selector was set to `prod` from previous session | Separate AWS accounts per environment with SCPs blocking cross-account access; enable deletion protection on all production databases; require MFA for destroy ops; never use same state file for multiple environments | 1. `aws rds modify-db-instance --deletion-protection` to enable 2. `terraform state list \| wc -l` to check blast radius 3. Split state per environment 4. Require MFA + approval for destroy in CI |
| `grep -rn "stableWeight: 0\|canaryWeight: 100" k8s/ --include="*.yaml"` returns matches | Canary analysis showed no errors — 5 minutes after full rollout, all requests failing | Canary configured with 100% traffic during testing so there was no "stable" baseline; analysis compared canary against itself | Keep 10-20% of traffic on old version during analysis window; use statistical significance testing, not simple threshold comparison; canary without a control group is a risky rollout with monitoring | 1. Set `stableWeight: 20` and `canaryWeight: 20` in rollout manifest 2. Add analysis template with t-test on error rate 3. Verify two separate metric streams (canary vs stable) 4. Re-run canary deployment |
| `grep -rn "vault\|Vault" main.tf && vault read -format=json sys/leases | jq '.data.leases | length'` shows zero active leases | Vault dynamic credentials stopped working — all services lost database access simultaneously | Vault database secret engine TTL was 1 hour with max lease TTL of 1 hour; all credentials expired simultaneously and every app tried to renew at the same time, overwhelming Vault | Set renewal TTL to stagger across services (not all at T-0); add buffer period (renew at 50% of TTL, not 100%); tune Vault rate limiting for peak renewal load; monitor lease expiration rate | 1. Set `ttl: 4h` and `max_ttl: 24h` with staggered `issue_time` 2. Renew at 50% TTL: `vault lease renew -increment=2h` 3. Monitor `vault.lease.expiration.count` metric 4. Load test renewal at peak scale |
| `terraform plan -out=plan.tfplan 2>&1 | grep "0 to add, 0 to change, 0 to destroy"` BUT `kubectl get all -o yaml | diff - <(helm template .)` shows drift | Infrastructure drift — what's running in production doesn't match Terraform state or Git | Manual `kubectl` changes made by on-call engineer to fix an incident were never codified back into IaC | GitOps with `selfHeal: true` to auto-revert manual changes; detect drift with `terraform plan -detailed-exitcode` on schedule; require all changes through IaC PRs | 1. `terraform plan -detailed-exitcode` (exit 2 = drift) 2. `terraform state list` and diff against Git 3. Import manual changes or revert 4. Enable GitOps self-heal: `selfHeal: true` in ArgoCD |


## What Good Looks Like

> Infrastructure is fully codified, versioned, and reproducible — nothing is created by hand and nothing drifts. Deployments are zero-downtime with automated rollback on health check failure. Secrets are never in plaintext, never in environment variables, and always retrieved at runtime from a secrets manager. Monitoring, alerting, and logging are standardized across every service. The developer experience from commit to production is seamless: a single command provisions, deploys, and verifies. Mean time to recovery is measured in minutes, not hours, because every failure has a runbook.

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Remote state with encryption at rest + locking (S3+DynamoDB, GCS, Azure Blob) | `grep -rn "backend\s*\"s3\"\|backend\s*\"gcs\"\|backend\s*\"azurerm\"" main.tf \| wc -l` → ≥ 1 AND `grep -rn "encrypt\s*=\s*true\|dynamodb_table" main.tf \| wc -l` → ≥ 1 | Add S3 backend with `encrypt = true` + `dynamodb_table` for locking |
| **[S2]** | State per environment per component (blast radius isolation) | `grep -rn "key\s*=\s*.*env\|workspace_key_prefix" main.tf \| wc -l` → ≥ 1 | Separate state keys: `states/prod/networking/terraform.tfstate` |
| **[S3]** | All modules pinned by immutable git tag or commit SHA | `grep -rn "source\s*=\s*\"git::" main.tf \| grep -c "ref="` → equals total module count | Replace branch refs with `?ref=v1.2.3` or commit SHA |
| **[S4]** | Provider versions pinned (`~>` pessimistic constraint) | `grep -rn "required_providers" main.tf -A 10 \| grep "version" \| grep -c "~>"` → equals provider count | Add `version = "~> 5.0"` to each required_provider |
| **[S5]** | `terraform fmt -check` + `terraform validate` enforced in CI | `grep -rn "terraform fmt\|terraform validate" .github/workflows/ \| wc -l` → ≥ 2 | Add `terraform fmt -check -recursive` and `terraform validate` to CI |
| **[S6]** | Speculative plan posted as PR comment; apply requires human approval | `grep -rn "terraform plan" .github/workflows/ \| wc -l` → ≥ 1 AND `grep -rn "environment.*production" .github/workflows/ \| wc -l` → ≥ 1 | Add plan-to-PR-comment action + production environment protection |
| **[S7]** | Argo CD/Flux deployed and managing all Kubernetes resources | `kubectl get pods -n argocd \| grep argocd \| wc -l` → ≥ 1 OR `kubectl get pods -n flux-system \| wc -l` → ≥ 1 | `helm install argocd argo/argo-cd` |
| **[S8]** | `selfHeal: true` and `prune: true` for production applications | `grep -rn "selfHeal:\s*true" argocd/ \| wc -l` → ≥ 1 AND `grep -rn "prune:\s*true" argocd/ \| wc -l` → ≥ 1 | Set `syncPolicy.automated.selfHeal: true` and `prune: true` |
| **[S9]** | SSO (OIDC) enabled; RBAC configured per team | `grep -rn "oidc\|dex" argocd/ \| wc -l` → ≥ 1 | Configure ArgoCD SSO with OIDC provider |
| **[S10]** | Progressive delivery configured (Argo Rollouts or Flagger) with automated analysis | `kubectl get pods -n argo-rollouts \| wc -l` → ≥ 1 OR `kubectl get pods -n flagger-system \| wc -l` → ≥ 1 | `helm install argo-rollouts argo/argo-rollouts` |
| **[S11]** | No plaintext secrets in Git, `.tfvars`, or Kubernetes manifests | `grep -rnE "(password\|secret\|token\|key)\s*=\s*\"[^\"]{8,}\"" . --include="*.tfvars" --include="*.yaml" \| wc -l` → 0 | Run `trufflehog filesystem .` and rotate any found secrets |
| **[S12]** | External Secrets Operator syncing from cloud secret manager | `kubectl get pods -n external-secrets \| wc -l` → ≥ 1 | `helm install external-secrets external-secrets/external-secrets` |
| **[S13]** | SLOs defined for all critical user journeys with error budgets | `grep -rn "SLO\|error_budget\|sloth\|pyrra" . --include="*.yaml" --include="*.tf" \| wc -l` → ≥ 1 | Generate SLO manifest with `sloth` or `pyrra` |
| **[S14]** | 3-2-1 backup rule applied to all Tier 0-2 data stores | `grep -rn "backup_vault\|backup_plan\|backup_retention" main.tf \| wc -l` → ≥ 1 AND at least 3 copies configured | Add `aws_backup_plan` with cross-region + cross-account copies |
| **[S15]** | DR test conducted within last quarter; postmortem action items tracked | `grep -rn "dr.*test\|game.*day\|failover.*test" .github/workflows/ \| wc -l` → ≥ 1 AND `find . -name "postmortem*" -mtime -90 \| wc -l` → ≥ 1 | Schedule quarterly DR test workflow + postmortem template |

## Footguns
<!-- DEEP: 10+min — war stories from production infrastructure -->

| Footgun | What Happened | Root Cause | How to Prevent |
|---------|---------------|------------|----------------|
| Terraform destroyed production database because state was shared across environments, and a `terraform apply` meant for staging ran against prod | A developer ran `terraform apply` in the staging directory, but the Terraform backend was configured identically for both staging and production. The state file was in the same S3 bucket with the same key prefix. The `count` parameter change in a module triggered a destroy-and-recreate of the RDS instance — in production, at 2:00 PM on a Tuesday. Recovery from snapshot took 4 hours. | State isolation was configured by directory convention, not enforced. Both environments used `bucket = "company-terraform-state"` and `key = "infra/terraform.tfstate"`. No workspace separation, no different state keys per environment. | **Isolate state per environment at the infrastructure level** — separate S3 buckets or separate keys: `env:/staging/terraform.tfstate` vs `env:/production/terraform.tfstate`. Use Terraform workspaces OR separate backend configs per environment, not both. Add `prevent_destroy = true` lifecycle rule on stateful resources (RDS, S3, DynamoDB). Run `terraform plan` and POST it as a PR comment — require human approval for plans that include destroys. |
| Argo CD auto-sync nuked a manually patched production config — the patch was a hotfix applied at 3:00 AM that nobody committed to Git | On-call engineer fixed a P0 by changing a Kubernetes ConfigMap via `kubectl edit` at 3:00 AM. Argo CD's self-healing (default: 3-minute reconciliation) detected the drift and reverted to the Git version — which had the bug. The incident reopened 3 minutes later. The engineer patched it again. Argo CD reverted it again. This loop continued for 40 minutes before someone disabled auto-sync. | `selfHeal: true` + manual kubectl edits = infinite loop. The on-call engineer didn't know the cluster was GitOps-managed. The runbook said "edit the ConfigMap" but was written before Argo CD was deployed. | **If using GitOps, NEVER manually edit cluster resources.** All changes must flow through Git. If you need an emergency hotfix, either: (a) commit + push to Git and let Argo CD sync, or (b) disable auto-sync temporarily with `argocd app set myapp --sync-policy none`, apply the hotfix, then re-enable. Update runbooks to include the GitOps workflow. Add a PagerDuty note: "This cluster is GitOps-managed. Do not kubectl edit. Push to Git or disable sync." |
| Vault seal triggered at 3:00 AM when the auto-unseal KMS key accidentally rotated — all services lost database credentials, 2-hour outage | HashiCorp Vault was configured with AWS KMS auto-unseal. The security team rotated the KMS key as part of a quarterly key rotation policy. Vault sealed because it couldn't decrypt its master key with the old KMS key version that was scheduled for deletion. Every service using dynamic database credentials lost access simultaneously. | The KMS key rotation policy was applied to ALL keys, including the Vault unseal key, without an exception. The KMS key had automatic key rotation enabled — when rotation happened, Vault's reference to the old key version broke because the new key couldn't decrypt data encrypted by the old key. | **Never auto-rotate the KMS key used for Vault auto-unseal.** This key is special — it encrypts Vault's master key and must be available in all versions. Tag it: `vault:unseal:do-not-rotate`. If you must rotate, manually re-wrap the master key with the new KMS key version using `vault operator rekey`. Test Vault unseal recovery quarterly — bring up a fresh Vault instance and verify it can unseal. |
| DNS failover didn't work during a real region failure because TTL was 86400 — the old IP was cached in ISP resolvers, CDNs, and client DNS caches worldwide | A planned region failover test passed because the team cleared DNS caches before testing. During an actual AWS us-east-1 outage, they flipped the DNS record to point to us-west-2. The old record was cached with a 24-hour TTL at thousands of ISP resolvers across the globe. Users in Australia still resolved to the dead region 18 hours later. | The test was not realistic — they assumed DNS propagates instantly. It doesn't. ISP resolvers, CDN edge caches, browser DNS caches, and OS-level caches all respect TTL independently. A 24h TTL means the worst-case propagation is 24 hours. | **Set DNS TTL ≤ 60 seconds for critical endpoints.** This is the single highest-leverage change for disaster recovery. Use health-check-based failover (Route 53 failover records, Azure Traffic Manager, GCP Cloud DNS routing policies). Test failover WITHOUT clearing caches — use a geographically distributed monitoring service (Pingdom, Catchpoint) to verify that real users in multiple regions actually see the new IP. |
| Terraform plan showed 0 changes but `terraform apply` destroyed and recreated 200 security group rules — took down every service for 45 minutes | A developer refactored security group rules from inline `ingress`/`egress` blocks to standalone `aws_security_group_rule` resources. The Terraform plan showed "0 to add, 0 to change, 0 to destroy" because the resulting configuration was equivalent. But the apply deleted the inline rules (which removed all security group permissions) before creating the standalone rules. For 90 seconds, every security group had zero inbound rules — all services were unreachable. Recovery required manually adding back rules via AWS console. | Terraform's plan only shows net changes to resources, not the ordering of destructive operations within a resource update. Migrating inline rules to standalone resources requires `create_before_destroy = true` lifecycle rule, which Terraform doesn't enforce by default. | **Always run `terraform plan` with `-detailed-exitcode` in CI and have a human review plans that show ANY changes to security groups, IAM, or network ACLs.** For security group refactors, use `terraform state mv` to migrate resources without destroy/create cycles. Add `lifecycle { create_before_destroy = true }` on security groups. Test security group changes in a staging environment with actual traffic flowing before applying to production. |

## Calibration — How to Know Your Level
<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You `kubectl edit` or click in the AWS console to make changes | All infrastructure changes flow through Git → CI → apply. You haven't touched a cloud console in 6 months | You design the platform other teams use — they don't know what Terraform or Kubernetes are, they just push code and it deploys |
| You run `terraform apply` from your laptop and hope it works | Your CI pipeline runs `terraform plan` on every PR and posts the diff as a comment. Apply requires human approval | You've reduced the mean time from commit to production from 2 hours to 8 minutes, and you can prove it with DORA metrics |
| You discover that a secret is in plaintext by accident — during a code review or security scan | Secrets are managed by Vault/SOPS/External Secrets Operator. A pre-commit hook blocks any commit with an AWS key pattern or `password =` | You've designed a secret rotation system that automatically rotates database credentials every 30 days with zero application downtime |

**The Litmus Test:** Can you recover from a complete region failure — DNS flip, database failover, application redeployment — in under 15 minutes without a runbook? If you need a runbook, your system isn't resilient enough. If the runbook is wrong, you find out during the incident.

## Deliberate Practice

DevOps skill is built in the crucible of failure — incident response, recovery drills, and chaos engineering. The engineer who has recovered from 50 failures is calm during the 51st.

### The DevOps Improvement Loop

```
BUILD → BREAK → FIX → AUTOMATE PREVENTION → repeat
```

After every incident: the blameless post-mortem is your training data. Don't just fix the root cause — ask: "What would have caught this earlier? A test? An alert? A design review?" Close the class of failure, not just the specific instance.

### Practice Routines by Skill Level

| Level | Practice | Frequency |
|---|---|---|
| **Novice** | Reproduce a production incident in a staging environment. Fix it. Document the steps. Now have someone else follow your runbook while you watch silently. | Monthly |
| **Competent** | Write a runbook for a service you own. Have a teammate execute it cold (no help from you). Time them. Every question they ask is a gap in your runbook. | Quarterly |
| **Expert** | Simulate a full region failure: cut off all traffic to one region. Time recovery end-to-end. Write up findings: what failed in your failover process? What surprised you? | Quarterly |
| **Master** | Design a chaos experiment for production: what happens when a critical dependency has 5s latency? Run it during business hours (with safeguards). Write up findings. | Monthly |

### The One Highest-Leverage Activity

**Do a "walk the floor" tour of your infrastructure monthly.** Pick a random service. Can you find its: runbook? dashboards? recent deployment history? on-call rotation? If any of these takes more than 60 seconds, that's your next improvement.

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
