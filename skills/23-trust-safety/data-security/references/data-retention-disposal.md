# Data Retention & Secure Disposal

## Overview
Automated data lifecycle management — defining retention periods, enforcing deletion, and securely disposing of data at end-of-life.

## Retention Schedule Design
| Data Category | Retention Period | Regulation |
|---|---|---|
| Financial records | 7 years | IRS, Sarbanes-Oxley |
| Employment records | 7 years post-employment | EEOC |
| Customer PII | 2 years post-relationship | GDPR minimization |
| Security logs | 1-3 years | SOC 2 (1yr), PCI DSS (3yr) |
| Application logs | 30-90 days | Legitimate interest |
| Backups | 30-90 days operational | Business continuity |

## Automated Enforcement
- S3/GCS lifecycle policies with expiration actions
- TTL indexes (MongoDB, DynamoDB)
- PostgreSQL pg_partman partition pruning
- Kafka retention.ms for streaming data
- Legal hold override: flag in data catalog blocks automated deletion

## Secure Disposal Methods
### Cryptographic Erasure (Crypto-Shredding)
Destroy the KEK → all DEKs become unrecoverable → all data effectively erased.
Advantage: instant, provable (KMS audit trail), scalable.

### NIST SP 800-88 Media Sanitization
- **Clear:** Logical overwrite — same-organization reuse
- **Purge:** Cryptographic erase or block-level overwrite — decommissioning
- **Destroy:** Physical destruction — highest classification, end-of-life drives

## Verification
Quarterly deletion tests: verify data is unrecoverable after disposal.
Audit trail: proof of deletion with timestamp, method, and verifier.
