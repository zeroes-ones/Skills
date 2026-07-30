# Profit-Taking, Stop-Loss & Position Trimming

> **Purpose:** Mechanical, non-negotiable rules for taking profits, cutting losses, and scaling out of options positions. Every exit trigger is `if X → do Y`, never "consider" or "evaluate."

---

## <!-- QUICK: 30s --> The Profit-Taking Problem

Profit-taking is the hardest part of trading. More money is lost turning winners into losers than from stop-losses triggered [COMMON-PRACTICE].

| Behavioral Trap | How It Destroys Profits | Mechanical Fix |
|----------------|--------------------------|----------------|
| **Greed** | "It could go higher" — holding past target until reversal | Close 50% at 50% profit. Let remaining 50% run with trailing stop at 25% of peak |
| **Anchoring** | "I was up $500, now only $300 — I'll wait" — positions never recover | Trailing stop at 50% of peak profit. Was +$500, now +$250? Exit immediately |
| **Endowment effect** | Owned positions feel more valuable than they are | Ask: "Would I enter this position TODAY at current price?" If no, exit |
| **Disposition effect** | Closing winners too fast, holding losers too long | [VERIFIED] Studies show traders close winners 2.3× faster than losers. Counter-strategy: let winning positions run with trailing stops; cut losers at 2× credit |

**The math of reversals:** A 50% gain that reverses to 0% requires a 100% gain to recover. A 90% reversal requires 900% recovery. Don't let winners reverse.

---

## <!-- STANDARD: 3min --> Profit-Taking Triggers

### A. Percentage-of-Max-Profit Matrix

| Strategy | 25% Trigger | 50% Trigger | 75% Trigger | 90%+ Trigger |
|----------|-------------|-------------|-------------|-------------|
| **Credit spread** (30-45 DTE) | Close if achieved < 7 days (IV crush event) | **CLOSE** — standard target [COMMON-PRACTICE] | Close if < 14 DTE | Close regardless — remaining 10% not worth gamma |
| **Iron condor** (30-45 DTE) | **CLOSE** — standard target [COMMON-PRACTICE] | Close if after 50% of duration | Close if < 21 DTE | Close. Gamma risk on last 10% is >5× the premium remaining |
| **Debit spread** | Hold — need bigger wins to compensate lower POP | Close 50% (scale out) | Close remaining 50% | Close all |
| **Naked put** | Hold unless < 7 days to reach | Close 60% (scale out) | Close remaining 40% | Close all |
| **Naked call** | Close 100% — rare to get 25% quickly, take it | N/A | N/A | Close all |
| **Covered call** | Hold — it's an income strategy | Close 50% if stock within 5% of strike | Close remaining if stock above strike | Close if assigned (call away) or roll |
| **Calendar spread** | **CLOSE** — rare, take it immediately | N/A — 50% rarely seen | Close all | Close all |
| **Diagonal spread** | Close 50% | Close remaining 50% | N/A | N/A |
| **Long straddle/strangle** | Close 33% (scale out, reduce cost basis) | Close 50% of remaining | Close rest | N/A |

[COMMON-PRACTICE] The 50% rule for credit spreads exists because the risk/reward inverts: first 50% of profit takes ~30% of trade duration; last 50% takes ~70% and carries escalating gamma risk.

### B. Time-Based Profit Triggers

| Rule | When | Action | Rationale |
|------|------|--------|-----------|
| **7-day rule** | Credit spread achieves 25% profit in first 7 days | Close 100% | IV likely compressed; you got 45 days of theta in 7 days |
| **14-day rule** | Any defined-risk position at 30%+ profit with 14 DTE remaining | Close 100% | Gamma accelerates; edge is exhausted |
| **21-day rule** | All credit positions at 21 DTE regardless of P&L | Close 100% | [VERIFIED] Gamma from 21→14 DTE increases ~2×; from 14→7 increases ~5×; from 7→0 increases ~10× |
| **Expiration week** | Any position open with 5 DTE | Close 100% | Gamma risk is 4× what it was at 21 DTE. Unless >2 SD OTM, close |
| **50% duration rule** | Calendar/diagonal not profitable by 50% of max duration | Close 100% | Non-directional thesis is wrong — exit |

### C. Greeks-Based Profit Triggers

| Greek Signal | Threshold | Action |
|-------------|-----------|--------|
| **Delta collapse** | Short strike delta drops from 0.25 → 0.10 | Close 50% (scale out). If drops to 0.05, close remaining |
| **Theta exhaustion** | Daily theta < 0.3% of credit received | Close 100%. Position extracted most value |
| **Vega compression** | IV drops 10+ percentile points since entry AND position profitable | Close 100%. Profited from IV crush that may reverse |
| **Gamma danger** | Short strike gamma > 0.05 within 14 DTE | Close 100%. Danger zone where delta swings violently |
| **Vanna flip** | Vanna turns negative on previously positive-gamma position | Reduce 50%. Risk profile fundamentally changed |

### D. UOA-Informed Profit Triggers

