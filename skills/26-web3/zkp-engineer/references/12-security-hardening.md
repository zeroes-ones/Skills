## 12. Security Hardening

### Constraint Completeness Audit

For every circuit, verify:

1. **Output signal audit:** Every `signal output` is reachable through `<==` or `===` from `signal input`
2. **Intermediate signal audit:** Every intermediate signal participates in at least one constraint path to output
3. **Boolean audit:** Every signal representing a bit has `x * (x - 1) === 0`
4. **Range audit:** Every public input has Num2Bits range check
5. **Division audit:** No division by unconstrained variable; handle zero case explicitly
6. **Nullifier audit:** Nullifier computation includes domain separator; contract prevents replay

### Signal Privacy

Signals marked `signal input` are private by default in Circom 2. However:
- Any signal passed as public input to `snarkjs groth16 prove` becomes public
- Intermediate signals derived from private inputs are private ONLY if they don't appear as public
- **Golden rule:** Only the final commitment/root/nullifier should be public
