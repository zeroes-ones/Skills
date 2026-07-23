# Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Security review = run `npm audit` / `pip audit`. Check for hardcoded secrets. Don't use `eval()`. Use parameterized queries. Use HTTPS. That's it.
- **What to skip**: STRIDE threat modeling. OWASP Top 10 full assessment. Penetration testing. SAST/DAST tools. Security review process. Compliance frameworks. Dependency audit beyond `audit`.
- **Coordination**: You review your own code. No coordination needed.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Lightweight security review for auth, payment, and PII code. OWASP Top 10 checklist (critical items). Automated dependency scanning (Dependabot/Snyk). Secrets detection in CI (truffleHog/gitleaks). Basic CSP headers. Input validation review.
- **What to skip**: Full STRIDE threat model. Penetration testing. SAST/DAST pipeline. Compliance mapping. SBOM generation. Container scanning.
- **Coordination**: Security reviewer assigned for sensitive PRs. Weekly security check-in. Security findings in shared backlog.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Dedicated security reviewer. STRIDE threat model for critical components. SAST in CI (Semgrep/CodeQL). DAST for deployed environments. Dependency scanning with SLA for fixes. Container image scanning. OWASP Top 10 full assessment per release. Compliance mapping (SOC 2, GDPR). SBOM generation. Security review process with gates.
- **What to skip**: Full-time security team (1-2 specialists is enough). Penetration testing every release. Bug bounty program. Red team exercises.
- **Coordination**: Security review required for auth/payment/PII changes. Monthly security posture review. Vulnerability management process.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Security team (3+ engineers). Full SSDLC (secure software development lifecycle). STRIDE threat model for all components. SAST + DAST + IAST + SCA in CI/CD. Penetration testing per release + annual external audit. Bug bounty program. Red team exercises. Compliance automation (SOC 2, PCI DSS, HIPAA, FedRAMP). Security champions program. Incident response team.
- **What's full production**: Security operations center (SOC). Continuous security monitoring. Automated compliance evidence collection. Threat intelligence integration. Secure code training program.
- **Coordination**: Weekly security review. Monthly threat modeling session. Quarterly penetration test. Annual compliance audit. Incident response drills quarterly.

### Transition Triggers
- **Solo → Small**: First security incident or enterprise customer asking about security practices.
- **Small → Medium**: SOC 2 or compliance audit required. First penetration test finding critical issues. >10K users.
- **Medium → Enterprise**: Regulatory compliance (PCI DSS, HIPAA, FedRAMP). Public breach in similar company. >100K users.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | backend-developer | Feature implementation with auth/data handling |
| **This** | security-reviewer | Vulnerability report with CVSS scores and reproduction steps |
| **After** | security-engineer | Remediation plan and security control hardening |

Common chains:
- **Chain**: backend-developer → security-reviewer → security-engineer — Security review finds vulnerabilities; security engineer designs fixes
- **Chain**: devops-engineer → security-reviewer → compliance-officer — Infrastructure reviewed for security gaps; compliance validates against frameworks (SOC 2, PCI DSS)
