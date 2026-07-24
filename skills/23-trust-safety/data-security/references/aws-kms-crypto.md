# AWS KMS Cryptographic Details

## Overview
AWS Key Management Service (KMS) provides managed HSM-backed key storage with automatic rotation and fine-grained access control via IAM and key policies.

## Key Hierarchy
1. **Data Encryption Key (DEK)**: Encrypts actual data (row-level, file-level)
2. **Key Encryption Key (KEK)**: Encrypts DEKs, stored in KMS
3. **Master Key (CMK)**: AWS-managed or customer-managed, never leaves HSM

## Envelope Encryption
1. Generate DEK (plaintext + encrypted copy) via KMS GenerateDataKey
2. Encrypt data with plaintext DEK using AES-256-GCM
3. Store encrypted DEK alongside ciphertext
4. Discard plaintext DEK immediately
5. Decrypt: call KMS Decrypt on encrypted DEK

## Key Rotation
- AWS-managed CMK: Automatic every 365 days
- Customer-managed CMK: Optional, automatic yearly rotation available
- Imported key material: Manual rotation required

## Grant-Based Access
- Temporary, narrowly-scoped delegation
- Lower latency than key policy evaluation
- Common for batch encryption/decryption at scale

## References
- AWS KMS Developer Guide: https://docs.aws.amazon.com/kms/latest/developerguide/
