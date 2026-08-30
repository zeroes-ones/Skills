# Context Optimizer — Worked Example: Support-Agent Payload Optimization

> **Example type:** Real-world context-cost optimization case study (synthetic but production-plausible). Figures tagged `[VERIFIED]` (pricing/policy 2026-08), `[COMPUTED]` (derived from measurements), or `[ESTIMATED]` (projected).

## Scenario

A B2B support agent sends a 48K-token context payload per request: 30K of repeated instructions + static specs, 12K of relevant files, 6K of history. 20K requests/month on Claude Sonnet 4 (`[VERIFIED 2026-08-29]`: input $3.00/M, output $15.00/M, cached read $0.30/M). Cost: $4,620/month on this endpoint alone, growing.

## Baseline Measurement `[COMPUTED]`

Per-level ledger from 500 real requests (provider `usage` fields):

| Level | Tokens | Share of cost |
|-------|-------:|--------------:|
| L1 rules + L2 specs (repeated) | 30,000 | 62% |
| L3 files (relevant) | 12,000 | 25% |
| L5 history (raw) | 6,000 | 13% |
| Cache hit rate | 4% | — |

## Applied Levers (in ladder order)

1. **Reduce** — dedup removed 4,200 tokens of copied code blocks and duplicate error messages (lossless, free).
2. **Stabilize** — froze the 30K L1/L2 prefix byte-for-byte, added `cache_control`, deterministic ordering. Hit rate: 4% → 91%.
3. **Compress** — history summarized to decisions-only (600 tokens) with a retention test at 96% (constraint probes included).
4. **Cap output** — `max_tokens: 1000` for chat; extraction moved to JSON schema (500-token cap).

## Results After 30 Days `[COMPUTED]`

| Metric | Before | After | Delta |
|--------|-------:|------:|------:|
| Input tokens/request | 48,000 | 9,400 (4,000 cached read) | -80% |
| Cache hit rate | 4% | 91% | +87 pts |
| Output tokens/request | 2,400 | 860 | -64% |
| $/request | $0.231 | $0.043 | -81% |
| $/month (20K requests) | $4,620 | $860 | **-$3,760/month** |
| Retention score | — | 96% | quality held |

Annualized: **$45,120/year saved** `[COMPUTED]` — with CSAT up 1.1 points (faster answers, no truncation retries).

## Financial Impact

- **Direct savings:** $45,120/year.
- **Implementation cost:** ~2 engineer-weeks (~$18K loaded) → **payback in ~5 months, 2.5x ROI in year one.**

## Best Case `[ESTIMATED]`

Same ladder applied to the org's 4 other LLM endpoints (triage, codegen, extraction, review) with shared budgets → **$118K/year** combined, with one shared budget config and one cost dashboard.

## Worst Case

If the prefix had been minified during optimization (reformatted "to improve it"), the cache would have busted back to ~0% — adding $3,960/month back. If the history summary had shipped without a retention test, a dropped constraint ("never deploy on Fridays") would have caused a wrong action — a $20K incident class. The optimization is fragile to cache churn and retention-free compression.

## Lessons Learned & Key Takeaways

- **Key takeaway — the ladder order is the strategy:** stabilize-before-compress delivered ~70% of the savings alone; the rest came from reduce, compress, and cap.
- **Lesson learned — dedup is free money:** 4,200 tokens/request removed losslessly before any lossy step; always dedup first.
- **Lesson learned — retention tests are the quality gate:** the 96% score with constraint probes proved the summary was safe; without probes, topics-only summaries look good and drop decisions.
- **Learning — minification and caching must be coordinated:** the cache prefix is frozen; optimization never touches it. A "helpful" reformat is a $3,960/month mistake.
- **Lesson learned — report dollars AND retention:** the board-read number is $45K/year with quality held; neither alone is convincing.

## Repro

```bash
# 1. Capture 500 real requests (provider usage fields) → requests.jsonl
# 2. Run the audit (measure + lever checklist):
bash skills/22-ai-engineering/context-optimizer/scripts/context-audit.sh requests.jsonl
# 3. Baseline cost:
python3 skills/22-ai-engineering/token-efficiency/scripts/token-cost-calculator.py \
  --analyze requests.jsonl --price claude-sonnet-4:3:15:0.30
# 4. After the fix, re-run and compare $/request and hit rate:
python3 skills/22-ai-engineering/token-efficiency/scripts/token-cost-calculator.py \
  --cache requests-after.jsonl --price claude-sonnet-4:3:15:0.30
```
