# Recursive Proving & Folding Schemes

## Overview

Recursive proving enables verification of a proof inside another circuit, creating proof-of-proof chains. Folding schemes (Nova, SuperNova, Protostar) are more efficient alternatives that "fold" verification work across steps.

## Proof Composition vs Folding

| Property | Proof Composition | Nova Folding | SuperNova | ProtoStar |
|----------|-------------------|--------------|-----------|-----------|
| Per-step overhead | Full verification circuit (~20K constraints) | ~10K constraints | ~15K constraints | ~20K constraints |
| Supported programs | Uniform (same circuit each step) | Uniform (IVC) | Non-uniform (NIVC) | Non-uniform |
| Recursion depth | Limited (2-4 levels practical) | Unlimited | Unlimited | Unlimited |
| FFT per step | Yes | No | No | No |
| Maturity | High (Halo2, Plonky3) | Medium (Nova Scotia) | Low-Medium | Low |
| Trusted setup | Depends on system | Transparent | Transparent | Transparent |

## Nova: Incrementally Verifiable Computation (IVC)

Nova enables proving N sequential steps where each step is the SAME circuit.

### Architecture

```
Step 0: F(z_0, w_0) → z_1
Step 1: F(z_1, w_1) → z_2
...
Step N: F(z_N, w_N) → z_{N+1}

Nova folds all steps into one proof:
- Primary circuit: F (the step function)
- Secondary circuit: Verifies folding
- Prover: Runs all steps, folds claims
- Verifier: Checks final folded claim (O(1) work)
```

### Circom + Nova Scotia Example

```circom
// Step circuit for iterative hash chain
pragma circom 2.1.6;

include "circomlib/circuits/poseidon.circom";

// z_i is the current hash, z_next is the next hash
template HashStep() {
    signal input z_i;        // Current state
    signal input data;       // Input data for this step
    signal output z_next;    // Next state

    component hash = Poseidon(2);
    hash.inputs[0] <== z_i;
    hash.inputs[1] <== data;
    z_next <== hash.out;
}
```

```rust
// Nova Scotia Rust side (simplified)
use nova_scotia::{create_public_params, create_recursive_circuit, FileHandler};

// Step 1: Generate parameters
let pp = create_public_params::<HashStep>(r1cs_path.clone());

// Step 2: Create recursive circuit
let recursive_snark = create_recursive_circuit(
    FileHandler::new(&r1cs_path, &wasm_path),
    vec![initial_state],
    pp,
);

// Step 3: Generate proofs for each step
for (i, data) in inputs.iter().enumerate() {
    let proof = recursive_snark.prove_step(data);
    recursive_snark.verify_step(&proof);
}
```

## SuperNova: Non-uniform IVC (NIVC)

SuperNova extends Nova to support MULTIPLE different step circuits — useful for VMs with different opcodes.

```
Instead of: F(z_i, w_i) → z_{i+1} (one circuit)
SuperNova:  F_j(z_i, w_i) → z_{i+1} (j selects circuit)

Use case: zkVM with different opcode implementations
- ADD circuit: adds two registers
- MUL circuit: multiplies two registers
- SHA256 circuit: hashes memory region
- Each is a separate circuit; SuperNova folds across all
```

## ProtoStar

ProtoStar is designed for non-uniform computation with accumulator-based folding. It's the newest of the folding schemes and supports:
- Accumulator-based folding (like Nova)
- Multiple circuit types (like SuperNova)
- Better support for non-deterministic computation

## When to Use Each

### Nova
- Single, fixed step function
- Sequential computation (blockchain, rollup batch processing)
- Maximum efficiency per step

### SuperNova
- Multiple instruction types (VMs, interpreters)
- Branching program logic
- Different circuits per operation type

### ProtoStar
- Non-uniform computation with complex branching
- When Nova/SuperNova accumulator structure doesn't fit
- Cutting-edge research applications

### Traditional Proof Composition
- Simple 2-3 level recursion
- When using mature systems (Halo2, Plonky3)
- Don't want to adopt folding scheme dependencies

## Production Deployments

| System | Technique | Notes |
|--------|-----------|-------|
| Nova Scotia | Nova + Circom | Circom circuits folded with Nova |
| Zcash Orchard | Halo2 accumulation | Native recursion |
| Scroll zkEVM | Halo2 (fork) | Proof composition |
| Polygon Zero | Plonky3 recursion | STARK-like recursion |
| Risc Zero | STARK → Groth16 | Two-layer composition |
| SP1 | Plonky3 folding | Custom folding scheme |

## Folding Performance Benchmarks

| Scheme | Per-step proving (2^16 constraints) | Per-step proving (2^20 constraints) |
|--------|-------------------------------------|-------------------------------------|
| Nova (Nova Scotia) | ~0.8s | ~2.1s |
| Halo2 Native Recursion | ~3.2s | ~12.5s |
| Groth16 Composition | ~12s | ~180s |
| Plonky3 Recursion | ~0.5s | ~1.8s |
