# SOC 2 Readiness — Orchestra Platform

## Framework & Timeline

Orchestra is pursuing **SOC 2 Type I** (point-in-time assessment of control design), with a target of achieving **Type II** (6-month observation of control effectiveness) within 12 months of Type I completion.

**Timeline**: Type I audit starts in 3 months. The Type II observation period begins the day after the Type I report is issued.

## Trust Services Criteria

Orchestra's SOC 2 scope covers three of the five Trust Services Criteria:

| Criteria | Covered? | Key Controls |
|---|---|---|
| **Security** | ✅ Full | Access control, encryption, vulnerability management, network segmentation |
| **Availability** | ✅ Full | Monitoring, alerting, disaster recovery, capacity planning |
| **Confidentiality** | ✅ Full | Encryption at rest (AES-256 via KMS), encryption in transit (TLS 1.3), data classification policy |
| Processing Integrity | ❌ Out of scope | — |
| Privacy | ❌ Out of scope | — |

## Control Inventory — 32 Controls Across 5 Domains

### Information Security (8 controls)
- Access control policy (documented, reviewed annually)
- Encryption standards (AES-256 at rest, TLS 1.3 in transit)
- Vulnerability management (weekly scans, 30-day remediation SLA for HIGH, 7-day for CRITICAL)
- Security awareness training (onboarding + annual refresher)
- Asset inventory (automated via AWS Config)
- Data classification policy (public, internal, confidential, restricted)
- Acceptable use policy
- Third-party risk management program

### Access Control (6 controls)
- Role-based access control (RBAC) with documented role definitions
- Multi-factor authentication enforced for all human users
- Quarterly access reviews (currently semi-automated — see gaps below)
- Structured offboarding process (revoke within 4 hours of termination)
- Privileged access management (break-glass accounts with audit logging)
- Password policy (minimum 16 characters, no expiration per NIST 800-63B)

### Change Management (7 controls)
- Pull request required for all production changes
- Mandatory code review by a second engineer
- CI/CD pipeline gates (tests, lint, container scan)
- Change approval for production deployments (manual approval gate)
- Infrastructure changes require `terraform plan` review
- Rollback plan documented for every production change
- Separation of duties — engineer who merges cannot approve their own PR

### Risk Management (5 controls)
- Risk register maintained in Notion, reviewed quarterly
- Quarterly risk assessment with engineering leadership
- Vendor risk reviews (annual for critical vendors, bi-annual for others)
- Business continuity plan (tested annually)
- Insurance review (annual)

### Monitoring & Response (6 controls)
- Centralized logging with immutable storage (Loki, 30-day retention)
- Alert routing and escalation policy (P1/P2/P3 with PagerDuty)
- Incident response plan (documented, tabletop-tested quarterly)
- Quarterly incident response tests (simulated scenarios)
- Vulnerability disclosure program (security@orchestra.io)
- Penetration testing (annual, external firm)

## Evidence Collection

Evidence is gathered through two channels:

- **Automated** — Drata integrates with AWS, GitHub, PagerDuty, and the HR system to collect continuous evidence (MFA status, access reviews, vulnerability scan results, alert acknowledgements).
- **Manual** — quarterly screenshots and document exports for controls without API integration (risk register updates, training completion records, policy review sign-offs).

## Known Gaps (8 Items)

The following gaps are tracked in the compliance backlog and must be resolved before the Type I audit:

1. **RBAC audit trail incomplete** — IAM role changes are logged, but Kubernetes RBAC changes are not centrally collected. Planned: OPA Gatekeeper audit logging.
2. **Quarterly access review not fully automated** — currently a manual spreadsheet export from AWS IAM combined with GitHub team membership. Planned: Drata access review workflow.
3. **Vendor risk assessment pending for Auth0** — contract signed, assessment in progress.
4. **Vendor risk assessment pending for Stripe** — scheduled for next quarter.
5. **Incident response plan not tabletop-tested** — first test scheduled for next month.
6. **Data classification labels not applied to S3 objects** — AWS Macie deployment in progress.
7. **Penetration test report > 12 months old** — new engagement starts next quarter.
8. **Break-glass procedure not documented** — draft in review.
