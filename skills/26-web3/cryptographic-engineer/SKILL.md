---
name: cryptographic-engineer
description: "Use when implementing threshold cryptography (FROST Schnorr, BLS aggregation, t-of-n signing), deploying Multi-Party Computation (MP-SPDZ with 40+ protocols, Shamir Secret Sharing, Garbled Circuits), configuring Fully Homomorphic Encryption (HEIR compiler, Concrete for TFHE, SEAL for CKKS/BFV, OpenFHE multi-scheme), engineering Trusted Execution Environments (Intel SGX remote attestation, AMD SEV-SNP confidential VMs, AWS Nitro Enclaves), planning post-quantum cryptographic migration (ML-KEM Kyber, ML-DSA Dilithium, SLH-DSA SPHINCS+), designing key management ceremonies (HSM with PKCS#11, Shamir Secret Sharing backup, entropy health monitoring). Handles MPC protocol selection (dishonest vs honest majority, reactive vs non-reactive computation, preprocessing), FHE scheme selection (TFHE for bitwise, CKKS for approximate, BGV/BFV for exact), threshold signing architectures (FROST two-round, BLS non-interactive, key resharing), TEE attestation workflow (SGX DCAP, SEV-SNP VCEK, Nitro PCR), and PQC migration strategy (crypto inventory, hybrid key exchange, certificate chain migration). Do NOT use for basic encryption (use security-engineer), TLS configuration (use devops-engineer), smart contract cryptography (use zkp-engineer or smart-contract-auditor), or password hashing (use backend-developer)."
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: specialized
status: stable
version: "1.0.0"
updated: 2026-07-24
tags: [cryptography, mpc, fhe, threshold-signatures, tee, post-quantum, key-management]
token_budget: 3500
dependencies:
  tools: [mp-spdz, zama-concrete, microsoft-seal, openfhe, heir, liboqs, frost-secp256k1, sgx-sdk, pykcs11]
  packages: []
  permissions: [hsm-access, tee-enclave-signing]
output:
  type: "protocol-spec, implementation, migration-plan"
  path_hint: "cryptographic-engineer/"
chain:
  consumes_from:
    - security-engineer
    - system-architect
    - backend-developer
  feeds_into:
    - zkp-engineer
    - smart-contract-auditor
    - compliance-officer
  alternatives:
    - security-engineer
    - devops-engineer
---
> **Portability target:** Spec-level (runs on Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI). No vendor-specific frontmatter fields.

<!-- QUICK: 30s -->
## Route the Request

```
Cryptographic requirement identified
├─ Need encryption at rest/in-transit with known primitives
│  └─ Route to: security-engineer (basic crypto handled downstream)
├─ Need threshold signing, MPC, FHE, or PQC
│  └─ Route to: Cryptographic Engineer (this skill)
│
├─ What type of secure computation?
│  ├─ N parties compute on private inputs → MPC Protocol Selection
│  ├─ Compute on encrypted data without decryption → FHE Scheme Selection
│  ├─ Sign with t-of-n key shares → Threshold Signature Architecture
│  ├─ Run workload in hardware-enforced isolation → TEE Platform Selection
│  ├─ Future-proof against quantum attackers → PQC Migration Path
│  └─ Generate, distribute, or rotate key material → Key Ceremony Design
│
├─ Need zero-knowledge proof instead of general MPC?
│  └─ Route to: zkp-engineer
│
├─ Smart contract cryptography (on-chain verification, signatures)?
│  └─ Route to: smart-contract-auditor
│
└─ Need compliance certification (FIPS 140, Common Criteria)?
   └─ Route to: compliance-officer
```

<!-- STANDARD: 3min -->
## Ground Rules — Read Before Anything Else

1. **Never roll your own crypto.** Always use formally verified implementations from established libraries (libsodium, OpenSSL, Bouncy Castle). Custom cryptographic code is the #1 source of critical vulnerabilities.

