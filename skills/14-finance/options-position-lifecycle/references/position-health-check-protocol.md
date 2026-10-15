# Position Health Check Protocol

The ordered per-position scan. Seven steps, fixed sequence, roughly two minutes per position for someone who has done it a hundred times. The order is the protocol: steps 1–3 are gates that end the scan, steps 4–7 are diagnostics that shape the action.

## Why the order is fixed

Every position-management failure worth documenting comes from reading the financial output before the structural inputs. A trader who opens with "we're down 18%" is already negotiating with a number they cannot control. A trader who opens with "the level held, the structure is intact, we have 31 days" has three facts that determine almost everything, and the P&L is a consequence rather than a prompt.

The order also makes the scan parallelisable: because steps 1–3 are gates, a whole book can be triaged in a few minutes by running the gates on everything and only finishing steps 4–7 on the survivors. That is the difference between reviewing twenty positions and reviewing none.

Ordered by **what cannot be recovered**:

1. Thesis — if it is gone, nothing downstream matters.
2. Structure — if it is not what you think it is, every number downstream is wrong.
3. Clock — if the clock has run out, the best plan is unavailable.
4. P&L — what the market has said so far.
5. Liquidity — whether the exit you are planning is physically possible.
6. Events — what will happen before the clock runs out.
7. Instruments — whether the machine that is supposed to execute your plan is still plugged in.

## Step 1 — Thesis: is the level still intact?

**Definition.** The thesis is a level or a named condition that had to be true for the position to be worth holding. "I think it goes up" is not a thesis. "The 50-day holds on a closing basis and the stock stays above the short strike until expiry" is.

**Pass criteria.**
- The invalidation is written as a price, a level, or an unambiguous condition.
- The last close (or the defined measurement, for a condition) is on the correct side of it.
- The statement is unchanged since the last review, or a change is recorded with a reason and a date.

**Fail criteria.**
- No level exists, or the level was restated without a written reason.
- The measurement is ambiguous (intraday touch versus closing basis — pick one and record which).
- The level broke and the previous review did not record a disposition.

**Worked example.** A 32-DTE put credit spread on a name at 118, short strike 112, invalidation "closing basis under 112". The last close is 111.40. Step 1 fails. The scan stops. The position escalates one rung. Nothing else about the position is examined until the disposition is written, because a broken level is not improved by knowing that the trade is currently up on theta.

**Common error.** Grading the thesis against the *mid* rather than the close. A wick through a level on a thin session is not a breach of a closing-basis invalidation; treating it as one produces a cut that the plan never authorised. State the measurement at entry, then hold yourself to it in both directions.

## Step 2 — Structure integrity: is this the position you think it is?

**Definition.** Compare the structure now held against the structure as designed. Legs present, widths unchanged, ratios at design, no naked exposure, no residual stock from an assignment.

**Checks.**

| Check | How | Fail looks like |
|-------|-----|-----------------|
| Leg count | Count positions against the design | One leg closed early "to reduce cost" |
| Widths | Compare spreads between strikes | A stop-loss that closed one leg, leaving a naked short |
| Ratios | Compare contract counts per leg | A 1:1 spread that has become 2:1 after a partial close |
| Underlying exposure | Look for stock or a residual option | Assignment left 100 shares nobody planned for |
| Expiry alignment | Confirm all legs expire together | A diagonal created accidentally by a roll on one side |

**Why it is a gate.** Every downstream number — max loss, break-even, margin — is computed from the structure as designed. If the structure changed and the numbers did not, the plan is being run against a position that no longer exists.

**Fail example.** A four-leg iron condor where the call spread's short leg was bought back during a spike. The position is now a put credit spread plus a naked long call — a completely different risk profile with a completely different margin treatment. Step 2 fails regardless of whether the position is profitable, and the disposition is CONVERT or RESTRUCTURE, executed through `options-leg-management`.

## Step 3 — Clock: what does the DTE bucket force?

**Definition.** DTE remaining, mapped to the bucket, mapped to what that bucket forces.

| Bucket | Forced by the clock |
|--------|---------------------|
| 0–2 DTE | Expiry protocol: decide by 15:45 ET on expiry day; assignment risk is live; no new extrinsic |
| 3–7 DTE | Gamma watch: intraday attention; pay no new extrinsic to extend |
| 8–21 DTE | Repairs still possible; theta accelerates; rolls get expensive |
| 22–45 DTE | The working zone: level tests can still complete; trims are cheap |
| 46+ DTE | Structural thinking zone: rolls are near-free in theta terms, patience is affordable |
| LEAPS (>365 DTE) | Monthly rhythm and planned roll windows; delta- and rho-driven |

**Pass criteria.** The bucket and one sentence of "what this forces" are written. The sentence names an action or an explicit non-action.

