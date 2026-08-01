# LEAPS Behavioral Pitfalls

> **Portability target:** Spec-level. Behavioral concepts are universal — detection rules are implementable in any trading journal.

## The LEAPS Paradox

LEAPS are mathematically superior to shares for capital efficiency (4:1 leverage at 0.80+ delta, [VERIFIED]). Yet most LEAPS traders lose money. The problem is NOT the math — it's what traders do with the leverage.

## The Five LEAPS-Specific Killers

| Bias | LEAPS Manifestation | Cost | Fix |
|------|-------------------|------|-----|
| Leverage Induced Overconfidence | "4:1 leverage means I can control 4× the shares." Result: 6 positions at 4:1 = 24:1 effective leverage. A 4% market drop = -16% portfolio. | $5K-$25K drawdown — the leverage that amplifies gains amplifies losses identically | **Size LEAPS by DELTA DOLLARS, not contract count.** 1 DITM LEAPS call (0.85Δ × $15,000 notional) = $12,750 delta exposure. Compare to your account size — this is 5 contracts' worth of delta risk, not 1 contract |
| DTE Complacency | "I have 18 months — there's plenty of time for this to work." Stock drops 25% with DTE 450. The LEAPS loses 45%. "Still time." At DTE 90, stock is flat vs. original — but theta decay + IV changes cost 35% of premium. | $3K-$8K per position — DTE complacency turns "patient investors" into bag holders | **Set a TIME-BASED exit, not just a price-based exit.** If the thesis hasn't materialized by DTE 180 (even if the position isn't at max loss), exit. Time expiry is a real cost — the LEAPS clock is always ticking |
| Extrinsic Decay Denial | "$3.00 of the $15.00 premium is extrinsic — that's only 20%, acceptable." Over 18 months, that $3.00 decays to zero even if the stock is flat. The stock must rise 20%+ just to offset extrinsic decay. | $1K-$3K per contract in hidden time cost — extrinsic is a guaranteed loss that "cheap" LEAPS amplify | **Model extrinsic as a guaranteed cost, not a maybe.** LEAPS with > 15% extrinsic-to-premium ratio: the stock must rise > extrinsic% just to break even. This is the hidden cost of "cheaper" LEAPS |
| Missed Dividend Accumulation | Stock yields 2.5%, held for 2 years via LEAPS. Missed dividends = 5% of notional. At 4:1 leverage, this is 20% of premium — or $2,000 on a $10,000 LEAPS position. | $1.5K-$3K per LEAPS position over 2 years — dividends quietly compound against you | **Quantify dividend gap before entry.** High-yield (> 3%) stocks rarely work for LEAPS replacement. The missed dividends are a first-order cost that leverage amplifies |
| The Roll-or-Die Fallacy | LEAPS at DTE 60, stock at breakeven. "I'll roll to another 18-month LEAPS and give it more time." Rolling locks in the loss and commits new capital to a thesis that failed. Double-down disguised as patience. | $2K-$5K per rolled position — rolling a losing LEAPS without a fresh thesis is just doubling down | **Roll ONLY with a new, independently valid thesis.** "Giving it more time" is not a thesis. If you wouldn't enter this LEAPS today at current prices, don't roll |

## Detection Rules for LEAPS Journals

| Rule | Detection | Alert |
|------|-----------|-------|
| Over-leverage | Sum of (Δ × notional) across all LEAPS > 150% of account equity | "LEAPS Leverage Alert: Portfolio delta exceeds 1.5× account. Equivalent to 150%+ equity exposure." |
| Extrinsic trap | Any LEAPS with extrinsic/premium > 20% AND held > 6 months AND flat/down | "Extrinsic Decay Warning: LEAPS extrinsic is consuming premium. Required stock rise to break even: X%." |
| Dividend gap | Stock dividend yield > 2.5% AND held as LEAPS replacement | "Dividend Alert: Missing $(amount) in dividends over holding period. Consider shares for high-yield stocks." |
| DTE cliff | DTE < 120 on any LEAPS without a roll/exit plan | "DTE Warning: LEAPS approaching acceleration zone. Time decay will accelerate rapidly at DTE < 90." |
| Serial rolling | More than 1 roll on same underlying within 12 months | "Double Roll Alert: Same underlying rolled twice. Is the thesis valid or are you avoiding a realized loss?" |

## The Most Important Test

**Weekly check:** "If I had cash instead of this LEAPS position, would I buy it today at the current market price?"

If the answer is no — exit. The premium paid in the past is irrelevant. Only the forward expected return matters.

The sunk cost fallacy is the #1 LEAPS account destroyer. The market doesn't remember what you paid. Neither should you.
