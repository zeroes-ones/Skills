# Safe Conversion Catalog — defined-risk leg surgery

This is the desk's catalogue of leg operations that change a structure's shape **without ever
creating an uncovered short**. Every entry states the exact package, the resulting leg list, the
gates that must pass, and the way the conversion loses money.

## Sign discipline (read this before the table)

Model a bull fly as `+1× K1 (near) / −2× K2 (body) / +1× K3 (far)`, where `+` is long and `−` is
short, and all three strikes share an expiry.

A conversion is written as a **package**: the exact set of closing and opening legs submitted as
one order at one net price. The package's arithmetic is only correct at the price it actually
fills — so the result column below is the *target* state, and the basis must be re-derived from
the fill before any take-profit level is trusted.

Three rules make the sign discipline mechanical:

1. **State the post-order leg list, not the pre-order legs.** The package is judged by the state
   it leaves.
2. **Never close a long that defines a short without closing that short in the same package.**
3. **A single-leg close is legal in exactly one shape:** the long leg of a two-leg spread whose
   short has already been bought back (see `Spread → long-only`).

## The catalog

| Conversion | Package legs (exact) | Resulting leg list | What it fixes | What it costs |
|---|---|---|---|---|
| **Fly → vertical** (downgrade, tag `VD`) | `{ sell 1× K3 + buy 1× K2 }` | `+1 K1 / −1 K2` — a debit call spread | Dead or illiquid far wing; IV-crush exposure on a tail you no longer believe in | Converts max-profit geometry from a point (K2) into a range (≥K2); the body now caps upside |
| **Fly → long-only** (house money, tag `HM`) | `{ buy 2× K2 + sell 1× K3 }`, keeping `+1 K1` | `+1 K1` only | Removes both short bodies; risk becomes the premium already paid | A net debit equal to `2 × K2_mid − 1 × K3_mid`, which is small only after the bodies decay |
| **Spread → long-only** | Buy back the short; keep the long | `+1` long leg | Removes the assignment/pin surface entirely | Keeps the full premium at risk; this is the ONLY single-leg close that is always structurally safe |
| **Financed roll-up** (fly, tag `RU`) | ONE package: close the current fly, open the same fly at higher strikes | Same shape, higher strikes | Re-centres the body over a spot that has moved up | A net debit that must be ≤ realized proceeds; the new body must sit above spot with room |
| **Condor defense** (tag `CD`) | Close the threatened side's two legs as ONE package | A defined vertical on the surviving side | Removes the side that is being tested without touching the side that is not | Gives up the credit that side had collected; optionally roll that side to a later expiry as a second, separate ticket |
| **Calendar roll** (tag `CR`) | Whole structure to a later expiry as ONE package | Same shape, later expiry | Removes front-leg pin and gamma risk while the thesis lives | A net cost subject to a cap of about 50% of the current mark |
| **Rung scale-out** (tag `SC`) | Close whole structure-units as one package each | Fewer units of the same shape | Banks profit without unbalancing anything | Reduces the position's remaining upside in whole-unit steps |

## Per-conversion gates

| Conversion | Must be true before submitting | Reject if |
|---|---|---|
| Fly → vertical | Far wing `≥ 30%` of structure value, OR DTE `≤ 7`, OR IV percentile `≥ 80` on a debit structure | The far wing is cheap and the body has room — downgrading there donates the tail for nothing |
| Fly → long-only | `2 × K2_mid − 1 × K3_mid` computed from live quotes; free-runner test applied (see `(references/house-money-conversion.md)`) | The conversion's net debit is not subtracted; "it looks cheap" is not a price |
| Spread → long-only | None beyond the standard pre-action protocol | Almost never — this conversion removes risk, it does not add it |
| Financed roll-up | Net debit ≤ realized proceeds from the same structure; new body above spot; DTE ≥ 5 | The roll is funded by a size increase, or the new body sits below spot |
| Condor defense | The threatened side's short is actually breached, not merely touched | Both sides are breached — then close the whole condor |
| Calendar roll | DTE ≤ 5 on the front leg; thesis intact; net cost ≤ ~50% of current mark | The net cost exceeds the cap — then close, do not roll |
| Rung scale-out | Unit count ≥ 2; the profit trigger actually fired | Unit count is 1 — close the whole structure or hold |

## The naked-state catalogue — what each conversion would look like if done wrong

| Wrong execution | State it leaves | Consequence |
|---|---|---|
| Close only the long wing `K1` | `−2 K2 / +1 K3` | Two short calls partially covered; the uncovered remainder is unlimited-risk |
| Close only the short bodies `−2 K2` (both) | `+1 K1 / +1 K3` | A long strangle — defined risk, but not the structure you think you hold |
| Close one of the two bodies | `+1 K1 / −1 K2 / +1 K3` | A broken fly: long the near wing and the far wing, short one body. Not a named shape and not covered by the original plan's rules |
| Sell the far wing `K3` alone | `+1 K1 / −2 K2` | Two naked short calls; the exact accident R1 exists to prevent |
| Buy back the short of a spread, then sell the long in a second ticket | Between the two fills the state is defined; if the order is reversed the long is gone first | Selling the long first leaves a naked short |
| Roll one side of a condor and then the other | Both sides replaced as separate tickets | Two spreads of slippage on a scare, and a structure with no thesis |

## The "one-ticket-or-nothing" test

Every row above is a **same-structure change**, which means R2 applies: one multi-leg order at a
single net price. The test is mechanical:

```text
  Does the operation change the leg set of ONE structure?
        │
        ├── YES ──▶ draft ONE complex order at a net price
        │              │
        │              ├── fills ──▶ done; log the fill
        │              └── rejected twice ──▶ split shorts-first ONLY if every
        │                                       intermediate state passes R1
        │
        └── NO (it creates a second, independent structure)
               └── it is not a conversion; it is a new position — route to the
                   structure-building skills
```

## What a completed conversion looks like

The output of any conversion in this catalog is four lines, in this order:

1. **Pre-state** — the leg list as it stands now, read from the position screen.
2. **Package** — the exact legs and sides submitted as one order at a net price.
3. **Post-state** — the resulting leg list, with the R1 test result written next to it.
4. **Money** — the net debit or credit in dollars per unit `[COMPUTED]` from named `[ESTIMATED]`
   inputs, and the surviving structure's re-derived basis.

If a conversion cannot produce all four lines, it is not ready to submit. `[COMMON-PRACTICE]`
This four-line shape is the desk's convention, not an exchange or regulatory requirement.

## Sources and provenance

- `[VERIFIED]` That a listed option is a separable, independently exercisable instrument, and
  that a multi-leg position is not a single instrument to the exchange: the OCC's standard
  options disclosure document, and US options exchange rules on exercise and assignment.
- `[VERIFIED]` That US options exchanges provide complex/package order types that execute at a
  single net price: CBOE and other US options exchange rulebooks. The exact order-type names and
  supported combinations are venue-specific; verify against the exchange whose market you route
  to.
- `[COMPUTED]` All arithmetic in this file is deterministic from stated inputs; worked numbers
  live in `(references/leg-arithmetic-worked-examples.md)`.
- `[ESTIMATED]` The gate thresholds (`≥ 30%` dead-wing test, `≤ ~50%` calendar-roll cost cap,
  `≤ 7` DTE downgrade window) are data-backed desk thresholds derived from data on this desk's
  own leg-op study. They are approximate, are not exchange rules, and are not a guarantee.
