# Compilation Profiles

<!-- STANDARD: 3min -- profile-guided pre-compilation and where each platform supports it -->

## The problem they solve

On runtimes that mix ahead-of-time compilation, just-in-time compilation and interpretation, code that
has not been pre-compiled must be verified and compiled *while the user waits* — which lands the cost
in Phase 3 (to-interactive) rather than Phase 1.

Android documents this hybrid directly: ART "uses ahead-of-time (AOT) compilation, and starting in
Android 7, it uses a hybrid combination of AOT compilation, just-in-time (JIT) compilation, and
interpretation, and the AOT compilation can be profile-guided." *(Source: Android, "Configure ART".)*

The consequence for launch: whether the code paths involved in start-up are pre-compiled changes
what the user experiences, without changing a line of the app.

## What a profile does

A profile is a set of hot code paths. Shipping one lets the runtime pre-compile those paths so they
are optimised on first run rather than during it.

Android's Baseline Profiles documentation states the mechanism and the benefit: by shipping a profile,
"Android Runtime (ART) can optimize specified code paths through Ahead-of-Time (AOT) compilation,
providing performance enhancements for every new user and every app update", and this "lets apps
optimize startup, reduce interaction jank, and improve overall runtime performance for users from the
first launch." *(Source: Android, "Baseline Profiles overview".)*

The documented use cases are exactly the launch-relevant ones: "app startup, navigating between
screens, or scrolling through content, making them smoother from the first time they run."

## Which platforms have an equivalent

| Platform | Mechanism | Notes |
|---|---|---|
| Android | Baseline Profiles, Startup Profiles | profile-guided AOT; installed by the profile installer on first run |
| Apple (iOS/macOS) | AOT compilation at build time; no runtime JIT for app code | the "profile" equivalent does not apply the same way — pre-main work is the lever |
| JVM (server/desktop) | AppCDS / class-data sharing, AOT caches | shifts class loading and verification out of start-up |
| .NET | ReadyToRun, composite R2R, AOT publishing | reduces JIT at start-up |
| V8/Node | code cache / snapshot (per runtime) | reduces parse and compile cost at start-up |
| Python | `.pyc` caching; import cost is the dominant term | see the serverless/CLI file |
| WASM runtimes | AOT-compiled modules where supported | avoids compile-at-instantiation |

**The pattern:** wherever a runtime can compile later, a profile or cache lets it compile earlier —
outside the user's critical path.

## Where the profile belongs in the fix order

```
Phase 3 dominates, and the cause is verification/JIT?
├── Confirm it: compare a first run to a subsequent run.
│   ├── First run slow, later runs fast → compilation cost is real
│   └── Both slow → it is not compilation; look elsewhere
└── Yes ↓
    Ship a profile covering the launch-critical and first-interaction paths.
    Then re-measure: TTFD should improve; TTID typically will not.
```

**TTID usually does not move.** A compilation profile addresses Phase 3. If TTID is the problem, the
profile is the wrong lever — which is why the attribution comes first (R3).

## Generating and maintaining one

```text
1. Identify the paths that matter: launch, first screen, the first action the user takes.
2. Generate a profile by exercising those paths on a representative build.
3. Ship it in the app, not as a separate download.
4. Verify it is actually installed and applied (the platform exposes this).
5. Re-generate when the launch-critical code changes materially.
6. Track it in the launch budget: a stale profile is a silent regression source.
```

**The maintenance trap:** a profile that is generated once and never refreshed slowly stops covering
the code that actually runs at start-up. It still ships, still looks configured, and no longer helps.
Treat it as a build artefact with a regeneration trigger, not a one-time addition.

## Verifying it worked

| Check | Method |
|---|---|
| The profile is present in the build | inspect the artefact, not the build script |
| The profile was installed | the platform exposes installation state; check it |
| The paths are covered | compare the profile's methods to the launch trace's methods |
| TTFD improved | re-measure with the identical method (R5) |
| TTID unaffected | confirm it did not regress; the profile should not change Phase 1 |

**What "it did not help" usually means:** the profile does not cover the paths that actually run, the
profile did not install, or the cost was never compilation in the first place. Diagnostic order:
confirm installation, then coverage, then re-check the attribution.

## When a profile is the wrong lever

| Situation | Why |
|---|---|
| Phase 1 dominates | a profile addresses compilation, not loader or initializer cost |
| Phase 2 dominates | it does not reduce layout or theme work |
| The runtime has no JIT | nothing to pre-compile |
| The cost is data, not code | sequencing is the fix, not compilation |
| The code paths are already trivial | there is nothing worth profiling |

## Checklist

- [ ] The runtime's compilation model is known (AOT, JIT, interpretation, or a mix)
- [ ] Compilation cost is confirmed by comparing a first run to a subsequent one
- [ ] A profile is shipped where the platform supports one and the paths matter
- [ ] The profile's installation is verified on a real build
- [ ] The profile's coverage is compared against the launch trace
- [ ] A regeneration trigger exists for launch-critical code changes
- [ ] TTFD is re-measured after shipping it, by the same method as the baseline
- [ ] TTID is confirmed unchanged (the profile should not affect Phase 1)
- [ ] The profile is tracked as a build artefact with an owner, not as a one-time task
