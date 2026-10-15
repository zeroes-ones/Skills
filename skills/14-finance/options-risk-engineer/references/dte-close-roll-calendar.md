# DTE Close/Roll Calendar — The Consolidated Bucket Map

This file owns the **calendar and the force** of expiration management: which DTE bucket a position
is in, what the passage of time does to it, when review is mandated, when the default action fires,
when a roll is permitted, and the deadline after which the decision is no longer yours.

It does **not** own entry craft. Where a bucket's *content* (which strategy to open, at which
strike, at which DTE) belongs to another skill, that is stated explicitly in every row. This
calendar reconciles the piecewise DTE rules that already exist across the options family into one
table so a position can never fall between two owners.

## §1 — Why These Boundaries and Not Round Numbers

The bucket boundaries below are **desk policy placed on a derived ladder**. The ladder's *shape* is
derived; the boundary *numbers* are a chosen grid. Both halves are stated separately so neither can
hide behind the other.

**What is derived.** The boundary sits where the gamma a position carries stops being paid for by the
premium it still has to collect. At the money with r ≈ 0 (S = K, d1 = σ√T/2):

```
Gamma_ATM = φ(d1) / (S · σ · √T)                        [Δdelta per $1 of underlying]
ATM value V_ATM = S · (2Φ(d1) − 1) ≈ S · σ · √(T/2π)

Γ_ATM / V_ATM = φ(0)·√(2π) / (S²σ²T) = 1 / (S²σ²T)      because φ(0)·√(2π) = 1 exactly
```

**Corrected — and this is the part the first edition of this file got wrong.** It claimed
`Gamma_ATM / |Theta_ATM| = 2 / (S² · σ² · T)` and therefore `∝ 1/T`. The true ratio is
**independent of T**; the √T cancels:

```
Theta_ATM = − S · φ(d1) · σ / (2 · √T)                 [per year]
Γ / |Θ|   = [φ/(Sσ√T)] ÷ [Sφσ/(2√T)] = 2 / (S²σ²)      no T remains
```

and the Black–Scholes identity `Θ + ½σ²S²Γ = 0` holds at every T — which is exactly what
`portfolio-greeks-aggregation.md` states as `Θ ≈ −½·Γ·S²σ²`. The two statements are the same
identity; the earlier `2/(S²σ²T)` form contradicted the skill's own reference by a factor of `1/T`
(8.1× at 45 DTE, 122× at 3 DTE).

So "each halving of remaining life is one risk-doubling" is **not** true of `Γ/|Θ|` — that ratio is
flat in time and cannot produce a ladder. The quantity that genuinely scales as `1/T`, and the one
that describes the last three weeks, is **gamma per dollar of premium still at stake**: the premium
is what remains to be collected, the gamma is what the market can take back.

**What that yields.** From a 45-DTE entry — the open window this skill already documents:

| Remaining life | Γ (∝ 1/√T) vs entry | Γ per $ of premium (∝ 1/T) vs entry |
|---|---|---|
| 45 DTE (entry) | 1.00× | 1× |
| 22.5 DTE | 1.41× | 2× |
| 11.25 DTE | 2.00× | 4× |
| 5.6 DTE | 2.83× | 8× |
| 2.8 DTE | 4.00× | 16× |

The 2× / 4× / 8× / 16× rungs land at **≈22 / ≈11 / ≈6 / ≈3 DTE**. (Numeric check, S = 100, σ = 0.20,
r = 0: Γ/|V| = 1/(100² × 0.04 × T) → 0.0203 at 45 DTE, 0.0434 at 21, 0.1304 at 7, 0.3042 at 3 — the
ratios are 1.00 / 2.14 / 6.43 / 15.0, i.e. the doubling ladder. Γ/|Θ| = 0.005 at **every** one of
those dates.)

**What is chosen.** The zone labels in use — `14–21 plan`, `7–14 gamma acceleration`, `3–7 active`,
`0–3 critical` — and the bucket map's `0 / 1–7 / 8–20 / 21–59 / 60–120 / 121–365 / >365` are those
rungs rounded onto the listed weekly / monthly / quarterly expiration grid, plus the entry-craft
owners' own bands. The numbers 21, 14, 7 and 3 are therefore **[ESTIMATED] desk policy resting on a
[COMPUTED] shape**, not measured constants; the 60 / 120 / 365 rungs are calendar-grid choices with no
γ-scaling argument behind them at all. The `21–59` upper end of the monthlies bucket is one of those
chosen rungs, not a derived one — see §2 for why it is 59 and not 60.