2. **Never hard-code keys, nonces, or entropy seeds.** Keys must come from HSM/KMS with audit trail. Nonces must be cryptographically random per invocation. Entropy must be validated against NIST SP 800-90B.

3. **Favor memory-safe languages for crypto implementations.** C/ASM crypto code is acceptable only for performance-critical paths with formal verification. All other crypto code must be Rust, Go, or higher-level bindings.

4. **PQC migration must start now -- not when quantum breaks RSA.** Hybrid certificates and dual-key exchange should be deployed before production reliance on classical-only schemes becomes entrenched.

5. **Admit uncertainty -- never fabricate API details.** If uncertain about an API method, package version, or configuration syntax, say so explicitly. Never invent a function signature or configuration key. Hallucinated crypto code cannot be distinguished from working code without expert review.

6. **Flag your knowledge cutoff for rapidly evolving crypto domains.** PQC standards, TEE attestation APIs, and FHE compiler toolchains evolve quarterly. State your cutoff date and recommend verifying against current docs.

7. **Never guess security configurations.** If unsure about the correct KDF parameters, AEAD nonce size, or MPC protocol security model, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."

8. **Distinguish what you know from what you infer.** Explicitly mark statements as: [VERIFIED] -- from official docs, [COMMON-PRACTICE] -- widely used but not authoritative, [INFERRED] -- your best guess based on patterns, [UNKNOWN] -- you're unsure.

<!-- QUICK: 30s -->
## When to Use

- When implementing threshold cryptography: FROST Schnorr (RFC 9591), BLS aggregation, t-of-n signing with identifiable aborts
- When deploying MPC protocols: MP-SPDZ with dishonest/honest majority selection, Shamir Secret Sharing, Garbled Circuits with oblivious transfer
- When configuring FHE: HEIR compiler for MLIR-based pipeline, Concrete for TFHE programmable bootstrapping, SEAL for CKKS approximate arithmetic, OpenFHE for multi-scheme support
- When engineering TEE attestation: Intel SGX DCAP quote verification, AMD SEV-SNP VCEK certificate chain, AWS Nitro Enclaves PCR binding, ARM CCA Realm token verification
- When planning PQC migration: crypto inventory via TLS fingerprinting, ML-KEM-1024 key encapsulation, ML-DSA Dilithium signatures, hybrid X.509 certificates with NIST Round 3 algorithms
- When designing key management ceremonies: HSM PKCS#11 operations, Shamir backup with Feldman Verifiable Secret Sharing, multi-party entropy ceremonies with SP 800-90B validation
- When building cryptographic agility layers: algorithm registry design, protocol negotiation with downgrade prevention, hybrid middleware for cross-scheme compatibility
- When auditing cryptographic code for side-channel resistance: constant-time verification, memory access pattern analysis, timing attack mitigation

<!-- STANDARD: 3min -->
## Decision Trees

### Tree 1: MPC Protocol Selection

```
MPC needed for N parties
├─ All parties may be malicious?
│  ├─ YES → Dishonest majority protocol (SPDZ2k, MASCOT)
│  │  └─ Requires preprocessing → Use function-independent correlated randomness
│  └─ NO → Honest majority protocol (Shamir, Rep3)
│     └─ Faster, less communication, but security requires >50% honest
├─ Computation is interactive (multi-round)?
│  ├─ YES → Reactive computation (SPDZ with state)
│  └─ NO → Non-reactive (single-shot function evaluation)
├─ Number of parties:
│  ├─ 2 parties → Yao's Garbled Circuits (fastest for 2PC)
│  ├─ 3-10 parties → Shamir Secret Sharing (efficient for small groups)
│  └─ 10+ parties → SPDZ/MP-SPDZ (scales with preprocessing)
└─ Performance requirement?
   ├─ < 1s latency → Garbled Circuits or honest-majority Shamir
   ├─ < 1min → SPDZ with offline preprocessing
   └─ > 1min acceptable → Any protocol; choose by security model
```

