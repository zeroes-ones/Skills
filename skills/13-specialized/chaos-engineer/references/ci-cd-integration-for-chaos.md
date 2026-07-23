# CI/CD Integration for Chaos

### Pipeline Integration
Run chaos experiments in staging on every merge to main — catch resilience regressions like we catch functional bugs.

```yaml
# Example GitHub Actions + LitmusChaos integration
chaos-tests:
  runs-on: ubuntu-latest
  steps:
    - name: Install LitmusChaos
      run: kubectl apply -f https://litmuschaos.github.io/litmus/litmus-operator.yaml
    - name: Run chaos experiments
      run: |
        kubectl apply -f experiments/pod-kill.yaml
        kubectl wait --for=condition=Completed chaosengine/pod-kill --timeout=300s
    - name: Check experiment result
      run: kubectl get chaosresult pod-kill -o jsonpath='{.status.experimentStatus.verdict}'
```


**What good looks like:** Chaos experiment catalog with 10+ experiments covering different fault types. GameDay completed in the last 30 days with documented findings. Blast radius controls tested and verified. Resilience score for each service tracked over time.

### SLO-Based Experiment Gating
Only run chaos experiments if error budget is healthy:
- Check SLO burn rate. If error budget burn rate > 2 for the current window, skip chaos experiments.
- Only run experiments on services with sufficient error budget (>50% remaining).
- If an experiment consumes error budget, account for it: chaos experiments consume error budget.

### Error Budget Integration
- Chaos experiments are not free — they consume error budget (artificially by injecting failures).
- Define a chaos budget as a fraction of total error budget (e.g., 5% of error budget reserved for chaos).
- If chaos budget is depleted, pause ALL experiments until next window.
- Automate: link chaos experiment results to SLO dashboards. If an experiment causes an SLO violation, that's data, not failure — but track it.
