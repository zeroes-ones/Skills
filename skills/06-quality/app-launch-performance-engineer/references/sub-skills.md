# Sub-Skills

<!-- QUICK: 30s -- when to split into a narrower session -->

| Sub-skill | When to use it | Where it lives |
|---|---|---|
| `mode-triage` | Which launch mode is failing | `references/launch-modes.md` — Decision Tree 1, R1/R6 |
| `metrics` | TTID versus TTFD, and what each governs | `references/launch-metrics.md` — R2 |
| `attribution` | Where the time goes, by phase | `references/init-cost-attribution.md` — R3 |
| `pre-main` | Loader, relocations, framework init | `references/pre-main-cost.md` |
| `static-init` | Finding and removing initializers | `references/static-initializers.md` |
| `third-party-init` | Self-initialising dependencies | `references/third-party-init.md` |
| `profiles` | Profile-guided pre-compilation | `references/compilation-profiles.md` |
| `web` | Hydration and time-to-interactive | `references/web-hydration.md` |
| `serverless-cli` | Module-graph cold start | `references/serverless-and-cli.md` |
| `budget` | Budgets, gates and alerts | `references/launch-budgets.md` — R4 |
| `method` | Measuring repeatably and comparing honestly | `references/measurement-method.md` — R1/R5 |

## Split when

- **The complaint names a mode and you need the attribution** — that is `attribution`, and it is a
  bounded session.
- **One platform is in scope** — `serverless-cli` or `web` alone, without the mobile work.
- **The budget is the deliverable** — `budget` plus `method`, and stop there.
- **The linkage is the suspected cause** — hand the pre-main measurement to
  `library-linkage-architect`; do not decide the linkage here.
- **The problem is a first-use stutter, not launch** — route to `library-linkage-architect` (binding
  mode) and `performance-engineer`.

## Stay whole when

- **A launch complaint has no measurement yet.** Mode triage, method, baseline and attribution are one
  piece of work; doing them separately produces a number nobody trusts and an attribution nobody can
  check.
- **A launch budget is being established.** The budget, the gate and the method are interdependent —
  a budget on an unreliable measurement flaps and gets disabled.

## Adjacent skills, and the boundary

| Neighbour | They own | This skill owns |
|---|---|---|
| `library-linkage-architect` | The linkage form, library count and binding mode that set the floor | Measuring and attributing the cost that form creates |
| `performance-engineer` | Profiling method, load testing, broader performance budgets | Launch specifically, as a product-visible metric |
| `frontend-developer` | Bundle mechanics, code splitting, tree shaking | Hydration as a Phase 3 cost, and time-to-interactive |
| `firmware-developer` / `embedded-engineer` | ROM-to-app boot, bootloaders, early boot | Application launch, above the boot line |
| `mobile-architecture-patterns` | App structure and startup sequence | The measured cost of that structure |
| `observability-engineer` | Production metrics and alerting infrastructure | The launch metric definition and its budget |
| `shipping-and-launch` | Rollout, monitoring and go/no-go | The launch budget as an input to the go/no-go |
| `ci-cd-builder` | Pipeline construction | The launch benchmark the pipeline must run |

The pattern: neighbours own *what the app is* and *the instruments*; this skill owns *which launch is
slow, what it pays for, and whether it stays fixed*.