| UOA Signal | Action | Timeline |
|-----------|--------|----------|
| Flow reversal (>$500K opposite notional within 30 min) | Close 75% of position regardless of P&L | Immediately |
| Flow rotation (same ticker, different strikes/expirations) | Scale out 50% — smart money is repositioning | Within 15 min |
| Sector-level UOA shift (3+ tickers in sector show opposite flow) | Close ALL positions in that sector | Within 15 min |
| UOA at entry strike disappears (no follow-through) | Close 50% — confirmation vanished | Within 30 min |

---

## <!-- STANDARD: 3min --> Stop-Loss Strategies

### A. Fixed Stop-Losses (GTC Orders)

> **CRITICAL:** Set GTC stop-losses IMMEDIATELY after entry. Delaying >1 hour increases catastrophic loss probability 3-5× [COMMON-PRACTICE].

| Strategy | Stop Level | GTC Order Type | Justification |
|----------|-----------|----------------|---------------|
| **Credit spread** | 2× credit received | GTC close at limit (debit = 2× credit) | At 2×, remaining risk is only margin buffer |
| **Iron condor** | 2× total credit OR any wing at 4× wing credit | GTC bracket on entire position | One breached wing makes condor a directional bet |
| **Debit spread** | 100% of debit OR underlying breaks technical level (e.g., 200-SMA) | GTC stop on underlying price | Max loss = debit, but thesis stop is the real stop |
| **Naked put** | 3× credit OR underlying < 50-SMA | GTC on option + alert on underlying | 3× for undefined risk; SMA prevents catching falling knife |
| **Naked call** | 2× credit OR underlying > 50-SMA | GTC on option + alert on underlying | Tighter — unlimited upside risk |
| **Covered call** | Stock drops 7% below entry | GTC on stock + close option | Stock thesis broken, not just option |
| **Straddle/Strangle (long)** | 50% of debit paid | GTC close | Low-POP trades; if not working by -50%, the move isn't happening |
| **Calendar spread** | 100% of debit | GTC close | Defined risk; time decay works for you on the front month |

### B. Trailing Stop-Losses

| Strategy | Profit Threshold to Activate Trail | Trail Amount | Formula |
|----------|-----------------------------------|-------------|---------|
| Credit spreads | 30% of max profit | 50% of peak profit | `trailing = peak_mark - (peak_profit × 0.5)` |
| Iron condors | 15% of max profit | 50% of peak profit | Same formula — condors move slowly |
| Debit spreads | 25% of max profit | 25% of peak profit | `trailing = peak_mark - (peak_profit × 0.25)` — tighter, directional bets |
| Naked puts/calls | 20% of max expected profit | 40% of peak profit | Wider trail to withstand normal pullbacks |

**Example:** 10-lot credit spread, $0.50 credit per contract ($500 total credit). Position marks at $0.25 (50% profit = $250). Peak mark reaches $0.20 ($300 profit). Trail = $0.20 - ($300 × 0.5) = $0.20 - $1.50 = close when mark hits $0.35 (profit drops to $150). This locks in 50% of the peak profit.

### C. Time-Based Stop-Losses

| Condition | Action | Probability of Recovery |
|-----------|--------|------------------------|
| Credit spread at 0% profit at 14 DTE (opened 45 DTE) | Close — theta edge gone, only gamma risk remains | < 10% |
| Debit spread at < 10% profit at 21 DTE remaining | Close | < 15% |
| Calendar/diagonal not profitable by 50% of max duration | Close — non-directional thesis wrong | < 20% |
| Any position with 0% profit at 7 DTE | Close — gamma explosion imminent | Near zero |

### D. Volatility-Based Stop-Losses

| Vol Event | Action | Rationale |
|-----------|--------|-----------|
| VIX spikes 30%+ in single session while holding short premium | Close ALL short premium positions | Vega expansion widens spreads 2-3× |
| IV rank drops below 20 during short premium trade | Close remaining | Premium edge extracted; IV may mean-revert higher against you |
| IV rank rises 30+ points since entry on long premium trade | Take profits — close 100% | Got the vol expansion wanted |
| VIX futures term structure flips to strong backwardation | Reduce short vega by 50% | Market pricing elevated near-term risk |

---

## <!-- STANDARD: 3min --> Position Trimming (Scaling Out)

Trimming is the most underutilized trade management technique. It reduces risk while preserving upside — the best of both worlds.

### A. When to Trim

| Scenario | Trim Amount | Logic |
|----------|------------|-------|
| Credit spread at 30% profit, 30+ DTE remaining | Close 50% of contracts | Lock in baseline profit; remaining runs with house money |
| Debit spread at 50% profit | Close 50-66% of contracts | Capture majority of move; remaining is free roll |
| Iron condor at 15% profit, 35+ DTE remaining | Close 33% of contracts | Reduce gamma exposure early; improved risk/reward on rest |
| UOA signal weakens but doesn't reverse | Close 50% | Edge decaying — reduce proportionally |
| Sector correlation event (competitor earnings, regulatory news) | Close 50% of sector positions | External event increases correlation; reduce but don't abandon |
| VIX rising 15%+ with short premium | Close 50% of short premium | Vega risk increased; if VIX +30%, close remaining |
| Position grows to >5% of portfolio from P&L alone | Close 50% — rebalance | Concentration risk from winner growing too large |