**Limitations, stated explicitly.** The reduced form is exact only at the money with r = q = 0; it
holds approximately for near-the-money strikes and decays as the option moves away from the money,
where vega and vol-of-vol dominate the behaviour; it assumes a constant σ and a fixed strike; and the
denominator is the ATM value, not any particular position's mark. Recompute Γ/V from the position's
own Greeks before relying on a level — the **shape** (γ per premium dollar doubles with each halving of
remaining life) is robust, the **level** and the exact grid points are not. Admit uncertainty here
rather than quoting 21/7/3 as universal constants.

### Reconciliation of the existing corpus rules

| Rule as previously stated | Owner | Where it lands here |
|---|---|---|
| "close spreads at 50% max profit or 7 DTE, whichever comes first" | `options-risk-engineer` | Weeklies bucket, default action window |
| "plan at 14–21, gamma acceleration 7–14, critical 0–3" | `options-risk-engineer` | The 2× / 4× / 8× / 16× rungs of the **γ-per-premium** ladder (§1), rounded onto the listed expiration grid — an [ESTIMATED] grid on a [COMPUTED] shape, **not** a Γ/θ crossover (Γ/θ is flat in T) |
| "roll at 21 DTE" | `swing-options-trader` | Monthlies bucket, roll window (= T₀/2 for a 45-DTE entry) |
| "DTE < 90 → roll" | `leaps-strategist` | Annuals/LEAPS roll window (= T₀/4 for a 365-DTE entry) |
| "0DTE: close by 2:45 PM" | `intraday-options-trader` | 0DTE bucket, 14:45 ET default close |
| *(previously uncovered)* | — | **Quarterlies 60–120 DTE — this calendar is its only home** |

## §2 — The Consolidated Bucket Map

| Bucket | DTE zone | What the clock does (θ vs Γ) | Γ per $ of premium vs a 45-DTE entry — `Γ/V = 1/(S²σ²T)`, doubles per halving | Mandated review | Default action window | Roll window (the window is ours; the decision is not) | Hard deadline |
|---|---|---|---|---|---|---|---|
| **0DTE** | 0 DTE (same session) | Both maximal and path-dependent; Γ now re-rates faster than any P&L estimate can be refreshed intraday | diverges as T → 0 | Continuous (≤5 min) | Close by **14:45 ET**; **15:00 ET** hard stop | One pre-agreed strike set at 09:35; no discretionary re-entry | **15:00 ET** for equity-style; cash-settled index may hold to its settlement print |
| **Weeklies** | 1–7 DTE | Γ acceleration is the dominant term; θ is large but no longer compensates the Γ you are accepting | 6.4× – 45× | Daily at ≤7 DTE; **hourly at ≤3 DTE** | Close at 50% of max profit **or** 3 DTE, whichever comes first | T−7 → T−5, into the next monthly | T−1 15:00 ET for shorts within 2% of spot; **T−0 15:00 ET absolute** |
| **Gamma shoulder** | 8–20 DTE | θ still drives the P&L; Γ is rising but not yet governing | 2.25× – 5.6× | Twice weekly (Mon and Thu) | Hold. Resting orders at 50% of max profit. Add no new credit | **14–20 DTE** | 7 DTE |
| **Monthlies** | **21–59 DTE** | θ dominant and near-linear; Γ low and stable. This is the *open and scale* zone | 0.76× – 2.14× | Weekly | Roll expiring monthlies into the next monthly; this is the standard entry zone | **21–30 DTE** | 21 DTE for short premium; 7 DTE for defined-risk already at max profit |
| **Quarterlies** | **60–120 DTE** | θ near-linear; Γ negligible for OTM strikes. A pure carry position; vega is the only live Greek of size | 0.375× – 0.75× | Bi-weekly, plus each quarterly expiration | Hold. Harvest at 50–75% of max profit | **60–75 DTE**, into the next Mar/Jun/Sep/Dec quarterly | 45 DTE |
| **Annuals** | 121–365 DTE | θ small in absolute terms; Γ minimal; vega governs | 0.12× – 0.37× | Monthly | Hold; manage by delta and vega, not by theta | **121–150 DTE** | 90 DTE |
| **LEAPS / long-dated** | >365 DTE | θ ≈ 0 relative to position value. The risks are vega, corporate action, and early assignment — **not** decay | < 0.12× | Monthly, plus every earnings date and every ex-dividend date | Hold as a capital-efficient stock substitute. Roll the long leg into a new long-dated leg | **120–90 DTE** (`leaps-strategist` owns the 90-DTE trigger) | 60 DTE |

