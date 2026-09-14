# Backtest Example — agent-runtime-economy

> **Hypothetical demonstration scenario** for skill-runner validation.
> No production data is claimed. Every figure is **[COMPUTED]** from the explicitly stated
> **[ESTIMATED]** assumptions below.

## Assumptions ([ESTIMATED])

- Scenario: a coding agent runs 800 sessions a month against a 200k-token window.
- Ambient floor, routing miss rate, and retry rate are illustrative inputs.
- Blended token price $12 per 1M tokens.

| Parameter | Value | Tag |
|---|---|---|
| Sessions per month | 800 | [ESTIMATED] |
| Ambient floor (listing + rules + tool schemas) | 43,000 tokens | [ESTIMATED] |
| Loaded skill (compiled) | 3,100 tokens | [ESTIMATED] |
| Baseline routing rank-1 | 72.8% | [COMPUTED] |
| Cost of a routing miss (wrong load + redo) | 6,200 tokens | [ESTIMATED] |
| Baseline turns per session | 12 | [ESTIMATED] |
| Turns spent after convergence (no stop rule) | 3 | [ESTIMATED] |
| Blended token price per 1M | $12 | [ESTIMATED] |

## Computed scenario ([COMPUTED])

**Where the budget actually goes** (per session, ambient paid every turn):

- Ambient floor: 43,000 × 12 turns = 516,000 tokens
- Loaded skill: 3,100 × 12 = 37,200 tokens
- Routing misses: 27.2% × 6,200 = 1,686 tokens average
- Post-convergence turns: 3 × (43,000 + 3,100) = 138,300 tokens

Per session: ~693,000 tokens = **$8.32**. Monthly (800 sessions): **$6,656**.

**Ranked by size:** ambient 74% · post-convergence 20% · loaded skill 5% · routing misses 0.2%.

This is the finding: **the skill body — the thing teams optimise — is 5% of the bill.** Ambient context and turns-after-convergence are 94%.

**With the three levers applied:**

| Lever | Change | Effect |
|---|---|---|
| Trim ambient listing (routing signatures, ~40 tokens/skill) | 43,000 → 15,000 | −65% on the dominant line |
| Stop rule (ends 3 turns early) | 12 → 9 turns | −25% of turns |
| Routing precision (72.8% → 85%) | misses 27.2% → 15% | Small absolute, but removes redo work |

Per session: (15,000 × 9) + (3,100 × 9) + miss ≈ 163,800 = **$1.97**.
Monthly: **$1,576** vs $6,656 — **$5,080/month** avoided, ≈76%.

## Best case

The ambient floor is measured first, so the team spends its effort on the 74% line instead of the 5% line. The stop rule ends converged sessions early, and routing precision is tracked as a first-class efficiency metric rather than a quality afterthought.

## Worst case

The team optimises skill bodies for a quarter. Sessions get 5% cheaper and everyone concludes the problem is hard. Meanwhile the ambient floor is never measured, sessions still run past convergence, and the actual bill is untouched. The efficiency work was real; it was aimed at the wrong line.

## Learnings / key takeaways

1. The ambient floor dominates and is measured last — the single most expensive inversion in agent engineering.
2. Turns-after-convergence is the second-largest line and the cheapest to fix; it needs only a stop rule.
3. Optimising the loaded payload is a rounding error by comparison.
4. Routing misses look like quality bugs and are priced like efficiency bugs.
5. A budget that is raised whenever it binds discards the only signal it produced.

## What this does not show

- No real session traces underlie these numbers; they are stated assumptions for arithmetic.
- Token counts depend heavily on the runtime and host; the *ranking of levers* transfers, the absolute figures do not.
- Per the repo's own rule, retrieval and cost claims are **[COMMON-PRACTICE]** hypotheses until measured against a live baseline.
