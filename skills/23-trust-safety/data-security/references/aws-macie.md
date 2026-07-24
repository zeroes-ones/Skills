# AWS Macie — Sensitive Data Discovery and Classification

## Overview
Amazon Macie is a managed data security service that uses machine learning and pattern matching to discover and classify sensitive data in S3 buckets.

## Detection Capabilities
- **Managed data identifiers**: PII (names, SSN, credit cards), PHI, credentials, financial
- **Custom data identifiers**: Regex patterns for organization-specific data
- **ML-based classification**: Automatically identifies sensitive documents
- **S3 Bucket inventory**: Continuous monitoring of bucket security posture

## Classification Process
1. **Discovery**: Automated daily scan of S3 buckets
2. **Sensitive data findings**: PII, PHI, PCI, credentials flagged
3. **Severity scoring**: High/Medium/Low based on data type + volume
4. **Policy findings**: Public access, encryption status, sharing

## Key Features
- **Automated sensitive data discovery**: No manual rules for common data types
- **S3 bucket-level analytics**: Encryption, public access, sharing status
- **Multi-account**: Macie delegated administrator for Organizations
- **Findings to EventBridge**: Automated remediation (quarantine, encrypt, notify)

## Pricing
- Per GB of S3 data scanned per month
- Per S3 bucket for bucket-level analysis

## References
- Amazon Macie: https://aws.amazon.com/macie/
