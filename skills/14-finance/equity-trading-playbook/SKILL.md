---
name: equity-trading-playbook
description: >
  Use when the question is MAKING MONEY trading shares and ETFs — "how do I make money in stocks",
  "why do I keep losing on stocks", "what win rate do I need", "should I trend follow or buy dips",
  "is my stop too tight", "my win rate is high but I'm down", "which setups make money". Handles the
  payoff corner (b, p, break-even p*, expectancy in R), the regime-to-corner map, exit arithmetic,
  cost drag in R, streak survival, the risk-per-trade ceiling, and the pre-registered loop that
  moves a negative-expectancy book to positive. Ships a deterministic payoff checker. Do NOT use to
  find the stock (fundamental-analyst, technical-signals-engineer) or define a regime
  (technical-signals-engineer, macro-strategist), nor for open positions
  (equity-position-lifecycle), tax lots (equity-tax-lot-and-exit-management), margin or
  concentration (equity-risk-and-capital-engineer), sizing bands (portfolio-signal-manager,
  algorithmic-trader), book expectancy and the kill list (edge-and-payoff-engineering), or review
  timeframe.
license: MIT
author: "Sandeep Kumar Penchala"
type: finance
status: active
version: "1.0.0"
updated: 2026-10-14
tags:
  - equity
  - etf
  - payoff-corner
  - expectancy
  - break-even-win-rate
  - payoff-ratio
  - r-units
  - position-sizing
  - streak-survival
  - cost-drag
  - regime-matching
  - strategy-selection
  - iteration-protocol
  - overfitting
  - deterministic-calculator
token_budget: 4500
chain:
  examples:
  - skills/14-finance/equity-trading-playbook/examples/checks
  consumes_from: [equity-position-lifecycle, equity-risk-and-capital-engineer, edge-and-payoff-engineering]
  feeds_into: [equity-position-lifecycle]
---

# Equity Trading Playbook

> **Portability target:** spec-level. The payoff arithmetic is unit-free (R) and the checker is
> stdlib-only Python 3 with no network, no vendor and no broker dependency. Every threshold is a
> named, printed constant. No broker-specific command appears anywhere in this skill.

<!-- QUICK: 30s -->
The whole skill is four numbers on a card:

```
b  = tp / sl                the payoff ratio your EXITS imply
p* = 1 / (1 + b)            the win rate those exits require to break even
E  = p*b - (1-p)            your expectancy per trade, in R
c_R = bps / (100*stop_pct)  what cost takes out of it
```

**`p*` is decided by the exits and by nothing else.** If the card's `p*` is above the win rate you
actually have, no amount of discipline fixes it — you rotate the payoff corner, which is a rules
change available today.

This skill owns **which payoff corner to trade, in which regime, with which rules, and how to iterate
toward positive expectancy without curve-fitting.** It does not pick the stock — that is
`fundamental-analyst` and `technical-signals-engineer` — and it does not manage an open position —
that is `equity-position-lifecycle`.

<!-- STANDARD: 3min -->
The honest headline: **the equity corner that pays best demands the smallest size.** A 1R-stop, 3R-
target breakout card at a 40% hit rate has `E = +0.600000R` and `p* = 0.250000` — and an 11-trade
expected losing streak, which at a 20% drawdown tolerance allows only `1.2336%` of equity per trade.
A high-win-rate range-fade corner at 65% has `E = +0.137500R` and allows `2.5351%`. On the shipped
synthetic ledger, one cohort pays `+0.590000R` net and another bleeds `−0.260000R` at a **62.5% win
rate**. All three facts are arithmetic, and all three are reproducible with one command.

<!-- DEEP: 10+min -->
**This skill does not promise a profit.** It identifies a positive-expectancy *configuration* of an
assumed `p` and `b`. `p` is an estimate with sampling error. The iteration protocol exists to prevent
self-deception, not to guarantee a result. See `(references/what-this-cannot-promise.md)` before
quoting anything.

---

## Route the Request

### Auto-Route (no user input needed)

| The request sounds like | Where it goes |
|---|---|
| "How do I make money in stocks?" | DT1 → name a payoff corner, then run the checker |
| "Why do I keep losing on stocks?" | DT4 — convert the book to R, compute `b`, read `p*`, compare to the measured `p` |
| "What win rate do I need?" | `p* = 1/(1+b)` from your own exit rules. Run the checker; do not quote 50% |
| "Should I trend follow or buy dips?" | DT2 — the answer depends on the regime read, so ask for it first |
| "Is my stop too tight?" | `(references/cost-drag-and-stop-distance.md)` — `c_R = bps/(100*stop_pct)`, and `S* = bps/(100*E)` |
| "My win rate is high but I'm down" | DT4 — this is the disposition profile. `b = 0.333333` requires `p* = 0.75` |
| "Which setups make money?" | `(references/payoff-corners-for-equities.md)` — the corner table, then DT1 |
| "How many trades before I can trust this?" | `n_req = 4*(sd/\|E_net\|)^2`, printed by the checker per card |
| "Should I size up?", "is my strategy profitable?" | `R_max = D_tol/(L*safety)` for the ceiling (the *band* belongs to `trade-sizing-recovery`); `--from-log` for the record, reading `E_net(R)` and not the currency view |

### Ask, or fetch — never assume

1. **What are `tp` and `sl`, in R?** Not "a 2:1" but the two distances. `b` is their ratio and nothing
   else; a card whose exits are unspecified has no `b` at all.
2. **What win rate was measured, on how many trades, in what window?** An unqualified `p` is the most
   misleading figure in this skill.
3. **What is the round-trip cost in basis points, and the stop distance in percent of price?** Their
   ratio is `c_R`; neither number alone is enough.
4. **Which regime was the `p` measured in, and which is in force?** See DT2.
5. **Is the question about a card (a hypothesis) or a ledger (a record)?** Different commands.

---

## Anti-Rationalization

| The rationalization | The reality |
|---|---|
| "My win rate is 62%, well above break-even" | Break-even is not 50%. It is `p* = 1/(1+b)`, and on a 0.5R target with a 1.5R stop it is **0.750000**. 62% is thirteen points short |
| "The strategy works, I just need to be more disciplined" | Discipline scales expectancy; it does not change its sign. A negative `E_net` stays negative at every size |
| "A 2:1 payoff means I only need to win 40%" | `p* = 1/(1+2) = 0.333333`, so 2:1 needs 33.3%, not 40%. And at `p = 0.40` a 2:1 card pays only `+0.200000R` — the 3:1 card pays `+0.600000R` on the same `p` |
| "I'll take the profit at 0.5R and give the loser room to 1.5R" | `b = 0.333333` → `p* = 0.750000`. This single sentence is the most common reason a competent retail trader bleeds |
| "Position sizing is where the edge is" | Size scales `E`; it never changes its sign. And currency-denominated `p` and `b` are contaminated by size, which is the opposite of a fix |
| "Dollars are what matter, so I'll compute `b` in dollars" | Currency `b` measures `mean(r*R \| win) / \|mean(r*R \| loss)\|`, which is `b` times a ratio of average position sizes. See `(references/r-units-versus-currency.md)` |
| "My backtest says 3:1 with a 55% win rate" | Then `E = +1.200000R` per trade, which is larger than any equity corner in the table. Look for look-ahead, survivorship, or a stop that could not have filled |
| "Fewer, bigger trades is the same edge with less work" | `n_req` is the sample the *mean* needs. Fewer trades is a smaller sample, so it is *less* measurable, not the same edge |
| "The stop is just insurance, it doesn't change the edge" | The stop sets `sl`, `sl` sets `b`, `b` sets `p*`, and `sl_pct` sets `c_R`. The stop is three of the four numbers on the card |
| "I'll test the change and see" / "five failed cycles means I need better parameters" | Without a pre-registered falsifier and `n_required` trades, "seeing" is reading noise; and five cycles with `E_net <= 0` is evidence about the *corner*, not its parameters. If `b = 0.333333` the problem is `p* = 0.75`, and no parameter fixes it |
| "Commission is negligible on equities" | At a 5% stop, yes (`c_R = 0.01R`). At a 0.5% stop, `c_R = 0.10R` — half of a thin `E`. `c_R = bps/(100*stop_pct)` has no size term in it |

---

## Ground Rules

**These are gates, not advice. Each has a mechanical trigger and a fixed response.**

