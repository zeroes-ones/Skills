# Position Health Check Protocol

The ordered check that runs before any action is considered on an open equity position. It is deliberately boring and deliberately fixed: the point is that the same eight questions are asked in the same order every time, so that a decision made on a bad day looks like a decision made on a good one.

**Portability target:** spec-level. Nothing here depends on a particular broker, screen or platform.

## Why the order is the protocol

For an option, the clock eventually forces the review — DTE runs out and the position resolves itself. An equity position never does. Nothing expires, nothing settles to zero because a date passed, and no margin desk arrives to ask what you intend. What is left is the order in which you look at things, and the order is where the mistakes live.

If the first number in a review is a P&L percentage, the review is already about the wrong variable. The position can be down 30% with an intact thesis or up 40% with a broken one. The order below puts the level before the money on purpose, and puts the forced action before the level, because a margin call settles arguments that the level only starts.

## The eight steps

| Step | Question | Data needed | Gate? |
|---|---|---|---|
| 1 | Forced action live? | Margin, borrow, intraday-margin, halt/delisting state | **YES** |
| 2 | Is the written invalidation level intact on the close? | The level, the close | **YES** |
| 3 | Is it still the position the contract describes? | Share count, lot set, basis, overlays, corporate actions | **YES** |
| 4 | What is on the event clock inside 10 business days? | Earnings, ex-dividend, reconstitution, FOMC | No |
| 5 | What is on the tax clock? | Days to the anniversary, window states | No |
| 6 | Where is the position against its plan rung and band? | Mark, basis, band definitions | No |
| 7 | Can the exit fill at size, and is it inside the per-idea band? | Spread, depth, position percentage | No |
| 8 | Are the level, target, date and event list written? | The contract itself | No |

**Steps 1–3 are gates.** A FAIL on any of them ends the check and escalates the position to ACT. There is no partial credit and no "mostly intact". An invalidation that has been breached by 2% has been breached.

## Pass/fail criteria, step by step

### Step 1 — Forced action

- **FAIL** if a margin call is outstanding, a borrow has been recalled, the account carries a live intraday (day-trading) margin restriction — the framework that replaced the "pattern day trader" designation in 2026, so verify the current requirement with the firm — or the security is halted or delisting.
- The regulation matters here: a deficiency of **$1,000 or less** requires no action, and above that the firm must liquidate — with **no advance notice required** [VERIFIED — 12 CFR 220.4(d)]. That is a fact about the account, not an opinion about the position.
- Pass/fail is not a judgement call in this step. It is a lookup.

### Step 2 — Thesis and invalidation

- **FAIL** if the close is beyond the written level, or if the reason the position exists has been withdrawn (the thesis was never "it is a stock I own").
- The level must be a **price**, written at entry and versioned. A percentage of entry is not a level: it moves every time the basis moves, which is precisely the failure the level exists to prevent [COMMON-PRACTICE] — the convention is a desk convention, not a regulatory one.
- If no level exists, the step **FAILS by absence**. An undocumented position is unmanaged, and the fix is to write the level now and re-run the check from step 1.

### Step 3 — Position identity

Equity positions mutate quietly. Between reviews a position can gain shares from a reinvestment, lose shares to a call or a tender, change basis from a spin-off, or acquire an overlay nobody remembers writing. Check, in order:

- **Share count** against the contract.
- **Lot set** — how many lots, acquired when, at what basis. This is not a tax exercise here; it is an identity check, because a trim decision made against the wrong lot is a different decision.
- **Basis** — if it moved and nobody can say why, that is the finding.
- **Overlays** — written calls, protective puts, collars, a standing order that never filled.
- **Pending corporate actions** — merger, cash-and-stock election, spin-off, special distribution, split. A forced corporate action delivers a *new* position; the router runs again on it.

- **FAIL** on any unexplained discrepancy.

### Step 4 — Event clock

List, with dates, everything inside the next ten business days:

- Earnings (date and intraday or post-close timing).
- Ex-dividend date — and, if a qualified-dividend window is in play, the 61-day count inside the 121-day period beginning 60 days before the ex-date [VERIFIED — IRC §1(h)(11), §246(c)].
- Index reconstitution: S&P share and IWF changes are effective after the close of the third Friday of March, June, September and December [VERIFIED — S&P U.S. Indices Methodology]; the Russell reconstitution runs annually in June, effective after the close of the last Friday in June, moving to a semi-annual schedule (June and December) from 2026 [VERIFIED — FTSE Russell reconstitution documentation].
- Macro events with a scheduled date.

The output of this step is a list. "Nothing material" is a valid list, but it must be written, not assumed.

### Step 5 — Tax clock

Three dates, nothing more:

