# Sub-Skills

<!-- QUICK: 30s -- when to split into a narrower session -->

| Sub-skill | When to use it | Where it lives |
|---|---|---|
| `linkage-form` | Choosing the form for a reusable unit | `references/linkage-forms.md`, `references/static-vs-dynamic.md` — Decision Tree 1 |
| `abi-policy` | Declaring the surface and the breaking-change rules | `references/abi-stability.md` — Decision Tree 2, R3 |
| `symbol-surface` | Export control and collision triage | `references/symbol-visibility.md` — R5 |
| `binding-mode` | Eager versus lazy, and where each belongs | `references/binding-modes.md` |
| `runtime-loading` | Designing a load site, the unload question, failure states | `references/runtime-loading.md` — Decision Tree 3, R4 |
| `update-model` | Remediation path, exposure window, rehearsal | `references/update-model.md` — Decision Tree 4, R2 |
| `plugin-contract` | The ABI shape at an extension point | `references/plugin-abi.md` |
| `process-safety` | `fork`, load order, initialisation ordering | `references/process-safety.md` |
| `platform-rules` | What a channel permits to be shipped and loaded | `references/platform-constraints.md` — R6 |

## Split when

- **One decision dominates.** "Should this be a shared library?" is `linkage-form`; it does not need
  the plugin ABI or the process-safety pass.
- **The task is an ABI declaration for an existing library** — that is `abi-policy` plus
  `symbol-surface`, and it is bounded.
- **A single platform rule is the blocker** — resolve the constraint (`platform-rules`), then return.
- **The question is really about launch cost** — hand the measurement to
  `app-launch-performance-engineer`; this skill decides the linkage that sets the floor.
- **The question is really about build time or build graphs** — that is `build-system-design`.

## Stay whole when

- **A new reusable library is being designed.** Form, ABI, visibility, versioning and the update model
  are one coherent decision; splitting them produces a library with a form but no contract, or a
  contract with no remediation path.
- **A plugin ecosystem is being introduced.** The ABI, the load lifecycle, the unload decision and the
  platform rule are interdependent — and the platform rule may remove the whole design.
- **A critical dependency's remediation path is being established.** That spans linkage, packaging,
  rehearsal and ownership, and it needs to be done as one piece of work with one owner.

## Adjacent skills, and the boundary

| Neighbour | They own | This skill owns |
|---|---|---|
| `build-system-design` | Build speed, system selection, caching, remote execution | What is produced and how it links |
| `dependency-governance` | Version policy, CVE triage across repos, licence compliance | The linkage of a chosen dependency, and its remediation path |
| `system-architect` | Service decomposition, topology, C4/ADRs | The linkage of the units inside those services |
| `codebase-design` | Module seams, interface depth, deletion tests | The binary boundary behind a module boundary |
| `api-designer` / `secure-api-design` | Network API contracts and their security | Binary ABI and loaded-surface exposure |
| `performance-engineer` | Profiling, budgets, load testing | Size and load cost as an input to the budget |
| `app-launch-performance-engineer` | Launch measurement and init-cost attribution | The linkage choice that sets the launch floor |
| `plugin-ecosystem-architect` | The extension platform: capabilities, lifecycle, marketplace | The ABI contract that platform relies on |
| `native-interop-engineer` | Marshalling, ownership and error propagation across languages | The linkage form the interop boundary uses |

The pattern: the neighbours own *process and system shape*; this skill owns *what the binary boundary
is* — the form, the contract, and the cost of changing it later.
