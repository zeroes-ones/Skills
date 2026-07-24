# Circom 2 Circuit Patterns

## Overview

Production-proven Circom 2 circuit patterns for common ZKP operations.

## Signal Types

| Type | Declaration | Constraint | Visibility |
|------|------------|------------|------------|
| Private input | `signal input x;` | Must constrain | Not in proof |
| Public input | `signal input x;` (passed at prove time) | Must constrain | Visible to verifier |
| Output | `signal output y;` | Must constrain (via <== or ===) | Visible to verifier |
| Intermediate | `signal z;` | Must constrain | Not in proof |
| Component output | `c.out` | Auto-constrained by component | Depends |

## Key Operators

- `<==` : Constrain AND assign (preferred for safety)
- `<--` : Assign ONLY (dangerous — use only for witness computation, must pair with `===`)
- `===` : Constrain equality between two signals

## Standard Patterns

### 1. Merkle Tree Inclusion Proof

```circom
pragma circom 2.1.6;

include "circomlib/circuits/poseidon.circom";

template MerkleProof(levels) {
    signal input leaf;
    signal input root;
    signal input pathElements[levels];
    signal input pathIndices[levels];

    component hashers[levels];
    signal levelHashes[levels + 1];
    levelHashes[0] <== leaf;

    for (var i = 0; i < levels; i++) {
        hashers[i] = Poseidon(2);
        hashers[i].inputs[0] <== pathIndices[i] == 0
            ? levelHashes[i]
            : pathElements[i];
        hashers[i].inputs[1] <== pathIndices[i] == 0
            ? pathElements[i]
            : levelHashes[i];
        levelHashes[i + 1] <== hashers[i].out;
    }

    root === levelHashes[levels];
}
```

### 2. Hash Preimage Proof

```circom
template HashPreimage() {
    signal input preimage;
    signal input hash;

    component poseidon = Poseidon(1);
    poseidon.inputs[0] <== preimage;
    hash === poseidon.out;
}
```

### 3. Ownership Proof (signature verification)

```circom
include "circomlib/circuits/eddsaposeidon.circom";

template OwnershipProof() {
    signal input message;
    signal input signature_R8x;
    signal input signature_R8y;
    signal input signature_S;
    signal input publicKey_Ax;
    signal input publicKey_Ay;

    component verifier = EdDSAPoseidonVerifier();
    verifier.enabled <== 1;
    verifier.Ax <== publicKey_Ax;
    verifier.Ay <== publicKey_Ay;
    verifier.R8x <== signature_R8x;
    verifier.R8y <== signature_R8y;
    verifier.S <== signature_S;
    verifier.M <== message;

    verifier.valid === 1;
}
```

### 4. Range Check (Multiple Methods)

```circom
include "circomlib/circuits/bitify.circom";
include "circomlib/circuits/comparators.circom";

// Method 1: Bit decomposition
template RangeCheckBits(nBits) {
    signal input value;
    component bits = Num2Bits(nBits);
    bits.in <== value;
    // Bits are now constrained 0/1, value < 2^nBits
}

// Method 2: LessThan comparator
template RangeCheckLessThan(nBits) {
    signal input value;
    signal input maxValue;
    component lt = LessThan(nBits);
    lt.in[0] <== value;
    lt.in[1] <== maxValue;
    lt.out === 1;  // value < maxValue
}
```

### 5. Nullifier Computation

```circom
template Nullifier() {
    signal input identitySecret;
    signal input externalNullifier;
    signal input scope;  // Domain separator
    signal output nullifierHash;

    component hash = Poseidon(3);
    hash.inputs[0] <== identitySecret;
    hash.inputs[1] <== externalNullifier;
    hash.inputs[2] <== scope;
    nullifierHash <== hash.out;
}
```

### 6. Conditional Logic (MUX)

```circom
template ConditionalTransfer() {
    signal input condition;    // 0 or 1
    signal input ifTrue;
    signal input ifFalse;
    signal output result;

    // Boolean constraint on condition
    condition * (condition - 1) === 0;

    // result = condition * ifTrue + (1 - condition) * ifFalse
    result <== condition * ifTrue + (1 - condition) * ifFalse;
}
```

## Circomlib Essentials

| Circuit | Use | Constraints |
|---------|-----|-------------|
| `Poseidon(n)` | n-to-1 hash | ~240 per hash |
| `MerkleProof(levels)` | Merkle inclusion | ~240 * levels |
| `EdDSAPoseidonVerifier()` | Signature verify | ~7500 |
| `Num2Bits(n)` | Decompose to n bits | n + 1 |
| `LessThan(n)` | Compare two n-bit values | ~2n |
| `IsZero()` | Check if signal is zero | 2 |
| `IsEqual()` | Check if two signals equal | 2 |
| `Multiplexor(n)` | Select from 2^n options | ~2^n |

## Performance Tips

1. **Minimize constraints:** Each `<==` generates a constraint. Combine operations where safe.
2. **Use `Num2Bits` sparingly:** Determines constraint count for range checks.
3. **Poseidon over MiMC:** Poseidon is more constraint-efficient.
4. **Pre-compute outside circuit:** Move heavy computation to witness generation.
5. **Use circom_tester for tests:** `npm install circom_tester` for Mocha-based testing.
