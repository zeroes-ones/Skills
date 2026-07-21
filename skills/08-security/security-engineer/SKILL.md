---
name: security-engineer
description: Application security, penetration testing, IAM design, secrets management, API security, network security, zero trust, and security monitoring. Triggered by security, pentest, IAM, secrets, zero trust, vulnerability, threat model, API security.
author: Sandeep Kumar Penchala
---

# Security Engineer

Design, implement, and validate security controls across the application, infrastructure, and network
layers. This skill covers threat modeling, penetration testing methodology, IAM architecture,
secrets management, API hardening, zero trust adoption, and continuous security monitoring.

## When to Use

- Conducting threat modeling sessions using STRIDE, PASTA, or attack trees
- Performing penetration tests against web applications, APIs, cloud infrastructure, or mobile apps
- Designing IAM strategies: role-based access control, attribute-based access control, just-in-time access
- Implementing secrets management with HashiCorp Vault, AWS Secrets Manager, or SOPS
- Hardening APIs against OWASP Top 10: injection, broken auth, SSRF, excessive data exposure
- Architecting network security: network policies, WAF, DDoS protection, segmentation
- Adopting zero trust architecture: micro-segmentation, continuous verification, device trust
- Building a security monitoring and detection pipeline (SIEM, SOAR, threat intelligence feeds)

