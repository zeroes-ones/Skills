# Condor Defense Playbook

An iron condor is two credit verticals sharing a range thesis. When one side is tested, the
defense is not "some adjustment" — it is a specific, narrow operation: **close the threatened
side's two legs as ONE package**, leaving a defined vertical on the other side.

## Touched versus breached

The first decision is classification, and it is the one most often skipped. A scare and a break
look identical on a 1-minute chart and are completely different events.

| Test | Touched (hold) | Breached (defend) |
|---|---|---|
| RTH close relative to the threatened short strike | No close beyond it | A session close beyond it |
| Number of tests | The level is being tested and holding | The level gave way; the strike is now ITM |
| Volume / breadth at the level | No expansion | Expansion with the move |
| Distance from spot to the short | Inside roughly 1σ of the remaining horizon | Outside ~1σ, or moving away steadily |
| Time to expiry | Enough left for the range thesis to be re-tested | Little left; the range is settled |
| Event calendar | Nothing inside the remaining life | An event inside the remaining life that supports the direction |

`[COMMON-PRACTICE]` The desk rule of thumb is: **a touch is not a break, and a close is.** The
thresholds for "inside ~1σ" and "enough left" are data-backed desk thresholds derived from data
on this desk's own study, are approximate, and must be re-derived on your own book.

## The defense operation, exactly

Worked on a one-unit condor with shorts at 95P / 105C and longs at 90P / 110C:

```text
  threatened side = the CALL side (spot has moved up through 105)

  package: { buy 1x 105C ; sell 1x 110C }        ONE order, one net price
  resulting leg list: -1 x 95P / +1 x 90P        (a defined put credit vertical)

  arithmetic, from 2.40 paid on the short and 0.30 received on the long:
     buy  1x 105C  →  -2.40 x 100 = -$240
     sell 1x 110C  →  +0.30 x 100 = +$30
     net debit = $210 per unit                    [COMPUTED] from [ESTIMATED] inputs
  surviving side max loss = width 5.00 x 100 - credit 160 = $340 per unit   [COMPUTED]
```

Two properties of this operation matter more than the arithmetic:

1. **The surviving side is untouched.** Its credit, its risk and its own take-profit rung remain
   exactly as they were.
2. **The resulting state is defined-risk on its own.** A put credit vertical has a bounded loss
   with no reference to the closed side.

## Never roll both sides on a scare

Rolling both sides replaces the whole condor with a new one at a cost of two spreads of slippage
plus two new strikes to defend. Three separate arguments against it:

| Argument | Detail |
|---|---|
| It is more expensive than the problem | Two sides of slippage on four legs, paid to convert one tested side into two untested ones |
| It destroys the thesis record | The original range thesis was falsified by the break; re-selling two new strikes is a **new position** and needs its own thesis, invalidation and expectancy |
| It doubles the assignment surface | Two fresh shorts, both unseasoned, both with a full event window ahead |

If both sides are genuinely breached — a real range break, not a scare — the correct operation is
the opposite one: **close the whole condor as a single package**. That is a stop, not a defense.

## One side or the whole thing: the decision

```text
   one side tested
        │
        ├── RTH close beyond that side's short strike?
        │        ├── NO  ──▶ TOUCH. Hold; re-check next session. Do not pay
        │        │            two spreads for a wiggle
        │        └── YES ──▶ continue
        │
        ├── is the OTHER side also beyond its short strike?
        │        ├── YES ──▶ both sides breached ──▶ close the WHOLE condor,
        │        │             one package. This is a stop
        │        └── NO  ──▶ close the threatened side's TWO legs as ONE package
        │                      │
        │                      └── optional second ticket: reopen THAT side at a
        │                          later expiry. This creates a calendar-style side
        │                          and is a NEW decision with its own ledger row
        │
        └── can the surviving side's credit be monetized instead?
                 └── if its value has already collapsed, consider closing the
                     survivor too and taking the combined credit as the trade's
                     whole result
```

