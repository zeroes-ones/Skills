# Provider Pricing Matrix

> **`[VERIFIED 2026-08-29]`** — figures re-verified against provider pricing pages on this date. Pricing changes quarterly; re-verify at every research loop (RP3) and update the `[VERIFIED]` date. All prices USD per 1M tokens.

> **Snapshot, not law:** This table is a *dated snapshot for worked examples only*. The universal rules that survive price changes live in SKILL.md `Universal Economics` (U1-U8): output ≈ 3-5× input, cached read ≈ 1/10-1/25 of input, ~100× tier spread, lever order reduce → cache → cap. When a figure here is stale, the U-rules still hold — optimize with the rules, quote prices only with the date.

## Input / Output / Cached Read

| Model | Input | Output | Cached read | Cache min prefix |
|-------|------:|-------:|------------:|-----------------:|
| Claude Opus 4 | $15.00 | $75.00 | $1.50 | 1,024 tokens |
| Claude Sonnet 4 | $3.00 | $15.00 | $0.30 | 1,024 tokens |
| Claude Haiku 3.5 | $0.80 | $4.00 | $0.08 | 1,024 tokens |
| GPT-4o | $2.50 | $10.00 | $1.25 | 1,024 tokens |
| GPT-4o mini | $0.15 | $0.60 | $0.075 | 1,024 tokens |
| Gemini 1.5 Pro | $1.25 | $5.00 | $0.3125 | 32,768 tokens |
| Gemini 1.5 Flash | $0.075 | $0.30 | $0.01875 | 32,768 tokens |

## Rules of Thumb (stable across providers)

- **Output is 3-5× input.** Every output token you don't generate saves more than every input token you don't send.
- **Cached read is 1/10 to 1/25 of uncached input.** Cache is the single highest-ROI lever.
- **Batch discounts** (50% off) apply to async/batch endpoints on some providers — for non-interactive workloads, batch pricing halves input+output cost.
- **Model-tier spread is ~100×** (Haiku/Flash vs Opus/Pro). Routing easy tasks to the small model is often the cheapest lever of all.

## Cost Multipliers by Token Class (relative to uncached input = 1.0)

| Token class | Relative cost |
|-------------|--------------:|
| Cached read | 0.04 - 0.10 |
| Uncached input | 1.0 |
| Output | 3 - 5 |

## Verification Protocol

1. Open the provider pricing page (link stored here).
2. Confirm the model, tier, and region match the deployed configuration.
3. Record the three numbers (input/output/cached) with today's date.
4. Tag every downstream calculation `[VERIFIED <date>]`. Anything older than 90 days is `[STALE]` — re-verify before quoting it.

## Where to Look

- Anthropic: https://docs.anthropic.com/en/docs/about-claude/pricing
- OpenAI: https://openai.com/api/pricing/
- Google Gemini: https://ai.google.dev/gemini-api/docs/pricing