| Rule | Mechanical Trigger | Violation Response |
|---|---|---|
| R1 | A win rate is quoted without the `b` it was earned on, and without `p*` | STOP. Compute `p* = 1/(1+b)` for that book and restate both numbers in one sentence, or strike the win rate |
| R2 | A payoff ratio or expectancy is computed on currency P&L rather than R | STOP. Convert with `r_i = pnl_i / risk_i` where `risk_i` is the INITIAL planned risk, then recompute. If `risk` is missing, the statistic does not exist |
| R3 | Any word in the family "proven", "confirmed", "validated" applied to a card | STOP. Quote `E_net`, the sample size, the window, and `n_req`. A card is a hypothesis until `n_req` trades exist |
| R4 | A stop or target distance is stated without its unit (R, ATR multiple, or percent of price) | STOP. Name the unit. `c_R`, `R_max` and the share count all depend on which one it is |
| R5 | A position size is recommended | STOP. This skill derives a `R_max` CEILING only. Hand the band to `trade-sizing-recovery`, `portfolio-signal-manager` or `algorithmic-trader` |
| R6 | A regime label is asserted without a named source | STOP. Cite `technical-signals-engineer` (`references/regime-detection.md`) or `macro-strategist` (`references/macro-regime-classification.md`) |
| R7 | A stock, ETF or ticker is recommended | STOP. Selection belongs to `fundamental-analyst` and `technical-signals-engineer`. This skill says which payoff to buy, never what to buy it on |
| R8 | A checker verdict is quoted without its assumed `p` on the same line | STOP. A verdict is conditional on `p`. Carry the assumption with the verdict |
| R9 | `--from-log` output is quoted without the ledger's provenance lines | STOP. The checker echoes them for exactly this reason; paste them with the numbers |
| R10 | A synthetic fixture is presented as a result, a backtest or a market finding | STOP. It is a demonstration of the tool. The shipped ledger carries `SYNTHETIC` in its header and the checker echoes it |
| R11 | A card is changed without a pre-registered hypothesis naming ONE lever | STOP. Rule 1 of the protocol; write the lever, the change, the predicted direction and the falsifier first |
| R12 | A cycle is declared successful before `n_required` trades, or the cycle count `m` is reset by a rename or a rotation | STOP. Report the cycle as IN PROGRESS. `m` counts the book, and `alpha_i = 0.05/m` only ever tightens |

**Always:**
- **Admit uncertainty** — if `p`, the average loss magnitude, the cost rate or the sample behind `p`
  is unknown, say so before printing a number.
- Print `p*` next to every `b`. A payoff ratio without its break-even win rate is half a card.
- Print `c_R` next to every `E`. A gross expectancy in a cost-bearing instrument is a flattering one.
- Keep the `SYNTHETIC` label attached to synthetic data. It is cheap and it is the whole defence.

---

## The Expert's Mindset

<!-- QUICK: 30s -->
An expert reads a proposed trade and looks **first at the exits**, not the entry. The exits produce
`b`; `b` produces `p*`; `p*` decides whether the entry's win rate is even relevant. An expert prices
a card in three seconds and refuses to discuss the indicator until `p*` is on the table.

Three habits distinguish the expert from the enthusiast: they **convert to R before computing
anything** (currency `p` and `b` mix sizing into entry skill, and the mixture is not separable); they
**distinguish a card from a record** ("here is the corner I intend to trade and what it requires" is a
card; "here is what my book did over n trades" is a record); and they **quote the refusals** (every
`n/a` is a named guard with a reason — `sl = 0` is not a stop, `E_net <= 0` has no `n_req`, a
currency-mode ledger has no R fields).

And the habit underneath all three: **an expert is more interested in the corner they have been
avoiding than in the one they have been trading.** On the shipped ledger the finding is not "the
trend cohort pays" — it is "one cohort is negative at a 62.5% win rate, and it is the cohort with the
most trades".

---

## Deliberate Practice

<!-- STANDARD: 3min -->
| Level | Drill | Time | Success criterion |
|---|---|---|---|
| Novice | Run `payoff_check.py --tp 3.0 --sl 1.0 --p 0.40` and hand-verify every field against the table in `../examples/checks/01-trend-breakout-positive.md` | 30 min | Every value matches on paper, including `sd = 1.959592` and `n_req = 42.667` |
| Intermediate | Take your own last 20 trades, add `risk` and `cost` columns, and run `--from-log`. Explain why the currency `b` and the R `b` differ | 45 min | Can state the contamination condition without looking it up |
| Advanced | Run `--from-log` on the synthetic ledger and identify which cohort carries the pooled book, and why pooling is the wrong summary | 40 min | Names `trend-breakout` at `+0.590000R` and `disposition-quick-tp` at `−0.260000R` inside a pooled `+0.066613R` |
| Advanced | Take one card, hold `p` fixed, and run the checker at four stop distances. Chart `c_R` against `stop_pct` | 60 min | Reproduces the hyperbola and identifies the `S*` at which the card crosses zero |
| Expert | Run the iteration protocol on a real book for one full cycle: pre-register, `n_req` trades, holdout, adjusted `alpha_i`, and a written verdict | one cycle | The holdout figure is reported whatever it says, and `m` was written down before the cycle began |
| Expert | Build the disposition card from your own exits and derive the `p*` it implies. Then decide, in writing, whether to rotate | 30 min | The answer is a rules change, not a discipline resolution |

**The one drill that changes behaviour.** Take the single best trade in your book and the single worst,
delete both, and re-run `--from-log`. If any cohort's `E_net` changes sign, that cohort's headline
rested on two trades. Do it once a quarter on the real ledger.

**The drill that fixes the habit for good.** In one paragraph: the `b` your exits imply, the `p*`
that follows, and the win rate you have measured over at least `n_req` trades. If `p` is below `p*`,
stop reading and rotate the corner. If `p` is above `p*`, write down the sample size and the regime
the `p` came from. It works because it forces the exits into the conversation before the entry, which
is the only order in which the arithmetic is meaningful.

---

## Operating at Different Levels

| Level | Scope | Autonomy | Craft expectation |
|---|---|---|---|
| L1 Apprentice | Run the checker on a card someone else specified; read the verdict and the sensitivity block | None — the card is given | Can report `b`, `p*`, `E_net` and `n_req` and say which line drove the verdict |
| L2 Practitioner | Write the card: entry, exits, regime filter, size ceiling, kill criteria. Fix `p*` before trading | Sets the card, not the thresholds | Can explain in one sentence why a `p*` above the measured `p` is fatal, and rotate |
| L3 Senior | Run the iteration protocol: pre-register, measure over `n_req`, holdout by time, count `m`, keep the cycle log | Owns the measurement | Distinguishes a `p` change from a `b` change from a cost change, and can attribute each cycle's result to one lever |
| L4 Lead | Own the corner system across several books with different holding periods; maintain the cohort tags and the kill list | Owns the strategy portfolio | Can show, from the cycle log, which corner was rotated when and whether the rotations were pre-registered |
| L5 Transformative | Own the governance: who runs the checker, who measures, who independently checks the verdict. Make `p*`, `c_R` and `n_req` non-optional fields on every card | Owns the evidence chain | Can produce, on demand, a multi-cycle trail showing each lever's measured effect and the refusals that bound them |

**The shift that matters:** at L1–L2 the trader is looking for a card that works. At L3+ they are
maintaining a record of which lever moved the arithmetic and by how much, and the record's most
valuable entries are the cycles that failed.

---

## When to Use

- **Choosing which payoff corner to trade** — high `b` and low `p`, or low `b` and high `p` — and
  computing `E`, `p*` and `b*` for the choice.
- **Answering "what win rate do I need"** from the exits you actually use, rather than from 50%.
- **Diagnosing a negative-expectancy equity book** before changing anything: convert to R, compute
  `b`, read `p*`, compare with the measured `p`.
- **Deciding whether a stop is too tight**, with `c_R = bps/(100*stop_pct)` and the break-even stop
  `S* = bps/(100*E)`.
- **Mapping a regime onto a corner** — while citing `technical-signals-engineer` or
  `macro-strategist` for the regime definition rather than inventing one.
- **Deriving the risk-per-trade ceiling** from streak survival: `L = ln(N)/ln(1/(1−p))` and
  `R_max = D_tol/(L*safety)`.
- **Turning an R ceiling into a share count**, given an ATR stop, a price and a capital figure.
- **Running the pre-registered iteration loop** that moves a book toward positive expectancy without
  curve-fitting, including the Bonferroni-adjusted significance bar.
