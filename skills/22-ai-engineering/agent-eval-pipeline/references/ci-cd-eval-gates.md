# CI/CD Evaluation Gates

<!-- QUICK: 30s -- CI/CD evaluation gates block merging agents that fail quality thresholds. Design pre-merge, post-merge, and daily gates with statistical decision rules, cost budgets, and rollback automation. -->

## Gate Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         CI/CD Pipeline                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│  │ Pre-merge│───▶│  L1 Gate │───▶│  L2 Gate │───▶│  L3 Gate │   │
│  │  Commit  │    │ (Block)  │    │ (Block)  │    │ (Warn)   │   │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘   │
│       │               │               │               │         │
│       ▼               ▼               ▼               ▼         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│  │  Merge   │    │  PR      │    │  PR       │    │  Slack   │   │
│  │ Blocked  │    │ Blocked  │    │ Blocked   │    │ Alert    │   │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘   │
│                                                                   │
│  Post-merge:                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
│  │  Deploy  │───▶│ Canary   │───▶│ Full     │                   │
│  │  Canary  │    │ Eval     │    │ Deploy   │                   │
│  └──────────┘    └──────────┘    └──────────┘                   │
│       │               │                                           │
│       ▼               ▼                                           │
│  ┌──────────┐    ┌──────────┐                                    │
│  │ Rollback │    │ Promote  │                                    │
│  │ Canary   │    │ Canary   │                                    │
│  └──────────┘    └──────────┘                                    │
└──────────────────────────────────────────────────────────────────┘
```

## Gate Definitions

### Gate 1: L1 Tool Correctness (Pre-Merge, Blocking)

```yaml
gate: l1_tool_correctness
stage: pre-merge
action: block  # Merge denied if gate fails

rules:
  - name: all_tool_tests_pass
    type: exact_match
    condition: "l1_pass_count == l1_total_count"
    failure_message: "{failed_count} L1 tool tests failed. Merge blocked."
    
  - name: test_coverage_maintained
    type: comparison
    condition: "current_l1_test_count >= baseline_l1_test_count"
    failure_message: "L1 test count decreased from {baseline} to {current}. Add tests for new tools."

timeout: 120  # seconds
cost_budget: 2.00  # USD
```

### Gate 2: L2 Scenario Tests (Pre-Merge, Blocking)

```yaml
gate: l2_scenario_tests
stage: pre-merge
action: block
evaluation_method: sprt  # Sequential testing for cost efficiency

rules:
  - name: sprt_pass
    type: sprt
    config:
      p0: 0.95
      p1: 0.85
      alpha: 0.05
      beta: 0.20
      max_tests: 100
    failure_message: "SPRT rejected: agent pass rate likely ≤ {p1}"

  - name: no_critical_scenario_regression
    type: per_scenario
    conditions:
      - "scenario.pass_rate >= 0.90 for critical scenarios"
      - "scenario.pass_rate >= 0.80 for non-critical scenarios"
    failure_message: "Scenario '{scenario_name}' degraded to {pass_rate}"

  - name: hallucination_rate_bounded
    type: threshold
    condition: "hallucination_rate <= 0.05"
    failure_message: "Hallucination rate {hallucination_rate} exceeds 5% threshold"

timeout: 600  # seconds
cost_budget: 15.00  # USD
```

### Gate 3: L3 E2E Pipeline (Pre-Merge, Warning)

```yaml
gate: l3_e2e_pipeline
stage: pre-merge
action: warn  # Non-blocking; alerts but allows merge

rules:
  - name: e2e_completion_rate
    type: comparison_against_baseline
    condition: "current_completion_rate >= baseline_completion_rate - 0.05"
    failure_message: "E2E completion dropped from {baseline} to {current}"

  - name: phase_regression_check
    type: per_phase
    condition: "phase.success_rate >= baseline_phase.success_rate - 0.10"
    
timeout: 1800  # seconds (30 min)
cost_budget: 40.00  # USD
```

### Gate 4: Canary Evaluation (Post-Merge, Blocking)

```yaml
gate: canary_evaluation
stage: post-merge (canary)
action: block_rollout  # Blocks full rollout if gate fails

