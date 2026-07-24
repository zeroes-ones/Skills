---
name: cryptographic-engineer
description: Use when implementing threshold cryptography (FROST Schnorr, BLS aggregation, t-of-n signing), deploying Multi-Party Computation (MP-SPDZ with 40+ protocols, Shamir Secret Sharing, Garbled Circuits with oblivious transfer), configuring Fully Homomorphic Encryption (HEIR compiler, Concrete for TFHE, SEAL for CKKS/BFV, OpenFHE multi-scheme, scheme selection between TFHE for bitwise/CKKS for approximate/BGV for exact/BFV for integer), engineering Trusted Execution Environments (Intel SGX remote attestation, AMD SEV-SNP confidential VMs, AWS Nitro Enclaves with vsock, ARM CCA Realm), planning post-quantum cryptographic migration (ML-KEM Kyber key encapsulation, ML-DSA Dilithium signatures, SLH-DSA SPHINCS+ stateless hash-based, hybrid X.509 certificates with NIST Round 3 algorithms), designing key management ceremonies (HSM with PKCS#11, Shamir Secret Sharing backup with verifiable shares, entropy health monitoring, split-knowledge procedures), or architecting cryptographic agility layers (algorithm inventory, migration planning with hybrid schemes, protocol negotiation downgrade prevention). Handles MPC protocols (dishonest majority vs honest majority selection, reactive vs non-reactive computation, preprocessing with function-independent correlated randomness), FHE scheme selection (TFHE for low-latency bitwise operations < 50ms, CKKS for approximate SIMD computation on floating-point vectors, BGV/BFV for exact integer arithmetic on encrypted data, bootstrapping overhead analysis and level budgeting), threshold signing architectures (FROST two-round signing with identifiable aborts, BLS non-interactive threshold aggregation, key resharing for committee rotation without key-regeneration), TEE attestation workflow (SGX DCAP quote verification, SEV-SNP attestation report with VCEK certificate chain, Nitro Enclaves PCR-based cryptographic attestation, memory encryption engine monitoring for cold-boot attack detection), and PQC migration strategy (crypto inventory using protocol detection via TLS fingerprinting, hybrid key exchange with classical+PQC dual agreement, certificate chain migration timeline with CRL/OCSP backward compatibility). Do NOT use for basic encryption (use security-engineer), TLS configuration (use devops-engineer), smart contract cryptography (use zkp-engineer or smart-contract-auditor), or password hashing (use backend-developer).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: specialized
status: stable
version: 1.0.0
updated: 2026-07-24
tags: [cryptography, mpc, fhe, threshold-signatures, tee, post-quantum, key-management]
token_budget: 4500
chain:
  consumes_from:
    - security-engineer
    - system-architect
    - backend-developer
  feeds_into:
    - zkp-engineer
    - smart-contract-auditor
    - compliance-officer
---

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

# Cryptographic Engineer — Advanced Cryptography Implementation

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

## 2. Decision Tree: MPC Protocol Selection

Choose your MPC protocol stack based on the adversary model and computation type. The wrong choice can mean $1M+ in unnecessary overhead or insufficient security.

```
┌── MPC Protocol Selection ──────────────────────────────────────┐
│                                                                 │
│  How many corrupt parties can you tolerate?                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ t < n/2 (honest majority)?                                │  │
│  │  ├─ Reactive computation needed? ─► SPDZ (online phase)   │  │
│  │  │  └─ Low latency < 100ms? ─► Replicated Secret Sharing  │  │
│  │  │     (3-party, dishonest minority, 1 corrupt)           │  │
│  │  └─ Non-reactive (batch)? ─► BGW/GMW with Shamir shares   │  │
│  │     └─ Boolean circuits? ─► GMW with OT extension         │  │
│  │        └─ Arithmetic circuits? ─► BGW (Shamir-based)      │  │
│  │                                                           │  │
│  │ t < n (dishonest majority)?                                │  │
│  │  ├─ Need preprocessing? ─► SPDZ-like (MASCOT/Overdrive)   │  │
│  │  │  ├─ Function-independent preprocessing ─► MASCOT       │  │
│  │  │  └─ Function-dependent preprocessing ─► SPDZ2k         │  │
│  │  └─ Garbled circuits sufficient? ─► Yao with OT           │  │
│  │     └─ Malicious security? ─► Authenticated garbling      │  │
│  │        (WRK/Wang-Katz, ~2x overhead vs semi-honest)       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Protocol selection matrix (n=3, varied t):                     │
│  ┌─────────────────────┬──────────┬────────────┬─────────────┐  │
│  │ Protocol            │ Security │ Throughput │ Round-trips │  │
│  ├─────────────────────┼──────────┼────────────┼─────────────┤  │
│  │ Replicated (3PC)    │ 1 corrupt│ 10M AND/s  │ 1 (online)  │  │
│  │ Shamir (BGW)        │ t < n/2  │ 1M mult/s  │ O(depth)    │  │
│  │ SPDZ (MASCOT)       │ n-1 corr │ 100K mult/s│ 1 online    │  │
│  │ Yao (semi-honest)   │ 1 corrupt│ 1M gates/s │ 2           │  │
│  │ Yao (malicious)     │ 1 corrupt│ 500K gate/s│ 2           │  │
│  │ GMW (OT-based)      │ 1 corrupt│ 500K AND/s │ O(depth)    │  │
│  └─────────────────────┴──────────┴────────────┴─────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation with MP-SPDZ (Python DSL):**
```python
# MP-SPDZ example: Secure inner product with malicious security
# Compile: ./compile.py -R 64 inner_product
# Run: Scripts/2-party-malicious.sh inner_product

from Compiler import mpc_math, util

def inner_product(x, y, n):
    """Compute dot(x, y) with active security against n-1 corruptions"""
    res = sint(0)
    @for_range(n)
    def _(i):
        res += x[i] * y[i]
    return res

x = [sint.get_input_from(0) for _ in range(10)]
y = [sint.get_input_from(1) for _ in range(10)]
result = inner_product(x, y, 10)
print_ln("Inner product: %s", result.reveal())
```

**Key decision factors:**
- **Round complexity:** FHE-based MPC (1 round) vs OT-based (O(depth)) — latency-sensitive apps need constant-round
- **Corruption threshold:** Dishonest majority requires SPDZ-like preprocessing (10-100x overhead vs honest majority)
- **Circuit type:** Arithmetic circuits (Shamir/BGW) are 100x faster for numeric computation than Boolean (GMW/Yao)
- **Setup assumptions:** CRS model (SPDZ) vs plain model (BGW, replicated) — CRS adds trusted setup risk

---

## 3. Decision Tree: FHE Scheme Selection

FHE scheme choice depends on the computation type. Wrong scheme = silent correctness failure or $500K+ calculation errors.

```
┌── FHE Scheme Selection ────────────────────────────────────────┐
│                                                                 │
│  What are you computing on encrypted data?                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Bitwise operations (comparisons, branching)?               │  │
│  │  └─► TFHE (Concrete/OpenFHE) — ~50ms/op, programmable     │  │
│  │     bootstrapping at each gate, latency-optimized          │  │
│  │                                                           │  │
│  │ Approximate real numbers (ML inference, stats)?            │  │
│  │  └─► CKKS (SEAL/OpenFHE) — SIMD batch (up to 32K slots),  │  │
│  │     approximate arithmetic, rescaling after each mult      │  │
│  │     ⚠ NEVER use for exact equality or integer division     │  │
│  │                                                           │  │
│  │ Exact integer arithmetic (financial, voting)?              │  │
│  │  ├─ BGV (HElib/OpenFHE) — exact integers, modulus chain    │  │
│  │  │  for level management, SIMD packing via CRT             │  │
│  │  └─ BFV (SEAL/OpenFHE) — exact integers, scale-invariant,  │  │
│  │     simpler noise management, good for small integers      │  │
│  │                                                           │  │
│  │ Multi-scheme pipeline (pre-process + compute)?             │  │
│  │  └─► HEIR compiler — IR-based, supports TFHE→CKKS→BGV      │  │
│  │     lowering, automatic scheme selection per operation     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Scheme comparison matrix:                                       │
│  ┌──────────┬──────────┬──────────┬─────────┬──────────────┐    │
│  │ Scheme   │ Data Type│ SIMD     │ Bootstr │ Best For      │    │
│  ├──────────┼──────────┼──────────┼─────────┼──────────────┤    │
│  │ TFHE     │ Bits     │ No       │ Gate-lvl│ Comparisons   │    │
│  │ CKKS     │ Complex  │ 32K slot │ Level   │ ML inference  │    │
│  │ BGV      │ Integers │ CRT pack │ Mod-sw  │ Exact arith   │    │
│  │ BFV      │ Integers │ CRT pack │ Scale   │ Fixed-point   │    │
│  └──────────┴──────────┴──────────┴─────────┴──────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

**CKKS example (SEAL C++):**
```cpp
// Microsoft SEAL: Encrypted logistic regression inference
EncryptionParameters parms(scheme_type::ckks);
size_t poly_modulus_degree = 32768;  // 2^15 for 128-bit security
parms.set_poly_modulus_degree(poly_modulus_degree);
parms.set_coeff_modulus(CoeffModulus::Create(poly_modulus_degree, {60, 40, 40, 60}));
SEALContext context(parms);

// Pack 8192 features into one ciphertext via SIMD
Plaintext weights;
encoder.encode(weight_vector, scale, weights);
Ciphertext encrypted_result;
evaluator.multiply_plain(encrypted_input, weights, encrypted_result);
evaluator.relinearize_inplace(encrypted_result, relin_keys);
evaluator.rescale_to_next_inplace(encrypted_result);  // ⚠ CRITICAL: rescale after each mult
```

**Bootstrapping budget tracking:**
```python
# Level budget analysis for CKKS pipeline
# Each multiplication consumes one level; bootstrapping resets levels
initial_levels = 12    # From coeff_modulus chain
ops = [
    ("multiply", 1), ("rotate", 0), ("multiply", 1),  # Level 12 → 10
    ("bootstrap", 0),                                   # Reset to top
    ("multiply", 1), ("multiply", 1),                   # Level 12 → 10
]
remaining = initial_levels
for op, cost in ops:
    if op == "bootstrap":
        remaining = initial_levels  # ⚠ Bootstrapping cost: ~10s per ciphertext
    else:
        remaining -= cost
    assert remaining >= 0, f"Level budget exhausted at {op} — $200K+ data corruption risk"
```

---

## 4. Decision Tree: Threshold Signature Architecture

```
┌── Threshold Signature Architecture ─────────────────────────────┐
│                                                                 │
│  Requirements analysis:                                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Need non-interactive signing (no co-signer coordination)?  │  │
│  │  └─► BLS Threshold — single-round, aggregatable, but      │  │
│  │     requires pairing-friendly curve (BLS12-381, BN254)     │  │
│  │     ⚠ Keygen requires DKG (distributed key generation)     │  │
│  │                                                           │  │
│  │ Need identifiable aborts (know which party refused)?       │  │
│  │  └─► FROST (Schnorr) — 2-round signing, identifies        │  │
│  │     misbehaving signers, compatible with standard Schnorr  │  │
│  │     ⚠ Interactive: all signers must participate round 1    │  │
│  │                                                           │  │
│  │ Need ECDSA compatibility (Bitcoin/Ethereum)?               │  │
│  │  └─► GG20/GG18/CGGMP — multi-round, supports secp256k1    │  │
│  │     ⚠ 5+ rounds, higher latency, Paillier ZK required      │  │
│  │                                                           │  │
│  │ Need committee rotation without re-keying?                 │  │
│  │  └─► Proactive secret sharing with key resharing          │  │
│  │     (Herzberg dynamic proactive scheme)                    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Protocol comparison:                                            │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────────┐   │
│  │ Protocol │ Rounds   │ Curve    │ Size     │ Abort ID     │   │
│  ├──────────┼──────────┼──────────┼──────────┼──────────────┤   │
│  │ FROST    │ 2        │ secp256k1│ 64B sig  │ Yes          │   │
│  │ BLS      │ 1 (non-i)│ BLS12-381│ 96B sig  │ No           │   │
│  │ GG20     │ 5-7      │ secp256k1│ 64B sig  │ Yes          │   │
│  │ CGGMP    │ 4-6      │ secp256k1│ 64B sig  │ Yes          │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**FROST threshold signing (Rust):**
```rust
// frost-secp256k1: t-of-n Schnorr threshold signature
use frost_secp256k1 as frost;
use rand::thread_rng;

// Round 1: Each signer generates nonces and commitments
let mut rng = thread_rng();
let (secret_package, round1_package) = frost::keys::KeyPackage::try_from(participant_secret)
    .unwrap()
    .new_nonce(&mut rng)
    .unwrap();

// Coordinator aggregates commitments
let signing_package = frost::SigningPackage::new(round1_packages, message);

// Round 2: Each signer produces signature share
let signature_share = frost::sign(&signing_package, &secret_package, &round1_package)
    .map_err(|e| IdentifiableAbort::from(e))?;  // ← identifiable abort

// Coordinator aggregates shares into final Schnorr signature
let group_signature = frost::aggregate(&signing_package, &signature_shares, &group_public_key)
    .unwrap();
verify(&group_public_key, message, &group_signature);  // Standard Schnorr verify
```

**BLS threshold aggregation (no signer interaction):**
```python
# Each party signs locally; aggregator combines
from py_ecc.bls import G2ProofOfPossession as bls

# Party i signs with its key share (no coordination needed)
sig_share_i = bls.Sign(sk_share_i, message)

# Aggregator: combine t shares via Lagrange interpolation
aggregated_sig = bls.Aggregate(sig_shares)  # O(n) aggregation, constant-size result

# Verify: PK is group public key (reconstructed from shares)
bls.Verify(group_pk, message, aggregated_sig)  # True if >= t honest signers
```

---

## 5. Decision Tree: TEE Platform Selection

```
┌── TEE Platform Selection ───────────────────────────────────────┐
│                                                                  │
│  Workload characterization:                                      │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Application-level enclave (isolated process within VM)?     │  │
│  │  ├─ Intel SGX (TDX for full VM) — 256MB EPC, DCAP v4       │  │
│  │  └─ AWS Nitro Enclaves — full Linux VM, vsock comms        │  │
│  │                                                             │  │
│  │ Full VM confidential computing (lift-and-shift)?            │  │
│  │  ├─ AMD SEV-SNP — encrypted VM state, VCEK attestation     │  │
│  │  ├─ Intel TDX — full VM TEE, MRTD measurement, 1TB max     │  │
│  │  └─ ARM CCA Realm — hardware-enforced, RMM firmware        │  │
│  │                                                             │  │
│  │ Multi-cloud portability requirement?                        │  │
│  │  └─ Enarx (Wasm-based), K8s Confidential Containers (CoCo) │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Platform comparison:                                            │
│  ┌──────────┬──────────┬────────────┬──────────┬─────────────┐   │
│  │ Platform │ Enclave  │ Attestation│ Memory   │ Cloud       │   │
│  ├──────────┼──────────┼────────────┼──────────┼─────────────┤   │
│  │ SGX DCAP │ Process  │ ECDSA/DCAP │ 256MB    │ Azure/Ali   │   │
│  │ SEV-SNP  │ Full VM  │ VCEK cert  │ 4TB+     │ AWS/GCP/Az  │   │
│  │ Nitro    │ VM (nop) │ PCR-based  │ Config   │ AWS only    │   │
│  │ TDX      │ Full VM  │ DCAP ext   │ 1TB      │ Azure/GCP   │   │
│  │ ARM CCA  │ VM Realm │ CCA token  │ Config   │ Emerging    │   │
│  └──────────┴──────────┴────────────┴──────────┴─────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

**AWS Nitro Enclaves attestation (Rust):**
```rust
// Nitro Secure Module (NSM) API for cryptographic attestation
use nsm_lib::{Request, Response, Digest};

let request = Request::Attestation {
    public_key: Some(&signing_key.public_bytes()),
    user_data: Some(pcr_binding_hash),   // Bind to specific PCR values
    nonce: Some(&random_nonce),           // Prevents replay attacks
};

let nsm_fd = nsm_lib::nsm_lib_init();
let response = nsm_lib::nsm_send_request(nsm_fd, &request)
    .expect("NSM attestation failed");

// Verify: Document -> AWS Public Cert -> AWS Root CA
let attestation_doc = parse_cbor(&response.attestation_document);
verify_aws_certificate_chain(&attestation_doc.cabundle)
    .map_err(|_| "CRITICAL: Chain validation skipped")?;

assert_eq!(attestation_doc.pcrs[0], expected_enclave_image_hash);
```

**Intel SGX DCAP quote verification (C++):**
```cpp
// SGX DCAP v4: Quote verification with collateral
sgx_ql_qe_report_info_t qve_report_info;
sgx_quote3_t *p_quote = (sgx_quote3_t *)quote_buffer;

// Get PCK cert chain, TCB info, QE identity
tee_supplicant_get_collateral(&p_quote->certification_data, &collateral);

quote3_error_t ret = sgx_qv_verify_quote(
    p_quote, quote_size, &collateral, current_time,
    &verification_result,
    supplemental_data_size > 0  // LVI/MMIO mitigation status
);

// Non-trivial: must check isv_enclave_report_status != QV_RESULT_OK
if (verification_result.isv_enclave_report_status != SGX_QL_QV_RESULT_OK) {
    report_error("Enclave identity mismatch or revoked TCB");
}
```

---

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

## 7. Decision Tree: Key Ceremony Design

```
┌── Key Ceremony Design ─────────────────────────────────────────┐
│                                                                │
│  What is the threat model for key material?                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ Treasury/custody ($100M+)?                               │    │
│  │  └─ HSM quorum (n-of-m) + Shamir backup + air-gapped    │    │
│  │     ceremony with video audit + tamper-evident seals     │    │
│  │                                                         │    │
│  │ Decentralized protocol (DAOs, bridges)?                  │    │
│  │  └─ MPC-based ceremony (no single point of compromise)  │    │
│  │     + Verifiable Secret Sharing (Feldman VSS)            │    │
│  │                                                         │    │
│  │ Enterprise PKI (short-lived keys < 90d)?                 │    │
│  │  └─ HSM-backed CA with offline root + online issuing    │    │
│  │     + TEE for key protection during signing              │    │
│  │                                                         │    │
│  │ Crypto exchange wallet?                                  │    │
│  │  └─ Threshold ECDSA (GG20) with geographic distribution │    │
│  │     + Proactive refresh every 30-90 days                 │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                │
│  Ceremony checklist (air-gapped HSM ceremony):                  │
│  1. Entropy sourcing: hardware RNG + dice rolls (mix via KDF)  │
│  2. Shamir splitting: t-of-n, verifiable shares (Feldman)       │
│  3. Share distribution: tamper-evident envelopes, chain-of-custody│
│  4. Ceremony recording: dual video, witness log, GPS timestamp │
│  5. Verification: reconstruct pubkey from each subset, test sig│
│  6. Share custody: safe deposit boxes, geographic distribution │
│  7. Emergency recovery: documented procedure, quorum call-list  │
└────────────────────────────────────────────────────────────────┘
```

**Feldman Verifiable Secret Sharing (Rust):**
```rust
// Verifiable Shamir sharing: shares can be verified without reconstruction
use curv::elliptic::curves::{Secp256k1, Point};
use curv::BigInt;

struct FeldmanVSS {
    n: usize,             // Total shares
    t: usize,             // Threshold
    generator: Point<Secp256k1>,
}

impl FeldmanVSS {
    fn split(&self, secret: &BigInt) -> (Vec<BigInt>, Vec<Point<Secp256k1>>) {
        // f(x) = secret + a1*x + a2*x^2 + ... + at*x^t mod q
        let coeffs = self.generate_polynomial(secret, self.t);
        let shares: Vec<_> = (1..=self.n)
            .map(|i| self.evaluate(&coeffs, BigInt::from(i)))
            .collect();
        // Commitments: A_j = g^a_j for verification
        let commitments: Vec<_> = coeffs.iter()
            .map(|c| self.generator.clone() * c)
            .collect();
        (shares, commitments)
    }

    fn verify_share(&self, share: &BigInt, index: usize,
                    commitments: &[Point<Secp256k1>]) -> bool {
        let lhs = self.generator.clone() * share;
        let mut rhs = commitments[0].clone();
        let x = BigInt::from(index + 1);
        for j in 1..commitments.len() {
            rhs = rhs + commitments[j].clone() * x.pow(j as u32);
        }
        lhs == rhs  // g^f(i) == prod A_j^{i^j}
    }
}
```

---

## 8. MPC Implementation Patterns

### 8.1 Shamir Secret Sharing (Python reference)

```python
from secrets import randbelow
from dataclasses import dataclass

# Prime field (secp256k1 order as example)
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

@dataclass
class ShamirShare:
    x: int  # Evaluation point
    y: int  # f(x) mod P

def share_secret(secret: int, t: int, n: int) -> list[ShamirShare]:
    """t-of-n Shamir sharing: create n shares, any t can reconstruct"""
    coeffs = [secret] + [randbelow(P) for _ in range(t - 1)]
    shares = []
    for i in range(1, n + 1):
        y = sum(c * pow(i, j, P) for j, c in enumerate(coeffs)) % P
        shares.append(ShamirShare(i, y))
    return shares

def reconstruct(shares: list[ShamirShare]) -> int:
    """Lagrange interpolation at x=0 to recover secret"""
    secret = 0
    for i, si in enumerate(shares):
        num, den = 1, 1
        for j, sj in enumerate(shares):
            if i != j:
                num = num * (0 - sj.x) % P
                den = den * (si.x - sj.x) % P
        lagrange_coeff = num * pow(den, -1, P) % P
        secret = (secret + si.y * lagrange_coeff) % P
    return secret
```

### 8.2 Garbled Circuits with Oblivious Transfer (Rust with mpz)

```rust
// Garbled circuit evaluation: Garbler encrypts circuit, Evaluator evaluates
// Uses half-gates optimization (Zahur-Rosulek-Evans, Eurocrypt 2015)

use mpz_core::{Block, GarbledCircuit};
use mpz_ot::chou_orlandi::{Receiver as OTReceiver, Sender as OTSender};

struct GarbledAndGate {
    // Half-gate: 2 ciphertexts per AND gate (optimal)
    garbler_half: [Block; 2],
    evaluator_half: [Block; 2],
}

fn garble_and(a0: Block, a1: Block, b0: Block, b1: Block,
              delta: Block) -> GarbledAndGate {
    // Free-XOR: delta = global offset for wire label encoding
    // Label encoding: W^0 = w, W^1 = w XOR delta
    let t_g = H(a0) ^ H(a0 ^ delta) ^ (b0 & delta);  // Garbler half-gate
    let t_e = H(b0) ^ H(b0 ^ delta) ^ a0;              // Evaluator half-gate
    GarbledAndGate {
        garbler_half: [t_g, t_g ^ a0],
        evaluator_half: [t_e, t_e ^ b0],
    }
}
// Total communication: 2 * 128 bits per AND gate (half-gates)
```

### 8.3 MPC Security Hardening Checklist
- [ ] Constant-time comparisons in GMW inner loop (no early exit on branch)
- [ ] Randomize gate evaluation order per execution (defeat timing correlation)
- [ ] Use fresh OT correlations per session (never reuse OT precomputation)
- [ ] Verify zero-knowledge proofs in SPDZ preprocessing phase
- [ ] Rate-limit corrupt party detection (identifiable aborts leak correlation info)
- [ ] Network padding: uniform message sizes regardless of computation path

---

## 9. FHE Implementation Patterns

### 9.1 TFHE Programmable Bootstrapping (Zama Concrete)

```python
# Concrete: TFHE with programmable bootstrapping
# Each bootstrapping = refresh noise + evaluate lookup table (PBS)
from concrete import fhe
import numpy as np

@fhe.compiler({"x": "encrypted", "y": "encrypted"})
def encrypted_min(x, y):
    """Compute min(x, y) with PBS at each comparison"""
    # PBS evaluates: f(x-y) where f is a sign function
    # Doing min with one PBS: min(x,y) = x if x <= y else y
    return fhe.min(x, y)  # Single PBS for the sign test

# Configuration for 128-bit security
configuration = fhe.Configuration(
    parameter_selection_strategy=fhe.ParameterSelectionStrategy.MULTI,
    show_graph=True,  # Visualize PBS operations in circuit
)

inputset = [(np.random.randint(0, 100, size=()) for _ in range(2)) for _ in range(1000)]
compiler = fhe.Compiler(encrypted_min, {"x": "encrypted", "y": "encrypted"})
circuit = compiler.compile(inputset, configuration)

# Circuit stats: bootstrappings, key sizes, noise budget
print(f"PBS count: {circuit.programmable_bootstrap_count}")
print(f"Key size: {circuit.size_of_secret_keys // 1024} KB")
```

### 9.2 CKKS Packing Strategy with SEAL

```cpp
// Optimal packing: encode multiple values into one ciphertext via SIMD
// For logistic regression: pack feature vectors into single ciphertext
std::vector<double> features(8192);
encoder.encode(features, scale, plain_features);

// ⚠ CRITICAL: Never compare CKKS values for equality
// WRONG (silent failure, $500K+ error):
//   if (enc_a == enc_b) { ... }  // CKKS is APPROXIMATE

// CORRECT: Compare thresholded difference
Ciphertext diff;
evaluator.sub(enc_a, enc_b, diff);
Plaintext threshold;
encoder.encode(std::vector<double>(N, 1e-6), scale, threshold);
// Bootstrapping-intensive comparison — consider BFV/BGV instead
```

### 9.3 HEIR Compiler Pipeline (Google)

```python
# HEIR: MLIR-based FHE compiler — automatic scheme selection
# heir-opt --heir-scheme-lowering lower.mlir > lower_tfhe.mlir

# Input: High-level MLIR describing encrypted computation
# heir-opt lowers through:
#   1. heir-scheme-lowering: FHE dialect -> TFHE/CKKS/BGV IR
#   2. heir-bootstrap-placement: Insert bootstrapping operations
#   3. heir-noise-analysis: Verify budget is not exceeded
#   4. heir-codegen: Emit OpenFHE/Concrete/SEAL runtime code
```

**FHE performance optimization checklist:**
- [ ] Pack independent values into SIMD slots (32K parallelism for CKKS)
- [ ] Minimize bootstrap calls (< 50 per circuit for latency < 500ms)
- [ ] Use leveled operations when possible (no bootstrap between linear layers)
- [ ] Precompute plaintext constants as Plaintext (not encrypted)
- [ ] Batch rotation keys: one key per rotation index, share across circuits

---

## 10. Threshold Signature Implementation

### 10.1 FROST Two-Round Signing Protocol

```python
# FROST Schnorr threshold: Round 1 (commitment) + Round 2 (sign)
# From RFC 9591 (CFRG) — production-grade FROST specification
from hashlib import sha256
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class FrostSigner:
    index: int
    sk_share: int       # Secret key share
    pk: int             # Group public key
    t: int              # Threshold
    n: int              # Total signers
    
    def round1_commit(self, msg: bytes) -> tuple:
        """Generate hiding + binding nonce commitments"""
        hiding_nonce = randbelow(P)
        binding_nonce = randbelow(P)
        # Commit_i = (g^hiding, g^binding)
        hiding_commit = pow(G, hiding_nonce, P)
        binding_commit = pow(G, binding_nonce, P)
        return (hiding_commit, binding_commit), (hiding_nonce, binding_nonce)
    
    def round2_sign(self, msg: bytes, all_commits: dict,
                    my_nonces: tuple) -> Optional[int]:
        """Produce signature share with identifiable abort"""
        hiding_nonce, binding_nonce = my_nonces
        
        # Aggregate commitments: R = prod(commit_i_hiding) * prod(commit_i_binding)^rho
        group_commitment = aggregate_commitments(all_commits, msg)
        
        # Challenge: c = H(group_commitment, pk, msg)
        c = int.from_bytes(sha256(group_commitment + str(pk).encode() + msg).digest(), 'big')
        
        # Binding factor rho_i = H(i, all_commits, msg)
        rho_i = int.from_bytes(sha256(f"{self.index}{all_commits}{msg}".encode()).digest(), 'big')
        
        # Lagrange coefficient lambda_i = prod_{j!=i} j/(j-i) mod q
        lambda_i = lagrange_coefficient([s for s in signers], self.index)
        
        # Signature share: z_i = hiding_nonce + binding_nonce*rho_i + lambda_i * sk_share * c
        z_i = (hiding_nonce + binding_nonce * rho_i + lambda_i * self.sk_share * c) % P
        return z_i

def aggregate_frost(msg: bytes, group_commitment: int, sig_shares: dict,
                    group_pk: int) -> bytes:
    """Aggregate t signature shares into a standard Schnorr signature"""
    # z = sum(z_i) mod q
    z = sum(sig_shares.values()) % P
    # (R, z) is a standard Schnorr signature verifiable against group_pk
    signature = group_commitment.to_bytes(32, 'big') + z.to_bytes(32, 'big')
    return signature
```

### 10.2 Proactive Key Resharing

```python
def proactive_reshare(old_shares: dict[int, int], t_old: int, t_new: int,
                      n_new: int) -> dict[int, int]:
    """Rotate committee without changing the group secret key.
    
    Each old shareholder i creates sub-shares of its share for the new committee.
    New shareholder j sums weighted sub-shares from t_old old holders.
    The group secret key remains identical — no key regeneration needed.
    
    Herzberg dynamic proactive scheme (CRYPTO 1995).
    """
    new_shares = {j: 0 for j in range(1, n_new + 1)}
    
    for i_old, old_share in old_shares.items():
        # Old holder i: split its share into n_new sub-shares (threshold t_new)
        sub_shares = share_secret(old_share, t_new, n_new)
        for sub_share in sub_shares:
            new_shares[sub_share.x] = (new_shares[sub_share.x] + sub_share.y) % P
    
    return new_shares  # Same secret, new committee — no key ceremony needed
```

---

## 11. TEE Attestation & Secure Enclave Patterns

### 11.1 Remote Attestation Protocol

```
Enclave (Prover)                    Verifier (Relying Party)
     |                                        |
     |--- 1. Request attestation ----------->|
     |<-- 2. Nonce + expected PCR values ----|
     |                                        |
     | 3. Generate Quote (report)             |
     |    - Enclave identity (MRENCLAVE)      |
     |    - TCB level (CPUSVN, ISVSVN)        |
     |    - User data = Hash(nonce, pk)       |
     |                                        |
     |--- 4. Quote + ephemeral PK ---------->|
     |                                        |
     |    5. Verify attestation:              |
     |       a) Quote signature (IAS/DCAP)    |
     |       b) MRENCLAVE matches expected    |
     |       c) TCB level >= minimum          |
     |       d) Nonce matches                 |
     |       e) Certificate chain valid       |
     |                                        |
     |<-- 6. Establish secure channel --------|
     |    (encrypt session key to enclave PK) |
```

### 11.2 Sealing — Persisting State Across Enclave Restarts

```cpp
// SGX: Seal data to enclave identity (MRENCLAVE) or signing identity (MRSIGNER)
sgx_status_t seal_secret(const uint8_t *secret, size_t len,
                         uint8_t *sealed_blob, size_t sealed_len) {
    // Policy: MRENCLAVE — only this exact enclave binary can unseal
    sgx_sealed_data_t *sealed = (sgx_sealed_data_t *)sealed_blob;
    
    // Key policy: bind to enclave identity + TCB
    // KEYPOLICY_MRENCLAVE: exact binary match (secure, breaks on updates)
    // KEYPOLICY_MRSIGNER: any enclave from same developer (flexible)
    uint16_t key_policy = SGX_KEYPOLICY_MRENCLAVE;
    
    sgx_status_t ret = sgx_seal_data(
        0,                    // Additional MAC text
        NULL,                 // No additional text
        len, secret,
        sealed_len, sealed
    );
    
    // ⚠ Store sealed blob on untrusted storage (disk, database)
    // It's encrypted + authenticated with hardware-derived key
    return ret;
}
```

### 11.3 AMD SEV-SNP Attestation Verification

```python
# AMD SEV-SNP: Verify attestation report with VCEK certificate chain
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
import requests

def verify_sev_attestation(report: bytes, expected_measurement: bytes) -> bool:
    """Verify SEV-SNP attestation report against AMD KDS"""
    
    # 1. Parse attestation report
    attestation = parse_sev_report(report)
    
    # 2. Fetch VCEK certificate from AMD KDS (Key Distribution Service)
    chip_id = attestation.chip_id
    vcek_url = f"https://kdsintf.amd.com/vcek/v1/{chip_id}"
    response = requests.get(vcek_url)
    
    chain_pem = f"{response.text}\n{AMD_ROOT_CA_PEM}\n{AMD_SEV_CA_PEM}"
    
    # 3. Verify certificate chain: VCEK -> SEV-CA -> AMD Root
    vcek_cert = x509.load_pem_x509_certificate(response.text.encode())
    ca_cert = x509.load_pem_x509_certificate(AMD_SEV_CA_PEM.encode())
    root_cert = x509.load_pem_x509_certificate(AMD_ROOT_CA_PEM.encode())
    
    verify_cert_chain(vcek_cert, ca_cert, root_cert)
    
    # 4. Verify report signature using VCEK public key
    vcek_pubkey = vcek_cert.public_key()
    verify_report_signature(report, vcek_pubkey)
    
    # 5. Validate measurement and policy
    assert attestation.measurement == expected_measurement  # Launch digest match
    assert attestation.policy & POLICY_DEBUG == 0  # Debug must be disabled
    assert attestation.tcb_version >= MINIMUM_TCB
    
    return True
```

---

## 12. Post-Quantum Cryptography Implementation

### 12.1 ML-KEM Key Encapsulation (liboqs)

```python
# OQS Python bindings: ML-KEM-768 (FIPS 203, NIST standard)
import oqs

# Alice: Generate keypair
with oqs.KeyEncapsulation("ML-KEM-768") as alice:
    alice_public = alice.generate_keypair()
    # Encapsulation: Bob creates shared secret + ciphertext
    with oqs.KeyEncapsulation("ML-KEM-768") as bob:
        ciphertext, bob_shared = bob.encap_secret(alice_public)
    # Decapsulation: Alice recovers shared secret
    alice_shared = alice.decap_secret(ciphertext)
    assert bob_shared == alice_shared  # 256-bit shared secret
```

### 12.2 Hybrid X.509 Certificates

```python
# Hybrid certificate: ECDSA P-256 + ML-DSA-44 signatures
# Two independent signatures on the same TBSCertificate
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec

def create_hybrid_cert(csr: x509.CertificateSigningRequest,
                       ca_ecdsa_key, ca_mldsa_key) -> x509.Certificate:
    """Build X.509 cert with dual signature algorithm"""
    
    builder = x509.CertificateBuilder()
    builder = builder.subject_name(csr.subject)
    builder = builder.issuer_name(ca_cert.subject)
    builder = builder.public_key(csr.public_key())
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.not_valid_before(datetime.utcnow())
    builder = builder.not_valid_after(datetime.utcnow() + timedelta(days=365))
    
    # Standard ECDSA signature (classical)
    cert_bytes = builder.sign(ca_ecdsa_key, hashes.SHA256())
    
    # ML-DSA-44 alternate signature (PQC) in certificate extension
    # OID: 2.16.840.1.101.3.4.3.17 (id-alg-mldsa-44)
    mldsa_sig = sign_mldsa44(cert_bytes.tbs_certificate_bytes, ca_mldsa_key)
    
    cert = cert_bytes.add_extension(
        x509.UnrecognizedExtension(
            oid=MLDSA44_SIG_OID,
            value=mldsa_sig
        ), critical=False
    )
    return cert

# ⚠ Both signatures MUST validate — single-signature acceptance = downgrade attack
```

### 12.3 Crypto Inventory & Migration Timeline

```python
# Automated crypto inventory via TLS fingerprinting
def inventory_crypto_endpoints(hosts: list[str]) -> dict:
    """Scan endpoints, classify by quantum risk, generate migration plan"""
    results = {}
    for host in hosts:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.connect((host, 443))
            cipher = s.cipher()
            cert_der = s.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(cert_der)
            
            results[host] = {
                "kex_algorithm": cipher[0],           # e.g., ECDHE-RSA
                "sig_algorithm": cert.signature_algorithm_oid._name,
                "pqc_ready": is_pqc_cipher(cipher),   # False for classical
                "hnld_risk": has_long_lived_data(host),  # Harvest-now-decrypt-later
                "migration_priority": calculate_priority(cipher, cert),
            }
    return results

# Migration timeline:
# Year 0-1: Inventory + hybrid TLS 1.3 deployment
# Year 1-2: PQC-only internal services, hybrid external
# Year 2-3: Deprecate RSA/ECDH, PQC-only for long-lived secrets
# Year 3-5: Remove classical fallback (full PQC migration)
```

---

## 13. Key Management & Ceremonies

### 13.1 HSM Integration via PKCS#11

```python
# PKCS#11: Hardware Security Module integration
# Uses SoftHSM2 for development, production HSM (Thales/Gemalto/Utimaco)
from PyKCS11 import PyKCS11

pkcs11 = PyKCS11.PyKCS11Lib()
pkcs11.load("/usr/lib/softhsm/libsofthsm2.so")  # Production: vendor .so
pkcs11.initialize()

slots = pkcs11.getSlotList(tokenPresent=True)
session = pkcs11.openSession(slots[0])

# Authenticate to HSM (split-knowledge in production: two officers enter PIN halves)
session.login("1234")  # Production: dual-control PIN entry

# Generate RSA-4096 key inside HSM (key never leaves hardware)
pub_template = [
    (PyKCS11.CKA_CLASS, PyKCS11.CKO_PUBLIC_KEY),
    (PyKCS11.CKA_TOKEN, True),
    (PyKCS11.CKA_MODULUS_BITS, 4096),
    (PyKCS11.CKA_PUBLIC_EXPONENT, (0x01, 0x00, 0x01)),
    (PyKCS11.CKA_LABEL, "Root-CA-2026"),
]
priv_template = [
    (PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY),
    (PyKCS11.CKA_TOKEN, True),
    (PyKCS11.CKA_PRIVATE, True),
    (PyKCS11.CKA_SENSITIVE, True),      # Cannot be extracted
    (PyKCS11.CKA_EXTRACTABLE, False),   # ⚠ CRITICAL: Prevent export
    (PyKCS11.CKA_SIGN, True),
    (PyKCS11.CKA_LABEL, "Root-CA-2026"),
]
(pub_key, priv_key) = session.generateKeyPair(pub_template, priv_template)

# Sign operation inside HSM
mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA256_RSA_PKCS)
signature = session.sign(priv_key, data_to_sign, mechanism)

session.logout()
session.closeSession()
```

### 13.2 Entropy Sourcing & Health Monitoring

```python
# Multi-source entropy mixing for key ceremonies
# NEVER trust a single entropy source — mix multiple independent sources
import os, time, hashlib
from struct import pack

def ceremony_entropy(num_bytes: int = 64) -> bytes:
    """Mix entropy from hardware RNG + timing jitter + CPU RDRAND"""
    sources = []
    
    # Source 1: OS CSPRNG (getrandom syscall)
    sources.append(os.urandom(num_bytes))
    
    # Source 2: CPU RDRAND (Intel/AMD hardware RNG)
    # Each RDRAND instruction: 64 bits of hardware entropy
    rdrand_bytes = b""
    for _ in range(num_bytes // 8):
        rdrand_bytes += pack("<Q", rdrand64())  # CPU intrinsic
    sources.append(rdrand_bytes)
    
    # Source 3: Timing jitter (clock jitter entropy, SP 800-90B)
    jitter = b""
    for _ in range(num_bytes * 8):
        t1 = time.perf_counter_ns()
        time.sleep(0)  # Yield — measurement noise from scheduler
        t2 = time.perf_counter_ns()
        jitter += pack("<Q", t2 - t1)
    sources.append(hashlib.sha512(jitter).digest()[:num_bytes])
    
    # Mix via HKDF: entropy = HKDF-Extract(source1 || source2 || source3)
    mixed = hashlib.sha512(b"".join(sources)).digest()
    return mixed[:num_bytes]

# ⚠ Continuous entropy health monitoring (SP 800-90B):
# - Monitor entropy source statistics (min-entropy estimate)
# - Alert if source produces repeat outputs or fails statistical tests
# - Fail closed: refuse key generation if entropy quality < threshold
```

---

## 14. Cryptographic Agility Architecture

### 14.1 Algorithm Inventory & Registration

```python
# Cryptographic algorithm registry with agility support
# Central registry to manage migration and deprecation
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Dict, Optional

class AlgorithmStatus(Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"    # Accept existing, don't create new
    LEGACY = "legacy"            # Verify only, migration required
    FORBIDDEN = "forbidden"      # Reject outright (e.g., SHA-1, RSA-1024)

@dataclass
class CryptoAlgorithm:
    name: str
    category: str            # "kex", "signature", "encryption", "hash"
    status: AlgorithmStatus
    deprecation_date: Optional[datetime]
    migration_target: Optional[str]
    impl: Callable

class CryptoRegistry:
    """Central algorithm registry — single source of truth for crypto policy"""
    def __init__(self):
        self._algos: Dict[str, CryptoAlgorithm] = {}
    
    def register(self, algo: CryptoAlgorithm):
        self._algos[algo.name] = algo
    
    def get_active(self, category: str) -> list[CryptoAlgorithm]:
        """Get active algorithms for a category (used for selection)"""
        return [a for a in self._algos.values()
                if a.category == category and a.status == AlgorithmStatus.ACTIVE]
    
    def negotiate(self, peer_algos: list[str], category: str) -> Optional[CryptoAlgorithm]:
        """Protocol negotiation with downgrade prevention.
        
        Sorts by preference: PQC-first, then classical.
        ⚠ Never selects DEPRECATED or FORBIDDEN algorithms.
        """
        our_preferred = self.get_active(category)
        our_preferred.sort(key=lambda a: 0 if "ml-" in a.name else 1)  # PQC first
        
        for algo in our_preferred:
            if algo.name in peer_algos and algo.status == AlgorithmStatus.ACTIVE:
                return algo  # Selected best mutually-supported algorithm
        
        return None  # No common algorithm — fail closed, refuse connection

# Example: TLS-like negotiation
registry = CryptoRegistry()
registry.register(CryptoAlgorithm("ECDHE-X25519", "kex", AlgorithmStatus.DEPRECATED,
    deprecation_date=datetime.now() + timedelta(days=730), migration_target="ML-KEM-768"))
registry.register(CryptoAlgorithm("ML-KEM-768", "kex", AlgorithmStatus.ACTIVE))
registry.register(CryptoAlgorithm("RSA-2048", "kex", AlgorithmStatus.LEGACY))

# Attacker tries downgrade: offers only RSA-2048
selected = registry.negotiate(["RSA-2048"], "kex")
assert selected is None  # ⚠ RSA-2048 is LEGACY, negotiation MUST fail

# Proper negotiation: offers classical + PQC
selected = registry.negotiate(["ECDHE-X25519", "ML-KEM-768"], "kex")
assert selected.name == "ML-KEM-768"  # PQC preferred
```

### 14.2 Hybrid Scheme Middleware

```python
# Transparent hybrid layer: classical + PQC dual computation
class HybridKEM:
    """Dual KEM: produces key_material = KDF(classical_ss || pqc_ss)
    
    Both key exchanges MUST complete successfully.
    Single failure = reject connection (downgrade prevention).
    """
    def __init__(self, classical: str = "X25519", pqc: str = "ML-KEM-768"):
        self.classical_kem = ClassicalKEM(classical)
        self.pqc_kem = PQKEM(pqc)
    
    def encapsulate(self, classical_pk: bytes, pqc_pk: bytes) -> tuple:
        ct_classical, ss_classical = self.classical_kem.encap(classical_pk)
        ct_pqc, ss_pqc = self.pqc_kem.encap(pqc_pk)
        
        # Both MUST succeed — fail closed
        if not ss_classical or not ss_pqc:
            raise DowngradePreventionError("Refusing to fall back to single KEM")
        
        # Key derivation: KDF(ss_classical || ss_pqc)
        combined_key = HKDF_SHA256(ss_classical + ss_pqc, salt=None, info=b"hybrid-kem")
        return (ct_classical + ct_pqc), combined_key
```

---

## 15. Anti-Rationalization

**Warning: Advanced cryptography implementations are unforgiving. You cannot "mostly get it right."**

These are the rationalizations that lead to catastrophic failures. When you hear yourself thinking any of these, **stop and reassess**:

1. **"We'll use CKKS for the financial calculation — the approximation error is small enough."** No. CKKS produces approximate results. A 0.001% error on a $500M trade is $5,000. Use BGV/BFV for exact arithmetic. There is no "close enough" in financial cryptography.

2. **"The enclave is secure because SGX protects against all attacks."** SGX has been broken repeatedly: LVI (CVE-2020-0551), Plundervolt (CVE-2019-11157), SGAxe (CVE-2020-0549). Enclaves reduce trust, they don't eliminate it. Defense in depth is mandatory.

3. **"We can skip the certificate chain validation in attestation — the quote signature is enough."** Skipping chain validation means a revoked or compromised TCB is silently accepted. An attacker with a compromised but not-yet-expired PCK can sign arbitrary quotes.

4. **"The hybrid implementation will fall back to classical-only if PQC fails."** This is the textbook downgrade attack. If the adversary can force a PQC failure (packet corruption, CPU overload on lattice operations), they force classical-only security. Hybrid must fail closed.

5. **"We'll reuse the same threshold shares after the committee rotates — nobody will notice."** Proactive security requires fresh shares after each rotation. Reusing shares across epochs enables an adversary who slowly compromises parties over time to reconstruct the key.

6. **"The FHE bootstrapping budget calculation is a rough estimate."** Budget exhaustion causes silent decryption failure — the ciphertext decrypts to random noise with no error indication. $200K+ of encrypted data becomes irrecoverable garbage.

7. **"The MPC protocol is constant-time because we used constant-time operations."** True constant-time requires uniform memory access patterns, no data-dependent branching, and identical instruction counts across all execution paths. A single if-statement on secret data leaks through timing.

8. **"We sourced entropy from /dev/urandom — that's sufficient."** On VMs, containers, and embedded devices, `/dev/urandom` may have dangerously low entropy at boot. For key ceremonies, use multiple independent entropy sources with statistical validation (SP 800-90B).

**If you are uncertain about any security property, escalate to a cryptographic protocol audit with formal verification (ProVerif/Tamarin/EasyCrypt) before deployment.**

---

## 16. Gotchas & Pitfalls

### Critical Failures by Domain

| # | Domain | Pitfall | Impact | Mitigation |
|---|--------|---------|--------|------------|
| 1 | FHE | CKKS used for exact equality checks — comparison always fails due to approximation noise | $500K+ financial calculation error, incorrect access control decisions | Use BGV/BFV for equality; CKKS only for approximate statistics/ML |
| 2 | MPC | Garbled circuit evaluation timing leaks circuit depth — attacker correlates wall-clock time with computation structure | Partial key leakage, circuit structure recovery | Uniform circuit padding, random gate scheduling, fixed-time evaluation |
| 3 | TEE | SGX LVI/Plundervolt speculative execution bypass reads enclave memory through voltage fault injection | $1M+ key material exfiltration from production enclaves | Apply LVI/MMIO mitigations, update microcode, monitor TCB recovery |
| 4 | Threshold | Signature share reuse across committee rotations — adversary who compromises t parties across epochs reconstructs key | Full key compromise, irreversible in most custody systems | Proactive resharing with fresh randomness each epoch, verify share freshness |
| 5 | PQC | Hybrid implementation silently falls back to classical-only on PQC negotiation failure | Classical-only security despite claiming quantum resistance | Fail closed: reject connection if either KEM fails, log both results |
| 6 | TEE | Attestation verification omits certificate chain validation — accepts revoked TCB signatures | Attacker signs arbitrary quotes with compromised but unexpired PCK | Full chain: quote -> PCK -> processor CA -> root, check CRL freshness |
| 7 | FHE | Bootstrapping budget exhausted mid-computation — ciphertext decrypts to random noise with no error signal | $200K+ encrypted data corruption, irreversible data loss | Static budget analysis + runtime level tracking, conservative margin (2+ levels) |
| 8 | Entropy | /dev/urandom on freshly-booted VM/container returns deterministic output before entropy pool initialized | Predictable keys generated in early boot sequence | Block boot until entropy pool seeded (getrandom with GRND_RANDOM), mix hardware RNG |
| 9 | MPC | OT extension correlation reuse across sessions — attacker correlates transcripts to break OT security | Loss of OT security = loss of MPC security for all GMW/Yao protocols | Fresh base OTs per session, use OT extension with random oracle model proofs |
| 10 | PQC | X.509 hybrid certificate with single signature — verifier accepts classical-only path | Downgrade to classical-only certificate validation | Dual signature verification required, reject certs with only one valid signature |

### Code-Level Gotchas

```python
# GOTCHA 1: Non-constant-time comparison in MPC
# WRONG — leaks secret through branch timing
if secret_value == 0:
    result = compute_path_a()
else:
    result = compute_path_b()

# CORRECT — both paths computed, selection via arithmetic
path_a = compute_path_a()
path_b = compute_path_b()
result = path_a + (secret_value != 0) * (path_b - path_a)

# GOTCHA 2: CKKS equality check
# WRONG — CKKS is approximate, equality is meaningless
if enc_a == enc_b:  # NEVER true, even for semantically equal values
    execute_high_value_action()

# CORRECT — Use BFV/BGV for equality-dependent logic
# Or compute: |a-b| < epsilon (approximate comparison)
diff = enc_a - enc_b
threshold_test = (diff * diff).decrypt() < epsilon**2

# GOTCHA 3: Unvalidated attestation nonce
# WRONG — No nonce binding, attacker replays old attestation
quote = generate_quote(enclave_pk, b"")

# CORRECT — Bind to fresh challenge
nonce = os.urandom(32)
quote = generate_quote(enclave_pk, nonce)
assert verify_quote(quote, nonce)  # Nonce prevents replay
```

---

## 17. References

This skill is supported by in-depth reference documents in the `references/` directory. Each provides detailed specifications, attack models, and deployment patterns:

| Reference File | Contents | When to Read |
|---|---|---|
| `mpc-protocol-comparison.md` | MP-SPDZ protocol matrix (40+ protocols), Shamir optimization, garbled circuit with half-gates, OT extension parameters | Selecting MPC protocol for your threat model |
| `fhe-scheme-selection.md` | TFHE/CKKS/BGV/BFV decision matrix with latency benchmarks, bootstrapping cost analysis, HEIR pipeline configuration | Choosing FHE scheme for specific computation |
| `threshold-signature-patterns.md` | FROST two-round protocol (RFC 9591), BLS non-interactive aggregation, GG20 multi-round ECDSA, CGGMP optimized | Implementing threshold signing for custody |
| `tee-attestation-workflow.md` | SGX DCAP v4 flow, SEV-SNP VCEK chain, Nitro PCR binding, ARM CCA token verification, attestation service integration | Deploying remote attestation infrastructure |
| `post-quantum-migration-guide.md` | NIST FIPS 203/204/205 standards, hybrid certificate X.509 extensions, TLS 1.3 PQC ciphersuites, migration timeline templates | Planning organizational PQC migration |
| `key-management-ceremony.md` | HSM PKCS#11 operations, Shamir backup with Feldman VSS, entropy health monitoring (SP 800-90B), split-knowledge procedures | Designing key generation ceremonies |
| `cryptographic-agility-patterns.md` | Algorithm registry design, protocol negotiation with downgrade prevention, hybrid middleware, crypto inventory automation | Building agile cryptographic infrastructure |
| `mpc-security-hardening.md` | Constant-time circuit evaluation, side-channel defenses, malicious majority detection, identifiable abort handling | Hardening MPC deployments for production |
| `fhe-performance-optimization.md` | Bootstrapping budget tracking, SIMD packing strategies, batching rotation keys, level-aware circuit design | Optimizing FHE for latency and throughput |
| `threshold-key-resharing.md` | Herzberg dynamic proactive scheme, committee rotation protocol, share freshness verification, distributed key generation (DKG) | Implementing non-disruptive key rotation |

### External Standards & Specifications

- **MPC:** MP-SPDZ documentation (https://github.com/data61/MP-SPDZ), SPDZ paper (Damgard et al., CRYPTO 2012)
- **FHE:** TFHE deep dive (Chillotti et al., JoC 2020), CKKS (Cheon et al., ASIACRYPT 2017), HEIR compiler (https://heir.dev)
- **Threshold:** FROST RFC 9591 (IETF CFRG), BLS signatures (Boneh-Lynn-Shacham, JoC 2004), GG20/CGGMP specifications
- **TEE:** Intel SGX DCAP (https://download.01.org/intel-sgx/), AMD SEV-SNP API (https://www.amd.com/en/developer/sev.html), AWS Nitro Enclaves SDK
- **PQC:** NIST FIPS 203/204/205, NIST SP 800-208 (stateful hash-based), IETF TLS PQC drafts
- **Key Management:** NIST SP 800-57 (key management), PKCS#11 v3.0, NIST SP 800-90B (entropy)

### Tool Versions Used in Examples

| Tool | Version | Purpose |
|---|---|---|
| MP-SPDZ | 0.3.8+ | MPC DSL, 40+ protocol backends |
| Zama Concrete | 2.6+ | TFHE with programmable bootstrapping |
| Microsoft SEAL | 4.1+ | CKKS/BFV homomorphic encryption |
| OpenFHE | 1.2+ | Multi-scheme FHE (TFHE/CKKS/BGV/BFV) |
| Google HEIR | 0.0.1+ | MLIR-based FHE compiler |
| liboqs | 0.10+ | Post-quantum cryptography |
| frost-secp256k1 | 2.0+ | FROST threshold Schnorr signatures |
| Intel SGX SDK | 2.23+ | SGX enclave development |
| PyKCS11 | 1.5+ | HSM PKCS#11 interface |

---
