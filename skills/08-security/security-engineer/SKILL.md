---
name: security-engineer
description: Application security, penetration testing, IAM design, secrets management,
  API security, network security, zero trust, and security monitoring. Triggered by
  security, pentest, IAM, secrets, zero trust, vulnerability, threat model, API security.
author: Sandeep Kumar Penchala
type: security
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- security-engineer
token_budget: 2835
chain:
  consumes_from:
  - cloud-architect
  - compliance-officer
  - devops-engineer
  - gdpr-privacy
  - hipaa-technical-implementation
  - incident-responder
  - privacy-engineer
  - system-architect
  feeds_into:
  - backend-developer
  - ci-cd-builder
  - cloud-architect
  - compliance-officer
  - cto-advisor
  - devops-engineer
  - firmware-developer
  - hipaa-technical-implementation
  - incident-responder
  - networking-engineer
  - privacy-engineer
  - security-reviewer
  - system-architect
  - trust-safety-engineer
output:
  type: code
  path_hint: ./
------
# Security Engineer

Design, implement, and validate security controls across the application, infrastructure, and network
layers. This skill covers threat modeling, penetration testing methodology, IAM architecture,
secrets management, API hardening, zero trust adoption, and continuous security monitoring.

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->
```
What are you trying to do?
├── Threat model a system (STRIDE, PASTA) → Jump to "Core Workflow" — Phase 1 (Threat Modeling)
├── Review security architecture or harden APIs → Jump to "Core Workflow" — Phase 2 (App & API Security)
├── Set up secrets management (Vault, SOPS) → Jump to "Core Workflow" — Phase 4 (Secrets Management)
├── Implement zero trust architecture → Jump to "Core Workflow" — Phase 5 (Network Security & Zero Trust)
├── Respond to a vulnerability or security incident → Jump to "Core Workflow" — Phase 6 (Monitoring & Detection)
├── Need compliance or regulatory guidance → Invoke `compliance-officer` skill instead
├── Active breach in progress → Invoke `incident-responder` skill instead
├── Need cloud security architecture → Invoke `cloud-architect` skill instead
├── Need infrastructure hardening → Invoke `devops-engineer` skill instead
└── Not sure? → Describe the problem in plain language and I'll route you
```
Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces. Security engineering deals in probabilities and trade-offs — absolute claims create a false sense of safety.

- **Never claim a system is "secure."** Security is a spectrum, not a binary state. Every system has undiscovered vulnerabilities, and every defense can be bypassed given enough time and resources. Say "this configuration reduces the attack surface against these specific threats" rather than "this system is secure."
- **Threat models are hypotheses, not guarantees.** STRIDE, PASTA, and attack trees help identify *plausible* threats, but they can miss novel attack vectors. Every threat model output should be validated with actual penetration testing and red team exercises before relying on it for design decisions.
- **CVE severity depends on context.** A CVSS 9.8 in a dependency used only in a build tool with no network exposure is not a production-critical vulnerability. A CVSS 5.3 in an authentication library exposed to the internet may be. Always evaluate CVEs against actual deployment context and exploitability, not just the score.
- **Never recommend security through obscurity.** Kerckhoffs's principle states that a cryptosystem should be secure even if everything about it except the key is public knowledge. Secrets in source code, custom "unbreakable" algorithms, and hidden endpoints are not security controls — they are future incidents waiting to happen.
- **Admit when you're operating outside your threat model.** If the user describes a system or attack vector you haven't fully mapped, say so. Recommending controls without understanding the full system architecture and data flows is how critical gaps get missed. Ask for the information you need before prescribing.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Conducting threat modeling sessions using STRIDE, PASTA, or attack trees
- Performing penetration tests against web applications, APIs, cloud infrastructure, or mobile apps
- Designing IAM strategies: role-based access control, attribute-based access control, just-in-time access
- Implementing secrets management with HashiCorp Vault, AWS Secrets Manager, or SOPS
- Hardening APIs against OWASP Top 10: injection, broken auth, SSRF, excessive data exposure
- Architecting network security: network policies, WAF, DDoS protection, segmentation
- Adopting zero trust architecture: micro-segmentation, continuous verification, device trust
- Building a security monitoring and detection pipeline (SIEM, SOAR, threat intelligence feeds)

