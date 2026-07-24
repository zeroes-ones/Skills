# Key Management & HSM Reference

## FIPS 140-2 / 140-3 Security Levels

| Level | Protection | Examples | Use Case |
|-------|-----------|----------|----------|
| Level 1 | Software-based, basic crypto module | OpenSSL FIPS module | Development, testing |
| Level 2 | Tamper-evident coatings, role-based auth | TPM 2.0, YubiKey | Per-node TLS keys, disk encryption |
| Level 3 | Tamper-resistant, identity-based auth, physical security | AWS CloudHSM, Thales Luna, nCipher | Root CA, DNSSEC KSK, PCI PIN |
| Level 4 | Tamper-active (self-destruct on intrusion) | Military-grade HSMs | Sovereign key material |

## Key Hierarchy Design

```
Master Key (HSM, offline, M-of-N ceremony)
    |
    +-- Key Encryption Key 1 (KMS, online, rotated annually)
    |       |
    |       +-- DEK 1 (AES-256, per-data-item, rotated on data change)
    |       +-- DEK 2 (AES-256, per-session, ephemeral)
    |
    +-- Key Encryption Key 2 (KMS, online, rotated annually)
            |
            +-- DEK 3, DEK 4, ...
```

## Envelope Encryption Pattern

1. `(plaintext_dek, encrypted_dek) = KMS.GenerateDataKey(CMK, "AES_256")`
2. `ciphertext = AES-256-GCM(plaintext, plaintext_dek, nonce=counter)`
3. Store: `encrypted_dek || nonce || ciphertext || auth_tag`
4. Decrypt: `plaintext_dek = KMS.Decrypt(encrypted_dek)` → decrypt ciphertext
5. Rotate DEK: re-encrypt data with new DEK, discard old DEK
6. Rotate CMK: `KMS.ReEncrypt(encrypted_dek, new_CMK)` — no data re-encryption needed

## HSM Selection Matrix

| Provider | Type | FIPS Level | Key Types | Best For |
|----------|------|-----------|-----------|----------|
| AWS CloudHSM | Dedicated HSM | Level 3 | RSA, ECC, AES, HMAC | AWS-centric PKI, high-throughput signing |
| GCP Cloud HSM | Multi-tenant HSM | Level 3 | RSA, ECC, AES | GCP workload encryption, KMS integration |
| Azure Dedicated HSM | Dedicated HSM | Level 3 | RSA, ECC, AES | Azure-centric, compliance-heavy workloads |
| YubiHSM 2 | USB HSM | Level 2+ | RSA, ECC, AES, Ed25519 | Developer CA, small-scale PKI |
| Thales Luna | Network HSM | Level 3 | All standard algorithms | Enterprise PKI, high-assurance |
| nCipher nShield | Network HSM | Level 3 | All + custom code | Code signing, sovereign key management |

## Key Ceremony Procedures

1. **Pre-ceremony**: verified hardware, clean room, recorded environment
2. **M-of-N split**: key shares distributed to custodians across organizational boundaries
3. **Dual control**: minimum 2 custodians present for any key operation
4. **Audit trail**: full video recording, signed witness statements, tamper-evident seals
5. **Annual verification**: confirm all custodians can access their key shares