### Tree 2: FHE Scheme Selection

```
FHE needed for computation on encrypted data
├─ Computation type:
│  ├─ Bitwise operations (comparison, equality, bit extraction)
│  │  └─ TFHE (Concrete) — <50ms per gate, programmable bootstrapping
│  ├─ Approximate arithmetic on floating-point vectors
│  │  └─ CKKS (SEAL, OpenFHE) — SIMD operations, leveled scheme
│  │  └─ WARNING: 0.001% error on $500M = $5,000. Use BGV/BFV for exact.
│  ├─ Exact integer arithmetic
│  │  └─ BGV (OpenFHE, SEAL) — exact, leveled, good for integers
│  │  └─ BFV (OpenFHE, SEAL) — exact, better for small modulus
│  └─ Mixed: bitwise + arithmetic
│     └─ Multi-scheme via OpenFHE or CHIMERA hybrid
├─ Bootstrapping needed?
│  ├─ YES → Must budget depth: each bootstrap adds 10-60s overhead
│  │  └─ Level-aware circuit design to minimize bootstraps
│  └─ NO → Leveled scheme sufficient; set multiplicative depth upfront
└─ Latency requirement:
   ├─ Interactive (< 100ms) → TFHE only (programmable bootstrap)
   ├─ Batch (seconds) → CKKS/BGV with SIMD packing
   └─ Offline (minutes+) → Any scheme; optimize for throughput
```

### Tree 3: Threshold Signature Architecture

```
Threshold signing required for t-of-n key shares
├─ Interaction model:
│  ├─ Two-round signing acceptable → FROST (RFC 9591)
│  │  └─ Identifiable aborts, key resharing, committee rotation
│  ├─ Non-interactive required → BLS threshold signatures
│  │  └─ Signature aggregation without interaction, needs pairing-friendly curve
│  └─ Multi-round ECDSA → GG20 or CGGMP
│     └─ High round complexity, but works with existing ECDSA infrastructure
├─ Key rotation:
│  ├─ Proactive security with shareholder changes
│  │  └─ Herzberg dynamic proactive secret sharing
│  └─ Static committee → Single DKG ceremony, no resharing
├─ Abort handling:
│  ├─ Identifiable abort needed → FROST (identifies misbehaving party)
│  └─ Silent abort acceptable → Basic threshold protocols
└─ Curve requirements:
   ├─ Pairing-friendly → BLS (BLS12-381, BN254)
   └─ Non-pairing → FROST (secp256k1, P-256 via frost-secp256k1)
```

### Tree 4: Post-Quantum Migration Path

```
PQC migration triggered: assess current crypto inventory
├─ TLS termination → Hybrid key exchange (ML-KEM + X25519)
│  └─ Use TLS 1.3 hybrid ciphersuites (draft-ietf-tls-hybrid-design)
├─ Certificate chain → Hybrid X.509 (ML-DSA + ECDSA)
│  └─ Dual cert chain with backward-compatible CRL/OCSP
├─ Signature verification → ML-DSA (Dilithium) or SLH-DSA (SPHINCS+)
│  ├─ High-throughput → ML-DSA (faster verification)
│  └─ Conservative security → SLH-DSA (hash-based, minimal assumptions)
├─ Key encapsulation → ML-KEM (Kyber) FIPS 203
│  └─ Replace RSA-KEM, ECDH with ML-KEM-768 or ML-KEM-1024
└─ Risk level:
   ├─ Data must survive 10+ years → Migrate now (harvest-now-decrypt-later)
   ├─ High-value assets → Hybrid mode: classical + PQC dual agreement
   └─ Low-risk → Monitor, plan migration within 2 years
```

<!-- STANDARD: 3min -->
## Core Workflow

