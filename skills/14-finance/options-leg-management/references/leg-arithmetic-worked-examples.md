# Leg Arithmetic — Worked Examples

Every figure in this file is arithmetic performed on **explicitly stated inputs**. Inputs are
marked `[ESTIMATED]` because they are illustrative prices chosen to make the arithmetic
readable; the results are marked `[COMPUTED]` because they follow deterministically from those
inputs. No figure here is a measured market result, and none of these are trade recommendations.

## Inputs used throughout

| Input | Value | Tag | Note |
|---|---|---|---|
| Underlying | XYZ | — | Hypothetical ticker |
| Spot | $100.00 | `[ESTIMATED]` | Chosen so the body sits at the money |
| Expiry | one expiry for the fly legs | — | Legs of a fly share an expiry |
| `+1× 95C` (near wing K1) | $6.10 | `[ESTIMATED]` | |
| `−2× 100C` (body K2) | $3.05 | `[ESTIMATED]` | |
| `+1× 105C` (far wing K3) | $1.35 | `[ESTIMATED]` | |
| Contract multiplier | 100 | `[VERIFIED]` | Standard US listed equity-option multiplier |
| Width | $5.00 | `[COMPUTED]` | `105 − 100`, also `100 − 95` |

## Example A — the fly's basis and its maximum value

```text
  net debit      = 6.10 − 2 × 3.05 + 1.35
                 = 6.10 − 6.10 + 1.35
                 = 1.35 per fly .......... $135 per fly
  max value      = width = 5.00 .......... $500 per fly (spot at K2 at expiry)
  max loss       = net debit = 1.35 ...... $135 per fly
  scale-out line = 1.8 × 135 ............. $243 per fly
```

All four lines are `[COMPUTED]` from the `[ESTIMATED]` inputs above. The `1.8×` scale-out
multiplier is a data-backed desk threshold derived from data, not an exchange rule.

## Example B — fly → vertical downgrade

The package closes the far wing and buys back one body contract. The `105` wing leaves the
position, so the strikes that survive are `95` and `100` — the width is `100 − 95`, not `105 − 95`.

```text
  sell 1× 105C  → + 1.35 × 100 = +$135
  buy  1× 100C  → − 3.05 × 100 = −$305
  net package debit              = $170 per fly          [COMPUTED]

  resulting leg list: +1× 95C / −1× 100C                 (a debit call spread)
  vertical basis     = fly debit + package debit
                     = 135 + 170 = $305 per unit         [COMPUTED]
  vertical width     = (100 − 95) × 100 = $500 per unit   [COMPUTED]
  max value          = width, at spot ≥ 100 = $500        [COMPUTED]
  max profit         = 500 − 305 = $195 per unit          [COMPUTED]
  max loss (held)    = basis = 305 per unit = $305        [COMPUTED]
  break-even at expiry = 95 + 3.05 = $98.05               [COMPUTED]
```

Read the economics honestly: after the downgrade the position needs the underlying **above
$98.05** at expiry just to break even, and the surviving `95 / 100` spread caps out at
`100 − 95 = $5.00` = `$500` per unit of *value* `[COMPUTED]`. Against the `$305` `[COMPUTED]` of
basis already paid, the most it can return is `500 − 305 = $195` per unit `[COMPUTED]`, the same
`$195` the downgrade mechanics state for this strike set. That is a different trade from the fly,
which is the point of marking the basis.

## Example C — fly → long-only, priced while the bodies are still rich

```text
  buy  2× 100C  → − 2 × 3.05 × 100 = −$610
  sell 1× 105C  → + 1.35 × 100     = +$135
  net package debit                 = $475 per unit     [COMPUTED]
```

A `$475` `[COMPUTED]` debit to keep a `95C` worth `$610` `[ESTIMATED]` is a poor trade: you are
paying 78% of the runner's value `[COMPUTED]` to remove the bodies. The correct conclusion is
**do not convert yet**.

## Example D — the same conversion after decay

Bodies and wing have decayed with a few days left and the spot has drifted away from the body.

```text
  inputs (spot $96, DTE 3):
    100C ≈ $0.25  105C ≈ $0.05  95C ≈ $1.55 ............ [ESTIMATED]

  buy  2× 100C  → − 2 × 0.25 × 100 = −$50
  sell 1× 105C  → + 0.05 × 100     = +$5
  net package debit                 = $45 per unit      [COMPUTED]

  retained 95C value ≈ 1.55 × 100   = $155 per unit     [ESTIMATED]
  cost as a share of the runner     = 45 / 155 = 29%    [COMPUTED]
```

Now the conversion is cheap and defensible: the runner is bought free of its short siblings for
29% of its own value `[COMPUTED]`. This is the regime in which "house money" is a real description
rather than a feeling.

## Example E — the free-runner test (three units)

