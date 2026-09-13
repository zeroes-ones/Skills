# Ecosystem Economics

<!-- STANDARD: 3min -- incentives, platform risk, and the value exchange -->

## Why an economics file belongs in an architecture skill

A platform's technical design determines whether the ecosystem *can* exist. **Its incentive design
determines whether it does.** Third parties build where the value exchange works for them, and they stop
where it does not — regardless of how well-designed the API is.

## The value exchange

Every extension developer is asking an implicit question: *what do I get, and what do I give up?*

| They get | They give up |
|---|---|
| Access to your users | Their time, and often their money |
| A distribution channel | Control over their release schedule (your contract) |
| Capability they could not build alone | Their roadmap constrained by yours |
| Revenue, leads, or reputation | Their code running under your policy |

**The platform must make this exchange clearly favourable**, or the developer builds an integration
elsewhere — usually directly against an API, without your platform's constraints.

## What drives adoption

| Driver | Why it matters |
|---|---|
| **User demand** | developers go where the users are; this is the primary driver |
| **Time-to-first-value** | the first-hour budget (see `developer-experience.md`) |
| **Revenue or strategic benefit** | a clear commercial reason to invest |
| **Stability** | a platform that breaks integrations consumes the developer's budget |
| **Distribution** | being discoverable by users, not just buildable |
| **Support and responsiveness** | whether questions get answered |
| **Escape hatches** | whether they can leave without losing their users |

**The last one is underrated.** A platform that developers cannot leave is a platform they will not
enter, because the risk is asymmetric against them.

## Platform risk, and how it is perceived

Developers assess the risk of building on you. Each risk has a technical mitigation.

| Perceived risk | Technical mitigation |
|---|---|
| "You will compete with me" | a published boundary: what the platform will and will not build |
| "You will change the terms" | a stability contract with tiers and windows |
| "You will break my integration" | version negotiation, deprecation, rehearsed breaks |
| "You will take my users" | a fair revenue model, and a policy on platform-built replacements |
| "You will deprecate the whole platform" | a stated commitment period, and a wind-down plan |
| "I cannot get support" | a responsive channel, and an escalation path |

**Publishing what the platform will not build is the highest-value signal**, because it is the risk
developers cannot otherwise assess. A clear "we will build the core, you build the edges, here is the
line" converts a large uncertainty into a known boundary.

## The economics of different extension classes

| Class | Developer's incentive | Platform's cost |
|---|---|---|
| Theme/appearance | low effort, aesthetic control | low |
| Integration/connector | commercial (their service reaches your users) | moderate (contract stability) |
| Automation/scripting | personal productivity | low (capability-gated) |
| Content/data provider | reach | moderate |
| AI/LLM extension | access to their model or workflow | moderate-high (cost, safety) |
| Build/transform step | developer tooling value | high (isolation, performance) |

The pattern: **classes with a commercial incentive for the developer sustain themselves**, and classes
with only aesthetic or personal value need the platform to reduce cost further (a one-command scaffold,
no review, minimal contract).

## Revenue, if there is any

| Model | Effect on the ecosystem |
|---|---|
| Free, no revenue | fastest adoption; hardest to sustain good extensions |
| Paid, platform takes a cut | sustains quality; needs a fair rate and clear terms |
| Paid, platform takes none | sustains nothing on the platform's side; a subsidy |
| Bring-your-own monetisation | flexible; needs a policy to avoid abuse |

Whatever the model: **publish it, and do not change it without a window.** A revenue-term change is the
fastest way to lose a mature ecosystem.

## The platform-versus-partner boundary

The single most important non-technical commitment:

```text
We will build:   the core capability, the platform, the contract, the tooling
You will build:  the integrations, the verticals, the long tail
The line is:     <stated explicitly, and honoured>
```

**Honouring it is the point.** A platform that later builds a popular partner's extension destroys the
incentive for everyone, permanently — because every remaining developer now knows the boundary moves
against them.

## Ecosystem health metrics

| Metric | Signals |
|---|---|
| Active extensions (updated in the last N months) | whether the ecosystem is alive or decaying |
| New publishers per quarter | whether it is growing |
| Median time-to-first-working-extension | the DX budget, measured |
| Contract-break incidents per release | contract health |
| Support volume per extension | whether the platform is self-service |
| Extension abandonment rate | where the exchange is failing |
| Concentration (top N extensions' install share) | whether it is a market or a monoculture |

**The concentration metric is worth stating explicitly.** An ecosystem where three extensions hold 90% of
installs is a monoculture: it has the risks of a platform without the diversity that justifies one.

## Failure patterns

| Pattern | Mechanism | The technical fix is insufficient because |
|---|---|---|
| The ecosystem never forms | the first hour is too slow | it is a DX problem (see `developer-experience.md`) |
| It forms and then decays | incentives were never there | no revenue or reach for the developer |
| It becomes a monoculture | the boundary is unclear and one publisher dominates | needs a published boundary |
| It becomes a liability | no revocation or removal path | a lifecycle problem (see `lifecycle.md`) |
| It collapses on a break | no stability contract | a contract problem (see `stability-contract.md`) |

Each has a technical component and a non-technical one, and the non-technical one is usually why the
technical fix did not take.

## Checklist

- [ ] The value exchange is stated from the developer's perspective, not the platform's
- [ ] User demand is established (or the platform is built ahead of it, knowingly)
- [ ] The platform-versus-partner boundary is published, and honoured
- [ ] The revenue model, if any, is published with a change window
- [ ] An escape path exists: a developer can leave without losing their users
- [ ] Developer-perceived risks are addressed explicitly, especially "you will compete with me"
- [ ] Ecosystem health metrics are collected, including concentration
- [ ] The extension classes with only aesthetic/personal incentives have the lowest possible friction
- [ ] Support responsiveness is a stated commitment, not a hope
