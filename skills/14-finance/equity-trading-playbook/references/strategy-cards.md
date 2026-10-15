# Strategy cards — the template and the invariants

A **strategy card** is the written spec of a payoff corner: what arms it, where it exits, how big it
is, and when it is declared wrong. This file is the template and the authoring rules. The concrete
cards — SC-0 through SC-6, with their worked arithmetic — are in
`../examples/strategy-cards.md`.

The distinction matters. This file says **what a card must contain and why**; the examples file
contains **actual cards**. A card missing any of the four required fields below is not a card, and
a card whose corner has never been computed is not testable.

## 1. The template

```
CARD <ID> — <name>
  setup tag      : <the cohort key written into every trade's `setup` column>
  corner         : b = <tp/sl>   p* = 1/(1+b) = <value>   assumed p = <value>
  E              : <p*b-(1-p)>R    E_net = <E - c_R>R    verdict <POSITIVE|MARGINAL|NEGATIVE>
  n_required     : <n_req from payoff_check.py>

  ENTRY
    condition    : <mechanical. If it contains "looks like", it is not a condition>
    time frame   : <the timeframe the condition is evaluated on>
    confirmation : <optional; must be mechanical, and it changes p, so it must be measured>

  EXITS
    stop         : <the level that proves the entry WRONG, and its distance in R / ATR / percent>
    target       : <the level the move can reach, and its distance in R>
    partials     : <none, or the exact rule. A partial exit changes b and must be computed>
    trail        : <none, or the exact rule, and the admission that b becomes a distribution>

  REGIME FILTER
    read         : <which read must be true>
    supplied by  : <technical-signals-engineer | macro-strategist> and the reference file
    disarmed by  : <the read that turns the card OFF>

  SIZE
    ceiling      : R_max = D_tol/(L*safety) = <value>% of equity
    derivation   : L = ln(N)/ln(1/(1-p)) = <value> at p = <value>, N = <value>
    band         : <owned by trade-sizing-recovery / portfolio-signal-manager / algorithmic-trader>

  COST
    c_R          : <bps/(100*stop_pct)>R  at <bps> bps round trip and a <stop_pct>% stop
    S*           : <bps/(100*E)>% of price — the tightest stop at which the card still pays

  KILL CRITERIA
    measurement  : <the exact figure that falsifies the card>
    horizon      : <n_required trades, not a date>
    stop rule    : after 5 cycles with E_net <= 0, ROTATE the corner, do not tune
```

## 2. The six invariants

Every card must satisfy all six. Each is a check with a failure response.

| # | Invariant | Failure response |
|---|---|---|
| I1 | **The entry condition is mechanical.** A second person reading it would enter the same trade on the same bar | rewrite it, or the card cannot be measured, because two people are running two cards under one tag |
| I2 | **The exit rules produce a computable `b`.** If a partial exit or a trail is present, `b` is replaced by the *measured* average win / average loss ratio and the card says so | compute `b` from the realised ledger, not from intent |
| I3 | **`p*` is printed on the card before any trade.** The card states the break-even win rate its own exits imply | compute `p* = 1/(1+b)`; if it is above the best measured `p` for this setup, the card is a donation |
| I4 | **A regime filter exists and is cited.** The card names which read arms it and which read disarms it | add the filter, or the card's `p` is measured across regimes it was not designed for |
| I5 | **`R_max` is derived from the streak arithmetic, not from confidence.** `L` and `R_max` are both printed | derive them; the sizing *band* is not yours to set, but the *ceiling* is |
| I6 | **Kill criteria are pre-registered, with a trade horizon and a rotation clause** | write them before the first trade. A card with no falsifier is SC-0 in `../examples/strategy-cards.md` |

## 3. The `setup` tag is load-bearing

Every trade logged under a card carries the card's `setup` tag, and the tag is what makes cohort
attribution possible. `payoff_check.py --from-log` groups by it; `edge-and-payoff-engineering` builds
the kill list from it.

Rules for the tag:

- **One tag per card.** A card named `trend-pullback` writes `trend-pullback` into every trade,
  including the losers, including the trades abandoned early.
- **A tag is never recycled for a changed card.** If the entry rule changes materially, the card gets
  a new tag. Otherwise the cohort contains two populations and its `p` describes neither.
- **A trade with no tag does not exist for attribution.** It still affects the account, so it must
  either be tagged or reconciled as something else (an unplanned trade, an error, a hedge).
- **Tags are stable strings.** `trend-pullback`, not `Trend Pullback / v2 (final)`.