- **Use `/security-reviewer` instead** when: You need a code-level security review of a PR, dependency audit on a specific change, or SAST finding triage. Security-engineer builds the security program; security-reviewer inspects individual changes against it.
- **Use `/incident-responder` instead** when: A security incident is in progress or has just been detected — active containment, eradication, and recovery. Security-engineer builds preventive controls; incident-responder handles active breaches.

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### Threat Modeling Depth

```
System maturity and risk?
├── Greenfield (new system, pre-code) → Full STRIDE per component. DFDs from architecture.
│     Goal: Eliminate threats in design before they become code. Cheapest time to fix.
├── Brownfield (existing system, new feature) → Threat modeling on changed components only.
│     Focus: Data flows crossing trust boundaries. Input validation at new entry points.
├── Scale (prod with >10K users) → Continuous threat modeling. PASTA or attack trees.
│     Goal: Prioritize by business impact. Red team exercises for validation.
└── Compliance-driven (PCI-DSS, SOC 2) → Asset-based. Map threats to control requirements.
      Goal: Demonstrate due diligence. Generate compliance artifacts alongside findings.
```

### Security Tooling by Team Size

```
Team size?
├── Solo → OWASP ZAP (free). GitHub Dependabot (free). Manual pentest checklist.
│     Cost: $0. Time: 4 hours/month for security review.
├── Small (2-10) → Snyk/Burp Suite Community + npm audit + Trivy + Semgrep (OSS).
│     Cost: $0-200/month. CI-integrated SAST. Monthly manual review of critical paths.
├── Medium (10-50) → Burp Suite Pro + Snyk Team + Wazuh SIEM + HashiCorp Vault.
│     Cost: $500-5K/month. Dedicated security engineer. Quarterly pentests.
└── Enterprise (50+) → Full AppSec program. DAST + SAST + IAST + RASP. Bug bounty.
      Cost: $50K+/month. Security team (3+). Continuous red team. SOC 2 Type II.

**What good looks like:** The output opens correctly in the target tool. All validations pass. No placeholder content remains.

```

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Threat Modeling and Risk Assessment
1. Diagram the system: data flow diagrams (DFDs) showing trust boundaries, external entities, data stores, and processes.
2. Apply STRIDE per element: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.
3. Identify threats and rank by likelihood × impact using a risk matrix (CVSS or custom scoring).
4. Define mitigations: eliminate the threat, reduce likelihood, reduce impact, transfer risk, or accept with justification.
5. Document in a threat model register; review quarterly or on major architectural changes.

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Application and API Security
1. Integrate SAST (Semgrep, SonarQube, CodeQL) into the CI pipeline at PR time; block on critical/high findings.
2. Run SCA (Dependabot, Snyk, OWASP Dependency-Check) to detect vulnerable open-source libraries.
3. Perform DAST (OWASP ZAP, Burp Suite) against staging environments on a schedule and on major releases.
4. Harden API endpoints: implement rate limiting, input validation, output encoding, proper CORS, and content security policies.
5. Enforce authentication and authorization at the API gateway; use OAuth2/OIDC with short-lived tokens and refresh token rotation.
6. Protect against OWASP Top 10: parameterized queries for SQL injection, HTML entity encoding for XSS, strict deserialization.

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Identity and Access Management (IAM)
1. Design role-based access control (RBAC) with well-defined role hierarchies and least-privilege defaults.
2. Implement just-in-time (JIT) access for privileged operations: request, approve, grant temporary elevation, auto-revoke.
3. Use OIDC for service-to-service and CI/CD-to-cloud authentication — no long-lived static credentials.
4. Enforce multi-factor authentication (MFA) for all human users; hardware security keys for administrative roles.
5. Implement permission boundaries and service control policies to limit the blast radius of compromised credentials.
6. Audit IAM quarterly: review unused roles, overly permissive policies, and inactive users; use IAM Access Analyzer or Policy Simulator.

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Secrets Management
1. Centralize secrets in a dedicated vault (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault).
2. Implement dynamic secrets for databases: generate ephemeral credentials on demand, auto-expire within hours.
3. Use envelope encryption: encrypt data with a data key, encrypt the data key with a master key (KMS).
4. Never log, echo, or commit secrets; use pre-commit hooks (detect-secrets, gitleaks) to block accidental exposure.
5. Rotate secrets automatically: database passwords, API keys, TLS certificates — all on a defined rotation schedule.
6. For Kubernetes: use External Secrets Operator or Sealed Secrets; never store raw secrets in etcd without encryption at rest.