**Reading the table:** the "default action window" is where the *default* outcome happens without a
written decision to the contrary. "Hard deadline" is the last DTE at which the decision is still
yours — past it, the exchange, the OCC, or the broker decides for you. Review cadence, roll window and
hard deadline are each stated **once per bucket**, in this table, and DT6 in `SKILL.md` repeats the same
values rather than a second set. If the two ever disagree, this table wins.

**The 21–59 / 60–120 boundary is a chosen split, and it is stated once — here.** The first edition of
this table carried `monthlies 21–60` beside `quarterlies 60–120`, which put **60 DTE in two buckets at
once**: a 60-DTE position was simultaneously "monthlies — roll window 21–30, hard deadline 21 DTE" and
"quarterlies — roll window 60–75, hard deadline 45 DTE". Two buckets, two clocks, one position, and no
rule saying which won. The fix is the smallest one that makes the labels a **partition**: the monthlies
bucket ends at **59** and the quarterlies bucket starts at **60**. `[ESTIMATED]` — this is desk policy
on the listed expiration grid, not a γ-scale rung; §1 derives no boundary at 59 or at 60. The
consequence, stated plainly so it is never re-derived: **a position at exactly 60 DTE is a quarterly.**
It carries the quarterlies review cadence (bi-weekly, plus each quarterly expiration), the quarterlies
roll window (**60–75 DTE**) and the quarterlies hard deadline (**45 DTE**) — one set, no other. Nothing
about the 8–20 / 21–59 edge, the 120 / 121 edge or the 365 edge changes: those three were already
disjoint, at 20→21, 120→121 and 365→>365.

**Every roll window in the table is disjoint from every other.** The six windows are
`T−7 → T−5` (weeklies), `14–20` (gamma shoulder), `21–30` (monthlies), `60–75` (quarterlies),
`121–150` (annuals) and `120–90` (LEAPS), and no DTE value appears in two of them. Two windows used to
collide and both were moved onto their own bucket's edge rather than left to overlap:
the gamma shoulder's window was `14–21`, which reached one day into the monthlies bucket (21) whose own
window starts there; and the annuals' window was `120–150`, which began one day below its own bucket
(121) and shared that day with the LEAPS window `120–90`. The annuals and LEAPS windows are ordered
*down* into the next bucket by design — a long-dated position rolls as it shortens — which is why they
sit low in the DTE axis; what is **not** by design is two of them claiming the same day.

**The Γ-per-premium column is the honest one.** It is `45 / DTE` for an entry at 45 DTE, because
`Γ/V = 1/(S²σ²T)` and the `S²σ²` factor cancels in the ratio. It doubles on every halving of remaining
life, which is the ladder §1 derives. The previous edition's `Γ/θ vs entry` column (4×–16×, 2×–4×,
1×–2× …) came from the false `Γ/θ ∝ 1/T` formula and has been removed: `Γ/θ = 2/(S²σ²)` is flat in
time and cannot scale with DTE at all. The bucket **boundaries** remain desk policy rounded onto the
listed expiration grid — a derived shape on a chosen grid, not measured constants.

**Roll rule — not ours (corrected ownership).** This calendar owns the roll **window** and the
**hard deadline**: *when* a roll may be executed and *when* the decision stops being yours. The roll
**rule** (a roll must be credit-or-flat on the same strike and structure class), the roll **cap**, and
the decision *whether* to roll, trim or close are **`options-position-lifecycle`'s**. Ask that skill
for the verdict at the window; this calendar only enforces that the window is used and the deadline is
not passed. Do not restate the rule here — two owners for one rule is how the last edition drifted.

