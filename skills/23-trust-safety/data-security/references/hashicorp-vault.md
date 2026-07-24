# HashiCorp Vault — Encryption as a Service

## Overview
HashiCorp Vault provides secrets management, encryption as a service, and privileged access management across multi-cloud and on-premises environments.

## Secrets Engines
- **Transit**: Encryption as a service (encrypt/decrypt/hash without storing data)
- **KV (v2)**: Key-value secrets storage with versioning
- **PKI**: Dynamic X.509 certificate generation
- **Database**: Dynamic database credential generation

## Encryption as a Service (Transit)
1. Application sends plaintext to Vault Transit API
2. Vault encrypts with named key, returns ciphertext
3. Application stores ciphertext (never the key)
4. Decrypt: send ciphertext back to Vault

Benefits: applications never see encryption keys, centralized key rotation, auditing

## Key Rotation
- **Transit**: Rotate keys on schedule; old versions retained for decryption
- **Rewrap**: Batch re-encrypt ciphertext with new key version
- **Min decryption version**: Control how many versions back decryption works

## Deployment Models
- **Dev**: Single node, in-memory storage (never for production)
- **HA with Raft**: Integrated storage, leader election, auto-unseal
- **External storage**: Consul/etcd/ZooKeeper backend, HSM auto-unseal

## References
- Vault: https://developer.hashicorp.com/vault/docs