- **Auditing someone else's strategy claim** — a high win rate with no `b`, a currency-denominated
  payoff ratio, a `b` that moved from a `p` loss, a fifth-cycle "improvement" with no holdout.

## When NOT to Use

| Not this skill | Use instead |
|---|---|
| Which stock, ETF or sector to trade; valuation, screening, financial statements | `fundamental-analyst` — selection and valuation are owned there |
| Indicator computation, signal confirmation, multi-timeframe alignment, the definition of a trend or a range | `technical-signals-engineer` — this skill cites its reads and never defines them |
| Macro regime classification, risk-on/risk-off, central bank reaction functions | `macro-strategist` |
| Whether to hold, trim, cut, average down or rotate an OPEN position, and at what cadence | `equity-position-lifecycle` |
| Which tax lot to sell, wash sales, long-term vs short-term holding clocks | `equity-tax-lot-and-exit-management` |
| Margin regimes, borrow availability, forced liquidation, liquidity and exit cost, concentration limits | `equity-risk-and-capital-engineer` |
| The position-sizing band, ladder or fractional-Kelly policy | `trade-sizing-recovery`; portfolio-level aggregation → `portfolio-signal-manager`; systematic execution and backtest engine → `algorithmic-trader` |
| Measuring a book's expectancy, cohort attribution, the kill list, expectancy decay over time | `edge-and-payoff-engineering` |
| Which review timeframe a book's statistics are trustworthy at; per-period drawdown resolution | `timeframe-performance-statistics` |
| Sharpe, Sortino, Calmar, profit factor, benchmark-relative returns | `trade-performance-analyst` |
| Option structures, spreads, hedging with options | `options-strategist`, `advanced-options-structures` |
| Which datasets to buy and what they cost | `trading-decision-data-catalogue` |
| Building the automated scanner-to-execution pipeline | `options-automation-engineer` for the pipeline pattern; `algorithmic-trader` for the equity engine |

---

## Decision Trees

### DT1 — Which payoff corner should this card buy?

```
What does the STRUCTURE say about the stop?
  ├─ the entry is invalidated a short distance away, and the move can run far
  │     ├─ regime read says TRENDING / uptrend
  │     │     └─ corner: b = 2..5, p* = 0.17..0.33        -> size SMALLEST (L is longest)
  │     ├─ regime read says RANGE-BOUND
  │     │     └─ a 3R target in a range is a target that never fills.
  │     │           Either take the boundary trade (DT2) or do not take the trade
  │     └─ regime read is ABSENT or undefined
  │           └─ STOP. You do not have a card, you have SC-0. Get the read first.
  ├─ the entry is invalidated far away, and the move is short
  │     └─ corner: b = 0.33..0.75, p* = 0.57..0.75
  │           ▼
  │        THIS IS THE DISPOSITION PROFILE unless p* is under ~0.60.
  │        Read p* aloud before sizing. If p* > your measured p, rotate.
  └─ the entry and the target are roughly equidistant
        └─ b = 1.0, p* = 0.50  -> a coin-flip card.
              ├─ your measured p > 0.50 by more than 2 standard errors?  -> trade it, small
              └─ otherwise                                               -> rotate. There is no
                                                                            room to manoeuvre here
```

### DT2 — Trend follow or buy the dip?

```
Is there a regime read from technical-signals-engineer or macro-strategist?
  ├─ NO  -> STOP. "Trend or range" is a regime question and this skill does not own the definition.
  │         Ask for the read, or fetch it, and say the card is on hold until it exists.
  └─ YES ->
        ├─ TRENDING / uptrend
        │     ├─ pullback to a defined level with a rejection?
        │     │     └─ YES -> trend-continuation card. b = 2..5. Stop at the rejection low.
        │     └─ consolidation breaking on volume?
        │           └─ YES -> breakout card. b = 2..3. Beware the false break (DT3).
        ├─ RANGE-BOUND
        │     ├─ price at a tested boundary with a rejection?
        │     │     └─ YES -> range-fade card. b = 0.5..1.0. Target the mid or the far side.
        │     │             NOTE: this corner needs n_req trades before the edge is visible.
        │     └─ a boundary BROKE and failed to hold?
        │           └─ YES -> failed-breakout card. b = 1.5..3.
        ├─ HIGH VOLATILITY
        │     └─ same entries, wider price stops, FEWER shares for the same R.
        │           Volatility and share count move in opposite directions. Always.
        └─ RISK-OFF / correlation spike
              └─ the "entries" are now one position. Cut the COUNT, not just the size.
```

### DT3 — Is this card's arithmetic able to pay?

```
1. b  = tp / sl                    (exits only; the entry is not in this formula)
2. p* = 1 / (1 + b)
3. c_R = bps / (100 * stop_pct)
   │
   ├─ p* is above your measured p by more than 2 standard errors?
   │     └─ YES -> the card cannot pay at your win rate. Do NOT tune the entry.
   │               Change the EXITS (target wider, stop tighter) or rotate the corner.
   ├─ c_R >= E ?
   │     └─ YES -> cost alone eats the edge. E_net = E - c_R is <= 0 and the card is dead
   │               at this stop distance. Widen the stop or change instrument.
   └─ proceed
4. E = p*b - (1-p)   and   E_net = E - c_R
   │
   ├─ E_net <= 0            -> NEGATIVE. Rotate the corner, not the parameters.
   ├─ 0 < E_net < 0.20R     -> MARGINAL. Trade small or do not trade it.
   └─ E_net >= 0.20R        -> POSITIVE. Continue to step 5.
5. n_req = 4 * (sd / |E_net|)^2
   │
   ├─ n_req > your realistic trade count in a year?
   │     └─ YES -> you cannot ever measure this. Widen b, or trade it and SAY SO on the card.
   └─ proceed
6. L = ln(N) / ln(1/(1-p))   and   R_max = D_tol / (L * safety)
   │
   ├─ R_max is smaller than the size you intended?
   │     └─ YES -> lower the size, shorten N, or raise the tolerance. Those are the only levers.
   └─ proceed. The card is specified. Run it and log the setup tag.
```

### DT4 — Why is this book losing despite a high win rate?

```
1. Convert EVERY trade to R:  r_i = pnl_i / risk_i     (risk_i = INITIAL planned risk)
   │
   ├─ risk is missing, or was recorded after the outcome was known?
   │     └─ STOP. The book cannot be diagnosed until risk is recorded at entry.
2. Compute b_R and b_currency
   │
   ├─ they differ by more than 5%?
   │     └─ the currency figure is contaminated by position size. Use b_R only.
3. p* = 1 / (1 + b_R)
   │
   ├─ p* > p by a lot (say > 5 points)?
   │     └─ THE EXITS ARE WRONG. Disposition profile if b_R < 0.5. Go to step 5.
   ├─ p* ~= p (within a point or two)?
   │     └─ THE EDGE IS THE COST. If c_R >= E, the stop is too tight for the cost structure.
   └─ p* < p, but the book still loses?
         └─ one or two trades carry it, or the average loss is not 1R. Remove the largest
              win and the largest loss and recompute. If E_net flips, it was two trades.
5. The only three repairs, in the order to try them:
     ├─ widen the TARGET            -> raises b, lowers p (measure it)
     ├─ tighten the STOP            -> raises b, raises c_R (measure both)
     └─ cut the COST                -> different instrument, limit orders, wider stop
   ▼
   Rotate the CORNER. Recompute b, p*, c_R, E_net, n_req, L, R_max.
   Pre-register the cycle. Measure over n_required trades. Then decide.
```

---

## Core Workflow

### Phase 1 — Fix the unit before computing anything

1. For every closed trade, record `risk` = the **initial** planned risk at entry, before the outcome
   was known. `r_i = pnl_i / risk_i`.
2. Record `cost` = commission + fees + spread for that trade.
3. Record `setup` = the card's tag. One tag per card; never recycled.
4. If `risk` is missing for any trade, the whole computation stops. `payoff_check.py --from-log`
   will refuse rather than invent a denominator.

**Complete when** every row has a positive `risk`, a `cost` and a `setup`, and the row count
reconciles to the broker's closed-trade count.

### Phase 2 — Compute the corner, in R

