# Data Masking & Tokenization

## Overview
Techniques for protecting sensitive data in non-production environments, analytics, and payment systems while maintaining data utility.

## Static Data Masking (SDM)
Permanent masking applied when copying production data to non-production.
- **Format-Preserving Encryption (FPE):** Preserves format and referential integrity
- **Substitution:** Realistic fake data from Faker library
- **Shuffling:** Randomize within column — preserves statistical distributions
- **Nullification:** Simplest, breaks foreign keys

## Dynamic Data Masking (DDM)
Real-time masking based on user role — data remains unmasked in storage.
- SQL Server DDM, PostgreSQL anon extension, BigQuery policy tags
- Support agent sees: j***@domain.com, ***-**-1234
- Privileged user sees full data with audit trail

## Tokenization
Replace sensitive data with non-sensitive surrogate tokens.
- **Vault-based:** Token ↔ value mapping in secure vault (PCI standard)
- **Vaultless:** HMAC-based deterministic tokens — no vault needed
- **Format-preserving:** Token maintains original format for legacy compatibility

## Advanced Techniques
### k-Anonymity
Each record indistinguishable from at least k-1 others. Suppress or generalize quasi-identifiers.

### Differential Privacy
Add calibrated noise to query results. Guarantees individual privacy with ε-differential privacy budget.
