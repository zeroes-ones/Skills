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

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "I'll update Terraform after this manual fix — it's an emergency." | That "emergency fix" in the AWS console is now permanent drift. The next `terraform apply` reverts it back, re-triggering the same outage during peak traffic when customer impact is 10x higher. Cost: $50K-$200K per drift-related incident. |
| "We'll write the rollback plan after the deploy ships." | The migration that took 2 minutes on staging takes 40 minutes on production data, locks the table, and takes down checkout. Nobody knows the rollback because the `down` method was never written. Cost: $90K-$400K in lost revenue from weekend downtime. |
| "DR docs are good enough — we'll test failover when we have time." | Runbooks reference decommissioned tools. DNS changes were never committed to Git. Cross-region IAM permissions don't exist. When you actually need DR, it will fail. Untested DR is not DR — it's wishful thinking in a markdown file. |
| "Static credentials are fine — it's an internal dev tool." | That IAM key with AdministratorAccess gets scraped from a public repo fork in 4 minutes by automated tooling. Cost: $80K-$250K in crypto mining fraud, SOC 2 audit failure, and mandatory customer notification from one leaked key. |
| "We don't need OIDC — managing long-lived IAM users is simpler." | Long-lived credentials are a single point of compromise. If leaked, attacker has permanent access until you notice and rotate — average detection time: 207 days. OIDC gives you short-lived tokens scoped per step. Simplicity today is a breach tomorrow. |

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
| **R8** | **NEVER guess infrastructure tool versions — anchor to the runtime.** Terraform providers, Kubernetes API versions, Docker engine, and Helm chart API versions change between releases. Generating code against the wrong version produces broken manifests. | Trigger: writing Terraform HCL, Helm charts, Kubernetes manifests, or Dockerfiles without first running `scripts/runtime-version-detect.sh` on the target project | STOP. Run: `scripts/runtime-version-detect.sh`. Then VERIFY: terraform version (`terraform version`), kubectl server version (`kubectl version --short`), docker version (`docker version --format '{{.Server.Version}}'`), helm version (`helm version --short`). Prepend to output: "## 🔗 Anchored Versions (source: runtime-version-detect.sh)\n- Terraform: X.Y.Z (state snapshot version: A.B)\n- Kubernetes API: v1.XX\n- Helm: vX.Y.Z\n- Docker Engine: XX.Y.Z" |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
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

### Scale Depth

### Solo (1 person, 0-100 users)
- **What changes**: DevOps = PaaS (Vercel/Railway/Render). No IaC. No containers. No CI/CD pipeline. Manual `git push` deploy. Monitoring = built-in PaaS dashboard. Secrets in platform env vars.
- **What to skip**: Terraform/Pulumi, Docker, Kubernetes, CI/CD pipelines, GitOps, observability stack (Prometheus/Grafana), secrets management (Vault), infrastructure monitoring.
- **Coordination**: You are ops + dev. No coordination needed. **Cost**: $0-100/month.

### Small Team (2-10 people, 100-10K users)
- **What changes**: IaC for infrastructure (Terraform). Docker for consistent environments. CI/CD with test + deploy. Managed services for database, cache, queue. Basic monitoring (logs + uptime + basic metrics). Secrets in CI/CD secrets manager. Staging environment.
- **What to skip**: Kubernetes, GitOps, service mesh, full observability (just logs + uptime + basic metrics), multi-region, self-hosted anything.
- **Coordination**: DevOps tasks shared among developers. Weekly infra review. PagerDuty for production alerts (rotating). **Cost**: $200-1,000/month.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Dedicated DevOps/SRE (1-2 people). Kubernetes or ECS. GitOps (Argo CD/Flux). Full observability (Prometheus + Grafana + Loki + Tempo). IaC per environment with state isolation. Secrets management (Vault or cloud KMS). CI/CD with security scanning. Auto-scaling. Blue-green deployments. SLOs defined.
- **What to skip**: Multi-cloud, service mesh, chaos engineering, dedicated platform team.
- **Coordination**: DevOps weekly planning. Monthly infrastructure review. On-call rotation (follow-the-sun if needed). **Cost**: $5,000-20,000/month.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Platform engineering team (3+ engineers). Internal developer platform (Backstage). Multi-cloud infrastructure. Service mesh (Istio/Linkerd). Full GitOps. Secrets management with rotation. Chaos engineering. Multi-region active-active. SLOs with error budgets. FinOps practice. Compliance automation. Capacity planning.
- **What's full production**: Developer platform as a product. Self-service infrastructure. Automated compliance. Cost optimization dashboard. Platform engineering metrics (DORA + platform adoption).
- **Coordination**: Platform team weekly. Monthly infrastructure review. Quarterly capacity planning. On-call with escalation paths. **Cost**: $50,000-200,000+/month.