## §3 — Expiry-Week Mechanics, T−5 to T+1

All times Eastern. This is the timeline the phase enforces. T−0 is expiration day.

| Leg | Clock | Mandated action | If you do nothing |
|---|---|---|---|
| **T−5** (Mon of expiry week) | Pin-risk monitoring begins | List every short strike within 2% of spot. For each ITM short leg, open an action record: close / roll / accept | Nothing happens yet. Positions are still liquid and rolls are still cheap |
| **T−4** | Roll economics close | Roll while the market is still two-sided — the *decision* to roll at all is `options-position-lifecycle`'s; this calendar only says the window closes here. Check every short call's ex-dividend date against its remaining time value | Spreads begin to widen; a roll that was flat on T−4 costs a debit by T−2 |
| **T−3** | Margin inflation begins | Final roll or final close for any position that cannot accept assignment. Recompute margin: short-option margin inflates into the final week and can rise sharply | Broker margin requirement rises on its own. You find out when the excess-liquidity number shrinks |
| **T−2** | Assignment funding decision | For every ITM short leg you intend to accept: verify the cash or shares are actually there. Assignment funding failure is a broker-initiated close, at the broker's price | An unfunded assignment risk becomes a forced close on T−0 or T−1 at whatever price the market offers |
| **T−1** | Early-assignment day | This is the dividend-capture day. Any short ITM American call whose remaining time value is below the upcoming dividend can be exercised against you **today** | Assignment overnight. You learn about it after the fact |
| **T−0 09:35** | Pin guard | Re-confirm: any short strike within 1% of spot → close, do not monitor | Pin risk stays live and re-rates to the underlying's afternoon move |
| **T−0 12:00** | Half-day check | On a half session the close is 13:00 ET — collapse the whole remainder of this table onto the morning | On a half day, everything below happens four hours early |
| **T−0 14:45** | Last voluntary close | Close everything you do not want assigned. This is the 0DTE default close and the last practical voluntary exit for any short leg | You are now relying on the broker's process, not your own |
| **T−0 15:00** | Practical absolute deadline | Your own execution is realistically over. Spreads are at their widest and market makers are withdrawing | Broker auto-liquidation windows begin in this region; you are a price-taker [BROKER-VERIFIED, broker-dependent] |
| **T−0 15:45** | Do-not-rely window | Recorded here as the point past which a limit order at mid has near-zero fill probability. Treat 15:45 as a deadline for **hoping**, not a deadline for acting | An unfilled limit order provides exactly the protection of doing nothing |
| **T−0 16:00** | Equity options stop trading | Whatever you hold is what settles. SPX and VIX options trade until 16:15 ET [VERIFIED — exchange rules] | Position settles per its own terms (below) |
| **T−0 17:30** | OCC exercise-notice cut-off | Exercise notices for expiring options are delivered to OCC by 17:30 ET on expiration day [VERIFIED — OCC By-Laws Art. VI, exercise notices]. Your broker's internal cut-off is **earlier** and is the one that binds you [BROKER-VERIFIED] | Your broker's earlier cut-off already passed; the decision was made for you |
| **T−0 evening** | Clearing | OCC processes exercise and assignment notices; the broker is notified | — |
| **T+1 09:30** | Realization | Assignment notifications read. Any auto-exercised short leg is a stock position at Monday's open. Weekend gap is realized, not avoided | Cash-settled index positions net out in cash; everything else is now a share position with share-position risk |

## §4 — What Happens If You Do Nothing

