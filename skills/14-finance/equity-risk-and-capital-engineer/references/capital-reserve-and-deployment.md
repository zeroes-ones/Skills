# Capital Reserve and Deployment

The reserve and the ladder. This file answers the one question the rest of the skill does not:
**how much of the account's buying power is allowed to be at risk at once, and what happens when the
answer changes because the book has already lost money?**

It is the equity sibling of the options book's `capital-liquidity-preservation.md`. The two files
share one shape and one sentence: **the reserve exists so that a good position never has to be
liquidated at a bad price.** They are **sibling policy sets, not two copies of one policy**: each is
correct for its own instrument class — an options book uses the options file, an equity-only book
uses this one — and **if the two ever disagree, on a number or on the same account, this one defers.**

They are **not numerically identical**, and claiming otherwise would be a non-contradiction claim
that hides a real difference. Read them side by side:

| | This file (equity) | `capital-liquidity-preservation.md` (options) |
|---|---|---|
| `R_dd` coefficient | `0.15 × NAV` | `0.20 × NAV` — a gamma-heavy options book's stress cash demand is larger relative to NAV |
| `R_tail` middle term | `0.50 × WCSD` — a simultaneous **drawdown** | `0.50 × WCML` — a simultaneous **max loss** |
| Ladder, committed-margin ceilings | 60% / 45% / 30% / 15% | 50% / 35% / 25% / 15% — three of the five states differ |
| Ladder, max new-ticket caps | 8% / 5% / 3% / 0 | 10% / 5% / 3% / 2% / 0 — three differ |
| Which term binds in the file's own worked example | `R_tail`, because correlated drawdown dominates an equity book | `R_dd` |

**The sentence is shared; the numbers are not.** Everything else about the two files is
instrument-specific, and a number carried from one into the other is a number whose derivation does
not hold there.

It owns three things:

1. The **uncommitted buying-power reserve floor** — the cash that is never spent, checked before a
   ticket rather than after.
2. The **deployment ladder** — how the commitment ceiling shrinks as the book deteriorates.
3. The **exit-cost term** and the **forced-selling order** — what every position must be able to do,
   and what gets closed first when capital is genuinely needed.

It does **not** own position sizing (`portfolio-signal-manager`, `algorithmic-trader` do), margin
computation (`margin-regimes-and-forced-liquidation.md` does), or security selection
(`fundamental-analyst`, `technical-signals-engineer`, `macro-strategist` do).

## §1 — The Reserve Floor

The floor is a **pre-trade** test. A reserve computed after the ticket is a post-mortem, not a policy.

```
uncommitted_BP_after_fill = total_BP − (committed_margin + new_ticket_margin)
reserve_floor             = max( R_dd , R_tail , R_exit )
```

