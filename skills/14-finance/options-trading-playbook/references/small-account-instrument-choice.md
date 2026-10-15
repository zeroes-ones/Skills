# Small-Account Instrument Choice

Below a certain account size the options structure itself becomes the cost. This
file derives the crossover — where a multi-leg, multi-rung options card stops
paying its own fees — and states the instrument choice that follows from it. Every
number is `[COMPUTED]` from the ticket arithmetic in
`references/cost-drag-per-leg-and-per-rung.md`.

This file owns **instrument choice given a size constraint**. It does not own the
size constraint itself: how much of an account may be risked per trade is
`trade-sizing-recovery`'s number, and what the book's aggregate exposure should be
is `options-risk-engineer`'s.

---

## The asymmetry

Two facts, both arithmetic, and they point in opposite directions:

```
cost_per_trade = fee_per_contract x legs x 2      scales with LEGS
c_R            = cost_per_trade / R_dollars       rises as 1 / R_dollars
```

An options structure's cost is per contract, per leg, per ticket. A stock or ETF
position's cost is a commission plus a spread stated in **basis points of
notional** — roughly 0.05% to 0.30% round trip for liquid instruments
`[COMMON-PRACTICE]`. The options fee does not care how small the position is; the
equity cost does.

Take a `$5.20` round trip on a 4-leg structure and ask what notional an equity
equivalent would have to be for the same relative cost at 0.15% round trip:

```
notional = 5.20 / 0.0015 = $3,466.67                        [COMPUTED]
```

**A 4-leg options ticket at `$0.65` costs the same *relatively* as a `$3,467`
equity trade.** For a `$500` max-loss structure, `c_R = 5.20/500 = 0.0104R` and the
equity equivalent is `5.20/0.0104 = $500` — small accounts are not merely paying
more, they are paying a fixed fee against a small denominator.

---

## The crossover by structure size

Long-premium card, `b = 2.5`, `p = 0.35`, `E = 0.2250R` `[COMPUTED]`. `E_net` and
the verdict are the tool's own output for each row (see the commands at the end of
this file):

| Structure `R` | Legs | `c_R` | `E_net` | Verdict | Share of edge lost to cost |
|---|---|---|---|---|---|
| `$500` | 1 | 0.0026 | +0.2224 | POSITIVE | 1.2% |
| `$500` | 2 | 0.0052 | +0.2198 | POSITIVE | 2.3% |
| `$500` | 4 | 0.0104 | +0.2146 | POSITIVE | 4.6% |
| `$100` | 2 | 0.0260 | +0.1990 | POSITIVE | 11.6% |
| `$100` | 4 | 0.0520 | +0.1730 | POSITIVE | 23.1% |
| `$50` | 4 | 0.1040 | +0.1210 | POSITIVE | 46.2% |
| `$25` | 4 | 0.2080 | +0.0170 | MARGINAL | 92.4% |
| `$15` | 4 | 0.3467 | −0.1217 | NEGATIVE | 154.1% |

The "share of edge lost" column is `c_R / E`. At `$25` it is 92% — the card still
technically pays and is indistinguishable from noise. At `$15` the cost exceeds the
edge.

Now the same test on the **credit** corner, which is the corner small accounts are
usually pushed toward, because it is presented as the low-capital strategy. Use
`b = 0.5, p = 0.68` (`E = +0.0200R` gross, `se_E = 0.0443R`, a thin edge
`[COMPUTED]`). Every `E_net` and verdict below is the tool's own output:

| Structure `R` | Legs | `c_R` | `E_net` | Verdict |
|---|---|---|---|---|
| `$500` | 4 | 0.0104 | +0.0096 | MARGINAL |
| `$100` | 1 | 0.0130 | +0.0070 | MARGINAL |
| `$100` | 2 | 0.0260 | −0.0060 | MARGINAL |
| `$100` | 4 | 0.0520 | −0.0320 | MARGINAL |
| `$50` | 1 | 0.0260 | −0.0060 | MARGINAL |
| `$50` | 2 | 0.0520 | −0.0320 | MARGINAL |
| `$50` | 4 | 0.1040 | **−0.0840** | **NEGATIVE** |

Read the column of verdicts, not the column of signs. The thin credit edge is
already inside one standard error at `$500` — before any of this matters — and
then stays `MARGINAL` all the way down to `$50`, where a four-leg structure finally
drives it past the noise band into `NEGATIVE`. **`MARGINAL` is the more dangerous
verdict of the two, because a card that is `NEGATIVE` can be abandoned on sight
while a card that is `MARGINAL` can be traded for years on the strength of a
rounding error.**

The correct reading of this table is not "make the structure bigger". It is that a
`+0.02R` edge on a `b = 0.5` credit card is not worth expressing through a
structure whose fee is a large fraction of `R`, at any size.

---

## The derived rules

Derived from the two tables, not asserted:

