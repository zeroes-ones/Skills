# Data Classification Frameworks

## Overview
Systematic approach to categorizing data by sensitivity, regulatory requirements, and business impact. Foundation for all data protection decisions — you cannot protect what you do not know you have.

## Classification Taxonomy (4-Tier Standard)

### Public
- Data intentionally shareable with the public
- Examples: marketing materials, press releases, open-source code, public documentation
- Protection: no special controls required

### Internal
- Business-confidential but low impact if exposed
- Examples: meeting notes, project plans, internal wiki, non-sensitive emails
- Protection: access restricted to employees, basic access logging

### Confidential
- Regulated or high business impact
- Examples: PII (names, emails, SSNs), financial records, intellectual property, source code
- Protection: encryption at rest and in transit, access control, audit logging, DLP coverage

### Restricted
- Highest sensitivity — exposure causes severe harm
- Examples: encryption keys, root credentials, biometric data, board minutes, merger documents
- Protection: envelope encryption with HSM, just-in-time access, full session recording, break-glass procedures

## Automated Labeling
- Regex patterns: SSN \\d{3}-\\d{2}-\\d{4}, PAN \\d{4}[- ]?\\d{4}[- ]?\\d{4}[- ]?\\d{4}
- Column name heuristics: columns named "ssn", "password", "credit_card", "dob"
- ML classification: NLP for unstructured documents, data fingerprinting

## Metadata Propagation
- S3 object tags, BigQuery column labels, database comments
- Data catalog integration: AWS Glue, Azure Purview, Collibra, BigID
- Pipeline inheritance: derived datasets auto-tagged from source classification
