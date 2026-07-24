# Healthcare Security Production Checklist

## Pre-Deployment
- [ ] Business Associate Agreements signed with ALL vendors handling PHI
- [ ] Encryption at rest configured and validated (AES-256-GCM minimum)
- [ ] TLS 1.3 enforced, cipher suites restricted, certificate pinning active
- [ ] Audit logging: all PHI access logged with user, patient, timestamp, purpose
- [ ] Access control: RBAC with least privilege, break-glass procedure documented
- [ ] Session management: 15-min idle timeout, JWT rotation, forced re-auth after inactivity
- [ ] PHI data classification labeling complete (direct, limited, de-identified)
- [ ] Vulnerability scan on all production infrastructure (0 critical findings)

## Incident Response Readiness
- [ ] Breach notification procedures documented (HIPAA 60-day rule)
- [ ] PHI breach forensic partner on retainer
- [ ] Communication templates: patients, HHS, media (>500 individuals)
- [ ] Tabletop exercise completed within last 6 months

## Ongoing
- [ ] Monthly access review: who accessed what PHI
- [ ] Quarterly vulnerability scan + penetration test
- [ ] Annual HIPAA Security Risk Assessment (SRA)
- [ ] BAAs reviewed annually — new vendors, expired agreements