- **Days to the anniversary.** The holding period begins the day *after* the buy trade date and ends *on* the sale trade date, so the earliest long-term sale is the buy date plus one year plus one day [VERIFIED — IRC §1222, IRS Pub 550].
- **Wash-sale window state.** The window is 61 days: 30 before through after the loss sale, and replacement shares inherit the old holding period [VERIFIED — IRC §1091, §1223(3)].
- **Qualified-dividend window state.** Open, met, or not applicable.

This step **flags**; it does not decide. It produces one line that step 6 and the router consume.

### Step 6 — Plan rung and band

Label the position exactly one of: **rung hit**, **inside band**, **band breach**. Not "about flat", not "a bit underwater". The band is defined by `portfolio-signal-manager`'s published caps — no position above 10% of the book, no sector above 25% [VERIFIED — the caps published in this library's `portfolio-signal-manager`].

### Step 7 — Liquidity and concentration

- Can the intended exit fill at the size you intend, at a spread you would accept today?
- Is the position inside its per-idea band **after** the change you are contemplating (an add, an average down, a partial trim)?

If either answer is no, record which one, because step 7 is what makes clause 3 of the average-down gate fail on so many real positions.

### Step 8 — Records

Write: the invalidation level, the target, the improve-by date, the event list with dates, the tax flag, and the standing queued actions. The contract is not a feeling; it is five fields.

## Stop-early rule

A FAIL on steps 1–3 ends the review and produces a disposition immediately:

| Failed step | Immediate disposition |
|---|---|
| 1 (forced) | CLOSE or reduce only, inside the window the firm gave you |
| 2 (thesis/level) | CUT, or CLOSE if there is no reason to own the name at all; tax is not a counter-argument |
| 3 (identity) | Freeze the name, rebuild the contract, then re-run from step 1 |

Only when steps 1–3 all PASS does the review continue to the clocks, the band and the liquidity check, and only then does the router pick an action.

## Worked transcript

A four-month-old position, down 15%, earnings in six sessions, invalidation level not on file.

```text
Step 1 forced action ....... clear (no margin call/recall, no intraday flag)   PASS
Step 2 thesis/level ........ FAIL — no written level exists                    ACT
Step 3 identity ............ not reached
```

Disposition: freeze new risk in the name, write the level and version it, then re-run from step 1. Note what did *not* happen: the earnings decision was not made, the average-down gate was not run, and no action was taken on price. Those are all downstream of step 2, and step 2 failed.

On the second pass, with the level written:

```text
Step 1 forced action ....... clear                                             PASS
Step 2 thesis/level ........ level intact on the close                         PASS
Step 3 identity ............ 600 sh, 3 lots, basis confirmed, no overlay       PASS
Step 4 event clock ......... earnings in 6 sessions → PREPARE, decide now
Step 5 tax clock ........... 240 days to the anniversary; no window open       flag: none
Step 6 plan rung ........... inside band, no rung hit
Step 7 liquidity/concentration  exit fills at size; position 16% of the book → over band
Step 8 records ............. level, target, improve-by date and event list written
```

Router result: the event clock forces a written pre-earnings decision; the average-down gate fails at clause 3 on arithmetic ($40,000 of a $250,000 account is 16% against a 10% cap [COMPUTED]: 40,000 ÷ 250,000 = 16.0%); the disposition is HOLD-WITH-DEADLINE with an improve-by date and a level trigger.

## Failure modes of the protocol itself

1. **Step 6 read first.** The single most common collapse of the protocol. Countermeasure: steps 1–3 are written down before step 6 is looked at.
2. **Step 2 passed by assertion.** "The thesis is fine" without a level. Countermeasure: the level is a price or the step fails.
3. **Step 3 skipped because the position "hasn't changed".** Equity positions change without anyone trading them. Countermeasure: the identity check is a gate.
4. **Step 5 turning into a decision.** The tax clock flags; the router decides. Countermeasure: step 5 has no disposition of its own.
5. **The transcript being thrown away.** An unrecorded review cannot be graded, and an ungraded review cannot improve the protocol. Countermeasure: the review record is the evidence format in `examples/backtest/README.md`.

## Verification guardrails for a review

- **Complete when** steps 1–8 are each marked pass/fail or recorded as not-reached.
- **Complete when** the invalidation level is written as a price, with its version date.
- **Complete when** the event list carries dates, and every event inside 10 business days has a written pre-event decision.
- **Complete when** the tax flag is one line naming the nearest date and any open window.
- **Complete when** the band state is a label with the arithmetic behind it.
- **Complete when** exactly one action is chosen and the losers are queued in writing.
- **Complete when** the next review date and the level trigger are both on file.
- **Complete when** the action carries one sentence of expectation and a grading date.

If any of those is missing, the position is flagged unmanaged at the next book review — not because the review was wrong, but because it cannot be shown to have happened.
