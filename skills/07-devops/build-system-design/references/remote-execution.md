# Remote Execution Architecture

## When to Invest in Remote Execution

Remote execution is worth the investment when ALL of these are true:
1. Builds are fully hermetic (verified)
2. Local cache hit rate > 90%
3. Clean build time > 15 minutes
4. Team size > 20 engineers
5. CI build time is a bottleneck for PR merge velocity

## Managed Services

| Provider | Pricing Model | Key Features |
|----------|--------------|--------------|
| BuildBuddy | Per-seat + compute | Excellent UX, built-in analytics, SOC 2 |
| EngFlow | Compute-based | REAPI-native, enterprise focus |
| Flare Build | Per-seat | Simpler setup, good for mid-size teams |

Managed services provide: zero ops burden, excellent dashboards, built-in remote cache, support.

## Self-Hosted

### BuildBarn (Open Source)
```bash
# Run BuildBarn CAS + scheduler
docker run -p 8980:8980 ghcr.io/buildbarn/bb-storage:latest
docker run -p 8981:8981 ghcr.io/buildbarn/bb-scheduler:latest
docker run ghcr.io/buildbarn/bb-worker:latest
```

### bazel-remote (Lightweight Cache)
```bash
# Simple remote cache, no execution
docker run -p 9090:9090 -v /data:/data buchgr/bazel-remote-cache
```

## Scaling Milestones

| Team Size | Recommendation | Monthly Cost (est.) |
|-----------|---------------|---------------------|
| 20-50 | Remote caching only | $200-$1000 |
| 50-200 | Remote execution for CI | $2K-$10K |
| 200+ | Remote execution for all | $10K-$50K+ |
| 500+ | Dedicated build cluster | $50K-$200K+ |

## Common Pitfalls

- Enabling remote execution before hermeticity → flaky builds at scale
- Not sizing workers correctly → builds slower than local
- Not monitoring worker health → idle workers wasting money
- Not caching toolchains on workers → cold start latency per build