<!-- DEEP: 10+min -->
### Phase 5 (~25 min): Network Security and Zero Trust
1. Implement micro-segmentation: default-deny network policies, explicit allow rules between specific services.
2. Deploy a Web Application Firewall (AWS WAF, Cloudflare, ModSecurity) with OWASP Core Rule Set; tune to reduce false positives.
3. Protect against DDoS: CloudFront/Cloudflare at the edge, AWS Shield Advanced or equivalent for layer 3/4 protection.
4. Zero trust principles: never trust, always verify — authenticate every request regardless of source network.
5. Use mutual TLS (mTLS) for service-to-service communication; manage certificates with cert-manager or a service mesh.
6. Implement outbound traffic inspection with a forward proxy to detect data exfiltration and command-and-control traffic.

<!-- DEEP: 10+min -->
### Phase 6 (~25 min): Security Monitoring and Incident Detection
1. Aggregate logs centrally: CloudTrail, VPC Flow Logs, application logs, WAF logs → SIEM (Splunk, Elastic Security, Sentinel).
2. Define detection rules for common attack patterns: credential brute-force, privilege escalation, data exfiltration, crypto mining.
3. Set up SOAR playbooks for automated triage: enrich alerts with threat intelligence, quarantine compromised hosts, revoke credentials.
4. Hunt for threats proactively: run hypothesis-driven threat hunts monthly based on threat intelligence and MITRE ATT&CK.
5. Tune alerting to balance signal-to-noise: measure mean time to detect (MTTD) and mean time to acknowledge (MTTA).


### Cross-skills Integration
```bash
# Security review → Security implementation → Compliance mapping
/security-reviewer && /security-engineer && /compliance-officer
# Infrastructure security → Security hardening → Incident response
/devops-engineer && /security-engineer && /incident-responder
# Security reviewer finds issues. Security engineer implements fixes. Compliance officer maps to controls.
```

## Sub-Skills
<!-- QUICK: 30s -- table of deeper dives by topic -->
When this skill is invoked, the agent may need to drill into these specialized areas:

| Sub-Skill | When to Use |
|-----------|-------------|
| `threat-modeling` | Applying STRIDE, attack trees, and MITRE ATT&CK to architecture and new features |
| `sast-implementation` | Writing Semgrep rules, custom detectors, and CI gates for code-level security |
| `secrets-management` | Implementing Vault patterns, pre-commit hooks, secret rotation, and just-in-time access |
| `auth-security` | Designing MFA, password policies, OAuth2 threat mitigation, and session management |
| `network-security` | Architecting zero trust, mTLS, WAF deployment, and API gateway security |
| `container-security` | Scanning images for CVEs, enforcing non-root users, read-only filesystems, and seccomp profiles |
| `dependency-security` | Managing software supply chain risk: SBOM, vulnerability triage, and automated patching |
| `security-champions` | Embedding security culture through training, gamification, and champion programs |

## Scale Depth: Solo → Small → Medium → Enterprise

