## Core Workflow

### Phase 1: IAM Hardening

Execute in order. Do not skip steps.

```
1. INVENTORY ALL IDENTITIES
   |-- List all IAM users, roles, groups, service accounts (AWS, Azure, GCP)
   |-- Run IAM Credential Report (AWS) / List service principals (Azure) / List service accounts (GCP)
   |-- Flag unused credentials: users with no activity >90 days, access keys >90 days old, service accounts without key rotation
   |-- Identify root account status: MFA enabled? Access keys present? Last activity?

2. ENFORCE ACCOUNT-LEVEL GUARDRAILS
   |-- AWS SCPs at org root: Deny leaving org, deny public S3 ACLs, deny root user usage, deny disabling CloudTrail
   |-- Azure Management Group policies: Require MFA for admins, deny public blob, require encryption at rest
   |-- GCP Organization Policies: Disable service account key creation, restrict Domain Restricted Sharing, enforce VPC Service Controls
   |-- Password policy: Minimum 14 characters, MFA required for all human users

3. DESIGN ROLE HIERARCHY WITH LEAST PRIVILEGE
   |-- Principle: Start with AWSDenyAll (implicit deny), add only what is required
   |-- Federation-first: No IAM users -- use AWS SSO/Azure AD/GCP Workforce Identity with SCIM provisioning
   |-- Role categories:
   |   |-- Human roles: Developer (read-only + limited dev actions), Operator (read-only + break-glass), Admin (full but MFA + just-in-time)
   |   |-- Service roles: Per-service with minimum permissions (LambdaRole-S3Read-accountid-bucketname)
   |   |-- Cross-account roles: Specific external account IDs with external ID conditions
   |-- Permission boundaries: Enforce maximum permissions even if role policy is broader
   |-- IAM conditions: aws:SourceIp, aws:RequestedRegion, aws:MultiFactorAuthPresent, ec2:ResourceTag

4. POLICY ANALYSIS LOOP
   |-- Run IAM Access Analyzer: External access findings -> resolve within 24h
   |-- Policy Simulator: Test every role against intended actions
   |-- Unused access analysis: IAM Access Analyzer unused access findings -> remove within 7 days
   |-- Quarterly review: All policies >100 lines reviewed for scope creep
   |-- Automated remediation: AWS Config rules for IAM (iam-user-no-policies-check, iam-policy-no-statements-with-admin-access)

5. EMERGENCY ACCESS (BREAK-GLASS)
   |-- Dedicated break-glass role with CloudTrail alert on any usage
   |-- No break-glass user -- only assume-role with MFA
   |-- Auto-removal: Break-glass session auto-expires at 1 hour
   |-- Post-access review: Every break-glass usage reviewed by security team within 24h
   |-- Quarterly test: Verify break-glass procedures still work
```

### Phase 2: Network Security Architecture

