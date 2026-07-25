## Production Checklist

- [ ] **[ED1]** Schema registry deployed, all types registered with BACKWARD compatibility before producers deploy
- [ ] **[ED2]** DLQ configured per consumer, max 3 retries, alert on DLQ depth > 0
- [ ] **[ED3]** Idempotency keys on every event, dedup store tested under concurrent load
- [ ] **[ED4]** Consumer lag monitoring: alert at >1000 messages or >30s staleness
- [ ] **[ED5]** Schema compatibility validation in CI — breaking changes blocked at PR
- [ ] **[ED6]** Correlation IDs propagated end-to-end
- [ ] **[ED7]** Event payloads <1MB, large data in object storage with URL references
- [ ] **[ED8]** Critical events (payments, orders) on dedicated topics — never mixed with analytics
- [ ] **[ED9]** Circuit breakers on all sync calls from handlers, <5s timeout
- [ ] **[ED10]** Transactional outbox for events published in DB transactions
- [ ] **[ED11]** Consumer groups per environment
- [ ] **[ED12]** Snapshot strategy for event-sourced aggregates, replay <5s
- [ ] **[ED13]** Event version deprecation policy with N-release migration window
- [ ] **[ED14]** Chaos testing: poison message injection, partition failure, network partition quarterly
