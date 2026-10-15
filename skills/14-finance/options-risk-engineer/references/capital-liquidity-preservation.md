# Capital & Liquidity Preservation

The reserve floor and the deployment ladder. This file answers one question the rest of the skill
does not: **how much of the account's buying power is allowed to be at risk at once, and what
happens when the answer changes because the book already lost money?**

It owns three things:

1. The **uncommitted buying-power reserve floor** — the cash that is never spent, checked before a
   ticket rather than after.
2. The **deployable-capital ladder** — how the commitment ceiling shrinks as the book deteriorates.
3. The **exit-liquidity record** and the **forced-selling order** — what every position must be able
   to do, and what gets closed first when capital is genuinely needed.

It does **not** own position sizing (Phase 4 and `portfolio-signal-manager` do), margin
computation (Phase 3 and `margin-requirements.md` do), or strategy selection
(`options-strategist` does). Where those already exist, this file references them rather than
restating them.

## §1 — The Reserve Floor

The floor is a **pre-trade** test. A reserve computed after the ticket is a post-mortem, not a
policy. Compute

```
uncommitted_BP_after_fill = total_BP − (committed_BPR + new_ticket_BPR)
```

and require it to satisfy **all three** terms below. If any term fails, the ticket is blocked until
an existing position is closed (see §4 for the order).

```
reserve_floor = max( R_dd , R_tail , R_exit )
```

| Term | Definition | Derivation |
|---|---|---|
| `R_dd` — drawdown reserve | `0.20 × NAV` | [ESTIMATED ±40%] The reserve must fund the **incremental** margin a broker demands when a drawdown arrives. Brokers expand options requirements in stress through concentration add-ons, liquidity add-ons, and a volatility premium — the existing margin reference records IBKR raising maintenance requirements to 50%+ in March 2020 [VERIFIED — broker margin history]. Working in NAV terms: `0.25` (index drawdown modelled) × `0.60` (deepest deployment ceiling in §2) × `1.6` (midpoint of the 1.5–2.0× expansion range) ≈ `0.24`. The floor is set at `0.20` as desk policy because part of the incremental demand is met by the equity cushion itself rather than by uncommitted buying power. Visible arithmetic; disagree with it and set your own — but write it down |
| `R_tail` — tail reserve | `0.50 × WCML`, where `WCML` = the book's **worst-case simultaneous max loss** at correlation → 1.0 (the scenario R5 already mandates) | [ESTIMATED ±30%] In a correlation→1.0 drawdown, only the portion of modelled simultaneous max loss that is **cash-demanded during** the episode — margin calls, assignment funding, forced closes — must sit in uncommitted buying power. The remainder is mark-to-market on positions still inside the broker's requirement and therefore still holdable. That cash-demanded fraction is not observable in advance. **If the desk has no margin-expansion history of its own, use `1.0 × WCML`** and relax to 0.50 only with at least 12 months of evidence. Start strict |
| `R_exit` — exit-cost reserve | `1.5 × exit_cost(book)`, where `exit_cost(book) = Σ (position_value_i × exit_cost_pct_i)` | The formula is [COMPUTED]. `exit_cost_pct` is the round-trip cost recorded at entry (§3). The `1.5×` multiplier is [ESTIMATED ±25%]: spreads widen precisely when capital is short, by roughly 1.3–2.0× in a stressed tape, and the reserve must be able to fund a *managed* unwind, not a distressed one |

**Why a reserve at all.** Every term above exists so that a **good** position never has to be
liquidated at a **bad** price. A book with no reserve is a book whose best assets are the ones the
margin clerk sells first, at the worst moment, because they are the easiest to sell. The reserve is
the price of never being forced to do that.

### §1.1 — The floor tested end to end: a worked example [COMPUTED]

Every figure below is arithmetic on the §1 formulas. No step is rounded for display except to the
whole dollar.

