# Production Agent Monitoring

## Metrics Dashboard

### Quality Metrics
- Task success rate (daily, weekly trend)
- User satisfaction score (thumbs up/down ratio)
- Escalation rate (% tasks escalated to human)

### Safety Metrics
- Prompt injection detection rate
- Hallucination rate (sampled)
- Refusal accuracy (correct refusals vs false positives)

### Performance Metrics
- P50, P95, P99 response latency
- Token usage per task
- Cost per task

### Drift Detection
- Output embedding drift (cosine similarity to baseline)
- Vocabulary drift (KL divergence of word distributions)
- Behavioral drift (change in decision patterns)

## Alert Thresholds
| Metric | Warning | Critical |
|--------|---------|----------|
| Success rate drop | -2% | -5% |
| Hallucination rate | > 2% | > 5% |
| Injection bypass rate | > 0.5% | > 2% |
| P95 latency increase | +30% | +100% |
| Embedding drift | > 0.1 | > 0.3 |