### Transition Triggers
- **Solo → Small**: Second developer joins. PaaS limitations hit (cost or features).
- **Small → Medium**: 3+ services. Manual deploys causing issues. First production incident at 3 AM.
- **Medium → Enterprise**: 10+ services with cross-team ownership. Multi-region or compliance required. >50 engineers.

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

## Decision Trees **(QUICK)**

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

## Core Workflow **(STANDARD)**

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 1 (~15 min): Discovery & Infrastructure Audit
1. **Inventory & Classification** — Catalog every resource across accounts/projects. Identify snowflake servers, untagged resources, and resources not managed by IaC. Use `aws resourcegroupstaggingapi`, `gcloud asset search-all-resources`, or cloud asset inventory tools.
2. **Architecture Mapping** — Diagram network topology (VPC peering, transit gateway, PrivateLink), data flows, and service dependencies. Document environment topology: dev → staging → UAT → production → DR.
3. **Maturity Assessment** — Evaluate IaC coverage (%), CI/CD adoption, observability posture, incident response process. Score 1-5 on each DORA capability.
4. **Security & Compliance Constraints** — Map regulatory requirements (SOC2, HIPAA, PCI-DSS, GDPR) to infrastructure controls: network segmentation, encryption requirements, data residency, audit logging.
  Complete when: complete resource inventory is cataloged across all accounts, network topology diagram is documented, DORA maturity score is assessed, and regulatory control mapping is complete.

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
  Complete when: Terraform/Pulumi/CDK tool selection is documented with trade-offs, repository structure follows bounded-context separation, remote state is configured with encryption and locking, and modules are versioned by git tag.


## Gotchas

| Gotcha | Cost | Fix |
|--------|------|-----|
| Running `terraform apply` directly from a laptop without remote state locking — two engineers apply simultaneously, corrupting the state file and leaving infrastructure in an unrecoverable split-brain state | $50K-$200K in infrastructure recovery and downtime | Always use remote state with DynamoDB (AWS) or GCS (GCP) locking; never run applies from local machines for shared state; CI/CD is the only path to production applies |
| Hardcoding secrets in `.tfvars` files committed to git — the secret is now in the git history forever, accessible to anyone with repo access; rotation requires rewriting git history | $20K-$100K in secret rotation, incident response, and potential compliance violations | Use `data` sources to fetch secrets at plan time (AWS Secrets Manager, Vault); mark all secret variables with `sensitive = true`; add `.tfvars` to `.gitignore` and use CI-injected variables instead |
| Refactoring a Terraform module without incrementing the version — 14 downstream environments pick up the breaking change on their next `terraform init -upgrade` and all fail to plan | $30K-$150K in cascading plan failures across the org | Always tag module releases with semantic versions; downstream consumers pin to a specific version, not `main`; run `terraform plan` in a canary environment before rolling out module updates broadly |
| Destroying infrastructure with `terraform destroy` without checking `prevent_destroy` lifecycle rules — the production database is deleted because the RDS module didn't have deletion protection enabled | $100K-$500K in data loss and recovery | Enable `prevent_destroy = true` on all stateful resources (RDS, S3 buckets, DynamoDB tables); add `deletion_protection = true` at the cloud provider level; require manual approval for any destroy plan targeting production |


