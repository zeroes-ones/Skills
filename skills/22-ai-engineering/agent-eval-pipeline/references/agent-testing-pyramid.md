# Agent Testing Pyramid

<!-- QUICK: 30s -- The agent testing pyramid adapts traditional software testing to AI agent evaluation, with unit tests at the base, integration tests in the middle, and E2E behavioral tests at the top. -->

## Overview

Traditional testing pyramids (unit → integration → E2E) fail for AI agents because agent behavior is non-deterministic. The Agent Testing Pyramid introduces three tiers designed for stochastic systems:

| Tier | Scope | Determinism | Sample Size | Cost/Test | Catch Rate |
|------|-------|-------------|-------------|-----------|------------|
| **L1: Tool Correctness** | Single tool call | Deterministic | 100+ per tool | $0.01 | ~95% of regressions |
| **L2: Multi-Turn Scenarios** | 3-10 turn conversations | Semi-deterministic (temperature=0) | 50+ per scenario | $0.15 | ~80% of behavioral bugs |
| **L3: E2E Pipeline Compliance** | Full 10-phase workflow | Non-deterministic | 20+ per pipeline | $2.00 | ~70% of integration failures |

## L1: Tool Correctness Tests (Unit Equivalent)

Tests that verify a single tool call produces the correct output given a specific input. These are the only **deterministic** tests in the pyramid.

### What to Test
```python
# L1 Test: Verify tool parses args correctly
def test_search_tool_date_parsing():
    """Search tool correctly parses ISO 8601 dates."""
    result = agent.invoke_tool(
        tool_name="search_files",
        args={"date_range": "2024-01-01..2024-01-31"},
        mock_filesystem={
            "report-2024-01-15.md": "Q1 planning doc",
            "report-2024-02-01.md": "Q2 kickoff"
        }
    )
    assert len(result.files) == 1
    assert result.files[0].name == "report-2024-01-15.md"

# L1 Test: Verify tool validates edge cases
def test_file_write_permission_denied():
    """Tool correctly handles permission errors."""
    result = agent.invoke_tool(
        tool_name="write_file",
        args={"path": "/etc/config.yaml", "content": "unauthorized"},
        mock_permissions={"write": False}
    )
    assert result.error_code == "PERMISSION_DENIED"
    assert "cannot write" in result.message.lower()
```

### L1 Coverage Requirements
- Every tool must have tests for: happy path, null/missing args, boundary values, error states, and invalid inputs
- Parser edge cases: empty strings, Unicode, very long inputs (>100KB), special characters in paths
- Mock the environment, not the tool logic

## L2: Multi-Turn Scenario Tests (Integration Equivalent)

Tests that verify the agent follows expected behavior across 3-10 turns of conversation. Run with `temperature=0` for reproducibility but expect minor output variation.

### Scenario Design Pattern
```yaml
# scenario: code-review-with-constraints.yaml
name: "Code review with security constraints"
turns:
  - user: "Review this PR for security issues"
    files: ["src/auth/login.ts"]
    expected:
      - agent_asks_question: true  # Must clarify scope
      - tool_called: "read_file"
      - file_accessed: "src/auth/login.ts"

  - user: "Focus on authentication bypass risks"
    expected:
      - tool_called: "grep"
      - pattern_searched: "session|token|jwt|cookie"
      - output_contains: ["SQL injection", "XSS", "CSRF"]

  - user: "Are there any hardcoded secrets?"
    expected:
      - output_does_not_contain: ["looks good", "no issues", "everything fine"]  # Anti-pattern: dismissive language
      - severity_assigned: "critical"  # Must flag hardcoded secrets as critical

quality_thresholds:
  min_turns_completed: 3
  max_hallucination_rate: 0.05
  required_tools_used: ["read_file", "grep"]
```

### Scenario Diversity Matrix
| Dimension | Variation 1 | Variation 2 | Variation 3 |
|-----------|------------|------------|------------|
| User expertise | Beginner (vague requests) | Intermediate (specific asks) | Expert (technical jargon) |
| Context size | Small (<5 files) | Medium (10-50 files) | Large (100+ files) |
| Ambiguity | Clear request | Implicit needs | Contradictory constraints |
| Error injection | Clean inputs | Missing files | Corrupted data |

## L3: E2E Pipeline Compliance Tests (System Equivalent)

Tests that verify the agent completes a full 10-phase workflow end-to-end. These are non-deterministic and require **statistical evaluation** (see `statistical-eval-methodology.md`).

### Pipeline Phases Tested
1. **Context Gathering** — Agent discovers project structure, reads relevant files
2. **Requirement Parsing** — Agent extracts actionable tasks from user request
3. **Planning** — Agent creates an execution plan with dependencies
4. **Tool Selection** — Agent chooses correct tools for each sub-task
5. **Execution** — Agent invokes tools in correct order
6. **Error Recovery** — Agent detects and recovers from failures
7. **Output Generation** — Agent produces structured output
8. **Self-Review** — Agent validates its own output
9. **Iteration** — Agent incorporates feedback and refines
10. **Delivery** — Agent presents final result with evidence

### E2E Metrics Tracked
```python
E2E_METRICS = {
    "pipeline_completion_rate": "float, 0.0-1.0",
    "phase_success_rate": "dict[phase_name, float]",
    "error_recovery_success": "float, 0.0-1.0",  # Fraction of injected errors recovered
    "mean_turns_per_phase": "dict[phase_name, float]",
    "token_efficiency": "float",  # Useful tokens / total tokens
    "tool_usage_accuracy": "float",  # Correct tool chosen / total tool calls
}
```

## Pyramid Enforcement in CI

```yaml
# CI pipeline configuration
eval_gates:
  l1_tool_tests:
    action: block  # Must pass 100%
    threshold: 1.0

  l2_scenario_tests:
    action: block  # Must pass ≥ 95%
    threshold: 0.95

  l3_e2e_tests:
    action: warn   # Degradation > 5% triggers warning
    threshold: 0.90
    comparison: previous_commit  # Compare against baseline
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Skipping L1 for L3 directly | E2E tests are slow ($2/test) and noisy; you'll miss 95% of regressions | Build L1 first (100+ tests, $0.01 each), then L2, then L3 |
| Using `assert "error" not in output` | LLMs describe errors differently each run; string matching is brittle | Use semantic assertions: `assert_no_error_pattern(output)` using embedding similarity |
| Testing only happy paths | LLMs are most likely to fail on edge cases; happy path tests give false confidence | Inject errors: missing files, permission denied, ambiguous requests, contradictory constraints |
| Running L2 at temperature > 0 | Non-deterministic output breaks assertion reliability | Set `temperature=0` for L2; reserve non-zero temperature for L3 statistical evaluation |

## What Good Looks Like

- L1: 100+ tool tests, all passing, < 2 seconds total runtime
- L2: 50+ scenario tests, ≥ 95% pass rate, < 60 seconds total runtime
- L3: 20+ E2E pipeline runs, ≥ 90% completion rate, statistical significance confirmed via SPRT
- CI blocks merges when any L1 failure or L2 degradation > 5% is detected
