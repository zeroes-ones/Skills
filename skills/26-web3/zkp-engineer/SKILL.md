---
name: zkp-engineer
description: "Use when designing zero-knowledge proof circuits, selecting ZKP proof systems (Groth16/STARKs/Halo2/Plonky3), writing Circom 2/Noir/Halo2 circuit code, auditing circuits for under-constraint vulnerabilities, implementing recursive proving with Nova/SuperNova folding schemes, or architecting ZKP-based privacy solutions (private transactions, zk-rollups, zk-identity, zkML, zk-email). Handles circuit design languages (Circom 2 R1CS constraints, Noir PLONK backend, Halo2 lookup tables and custom gates, ZoKrates), proof system selection (Groth16 trusted setup with Powers of Tau, STARKs transparent FRI-based, Halo2 recursive without trusted setup, Plonky3 small-field plonkish arithmetization), constraint security hardening (under-constraint detection, missing input validation prevention, range check enforcement, Boolean constraint verification, signal privacy in witness computation), recursive proving (Nova folding for IVC, SuperNova for NIVC, Protostar for non-uniform computation), and ZKP integration patterns (Solidity verifier deployment, on-chain verification gas costs, off-chain proving). Do NOT use for general cryptography (use cryptographic-engineer), smart contract development (use smart-contract-auditor), blockchain architecture (use system-architect), or ML model training (use ml-ai-engineer)."
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: specialized
status: stable
version: "1.0.0"
updated: 2026-07-24
tags: [zkp, zero-knowledge, circom, noir, halo2, groth16, starks, plonky3, recursive-proving]
token_budget: 3500
dependencies:
  tools: [circom, snarkjs, noir, halo2, plonky3, nova-scotia]
  packages: []
  permissions: [evm-node-access, etherscan-api]
output:
  type: "circuit-code, verifier-contract, constraint-audit-report"
  path_hint: "zkp-engineer/"
chain:
  consumes_from:
    - cryptographic-engineer
    - system-architect
    - backend-developer
  feeds_into:
    - smart-contract-auditor
    - security-engineer
    - devops-engineer
  alternatives:
    - cryptographic-engineer
    - ml-ai-engineer
---
> **Portability target:** Spec-level (runs on Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI). No vendor-specific frontmatter fields.

<!-- QUICK: 30s -->
## Route the Request

```
ZKP requirement identified
├─ Need to prove X without revealing Y?
│  ├─ Verify private computation on public blockchain → zk-rollup or zk-application
│  ├─ Prove identity/credential without revealing data → zk-identity, zk-email
│  ├─ Prove ML inference on private data → zkML
│  └─ Prove transaction validity privately → private transaction
│
├─ Which proof system?
│  ├─ Single proof, needs on-chain verification at low gas cost
│  │  └─ Groth16 (smallest verification cost, requires trusted setup)
│  ├─ No trusted setup, transparent, scalable verification
│  │  └─ STARKs (FRI-based, large proof size, no trusted setup)
│  ├─ Recursive proofs needed (prove many statements in one)
│  │  └─ Halo2 (recursive without trusted setup) or Nova (folding)
│  └─ Ultra-fast proving, custom arithmetization
│     └─ Plonky3 (small-field plonkish, 100x faster than Groth16)
│
├─ Circuit language?
│  ├─ Low-level constraint control, R1CS-focused
│  │  └─ Circom 2 (most mature, largest ecosystem)
│  ├─ High-level Rust-like language, PLONK backend
│  │  └─ Noir (Barretenberg backend, growing ecosystem)
│  ├─ Custom gates and lookup tables, maximum flexibility
│  │  └─ Halo2 (Rust DSL, complex but powerful)
│  └─ Python-like DSL for prototyping
│     └─ ZoKrates (good for learning, limited production use)
│
├─ Security posture?
│  ├─ Under-constraint analysis needed → Constraint Security (Decision Tree 3)
│  └─ Production hardening needed → Security Hardening (ref 12-security-hardening.md)
│
└─ Deployment target?
   ├─ EVM chain → Solidity verifier (on-chain)
   └─ Off-chain verification → Native verifier (Rust/Go/TypeScript)
```

<!-- STANDARD: 3min -->
## Ground Rules — Read Before Anything Else

- **Flag your knowledge cutoff.** Cryptographic standards, ZK proof systems, and smart contract platforms evolve rapidly. If your training data predates the latest FIPS/NIST publication, protocol upgrade, or EVM fork, state your cutoff date and recommend verifying against current documentation.
- **Never guess security parameters.** If you're unsure about the correct key size, curve selection, proof system parameter, or gas optimization, do NOT provide a "reasonable default." Say: "Security parameters must be verified against current best practices. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Mark statements as: [VERIFIED] — from official docs/standards, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure.

