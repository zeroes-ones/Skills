## 10. Circuit Testing & Auditing

### Testing Checklist

1. **Boundary tests:** Test with min/max values, zero inputs, field modulus - 1
2. **Constraint coverage:** Every `===` and `<==` must be exercised by at least one test
3. **Negative tests:** Generate invalid witnesses and verify they fail proof generation
4. **Witness malleability:** Test that changing any unconstrained signal changes the witness but not the proof validity
5. **Fuzz testing:** Use circom_tester or noir-tester to fuzz input ranges
6. **Differential testing:** Compare Circom output against reference implementation (Python/TypeScript)
7. **Gas profiling:** Deploy verifier to testnet, measure actual gas with various inputs

### Auditing Anti-Patterns

| Pattern | Severity | Detection |
|---------|----------|-----------|
| `<--` without corresponding `===` | CRITICAL | Grep for `<--` in circuit |
| Signal declared `output` but never constrained | CRITICAL | Review all output signals |
| Missing Boolean constraint on bit signals | HIGH | Check `x*(x-1)===0` for all bits |
| Public input without range check | HIGH | Audit all public signals |
| Division or modulo in constraints | MEDIUM | Check for `/` and `%` in constraints |
| Signal re-assignment after `<==` | MEDIUM | Check for duplicate signal assignments |