**Fail criteria.** The bucket crosses into a tighter one and the plan has not been re-examined. A repair that needed a level test at 20 DTE cannot complete at 9 DTE; that is a step 3 fail, not a step 1 fail.

**The stop-early rule in practice.** Steps 1–3 each terminate the scan on failure. The point is not speed for its own sake; it is that a position failing steps 1–3 has an answer already, and continuing to steps 4–7 invites the P&L to argue with the structure. Once the escalation is written, the position may return to the scan at step 4 — but only after the disposition exists.

## Step 4 — P&L versus plan (a band, not an emotion)

**Definition.** Place the position into one of three bands, defined at entry by `trade-sizing-recovery`:

- **Rung hit** — at or above a take-profit rung. Action: TRIM whole units.
- **Inside band** — between the rungs and the stop band. Action: continue to steps 5–7.
- **Band breach** — through the stop band. Action: CUT, or RESTRUCTURE if and only if the written gate passes.

**Why bands and not feelings.** A band is a pre-commitment. It was set when the trader was calm and had no position in the outcome. Reading the number against a band produces a decision; reading it against yesterday produces a narrative.

**Worked example.** A debit vertical cost $1.80 ($180 per spread) on a $5.00-wide spread. Rung 1 is that family's TP rung 1 in `trade-sizing-recovery`'s Canonical Threshold Table — 50% of max profit for a debit vertical, i.e. $1.80 + 0.5 × ($5.00 − $1.80) = $3.40 [COMPUTED]. The position is marked $3.41. Rung hit → TRIM. The fact that the underlying "looks like it wants to keep going" is not a step-4 input; it is a step-6 input at best, and it does not outrank a booked rung.

**Common error.** Re-basing the band mid-trade. If the band moves, that is a rule change, and rule changes require a written reason and a grading date, both recorded in the review log.

## Step 5 — Liquidity: does the exit still fill at size?

**Definition.** Whether the intended exit is physically executable at the size required, within a spread you would accept.

**What to read.**
- Bid/ask width in absolute and percentage terms, and how it has moved since entry.
- Open interest and today's volume on each leg you intend to trade.
- Whether the exit is one structure trade or a set of legs that must be legged (a liquidity risk all its own).
- The session: a market you can only trade in RTH is a market you cannot exit at 4:05 p.m.

**Classification.**

| Reading | Classification | Consequence |
|---------|---------------|-------------|
| Width ≤ 5% of mark, OI in the thousands | Tradeable | Exit is a real option |
| Width 5–15% of mark, OI in the hundreds | Marginal | Exit works but costs; price it into the decision |
| Width > 15% of mark, OI under a few hundred | Not reliably tradeable | Reclassify as a write-off candidate |
| No bid at all | Unexecutable | Write-off; the attention you stop spending is the recovery |

**Worked example.** A $0.35 mark with a $0.15 wide market: the round trip is roughly 43% of the remaining value [COMPUTED: $0.15 ÷ $0.35 = 43%] from the quoted market. If the remaining value is small, paying that to exit is worse than letting it expire — which is an execution judgement, not a change to the decision that the position is dead.

**Rule.** Liquidity decides the *mechanism*, never the *decision*. Whether you cut or write off is execution; whether you leave is thesis.

## Step 6 — Events before expiry

**Definition.** Every scheduled event between now and expiry that can change the position's outcome independently of the level.

Use the checklist in `event-and-expiry-recheck.md`. The minimum set for equity options:

- Earnings, with the before-open/after-close distinction.
- FOMC and other scheduled macro prints inside the window.
- Ex-dividend dates for every short call leg.
- Index rebalance and quarterly expiration effects for index-heavy underlyings.
- Trading holidays and half-sessions, because they move the expiry-day clock.

**Pass criteria.** Each item is explicitly present or explicitly absent in the record. An empty event list is a pass only if it was checked, not if it was assumed.

**Fail consequence.** PREPARE, not ACT: the decision is made now and executed at the event boundary. Deciding to "see what happens" across an earnings print is a bet on the print, and if that is the intent it must be sized as one.

## Step 7 — Are the brackets live and correctly priced?

**Definition.** Both instruments exist, on the correct side, priced against the structure as it is now held, and valid for the session they need to fill in.

**Checklist.**
- TP order exists, or a documented deliberate no-TP status ("dead lot, no-TP by construction").
- SL reference exists as a level plus an action, not as a resting order only.
- Both are priced against the *current* structure, not the structure at entry.
- Session validity: RTH-only venues will not fill in extended hours.
- Quantity matches the structure; a bracket sized for the original leg count after a partial close is a latent naked position.

**Why this is last.** It is the least interesting step and the most commonly skipped, which is exactly why it earns a permanent slot. An unmanaged structure overnight is a structure whose worst case nobody wrote down.

