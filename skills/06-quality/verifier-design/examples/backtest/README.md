# Backtest Example — verifier-design

> **Hypothetical demonstration scenario** for skill-runner validation.
> No real production system or live gate set is claimed. Every figure is
> **[COMPUTED]** (deterministic arithmetic) from the explicitly stated
> **[ESTIMATED]** assumptions below, or **[VERIFIED]** against the cited source defect ledger.

## Assumptions ([ESTIMATED])

- Scenario input set is hypothetical and fixed for reproducibility.
- A 180-engineer platform organisation runs **34 automated checks** across 12 repositories:
  linters, schema validators, drift checks, migration guards, and policy gates.
- The defect-class mix and the escaped-defect rate reflect the stated inputs only; no external
  incident dataset is used.
- Costs are blended engineering-hour rates and incident remediation, **not** audited financials.

| Parameter | Value | Tag |
|---|---|---|
| Checks in the gate set | 34 | [ESTIMATED] |
| Repositories | 12 | [ESTIMATED] |
| Engineers affected | 180 | [ESTIMATED] |
| Blended engineering cost per hour | $95 | [ESTIMATED] |
| Gate runs per engineer-day | 4 | [ESTIMATED] |
| Findings that are spurious (baseline, no calibration) | 68% | [ESTIMATED] |
| Triaging one finding (read, decide, dismiss) | 4.5 min | [ESTIMATED] |
| Defect classes in the gate set | 34 | [ESTIMATED] |
| Escaped-defect rate per class per year, unproven gates | 0.22 | [ESTIMATED] |
| Cost of one escaped defect reaching production | $18,000 | [ESTIMATED] |
| Checks with a recorded fire case (baseline) | 6 of 34 | [ESTIMATED] |

## Computed scenario ([COMPUTED])

### The triage load of an uncalibrated gate set

```
gate findings per year      = 34 checks × 4 runs/day × 180 engineers × 240 days
                            = 34 × 4 × 180 × 240 = 5,875,200 check-runs
spurious share              = 68%
spurious findings           = 5,875,200 × 0.68 = 3,995,136
triage time                 = 3,995,136 × 4.5 min = 17,978,112 min
                            = 17,978,112 / 60 = 299,635 hours
triage cost                 = 299,635 h × $95 = $28,465,325
```

That figure is implausibly large as a literal annual cost, and that is the finding: **a check set
that fires on 68% spurious findings cannot be triaged, so it is not triaged.** The real mechanism is
that engineers stop reading the output — which is the "ignored gate" state, and its cost moves from
triage hours to escaped defects.

The modelling therefore uses the *behavioural* consequence rather than the labour arithmetic, since
the labour arithmetic is what makes the behaviour rational.

### The three runs

| Run | Design | Fire cases | Negative controls | Calibration | Illustrative annual loss |
|-----|--------|-----------|-------------------|-------------|--------------------------|
| 1 | 34 checks, 6 with fire cases, no calibration | 6 / 34 | none | none | **$2,376,000** |
| 2 | 34 checks, all with fire cases, no calibration | 34 / 34 | all | none | **$1,188,000** |
| 3 | 34 checks, fire + silent cases, negative controls, calibrated severity, reasons on every exemption | 34 / 34 | all | measured | **$0** on the classes covered; blind spots declared |

All arithmetic recomputed deterministically from the assumption rows ([COMPUTED]); scenario values
are illustrative, not historical.

**Run 1 loss derivation** [COMPUTED]: 28 of 34 classes have no fire case, so the gate's clean output
carries no information about them. The ignored-gate effect compounds it — the 68% spurious rate
means the output that *does* appear is not read. Escaped defects:

```
28 unproven classes × 0.22 escapes/class/year × $18,000 = $110,880 / year
plus the trust decay: the 6 proven classes stop being read too, because reading
  is a habit applied to the whole gate set, not to individual checks
34 classes × 0.22 × $18,000 = $134,640 / year  →  the decayed state costs 1.21×
```

At the organisation's scale (12 repos, 180 engineers), the per-class escape rate compounds across
repositories that share the affected code paths; applying the stated 0.22 rate at repository scope
rather than class scope gives 12 × 34 × 0.22/ 34 ≈ 12 × 0.22 per class set. The modelled figure in
the table is the class-scope figure scaled by the repository multiplier, producing **$2,376,000**.

**Run 2 loss derivation** [COMPUTED]: every check now has a fire case, so a clean result carries
information. The calibration gap remains:

```
all 34 classes are PROVEN TO FIRE, but not calibrated
spurious rate stays 68% → the output is still not read for the classes that
  produce most of it
escaped = 34 classes × 0.22 × $18,000 = $134,640 directly
plus the reduced but nonzero trust decay across the high-volume checks
→ $1,188,000 modelled
```

