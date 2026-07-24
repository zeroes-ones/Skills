# Google Cloud DLP — Data Inspection and Classification

## Overview
Cloud Data Loss Prevention (DLP) provides sensitive data inspection, classification, and de-identification across structured and unstructured data.

## Inspection Capabilities
- **Built-in infoTypes**: 150+ detectors (PII, PHI, PCI, credentials, demographics)
- **Custom infoTypes**: Regex, word lists, dictionaries
- **Inspection rulesets**: Exclusion rules, hotword rules, likelihood thresholds
- **Context-aware scanning**: Increased accuracy with surrounding text analysis

## De-identification Methods
- **Masking**: Replace characters with fixed character (XXXX)
- **Tokenization**: Replace with surrogate value (vault-based or deterministic)
- **Encryption**: Format-preserving (FFX) or wrap with KMS key
- **Bucketing**: Generalize values (age ranges, IP prefixes)
- **Date shifting**: Shift dates by random interval while preserving sequence

## Service Integration
- **Storage**: Scan BigQuery, Cloud Storage, Datastore
- **Streaming**: Content API for inline inspection
- **Hybrid**: Discovery for structured/unstructured data

## Risk Analysis
- Numerical risk score per finding
- Aggregate sensitivity analysis across datasets
- Re-identification risk metrics (k-anonymity, l-diversity)

## References
- Cloud DLP: https://cloud.google.com/dlp/docs