### Solo
Focus: basic AppSec (OWASP ZAP + Dependabot), manual threat modeling on critical paths. IAM: AWS IAM roles, no long-lived keys. Secrets: .env in gitignored vault, manual rotation. Monitoring: CloudTrail + GuardDuty. Team: part-time security (dev wears security hat). Skip: enterprise SIEM, full AppSec program, dedicated security team.

### Small Team
Focus: CI-integrated AppSec (Snyk/Trivy + Semgrep OSS), quarterly STRIDE reviews. IAM: RBAC + MFA for all humans. Secrets: HashiCorp Vault OSS or cloud secret manager. Monitoring: Wazuh/Elastic SIEM (OSS). Team: 1 dedicated security engineer. Coordination: with dev team on SAST findings triage, with DevOps on secrets rotation.

### Medium Team
Focus: Continuous threat modeling (PASTA), Burp Suite Pro + custom rules. IAM: JIT access + OIDC + quarterly access reviews. Secrets: Vault Enterprise, dynamic secrets, auto-rotation. Monitoring: Splunk/Elastic + SOAR playbooks. Team: Security team (2-3) + security champions. Coordination: with platform engineering on runtime security, with legal on compliance evidence.

### Enterprise
Focus: Full AppSec program (SAST+DAST+IAST+RASP, bug bounty). IAM: ABAC + permission boundaries + automated deprovisioning. Secrets: Multi-region Vault clusters, HSM-backed, envelope encryption. Monitoring: Full SOC (SIEM+SOAR+UEBA+threat intel, 24/7). Team: CISO + AppSec + InfraSec + SOC + GRC (8+). Coordination: with board/audit committee on security posture reporting, with legal on breach notification, with regulatory affairs on FedRAMP/SOC 2.

### Transition Triggers
| From → To | Trigger |
|-----------|---------|
| Solo → Small | First security incident; first enterprise customer security review |
| Small → Medium | SOC 2/ISO 27001 certification; dedicated security hire justified |
| Medium → Enterprise | IPO prep, operating critical infrastructure, or regulatory mandate (FedRAMP, PCI-DSS Level 1) |

## What Good Looks Like

