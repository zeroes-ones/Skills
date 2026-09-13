# Platform Constraints

<!-- STANDARD: 3min -- what each distribution channel permits to be shipped and loaded -->

> **Verification note.** These are *categories* of constraint, not current rule text. Distribution
> and store policies change between releases and differ by product category and region. Confirm the
> current policy for the specific channel and product before relying on it (R6), and mark a recalled
> rule ESTIMATED rather than stating it as current.

## Why this is a ground rule

A linkage form the platform forbids is not an option, regardless of its engineering merits. Teams
that choose a form on technical grounds and discover the restriction late pay for it with a
redesign — often after the architecture is built around it.

## The constraint categories

| Category | The question it raises | What it removes |
|---|---|---|
| **Runtime code loading** | may the app load code that did not ship with it? | runtime loading, plugin ecosystems, hot updates |
| **Bundled runtimes/binaries** | may you ship a runtime or third-party binaries? | bundling a VM, a runtime, or a vendored library |
| **Private/undocumented API use** | may the app call non-public interfaces? | certain integrations and shortcuts |
| **Code signing and entitlements** | does every loaded unit need to be signed and entitled? | unsigned or dynamically generated code |
| **Static analysis and review** | is the shipped artefact inspected for specific constructs? | obfuscation, dynamic generation, private symbols |
| **Licence and content policy** | does the channel restrict what may be included? | some dependencies entirely (see `dependency-governance`) |
| **Sandboxing** | what may the process access at runtime? | filesystem/network patterns a sidecar or plugin needs |
| **Update mechanism** | may the app update itself outside the store? | self-updating binaries; forced review cycles |
| **Architecture and packaging** | which architectures and bundle shapes are accepted? | unusual packaging, fat binaries in some contexts |

## The constraints that most often change a decision

### Runtime code loading

Where a channel forbids loading code that did not ship with the app, an entire category of design
becomes unavailable:

| Design | Status under such a policy |
|---|---|
| A native plugin that a user installs | usually not permitted |
| Interpreted scripts fetched at runtime | usually not permitted |
| A configuration-driven rules engine with shipped code | permitted — the code shipped |
| Server-driven UI (the layout is data, not code) | permitted |
| A self-updating binary outside the store | usually not permitted |

**The architectural consequence:** if the channel forbids dynamic code, the plugin ecosystem must be
*sandboxed and shipped* (for example a WASM or interpreter host in the box, running content that is
data rather than native code) — or the product must not have plugins. That is a design decision the
channel forces, and it belongs in the linkage record.

### Bundled binaries and runtimes

Channels that inspect the shipped artefact may object to bundled binaries or runtimes. That removes:

- vendoring a library the platform already supplies;
- bundling an interpreter or VM;
- shipping a vendored crypto implementation where the platform has an approved one;
- fat/universal binaries in some contexts.

**The counterexample worth noting:** some environments *require* static, self-contained binaries
(minimal containers, appliance images, rescue tools). So the same choice can be forbidden in one
channel and required in another — which is exactly why R6 asks per target.

### Signing and entitlements

Where every loaded unit must be signed, runtime loading is not removed but becomes constrained: a
plugin must itself be signed and entitled. That converts the plugin ecosystem into a
*signed-extension* model, and adds a distribution problem (how does a third-party plugin get signed
and delivered?).

**Design consequence:** a marketplace for plugins in such an environment needs a signing pipeline and
a review process. That is a product decision surfaced by a platform rule.

## The decision procedure

```text
For each shipping target:
  1. Which channel(s) is this artefact delivered through?
  2. Does the channel permit loading code that did not ship? (runtime loading)
  3. Does it permit bundled runtimes and third-party binaries?
  4. Must every loaded unit be signed and entitled?
  5. Does it inspect the artefact, and for what?
  6. Are there licence/content restrictions on included dependencies?
  7. What sandbox limits apply at runtime?
  8. How may the product be updated, and with what review?
  9. Record each answer with its source and date.
Then: any form that a required channel forbids is removed from the option set,
      and the remaining choice is made from what is actually permitted (R6).
```

## Recording it

Per target, in the linkage decision record:

| Field | Example |
|---|---|
| Target | mobile app, primary store |
| Runtime loading | not permitted for newly-fetched native code |
| Implication | plugins must be sandboxed content in a shipped host, or absent |
| Bundled runtime | permitted, subject to review of the artefact |
| Signing | every loaded unit must be signed |
| Sandbox limits | no arbitrary filesystem writes outside the app container |
| Update path | store review; no self-update |
| Source, date checked | channel policy documentation, checked 2026-09 |

The `implication` field is the one that matters — it converts a policy sentence into a design
constraint someone can act on.

## What to do when the policy is unclear

| Situation | Approach |
|---|---|
| The policy text is ambiguous for this product category | ask the channel; do not interpret optimistically |
| The policy is not available in the target region | state the uncertainty; choose the more restrictive form |
| The policy changed recently | re-verify; recorded rules go stale |
| A grey area is central to the design | escalate; a design that depends on an interpretation is a risk |
| A different target permits what this one forbids | that is a per-target divergence in the linkage record, not an inconsistency |

**Fallback principle:** when the rule cannot be confirmed, choose the form that is permitted under
the *most restrictive plausible* reading, and record that you did so. A conservative choice costs
some efficiency; a wrong one costs a redesign.

## Checklist

- [ ] Each shipping target's channel is named, with the policy source and the date checked
- [ ] Runtime-loading permission is confirmed per target, not assumed
- [ ] Bundled-runtime and third-party-binary rules are confirmed per target
- [ ] Signing and entitlement requirements for loaded units are confirmed
- [ ] Any artefact inspection is understood, and the build complies
- [ ] Licence and content restrictions on dependencies are confirmed (with `dependency-governance`)
- [ ] Sandbox limits are known, and nothing in the design depends on exceeding them
- [ ] The update path is confirmed, including whether self-update is permitted
- [ ] Each constraint's *design implication* is written into the linkage record (R6)
- [ ] Any unconfirmed rule is marked unconfirmed rather than assumed