1. **Never deploy a circuit without under-constraint analysis.** Under-constrained circuits leak witness information and are the #1 source of ZKP exploits ($10M+ historically). Always run automated constraint checking.

2. **Never reuse trusted setup parameters across circuits.** Each circuit needs its own Phase 2 ceremony. Reusing parameters allows cross-circuit proof forgery if the toxic waste is compromised.

3. **Never skip range checks on public inputs.** Every public input must be proven within valid range (bit decomposition or LessThan). Missing range checks allow overflow attacks that bypass protocol invariants.

4. **Never use `<--` without `===` for output signals.** If an output signal is assigned with `<--`, it MUST be followed by a corresponding `===` constraint. An output with only `<--` is unconstrained and can be arbitrarily forged.

5. **Never assume Circom `<==` constrains intermediate signals.** `c <== a + b` constrains `c = a + b` but does NOT constrain whether `a` or `b` themselves are properly formed. Every signal needs its own constraint verification.

6. **Never use `mod` or `%` inside Circom constraint bodies.** Field division is well-defined but modulo behaves differently in finite fields. Use Num2Bits and reassemble for integer-like modulo operations.

7. **Never skip the Powers of Tau beacon contribution.** The final Phase 1 step must use a public random beacon (block hash) to prevent the last participant from knowing the toxic waste.

8. **Never deploy a Solidity verifier without gas benchmarking.** Deploy to testnet first and measure actual gas costs with realistic inputs. Theoretical estimates often underestimate by 2-3x.

9. **Never reuse nullifiers across applications without domain separation.** Nullifier computation must include a unique application scope. Without domain separation, a nullifier from App A can be replayed in App B, breaking privacy.

10. **Admit uncertainty -- never fabricate circuit constraints.** If uncertain about a constraint pattern, say so. A hallucinated constraint can create an exploitable under-constraint that formal verification tools would miss.

<!-- QUICK: 30s -->
## The Expert's Mindset

The ZKP engineer's job is not to write circuits — it's to **encode computational integrity into minimal constraints, ensure no witness can forge a proof, and deploy verifiers that remain secure under adversarial inputs**. The output is not a circuit; it's a trustless verification system.

### Mental Models

| Model | Description |
|---|---|
| **Every unconstrained signal is a backdoor** | A single missing constraint in a circuit means an attacker can generate a valid proof for an invalid statement. Constraint completeness is security, not correctness. |
| **The prover is always adversarial** | Never assume the prover will follow the intended witness generation path. Design circuits that reject any witness that doesn't satisfy all constraints, even if "no honest user would generate that input." |
| **Proof system selection is a multi-axis optimization** | Groth16 gives smallest proofs but requires a trusted setup. STARKs are transparent but produce larger proofs. There is no universal best — only best for specific requirements. |
| **Recursive proving is a force multiplier** | One proof verifying another proof enables compression, aggregation, and composability. Master recursion before attempting production ZKP systems at scale. |

### What Masters Know

- **Under-constrained circuits are the #1 vulnerability class.** More ZKP systems have been broken by missing constraints than by cryptographic breaks in the proof system itself. Every audit finds constraint bugs — the question is whether you find them before deployment.
- **Circuit optimization is a security discipline, not a performance one.** Reducing constraints is good; removing safety constraints to reduce constraints is catastrophic. Every removed constraint must be justified by a proof that it's redundant.
- **Trusted setups are organizational challenges, not cryptographic ones.** The math of a Powers of Tau ceremony is well-understood. Getting 100+ independent participants to verify their contributions honestly is a logistics and reputation problem.


## When to Use

- Designing ZKP circuits for private transactions, zk-rollups, or confidential smart contracts
- Selecting a proof system: Groth16 for small on-chain proofs, STARKs for transparency, Halo2 for recursion, Plonky3 for speed
- Writing Circom 2 circuits with R1CS constraints, or Noir programs with PLONK backend
- Auditing existing circuits for under-constraint vulnerabilities, missing input validation, or range check gaps
- Implementing recursive proving with Nova/SuperNova folding schemes for Incrementally Verifiable Computation (IVC)
- Deploying Solidity verifiers on EVM chains with gas optimization
- Migrating between proof systems (e.g., Groth16 => Plonky3 for performance)
- Architecting ZKP-based privacy solutions: private identity, zk-email, zkKYC, zkML inference verification
- Building zk-rollup infrastructure (validium, zkEVM, custom application-specific rollups)