### Phase 1: Requirements Analysis (est. 1-2 hours)
1. Identify cryptographic requirement (threshold signing, MPC, FHE, TEE, PQC, key ceremony)
2. Document threat model: who are the adversaries, what are their capabilities, what security property is needed?
3. Determine operational constraints: latency, throughput, number of parties, hardware availability
4. Select candidate primitives via Decision Trees
**Completion criteria:** Requirements document with threat model, security parameter selection, and primitive shortlist signed off by security-engineer.

### Phase 2: Primitive Selection & Protocol Design (est. 4-8 hours)
1. Run through full Decision Trees for the selected domain
2. Select specific protocol/scheme with security parameters
3. Design protocol flow: messages exchanged, serialization format, timeout handling
4. Document security assumptions: computational vs information-theoretic, honest vs dishonest majority, trusted setup requirements
**Completion criteria:** Protocol specification document with security proof references, parameter selection rationale, and alternative analysis.

### Phase 3: Implementation (est. 8-40 hours depending on complexity)
1. Select implementation language and library (MP-SPDZ, Concrete, SEAL, etc.)
2. Implement core protocol logic following library patterns
3. Write test vectors and integration tests
4. Implement error handling: identifiable aborts, timeout recovery, state reconciliation
**Completion criteria:** Working implementation passing all test vectors. All error paths produce clear diagnostic messages.

### Phase 4: Security Verification (est. 8-20 hours)
1. Verify constant-time execution: no data-dependent branching, uniform memory access
2. Run formal verification tools (ProVerif, Tamarin, EasyCrypt) for protocol security
3. Side-channel analysis: timing, power, cache-timing attack surface
4. Fuzz test inputs: malformed messages, boundary values, replay attacks
**Completion criteria:** Formal verification log, side-channel analysis report, fuzz test results with 100K+ test cases.

### Phase 5: Deployment & Ceremony (est. 4-16 hours)
1. Generate key material via HSM or secure multi-party ceremony
2. Validate entropy quality per NIST SP 800-90B
3. Deploy with secure configuration: TEE attestation verification, audit logging
4. Verify production integration: end-to-end test on testnet/staging
**Completion criteria:** Deployed system with audit trail. Ceremony log with participant attestations. Monitoring dashboards for cryptographic operations.

### Phase 6: Ongoing Monitoring & Migration (ongoing)
1. Monitor for cryptanalytic advances affecting selected primitives
2. Track library updates and security advisories
3. Plan periodic key rotation and protocol upgrades
4. Execute cryptographic agility migration when needed
**Completion criteria:** Monitoring runbook, upgrade schedule, incident response plan for cryptanalytic breakthroughs.

<!-- STANDARD: 3min -->
## Best Practices

| # | Domain | Best Practice |
|---|--------|---------------|
| 1 | All Cryptography | Use AEAD (ChaCha20-Poly1305 or AES-GCM) for all symmetric encryption. Never use ECB mode or raw RSA. |
| 2 | All Cryptography | Keys must be managed via KMS or HSM with audit trail. Never store keys in environment variables, config files, or source code. |
| 3 | MPC | Always verify the adversary model matches deployment reality. Dishonest majority deployed as honest majority = catastrophic failure. |
| 4 | MPC | Preprocessing must use function-independent correlated randomness to avoid selective failure attacks. |
| 5 | FHE | Budget bootstrapping depth before deployment. Budget exhaustion causes silent decryption failure with no error indication. |
| 6 | FHE | Level-aware circuit design: minimize multiplicative depth by reorganizing computation order. Each bootstrap level costs 10-60s. |
| 7 | Threshold Signatures | Implement identifiable aborts for production systems. In a t-of-n scheme, knowing WHICH party failed is critical for operational debugging. |
| 8 | TEE | Always verify the full certificate chain in attestation, not just the quote signature. A compromised-but-not-yet-expired PCK can sign arbitrary quotes. |
| 9 | PQC | Hybrid mode must fail closed. If PQC fails (packet corruption, CPU overload on lattice), the system must reject the connection, not fall back to classical-only. |
| 10 | Key Management | Use multiple independent entropy sources with statistical validation (SP 800-90B). /dev/urandom alone is insufficient for key ceremonies on VMs or embedded devices. |
| 11 | Key Management | Proactive security requires fresh shares after each committee rotation. Reusing shares across epochs enables gradual compromise. |
| 12 | Cryptographic Agility | Maintain an algorithm inventory with usage tracking. Without inventory, you cannot assess the blast radius of a cryptanalytic breakthrough against any single scheme. |
| 13 | Implementation | Favor formally verified implementations (HACL*, EverCrypt, libsodium) over hand-rolled crypto, even from well-known libraries. |
| 14 | Implementation | Constant-time requires uniform memory access patterns, no data-dependent branching, and identical instruction counts across all execution paths. A single if-statement on secret data leaks through timing. |