1. **Below `R ≈ $100`, prefer 1–2 legs to 4.** At `$100`, moving from 4 legs to 2
   saves `0.0260R` of `c_R` — more than eleven points of the long-premium edge.
2. **Below `R ≈ $50`, prefer 1 leg.** At `$50`, a 4-leg structure burns 46% of the
   long-premium edge and drives a thin credit edge to `−0.0840R`, past its noise
   band.
3. **Below `R ≈ $25`, the options structure is not the instrument.** The fee
   consumes 92% or more of the edge, and the remaining expectancy is inside one
   standard error. The same directional view expressed in the underlying, or in a
   single-leg option, carries a fee measured in basis points instead of tickets.
4. **Multi-rung scaling has a size floor of `N × legs × fee_per_contract` per
   spread.** For a 4-leg structure at `$0.65` with three rungs that is `$7.80`
   (`[COMPUTED]`). Below it, every rung banks less than it pays.
5. **Cost is a reason to change instrument, not a reason to widen the structure.**
   Widening the structure to make `R` bigger (a wider spread) does reduce `c_R` —
   but it also changes the payoff ratio if the stop stays in the same place, because
   `b = tp/sl` and the credit/width relationship has moved. Re-run the checker after
   the change; do not assume the edge survived it.

---

## What an options structure is actually good for at small size

| Instrument | Round-trip cost | What it costs at small size | What it buys |
|---|---|---|---|
| Single-leg long option | 2 tickets, `$1.30` at `$0.65` | 0.0130R on `R = $100` | Full convexity, one decision, no legging risk |
| 2-leg vertical | 4 tickets, `$2.60` | 0.0260R on `$100` | Defined risk, cheaper debit, capped payoff |
| 4-leg condor | 8 tickets, `$5.20` | 0.0520R on `$100` | Defined risk on both sides, and a `b ≈ 0.25` card needing `p = 80%` |
| Underlying (stock / ETF) | `~0.05–0.30%` of notional | 0.0015R at `R ≈ $3,467` | Linear exposure, no time decay, no expiry |
| Underlying + covered call | commission on both legs | between the two | Capped upside against a held position |

The fourth row is why a small account's most cost-forgiving expression of a
directional view is usually the underlying itself. The fifth row shows the option
overlay earning its ticket only when there is a real position to overlay.

---

## Failure modes

1. **Failure mode — the "low capital" credit spread is chosen by a small account
   because the margin requirement is small.** The margin is small *because* the
   structure is small, and the fee is not. This is the most common and most
   expensive error in the small-account options literature.
2. **Failure mode — a 4-leg structure is chosen for "defined risk" without pricing
   the fourth leg.** Defined risk is real and valuable; it is not free, and at
   `$100` of `R` it costs 23% of the long-premium edge or flips a thin credit edge
   negative.
3. **Failure mode — size is cut in a drawdown without re-checking `c_R`.** Cutting
   the structure to half size doubles `c_R`. A cost that was tolerable at
   `$500` may be fatal at `$250`, and the iteration protocol's cost cycle exists
   precisely to catch this.
4. **Failure mode — cost is compared across structures as a dollar amount rather
   than as `c_R`.** `$5.20` is 0.0104R on one structure and 0.3467R on another. The
   dollar figure is not the comparison.
5. **Failure mode — the half-spread is excluded from the leg-count comparison.** It
   is usually the largest component and it scales with legs.
6. **Failure mode — an account is assumed to be too small for a structure when the
   problem is the rung count.** A single close on a small structure is often
   affordable where a three-rung scale-out is not.
7. **Failure mode — a thin edge is accepted because the structure is cheap.** The
   `$50`-structure credit card at `+0.0096R` is POSITIVE by verdict and unusable in
   practice; the sample needed to see it is far beyond a small account's trade rate.
8. **Failure mode — "I'll size up when I'm right" is used to defer the cost
   question.** Sizing up does fix `c_R`. It also fixes `R`, and `R` is what the
   drawdown arithmetic in `references/streak-survival-by-corner.md` is computed
   against. The two cannot be decided separately.

---

## Worked checks

```bash
# the same card at four structure sizes: POSITIVE, POSITIVE, MARGINAL, NEGATIVE
for R in 500 100 25 15; do
  py -3 scripts/payoff_check.py --tp 2.5 --sl 1.0 --p 0.35 \
      --fee-per-contract 0.65 --legs 4 --r-dollars $R
done

# a thin credit edge on small 4-leg structures: MARGINAL, then NEGATIVE
for R in 500 100 50; do
  py -3 scripts/payoff_check.py --tp 0.5 --sl 1.0 --p 0.68 \
      --fee-per-contract 0.65 --legs 4 --r-dollars $R
done
```

See also: `references/cost-drag-per-leg-and-per-rung.md`,
`references/streak-survival-by-corner.md`,
`references/strategy-cards.md`.
