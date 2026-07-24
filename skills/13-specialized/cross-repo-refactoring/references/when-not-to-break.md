# When NOT to Break: Cost-Benefit Analysis Framework

## The Core Question

Every cross-repo breaking change must answer: "Is the benefit worth at least 2x the cost?"

## Cost Estimation

```
Migration Cost = Σ(consumer migration cost) + communication cost + risk cost

Consumer migration cost =
  (call sites × time per site × hourly rate)
  × (1 - automation coverage)
  + PR review time
  + deploy and verify time

Communication cost =
  (announcement time + documentation time + support time)
  × hourly rate

Risk cost =
  probability of incident × impact per incident
  × (1 - safety measure effectiveness)
```

## Benefit Estimation

```
Annual Benefit =
  performance savings/year
  + incident reduction/year
  + developer velocity improvement/year
  + security improvement/year
  + maintenance reduction/year
```

## Decision Matrix

| ROI Ratio | Decision | Action |
|-----------|----------|--------|
| > 3x | PROCEED | Strong ROI. Execute with normal caution. |
| 1.5x - 3x | PROCEED with caution | Tight timeline, escalate blockers quickly. |
| 1x - 1.5x | QUESTION | Can benefit be achieved cheaper? Alternative approaches? |
| < 1x | DO NOT BREAK | Live with current API. Add to tech debt register. |

## Red Flags (Any ONE = Don't Break)

- 3+ unmaintained consumer repos
- External consumers outside your org
- Migration touches authentication/authorization
- Primary benefit is "cleaner code" (unmeasurable)
- Consumer deploy cycle > 3 months
- No way to measure old API usage in production
- No consumer maintainer contact list

## When "Cleaner Code" IS Worth It

"Cleaner code" as a primary motivation almost never justifies a cross-repo break. Exception: the "unclean" code has caused 3+ production incidents in the past 12 months. In that case, the benefit is incident reduction — not cleanliness. Frame it that way.
