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
