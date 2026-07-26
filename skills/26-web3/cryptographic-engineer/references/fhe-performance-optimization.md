# FHE Performance Optimization — Bootstrapping, Packing, Batching

## Bootstrapping Budget Management

### CKKS Level Tracking
```python
class CKKSMetricTracker:
    def __init__(self, initial_levels: int, bootstrap_cost_ms: float = 10000.0):
        self.levels = initial_levels
        self.bootstrap_count = 0
        self.bootstrap_cost_ms = bootstrap_cost_ms
        self.total_latency_ms = 0.0

    def consume_level(self, op_name: str):
        self.levels -= 1
        if self.levels <= 0:
            raise BudgetExhausted(f"{op_name}: No levels remaining — $200K+ data corruption risk")

    def bootstrap(self):
        self.levels = self.initial_levels  # Reset to top
        self.bootstrap_count += 1
        self.total_latency_ms += self.bootstrap_cost_ms

    def estimate_latency(self) -> float:
        return self.total_latency_ms + (self.initial_levels - self.levels) * 5.0
```

### Bootstrapping Optimization Strategies
1. **Minimize operations between bootstraps:** Batch linear operations (add, rotate, mult-by-plain) before bootstrap
2. **Bootstrap only when needed:** Track noise budget, bootstrap at last safe level
3. **Use leveled operations:** When possible, use leveled versions (no bootstrap reset)
4. **Asynchronous bootstrapping:** For multi-ciphertext pipelines, bootstrap some while computing others

## SIMD Packing Strategies

### CKKS Batching
- **Maximum slots:** N/2 for CKKS (complex, one per slot)
- **Canonical embedding:** Map vectors to polynomial via FFT-like transform
- **Slot operations:** Addition (element-wise), multiplication (element-wise), rotation (shift + mask)

### Optimal Packing Patterns
```
# Pattern 1: Dense vector operations
[ v1, v2, v3, ..., v8192 ]  → one ciphertext
All 8192 operations performed simultaneously

# Pattern 2: Matrix packing
Row-major: each row in one ciphertext
Matrix-vector product: n rotations + n additions

# Pattern 3: Structured sparsity
Pack non-zero elements densely, index via rotation
```

## Batching Rotation Keys

```python
# Generate rotation keys for all needed shifts
rotation_indices = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
# Each rotation key: ~30MB (n=32768), total: ~400MB for all
# Trade-off: memory vs runtime — generate only indices you use
```

## Performance Budgeting for Real-World Applications

| Application | Target Latency | Max Bootstraps | Scheme | Notes |
|-------------|---------------|----------------|--------|-------|
| Real-time fraud detection | < 100ms | 2 | TFHE | PBS per comparison |
| Encrypted ML inference | < 5s | 5-10 | CKKS | SIMD parallelism |
| Private information retrieval | < 1s | 0-1 | BFV/BGV | Shallow circuit |
| Encrypted database query | < 500ms | 3-5 | TFHE | Gate-level comparisons |
| Financial settlement matching | < 10s | 10-20 | BGV | Exact arithmetic required |

## Common Optimization Mistakes
1. **Over-bootstrapping:** Bootstrapping every multiplication when leveled ops would suffice
2. **Under-bootstrapping:** Running out of levels silently corrupts ciphertext
3. **Unused SIMD slots:** Wasting parallelism by not packing data densely
4. **Missing relinearization:** Ciphertext size grows O(n^2) without relinearization after each multiplication