```
INPUTS
  NAV                          = $500,000
  total_BP  (live, broker)     = $400,000
  committed_BPR (open positions) = $180,000
  WCML  (Phase 6, correlation → 1.0, not a sum of premiums) = $160,000
  exit_cost(book) = Σ(position_value × exit_cost_pct)      = $  8,000

STEP 1 — uncommitted buying power BEFORE the ticket
  uncommitted_BP = total_BP − committed_BPR = 400,000 − 180,000 = $220,000

STEP 2 — the three floor terms, and the max
  R_dd   = 0.20 × NAV    = 0.20 × 500,000 = $100,000   ← BINDING TERM
  R_tail = 0.50 × WCML   = 0.50 × 160,000 = $ 80,000
  R_exit = 1.5  × exit   = 1.50 ×   8,000 = $ 12,000
  reserve_floor = max(100,000, 80,000, 12,000) = $100,000

STEP 3 — headroom available to new tickets
  headroom = uncommitted_BP − reserve_floor = 220,000 − 100,000 = $120,000

STEP 4 — the test, run BEFORE each ticket
  Ticket A: new_ticket_BPR = $140,000
      uncommitted_BP_after_fill = 400,000 − (180,000 + 140,000) = $80,000
      $80,000 < $100,000  →  BLOCKED. Short by $20,000, and R_dd is the term that binds.
  Ticket B: new_ticket_BPR = $90,000
      uncommitted_BP_after_fill = 400,000 − (180,000 + 90,000) = $130,000
      $130,000 ≥ $100,000  →  ALLOWED. It consumes $90,000 of the $120,000 headroom; $30,000 remains.
```

**What the example is built to catch.** Ticket A is the trap: $140,000 *looks* affordable because it
is smaller than the $220,000 of uncommitted buying power. The test is not against uncommitted BP — it
is against uncommitted BP **minus the floor**. And the number compared is the BPR the broker will
actually charge on the filled position, not the ticket's notional: a defined-risk spread can show a
large notional and a small BPR, and an undefined-risk leg can do the reverse. If the floor is tested
after the fill, Ticket A is already in the book and there is no decision left to make — which is the
failure mode §5 item 1 exists to name.

## §2 — The Deployable-Capital Ladder

```
deployable_capital = total_BP − reserve_floor
deployment_ratio   = committed_BPR / total_BP        (this is Phase 3's BPR)
```

The ladder **only tightens**. The effective ceiling on committed BPR is always

```
min( Phase 3 colour band , state ceiling )
```

so a state ceiling can never be used as relief from the existing Green / Yellow / Orange / Red
BPR bands — it can only add restriction. This is deliberate: the colour bands measure *current*
pressure, the state ceilings measure *accumulated damage*, and a book can be quiet and damaged at
the same time.

| Book state | Effective ceiling on committed BPR | Max new-ticket BPR | Why the ceiling moves |
|---|---|---|---|
| **Normal** — Green (BPR < 30%), no position taken to max loss this cycle, NAV within 5% of high-water | Phase 3 bands apply **unchanged** (Green < 30%, Yellow 30–50%) | ≤ reserve headroom; also ≤ 10% NAV notional (R6) | Nothing has been falsified yet |
| **After ONE position taken to max loss**, or Yellow (30–50%) | **≤ 50%** | ≤ 5% of NAV notional; same setup class only — **never** a size increase on the position that lost | One falsification is information: the sizing model or the regime read was wrong somewhere. Rebuild at the same size, not a larger one |
| **After TWO positions taken to max loss**, or Orange (50–70%) | **≤ 35%** | ≤ 3% of NAV notional; defined-risk only; no naked or undefined-risk legs | Two falsifications means the *book* is mis-sized, not one trade. Cut the ceiling, not just the ticket |
| **NAV drawdown ≥ 15%** from high-water | **≤ 25%** | ≤ 2% of NAV notional; defined-risk only; no new short vega | A 15% drawdown on an options book is a regime signal. The book's correlation and gamma assumptions were built in the old regime |
| **NAV drawdown ≥ 25%**, or Red (BPR > 70%), or margin utilisation > 70% | **≤ 15%** | **0 — no new tickets.** De-risk only; the reserve is now the only remaining buffer | This is the state the reserve floor exists to prevent reaching with forced sales |

At the ≤ 15% rung, ≥ 85% of buying power is uncommitted, which is the complement of the existing
"keep margin use below 40% for crash resilience" discipline — the ladder's job is to make that
ceiling shrink automatically as damage accumulates instead of relying on remembering it.

