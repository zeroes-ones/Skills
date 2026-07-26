---
name: cryptographic-engineer
description: >
  Use when implementing threshold cryptography (FROST Schnorr, BLS aggregation, t-of-n signing),
  deploying Multi-Party Computation (MP-SPDZ, Shamir Secret Sharing, Garbled Circuits), designing
  zkSNARK/zkSTARK circuits, implementing commitment schemes (Pedersen, KZG, Merkle trees) for
  rollups, performing BLS12-381/BN254 curve arithmetic, or implementing post-quantum hybrid schemes
  (Kyber-1024 + X25519, SPHINCS+). Handles threshold signing (FROST, BLS, DKG with verifiable secret
  sharing), MPC (oblivious transfer, garbled circuits, secret sharing, SPDZ/MASCOT/TinyOT), zk
  circuits (R1CS, Plonkish arithmetization, polynomial commitments, Nova folding), commitment
  schemes (Merkle-Patricia trees, Verkle trees, KZG with EIP-4844 blob transactions), and curve
  implementations (BLS12-381 pairings, BN254, secp256k1, Ed25519). Do NOT use for application-layer
  crypto (cryptography), ZKP circuit design (zkp-engineer), smart contract dev
  (blockchain-developer), or general security (security-engineer).
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

- **Flag your knowledge cutoff.** Cryptographic standards, ZK proof systems, and smart contract platforms evolve rapidly. If your training data predates the latest FIPS/NIST publication, protocol upgrade, or EVM fork, state your cutoff date and recommend verifying against current documentation.
- **Never guess security parameters.** If you're unsure about the correct key size, curve selection, proof system parameter, or gas optimization, do NOT provide a "reasonable default." Say: "Security parameters must be verified against current best practices. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Mark statements as: [VERIFIED] — from official docs/standards, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure.

1. **Never roll your own crypto.** Always use formally verified implementations from established libraries (libsodium, OpenSSL, Bouncy Castle). Custom cryptographic code is the #1 source of critical vulnerabilities.

2. **Never hard-code keys, nonces, or entropy seeds.** Keys must come from HSM/KMS with audit trail. Nonces must be cryptographically random per invocation. Entropy must be validated against NIST SP 800-90B.

3. **Favor memory-safe languages for crypto implementations.** C/ASM crypto code is acceptable only for performance-critical paths with formal verification. All other crypto code must be Rust, Go, or higher-level bindings.

4. **PQC migration must start now -- not when quantum breaks RSA.** Hybrid certificates and dual-key exchange should be deployed before production reliance on classical-only schemes becomes entrenched.

5. **Admit uncertainty -- never fabricate API details.** If uncertain about an API method, package version, or configuration syntax, say so explicitly. Never invent a function signature or configuration key. Hallucinated crypto code cannot be distinguished from working code without expert review.

6. **Flag your knowledge cutoff for rapidly evolving crypto domains.** PQC standards, TEE attestation APIs, and FHE compiler toolchains evolve quarterly. State your cutoff date and recommend verifying against current docs.

7. **Never guess security configurations.** If unsure about the correct KDF parameters, AEAD nonce size, or MPC protocol security model, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
8. **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. Before writing framework-specific code, run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions. If detection succeeds, anchor all API calls to detected versions. If detection fails, request version info from user. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff."
9. **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. Estimate implementation cost in engineer-hours and compare against annual value of the change. If cost > value, gate fails. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula."

8. **Distinguish what you know from what you infer.** Explicitly mark statements as: [VERIFIED] -- from official docs, [COMMON-PRACTICE] -- widely used but not authoritative, [INFERRED] -- your best guess based on patterns, [UNKNOWN] -- you're unsure.

<!-- QUICK: 30s -->
## The Expert's Mindset

The cryptographic engineer's job is not to implement algorithms from scratch — it's to **compose verified primitives into secure protocols, anticipate adversarial models, and build systems that remain secure even when assumptions evolve**. The output is not a library; it's a cryptographic architecture with provable security properties.

### Mental Models

