# Efficiency ROI Worksheet

> Template for dollar-quantified optimization proposals. Every optimization claim must fill this worksheet — a proposal without the numbers is a guess with a budget attached (AR-01, AR-02).

## 1. Baseline (must reproduce the bill within ±10%)

| Metric | Value | Source |
|--------|-------|--------|
| Requests/day | | requests.jsonl |
| Avg input tokens/request | | provider `usage` |
| Avg output tokens/request | | provider `usage` |
| Cache hit rate | | `--cache` output |
| Avg $/request | | token-cost-calculator |
| $/day, $/month | | token-cost-calculator |
| $/done (per task type) | | token-cost-calculator |

## 2. Proposed Change

- **Lever(s):** reduce input / cache / cap output / route to cheaper model
- **Scope:** which endpoint(s), which task type(s)
- **Quality floor held:** success rate / retention / accuracy — list the gate and its current value

## 3. Projected Impact

| Metric | Before | After | Delta |
|--------|-------:|------:|------:|
| Tokens/request (in/out) | | | |
| $/request | | | |
| Cache hit rate | | | |
| $/day | | | |
| $/month | | | |
| $/done | | | |

## 4. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Cache busting on deploy | Med | High ($ one-time + recurring) | Prefix byte-diff in CI; freeze approval |
| Compression drops a fact | Low | Very high (wrong answer) | Retention test ≥ 90% + rollback plan |
| Truncation from tighter cap | Med | Low | `finish_reason` monitor; per-type caps |

## 5. Payback Math

- One-time implementation cost (engineering hours × $/hr + tooling): $_____
- Recurring savings/month: $_____
- Payback period: _____ months
- Break-even hit rate / success rate / retention that keeps the change net-positive: _____

## 6. Decision

- [ ] Approve with owner sign-off (name/date) — required if any quality metric moves
- [ ] Reject — quality floor cannot be held
- [ ] Defer — baseline insufficient (measure more first)

## 7. Post-Deployment Verification (Loop 3)

- [ ] Re-run baseline analysis 7 days post-deploy; compare actual vs projected
- [ ] Confirm quality metrics flat or better
- [ ] Feed learnings back into the cost model and this worksheet archive