<!-- DEEP: 10+min -->
## Error Decoder

### War Story 1: FHE Bootstrapping Budget Exhaustion

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| Encrypted data silently decrypts to random noise; no error message or warning. | FHE scheme bootstrapping budget was calculated as a rough estimate rather than exact. Deep circuits exhausted the noise budget mid-computation. | Recalculate bootstrapping budget precisely for each circuit level. Add noise budget monitoring that raises an alert before budget drops below 20%. Implement automatic circuit reorganization when budget is insufficient. | Budget exhaustion causes silent decryption failure in FHE. Unlike classical crypto where failures are loud, a ciphertext that exhausted its budget decrypts to random garbage with zero error indication. Budget tracking must be as rigorous as memory management -- every level costs real noise headroom. Always over-provision budget by 30% for safety margin. |

### War Story 2: MPC Dishonest Majority Assumption Mismatch

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| During a multi-party computation, one party reconstructs all other parties' secret inputs without detection. Protocol had no leakage indicators. | The protocol was designed for honest majority (Shamir Secret Sharing, Rep3) but deployed in a setting where one of five parties was actively malicious. The protocol had no mechanism to detect or prevent malicious behavior from a minority. | Switch to a dishonest majority protocol (SPDZ2k with MACs, MASCOT) that provides security against up to N-1 malicious parties. Add identifiable abort for detection of misbehavior. Use information-theoretic MACs to authenticate all shared values. | A protocol's security model is not a suggestion -- it is a hard bound. Deploying honest-majority MPC in a dishonest-majority setting is equivalent to deploying HTTP with the expectation of TLS-level security. Always verify that the operational threat model matches protocol assumptions before deployment. |

### War Story 3: TEE Attestation Chain Verification Skipped

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| Remote attestation endpoint accepts attestation quotes from an enclave running compromised firmware. The verified quote signature is valid but the TCB (Trusted Computing Base) is revoked. | The attestation verification code checks the quote signature but skips certificate chain validation. An attacker with access to a compromised-but-not-yet-expired Platform Configuration Key (PCK) can sign arbitrary attestation quotes that pass signature verification. | Implement full DCAP quote verification including PCK certificate chain validation against Intel's root CA. Verify TCB status via the Intel Provisioning Certificate Service (PCS). Check TCB expiration and revocation status on every attestation. Implement a CRL cache with aggressive refresh. | Quote signature verification alone is insufficient. The full certificate chain -- including PCK, TCB level, and root CA -- must be validated on every attestation. A compromised enclave with valid-looking timestamps will pass partial verification. Defense in depth applies to the verification pipeline, not just the application. |

