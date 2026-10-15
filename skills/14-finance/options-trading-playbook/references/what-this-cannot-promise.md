# What This Cannot Promise

This file is the honest boundary of the skill. It is not a disclaimer bolted to the
end; it is the part that says what the arithmetic does and does not establish, so
that a reader who skips everything else still knows what they are holding.

**Read this before acting on anything else in this skill.**

---

## 1. The arithmetic identifies a positive-expectancy configuration. It cannot guarantee one.

`payoff_check.py` answers a conditional question: *if* the win rate is `p` and the
payoff ratio is `b`, then the expectancy is `p·b − (1−p)` and the break-even win rate
is `1/(1+b)`. That is a theorem. It is true of every tradeable payoff, in every
market, forever.

It does **not** establish that the win rate is `p`. It does not establish that the
payoff ratio will be `b`. It has no market data, no backtest, no price history and no
forecast, and it makes no prediction about any instrument.

A `POSITIVE` verdict means: *on these inputs, this corner pays.* It means nothing
about whether the inputs are right. Every POSITIVE verdict in `examples/checks/` is a
statement about a card, not about a strategy's future.

**Therefore:** no output of this skill, and no sentence in it, should ever be read as
"this strategy is profitable". If a document in this repository implies that, the
document is wrong regardless of the arithmetic inside it.

---

## 2. `p` is an estimate with sampling error, and the error is often larger than the edge.

This is the single most important honest statement in the skill.

A win rate measured over `n` decided trades has a standard error of approximately

```
se_p = sqrt( p (1 - p) / n )                              [COMPUTED]
```

| `p` | `n` | `se_p` | Approximate 95% interval |
|---|---|---|---|
| 0.35 | 40 | 0.0754 | 0.20 – 0.50 |
| 0.35 | 250 | 0.0302 | 0.29 – 0.41 |
| 0.50 | 40 | 0.0791 | 0.35 – 0.65 |
| 0.68 | 250 | 0.0295 | 0.62 – 0.74 |
| 0.78 | 40 | 0.0655 | 0.65 – 0.91 |
| 0.80 | 40 | 0.0632 | 0.68 – 0.92 |
| 0.80 | 250 | 0.0253 | 0.75 – 0.85 |

Now put the interval against the requirement. The `b = 0.25` credit card needs
`p* = 0.80` just to break even. Measured over 40 trades at `p = 0.80`, the interval
runs from **0.68 to 0.92** — it contains the break-even rate *and* six points of
comfortable profit *and* twelve points of loss. **A 40-trade record cannot answer
the question the card asks.** Neither can a 250-trade record answer it precisely:
the interval is 0.75 to 0.85, still spanning the whole decision.

Two consequences follow, and both are acted on elsewhere in this skill:

- The sample needed is computed (`n_req`), not chosen. See
  `references/the-iteration-protocol.md` step 3.
- A win rate with a wide interval cannot be used to set risk per trade. See
  `references/streak-survival-by-corner.md`.

---

## 3. The iteration protocol exists to stop self-deception. It does not guarantee a result.

The protocol's rules are all *defensive*:

| Rule | What it prevents |
|---|---|
| Pre-register the hypothesis | reading a known outcome as a prediction |
| One change per cycle | attributing a mixed result to the wrong lever |
| A cycle is `n_req` trades | measuring a winning streak as evidence |
| Hold out the last 30% | fitting the answer to the data |
| Count cycles, apply Bonferroni | a searched result passing an unsearched test |
| Five cycles, then rotate | tuning a card that has no edge |
| Log the `setup` tag | losing the record that would have shown the search |

Not one of those rules increases the chance of finding an edge. Every one of them
increases the chance that a *false* edge is recognised as false. **The protocol's
output is honest evidence, and honest evidence is frequently negative.**

A book run under this protocol may legitimately end with every corner retired. That
is a correct outcome of the process, not a failure of it.

---

## 4. The costs are estimates too.

Fees, commissions, regulatory charges and half-spreads are inputs to this skill, not
its findings. `cost_per_trade = fee_per_contract × legs × 2` is the *shape* of the
cost; the number you put in `--fee-per-contract` is yours to verify against your own
broker's schedule and the current exchange fee table.

`[COMMON-PRACTICE]` The half-spread is usually the largest component and the one most
often omitted. `[VERIFIED]` the round-trip ticket count is two per leg — one to open,
one to close — for a standard listed option. `[VERIFIED]` the standard US
equity-option contract multiplier is 100, which is why `--multiplier` defaults to it
and is printed rather than assumed. These are mechanics, not measurements of your
account.