5. `py -3 scripts/payoff_check.py --from-log <ledger>` (add `--setup <tag>` to narrow to one cohort, `--csv-out <file>` for the table as CSV) → per-cohort `p`, `b_R`, `E_R`, `c_R`, `E_net`.
6. Read the `CONTAMINATED` flags and the `b_$` versus `b_R` gaps. A gap is sizing, not edge.
7. For each positive cohort, `p* = 1/(1+b_R)` and compare with the cohort's own `p`. **Complete when** every cohort has `p`, `b_R`, `E_net`, `c_R` and `p*` written down, and the pooled
book figure is reported alongside the cohort table rather than instead of it.

### Phase 3 — Specify the card

8. Write the card from `(references/strategy-cards.md)`: entry, exits, regime filter, size ceiling,
   cost, kill criteria.
9. Compute the card's corner with `payoff_check.py --tp --sl --p --cost-bps --stop-pct`.
10. Read the sensitivity block. If `p − 5pp` flips the verdict, the card rests on a five-point
    estimate.
11. Derive `R_max`, then the share count with `--atr --atr-value --price --capital`.
12. Work the cost in dollars once, so `c_R` stops being an abstraction: a $10,000 position at a 0.05%
    round trip pays $5 cost; on a 5.0% stop that is a $500 risk and `c_R = 5/500 = 0.010000R`, and
    on a 1.0% stop it is a $100 risk and `c_R = 5/100 = 0.050000R`. The notional cancels out of the
    ratio, but seeing the dollars once is what makes the stop-distance dependence obvious.
    [COMPUTED] — `c_R = round_trip_cost / R_dollars`, with `R_dollars = notional x stop_pct/100`.

**Complete when** the card states `b`, `p*`, `E_net`, `c_R`, `S*`, `n_req`, `L`, `R_max` and the
kill criteria, all with the formula that produced them.

### Phase 4 — Run the iteration protocol

13. Pre-register: one lever, the change, the predicted `E_net` direction, the falsifier, `n_required`.
14. Measure only after `n_req` trades; split the window 70/30 by close date.
15. Count `m`, compute `alpha_i = 0.05/m`, and print it in the cycle log.
16. After five cycles with `E_net <= 0`, rotate the corner. Do not tune.

**Complete when** the cycle log holds the holdout figure, its sample size, the adjusted `alpha_i` it
was judged against, and the next action.

### Failure Modes

**Failure modes and known limitations — what goes wrong with equity strategy selection, and the countermeasure for each:**

1. **Failure mode: the exits imply an unpayable corner and nobody computes `p*`.** A 0.5R target with a 1.5R stop is `b = 0.333333`, so `p* = 0.750000`, and a 62% win rate loses `0.173333R` per trade. Countermeasure: compute `p*` before trading (R1, R3).
2. **Failure mode: a payoff ratio computed on currency P&L.** The shipped `sizing-slip` cohort reads `b = 1.000000` in R and `10.000000` in currency on the same three trades. Countermeasure: R2 — convert to R with the initial planned risk, always.
3. **Failure mode: a high win rate treated as evidence of an edge.** A win rate is only meaningful against its own `p*`. Countermeasure: R1 and DT4.
4. **Failure mode: the corner is tuned instead of rotated.** Five cycles at `E_net <= 0` on a `b = 0.333333` card is evidence about the corner, not its parameters. Countermeasure: Rule 6 of the protocol and R13.
5. **Failure mode: `n_req` ignored, so a cycle is declared a success on 20 trades.** At `b = 3`, `p = 0.40` the sample needed is 42.667 trades; at `b = 0.75`, `p = 0.65` it is 171.434. Countermeasure: R12 — log `n_required` before the cycle and report IN PROGRESS until it is met.
6. **Failure mode: the significance bar is never adjusted for the number of cycles.** At `m = 10` the per-comparison level is 0.005, and a book that has run ten cycles at 0.05 has been selecting noise for nine rounds. Countermeasure: Rule 5 and R13 — `m` is monotone.
7. **Failure mode: no holdout, or a holdout that was re-fitted.** The second holdout figure is in-sample by construction. Countermeasure: Rule 4 — a change suggested by the holdout requires a new, later window.
8. **Failure mode: cost omitted until the reconciliation.** Cost shifts the mean and leaves `sd` where it was, so `n_req` rises from 147.405 to 171.434 at `c_R = 0.01` on a thin corner, and a 0.10% stop at 5 bps is `c_R = 0.500000R`. Countermeasure: populate `cost` before the cycle; the card prints `c_R` and `S*`.
9. **Failure mode: the stop is a comfort level rather than an invalidation level.** A comfort stop is usually too far, which lowers `b`, and usually unrelated to structure, which lowers `p`. Countermeasure: place the stop where the entry is disproved, then compute `b`.
10. **Failure mode: cohorts pooled to reach the sample.** The shipped ledger pools to `+0.066613R` while containing a cohort at `+0.590000R` and another at `-0.260000R`. Countermeasure: one population per run; a cohort too small to test is a finding about the book.
11. **Failure mode: a regime filter that is not there.** A trend corner's `p` measured in a bull market is partly a measurement of the bull market; in a downtrend the `b` is unchanged and the `p` is not. Countermeasure: R6 — cite the read and label the `p` with the regime it came from.
12. **Failure mode: the arithmetic mistaken for a forecast.** A positive `E_net` is conditional on an assumed `p`. Countermeasure: R3 and `(references/what-this-cannot-promise.md)` — quote every verdict with its assumed `p` and its `n_req`.
13. **Failure mode: gap risk is unmodelled by the two-point distribution.** A stop that gaps turns `-1R` into `-2R`, which invalidates `sd`, `n_req` and `R_max` at once; a sample with one tail event and no second one cannot estimate tail risk. Countermeasure: cut size on gap grounds, assessed by `equity-risk-and-capital-engineer`.
14. **Failure mode: the card review displaces the position review.** A trader optimises a corner instead of writing an exit level for an open position. Countermeasure: the card fixes the corner once per cycle; the open position is `equity-position-lifecycle`'s business.

**Exit conditions / stopping rules for this skill's own work:**

- **Exit condition:** the card carries `b`, `p*`, `E_net`, `c_R`, `S*`, `n_req`, `L`, `R_max` and the kill criteria.
- **Exit condition:** `n_req = n/a` because `E_net <= 0` is reported as the finding, and the corner is rotated rather than tuned.
- **Exit condition:** `R_max` is reported as a **ceiling**, and the sizing band is handed off.
- **Stop-loss on the analysis itself:** if a conclusion survives only by choosing the corner after seeing the numbers, the analysis is abandoned and restarted from the regime read.
- **Cut-loss:** if `risk` is missing or was recorded after the outcome, no statistic is reported until the ledger is rebuilt.
- **Exit plan:** archive the checker's full stdout for every cycle, including the cycles you dislike.

### Regime Table

| Regime | What the corner does | What changes here |
|---|---|---|
| **Bull market / bull regime / uptrend** | High-`b` corners pay: `b = 2..5`, `p* = 0.17..0.33`. Serial correlation is positive and pullbacks resolve with the trend | The danger is over-confidence. A `p` measured entirely inside an uptrend is partly a measurement of the uptrend. Label the `p` with the window and the regime it came from |
| **Correction / pullback** | The fixed-`b` card absorbs a loss cluster a discretionary card does not. `L` at `p = 0.40`, `N = 250` is 10.809 — this is where an 11-trade streak is met | A card without a regime filter is running a trend corner into a decline. Re-measure `p`; do not re-derive `b` |
| **Bear market / downturn / drawdown / recession** | The trend corner works here only if the card defines the short side. A long-only book on a trend corner has a `b` measured in one regime and a `p` from another | `p` is the regime-dependent term. Re-measure the corner on the new regime's trades before believing it |
| **Crash / tail event / black swan (for example March 2020)** | The two-point `sd` assumption fails outright: a gap through the stop turns `−1R` into `−2R`, so the distribution underpinning `sd`, `n_req` and `R_max` is not the one being sampled | Treat the crash as a **named observation**, not a data point. Cut size on gap grounds. A sample with one crash and no second one cannot estimate crash risk |

---

## Best Practices

<!-- QUICK: 30s -->
1. **Compute `p*` before you compute anything about the entry.** `p* = 1/(1+b)` comes from the exits
   alone, and it is the number that decides whether the entry matters.
2. **Convert to R before computing `p` and `b`.** Currency statistics mix sizing into entry skill;
   `(references/r-units-versus-currency.md)` proves it with two trades.