### War Story 4: PQC Hybrid Downgrade Attack

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| Under heavy network load, a PQC+classical hybrid key exchange silently falls back to classical-only. An attacker observing the network induces the fallback condition then breaks the classical exchange. | The hybrid implementation treats the PQC key exchange as an enhancement that can be dropped: "If ML-KEM fails (timeout, malformed response), fall back to X25519-only." An adversary can force the PQC failure by delaying or corrupting the ML-KEM share. | Hybrid must fail closed: if the PQC component of the exchange fails, reject the connection entirely. Implement atomic key agreement where both ML-KEM and X25519 shares MUST complete before either is used. Log all hybrid exchange failures for security monitoring. | A hybrid scheme that falls back to classical-only is not hybrid security -- it is classical security with extra latency. The adversary's incentive is exactly to induce the fallback condition. Any PQC migration must follow the principle: both or nothing. Ratcheted protocols (like Signal's PQXDH) provide a better model. |

### War Story 5: Threshold Share Reuse After Committee Rotation

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| Over six months, an attacker who slowly compromises one party per month eventually reconstructs the full private key. Each compromise reveals only one share, but across epochs the attacker accumulates t-of-n shares. | The threshold signing scheme reuses the same secret shares across committee rotations. While the identity of committee members changes, the underlying shares remain unchanged. An adversary who compromises one party each rotation over N rotations eventually collects t shares. | Implement proactive secret sharing with Herzberg's dynamic scheme: after each committee rotation, generate fresh shares via distributed re-sharing. Use the FROST key resharing protocol that produces combinatorially independent shares. Verify share freshness before each signing round. | Threshold signing committees require proactive security: fresh shares after each rotation. Reusing shares across epochs creates a time-accumulation attack surface. An adversary doesn't need t parties simultaneously -- they just need them over time. Share freshness verification must be part of every signing round's preconditions. |

### War Story 6: Constant-Time Violation in MPC Implementation

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| Timing analysis of an MPC node reveals secret-dependent execution time. Statistical analysis over 10K queries reconstructs secret shares from timing variation of 0.5 microseconds. | The MPC implementation uses an if-statement on a secret-shared value to select between computation paths. While the if-condition is computed on secret data, the branch selection leaks one bit of information per conditional through timing. | Use oblivious selection (cmov, conditional swap) for all secret-dependent branching. Verify constant-time at the assembly/LLVM IR level using ctgrind or dataflow analysis. Add fuzz testing that measures execution time variance across all input combinations. | Constant-time is not optional in MPC. Every conditional branch on secret data creates a timing side channel that accumulates across protocol rounds. A single if-statement leaking 1 bit per round, over 10K rounds, reconstructs a 256-bit secret. Memory-safe languages help but do not guarantee constant-time execution -- verification must be at the instruction level. |

<!-- STANDARD: 3min -->
## Scale Depth: Solo => Small => Medium => Enterprise

### Solo (0-10 users, personal research or small team)
- **Scope:** Single protocol implementation, one FHE scheme, basic threshold signatures
- **Tools:** MP-SPDZ basic protocols, SEAL or Concrete, frost-secp256k1 library
- **Key management:** Local HSM or software key store with encrypted backup
- **Attestation:** Basic SGX DCAP or Nitro Enclaves for single enclave
- **PQC:** Algorithm inventory for personal projects, experimental migration
- **Constraints:** Manual key rotation, no formal verification, limited side-channel analysis

### Small Team (10-100 users, single product or startup)
- **Scope:** 2-3 protocol implementations, multi-scheme FHE pipeline, threshold signing for custody
- **Tools:** OpenFHE for multi-scheme support, MP-SPDZ curated protocols, formal verification for critical paths
- **Key management:** Cloud KMS (AWS KSM, GCP Cloud KMS) with HSM backing
- **Attestation:** Automated DCAP/SEV-SNP verification pipeline
- **PQC:** Hybrid migration for production TLS and certificate chains
- **Constraints:** Scheduled key rotation, formal verification for high-value circuits, basic side-channel review

