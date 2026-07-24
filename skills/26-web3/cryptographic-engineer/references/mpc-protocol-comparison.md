# MPC Protocol Comparison — MP-SPDZ, Shamir, Garbled Circuits

## Protocol Taxonomy

### By Adversary Model
| Protocol Family | Corruption Threshold | Security Model | Setup Assumption | Best For |
|----------------|---------------------|----------------|------------------|----------|
| Replicated Secret Sharing (3PC) | t=1, n=3 | Semi-honest/Malicious | None | Low-latency, 3-party |
| Shamir (BGW) | t < n/2 | Semi-honest | None | Honest majority, arithmetic |
| SPDZ (MASCOT) | t < n | Malicious | CRS | Dishonest majority |
| SPDZ2k | t < n | Malicious | CRS | Dishonest majority + k-bit fields |
| Yao (Garbled Circuits) | t=1, n=2 | Semi-honest/Malicious | OT | Boolean circuits, 2-party |
| GMW | t=1, n=2..m | Semi-honest | OT | Boolean circuits, multi-party |

### Communication Complexity
| Protocol | Online Rounds | Online Communication | Preprocessing |
|----------|--------------|---------------------|---------------|
| Replicated 3PC | 1 per AND | O(n * |C|) | None |
| SPDZ (MASCOT) | 1 per mult | O(n * |C|) | O(n^2 * |C|) OT correlations |
| Yao (half-gates) | 2 (constant) | O(|C| * kappa) | O(|C|) OTs |
| Shamir BGW | O(depth) | O(n * depth) | None |

## MP-SPDZ DSL Reference

MP-SPDZ supports 40+ protocol backends through a Python-like DSL:

```python
# Secure multi-party sorting with malicious security
from Compiler import sorting

n = sint.get_input_from(0)  # Array size (secret)
arr = [sint.get_input_from(i % 2) for i in range(n.reveal())]
sorted_arr = sorting.sort(arr)
print_ln("Sorted: %s", sorted_arr.reveal())
```

### Backend Selection Guide
- `replicated-ring.sh` — 3-party semi-honest, fastest
- `malicious-rep-ring.sh` — 3-party malicious
- `mascot-party.x` — 2-party malicious, OT-based preprocessing
- `semi-party.x` — 2-party semi-honest, OT-based
- `shamir-party.x` — N-party honest majority, Shamir-based

## Garbled Circuits: Half-Gates Optimization

Zahur-Rosulek-Evans (Eurocrypt 2015): reduces each AND gate to **2 ciphertexts** (optimal).

```
Garbler (Alice):
  - Generates 2 random wire labels per wire (w^0, w^1), w^1 = w^0 XOR Delta
  - For each AND gate: computes 2 ciphertexts
  - Sends garbled circuit + input labels for Alice's bits

Evaluator (Bob):
  - Receives Bob's input labels via OT (oblivious transfer)
  - Evaluates gate-by-gate: decrypts one ciphertext per gate
  - Learns output labels, maps to plaintext via output decoding table
```

**Security hardening:** Use authenticated garbling (WRK scheme) for malicious security at ~2x overhead.