## Decision Trees

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
```

## Core Workflow

### Phase 1: Threat Modeling and Risk Assessment
1. Diagram the system: data flow diagrams (DFDs) showing trust boundaries, external entities, data stores, and processes.
2. Apply STRIDE per element: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.
3. Identify threats and rank by likelihood × impact using a risk matrix (CVSS or custom scoring).
4. Define mitigations: eliminate the threat, reduce likelihood, reduce impact, transfer risk, or accept with justification.
5. Document in a threat model register; review quarterly or on major architectural changes.

### Phase 2: Application and API Security
1. Integrate SAST (Semgrep, SonarQube, CodeQL) into the CI pipeline at PR time; block on critical/high findings.
2. Run SCA (Dependabot, Snyk, OWASP Dependency-Check) to detect vulnerable open-source libraries.
3. Perform DAST (OWASP ZAP, Burp Suite) against staging environments on a schedule and on major releases.
4. Harden API endpoints: implement rate limiting, input validation, output encoding, proper CORS, and content security policies.
5. Enforce authentication and authorization at the API gateway; use OAuth2/OIDC with short-lived tokens and refresh token rotation.
6. Protect against OWASP Top 10: parameterized queries for SQL injection, HTML entity encoding for XSS, strict deserialization.

### Phase 3: Identity and Access Management (IAM)
1. Design role-based access control (RBAC) with well-defined role hierarchies and least-privilege defaults.
2. Implement just-in-time (JIT) access for privileged operations: request, approve, grant temporary elevation, auto-revoke.
3. Use OIDC for service-to-service and CI/CD-to-cloud authentication — no long-lived static credentials.
4. Enforce multi-factor authentication (MFA) for all human users; hardware security keys for administrative roles.
5. Implement permission boundaries and service control policies to limit the blast radius of compromised credentials.
6. Audit IAM quarterly: review unused roles, overly permissive policies, and inactive users; use IAM Access Analyzer or Policy Simulator.

### Phase 4: Secrets Management
1. Centralize secrets in a dedicated vault (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault).
2. Implement dynamic secrets for databases: generate ephemeral credentials on demand, auto-expire within hours.
3. Use envelope encryption: encrypt data with a data key, encrypt the data key with a master key (KMS).
4. Never log, echo, or commit secrets; use pre-commit hooks (detect-secrets, gitleaks) to block accidental exposure.
5. Rotate secrets automatically: database passwords, API keys, TLS certificates — all on a defined rotation schedule.
6. For Kubernetes: use External Secrets Operator or Sealed Secrets; never store raw secrets in etcd without encryption at rest.

### Phase 5: Network Security and Zero Trust
1. Implement micro-segmentation: default-deny network policies, explicit allow rules between specific services.
2. Deploy a Web Application Firewall (AWS WAF, Cloudflare, ModSecurity) with OWASP Core Rule Set; tune to reduce false positives.
3. Protect against DDoS: CloudFront/Cloudflare at the edge, AWS Shield Advanced or equivalent for layer 3/4 protection.
4. Zero trust principles: never trust, always verify — authenticate every request regardless of source network.
5. Use mutual TLS (mTLS) for service-to-service communication; manage certificates with cert-manager or a service mesh.
6. Implement outbound traffic inspection with a forward proxy to detect data exfiltration and command-and-control traffic.

### Phase 6: Security Monitoring and Incident Detection
1. Aggregate logs centrally: CloudTrail, VPC Flow Logs, application logs, WAF logs → SIEM (Splunk, Elastic Security, Sentinel).
2. Define detection rules for common attack patterns: credential brute-force, privilege escalation, data exfiltration, crypto mining.
3. Set up SOAR playbooks for automated triage: enrich alerts with threat intelligence, quarantine compromised hosts, revoke credentials.
4. Hunt for threats proactively: run hypothesis-driven threat hunts monthly based on threat intelligence and MITRE ATT&CK.
5. Tune alerting to balance signal-to-noise: measure mean time to detect (MTTD) and mean time to acknowledge (MTTA).

## Sub-Skills

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

## Cross-Skill Coordination

Security engineers protect the entire organization — they must coordinate with every development team, DevOps for infrastructure hardening, compliance for regulatory alignment, and incident responders for threat containment.

### Coordinate With

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **All Developers** (Backend, Frontend, Mobile, Fullstack) | Auth design, data protection, dependency management | Security requirements per data classification, approved crypto libraries, secure coding patterns, dependency allowlists |
| **Security Reviewer** | Pre-merge security audits, vulnerability triage | Review scope, risk appetite, findings that need architectural changes; escalate Critical findings for immediate action |
| **DevOps Engineer** | Infrastructure security, secrets management, network policies | Vault/Secrets Manager architecture, security group/NetworkPolicy design, IAM least-privilege, container hardening |
| **Cloud Architect** | Cloud security posture, IAM, encryption | KMS key policies, SCP design, CloudTrail/Audit Log configuration, WAF rules, DDoS protection |
| **CI/CD Builder** | Pipeline security integration | SAST/SCA/DAST tool placement in pipeline, secret scanning, signed commits, SLSA provenance |
| **Compliance Officer** | Control implementation, evidence collection | Technical control evidence, vulnerability management metrics, audit preparation support |
| **Incident Responder** | Threat detection, incident response | Detection rules, SOAR playbooks, forensic tooling access, threat intelligence sharing |

### Communication Triggers

| Trigger | Notify | Why |
|---------|--------|-----|
| Critical CVE affecting production dependency | All service owners, DevOps, CI/CD Builder | Coordinated patching; assess exploitability and blast radius |
| Security incident detected (breach, data leak, active attack) | Incident Responder, Compliance Officer, CTO | Immediate war room; legal notification assessment |
| New security tool/control being deployed (WAF, IDS, DLP) | DevOps, Cloud Architect, All developers | Integration impact; potential false positives during tuning period |
| Password/secret policy change | All developers, DevOps | Tooling update; CI secret scanning may flag newly non-compliant secrets |
| Zero-day affecting a technology in our stack | All service owners, Incident Responder | Emergency assessment; mitigations while patch is unavailable |

### Escalation Path

```
Active security breach? → Incident Responder (declare SEV1) → CISO → CTO
Regulatory non-compliance? → Compliance Officer → Legal Advisor → CEO
Critical vulnerability unpatched > SLA? → Service owner → Engineering Manager → CTO
Security tool outage (WAF down, IDS offline)? → DevOps → Cloud Architect
```

## Best Practices

- **Shift left**: security testing in the IDE and at PR time; don't wait for staging or production scans.
- **Defense in depth**: no single control should be the only line of defense; layer preventive, detective, and corrective controls.
- **Assume breach**: design systems to limit blast radius, detect intrusions quickly, and recover gracefully.
- **Secrets never travel in plaintext**: encrypt in transit (TLS) and at rest (KMS); use ephemeral credentials whenever possible.
- **Patch aggressively**: automate OS and dependency patching; SLA: critical patches within 24 hours, high within 7 days.

## Production Checklist

- [ ] Threat model documented for all tier-1 services; reviewed within the last 6 months
- [ ] SAST, SCA, and container scanning integrated into CI pipeline; critical/high findings block merge
- [ ] DAST scanning runs weekly against staging; results triaged and remediated
- [ ] API gateway enforces authentication, authorization, rate limiting, and input validation
- [ ] IAM: no long-lived credentials, MFA for all humans, least-privilege roles, quarterly access reviews
- [ ] Secrets management: centralized vault, auto-rotation enabled, pre-commit hooks detect plaintext secrets
- [ ] Network: default-deny policies, WAF deployed, DDoS protection active, mTLS for east-west traffic
- [ ] SIEM aggregating all security logs; detection rules aligned to MITRE ATT&CK framework
- [ ] Incident response playbooks documented and tabletop-exercised annually
- [ ] Vulnerability disclosure program and bug bounty policy published

## References

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- MITRE ATT&CK Framework: https://attack.mitre.org/
- NIST Zero Trust Architecture (SP 800-207): https://www.nist.gov/publications/zero-trust-architecture
- OWASP Application Security Verification Standard (ASVS): https://owasp.org/www-project-application-security-verification-standard/
- HashiCorp Vault Best Practices: https://developer.hashicorp.com/vault/docs/enterprise/best-practices