```
1. ACCOUNT/PROJECT SEGMENTATION
   |-- Separate accounts/projects per environment (prod, staging, dev, security, shared-services)
   |-- Separate accounts/projects per workload tier (data, compute, network)
   |-- AWS Organizations with OU structure: Security (audit, logging), Infrastructure (networking, shared), Workloads (per-app)
   |-- Azure Management Groups mirroring: Root -> Production -> Applications / Data, Non-Production, Sandbox (with spending limits)

2. VPC/VNET/VCN DESIGN
   |-- Tiered subnet architecture:
   |   |-- Public subnets: ALB/NLB, CloudFront, API Gateway -- never application instances
   |   |-- Private app subnets: EC2/VM/GCE instances, ECS/EKS/AKS/GKE pods -- no public IPs
   |   |-- Private data subnets: RDS/Aurora/CosmosDB/Cloud SQL -- no internet access, no public IPs
   |   |-- Intra-tier: Security groups for east-west traffic, NetworkPolicy for Kubernetes
   |-- CIDR planning: Non-overlapping ranges per VPC/VNet, /16 per VPC minimum for expansion
   |-- VPC endpoints (PrivateLink): All AWS service access via VPC endpoints -- no NAT gateway for S3, DynamoDB, KMS, STS, SSM, ECR
   |-- Transit Gateway / Hub-Spoke: Centralized egress inspection, inter-VPC routing with route table segmentation

3. LAYERED SECURITY GROUPS (REFERENCE ARCHITECTURE)
   |-- SG-External: Your corporate/office/VPN CIDRs only -- allows SSH/RDP to bastion
   |-- SG-Bastion: Allows SSH from SG-External, allows SSH to SG-App
   |-- SG-App: Allows HTTP/HTTPS from ALB security group only, allows app port from SG-Bastion
   |-- SG-Data: Allows database port from SG-App only, no other ingress
   |-- SG-Monitoring: Allows Prometheus/Grafana from monitoring VPC only
   |-- Rule: No security group ever references 0.0.0.0/0 for sensitive ports

4. WAF AND DDoS PROTECTION
   |-- AWS WAF: Deploy on CloudFront/ALB with AWS Managed Rules (Core Rule Set, SQL database, PHP/WordPress)
   |-- Rate-based rules: 2000 requests per 5 minutes per IP (adjust per application profile)
   |-- IP reputation: Block AWS IPSet of known malicious IPs
   |-- AWS Shield Advanced: For internet-facing applications (costs $3,000/month + data transfer but includes DDoS cost protection)
   |-- Azure WAF: Front Door/Application Gateway with OWASP 3.2 ruleset in Prevention mode
   |-- GCP Cloud Armor: Pre-configured WAF rules + Adaptive Protection (ML-based L7 DDoS detection)

5. EGRESS FILTERING
   |-- Default deny outbound from all private subnets -- explicit allow only
   |-- Proxy all outbound HTTP/HTTPS through forward proxy for content inspection and DLP
   |-- AWS Network Firewall / Azure Firewall / GCP Cloud NGFW: Stateful inspection with domain allowlisting
   |-- DNS firewall: Route 53 Resolver DNS Firewall / Azure DNS Private Resolver DNS Forwarding Rules / GCP Cloud DNS policies
```

### Phase 3: Secrets Management

```
1. SECRET INVENTORY & CLASSIFICATION
   |-- Scan code repos: git-secrets, truffleHog, detect-secrets for committed secrets
   |-- Scan environment variables: env | grep -iE 'key|secret|token|password|credential'
   |-- Scan CI/CD pipeline configuration: GitHub Actions secrets, GitLab CI variables, Jenkins credentials
   |-- Classify: Database credentials (rotate every 30 days), API keys (rotate every 90 days), TLS certificates (rotate before expiry, 30-day buffer)
   |-- Catalog all secrets: Owner, rotation frequency, last rotation date, systems that consume it

2. DEPLOY MANAGED SECRETS STORE
   |-- AWS Secrets Manager: AWS-managed KMS encryption, automatic rotation (Lambda-based), cross-account access via resource policies, $0.40/secret/month + $0.05/10,000 API calls
   |-- Azure Key Vault: HSM-backed keys (FIPS 140-2 Level 2), RBAC or access policies, automatic rotation (Event Grid + Azure Functions), soft delete + purge protection mandatory
   |-- GCP Secret Manager: Regional or global replication, IAM-based access, automatic rotation (Cloud Scheduler + Cloud Functions), versioning with aliases
   |-- HashiCorp Vault (for multi-cloud): Dynamic secrets (generate on-demand, auto-expire), database credential rotation, PKI engine for internal certificates

3. ELIMINATE ENVIRONMENT VARIABLE SECRETS
   |-- Application code: Never reads from process.env -- reads from secrets manager SDK at startup
   |-- Kubernetes: External Secrets Operator (ESO) syncs AWS/GCP/Azure secrets to K8s secrets, or CSI Secret Store driver mounts secrets as tmpfs volumes
   |-- CI/CD: OIDC federation (GitHub Actions -> AWS IAM, no long-lived keys), short-lived tokens (max 1 hour)
   |-- Database connections: Use IAM database authentication (RDS IAM auth, Cloud SQL IAM auth) -- no passwords

4. JUST-IN-TIME (JIT) CREDENTIAL GENERATION
   |-- Developer access: AWS SSO / Azure AD PIM / GCP Workforce Identity -- temporary credentials, max 8 hours
   |-- CI/CD pipelines: OIDC federation with short-lived tokens -- no static credentials
   |-- Cross-account access: AssumeRole with ExternalId condition, max session duration 1 hour
   |-- Emergency access: Break-glass role with immediate CloudTrail alert, max 1 hour

5. ROTATION AUTOMATION
   |-- Enable automatic rotation on all Secrets Manager secrets (scheduled Lambda/Function)
   |-- Monitor LastRotatedDate via CloudWatch/Dashboard Alert if rotation fails >2x scheduled frequency
   |-- Database credentials: Use secrets manager rotation with multi-user strategy (two alternating credentials) for zero-downtime rotation
   |-- TLS certificates: ACM/Azure Key Vault certificates auto-renewal with DNS validation
```

