---
name: devops-engineer
description: >
  Use when implementing Infrastructure as Code, designing GitOps workflows, managing
  secrets and configuration, planning disaster recovery, or automating deployment
  pipelines. Handles Terraform and Pulumi IaC patterns, GitOps with Argo CD, secret
  management (Vault, external-secrets), progressive delivery (canary, blue-green,
  feature flags), cost optimization, and disaster recovery planning. Do NOT use for
  cloud architecture design, CI/CD pipeline authoring, Kubernetes manifests, or
  observability instrumentation.
license: MIT
tags:
- devops
- iac
- terraform
- gitops
- deployment
- secrets
- disaster-recovery
- finops
author: Sandeep Kumar Penchala
type: devops
status: stable
version: 1.1.0
updated: 2026-07-23
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
---

# DevOps Engineer
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

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

> See [references/core-workflow.md](references/core-workflow.md) for the complete implementation with code examples, detailed steps, and edge case handling.

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

## What Good Looks Like

> Infrastructure is fully codified, versioned, and reproducible — nothing is created by hand and nothing drifts. Deployments are zero-downtime with automated rollback on health check failure.

> See [references/what-good-looks-like.md](references/what-good-looks-like.md) for the full quality standard.


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

## Gotchas

- **Terraform `count` vs `for_each`**: When you remove an item from the MIDDLE of a count-based list, Terraform shifts all subsequent resource indices. The resource at index 3 gets destroyed and recreated as index 2 — potentially destructive. `for_each` with stable keys prevents index shifting.
- **Terraform state file** in S3 with DynamoDB locking — if the DynamoDB table is in a different region and that region has an outage, ALL Terraform operations fail with "Error acquiring state lock." Co-locate the lock table with the state bucket.
- **`terraform plan -out`** saves the plan at planning time, but the plan is a snapshot of the state at that moment. If another CI pipeline applies changes between your plan and apply, the apply fails with "state has changed" — but the failure message doesn't tell you what changed.
- **Kubernetes `imagePullPolicy: Always`** re-pulls the image every pod start, including restarts. During a registry outage, pods can't restart. Use `IfNotPresent` with digest-based tags (e.g., `myapp@sha256:...`) for production.
- **Helm's `--wait` flag** waits for pods to be "Ready" but doesn't check for CrashLoopBackOff — a pod that starts, crashes, restarts, crashes, restarting forever is "Ready" between crashes. Helm reports success on a failing deployment.
- **Secret management**: `kubectl get secret -o yaml` reveals base64-encoded (NOT encrypted) secrets. Anyone with `get secret` permissions can decode them. Use External Secrets Operator or Sealed Secrets, never store plain secrets in Kubernetes Secret objects.


## Verification

- [ ] Run `terraform validate` — configuration is valid
- [ ] Run `terraform plan` — plan is clean (no unexpected creates/destroys)
- [ ] Run `checkov` or `tfsec` on Terraform — zero high/critical findings
- [ ] Verify state locking: run `terraform plan` in two terminals simultaneously — second one waits for lock, doesn't corrupt state
- [ ] Secrets check: `tfsec` or `detect-secrets` confirms no plaintext secrets in configs
- [ ] Deploy to staging, verify health, then promote to production — GitOps workflow is end-to-end functional


## References

Detailed reference material loaded on demand:

- **Core Workflow — Full Implementation**: See [core-workflow.md](references/core-workflow.md)
- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)
- **Calibration — How to Know Your Level**: See [calibration.md](references/calibration.md)
- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Infrastructure Cost per User at Scale**: See [cost-per-user.md](references/cost-per-user.md)
- **Error Decoder**: See [error-decoder.md](references/error-decoder.md)
- **Footguns**: See [footguns.md](references/footguns.md)
- **When Managed Services Save Money**: See [managed-services.md](references/managed-services.md)
- **Scale Depth: Solo → Small → Medium → Enterprise**: See [scale-depth.md](references/scale-depth.md)
- **Self-Hosting Breakeven Calculator**: See [self-hosting.md](references/self-hosting.md)
- **Sub-Skills**: See [sub-skills.md](references/sub-skills.md)