## Error Decoder — War Stories from the Trenches

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| `terraform plan` shows no changes but `terraform apply` destroys and recreates a stateful resource | Someone renamed the resource in Terraform without using `moved` blocks. Terraform sees the old name as "deleted" and the new name as "created" — plan shows `0 to add, 1 to change, 0 to destroy` because of a provider bug with `create_before_destroy` lifecycle rules on immutable attributes | Always use `terraform state mv` or `moved` blocks when renaming resources. Run `terraform plan -refresh-only` before apply to see what Terraform thinks exists vs what actually exists. Add `prevent_destroy = true` on stateful resources (databases, volumes, DNS zones) | Terraform's plan lies when lifecycle rules and renames intersect. `moved` blocks are not optional — they're the only safe way to rename. `prevent_destroy` on stateful resources catches accidental deletion before it reaches the provider. |
| Argo CD reports "Synced" and "Healthy" but the pod is running an image from 3 days ago | The Git commit SHA in the manifest matches, but the image tag is `:latest` and the container runtime pulled a new image. Argo CD's self-heal sees the manifest hasn't changed — no diff to reconcile. The running image is different from what was tested | Pin image tags by SHA256 digest in all GitOps manifests. Set `imagePullPolicy: Always` and a `status.imageID` annotation check in Argo CD's diff customization. Use a mutation webhook (Kyverno/OPA) that rejects any pod spec with `:latest` tag in production namespaces | GitOps reconciles manifests, not running state. `:latest` creates a gap between "what Git says" and "what's actually running." The only safe pointer is a content-addressable digest. |
| Vault dynamic database credentials work for 4 hours then every service gets `Access denied for user` | Vault's default lease TTL is 768 hours, but the MySQL `wait_timeout` is 28800 seconds (8 hours). The database kills idle connections while Vault thinks the credential is still valid. Services with connection pools hold connections past idle timeout but Vault doesn't rotate the credential | Set database `wait_timeout` to 2× Vault's lease TTL or set Vault TTL to ≤ database timeout ÷ 2. Use `vault agent` with auto-auth and template rendering to rotate credentials client-side. Implement connection pool health checks that validate credentials on borrow | Vault manages credential lifecycle but doesn't know about database session lifecycle. Lease TTL and database timeout must be coordinated — or Vault will issue credentials to dead sessions. |
| Terraform state lock in DynamoDB won't release — every pipeline is blocked with `Error acquiring the state lock` | A `terraform apply` was force-killed mid-execution. The process couldn't release the DynamoDB lock. The lock entry's TTL was never set because the put and delete happen in the same API call. The lock persists forever | Set `dynamodb_table` with `server_side_encryption` and `point_in_time_recovery`. Add a `force-unlock` runbook: `terraform force-unlock <LOCK_ID>`. Implement a Lambda that scans for locks older than 2× the max pipeline timeout and deletes them. Add `-lock-timeout=30m` to all CI terraform commands | DynamoDB state locks are advisory, not transactional. No process = no release. Always pair distributed locks with a timeout-based unlocker — a stuck CI runner becomes a global deployment freeze. |
| Pulumi preview succeeds but `pulumi up` fails mid-deploy — resources partially created with no rollback | Pulumi creates 5 resources in dependency order. Resource 3 fails on a validation error (name too long for AWS API). Resources 1 and 2 are created and stay created. There's no atomic rollback — you now have orphaned resources | Use `pulumi up --target` for high-risk resource groups. Wrap resource creation in `pulumi.all([])` with explicit `dependsOn` to make groups fail atomically. Run `pulumi destroy --target <URN>` for orphan cleanup. Pre-validate with CloudFormation Guard or OPA policies before pulumi up | Pulumi (and Terraform) are eventually consistent — they don't roll back on partial failure. The provider creates what it can, fails on what it can't. Always have a cleanup plan for partial deployments. |
| HashiCorp Vault sealed itself during a routine node restart and no one had the unseal keys | Vault was deployed on a single node with auto-unseal via cloud KMS, but the IAM role for KMS access was on an EC2 instance profile that was accidentally detached during a security group audit. The standby node couldn't auto-unseal because it had the same detached profile | Use `recovery_keys` with Shamir's Secret Sharing, store at least 3 key shares across 3 different custody holders in separate physical locations. Test the unseal procedure quarterly — timed and documented. Deploy Vault in HA with 3 nodes across 3 AZs, each with independent KMS access via resource-based policy | Auto-unseal is a single point of failure if all nodes share the same KMS authentication. The unseal procedure isn't tested until it's needed — and by then, the keys are unreachable. HA + independent auth paths + regular unseal drills. |


## Best Practices

