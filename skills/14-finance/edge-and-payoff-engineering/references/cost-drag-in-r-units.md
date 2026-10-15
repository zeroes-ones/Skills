# Cost Drag in R Units

```
c_R = cost_per_trade / R_dollars
E_net = E - c_R
```

Cost is an input, never a default of zero. The engine accepts a `cost` column and
subtracts it, and when that column is missing or all-zero it prints the warning
below **in capitals, on every run, before any statistic**:

```
*** COST IS ZERO IN THIS RUN ***  No `cost` column was supplied (or every row
carried 0). Every expectancy figure below is therefore GROSS. Real commissions,
exchange and regulatory fees, and half the bid-ask spread are not free; on a
short-dated option a realistic round trip is a meaningful fraction of one R. A
gross number is a flattering number. Supply `cost` and re-run before acting on
anything here.
```

`[VERIFIED]` — that is the engine's literal output on the hand-check fixture,
which deliberately has no `cost` column so that the warning is demonstrated.

---

## 1. Why cost is expressed in R and not in currency

`c_R` is a **ratio of two currency amounts**, so it is dimensionless and can be
subtracted directly from `E`, which is in R units. This is not a stylistic choice.
A currency-vs-R subtraction is the classic unit error in this subject:

```
WRONG:   E (in R)  -  cost (in dollars)          -> meaningless, and it can flip
                                                    the sign of a near-zero edge
RIGHT:   E (in R)  -  c_R (in R)  where c_R = mean_cost / mean_R
```

`[VERIFIED]` — the illustrative ledger's `mean cost per trade` is `6.00` and its
`mean planned risk` is `200.75`, so `c_R = 0.029875`: about three percent of one R.
The engine prints both the currency figure and `c_R` so the conversion is visible
rather than buried.

**In currency mode** there is no planned R, so the engine proxies `R_dollars` with
the mean absolute loss and says so in the `UNITS MODE` block. It is a proxy, it is
labelled, and it is only used because the alternative — not computing cost drag at
all — is worse.

---

## 2. What belongs in `cost`

One number per closed trade, in the same currency as `pnl`:

| Component | In or out | Notes |
|---|---|---|
| Broker commission, both sides | **In** | Per contract, in and out, including any per-ticket minimum |
| Exchange and regulatory fees | **In** | Often small per contract, non-trivial in aggregate |
| Clearing fees | **In** | Per contract |
| **Half the bid-ask spread, both sides** | **In** | The part people forget, and usually the largest single component on a short-dated option |
| Financing / borrow / margin interest | **In** | Real cash cost of carrying the position |
| Assignment and exercise fees | **In** | Belongs to the trade that ended in the assignment |
| Market data subscriptions | **Out** | A fixed cost of operating, not a per-trade cost. Treat separately if it matters |
| Taxes | **Out** | Depends on the whole year's activity; not a per-trade cost in the sense used here |
| Slippage beyond the half-spread (market impact, partial fills, gap fills) | **Judgement** | If you can measure it, put it in and say so in the provenance line |

**The one rule that matters:** if `pnl` in the ledger is already **net** of cost,
then `cost` must be left empty — otherwise the cost is subtracted twice, and the
engine cannot detect that. The engine's `examples/README.md` recommends
`pnl` = gross realised P&L and `cost` = the round trip, because that makes the two
columns auditable separately.

---

## 3. How large is "large"?

`c_R` is not a fixed number and this skill does not quote a typical one, because
none was measured here. What can be said is structural:

* **`c_R` scales inversely with the size of one R.** A trader risking a large
  amount per trade has a small `c_R` in R terms for the same commission schedule.
  This is the real reason small accounts struggle: the same fee schedule is a
  larger fraction of a smaller R.
* **`c_R` scales inversely with the planned profit per trade.** A book with a
  wide target and a long holding period pays the same cost across a larger
  numerator, so `c_R` is a smaller fraction of `E`.
* **`c_R` does not scale with the number of contracts in a simple way.** Per
  contract fees scale linearly; the spread component scales with the number of
  contracts too, but the *relative* impact falls because the risk per trade also
  scales. What changes the ratio is trading more often, not trading bigger.

**The comparison that matters is `c_R` against `|E|`.** On the shipped illustrative
ledger `|E| = 0.000941R` and `c_R = 0.029875R` `[VERIFIED]`: the cost is **32
times** the signal. The engine flags that case explicitly:

```
*** COST IS THE BINDING CONSTRAINT: gross E = 0.0009 is
    smaller than c_R = 0.0299, so the book pays more to
    trade than it earns before costs. ***
```