3. **Print `c_R` beside every `E`.** `c_R = bps/(100*stop_pct)` has no size term in it, and it is the
   term that decides the tight-stop corners.
4. **Try the `b` lever before the `p` lever.** `dE/db = p` is a rules change available today; `dE/dp = b + 1` requires a signal you may not have. And after five negative cycles, **fix the corner, not the parameters** — rotation is the response, tuning is the loop that never terminates.
6. **`n_req` is a commitment, not an estimate.** Copy it into the cycle log before the cycle begins,
   and report IN PROGRESS until it is met.
7. **Split by time, 70/30, and never re-fit on the holdout.** A random split leaks regime information
   across the boundary and flatters every strategy.
8. **Count `m` and print `alpha_i = 0.05/m`.** The bar only tightens, and resetting `m` is the
   arithmetic equivalent of forgetting nine of your ten comparisons.
9. **Tag every trade with its `setup`.** Cohort attribution is impossible without it, and the pooled
   number is the one that hides both signs.
10. **Quote `R_max` as a ceiling and hand the band off.** The band belongs to `trade-sizing-recovery`,
    `portfolio-signal-manager` and `algorithmic-trader`.
11. **Label every `p` with its sample size, its window and its regime.** An unqualified `p` is the most
    misleading figure in this skill.
12. **Keep the `SYNTHETIC` label attached to synthetic data.** The checker echoes the ledger's own
    provenance lines so the label cannot be detached; the label is the whole defence.

---

## Error Decoder

| Symptom | Root Cause | Fix | Lesson |
|---|---|---|---|
| "My win rate is 62% but I'm losing" | The exits imply a high `p*`. A 0.5R target with a 1.5R stop is `b = 0.333333`, so `p* = 0.750000` | Compute `p*` from your own exits, then widen the target or tighten the stop | The win rate is not the problem; `b` is |
| `b_R` and `b_$` differ by more than a few percent | Risk per trade varies, so the currency payoff ratio carries a size ratio | Use `b_R`; read the `CONTAMINATED` flag in `--from-log` | A gap between the units IS the sizing |
| `E_R_ratio` and the realised mean R disagree | The average loss is not exactly 1R, so `E = p*b − (1−p)` understates or overstates by the average loss magnitude | Use the realised mean R; the ratio form is only exact at a 1R average loss | A stop that slips changes the formula's domain |
| `n_req = n/a` in the output | `E_net <= 0`: no sample size reaches `+2σ` on a non-positive mean | Rotate the corner; more trades do not help | A guard firing is a result |
| `b = n/a` | `--sl 0` was passed | Supply a positive stop. A 0R stop is not a stop | The engine refuses rather than dividing |
| `R_max = n/a` | `L = 0`, because `n < 2` or `p = 1` | Use `--n >= 2`, or accept that a card with no losing trade has no streak ceiling | Both causes are statements about the assumption |
| Verdict says MARGINAL and the trader wants POSITIVE | `0 < E_net < 0.20R` | Widen `b`, or trade it small, or do not trade it | MARGINAL is a defined band, printed by the engine |
| "The change worked" after 20 trades | `n_required` was never reached | Recompute `n_req` after the change and report IN PROGRESS | A sample too small by construction cannot support a conclusion |
| The same corner keeps failing | The corner is `b <= 0.5`, so `p* >= 0.667` | Rotate the corner; the exit rules are the problem | Parameter tuning cannot move `p*` |
| `--from-log` reports CURRENCY MODE | The `risk` column is absent or non-positive on some row | Add the initial planned risk, recorded before the outcome | The engine will not invent a denominator |
| A zero-cost warning fires | The ledger has no `cost` column | Add `cost` and re-run before quoting any figure | Zero cost is flattering, and it is stated |
| The pooled book looks fine but a cohort is bleeding | Pooling hides sign structure | Read the cohort table, not the pooled row | `+0.066613R` pooled against `+0.590000R` and `−0.260000R` inside it |

---

## Error Recovery

**If the verdict looks too good:** read the sensitivity block first. A card whose `p − 5pp` line is
still POSITIVE is robust to a five-point estimate error; one whose `p − 5pp` line is NEGATIVE is
resting on a number the sample cannot support. Then check whether the assumed `p` came from a real
sample with a size and a window, or from an intention.

**If the ledger will not reconcile to the broker's total:** stop. Export again with one row per
closing fill, add `cost`, and confirm `risk` was recorded at entry. An unreconciled ledger cannot
produce a reportable statistic, and the arithmetic above it will look healthy while being wrong.

**If `E_net` flips when one trade is removed:** the headline was never the edge. Report both figures,
state that the cohort rests on one observation, and stop quoting the corner until the sample grows.

**If a cycle's holdout disagrees with its fit window:** report the holdout figure and do not re-fit.
The honest sentence is "this change worked in-sample and did not work out-of-sample, so it is a new
hypothesis requiring a new window".

**If you have already acted on a claim this skill contradicts:** say so in the next cycle log, with
both figures and the dates. The checker's output is archived and the contradiction is checkable. A
correction in the record is worth more than a quietly dropped claim.

---

## Cross-Skill Coordination

### Upstream (what this skill needs)

| Upstream Skill | Artifact Needed | What You'll Use It For |
|----------------|-----------------|------------------------|
| `equity-position-lifecycle` | The open-position decision set and the review cadence keyed to the four equity clocks | The counterpart this skill feeds: a card specifies the corner, the lifecycle decides whether and how much of an open position to act on |
| `equity-risk-and-capital-engineer` | Gap and event risk, liquidity and exit-cost planning, margin and concentration limits, the settlement calendar | The risks this skill's two-point `sd` does not model, and the reason `R_max` must fall when a position can gap through the stop |
| `edge-and-payoff-engineering` | Book-level expectancy measurement, cohort attribution, the kill list, the sibling ledger schema | The measurement this skill's `--from-log` reads a ledger for, and the owner of the currency-versus-R conversion as a book-level statistic |
| `technical-signals-engineer` | The indicator formulas, the regime definitions, multi-timeframe alignment rules, ETF parameter treatment | Every regime filter on every card, cited by name rather than redefined |
| `macro-strategist` | Macro regime classification and the risk-on/risk-off framework | The macro read that arms or disarms a card, and the label attached to a `p` measured in one regime |
| `fundamental-analyst` | Screening methodology and valuation methods | Candidate selection — which instruments the corner is applied to |
| `trading-decision-data-catalogue` | Which datasets are worth having, which are free, and what each costs | Where the price series and the ledger should come from; this skill reads only the CSV it is given |
| `portfolio-signal-manager`, `algorithmic-trader`, `trade-sizing-recovery` | Sizing bands, ladders and fractional-Kelly policy | The band this skill's `R_max` ceiling sits inside, which it refuses to set |

### Downstream (what this skill produces)

| Downstream Skill | Deliverable | What They'll Do With It |
|------------------|-------------|-------------------------|
| `equity-position-lifecycle` | The card's `b`, `p*`, `E_net`, `R_max` and kill criteria, plus the `setup` tag | Judge an open position against the corner it was opened on, rather than against an impression |
| `edge-and-payoff-engineering` | A tagged ledger and a per-cohort corner table with `b_R`, `E_R` and `c_R` | Run book-level expectancy, cohort attribution and the kill list on a ledger whose `risk` and `cost` columns are already correct |
| `portfolio-signal-manager` | `R_max` as a ceiling, per card, with the `L` behind it | Place the ceiling inside a sizing band alongside correlation and portfolio-level constraints |
| `algorithmic-trader` | The corner each rule set buys, and the `n_req` its evaluation window must clear | Set the evaluation window before parameters are fitted to one |
| `trade-sizing-recovery` | `L`, `R_max`, and the realised average win/loss in R | Recalibrate loss bands against realised averages rather than intended ones |
| `equity-risk-and-capital-engineer` and `equity-tax-lot-and-exit-management` | The corners whose stops are tight enough for cost and gap risk to bind, and the `setup` tag with the window each corner was measured over | Assess liquidity, gap exposure and concentration on the positions that need it, and attribute lots and holding periods to the corner that produced them |

**Coordination rule:** the **corner** belongs here; the **instrument** to `fundamental-analyst` and
`technical-signals-engineer`; the **regime read** to `technical-signals-engineer` and
`macro-strategist`; the **open-position decision** to `equity-position-lifecycle`; the **band** to the
sizing skills; the **book-level expectancy** to `edge-and-payoff-engineering`. When a request crosses
two of those, answer the part you own and name who owns the rest.