1. **Codify everything — no ClickOps.** Every resource from VPC to DNS record lives in Terraform/Pulumi/Crossplane. Manual console changes must be synced to IaC within 24 hours or auto-reverted by drift detection.
2. **Use remote state with locking.** Store Terraform state in S3/GCS/Azure Storage with DynamoDB/Blob lease locking. Never commit state files to Git. Co-locate the lock mechanism with the state bucket.
3. **Isolate blast radius via state separation.** Split Terraform state by environment (`prod`, `staging`, `dev`) and by concern (`network`, `compute`, `data`). A corrupted staging state should never block production changes.
4. **GitOps is the reconciliation loop, not the deploy trigger.** Argo CD/Flux continuously reconcile cluster state with Git. Manual `kubectl apply` on a GitOps cluster must be treated as an incident — it creates drift that auto-heal will revert.
5. **Enforce environment promotion gates.** Artifacts flow `dev → staging → prod`, never directly to prod. Staging runs production-data-mirrored integration tests. No cherry-pick to production without passing staging first.
6. **Secrets never touch disk or Git.** Use Vault dynamic secrets, External Secrets Operator, or cloud KMS with short-lived tokens. Rotate credentials on a schedule — static credentials longer than 90 days are a finding.
7. **Progressive delivery limits blast radius.** 5% canary → 25% → 100% with automated metric comparison. If canary shows >2× error rate, halt and rollback automatically. Blue-green for instant rollback when infrastructure budget allows 2× capacity.
8. **Monitoring from the user's perspective.** Measure P95/P99 latency at the edge (CDN/ALB), not at the load balancer. SLO burn-rate alerts fire before the error budget exhausts. Synthetic probes test the full user journey every 60 seconds.
9. **Immutable infrastructure — never patch in place.** Replace AMIs, container images, and server configs; don't SSH in to fix. Immutability eliminates configuration drift and snowflake servers, and makes rollback a redeploy of the previous artifact.
10. **Run disaster recovery drills, not just DR plans.** Quarterly failover to DR region with production traffic. Measure RPO (actual data freshness) and RTO (time to fully operational). A DR plan that hasn't been tested in 6 months doesn't exist.


## Error Recovery **(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

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


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## Production Checklist **(STANDARD)**

1. [ ] **Terraform state is remote with locking** — S3 + DynamoDB, GCS + object lock, or TFC/E — and state bucket has versioning enabled with MFA delete.
2. [ ] **Terraform plan runs clean** — zero unexpected creates/destroys/drifts on `terraform plan` from a clean checkout against every environment.
3. [ ] **Drift detection is enabled and alerting** — AWS Config rules, Terraform drift detection, or Argo CD `OutOfSync` alerts fire within the sync interval + 5 minutes.
4. [ ] **Secrets never appear in plaintext** — `tfsec`/`checkov`/`detect-secrets` pass with zero findings. No `sensitive = false` on secret outputs.
5. [ ] **IAM roles follow least privilege** — no `*` in Action or Resource for production roles. Service roles scoped to specific resources. Wildcard policies flagged as critical.
6. [ ] **All infrastructure is tagged** — mandatory tags enforced by SCP/Terraform validation: `cost_center`, `environment`, `owner`, `compliance` at minimum. Nightly compliance scan auto-terminates untagged resources after 48 hours.
7. [ ] **Encryption at rest is enabled** — S3 SSE-KMS, RDS encryption, EBS encryption by default in all regions, DynamoDB encryption. KMS key rotation enabled.
8. [ ] **Encryption in transit enforced** — ALB HTTPS only with minimum TLS 1.2. Service mesh mTLS for inter-service traffic. Vault auto-unseal in production.
9. [ ] **Rollback is tested and automated** — one-command rollback to previous deployment. Rollback smoke test verifies health. Rollback completes in < 5 minutes from trigger.
10. [ ] **Disaster recovery documented and drilled** — DR runbook with RPO/RTO targets. Quarterly failover drill with production traffic. Recovery from backup tested monthly by restoring to a staging cluster.
11. [ ] **Policy as code gates all deployments** — OPA/Checkov/Sentinel blocks non-compliant resources in CI. Production deploys require policy pass + human approval for infrastructure changes affecting security boundaries.
12. [ ] **Alerting covers the golden signals** — latency (P95/P99), error rate (5xx), throughput (RPS), saturation (CPU/memory/disk). Alerts are multi-window burn-rate based, not raw threshold.
13. [ ] **Runbooks are executable, not prose** — every alert links to a runbook where steps are scripts. Runbook validation runs weekly in staging. Any runbook not validated in 90 days is flagged.
14. [ ] **Access to production infrastructure requires MFA** — IAM policies enforce MFA for console access. AssumeRole requires MFA context key. Break-glass procedures documented for MFA device loss.

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

## Anti-Patterns

