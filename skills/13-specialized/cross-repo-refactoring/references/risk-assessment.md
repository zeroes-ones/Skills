# Breaking Change Risk Assessment

## Blast Radius Quantification

```
Blast Radius = Consumer Count × Call Site Count × Deployment Coupling

Deployment Coupling:
- 0.2: Independent deploy schedules, canary-enabled consumers
- 0.5: Coordinated deploy windows, shared on-call
- 0.8: Tightly coupled deploy, shared fate
- 1.0: Same deploy pipeline (effectively monorepo)
```

## Risk Matrix

| Probability | Low Impact | Medium Impact | High Impact | Critical Impact |
|------------|------------|---------------|-------------|-----------------|
| High (>20%) | Mitigate | Active management | Escalate to EM | STOP — redesign |
| Medium (5-20%) | Accept | Mitigate | Active management | Escalate to EM |
| Low (<5%) | Accept | Accept | Mitigate | Active management |

## Rollback Planning

### Canary Deployment for Breaking Changes

1. Deploy new API + old API to 1% of traffic
2. Monitor error rates, latency, deprecated API counter
3. If stable: 1% → 10% → 50% → 100%
4. If errors: rollback immediately. Root cause before next attempt.

### Emergency Rollback Procedure

```
1. Identify: which consumer broke? what error?
2. Decide: rollback provider OR rollback consumer?
   - If provider rollback is fast (<2 min): rollback provider, debug offline
   - If provider rollback is slow: deploy compatibility shim on consumer side
3. Execute rollback
4. Verify: error rates return to baseline
5. Post-mortem: what did consumer discovery miss?
```

## Go/No-Go Checklist

Before executing a breaking change deployment:
- [ ] All consumer maintainers acknowledged the timeline
- [ ] Runtime deprecation counter is zero for all known consumers
- [ ] Rollback plan documented and tested
- [ ] On-call team briefed on potential issues
- [ ] Canary deployment configured
- [ ] Monitoring dashboard visible to entire team
