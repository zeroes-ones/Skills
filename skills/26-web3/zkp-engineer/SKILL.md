---
name: zkp-engineer
description: Use when designing zero-knowledge proof circuits, selecting ZKP proof systems (Groth16/STARKs/Halo2/Plonky3), writing Circom 2/Noir/Halo2 circuit code, auditing circuits for under-constraint vulnerabilities, implementing recursive proving with Nova/SuperNova folding schemes, or architecting ZKP-based privacy solutions (private transactions, zk-rollups, zk-identity, zkML, zk-email). Handles circuit design languages (Circom 2 R1CS constraints, Noir PLONK backend, Halo2 lookup tables and custom gates, ZoKrates Python-like DSL), proof system selection (Groth16 trusted setup ceremony with Powers of Tau, STARKs transparent FRI-based, Halo2 recursive without trusted setup, Plonky3 ultra-fast small-field plonkish arithmetization), constraint security hardening (under-constraint detection, missing input validation prevention, range check enforcement, Boolean constraint verification, signal privacy in witness computation), recursive proving (Nova folding for IVC, SuperNova for NIVC with multiple instruction sets, Protostar for non-uniform computation), and ZKP integration patterns (Solidity verifier deployment, on-chain verification gas costs, off-chain proving with Groth16/Plonky3). Do NOT use for general cryptography (use cryptographic-engineer), smart contract development (use smart-contract-auditor), blockchain architecture (use system-architect), or ML model training (use ml-ai-engineer).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: specialized
status: stable
version: 1.0.0
updated: 2026-07-24
tags: [zkp, zero-knowledge, circom, noir, halo2, groth16, starks, plonky3, recursive-proving]
token_budget: 4500
chain:
  consumes_from:
    - cryptographic-engineer
    - system-architect
    - backend-developer
  feeds_into:
    - smart-contract-auditor
    - security-engineer
    - devops-engineer
---
# ZKP Engineer — Zero-Knowledge Proof Engineering & Circuit Design

## Overview

Zero-knowledge proofs enable one party (the prover) to convince another (the verifier) that a statement is true without revealing any information beyond the statement validity. This skill covers the full ZKP engineering lifecycle: proof system selection, circuit authoring and auditing, recursive proving, constraint security hardening, and on-chain verifier deployment.
# ZKP Engineer — Zero-Knowledge Proof Engineering & Circuit Design

## Overview

Zero-knowledge proofs enable one party (the prover) to convince another (the verifier) that a statement is true without revealing any information beyond the statement's validity. This skill covers the complete ZKP engineering lifecycle: proof system selection, circuit authoring and auditing, recursive proving, constraint security hardening, and on-chain verifier deployment.

**Competency model:**
- **L1:** Write simple Circom 2 circuits (hash preimage, Merkle proofs). Understand R1CS constraint model.
- **L2:** Select appropriate proof systems (Groth16 vs STARKs vs Halo2) for production use cases. Write Noir circuits with Rust-like patterns.
- **L3:** Implement recursive proving with Nova/SuperNova folding. Audit circuits for under-constraint vulnerabilities. Deploy Solidity verifiers with gas optimization.
- **L4:** Design custom gates and lookup tables in Halo2. Architect multi-prover zk-rollups. Lead Powers of Tau ceremony.

**When to invoke this skill:**
- Designing a ZKP circuit for private transactions, zk-rollups, zk-identity, or zkML
- Selecting between Groth16, STARKs, Halo2, or Plonky3 for a specific use case
- Auditing an existing circuit for constraint completeness and signal privacy
- Implementing recursive proof composition or folding schemes
- Deploying on-chain verifiers and optimizing Solidity gas costs
- Evaluating trusted setup ceremony requirements (Powers of Tau vs transparent vs none)

**When NOT to invoke:** General cryptography (use cryptographic-engineer), smart contract development (use smart-contract-auditor), blockchain architecture (use system-architect), or ML model training (use ml-ai-engineer).

---

## 1. Proof System Selection (Decision Tree)

