# Healthcare Security Best Practices

## Defense-in-Depth for PHI
1. **Encrypt at rest (AES-256-GCM) AND in transit (TLS 1.3 only)** — never XOR-only
2. **Role-based access with break-glass** — emergency access audited within 24 hours
3. **Audit all PHI access** — who, what, when, patient ID, purpose
4. **Data minimization** — collect only PHI needed for treatment/payment/operations
5. **Automatic session termination** after 15 minutes idle in clinical settings

## Secure Development Lifecycle for Healthcare
- Threat model every data flow touching PHI (STRIDE-LM)
- Static analysis: Semgrep with healthcare rules, 0 findings
- Penetration test annually + after significant changes
- SBOM for every medical device — track every dependency

## Emergency Access Patterns
- Break-glass: elevated privilege with full audit trail
- Override workflow: nurse can override med admin warning, fully logged
- Downtime mode: local cache of critical orders when EHR unavailable
