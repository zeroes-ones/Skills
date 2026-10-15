# What this cannot promise

**This skill can identify a positive-expectancy configuration. It cannot guarantee one.** That
sentence is the whole file, and everything below is the detail behind it. Read this before quoting any
number this skill produces, and read it again before acting on one.

## 1. The arithmetic is right and the trade can still lose

The engine computes `E = p*b − (1−p)` exactly. When it reports `+0.600000R` for a `b = 3`, `p = 0.40`
card, that figure is `[COMPUTED]` and it is correct: **if** the win rate is 0.40 and **if** the average
loss is 1R and **if** nothing else moves.

None of those "if"s is established by the arithmetic. Each is an assumption the arithmetic consumes:

| Assumption | Where it comes from | What breaks it |
|---|---|---|
| `p` is 0.40 | the trader's estimate | the market changes; the estimate was never measured |
| the average loss is exactly 1R | the stop is honoured at its level | a gap through the stop turns `−1R` into `−2R` or worse |
| the average win is exactly `+bR` | the target is filled at its level | a partial fill, a missed exit, an early close |
| cost is `c_R` | a reported round trip | slippage is not in the report |
| trades are independent | nothing — it is a modelling convenience | a correlation spike makes them one position |

`E = +0.600000R` on a card is a statement about the card. The account holds dollars, and the dollars
come from a distribution the card only approximates.

## 2. `p` is an estimate, and it carries sampling error

A measured win rate of 0.40 on 50 trades has a standard error of roughly
`sqrt(0.40*0.60/50) = 0.0693` — nearly seven percentage points. The `n_req` figure the engine prints
is exactly the trades needed to separate the mean from zero at two standard errors, and it is
therefore the **minimum** sample before a `p` is even worth quoting.

Three specific consequences:

1. **A `p` without a sample size and a window is not a number.** "My win rate is 62%" on 15 trades has
   a standard error of about 12.5 points. It is compatible with a true `p` anywhere from 0.37 to 0.87.
2. **A `p` measured inside one regime describes that regime.** A trend card's `p` estimated entirely
   during a bull market is partly a measurement of the bull market.
3. **A `p` measured on one corner does not transfer.** The `p` of "buy the pullback to support" in a
   trend is not the `p` of "buy the pullback to support" in a range.

The engine's sensitivity block exists for this reason: if `p − 5pp` flips the verdict, the card is
resting on a five-point estimate that a real sample may not support.

## 3. The iteration protocol exists to prevent self-deception, not to guarantee a result

The seven rules in `the-iteration-protocol.md` — pre-register, one lever, `n_req` per cycle, holdout by
time, Bonferroni-adjusted bar, rotate after five negative cycles, tag every trade — prevent exactly
one failure: **concluding from a sample that could not have supported the conclusion.**

They do not:

- make a negative corner positive,
- make a measured `p` persist,
- detect a regime change,
- validate a rule that cannot be executed at the size intended,
- or produce a profit.

A protocol-following book can be scrupulously honest, out-of-sample validated, and still lose money
next quarter, because the market is not a stationary process and no protocol makes it one.

## 4. The specific things this skill cannot do

| Cannot | Why |
|---|---|
| Predict a price, a level or a direction | it has no price model at all |
| Validate a backtest | it has no engine, no fills, no slippage model and no survivorship correction |
| Recommend an instrument | instrument selection belongs to `fundamental-analyst` and `technical-signals-engineer` |
| Define a regime | regime definitions belong to `technical-signals-engineer` and `macro-strategist` |
| Measure a book's expectancy | that is `edge-and-payoff-engineering`; this skill's `--from-log` is a cohort description, not an attribution engine |
| Set a position size | it derives a *ceiling* from streak survival; the sizing *band* belongs to `trade-sizing-recovery`, `portfolio-signal-manager` and `algorithmic-trader` |
| Manage an open position | that is `equity-position-lifecycle` |
| Decide which lot to sell, or when a holding period ends | that is `equity-tax-lot-and-exit-management` |
| Assess margin, borrow, liquidity or concentration | that is `equity-risk-and-capital-engineer` |
| Tell you what to buy data-wise | that is `trading-decision-data-catalogue` |
| Annualise anything | the engine has no calendar-year return model and does not print one |
| Claim a benchmark comparison | there is no benchmark anywhere in the arithmetic |

## 5. The engine's own guards are limits, not defects

Every refusal in the output is a limit stated out loud:

- **`n_req = n/a` when `E_net <= 0`.** No sample size reaches `+2σ` on a non-positive mean. A tool that
  printed a number here would invite the reader to wait for one.