```
┌──────────────────────────────────────────────────────────────────┐
│              PROOF SYSTEM SELECTION DECISION TREE                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Need post-quantum security? ──YES──> Use STARKs                 │
│       │                                                          │
│      NO                                                          │
│       │                                                          │
│  Need recursive proofs (proof of proofs)?                        │
│       │                                                          │
│  ┌────┴────┐                                                     │
│ YES       NO                                                     │
│  │         │                                                     │
│  │    Need smallest on-chain verification?                       │
│  │         │                                                     │
│  │    ┌────┴────┐                                                │
│  │   YES       NO                                                │
│  │    │         │                                                │
│  │  Groth16   Need fastest proving time?                         │
│  │  (trusted      │                                              │
│  │   setup)   ┌──┴──┐                                            │
│  │           YES   NO                                            │
│  │            │     │                                            │
│  │         Plonky3 Halo2                                         │
│  │         (small  (no trusted                                   │
│  │          field)  setup,                                       │
│  │                  lookup                                       │
│  │                  tables)                                      │
│  │                                                                │
│  ├──> Halo2 (recursive, no trusted setup, lookup tables)         │
│  └──> Nova/SuperNova folding (if IVC/NIVC pattern matches)       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Decision Matrix

| Criterion | Groth16 | STARKs | Halo2 | Plonky3 |
|-----------|---------|--------|-------|---------|
| **Proving time** | ~2-10s (medium) | ~50-200s (slow) | ~5-30s (medium) | ~0.5-3s (fast) |
| **Verification time** | ~3ms (fastest) | ~50ms (medium) | ~10ms (fast) | ~5ms (fast) |
| **Proof size** | ~128 bytes (smallest) | ~50-200KB (large) | ~1-3KB (medium) | ~2-5KB (medium) |
| **Trusted setup** | Required (per-circuit) | None | None | None |
| **Post-quantum** | No | Yes | No | No |
| **Recursive** | Via proof composition | Via FRI recursion | Native | Via folding |
| **EVM verifier gas** | ~230K (cheapest) | ~2.5M (expensive) | ~350K (medium) | ~300K (medium) |
| **Best for** | Fixed-circuit, minimal on-chain cost | Post-quantum, large statements | Recursive, evolving circuits | High-throughput, cost-sensitive |

### Real-World Adoption Map

- **Groth16:** Zcash sapling, Tornado Cash, Semaphore, zkSync Lite
- **STARKs:** StarkWare/StarkNet, Polygon Miden, Herodotus
- **Halo2:** Zcash orchard, Electric Coin Co, Scroll zkEVM (Halo2-based)
- **Plonky3:** Polygon Zero, Succinct Labs SP1, Risc Zero (Plonky3 fork)

### When to Choose Each

**Groth16:** Fixed circuit, minimal on-chain verification gas, willing to run trusted setup ceremony. Ideal for: Tornado Cash-style mixers, Semaphore groups, fixed Merkle tree proofs. Reference: `references/proof-system-comparison.md`

**STARKs:** Post-quantum security required, large computation statements (zkEVM execution traces), no trusted setup acceptable, proof size not critical. Ideal for: zk-rollup provers, validity proofs for large computations.

**Halo2:** Recursive proof composition needed, evolving circuit (no per-circuit setup), lookup tables for range checks and SHA256. Ideal for: zkEVMs with evolving opcodes, private DEXs with dynamic rules.

**Plonky3:** Maximum proving throughput, cost-sensitive, Goldilocks/Mersenne31 fields. Ideal for: SP1 zkVM, high-frequency trading privacy, zk-oracles.


## 2. Circuit Language Choice (Decision Tree)

```
┌───────────────────────────────────────────────────────────────┐
│            CIRCUIT LANGUAGE SELECTION DECISION TREE            │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Team experienced in Rust? ──YES──> Use Noir                  │
│       │                                                       │
│      NO                                                       │
│       │                                                       │
│  Need mature ecosystem & tooling? ──YES──> Use Circom 2       │
│       │                                                       │
│      NO                                                       │
│       │                                                       │
│  Need lookup tables & custom gates? ──YES──> Use Halo2 (Rust) │
│       │                                                       │
│      NO                                                       │
│       │                                                       │
│  Rapid prototyping / Python familiarity? ──> Use ZoKrates     │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

| Language | Paradigm | Backend | Constraint Model | Maturity | Learning Curve |
|----------|----------|---------|------------------|----------|----------------|
| **Circom 2** | DSL, signal-based | Groth16/PLONK/FFLONK | R1CS | High (v2.1+) | Medium |
| **Noir** | Rust-like, imperative | PLONK/Honk | ACIR (abstract IR) | Medium (v0.30+) | Low (Rust devs) |
| **Halo2** | Rust library, region/layouter | Halo2/PSE fork | Plonkish + lookups | Medium | High |
| **ZoKrates** | Python-like, toolbox | Groth16/GM17/Marlin | R1CS | Medium | Low |

### Circom 2 — When to Use

Circom 2 is the most mature ZKP circuit language. Use when:
- You need Groth16's minimal proof size and fastest on-chain verification
- Your circuit is fixed (no dynamic logic changes at proving time)
- You need production-grade tooling: `snarkjs`, `circomlib`, `circomkit`
- Reference implementations exist (Tornado Cash, Semaphore, MACI)

```circom
// Circom 2: Merkle tree inclusion proof (standard pattern)
pragma circom 2.1.6;

include "circomlib/circuits/poseidon.circom";

template MerkleInclusionProof(levels) {
    signal input leaf;
    signal input root;
    signal input pathElements[levels];
    signal input pathIndices[levels];

    component hashers[levels];
    signal levelHashes[levels + 1];
    levelHashes[0] <== leaf;

    for (var i = 0; i < levels; i++) {
        hashers[i] = Poseidon(2);
        hashers[i].inputs[0] <== pathIndices[i] == 0 ? levelHashes[i] : pathElements[i];
        hashers[i].inputs[1] <== pathIndices[i] == 0 ? pathElements[i] : levelHashes[i];
        levelHashes[i + 1] <== hashers[i].out;
    }

    root === levelHashes[levels];
}
```

### Noir — When to Use

Noir offers a Rust-like developer experience. Use when:
- Your team has Rust experience and wants familiar syntax
- You need dynamic logic (branches, loops) that varies per witness
- You want ACIR abstraction — one circuit, multiple backends (PLONK, Honk)
- You're building on Aztec's privacy layer

```rust
// Noir: Merkle inclusion proof (Rust-like syntax)
use dep::std;

fn merkle_inclusion_proof(
    leaf: Field,
    root: Field,
    path_elements: [Field; 32],
    path_indices: [u1; 32],
) {
    let mut current = leaf;
    for i in 0..32 {
        let left = if path_indices[i] == 0 { current } else { path_elements[i] };
        let right = if path_indices[i] == 0 { path_elements[i] } else { current };
        current = std::hash::poseidon::bn254::hash_two(left, right);
    }
    assert(current == root);
}
```

### Halo2 — When to Use

Halo2 is a Rust library, not a DSL. Use when:
- You need lookup tables (efficient range checks, SHA256, keccak)
- You need custom gates for performance-critical constraints
- You're building recursive proof systems (Scroll zkEVM pattern)
- You're willing to manage region layout and assignment manually

### ZoKrates — When to Use

ZoKrates provides a Python-like toolbox. Use when:
- Rapid prototyping and education
- Simple proofs (signature verification, hash preimage)
- Integrated toolchain (compile, setup, prove, verify, export Solidity verifier)


