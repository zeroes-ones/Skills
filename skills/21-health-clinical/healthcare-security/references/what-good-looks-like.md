# What Good Looks Like — Healthcare Security

BEFORE/AFTER comparisons for common healthcare security scenarios.

## BEFORE: Naive Cloud Deployment for PHI

```
AWS Account
├── S3 Bucket (no encryption) with MRI images
├── RDS PostgreSQL (no encryption at rest) with patient records
├── EC2 web server (TLS 1.0, self-signed cert)
├── Lambda for HL7 message processing (logs full PHI to CloudWatch)
└── No BAA with AWS, no network segmentation
```

**Findings:** 14 HIPAA Security Rule violations. Encryption absent everywhere.
PHI in plaintext logs replicated across 3 regions. BAA not executed with
AWS — every AWS service processing PHI is a compliance liability.

## AFTER: HIPAA-Compliant Architecture

```
AWS Account (BAA executed & current)
├── S3 Bucket (AES-256 SSE-KMS, CMK rotation 90d, versioning, MFA delete)
│   ├── MRI images encrypted at rest, access logs to dedicated CloudTrail
│   └── Lifecycle policy: 7yr retention, then glacier with legal hold
├── RDS PostgreSQL (encryption at rest with CMK, TLS 1.2+ sslmode=verify-full)
│   ├── Column-level encryption for SSN, MRN via pgcrypto
│   ├── Audit logging (pgaudit) to isolated S3 bucket
│   └── Automated backups encrypted, cross-region replication encrypted
├── ALB (TLS 1.2+, HSTS, WAF with OWASP rules) → EC2 (no local PHI storage)
├── Lambda (structured JSON logging, PHI redaction middleware strips
│   patient identifiers before CloudWatch)
└── VPC segmentation: PHI subnet (private, no internet), DMZ (public ALB only),
    management subnet (bastion + monitoring)
```

**Result:** All 14 violations resolved. Encryption at rest and in transit
enforced everywhere. PHI never reaches logs. BAA covers all AWS services.
Network segmentation limits blast radius.

## BEFORE: Medical Device Network — Flat

```
Single VLAN: 192.168.1.0/24
├── Nurse workstations (Windows 10)
├── Infusion pumps (Windows 7, EOL 2020)
├── MRI controller (Windows XP, no patches since 2014)
├── PACs server
├── Guest WiFi bridge
└── Internet gateway
```

## AFTER: Segmented Clinical Network

```
IoMT VLAN (10.10.0.0/24): Infusion pumps, MRI controller, patient monitors
  → No internet. Inline IPS. NAC whitelist. CBOM inventory.
Biomed VLAN (10.20.0.0/24): PACS, imaging workstations, device management
  → Proxy-only internet. Application whitelisting.
Clinical VLAN (10.30.0.0/24): Nurse workstations, EHR thin clients
  → Internet via authenticated proxy. EDR on every endpoint.
Guest VLAN (10.99.0.0/24): Patient/visitor WiFi
  → Internet only. No route to any clinical VLAN.
Corporate VLAN (10.50.0.0/24): Admin, billing, email
  → Standard enterprise controls.
```

## BEFORE: De-identification — "We Removed Names"

Dataset published for research. Names removed. ZIP codes, DOB, and gender
retained. Re-identification attack linked 87% of records to named individuals
within 48 hours.

## AFTER: Safe Harbor De-identification with Audit Trail

All 18 identifiers removed (DICOM headers scrubbed, FHIR extensions filtered,
free-text notes reviewed). Data Use Agreement prohibits re-identification.
Statistical disclosure risk assessment completed. Audit trail documents each
removal. Expert Determination certification on file for edge cases.
