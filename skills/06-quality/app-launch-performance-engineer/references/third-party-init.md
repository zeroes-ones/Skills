# Third-Party Initialisation

<!-- STANDARD: 3min -- auto-registration hooks, content providers, and the dependency-init inventory -->

## The problem in one sentence

**Dependencies initialise themselves, which puts their cost on your critical path without your
deciding it** — and that unowned cost is usually a larger share of pre-main time than anything you
wrote.

## The mechanisms, by platform

| Mechanism | Platform | Runs |
|---|---|---|
| Content providers declared in the manifest | Android | before the app's own `onCreate` |
| Auto-configuration / auto-registration | framework-specific (Java, .NET, Spring-like) | at start-up |
| `+load` and linker-added constructors | Apple | before `main` |
| Module-level side effects | Python, Node, Ruby | at import of the module |
| Class initialisers on first reference | JVM | at first touch of the class |
| Static registration macros | C/C++ | at load or first use |

**The Android case is the most documented and the most commonly hit.** Android's App Startup library
exists specifically so that "instead of defining separate content providers for each component you
need to initialize, App Startup allows you to define component initializers that share a single
content provider. This can significantly improve app startup time." Its guidance then states: "If you
previously used content providers to initialize components in your app, make sure that you remove
those content providers when you use App Startup." *(Source: Android, App Startup library.)*

The second sentence is the important one. Consolidating without removing leaves the old providers in
place, and the saving does not materialise — a failure mode where the fix was applied and the number
did not move.

## Building the inventory

The goal is a list of **everything that initialises itself**, with its measured cost. Not what you
wrote — what runs.

```text
1. Enumerate, per platform:
     Android    → declared providers (manifest merges from AARs are the hidden ones)
     Apple      → linked libraries with +load / constructors
     JVM        → auto-configuration entries and class-initialiser side effects
     Python/JS  → module-scope code in imported modules
     Any        → the actual loaded library set

2. For each, determine whether it is needed at start-up at all.
3. Measure each by ablation (remove/defer, re-measure, restore, re-check the control).
4. Sort by measured cost, descending.
5. Decide per item: remove, defer, consolidate, or accept.
```

**Step 1 is where the surprises are.** On Android, a dependency's provider arrives through the
manifest merge and is invisible in your own manifest source. On Apple platforms, a linked library's
`+load` runs without appearing anywhere in your code. Neither is visible in a code review.

## Measuring an initialiser's cost

Ablation is the reliable method, and it needs a control:

```text
For each candidate:
  control      = cold start, median device, ≥10 runs, median recorded
  remove/defer = exactly one initialiser
  measured     = cold start, identical method
  delta        = measured − control
  restore      = re-measure the control to confirm no device drift
```

**Why the control re-measurement matters:** devices warm up, background load varies, and thermal state
changes. Without re-checking the control, a device that got 40 ms faster during your test will be
credited to whatever you removed.

## The decision per initialiser

```text
Is it needed before the first frame?
├── No  → DEFER past TTID. Measure Phase 3 afterwards to confirm the cost moved, not grew.
└── Yes ↓
    Is it needed at all?
    ├── No  → REMOVE the dependency. The cheapest initialiser is the one you do not link.
    └── Yes ↓
        Are there several components each initialising themselves?
        ├── Yes → CONSOLIDATE into one ordered path (and remove the old hooks)
        └── No  → ACCEPT, and record its measured cost so a future addition is comparable
    Finally:
    └── Is a third-party initialiser doing I/O or reading the environment?
        ├── Yes → treat it as a HAZARD, not just a cost: it can fail in some environments
        └── No  → it is a cost item; the decision above stands
```

## The consolidation pattern

```text
Before:                          After:
  Provider A (SDK 1)               One initialisation path, ordered by the app:
  Provider B (SDK 2)                 init_1()  ← SDK 1, first because …
  Provider C (SDK 3)                 init_2()  ← SDK 3, depends on 1
  App onCreate                        init_3()  ← SDK 2, independent
                                   App onCreate (nothing left to do)
```

Three requirements for the consolidation to actually pay:

1. **Remove the replaced hooks.** The old providers must go, or the cost stays.
2. **Order explicitly.** You now own the ordering, which is better than inheriting the linker's.
3. **Verify by measurement.** Confirm the total fell; do not assume the consolidation worked.

## What to do about a dependency you cannot change

| Situation | Approach |
|---|---|
| Initialises itself, needed, no config to defer | Accept, record the cost, and re-check on each upgrade |
| Initialises itself, not needed at start-up | Find the API to defer it, or wrap and lazy-load it |
| Initialises itself and does I/O | Treat as a hazard; test with a minimal environment |
| Cannot be deferred and is large | Consider whether the capability justifies its launch cost, or whether a lighter alternative exists |
| Vendored/forked and fixable | Patch it and record the divergence — but own the maintenance |

## Reporting

```text
Third-party init inventory — <app> — <date>

| Component       | Mechanism      | Needed at start? | Measured cost | Decision        |
|-----------------|----------------|------------------|---------------|-----------------|
| SDK A           | manifest provider | yes            | 180 ms        | consolidate     |
| SDK B           | manifest provider | no             | 120 ms        | defer past TTID |
| SDK C           | static init    | no               |  45 ms        | remove          |
| SDK D           | static init    | yes              |  30 ms        | accept          |
| (unattributed)  | —              | —                | 240 ms        | stated residual |
                                          -----------
sum of measured                                   375 ms + residual

Method: cold, <device class>, cache cleared, 20 runs, median.
```

The table is the deliverable: it converts "the framework is slow" into a list with owners and costs.

## Checklist

- [ ] Every self-initialising dependency is enumerated per platform, including manifest-merge cases
- [ ] Each one's cost is measured by ablation with a control re-measurement
- [ ] The inventory is sorted by measured cost, not by suspicion
- [ ] Replaced hooks are removed when a consolidation is applied
- [ ] Deferred work is verified to have moved cost out of the total, not into Phase 3
- [ ] Initialisers doing I/O are treated as hazards and tested with a minimal environment
- [ ] Unchangeable dependencies have a recorded cost, re-checked on upgrade
- [ ] The inventory is recorded with its measurement method (R5)