The shipped synthetic ledger demonstrates why: four tags, four corners, pooled `E_net = +0.066613R`,
and inside it one cohort at `+0.590000R` and another at `−0.260000R`. Drop the tags and the pooled
number is all that is left, and the pooled number describes none of the cohorts.

## 4. The authoring order

Write a card in this order. Each step constrains the next, and doing them out of order is how a card
ends up with exits chosen to justify an entry.

```
1. REGIME READ      what read must be true?                    (cited from a neighbour skill)
2. ENTRY            what mechanical condition fires?           (only inside that read)
3. STRUCTURE        what level does the entry invalidate?      -> the STOP
4. STRUCTURE        what level can the move reach?             -> the TARGET
5. CORNER           b = tp/sl ; p* = 1/(1+b)                   (READ THIS BEFORE PROCEEDING)
6. PLAUSIBILITY     is p* below the best p I have measured on this shape?
                    if no -> go back to step 4, and change the EXITS
7. COST             c_R = bps/(100*stop_pct) ; S* = bps/(100*E)
8. MEASUREMENT      n_req = 4*(sd/E_net)^2 ; L = ln(N)/ln(1/(1-p))
9. SIZE             R_max = D_tol/(L*safety)
10. KILL            the falsifier, the horizon, the rotation clause
```

Step 5 is the step that is skipped, and skipping it is the entire mechanism by which a card with
`p* = 0.750000` gets traded at a 62% hit rate.

## 5. The five card shapes, and what each is for

| Shape | `b` | `p*` | Regime it belongs to | The one thing to watch |
|---|---|---|---|---|
| Trend continuation / pullback | 2–5 | 0.17–0.33 | trending / uptrend | it sizes *smallest*: `L` is longest at a low `p` |
| Breakout from contraction | 2–3 | 0.25–0.33 | trending, volatility expanding | the false break is the other card (below) |
| Range fade / mean reversion | 0.5–1.0 | 0.50–0.67 | range-bound | it needs `n_req` trades before the edge is even measurable |
| Failed breakout / reversal | 1.5–3 | 0.25–0.40 | range-bound, trend-end | `p` is an assumption, not a finding |
| Event drift (post-event) | 1.5–3 | 0.25–0.40 | event-driven | gap risk through the stop is unmodelled by the algebra |

And the anti-shape, which is not a card:

| Anti-shape | `b` | `p*` | Why it happens | Why it loses |
|---|---|---|---|---|
| **The disposition default** | **0.333333** | **0.750000** | cut winners, let losers run | a 62% win rate is 13 points short of break-even |

## 6. Where a card's numbers come from, and where they do not

| Field | Source | Tag |
|---|---|---|
| `b`, `p*`, `E`, `E_net`, `f*`, `sd`, `n_req`, `L`, `R_max`, `c_R`, `S*` | `payoff_check.py`, or the arithmetic shown in `../examples/strategy-cards.md` | `[COMPUTED]` |
| assumed `p` | the trader's estimate, and it is an *assumption* | `[ESTIMATED]` |
| `bps` round-trip cost | the trader's own statement and fills | `[ESTIMATED]` until measured from 20 fills, then `[BROKER-VERIFIED]` |
| regime read | `technical-signals-engineer` / `macro-strategist` | cited, not restated |
| sizing band | `trade-sizing-recovery` / `portfolio-signal-manager` / `algorithmic-trader` | cited, not restated |

**A card must never carry a number whose source is not one of those rows.** In particular, a card must
never contain a measured `p` without the sample size and the window it was measured over, because an
unqualified `p` is the single most misleading figure in the whole skill.

## 7. The card review, quarterly

- [ ] Every open card has an `n_required` and a trades-so-far count.
- [ ] Every open card's last cycle has a holdout figure and an adjusted `alpha_i`.
- [ ] The cycle counter `m` is monotone and has not been reset by a rename.
- [ ] Any card with five cycles at `E_net <= 0` has been **rotated**, not tuned.
- [ ] Every `setup` tag in the ledger is attached to a card, or is explicitly reconciled.
- [ ] The pooled book figure is reported **with** the cohort table, never alone.
- [ ] Any card whose `p` was measured in one regime is labelled with that regime.
- [ ] **Complete when** each card has a verdict, a sample size, a window and a next action.

## Cross-references

- The concrete cards: `../examples/strategy-cards.md`
- The corners the shapes come from: `payoff-corners-for-equities.md`
- The disposition anti-shape, derived: `break-even-payoff-and-the-disposition-trap.md`
- Which shape belongs to which regime: `regime-to-strategy-map.md`
- The measurement each card commits to: `the-iteration-protocol.md`
- The permanent limits a card inherits: `what-this-cannot-promise.md`
