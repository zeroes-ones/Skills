# Modular Monolith Architecture — The Pragmatic Middle Ground

> Original explainer for interview prep and learning. [research-source: title-only]

## What it is

A modular monolith is **one deployable application** whose internal structure is split into modules that mirror bounded contexts — each module owns its data, exposes a clear internal API, and cannot reach into another module's internals. It is a monolith in *operations* (one build, one deploy) and modular in *code* (enforced boundaries).

## Why it exists

Monoliths are simple to operate but can turn into a ball of mud. Microservices fix coupling but add distributed-systems cost (network, consistency, ops, debugging). The modular monolith captures most of the *code-quality* benefit of microservices (enforced boundaries, ownership, testability) while keeping the *operational* simplicity of one deployable. It is the correct default for most teams; extract services later when a boundary genuinely needs independent scaling/deploys.

## How to build one (the rules that make it work)

1. **Modules = bounded contexts.** One module per business capability (e.g., `orders`, `catalog`, `billing`, `identity`). Follow DDD seams, not technical layers.
2. **Modules own their data.** No module reads another's tables directly — only through the owning module's API. (Shared DB tables silently undo modularity.)
3. **Enforce boundaries mechanically.** Package/compile-time rules: no cross-module imports of internals; public API surface only. Architecture tests fail the build on violations.
4. **Internal APIs are real contracts.** Treat module boundaries like service boundaries: versioned, tested, and changed through the owning module.
5. **Async for the hard couplings.** If two modules need to react to each other, use an in-process event bus (or a real queue when you need durability/scale); avoid deep synchronous call chains between modules.
6. **One deployable, many seams.** Because boundaries exist, extracting a module into a service later is a mechanical step, not a rewrite.

## When to stay monolith (link to full analysis)
See `when-monolith-wins.md` in this repo for the decision table (team < 20, DB CPU < 50%, single stack, low deploy cadence → monolith). The modular monolith is how you keep that simplicity *without* forgoing clean boundaries.

## Modular monolith vs microservices (interview table)

| Axis | Modular monolith | Microservices |
|---|---|---|
| Deploy | One unit | Per-service |
| Coupling control | Code-level rules | Network + contracts |
| Consistency | Local transactions possible | Sagas/outbox (eventual) |
| Independent scaling | Whole app | Per service |
| Failure isolation | Process-level (one crash = all) | Per service (with circuit breakers) |
| Team autonomy | Shared repo, code rules | Independent repos/teams |
| Ops complexity | Low | High |
| Right for | Most products, early scale | Genuine team/scale drivers |

## Anti-patterns

- ❌ **Layered monolith in disguise:** modules split by layer (`controllers`, `services`, `repos`) instead of bounded contexts — that's still a ball of mud with folders.
- ❌ **Shared everything:** a shared `models`/`db` package that every module imports recreates the coupling you were avoiding.
- ❌ **Soft boundaries:** "we'll just be disciplined" without compile-time enforcement — discipline decays; tests enforce.
- ❌ **Premature extraction:** splitting into services before a concrete driver (independent deploys/scaling) — you pay distributed cost for no benefit.

## Interview answer skeleton

"A modular monolith is one deployable with hard, enforced module boundaries aligned to bounded contexts; each module owns its data and exposes a real API. It gives most of microservices' maintainability with monolith simplicity, and it makes later extraction mechanical. I'd start there and split a module into a service only when it needs independent scaling or deploy cadence."

## Deliberate-practice drills

1. **Boundary drill:** take a monolith feature set and draw bounded contexts + module APIs; identify one illegal cross-module reach you'd forbid first.
2. **Enforcement drill:** write the architecture-test rules that would fail a build on cross-module access.
3. **Extraction drill:** pick one module and write the 5-step plan to extract it into a service (API first, data move, strangler, cutover, rollback).
4. **Comparison drill:** for a 40-engineer, 200K-DAU product, argue monolith vs modular-monolith vs microservices with concrete drivers.
5. **Interview drill:** "your CTO says 'we need microservices for scale' — respond." Use drivers + modular monolith as the default.

## References
- `when-monolith-wins.md` (this repo) — the full monolith decision analysis
- microservices-patterns.md, system-design-101.md (this repo)
- `codebase-design` SKILL.md — module/package design and shallow-module checks
- `domain-modeling` SKILL.md — bounded contexts and domain seams
