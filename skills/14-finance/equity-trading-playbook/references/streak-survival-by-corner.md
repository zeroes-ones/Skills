# Streak survival by corner

`L ≈ ln(N)/ln(1/(1−p))` is the expected **longest** run of consecutive losses in `N` trades. It
depends on `p` and `N` and on nothing else — not on `b`, not on the edge, not on the instrument. From
it, the risk per trade ceiling is

```
R_max = D_tolerance / (L * safety)
```

This file derives both, tabulates them by corner, and states plainly what the formula does and does
not promise.

## 1. Where `L ≈ ln(N)/ln(1/(1−p))` comes from

Model the outcomes as independent with win probability `p`. In a run of `N` trades, the number of
runs of losses is about `N(1−p)`, so the expected number of opportunities for a losing streak is
about `N(1−p)`; a given opportunity fails to produce a streak of length `k` with probability
`1 − (1−p)^k`. Setting the expected number of streaks of length `k` equal to 1:

```
N * (1-p) * (1-p)^k  ~  1
N * (1-p)^(k+1)      ~  1
k+1                  ~  ln(N) / ln(1/(1-p))
L                    ~  ln(N) / ln(1/(1-p))   - 1, approximated here as the leading term
```

The formula implemented is `L = ln(N)/ln(1/(1−p))`, i.e. the `−1` is dropped. **That makes `L`
slightly conservative at small `N` and negligible at large `N`.** It is a named approximation, and
`payoff_check.py` prints it as `L ~ ...` with the tilde for exactly that reason.

Two guards fire on degenerate input, and both are deliberate:

- `p = 0` → every one of the `N` trades loses → `L = N`. The formula would divide by `ln(1) = 0`.
- `p = 1` → nothing loses → `L = 0`, and `R_max` is reported `n/a` with the reason. There is no
  streak ceiling for a card with no assumed losing trade.

## 2. The table, at `N = 250` trades

`R_max` is at `D_tolerance = 20%` of equity and `safety = 1.5`.

| `p` | `1/(1−p)` | `ln(1/(1−p))` | `L` at N=250 | `L` at N=1000 | `R_max` at N=250 |
|---|---|---|---|---|---|
| 0.25 | 1.333333 | 0.287682 | 19.193 | 24.012 | 0.6947% |
| 0.30 | 1.428571 | 0.356675 | 15.480 | 19.367 | 0.8613% |
| 0.333333 | 1.500000 | 0.405465 | 13.618 | 17.037 | 0.9791% |
| 0.40 | 1.666667 | 0.510826 | **10.809** | 13.523 | **1.2336%** |
| 0.42 | 1.724138 | 0.544727 | 10.136 | 12.681 | 1.3154% |
| 0.45 | 1.818182 | 0.597837 | **9.236** | 11.556 | **1.4437%** |
| 0.50 | 2.000000 | 0.693147 | 7.966 | 9.966 | 1.6738% |
| 0.55 | 2.222222 | 0.798508 | 6.915 | 8.651 | 1.9283% |
| 0.571429 | 2.333333 | 0.847298 | 6.517 | 8.153 | 2.0461% |
| 0.60 | 2.500000 | 0.916291 | 6.026 | 7.539 | 2.2127% |
| 0.625 | 2.666667 | 0.980829 | 5.629 | 7.043 | 2.3685% |
| 0.65 | 2.857143 | 1.049822 | **5.259** | 6.580 | **2.5351%** |
| 0.70 | 3.333333 | 1.203973 | 4.586 | 5.737 | 2.9074% |
| 0.75 | 4.000000 | 1.386294 | 3.983 | 4.983 | 3.3477% |

Two readings, and they move in opposite directions:

1. **A low `p` implies a long losing streak** — 10.809 at a 40% hit rate, against 5.259 at 65%. This
   is the first cost of the high-`b` corners, and it is paid in position size.
2. **The longer the window, the longer the streak** — `L` at 1000 trades is 25% larger than at 250 for
   `p = 0.40`. A trader who has survived 250 trades has not yet met the streak a 1000-trade career
   contains.

## 3. The table by corner

| Corner | `b` | assumed `p` | `p*` | `L` | `R_max` | The trade-off in one line |
|---|---|---|---|---|---|---|
| Trend / breakout 3R | 3.00 | 0.40 | 0.250000 | 10.809 | **1.2336%** | pays +0.600000R, sizes smallest |
| Trend / breakout 2R | 2.00 | 0.40 | 0.333333 | 10.809 | **1.2336%** | pays +0.200000R, sizes smallest |
| Failed breakout 2R | 2.00 | 0.42 | 0.333333 | 10.136 | 1.3154% | pays +0.260000R |
| Event drift 2R | 2.00 | 0.45 | 0.333333 | 9.236 | 1.4437% | pays +0.350000R |
| The 1:1 corner | 1.00 | 0.45 | 0.500000 | 9.236 | 1.4437% | pays −0.100000R: size is irrelevant |
| Mean reversion 0.75R | 0.75 | 0.65 | 0.571429 | **5.259** | **2.5351%** | pays +0.137500R, sizes largest |
| Disposition 0.5R / 1.5R | 0.33 | 0.62 | **0.750000** | 5.706 | 2.3365% | pays −0.173333R: size is irrelevant |