- **`sd` is the two-point sd.** It knows only `{+b, −1}`. Real R-multiples spread between those points,
  so the sample you need is **larger** than `n_req`, never smaller.
- **`b = n/a` when `sl = 0`.** A 0R stop is not a stop, and the engine refuses rather than dividing.
- **`p` outside `[0,1]` is refused.** It is not a probability and no expectancy is computed from it.
- **`R_max` is reported `n/a` when `L = 0`.** One trade has no streak; a card with `p = 1` has no
  losing trade and therefore no streak ceiling. Both are statements about the assumption.
- **Currency mode reports every R field as `n/a`.** The engine will not invent a denominator.
- **A zero-cost warning fires when the ledger has no `cost` column.** Zero cost is flattering.

## 6. The synthetic fixtures are not evidence

`examples/logs/equity-book-synthetic.csv` is **SYNTHETIC**. Every trade, symbol, date and dollar figure
in it is invented, and its four cohorts were designed with round numbers so that a reader can verify
the arithmetic by hand. It carries **no market information**. Its `+0.590000R` cohort is arithmetic on
a fixture, not a track record, and it must never be quoted as one.

Every card in `examples/checks/` is `[ILLUSTRATIVE]`: the `p` in each one is an assumption. A POSITIVE
verdict there says an assumed `p` and `b` produce a positive expectancy on paper. It says nothing about
whether that `p` is attainable.

**The engine echoes each log's own `# PROVENANCE:` lines into its output specifically so that an
output cannot be detached from the label of the data behind it.** If you see a figure from that log in
a document without the word SYNTHETIC beside it, the document is wrong regardless of the arithmetic.

## 7. What "positive expectancy" does and does not mean

`E_net > 0` means: **on the assumed `p`, the assumed `b` and the assumed cost, the average trade adds
to the account.** That is a conditional statement and it is the only one the arithmetic can make.

It does not mean:

- the strategy is "proven" — nothing here has a significance test against a null of no edge;
- the strategy will be positive next month;
- the trader executing it will realise the assumed `p`;
- the drawdown will stay inside the tolerance `D_tolerance` was set to;
- any particular trade, week, month or year will be profitable.

The correct sentence to write next to any positive verdict is: *"On an assumed `p` of X and a payoff
ratio of Y, the expectancy is Z R per trade. The `p` is an estimate; the next `n_req` trades are what
test it."*

## 8. When to stop and hand off

Stop and hand off rather than extrapolate when any of these is true:

- **A request needs an instrument, a level, or a date.** Hand to `fundamental-analyst` or
  `technical-signals-engineer`.
- **A request needs a regime label.** Hand to `technical-signals-engineer` or `macro-strategist`.
- **A request needs a measured expectancy over a whole book, or a cohort attribution.** Hand to
  `edge-and-payoff-engineering`.
- **A request needs a review cadence or a metric definition.** Hand to
  `timeframe-performance-statistics` or `trade-performance-analyst`.
- **A request needs a lot choice, a wash-sale check or a holding-period clock.** Hand to
  `equity-tax-lot-and-exit-management`.
- **A request needs a margin figure, a borrow rate, an exit-cost estimate or a concentration limit.**
  Hand to `equity-risk-and-capital-engineer`.
- **A request asks whether the strategy is "safe" or "guaranteed".** The answer is no, in both cases,
  and this file is the citation.

## 9. Admit uncertainty, every time

If any of `p`, `b`, `c_R`, the average loss magnitude, or the sample behind `p` is unknown, say so
**before** any number is printed. An output computed on unknown inputs is arithmetic on unknown inputs.

The honest form of any answer this skill gives is:

> Here is the payoff corner your rules buy. Here is the break-even win rate it requires. Here is
> whether the win rate you assume clears that bar, and by how much. Here is the sample you would need
> before the answer is a measurement rather than an assumption. **Here is what I do not know.**

Past performance does not predict future results, and a positive expectancy configuration is not a
prediction of profit. Neither claim is a hedge; both are the content of this file.

## Cross-references

- The protocol this file bounds: `the-iteration-protocol.md`
- How the protocol is defeated anyway: `overfitting-by-iteration.md`
- The guards and their reasons: `payoff-corners-for-equities.md`,
  `streak-survival-by-corner.md`, `cost-drag-and-stop-distance.md`
- The synthetic fixtures: `../examples/README.md`,
  `../examples/logs/equity-book-synthetic.csv`
- The sibling skill that owns book-level expectancy: `edge-and-payoff-engineering`
