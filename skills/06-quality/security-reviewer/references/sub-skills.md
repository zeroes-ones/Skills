# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `auth-security-review` | JWT/OAuth2/SAML/OIDC implementation, session management, MFA bypass attempts | Token validation gaps, algorithm confusion, missing claims verification, session fixation, CSRF |
| `injection-defense-review` | SQL, NoSQL, command injection, LDAP, XSS, SSTI, path traversal | Parameterization audit, ORM escape analysis, context-aware encoding, CSP bypass testing |
| `data-protection-review` | PII/PHI handling, encryption at rest/transit, data minimization, logging | Field classification, KMS key management, TLS configuration, PII-in-logs grep, GDPR/CCPA retention |
| `api-security-review` | REST/GraphQL/gRPC endpoint hardening, rate limiting, CORS, mass assignment | Auth middleware coverage (every endpoint), input allowlists, CORS origin validation, resource ownership checks |
| `dependency-audit` | SBOM generation, CVE triage, supply chain risk, transitive dependency analysis | `npm audit`/`pip audit`/`govulncheck`, reachability analysis, pinned versions, lockfile integrity |
| `container-iac-review` | Dockerfile hardening, Kubernetes manifests, Terraform/Pulumi security | Non-root containers, read-only fs, capability dropping, least-privilege IAM, network policy audit |
| `mobile-security-review` | React Native/Flutter/native app security: storage, transport, code integrity | Keychain/Keystore usage, cert pinning, ProGuard/R8 rules, root/jailbreak detection, screenshot blocking |
| `threat-modeling` | STRIDE per component during code review (not just architecture diagrams) | Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege |
