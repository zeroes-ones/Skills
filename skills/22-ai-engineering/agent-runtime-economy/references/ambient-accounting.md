# Ambient Accounting

What is present before the first task token — and why it is measured first.

## What it includes

| Tier | Example | Paid |
|---|---|---|
| Listing | Skill names + descriptions | Every session |
| Rules | Always-on principles, project rules | Every session |
| Tool schemas | MCP tool definitions and their parameters | Every turn |
| Memory | Injected prior-run context | Every turn it is injected |
| System prompt | Persona, framing | Every turn |

## Why it comes first

Every session pays it whether or not work happens. It is the floor under every other optimisation, so a measurement that ignores it is measured against an unknown. Optimising a skill body while the floor is unmeasured is the most common wasted efficiency effort.

## How to measure

1. Capture the full prompt as the runtime sends it, before any task content.
2. Count tokens per tier with a real tokenizer, not a word count — the two differ by 1.5–2.3× on prose with identifiers.
3. Record it as one number plus its breakdown.

## The measurement trap

Word counts understate tokens; `chars/4` overstates them. Both are common in tooling and both mislead. Use a real BPE tokenizer.

## Failure modes

- **Estimated instead of measured.** An estimate that is off by 2× misdirects the entire optimisation.
- **Listing ignored as "just metadata".** On a large library the listing is often the single largest ambient tier.
- **Tool schemas forgotten.** MCP tool definitions load per turn and are easy to omit from the count.
- **Measured once, never re-measured.** Adding a skill, tool, or memory surface moves the floor.
- **Optimising below the floor.** Reducing a payload that is 3% of the budget while the floor is 40%.