---

## Proactive Triggers

- **A win rate is stated with no `b` attached** → compute `p* = 1/(1+b)` for the exits and say whether
  the win rate clears it. 🔴
- **The exits imply `p* >= 0.70`** → say so immediately, before any discussion of entries. This is the
  disposition profile at `b <= 0.43`. 🔴
- **`b` and `p` moved in the same cycle** → flag that neither change can be attributed, and that the
  cycle is a comparison of two configurations rather than a test of one lever. 🟠
- **`n_req` exceeds the trader's realistic annual trade count** → say that the corner cannot ever be
  measured by this book, and that it is therefore being traded on an assumption. 🟠
- **A stop is under about 1% of price** → announce that `c_R` is now a first-class term, compute it,
  and print `S* = bps/(100*E)`. 🟠
- **A ledger has no `cost` column, or `b_$` and `b_R` differ** → refuse to quote any figure until `cost` exists, and surface the unit gap as the contamination it is. 🔴
- **`E_net` for the pooled book is positive while a cohort's is negative** → report both, and say that
  the pooled figure describes no cohort in the book. 🔴
- **A fifth cycle returns `E_net <= 0`** → name the rotation, and name the corner to rotate to. 🟠
- **A `p` arrives with no sample size or window** → ask for both before using it, and label it
  unqualified if they do not arrive. 🟡
- **A card's stop is a round number unrelated to structure** → flag it as a comfort stop, which lowers
  both `b` and `p`. 🟡
- **A backtest reports `E` above `+1.0R` per trade** → flag it as above every equity corner in the
  table and ask about look-ahead, survivorship and stop fills. 🟠

---

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| ❌ "My win rate is 62%, well above break-even" | ✅ Compare it to `p* = 1/(1+b)` for your own exits — on a 0.5R/1.5R card that is 0.750000 |
| ❌ Computing `b` from a currency ledger | ✅ Convert to R with the initial planned risk, every time, before computing `p` and `b` |
| ❌ Taking the profit at 0.5R and giving the loser room to 1.5R | ✅ Rotate the corner: widen the target, tighten the stop, or remove the cap on the winner |
| ❌ Tuning parameters after five negative cycles | ✅ Rotate to a different payoff corner. The corner is wrong, not its parameters |
| ❌ Declaring a cycle successful on 20 trades | ✅ Log `n_required` before the cycle and report IN PROGRESS until it is met |
| ❌ Re-fitting on the holdout | ✅ A change suggested by the holdout is a new hypothesis requiring a new, later window |
| ❌ Re-setting the cycle counter when the setup is renamed | ✅ `m` counts the book and only ever increases; `alpha_i = 0.05/m` only tightens |
| ❌ Pooling cohorts to reach the sample | ✅ One population per run; a cohort too small to test is a finding about the book |
| ❌ Quoting `R_max` as a recommended size | ✅ Quote it as a ceiling and hand the band to `trade-sizing-recovery`, `portfolio-signal-manager` or `algorithmic-trader` |
| ❌ Using "looks like a trend" as a regime filter | ✅ Cite `technical-signals-engineer`'s regime read or `macro-strategist`'s macro regime, by name |
| ❌ Presenting `examples/` output as a backtest | ✅ Label it `[ILLUSTRATIVE]`; the ledger carries `SYNTHETIC` in its header and the checker echoes it |
| ❌ Quoting a card verdict without its assumed `p` | ✅ Carry the assumption with the verdict: "at an assumed `p` of 0.40, `E_net` is +0.590000R, and `n_req` is 43 trades" |

---

## State Log

| Step | State | Possible Transition | What Could Go Wrong | Record |
|------|-------|-------------------|---------------------|--------|
| 1 | Ledger exported with `risk`, `cost`, `setup` | → 2 if `risk` is the initial planned risk; → STOP if not | Risk recorded after the outcome; missing cost column | Export date, row count, provenance block |
| 2 | Corner computed in R | → 3 | Currency `p` and `b` used instead of R | `p`, `b_R`, `E_R`, `c_R`, `E_net`, and the contamination flags |
| 3 | `p*` read against the measured `p` | → 4 if `p > p*`; → rotate if `p < p*` | A high win rate accepted without computing `p*` | `p*`, the measured `p`, and the gap in points |
| 4 | Card specified with all fields | → 5 | A field invented rather than computed | `b`, `p*`, `E_net`, `c_R`, `S*`, `n_req`, `L`, `R_max`, regime read, kill criteria |
| 5 | Cycle pre-registered | → 6 | Two levers changed at once; no falsifier written | The lever, the change, the predicted direction, the falsifier, `n_required` |
| 6 | `n_required` trades measured | → 7 | Measured early and read as a result | Trades so far, `n_required`, IN PROGRESS or COMPLETE |
| 7 | Holdout evaluated | → 8 | Holdout re-fitted; holdout figure suppressed | Fit `E_net`, holdout `E_net`, sample sizes in each |
| 8 | Cycle verdict recorded with its adjusted bar, and the rotation decision taken if `m >= 5` with `E_net <= 0` | → next cycle, or → Phase 3 with a new corner | `m` reset; `alpha_i` not printed; tuned instead of rotated | `m`, `alpha_i`, verdict, the next action, and the corner rotated from and to |

---

## Production Checklist

- [ ] **CR1: Ledger has `risk`, `cost` and `setup` on every row** — **Complete when** `risk` is positive on all rows and was recorded at entry.
- [ ] **CR2: Every trade converted to R** — **Complete when** `r_i = pnl_i / risk_i` exists for every row with no exceptions.
- [ ] **CR3: Cohort table produced** — **Complete when** `--from-log` output is archived with the ledger's provenance lines attached.
- [ ] **CR4: Contamination checked** — **Complete when** `b_$` versus `b_R` gaps and any `CONTAMINATED` flags are recorded.
- [ ] **CR5: `p*` computed for every open cohort** — **Complete when** each cohort's `b_R` has a `p*` beside it and the measured `p` has been compared to it.
- [ ] **CR6: Card written with all nine fields** — **Complete when** `b`, `p*`, `E_net`, `c_R`, `S*`, `n_req`, `L`, `R_max` and the kill criteria are all present with their formulas.
- [ ] **CR7: Regime read cited by name** — **Complete when** the card names `technical-signals-engineer`'s regime read or `macro-strategist`'s macro regime, and the read that disarms it.
- [ ] **CR8: Cost measured, not estimated, and the break-even stop computed** — **Complete when** the round-trip bps figure comes from at least 20 recorded fills and `S* = bps/(100*E)` on the card is compared to the stop the pattern actually produces.
- [ ] **CR10: `R_max` derived and labelled a ceiling** — **Complete when** `L` and `R_max` are both printed, and the sizing band is handed to the owning skill.
- [ ] **CR11: Cycle pre-registered before it starts** — **Complete when** the lever, the change, the predicted `E_net` direction, the falsifier and `n_required` are all written down and dated.
- [ ] **CR12: Holdout split by close date, 70/30** — **Complete when** the split is dated, the fit and holdout figures are both recorded, and the holdout was not re-fitted.
- [ ] **CR13: `m` counted and `alpha_i = 0.05/m` printed** — **Complete when** the adjusted bar appears in the cycle log and `m` was not reset by a rename or a rotation.
- [ ] **CR14: Outlier sensitivity run** — **Complete when** the largest win and the largest loss have been removed in a re-run and both figures are in the record.
- [ ] **CR15: Kill criteria pre-registered with a rotation clause** — **Complete when** the falsifier names a figure and the five-cycle rotation rule is written on the card.
- [ ] **CR16: Every `p` labelled with sample size, window and regime, and `E_net <= 0` reported as the finding** — **Complete when** no unqualified win rate appears anywhere, the `n_req = n/a` line is quoted verbatim, and the archive contains the cycles the desk would rather forget.

---

## What Good Looks Like

A well-run equity strategy process sounds like a lab notebook, not a tip sheet. It names its corner,
its break-even win rate and its sample size in one breath; it quotes the constraint that failed as
readily as the verdict that passed; it reports `E_net` in R and never in currency; and it refuses to
declare a cycle successful before `n_required` trades exist. When the corner cannot pay, it says so in
one line and rotates, because rotating is a rules change and tuning is not.

