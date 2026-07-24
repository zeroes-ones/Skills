# OWASP ASVS Mapping to SDLC

## Verification Level Selection

| Level | Name | Requirements | Verification Method | Appropriate For |
|-------|------|-------------|---------------------|-----------------|
| L1 | Opportunistic | ~32 | Automated (SAST + DAST) | Internal tools, low-risk apps, informational websites |
| L2 | Standard | ~112 | Automated + Manual review of auth/crypto/session code + Pen test | B2B SaaS, e-commerce, healthcare PHI, financial PII |
| L3 | Advanced | ~230+ | All L2 methods + Architecture review + Formal methods + Red team | Banking, payments, critical infrastructure, national security |

## SDLC Phase Mapping (L2 Example)

### Design Phase (V1: Architecture, Design, Threat Modeling)
- V1.1: Secure Software Development Lifecycle -- documented process, security training required
- V1.2: Authentication Architecture -- MFA design, credential recovery flow reviewed
- V1.4: Access Control Architecture -- deny by default, least privilege enforcement points
- V1.5: Input and Output Architecture -- encoding libraries selected, parameterization mandatory
- V1.11: Business Logic Architecture -- separation of duties, transaction limits, anti-fraud checks

### Development Phase (V2-V8: Technical Controls)
- V2: Authentication -- password policy (NIST SP 800-63B), MFA, credential recovery, brute force protection
- V3: Session Management -- cookie attributes, fixation prevention, logout, idle timeout
- V4: Access Control -- IDOR prevention, privilege escalation prevention, CORS, JWT validation
- V5: Validation, Sanitization, Encoding -- parameterized queries, contextual output encoding, file upload validation
- V6: Cryptography -- approved algorithms only, key management, random number generation
- V7: Error Handling and Logging -- no sensitive data in logs, no stack traces in production
- V8: Data Protection -- encryption at rest, TLS 1.2+ in transit, sensitive data minimization

### Testing Phase (V9-V10: Verification)
- V9: Communications -- TLS configuration, certificate validation, HTTP security headers
- V10: Malicious Code -- dependency scanning, integrity verification, malware detection

### Operations Phase (V11-V14: Operational Controls)
- V11: Business Logic -- anti-automation, transaction integrity, workflow enforcement
- V12: Files and Resources -- file upload limits, path traversal prevention, SSRF prevention
- V13: API and Web Services -- REST/GraphQL security, rate limiting, API versioning
- V14: Configuration -- secure defaults, no debug in production, CORS allowlist, CSP

## Verification Workflow

1. Sprint begins: Identify new features. Cross-reference ASVS requirements.
2. Development: SAST + secret scanning in CI. Block on HIGH/CRITICAL findings.
3. Code review: Security reviewer validates authN, authZ, input validation against ASVS checklist.
4. QA: DAST baseline on staging. Manual test cases for ASVS requirements not testable by automation.
5. Pre-release: Security sign-off. Evidence package: SAST results + DAST results + code review sign-off.
6. Quarterly: Full ASVS re-verification. Evidence collected and archived for audit trail.
