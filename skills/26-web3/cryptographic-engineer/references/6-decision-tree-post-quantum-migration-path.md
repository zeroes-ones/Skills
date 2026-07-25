## 6. Decision Tree: Post-Quantum Migration Path

```
┌── PQC Migration Path ───────────────────────────────────────────┐
│                                                                  │
│  Phase 1: Crypto Inventory                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 1. Scan all TLS endpoints (cipher suite enumeration)      │   │
│  │ 2. Map key exchange: RSA/ECDH -> which systems?           │   │
│  │ 3. Map signatures: RSA-PSS/ECDSA -> which certificates?   │   │
│  │ 4. Classify: harvest-now-decrypt-later risk assessment    │   │
│  │ 5. Identify long-lived secrets (>10yr confidentiality)    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Phase 2: Hybrid Deployment                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ X.509 hybrid certificates: ECDSA + ML-DSA-87 signature    │   │
│  │ TLS 1.3 hybrid: X25519 + ML-KEM-768 key agreement         │   │
│  │ Dual computation: key_material = KDF(ecdh || mlkem)       │   │
│  │ ⚠ CRITICAL: Both MUST succeed — fallback = attack vector  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Phase 3: Full PQC (NIST standards)                              │
│  ┌──────────┬──────────────┬──────────────┬─────────────────┐   │
│  │ Algorithm│ Standard     │ Use Case     │ Key/Sig Size    │   │
│  ├──────────┼──────────────┼──────────────┼─────────────────┤   │
│  │ ML-KEM   │ FIPS 203     │ Key encap    │ 768-1184 bytes  │   │
│  │ ML-DSA   │ FIPS 204     │ Signatures   │ 2420-4627 bytes │   │
│  │ SLH-DSA  │ FIPS 205     │ Backup sig   │ 7856-49856 bytes│   │
│  │ XMSS/LMS │ NIST SP 800  │ Code signing │ ~2.5KB per key  │   │
│  └──────────┴──────────────┴──────────────┴─────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

**Hybrid key exchange with liboqs (C):**
```c
// liboqs: Classical + PQC hybrid KEM
#include <oqs/oqs.h>

// Classical: X25519 ECDH
uint8_t ecdh_public[32], ecdh_secret[32];
X25519(ecdh_public, ecdh_secret, basepoint);

// PQC: ML-KEM-768 key encapsulation
OQS_KEM *kem = OQS_KEM_new(OQS_KEM_alg_ml_kem_768);
uint8_t mlkem_public[1184], mlkem_secret[2400], mlkem_ciphertext[1088];
OQS_KEM_keypair(kem, mlkem_public, mlkem_secret);

// HYBRID: Concatenate then KDF (both MUST succeed)
uint8_t combined[32 + 32];  // ECDH shared || ML-KEM shared
memcpy(combined, ecdh_shared, 32);
memcpy(combined + 32, mlkem_shared, 32);
HKDF_SHA256(combined, 64, NULL, 0, final_key, 32);

OQS_KEM_free(kem);
// NEVER fall back to classical-only if PQC fails — fail closed!
```

---
