# Launch Budgets

<!-- DEEP: 5+min -- budgets, per-mode thresholds, CI gates and production alerts -->

## Why a budget and not a target

A target is a number someone hopes for. A budget is a number that **fails something** when it is
exceeded. Launch cost only stays flat if exceeding it has a consequence, because every release adds a
little initialisation and almost nothing removes it.

This is R4: numeric, per mode, per device class, and wired to a gate that can fail.

## The published thresholds, where they exist

Start from the platform's own definition of excessive, where one is published. Android is the clearest
example: start-up is considered excessive at **cold ≥ 5 s, warm ≥ 2 s, hot ≥ 1.5 s**, measured as TTID.
*(Source: Android vitals launch-time guidance.)*

Those thresholds are useful for three things:

1. **A sanity floor** — if you exceed a vendor-published excessive threshold, that is unambiguous.
2. **Per-mode framing** — they are different per mode, which proves a single target is wrong.
3. **A citable source** — you can point at the platform's own documentation rather than your own
   opinion.

**But they are a floor, not a goal.** 4.9 s cold start is not good; it is merely not-yet-published-as-
excessive. Your budget should normally be far tighter, derived from your own baseline and your users.

## Deriving your own budget

```text
1. Measure the current median, cold, on the median device class (≥10 runs).
   → baseline
2. Set the budget at or slightly below what you can defend:
     budget = baseline            if launch is currently acceptable
     budget = baseline − target%  if you are improving
   → never set a budget you have not measured yourself capable of meeting
3. Set a p90 ceiling as well as a median.
   → the tail is what users complain about, and the median hides it
4. State the method with the budget. A budget without a method is not reproducible (R5).
```

| Budget component | Example |
|---|---|
| Mode | cold |
| Device class | median mid-tier, <named model class> |
| Metric | TTFD |
| Median budget | 1,800 ms |
| p90 ceiling | 2,600 ms |
| Method | 20 runs, process killed between runs, cache cleared |
| Baseline at adoption | 2,410 ms median, 3,380 ms p90 |
| Owner | <name> |

## The two gates, and why you need both

| Gate | Catches | Cannot catch |
|---|---|---|
| **CI benchmark** | causes, on the change that introduced them | device-specific behaviour, real-world variance |
| **Production metric** | what users actually experience | the cause — only the symptom |

```text
Change lands ──▶ CI benchmark ──▶ fails?  block the merge, or require a recorded budget increase
                                  passes? merge

Release ships ──▶ production metric ──▶ drifts? alert, and bisect the release
```

The CI gate attributes; the production gate detects what CI cannot see (a device class you do not test
on, a network condition, a platform update). Neither alone is sufficient.

## What to use for each

| Gate | Candidate mechanism |
|---|---|
| CI, Android | the platform's macrobenchmark tooling in a device farm |
| CI, Apple | an XCTest performance case on a representative simulator or device |
| CI, web | a Lighthouse-CI style budget on time to interactive |
| CI, serverless/CLI | wall-clock on N cold invocations in a controlled runner |
| Production, any | the platform's own start-up vitals (Android's are automatic), plus real-user monitoring |

**Prefer the metric the platform reports automatically** for production, because it requires no
instrumentation discipline in the app. Android reports TTID for every app; that makes it the right
production signal, with TTFD added by the app where it matters.

## The failure response

A gate is only real if exceeding it has a defined consequence:

```text
Gate failed →
├── Is the regression attributable and small?
│   ├── Yes, and justified → require a RECORDED budget increase with a reason
│   └── Yes, and not justified → fix it before merge
└── Is the regression large or unexplained?
    ├── Bisect the change (Decision Tree 4 in SKILL.md)
    └── Escalate if it cannot be attributed

NEVER: disable the gate to make a release.
NEVER: raise the budget silently.
```

The recorded-increase path matters: launch cost sometimes legitimately rises because a capability was
added. Making that explicit converts a silent drift into a decision with an owner.

## What makes a budget decay

| Decay mechanism | Defence |
|---|---|
| A dependency adds an initializer | the CI gate, plus an init inventory per dependency addition |
| A splash screen absorbs the cost | the splash check in Verification (R4) |
| The measurement becomes unreliable, so results are ignored | keep the method stable and documented |
| The gate is flaky, so it gets disabled | fix the flakiness; a disabled gate is worse than none |
| A new device class becomes the median | re-baseline periodically and state the class |
| Budget raised for a release and never lowered | require a re-review date on every increase |

## Budgeting on multiple platforms

Do not impose one number across platforms. The modes, the metrics and the achievable numbers differ.

| Surface | Realistic framing |
|---|---|
| Mobile cold | the tightest budget, because the median device is weakest |
| Desktop cold | often looser, but the tail matters (cold disk cache) |
| Web | time to interactive, not first paint |
| Serverless | per-invocation cold start, plus a p99 ceiling |
| CLI | per-invocation, and it is paid every time — the tightest relative budget |

## Reporting

```text
Launch budget — <surface> — adopted <date>

| Mode | Metric | Device class        | Median | p90    | Method                 | Owner |
|------|--------|---------------------|--------|--------|------------------------|-------|
| cold | TTFD   | median mid-tier     | 1,800  | 2,600  | 20 runs, killed, clear | <name>|
| cold | TTID   | median mid-tier     |   800  | 1,150  | 20 runs, killed, clear | <name>|
| warm | TTFD   | median mid-tier     | 1,100  | 1,600  | 20 runs, app backed out| <name>|

Baseline at adoption: cold TTFD 2,410 / 3,380.
Gate: CI benchmark fails the build; production alert on the platform vitals.
Increase policy: recorded reason + re-review date, never silent.
```

## Checklist

- [ ] The budget is numeric, per mode, per device class (R4)
- [ ] Both a median and a p90 ceiling are set
- [ ] The measurement method is stated alongside the number (R5)
- [ ] The platform's published excessive thresholds are known and cited, as a floor
- [ ] A CI gate can fail the build on a regression
- [ ] A production metric (preferably the platform's automatic one) alerts on drift
- [ ] The failure response is defined: fix, or record a justified increase
- [ ] Budget increases require a reason and a re-review date
- [ ] The gate is not disabled to ship a release
- [ ] Each surface has its own budget, not one number imposed across platforms
