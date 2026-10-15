# Strategy cards — one payoff corner per card, with the arithmetic attached

**Every card here is a hypothesis, not a result.** A card names a payoff corner, the regime it is
meant for, and the rules that produce that corner. It does not claim the corner is attainable. The
`p` figures are *targets to be measured*, and the tool in `../scripts/payoff_check.py` is what turns
a card into `b`, `E`, `p*` and `R_max` before capital is risked. Nothing here is an instrument
recommendation; the card says *which payoff* to buy, `fundamental-analyst` and
`technical-signals-engineer` say *what* to buy.

Read a card like a lab protocol: entry condition, exit rules, size rule, kill criteria. If any of
those four is missing, the card is not tradeable, it is a mood.

---

## How to read the columns

| Column | Meaning |
|---|---|
| `TP` | profit target, in R (multiples of the planned risk) |
| `SL` | stop distance, in R. `1.0R` is the reference; a card whose average realised loss is not 1R must be measured by the mean R, not by the closed form |
| `b (target)` | `TP/SL`, the payoff ratio the rules mechanically produce |
| `p* (required)` | `1/(1+b)` — the win rate below which the corner cannot pay, whatever the skill |
| `p (assumed)` | the win rate the card is *designed* to be measured against. Not a claim |
| `E (at assumed p)` | `p*b − (1−p)`, the expectancy per trade in R, before cost |
| `regime filter` | the read that must be true before the card is armed. The regime **definition** belongs to `technical-signals-engineer`; the macro regime belongs to `macro-strategist` |
| `size rule` | what constrains the risk per trade. The final band belongs to `trade-sizing-recovery`, `portfolio-signal-manager`, `algorithmic-trader` |

---

## SC-0 — The default card. Do not trade this one.

This is the anti-card, and it exists because it is the shape a book falls into when nobody writes
rules down.

| Field | Value |
|---|---|
| Entry | "when it looks good" — no mechanical trigger |
| TP | take the profit as soon as it is green, typically at about **0.5R** |
| SL | "give it room", typically at about **1.5R**, or no stop at all |
| `b` | `0.5/1.5 =` **0.333333** |
| `p* (required)` | `1/(1+0.333333) =` **0.750000** |
| `p (assumed)` | 0.62 — a *high* win rate |
| `E` | `0.62*0.333333 − 0.38 =` **−0.173333R** |
| Regime filter | none |
| Size rule | whatever feels affordable |
| Kill criteria | none, because there is no hypothesis to falsify |

**A 62% win rate loses 0.173333R per trade on this card, and it needs 75% to break even.** Run
`payoff_check.py --tp 0.5 --sl 1.5 --p 0.62` and read the whole output; the sensitivity block shows
that even 67% is negative. This card is not a straw man — it is what "cut winners, let losers run"
looks like once it is reduced to two numbers, and it is the single most common reason a competent
retail equity trader bleeds.

---

## SC-1 — Trend pullback continuation

| Field | Value |
|---|---|
| Setup tag | `trend-pullback` |
| Entry | Instrument is in a confirmed uptrend (higher highs AND higher lows on the weekly, price above a rising long moving average). Price pulls back to a defined support and prints a rejection. Enter on the rejection, not on the way down |
| Regime filter | trending / uptrend. If the trend read is absent or the instrument is range-bound, the card is disarmed — the same entry in a range is a whipsaw generator |
| SL | one **ATR** below the rejection low, or the pullback low, whichever is closer. That distance **is** `1R` |
| TP | **3R**, or a structural target if the structure is closer. No trailing exit mid-trade — the exit rule is the whole card |
| `b (target)` | **3.000000** |
| `p* (required)` | **0.250000** |
| `p (assumed)` | 0.40 |
| `E (at 0.40)` | **+0.600000R** gross; `+0.590000R` net at `c_R = 0.01` |
| Size rule | `R_max` from the streak arithmetic at `p = 0.40`, `D_tol = 20%`, `safety = 1.5` is **1.2336% of equity**. This corner pays the most and sizes the smallest — the two facts travel together |
| Kill criteria | after `n_req = 42.667` trades, if the measured `E_net` is <= 0, the corner is wrong. Rotate the corner; do not tune the parameters |