### Medium Team (100-10K users, growth-stage product)
- **Scope:** Full protocol suite, production MPC/FHE infrastructure, threshold signing at scale
- **Tools:** HEIR compiler for FHE optimization, custom MPC protocol extensions, Certora/EasyCrypt formal verification
- **Key management:** Dedicated HSM cluster with PKCS#11, Shamir backup with Feldman VSS
- **Attestation:** Multi-platform attestation (SGX + SEV-SNP + Nitro), attestation service with CRL management
- **PQC:** Organization-wide crypto inventory, migration plan with timeline, hybrid production deployment
- **Constraints:** Automated key rotation with proactive security, continuous side-channel monitoring, incident response for cryptanalytic events

### Enterprise (10K+ users, financial infrastructure or regulated)
- **Scope:** Organization-wide cryptographic agility layer, multi-scheme FHE at scale, global threshold signing infrastructure
- **Tools:** Custom HEIR passes for domain-specific FHE, EasyCrypt formal proofs for all critical protocols, automated crypto inventory and migration orchestration
- **Key management:** Geo-distributed HSM clusters, split-knowledge ceremonies with independent witnesses, NIST SP 800-57 compliant lifecycle
- **Attestation:** Federated attestation across cloud providers, automated TCB monitoring with revocation alerting
- **PQC:** Complete hybrid migration with quantum-safe fallback, harvest-now-decrypt-later protection for all data with 10+ year confidentiality requirements
- **Constraints:** FIPS 140-3 Level 3+ compliance, Common Criteria certification, continuous audit, dedicated crypto team

### Transition Triggers
- **Solo => Small:** Second protocol implementation required; first key rotation scenario without downtime
- **Small => Medium:** Formal verification needed after incident; PQC migration becomes business-critical
- **Medium => Enterprise:** Regulatory mandate (FIPS, CC); TVL or assets under management exceed $100M; customer contracts require certified cryptography

<!-- STANDARD: 3min -->
## Production Readiness Checklist

| # | Item | Ref |
|---|------|-----|
| CR1 | All cryptographic primitives use formally verified implementations (HACL*, libsodium, or vendor-verified libraries) | [V1] |
| CR2 | Keys managed via HSM or KMS with full audit trail. No keys in source code, env vars, or config files | [V2] |
| CR3 | Entropy validated per NIST SP 800-90B. Multiple independent entropy sources for key ceremonies | [V3] |
| CR4 | Constant-time verified at instruction level (ctgrind, dataflow analysis). No secret-dependent branching | [V4] |
| CR5 | FHE bootstrapping budget calculated with 30% safety margin. Noise monitoring with early warning | [V5] |
| CR6 | MPC protocol security model matches deployment threat model (dishonest vs honest majority verified) | [V6] |
| CR7 | TEE attestation chain fully validated (PCK certificate chain, TCB status, CRL check) | [V7] |
| CR8 | PQC hybrid mode fails closed. No classical-only fallback on PQC failure | [V8] |
| CR9 | Threshold shares refreshed after each committee rotation. Proactive security with Herzberg scheme | [V9] |
| CR10 | Cryptographic agility layer implemented: algorithm registry, protocol negotiation, downgrade prevention | [V10] |
| CR11 | Security proofs documented and externally reviewable (ProVerif/Tamarin/EasyCrypt logs) | [V11] |
| CR12 | Incident response plan for cryptanalytic breakthrough: impact assessment, migration triggers, communication plan | [V12] |
| CR13 | Side-channel analysis completed: timing, power, cache-timing, electromagnetic for TEE environments | [V13] |
| CR14 | Library update monitoring automated: CVE tracking, dependency scanning, update testing pipeline | [V14] |
| CR15 | Key lifecycle documented: generation, distribution, rotation, revocation, destruction with attestation | [V15] |

<!-- STANDARD: 3min -->
## Cross-Skill Coordination

