## 1. Overview

This skill covers production-grade implementation of advanced cryptographic primitives beyond standard encryption: **Multi-Party Computation (MPC)**, **Fully Homomorphic Encryption (FHE)**, **Threshold Signatures**, **Trusted Execution Environments (TEE)**, **Post-Quantum Cryptography (PQC)**, and **Key Management Ceremonies**. Each domain requires deep understanding of mathematical foundations, protocol security models, side-channel resistance, and operational deployment patterns.

**When to invoke this skill:** You are implementing any of the above primitives in a production system handling financial transactions, custody, confidential computing, or long-term secrecy. This skill provides decision frameworks, reference implementations, and security hardening guidance that basic crypto libraries do not cover.

**When NOT to invoke:** Basic AES-GCM/ChaCha20-Poly1305 encryption, TLS termination, password hashing with Argon2id, or smart contract-level cryptography — those belong to `security-engineer`, `devops-engineer`, `backend-developer`, `zkp-engineer`, or `smart-contract-auditor`.

**Core libraries covered:**
| Domain | Libraries & Frameworks |
|--------|----------------------|
| MPC | MP-SPDZ (40+ protocols), SCALE-MAMBA, EMP-toolkit, libsnark |
| FHE | Google HEIR, Zama Concrete (TFHE), Microsoft SEAL (CKKS/BFV), OpenFHE, HElib |
| Threshold Signatures | FROST (Zcash foundation), BLS (herumi/bls), GG20/GG18 (Binance tss-lib) |
| TEE | Intel SGX SDK/DCAP, AMD SEV-SNP, AWS Nitro SDK, ARM CCA veraison |
| PQC | liboqs (Open Quantum Safe), pqcrypto-py, BoringSSL PQ, NIST ref impls |
| Key Management | PKCS#11 (SoftHSM2/OpenSC), Hashicorp Vault, AWS KMS, Google Cloud KMS |

**Security model assumptions by domain:**
- **MPC:** Up to `t` corrupt parties (honest/dishonest majority), static vs adaptive corruption
- **FHE:** IND-CPA security (no chosen-ciphertext attacks possible by construction), circuit privacy for output
- **Threshold Signatures:** Unforgeability under `t-1` corruptions, robustness (identifiable aborts)
- **TEE:** Hardware root of trust, side-channel resistance at microarchitectural level
- **PQC:** Quantum attacker with polynomial-time access to a CRQC (cryptographically relevant quantum computer)

---