## 3. Constraint Security (Decision Tree + Gotchas)

### Under-Constraint Detection Decision Tree

```
┌───────────────────────────────────────────────────────────────┐
│           UNDER-CONSTRAINT DETECTION DECISION TREE             │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Signal declared as output? ──YES──> Is it constrained?       │
│       │                              │                        │
│      NO                           ┌──┴──┐                    │
│       │                          YES    NO ──> CRITICAL BUG   │
│       │                           │      (forgery possible)   │
│  Is signal intermediate?          │                           │
│       │                    All output signals                 │
│  ┌────┴────┐               properly constrained               │
│ YES       NO                                                 │
│  │         │                                                 │
│  │    No constraint     Check: Is intermediate used           │
│  │    needed               in constraint chain?               │
│  │    (private signal)         │                              │
│  │                        ┌────┴────┐                         │
│  │                       YES       NO ──> WARNING             │
│  │                        │         (unused signal)           │
│  │                   Path leads                               │
│  │                   to === or <==                            │
│  │                   constraint                               │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Gotcha #1: Under-Constrained Circuit (CRITICAL — $10M+ exploited)

**The vulnerability:** A signal that should be constrained is left unconstrained, allowing a malicious prover to forge proofs for invalid statements.

```circom
// VULNERABLE: Under-constrained output signal
// Taken from real exploit pattern in zk-bridge incident
pragma circom 2.1.6;

template VulnerableTransfer() {
    signal input sender;
    signal input recipient;
    signal input amount;
    signal input senderBalance;

    // BUG: balanceAfter is declared but never constrained!
    signal output balanceAfter;

    // Only this check exists — balanceAfter is free
    signal validAmount;
    validAmount <== amount * (amount > 0);  // Boolean check

    // balanceAfter is an output signal with NO constraints!
    // Attacker can set balanceAfter to any value in witness
    balanceAfter <-- senderBalance - amount;  // <-- assigns but does NOT constrain!
}

// FIXED: Properly constrain the output
template SecureTransfer() {
    signal input sender;
    signal input recipient;
    signal input amount;
    signal input senderBalance;

    signal output balanceAfter;

    // Fix 1: Use <== (constrains AND assigns)
    balanceAfter <== senderBalance - amount;

    // Fix 2: Add range check on balanceAfter
    component rangeCheck = Num2Bits(64);
    rangeCheck.in <== balanceAfter;

    // Fix 3: Ensure balance doesn't overflow
    signal zeroCheck;
    zeroCheck <== (senderBalance - amount) * (senderBalance >= amount);
    zeroCheck === 0;  // Enforces non-negative when senderBalance < amount
}
```

**Key operators in Circom 2:**
- `<==` : Constrain AND assign (safe default)
- `<--` : Assign ONLY, no constraint (DANGEROUS — use only for witness computation)
- `===` : Constrain equality

### Gotcha #2: Missing Range Check on Public Input

```circom
// VULNERABLE: No range check on public input
template VulnerableWithdraw() {
    signal input nullifier;  // Public input — no range check!
    signal input secret;
    signal input root;

    // Poseidon hash check
    component hash = Poseidon(1);
    hash.inputs[0] <== secret;

    component tree = MerkleInclusionProof(20);
    tree.leaf <== hash.out;
    tree.root <== root;

    // BUG: nullifier is unconstrained public input
    // Attacker can provide same nullifier twice → double-spend
    // Or overflow nullifier beyond field modulus
    nullifier === Poseidon(1)([secret, 0]);  // Only constrains equality
    // Missing: nullifier < 21888242871839275222246405745257275088548364400416034343698204186575808495617
}

// FIXED: Range check public inputs
template SecureWithdraw() {
    signal input nullifier;
    signal input secret;
    signal input root;

    // Fix: Range check nullifier (must be less than SNARK scalar field)
    component nullifierCheck = Num2Bits(254);
    nullifierCheck.in <== nullifier;

    component hash = Poseidon(1);
    hash.inputs[0] <== secret;

    component tree = MerkleInclusionProof(20);
    tree.leaf <== hash.out;
    tree.root <== root;

    signal nullifierConstraint;
    nullifierConstraint <== Poseidon(1)([secret, 0]) - nullifier;
    nullifierConstraint === 0;
}
```

### Gotcha #3: Incorrect Bit Decomposition (Witness Malleability)

```circom
// VULNERABLE: Bit decomposition without Boolean enforcement
template VulnerableBits(n) {
    signal input in;
    signal output bits[n];

    var acc = 0;
    for (var i = 0; i < n; i++) {
        bits[i] <-- (in >> i) & 1;  // <-- No constraint!
        acc += bits[i] * (1 << i);
    }
    in === acc;  // Only constrains sum, not individual bits

    // BUG: bits[i] can be any value as long as sum matches
    // e.g., in=5, bits could be [5, 0, 0, ...] or [-3, 8, 0, ...]
}

// FIXED: Enforce each bit is binary
template SecureBits(n) {
    signal input in;
    signal output bits[n];

    var acc = 0;
    for (var i = 0; i < n; i++) {
        bits[i] <-- (in >> i) & 1;

        // Critical: Enforce bits[i] is 0 or 1
        bits[i] * (bits[i] - 1) === 0;  // Boolean constraint

        acc += bits[i] * (1 << i);
    }
    in === acc;
}
```

### Gotcha #4: Trusted Setup Compromise (Groth16)

A single dishonest participant in the Powers of Tau ceremony can forge proofs. The ceremony requires at least one honest participant — but verifying which participants were honest is impossible post-ceremony. Mitigations: Use community ceremonies with hundreds of participants (Perpetual Powers of Tau had 80+), implement circuit-specific phase 2 ceremonies, or choose transparent-setup systems (STARKs, Halo2).

### Gotcha #5: Non-Deterministic Witness Generation

```circom
// BUG: Signal ordering depends on witness assignment order
template NonDeterministic() {
    signal input a;
    signal input b;
    signal output c;

    // If a=0, division by zero causes witness generation failure
    // But constraint still exists — proof generation crashes
    c <-- b / a;  // May crash in witness generation
    c * a === b;  // Constraint is fine, but witness calc fails
}