| Position state at the close | Outcome | Notes |
|---|---|---|
| Long, ITM by ≥ $0.01 | Auto-exercised by OCC's exercise-by-exception unless the holder instructs otherwise [VERIFIED — OCC exercise-by-exception] | The default is exercise, not expiry. "It probably won't be exercised" is the exact inverse of reality |
| Long, ITM, but you lack the cash or shares to fund it | Broker may close the option before the close to avoid creating an unfunded obligation [BROKER-VERIFIED] | You do not get to choose the price |
| Long, OTM | Expires worthless | — |
| Short, ITM by ≥ $0.01, American-style physical | Assigned. Short call → you deliver 100 shares per contract (short stock if you do not own them, with unlimited upside risk). Short put → you buy 100 shares per contract | Not optional. This is the mechanism, not a risk |
| Short, ITM by ≥ $0.01, European cash-settled index | Cash settlement of the intrinsic difference. No shares, no Monday gap on the underlying | Why cash-settled index options are preferred for undefined-risk structures |
| Short, OTM | Expires worthless; premium retained | — |
| Any short leg inside the pin band at the close | Assignment is genuinely uncertain in both direction and quantity | This is the one case where the outcome is not knowable in advance — which is why the calendar closes it rather than predicting it |

## §5 — American vs European: The Two Mechanics That Change the Whole Decision

**American-style, physically settled (all standard listed equity and ETF options — SPY, QQQ, IWM,
AAPL, and every single-stock option).**

- Exercisable by the holder on **any business day** before expiration, not just at expiration.
- Settlement delivers **100 shares per contract**. Assignment creates a share position.
- **Ex-dividend early-assignment risk applies to ITM short calls.** When the remaining time value is
  below the upcoming dividend, exercise becomes rational for the holder and assignment probability
  rises sharply [VERIFIED — dividend-driven early exercise].
- Consequence for the calendar: the T−1 rung is a real decision rung, not a formality.

**European-style, cash-settled (the index complex — SPX, XSP, NDX, RUT, DJX, VIX).**

- **No early exercise. No assignment. No shares.** Settlement is a cash difference.
- Consequence for the calendar: the T−5 → T−1 rungs are about *price* risk and roll economics only.
  The T−1 dividend rung does not exist for these products.
- **Settlement-value mechanics differ by listing, and this is the trap:**
  - Third-Friday SPX/NDX/RUT contracts are **AM-settled, European-style** — the settlement value is
    a Special Opening Quotation computed from opening prices on expiration day, **not** the closing
    index level [VERIFIED — CBOE contract specifications]. A position can be ITM at Thursday's
    close and settle OTM at Friday's open, or the reverse.
  - Weekly and end-of-month index contracts (SPXW and equivalents) are **PM-settled to the close**
    [VERIFIED — CBOE].
  - VIX options are **European-style, cash-settled, expire on Wednesday, and settle to a Special
    Opening Quotation of VIX** — they do not expire on the third Friday with the equity complex
    [VERIFIED — CBOE VIX contract specifications].
- **Corporate action, and this is where you must flag your knowledge cutoff.** Splits, mergers, and
  spin-offs produce **adjusted (non-standard) contracts** with a changed deliverable. An adjusted
  contract's strike, multiplier, and settlement no longer match the standard template — treat any
  position inherited from before your knowledge cutoff as unverified until the contract terms are
  read from the exchange or the broker. Never guess security terms.

## §6 — Calendar Hazards That Move the Deadline

| Hazard | Effect on the calendar | Handling |
|---|---|---|
| **Half-day session** (the Friday after US Thanksgiving, Christmas Eve when it falls on a Friday) | The equity close is 13:00 ET; options cease trading then. Every rung from 12:00 down collapses into the morning | Treat the whole T−0 column as shifted four hours earlier. The 14:45 close becomes 10:45 |
| **Standard monthly expiration** | Third Friday of the month | The default monthly roll rung |
| **Quarterly expiration / triple witching** (third Friday of Mar, Jun, Sep, Dec) | Stock options, index options, and index futures expire together; liquidity concentrates and then withdraws. Index rolls are best done ahead of it | Move the quarterly roll window *before* the quarterly date, not into it |
| **Weekly and end-of-month listings** | Only a subset of underlyings carries them (major ETFs and index products) | Never assume a weekly exists for a single name — confirm the listing before planning a weekly roll |
| **Exchange holiday on the expiration Friday** | Expiration moves to the preceding business day | Pull the whole timeline forward; do not assume the third Friday |
| **Non-standard / adjusted contracts** | Changed deliverable after a corporate action | Never guess security terms; read the contract terms |
| **Early broker close** | Brokers close exercise/assignment desks earlier than OCC's 17:30 ET cut-off | The binding deadline is always the broker's [BROKER-VERIFIED] |

