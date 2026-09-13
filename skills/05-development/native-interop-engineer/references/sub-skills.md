# Sub-Skills

<!-- QUICK: 30s -- when to split into a narrower session -->

| Sub-skill | When to use it | Where it lives |
|---|---|---|
| `justification` | Whether to cross at all | `references/boundary-justification.md` — R6 |
| `binding-mechanism` | Which mechanism, and what it guarantees | `references/binding-mechanisms.md` |
| `abi` | What ABI to expose | `references/abi-choice.md` |
| `ownership` | Allocator, owner, freer, lifetime | `references/memory-ownership.md` — R1 |
| `marshalling` | Data shapes and their cost | `references/marshalling.md` — R2 |
| `strings` | Encoding, length, lifetime | `references/strings-and-encodings.md` |
| `errors` | How failures cross | `references/error-propagation.md` — R3 |
| `containment` | Catching panics and exceptions at the boundary | `references/panic-and-exception-containment.md` |
| `callbacks` | Re-entrancy and callback lifetime | `references/callbacks-and-reentrancy.md` — R4 |
| `threading` | Attachment, affinity, the guard | `references/threading-and-affinity.md` — R4 |
| `performance` | Per-crossing cost and crossing count | `references/performance-at-the-boundary.md` — R2 |

## Split when

- **One concern dominates.** "Our callback deadlocks" is `callbacks` plus `threading`; it does not need the
  marshalling or ABI review.
- **The boundary is being justified** — that is `justification` alone, and it may end the work.
- **A crash is being diagnosed** — start with `ownership` and `containment`, in that order.
- **A specific binding is being implemented** — `binding-mechanism` plus the language's own interop
  contracts.
- **The question is the linkage form or ABI versioning** — hand to `library-linkage-architect`.

## Stay whole when

- **A new boundary is being designed.** Justification, shape, ownership, errors, threading and cost are one
  contract; splitting them produces a boundary with an ABI and no ownership rules, or ownership rules with
  no error contract.
- **A boundary is being made safe after an incident.** The response spans ownership, containment and
  testing together; a partial fix leaves the class of defect in place.

## Adjacent skills, and the boundary

| Neighbour | They own | This skill owns |
|---|---|---|
| `library-linkage-architect` | The linkage form, ABI versioning policy, the unload reality | The crossing: ownership, marshalling, errors, threads |
| `plugin-ecosystem-architect` | The extension platform, capability model and lifecycle | Implementing the boundary that enforces them |
| `api-designer` | A network API contract as an alternative | Why a binary boundary may or may not beat a service |
| `performance-engineer` | End-to-end profiling and budgets | The boundary's share, measured per crossing |
| `appsec-engineer` | The memory-safety threat model | Implementing safe interop within that model |
| `debugging-and-error-recovery` | Systematic bisection of an unexplained failure | The boundary-specific failure modes to look for |
| `embedded-engineer` | Device-side constraints and toolchains | The interop to the target's platform APIs |
| `kotlin-multiplatform` | The shared/native boundary design | The platform interop implementations |

The pattern: `library-linkage-architect` decides *what the boundary is*; `plugin-ecosystem-architect`
decides *what it enforces*; this skill makes *the crossing itself* correct — memory, errors, threads and
cost.