```text
  position: 3 flies, total debit = 3 × 135 = $405        [COMPUTED]

  close unit 1 at $455 ............................ [ESTIMATED fill]
  close unit 2 at $470 ............................ [ESTIMATED fill]
  realized to date                = $925                  [COMPUTED]
  convert the remaining 1 unit at $45 (Example D) ...... [COMPUTED]
  conversion cost = units_remaining × 45 = 1 × 45 = $45  [COMPUTED]
  net cash = 925 − 405 − 45 = +$475                       [COMPUTED]
  net cash ≥ 0  →  the surviving runner is FREE          [COMPUTED]

  counter-check, after only ONE close (2 units still open):
  conversion cost = units_remaining × 45 = 2 × 45 = $90  [COMPUTED]
  net cash = 455 − 405 − 90 = −$40                        [COMPUTED]
  → the runner was NOT yet free; converting there was
    an un-priced bet, not house money
```

The counter-check is the point of the example. The same operation is defensible after two
scale-outs and indefensible after one.

## Example F — spread → long-only

```text
  position: +1× 95C / −1× 100C, basis $305 per unit  .... from Example B
  buy back 1× 100C at $0.05  → − $5 per unit             [ESTIMATED input]

  resulting leg list: +1× 95C
  risk remaining = premium already paid, no assignment surface
  net cash change = −$5 per unit                         [COMPUTED]
```

This is the only single-leg close in the catalog that is always structurally safe, because the
leg being sold (the long) has no short sibling left to uncover. It still gets a ledger row.

## Example G — financed roll-up arithmetic

```text
  current fly: body 100, wings 95 / 105; spot has moved up to $103
    current mark of the fly = $2.80 per unit              [ESTIMATED]
  new fly one strike-set higher: body 105, wings 100 / 110
    open cost = $1.95 per unit                            [ESTIMATED]
  net debit = 1.95 − 2.80 = −0.85  → a CREDIT of $85      [COMPUTED]

  new body at 105 vs. spot 103 → the body sits above spot
  DTE remaining = 9  (≥ 5)  → gate passes
```

Both gates pass, so the roll-up is legal: it is financed by a credit rather than by new capital,
and the new body sits above spot with room. A roll-up that required a **debit** would have to be
funded out of realized proceeds, not out of new capital.

## Example H — condor defense arithmetic

```text
  iron condor: short 95P / long 90P  and  short 105C / long 110C
  credit collected at entry = $1.60 per unit = $160 per unit   [ESTIMATED input]

  threatened side gets breached; close the CALL side as one package:
    buy  1× 105C at $2.40   → −2.40 × 100 = −$240               [ESTIMATED input]
    sell 1× 110C at $0.30   → +0.30 × 100 = +$30                [ESTIMATED input]
    net debit = 240 − 30 = $210 per unit                        [COMPUTED]

  resulting leg list: short 95P / long 90P  (a defined put credit spread)
  surviving side max loss = width 5.00 × 100 − credit 160
                          = 500 − 160 = $340 per unit           [COMPUTED]
```

The surviving put vertical is defined-risk on its own. The operation removed the tested side
without touching the untested side, which is exactly what condor defense is supposed to do.

The `$210` `[COMPUTED]` debit is cash already spent to remove the call side; it is not part of
the `$340` `[COMPUTED]`, which describes only the survivor's own worst case. The two figures
answer different questions and are not added together into one "max loss".

## Example I — calendar roll cost cap

```text
  calendar (short front / long back), current mark = $2.20 per unit  [ESTIMATED]
  front leg DTE = 4  → roll window is open                     [COMPUTED]
  roll package (close front+back, open further front+back) costs
    net = $0.95 per unit                                      [ESTIMATED]

  cap = 50% of current mark = 0.50 × 2.20 = $1.10              [COMPUTED]
  0.95 ≤ 1.10  →  the roll clears the cap; proceed
  if the package had cost $1.25  →  1.25 > 1.10  →  close, do not roll
```

## How to re-derive these on your own book

1. Read the live leg list; do not reuse a mark older than the current session.
2. Recompute the fly debit from the **entry fills**, not from the mark.
3. Recompute every conversion package from **live quotes**, and record the mid at the moment of
   drafting so slippage can be measured after the fill.
4. Re-derive the surviving structure's basis from the **fill**, not the plan.
5. Store the close-the-whole-structure price at the same timestamp. Without it, none of the
   arithmetic above can be scored.

`[COMMON-PRACTICE]` Steps 1–5 are the desk's evidence convention; the arithmetic itself is
`[COMPUTED]` and independent of any vendor.

## Uncertainty and limits

- The `[ESTIMATED]` prices are illustrative and approximate. Real quotes on near-worthless legs
  are indicative, often stale by minutes, and are **not a guarantee** of a fill.
- `Past performance` of any conversion pattern does not predict its next result; the same
  arithmetic at different prices produces a different decision.
- Rounding: options prices quote in minimum increments that vary by price level and venue.
  Where a computed figure falls between increments, the fill — not the model — is the truth.
- The gate thresholds used above (`1.8×`, `≥ 30%`, `≤ ~50%`, `≤ 7 DTE`, `≤ 2 DTE`) are data-backed
  desk thresholds derived from data on this desk's study, not exchange rules. Re-derive them on
  your own book, and treat them as approximate at all times.
