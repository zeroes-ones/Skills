# Healthcare Security Calibration

## Skill Implementation Verification
Run these checks after every healthcare-security invocation:

- [ ] PHI identified and classified correctly (direct identifier vs limited dataset vs de-identified)
- [ ] Threat model covers BOTH HIPAA Security Rule AND Privacy Rule
- [ ] BREACH protocol: response plan includes 60-day notification timeline
- [ ] Audit trail: all PHI access logged, immutable, searchable by patient
- [ ] Encryption: at rest (AES-256-GCM) and in transit (TLS 1.3), keys managed in HSM/KMS
- [ ] FHIR/SMART on FHIR: scopes validated, token expiration < 1 hour, refresh rotation

## Common Calibration Failures
| Failure | Detection | Fix |
|---------|-----------|-----|
| PHI in debug logs | grep for MRN patterns, SSN format | PII redaction middleware |
| Unscoped FHIR tokens | Token introspection shows patient/* scope | Scope to specific resources |
| Missing BAA | Vendor list vs signed BAA registry | Initiate BAA before data sharing |