## §7 — Failure Modes of the Calendar Itself

1. **The calendar is treated as advice rather than a force.** A bucket with a "recommended" action
   degrades to no action. Mitigation: the hard deadline is a *trigger*, logged with a timestamp,
   not a suggestion.
2. **Rolls accumulate — a lifecycle risk, not a calendar one.** Rolling indefinitely keeps a broken
   thesis alive and pays the spread every cycle. Mitigation belongs to `options-position-lifecycle`
   (its roll rule and roll cap); this calendar's contribution is only that the roll *window* is finite
   and the hard deadline is enforced.
3. **Debit rolls disguised as rolls.** A roll that widens risk is a new position. Mitigation:
   `options-position-lifecycle`'s credit-or-flat test — this calendar does not restate it.
4. **Bucket boundary mis-assignment.** A 20-DTE position treated as a monthly because 21 is the
   nominal boundary. Mitigation: buckets are assigned by the position's own **gamma** (Γ ∝ 1/√T) and
   the *nearest* boundary, not by rounding down to the gentler bucket.
5. **Half-day blindness.** Applying the 14:45 rung on a 13:00 close. Mitigation: the session
   calendar is a required input, checked at T−5.
6. **European/American conflation.** Applying equity-style early-assignment logic to cash-settled
   index options (or the reverse) produces either a phantom risk or a real unmanaged one.
   Mitigation: settlement type is a required field on every position record.
7. **Settlement-print blindness.** Assuming an AM-settled index contract settles at the close.
   Mitigation: settle-on-open vs settle-on-close is a required field.
8. **Quarterlies invisibly unmanaged.** The 60–120 DTE bucket had no owner before this calendar;
   positions sat between "monthly" and "long-dated" with no review cadence. Mitigation: the
   bi-weekly review and the 60–75 DTE roll window.
9. **Assignment funding assumed.** Deciding to accept assignment without verifying the cash or
   shares exist. Mitigation: the T−2 funding check; funding failure is a forced close at the
   broker's price.
10. **Corporate action ignored across a knowledge cutoff.** Mitigation: `Flag your knowledge
    cutoff` — an inherited position is unverified until its terms are re-read.

## §8 — Verification

- [ ] Every open position carries a bucket label and a settlement-type label.
- [ ] The seven buckets are a **partition**: every DTE value lands in exactly one of
      `0 / 1–7 / 8–20 / 21–59 / 60–120 / 121–365 / >365`. In particular a 60-DTE position is a
      quarterly — it is not also a monthly, and it does not carry two roll windows or two deadlines.
- [ ] Every bucket's **roll window is disjoint** from every other bucket's: `T−7 → T−5`, `14–20`,
      `21–30`, `60–75`, `121–150`, `120–90` — no DTE value appears in two of them.
- [ ] Review cadence, roll window and hard deadline are taken from §2's table (or DT6, which repeats it
      verbatim) — never from a second, locally-invented set of boundaries.
- [ ] Every position past its default action window has a written, timestamped hold decision.
- [ ] No position is past its hard deadline without a hold decision.
- [ ] Every roll this cycle was reported to `options-position-lifecycle` for its credit-or-flat and
      roll-cap verdict, and no position was rolled past this calendar's hard deadline. (The rule and the
      cap are that skill's to state; the window and the deadline are this one's.)
- [ ] Pin risk is expressed in the two Phase-1 bands — 2% of spot to monitor, 0.5% to act, 1% on T−0 —
      and no other percentage is in use anywhere in the file.
- [ ] The Γ-per-premium column is quoted (or recomputed from the position's own Greeks), and no `Γ/θ`
      ladder is claimed anywhere: `Γ/θ = 2/(S²σ²)` is flat in T and cannot generate rungs.
- [ ] The expiry-week rungs are scheduled (not just known), including the half-day shift.
- [ ] Ex-dividend dates are checked for every ITM short American call.
- [ ] Settlement-print basis (AM/PM) is recorded for every index position.
- [ ] Every position's contract terms have been re-read since the last corporate action affecting it.
