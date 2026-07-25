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
