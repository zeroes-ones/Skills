# Measurement Protocol — Token Accounting per Level

## The Baseline Contract

An optimization without a measured baseline is a guess with a budget attached (Ground Rule R1). The baseline must:

1. Cover >= 100 real requests (not synthetic).
2. Use provider `usage` fields (input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens) — never word counts.
3. Reproduce the provider bill within ±10% for the sampled period.

## Per-Level Accounting

Token-account the payload by context level (from context-engineering's hierarchy):

| Level | Content | Typical share |
|-------|---------|---------------|
| L1 | Rules / instructions | 2-10% |
| L2 | Specs / static docs | 10-25% |
| L3 | Source files / references | 40-60% |
| L4 | Error output | 0-15% |
| L5 | Conversation history | 5-25% |

Record the share of cost per level — the optimizer targets the largest cost driver first (Decision Tree 1).

## Token-to-Dollar Reconciliation

```
cost = (cache_creation + input - cache_read) × $input/1M
     + cache_read × $cached/1M
     + output × $output/1M
```

Verify the computed total against the provider dashboard. Tag pricing `[VERIFIED <date>]`.

## Tools

- `skills/22-ai-engineering/token-efficiency/scripts/token-cost-calculator.py --analyze requests.jsonl` — baseline analysis.
- `--cache` — hit-rate check.
- `--trend` — period-over-period growth with > 20% alert.
- `--check-budget` — budget validation.

## Tokenizer Discipline

- Count with the provider's real tokenizer (tiktoken for OpenAI models, provider SDK elsewhere).
- Word counts are 10-30% off; tag word-based estimates `[ESTIMATED]` with the error bound.

## Ledger Output

A per-level token ledger (level → tokens → $ → share) committed with the optimization. The ledger is the before/after proof.