**Why the regime filter is load-bearing.** This is the corner that pays when serial correlation is
positive: a pullback inside a trend resolves in the trend's direction. In a range, the same entry
buys the top of the range. `technical-signals-engineer` owns the regime read — this card only
declares which read it needs.

---

## SC-2 — Breakout from a consolidation

| Field | Value |
|---|---|
| Setup tag | `breakout-2r` |
| Entry | Price closes above a well-defined consolidation high (at least 4–6 weeks of contraction), on expansion of volume versus the consolidation's average. Enter on the close or on the first minor pullback to the breakout level, not on an intraday spike |
| Regime filter | trending, and volatility expanding out of a contraction. In a range-bound market the same breakout is the classic false break |
| SL | the far side of the breakout level, or 1 ATR, whichever is closer — `1R` |
| TP | **2R**, or the measured move of the consolidation if it is nearer |
| `b (target)` | **2.000000** |
| `p* (required)` | **0.333333** |
| `p (assumed)` | 0.40 |
| `E (at 0.40)` | **+0.200000R** gross |
| Size rule | `R_max` = **1.2336%** at `p = 0.40` (same streak as SC-1, because `L` depends on `p` and `n`, not on `b`). Note `n_req = 216.000` — nearly five times SC-1's measurement burden |
| Kill criteria | same rule. The one thing to watch here is cost: `c_R* = 0.20R`, so at a 5 bps round trip the break-even stop is `S* = 5/(100*0.20) = 0.25%` of price. Any stop tighter than that makes SC-2 a loser even when the entry is right |

---

## SC-3 — Range fade

| Field | Value |
|---|---|
| Setup tag | `range-fade` |
| Entry | Instrument is range-bound by the `technical-signals-engineer` range read (price oscillating between a tested upper and lower boundary, ADX low). Price reaches the boundary and prints a rejection. Enter against the boundary, never mid-range |
| Regime filter | **range-bound**, and specifically *not* trending. This is the card that a trend destroys |
| SL | beyond the boundary by 1 ATR — `1R` |
| TP | **0.75R** — the mid or the far side, whichever is nearer. Mean reversion's honest shape is a target SMALLER than its stop |
| `b (target)` | **0.750000** |
| `p* (required)` | **0.571429** |
| `p (assumed)` | 0.65 |
| `E (at 0.65)` | **+0.137500R** gross; `+0.127500R` net at `c_R = 0.01` |
| Size rule | `R_max` = **2.5351%** — larger than the trend cards, because `L = 5.259` at `p = 0.65` |
| Kill criteria | `n_req = 147.405` trades **before the edge is measurable at all**. A range-fade book abandoned after 40 trades has not been tested, it has been interrupted |

**The asymmetry to internalise.** The bigger size allowance and the shorter losing streak are real
advantages of the high-`p` corner. The thin expectancy and the 147-trade measurement burden are the
price of them. Both facts are on the same card, and a reader who quotes one without the other is
quoting half a card.

---

## SC-4 — Failed-breakout reversal

| Field | Value |
|---|---|
| Setup tag | `failed-break` |
| Entry | Price breaks a tested boundary, fails to hold it, and closes back inside within the same or the next session. Enter on the close back inside, with the failed break as the reference |
| Regime filter | range-bound, or trend-end. This is the one card that *uses* the failure of SC-2's condition |
| SL | beyond the extreme of the failed break — `1R` |
| TP | the opposite boundary, or **2R**, whichever is nearer |
| `b (target)` | **2.000000** |
| `p* (required)` | **0.333333** |
| `p (assumed)` | 0.42 |
| `E (at 0.42)` | `0.42*2.0 − 0.58 =` **+0.260000R** gross |
| Size rule | `L` at `p = 0.42` and `n = 250` is `ln(250)/ln(1/0.58) = 5.521461/0.544727 =` **10.136**, so `R_max = 20/(10.136*1.5) = 20/15.204 =` **1.3154%** |
| Kill criteria | `n_req = 4*(1.480675/0.260000)^2 = 4*32.431930 =` **129.728** trades. Below that, the measured `E_net` is a description, not a test |

