# Additional Resources — futures-options-trader

> Deep knowledge loaded on demand. Keep SKILL.md lean; put extended examples, mechanics depth, and worked cases here.

## FOP Pricing Conventions (Mechanics)

**Premium quoting:** FOP premium is quoted in underlying price terms, not dollars. To get cash premium per contract: **cash premium = quoted premium × contract multiplier**. This is the single most common source of mis-sized FOP trades.

| Product | Future multiplier | Minimum tick | Tick value | Quoting convention |
|---------|------------------|--------------|------------|--------------------|
| ES options | $50 × index | 0.25 index pt | $12.50 | Index points |
| MES options | $5 × index | 0.25 index pt | $1.25 | Index points |
| CL options | 1,000 bbl | $0.01 | $10.00 | Dollars per barrel |
| GC options | 100 troy oz | $0.10 | $10.00 | Dollars per ounce |
| ZC options | 5,000 bu | 1/8 cent ($0.00125) | $6.25 | Cents per bushel |
| ZB options | $100,000 face | 1/64 pt | $15.625 | Points (32nds/64ths) |

> **[VERIFICATION REQUIRED]** The table above is a reference baseline for the quoting math. Multipliers and minimum ticks change and products get delisted — verify the current CME/ICE product spec page for the exact contract and month before emitting any number. Never quote a spec from this table as if current.

**Example — ES call quoted at 12.50 (points):**
- Cash premium = 12.50 × $50 = **$625 per contract**.
- Breakeven at expiry = strike + 12.50 index points.
- Tick value: 0.25 pt × $50 = $12.50 per tick.

**Example — CL put quoted at $2.15/bbl:**
- Cash premium = $2.15 × 1,000 bbl = **$2,150 per contract**.
- Breakeven = strike − $2.15.

## Exercise and Assignment Mechanics

- **Exercise/assignment creates a futures position**, not cash. Exercising a call = long the underlying future; a put = short the future. The futures position inherits SPAN margin, roll, and FND/LTD obligations.
- **American-style** (most CME FOPs): buyer may exercise any time before the exercise deadline; short holders face assignment risk on any ITM leg. Early exercise is rational when the option's time value is less than the benefit of holding the underlying (dividends on index/stock baskets, carry on commodities, rates on fixed income).
- **European-style** (some products): exercise only at expiry — no early-assignment risk, but also no early-exercise benefit.
- **Expiry vs delivery:** an option expires against the future; the future has its own LTD and FND. An option exercised into a futures month that is inside its FND window converts directly into a delivery obligation.
- **Exercise cutoff** is product-specific (often after the regular close or a fixed time on the last trading day). Verify the current cutoff for the product — it determines whether a same-day decision is still executable.

> Exercise style, cutoff times, and assignment conventions are [VERIFIED]-only facts. If not confirmed from the exchange/broker this session, mark [UNKNOWN] and do not build a plan on them.

## Early-Exercise Case Studies

**Case A — Dividend capture on index FOPs:** A deep-ITM ES call (delta 0.95, all intrinsic value) is held over an S&P 500 dividend ex-date. A counterparty exercises to capture the dividend. Result: long ES futures appear at the assignment, requiring margin that the "defined-risk option" budget did not reserve. *Lesson: before holding deep-ITM American calls over dividend events, either close the option or reserve futures margin.*

**Case B — High-carry commodity:** A deeply ITM ZC call into the delivery month carries no time value; the option holder exercises to take delivery of the cheap future. The short is assigned a long ZC futures position inside its FND window and must decide: take delivery (silo/storage logistics) or liquidate into a thin front-month book. *Lesson: deep-ITM commodity FOPs near delivery behave like futures — treat the short as potentially assigned.*

**Case C — Rates move against a short put:** A short 6E put goes deep ITM on a sharp FX move; assignment risk is realized at the next exercise cycle. The trader now holds a short EUR futures position in a fast market. *Lesson: short American FOPs need an assignment plan (accept the future, or hedge the delta) written before the trade.*

## Expiry-Collision Worked Example

**Setup:** Mid-September. Trader sells a ZC December call. December ZC futures LTD is mid-December; FND begins a few sessions after LTD.

- **Option expiry:** December option on December future — the option expires shortly before the future's LTD (verify exact dates).
- **Collision risk:** If the short call is ITM at option expiry and gets assigned, the trader holds December ZC futures with FND approaching — a delivery decision within days.
- **Correct plan:** decide before the option's expiry whether to (a) close the option, (b) roll the option to March, or (c) accept December futures and roll them to March before FND-5. Record in the State Log; never carry the position into the window without a decision.

## War Story

A trader recommended "a covered call on CL" using equity-option instincts: buy 1 CL future, sell a call, and call it defined risk. The mechanics were never verified. The short CL call was American-style and deep ITM after a rally; assignment hit on a Friday, creating a second long CL future. Monday's gap down against two long contracts produced a margin call at $18,000 beyond the "defined-risk" estimate, and the forced liquidation crystallized the loss. Root cause: two unverified mechanics — exercise style (assignment possible) and the futures leg's SPAN margin. The fix in this skill: Phase 0 spec verification (R1) and the Phase 4 exercise/assignment check (R3/R4) run before any covered-call recommendation, and the resulting-futures-position statement (R2) in every plan.

## Reference Material

- [CME Group — Options on Futures education](https://www.cmegroup.com/education/courses/option-course.html) — official mechanics and conventions
- [CME Group — Product specifications](https://www.cmegroup.com/markets/) — per-product FOP specs (verify current values here)
- [ICE — Futures and options product pages](https://www.theice.com/products) — ICE-listed FOP specs
- Broker/clearing documentation for SPAN margin on short FOP structures — current rates only from the API, never cached
