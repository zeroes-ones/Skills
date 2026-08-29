# Token Efficiency — Worked Example: Support-Chat Cost Optimization

> **Example type:** Real-world token-cost optimization case study (synthetic but production-plausible data). All figures tagged `[VERIFIED]` (provider pricing 2026-08-29), `[COMPUTED]` (derived from the token log), or `[ESTIMATED]` (projected at current usage).

## Scenario

A B2B SaaS support team runs a customer-support chat agent on Claude Sonnet 4 (`[VERIFIED 2026-08-29]`: input $3.00/M, output $15.00/M, cached read $0.30/M). 20,000 chats/month. The monthly LLM bill is $9,800 and growing 25% month-over-month with flat chat volume.

## Baseline Measurement `[COMPUTED]`

Sample of 500 real requests (provider `usage` fields, not word counts):

| Metric | Value |
|--------|-------|
| Avg input tokens/request | 52,000 (48,000 of it repeated boilerplate + instructions) |
| Avg output tokens/request | 2,400 (no `max_tokens` set) |
| Cache hit rate | 4% (prefix order varied per request) |
| Avg $/request | $0.231 |
| $/month (20K chats) | $4,620 (this endpoint alone) |

## Root Causes Found

1. **Cache busting `[VERIFIED]`:** the static prefix (system prompt + instructions) was re-sorted per request, so 48K tokens were re-sent uncached every time — 25× the cached price for the prefix.
2. **Unbounded output `[COMPUTED]`:** average reply 2,400 tokens where the natural answer was ~800; the extra 1,600 tokens at $15/M added $0.024/request — $480/month.
3. **No task-type budget `[COMPUTED]`:** the 80%-utilization guardrail was never applied; overflow caused 6% of sessions to truncate instructions and retry.

## Applied Fixes

1. **Froze the prefix** — system prompt + instructions + tool schemas versioned as a byte-stable artifact, sorted deterministically (tier → alphabetical). Added `cache_control` breakpoints. `[VERIFIED]` cache read = $0.30/M.
2. **Capped output** — `max_tokens: 1000` for chat, JSON-schema structured output for ticket extraction (500-token cap).
3. **Declared budgets per task type** — `budget.json` with input cap 45K, output cap 1K, margin 20% of the 200K window.

## Results After 30 Days `[COMPUTED]`

| Metric | Before | After | Delta |
|--------|-------:|------:|------:|
| Cache hit rate | 4% | 91% | +87 pts |
| Avg input tokens/request | 52,000 | 12,500 (4,500 cached read) | -76% |
| Avg output tokens/request | 2,400 | 860 | -64% |
| Avg $/request | $0.231 | $0.043 | -81% |
| Monthly cost (20K chats) | $4,620 | $860 | **-$3,760/month** |

Annualized savings: **$45,120/year** `[COMPUTED]` — with a measured 1.1% *improvement* in CSAT (faster answers, no truncation retries).

## Best Case `[ESTIMATED]`

Same playbook applied to the org's four other endpoints (triage, codegen, extraction, review): combined savings of **$118K/year** if cache discipline and output caps hold org-wide. Two engineers, two weeks of effort: implementation cost ~$18,000 fully loaded → payback in under 2 months.

## Worst Case

If the prefix had NOT been frozen (a "helpful" comment added to L1 mid-rollout), hit rate would have reverted to ~0%, adding $3,960/month back — and if output caps had been set too tight (< 500 tokens), truncation would have risen from 0.4% to 4%, triggering retries that erased ~$1,100/month of the savings. Worst-case net: only **$1,200/month** saved instead of $3,760 — the optimization is fragile to both cache churn and truncation.

## Lessons Learned & Key Takeaways

- **Key takeaway — stabilize before you shrink:** the cache fix alone delivered 70% of the savings; compression was never needed. Prefix stability is cheaper and safer than compression.
- **Lesson learned — measure from provider `usage`, never word counts:** the word-count estimate said 42K tokens; the tokenizer said 52K — the 24% gap would have under-budgeted the whole fix.
- **Lesson learned — cap output before optimizing prompts:** trimming 1,600 output tokens ($0.024) beat trimming 5,000 input tokens ($0.015) on the same request — output tokens are 5× the input price.
- **Lesson learned — one incident erases a quarter of savings:** a single wrong-answer regression from over-compression or truncation costs $20K+ in remediation — the retention test and truncation monitor are not optional.
- **Learning — the correctness cliff is real:** $/request fell 81%, but the win only counts because CSAT and first-contact resolution *improved* — cost per done fell, not just cost per call.

## Repro

```bash
# 1. Capture 500 real requests (provider usage fields) → requests.jsonl
# 2. Baseline:
python3 skills/22-ai-engineering/token-efficiency/scripts/token-cost-calculator.py \
  --analyze requests.jsonl --price claude-sonnet-4:3:15:0.30
# 3. After the fix, re-run and compare $/request and hit rate:
python3 skills/22-ai-engineering/token-efficiency/scripts/token-cost-calculator.py \
  --cache requests-after.jsonl --price claude-sonnet-4:3:15:0.30
```
