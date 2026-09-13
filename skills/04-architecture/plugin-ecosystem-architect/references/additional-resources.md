# Additional Resources — plugin-ecosystem-architect

> Deep knowledge loaded on demand. `SKILL.md` stays lean; extended material lives here and in the
> sibling reference files.

## Reference file map

| File | Covers |
|---|---|
| `platform-decision.md` | When a platform is warranted, the cost gradient, and when a module boundary or configuration surface is enough |
| `extension-points.md` | Abstractions versus internals, the extension-point test, and the stability tiers |
| `stability-contract.md` | Tiers, the deprecation sequence, the mismatch matrix, degradation and shims |
| `capability-model.md` | Capabilities, the enforcement chokepoint, default deny, consent moments, and anti-patterns |
| `isolation.md` | The five isolation options, structural sandbox enforcement, resource limits and hostile testing |
| `lifecycle.md` | The seven states, replace mechanisms, capability expansion, rollback, revocation and data handling |
| `distribution-and-trust.md` | Publishing models, signing and verification, scanning, the review question, and revocation |
| `version-negotiation.md` | The declaration, the full mismatch matrix, refusal messages, degradation and the version matrix test |
| `developer-experience.md` | The first-hour budget, the eight DX deliverables, structured errors, and DX metrics |
| `ecosystem-economics.md` | The value exchange, adoption drivers, platform risk, the platform-versus-partner boundary, health metrics |
| `anti-patterns.md` | Fifteen platform anti-patterns with detection heuristics and a sweep script |
| `error-decoder.md` | Fifteen symptoms in long form: mechanism, diagnosis, fix, recurrence guard |
| `sub-skills.md` | When to split the session, and the boundary with adjacent skills |

## Extended example

`examples/backtest/README.md` runs an extension-platform remediation against a stated scenario, with the
arithmetic shown and every figure provenance-tagged.

## Source material

Platform rules on third-party code, store review and sandbox capabilities change between releases and
differ by product category. Confirm the current version before relying on a rule.

| Source | What it governs |
|---|---|
| Platform distribution and store policy documentation (per channel, current version) | Whether third-party code may be loaded, bundling, signing, review and update rules |
| webassembly.org use-cases documentation | Sandboxed runtimes for untrusted code and portable distribution |
| Sandbox/runtime capability documentation (per runtime, current version) | The import-as-capability model, limits, and marshalling behaviour |
| `dlopen(3)` and platform loader documentation | Load, symbol scope and unload behaviour at a native extension boundary |
| Platform permission-model documentation (browsers, mobile OSes, container runtimes) | Precedents for capability naming and consent UX |
| `api-designer` versioning conventions | Reused for extension-contract versioning and deprecation windows |

## Verification harness

`scripts/verify-skill.sh` asserts this skill's own invariants: that all six ground rules are present with
enforcement columns, that the capability model requires an enforcement chokepoint (not just a
declaration), that isolation is a named mechanism per class, that the lifecycle includes disable,
rollback and removal, that version negotiation defines every mismatch outcome, and that developer
experience is a deliverable rather than a follow-up. Run it before relying on the skill's output.