> Every pull request runs SAST, SCA, and container scanning in CI, and critical findings block merge without exception. Secrets never touch plaintext — pre-commit hooks catch them, Vault issues dynamic credentials that auto-expire, and rotation is fully automated. The threat model is a living document reviewed every quarter, and new features ship with abuse cases already mitigated. The SIEM surfaces actionable signals, not noise, and the mean time to remediate a critical CVE is under 24 hours. Security is embedded in the engineering workflow, not bolted on at release time.

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `compliance-officer` | Control requirements mapped to technical implementations, compliance evidence expectations, audit preparation support | Before implementing security controls that must satisfy regulatory frameworks |
| `system-architect` | System topology, trust boundaries, data flow diagrams, component interactions | Before threat modeling or designing security architecture |
| `cloud-architect` | KMS key policies, SCP design, CloudTrail/Audit Log configuration, WAF rules, DDoS protection | Before configuring cloud security posture or IAM policies |
| `devops-engineer` | Vault/Secrets Manager architecture, security group/NetworkPolicy design, IAM least-privilege, container hardening | Before implementing secrets management or network security controls |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `security-reviewer` | Security requirements per data classification, approved crypto libraries, secure coding patterns, dependency allowlists | Code reviews miss security issues — vulnerabilities ship to production |
| `backend-developer` | Auth design patterns, data protection requirements, secure coding guidance, dependency security policies | Developers implement insecure patterns — technical debt accumulates |
| `incident-responder` | Detection rules, SOAR playbooks, forensic tooling access, threat intelligence sharing | Incident response has no detection capability — breaches go unnoticed |
| `compliance-officer` | Technical control evidence, vulnerability management metrics, security monitoring coverage | Compliance audits fail without technical evidence — certification at risk |

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| SAST/SCA scanner flags a critical CVE in a transitive dependency with a published exploit | Assess exploitability in your context (is the vulnerable code path reachable?), then apply the patch within 24 hours per SLA. If patching is blocked, implement a compensating control (WAF rule, network segmentation) and document the risk acceptance. | Critical CVEs with known exploits are being actively targeted. Every hour of delay increases the probability of compromise exponentially. |
| A developer commits an `.env` file or hardcoded secret that passes pre-commit hooks | Investigate why the pre-commit hook didn't catch it — the secret pattern may be missing from the detection rules. Rotate the exposed credential immediately. Add the detected pattern to the hook and scan the full repo history for prior exposures. | A secret that survives pre-commit hooks today means it was also missed yesterday. Every undetected secret in git history is a latent breach waiting to happen. |
| CloudTrail/Audit Log shows an IAM principal performing an action it has never performed before | This is an anomaly signal. Check if it's a new team member, a legitimate automation change, or a compromised credential. Correlate with login geography and source IP. If suspicious, revoke the credential and initiate incident response. | Unusual IAM activity is the most common early indicator of credential compromise. Novelty alone doesn't equal malice, but it demands immediate investigation. |
| A new S3 bucket or storage resource is created without Block Public Access enabled | Immediately enable Block Public Access at the bucket level and investigate the creation context. If this was an automated provisioning pipeline, fix the template. Public S3 buckets are the #1 cause of cloud data breaches. | Default-open storage is a data exfiltration waiting to happen. A single misconfigured bucket can expose millions of records in minutes. |
| Vulnerability scanner finds an unpatched critical CVE that was disclosed >7 days ago with a CVSS score ≥9.0 | This is an SLA violation — the CVE should have been patched within 24 hours. Escalate to the service owner and security leadership. Apply the patch immediately and conduct a postmortem on why the SLA was missed. | A missed SLA on a 9.0+ CVE is a near-miss incident. The vulnerability was exploitable for at least 6 days longer than policy allows — determine if it was exploited during that window. |
| SIEM alert fires for an outbound data transfer exceeding 500MB from a database-hosting subnet to an external IP | This is a potential data exfiltration event. Immediately isolate the source host, preserve forensic evidence (memory dump, network flows, process list), and initiate incident response. Outbound data transfer from data-tier subnets should be near-zero. | Large outbound flows from database subnets are almost never legitimate. Databases don't initiate outbound connections to the internet — someone or something is exfiltrating data. |
| An OWASP dependency-check or npm audit returns a vulnerability in a package that hasn't been updated in >2 years | The package is likely abandoned. Replace it with an actively maintained alternative, or fork and patch it yourself if it's critical to your application. Unmaintained dependencies accumulate known vulnerabilities without fixes. | Abandoned packages are time bombs. The Log4Shell crisis proved that even widely-used libraries can become unmaintained and critically vulnerable. |
| Security scanning pipeline is bypassed or disabled for an "emergency hotfix" without documented approval | The hotfix must still pass SAST and secret scanning — these checks add <2 minutes. If truly impossible, require a break-glass approval from the security lead with a 24-hour remediation window. Bypassing security gates normalizes the behavior. | Emergency bypasses are how Shadow IT creeps into production. Every bypass that isn't remediated becomes the new normal — and attackers know to target the un-scanned paths. |

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Shift left**: security testing in the IDE and at PR time; don't wait for staging or production scans.
- **Defense in depth**: no single control should be the only line of defense; layer preventive, detective, and corrective controls.
- **Assume breach**: design systems to limit blast radius, detect intrusions quickly, and recover gracefully.
- **Secrets never travel in plaintext**: encrypt in transit (TLS) and at rest (KMS); use ephemeral credentials whenever possible.
- **Patch aggressively**: automate OS and dependency patching; SLA: critical patches within 24 hours, high within 7 days.

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|-----------------|---------------------|
| Running SAST as a nightly job instead of blocking PRs on critical/high findings | Integrate SAST into the CI pipeline so it runs on every PR. Configure severity gates: critical and high findings block merge. Nightly scans find vulnerabilities hours after they've been merged — PR-time scans prevent them from reaching main. |
| Storing secrets in environment variables and assuming they're secure because "only the app can read them" | Use a secrets manager (HashiCorp Vault, AWS Secrets Manager) with dynamic credentials that auto-expire. Environment variables leak through child processes, debug endpoints, crash dumps, and logging frameworks. They are not a security boundary. |
| Running a penetration test, filing the report, and not remediating findings for months | Assign each pen test finding an owner, severity-based SLA (Critical: 7 days, High: 30 days), and track to closure in the same system as engineering bugs. An un-remediated pen test finding is a documented, known vulnerability that your security team acknowledged and ignored. |
| Implementing threat modeling only at project kickoff and never revisiting it | Treat the threat model as a living document reviewed every quarter and updated on every major architecture change. A threat model from the MVP phase doesn't account for the payment integration, third-party API, or admin panel added 6 months later. |
| Allowing IAM roles with wildcard permissions (`s3:*`, `ec2:*`) because "it's easier than figuring out the exact actions" | Start with `ReadOnlyAccess` and add specific actions as needed based on actual API calls (use IAM Access Analyzer to identify required permissions). Wildcards are the #1 cause of privilege escalation paths. A compromised Lambda with `s3:*` can read, write, and delete every bucket in the account. |
| Disabling IMDSv2 on EC2 instances because "the legacy app needs IMDSv1" | Migrate the legacy app to IMDSv2 (session-oriented metadata access) or isolate it in a separate subnet with additional network controls. IMDSv1 is vulnerable to SSRF attacks that can leak IAM credentials — the Capital One breach exploited exactly this weakness. |
| Running vulnerability scans but never building an SBOM or tracking transitive dependencies | Generate an SBOM (CycloneDX/SPDX) for every application and store it alongside the build artifact. Transitive dependencies are the silent attack surface — Log4Shell was a transitive dependency in thousands of applications that "didn't use Log4j directly." |