No fee schedule, no exchange rule, and no product listing in this skill is asserted
to be current. Exchange rules change; verify them where they are published.

---

## 5. What the sensitivity panel does and does not do

`payoff_check.py` prints `E` at `p ± 5pp`, at `b ± 0.25`, and at `cost × 0.5 / × 2`.
That panel shows **the sensitivity of the arithmetic to its inputs.** It is not a
confidence interval, not a scenario probability, and not a bound. It says "if this
input were five points different, here is what the formula would say". It assigns no
probability to any of those alternatives.

A `MARGINAL` verdict is the tool being honest about resolution: `|E_net| < se_E` at
the planned sample. It is not a hedge and it is not a soft "probably fine". A card
that is `MARGINAL` cannot be distinguished from no edge, and no amount of trading
style changes that.

---

## 6. Nothing here is market data, and nothing here is a benchmark.

This skill contains:

- **No price series.** No OHLCV, no quote, no settlement, no implied vol, no
  realised vol.
- **No vendor data.** Sourced from exchange rules only, and only for ticket counts
  and the contract multiplier — no vendor feed, no network call, no third-party
  dependency anywhere in the engine.
- **No benchmark and no risk-free rate.** The engine does not compute a Sharpe, a
  Sortino, an alpha, or any comparison against an index. A claim about
  outperformance is outside its scope entirely.
- **No backtest.** `examples/logs/synthetic-options-log.csv` is
  **SYNTHETIC / ILLUSTRATIVE**. It is invented by the skill author, it is not market
  data, it is not a backtest, and it carries no market information. Any number
  derived from it describes the file and nothing else. The label travels with the
  data: the generator writes it into the file's header comments and the engine echoes
  it into every output.

Do not quote a synthetic-fixture number as a finding about any instrument, strategy,
volatility regime or period. If you see one quoted that way, in this repository or
anywhere else, the quoting document is wrong.

---

## 7. Correlation is outside this skill.

Every number here is per-card and per-cohort. A book of five short-premium positions
in the same index is not five independent draws; the streak, the standard error and
the survivable risk per trade are all computed as though it were. The correlation and
concentration question belongs to `options-risk-engineer`, and the answer there will
make this skill's numbers *more* conservative, not less.

Specifically: `sd`, `n_req` and `R_max` all assume independent trades. Correlated
losses raise the realised `sd` of the book above the per-card figure and lower the
risk per trade the book can survive.

---

## 8. What to do when the tool says something you dislike

In order:

1. **Check the `R BASIS` line.** Most wrong outputs are a wrong `R`. If the stop is
   inside the structural max loss and `R` was defined as the max loss, every number
   below is wrong in the flattering direction.
2. **Check the `p`.** It is an estimate, and the panel shows what happens five points
   either way. If the verdict depends on `p` being the number you typed, the verdict
   depends on something you have not measured.
3. **Check the cost.** `c_R = 0` is the most flattering possible input. A card that is
   positive only at zero cost is not positive.
4. **Then accept the verdict and change the card.** Not the inputs.

The tool is deterministic: identical inputs produce byte-identical output, verified
by `scripts/verify-skill.sh` running each documented command twice and diffing. If you
get a different answer, your inputs differ. That is the only way it can differ.

---

## 9. Knowledge boundary

`Flag your knowledge cutoff`: the option mechanics referenced here — the two-tickets-
per-leg round trip, the 100-share standard multiplier, assignment and exercise being
broker- and exchange-fee events — are long-standing listed-option conventions, and
they are the only external facts this skill relies on. Product listings, fee
schedules, margin requirements and exchange rules have all changed over time and
should be verified at the source before being relied on.

`Admit uncertainty`: this skill's algebra is exact and its inputs are not. Where this
skill states a number, it is either the tool's own output, a `[COMPUTED]` derivation
with the formula shown, an `[ESTIMATED]` figure with its derivation, or an
`[ILLUSTRATIVE]` invented value. Where it cannot know something, it says so and
stops — it does not substitute a plausible number.

`Never guess security`: nothing in this skill selects, recommends or prices a security.
It prices a *payoff*.

---

## The one-sentence version

**This skill can tell you what a payoff pays, what win rate it requires, how long a
sample it needs, and where the cost crosses the edge — and it cannot tell you whether
your win rate is real, whether the market will supply it, or whether the card will
make money. Everything in it that looks like a promise is a conditional.**