<!-- STANDARD: 3min -->
## Decision Trees

### Tree 1: Proof System Selection

```
ZKP proof system needed
├─ On-chain verification (EVM)?
│  ├─ Single proof, minimum gas cost
│  │  └─ Groth16 (trusted setup needed, ~300K gas)
│  ├─ Multiple proofs aggregated
│  │  ├─ Groth16 batch verification (optimized by some verifiers)
│  │  └─ Halo2 recursive verification (~500K gas)
│  └─ No trusted setup, auditability required
│     └─ STARKs on-chain via StarkNet or RISC Zero (~1M gas)
├─ Off-chain verification?
│  ├─ Maximum speed
│  │  └─ Plonky3 (100x faster than Groth16, small-field, plonkish)
│  ├─ Recursive proofs (prove many computations)
│  │  ├─ Halo2 (recursive without trusted setup, custom gates)
│  │  └─ Nova/SuperNova (folding, fastest for IVC)
│  └─ No recursion, simple verification
│     └─ Any system; choose by proof size and verification time
├─ Trusted setup acceptable?
│  ├─ YES → Groth16 (smallest proofs, fastest verification)
│  └─ NO → STARKs, Halo2, Plonky3 (all transparent)
└─ Proof size constraint?
   ├─ < 256 bytes → Groth16 only
   ├─ < 10 KB → Halo2/Plonky3
   └─ Any size → STARKs (tunable via FRI parameters)
```

### Tree 2: Circuit Language Selection

```
Circuit implementation needed
├─ Prior experience:
│  ├─ JavaScript/TypeScript background → Circom 2 (JS-like syntax)
│  ├─ Rust background → Noir (Rust-like, Barretenberg backend)
│  └─ No preference → Start with Circom 2 (largest ecosystem, most examples)
├─ Constraint type:
│  ├─ R1CS (Rank-1 Constraint System)
│  │  └─ Circom 2 (native R1CS, finest-grained control)
│  ├─ PLONKish (custom gates + lookup tables)
│  │  ├─ Halo2 (Rust DSL, maximum flexibility)
│  │  └─ Noir (automatic PLONK -> UltraPLONK)
│  └─ Small-field arithmetization
│     └─ Plonky3 (PLONKish over Goldilocks field)
├─ Ecosystem maturity:
│  ├─ Largest → Circom 2 (most libraries, tools, audits)
│  ├─ Growing fast → Noir (Aztec ecosystem, Barretenberg)
│  └─ Academic/niche → Halo2 (Electric Coin Co.)
└─ Learning curve:
   ├─ Gentle → Noir (high-level, automatic constraint generation)
   ├─ Moderate → Circom 2 (signal-based, needs constraint thinking)
   └─ Steep → Halo2 (custom gates, lookup tables, chip architecture)
```

### Tree 3: Constraint Security (Under-Constraint Detection)

```
Circuit analysis for under-constraints
├─ Output signal assignment:
│  ├─ signal output out;
│  │  out <== expr; -- OK, fully constrained
│  │  out <-- expr; -- DANGER: needs === constraint after
│  │  └─ If <-- without === → CRITICAL: output is unconstrained
│  └─ Missing === after <-- → Must add: expr === out;
├─ Boolean constraints:
│  ├─ bit * (bit - 1) === 0 -- OK, properly constrained
│  └─ bit === 0 or bit === 1 -- DANGER: === is not enough, use the quadratic constraint
├─ Range checks on public inputs:
│  ├─ Bits2Num or Num2Bits with LessThan -- OK
│  └─ No range check on public input -- CRITICAL: overflow attack possible
├─ Intermediate signals:
│  ├─ Every signal constrained by at least one quadratic equation -- OK
│  └─ Some signals in expression but never in === -- DANGER: free variable
└─ Template arguments:
   ├─ Verified inside template -- OK
   └─ Used without constraint -- DANGER: attacker picks argument value
```

### Tree 4: Recursive Proving Strategy

