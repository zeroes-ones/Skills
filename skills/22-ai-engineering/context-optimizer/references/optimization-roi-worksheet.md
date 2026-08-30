# Optimization ROI Worksheet — Dollar-Quantified Before/After

> Every optimization proposal fills this worksheet. A proposal without the numbers is a guess with a budget attached (AR-01, AR-02).

## 1. Baseline (must reproduce the bill within ±10%)

| Metric | Value | Source |
|--------|-------|--------|
| Requests/day | | requests.jsonl |
| Tokens/request (in/out) | | provider `usage` |
| Per-level token ledger | | measurement-protocol.md |
| Cache hit rate | | `--cache` |
| $/request | | token-cost-calculator |
| $/day, $/month | | token-cost-calculator |
| $/done (per task type) | | cost-per-done.md |

## 2. Proposed Change

- **Lever(s):** reduce / cache / compress / cap output
- **Scope:** which task type(s), which level(s)
- **Retention floor:** current retention + success rate (the quality gate)

## 3. Projected Impact

| Metric | Before | After | Delta |
|--------|-------:|------:|------:|
| Input tokens/request (per level) | | | |
| Output tokens/request | | | |
| Cache hit rate | | | |
| $/request | | | |
| $/day | | | |
| $/month | | | |
| $/done | | | |
| Retention score | | | |

## 4. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Cache busting on deploy | Med | High ($ one-time + recurring) | Prefix byte-diff in CI; freeze approval |
| Compression drops a constraint | Low | Very high (wrong answer) | Retention test >= 90% + rollback |
| Truncation from tighter cap | Med | Low | `finish_reason` monitor; per-type caps |
| Retry tax on cheap path | Med | Med | $/done tracking; fallback routing |

## 5. Payback Math

- One-time implementation cost: $_____
- Recurring savings/month: $_____
- Payback period: _____ months
- Break-even retention / success rate that keeps the change net-positive: _____

## 6. Decision

- [ ] Approve with owner sign-off (name/date) — required if any quality metric moves
- [ ] Reject — retention floor cannot be held
- [ ] Defer — baseline insufficient (measure more first)

## 7. Post-Deployment Verification (Loop 3)

- [ ] Re-run the baseline analysis 7 days post-deploy; compare actual vs projected
- [ ] Confirm retention and success metrics flat or better
- [ ] Feed learnings back into the cost model and this worksheet archive