- **Manual infrastructure changes (ClickOps) outside of IaC** — an on-call engineer manually increases an RDS instance size via the AWS console during a 2 AM incident to restore service, then forgets to update the Terraform config. The next `terraform apply` reverts the instance back to the smaller size, re-triggering the exact same outage during business hours when customer traffic is 10x higher. The resulting 4-hour production outage costs $50K in SLA credits, $30K in engineering firefighting time, and $120K in customer trust erosion. **Total cost: $50K-$200K per drift-related outage from manual infrastructure changes.** Immediately after any emergency manual change, create a Jira ticket to sync the change back into IaC within 24 hours, and enable AWS Config rules or drift detection to alert on infrastructure-state mismatches.
- **Terraform `count` vs `for_each`**: When you remove an item from the MIDDLE of a count-based list, Terraform shifts all subsequent resource indices. The resource at index 3 gets destroyed and recreated as index 2 — potentially destructive. `for_each` with stable keys prevents index shifting.
- **Terraform state file** in S3 with DynamoDB locking — if the DynamoDB table is in a different region and that region has an outage, ALL Terraform operations fail with "Error acquiring state lock." Co-locate the lock table with the state bucket.
- **`terraform plan -out`** saves the plan at planning time, but the plan is a snapshot of the state at that moment. If another CI pipeline applies changes between your plan and apply, the apply fails with "state has changed" — but the failure message doesn't tell you what changed.
- **Kubernetes `imagePullPolicy: Always`** re-pulls the image every pod start, including restarts. During a registry outage, pods can't restart. Use `IfNotPresent` with digest-based tags (e.g., `myapp@sha256:...`) for production.
- **Helm's `--wait` flag** waits for pods to be "Ready" but doesn't check for CrashLoopBackOff — a pod that starts, crashes, restarts, crashes, restarting forever is "Ready" between crashes. Helm reports success on a failing deployment.
- **Secret management**: `kubectl get secret -o yaml` reveals base64-encoded (NOT encrypted) secrets. Anyone with `get secret` permissions can decode them. Use External Secrets Operator or Sealed Secrets, never store plain secrets in Kubernetes Secret objects.
- **Hardcoding credentials in CI/CD pipeline configuration instead of using a secrets manager.** A developer pastes an AWS access key into a Jenkinsfile or GitHub Actions YAML so a deployment "just works." Six months later, that key — which had AdministratorAccess — appears in a public repository fork because someone set the repo to public for a demo. An attacker scrapes GitHub for exposed credentials, finds the key within 4 minutes using automated tooling, and spins up $80,000 in crypto mining EC2 instances before AWS abuse detection kicks in. The breach also triggers a SOC 2 audit failure and mandatory customer notification costing $150K in legal and remediation. **Total cost: $80K-$250K in direct fraud, forensic audit, legal fees, and compliance penalties per credential leak.** Never store credentials in pipeline configs — use GitHub Actions secrets, HashiCorp Vault, or AWS Secrets Manager with short-lived tokens, and enable GitGuardian or truffleHog in CI to block pushes containing secrets.
- **Deploying on Friday afternoon without a tested rollback plan.** The team pushes a migration that drops and recreates a column at 4:30 PM Friday. The migration takes 40 minutes on production data instead of the 2 minutes it took on the staging subset, locks the table, and takes down checkout. The developer who wrote it left for the weekend 15 minutes ago. No one else knows the rollback procedure, and the on-call engineer spends 3 hours reading the migration code before discovering the `down` method was never written. **Total cost: $90K-$400K in lost revenue from 6+ hours of weekend downtime, depending on traffic volume and SLA penalties.** Enforce a deployment freeze window (e.g., no Friday deploys after 2 PM), require every migration to have a tested rollback path validated in a staging environment with production-scale data, and ensure at least two engineers are familiar with every deployable change before it reaches production.
- **Configuring auto-scaling on CPU alone while ignoring application-level backpressure.** Your service auto-scales perfectly on CPU — adding instances when CPU hits 70% and removing them at 30%. But your application's real bottleneck is database connection pool exhaustion: each new instance opens 20 connections, and at 10 instances the database hits its 200-connection limit. The auto-scaler sees CPU at 45% (fine), but users see 503 errors because the app can't get a database connection. The next 3 instances that spin up make the problem worse by attempting more connections that immediately fail. **Total cost: $30K-$150K in degraded service during a traffic surge that auto-scaling was supposed to prevent.** Instrument application-level metrics (connection pool utilization, request queue depth, P99 latency) as scaling signals alongside CPU, set maximum instance counts based on downstream resource limits, and use predictive scaling during known traffic events rather than relying solely on reactive scaling.
- **Running databases and stateful workloads in Kubernetes without understanding PersistentVolume reclaim policies.** You deploy PostgreSQL in Kubernetes with the default `Delete` reclaim policy on the PersistentVolume. A Helm upgrade replaces the StatefulSet, the old PVC is deleted, and the PV is destroyed — taking 18 months of customer data with it. Your S3 backups exist but restoring 2TB of data takes 14 hours, during which the application is down. The incident triggers a data-loss notification to all customers under GDPR, and three enterprise customers invoke their SLA penalty clauses. **Total cost: $200K-$1.5M in downtime, data restoration labor, SLA penalties, and customer churn from permanent data loss.** Always set PersistentVolume reclaim policy to `Retain` for databases and stateful workloads, schedule automated backup verification (restore from backup to a test cluster weekly), and use Velero or similar tools to snapshot both PVs and Kubernetes resource definitions.
- **Terraform remote state without cross-account access controls** — your Terraform state for production infrastructure lives in an S3 bucket in the shared DevOps account. An intern with read-only access to the DevOps account clones a repo that references that state backend. They run `terraform plan` from their local machine during onboarding, and it works — meaning anyone with DevOps account credentials can read all production resource IDs, ARNs, database endpoints, and secret references serialized in the state file. A credential leak from a compromised laptop exposes the state file to an attacker who now has a complete topology map of your production infrastructure and knows exactly which S3 buckets, RDS instances, and IAM roles exist. **Total cost: $50K-$500K in breach impact from infrastructure topology exposure — the state file IS a security document.** Fix: Encrypt state files with KMS keys that have per-environment key policies; use Terraform Cloud or remote backends with explicit IAM conditions (require MFA, restrict source IPs); treat state file access as equivalent to production data access in your security review process; never store state files in shared developer-accessible buckets.
- **Container image registries without vulnerability scanning at push time** — your CI pipeline builds and pushes Docker images to ECR/Artifact Registry without scanning. A developer pulls `python:3.9-slim` which includes a critical OpenSSL CVE patched 6 months ago. Over 8 months, 800 production images accumulate unpatched CVEs. During a SOC 2 audit, the auditor flags 47 critical CVEs in actively deployed containers. Remediation requires patching and redeploying 47 services within 30 days or losing certification — an all-hands effort costing 200+ engineering hours. One customer pauses their $500K contract renewal pending the audit outcome. **Total cost: $100K-$500K in audit remediation, contract risk, and emergency patching sprints from unscanned container images.** Fix: Integrate vulnerability scanning into the CI pipeline (Trivy, Grype, or AWS ECR scanning); fail builds on critical CVEs with a fix available; implement a recurring scan of all deployed images and auto-create Jira tickets for newly discovered CVEs; set an SLO for mean time to patch critical CVEs (e.g., 72 hours).
- **Git branch protection without requiring pull requests on the default branch** — you enable branch protection on `main` requiring status checks and CODEOWNERS reviews, but leave "Require a pull request before merging" unchecked. A developer force-pushes directly to `main` during a late-night incident while "fixing a typo." The force-push overwrites three merged PRs from the previous day, reverting critical security patches. The overwritten commits are unreferenced and garbage-collected after 90 days, making recovery impossible from Git alone. The security patches were for an authentication bypass vulnerability — the revert goes undetected for 3 weeks until a penetration test finds the vulnerability live in production. **Total cost: $100K-$1M in security incident response, customer notification, and regulatory fines from force-pushed security patches.** Fix: Enable "Require a pull request before merging" on all protected branches; enable "Do not allow bypassing the above settings" including administrators; implement repository-level force-push blocking via `receive.denyNonFastForwards` server-side hook; use GitHub push protection or pre-receive hooks to prevent direct pushes to protected branches even by admins.

## Verification

- [ ] Run `terraform validate` — configuration is valid
- [ ] Run `terraform plan` — plan is clean (no unexpected creates/destroys)
- [ ] Run `checkov` or `tfsec` on Terraform — zero high/critical findings
- [ ] Verify state locking: run `terraform plan` in two terminals simultaneously — second one waits for lock, doesn't corrupt state
- [ ] Secrets check: `tfsec` or `detect-secrets` confirms no plaintext secrets in configs
- [ ] Deploy to staging, verify health, then promote to production — GitOps workflow is end-to-end functional

## Verification Guardrails

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

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