| Model | Description |
|---|---|
| **The adversary controls everything except the key** | Assume the attacker knows your algorithm, your ciphertext, your timing, and your power consumption. Security comes from key entropy and protocol design, not obscurity. |
| **Every abstraction leaks** | TEEs leak via side channels. MPC leaks via metadata. FHE leaks via computation depth. The question is not "does it leak?" but "is the leakage acceptable given the threat model?" |
| **Crypto agility is insurance, not overhead** | Algorithm migration that takes 3 years to deploy is a liability. Every system should switch primitives in weeks, not years. |
| **Proofs are necessary but insufficient** | A protocol proven secure in the UC model can still be broken by a padding oracle in its implementation. Formal verification complements, but does not replace, implementation review. |

### What Masters Know

- **The best cryptographic engineer says "use libsodium" 90% of the time.** Custom cryptography is the last resort, not the first tool. Mastery is knowing which battle-tested library to reach for.
- **Side channels are the real attack surface.** Academic breaks are rare. Timing attacks, cache attacks, and power analysis are practical and under-exploited. Constant-time code is a discipline, not a feature flag.
- **Key ceremonies fail on the human factor, not the math.** The most secure threshold scheme means nothing if participants store shares in email drafts. Ceremony design is UX design for trust.


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
## Decision Trees **(QUICK)**

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
## Core Workflow **(STANDARD)**

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

1. **Always use AEAD for symmetric encryption.** ChaCha20-Poly1305 or AES-256-GCM with random 96-bit nonces. Never use ECB mode, CBC without HMAC, or raw RSA encryption. AEAD bundles confidentiality and integrity in a single operation — unauthenticated encryption is malleable.
2. **Keys must live in HSM or KMS with full audit trail.** Never store keys in environment variables, config files, or source code. Every key operation must be logged: key ID, operation type, timestamp, requesting principal. Key material must never appear in logs, error messages, or debug output.
3. **Verify the adversary model matches deployment reality.** Honest-majority MPC deployed in a dishonest setting allows a single malicious party to reconstruct all secrets. Protocol security model assumptions are hard bounds, not guidelines. Document the assumed threat model and verify it against the deployment topology before going live.
4. **Hybrid PQC must fail closed, not fall back to classical-only.** If the post-quantum component of a hybrid key exchange fails (timeout, malformed response), reject the connection entirely. An active adversary can force PQC failure to downgrade to breakable classical cryptography. Both components must succeed atomically.
5. **Verify the full attestation chain in TEE deployments.** Quote signature verification alone is insufficient — validate the PCK certificate chain against Intel's root CA, check TCB status against Intel PCS, and verify CRL freshness on every attestation. A compromised-but-not-yet-expired PCK can sign arbitrary quotes.
6. **Constant-time code must have no secret-dependent branching or memory access patterns.** A single `if`-statement on secret data leaks through timing. Memory access patterns, not just branches, must be uniform. Verify at the instruction level with ctgrind, dudect, or dataflow analysis. Compiler optimizations can reintroduce branches — check assembly output.
7. **Proactive security requires fresh shares after every committee rotation.** Reusing threshold shares across epochs creates a time-accumulation attack surface — an adversary compromising one party per rotation eventually collects t-of-n shares. Use Herzberg's dynamic proactive secret sharing or FROST key resharing protocol.
8. **Maintain a cryptographic inventory with algorithm-to-usage mapping.** Without an inventory, you cannot assess the blast radius of a cryptanalytic breakthrough against any single algorithm, nor estimate PQC migration timelines. Track: algorithm, key size, protocol, deployment location, migration status.
9. **Favor formally verified implementations over hand-rolled crypto.** HACL*, EverCrypt, and libsodium have machine-checked proofs of memory safety, functional correctness, and cryptographic security. Even well-known libraries can have subtle implementation bugs that formal verification catches.
10. **FHE bootstrapping budgets must include a 30% safety margin.** Budget exhaustion causes silent decryption failure — ciphertexts decrypt to random noise with zero error indication. Track noise budget per circuit level and raise alerts before dropping below 20%. Always over-provision relative to theoretical estimates.

<!-- STANDARD: 3min -->
## Error Recovery