### Phase 4: Compliance Automation

```
1. SELECT COMPLIANCE FRAMEWORK(S)
   |-- CIS Benchmarks: CIS AWS Foundations (v2.0.0, 49 controls), CIS Azure Foundations, CIS GCP Foundations
   |-- PCI DSS v4.0: Cloud-specific requirements (Req 7: access control, Req 8: MFA)
   |-- HIPAA: Administrative, Physical, Technical Safeguards mapped to cloud controls
   |-- SOC 2: Trust Services Criteria (Security, Availability, Confidentiality) mapped to AWS Config/Azure Policy
   |-- Custom: Internal security policy mapped to cloud-native controls

2. DEPLOY COMPLIANCE SCANNING
   |-- Prowler (AWS): 300+ checks across CIS, PCI, HIPAA, GDPR, SOC 2, ENS, AWS FTR
   |-- ScoutSuite (multi-cloud): AWS, Azure, GCP assessment with HTML dashboards
   |-- AWS Config: Managed rules (CIS benchmark conformance packs), custom rules via Lambda
   |-- Azure Policy: Built-in initiative definitions (CIS, PCI, HIPAA), custom policies, deploy-if-not-exist remediation
   |-- GCP Security Command Center: Built-in compliance reports (CIS, PCI, ISO 27001, SOC), custom detectors

3. COMPLIANCE-AS-CODE IMPLEMENTATION
   |-- Terraform Sentinel (Enterprise): Policy-as-code with import tfplan/v2, enforce before apply
   |-- Open Policy Agent (OPA): Rego policies for Terraform plan JSON, Kubernetes admission control, Envoy authorization
   |-- Regula: Pre-built Rego rules for Terraform and CloudFormation (from Fugue), CI/CD integration
   |-- cfn-guard: AWS CloudFormation policy-as-code (Guard rules v2), validate templates pre-deployment
   |-- checkov: Bridgecrew's IaC scanner with 750+ built-in policies, custom Python/Graph policies

4. CONTINUOUS MONITORING & DRIFT DETECTION
   |-- Schedule: Prowler/ScoutSuite daily, AWS Config continuous, Azure Policy evaluation every 15 minutes
   |-- Drift detection: Compare deployed resources against IaC definitions daily
   |-- Findings aggregation: AWS Security Hub (centralized findings from Config, GuardDuty, Inspector, Macie, IAM Access Analyzer)
   |-- Alerting: PagerDuty/OpsGenie for CRITICAL findings, Slack/Teams digest for HIGH, weekly email for MEDIUM
   |-- Dashboard: Security Hub + QuickSight / Azure Workbooks / GCP Security Command Center dashboard

5. EVIDENCE COLLECTION & AUDIT TRAIL
   |-- Automated evidence: CloudTrail (management events, 7-year retention in S3 Glacier Deep Archive with legal hold)
   |-- Config timeline: AWS Config configuration recorder with delivery to S3, 7-year retention
   |-- Change tracking: Tag all resources with Owner, Environment, CostCenter, DataClassification
   |-- Audit prep: Pre-built evidence packs for PCI DSS ROC, SOC 2 Type II, HIPAA attestation
```