**Signs of Excellence:** `p*` is computed from the exits and read aloud before any discussion of the
entry. Every statistic is in R, with the currency view kept only as a contamination control.
`n_required` is logged before the cycle begins, and cycles short of it are reported IN PROGRESS. `m`
only ever increases, `alpha_i = 0.05/m` is printed every cycle, and the holdout figure is quoted even
when it is bad. `R_max` is presented as a ceiling with the sizing band handed off.

**Signs of Dysfunction:** the first number mentioned is a win rate with no `b` beside it; `b` is
computed on dollar P&L; a cycle is declared a success after 20 trades and the holdout window has moved
twice; the cycle counter was reset when the setup tag was renamed; the pooled book figure is quoted
alone with an opposite-sign cohort unmentioned; a position size is recommended on the basis of a
confidence level rather than a streak calculation.

---

## Verification Guardrails

### Pre-Generation

- [ ] The ledger's provenance is declared, or the run is refused until it is.
- [ ] `risk` is the **initial** planned risk at entry, recorded before the outcome was known.
- [ ] `cost` exists on every row; a zero-cost run is labelled as gross of commission and spread.
- [ ] Every statistic is in R, and the currency view is present only as a control.
- [ ] The card's `p*` has been computed from its own exits and compared to a measured `p`.
- [ ] The regime read is cited from `technical-signals-engineer` or `macro-strategist` by name.
- [ ] The cycle's lever, change, predicted direction, falsifier and `n_required` are written down.

### Post-Generation

- [ ] `p`, `b_R`, `E_R`, `c_R`, `E_net`, `n_req`, `L` and `R_max` are all in the record with formulas.
- [ ] No currency-denominated payoff ratio appears as a decision variable.
- [ ] `R_max` is labelled a ceiling, and the sizing band is attributed to its owning skill.
- [ ] `n_req = n/a` (from `E_net <= 0`) is quoted verbatim where it fired.
- [ ] `S* = bps/(100*E)` is present for every card whose stop is under about 3% of price.
- [ ] The holdout figure is recorded with its sample size and split date; `m` and `alpha_i` are in the cycle log and `m` is monotone.
- [ ] The outlier sensitivity run is complete, both figures are recorded, and any synthetic fixture is labelled `SYNTHETIC` wherever its output appears.
- [ ] The full stdout of every cycle is archived under a dated path.

---

## References

| Reference | Covers | Use When |
|-----------|--------|----------|
| [payoff-corners-for-equities.md](references/payoff-corners-for-equities.md) | The corner table with every row derived, the `dE/dp` versus `dE/db` exchange rate, why the 3R corner is the outlier | Choosing a corner, or explaining why a high win rate is not an edge |
| [break-even-payoff-and-the-disposition-trap.md](references/break-even-payoff-and-the-disposition-trap.md) | `b*` and `p*`, the break-even table, the disposition trap derived in full, the three repairs and their caveats | "What win rate do I need", and every `p* = 0.750000` conversation |
| [stop-and-target-arithmetic.md](references/stop-and-target-arithmetic.md) | The three stop units, the ATR-to-percent conversion, structural stop and target selection, trailing exits and the `b` that is not there | Placing a stop or a target, or arguing with one |
| [regime-to-strategy-map.md](references/regime-to-strategy-map.md) | Regime x corner x entry x exit x sizing x owning skill, the two directional claims derived, the volatility-to-size chain | "Trend follow or buy the dip", and any regime filter question |
| [r-units-versus-currency.md](references/r-units-versus-currency.md) | The two-trade proof, the single-added-trade flip, the general agreement condition, how to record `risk` honestly | Before computing any `p` or `b`, and whenever a dollar statistic looks too good |
| [cost-drag-and-stop-distance.md](references/cost-drag-and-stop-distance.md) | `c_R = bps/(100*stop_pct)`, the cost table, the break-even cost `c_R* = E`, the break-even stop `S*`, the five-step routine | "Is my stop too tight", and every tight-stop corner |
| [streak-survival-by-corner.md](references/streak-survival-by-corner.md) | `L` derived and tabulated, `R_max` by corner, what `L` is not, the volatility-to-share-count chain | Sizing, and why the best-paying corner sizes smallest |
| [the-iteration-protocol.md](references/the-iteration-protocol.md) | The seven rules, the pre-registration template, the Bonferroni table, the five-cycle rotation rule, the cycle-log schema | Running a cycle, and diagnosing a suspicious iteration history |
| [overfitting-by-iteration.md](references/overfitting-by-iteration.md) | The eight ways the protocol is defeated while being followed, each with its arithmetic tell and countermeasure | Auditing an iteration history, or your own |
| [strategy-cards.md](references/strategy-cards.md) | The card template, the six invariants, the `setup` tag rules, the authoring order, the five card shapes | Writing or reviewing a card |
| [from-negative-to-positive-walkthrough.md](references/from-negative-to-positive-walkthrough.md) | One book run through three cycles end to end, lever selection, the falsifiers, the recomputed `n_req` | Seeing the protocol applied, and why `b` precedes `p` |
| [what-this-cannot-promise.md](references/what-this-cannot-promise.md) | The assumptions the arithmetic consumes, `p`'s sampling error, the specific things this skill cannot do, the engine's guards as limits | Before quoting anything, and whenever a claim sounds like a guarantee |
| [measured-evidence.md](references/measured-evidence.md) | What the six studies under `examples/` actually measured — where the positivity frontier ends and why cash itself fails it, the `Φ(Sharpe·√fraction)` law and its derived table, why 7,380 configurations produced no all-green year, why narrowing the universe destroys diversification, and the two sleeve lessons — each number with its source path and its tag | Before quoting any "profitable every period" claim, and whenever a study number is about to be repeated without its window |

### Data, sources and thresholds

