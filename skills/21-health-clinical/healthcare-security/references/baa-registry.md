# BAA Registry — Business Associate Agreement Management

A Business Associate Agreement (BAA) is required under HIPAA for any entity
that creates, receives, maintains, or transmits PHI on behalf of a covered
entity. The conduit exception is narrow and easily lost. This registry template
ensures every vendor relationship is tracked and compliant.

## BAA Registry Schema

| Field | Description | Example |
|---|---|---|
| Vendor Name | Legal entity name | Amazon Web Services, Inc. |
| Service/Product | What service processes PHI | AWS S3 (object storage) |
| BAA Status | Signed, Pending, Expired, Not Offered | Signed |
| BAA Execution Date | Date BAA was executed | 2025-01-15 |
| BAA Expiration | Expiration or renewal date | 2026-01-15 (annual review) |
| PHI Data Types | What PHI the vendor handles | DICOM images, patient demographics |
| Sub-processors | Vendors used by the BA that also touch PHI | AWS sub-processors (see AWS DPA) |
| Sub-processor Audit Date | Last review of sub-processor list | 2025-Q3 |
| Encryption at Rest | Is PHI encrypted at rest by vendor? | Yes (SSE-KMS CMK) |
| Encryption in Transit | Is PHI encrypted in transit? | Yes (TLS 1.2+) |
| SOC 2 Type II | Latest SOC 2 report date and result | 2025-06, clean opinion |
| Penetration Test | Latest pen test date and summary | 2025-Q2, 2 medium findings remediated |
| Incident Response SLA | Contractual incident notification timeline | Within 24 hours of confirmed breach |
| Last Audit | Date of internal vendor security review | 2025-08-01 |
| Risk Rating | Low/Medium/High/Critical | Low |
| Notes | Any exceptions, concerns, or compensating controls | N/A |

## Conduit Exception Checklist

A vendor qualifies for the conduit exception (no BAA required) ONLY if ALL
conditions are met:

- [ ] The vendor merely transmits PHI (like a postal service or telecom carrier)
- [ ] The vendor does NOT store PHI (even temporarily beyond transmission latency)
- [ ] The vendor does NOT access, view, or process PHI content
- [ ] The vendor has no persistent copy of PHI after transmission completes

**Common mistake:** Cloud storage (S3, Blob Storage, GCS) NEVER qualifies
for conduit exception — PHI persists on disk.

## Cloud Vendor BAA Availability

| Vendor | BAA Offered? | Notes |
|---|---|---|
| AWS | Yes | Covers core services (S3, RDS, EC2, Lambda, etc.). Must be executed explicitly. |
| Azure | Yes | Available for Azure, Dynamics 365, and M365 enterprise tiers. |
| GCP | Yes | Covers core GCP services. Requires BAA execution per project. |
| Twilio SendGrid | Yes (paid tiers) | Email delivery with PHI requires BAA + dedicated IP. |
| Datadog | Yes (enterprise) | Log management with PHI requires BAA. |
| Snowflake | Yes | Requires enterprise edition with HIPAA compliance package. |

## Quarterly BAA Review Checklist

- [ ] All new vendors from last quarter assessed for BAA requirement
- [ ] Expiring BAAs flagged for renewal (90-day advance notice)
- [ ] Sub-processor lists reviewed for all active BAAs
- [ ] SOC 2 reports reviewed — any qualified opinions escalated
- [ ] Penetration test results reviewed — open findings tracked
- [ ] Incident response contact lists verified for all BAs
- [ ] Changes in vendor service scope re-assessed for PHI exposure