**Why this card can carry a slightly better `p` than SC-2.** The failed break is a *filtered*
breakout: you are trading the breakout that already proved itself wrong, and the population of
failed breaks is not the population of all breaks. Whether that lift is real is exactly what the
`n_req` measurement is for — it is an assumption on the card, not a finding.

---

## SC-5 — Event continuation (post-event drift)

| Field | Value |
|---|---|
| Setup tag | `event-drift` |
| Entry | A scheduled event (earnings, guidance, a regulatory decision) produces a gap in the direction of the pre-existing trend, and price holds the gap's edge for N sessions. Enter on the hold, with the event date behind you, not before it |
| Regime filter | event-driven. The event calendar and the gap-risk assessment belong to `equity-risk-and-capital-engineer`; the drift's macro backdrop belongs to `macro-strategist` |
| SL | the far edge of the gap, or 1.5 ATR — `1R` after converting. **Gap risk is the reason this card's stop is wider than the intraday distance suggests** |
| TP | **2R** |
| `b (target)` | **2.000000** |
| `p* (required)` | **0.333333** |
| `p (assumed)` | 0.45 |
| `E (at 0.45)` | **+0.350000R** gross |
| Size rule | `R_max = 20/(9.236*1.5) = 20/13.854 =` **1.4437%** at `p = 0.45`. Reduce further where the position can gap through the stop — a stop is a level, not a guarantee |
| Kill criteria | the same `E_net <= 0` rule, **plus** a hard rule that an unhedged position through a scheduled event is a different bet than the card. If the card says "after the event", holding into the event is a different card and must be pre-registered as one |

---

## SC-6 — Volatility contraction entry (low-vol base)

| Field | Value |
|---|---|
| Setup tag | `vol-contraction` |
| Entry | Realised range contracts materially versus its own recent average (an ATR or Bollinger-band-width contraction, definition owned by `technical-signals-engineer`). Enter on the first expansion in either direction, with the direction supplied by the trend read |
| Regime filter | low-volatility. In a high-volatility regime the base is not a base, it is a pause inside the move |
| SL | the opposite edge of the contraction — `1R`. This stop is *tight in price terms*, which is what makes the cost derivation bind |
| TP | **2R**, or 3R when the trend read is strong — but the card must declare which, before entry |
| `b (target)` | **2.000000** (at `TP = 2R`) |
| `p* (required)` | **0.333333** |
| `p (assumed)` | 0.40 |
| `E (at 0.40)` | **+0.200000R** gross |
| Size rule | `R_max =` **1.2336%**. **And the cost term is the binding constraint here**: a contraction stop is often 0.5–1.5% of price, so at 5 bps round trip `c_R` is 0.033–0.10R against an `E` of 0.20R. Compute `c_R` for every card before trading it |
| Kill criteria | same rule, plus a cost kill: if the realised `c_R` exceeds 0.10R over 20 trades, the stop is too tight for the instrument's cost structure and the card is wrong *as specified* |

---

## Card invariants — true of every card above

1. **A card without a regime filter is SC-0 wearing a costume.** The entry rule generates `p` only
   inside the regime it was designed for.
2. **`p` on a card is a target, not a measurement.** The measurement happens over `n_req` trades,
   with the iteration protocol in `../references/the-iteration-protocol.md`.
3. **Size comes from streak survival, not from confidence.** `R_max = D_tol/(L*1.5)` is the same
   formula on every card; only `p` changes `L`.
4. **`c_R` is printed on the card or the card is incomplete.** `c_R = bps/(100*stop_pct)`, and the
   break-even stop `S* = bps/(100*E)` is the number that decides whether the card can be traded at
   the stop the pattern actually produces.
5. **Kill criteria are pre-registered, not discovered.** After 5 iteration cycles with
   `E_net <= 0`, the corner is wrong and the response is rotation, not tuning.
6. **A card that cannot fail is not a card.** If no measurement could falsify it, it is SC-0.

## What a card is not

A card is not a forecast, a rating, a recommendation, or evidence that anyone makes money trading
it. It is a **payoff spec**: it says which corner the rules buy and what that corner requires to be
profitable. Every number above is `[COMPUTED]` arithmetic from the stated `p`, `b` and cost, or
`[ILLUSTRATIVE]` where it is an assumption about the market. See
`../references/what-this-cannot-promise.md`.
