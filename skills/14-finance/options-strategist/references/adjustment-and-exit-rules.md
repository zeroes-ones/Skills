# Adjustment and Exit Rules

## Purpose
Standardized exit, adjustment, and stop-loss rules for all options strategies. These rules are designed to remove emotion from trade management by providing concrete, quantifiable triggers for every possible scenario. Rule #1: plan the exit before entering the trade.

---

## Profit Targets by Strategy Type

| Strategy | Profit Target | Rationale |
|----------|--------------|-----------|
| Credit Spreads (bull put, bear call) | 50% of max credit | Captures half the premium early. Remaining 50% requires doubling the unrealized gain with proportionally more risk. Redeploy freed capital. |
| Iron Condors | 25% of max credit | Condors have 4 legs with 4 commission costs; closing at 25% locks in a meaningful gain while avoiding late-stage gamma risk. [COMMON-PRACTICE] |
| Naked Puts / CSPs | 50–80% of max profit (premium) | Close at 50% for redeployment, 80% if no better opportunities exist. Remaining 20% isn't worth the theta remaining when > 14 DTE. |
| Naked Calls | 50% of max profit | Higher tail risk than naked puts; capture profit early to avoid catastrophic gap moves. |
| Covered Calls | 50–80% of premium | Close at 50% for standard management. Close at 80% with > 14 DTE remaining. |
| Debit Spreads (bull call, bear put) | 50% of max profit | Remaining profit requires doubling the gain. Debit spreads bleed theta — waiting for 100% is statistically negative expectation. |
| Straddles / Strangles (long) | 25% of debit paid | These are low-POP strategies. Take profits when they appear — large winners are rare and must be captured. |
| Calendars / Diagonals | 25–50% of max profit | Complex profit profiles; close at 25% if achieved early, hold to 50% if near expiration with position behaving. |
| Butterflies | 30–50% of max profit | Butterfly profits are fragile and concentrated near expiration at the center strike. Capture gains before theta erosion on the long wings. |
| Ratio Spreads | 50% of credit received | Ratio spreads have undefined risk on the over-weighted side. Close early to avoid the tail scenario where the ratio amplifies losses. |

[VERIFIED] The 50% profit-taking rule for credit spreads is back-tested and widely adopted. Studies show that closing credit spreads at 50% max profit and redeploying capital to a new 30–45 DTE spread produces a higher annualized return than holding to expiration, even accounting for additional commissions.

---

## Stop-Loss Rules by Strategy Type

| Strategy | Stop-Loss Trigger | Dollar Example |
|----------|------------------|----------------|
| Credit Spreads | 2× credit received | Collected $1.50 → close at $3.00 loss. Max loss is $3.50 on a $5-wide spread — the 2× stop leaves $0.50 of risk buffer before structural max loss. |
| Debit Spreads | 100% of debit paid | Paid $2.00 → close at $0.00 value (total loss). Debit spreads cannot lose more than the debit paid — the stop IS the max loss. |
| Iron Condors | 2× credit received across the entire position | Collected $2.00 → close at $4.00 debit. OR close if any short strike is breached and holds for 2 consecutive days. |
| Naked Puts | 3× credit received, OR stock drops below 200-SMA | Collected $1.00 → close at $3.00. The 3× stop reflects the undefined risk nature — wider stop needed to avoid whipsaw, but still caps catastrophic loss. |
| Naked Calls | 2× credit received (tighter than puts due to unlimited upside risk) | Collected $1.00 → close at $2.00. Unlimited upside = no structural cap — the stop must be tighter. |
| Covered Calls | Underlying drops 10% below cost basis | Cost basis $95 → close entire position (buy back call + sell shares) at $85.50. Thesis broken — do not continue selling calls on a falling asset. |
| CSP (pre-assignment) | Stock drops 5% below strike | Strike $95, stock at $90.25 → close CSP for loss. Assignment means owning at 5% above market. |
| Calendars / Diagonals | 2× debit paid | Paid $1.50 → close at $3.00 loss. Theta decay and vega are the edges; neither compensates for large directional moves. |
| Butterflies | 100% of debit paid (or 2× credit for iron butterfly) | Paid $0.50 → close at $0.00. Butterfly gains are concentrated — if it's not working near expiration, it won't work. |