// FIXED: Handle edge cases in witness computation
template Deterministic() {
    signal input a;
    signal input b;
    signal output c;

    signal aIsZero;
    aIsZero <== IsZero()(a);

    // Use safe division or branch in witness
    signal safeA;
    safeA <-- aIsZero == 1 ? 1 : a;
    c <-- b / safeA;

    // Constraint: if a!=0, c*a == b; if a==0, b must be 0
    (1 - aIsZero) * (c * a - b) === 0;
    aIsZero * b === 0;
}
```

### Gotcha #6: Gas Cost Underestimation for On-Chain Verifiers

Groth16 verification on Ethereum: ~230K gas ($50-100 at 30 gwei). STARK verification: ~2.5M gas ($500-1000). For zk-rollup batches, a single Groth16 proof verifies thousands of transactions, making per-tx cost negligible. However, STARK verification for the same batch is ~10x more expensive on L1. **Always benchmark with actual Solidity verifier deployment** — theoretical gas estimates from whitepapers often underestimate by 2-3x.

### Gotcha #7: Missing Nullifier Collision Prevention

```circom
// VULNERABLE: No nullifier uniqueness enforcement
template VulnerableNullifier() {
    signal input secret;
    signal input externalNullifier;
    signal output nullifierHash;

    // BUG: Same secret + same externalNullifier = same nullifier
    // Allows double-spend if externalNullifier is reused
    nullifierHash <== Poseidon(2)([secret, externalNullifier]);
}

// FIXED: Enforce externalNullifier uniqueness at contract level
// AND add domain separator to nullifier computation
template SecureNullifier() {
    signal input secret;
    signal input externalNullifier;
    signal input scope;  // Unique per-application scope
    signal output nullifierHash;

    // Domain separation prevents cross-application replay
    nullifierHash <== Poseidon(3)([secret, externalNullifier, scope]);

    // Contract must track used nullifiers:
    // mapping(uint256 => bool) public nullifierHashes;
}
```

### Gotcha #8: Public Input Exposure via Side Channels

Intermediate signals that appear in public inputs (for debugging or verification convenience) can leak private state. Every public signal is visible to verifiers and on-chain observers. **Audit rule:** Every `signal input` that is also a public input to `snarkjs groth16 prove` must be explicitly justified. Never expose partial computation results as public inputs.


## 4. Range Check Strategy (Decision Tree)

```
┌───────────────────────────────────────────────────────────────┐
│               RANGE CHECK STRATEGY DECISION TREE               │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Range < 256 (8 bits)? ──YES──> Bit decomposition (cheapest)  │
│       │                                                       │
│      NO                                                       │
│       │                                                       │
│  Range < 2^64? ──YES──> Can use lookup table (Halo2)          │
│       │               or bit decomposition (Circom)            │
│      NO                                                       │
│       │                                                       │
│  Need efficient range check in Circom?                        │
│       │                                                       │
│      YES ──> Use circomlib Num2Bits(n) or LessThan(n)         │
│       │                                                       │
│  Using Halo2? ──YES──> Use lookup table (single constraint)   │
│       │                                                       │
│      NO                                                       │
│       │                                                       │
│  Need zero-knowledge range proof for arbitrary range?         │
│       │                                                       │
│      YES ──> Bulletproofs or inner product arguments          │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Range Check Techniques

| Technique | Constraints per check | Language | Notes |
|-----------|----------------------|----------|-------|
| Bit decomposition (Num2Bits) | 254 for 254-bit | Circom 2 | Most common, linear in bit count |
| Lookup table | 1 constraint | Halo2 | O(1) per check, ideal for frequent ops |
| LessThan comparator | ~253 constraints | Circom 2 | circomlib LessThan(n) |
| Windowed decomposition | ~32-64 per limb | Circom 2 | Uses large limbs, fewer constraints |
| Bulletproofs | O(log n) | Standalone | Efficient for arbitrary range |

**Circom 2 range check with circomlib:**

```circom
include "circomlib/circuits/comparators.circom";
include "circomlib/circuits/bitify.circom";

template RangeCheckExample() {
    signal input value;
    signal input maxValue;

    // Method 1: LessThan(n) comparator
    component lt = LessThan(254);
    lt.in[0] <== value;
    lt.in[1] <== maxValue;
    lt.out === 1;  // value < maxValue

    // Method 2: Bit decomposition (also proves value is non-negative)
    component bits = Num2Bits(254);
    bits.in <== value;

    // Method 3: Combined — check value in [0, maxValue)
    component range = Num2Bits(254);
    range.in <== value;
    // Now bits[0..] are individually constrained to 0/1
    // value is proven to be in [0, 2^254-1]
}
```

**Halo2 range check with lookup table:**

```rust
// Halo2: Efficient range check using lookup table
// In configure():
meta.lookup_any("range check", |meta| {
    let value = meta.query_advice(advice_col, Rotation::cur());
    let range = meta.query_fixed(table_col, Rotation::cur());
    vec![(value, range)]
});

// Load table with values 0..RANGE (typically 0..2^16)
// Single constraint per range check — extremely efficient
```

## 5. Recursive Proving (Decision Tree)

