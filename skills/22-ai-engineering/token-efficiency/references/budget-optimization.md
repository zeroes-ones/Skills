# Budget Optimization — The Lever Ladder, Projected

## The Ladder (fixed order)

1. **Stabilize the cache** (cheapest, compounds everything else)
2. **Reduce input** — dedup, exclusion, whitespace (lossless)
3. **Compress** — lossy, retention-gated >= 90%
4. **Cap output** — max_tokens per task type + structured output

Never compress before stabilizing the cache. A stable prefix at 1/10 the price beats any compression of an unstable one.

## The `--optimize` Projection

```bash
python3 skills/22-ai-engineering/token-efficiency/scripts/token-cost-calculator.py \
  --optimize requests.jsonl --price <model>:<in>:<out>:<cache>
```

Output: current cost + hit rate, then per-lever monthly savings `[ESTIMATED]`:

| Lever | Modeled as | Defaults |
|-------|-----------|----------|
| L1 Stabilize cache | hit rate → `--cache-target` (0.90) | uncached input shifts to cached reads |
| L2 Reduce input | `--input-trim` (0.20) of uncached input | dedup/exclusion |
| L3 Compress | `--input-trim` of remaining | retention-gated |
| L4 Cap output | `--output-trim` (0.35) of output | max_tokens/structured output |

It recommends fixing caching first when hit rate < 60%.

## Projections Are Not Results

- `[ESTIMATED]` projections model levers — they are planning numbers, not savings.
- After each lever, re-run `--analyze` to measure actuals and confirm retention/quality held.
- Report $/done (not just $/request) and the retention score alongside every projection.

## Ranked Strategy Mix

The ranked plan is: apply L1 first (highest ROI, lowest risk), measure, then L2, L3, L4 in order. A projection that ranks compression above caching is a red flag — the ladder order is fixed for a reason (the anti-patterns in the SKILL.md).

## Worked Decision (from the context-optimizer example)

48K-token support payload, 4% hit rate: `--optimize` ranks cache stabilization first (projected $99/month vs $27 reduce, $22 compress, $29 output at 500 req/day). Applying the ladder in order reached 91% hit rate, -81% $/request, retention 96%.