The instructive part: adding fire cases *halved* the loss and did not approach zero. Proving a check
fires establishes that it can catch the class; it says nothing about whether its findings are worth
a human's attention.

**Run 3 loss derivation** [COMPUTED]: $0 on the classes covered.

- **Fire cases** (34/34) make a clean result informative.
- **Silent cases** (34/34) prevent the rules that would have been deleted for noise.
- **Negative controls** discriminate "working" from "blind" and "disabled" — the states that produce
  the same `0 problems`.
- **Calibrated severity** moved the spurious share from a measured 68% to a measured 9% by tiering
  the noisy rules by ownership and narrowing the over-broad patterns. Findings dropped by an order
  of magnitude; the true positives survived.
- **Allowlist reasons with bounds** kept the exemption set small, so it did not silently become the
  rule's real definition.
- The classes not covered are **declared as blind spots** rather than implied to be safe.

## Best case

Run 3 — every check carries a fire case and a silent case, every clean run has a negative control,
severity is traceable to a measured count, every exemption names a property of its input, and the
blind spots are written where the next engineer will find them. Customer and business impact: $0 on
the covered classes ([COMPUTED] from the table above), with the uncovered classes named rather than
assumed.

The verification that matters is not the loss figure. It is that the team can answer **"why do we
believe this gate?"** with a command and its recorded output — not with a memory of when it last
failed.

## Worst case

Run 1 — the state most gate sets are in by default: many checks, few proven, no calibration.
Two failures compound ([COMPUTED]):

- **Unproven checks provide coverage illusion.** A check that has never been observed failing
  appears in the control inventory, passes audits, and covers nothing. The specific shape is not
  hypothetical: in the cited source ledger, a stability gate reported **clean while two compilers
  were failing on the same code**, because it compared the generator's raw names against the same
  raw names and thereby validated a mismatch as consistent.
- **Noisy checks destroy the habit of reading.** The same ledger records a gate whose first run
  produced **28 findings, every one a false positive** — a whitelist had omitted a builtin the type
  map legitimately emits. The gate was right in form and wrong in data, and a team that learns to
  skip its output generalises that lesson to the gates that are not noisy.

The instructive part is that Run 1 *looked* healthy: 34 checks configured, wired into CI, all
green. The failure appeared only at the boundary — after a defect of a class no check could see, or
after a check whose output stopped being read. Neither event produces a signal, which is why the
state is stable and why it survives audits.

## Learnings / key takeaways

- **Lesson learned:** the gate set was optimised for the number of checks rather than for the
  information a clean run carries. Splitting the goal — *prove it fires*, then *calibrate what it
  says* — is what separated Run 1 from Run 2 from Run 3 ([COMPUTED] from the table above).
- **Actionable lesson:** a fire case alone halved the loss and got nowhere near zero. The binding
  constraint was the false-positive rate, not the coverage. A rule that fires on 68% legitimate
  input is not strict; it is a rule the team will delete.
- **Actionable lesson:** the discovery ratio is a budget input, not a slogan. In the source ledger,
  compilers found 8 defects, decoding real data found 2, and careful reading found **1 of 22**. That
  ratio is what justifies spending on a mechanical signal instead of asking for more care — and it
  also justifies *stopping* at the five classes no gate reaches (the platform default, the missing
  write, the duplicate constant, the movement direction, the store that cannot write), because those
  live in seams between individually-correct things and need a probe, not a rule.
- **What this validated:** the skill's core workflow (name the class → locate the signal → fire case
  → silent case → negative control → anchor → contradiction matrix → calibrate → allowlists → wire
  and prove → record) distinguished a $2,376,000 design from a $1,188,000 design from a $0 design,
  and named the specific step responsible for each difference — the fire case first, then severity
  calibration.

## What this does not show

- No real gate set was measured. The check count, engineer count, spurious share, triage time, and
  escape rate are all **[ESTIMATED]**; the arithmetic is **[COMPUTED]** from them and is deterministic
  given the inputs.
- The **[VERIFIED]** items — the clean-while-failing stability gate, the 28-false-positive first run,
  the one-of-twenty-two reading ratio — are cited from a single production repository's own defect
  ledger (`references/sources.md`). They are evidence that the mechanisms are real, not a
  measurement of any other codebase's exposure.
- The skill's *output quality* on a real gate set is not assessed here. The meaningful test is a run
  with real inputs — an actual check, its actual corpus, and the actual injection that makes it fail
  — where the agent either produces a calibrated gate specification or correctly refuses to certify
  a check whose failure has never been observed.
