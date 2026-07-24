# Noir Circuit Development

## Overview

Noir is a Rust-like DSL for zero-knowledge proofs developed by Aztec Network. It compiles to an Abstract Circuit Intermediate Representation (ACIR) that is backend-agnostic.

## Key Concepts

### Frontend vs Backend

- **Noir (frontend):** Write circuits in Rust-like syntax
- **Barretenberg (backend):** Honk/PLONK proving system
- **ACIR:** Intermediate representation; same circuit works with multiple backends

### Project Structure

```
my_circuit/
├── Nargo.toml          # Project manifest
├── Prover.toml         # Prover inputs (private)
├── Verifier.toml       # Public inputs
└── src/
    └── main.nr         # Circuit entry point
```

## Standard Patterns

### 1. Hash Preimage

```rust
use dep::std;

fn main(preimage: pub Field, hash: pub Field) {
    let computed = std::hash::poseidon::bn254::hash_one(preimage);
    assert(computed == hash);
}
```

### 2. Merkle Inclusion Proof

```rust
use dep::std;

fn main(
    leaf: Field,
    root: pub Field,
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

### 3. Signature Verification

```rust
use dep::std;

fn main(
    message: [u8; 32],
    signature: [u8; 64],
    public_key: pub [u8; 64],
) {
    let valid = std::ecdsa_secp256k1::verify_signature(
        public_key,
        signature,
        message
    );
    assert(valid);
}
```

### 4. Range Check

```rust
fn main(value: Field, max: pub Field) {
    // Range check: 0 <= value < max
    assert(value < max);
    
    // Or bound check
    assert(value >= 0);
    assert(value < 2^64);
}
```

### 5. Conditional Logic

```rust
fn main(condition: bool, if_true: Field, if_false: Field) -> pub Field {
    if condition {
        if_true
    } else {
        if_false
    }
}
```

### 6. Structs and Generics

```rust
struct MerkleTree<let N: u32> {
    root: Field,
    path_elements: [Field; N],
}

fn verify<let LEVELS: u32>(
    tree: MerkleTree<LEVELS>,
    leaf: Field,
    indices: [u1; LEVELS],
) {
    // Generic over tree depth
}

fn main() {
    let tree = MerkleTree {
        root: 0,
        path_elements: [0; 20],
    };
    verify(tree, 0, [0; 20]);
}
```

## Noir vs Circom 2

| Feature | Noir | Circom 2 |
|---------|------|----------|
| Syntax | Rust-like | DSL |
| Constraint model | ACIR (abstract) | R1CS |
| Backends | PLONK, Honk | Groth16, PLONK, FFLONK |
| Dynamic logic | Native (if/for) | Compile-time only |
| Debugging | Rust debugging tools | circom_tester |
| Maturity | Medium (v0.30+) | High (v2.1+) |
| Ecosystem | Aztec, nargo | snarkjs, circomlib |

## Noir Workflow

```bash
# Create project
nargo new my_project
cd my_project

# Write circuit in src/main.nr

# Check circuit (compiles to ACIR)
nargo check

# Generate Prover.toml template
nargo check

# Execute witness
nargo execute

# Generate proof
nargo prove

# Verify proof
nargo verify

# Generate Solidity verifier
nargo codegen-verifier
```

## Common Pitfalls

1. **Mutable references:** Noir uses let mut; mutations are tracked in constraints
2. **Field arithmetic:** All numbers are field elements; no integer overflow semantics
3. **Public inputs:** Marked with `pub` keyword in main() parameters
4. **No randomness in circuit:** Randomness must be provided as witness input
5. **For loop bounds:** Must be compile-time constants in Noir (unlike Circom which requires template parameters)
