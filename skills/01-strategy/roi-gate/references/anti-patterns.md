# ROI Anti-Patterns — When NOT to Apply ROI Gating

## Critical Exceptions (Bypass ROI Gate)

| Scenario | Reasoning | Route To |
|----------|-----------|----------|
| Active P0/P1 incident | Downtime costs dwarf analysis costs | `incident-responder` |
| Security vulnerability (CVE ≥ 7.0) | Risk is unbounded, not calculable | `security-engineer` |
| Legal/compliance mandate | Non-negotiable, fines exceed any dev cost | `compliance-officer` |
| Data loss/corruption | Irreversible harm, cost infinite | `incident-responder` |
| Dependency with known exploit | Zero-day risk invalidates ROI math | `security-engineer` |

## Common Anti-Patterns

### 1. Analysis Paralysis
**Symptom:** Spending 2 hours calculating ROI for a 30-minute fix.
**Rule:** If estimated effort < 2 hours AND traffic impact < 5%, auto-pass TRIVIAL tier.

### 2. False Precision
**Symptom:** Calculating ROI to 4 decimal places with guessed inputs.
**Rule:** All estimates are ±50%. Direction matters more than precision.

### 3. Sunk Cost Fallacy
**Symptom:** "We already spent $X building it, so we should keep investing."
**Rule:** Past costs are irrelevant. Only forward-looking costs matter.

### 4. Vanity Optimization
**Symptom:** Optimizing code paths that handle < 1% of traffic for marginal gains.
**Rule:** If estimated annual savings < 10× development cost, STOP.

### 5. The "Technical Debt" Blank Check
**Symptom:** Labeling any refactor as "paying down tech debt" to bypass ROI.
**Rule:** Technical debt repayment still needs ROI justification. Quantify the interest.

## Real Cost Examples

| Anti-Pattern | Real Cost | What Happened |
|-------------|-----------|---------------|
| Analysis Paralysis | $4,200 | Team spent 3 days modeling ROI for a 2-hour cache config change |
| False Precision | $18,000 | 2-week ROI analysis with made-up revenue numbers for a login page redesign |
| Sunk Cost | $250,000+ | Continued investing in a failing microservice for 6 months after clear failure signals |
| Vanity Optimization | $8,500 | Optimized a batch job from 45s to 38s — runs once nightly, saves $0.03/month |
| Tech Debt Blank Check | $120,000 | 3-month "cleanup" of a module handling 0.5% of traffic with zero bugs in 2 years |
