## 8. MPC Implementation Patterns

### 8.1 Shamir Secret Sharing (Python reference)

```python
from secrets import randbelow
from dataclasses import dataclass

# Prime field (secp256k1 order as example)
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

@dataclass
class ShamirShare:
    x: int  # Evaluation point
    y: int  # f(x) mod P

def share_secret(secret: int, t: int, n: int) -> list[ShamirShare]:
    """t-of-n Shamir sharing: create n shares, any t can reconstruct"""
    coeffs = [secret] + [randbelow(P) for _ in range(t - 1)]
    shares = []
    for i in range(1, n + 1):
        y = sum(c * pow(i, j, P) for j, c in enumerate(coeffs)) % P
        shares.append(ShamirShare(i, y))
    return shares

def reconstruct(shares: list[ShamirShare]) -> int:
    """Lagrange interpolation at x=0 to recover secret"""
    secret = 0
    for i, si in enumerate(shares):
        num, den = 1, 1
        for j, sj in enumerate(shares):
            if i != j:
                num = num * (0 - sj.x) % P
                den = den * (si.x - sj.x) % P
        lagrange_coeff = num * pow(den, -1, P) % P
        secret = (secret + si.y * lagrange_coeff) % P
    return secret
```

### 8.2 Garbled Circuits with Oblivious Transfer (Rust with mpz)

```rust
// Garbled circuit evaluation: Garbler encrypts circuit, Evaluator evaluates
// Uses half-gates optimization (Zahur-Rosulek-Evans, Eurocrypt 2015)

use mpz_core::{Block, GarbledCircuit};
use mpz_ot::chou_orlandi::{Receiver as OTReceiver, Sender as OTSender};

struct GarbledAndGate {
    // Half-gate: 2 ciphertexts per AND gate (optimal)
    garbler_half: [Block; 2],
    evaluator_half: [Block; 2],
}

fn garble_and(a0: Block, a1: Block, b0: Block, b1: Block,
              delta: Block) -> GarbledAndGate {
    // Free-XOR: delta = global offset for wire label encoding
    // Label encoding: W^0 = w, W^1 = w XOR delta
    let t_g = H(a0) ^ H(a0 ^ delta) ^ (b0 & delta);  // Garbler half-gate
    let t_e = H(b0) ^ H(b0 ^ delta) ^ a0;              // Evaluator half-gate
    GarbledAndGate {
        garbler_half: [t_g, t_g ^ a0],
        evaluator_half: [t_e, t_e ^ b0],
    }
}
// Total communication: 2 * 128 bits per AND gate (half-gates)
```

### 8.3 MPC Security Hardening Checklist
- [ ] Constant-time comparisons in GMW inner loop (no early exit on branch)
- [ ] Randomize gate evaluation order per execution (defeat timing correlation)
- [ ] Use fresh OT correlations per session (never reuse OT precomputation)
- [ ] Verify zero-knowledge proofs in SPDZ preprocessing phase
- [ ] Rate-limit corrupt party detection (identifiable aborts leak correlation info)
- [ ] Network padding: uniform message sizes regardless of computation path

---
