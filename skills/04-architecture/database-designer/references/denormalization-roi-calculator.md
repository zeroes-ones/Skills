# Denormalization ROI Calculator

```
For each denormalization: 
ROI = (read_latency_reduction_ms × reads_per_second × user_value_per_ms) - (write_penalty_ms × writes_per_second × write_cost_factor) - (storage_cost)

Example: Denormalizing `order_count` onto `users` table:
- Reads: 1000/s, latency down from 50ms to 5ms (45ms saved)
- Writes: 10/s, latency up from 10ms to 12ms (2ms penalty)
- Storage: 4 bytes × 1M users = 4MB — negligible
- ROI: (45ms × 1000 × 1000 reqs) - (2ms × 10 × 1000) = overwhelmingly positive

Denormalize when: read:write ratio > 100:1 and read latency > 20ms.
Do NOT denormalize when: read:write ratio < 10:1 (maintenance will kill you).
```
