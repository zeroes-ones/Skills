# Generalized Conflict Resolution Framework

## Domain-Independent Weighted Decision Matrix

```

1. CALIBRATE SCORES (make them comparable)
   calibration_factor[skill] = historical_accuracy[skill] / avg_confidence[skill]
   calibrated_score = raw_score * calibration_factor

2. DETERMINE DOMAIN WEIGHTS
   Weights are context-dependent, not fixed:
   ├── Data quality higher → skill with fresher data gets more weight
   ├── Domain match higher → skill whose domain matches the question gets more weight
   ├── Track record higher → skill with better historical accuracy gets more weight
   └── Recency higher → skill with more recent analysis gets more weight

3. COMPUTE WEIGHTED DECISION
   decision_score = Σ (calibrated_score[i] * weight[i] * direction[i])
   where direction: BUY/AGREE=+1, HOLD/NEUTRAL=0, SELL/DISAGREE=-1

4. THRESHOLD TO DECISION
   Strong positive (>+15) → Strong action
   Weak positive (+5 to +15) → Action with caution (50% size, tighter stops)
   Neutral (-5 to +5) → No action (insufficient signal)
   Weak negative (-5 to -15) → Reverse action with caution
   Strong negative (<-15) → Strong reverse action

5. DOCUMENT (auditable)
   - Calibration factors and their source
   - Weight derivation rationale
   - Decision score computation
   - Confidence in the resolution itself

```

## Domain-Specific Weight Tables

### Finance/Trading
| Regime | Technical Weight | Fundamental Weight | Rationale |
|--------|-----------------|-------------------|-----------|
| Trending (ADX>25) | 0.65 | 0.35 | Technicals dominate in trends |
| Ranging (ADX<20) | 0.35 | 0.65 | Fundamentals anchor range-bound markets |
| Volatile (VIX>30) | 0.50 | 0.50 | Neither source reliable in chaos |
| Earnings week | 0.25 | 0.75 | Technicals break down near earnings |

### Code Review
| Context | Code Review Weight | Security Review Weight | Rationale |
|---------|-------------------|----------------------|-----------|
| Feature code | 0.60 | 0.40 | Correctness primary, security secondary |
| Auth/payment code | 0.30 | 0.70 | Security primary for sensitive paths |
| Refactoring | 0.70 | 0.30 | Correctness of transformation key |
| New dependency | 0.40 | 0.60 | Supply chain security paramount |

### Product Decisions
| Context | Product Manager Weight | UX Researcher Weight | Rationale |
|---------|----------------------|---------------------|-----------|
| New feature | 0.55 | 0.45 | Both strategic and user need |
| Usability fix | 0.30 | 0.70 | User research leads |
| Revenue feature | 0.70 | 0.30 | Business viability check |
| Accessibility | 0.35 | 0.65 | Compliance + user need |