---

## 4. Cutting cost: the levers, in order of ease

1. **Trade less frequently.** Cost is per trade, so frequency is a direct
   multiplier. A book that halves its trade count halves its total cost with no
   change to `p`, `b` or the sizing rule.
2. **Increase the size of one R relative to the fixed per-trade cost.** Fewer,
   larger positions on the same capital. Note the interaction with `R_max`: cost
   economies do not license risking more than the streak derivation allows.
3. **Use structures with a tighter spread.** A multi-leg structure with a wide
   bid-ask pair pays the spread twice per leg. Strike selection can move the
   spread more than contract selection can.
4. **Negotiate the commission schedule.** At sufficient volume, per-contract
   pricing moves. This is the only lever whose value depends on a third party.
5. **Reduce the number of legs.** Every leg is its own commission and its own
   half-spread. A four-leg structure costs twice a two-leg structure of the same
   risk, all else equal.

`[ILLUSTRATIVE]` — a round trip costing `$6.00` against a mean risk of `$200.75`
is `c_R = 0.0299`; the same `$6.00` against a mean risk of `$2,000` would be
`c_R = 0.0030`, ten times smaller. Neither number is a claim about any real
commission schedule; they are the same invented cost against two invented account
sizes, shown to make the scaling legible.

---

## 5. Where cost enters the verdict

Cost changes the verdict in three distinct ways, and it is worth knowing which one
applies:

| Situation | What cost does | How the engine reports it |
|---|---|---|
| `E > b*` and `E > c_R` | Reduces `E` but leaves the sign | Plain `E_net` row |
| `E > b*` and `E <= c_R` | **Flips the sign** | `*** COST IS THE BINDING CONSTRAINT ***` banner |
| `E < b*` | Worsens an already-negative book | The disposition banner fires first; cost is secondary |

The middle row is the dangerous one, because the gross book looks fine. It is also
the one that a zero-cost default hides completely — a run without `cost` would
report `POSITIVE EDGE` on a book that loses money. That is why the warning is
printed in capitals before any statistic, and why it is not suppressible.

---

## 6. Failure modes

1. **Failure mode — the zero-cost default.** A run without `cost` reports gross
   figures. The engine's warning exists because this mistake is both common and
   invisible in the output.
2. **Failure mode — double-counting cost.** `pnl` already net of cost **and** a
   populated `cost` column subtracts the cost twice, and nothing in the file
   reveals it. Declare the choice in a `# PROVENANCE:` line.
3. **Failure mode — forgetting the spread.** Commission schedules are published;
   half-spreads are not. On short-dated options the spread is frequently the
   larger component, so a `cost` column built from commission alone understates
   `c_R` substantially. `[COMMON-PRACTICE]`
4. **Failure mode — a currency-vs-R subtraction.** `E − cost` in mixed units can
   flip a verdict, and it looks like a plausible number when printed.
5. **Failure mode — cost measured per round trip but recorded per leg.** Two legs
   at `$3` is `$6`, not `$3`. Check the count, not the ticket.
6. **Failure mode — treating fixed operating costs as per-trade costs.** Data
   subscriptions and platform fees do not scale with trade count; putting them in
   `cost` makes trading less frequently look artificially better.
7. **Failure mode — ignoring cost because the account is "large".** `c_R` is a
   ratio. A large account with a large R has a small `c_R`, which is a reason to
   check it, not a reason to skip it.
8. **Failure mode — a cost change that is not re-measured.** A commission
   renegotiation, a move to a wider strike, or a change in trade frequency moves
   `c_R`, and every past verdict is then stated at the old cost.

---

## 7. The one-page procedure

```
1. Decide: is `pnl` gross or net? Write it in a `# PROVENANCE:` line.
2. If gross: put the whole round trip in `cost`, half-spread included.
   If net: leave `cost` empty.
3. Run the engine. Confirm the warning is ABSENT from the output.
4. Read `c_R`. Compare it to `|E|`.
   c_R > |E|        -> cost is the binding constraint. Read the banner.
   c_R > |E|/3      -> cost is material; the cost lever is worth ranking.
   c_R < |E|/10     -> cost is not the current constraint. Look at p and b.
5. Record c_R in the state log -- it moves, and a move is itself a finding.
```

Cost is the cheapest of the four levers to pull and the easiest to forget. It
requires no market view, no filter, no target change and no new trade. On a book
whose gross expectancy is small, it is often the only lever that can be pulled
today — and the arithmetic of `c_R` versus `|E|` is what says so.
