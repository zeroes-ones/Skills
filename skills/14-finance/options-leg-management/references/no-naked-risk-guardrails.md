# No-Naked-Risk Guardrails — the R1 test, run mechanically

Ground Rule R1 is not a sentiment, it is a test with an input, an algorithm and a failure
response. This file makes it mechanical.

## The input: a resulting leg list

Before any leg order is drafted, write down the state the order will leave:

```text
  structure: <id>                          expiry: <date>
  leg 1: <+/-> <qty> x <strike><C|P>   avg <price>
  leg 2: ...
  ...
  units: <n>
```

Rules for the artifact:

- Quantities are **signed**. `+2` is long two, `−2` is short two. A list without signs is not an
  input to this test.
- Quantity is **total contracts**, not units. A three-unit fly is `+3 / −6 / +3`.
- The list must match the platform's position screen leg for leg before the test is meaningful.
  A drift between the artifact and the screen is the first symptom of a partially executed
  operation, or of an assignment that was never triaged.

## The algorithm

```text
  for each (right, side) in the leg list:
      shorts[r] = sum of |qty| over legs that are SHORT of right r
      covers[r] = sum of  qty   over legs that are LONG  of right r and
                                 sit at a strike that protects a short strike
      if shorts[r] > covers[r]:
          FAIL — report the uncovered count and the strikes
  if no (right, side) fails:
      PASS — but only if the resulting shape is also one of:
          vertical · fly/butterfly · condor · calendar/diagonal · collar
          (or a long-only position, which has no shorts at all)
```

The second condition matters. A configuration can pass the count test and still be a shape with
no defined maximum loss — a ratio spread whose extra shorts happen to be "covered" by longs at a
worse strike is the classic case. Count first, then classify the shape.

## Coverage rules by shape

| Shape | Short leg | What counts as cover | Notes |
|---|---|---|---|
| Vertical (credit or debit) | 1 short per unit | 1 long, same right, different strike, same expiry | Any width is defined-risk; the width is the max loss |
| Fly / butterfly | 2 short bodies per unit | 2 long wings per unit (near + far) | The wings must sit on **opposite** sides of the body. Two longs on one side is not a fly |
| Iron condor | 2 shorts (one call, one put) per unit | 1 long call + 1 long put per unit | Each short is covered on its own side |
| Calendar / diagonal | short front leg | long back leg, same right | Defined-risk in the sense that max loss is bounded by the debit paid plus the front-leg strike risk if the back leg expires first; verify the near/far ordering |
| Collar / covered | short call | long stock, or a long call at a higher strike | For a short call against stock, the share count is the cover |
| Ratio / backspread | extra shorts beyond the longs | nothing | **Fails R1** unless the extra shorts are themselves covered by a further long. An uncovered ratio is the accident this test exists for |
| Long-only (any combination) | none | n/a | Always passes count; still classify the shape for its own risk |

## Worked tests

### Test 1 — a three-unit fly, healthy

```text
  +3 x 95C  /  -6 x 100C  /  +3 x 105C
  shorts(call) = 6      covers(call) = 3 (95C) + 3 (105C) = 6      PASS
  shape = fly, wings on opposite sides of the body                 PASS
```

### Test 2 — the same fly after closing the near wing (FORBIDDEN)

```text
  -6 x 100C  /  +3 x 105C
  shorts(call) = 6      covers(call) = 3                           FAIL
  uncovered = 6 - 3 = 3 short call contracts
  response = STOP. Buy back 3 x 100C in the SAME package as the
             95C sale, or do not sell the wing
```

The failure is not "the position is now dangerous in theory". Three uncovered short call
contracts have unbounded loss above the strike, and the margin requirement on them rises as the
underlying rises, precisely when the account is least able to absorb it.

### Test 3 — condor after a one-side close

```text
  -1 x 95P / +1 x 90P / -1 x 105C / +1 x 110C     (1 unit, credit structure)
  close the CALL side as one package:
  -1 x 95P / +1 x 90P
  shorts(put) = 1       covers(put) = 1                            PASS
  shape = put credit vertical                                      PASS
```

### Test 4 — a ratio that passes counts and fails classification

```text
  +1 x 95C / -3 x 100C
  shorts(call) = 3      covers(call) = 1                           FAIL
```

Note the shape of the failure: this is what a fly degrades into if one body is closed and one
wing is kept. It looks tidy on a position screen and it is not a named defined-risk structure.

### Test 5 — a partially filled package

```text
  intended package: { sell 1x 105C + buy 1x 100C }
  fills: 105C sold, 100C buy still working
  intermediate state: +1 x 95C / -2 x 100C / 0 x 105C
  shorts(call) = 2      covers(call) = 1                           FAIL
```

This is why short buy-backs are sequenced **first** when a package cannot be entered as a
package: the intermediate state after a partial fill of the other leg is naked. Buy back the
body first and the partial state is `+1 K1 / −1 K2` — a defined vertical — which is a safe
place to be caught.

## When the test fails: the response ladder

| Step | Action | If unavailable |
|---|---|---|
| 1 | Do not submit the order as drafted. Re-draft as a package that keeps the coverage intact | Go to step 2 |
| 2 | If the order has already filled and the state is naked: buy back the uncovered short contracts immediately as one package | Go to step 3 |
| 3 | If the market has moved away: close the whole structure as one package — a realised loss is strictly better than an uncovered short carried overnight | Go to step 4 |
| 4 | If the venue will not fill anything (halt, no bid): buy underlying-equivalent protection so the exposure becomes a known position | Go to step 5 |
| 5 | Pre-accept the assignment in writing, with the resulting stock position sized and funded, and log the decision with a timestamp | Escalate to the desk |

`[COMMON-PRACTICE]` The ladder is the desk's convention. The underlying fact — that an uncovered
short has unbounded loss (call) or strike-to-zero loss (put) — is `[VERIFIED]` in the OCC's
standard options disclosure and in US options exchange rules.

## Common ways the test gets skipped

1. **The "obviously safe" close.** Selling a long leg of a spread to "take some off" feels
   safe because it converts a position into cash. It converts a defined-risk spread into an
   uncovered short.
2. **The screen-shaped illusion.** A position screen that shows net quantities can hide the leg
   structure. Run the test against the LEG list, never against the net.
3. **The mid-flight partial.** A package that is half-filled is a state, not a transition. Test
   the states the order can be caught in, not only the intended end state.
4. **The legacy assumption.** A structure that arrived on the book as a ticket — not built by
   you — has never had the test run. Run it before touching anything.
5. **The assignment blind spot.** An assignment overnight changes the leg list without any order
   being placed. Re-run the test after every assignment, before the next decision.

## Uncertainty and limits

- This test covers **strike coverage**, not margin adequacy, not portfolio-level risk, and not
  buying power. A position can be defined-risk and still unfundable in the account's margin
  regime. That check belongs with `options-risk-engineer` and the broker's published margin
  schedule.
- The classification list is not exhaustive. If a shape is not on it, treat the position as
  requiring the count test **plus** a written maximum-loss derivation, and state the derivation.
- European-style and cash-settled products do not convert to stock on exercise, so the failure
  mode of a naked short there is a settlement debit rather than a stock position. The count test
  still applies; the consequence differs. Verify the product's exercise style and settlement
  against the broker's product specification — do not infer it.
- Approximate is approximate: a "cover" at a strike 1¢ away from the short still counts as cover
  for this test, and it is economically almost no protection. The test is a **floor**, not a
  quality measure.