```
Need to prove N sequential computations
├─ Computations are the same instruction type?
│  ├─ YES → Nova folding scheme (fastest IVC)
│  │  └─ Single instruction, repeated N times
│  └─ NO → SuperNova (NIVC, multiple instruction sets)
│     └─ Cycle between different instruction types
├─ Need parallel proving?
│  └─ Protostar (non-uniform IVC with parallelism)
├─ Proof composition (not folding):
│  ├─ Halo2 recursive verification (inner circuit proven, outer circuit verifies inner proof)
│  └─ PLONK recursion via accumulation scheme
└─ Performance target:
   ├─ Minimum proving time → Nova (folding is fastest)
   ├─ Minimum verification time → Halo2 (accumulation then single verification)
   └─ Balance → Protostar
```

<!-- STANDARD: 3min -->
## Core Workflow

### Phase 1: Proof System & Language Selection (est. 1-2 hours)
1. Identify the proving goal: private computation, rollup, identity, zkML
2. Assess constraints: on-chain verification, recursion needs, trusted setup tolerance
3. Select proof system via Decision Tree 1
4. Select circuit language via Decision Tree 2
**Completion criteria:** Proof system and language selected with documented rationale. Alternatives considered and rejected with trade-off analysis.

### Phase 2: Circuit Design & Implementation (est. 4-20 hours)
1. Implement circuit in selected language (Circom 2, Noir, Halo2, ZoKrates)
2. Define all public inputs, private inputs, and output signals
3. Write constraint equations for every signal relationship
4. Implement range checks for all public inputs (Num2Bits, LessThan)
5. Apply Boolean constraints to all bit signals: `bit * (bit - 1) === 0`
6. Verify intermediate signals are constrained by at least one quadratic equation
**Completion criteria:** Circuit compiles without errors. All signals have corresponding constraints. Range checks and Boolean constraints applied. `circom --r1cs` shows expected constraint count.

### Phase 3: Constraint Auditing (est. 4-8 hours)
1. Run automated under-constraint detection: `circom --inspect` or custom scripts
2. Verify every `<--` has a following `===` constraint
3. Check all public inputs for range constraints
4. Verify Boolean constraint pattern: `signal * (signal - 1) === 0` for all bits
5. Fuzz test: generate random valid inputs and verify proof verification passes
6. Negative test: generate invalid witnesses and verify proof verification fails
**Completion criteria:** Automated audit passes. All output signals are constrained. All public inputs have range checks. No free variables in the constraint system.

### Phase 4: Recursive Composition & Optimization (est. 4-12 hours)
1. If recursive proving needed: select Nova (IVC), SuperNova (NIVC), or Halo2
2. Implement folding scheme circuits for iterative computation
3. Write recursive verification circuit
4. Profile proving time and proof size
5. Optimize: reduce constraint count, leverage lookup tables, tune FRI parameters
**Completion criteria:** Recursive proving pipeline functional. Proving time and proof size meet performance targets. Folding verifier circuit constraints within budget.

### Phase 5: Verifier Deployment & Integration (est. 2-8 hours)
1. Generate Solidity verifier contract (snarkjs for Groth16, custom for others)
2. Deploy to testnet and measure actual gas costs
3. Optimize verification gas if needed (batch verification, calldata optimization)
4. Integrate verifier with application: frontend, wallet, or rollup node
5. End-to-end test: generate proof off-chain, verify on-chain
**Completion criteria:** Verifier deployed on target chain. Gas costs measured and documented. End-to-end proof generation and verification works end-to-end.

### Phase 6: Security Hardening & Production Readiness (est. 4-8 hours)
1. Run full under-constraint audit as final check
2. Verify trusted setup ceremony documentation (if Groth16)
3. Document security assumptions: soundness model, trusted setup assumptions
4. Add monitoring for proof verification failures
5. Write incident response plan for proof system vulnerability disclosure
**Completion criteria:** Security audit report. Production readiness checklist completed. Incident response plan documented.

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


