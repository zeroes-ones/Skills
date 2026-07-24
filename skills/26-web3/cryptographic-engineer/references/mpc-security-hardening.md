# MPC Security Hardening — Side Channels, Malicious Majority

## Side-Channel Attack Vectors in MPC

### 1. Timing Side Channels
**Attack:** Attacker measures wall-clock time of circuit evaluation to infer circuit depth/inputs.
**Mitigation:**
- Uniform circuit padding to fixed depth
- Random gate execution order (non-data-dependent)
- Fixed-time comparison primitives

### 2. Memory Access Patterns
**Attack:** Cache-timing through shared memory (GMW evaluation, OT extension tables).
**Mitigation:**
- Data-oblivious memory access (linear scan instead of indexed access)
- Constant-time OT extension (access all rows, mask result)
- Prefetch all data before computation

### 3. Network Traffic Analysis
**Attack:** Message sizes correlate with computation path (e.g., conditional output size).
**Mitigation:**
- Uniform message padding to circuit maximum output size
- Random inter-message delays (defeat timing correlation)
- Dummy messages during idle rounds

## Malicious Majority Protocol Hardening

### SPDZ (MASCOT) Security Properties
- **MACs:** Each secret share carries information-theoretic MAC
- **Sacrifice:** Open random triple to verify correctness before using
- **Input:** Prove knowledge via ZK proof of plaintext knowledge
- **Output:** Verify MAC on opened value before accepting

### Common Implementation Mistakes
1. **Reusing OT correlations:** Fresh base OTs per session for OT extension
2. **Insufficient statistical security:** SPDZ MAC field size (default: 40 bits = 1/2^40)
3. **Skipping sacrifice:** Verifying multiplication triples is mandatory for malicious security
4. **Non-randomized circuit:** Deterministic circuit can be probed across sessions

## Identifiable Abort Handling

When a corrupt party is detected:
1. **Log all messages** from that round (non-repudiation)
2. **Isolate the party** from subsequent rounds
3. **Do NOT retry** — retry leaks additional information
4. **Escalate** according to protocol governance (on-chain slashing, etc.)

## Formal Verification Considerations

Tools for protocol-level verification:
- **ProVerif:** Symbolic analysis, Dolev-Yao attacker model
- **Tamarin Prover:** Equational theories, stateful protocols
- **EasyCrypt:** Code-level proofs, probabilistic relational Hoare logic
- **SSProve:** MPC-specific, security against malicious adversaries