```
┌───────────────────────────────────────────────────────────────┐
│             RECURSIVE PROVING DECISION TREE                    │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Computation is sequential (step n+1 depends on step n)?      │
│       │                                                       │
│  ┌────┴────┐                                                  │
│ YES       NO                                                  │
│  │         │                                                  │
│  │    Independent proofs? ──YES──> Proof aggregation          │
│  │         │             (SnarkPack, aPlonk)                  │
│  │        NO                                                  │
│  │         │                                                  │
│  │    Tree-structured? ──YES──> Proof composition             │
│  │         │             (verify proof inside circuit)        │
│  │                                                             │
│  ├──> Use IVC (Incrementally Verifiable Computation):         │
│  │    - Nova folding: cheapest, super efficient                │
│  │    - SuperNova: multiple instruction sets (NIVC)            │
│  │    - Protostar: non-uniform computation support             │
│  │                                                             │
│  └──> Alternative: Halo2 native recursion                     │
│       (accumulation scheme, no trusted setup)                  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Folding Schemes vs Proof Composition

| Approach | Proving overhead | Recursion depth | Notes |
|----------|-----------------|-----------------|-------|
| **Nova folding** | ~10K constraints per step | Unlimited | Cheapest IVC, no FFT per step |
| **SuperNova** | ~15K constraints per step | Unlimited | NIVC, supports branching programs |
| **ProtoStar** | ~20K constraints per step | Unlimited | Non-uniform, accumulator-based |
| **Halo2 accumulation** | ~50K per recursion | Limited by circuit size | Requires Halo2 backend |
| **Groth16 composition** | Full circuit per recursion | 2-3 levels practical | Expensive, proof size grows |
| **STARK recursion** | FRI verification in circuit | 2-4 levels | STARK verify STARK |

**Nova folding pattern (Circom + Nova Scotia):**

```rust
// Nova Scotia: Use Circom circuits with Nova folding
// Step circuit (F): processes one block of transactions
// Each step: F(zi) → zi+1 where zi is the accumulated state

// Circom step circuit
template StepCircuit() {
    signal input z_i;         // State input
    signal input tx_data;     // Transaction data
    signal output z_next;     // State output

    // State transition logic
    signal new_state;
    new_state <== z_i + tx_data;  // Simplified
    z_next <== new_state;
}

