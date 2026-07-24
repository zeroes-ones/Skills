# GCP Cloud KMS — Symmetric and Asymmetric Encryption

## Overview
Google Cloud KMS provides key management with automatic rotation, HSM backing (Cloud HSM), and integrates with GCP services for encryption at rest.

## Key Types
- **Symmetric**: AES-256-GCM (software) or AES-256-CBC+HMAC (HSM)
- **Asymmetric**: RSA 2048/3072/4096, EC P-256/P-384 for sign/decrypt

## Protection Levels
- **SOFTWARE**: Keys protected in software (FIPS 140-2 Level 1)
- **HSM**: Keys in dedicated HSM cluster (FIPS 140-2 Level 3)

## Key Hierarchy
```
Key Ring → Key → Key Version
```
- **Key Ring**: Organizational container (per project, location)
- **Key**: Named cryptographic key with purpose and rotation policy
- **Key Version**: Specific key material version (1, 2, 3...)

## Automatic Rotation
- Symmetric keys: Optional, default 90-day rotation
- Keeps key version history for decryption of old data
- Primary version used for new encryption operations

## IAM Integration
- `roles/cloudkms.cryptoKeyEncrypterDecrypter`
- `roles/cloudkms.admin`
- Granular per-key, per-version permissions

## References
- Cloud KMS: https://cloud.google.com/kms/docs
