# Additional Resources — Trade Sizing & Recovery

Deep-dive companion to `SKILL.md`. Load when you need the math, worked cases, or the recovery appendix.

---

## 1. The Expectancy Formula (with retail options worked numbers)

```
Expectancy per trade (in R, where 1R = max loss of the position):
E = p × W − (1 − p) × L
```

- `p` = win probability (anchor to a class base rate; never invent >70%)
- `W` = average win in R (a 1.8× TP on a 1× debit ≈ +0.8R booked at first rung; full 2.5× ≈ +1.5R)
- `L` = average loss in R (≈ 1R when the SL band is honored; >1R when you hold and hope)

**Worked example — momentum fly class at 1R = $300, 1.5% sizing:**

| Scenario | p | Avg W | Avg L | E per trade | Comment |
|---|---|---|---|---|---|
| Disciplined | 0.45 | +1.0R | −0.9R | +0.045R ≈ $14 | thin edge, survives on volume + no blowups |
| Rungs at 1.8× only | 0.50 | +1.2R | −0.8R | +0.20R ≈ $60 | scale-outs convert base hits |
| Discipline dies at −50% | 0.45 | +1.0R | −1.6R | −0.43R ≈ −$129 | same picks, catastrophic sign flip |

**The point:** three traders, same signals, three sizing/exit regimes — a profitable system and a losing system. Sizing/exit is the variable.

**Risk of ruin intuition:** at 1.5% risk per trade, a 10-loss streak costs ~14% of the account — recoverable, and rare (p ≈ 0.45¹⁰ ≈ 0.03% at random; more common when signals are correlated). At 10% risk, the same streak costs ~65% — the account needs +185% to recover. Size for the streak, not for the average.

---

## 2. Loss Triaging — Three Worked Cases (generic)

### Case A — "−55%, 60 DTE, liquid, thesis intact"
- Numbers: cost 3.00, mark 1.35, spread 8%, OI 4,000, underlying above its invalidation level.
- Disposition: **HOLD-WITH-TP** at 2× mark (2.70), level-based SL stays (underlying close below the line = cut).
- Rationale: 60 DTE is enough time for the level to work; liquidity means the exit exists later too. No adds.

### Case B — "−55%, 9 DTE, thin, thesis broken"
- Numbers: cost 2.20, mark 0.95, spread 26%, OI 210, underlying below the level.
- Disposition: **CUT into the next bounce**; if no bounce in two sessions, accept market and exit.
- Rationale: 9 DTE leaves no time for recovery; the spread means every day held donates more. Rolling forward pays theta twice.

### Case C — "−85%, 400 DTE, bid 0.06"
- Disposition: **WRITE-OFF.** Exit fees and spread exceed salvage. Flag "no-TP by construction", remove from the attention set, let it expire.
- Rationale: attention is capital. A dead ticket that gets scanned daily is a tax on the positions that can still win.

---

## 3. Recovery Appendix — The Win-Next Protocol

1. **Book the loss mentally the day it closes.** The dollars are gone; the lesson is the only asset left.
2. **Reset size to base** (or half after two losses). Recovery is a base-rate game, not a comeback bet.
3. **Return to the proven class.** For this operator profile the proven pattern is defined-risk flies/spreads on gate-passed momentum names with GTC TP rungs and level-based invalidation.
4. **No same-name revenge.** 5-session cooldown on any name that was cut, absent a new gate-pass.
5. **Two wins at base → one ladder step.** Then back to base after any loss. Streaks are for booking, not for riding.
6. **Recompute the week.** Recovery is complete when the weekly expectancy table is green on the active class — not when a single trade "got it back".

---

## 4. Scale-Out Ladder Cheat Card

| Position size | Rung 1 | Rung 2 | Runner |
|---|---|---|---|
| 1 lot | 100% at first rung (≥1.8×) or at the level that kills the thesis | — | — |
| 2 lots | 1 lot at ~1.8× | 1 lot at ~2.5× or trail after rung 1 | — |
| 3 lots | 1 at 1.8× | 1 at 2.5× | 1 with invalidation trailed to entry |

**Rule of thumb:** each rung sold ≥ 1× the original debit = the trade is free; the runner is a lottery ticket you paid no rent for. All rungs are GTC sell-to-close orders, sized to the venue's session (RTH-only venues do not fill pre/post).

---

## 5. Session & Venue Notes (execution reality)

- **Thin option books:** use level-based exits, not stop orders — stop orders become market orders into 20–40% spreads.
- **RTH-only orders** (e.g., CORE-session brokerages) do not fill on pre/post prints; overnight "crosses" are information, never executions.
- **Non-agentic venues:** the skill produces ready-to-place specs (symbol, side, price, TIF, session) for one-word human approval.
- **Agentic venues:** standing TPs are pre-authorized once the position exists; entries always require explicit approval.
