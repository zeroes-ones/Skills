# Scale Depth: Solo → Small → Medium → Enterprise

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