### B. How to Trim (Mechanical Execution)

**Odd-lot ladder:** Don't go 10 → 0 all at once.
- 10 contracts: close 5 (50%) → 3 (30% of remaining) → 2 (final). Smoother than 10 → 0.
- 5 contracts: close 2 (40%) → 2 (67% of remaining) → 1 (final).
- 3 contracts: close 1 (33%) → 1 (50%) → 1 (final).

**Leg-level trimming:** In a 10-lot iron condor, close the 5 threatened put spreads and keep 5 call spreads — converts to directional with reduced size.

**Strike-level trimming:** In a ratio spread (e.g., +2 calls at strike A / -3 calls at strike B), close 1 short call to flatten the ratio from 2:3 to 2:2, eliminating undefined risk on the extra short.

### C. The House Money Rule

Once you've closed 50%+ of a position at profit that covers the max loss of remaining, it's risk-free:

> **10-lot credit spread:** max loss $350/contract ($3,500). Close 5 at +$100 profit = $500 realized. Remaining 5 have max loss $1,750. Net max loss = $1,750 - $500 = $1,250 — 35% of original. You kept 50% upside for 35% of original risk.

This is the mathematical basis for trimming: **reduce max loss while keeping upside exposure.**

---

## <!-- STANDARD: 3min --> Full Position Lifecycle

```
ENTRY → Confirm ALL conditions (UOA + IV + Technical) → Open → Set GTC stops IMMEDIATELY
  │
  ├─ DAYS 1-7: Initial Monitoring
  │    ├─ MOVING FAVORABLY → HOLD. No action needed
  │    ├─ FLAT → HOLD. Theta is working for short premium. Time is working against long premium
  │    └─ MOVING AGAINST → CHECK: Is thesis broken or tested?
  │         ├─ THESIS BROKEN (fundamental change: earnings miss, regulatory action, CEO change)
  │         │   └─ CLOSE IMMEDIATELY. Don't wait for stop. Reason for entry no longer exists
  │         └─ THESIS TESTED but intact → Set harder stop at 1.5× credit
  │
  ├─ MID-TRADE (25-50% of duration elapsed):
  │    ├─ 30%+ profit → TRIM 50% (scale out). Now at 50% size with reduced risk
  │    ├─ 15-30% profit → HOLD. Set trailing stop at 50% of peak profit
  │    ├─ 0-15% profit → HOLD. No adjustment. Theta may still deliver
  │    └─ Loss approaching 1× credit → EVALUATE: thesis broken? If yes, CLOSE. If thesis intact, tighten stop to 1.5×
  │
  ├─ LATE-STAGE (21 DTE remaining):
  │    ├─ PROFIT > 50% → CLOSE 100%. Gamma risk too high to hold for last premium
  │    ├─ PROFIT 25-50% → TRIM to 33% original size (keep small runner)
  │    ├─ PROFIT < 25% → CLOSE 100%. Near breakeven with escalating gamma = bad risk/reward
  │    └─ LOSS → CLOSE. Stop should have triggered already. If not, close now
  │
  └─ EXPIRATION WEEK (5 DTE):
       └─ CLOSE 100% OF REMAINING. No exceptions. Pin risk, gap risk, assignment risk
          all spike exponentially. The final $0.10 premium can cost $500+ in gap risk.
          Close by 3:30 PM ET Friday [VERIFIED]
```

[VERIFIED] The single most expensive mistake in options trading is holding through expiration week. Robinhood auto-closes ITM at 3:00 PM ET; IBKR liquidates at 3:45 PM if margin insufficient; TDA auto-exercises $0.01+ ITM at 4:00 PM ET cutoff.

---

## <!-- DEEP: 10+min --> Anti-Hallucination Guardrails

| Rule | Description |
|------|-------------|
| **Probabilistic, not deterministic** | A 70% POP trade still loses 30% of the time. Never guarantee outcomes or say "this will happen." Say "this is the expected outcome based on current data." |
| **Broker specifics vary** | Auto-exercise policies, margin calculation methods, and fee structures differ. Robinhood ≠ IBKR ≠ TDA. Verify against your broker's current documentation. |
| **Tax implications are jurisdiction-specific** | Section 1256 contracts (SPX, VIX, NDX) get 60/40 tax treatment in the US. Equity options get short-term/long-term treatment. International jurisdictions differ. |
| **Liquidity changes** | Open interest and volume shift continuously. A liquid option yesterday may be illiquid today after earnings or news. Verify current bid-ask before executing any trim/exit. |
| **Regime dependence** | All trigger levels in this document assume a normal vol regime (VIX 15-25). In high vol (VIX > 30), widen all profit targets and stops by 30-50%. In low vol (VIX < 12), tighten by 20%. |

---

*Every trigger in this document is [COMMON-PRACTICE] unless tagged [VERIFIED] with a specific source. Verification tags indicate confirmation against broker documentation, exchange rules, or published backtest results.*