[COMMON-PRACTICE] Stop-losses should be set as GTC (Good-Til-Cancelled) orders immediately after entry. Mental stops fail under pressure. A $3.00 GTC stop on a $1.50 credit spread executes automatically — no emotion, no hesitation, no "maybe it'll come back."

---

## Time-Based Exit Rules

| Rule | Applies To | Trigger | Rationale |
|------|-----------|---------|-----------|
| 21 DTE Rule | All credit spreads, iron condors, short strangles | Close all positions at 21 DTE | Gamma risk accelerates dramatically in the final 3 weeks. The remaining theta is not worth the gamma exposure. [VERIFIED] |
| 45 DTE Rule | Debit spreads | Close at 21–30 DTE if not at 30%+ profit | Debit spreads lose value to theta daily. The probability of recovery after 30 DTE declines rapidly. |
| Pre-Earnings Rule | All strategies with undefined risk, all credit spreads | Close all positions 2 trading days before earnings | Gap risk is unbounded. Defined risk protects against intraday moves, not overnight gaps. |
| Pre-FOMC Rule | All strategies on rate-sensitive underlyings | Close or reduce position size by 50% 1 day before FOMC | Rate decisions move entire markets. Neutral strategies on index ETFs are especially vulnerable. |
| Expiration Day Rule | All short options | Close by 3:30 PM ET on expiration Friday | Pin risk. The final $0.05 of premium is not worth the overnight gap risk. Never hold short options through expiration. |
| Holiday Rule | All neutral strategies | Close 1 day before extended market closures (3+ day weekends) | Multi-day gaps without ability to manage create outsized risk relative to theta decay during the closure. |
| 7-Day Rule (aggressive) | Short-dated credit spreads (7–14 DTE) | Close at 7 DTE regardless of P&L | Gamma risk is extreme below 7 DTE. A 0.05 delta short strike can flip to 0.90 delta on a 2% intraday move. |

---

## Rolling Rules

Rolling means closing the current position and opening a new one at a different expiration (and possibly different strikes) simultaneously.

### When to Roll (Valid Reasons)

| Scenario | Action | Validation |
|----------|--------|-----------|
| Short strike tested with 14+ DTE | Roll to next month, same strikes, for net credit | Net credit ≥ $0.05. If net debit is required, either close for loss or let expire — do NOT pay to maintain. |
| Profit target achieved early (e.g., 50% in 7 days) | Roll to next month, wider strikes, for additional credit | The rapid profit means IV has likely dropped. Widen strikes to maintain similar credit levels. |
| Covered call ITM, want to keep shares | Roll up and out: higher strike, further expiration | Net credit ≥ $0.05. If stock has rallied significantly, a small debit roll may be acceptable to avoid regret on capped gains. |
| Rolling to avoid earnings | Roll past earnings date | Only if net credit ≥ $0.05 and the new expiration is > 21 DTE after earnings. |

### When NOT to Roll (Invalid Reasons)

| Scenario | Why Not | Correct Action |
|----------|---------|----------------|
| "The trade will come back" (thesis broken) | Rolling a broken thesis to delay a loss is loss-amplification, not management | Close for loss. Accept the loss and move to the next trade. |
| Rolling for a debit to "save" the position | Paying to maintain a loser compounds losses | Close for loss. The debit roll adds new capital to a failing position. |
| "Just one more month" (3rd consecutive roll) | After 2 rolls, the position has been wrong for 60–90 days | Close the position. The market is telling you the thesis was wrong. |
| Rolling to "average down" the cost basis | This is the options equivalent of doubling down on a losing stock | Close the position. Averaging down on options is worse than on stocks — theta amplifies the error. |

