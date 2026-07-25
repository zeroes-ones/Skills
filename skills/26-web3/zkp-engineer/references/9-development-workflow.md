## 9. Development Workflow

### Standard Circom 2 Workflow

```bash
# 1. Compile circuit to R1CS
circom circuit.circom --r1cs --wasm --sym -o build/

# 2. View circuit info
snarkjs r1cs info build/circuit.r1cs
# Output: constraints, signals, wires, labels

# 3. Generate witness (test inputs)
node build/circuit_js/generate_witness.js build/circuit_js/circuit.wasm input.json witness.wtns

# 4. Powers of Tau (Phase 1 — download existing)
wget https://hermez.s3-eu-west-1.amazonaws.com/powersOfTau28_hez_final_21.ptau

# 5. Groth16 setup (Phase 2)
snarkjs groth16 setup build/circuit.r1cs powersOfTau28_hez_final_21.ptau circuit_0000.zkey
snarkjs zkey contribute circuit_0000.zkey circuit_final.zkey --name="Dev"

# 6. Export verification key
snarkjs zkey export verificationkey circuit_final.zkey verification_key.json

# 7. Generate proof
snarkjs groth16 prove circuit_final.zkey witness.wtns proof.json public.json

# 8. Verify proof
snarkjs groth16 verify verification_key.json public.json proof.json

# 9. Export Solidity verifier
snarkjs zkey export solidityverifier circuit_final.zkey Verifier.sol

# 10. Generate calldata for on-chain verification
snarkjs zkey export soliditycalldata public.json proof.json
```

### Noir Workflow

```bash
# 1. Create project
nargo new my_circuit
cd my_circuit

# 2. Write circuit in src/main.nr

# 3. Compile & generate Prover.toml template
nargo check
nargo execute

# 4. Generate proof
nargo prove

# 5. Verify proof
nargo verify

# 6. Generate Solidity verifier
nargo codegen-verifier

# 7. Generate contract for on-chain use
bb write_vk -b target/my_circuit.json -o target/vk
bb contract
```

### Halo2 Workflow

```rust
// Standard Halo2 circuit pattern
#[derive(Clone)]
struct MyCircuitConfig {
    advice: Column<Advice>,
    instance: Column<Instance>,
    selector: Selector,
    lookup_table: TableColumn,
}

impl Circuit<Fr> for MyCircuit {
    type Config = MyCircuitConfig;
    type FloorPlanner = SimpleFloorPlanner;

    fn configure(meta: &mut ConstraintSystem<Fr>) -> Self::Config {
        let advice = meta.advice_column();
        let instance = meta.instance_column();
        let selector = meta.selector();
        let lookup_table = meta.lookup_table_column();

        meta.create_gate("custom gate", |meta| {
            let s = meta.query_selector(selector);
            let a = meta.query_advice(advice, Rotation::cur());
            let b = meta.query_advice(advice, Rotation::next());
            vec![s * (a * b - a - b)]
        });

        meta.lookup("range check", |meta| {
            let value = meta.query_advice(advice, Rotation::cur());
            let range = meta.query_fixed(lookup_table, Rotation::cur());
            vec![(value, range)]
        });

        MyCircuitConfig { advice, instance, selector, lookup_table }
    }

    fn synthesize(&self, config: Self::Config, layouter: impl Layouter<Fr>) -> Result<(), Error> {
        // Witness assignment and constraint region layout
        Ok(())
    }
}
```