- `source:` the desk's own closed-trade ledger in the sibling schema (`trade_id,open_date,close_date,pnl,risk,cost,setup,symbol`) — [COMPUTED] every cohort statistic in the checker's `--from-log` output is arithmetic on that one file and nothing else.
- `data from:` `scripts/payoff_check.py`, run on `examples/logs/equity-book-synthetic.csv` — [ILLUSTRATIVE] the shipped ledger is SYNTHETIC, built by hand from the cohort design in its own header, and carries no market information.
- `verified against:` the broker's realised-P&L total for the same window — the one reconciliation that catches missing rows and undeclared cost [COMPUTED] when it agrees; the run is withheld when it does not.
- `source:` `edge-and-payoff-engineering` — owner of the book-level expectancy panel, cohort attribution, the kill list and the sibling ledger schema this skill's `--from-log` reads. [VERIFIED] as an internal-library citation: its `scripts/edge_engine.py` and `examples/logs/hand-check-synthetic.csv` are present in this repository, and this skill's checker reads that fixture successfully.
- `source:` `technical-signals-engineer` — owner of the indicator formulas, the regime definitions and the multi-timeframe rules this skill cites by name rather than restating. [VERIFIED] as an internal-library citation: `references/regime-detection.md`, `references/indicator-formulas.md` and `references/multi-timeframe.md` are present.
- `source:` `macro-strategist` — owner of the macro regime classification and the risk-on/risk-off framework. [VERIFIED] as an internal-library citation: `references/macro-regime-classification.md` and `references/risk-on-risk-off-framework.md` are present.
- `source:` `equity-risk-and-capital-engineer` — owner of gap and event risk, liquidity and exit-cost planning, margin regimes and concentration. [VERIFIED] as an internal-library citation: its references include `gap-and-event-risk.md`, `liquidity-and-exit-cost-planning.md` and `concentration-and-correlation-risk.md`.
- `source:` `equity-position-lifecycle`, `equity-tax-lot-and-exit-management` and `fundamental-analyst` — the open-position decision, the lot and holding-period rules, and candidate selection. [VERIFIED] as internal-library citations: each SKILL.md is present.
- `data from:` your own broker statements for the round-trip cost in basis points — commission, fee and spread schedules are account-, venue- and instrument-specific and change. [ESTIMATED] until 20 fills are recorded, then [BROKER-VERIFIED].
- `data from:` Yahoo Finance, Bloomberg, or your own broker's price series for daily closes and marks — levels only, never an intraday fill. [COMMON-PRACTICE] this skill reads no price data at all; the note exists so the boundary is explicit.
- `published by:` Cboe — its three free index CSVs (`VIX_History.csv`, `VVIX_History.csv`, `SKEW_History.csv`) are the volatility context this skill does **not** load; they are named only because `trading-decision-data-catalogue` cites them as the free index-volatility source. [VERIFIED — Cboe, via that skill's citation].
- `verified against:` exchange rules for session calendars, because whether a nominal "Friday" was a real trading session decides which date a ledger row's close lands on. [VERIFIED] as the class of source; no specific exchange rule is restated here.
- [ESTIMATED] The `MARGINAL` band of `0.20R` per trade and the streak-safety multiple of `1.5` are **named operating choices**, printed by the checker on every run and stated here so they can be argued with. The `0.20R` band sits where a corner is large enough to survive a cost estimate wrong by half, but small enough that a `p` from a small sample cannot separate it from zero; the `1.5` multiple buys about 16 losses instead of 11 at a 20% tolerance. They are **not** presented as data-derived thresholds and this skill says so plainly; the only thresholds here that are mathematically derived are identities, not fitted constants -- `p* = 1/(1+b)`, `c_R* = E`, `S* = bps/(100*E)` and `R_max = D_tol/(L*safety)`. Where a number depends on taste rather than on the algebra, it is labelled `[ESTIMATED]` and printed by the checker so a reader can move it and watch the cards move. No threshold here certifies a strategy.
- [ESTIMATED] `L ~ ln(N)/ln(1/(1-p))` drops a `-1` from the exact expression for the expected longest run, which makes it slightly conservative at small `N` and negligible at large `N`. The checker prints it with a tilde for this reason. Past performance is not a guarantee and no threshold in this skill certifies a strategy.
- `source:` the **Pattern Recognition Engine** meta-layer at `skills/14-finance/options-strategist/references/pattern-recognition-engine.md`. [VERIFIED] as an internal-library citation: the file is present in this repository. **This skill neither consults nor requires it.** That meta-layer names the price pattern a position is holding; this skill is about which PAYOFF CORNER a set of exits buys, which is a different question and is answerable without a pattern name. It is cited here so the boundary is explicit: a card's `b` comes from its exits, never from a pattern label.

## Gotchas

- **A 62% win rate can lose money, and the arithmetic is one line.** `b = 0.5/1.5 = 0.333333` gives `p* = 0.750000`; at `p = 0.62`, `E = 0.62*0.333333 - 0.38 = -0.173333R`, and `-0.193333R` with a 2% cost drag. [COMPUTED]
- **The corner that pays best sizes the smallest.** At `p = 0.40`, `N = 250`: `L = 10.809` and `R_max = 20/(10.809*1.5) = 1.2336%` of equity, against `2.5351%` for the 65%-win-rate range-fade corner. A `+0.600000R` corner and a `1.2336%` ceiling are the same fact. [COMPUTED]
- **Three trades can carry two different payoff ratios.** The shipped `sizing-slip` cohort reads `b_R = 1.000000` and `b_$ = 10.000000`, with `E_R_ratio = -0.333333` and `E$_ratio = +2.666667`. Same three trades, opposite signs; the gap is sizing. [COMPUTED]
- **Cost drag has no size term in it.** `c_R = bps/(100*stop_pct)` — the notional cancels. At 5 bps round trip a 5.0% stop is `c_R = 0.010000R` and a 0.5% stop is `c_R = 0.100000R`, at any position size and any share price. [COMPUTED]
- **One flag on the checker flips a verdict.** The same card at a 0.10% stop and a 5.0% stop gives `E_net = -0.150000R` (NEGATIVE) and `E_net = +0.340000R` (POSITIVE), both at 5 bps. [COMPUTED]
- **Break-even cost equals expectancy.** `c_R* = E`, so a card at `E = +0.200000R` dies at a round-trip cost of 0.20R — and by `S* = bps/(100*E) = 0.250000%`, that is any stop tighter than a quarter of a percent of price at 5 bps. [COMPUTED]
- **`n_req` is a floor, not a target, and the thin corner needs 4x the sample.** `sd` is the two-point sd over `{+b, -1}`, so it is smaller than the spread of real R-multiples: a card reporting `n_req = 42.667` needs *more* than 43 real trades, and `b = 0.75`, `p = 0.65` with `c_R = 0.01` needs 171.434. A thin edge is not a smaller version of a fat one. [COMPUTED]
- **Pooling hides sign structure.** The shipped ledger pools to `E_net = +0.066613R` while containing `trend-breakout` at `+0.590000R` net and `disposition-quick-tp` at `-0.260000R` net. The pooled figure describes no cohort in the book. [COMPUTED]
- **Currency `b` moved 0.800000 to 3.866667 on one added trade** whose R-multiple was only `+1.0R`, because the trade was taken at ten times the risk; the R expectancy stayed negative at `-0.066667R` throughout. And **a realised average loss of `-1.5R` breaks the closed form**: on the shipped `disposition-quick-tp` cohort `p*b - (1-p) = -0.166667` while the realised mean R is `-0.250000R`, the ratio between them being exactly the average loss magnitude. Use the mean. [COMPUTED]
- **`R_max` turns into a share count that moves opposite to volatility.** At `R_max = 1.2336%` of `$100,000`, risk dollars is `$1,233.55`; at a `$10.00` ATR stop that is 123 shares and a `$6,150.00` notional value, and at a `$2.50` stop it is 493 shares and `$24,650.00`. Same risk, four times the shares. [COMPUTED]
- **The synthetic ledger's net P&L is `$5,149.00` against `$5,400.00` gross, on `$251.00` of cost across 62 trades.** It is arithmetic on an invented fixture and is not a track record, a backtest or a finding. [ILLUSTRATIVE]
- **`R_max = n/a` is a result, not a defect.** It fires when `L = 0`: `p = 1` means no losing trade and therefore no streak, and a one-trade window has no streak either. Both are statements about the assumption, not about safety. [COMPUTED]

---

## Anti-Hallucination

**These rules bind every response this skill produces.**

- **Admit uncertainty.** If `p`, the average loss magnitude, the cost rate, the sample behind `p` or the regime that sample came from is unknown, say so before any number is printed.
- **Flag your knowledge cutoff.** This skill's thresholds, examples and figures are frozen as of **2026-10-14**, and every number in `SKILL.md`, `references/` and `examples/checks/` is either the checker's actual stdout or a derivation shown inline. Market regimes, commission schedules, spread levels and venue rules change; re-run the checker before quoting anything as current. Nothing here is a live market statement.
- **Never guess security** identifiers, tickers, contract specifications, venue rules, fee schedules, tax treatment or another person's account configuration. This skill names no instrument anywhere; selection belongs to `fundamental-analyst` and `technical-signals-engineer`. **Never guess a statistic either** — if the checker has not been run on the card or the ledger in question, the number does not exist yet.
- **Label provenance.** `[COMPUTED]` for arithmetic the checker or a stated derivation produced; `[ESTIMATED]` for an assumption, with the derivation shown; `[ILLUSTRATIVE]` for a synthetic fixture; `[VERIFIED]` for a claim checked against a named source — the source is named in the same sentence, and an internal-library citation names the repository file it resolves to.
- **Never claim or imply that a strategy is profitable.** A POSITIVE verdict says an *assumed* `p` and `b` produce a positive expectancy on paper. It is a conditional statement about a configuration, not a prediction, a guarantee or advice. Every such verdict is quoted with its assumed `p`, its `n_req`, and the sentence "the next `n_req` trades are what test it".
- **Never present the synthetic ledger as a result, a backtest or a market finding.** It is invented: invented trades, invented symbols (all prefixed `X`), invented currency, invented dates, and four cohorts designed with round numbers so a reader can verify the arithmetic by hand. It carries no market information whatsoever. The checker echoes its `# PROVENANCE:` lines into every output so the label cannot be detached; a downstream document that quotes one of its numbers without the word SYNTHETIC beside it is wrong regardless of the arithmetic.
- **Never invent a benchmark, a market return, a citation or a comparison.** There is no benchmark and no risk-free rate anywhere in this skill, and the checker prints neither.
- **A guard firing is a result, not an error.** Every `n/a` has a stated reason — `sl = 0` is not a stop, `E_net <= 0` has no `n_req`, currency mode has no R fields, `L = 0` has no streak, `p` outside `[0,1]` is not a probability. Report the reason; never substitute a number.
- **If you cannot verify a claim, say which part is unverified.** A card whose `p` rests on 30 trades, or a ledger whose `risk` column was filled in after the outcomes were known, has an unverified foundation even when every step of arithmetic above it is correct — and that fact belongs in the same paragraph as the number.
