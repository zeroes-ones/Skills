## 7. Decision Tree: Key Ceremony Design

```
┌── Key Ceremony Design ─────────────────────────────────────────┐
│                                                                │
│  What is the threat model for key material?                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ Treasury/custody ($100M+)?                               │    │
│  │  └─ HSM quorum (n-of-m) + Shamir backup + air-gapped    │    │
│  │     ceremony with video audit + tamper-evident seals     │    │
│  │                                                         │    │
│  │ Decentralized protocol (DAOs, bridges)?                  │    │
│  │  └─ MPC-based ceremony (no single point of compromise)  │    │
│  │     + Verifiable Secret Sharing (Feldman VSS)            │    │
│  │                                                         │    │
│  │ Enterprise PKI (short-lived keys < 90d)?                 │    │
│  │  └─ HSM-backed CA with offline root + online issuing    │    │
│  │     + TEE for key protection during signing              │    │
│  │                                                         │    │
│  │ Crypto exchange wallet?                                  │    │
│  │  └─ Threshold ECDSA (GG20) with geographic distribution │    │
│  │     + Proactive refresh every 30-90 days                 │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                │
│  Ceremony checklist (air-gapped HSM ceremony):                  │
│  1. Entropy sourcing: hardware RNG + dice rolls (mix via KDF)  │
│  2. Shamir splitting: t-of-n, verifiable shares (Feldman)       │
│  3. Share distribution: tamper-evident envelopes, chain-of-custody│
│  4. Ceremony recording: dual video, witness log, GPS timestamp │
│  5. Verification: reconstruct pubkey from each subset, test sig│
│  6. Share custody: safe deposit boxes, geographic distribution │
│  7. Emergency recovery: documented procedure, quorum call-list  │
└────────────────────────────────────────────────────────────────┘
```

**Feldman Verifiable Secret Sharing (Rust):**
```rust
// Verifiable Shamir sharing: shares can be verified without reconstruction
use curv::elliptic::curves::{Secp256k1, Point};
use curv::BigInt;

struct FeldmanVSS {
    n: usize,             // Total shares
    t: usize,             // Threshold
    generator: Point<Secp256k1>,
}

impl FeldmanVSS {
    fn split(&self, secret: &BigInt) -> (Vec<BigInt>, Vec<Point<Secp256k1>>) {
        // f(x) = secret + a1*x + a2*x^2 + ... + at*x^t mod q
        let coeffs = self.generate_polynomial(secret, self.t);
        let shares: Vec<_> = (1..=self.n)
            .map(|i| self.evaluate(&coeffs, BigInt::from(i)))
            .collect();
        // Commitments: A_j = g^a_j for verification
        let commitments: Vec<_> = coeffs.iter()
            .map(|c| self.generator.clone() * c)
            .collect();
        (shares, commitments)
    }

    fn verify_share(&self, share: &BigInt, index: usize,
                    commitments: &[Point<Secp256k1>]) -> bool {
        let lhs = self.generator.clone() * share;
        let mut rhs = commitments[0].clone();
        let x = BigInt::from(index + 1);
        for j in 1..commitments.len() {
            rhs = rhs + commitments[j].clone() * x.pow(j as u32);
        }
        lhs == rhs  // g^f(i) == prod A_j^{i^j}
    }
}
```

---
