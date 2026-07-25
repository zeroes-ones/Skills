## 4. Range Check Strategy (Decision Tree)

```
┌───────────────────────────────────────────────────────────────┐
│               RANGE CHECK STRATEGY DECISION TREE               │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Range < 256 (8 bits)? ──YES──> Bit decomposition (cheapest)  │
│       │                                                       │
│      NO                                                       │
│       │                                                       │
│  Range < 2^64? ──YES──> Can use lookup table (Halo2)          │
│       │               or bit decomposition (Circom)            │
│      NO                                                       │
│       │                                                       │
│  Need efficient range check in Circom?                        │
│       │                                                       │
│      YES ──> Use circomlib Num2Bits(n) or LessThan(n)         │
│       │                                                       │
│  Using Halo2? ──YES──> Use lookup table (single constraint)   │
│       │                                                       │
│      NO                                                       │
│       │                                                       │
│  Need zero-knowledge range proof for arbitrary range?         │
│       │                                                       │
│      YES ──> Bulletproofs or inner product arguments          │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Range Check Techniques

| Technique | Constraints per check | Language | Notes |
|-----------|----------------------|----------|-------|
| Bit decomposition (Num2Bits) | 254 for 254-bit | Circom 2 | Most common, linear in bit count |
| Lookup table | 1 constraint | Halo2 | O(1) per check, ideal for frequent ops |
| LessThan comparator | ~253 constraints | Circom 2 | circomlib LessThan(n) |
| Windowed decomposition | ~32-64 per limb | Circom 2 | Uses large limbs, fewer constraints |
| Bulletproofs | O(log n) | Standalone | Efficient for arbitrary range |

**Circom 2 range check with circomlib:**

```circom
include "circomlib/circuits/comparators.circom";
include "circomlib/circuits/bitify.circom";

template RangeCheckExample() {
    signal input value;
    signal input maxValue;

    // Method 1: LessThan(n) comparator
    component lt = LessThan(254);
    lt.in[0] <== value;
    lt.in[1] <== maxValue;
    lt.out === 1;  // value < maxValue

    // Method 2: Bit decomposition (also proves value is non-negative)
    component bits = Num2Bits(254);
    bits.in <== value;

    // Method 3: Combined — check value in [0, maxValue)
    component range = Num2Bits(254);
    range.in <== value;
    // Now bits[0..] are individually constrained to 0/1
    // value is proven to be in [0, 2^254-1]
}
```

**Halo2 range check with lookup table:**

```rust
// Halo2: Efficient range check using lookup table
// In configure():
meta.lookup_any("range check", |meta| {
    let value = meta.query_advice(advice_col, Rotation::cur());
    let range = meta.query_fixed(table_col, Rotation::cur());
    vec![(value, range)]
});

// Load table with values 0..RANGE (typically 0..2^16)
// Single constraint per range check — extremely efficient
```
