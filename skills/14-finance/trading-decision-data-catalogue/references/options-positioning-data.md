# Options Positioning Data — What Is Observed and What Is Inferred

Options data has one property that every other dataset class does not: **two of its most-quoted
figures are not measured at all.** Open interest is measured but is a day old. Dealer gamma is not
measured by anyone. The rest of this file is the discipline of keeping those two facts straight.

## §1 — The Observed / Inferred Split

| Figure | Status | Produced by | The failure it causes |
|---|---|---|---|
| Open interest per strike | **Observed, end of day** | the exchange / OCC clearing chain | read as intraday and treated as live positioning |
| Volume per strike | **Observed** | the exchange | read as directional when it is one leg of a structure |
| Volume by participant capacity | **Observed, sold as a dataset** | Cboe DataShop | bought and then compared against a retail tool that classifies differently |
| Implied volatility per contract | **Observed, model-dependent** | each feed's own model | two feeds disagree and one is silently chosen |
| Put/call ratio | **Observed, disaggregated** | Cboe daily market statistics | aggregated across index, ETF, equity and VIX and then read as one number |
| Dealer gamma by strike ("GEX") | **Inferred, never observed** | a vendor, using its own sign convention | presented as a measurement of dealer positioning |
| "Smart money" flow labels | **Inferred** | a vendor's heuristics | treated as a classification when it is a rule of thumb |

**The one-line version:** open interest is a fact about yesterday; GEX is a hypothesis about today.

## §2 — Open Interest Is an End-of-Day Figure

**Source:** exchange market-data product documentation. The claim: **open interest is an end-of-day
figure, so an intraday "OI" column is yesterday's.**

### 2.1 — The tell, and why it is decisive

The decisive evidence is in the product catalogues rather than in any statement of policy. Venues
sell a **separate end-of-day snapshot** and a **3:45pm ET snapshot in which open interest is an
*optional* field** `[VERIFIED — exchange market-data product documentation]`. The logic is short: if
open interest were an intraday quantity, there would be no market for a separate end-of-day product
and no reason for a 3:45pm product to price it as an option.

**This is how to settle the question for any venue whose behaviour you are unsure about:** look at
what the venue sells. A product catalogue is the cheapest documentation of a data limitation that
exists, and it cannot be accused of marketing.

### 2.2 — The practical consequences

1. **A "OI rising into the close" narrative is a statement about yesterday.** It may still be true
   today, but it has not been observed today.
2. **A backtest that fills at a strike's OI on the trade date is using next-day information** if it
   reads the value before publication, and yesterday's information if it reads it as today's. Neither
   is what the trader believes they are doing.
3. **OI-based screens are slow screens.** That is not a defect; it is a property. Treat an OI screen
   as a weekly filter, not an intraday trigger.

### 2.3 — How to record it

- `oi_as_of_date` — the exchange's own as-of date, not the read date.
- `oi_read_timestamp` — when you loaded it.
- `oi_source` — the venue and the product, so a second person can check the as-of.

A record with a read timestamp and no as-of date has not established freshness.

## §3 — Volume, Flow, and the Participant Question

Volume is observed. Direction is not. A single large print is one of at least six things, and the
public tape does not say which:

1. an opening buy,
2. an opening sell,
3. one leg of a spread whose other leg is in a different strike or expiry,
4. a hedge against a stock or futures position,
5. a roll from one expiry to another,
6. a close.

**Cboe DataShop sells open-close volume by participant capacity** — Customer, Pro-Customer, Broker,
Firm, Market Maker `[VERIFIED — Cboe DataShop]`. This is the dataset that answers *who* traded, and
most retail flow tools cannot answer it at all. Where it is not available, the honest label for a
single-leg flag is **unclassified flow**, not a signal.

**Cboe also publishes free daily market statistics** with put/call disaggregated by index, ETF,
equity and VIX, and three free index CSVs — `VIX_History.csv`, `VVIX_History.csv`,
`SKEW_History.csv`, with VIX from 1990 and VVIX from 2006 `[VERIFIED — Cboe]`. Those are STATE
series, free, and more useful to a positioning question than most paid flow.

### 3.1 — The 0DTE statistic to refuse

The widely quoted **"0DTE = 59% of SPX volume"** figure sits on a marketing page with **no as-of
date** `[ESTIMATED — undated vendor marketing page]`. It is not that the number is certainly wrong;
it is that a market-share statistic without a date cannot be right or wrong, and therefore cannot be
used. **Do not put it in a chart, and say why when asked** — an undated number that reaches a deck
becomes a fact.