rules:
  - name: quality_degradation
    type: agent_assay
    config:
      effect_size_threshold: 0.3
      p_value_threshold: 0.05
    condition: "agent_assay.defect_detected == false"
    failure_message: "Canary shows quality degradation (d={effect_size}, p={p_value}). Rolling back."

  - name: latency_regression
    type: threshold
    condition: "p95_latency <= baseline_p95_latency * 1.20"
    failure_message: "P95 latency increased {pct_change}%"

  - name: error_rate
    type: threshold
    condition: "error_rate <= 0.01"
    failure_message: "Canary error rate {error_rate} exceeds 1%"

canary_duration: 600  # Run canary for 10 minutes
rollback_command: "kubectl rollout undo deployment/agent-canary"
```

## Gate Configuration Best Practices

### Pre-Merge Speed vs. Coverage Trade-off

| Test Tier | Max Runtime | When to Run | Skip Conditions |
|-----------|-------------|-------------|-----------------|
| L1 (Tool) | 2 min | Every commit | Never |
| L2 (Scenario) | 10 min | Every PR | Docs-only changes, config-only changes |
| L3 (E2E) | 30 min | PR approval, daily | Labeled `skip-e2e` by reviewer |

### Cost Budget Enforcement

```python
class CostBudgetEnforcer:
    def __init__(self, monthly_budget: float = 500.00):
        self.monthly_budget = monthly_budget
        self.spent_this_month = self._query_current_spend()
    
    def approve_gate_run(self, gate: str, estimated_cost: float) -> bool:
        """Check if running this gate fits within budget."""
        if self.spent_this_month + estimated_cost > self.monthly_budget:
            if gate in ["l1_tool_correctness", "l2_scenario_tests"]:
                # Never skip blocking gates
                print(f"WARNING: Budget exceeded but {gate} is blocking — running anyway")
                return True
            else:
                print(f"SKIPPED: {gate} would exceed monthly budget (${self.spent_this_month + estimated_cost:.2f} > ${self.monthly_budget:.2f})")
                return False
        return True
```

### Gate Skip Conditions

```yaml
# .github/eval-gates.yml
skip_conditions:
  - pattern: "docs/**"
    skip_gates: [l3_e2e_pipeline]  # Docs changes don't need E2E
    
  - pattern: "config/**"
    skip_gates: [l3_e2e_pipeline]
    
  - pattern: "tests/**"
    skip_gates: []  # Test changes need all gates
    
  - label: "skip-e2e"
    require_approval: true
    skip_gates: [l3_e2e_pipeline]
    
  - label: "emergency-fix"
    require_approval: true
    skip_gates: [l3_e2e_pipeline]  # L1 and L2 still required
```

## Rollback Automation

```python
def automated_rollback_decision(metrics: dict) -> str:
    """
    Automated rollback decision based on post-deploy metrics.
    Returns: 'rollback', 'continue_monitoring', or 'promote'
    """
    decisions = []
    
    # Safety checks (any trigger → immediate rollback)
    if metrics.get("safety_violations", 0) > 0:
        return "rollback"
    
    # Quality checks (statistical test)
    if metrics.get("agent_assay_defect_detected", False):
        decisions.append("rollback")
    
    # Performance checks
    if metrics.get("p95_latency_increase_pct", 0) > 50:
        decisions.append("rollback")
    
    # Error rate checks
    if metrics.get("error_rate", 0) > 0.05:
        decisions.append("rollback")
    
    if "rollback" in decisions:
        return "rollback"
    
    # If all metrics are better than baseline
    if all_metrics_improved(metrics):
        return "promote"
    
    return "continue_monitoring"
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| All gates are warnings | Warnings become noise; teams ignore them within 2 weeks | At least L1 and L2 must be blocking; only L3 can be warning |
| No cost budget | Team runs $2K/month in eval costs without realizing it | Enforce monthly budget; warn at 80%, hard-stop non-blocking gates at 100% |
| Same thresholds for all changes | Docs change fails E2E gate unnecessarily | Skip conditions: docs → skip L3, model changes → run all gates |
| No rollback automation | Humans take 15+ minutes to decide; damage accumulates | Automate rollback for safety violations and clear quality regressions |
