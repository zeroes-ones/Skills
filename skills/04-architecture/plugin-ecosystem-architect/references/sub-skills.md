# Sub-Skills

<!-- QUICK: 30s -- when to split into a narrower session -->

| Sub-skill | When to use it | Where it lives |
|---|---|---|
| `platform-decision` | Whether a platform is warranted at all | `references/platform-decision.md` — Decision Tree 1 |
| `extension-points` | What to expose, and at what abstraction | `references/extension-points.md` — R1 |
| `stability-contract` | Tiers, deprecation, and what is promised | `references/stability-contract.md` — R2 |
| `capability-model` | Capabilities, the chokepoint, default deny | `references/capability-model.md` — R3 |
| `isolation` | In-process, sandboxed, or separate process | `references/isolation.md` — R5 |
| `lifecycle` | Install, disable, rollback, revoke, remove | `references/lifecycle.md` — R4 |
| `distribution` | Publishing, signing, verification, revocation | `references/distribution-and-trust.md` |
| `version-negotiation` | The declaration and every mismatch outcome | `references/version-negotiation.md` |
| `developer-experience` | Onboarding, local dev, testing, publishing | `references/developer-experience.md` — R6 |
| `ecosystem-economics` | Incentives, platform risk, the value exchange | `references/ecosystem-economics.md` |

## Split when

- **One decision dominates.** "Should we build a plugin system?" is `platform-decision` alone.
- **The capability model is the task** — `capability-model` plus `isolation`, and it is bounded.
- **An incident is live** — `lifecycle` (revoke) first, then the root cause.
- **The platform already exists and is failing** — start with the specific failure: contract breaks →
  `stability-contract`; unenforced capabilities → `capability-model`; no removal → `lifecycle`.
- **The question is the binary ABI mechanics** — hand to `library-linkage-architect`.

## Stay whole when

- **A platform is being designed from the start.** The boundary, capabilities, isolation, lifecycle,
  contract and DX are one design; splitting them produces a platform with a capability model and no
  removal path, or an isolation decision with no contract.
- **The platform has failed publicly.** The response spans contract, communication, remediation and DX
  together — a partial response usually addresses the symptom.

## Adjacent skills, and the boundary

| Neighbour | They own | This skill owns |
|---|---|---|
| `library-linkage-architect` | The binary ABI shape, linkage, unload reality | The contract, capability model and lifecycle the ABI serves |
| `api-designer` / `secure-api-design` | Network API contracts and their auth | The extension contract and its capability enforcement |
| `system-architect` | Core decomposition and boundaries | Where extension points can sit in that decomposition |
| `appsec-engineer` | The threat model for third-party code | Bounding what third-party code can do |
| `native-interop-engineer` | Cross-language marshalling at the boundary | The contract that boundary enforces |
| `ai-engineer` | The AI/LLM surface inside an extension | The extension platform it runs on |
| `automation-engineer` | Building one integration | The platform an integration targets |
| `developer-relations-advocate` | Growing and supporting the developer community | The DX deliverables that make growth possible |
| `shipping-and-launch` | Rollout and go/no-go | Ecosystem readiness as a launch input |
| `product-manager` | Ecosystem strategy and business terms | The technical contract and the trust model |

The pattern: neighbours own *the API, the core, or the community*; this skill owns *the boundary between
the platform and everything built on it* — the contract, the capability, the lifecycle, and the trust.