If a cryptographic implementation, verification, or deployment fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Implementation fails test vectors | Verify test vector source is authoritative. Check endianness, encoding, and parameter selection | Re-implement using a different verified library. Diff outputs byte-by-byte | Flag as potential library bug. File issue with maintainer with reproducible test case |
| Constant-time verification failure | Check for compiler optimizations that reintroduced branches. Use `volatile` or inline asm barriers | Rewrite the critical section using verified constant-time primitives | Accept the timing leak if below network jitter noise floor. Document residual risk |
| Dependency publishes a security advisory | Evaluate CVSS score and exploitability within 48 hours. If >= 7.0, initiate emergency patch cycle | Find an alternative library or implement a workaround | Document risk acceptance with a hard remediation deadline |
| Production deployment fails validation | Check the validation failure logs. Fix the specific validation error and re-run | Roll back to the last known-good version. Deploy incrementally | Escalate to security-engineer for expert review |

**Hard failure boundary:** If 3 independent approaches all fail, STOP. Log what was tried, capture error output, and report the blocking issue with full context.

<!-- DEEP: 10+min -->
## Error Decoder **(STANDARD)**

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
## Operating at Different Levels

Cryptographic engineering scales from library integration to novel protocol design based on organizational maturity and threat requirements.

| Level | Crypto Engineer Output Characteristics |
|---|---|
| **L1 — Library integrator** | Uses libsodium, OpenSSL, or Web Crypto API for standard operations (encrypt, sign, hash). Knows which algorithms to use for which scenarios. |
| **L2 — Protocol implementer** | Implements standard protocols from RFCs/NIST specs: TLS configuration, Noise framework handshakes, ECDH key exchange, JWT/JWE token crypto. |
| **L3 — Cryptographic architect** | Designs custom protocols with formal security models. Selects curves, proof systems, and parameters. Writes security proofs or delegates to specialists. |
| **L4 — Advanced cryptographer** | Deploys MPC, FHE, or ZKP in production. Designs threshold schemes (FROST, GG20). Manages PQC migration and crypto agility layers. |
| **L5 — Novel cryptographer** | Publishes new constructions, breaks existing ones, contributes to NIST/IRTF standards. Designs next-generation primitives and protocols. |

**Usage**: Say "at L2, implement TLS 1.3 with these parameters..." or calibrate by security requirements. Default: **L2** (protocol implementation).

### Scale Depth

#### Solo (0-10 users)
Use libsodium for all cryptographic operations. Standard algorithms only (AES-GCM, ECDH, Ed25519). Keys from environment-specific KMS (AWS KMS, GCP KMS). No custom protocol design. Regular dependency scanning for CVE monitoring.

#### Small Team (10-100 users)
Implement standard protocols from RFCs/NIST specs. Add HSM for signing keys. Run Wycheproof test vectors against all libraries. Constant-time verification for critical comparison operations. PQC migration plan drafted with algorithm inventory.

#### Medium Team (100-10K users)
Design custom protocols with formal security models. Deploy TEE infrastructure with full attestation chain validation. Threshold signing with proactive share refresh. FHE for privacy-preserving computation with bootstrapping budget monitoring. Formal verification with ProVerif/Tamarin. NIST SP 800-90B entropy validation for key ceremonies.

#### Enterprise (10K+ users)
MPC deployment with dishonest-majority protocols. Multi-cloud HSM federation with quorum-based access. Continuous side-channel analysis (timing, power, EM). Cryptographic agility layer with automated algorithm rotation. PQC hybrid deployment across entire infrastructure. Crypto incident response team with zero-day response SLA.

#### Transition Triggers
- Data classified as PII/PHI → HSM for encryption keys, AEAD required
- Multi-party computation needed → MPC protocol with formal security model
- Regulatory requirement (FIPS 140-3) → FIPS-validated modules, formal certification process
- PQC deadline announced → hybrid deployment begins, crypto inventory audit
- Cryptanalytic breakthrough on deployed algorithm → crypto agility layer activates, algorithm rotation within 30 days
- First key ceremony → NIST SP 800-90B entropy validation, multi-participant ceremony

## Production Readiness Checklist **(STANDARD)**

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

| Upstream Skill | What You Receive | When to Involve |
|-----------|-------|---------|
| **Upstream:** | `security-engineer` | Threat model, asset inventory, trust boundaries, security parameter requirements |
| **Upstream:** | `system-architect` | System boundaries, integration patterns, deployment topology, trust model |
| **Upstream:** | `backend-developer` | API contracts, data flow, key storage integration, application-level crypto integration |
| **Downstream** | `zkp-engineer` | Cryptographic primitives, proof system security, trusted setup parameters, circuit constraints |
| **Downstream** | `smart-contract-auditor` | On-chain crypto verification, signature scheme audit, verifier contract security |
| **Downstream** | `compliance-officer` | FIPS 140-3/Common Criteria certification requirements, audit evidence collection |