| Direction | Skill | Handoff |
|-----------|-------|---------|
| **Upstream** | `security-engineer` | Threat model, asset inventory, trust boundaries, security parameter requirements |
| **Upstream** | `system-architect` | System boundaries, integration patterns, deployment topology, trust model |
| **Upstream** | `backend-developer` | API contracts, data flow, key storage integration, application-level crypto integration |
| **Downstream** | `zkp-engineer` | Cryptographic primitives, proof system security, trusted setup parameters, circuit constraints |
| **Downstream** | `smart-contract-auditor` | On-chain crypto verification, signature scheme audit, verifier contract security |
| **Downstream** | `compliance-officer` | FIPS 140-3/Common Criteria certification requirements, audit evidence collection |

<!-- QUICK: 30s -->
## What Good Looks Like

The output of a cryptographic engineering engagement is:

- **Protocol specification** with formal security model, parameter selection rationale, and proof references
- **Implementation** using verified libraries, passing all test vectors, with constant-time verification
- **Key ceremony documentation** with entropy validation, participant attestations, and HSM audit logs
- **TEE attestation pipeline** with full certificate chain validation, TCB monitoring, and CRL management
- **PQC migration plan** with crypto inventory, hybrid deployment strategy, and timeline with failure triggers
- **Cryptographic agility layer** with algorithm registry, downgrade prevention, and migration automation

All cryptographic operations use AEAD or stronger. Keys are managed via KMS/HSM with audit trail. PQC migration plan is documented and funded. Every implementation has a security proof or references a published proof.

<!-- STANDARD: 3min -->
## References

### Inline Reference Files in `references/`

This skill is supported by 27 reference files. Key reference documents:

| File | Contents |
|------|----------|
| `references/decision-trees.md` | Summary of all 6 decision tree domains |
| `references/2-decision-tree-mpc-protocol-selection.md` | MPC protocol matrix (40+ protocols), Shamir optimization, garbled circuit |
| `references/3-decision-tree-fhe-scheme-selection.md` | TFHE/CKKS/BGV/BFV decision matrix with latency benchmarks |
| `references/4-decision-tree-threshold-signature-architecture.md` | FROST, BLS, GG20, CGGMP detailed patterns |
| `references/5-decision-tree-tee-platform-selection.md` | SGX DCAP v4, SEV-SNP VCEK, Nitro PCR, ARM CCA |
| `references/6-decision-tree-post-quantum-migration-path.md` | NIST FIPS 203/204/205, hybrid certs, TLS 1.3 PQC |
| `references/7-decision-tree-key-ceremony-design.md` | HSM PKCS#11, Shamir backup, Feldman VSS, entropy health |
| `references/14-cryptographic-agility-architecture.md` | Algorithm registry, protocol negotiation, hybrid middleware |
| `references/16-gotchas--pitfalls.md` | 16-domain pitfall matrix with impact and mitigation |

### External Standards & Specifications

| Standard | Purpose |
|----------|---------|
| FIPS 203 (ML-KEM) | Post-quantum key encapsulation mechanism |
| FIPS 204 (ML-DSA) | Post-quantum lattice-based digital signature |
| FIPS 205 (SLH-DSA) | Post-quantum stateless hash-based signature |
| NIST SP 800-57 | Key management recommendation |
| NIST SP 800-90B | Entropy source health testing |
| PKCS#11 v3.0 | Cryptographic token interface standard |
| RFC 9591 (FROST) | Threshold Schnorr signature scheme |
| SPDZ (Damgard et al., CRYPTO 2012) | MPC with preprocessing |

### Tool Versions

| Tool | Latest Version | Domain |
|------|----------------|--------|
| MP-SPDZ | 0.3.8+ | MPC protocols |
| Zama Concrete | 2.6+ | TFHE |
| Microsoft SEAL | 4.1+ | CKKS/BFV |
| OpenFHE | 1.2+ | Multi-scheme FHE |
| Google HEIR | 0.0.1+ | FHE compiler |
| liboqs | 0.10+ | Post-quantum crypto |
| frost-secp256k1 | 2.0+ | Threshold Schnorr |
| Intel SGX SDK | 2.23+ | TEE enclave |
| PyKCS11 | 1.5+ | HSM interface |