**Note where `b` does not appear.** Rows 1 and 2 have the same `L` and the same `R_max` because `L`
depends only on `p`. The 3R corner and the 2R corner have identical streak risk at the same hit rate,
and entirely different expectancies. That is `dE/db = p` in `payoff-corners-for-equities.md`: the
payoff lever moves `E` without touching the streak.

**Note what the 1:1 and disposition rows say.** `R_max` for a negative-expectancy card is a
meaningless number. The tool still computes and prints it, because the formula is defined, but the
verdict is NEGATIVE and no size makes it otherwise.

## 4. `L` is an expectation of the MAXIMUM, not a bound

Four things `L` is not:

1. **`L` is not the most losses you will have in a row.** It is the expected length of the *longest*
   run. Half of all windows contain a longer run. The `safety = 1.5` multiple in `R_max` exists to
   absorb exactly that, and 1.5 is a named choice, not a derivation.
2. **`L` is not a bound conditional on a losing regime.** The derivation assumes independent trades
   at constant `p`. In a correction, a downturn or a crash the trades are *not* independent — they
   are the same bet — and the realised streak exceeds `L`. This is the honest limit of the whole
   streak framework.
3. **`L` is not the number that stops you out.** The binding constraint is the drawdown tolerance
   `D_tolerance`, which is a policy decision. `R_max` translates one into the other; it does not
   choose the tolerance.
4. **`L` does not depend on the outcome sizes.** A `−1R` stop and a `−4R` gap are both "a loss" in
   the streak count, and wildly different in equity. Streak survival assumes the stop holds, which is
   `what-this-cannot-promise.md` territory.

## 5. `R_max` and what it is for

```
R_max = D_tolerance / (L * safety)
```

At `D_tolerance = 20%`, `p = 0.40`, `N = 250`, `safety = 1.5`:

```
R_max = 20 / (10.809 * 1.5) = 20 / 16.213 = 1.2336% of equity per trade
```

Meaning: if an 11-trade losing streak arrives at `1.2336%` per trade, the book loses about 13.6% —
inside the 20% tolerance, with room for the streak being a bit longer than expected. Worked:

```
11 losses x 1.2336% = 13.57% of equity
16 losses x 1.2336% = 19.74% of equity     <-- the tolerance is reached near 16
```

So `safety = 1.5` buys about 16 losses rather than 11 at the same tolerance. **That is what the
multiple is buying, stated in losses rather than in percent.**

**`R_max` is a ceiling, and only a ceiling.** It says "no more than this, or the streak arithmetic is
violated." It says nothing about the right size below that ceiling, and the band it sits in is the
business of `trade-sizing-recovery`, `portfolio-signal-manager` and `algorithmic-trader`. This skill
derives the ceiling; it does not place the bet.

## 6. `R_max` and volatility move in opposite directions

`R_max` is a percentage of *equity*. The dollars it permits are fixed by the account, while the
shares it permits fall as volatility rises:

```
risk_dollars = equity * R_max_pct / 100
shares       = floor( risk_dollars / (k * ATR) )
```

At `equity = $100,000`, `R_max = 1.2336%`, `risk_dollars = $1,233.55`:

| `k*ATR` (stop distance per share) | shares | notional at `$50` |
|---|---|---|
| `$10.00` | 123 | `$6,150` |
| `$5.00` | 246 | `$12,300` |
| `$2.50` | 493 | `$24,650` |

The dollar risk is identical in every row. **A high-volatility regime therefore does not raise your
risk; it lowers your share count.** A trader who keeps the share count fixed through a volatility
change has silently raised their `R`, and the streak arithmetic above no longer describes their book.

## 7. The one-line check

For any card, before trading it:

```
L     = ln(N) / ln(1/(1-p))          with your measured p and your intended N
R_max = D_tolerance / (L * 1.5)      as a percent of equity
```

If `R_max` is smaller than the size you intended, either the tolerance is too low, the window `N` is
too long, or `p` is lower than you assumed. All three are worth knowing before the streak rather than
after it.

## Cross-references

- The corners and their `E`: `payoff-corners-for-equities.md`
- Why a low `p` costs nothing in `E` but everything in size: `payoff-corners-for-equities.md`
- Volume and gap risk, which the streak model ignores: `equity-risk-and-capital-engineer` →
  `references/gap-and-event-risk.md`, `references/margin-regimes-and-forced-liquidation.md`
- Where the sizing band goes: `trade-sizing-recovery`, `portfolio-signal-manager`, `algorithmic-trader`
- What this arithmetic cannot promise: `what-this-cannot-promise.md`