<!-- QUICK: 30s -->
## Deliberate Practice

| Level | Practice Routine | Frequency |
|---|---|---|
| **Novice** | Implement standard crypto operations from RFCs against test vectors. Compare your output to libsodium | Weekly |
| **Competent** | Break (intentionally) weakened crypto: reduced-round AES, small-prime RSA, short-nonce GCM. Use Cryptopals challenges | Monthly |
| **Expert** | Implement a novel protocol from a recent paper (e.g., a new MPC construction from CRYPTO 2024). Identify where the proof assumptions break in practice | Quarterly |
| **Master** | Find and responsibly disclose a vulnerability in a production cryptographic library or protocol. Contribute a fix upstream | Annually |

**The One Highest-Leverage Activity:** Run the Wycheproof test suite against every crypto library you use. Document which tests pass and which fail. The gap between what the library claims and what it actually handles is where production bugs live.

## State Log

This skill maintains a **decision ledger** to prevent context drift across sessions. Every major architectural choice, parameter decision, and trade-off must be recorded.

### How the State Log Works

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for prior decisions. Summarize the 3 most recent in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "cryptographic-engineer",
     "phase": "Phase 3: Protocol Design",
     "decision": "What was chosen (algorithm, key size, curve)",
     "rationale": "Why this choice over alternatives",
     "constraints": ["FIPS 140-3 required", "Must run on mobile"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": false
   }
   ```
3. **Before completing work:** Verify all major decisions are recorded. A "major decision" is anything that, if changed, would require key rotation or protocol renegotiation.
4. **On context recovery:** Read the last 5 entries before proposing changes.

### Anti-Drift Check

Before beginning a new phase:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Would my proposed change require key rotation?
- [ ] If I'm contradicting a prior decision, have I documented WHY?

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| NIST announces a new PQC standard or deprecates an existing algorithm | Audit crypto inventory for affected algorithms. Estimate migration timeline. Draft a PQC migration update within 2 weeks | PQC transitions take 3-5 years in large organizations |
| CVE published for a cryptographic library you depend on | Assess impact within 24 hours. If CVSS >= 7.0, initiate emergency patch cycle | Crypto CVEs often enable complete compromise; the exploitation window is shrinking |
| Academic paper demonstrates practical attack on a primitive you use | Initiate deprecation timeline within 1 week. The primitive's security margin is gone | Attack improvements are monotonic — today's academic attack is tomorrow's script-kiddie tool |
| Key ceremony scheduled for production deployment | Pre-ceremony checklist: entropy source health verified, HSM firmware updated, participants trained, backup procedures documented | Failed ceremonies erode organizational trust and can delay deployment by months |
| Cryptographic bill or regulation proposed | Legal risk assessment within 2 weeks. Model impact on product architecture. Engage legal-advisor and regulatory-specialist | Regulatory changes can make current architectures non-compliant overnight |

## Anti-Patterns

### Anti-Pattern: Manual Nonce Generation
**What it looks like:** Generating nonces with `Math.random()`, `/dev/urandom` alone, or sequential counters without replay protection for stream ciphers and AEAD modes.
**Why it fails:** Nonce reuse in stream ciphers and AEAD (ChaCha20-Poly1305, AES-GCM) completely breaks confidentiality — XOR of two ciphertexts encrypted with the same key+nonce reveals XOR of plaintexts. Sequential counters without authentication allow ciphertext replay. AES-GCM nonce reuse catastrophically compromises both confidentiality and integrity.
**Do this instead:** Use your crypto library's built-in nonce generation (libsodium's `randombytes_buf`). For AES-GCM, use a 96-bit random nonce (collision probability at 2^32 messages is ~2^-32). For counters, include a per-message random prefix. Never use fixed or sequential nonces without authenticated replay protection.

### Anti-Pattern: PQC Downgrade Fallback
**What it looks like:** A hybrid key exchange that falls back to classical-only (X25519) when the PQC component (ML-KEM) fails due to timeout, malformed response, or CPU overload.
**Why it fails:** An active network adversary can force the PQC failure condition (delay packets, inject corruption) to downgrade the connection to classical-only. The adversary then applies classical or quantum attacks to the unprotected classical key exchange. The hybrid security property is completely lost.
**Do this instead:** Fail closed — reject the connection if either component fails. Use atomic key agreement where both ML-KEM and classical shares must complete before deriving the session key. Log all PQC failures for security monitoring to detect active downgrade attacks. Follow the Signal PQXDH pattern.

### Anti-Pattern: Trusting Test Vectors Alone
**What it looks like:** Validating a cryptographic implementation against NIST CAVP or Wycheproof test vectors and assuming correctness based on pass rate alone.
**Why it fails:** Test vectors cover known-answer scenarios but miss edge cases: zero-length inputs, boundary field elements, and adversarial parameter selection. Wycheproof explicitly includes near-miss test vectors that pass for incorrect implementations — these are the most revealing failures. Production failures often come from edge cases test vectors don't cover.
**Do this instead:** Run the full Wycheproof test suite and investigate every "acceptable" (non-passing) result. Add property-based tests: `decrypt(encrypt(m)) == m` for all inputs. Add fuzz testing with random bit flips. For constant-time code, verify with dudect or ctgrind on every build. Run differential testing against a reference implementation.

### Anti-Pattern: Insufficient Entropy for Key Generation
**What it looks like:** Using `/dev/urandom` alone on VMs, containers, or embedded devices for key ceremony entropy without validating entropy health.
**Why it fails:** VMs and containers can have low-entropy pools at boot due to identical initial snapshots. Embedded devices may have deterministic PRNG state across reboots. `/dev/urandom` on Linux never blocks, returning data even with insufficient entropy. Keys generated with low entropy are predictable and recoverable.
**Do this instead:** Use multiple independent entropy sources with statistical validation per NIST SP 800-90B. For key ceremonies, combine HSM internal TRNG, user-provided entropy (diceware, coin flips), and OS entropy. Verify entropy health before every key generation. On embedded devices, seed from factory-provisioned unique key plus environmental noise.

### Anti-Pattern: CBC Without Authentication
**What it looks like:** Using AES-CBC for encryption without an authenticated MAC over the ciphertext and IV, or revealing padding errors to the caller.
**Why it fails:** CBC without authentication is malleable — attackers can flip bits in ciphertext blocks to produce predictable plaintext changes. Padding oracle attacks can fully decrypt ciphertexts one byte at a time when the server reveals padding success/failure through timing or error messages.
**Do this instead:** Use AEAD modes (AES-GCM, ChaCha20-Poly1305) that bundle encryption and authentication. If CBC is unavoidable for legacy compatibility, use Encrypt-then-MAC with HMAC-SHA256 over IV + ciphertext. Use constant-time padding verification that never reveals padding validity to the caller.

### Anti-Pattern: Ignoring Side Channels in TEE
**What it looks like:** Assuming SGX/TDX/SEV memory encryption protects against all side-channel attacks, so no further hardening is applied to enclave code.
**Why it fails:** TEEs protect against memory inspection but not microarchitectural side channels: cache timing, branch prediction, speculative execution. Vulnerabilities like Spectre, Meltdown, and LVI allow an untrusted OS to extract secrets from enclaves through cache timing and transient execution attacks.
**Do this instead:** Apply constant-time programming within enclaves. Use data-oblivious algorithms that branch only on public data. Avoid secret-dependent memory access patterns. Validate with TEE-specific side-channel analysis tools. Assume the untrusted OS can observe cache state at instruction granularity.

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
## Verification Guardrails

- [ ] All cryptographic operations use AEAD or stronger (no CBC, no ECB, no unauthenticated modes)
- [ ] Keys managed via KMS/HSM with audit trail; no keys in source code, config files, or environment variables
- [ ] Constant-time verification: critical comparison operations pass `dudect` or equivalent TVLA
- [ ] Test vectors: NIST CAVP or Wycheproof test vectors pass for all implemented algorithms
- [ ] PQC migration plan documented with algorithm inventory, hybrid deployment strategy, and hard migration date
- [ ] Side-channel assessment completed: timing, cache-timing, and (for TEE) electromagnetic analysis
- [ ] Key ceremony documentation: participant attestations, entropy validation, backup share verification
- [ ] Every cryptographic decision recorded in the State Log with rationale and alternatives considered


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
