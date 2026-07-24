# Regression Detection in Agent Behavior

## Definition
A regression occurs when agent behavior changes in a way that degrades performance on previously-working inputs.

## Detection Methods

### Metric-Based
Track key metrics across versions:
- Task success rate (binary per test case)
- Average rubric score
- Response latency
- Token efficiency

### Distribution-Based
Compare output distributions, not just means:
- KL divergence between v1 and v2 output embeddings
- Vocabulary shift (new words appearing, old words disappearing)
- Structural changes (output format, section ordering)

## Regression Thresholds
| Metric | Warning | Block |
|--------|---------|-------|
| Success rate drop | > 2% | > 5% |
| Avg rubric drop | > 0.2 points | > 0.5 points |
| Latency increase | > 20% | > 50% |
| New failure patterns | > 3 new | > 10 new |

## Bisection Protocol
When regression detected:
1. Identify version range (last good → first bad)
2. Binary search through commits/changes
3. Isolate specific instruction change causing regression
4. Fix or revert