<!-- DEEP: 10+min -->
## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---------|------------|-----|--------|
| Production database exfiltrated via unpatched Log4j CVE-2021-44228 | Critical CVE known for 3 months; patch not applied because "it's just a library" with no ownership assigned | Implement SLA-driven patch policy (critical within 24 hours, high within 7 days); assign CVE ownership per service; automate dependency scanning in CI | Every unpatched critical CVE is a ticking time bomb -- the attacker doesn't care that you were "about to get to it" |
| AWS root access key found in public GitHub repo | Developer committed `.env` file with hardcoded credentials; no pre-commit hooks or secret scanning in place | Deploy pre-commit hooks (detect-secrets, gitleaks); scan all repos with secret scanning; rotate exposed credentials immediately; use IAM roles instead of keys | Secrets in source code are the #1 initial access vector for cloud breaches -- automation must catch them before git push, not after |
| 2 million customer records exposed via public S3 bucket | Bucket policy set to `Allow *` with `Principal: *` for ease of data sharing; no bucket-level block public access enabled | Enable S3 Block Public Access at account level; implement automated bucket policy scanner (CloudSploit, ScoutSuite); tag sensitive data buckets for extra monitoring | The convenience of a public bucket is never worth the headline: "Company exposes customer data" -- default-deny is the only safe default for cloud storage |
| SSRF vulnerability allowed attacker to access internal metadata service | Web app accepted user-supplied URLs without validation; no outbound network segmentation; IMDSv1 left enabled on EC2 instances | Validate and allowlist all user-supplied URLs; deploy outbound proxy with allowlist; migrate to IMDSv2; implement network segmentation for metadata endpoints | SSRF is the gift that keeps giving because internal services are trusted by default -- every user-supplied URL is a potential bridge to internal infrastructure |
| S3 bucket with sensitive customer data exposed | S3 bucket misconfigured as public; no automated S3 bucket policy scanning in CI/CD | Enable S3 Block Public Access at account level. Use IAM Access Analyzer for S3. Scan all buckets weekly with ScoutSuite or Prowler. Never store customer data in public buckets. | A FinTech startup exposed 500K customer records including SSNs through a public S3 bucket used for "temporary" file storage. Discovered by a security researcher. Cost: $5M settlement + mandatory 36-month credit monitoring for affected customers. |
| Log4Shell (CVE-2021-44228) missed in vulnerability scan | SBOM wasn't maintained; dependency tree included Log4J through a transitive dependency that the scanner didn't flag | Maintain a Software Bill of Materials (SBOM) for every application. Use a vulnerability scanner that supports transitive dependency analysis (Snyk, Trivy, Dependabot). Subscribe to CVE feeds for critical libraries. | A startup lost 2 weeks rebuilding their entire Docker image stack after discovering Log4J in a transitive dependency. The fix was deployed 14 days after the PoC was public -- their company name appeared in the breach notification lawsuit. |
| API key committed to public GitHub repo | Developer hardcoded an API key in config file and committed without .gitignore protection | Implement pre-commit hooks (git-secrets, truffleHog) that scan for secrets before allowing commits. Use organization-level secret scanning on all repos. Rotate any committed credential immediately. | A company's AWS root access key was committed in a public repo. Within 24 hours, a bot discovered it and spun up 200 GPU instances for crypto mining. The bill: $87K in 3 days before the key was disabled. |
| Zero-day exploit in third-party library caused data exfiltration | No runtime application self-protection (RASP); no egress network restrictions | Implement allow-listed egress network policies. Use RASP or WAF for runtime protection. Monitor unusual outbound data volumes with network detection and response (NDR). | A collaboration software vendor had a zero-day RCE in their file parser. Attackers exfiltrated 2GB of customer data over 3 months through the file processing service -- no one monitored egress traffic. |
| SSRF vulnerability allowed access to internal metadata service | Cloud metadata service (169.254.169.254) not blocked at instance level; no IMDSv2 enforcement | Enforce IMDSv2 (session-oriented metadata access). Block 169.254.169.254 access from application code. Use a web application firewall with SSRF prevention rules. Network-segment metadata service access. | Capital One breach (2019): SSRF in a WAF allowed access to the metadata service, which returned IAM credentials for an S3 read role. 100M+ records exposed. The fix: IMDSv2 + network-level blocking of metadata service from app containers. |


## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  Threat model documented for all tier-1 services; reviewed within the last 6 months
- [ ] **[S2]**  SAST, SCA, and container scanning integrated into CI pipeline; critical/high findings block merge
- [ ] **[S3]**  DAST scanning runs weekly against staging; results triaged and remediated
- [ ] **[S4]**  API gateway enforces authentication, authorization, rate limiting, and input validation
- [ ] **[S5]**  IAM: no long-lived credentials, MFA for all humans, least-privilege roles, quarterly access reviews
- [ ] **[S6]**  Secrets management: centralized vault, auto-rotation enabled, pre-commit hooks detect plaintext secrets
- [ ] **[S7]**  Network: default-deny policies, WAF deployed, DDoS protection active, mTLS for east-west traffic
- [ ] **[S8]**  SIEM aggregating all security logs; detection rules aligned to MITRE ATT&CK framework
- [ ] **[S9]**  Incident response playbooks documented and tabletop-exercised annually
- [ ] **[S10]**  Vulnerability disclosure program and bug bounty policy published

## References
<!-- QUICK: 30s -- links to deeper reading -->
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- MITRE ATT&CK Framework: https://attack.mitre.org/
- NIST Zero Trust Architecture (SP 800-207): https://www.nist.gov/publications/zero-trust-architecture
- OWASP Application Security Verification Standard (ASVS): https://owasp.org/www-project-application-security-verification-standard/
- HashiCorp Vault Best Practices: https://developer.hashicorp.com/vault/docs/enterprise/best-practices
