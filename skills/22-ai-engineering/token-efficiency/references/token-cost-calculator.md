# Token Cost Calculator — Formulas and Worked Examples

> Deep knowledge for `scripts/token-cost-calculator.py` and manual cost modeling. All pricing figures `[VERIFIED 2026-08-29]` against provider pricing pages; see `provider-pricing-matrix.md` for the table.

> **Formulas are universal; prices are snapshots.** The formulas, ratios, and worked-example *methods* below stay correct regardless of provider pricing. The absolute dollar figures are `[VERIFIED 2026-08-29]` examples — re-verify before quoting, and prefer the relative rules (SKILL.md `Universal Economics` U1-U8: output ≈ 3-5× input, cached ≈ 1/10-1/25 of input, ~100× tier spread).

## Core Formula

```
request_cost = (cache_creation_tokens + input_tokens - cache_read_tokens) × price_input
             + cache_read_tokens × price_cached_read
             + output_tokens × price_output
```

- **cache_creation_tokens**: billed at the **uncached input rate** (the first time a prefix is cached).
- **cache_read_tokens**: billed at the **cached rate** (1/10 to 1/25 of uncached, provider-dependent).
- **output_tokens**: billed at the **output rate**, which is 3-5× the input rate on most providers — the most expensive token class.

## Worked Example — Cache Economics

A 50,000-token request on Claude Sonnet 4 (`$3.00/M` input, `$15.00/M` output, `$0.30/M` cached read):

| Scenario | Cost |
|----------|------|
| Fully uncached (50K input) | $0.150 |
| Fully cached read (50K @ cached rate) | $0.015 |
| Cache miss + cache creation (50K @ input rate, first request) | $0.150 |
| Cache creation amortized over 20 requests (50K creation once + 19×50K cached reads) | ($0.150 + 19×$0.015)/20 = **$0.02175/request avg** |

**Insight:** a stable prefix pays for its creation on the second request, then compounds. A single byte change in the prefix resets the entire cache — every request pays the uncached rate until the new prefix stabilizes.

## Worked Example — Word vs Token

A code-heavy prompt that is 30,000 "words" tokenizes to ~38,000-42,000 tokens (code, whitespace, and identifiers tokenize 20-40% above word count). Budgeting on words under-provisions by 27%:

```
planned: 30,000 words ≈ 30,000 tokens → $0.09/request @ $3/M
actual:  40,000 tokens                     → $0.12/request (+33%)
```

At 300,000 requests/month the 33% error costs **~$9,000/month** of unplanned spend — and the overflow may trigger truncation/retry behavior that adds another 20% of requests.

## Worked Example — Output Cap Payback

Chat endpoint, no `max_tokens`, average output 2,000 tokens vs a 1,000 cap after optimization:

```
saved per request: 1,000 output tokens × $15/M = $0.015
at 20,000 chats/month: $300/month direct + latency + truncation-churn savings → ~$2,100/month total
```

Output tokens are the highest-margin savings per token because they are priced 3-5× above input.

## $/done (Cost per Successful Task)

```
$/done = total_cost(task_type) / successful_tasks(task_type)
```

Track `$/done`, not `$/request`. A cheap path that fails 18% of the time and retries on the expensive model can be 12% *more* expensive per done while looking 40% cheaper per call.

## Token-to-Dollar Quick Reference (per 1M tokens, USD)

| Model | Input | Output | Cached read | Cache min prefix |
|-------|------:|-------:|------------:|-----------------:|
| Claude Sonnet 4 | $3.00 | $15.00 | $0.30 | 1,024 tokens |
| Claude Opus 4 | $15.00 | $75.00 | $1.50 | 1,024 tokens |
| GPT-4o | $2.50 | $10.00 | $1.25 (cached input) | 1,024 tokens |
| GPT-4o mini | $0.15 | $0.60 | $0.075 | 1,024 tokens |
| Gemini 1.5 Pro | $1.25 | $5.00 | $0.3125 | 32,768 tokens |

> **Cache minimum prefix:** Anthropic/OpenAI cache ≥ 1,024 tokens; Gemini's implicit caching requires ≥ 32K tokens. Under the minimum, caching silently never engages — a common "why isn't caching working?" cause.