| # | Domain | Best Practice |
|---|--------|---------------|
| 1 | Circuit Safety | Every output signal must have both `<--` and `===`. Missing the constraint allows arbitrary forgery of the output value. This is the #1 cause of ZKP circuit exploits. |
| 2 | Input Validation | All public inputs must have range checks (bit decomposition or LessThan). Missing range checks allow overflow attacks that bypass protocol invariants. |
| 3 | Boolean Enforcement | Every bit signal must have `signal * (signal - 1) === 0`. Without this, a "bit" can hold any field element as long as the weighted sum constraint holds. |
| 4 | Trusted Setup | Production deployments require Phase 2 ceremonies with independent, verifiable contributions. Never use test ceremony parameters in production. |
| 5 | Gas Optimization | Always deploy Solidity verifiers to testnet and measure actual gas before mainnet. Theoretical estimates underestimate by 2-3x consistently. |
| 6 | Domain Separation | Nullifiers and commitments must include a unique application identifier. Without domain separation, cross-application replay attacks break privacy. |
| 7 | Constraint Verification | Use `circom --r1cs` to verify constraint count matches expectations. Oversized circuits waste proving resources; undersized circuits indicate missing constraints. |
| 8 | Recursive Proving | Nova folding is fastest for IVC with uniform computation. SuperNova supports non-uniform IVC with multiple instruction sets. Protostar supports maximal parallelism. |
| 9 | Benchmarking | Measure proving time, verification time, and proof size for realistic inputs before production. Performance varies significantly with circuit complexity and field size. |
| 10 | Upgrade Safety | Proof system migration requires redeploying verifiers. Plan for verifier contract upgradeability from day one. |
| 11 | Testing | Fuzz test with valid random inputs AND invalid witness data. Proof must verify for valid and fail for invalid. Negative test coverage is as important as positive. |
| 12 | Documentation | Document all security assumptions: soundness, zero-knowledge, trusted setup, FRI parameters. A proof system is only as secure as its weakest documented assumption. |

<!-- DEEP: 10+min -->
## Error Decoder

### War Story 1: Under-Constrained Output Signal ($10M+)

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| A ZKP-based privacy protocol is drained because an attacker generates valid proofs for arbitrary output values. The protocol accepts forged proofs that claim incorrect but seemingly valid statements. | A critical circuit used `<--` to assign an output signal but omitted the corresponding `===` constraint. The output signal was assigned via template output with `out <-- expr;` but no `expr === out;` followed. This left the output unconstrained -- the prover could assign ANY value to the output while still producing a valid proof. | Add the constraint `expr === out;` immediately after every `<--` assignment. Implement automated linting that detects `<--` without subsequent `===`. Add a pre-deployment check: grep for `<--` and verify each has a matching `===`. Use Circom 2.1's `output` keyword constraint verification. | The `<--` without `===` bug is the ZKP equivalent of a SQL injection -- simple, well-known, and catastrophically exploitable. This single pattern has caused multiple multi-million-dollar exploits. Every circuit must be audited for this pattern, and every CI pipeline must check for it automatically. |

### War Story 2: Trusted Setup Ceremony Compromise

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| An attacker who participated in the last position of a Powers of Tau ceremony is able to forge proofs for any circuit using that ceremony's output. The protocol suffers a complete loss of soundness. | The Powers of Tau ceremony's final contribution did not use a public random beacon. The last participant could compute the toxic waste (tau) because they knew their own contribution and could subtract it from the final output, leaving only the previous participants' contributions aggregated. With knowledge of tau, they can create valid proofs for false statements. | Always add a public random beacon as the final ceremony contribution. Use a recent Ethereum block hash, Bitcoin block hash, or NIST randomness beacon. The beacon contribution ensures that no participant can know the final toxic waste. Implement participant verification with on-chain attestations for transparency. | The last participant in a non-beaconed ceremony has full knowledge of the trapdoor. A trusted setup ceremony without a beacon contribution is not trusted at all -- it's a trapdoor ceremony. The beacon step is not optional; it transforms "trusted" from "trust the participants" to "trust the randomness of the beacon." |

### War Story 3: Missing Boolean Constraint in Vote/Commitment Circuit

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| A zk-application for anonymous voting allows an attacker to submit votes with weight > 1. The proof verifies successfully, but the vote tally is inflated. The attack goes undetected until a recount reveals the discrepancy. | The circuit used bit decomposition to convert a voting weight into bits but omitted the Boolean constraint `bit * (bit - 1) === 0` on each bit. Without this constraint, a "bit" signal could hold any field element. By setting a "bit" to a large field element, the attacker could make the weighted sum produce an arbitrary voting weight while still being representable in the bit structure. | Add `signal * (signal - 1) === 0` for every bit signal after decomposition. Use Circom's `Bits2Num` and `Num2Bits` templates which include Boolean checks. Validate constraints automatically with `circom --inspect`. | A bit that is not constrained to be binary is not a bit -- it's an unbounded field element. The Boolean constraint `x * (x-1) === 0` is the mathematical definition of binary: it forces x to be either 0 or 1 in a finite field. Skipping it is equivalent to allowing a vote of 1000 when the protocol intended a binary choice. |

