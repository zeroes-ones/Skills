# Encryption Architecture

## Overview
Multi-layer encryption strategy covering data at rest, in transit, and in use. Defense-in-depth: no single control failure exposes plaintext.

## Envelope Encryption
- **DEK (Data Encryption Key):** Encrypts actual data. Stored encrypted alongside data. Generated per resource.
- **KEK (Key Encryption Key):** Encrypts DEK. Stored in KMS/HSM. Never leaves KMS boundary.
- **Key Hierarchy:** HSM root key → KMS KEK → DEK per resource
- **Rotation:** DEK rotated per resource creation. KEK rotated annually. HSM root key rotated every 2-3 years.

## Encryption Layers
### Transparent Data Encryption (TDE)
- Database-level encryption at storage layer
- Protects against: physical disk theft, backup theft, improper media disposal
- Does NOT protect against: database compromise (attacker with SELECT sees plaintext)

### Column-Level Encryption
- Encrypt specific fields (PII, PHI, PCI)
- Protects against: database dump exfiltration, SQL injection data extraction
- Trade-off: encrypted columns cannot be indexed, searched, sorted, or joined

### Application-Layer Encryption
- Encrypt before data reaches database
- Protects against: database admin compromise, cloud provider access
- Key-per-tenant isolation for multi-tenant SaaS

## KMS Configuration
- Customer-managed keys (SSE-KMS/CMEK) for Confidential and Restricted data
- Separate KMS key per data classification tier
- CloudTrail/Cloud Audit Logs for every encrypt/decrypt operation
- KMS key policy: separate roles for key admin, key usage, and data access