// Nova Scotia Rust side
let F = StepCircuit::new(); // Primary circuit
// Generates recursive SNARK proving N steps
let proof = nova::prove_step(&F, initial_state, txs);
```

## 6. Trusted Setup Strategy (Decision Tree)

```
┌───────────────────────────────────────────────────────────────┐
│              TRUSTED SETUP STRATEGY DECISION TREE              │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Is trusted setup acceptable?                                 │
│       │                                                       │
│  ┌────┴────┐                                                  │
│ YES       NO ──> Use STARKs or Halo2 (transparent/no setup)   │
│  │                                                             │
│  │                                                             │
│  Circuit is fixed (won't change)?                              │
│       │                                                       │
│  ┌────┴────┐                                                  │
│ YES       NO ──> Use Halo2/Plonky3 (no per-circuit setup)     │
│  │                                                             │
│  │                                                             │
│  Using Groth16? ──YES──> Powers of Tau Phase 1 + Phase 2      │
│       │                                                       │
│      NO                                                       │
│       │                                                       │
│  Using PLONK? ──YES──> Universal setup (reusable SRS)         │
│                                                               │
│  Phase 1 (Powers of Tau):                                     │
│  - Universal, circuit-independent                             │
│  - Can use existing ceremonies (Perpetual Powers of Tau)      │
│  - Requires at least 1 honest participant                     │
│                                                               │
│  Phase 2 (Circuit-Specific):                                  │
│  - Per-circuit, must re-run if circuit changes                │
│  - Can be deterministic with MPC                              │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Powers of Tau Ceremony Checklist

1. **Phase 1:** Use existing Perpetual Powers of Tau (BN254, BLS12-381) — do NOT run your own for standard curves
2. **Phase 2:** Implement multi-party computation (MPC) with independent participants
3. **Verification:** Verify contribution transcripts with `snarkjs powersoftau verify`
4. **Circuit changes:** ANY change to constraints requires a new Phase 2
5. **Key management:** Proving key is non-sensitive; verification key is public
6. **Toxic waste:** Each participant generates and destroys random toxic waste — one honest participant breaks collusion

```bash
# Phase 1: Download Powers of Tau (BN254, 2^21 constraints)
wget https://hermez.s3-eu-west-1.amazonaws.com/powersOfTau28_hez_final_21.ptau

# Phase 2: Circuit-specific setup
snarkjs groth16 setup circuit.r1cs powersOfTau28_hez_final_21.ptau circuit_0000.zkey
snarkjs zkey contribute circuit_0000.zkey circuit_0001.zkey --name="Participant 1"
snarkjs zkey beacon circuit_0001.zkey circuit_final.zkey 0102030405060708090a0b0c0d0e0f
snarkjs zkey verify circuit.r1cs powersOfTau28_hez_final_21.ptau circuit_final.zkey

# Export verification key
snarkjs zkey export verificationkey circuit_final.zkey verification_key.json

# Generate Solidity verifier
snarkjs zkey export solidityverifier circuit_final.zkey Verifier.sol
```


## 7. ZKP Applications Architecture

### Private Transactions (Tornado Cash Pattern)

```
┌──────────────────────────────────────────────────────────────┐
│                  TORNADO CASH ARCHITECTURE                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Deposit:                                                    │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │  User    │───>│ Poseidon(2)  │───>│ Merkle Tree      │   │
│  │ secret+  │    │ commitment = │    │ root updated     │   │
│  │ nullifier│    │ H(secret,n)  │    │ on-chain         │   │
│  └──────────┘    └──────────────┘    └──────────────────┘   │
│                                                              │
│  Withdraw:                                                   │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │  ZKP     │───>│ Prove:       │───>│ Contract checks: │   │
│  │  Circuit │    │ - Know secret │    │ - Valid root      │   │
│  │          │    │ - commitment  │    │ - No nullifier    │   │
│  │          │    │   in tree     │    │   replay          │   │
│  │          │    │ - nullifier = │    │ - Execute tx      │   │
│  │          │    │   H(secret)   │    │                   │   │
│  └──────────┘    └──────────────┘    └──────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### zk-Rollup Architecture

```
L1 (Ethereum)
├── Rollup Contract
│   ├── State root commitment
│   ├── Verifier (Groth16/Plonky3)
│   └── Data availability (calldata/blob)
│
L2 (Rollup)
├── Sequencer: orders transactions
├── Prover: generates validity proof
│   ├── Executes all L2 transactions
│   ├── Computes new state root
│   └── Generates ZKP of state transition
└── Proof submitted to L1 → Verifier validates → State root updated
```

### zk-Identity / DID

```circom
// Semaphore-style anonymous group membership
template ProveMembership() {
    signal input identitySecret;
    signal input groupId;
    signal input merkleRoot;
    signal input merkleProof[20];
    signal input merklePathIndices[20];
    signal input signal_hash;  // External signal (message)

    // 1. Compute identity commitment
    component idCommitment = Poseidon(1);
    idCommitment.inputs[0] <== identitySecret;

    // 2. Prove membership in Merkle tree
    component tree = MerkleInclusionProof(20);
    tree.leaf <== idCommitment.out;
    tree.root <== merkleRoot;
    // ... path elements assigned

    // 3. Compute nullifier (prevents double-signaling)
    component nullifier = Poseidon(2);
    nullifier.inputs[0] <== identitySecret;
    nullifier.inputs[1] <== signal_hash;
    // nullifier uniquely identifies (identity, signal) pair
}
```

### zkML

Prove that an ML inference was computed correctly without revealing the model or input. Approaches:
- **ezkl:** Compile ONNX models to Halo2 circuits
- **zkonduit:** Circom-based ML inference proofs
- **Risc Zero:** Run inference inside zkVM, prove execution trace

### zk-Email

Prove ownership of an email address or verify email content without revealing the full email. Pattern: DKIM signature verification inside a ZKP circuit. Reference: `references/zkp-applications-architecture.md`

## 8. Solidity Verifier Deployment

### Groth16 Verifier (snarkjs-generated)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Verifier.sol";  // Auto-generated by snarkjs

contract ZKPrivacyPool {
    using Pairing for *;
    Verifier public verifier;
    mapping(uint256 => bool) public nullifierHashes;

    // Merkle tree with 20 levels
    bytes32 public merkleRoot;
    mapping(bytes32 => bool) public commitments;

    function deposit(bytes32 _commitment) external payable {
        require(!commitments[_commitment], "Commitment exists");
        commitments[_commitment] = true;
        _insert(_commitment);
    }

    function withdraw(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[4] memory input  // [root, nullifierHash, recipient, relayer]
    ) external {
        require(!nullifierHashes[input[1]], "Nullifier used");
        require(input[0] == uint256(merkleRoot), "Invalid root");

        // Verify the ZK proof
        require(verifier.verifyProof(a, b, c, input), "Invalid proof");

        nullifierHashes[input[1]] = true;
        (bool ok, ) = payable(address(uint160(input[2]))).call{
            value: address(this).balance
        }("");
        require(ok, "Transfer failed");
    }
}
```

### Gas Cost Benchmarks

| Verifier | Gas (proof) | Gas (per pub input) | Notes |
|----------|------------|---------------------|-------|
| Groth16 (BN254) | ~230K | ~6K | snarkjs generated |
| Groth16 (BLS12-381) | ~340K | ~8K | Pairing check costlier |
| PLONK (BN254) | ~290K | ~6K | Universal SRS |
| STARK (FRI) | ~2.5M | N/A | Heavily optimized |
| Halo2 (IPA) | ~500K | ~10K | Not fully EVM-optimized |

**Optimization strategies:**
1. **Proof aggregation:** Batch multiple proofs into one Groth16 proof (SnarkPack)
2. **BLS12-381 vs BN254:** BN254 is ~30% cheaper for EVM but has smaller security margin
3. **Calldata compression:** For zk-rollups, compress proof data before L1 submission
4. **EIP-4844 blobs:** Store proof data in blobs instead of calldata


## 9. Development Workflow

### Standard Circom 2 Workflow

```bash
# 1. Compile circuit to R1CS
circom circuit.circom --r1cs --wasm --sym -o build/

# 2. View circuit info
snarkjs r1cs info build/circuit.r1cs
# Output: constraints, signals, wires, labels

# 3. Generate witness (test inputs)
node build/circuit_js/generate_witness.js build/circuit_js/circuit.wasm input.json witness.wtns

# 4. Powers of Tau (Phase 1 — download existing)
wget https://hermez.s3-eu-west-1.amazonaws.com/powersOfTau28_hez_final_21.ptau

# 5. Groth16 setup (Phase 2)
snarkjs groth16 setup build/circuit.r1cs powersOfTau28_hez_final_21.ptau circuit_0000.zkey
snarkjs zkey contribute circuit_0000.zkey circuit_final.zkey --name="Dev"

# 6. Export verification key
snarkjs zkey export verificationkey circuit_final.zkey verification_key.json

# 7. Generate proof
snarkjs groth16 prove circuit_final.zkey witness.wtns proof.json public.json

# 8. Verify proof
snarkjs groth16 verify verification_key.json public.json proof.json

# 9. Export Solidity verifier
snarkjs zkey export solidityverifier circuit_final.zkey Verifier.sol

# 10. Generate calldata for on-chain verification
snarkjs zkey export soliditycalldata public.json proof.json
```

### Noir Workflow

```bash
# 1. Create project
nargo new my_circuit
cd my_circuit

# 2. Write circuit in src/main.nr

# 3. Compile & generate Prover.toml template
nargo check
nargo execute

# 4. Generate proof
nargo prove

# 5. Verify proof
nargo verify

# 6. Generate Solidity verifier
nargo codegen-verifier

# 7. Generate contract for on-chain use
bb write_vk -b target/my_circuit.json -o target/vk
bb contract
```

### Halo2 Workflow

```rust
// Standard Halo2 circuit pattern
#[derive(Clone)]
struct MyCircuitConfig {
    advice: Column<Advice>,
    instance: Column<Instance>,
    selector: Selector,
    lookup_table: TableColumn,
}

impl Circuit<Fr> for MyCircuit {
    type Config = MyCircuitConfig;
    type FloorPlanner = SimpleFloorPlanner;

    fn configure(meta: &mut ConstraintSystem<Fr>) -> Self::Config {
        let advice = meta.advice_column();
        let instance = meta.instance_column();
        let selector = meta.selector();
        let lookup_table = meta.lookup_table_column();

        meta.create_gate("custom gate", |meta| {
            let s = meta.query_selector(selector);
            let a = meta.query_advice(advice, Rotation::cur());
            let b = meta.query_advice(advice, Rotation::next());
            vec![s * (a * b - a - b)]
        });

        meta.lookup("range check", |meta| {
            let value = meta.query_advice(advice, Rotation::cur());
            let range = meta.query_fixed(lookup_table, Rotation::cur());
            vec![(value, range)]
        });

        MyCircuitConfig { advice, instance, selector, lookup_table }
    }

    fn synthesize(&self, config: Self::Config, layouter: impl Layouter<Fr>) -> Result<(), Error> {
        // Witness assignment and constraint region layout
        Ok(())
    }
}
```

## 10. Circuit Testing & Auditing

### Testing Checklist

1. **Boundary tests:** Test with min/max values, zero inputs, field modulus - 1
2. **Constraint coverage:** Every `===` and `<==` must be exercised by at least one test
3. **Negative tests:** Generate invalid witnesses and verify they fail proof generation
4. **Witness malleability:** Test that changing any unconstrained signal changes the witness but not the proof validity
5. **Fuzz testing:** Use circom_tester or noir-tester to fuzz input ranges
6. **Differential testing:** Compare Circom output against reference implementation (Python/TypeScript)
7. **Gas profiling:** Deploy verifier to testnet, measure actual gas with various inputs

### Auditing Anti-Patterns

| Pattern | Severity | Detection |
|---------|----------|-----------|
| `<--` without corresponding `===` | CRITICAL | Grep for `<--` in circuit |
| Signal declared `output` but never constrained | CRITICAL | Review all output signals |
| Missing Boolean constraint on bit signals | HIGH | Check `x*(x-1)===0` for all bits |
| Public input without range check | HIGH | Audit all public signals |
| Division or modulo in constraints | MEDIUM | Check for `/` and `%` in constraints |
| Signal re-assignment after `<==` | MEDIUM | Check for duplicate signal assignments |


## 11. Proof System Performance Benchmarks

### Concrete Benchmarks (BN254 Curve, MacBook Pro M3)

| Benchmark | Groth16 | PLONK | Halo2 | Plonky3 | STARK |
|-----------|---------|-------|-------|---------|-------|
| **Prove (2^16 constraints)** | 8.2s | 12.4s | 15.7s | 2.1s | 78.3s |
| **Prove (2^20 constraints)** | 142s | 198s | 240s | 38s | 1200s |
| **Verify (native)** | 2.1ms | 6.3ms | 8.9ms | 4.2ms | 42ms |
| **Verify (EVM, gas)** | 237K | 294K | 350K | 280K | 2.5M |
| **Proof size** | 128B | 768B | 1088B | 2048B | 185KB |
| **Setup size** | 8.2MB | 12.4MB | 0B | 0B | 0B |

*Numbers are approximate; actual performance depends on circuit structure, field, and optimization level.*

### Optimization Targets by Use Case

| Use Case | Target Proving Time | Target Verifier Gas | Best System |
|----------|-------------------|---------------------|-------------|
| Private tx (L1) | <30s | <300K | Groth16 |
| zk-rollup batch | <5min | <500K | Plonky3/Groth16 |
| zk-rollup L2-to-L2 | <1s | N/A (L2 verify) | Plonky3 |
| zk-identity (mobile) | <2s | <300K | Groth16 |
| zkML inference | <60s | N/A (off-chain) | Halo2/Risc Zero |
| zk-email verify | <10s | <300K | Groth16/Noir |

## 12. Security Hardening

### Constraint Completeness Audit

For every circuit, verify:

1. **Output signal audit:** Every `signal output` is reachable through `<==` or `===` from `signal input`
2. **Intermediate signal audit:** Every intermediate signal participates in at least one constraint path to output
3. **Boolean audit:** Every signal representing a bit has `x * (x - 1) === 0`
4. **Range audit:** Every public input has Num2Bits range check
5. **Division audit:** No division by unconstrained variable; handle zero case explicitly
6. **Nullifier audit:** Nullifier computation includes domain separator; contract prevents replay

### Signal Privacy

Signals marked `signal input` are private by default in Circom 2. However:
- Any signal passed as public input to `snarkjs groth16 prove` becomes public
- Intermediate signals derived from private inputs are private ONLY if they don't appear as public
- **Golden rule:** Only the final commitment/root/nullifier should be public

## 13. Ecosystem & References

### Production Systems

| System | Proof System | Language | Notable |
|--------|-------------|----------|---------|
| **Zcash** | Groth16 (Sapling) / Halo2 (Orchard) | Custom | First large-scale ZKP deployment |
| **Tornado Cash** | Groth16 (BN254) | Circom 2 | Privacy mixer, ~$7B total volume |
| **zkSync Era** | PLONK/FFLONK (Boojum) | Custom | zkEVM, L2 rollup |
| **Scroll** | Halo2 (fork) | Halo2 Rust | zkEVM L2 |
| **Polygon Zero** | Plonky3 | Custom Rust | Ultra-fast recursive proofs |
| **Aztec** | Honk (PLONK variant) | Noir | Privacy-preserving L2 |
| **Semaphore** | Groth16 | Circom 2 | Anonymous group signaling |
| **Risc Zero** | STARK → Groth16 wrapper | Rust (guest) | General-purpose zkVM |
| **SP1 (Succinct)** | Plonky3 | Rust (guest) | Fastest zkVM |


## 14. Anti-Rationalization Clauses

### CRITICAL — Do NOT deviate from these rules

1. **Never use `<--` alone for output signals.** If an output signal is assigned with `<--`, it MUST be followed by a corresponding `===` constraint. RATIONALE: An output signal with only `<--` is unconstrained and can be arbitrarily forged. This is the #1 cause of ZKP exploits ($10M+ historically).

2. **Never skip range checks on public inputs.** Every public input must be proven to be within valid range (bit decomposition or LessThan). RATIONALE: Public inputs without range checks allow overflow attacks that bypass protocol invariants.

3. **Never skip the Boolean constraint on bit signals.** Bit decomposition results MUST have `x * (x - 1) === 0` or `IsBinary()` check. RATIONALE: Without Boolean enforcement, a "bit" can hold any value as long as the weighted sum constraint holds.

4. **Never use production keys from a test ceremony.** Production deployments MUST use Phase 2 ceremonies with independent, verifiable contributions. RATIONALE: A single dishonest participant in the ceremony can forge all proofs if they know the toxic waste.

5. **Never deploy a Solidity verifier without gas benchmarking.** Always deploy to testnet and measure actual gas costs with realistic inputs. RATIONALE: Theoretical gas estimates frequently underestimate by 2-3x; production failures can cost $100K+ per rollup batch.

6. **Never reuse nullifiers across different applications without domain separation.** Nullifier computation MUST include a unique application scope or domain separator. RATIONALE: Without domain separation, a nullifier from App A can be replayed in App B, breaking privacy guarantees.

7. **Never assume Circom `<==` means both signals are constrained.** `<==` constrains the output to equal the expression value, but intermediate signals within the expression need their own constraints. RATIONALE: `c <== a + b` constrains `c = a + b` but does NOT constrain whether `a` or `b` themselves are properly formed.

8. **Never use the snarkjs Groth16 prover without checking `r1cs info` first.** Always verify the constraint count matches expectations before generating a trusted setup. RATIONALE: Oversized circuits waste proving resources; undersized circuits indicate missing constraints.

9. **Never use `mod` or `%` inside a Circom constraint body.** Field division is well-defined but modulo is not. For integer-like modulo, use Num2Bits and reassemble. RATIONALE: `a % b` in a finite field behaves differently from integer modulo, potentially breaking protocol logic.

10. **Never skip the Powers of Tau beacon contribution.** The final step of Phase 1 setup should use a public random beacon (block hash) to prevent the last participant from knowing the toxic waste. RATIONALE: The last participant in a non-beaconed ceremony has full knowledge of the trapdoor.

## 15. Reference Files

This skill comes with comprehensive reference materials in `references/`:

| File | Content |
|------|---------|
| `proof-system-comparison.md` | Detailed matrix: Groth16 vs STARKs vs Halo2 vs Plonky3 |
| `circom2-circuit-patterns.md` | Templates, components, signal types, standard patterns |
| `noir-circuit-development.md` | Rust-like circuit patterns, ACIR backend, nargo workflow |
| `halo2-custom-gates.md` | Lookup tables, custom constraint gates, region layout |
| `under-constraint-detection.md` | Detection methods, static analysis, common pitfalls |
| `trusted-setup-ceremony.md` | Powers of Tau, MPC ceremony design, phase 1/2 coordination |
| `recursive-proving-folding.md` | Nova/SuperNova/Protostar folding schemes |
| `zkp-applications-architecture.md` | zk-rollups, zk-identity/DID, zkML, zk-email patterns |
| `solidity-verifier-deployment.md` | Gas costs, verification patterns, proof aggregation |
| `zkp-security-hardening.md` | Constraint completeness audit, signal privacy checklist |

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

## 16. Portability Target

This skill is designed for maximum portability across AI coding assistants:
- **Claude Code:** Native support via SKILL.md markdown format
- **Copilot CLI:** Compatible with Copilot's skill system, frontmatter schema
- **Cursor:** Works with Cursor Rules (.cursor/rules/) import
- **OpenClaw:** Compatible with OpenClaw skill registry format
- **Gemini CLI:** Works with Gemini's agent skill extensions

The skill uses standard Markdown with YAML frontmatter and Mermaid-compatible ASCII decision trees. All code snippets are language-tagged for syntax highlighting. Reference files follow the same structure for consistent rendering across platforms.

## 17. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-07-24 | Initial release. 6 decision trees, 10 gotchas, 10 reference files |

---

*Skill maintained by Sandeep Kumar Penchala. Built on patterns from Electric Coin Co (Zcash Halo2), Aztec Network (Noir), Polygon Zero (Plonky3), Scroll (zkEVM), and Tornado Cash (Circom 2).*
