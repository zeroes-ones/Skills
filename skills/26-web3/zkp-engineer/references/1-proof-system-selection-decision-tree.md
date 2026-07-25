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
