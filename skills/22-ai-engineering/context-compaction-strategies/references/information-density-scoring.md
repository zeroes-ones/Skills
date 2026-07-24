# Information Density Scoring

## Token Importance Scoring

Score each token/section by:
```
importance = actionability × irreplaceability × decision_impact
```

### Actionability (0-1)
- Ground Rule: 1.0 (directly changes behavior)
- Example: 0.3 (illustrates, doesn't mandate)
- Prose connector: 0.0 (pure formatting)

### Irreplaceability (0-1)
- Unique constraint: 1.0 (can't be derived)
- Reference to external standard: 0.5 (recoverable)
- Common knowledge: 0.2 (model already knows)

### Decision Impact (0-1)
- Architecture decision: 1.0 (changes everything downstream)
- Naming convention: 0.2 (cosmetic)
- Optional suggestion: 0.1 (can be ignored)

## Scoring Table
| Content | Actionability | Irreplaceability | Impact | Score |
|---------|--------------|-----------------|--------|-------|
| "NEVER skip validation" | 1.0 | 1.0 | 0.8 | 0.80 |
| Decision tree path | 0.8 | 0.8 | 0.7 | 0.45 |
| Code example | 0.3 | 0.5 | 0.3 | 0.05 |
| "In this section..." | 0.0 | 0.0 | 0.0 | 0.00 |