[COMMON-PRACTICE] A valid roll produces a net credit of $0.05 or more and does not widen the overall risk beyond the original position's max loss. If a $5-wide spread had a $350 max loss, any roll that increases the total capital at risk beyond $350 is invalid — close instead.

---

## Adjustment Hierarchy (Priority Order)

When a position is threatened (short strike approached or breached), follow this hierarchy:

```
Level 1: DO NOTHING
  → Position is within profit zone. Price moving toward but not at short strike.
  → Intraday tests that reverse before close do not require action.
  → Condition: Underlying has NOT closed beyond short strike for 2 consecutive days.

Level 2: ROLL UNTESTED SIDE
  → One side threatened, other side safe.
  → Roll the safe side closer to collect additional credit.
  → Roll for net credit ≥ $0.05. Net credit reduces max loss on the threatened side.
  → Example: Iron condor call side tested. Roll put spread up (sell higher put, buy higher protective put) for $0.30 credit. Total position credit increases, breakevens improve on the call side.

Level 3: ROLL ENTIRE POSITION
  → Both sides uncomfortable but not breached.
  → Roll all legs to next expiration, same or slightly wider strikes.
  → Must be for net credit. If net debit is required, skip to Level 4.
  → Use only if thesis is intact but more time is needed.

Level 4: CLOSE THE POSITION
  → Short strike breached and holding for 2+ days.
  → OR roll would require net debit.
  → OR adjustment would increase total capital at risk beyond original max loss.
  → Accept the loss. Preservation of capital for the next trade is the priority.
```

### The Golden Rule of Adjustments
**Never adjust if the adjustment requires committing more capital than the original maximum loss of the position.** [VERIFIED] If a $5-wide credit spread had a $350 max loss and the proposed adjustment would add $200 in new risk (total now $550), close the original position for whatever loss it has incurred. Adding capital to a losing position is the behavioral finance error known as " escalation of commitment" — it is the single most expensive mistake options traders make.

---

## UOA-Informed Exits

| UOA Signal | Action | Priority Override |
|------------|--------|-------------------|
| Sudden large flow (>$1M notional in < 5 minutes) OPPOSITE your position | Exit immediately regardless of P&L | Overrides ALL other exit rules including profit targets and stop-losses |
| Opening activity confirms your direction (UOA aligns with position) | Hold to original profit target; no early exit needed | Confirmation signal — standard exit rules apply |
| UOA flow fades (volume drops below 20-day average for 3+ consecutive days) | Consider early exit at next profit-target milestone | Weakening flow = weakening edge. Tighten stops by 25%. |
| Multi-leg UOA opposite your structure detected | Exit immediately | Smart money is building the opposite position at scale |
| Sector-wide flow shift (3+ tickers in same sector show opposite flow within 60 minutes) | Exit all positions in that sector | Sector rotation overrides individual ticker thesis |

[INFERRED] UOA-informed exits should never be ignored. When institutional flow reverses at scale (>$1M notional in < 5 minutes), the probability that retail's thesis remains correct drops below 30%. Exiting immediately, even at a loss, preserves capital for re-entry when the new flow direction becomes clear.

---

## Post-Trade Review Checklist

After every closed trade, document:
1. **Entry date, strategy, strikes, credit/debit, DTE** — baseline data
2. **Exit date, P&L, % of max profit captured** — outcome data
3. **Was the exit rule followed?** If not, why not? — discipline audit
4. **Did UOA emerge during the trade that conflicted?** — signal review
5. **What would have happened if held to expiration?** — counterfactual for calibration
6. **Net return on capital deployed (%):** (P&L / Max Loss) × 100 — performance metric

[COMMON-PRACTICE] Traders who journal every trade and review monthly outperform those who don't by an estimated 15–20% annually. The review process identifies recurring errors (exiting too early, ignoring stops, over-sizing) that cost more than any single trade.
