# Invocation Strategy

## User-Invoked vs Model-Invoked

| Dimension | User-Invoked | Model-Invoked |
|-----------|-------------|---------------|
| **Activation** | User explicitly calls the skill | Model autonomously decides to invoke |
| **Cost when not used** | Zero context cost | Zero context cost (frontmatter only) |
| **Cost when used** | Full skill loaded into context | Full skill loaded into context |
| **Discovery** | User must know the skill exists | Model discovers based on description triggers |
| **Best for** | Specialized, infrequent tasks | Common patterns, safety gates, auto-detection |
| **Worst for** | Tasks where user doesn't know they need the skill | Tasks with high false-positive trigger rate |

## Orchestration Patterns

### Sequential
User-invoked skill A calls model-invoked skills B, C, D in order.
```
User → A (user-invoked) → B (model-invoked) → C (model-invoked) → D (model-invoked)
```
Use when: output of B feeds input of C.

### Parallel
User-invoked skill A calls model-invoked skills B, C, D simultaneously.
```
User → A → [B, C, D] (parallel)
         → aggregate results
```
Use when: B, C, D are independent. Warning: 3x context cost.

### Conditional
User-invoked skill A calls model-invoked skill B OR C based on decision tree.
```
User → A → Decision Tree → B (if condition X)
                          → C (if condition Y)
```
Use when: which skill to invoke depends on runtime conditions.

## Invocation Conditions

Model-invoked skills need narrow trigger conditions to avoid false positives:
- Filesystem conditions: `file_contains("*.py", "auth")` → security review
- Git conditions: `git diff --stat` > 200 lines → code review
- Content conditions: `file_contains("*", "TODO\|FIXME")` → tech debt audit

Without narrow triggers, the skill fires on every request → context budget explosion.

## When to Convert User-Invoked → Model-Invoked

Convert when:
- Users consistently forget to invoke the skill when they should
- The trigger conditions are unambiguous and narrow
- The cost of a false positive (unnecessary invocation) is low

## When to Convert Model-Invoked → User-Invoked

Convert when:
- The skill fires too often on false positives
- The skill is expensive (>3,000 tokens) and rarely needed
- Users complain about the skill interfering with other workflows
