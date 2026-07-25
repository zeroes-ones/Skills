## 3. Decision Tree: FHE Scheme Selection

FHE scheme choice depends on the computation type. Wrong scheme = silent correctness failure or $500K+ calculation errors.

```
┌── FHE Scheme Selection ────────────────────────────────────────┐
│                                                                 │
│  What are you computing on encrypted data?                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Bitwise operations (comparisons, branching)?               │  │
│  │  └─► TFHE (Concrete/OpenFHE) — ~50ms/op, programmable     │  │
│  │     bootstrapping at each gate, latency-optimized          │  │
│  │                                                           │  │
│  │ Approximate real numbers (ML inference, stats)?            │  │
│  │  └─► CKKS (SEAL/OpenFHE) — SIMD batch (up to 32K slots),  │  │
│  │     approximate arithmetic, rescaling after each mult      │  │
│  │     ⚠ NEVER use for exact equality or integer division     │  │
│  │                                                           │  │
│  │ Exact integer arithmetic (financial, voting)?              │  │
│  │  ├─ BGV (HElib/OpenFHE) — exact integers, modulus chain    │  │
│  │  │  for level management, SIMD packing via CRT             │  │
│  │  └─ BFV (SEAL/OpenFHE) — exact integers, scale-invariant,  │  │
│  │     simpler noise management, good for small integers      │  │
│  │                                                           │  │
│  │ Multi-scheme pipeline (pre-process + compute)?             │  │
│  │  └─► HEIR compiler — IR-based, supports TFHE→CKKS→BGV      │  │
│  │     lowering, automatic scheme selection per operation     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Scheme comparison matrix:                                       │
│  ┌──────────┬──────────┬──────────┬─────────┬──────────────┐    │
│  │ Scheme   │ Data Type│ SIMD     │ Bootstr │ Best For      │    │
│  ├──────────┼──────────┼──────────┼─────────┼──────────────┤    │
│  │ TFHE     │ Bits     │ No       │ Gate-lvl│ Comparisons   │    │
│  │ CKKS     │ Complex  │ 32K slot │ Level   │ ML inference  │    │
│  │ BGV      │ Integers │ CRT pack │ Mod-sw  │ Exact arith   │    │
│  │ BFV      │ Integers │ CRT pack │ Scale   │ Fixed-point   │    │
│  └──────────┴──────────┴──────────┴─────────┴──────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

**CKKS example (SEAL C++):**
```cpp
// Microsoft SEAL: Encrypted logistic regression inference
EncryptionParameters parms(scheme_type::ckks);
size_t poly_modulus_degree = 32768;  // 2^15 for 128-bit security
parms.set_poly_modulus_degree(poly_modulus_degree);
parms.set_coeff_modulus(CoeffModulus::Create(poly_modulus_degree, {60, 40, 40, 60}));
SEALContext context(parms);

// Pack 8192 features into one ciphertext via SIMD
Plaintext weights;
encoder.encode(weight_vector, scale, weights);
Ciphertext encrypted_result;
evaluator.multiply_plain(encrypted_input, weights, encrypted_result);
evaluator.relinearize_inplace(encrypted_result, relin_keys);
evaluator.rescale_to_next_inplace(encrypted_result);  // ⚠ CRITICAL: rescale after each mult
```

**Bootstrapping budget tracking:**
```python
# Level budget analysis for CKKS pipeline
# Each multiplication consumes one level; bootstrapping resets levels
initial_levels = 12    # From coeff_modulus chain
ops = [
    ("multiply", 1), ("rotate", 0), ("multiply", 1),  # Level 12 → 10
    ("bootstrap", 0),                                   # Reset to top
    ("multiply", 1), ("multiply", 1),                   # Level 12 → 10
]
remaining = initial_levels
for op, cost in ops:
    if op == "bootstrap":
        remaining = initial_levels  # ⚠ Bootstrapping cost: ~10s per ciphertext
    else:
        remaining -= cost
    assert remaining >= 0, f"Level budget exhausted at {op} — $200K+ data corruption risk"
```

---