### War Story 4: Proving System Implementation Bug (Verifier Accepts Invalid Proofs)

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| A production zk-rollup accepts a batch of invalid transactions. The proof verification passes, but the state transition commits to an invalid Merkle root. The rollup loses $5M+ in user funds before the issue is detected. | The Groth16 verifier implementation had a subtle bug in the pairing check: one of the eight pairing equations was omitted during a code refactoring. Without this check, the verifier accepted proofs that had valid structure but invalid computation. The bug was not caught because the gas-optimized verifier was hand-written rather than generated by snarkjs. | Always use snarkjs-generated verifiers for production. Never hand-optimize pairing checks. Add a verification test that checks: (1) valid proofs pass, (2) proofs with modified public inputs fail, (3) proofs with swapped proof elements fail, (4) proofs with random proof elements fail. Run the test suite after EVERY verifier modification. | The pairing equation is the heart of Groth16 verification. Removing even one of the eight checks breaks soundness completely. The complexity of elliptic curve pairings makes manual verification infeasible -- always use the code generator. The 2-3x gas savings from manual optimization is never worth the loss-of-soundness risk. |

### War Story 5: FRI Proof-of-Work Collapse Under Large Query Gap

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| A STARK-based zk-rollup's proof system suffers a soundness collapse. The verifier accepts a proof of a false computation. Analysis reveals that the FRI protocol's query parameters allowed an adversary to construct a valid-looking low-degree test despite the polynomial not being low-degree. | The FRI protocol parameters were chosen for fast proving time rather than soundness. The number of queries was too low relative to the security target, and the grinding factor for the Merkle tree oracle was underestimated. An adversary with moderate computational resources could find a proof that passed the query check despite the polynomial having degree higher than claimed. | Set FRI parameters using the provably sound formula: number of queries >= log2(security_level) + log2(blowup_factor). Use the "Grinding" factor to prevent adversarial Merkle tree manipulation. Never tune FRI parameters for performance without recalculating the concrete security level. Use established parameter sets from ethSTARK or RISC Zero. | FRI security is tunable but fragile: the interactive oracle proof model has different soundness characteristics than the standard model. Parameters that appear "safe" due to large fields can hide soundness gaps. Always use verified parameter sets from existing deployments rather than custom calculations. Soundness is monotonic with query count -- when in doubt, query more. |

### War Story 6: Solidity Verifier Out-of-Gas on Mainnet

| Symptom | Root Cause | Fix | Lesson |
|---------|-------------|-----|--------|
| A zk-rollup's Solidity verifier runs out of gas during mainnet verification of a complex proof batch. The entire rollup halts because no new batches can be verified. The protocol loses 6 hours of liveness and $200K+ in delayed finality. | The verifier gas estimate was based on testnet measurements with simple proofs. The production proof had 3x the constraint count, which caused the pairing computation to exceed the block gas limit. The gas-optimized verifier had inlined all pairings, making it impossible to split verification across multiple transactions. | Always benchmark verifier gas with production-representative proofs before mainnet deployment. Add a maximum constraint count per proof in the verifier that reverts with a clear message if the proof is too large. Implement batch splitting for large proofs. Use a fallback mechanism that allows increasing gas limit through governance if needed. | Theoretical gas estimates for pairing-based verification are unreliable. The actual gas cost depends on the number of pairings, which scales with constraint count and proof structure. The cost of a production failure ($200K+ in delays, reputation damage) vastly exceeds the cost of running a testnet benchmark ($50 in testnet gas). Always benchmark with production-sized proofs. |

<!-- STANDARD: 3min -->
## Operating at Different Levels

| Level | ZKP Engineer Output Characteristics |
|---|---|
| **L1 — Circuit implementer** | Writes Circom/Noir circuits from specifications. Implements hash functions, Merkle trees, signature verification in constraints. Tests with snarkjs/halo2 test vectors. |
| **L2 — Proof system integrator** | Selects proof systems (Groth16, STARKs, Plonky3) based on requirements. Writes verifier contracts. Integrates proving infrastructure with applications. |
| **L3 — ZKP architect** | Designs custom circuits with constraint optimization. Implements recursive proving. Audits circuits for under-constraint and soundness bugs. |
| **L4 — Proof system contributor** | Extends existing proof systems with new features (custom gates, lookup tables). Optimizes prover performance. Contributes to circom/halo2/Noir toolchains. |
| **L5 — Novel proof system designer** | Designs new arithmetizations, folding schemes, or proof systems. Publishes research. Sets new efficiency records for prover time, proof size, or verification cost. |

**Usage**: Say "at L2, help me integrate Groth16 with this circuit..." or calibrate by experience. Default: **L2** (proof system integration).
## Production Readiness Checklist

