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