## §4 — Dealer Gamma (GEX): Inferred, Never Observed

**Source:** vendor product documentation. `[COMMON-PRACTICE]`.

The chain is: open interest per strike → assign a dealer position sign → aggregate gamma per strike
→ present as "dealer gamma exposure". Every link after the first is an assumption.

| Link | Measured? | What can go wrong |
|---|---|---|
| Open interest per strike | Yes, end of day | a day old |
| Dealer position sign per strike | **No** | the sign convention is the vendor's; flipping it flips the conclusion |
| Dealer position **size** | **No** | OI is the total market's, not the dealers' |
| Gamma per strike | No | depends on the vendor's IV input |

1. **No exchange publishes dealer gamma by strike.** If a figure claims to be observed, it is
   mislabelled.
2. **The dealer-long-versus-short convention flips the conclusion.** The same OI table produces an
   opposite trade under the opposite convention, which is the definition of a model risk rather
   than a data risk.
3. **Two vendors disagreeing is the informative signal.** The disagreement tells you the quantity is
   unmeasured, which is more valuable than either number.
4. **If you use it, write the assumption next to the number** and state what would falsify it.

## §5 — Implied Volatility and the Disagreement Test

IV is observed per contract but is model-dependent, and vendor disagreement is routine.

1. **Diff two feeds on the same timestamp.** Not "on the same day" — on the same timestamp. This is
   the only test that isolates the model from the market.
2. **In illiquid strikes, check the quote age before the quote.** A mid built from a bid that has not
   updated in four hours is not a price. On an early-close day — **1:00pm ET** for equities
   `[VERIFIED — NYSE and Nasdaq published calendars]`, and options early **by venue** (1:15pm ET for
   eligible options on some venues, **13:00** at Cboe; check your venue's calendar) — the last update
   may predate the close.
3. **Compare IV against a realized measure and a term structure, not against a number from memory.**
   "IV is high" is a claim about a distribution that has not been estimated.
4. **Record which model produced the number.** Two analysts disagreeing about a Greek with different
   IV inputs disagree about the model, not the market.

## §6 — Ranked: Options Datasets for a Positioning Question

| Rank | Dataset | Kind | Cost | Verdict |
|---|---|---|---|---|
| 1 | **Cboe daily market statistics (free)** | STATE | free | the fastest honest read on aggregate positioning, disaggregated by product type `[VERIFIED — Cboe]` |
| 2 | **Cboe index CSVs (VIX, VVIX, SKEW)** | STATE | free | free, dated, and long history from 1990 / 2006 `[VERIFIED — Cboe]` |
| 3 | **End-of-day open interest per strike** | STATE | free or low | essential as a weekly filter; useless as an intraday trigger |
| 4 | **Cboe DataShop open-close by participant capacity** | SIGNAL | paid | the one paid dataset here that answers a question nothing free answers `[VERIFIED — Cboe DataShop]` |
| 5 | **Per-contract IV and the Greeks built from it** | STATE | free or low | useful, model-dependent, needs the disagreement test |
| 6 | **Dealer gamma / GEX** | SIGNAL (inferred) | paid | label the assumption or drop it |
| 7 | **Retail "unusual options activity" flags** | SIGNAL | free to $120/mo | mostly nice-to-know; see [overrated-datasets.md](overrated-datasets.md) |

## §7 — Checks Before Any Options Figure Enters a Sentence

1. **Is it observed or inferred?** Write the label.
2. **If observed, what is its as-of?** Write the date, not the read time.
3. **If inferred, what is the assumption?** Write it and state what would falsify it.
4. **Was the session a normal session?** Check the exchange calendar.
5. **Is the quote age acceptable?** Check before the price.
6. **Did two feeds disagree?** If you did not check, you do not know.
7. **What decision does this change?** If nothing, mark it nice-to-know.

**Source:** exchange market-data product documentation for the end-of-day and 3:45pm snapshot
structure and the optional open-interest field; Cboe for the free daily market statistics, the three
index history CSVs and the DataShop participant-capacity dataset; NYSE and Nasdaq calendars for the
session times and the early closes; vendor product documentation, tagged `[COMMON-PRACTICE]`, for the
GEX construction chain; and the undated vendor marketing page, tagged `[ESTIMATED]`, for the 0DTE
share-of-volume claim. No OCC or OPRA page was retrieved for this skill; where an OCC or OPRA figure
is needed, retrieve it from the publisher directly.