| # | Item | Ref |
|---|------|-----|
| CR1 | Under-constraint analysis passed: all `<--` have corresponding `===` constraints | [V1] |
| CR2 | All output signals are constrained by at least one quadratic equation | [V2] |
| CR3 | Boolean constraint `signal * (signal - 1) === 0` applied to every bit signal | [V3] |
| CR4 | Range checks (Num2Bits, LessThan, or custom) applied to all public inputs | [V4] |
| CR5 | No free variables in the constraint system: every signal appears in at least one constraint | [V5] |
| CR6 | `circom --r1cs` constraint count matches expectations (verified before and after changes) | [V6] |
| CR7 | Trusted setup ceremony completed with public random beacon final contribution | [V7] |
| CR8 | Solidity verifier deployed to testnet with gas benchmarked against production-representative proofs | [V8] |
| CR9 | Verifier passes all test vectors: valid proofs verify, invalid proofs rejected | [V9] |
| CR10 | Fuzz test passes: 10K+ random valid proofs generated and verified; 10K+ invalid witnesses rejected | [V10] |
| CR11 | Nullifier domain separation verified: unique application scope in nullifier computation | [V11] |
| CR12 | Incident response plan documented for proof system vulnerability disclosure | [V12] |
| CR13 | Prover performance benchmarked: proving time, memory usage, proof size for max-size circuit | [V13] |
| CR14 | Upgrade path for verifier contract: proxy pattern or governance-controlled address update | [V14] |
| CR15 | Trusted setup ceremony documentation: participant attestations, contribution verification, beacon source | [V15] |
| CR16 | External audit performed by non-team ZKP engineer (mandatory for production deployments) | [V16] |

<!-- STANDARD: 3min -->
## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|-----------|-------|---------|
| **Upstream:** | `cryptographic-engineer` | Cryptographic primitives (hash functions, signature schemes, field arithmetic), protocol security parameters, key management for proving keys |
| **Upstream:** | `system-architect` | System boundaries, trust model, integration patterns, rollup architecture, proving infrastructure design |
| **Upstream:** | `backend-developer` | API contracts for proof generation, witness data preparation, off-chain proving pipeline |
| **Downstream** | `smart-contract-auditor` | On-chain verifier contract audit, proving key integrity verification, upgrade path security |
| **Downstream** | `security-engineer` | Threat modeling for ZKP infrastructure, prover network security, ceremony security |
| **Downstream** | `devops-engineer` | Prover deployment automation, verifier contract deployment, monitoring for proof failures |

<!-- QUICK: 30s -->
## Deliberate Practice

| Level | Practice Routine | Frequency |
|---|---|---|
| **Novice** | Implement standard ZKP examples: Sudoku solver, Merkle tree membership, simple range proof in Circom/Noir | Weekly |
| **Competent** | Audit circuits from open-source ZKP projects (Tornado Cash, Semaphore, zkEVM). Find intentional bugs placed by trainers | Monthly |
| **Expert** | Implement a novel ZKP application from a recent paper (e.g., zk-email from CCS 2023). Deploy on testnet with verifier contract | Quarterly |
| **Master** | Find and disclose a constraint vulnerability in a production ZKP system. Contribute a fix or detection tool upstream | Annually |

**The One Highest-Leverage Activity:** Write a circuit that proves something, then write the exploit that generates a valid proof for a false statement by exploiting a constraint gap you intentionally left. The process of exploiting your own circuits teaches constraint thinking faster than any tutorial.

## State Log

This skill maintains a **decision ledger** to prevent context drift across ZKP engineering sessions.