## The stop-early rule, stated precisely

> If **any** of steps 1, 2 or 3 fails, write the ACT disposition on the escalation ladder, and only then resume from step 4.

Three consequences worth stating:

1. **The disposition is written before the P&L is read.** This is deliberate. It prevents the money from arguing with the structure.
2. **A step 1–3 fail cannot be cured by a good mark.** A position up 40% with a broken thesis is still an ACT; the profit is a reason to exit well, not to stay.
3. **Escalation is a rung, not a panic.** A step 1 fail moves the position one rung (WATCH → PREPARE, PREPARE → ACT). It does not authorise an immediate market exit unless the position was already at ACT.

## Timing budget

| Step | Trained practitioner | Under pressure |
|------|---------------------|----------------|
| 1 Thesis | 15 s | 10 s (the level is memorised) |
| 2 Structure | 25 s | 20 s |
| 3 Clock | 10 s | 5 s |
| 4 P&L | 15 s | 15 s |
| 5 Liquidity | 25 s | 20 s |
| 6 Events | 20 s | 30 s (this is the step that gets skipped, and the one that bites) |
| 7 Instruments | 15 s | 10 s |
| **Total** | **~2 min** | **~2 min** |

The budget matters because the alternative is not a slower review, it is no review. A scan that takes twenty minutes per position will be run on two positions a week.

## Worked transcript (abridged, three positions)

```text
Position A — 41 DTE, iron condor, credit $1.35, marked $1.10 = +18.5% of credit
 1 Thesis: level intact, no change since last review .................. PASS
 2 Structure: 4 legs, widths 5/5, ratio 1:1:1:1 ........................ PASS
 3 Clock: 41 DTE, working zone, repairs affordable .................... PASS
 4 P&L: +18.5% of credit [COMPUTED: (1.35 - 1.10) / 1.35]; the iron-condor
         rung 1 in trade-sizing-recovery's table is 25% of max credit
         → inside band ............................................... continue
 5 Liquidity: 0.20 wide on a 1.10 mark, OI in the thousands ............ tradeable
 6 Events: earnings 12 DTE before expiry .............................. PREPARE
 7 Instruments: TP armed at the family rung; SL level recorded ........ PASS
 → Action: HOLD, with the pre-earnings decision dated, not left to the event.

Position B — 28 DTE, put credit spread, marked −65% of credit
 1 Thesis: closing basis under the short strike 2 sessions ago ....... FAIL
 → STOP. Escalate PREPARE → ACT.
 → Action: CUT into the first RTH window. (Step 4 not consulted before the
   disposition was written.)

Position C — 6 DTE, long call, marked −22% of debit
 1 Thesis: breakout level held on the close ........................... PASS
 2 Structure: single leg, intact ..................................... PASS
 3 Clock: 6 DTE, gamma watch active; a level test cannot complete ..... FAIL
 → STOP. The plan needed a level test; the clock no longer allows it.
 → Action: CUT into strength today, while extrinsic remains.
```

Note what position C shows: a step 3 failure is not about the market, it is about the *plan* no longer fitting the *clock*. That is the single most common reason a position is carried into expiry unresolved.

## Failure modes of the protocol itself

1. **Running it out of order under time pressure.** Countermeasure: the seven steps are a numbered list in the record; an unnumbered review is not a review.
2. **Treating a pass as an endorsement.** Passing steps 1–3 means "no forced action", not "good trade". The router still decides.
3. **Replacing the check with a monitor.** An alert on the level is a good floor and a poor substitute; alerts do not check structure or events.
4. **Skipping steps 6 and 7 because they are boring.** These are precisely the steps with the largest ratio of avoided loss to effort.
5. **Letting the scan become the decision.** The scan produces a state; the router produces the action. Conflating them produces "the review said hold", which is not a thing.

## Record template

```text
position:            <name, structure, expiry, contract count>
reviewed_at:         <timestamp, timezone>  source: <quote source>
step1_thesis:        <level>  last_close: <price>  result: PASS|FAIL|CHANGED
step2_structure:     legs:<n> widths:<w> ratio:<r> naked:<none|detail>  result: PASS|FAIL
step3_clock:         dte:<n> bucket:<z> forces:<one sentence>            result: PASS|FAIL
step4_band:          rung:<t> inside|breach|rung_hit  mark:<price>
step5_liquidity:     width:<abs>/<%>  oi:<n>  classification:<tradeable|marginal|writeoff>
step6_events:        earnings:<date|none> fomc:<date|none> exdiv:<date|none> other:<...>
step7_instruments:   tp:<live|absent|n/a>  sl:<level: ...>  session:<rth|ext>
disposition:         <action>  rung:<WATCH|PREPARE|ACT|FORCE>
expectation:         <one sentence>   grade_on:<date>
```
