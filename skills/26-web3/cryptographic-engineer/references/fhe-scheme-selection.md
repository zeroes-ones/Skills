# FHE Scheme Selection — TFHE/CKKS/BGV/BFV Decision Matrix

## Selection Algorithm

```
1. Determine computation type:
   - Exact integer arithmetic → BGV or BFV
   - Approximate real/complex → CKKS
   - Bitwise/branching → TFHE

2. Determine throughput needs:
   - High throughput → CKKS with SIMD packing (32K slots)
   - Low latency (< 50ms) → TFHE with gate bootstrapping

3. Check noise budget:
   - Deep circuit (> 10 mults) → BGV with modulus switching or bootstrapping
   - Shallow circuit (< 10 mults) → BFV with scale-invariant noise
```

## Scheme Details

### TFHE (Torus FHE)
- **Primitive:** LWE/RLWE over torus (real numbers modulo 1)
- **Bootstrapping:** Programmable (PBS) — evaluates arbitrary LUT at each gate
- **Latency:** ~50ms per gate (dominated by bootstrapping)
- **Best for:** Comparisons, branching, decision trees, small lookup tables
- **Libraries:** Zama Concrete, OpenFHE (binfhe), TFHElib

### CKKS (Cheon-Kim-Kim-Song)
- **Primitive:** RLWE, approximate arithmetic on complex numbers
- **SIMD:** Up to 32,768 slots per ciphertext via canonical embedding
- **Rescaling:** After each multiplication to manage scale factor
- **Bootstrapping:** Refreshes ciphertext to top of modulus chain (~10s)
- **Best for:** ML inference, statistical computation, polynomial evaluation
- **⚠ WARNING:** Never use for equality checks or exact integer operations

### BGV (Brakerski-Gentry-Vaikuntanathan)
- **Primitive:** RLWE, exact integer arithmetic
- **Modulus switching:** Scale down after each multiplication
- **SIMD:** CRT packing for parallel integer operations
- **Best for:** Exact computation, financial calculations, voting systems

### BFV (Brakerski-Fan-Vercauteren)
- **Primitive:** RLWE, scale-invariant (no modulus switching)
- **Noise:** Grows linearly with depth, simpler management
- **Best for:** Small-depth circuits with small integer operands
- **Limitation:** Plaintext modulus must fit in 60 bits

## Performance Benchmarks (n=32768, 128-bit security)

| Operation | TFHE (Concrete) | CKKS (SEAL) | BGV (OpenFHE) | BFV (SEAL) |
|-----------|----------------|-------------|---------------|------------|
| Addition | 0.01ms | 0.05ms | 0.03ms | 0.04ms |
| Multiplication | N/A (via PBS) | 5ms | 8ms | 6ms |
| Bootstrapping | 50ms (PBS) | 10s | 15s | 20s |
| Rotation | N/A | 3ms | 4ms | 3ms |
| Ciphertext size | ~8KB | ~1MB | ~800KB | ~1MB |

## HEIR Compiler Pipeline

Google's HEIR uses MLIR to compile high-level encrypted computation:

```
[ High-level MLIR ] 
    → heir-scheme-lowering (TFHE/CKKS/BGV dialect selection)
    → heir-bootstrap-placement (automatic bootstrapping insertion)
    → heir-noise-analysis (budget verification)
    → heir-codegen (Concrete/SEAL/OpenFHE output)
```
