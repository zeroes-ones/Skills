# Gap and Event Risk

An option can be repriced continuously because it is a contract. A stock cannot be acted on
continuously, because the market closes. **Everything that happens while it is closed arrives as a
gap**, and a gap is the one risk an equity holder cannot manage after the fact — only size for
beforehand.

## §1 — The Gap Is the Whole Problem With Exits

The market is open roughly 6.5 hours out of 24 on weekdays and closed on weekends. Every one of the
remaining hours is a period in which the holder's exit plan cannot be executed and in which news
arrives freely.

```
A GAP IS NOT A FAST MOVE. A move can be traded into. A gap cannot.
```

Three consequences:

1. **Stops do not protect against gaps.** A stop order becomes a market order when it triggers; if
   the trigger price is skipped, the fill is at whatever the next available price is.
2. **The exit clock and the gap are additive.** A position that needs five sessions to leave at a
   stated participation rate has five sessions of gap exposure, and five sessions is five chances to
   gap.
3. **Events are scheduled gap generators.** Earnings, guidance, macro releases, index decisions,
   corporate actions: all of them arrive outside the holder's control and most of them arrive outside
   market hours.

## §2 — Stop-Loss Arithmetic, and Why It Is Not Protection [COMPUTED]

Position: 2,500 shares at $40.00 = $100,000. A stop-loss is placed at $36.00 — a planned 10% loss.

```
PLANNED
  trigger $36.00 × 2,500            = $90,000      loss $10,000  (10.0%)

ACTUAL, after an overnight gap from $40.00 to $31.00
  the stop triggers at the open, fills at $30.80
  $30.80 × 2,500                    = $77,000      loss $23,000  (23.0%)

SLIPPAGE VERSUS PLAN                $13,000, or 13 percentage points, in one night
```

[COMPUTED] from the stated inputs. The gap is the reason "I have a stop" is not an answer to "what is
my maximum loss on this position". The only honest answers are **size** and **the reserve floor**.

**The rule that follows:** a stop-loss bounds the loss only where trading is continuous. Where it is
not — overnight, weekends, halted, illiquid — the bound is the position size. Size for the gap, not
for the stop.

## §3 — Gap Exposure by Position Type

| Position | Overnight gap exposure | What bounds the loss |
|---|---|---|
| Large-cap, deep liquidity | Gaps are smaller and the next session's book is deep | Position size; the gap is recoverable in a session or two |
| Small/mid-cap, thin | Gaps are larger, and the book on the other side of the gap is thinner | Position size **and** the exit plan (`liquidity-and-exit-cost-planning.md`) |
| Concentrated single name | Everything above, with the whole book's outcome attached | The concentration cap and the reserve floor |
| Short | A gap **up** is a loss with no ceiling, plus a margin effect | The maintenance arithmetic in `margin-regimes-and-forced-liquidation.md` §3 plus the borrow status |
| Position in a name with a pending corporate action | The event's own date is the gap date | The event playbook and the offer's cutoff time |

## §4 — Scheduled Events Are Known Gap Dates

| Event | When | What it forces |
|---|---|---|
| Earnings | Known date, sometimes confirmed within days of the report | The largest single-name gap generator. A position sized without reference to its earnings date is sized on a coin flip with a known date |
| Guidance revision / pre-announcement | Unscheduled, and therefore **not** a known gap | Nothing can be planned; only size |
| Macro releases (rate decisions, inflation prints, employment) | Scheduled and published in advance | Moves the whole book at once — this is the *correlated* gap, and it is what `WCSD` in `capital-reserve-and-deployment.md` §1 is modelling |
| Index reconstitution / effective dates | Scheduled | See `index-and-event-calendar.md` |
| Lock-up expiry | Dated in the underwriting agreement | A scheduled supply increase |
| Corporate actions, tender deadlines | Dated in the filings | See `corporate-action-and-halt-playbook.md` |
| Halts | Unscheduled | Trading stops; no remedy exists |

**A known gap date is a decision point, not a surprise.** The only unacceptable position is one whose
earnings date was knowable and unread.

