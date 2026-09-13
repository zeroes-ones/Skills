# Additional Resources — app-launch-performance-engineer

> Deep knowledge loaded on demand. `SKILL.md` stays lean; extended material lives here and in the
> sibling reference files.

## Reference file map

| File | Covers |
|---|---|
| `launch-modes.md` | The cold/warm/hot taxonomy, what each pays for, and how to measure each correctly |
| `launch-metrics.md` | TTID versus TTFD, what each governs, how to capture both, and how to define "fully interactive" |
| `init-cost-attribution.md` | The three-phase model, attribution methods, ablation discipline, and the residual |
| `pre-main-cost.md` | Loader work, relocations, static initializers, framework init, and the third-party problem |
| `static-initializers.md` | Finding them, removing them, ordering hazards, and verifying the removal |
| `third-party-init.md` | Self-initialising dependencies per platform, and the consolidation pattern |
| `compilation-profiles.md` | Profile-guided pre-compilation, platform equivalents, and profile maintenance |
| `web-hydration.md` | Hydration as the web's Phase 3, time-to-interactive, and the boundary with frontend-developer |
| `serverless-and-cli.md` | Module-graph cold start, `-X importtime`, cumulative versus self time, and the lazy-init pattern |
| `launch-budgets.md` | Numeric budgets per mode, the two gates, the failure response, and decay mechanisms |
| `measurement-method.md` | Controlling conditions, median/p90, the noise floor, and reproducible comparison |
| `anti-patterns.md` | Fifteen launch anti-patterns with detection heuristics and a sweep script |
| `error-decoder.md` | Thirteen symptoms in long form: mechanism, diagnosis, fix, recurrence guard |
| `sub-skills.md` | When to split the session, and the boundary with adjacent skills |

## Extended example

`examples/backtest/README.md` runs a launch remediation against a stated scenario, with the arithmetic
shown and every figure provenance-tagged.

## Source material

Launch mechanisms and thresholds change between OS, runtime and toolchain releases. Confirm the current
version before citing a threshold.

| Source | What it governs |
|---|---|
| Android, "App startup time" (launch-time documentation) | The three launch states; TTID and TTFD definitions; the excessive start-up thresholds (cold ≥ 5 s, warm ≥ 2 s, hot ≥ 1.5 s) |
| Android, "Configure ART" | The hybrid AOT/JIT/interpretation model and profile-guided AOT |
| Android, "Baseline Profiles overview" | Profile-guided pre-compilation, its mechanism and its launch benefit |
| Android, App Startup library documentation | The content-provider consolidation pattern and the requirement to remove replaced providers |
| Apple, "Overview of Dynamic Libraries" (archived developer documentation) | `dyld` loading the app's dependent libraries before the app runs |
| Python documentation, command-line options | `-X importtime` for per-module cumulative and self import time |
| Chrome/Lighthouse Time to Interactive guidance; Web Vitals documentation | The web's interactivity metric and its measurement |
| Platform profiler documentation (per platform, current version) | Phase traces, launch instruments and macrobenchmark tooling |

## Verification harness

`scripts/verify-skill.sh` asserts this skill's own invariants: that all six ground rules are present
with enforcement columns, that the three launch modes and the two metrics are kept distinct, that
attribution is required before any cause is claimed, that the budget is numeric and gated, that the
splash-screen-as-fix anti-pattern is caught, and that the measurement method is a required part of any
figure. Run it before relying on the skill's output.
