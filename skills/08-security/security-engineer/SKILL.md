---
name: security-engineer
description: Application security, penetration testing, IAM design, secrets management, API security, network security, zero trust, and security monitoring. Triggered by security, pentest, IAM, secrets,
  zero trust, vulnerability, threat model, API security.
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
  - incident-responder
  - networking-engineer
  - privacy-engineer
  - security-reviewer
  - system-architect
  - trust-safety-engineer
output:
  type: code
  path_hint: ./
---
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

## Ground Rules — Read First

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
### Phase 1 (~15 min): Threat Modeling and Risk Assessment
1. Diagram the system: data flow diagrams (DFDs) showing trust boundaries, external entities, data stores, and processes.
2. Apply STRIDE per element: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.
3. Identify threats and rank by likelihood × impact using a risk matrix (CVSS or custom scoring).
4. Define mitigations: eliminate the threat, reduce likelihood, reduce impact, transfer risk, or accept with justification.
5. Document in a threat model register; review quarterly or on major architectural changes.

### Phase 2 (~30 min): Application and API Security
1. Integrate SAST (Semgrep, SonarQube, CodeQL) into the CI pipeline at PR time; block on critical/high findings.
2. Run SCA (Dependabot, Snyk, OWASP Dependency-Check) to detect vulnerable open-source libraries.
3. Perform DAST (OWASP ZAP, Burp Suite) against staging environments on a schedule and on major releases.
4. Harden API endpoints: implement rate limiting, input validation, output encoding, proper CORS, and content security policies.
5. Enforce authentication and authorization at the API gateway; use OAuth2/OIDC with short-lived tokens and refresh token rotation.
6. Protect against OWASP Top 10: parameterized queries for SQL injection, HTML entity encoding for XSS, strict deserialization.

### Phase 3 (~20 min): Identity and Access Management (IAM)
1. Design role-based access control (RBAC) with well-defined role hierarchies and least-privilege defaults.
2. Implement just-in-time (JIT) access for privileged operations: request, approve, grant temporary elevation, auto-revoke.
3. Use OIDC for service-to-service and CI/CD-to-cloud authentication — no long-lived static credentials.
4. Enforce multi-factor authentication (MFA) for all human users; hardware security keys for administrative roles.
5. Implement permission boundaries and service control policies to limit the blast radius of compromised credentials.
6. Audit IAM quarterly: review unused roles, overly permissive policies, and inactive users; use IAM Access Analyzer or Policy Simulator.

### Phase 4 (~15 min): Secrets Management
1. Centralize secrets in a dedicated vault (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault).
2. Implement dynamic secrets for databases: generate ephemeral credentials on demand, auto-expire within hours.
3. Use envelope encryption: encrypt data with a data key, encrypt the data key with a master key (KMS).
4. Never log, echo, or commit secrets; use pre-commit hooks (detect-secrets, gitleaks) to block accidental exposure.
5. Rotate secrets automatically: database passwords, API keys, TLS certificates — all on a defined rotation schedule.
6. For Kubernetes: use External Secrets Operator or Sealed Secrets; never store raw secrets in etcd without encryption at rest.

### Phase 5 (~25 min): Network Security and Zero Trust
1. Implement micro-segmentation: default-deny network policies, explicit allow rules between specific services.
2. Deploy a Web Application Firewall (AWS WAF, Cloudflare, ModSecurity) with OWASP Core Rule Set; tune to reduce false positives.
3. Protect against DDoS: CloudFront/Cloudflare at the edge, AWS Shield Advanced or equivalent for layer 3/4 protection.
4. Zero trust principles: never trust, always verify — authenticate every request regardless of source network.
5. Use mutual TLS (mTLS) for service-to-service communication; manage certificates with cert-manager or a service mesh.
6. Implement outbound traffic inspection with a forward proxy to detect data exfiltration and command-and-control traffic.

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

## Scale Depth
<!-- QUICK: 30s -- scaling differences at a glance -->
| Aspect | Solo | Small (2-20) | Medium (20-200) | Enterprise (200+) |
|--------|------|-------------|-----------------|-------------------|
| **Threat Modeling** | STRIDE on critical paths only | STRIDE per feature, quarterly review | Continuous threat modeling, PASTA framework | Threat modeling center of excellence, red team exercises |
| **AppSec Tools** | OWASP ZAP + Dependabot (free) | Snyk/Trivy + Semgrep OSS (CI-integrated) | Burp Suite Pro + Snyk Team + custom rules | Full AppSec program: SAST+DAST+IAST+RASP, bug bounty |
| **IAM** | AWS IAM roles, no long-lived keys | RBAC + MFA for all humans | JIT access + OIDC + quarterly access reviews | ABAC + permission boundaries + automated deprovisioning |
| **Secrets Mgmt** | .env in gitignored vault, manual rotation | HashiCorp Vault OSS or cloud secret manager | Vault Enterprise, dynamic secrets, auto-rotation | Multi-region Vault clusters, HSM-backed, envelope encryption |
| **Monitoring** | Cloud-native (CloudTrail + GuardDuty) | Wazuh/Elastic SIEM (OSS) | Splunk/Elastic + SOAR playbooks | Full SOC: SIEM+SOAR+UEBA+threat intel, 24/7 |
| **Team** | Part-time security (dev wears security hat) | 1 dedicated security engineer | Security team (2-3) + security champions | CISO + AppSec + InfraSec + SOC + GRC (8+) |

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

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Shift left**: security testing in the IDE and at PR time; don't wait for staging or production scans.
- **Defense in depth**: no single control should be the only line of defense; layer preventive, detective, and corrective controls.
- **Assume breach**: design systems to limit blast radius, detect intrusions quickly, and recover gracefully.
- **Secrets never travel in plaintext**: encrypt in transit (TLS) and at rest (KMS); use ephemeral credentials whenever possible.
- **Patch aggressively**: automate OS and dependency patching; SLA: critical patches within 24 hours, high within 7 days.


### Error Decoder

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Permission denied` | Missing file/system permissions | Use `chmod +x` or `sudo`; check user/group ownership |
| `command not found` | Required tool not installed | Install with `apt install`, `brew install`, or `npm install -g` |
| `File exists` | Output file already exists | Use `--force` flag or specify different output path |


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