## §5 — The Compound Event: A Gap During a Margin Call

This is how positions die, and it is arithmetic, not narrative.

```
SETUP
  Long position, market value $100,000, debit $50,000
  equity $50,000          requirement 0.25 × $100,000 = $25,000     cushion $25,000

AFTER AN OVERNIGHT GAP OF −24%
  market value $76,000    equity 76,000 − 50,000 = $26,000
  requirement 0.25 × 76,000 = $19,000                              cushion $7,000
  → no call yet, but the cushion has lost 72% of its value in one session

AFTER −33.33% (the call price computed in margin-regimes-and-forced-liquidation.md §3)
  market value $66,667    equity $16,667   requirement $16,667     cushion $0
  → MAINTENANCE CALL
```

[COMPUTED] from the maintenance arithmetic and the stated inputs. Now add the second compound: the
gap happened in a thin name, so the exit cost that was 3.21% is now 6% or worse, and the exit clock
that was four sessions is now eight. **The margin call and the exit clock are now racing, in the same
name, in the same week** — which is precisely the state the reserve floor exists to prevent.

## §6 — Behaviour Across the Four Regimes

| Regime | Gaps behave like | What changes for the exit | What the risk engineer does |
|---|---|---|---|
| **Bull market / uptrend** | Gaps up. Volatility low, gaps small, and the position's cushion grows | Exit costs fall; ADV rises; the plan looks easy | Re-measure, do not re-size. A plan that improved because the weather improved is not a better plan |
| **Correction / pullback** (−5% to −20%) | Gaps become two-sided and larger | Spreads widen; the days-to-liquidate estimate lengthens | Re-measure `exit_cost_pct` and the cushion; raise the cadence; do not add |
| **Bear market / downturn** (−20% or more) | Gaps down are routine; correlations converge | The book's clusters behave as one position; the exit is now a multi-session programme | Follow the forced-selling order in `capital-reserve-and-deployment.md` §4; risk first |
| **Crash / tail event** (a market collapse, a March-2020-style event) | Gaps of a size that no model predicted, in names that were liquid yesterday | Bids become optional; halts interrupt trading; the "exit plan" is a wish | Nothing can be done *in* the regime. Everything that matters was done before it: size, reserve, and no leverage on the concentrated name |

**Read the fourth row twice.** In a crash the risk engineer has no decisions to make, only consequences
to absorb. That is why this file exists ahead of the crash rather than during it.

## §7 — Failure Modes

1. **Treating a stop order as a maximum-loss guarantee.** It is not; it is a market order with a
   trigger.
2. **Sizing on the average day and holding through a scheduled event.** Earnings has a date; the date
   is free to look up.
3. **Ignoring the correlated gap.** A macro release moves every position at once, which is what makes
   `WCSD` the binding reserve term.
4. **Assuming liquidity survives a gap.** It does not: spreads widen and depth thins at exactly the
   moment size is needed.
5. **Holding a levered position through a scheduled event.** The call price in
   `margin-regimes-and-forced-liquidation.md` §3 does not wait for the report to be digested.
6. **Assuming a halt is a pause the holder can trade out of afterwards at the pre-halt price.** There
   is no such rule.
7. **Ignoring that a gap changes the exit cost as well as the price.** Two problems, one session.
8. **Using a single-scenario "what if it drops 10%" test.** The regimes in §6 are the scenarios; test
   all four.
9. **Believing an event risk model that has never been read in the crash regime.** Re-read the plan in
   the current regime, by name.
10. **Planning a stop at a round number.** Round numbers are where stops cluster and where liquidity
    is thinnest after a gap.

## §8 — Verification

- [ ] Every position's maximum loss is stated as size-based, not stop-based.
- [ ] Every scheduled event date touching a position is recorded, with its source.
- [ ] The book has been stress-tested at a **correlated** gap, not only at per-name gaps.
- [ ] The four regimes of §6 have each been applied to the current book, and the current regime named.
- [ ] No stop order is presented to the user as bounding the loss on a gapping position.
- [ ] The compound case of §5 has been computed for the largest levered position, in dollars.
