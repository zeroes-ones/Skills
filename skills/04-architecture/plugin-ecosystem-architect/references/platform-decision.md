# Platform Decision

<!-- STANDARD: 3min -- when a platform is warranted, and when a module boundary is enough -->

## The question to answer first

Most "we need a plugin system" requests are really "we need our own code to be modular". Those are
different problems with very different costs, and confusing them produces an extension platform that
nobody extends.

```
Who will write the extensions?
├── Only our own team                       → INTERNAL MODULE BOUNDARY (not a platform)
├── Named partners under contract           → LIMITED PLATFORM
├── Anyone, publicly                        → PUBLIC PLATFORM
└── End users writing their own automation   → SCRIPTING SURFACE (a variant; see isolation.md)
```

## The three answers, and what each costs

| Answer | What it is | Cost | Reversibility |
|---|---|---|---|
| **Internal module boundary** | Your code, your repo, your release | Low | High — refactor freely |
| **Limited platform** | Partners build against a contract | Medium — capability model, version negotiation, support | Low once partners ship |
| **Public platform** | Anyone builds and distributes | High — plus review, signing, revocation, abuse response, DX | Very low — the ecosystem is a commitment |

**The cost gradient is the point.** Each step adds an obligation that outlives the decision: a public
platform is a product with external customers whose work must not break, and with a trust boundary you
must defend.

## When a module boundary is the right answer

| Situation | Why not a platform |
|---|---|
| The "extensions" ship with the host | There is no version skew and no trust boundary |
| Only your team writes them | The contract can be refactored with the code |
| There is no distribution story | An extension nobody can install is not an ecosystem |
| The value is configurability, not capability | Configuration is data; use a schema, not a plugin API |
| You cannot support external developers | An unsupported platform produces abandoned integrations |

**The configuration-versus-extension distinction matters.** If the requirement is "let users change
behaviour within our defined capabilities", that is configuration with a schema — cheaper, safer, and
versionable. If the requirement is "let users add capabilities we did not define", that is a platform.

## When a platform is warranted

| Situation | Why |
|---|---|
| Domain experts need workflows you cannot anticipate | The capability space is genuinely open |
| Partners integrate their own services | The integration is their business, not yours |
| Users want to automate your product with theirs | The value is in the connection |
| A marketplace is the business model | The ecosystem is the product |
| You cannot build every integration | The long tail is the value |

The common thread: **the capability space is open, and the parties are external.** If either is false,
a module boundary (or configuration) is cheaper and better.

## The obligations a public platform creates

Accepting a public platform means accepting all of these, permanently:

| Obligation | Consequence of skipping it |
|---|---|
| A stability contract | Integrations break on your releases |
| A capability model, enforced | Third-party code gains your authority |
| An isolation decision | A partner's defect becomes your outage |
| Distribution and signing | A compromised update is indistinguishable from a good one |
| A revocation path | You cannot remediate third-party harm |
| Developer experience | The ecosystem does not form |
| Support and documentation | Integrations are abandoned |
| An abuse response process | The first malicious extension has no remedy |

**The honest read:** a public platform is roughly a second product. If the organisation is not prepared
to operate it, a limited platform or a configuration surface delivers most of the value at a fraction
of the commitment.

## The decisions that get harder later

These are the ones that make the decision effectively irreversible:

| Decision | Why it hardens |
|---|---|
| What the extension points expose | Built on by third parties; changing it breaks them |
| The capability names and semantics | Persisted in manifests; renaming breaks installed extensions |
| The manifest format | Every extension carries one |
| The distribution channel | Publishers have signed and listed there |
| The stability promise | Publicly stated; breaking it is a trust event |

**Design implication:** decide these before publishing anything. After the first third-party extension
ships, each becomes a migration.

## A cheap way to learn

If the platform is uncertain, the sequence that limits risk:

```text
1. Internal module boundary        — refactor freely, learn the seams
2. Configuration schema            — let users change behaviour within defined capabilities
3. Experimental extension surface  — an EXPERIMENTAL tier, no compatibility promise
4. Limited platform                — named partners, controlled distribution
5. Public platform                 — only once 1–4 have shown the demand and the seams
```

Each step is reversible. Step 5 is not.

## The decision, recorded

| Field | Example |
|---|---|
| Audience | named partners (12 today) |
| Kind | limited platform |
| Why not public | no review or abuse-response capacity yet |
| Extension points | 3, all abstractions; 2 stable, 1 experimental |
| Trust model | partner-signed, host-verified; capabilities enforced |
| Reversibility | points are stable; adding is easy, removing is a migration |
| Revisit trigger | if partner count exceeds ~50, or self-serve demand appears |

The `revisit trigger` is what turns this from a decision into a plan.

## Checklist

- [ ] The extension audience is named, not assumed
- [ ] The question "is this a platform or a module boundary?" has been answered explicitly
- [ ] If configuration suffices, a schema is used instead of an extension API
- [ ] If a platform is chosen, all eight public-platform obligations are accepted or consciously declined
- [ ] The decisions that harden (points, capability names, manifest, channel, promise) are settled before publishing
- [ ] A revisit trigger is recorded
- [ ] The decision is written down where the next team will find it
