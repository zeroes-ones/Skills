## 9. FHE Implementation Patterns

### 9.1 TFHE Programmable Bootstrapping (Zama Concrete)

```python
# Concrete: TFHE with programmable bootstrapping
# Each bootstrapping = refresh noise + evaluate lookup table (PBS)
from concrete import fhe
import numpy as np

@fhe.compiler({"x": "encrypted", "y": "encrypted"})
def encrypted_min(x, y):
    """Compute min(x, y) with PBS at each comparison"""
    # PBS evaluates: f(x-y) where f is a sign function
    # Doing min with one PBS: min(x,y) = x if x <= y else y
    return fhe.min(x, y)  # Single PBS for the sign test

# Configuration for 128-bit security
configuration = fhe.Configuration(
    parameter_selection_strategy=fhe.ParameterSelectionStrategy.MULTI,
    show_graph=True,  # Visualize PBS operations in circuit
)

inputset = [(np.random.randint(0, 100, size=()) for _ in range(2)) for _ in range(1000)]
compiler = fhe.Compiler(encrypted_min, {"x": "encrypted", "y": "encrypted"})
circuit = compiler.compile(inputset, configuration)

# Circuit stats: bootstrappings, key sizes, noise budget
print(f"PBS count: {circuit.programmable_bootstrap_count}")
print(f"Key size: {circuit.size_of_secret_keys // 1024} KB")
```

### 9.2 CKKS Packing Strategy with SEAL

```cpp
// Optimal packing: encode multiple values into one ciphertext via SIMD
// For logistic regression: pack feature vectors into single ciphertext
std::vector<double> features(8192);
encoder.encode(features, scale, plain_features);

// ⚠ CRITICAL: Never compare CKKS values for equality
// WRONG (silent failure, $500K+ error):
//   if (enc_a == enc_b) { ... }  // CKKS is APPROXIMATE

// CORRECT: Compare thresholded difference
Ciphertext diff;
evaluator.sub(enc_a, enc_b, diff);
Plaintext threshold;
encoder.encode(std::vector<double>(N, 1e-6), scale, threshold);
// Bootstrapping-intensive comparison — consider BFV/BGV instead
```

### 9.3 HEIR Compiler Pipeline (Google)

```python
# HEIR: MLIR-based FHE compiler — automatic scheme selection
# heir-opt --heir-scheme-lowering lower.mlir > lower_tfhe.mlir

# Input: High-level MLIR describing encrypted computation
# heir-opt lowers through:
#   1. heir-scheme-lowering: FHE dialect -> TFHE/CKKS/BGV IR
#   2. heir-bootstrap-placement: Insert bootstrapping operations
#   3. heir-noise-analysis: Verify budget is not exceeded
#   4. heir-codegen: Emit OpenFHE/Concrete/SEAL runtime code
```

**FHE performance optimization checklist:**
- [ ] Pack independent values into SIMD slots (32K parallelism for CKKS)
- [ ] Minimize bootstrap calls (< 50 per circuit for latency < 500ms)
- [ ] Use leveled operations when possible (no bootstrap between linear layers)
- [ ] Precompute plaintext constants as Plaintext (not encrypted)
- [ ] Batch rotation keys: one key per rotation index, share across circuits

---
