# Template Examples — Runnable Eval Configurations and Tests

Working templates for eval pipeline configuration and test case definitions.

## Eval Configuration (eval_config.yaml)

```yaml
eval:
  name: agent-compliance-pipeline
  version: "1.0"
  levels:
    l1_unit:
      enabled: true
      min_cases: 200
      gate: exact_match_regression_tolerance: 0.01
    l2_integration:
      enabled: true
      min_cases: 100
      gate: sprt_alpha: 0.05
      gate: sprt_beta: 0.20
    l3_e2e:
      enabled: true
      min_cases: 50
      gate: bootstrap_ci_threshold: 0.01
    l4_gotcha:
      enabled: true
      min_cases: 50
      gate: safety_failure_block: true

  judge:
    model: gpt-4o-mini
    calibration:
      min_kappa: 0.70
      recalibrate_months: 3
      position_bias_mitigation: symmetric
    dimensions:
      - correctness
      - efficiency
      - safety
      - completeness

  statistical:
    method: sprt
    alpha: 0.05
    beta: 0.20
    delta: 0.05
    max_iterations: 200
```

## Unit Test Template (test_l1_tool_calls.py)

```python
import pytest
from eval_harness import ToolCallEvaluator

TOOL_TESTS = [
    {
        "id": "tool-read-file-001",
        "input": "Read the contents of src/main.py",
        "expected_tool": "view",
        "expected_args": {"path": "src/main.py"},
    },
    {
        "id": "tool-edit-file-001",
        "input": "Change 'old_function' to 'new_function' in utils.py",
        "expected_tool": "edit",
        "expected_args": {
            "path": "utils.py",
            "old_str": "old_function",
            "new_str": "new_function",
        },
    },
]

@pytest.mark.parametrize("case", TOOL_TESTS, ids=[t["id"] for t in TOOL_TESTS])
def test_tool_call_correctness(case, agent):
    result = agent.process(case["input"])
    assert result.tool_name == case["expected_tool"]
    for key, value in case["expected_args"].items():
        assert key in result.tool_args
```

## Integration Test Template (test_l2_scenarios.py)

```python
import pytest
from eval_harness import ScenarioRunner, LLMJudge

SCENARIOS = [
    {
        "id": "scenario-create-refactor-001",
        "turns": [
            {"user": "Create a file hello.py with a greeting function",
             "expected_tools": ["create"],
             "expected_output_contains": "def greeting"},
            {"user": "Now refactor it to accept a name parameter",
             "expected_tools": ["edit"],
             "expected_output_contains": "def greeting(name)"},
        ],
    },
]

@pytest.mark.parametrize("scenario", SCENARIOS)
def test_multi_turn_scenario(scenario, agent, judge):
    runner = ScenarioRunner(agent, scenario["turns"])
    results = runner.execute()
    for turn_result, expected in zip(results, scenario["turns"]):
        assert turn_result.tool_name in expected["expected_tools"]
        score = judge.score(turn_result.output, expected["expected_output_contains"])
        assert score >= 3, f"Turn score {score} below threshold"
```

## CI/CD Gate Script (eval_gate.py)

```python
import sys
from eval_pipeline import SPRTRunner, EvalGate

def main():
    runner = SPRTRunner(alpha=0.05, beta=0.20, delta=0.05)
    result = runner.run_suite("config/eval_config.yaml")

    gate = EvalGate(result)
    decision = gate.decide()

    if decision.block:
        print(f"BLOCK: {decision.reason}")
        sys.exit(1)
    elif decision.inconclusive:
        print(f"INCONCLUSIVE: {decision.reason} — running more iterations")
        sys.exit(2)
    else:
        print(f"PASS: Score {result.composite_score:.3f}")
        sys.exit(0)

if __name__ == "__main__":
    main()
```
