# Healthcare Security Audit Checklist

Production readiness checklist for healthcare systems processing PHI. Run
before deployment, after major changes, and quarterly for existing systems.

## PHI Data Protection

- [ ] All PHI at rest encrypted with AES-256 (KMS CMK, not default service key)
- [ ] All PHI in transit over TLS 1.2+ with valid certificates
- [ ] Database connections use `sslmode=verify-full` (no `sslmode=disable`)
- [ ] S3/Blob Storage bucket policies deny unencrypted PUTs
- [ ] Column-level encryption for SSN, MRN, and financial account numbers
- [ ] Backup encryption enabled and verified (restore test performed)
- [ ] Encryption key rotation configured (90-day automatic rotation)

## Access Control

- [ ] Role-based access control (RBAC) with least privilege per role
- [ ] Multi-factor authentication on all PHI-accessing systems
- [ ] Emergency access procedure (break-glass) for clinical continuity
- [ ] Session timeout: 15 minutes idle, 12-hour hard limit
- [ ] Access review: quarterly for clinical staff, monthly for elevated privileges
- [ ] Deprovisioning: automated account disable within 24 hours of termination

## Audit Logging

- [ ] All PHI access logged (who, what, when, source IP, outcome)
- [ ] Audit logs immutable (append-only, WORM storage)
- [ ] Audit log integrity verified (hash chain or blockchain anchoring)
- [ ] PHI absent from application logs (pre-deployment grep verified)
- [ ] Log retention: 6 years minimum (HIPAA requirement)
- [ ] Alerting: anomalous access patterns (off-hours, bulk export, new IP)

## Network Segmentation

- [ ] Separate VLANs: IoMT, Biomed, Clinical, Guest, Corporate
- [ ] Default-deny ACLs between all clinical segments
- [ ] No internet access from IoMT VLAN (or proxy + DPI + IPS only)
- [ ] NAC in place — unknown devices blocked at port level
- [ ] East-west traffic monitoring between segments (NetFlow/IPFIX)

## BAA Compliance

- [ ] All PHI-processing vendors have signed, current BAAs
- [ ] BAA registry updated within last quarter
- [ ] Sub-processor lists reviewed for all BAAs
- [ ] BAA expiration alerts configured (90-day advance notice)
- [ ] New vendors screened for BAA requirement before PHI access

## Medical Device Security

- [ ] Complete inventory of all network-connected medical devices
- [ ] CBOM requested from manufacturers for all devices
- [ ] Vulnerability scanning operational on biomed VLAN
- [ ] EOL devices identified with replacement timelines
- [ ] No devices on unsupported OS without compensating controls

## Breach Readiness

- [ ] Breach notification pipeline documented and tested in last 12 months
- [ ] Contact lists current (patients, media, OCR)
- [ ] Notification templates drafted and legal-reviewed
- [ ] Incident response plan includes clinical continuity procedures
- [ ] Cyber insurance policy reviewed — ransomware coverage confirmed

## API Security (EHR/FHIR)

- [ ] SMART on FHIR with OAuth 2.0 implemented
- [ ] Resource-level scopes enforced (not `patient/*` wildcard)
- [ ] Psychotherapy notes require separate, explicit authorization
- [ ] Rate limiting configured (100 req/min per client default)
- [ ] API gateway WAF with OWASP healthcare-specific rules enabled