The optional second ticket — reopening the defended side further out — is where discipline
usually leaks. It is legal, it is a new position, and it must have: a new thesis, a new
invalidation, a new expectancy, its own ledger row, and a strike placed beyond the level that
must break to hurt you. Reopening "at the same strikes but later" on a broken range is a chase.

## Take-profit discipline on the side that survives

After the defense, the surviving side becomes a standalone credit vertical with its own rules.

| Item | What to set |
|---|---|
| Take-profit rung | The desk's convention is to close a credit vertical at about 50% of max credit, taken in whole units |
| Stop line | A session close beyond its short strike plus a small buffer |
| Time stop | Close before the last few DTE rather than defending it again |
| Assignment guard | It is still a short leg; the pin guard at ≤ 2 DTE applies unchanged |
| Ledger | The defense row carries tag `CD`; the survivor's rung updates are part of the same structure's plan |

## Anti-patterns specific to condor defense

| ❌ | Why it is wrong | ✅ |
|---|---|---|
| ❌ Rolling both sides on a scare | Pays two spreads to replace a structure whose range thesis was never falsified | ✅ Hold on a touch; defend one side on a close |
| ❌ Closing the threatened side's short leg alone | Leaves the long leg as a standalone long with no purpose and an unfunded cost basis | ✅ Close the side's two legs as one package |
| ❌ Closing the whole condor's threatened side and re-selling the SAME strikes at a later expiry without a new thesis | That is a fresh position described as a defense | ✅ Write the new thesis, invalidation and expectancy first, or close |
| ❌ Defending the side that is merely under pressure while the actually-breached side is left alone | Misclassification; the breached side is the one carrying the risk | ✅ Classify with the touched/breached table before choosing a side |
| ❌ Defending by buying a far OTM "insurance" leg while keeping the breached short at the same strike | This is a conversion into a different structure and must be designed as one — a new leg is a construction, not a defense | ✅ Either close the side, or design the resulting shape explicitly and re-run the R1 test |
| ❌ Calling a defended structure "the same trade" in the ledger | The credit, the strikes, the risk and the thesis all changed | ✅ The defense row is its own row with tag `CD` |

## Interaction with other skills

| Situation | Where it belongs |
|---|---|
| Deciding whether to enter the condor at all | `options-strategist` / `advanced-options-structures` |
| Building the condor as two verticals, staged at each level test | `staged-structure-formation` — the owner's hand-installed desk skill, **outside the shipped library**, so it may be absent. Where installed, it owns staged formation and per-side entry. If it is not: open each side through `options-strategist` as ONE complete defined-risk package, log both against one umbrella ledger with a row per ticket, count heat once for the idea, and accept that a lone vertical is already a complete trade — never sell the second side "somewhere" to finish the shape |
| Defending, closing, or rolling a formed condor's side | This skill |
| Portfolio-level limits that make a defense unaffordable | `options-risk-engineer` |
| Automating the defense trigger | `options-automation-engineer` |

## Sources, provenance and limits

- `[VERIFIED]` A short option that is not covered by a long at a protective strike carries
  unbounded (call) or strike-to-zero (put) risk, and a listed option is separately exercisable —
  OCC standard options disclosure document; US options exchange rules on exercise and assignment.
- `[VERIFIED]` US options exchanges provide complex/package order types at a single net price,
  which is what makes "close the side's two legs as one package" a realizable instruction — CBOE
  and other US options exchange rulebooks.
- `[COMPUTED]` The defense arithmetic above is derived from the stated inputs; the worked form is
  in `(references/leg-arithmetic-worked-examples.md)`, Example H.
- `[ESTIMATED]` The touched-versus-breached thresholds (an RTH close as the deciding event,
  "inside roughly 1σ", the 50% take-profit convention) are data-backed desk thresholds derived
  from data on this desk's study. They are approximate, are not exchange rules, and are not a
  guarantee.
- `[COMMON-PRACTICE]` "Never roll both sides on a scare" is a desk rule with an economic reason
  (two spreads of slippage for no thesis change), not a regulatory requirement.
- Past performance of this defense does not predict its next result.