This ladder is the capital-allocation face of two mechanisms that already exist in the skill and
is **not** a replacement for either:

- **Phase 3's BPR ladder** (Green < 30%, Yellow 30–50%, Orange 50–70%, Red > 70%) — tells you the
  account's current margin pressure.
- **The drawdown cascade in Proactive Triggers and DT2** — tells you *whether* you must act.

This ladder tells you *how much room you still have to take risk after you have already been
wrong*. It is the third axis, not a duplicate of the first two.

## §3 — Exit-Liquidity Planning at Entry

Every position carries a recorded exit record **before** the fill. A position without one is not a
position; it is a future forced sale.

| Field | Meaning | Default / cap |
|---|---|---|
| `exit_route` | The named mechanism by which this position leaves the book | One of: (a) expire OTM, (b) close at 50% of max profit, (c) roll inside the bucket's roll window, (d) buy back and hold the residual, (e) accept assignment / exercise, (f) **broker-assigned or broker-liquidated — this is not a route.** If (f) is the only route, the position fails the gate |
| `exit_cost_pct` | Round-trip cost as a percentage of position value | `(ask − bid) / mid` at entry, plus the Phase 4 slippage tier. Paying half the spread to enter and half to exit costs **one full spread**, expressed as a fraction of mid |
| `exit_cost_cap` | The worst round-trip cost this position may have | **Core positions ≤ 3%; satellite ≤ 5%.** Above 5%, size down until inside the cap or do not take the ticket |
| `exit_route_liquidity` | The sizing input that makes the exit cost reachable | `position ≤ min(5% of open interest, 5% of 20-day dollar volume)` — Phase 4's existing formula. This is the **input**, not a parallel rule |

**Why the OI/ADV cap is really an exit-cost cap.** Slippage is a *per-contract* term while position
value is linear in contracts, so `exit_cost_pct` rises only through the slippage tier — which is
exactly what the percentage-of-OI sizing controls. Phase 4's slippage table already shows the cliff:
below 1% of OI costs `$0.01–0.03/contract`; above 10% of OI costs `$0.15–0.40/contract` because "you
ARE the market maker" [ESTIMATED ±30%, from the existing liquidity table]. Sizing past 5% of OI is
how a position that looked cheap to enter becomes expensive to leave.

**Worked example [COMPUTED].** SPY 500 call, bid $2.45, ask $2.55, mid $2.50:

```
exit_cost_pct = (2.55 − 2.45) / 2.50 = 4.0% of position value
dollar cost    = $0.10 × 100 × contracts = $10 per contract
on a $250 position (mid × 100) that is $10 / $250 = 4.0%
```

4.0% sits between the 3% core cap and the 5% satellite cap, so this is a satellite position. On a
$25,000 position (100 contracts) the round-trip exit is approximately `$10 × 100 = $1,000`
[COMPUTED] — a real cost that must be inside the expected edge, not discovered later.

## §4 — Forced-Selling Avoidance: What Closes First

When capital is genuinely needed, the **wrong** order is "worst liquidity first." Selling the
least-liquid positions first maximizes slippage, realizes the worst price on the assets with the
least market to absorb them, and leaves the book holding nothing but the assets nobody wanted.

The correct order closes **risk first, economics second, housekeeping third, and the balance sheet
never**:

```
Capital is needed. What closes?
├── 1. Undefined-risk / route-less positions → CLOSE NOW
│      naked shorts, anything with no exit_route, anything with no stop
│      → removes the only unlimited-loss exposures in the book
├── 2. The position or correlated cluster that CAUSED the drawdown → CLOSE
│      close the risk, not the winners. Funding a loser with a winner
│      converts a temporary mark-to-market loss into a permanent one
│      AND leaves the tail in place
├── 3. Largest dollar exit cost among positions that CAN be exited inside their cap
│      position_value × exit_cost_pct — worst economics, not worst liquidity
│      (worst liquidity is the LAST criterion, not the first)
├── 4. Most short-gamma / short-vega positions → CLOSE
│      highest |Γ| and |vega| per dollar of remaining theta
│      → they get worse non-linearly if the move continues; removing them
│        lowers the RATE of further loss
├── 5. Zero-value residuals and expired-intent hedges → CLOSE
│      housekeeping: no market impact, recovers margin and attention
├── 6. Positions already inside their bucket's default action window → CLOSE
│      pre-paying a decision the DTE calendar was going to force anyway
├── 7. NEVER FIRST: tightest-spread, deepest-liquidity, closest-to-max-profit
│      these are the balance sheet; they fund the loss at the best price the
│      book can get, and selling them first leaves only the unwanted assets
└── 8. NEVER: one leg of a correlated cluster while keeping the rest
       converts a diversified cluster into a concentrated one — raising
       tail risk at the exact moment capital is shortest
```

