# Attention Dilution Metrics

## Definition
Attention dilution occurs when the volume of context reduces the model's effective attention to any single piece of information.

## Key Findings
- Models attend effectively to ~70% of context (Lost in the Middle problem)
- Information at beginning and end receives 2-3x more attention
- Middle-context information is most at risk of being ignored
- Each additional 1K tokens reduces per-token attention by ~0.1%

## Measurement
```python
def attention_coverage(context_tokens, model_window):
    """Estimate effective attention coverage."""
    if context_tokens < 0.3 * model_window:
        return 0.95  # Near-full attention
    elif context_tokens < 0.6 * model_window:
        return 0.85  # Good attention
    elif context_tokens < 0.8 * model_window:
        return 0.70  # Moderate dilution
    else:
        return 0.50  # Significant dilution
```

## Mitigation Strategies
1. **Position-critical information at edges** — Ground Rules at start, Verification at end
2. **Keep context < 60% of window** — Maintain high attention coverage
3. **Use structural markers** — Headers, numbered lists, tables anchor attention
4. **Repetition of critical constraints** — Single repetition at end improves recall
