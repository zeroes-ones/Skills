# Blast Radius (Military-Grade Controls)

### Scope Containment Dimensions
- **Traffic percentage**: canary traffic only (1% of users), internal-only traffic, synthetic traffic.
- **Infrastructure scope**: single pod, single node, single AZ, single region.
- **Service scope**: single endpoint, single service, non-critical service only.
- **User segment**: internal users, beta testers, free-tier customers (never enterprise customers if avoidable).
- **Time window**: low-traffic hours only (1–4 AM), weekend windows, never during known campaign/event periods.

### Abort Conditions
Auto-termination triggers (any one fires → experiment stops immediately):
- Error rate exceeds threshold (e.g., 5% increase from baseline over 30 seconds).
- P99 latency > 2x baseline for 60 seconds.
- Production alert fires and is acknowledged.
- Customer-facing impact detected by synthetic monitoring.
- Manual kill switch activated by Commander, Operator, or on-call engineer.

### Progressive Expansion Model
```
Staging (all experiments required to pass)
  → Canary (single instance, internal traffic, 15 min)
    → 1% production traffic (30 min, daytime)
      → 10% production traffic (30 min, daytime)
        → 50% production traffic (60 min, low-traffic window)
          → 100% production traffic (automated, continuous)
```
Each level requires N successful runs at the current level before advancing. N = 3 for infra/network faults, N = 5 for stateful faults.

### Time-Bounded Execution
- Every experiment has a `maxDuration` parameter. Hard stop enforced by tool.
- Auto-terminate if the responsible engineer does not acknowledge a "pre-go" prompt within 2 minutes.
- Default durations: prod experiments 5–15 minutes, staging experiments 10–30 minutes.
- Experiments that exceed their window without explicit extension are forcibly terminated.
