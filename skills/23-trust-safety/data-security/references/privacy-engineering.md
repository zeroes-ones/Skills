# Privacy Engineering

## Overview
Embedding privacy protections into data pipelines and applications. Privacy-by-design — not retrofitted after a breach or audit finding.

## Privacy-by-Design Principles
1. **Data Minimization at Ingestion:** Only collect fields with defined purpose
2. **Purpose Limitation:** Each data use mapped to a declared purpose
3. **Automated Pseudonymization:** Strip direct identifiers at ETL boundary
4. **Storage Limitation:** Automated retention enforcement with legal hold

## DSAR (Data Subject Access Request) API
### Right to Access (GDPR Art. 15)
Automated search across all data stores → JSON export within 30 days.

### Right to Erasure (GDPR Art. 17)
Identify all copies (primary DB, replicas, backups, data lake, analytics).
Delete or irreversibly anonymize. Document proof of erasure.

### Right to Portability (GDPR Art. 20)
Export in structured, machine-readable format: JSON, CSV, Parquet.

## Consent Management
- Capture: granular, purpose-specific consent at collection point
- Propagate: consent preferences flow through data pipelines
- Revoke: processing stops within 30 days of withdrawal

## Privacy-Enhancing Technologies (PETs)
- **Differential Privacy:** Calibrated noise prevents individual re-identification
- **Homomorphic Encryption:** Compute on encrypted data without decrypting
- **Secure Multi-Party Computation:** Joint computation without revealing inputs
- **Federated Learning:** Train models without centralizing raw data