### How the State Log Works

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for prior decisions. Summarize the 3 most recent in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "zkp-engineer",
     "phase": "Phase 2: Circuit Design",
     "decision": "Proof system, circuit language, constraint strategy",
     "rationale": "Why this combination over alternatives",
     "constraints": ["Must verify in <500K gas", "Must support 1M+ constraints"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify all proof system, circuit, and parameter decisions are recorded.
4. **On context recovery:** Read the last 5 entries before proposing changes.

### Anti-Drift Check

Before beginning a new phase:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with prior constraints?
- [ ] If I'm contradicting a prior decision, have I documented WHY?

## Proactive Triggers

| Trigger | Action | Why |
|---------|--------|-----|
| New proof system paper with significant efficiency improvement (>10x prover time reduction) | Evaluate within 2 weeks: benchmark against current proof system on representative circuits | ZKP performance is improving rapidly. A 10x improvement can change system architecture |
| Under-constraint vulnerability disclosed in a similar ZKP application | Immediately audit your circuits for the same pattern. Run the exploit PoC against your testnet deployment | ZKP vulnerabilities are often pattern-based — the same class of constraint gap appears across projects |
| Trusted setup ceremony scheduled | Pre-ceremony: verify ceremony toolchain, participant list, entropy source requirements, and backup procedures | A single compromised contribution can compromise the entire proof system |
| Verifier contract deployment on mainnet | Pre-deployment: verify bytecode matches audited source, set circuit breaker parameters, test upgrade path | Verifier bugs are irreversible without upgrade capability |
| Proving infrastructure at capacity (>80% utilization) | Scale horizontally immediately: add prover nodes, optimize circuit constraints, or batch proofs | Proof generation backlogs directly impact user experience |

## What Good Looks Like

An excellent ZKP engineering delivery produces:

- **Circuit code** that compiles cleanly, passes all automated constraint audits, and has documented constraint counts
- **Constraint audit report** showing every signal is properly constrained, no free variables exist, and all public inputs have range checks
- **Verifier contract** (Solidity or native) that is benchmarked on testnet, passes valid/invalid proof test vectors, and has an upgrade path
- **Proof system selection** documented with rationale: security assumptions, performance targets, trusted setup requirements
- **Recursive proving pipeline** (if applicable) with measured proving time, verification time, and proof size
- **Trusted setup ceremony documentation** with participant attestations and beacon source verification (for Groth16)
- **Security hardening report** documenting under-constraint analysis, fuzz test results, and incident response plan

All circuits are auditable, verifiably correct, and ready for production deployment.

<!-- STANDARD: 3min -->
## Verification Guardrails

- [ ] No unconstrained signals in the circuit (verified by static analysis and manual review)
- [ ] Every public input has a range check or other constraint preventing malicious witness injection
- [ ] Trusted setup ceremony completed with ≥ N independent participants, all attestations verified
- [ ] Verifier contract bytecode verified on-chain and matches audited source
- [ ] Fuzz test: 10K+ random valid proofs verified successfully; 10K+ invalid witnesses rejected
- [ ] Nullifier domain separation: unique application scope in nullifier computation
- [ ] Incident response plan for proof system vulnerability: verifier upgrade path, circuit breaker, disclosure timeline
- [ ] All ZKP decisions recorded in State Log with security assumptions documented


## References

| File | Contents |
|------|----------|
| `references/decision-trees.md` | Summary of all 6 ZKP decision tree domains |
| `references/1-proof-system-selection-decision-tree.md` | Groth16, STARKs, Halo2, Plonky3 detailed comparison |
| `references/2-circuit-language-choice-decision-tree.md` | Circom 2 vs Noir vs Halo2 vs ZoKrates |
| `references/3-constraint-security-decision-tree--gotchas.md` | Under-constraint detection, Boolean enforcement, range checks |
| `references/4-range-check-strategy-decision-tree.md` | Num2Bits, LessThan, custom range check patterns |
| `references/5-recursive-proving-decision-tree.md` | Nova, SuperNova, Halo2, Protostar folding |
| `references/6-trusted-setup-strategy-decision-tree.md` | Powers of Tau, Phase 2, beacon, participant verification |
| `references/7-zkp-applications-architecture.md` | Private transactions, zk-rollups, zk-identity, zk-email |
| `references/8-solidity-verifier-deployment.md` | Groth16/Plonky3/Halo2 verifier deployment patterns |
| `references/12-security-hardening.md` | Production hardening checklist for ZKP circuits |
| `references/14-anti-rationalization-clauses.md` | Anti-rationalization clauses (embedded in this SKILL.md) |

### External References

| System | Description |
|--------|-------------|
| Circom 2 | R1CS circuit language with JavaScript-like syntax (https://github.com/iden3/circom) |
| snarkjs | Groth16 proving and Solidity verifier generation (https://github.com/iden3/snarkjs) |
| Noir | High-level Rust-like ZK DSL (https://noir-lang.org) |
| Halo2 | Custom gates and lookup tables ZK DSL (https://github.com/zcash/halo2) |
| Plonky3 | Small-field PLONKish arithmetization (https://github.com/Plonky3/Plonky3) |
| Nova | Folding-based IVC (https://github.com/microsoft/Nova) |
| SuperNova | Non-uniform IVC with multiple instruction sets |
| ethSTARK | STARK parameter set for Ethereum |
| RISC Zero | ZKVM for general-purpose computation |
