# Observability for Chaos

### Golden Rule
Before running ANY experiment, verify: you can detect the failure you're about to inject. If you can't see it in your dashboards, your alerts, and your logs — **fix observability first**.

### Pre-Experiment Observability Check
1. Inject the fault in staging (1 pod, 30 seconds).
2. Check: does your latency dashboard show the spike?
3. Check: does your error rate dashboard show the increase?
4. Check: does your saturation dashboard show the resource constraint?
5. Check: do your logs contain the error (with correlation ID)?
6. Check: does your alert fire within the expected time window?
7. If ANY of these fail → STOP. Fix the observability gap. Document it. Re-test.

### Running Chaos Without Observability Is Just Breaking Things
- Without observability, you cannot confirm the hypothesis.
- Without observability, you cannot detect blast radius escape.
- Without observability, you cannot learn from the experiment.
- Without observability, you cannot prove the value of chaos engineering to leadership.