**The reserve floor is what makes step 7 unreachable.** With `uncommitted_BP ≥ reserve_floor`
enforced *before* each ticket, steps 1 through 4 are funded from uncommitted buying power and step
6 is never needed. That is the whole point: **the floor exists so that a good position never has to
be liquidated at a bad price.**

## §5 — Failure Modes of the Policy Itself

1. **Floor checked after the ticket.** The most common failure. The fill is done, the reserve is
   breached, and the next decision is already constrained. Mitigation: the pre-trade test in §1 is
   a gate, and a blocked ticket is logged.
2. **Reserve parked in positions.** "Cash drag" pressure converts the reserve into a position
   labelled as cash-like. Mitigation: the reserve is measured as uncommitted buying power, not as
   an intention.
3. **`WCML` computed as a sum of premiums rather than a sum of max losses.** Premium at risk is not
   max loss on undefined-risk structures. Mitigation: `WCML` reuses the Phase 0/correlation→1.0
   stress output, never a hand total of premiums.
4. **Ladder used as relief.** A book at a 25% drawdown argues its way back to the Normal ceiling.
   Mitigation: the ladder only tightens (§2), and the effective ceiling is the `min` of the colour
   band and the state ceiling.
5. **Exit cost recorded at entry and never re-measured.** Open interest and volume change; a liquid
   option becomes illiquid. Mitigation: the existing CR8 weekly liquidity refresh also refreshes
   `exit_cost_pct`.
6. **A "temporary" reserve drawdown that never gets repaid.** The reserve is spent to defend a lost
   position — the same reasoning that created the drawdown. Mitigation: a reserve breach blocks
   *all* new tickets until restored, with no discretionary exception.
7. **Liquidity-first liquidations.** Selling the illiquid assets first feels prudent ("get rid of
   the hard-to-sell things while we can") and is exactly backwards. Mitigation: §4 is an ordered
   list, and step 3 is explicit that worst-liquidity is the last criterion.
8. **Correlated cluster half-closed.** Closing one leg of a correlated cluster and keeping four
   leaves a concentrated version of the same tail with less diversification. Mitigation: step 8 of
   §4 — clusters close whole or not at all.
9. **Reserve denominated in buying power that itself shrinks.** Buying power falls as positions move
   against you, so a reserve expressed as an absolute dollar amount can silently shrink in real
   terms. Mitigation: the floor is recomputed from live `total_BP` every time it is tested.
10. **Assignment funding ignored.** Accepting assignment on T−2 without verified cash or shares
    converts a planned outcome into a broker-initiated sale. Mitigation: assignment funding is part
    of the T−2 rung of the DTE calendar and is a precondition for choosing route (e).

## §6 — Verification

- [ ] `reserve_floor` computed from live `total_BP` and NAV, with all three terms shown.
- [ ] Every new ticket has an `uncommitted_BP_after_fill` figure recorded *before* the fill.
- [ ] `deployable_capital` and `deployment_ratio` reported alongside the Phase 3 BPR.
- [ ] The effective ceiling was taken as `min(colour band, state ceiling)`.
- [ ] Every open position has a non-null `exit_route` that is not (f).
- [ ] Every open position has `exit_cost_pct ≤ exit_cost_cap`.
- [ ] Every open position satisfies `≤ min(5% of OI, 5% of 20-day ADV)`.
- [ ] A reserve breach is currently blocking new tickets, if one exists.
- [ ] The forced-selling order in §4 is recorded as the standing liquidation priority, so it is not
      improvised under pressure.