### Phase 5: Workload Security

```
1. CONTAINER IMAGE SECURITY
   |-- Image scanning: Scan every image in registry (ECR basic scanning / Inspector, ACR Defender, GCR Container Analysis)
   |-- Block deployment: Admission controller blocks images with CRITICAL vulnerabilities
   |-- Image signing: Cosign (Sigstore) -- sign images at build, verify at deployment via Kyverno/Gatekeeper
   |-- Minimal base images: Distroless, Alpine-slim, scratch -- no package manager, no shell if possible
   |-- SBOM generation: Syft/Grype at build, attest provenance with SLSA L3

2. KUBERNETES SECURITY BASELINE
   |-- Pod Security Standards (PSS): baseline or restricted profile -- no privileged, no hostNetwork, no hostPID, readOnlyRootFilesystem
   |-- NetworkPolicy: Default deny all, explicit allow for required pod-to-pod communication, namespace isolation
   |-- Admission control: OPA Gatekeeper or Kyverno with policies for: deny privileged pods, require resource limits, require non-root user, block latest tag
   |-- etcd encryption: Always enable encryption at rest (AWS EKS envelope encryption with KMS, Azure AKS, GCP GKE)
   |-- Secrets encryption: KMS plugin for Kubernetes secrets (not base64 encoding)
   |-- Runtime protection: Falco (syscall anomaly detection), Tetragon (eBPF-based enforcement)

3. SERVERLESS SECURITY
   |-- Lambda execution role: Per-function IAM role with least privilege -- no AdministratorAccess wildcard
   |-- Lambda in VPC: For database access, place Lambda in private subnet with VPC endpoints
   |-- Environment variables: No secrets in env vars -- read from Secrets Manager/Parameter Store inside handler
   |-- Function URL auth: AWS_IAM only for internal, never NONE (public, no auth)
   |-- CloudFront + WAF in front of API Gateway/Lambda URLs for DDoS and injection protection
   |-- Code signing: Enable Lambda code signing with Signer profiles

4. DATA PROTECTION
   |-- Encryption at rest: S3 default encryption (SSE-S3 or SSE-KMS), RDS encryption, EBS encryption by default (account-level setting)
   |-- Encryption in transit: TLS 1.2+ minimum for all services, ACM certificates on ALB/CloudFront/API Gateway
   |-- Key management: AWS KMS (customer-managed CMKs with key rotation, annual manual rotation for imported material)
   |-- S3 bucket policy: DenyInsecureTransport (block HTTP), DenyUnencryptedObjectUploads, RestrictPublicBucket
   |-- Data classification: Tag all S3 buckets/RDS instances with DataClassification: Public|Internal|Confidential|Restricted
   |-- Macie (AWS): Automated sensitive data discovery (PII, PHI, credentials) in S3 buckets

5. RUNTIME MONITORING & THREAT DETECTION
   |-- GuardDuty: Enable in all regions, continuous monitoring of VPC Flow Logs, CloudTrail, DNS logs
   |-- Security Hub: Aggregate findings, CIS checks, automated remediation via EventBridge + Lambda
   |-- AWS Inspector: Vulnerability scanning for EC2, ECR, Lambda -- automated SBOM-based
   |-- CloudTrail Insights: Anomaly detection on write management events
   |-- Azure Sentinel: Cloud-native SIEM with UEBA, automated investigation playbooks
   |-- GCP Security Command Center Premium: Event Threat Detection, Container Threat Detection
```
