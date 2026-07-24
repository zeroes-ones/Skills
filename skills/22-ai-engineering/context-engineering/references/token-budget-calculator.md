# Token Budget Calculator

## Overview

Formulas, heuristics, and tools for computing optimal token budgets across model providers.

## Model Window Reference

| Model | Context Window | Max Usable (80%) | Input $/1M tokens | Cached Input $/1M |
|-------|---------------|------------------|-------------------|-------------------|
| Claude 3.5 Sonnet | 200,000 | 160,000 | $3.00 | $0.30 |
| Claude 3 Opus | 200,000 | 160,000 | $15.00 | $1.50 |
| GPT-4o | 128,000 | 102,400 | $2.50 | $1.25 |
| GPT-4 Turbo | 128,000 | 102,400 | $10.00 | $5.00 |
| Gemini 1.5 Pro | 1,000,000 | 800,000 | $1.25 | $0.31 |
| Gemini 1.5 Flash | 1,000,000 | 800,000 | $0.075 | $0.01875 |

## Default Allocation Formula

```
usable_tokens = model_window * 0.80
L1_budget = usable_tokens * 0.03     # 3% — Rules (always)
L2_budget = usable_tokens * 0.10     # 10% — Specs
L3_budget = usable_tokens * 0.35     # 35% — Source files
L4_budget = usable_tokens * 0.05     # 5% — Errors
L5_budget = usable_tokens * 0.07     # 7% — History
buffer     = usable_tokens * 0.20     # 20% — Reserved
```

## Task Complexity Multipliers

**Simple tasks** (single file edit, typo fix):
- L3 multiplier: 0.6x (fewer source files needed)
- L4 multiplier: 0.0x (no error context)
- L5 multiplier: 0.5x (less history needed)

**Standard tasks** (feature implementation, moderate refactor):
- Use default allocations

**Complex tasks** (multi-file refactor, debugging, architecture changes):
- L3 multiplier: 1.3x (more source context)
- L4 multiplier: 2.0x (full error context)
- L5 multiplier: 1.5x (longer conversations)
- Buffer: reduce to 10%

## Cost Estimation Formula

```
cost_per_request = (input_tokens * input_price_per_1M / 1_000_000) +
                   (cached_tokens * cached_price_per_1M / 1_000_000) +
                   (output_tokens * output_price_per_1M / 1_000_000)

monthly_cost = cost_per_request * requests_per_day * 22_working_days
```

## Token Counting Tools

- **Anthropic:** `tokencount` Python library or `claude-tokenizer` npm package
- **OpenAI:** `tiktoken` library with `cl100k_base` encoding
- **Google:** Vertex AI `count_tokens` API endpoint
- **Generic:** `ttok` CLI tool (trim, count, truncate text by token count)

## Quick Sanity Checks

1. If L1 > 8K tokens: rules files need pruning
2. If L2 > 20K tokens: specs need summarization
3. If any single L3 file > 8K tokens: consider signature-only inclusion
4. If L4 > 10K tokens: error output needs aggressive trimming
5. If L5 > 15K tokens: conversation summarization is overdue

## Budget Visualization Template

```
L1: ████░░░░░░░░░░░░░░░░  4,800 / 160,000 (3%)
L2: ██████████░░░░░░░░░░ 16,000 / 160,000 (10%)
L3: ████████████████████ 56,000 / 160,000 (35%)
L4: ████░░░░░░░░░░░░░░░░  8,000 / 160,000 (5%)
L5: ██████░░░░░░░░░░░░░░ 11,200 / 160,000 (7%)
BUF:████████████████████ 32,000 / 160,000 (20%)
     ────────────────────
TOTAL:                  128,000 / 160,000 (80%)
```
