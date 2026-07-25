## 2. Decision Tree: MPC Protocol Selection

Choose your MPC protocol stack based on the adversary model and computation type. The wrong choice can mean $1M+ in unnecessary overhead or insufficient security.

```
┌── MPC Protocol Selection ──────────────────────────────────────┐
│                                                                 │
│  How many corrupt parties can you tolerate?                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ t < n/2 (honest majority)?                                │  │
│  │  ├─ Reactive computation needed? ─► SPDZ (online phase)   │  │
│  │  │  └─ Low latency < 100ms? ─► Replicated Secret Sharing  │  │
│  │  │     (3-party, dishonest minority, 1 corrupt)           │  │
│  │  └─ Non-reactive (batch)? ─► BGW/GMW with Shamir shares   │  │
│  │     └─ Boolean circuits? ─► GMW with OT extension         │  │
│  │        └─ Arithmetic circuits? ─► BGW (Shamir-based)      │  │
│  │                                                           │  │
│  │ t < n (dishonest majority)?                                │  │
│  │  ├─ Need preprocessing? ─► SPDZ-like (MASCOT/Overdrive)   │  │
│  │  │  ├─ Function-independent preprocessing ─► MASCOT       │  │
│  │  │  └─ Function-dependent preprocessing ─► SPDZ2k         │  │
│  │  └─ Garbled circuits sufficient? ─► Yao with OT           │  │
│  │     └─ Malicious security? ─► Authenticated garbling      │  │
│  │        (WRK/Wang-Katz, ~2x overhead vs semi-honest)       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Protocol selection matrix (n=3, varied t):                     │
│  ┌─────────────────────┬──────────┬────────────┬─────────────┐  │
│  │ Protocol            │ Security │ Throughput │ Round-trips │  │
│  ├─────────────────────┼──────────┼────────────┼─────────────┤  │
│  │ Replicated (3PC)    │ 1 corrupt│ 10M AND/s  │ 1 (online)  │  │
│  │ Shamir (BGW)        │ t < n/2  │ 1M mult/s  │ O(depth)    │  │
│  │ SPDZ (MASCOT)       │ n-1 corr │ 100K mult/s│ 1 online    │  │
│  │ Yao (semi-honest)   │ 1 corrupt│ 1M gates/s │ 2           │  │
│  │ Yao (malicious)     │ 1 corrupt│ 500K gate/s│ 2           │  │
│  │ GMW (OT-based)      │ 1 corrupt│ 500K AND/s │ O(depth)    │  │
│  └─────────────────────┴──────────┴────────────┴─────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation with MP-SPDZ (Python DSL):**
```python
# MP-SPDZ example: Secure inner product with malicious security
# Compile: ./compile.py -R 64 inner_product
# Run: Scripts/2-party-malicious.sh inner_product

from Compiler import mpc_math, util

def inner_product(x, y, n):
    """Compute dot(x, y) with active security against n-1 corruptions"""
    res = sint(0)
    @for_range(n)
    def _(i):
        res += x[i] * y[i]
    return res

x = [sint.get_input_from(0) for _ in range(10)]
y = [sint.get_input_from(1) for _ in range(10)]
result = inner_product(x, y, 10)
print_ln("Inner product: %s", result.reveal())
```

**Key decision factors:**
- **Round complexity:** FHE-based MPC (1 round) vs OT-based (O(depth)) — latency-sensitive apps need constant-round
- **Corruption threshold:** Dishonest majority requires SPDZ-like preprocessing (10-100x overhead vs honest majority)
- **Circuit type:** Arithmetic circuits (Shamir/BGW) are 100x faster for numeric computation than Boolean (GMW/Yao)
- **Setup assumptions:** CRS model (SPDZ) vs plain model (BGW, replicated) — CRS adds trusted setup risk

---
