# Budget Allocation — Per-Task-Type Tables

## The Rule

Budgets are per-task, not per-payload. Allocate by task type, sum to <= 80% of the model window, and keep a 20% margin for conversation growth and unexpected inclusion.

## Allocation Tables (input/output caps as % of usable window)

| Task type | L1 rules | L2 specs | L3 files | L4 errors | L5 history | Output cap |
|-----------|----------|----------|----------|-----------|------------|-----------:|
| Debugging | 10% | 5% | 30% | 15% | 5% | 1,000 |
| Feature implementation | 10% | 20% | 35% | 0% | 5% | 4,000 |
| Code review | 15% | 10% | 45% | 5% | 0% | 1,500 |
| Chat / support | 20% | 5% | 15% | 5% | 10% | 1,000 |
| Exploration | 10% | 5% | 40% | 0% | 15% | 500 |

Sum of input allocations + 20% margin = 100% of the model window (i.e., input allocations sum to <= 80%).

## Why Task-Aware

- **Debugging needs L4** (error output). Giving a debugging session a feature-style budget (no L4) forces the agent to work from symptom descriptions → wrong fixes (Error Decoder row 1 in the main SKILL).
- **Code review needs L3** (the diff + surrounding source) and almost no history.
- **Chat needs L1** (rules) more than anything — truncating rules in chat is how agents "forget" instructions.

## Budget Config (budget.json)

```json
{
  "debugging":   {"input_cap": 48000, "output_cap": 1000, "margin": 16000},
  "feature":     {"input_cap": 56000, "output_cap": 4000, "margin": 16000},
  "review":      {"input_cap": 60000, "output_cap": 1500, "margin": 16000},
  "chat":        {"input_cap": 44000, "output_cap": 1000, "margin": 16000},
  "exploration": {"input_cap": 48000, "output_cap": 500,  "margin": 16000}
}
```

(For a 200K window: usable = 160K; caps + margin = 160K.)

## Enforcement

- Every call site references the budget config, never hardcoded numbers.
- `token-cost-calculator.py --check-budget budget.json <window>` validates caps + margin <= usable.
- A budget change is a reviewable decision (State Log entry) — budgets are infrastructure, not preferences.
