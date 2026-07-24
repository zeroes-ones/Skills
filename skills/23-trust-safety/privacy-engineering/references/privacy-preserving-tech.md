# Privacy-Preserving Technologies

Decision framework and readiness assessment for homomorphic
encryption (HE), secure multi-party computation (SMPC), zero-knowledge
proofs (ZKP), federated learning, and private set intersection (PSI).

## Technology Selection Decision Tree

```
Do you need to compute on data you cannot see in plaintext?
  YES (data stays encrypted, you derive results without decryption)
    |-- Small computation (sum, average, count)?
    |    -> Partially Homomorphic Encryption (PHE) — Fast, practical
    |       RSA (multiplicative), Paillier (additive), ElGamal (multiplicative)
    |-- More complex but limited depth?
    |    -> Somewhat Homomorphic Encryption (SHE) — Moderate performance
    |       BGV, BFV schemes: limited number of operations of both types
    |-- Arbitrary computation on encrypted data?
         -> Fully Homomorphic Encryption (FHE) — 1000x-1Mx slower than plaintext
            CKKS (approximate arithmetic), TFHE (fast boolean), BGV/BFV (integer)
            Production readiness: Limited (2024). Use for low-throughput, high-value use cases
  NO (you can see the data, but want privacy against others)
    |-- Multiple parties compute together without sharing inputs?
    |    -> Secure Multi-Party Computation (SMPC)
    |       Shamir Secret Sharing, Garbled Circuits, Oblivious Transfer
    |       Use: multi-hospital medical research, financial fraud detection across banks
    |       Overhead: 10x-1000x communication overhead vs plaintext computation
    |-- Prove an attribute without revealing the value?
    |    -> Zero-Knowledge Proofs (ZKP)
    |       zk-SNARKs (constant proof size, trusted setup), zk-STARKs (no trusted setup, larger)
    |       Use: age verification (I'm over 18), identity (I'm on this allowlist), KYC (I passed)
    |       Bulletproofs: no trusted setup, linear verification — good for range proofs
    |-- Find common elements in two private datasets?
    |    -> Private Set Intersection (PSI)
    |       Use: contact discovery (which of my contacts use app X?), breached password check
    |       Protocols: Diffie-Hellman based (semi-honest), OT-based (malicious security)
    |-- Train ML without centralizing user data?
         -> Federated Learning (FL)
            On-device training -> share model gradients (not raw data) -> aggregate on server
            Combine with DP: add noise to gradients before sending (DP-FL)
            Risk: gradients can leak training data (gradient inversion attacks). DP mitigates this.

Alternative (simpler, often sufficient):
  -> On-device processing: all data stays local, only insights sent to server
     Use: keyboard suggestions, health alerts, content recommendations
     No raw data ever leaves the device — maximum privacy by architecture
```

## HE Readiness Assessment

| Question | Yes | No | Notes |
|----------|-----|----|-------|
| Is plaintext access to data impossible/precluded? | Consider HE | Use standard encryption | HE is expensive — only worth it when you truly cannot decrypt |
| Is the computation small (<100 operations per query)? | PHE/SHE viable | FHE may be too slow | Complexity drives overhead |
| Is latency budget >10 seconds per query? | HE viable | HE probably unsuitable | CKKS on 10K elements can take minutes |
| Is the dataset >100K records? | HE bottlenecked | Less concern | HE operates on individual ciphertexts — no bulk efficiency |
| Do you have dedicated hardware (GPU/FPGA)? | HE more viable | CPU-only very slow | GPU acceleration improves FHE 10-100x |

## ZKP Use Cases by Sector

| Sector | ZKP Application | Protocol |
|--------|----------------|----------|
| Identity | Prove age > 18 without revealing birthdate | Bulletproofs (range proof) |
| Finance | Prove solvency (assets > liabilities) without revealing balances | zk-SNARKs |
| Healthcare | Prove vaccination status without revealing medical record | BBS+ signatures |
| Supply Chain | Prove product origin without revealing full supply chain | zk-STARKs |
| Access Control | Prove membership in allowlist without revealing identity | Merkle proof + ZKP |

## Federated Learning Architecture

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Device 1│  │ Device 2│  │ Device N│   On-device training
│ (local  │  │ (local  │  │ (local  │   with local data only
│  data)  │  │  data)  │  │  data)  │
└────┬────┘  └────┬────┘  └────┬────┘
     │ Encrypted  │            │
     │ gradients  │            │
     ▼            ▼            ▼
┌────────────────────────────────────┐
│     Secure Aggregation Server      │  Aggregates encrypted
│     (federated averaging)          │  gradients without
│  DP noise added to aggregated      │  seeing individual
│  model before distribution         │  contributions
└────────────────────────────────────┘
```