| Term | Definition | Derivation |
|---|---|---|
| `R_dd` — drawdown reserve | `0.15 × NAV` | [ESTIMATED ±35%] The reserve must fund the **incremental** margin a broker demands when a drawdown arrives. Visible arithmetic: `0.25` (index drawdown modelled in a bear market) × `0.50` (deepest deployment ceiling on the ladder in §2) × `1.2` (maintenance-expansion factor: FINRA Rule 4210(c) long maintenance is 25% flat and does not stress-expand the way options add-ons do; the expansion that exists comes from a broker's own house maintenance on concentrated or low-priced names, which is a commercial setting — roughly 1.2× to 1.5×) ≈ `0.15`. The floor is set at `0.15` as desk policy because part of the incremental demand is met by the equity cushion itself rather than by uncommitted buying power. Disagree with the arithmetic and choose your own coefficients — but write them down |
| `R_tail` — tail reserve | `0.50 × WCSD`, where `WCSD` is the book's **worst-case simultaneous drawdown** at correlation → 1.0 across the equity book | [ESTIMATED ±30%] In a correlation→1.0 drawdown, only the part of the modelled simultaneous loss that is **cash-demanded during** the episode — maintenance calls, buy-ins on shorts, funding forced closes — must sit in uncommitted buying power. The rest is mark-to-market on positions still inside the broker's requirement and therefore still holdable. That cash-demanded fraction is not observable in advance. **If the book has no margin-expansion history of its own, use `1.0 × WCSD`** and relax to 0.50 only after 12 months of evidence. Start strict |
| `R_exit` — exit-cost reserve | `1.5 × exit_cost(book)`, where `exit_cost(book) = Σ (position_value_i × exit_cost_pct_i)` | The formula is [COMPUTED]. `exit_cost_pct` is the round-trip cost recorded at entry (`liquidity-and-exit-cost-planning.md` §3), **plus, for a short, the borrow fee accrued to the planned exit and the buy-in risk premium**. The `1.5×` multiplier is [ESTIMATED ±25%]: spreads widen precisely when capital is short, by roughly 1.3–2.0× in a stressed tape, and the reserve must fund a *managed* unwind, not a distressed one |

**Why an equity book still needs a reserve when its positions "can always be sold".** Because
"can always be sold" is a statement about price, not about price *you chose*. The position that can
always be sold is sold first by the margin clerk, in the worst tape, because it is the easiest to
sell. The reserve is the price of never being the forced seller.

### §1.1 — The floor tested end to end: a worked example [COMPUTED]

Every figure below is arithmetic on the §1 formulas. Nothing is rounded except to the whole dollar.

```
INPUTS
  NAV                                = $500,000
  total_BP (live, broker)            = $400,000
  committed_margin (open positions)  = $210,000
  WCSD (correlation → 1.0, a simultaneous drawdown of the book, not a sum of position values)
                                     = $240,000
  exit_cost(book) = Σ(position_value × exit_cost_pct) = $64,000

STEP 1 — uncommitted buying power BEFORE the ticket
  uncommitted_BP = total_BP − committed_margin = 400,000 − 210,000 = $190,000

STEP 2 — the three floor terms, and the max
  R_dd   = 0.15 × NAV   = 0.15 × 500,000 = $ 75,000
  R_tail = 0.50 × WCSD  = 0.50 × 240,000 = $120,000   ← BINDING TERM
  R_exit = 1.5  × exit  = 1.50 ×  64,000 = $ 96,000
  reserve_floor = max(75,000, 120,000, 96,000) = $120,000

STEP 3 — headroom available to new tickets
  headroom = uncommitted_BP − reserve_floor = 190,000 − 120,000 = $70,000

STEP 4 — the test, run BEFORE each ticket
  Ticket A: new_ticket_margin = $90,000
      uncommitted_BP_after_fill = 400,000 − (210,000 + 90,000) = $100,000
      100,000 < 120,000  →  BLOCKED. Short by $20,000, and R_tail is the term that binds.
  Ticket B: new_ticket_margin = $65,000
      uncommitted_BP_after_fill = 400,000 − (210,000 + 65,000) = $125,000
      125,000 ≥ 120,000  →  ALLOWED. It consumes $65,000 of the $70,000 headroom;
                            $5,000 remains.
```

**What the example is built to catch.**

- **Ticket A is the trap.** $90,000 *looks* affordable because it is far smaller than the $190,000
  of uncommitted buying power. The test is not against uncommitted BP — it is against uncommitted BP
  **minus the floor**.
- **The binding term is the tail reserve, not the drawdown reserve.** In an equity book the reserve
  is dominated by **correlated** drawdown, which is exactly the term a NAV-percentage rule cannot
  see. The nominal `0.15 × NAV` term is the smallest of the three.
- **The exit-cost term is close behind at $96,000.** For an equity book with a concentrated position
  that is *normal*, not extreme: a $150,000 position at a 3.21% round trip is $4,815 by itself
  (`liquidity-and-exit-cost-planning.md` §3.1). A book whose `R_exit` is small is a book that has
  never priced its own exits.
- **If the floor is tested after the fill, Ticket A is already in the book** and there is no decision
  left to make. That is failure mode §5.1.

## §2 — The Deployment Ladder

```
deployable_capital = total_BP − reserve_floor
deployment_ratio   = committed_margin / total_BP
```

The ladder **only tightens**. The effective ceiling on committed margin is always

```
min( margin-regime colour band , state ceiling )
```

so a state ceiling can never be used as *relief* from the ordinary Green / Yellow / Orange / Red
margin bands — it can only add restriction. The colour bands measure **current** margin pressure;
the state ceilings measure **accumulated damage**. A book can be quiet and damaged at the same time.

| Book state | Effective ceiling on committed margin | Max new-ticket notional — a **capital ceiling**, not a size rule | Why the ceiling moves |
|---|---|---|---|
| **Normal** — Green (margin use < 30%), no position taken to max loss this cycle, NAV within 5% of high-water | ordinary bands apply **unchanged** | ≤ reserve headroom; also ≤ **10% NAV single-name**, `portfolio-signal-manager`'s sizing rule, applied unchanged (see `concentration-and-correlation-risk.md` §1) | Nothing has been falsified yet |
| **After ONE position taken to a full planned loss**, or Yellow (30–50%) | **≤ 60%** | ≤ 8% of NAV notional; same-name only — **never** a size increase on the position that lost | One falsification is information: the sizing model or the regime read was wrong somewhere. Rebuild at the same size, not a larger one |
| **After TWO positions taken to a full planned loss**, or Orange (50–70%) | **≤ 45%** | ≤ 5% of NAV notional; **no new short positions** — a new short adds a borrow obligation that no rule protects (`short-borrow-and-buy-in-mechanics.md` §1) | Two falsifications means the *book* is mis-sized, not one trade. Cut the ceiling, not just the ticket |
| **NAV drawdown ≥ 15%** from high-water | **≤ 30%** | ≤ 3% of NAV notional; no new concentrated (> 10% NAV single-name) positions; no new short exposure | A 15% drawdown is a regime signal. The book's correlation and exit-cost assumptions were built in the old regime |
| **NAV drawdown ≥ 25%**, or Red (margin use > 70%), or margin utilisation > 70% | **≤ 15%** | **0 — no new tickets.** De-risk only; the reserve is now the only remaining buffer | This is the state the reserve floor exists to prevent reaching with forced sales |

**Read the third column as a capital ceiling, not a size rule.** The 8% / 5% / 3% rungs cap how much
of NAV the *book in a damaged state* may commit to a single new ticket. They are not position-sizing
rules and they do not replace `portfolio-signal-manager`'s **10% single-name / 25% sector** caps: a
ticket must satisfy **both**, and the tighter one binds. The **10% single-name** figure in the Normal
row is that sizing rule restated, not a tenth rule of this file's own. Every rung of the ladder is
`[ESTIMATED ±35%]` desk policy derived from the same reasoning as `R_dd` in §1, not a regulatory
limit.

At the ≤ 15% rung, ≥ 85% of buying power is uncommitted, which is the equity complement of the
options book's "keep margin use below 40% for crash resilience" discipline. The ladder's job is to
make that ceiling shrink automatically as damage accumulates, instead of relying on the holder
remembering it.

## §3 — The Exit-Cost Term for an Equity Book

```
exit_cost(book) = Σ_i [ position_value_i × exit_cost_pct_i ]
```

| Component of `exit_cost_pct` | For a long | For a short |
|---|---|---|
| Spread (round trip) | `(ask − bid) / mid` | `(ask − bid) / mid` |
| Impact (round trip) | `2 × k × σ_daily × sqrt(Q/ADV)` | same |
| Borrow accrued to the planned exit | — | `borrow_fee_annual × (holding_days / 365)` |
| Buy-in risk premium | — | [ESTIMATED ±50%]: a wide, deliberately unquantified allowance for the possibility that the position is closed by a buy-in rather than by the holder (see `short-borrow-and-buy-in-mechanics.md` §2). A short with no such allowance has an understated exit cost |

The last row is the one people leave out. A short's exit cost is not the spread plus impact on the
day of the exit; it is the spread plus impact plus whatever it cost to be *forced* to exit. The
premium is an estimate precisely because the buy-in price is not predictable — which is an argument
for carrying it, not against.

## §4 — Forced-Selling Order

When capital is genuinely needed, the **wrong** order is "worst liquidity first". Selling the
least-liquid positions first maximises impact, realises the worst price on the assets with the least
market to absorb them, and leaves the book holding nothing but the assets nobody wanted. **Worst
liquidity first is the wrong order — say it in those words, because it is the order people reach for
under pressure.**

The correct order closes **risk first, economics second, housekeeping third, and the balance sheet
never**:

```
Capital is needed. What closes?
├── 1. Route-less and recall-flagged positions → CLOSE NOW
│      no exit_route, no stop, a hard-to-borrow short with no locate, anything
│      whose only route is (f) broker liquidation
│      → removes the exposures that can be closed at someone else's price
├── 2. The position or correlated cluster that CAUSED the drawdown → CLOSE
│      close the risk, not the winners. Funding a loser with a winner converts a
│      temporary mark-to-market loss into a permanent one and leaves the tail in place
├── 3. Largest dollar exit cost among positions that CAN be exited inside their own cap
│      position_value × exit_cost_pct — worst economics, not worst liquidity
│      (worst liquidity is the LAST criterion here, not the first)
├── 4. Most concentrated name and the highest position-as-%-of-ADV → CLOSE
│      reduces concentration and the exit-cost asymmetry at the same time
├── 5. Highest borrow fee / shortest fail age on the short side → CLOSE
│      these are the positions whose clocks are not under the holder's control at all
├── 6. Housekeeping: odd lots, spin-off stubs, residual positions, dead tickers
│      no market impact; recovers margin and attention
├── 7. NEVER FIRST: deepest-liquidity, tightest-spread, closest-to-target winners
│      these are the balance sheet; they fund the loss at the best price the book
│      can get, and selling them first leaves only the unwanted assets
└── 8. NEVER: one leg of a correlated cluster while keeping the rest
       converts a diversified cluster into a concentrated one, raising the exit
       clock at the exact moment capital is shortest
```

**The reserve floor is what makes step 7 unreachable.** With `uncommitted_BP ≥ reserve_floor`
enforced *before* each ticket, steps 1 through 5 are funded from uncommitted buying power and step 7
is never needed. **That is the whole point.**

## §5 — Failure Modes of the Policy Itself

1. **Floor checked after the ticket.** The most common failure. The fill is done, the reserve is
   breached, and the next decision is already constrained. Mitigation: the §1 test is a gate, and a
   blocked ticket is logged with its binding term.
2. **Reserve parked in positions.** "Cash drag" pressure converts the reserve into a position
   labelled as cash-like. Mitigation: the reserve is measured as **uncommitted buying power**, not as
   an intention and not as the value of a money-market holding that has its own T+1.
3. **`WCSD` computed as a sum of position values rather than a simultaneous drawdown.** A sum of
   values is not a drawdown; it is the size of the book. Mitigation: `WCSD` reuses the
   correlation → 1.0 stress output from `concentration-and-correlation-risk.md` §3.
4. **Ladder used as relief.** A book at a 15% drawdown argues its way back to the Normal ceiling.
   Mitigation: the ladder only tightens, and the effective ceiling is the `min` of the colour band
   and the state ceiling.
5. **Exit cost recorded at entry and never re-measured.** ADV and spreads change; a liquid position
   becomes illiquid. Mitigation: the weekly re-measurement cadence in
   `liquidity-and-exit-cost-planning.md` §5 also refreshes `exit_cost_pct` and `R_exit`.
6. **A "temporary" reserve drawdown that never gets repaid.** The reserve is spent defending a lost
   position — the same reasoning that created the drawdown. Mitigation: a reserve breach blocks
   **all** new tickets until restored, with no discretionary exception.
7. **Liquidity-first liquidations.** Selling the illiquid names first feels prudent and is exactly
   backwards. Mitigation: §4 is an ordered list and step 3 states that worst-liquidity is last.
8. **Correlated cluster half-closed.** Closing one leg of five leaves a concentrated version of the
   same tail with less diversification. Mitigation: §4 step 8 — clusters close whole or not at all.
9. **Reserve denominated in buying power that itself shrinks.** Buying power falls as positions move
   against the holder, so an absolute reserve can shrink in real terms. Mitigation: the floor is
   recomputed from live `total_BP` every time it is tested, never cached.
10. **Short-side obligations omitted from the reserve.** Borrow fees, buy-in risk and the delivery
    obligation on a short are cash demands that a long-only reserve formula ignores. Mitigation: §3's
    short rows are part of `exit_cost_pct` before `R_exit` is computed.
11. **The reserve funded by the position that needs it.** Using the concentrated position as informal
    collateral for the reserve means a drawdown in that position removes both the position and the
    reserve. Mitigation: the reserve is uncommitted buying power, by definition not a position.

## §6 — Verification

- [ ] `reserve_floor` computed from live `total_BP` and NAV, with all three terms shown and the
      binding term named.
- [ ] Every new ticket has an `uncommitted_BP_after_fill` figure recorded **before** the fill.
- [ ] `deployable_capital` and `deployment_ratio` reported alongside the margin-regime band.
- [ ] The effective ceiling was taken as `min(colour band, state ceiling)`.
- [ ] `WCSD` traces to the correlation → 1.0 stress output, not to a sum of position values.
- [ ] Every open position has a non-null `exit_route` that is not (f).
- [ ] Every open position has `exit_cost_pct ≤ exit_cost_cap`, with the short rows of §3 included.
- [ ] A reserve breach, if one exists, is currently blocking all new tickets.
- [ ] The forced-selling order in §4 is recorded as the standing liquidation priority, so it is not
      improvised under pressure.
