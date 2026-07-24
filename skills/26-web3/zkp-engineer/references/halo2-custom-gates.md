# Halo2 Custom Gates & Lookup Tables

## Overview

Halo2 is a Rust library for ZKP circuit construction with plonkish arithmetization. Unlike Circom 2 (R1CS constraints), Halo2 supports custom gates and lookup tables.

## Architecture

### Core Components

- **Column types:** Advice, Instance, Fixed, Selector, TableColumn
- **Regions:** Grouped constraint assignment blocks
- **Layouter:** Assigns witness values and synthesizes constraints
- **Configure:** Define constraint system (gates, lookups)
- **Synthesize:** Assign witnesses and lay out regions

## Custom Gates

### Standard Gate Pattern

```rust
use halo2_proofs::{
    circuit::{Layouter, SimpleFloorPlanner},
    plonk::{Circuit, ConstraintSystem, Error},
    poly::Rotation,
};

#[derive(Clone)]
struct MyConfig {
    a: Column<Advice>,
    b: Column<Advice>,
    c: Column<Advice>,
    selector: Selector,
}

impl Circuit<Fr> for MyCircuit {
    type Config = MyConfig;
    type FloorPlanner = SimpleFloorPlanner;

    fn configure(meta: &mut ConstraintSystem<Fr>) -> Self::Config {
        let a = meta.advice_column();
        let b = meta.advice_column();
        let c = meta.advice_column();
        let selector = meta.selector();

        // Custom gate: s * (a * b - c) = 0
        meta.create_gate("multiplication gate", |meta| {
            let s = meta.query_selector(selector);
            let a = meta.query_advice(a, Rotation::cur());
            let b = meta.query_advice(b, Rotation::cur());
            let c = meta.query_advice(c, Rotation::cur());
            vec![s * (a * b - c)]
        });

        MyConfig { a, b, c, selector }
    }
}
```

### Fibonacci Gate (Cross-Row Constraint)

```rust
// Custom gate: a_{i+2} = a_{i+1} + a_i
meta.create_gate("fibonacci", |meta| {
    let s = meta.query_selector(selector);
    let a_cur = meta.query_advice(a, Rotation::cur());
    let a_next = meta.query_advice(a, Rotation::next());
    let a_next_next = meta.query_advice(a, Rotation(2));
    vec![s * (a_cur + a_next - a_next_next)]
});
```

## Lookup Tables

Lookup tables are Halo2's killer feature — they allow efficient range checks, hash functions, and arbitrary table lookups in a single constraint.

### Range Check via Lookup

```rust
fn configure(meta: &mut ConstraintSystem<Fr>) -> Self::Config {
    let value = meta.advice_column();
    let table = meta.lookup_table_column();

    // Load table with values 0..RANGE during synthesis
    // Each lookup costs 1 constraint regardless of range size
    meta.lookup("range check", |meta| {
        let v = meta.query_advice(value, Rotation::cur());
        let t = meta.query_fixed(table, Rotation::cur());
        vec![(v, t)]
    });

    MyConfig { value, table }
}

fn synthesize(
    &self,
    config: Self::Config,
    mut layouter: impl Layouter<Fr>,
) -> Result<(), Error> {
    // Load lookup table with values 0..2^16
    layouter.assign_table(
        || "range table",
        |mut table| {
            for i in 0..(1u64 << 16) {
                table.assign_cell(
                    || "value",
                    config.table,
                    i as usize,
                    || Value::known(Fr::from(i)),
                )?;
            }
            Ok(())
        },
    )?;
    Ok(())
}
```

### SHA256 via Lookup Table

The standard approach for SHA256 in Halo2 uses spread tables for efficient bitwise operations:

```rust
// Halo2 SHA256 uses:
// 1. Spread tables (16-bit → 32-bit spread for XOR, AND, NOT)
// 2. σ0, σ1, Σ0, Σ1 via custom gates
// 3. Maj, Ch via lookup-assisted custom gates
// Reference: zcash/halo2/halo2_gadgets/src/sha256.rs
```

## Region Layout

Regions group related constraints and witness assignments:

```rust
fn synthesize(
    &self,
    config: Self::Config,
    mut layouter: impl Layouter<Fr>,
) -> Result<(), Error> {
    layouter.assign_region(
        || "adder region",
        |mut region| {
            // Enable selector at offset 0
            config.selector.enable(&mut region, 0)?;

            // Assign advice columns
            region.assign_advice(
                || "a",
                config.a,
                0,  // offset
                || Value::known(Fr::from(3)),
            )?;

            region.assign_advice(
                || "b",
                config.b,
                0,
                || Value::known(Fr::from(5)),
            )?;

            // Result column — will be constrained to a * b
            region.assign_advice(
                || "result",
                config.c,
                0,
                || Value::known(Fr::from(15)),
            )?;
            Ok(())
        },
    )
}
```

## Performance Considerations

| Gadget | Constraints (Halo2) | Constraints (Circom R1CS) | Notes |
|--------|--------------------|-----------------------------|-------|
| Range check (16-bit) | 1 (lookup) | 17 (Num2Bits) | Halo2 17x more efficient |
| SHA256 | ~21K | ~25K | Both use table-assisted |
| Keccak256 | ~180K | ~250K | Heavy bitwise ops |
| Poseidon | ~240 | ~240 | Same efficiency |
| ECDSA verify | ~30K | ~35K | Comparable |

## When to Use Halo2 Custom Gates

- **Yes:** Range checks, SHA256, Keccak, bitwise operations, any function naturally expressed as table lookup
- **No:** Simple arithmetic (R1CS is simpler), small circuits (<1K constraints), when team has no Rust experience
