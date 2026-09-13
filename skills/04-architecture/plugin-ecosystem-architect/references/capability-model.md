# Capability Model

<!-- DEEP: 5+min -- capabilities, the enforcement chokepoint, and default-deny design -->

## The governing rule

**A capability that is declared but not enforced is not a control.** It is worse than no model at all,
because it creates the appearance of a boundary that does not exist.

This is R3, and it is the most consequential rule in the skill: unenforced capabilities are how a
third-party extension ends up exfiltrating user data while the platform's documentation says it cannot.

## The capability model, in four parts

| Part | Question | Example |
|---|---|---|
| **Capability** | What an extension may do | `content.read`, `network.outbound`, `user.email` |
| **Enforcement point** | Where the decision is made | a host service every privileged operation routes through |
| **Default posture** | What happens without a grant | deny |
| **Consent** | Who grants it, and when | the user, at install and on expansion |

All four are required. A model with capabilities and consent but no enforcement point is documentation.

## Default deny, and why it must be the default

```text
Default deny:
  Extension requests [content.read]
  → host grants content.read
  → any call to network.outbound FAILS in the enforcement point
  → the extension cannot reach the network, even by accident or by dependency
```

The alternative — default allow with documented restrictions — means an extension's *transitive
dependencies* also have the authority, which the requesting developer did not choose and cannot audit.
That is a supply-chain problem in the extension ecosystem, and default deny is what prevents it.

## The enforcement chokepoint

**One place that decides, or the model is decoration.** The chokepoint is the host service through
which every privileged operation passes.

```text
  Extension code
       │
       ▼
  ┌─────────────────────────┐
  │  CAPABILITY CHECK       │  ← the chokepoint. Everything privileged goes through here.
  │  does this extension    │
  │  hold this capability?  │
  └─────────────────────────┘
       │ granted        │ denied
       ▼                ▼
  host operation    typed refusal (not a silent no-op)
```

**Three properties of a correct chokepoint:**

1. **Unavoidable.** No path reaches the privileged operation except through it. If the extension can
   call the underlying primitive directly — a raw filesystem handle, a raw socket, an unrestricted
   host pointer — the chokepoint is bypassable and the model is void.
2. **Denying loudly.** A denied operation returns a typed error the extension can handle and the user
   can be told about. A silent no-op produces mysterious behaviour instead of a diagnosable gap.
3. **Auditable.** The chokepoint logs grants and denials, so abuse is detectable and support has data.

**Property 1 is where in-process models fail.** If extensions run in-process with host memory access,
they can usually reach the primitive regardless of the API you published, which is exactly why isolation
and the capability model are the same decision (see `isolation.md`).

## Designing the capability set

Capabilities should be:

| Property | Why |
|---|---|
| **Coarse enough to be meaningful** | `filesystem.all` is honest; 400 fine-grained permissions are unusable |
| **Fine enough to be defensible to a user** | "read your documents" is consentable; "do anything" is not |
| **Named by intent, not mechanism** | `content.read`, not `db.select` |
| **Stable identifiers** | persisted in manifests, so renaming is a migration (see `platform-decision.md`) |
| **Independently grantable** | one capability per meaningful choice |

### A workable starter set

| Capability | Grants | Consent framing |
|---|---|---|
| `content.read` | read the user's content | "see your content" |
| `content.write` | modify content | "change your content" |
| `content.delete` | delete content | "delete your content" |
| `network.outbound` | make outbound requests | "connect to the internet" |
| `user.identity` | the user's identity | "see who you are" |
| `user.email` | the user's email address | "see your email address" |
| `settings.read` / `settings.write` | read or change settings | "see / change your settings" |
| `events.subscribe` | observe host events | "see when things happen" |
| `notifications.send` | notify the user | "send you notifications" |
| `compute.long` | run long work | "run background work" |

**Note the absence of a filesystem capability from the starter set.** A public extension ecosystem
rarely needs raw filesystem access; it needs `content.*` and `network.*`. Exposing the filesystem is
usually a sign that the extension points were not abstracted (see `extension-points.md`).

## Consent, at the right moments

| Moment | What the user must see |
|---|---|
| **Install** | the full capability list, in their language, before they commit |
| **Expansion** | a new grant requested by an update, shown as a change — never silently granted |
| **Use** | optionally, a contextual prompt for a high-impact capability |
| **Audit** | a place to see and revoke what was granted |

**The expansion case is the one that breaks trust.** An update that adds a capability and gets it
granted silently is indistinguishable from an attack, from the user's point of view. Require
re-consent for expansion, and treat a decline as "the extension keeps its old grants".

## Capability anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Declared but unenforced | false assurance; the actual control is absent (R3) |
| Default allow | transitive dependencies inherit authority nobody chose |
| One omnibus capability (`all`) | destroys consent: the user must accept everything or nothing |
| Over-granular capabilities | unusable in a manifest and unintelligible in consent |
| Silent denial | the extension appears broken; the gap is undiagnosable |
| Grant-once, forever | a capability granted for a feature the user later removed is still held |
| Capability named by mechanism | binds the model to the host's internals |
| No audit surface | the user cannot see or revoke, which is the whole point of consent |

## Enforcing in each isolation model

| Isolation | How enforcement is guaranteed |
|---|---|
| Separate process | the process simply lacks the resources; capabilities are IPC surface access |
| Sandboxed runtime (e.g. WASM) | capabilities are the runtime's imports — absent unless granted by construction |
| Embedded interpreter | the host exposes only the capability-gated API surface; no primitives reachable |
| In-process native | only enforceable if no primitive is reachable — verify, do not assume (R5) |

**The sandboxed-runtime row is the strongest**, because enforcement is *structural*: the extension's
imports are literally the capability set, so a capability that was not granted does not exist as a
callable function. That is why sandboxing and capability models are usually chosen together.

## Verifying enforcement

Enforcement must be tested, not asserted:

```text
1. Build a test extension that DOES NOT request capability X.
2. Have it attempt the operation X would permit.
3. Confirm it fails with a typed refusal at the chokepoint.
4. Confirm the operation is impossible by any other route (no primitive reached).
5. Repeat for every capability in the set.
6. Repeat for the transitive-dependency case: does a dependency inherit the grant?
```

Step 4 is the one that distinguishes a real chokepoint from a documented one. Step 6 is the one that
catches default-allow leaks.

## Checklist

- [ ] Every capability has a stable identifier, named by intent
- [ ] There is exactly one enforcement chokepoint for privileged operations
- [ ] The posture is default deny
- [ ] A denied operation returns a typed, diagnosable refusal
- [ ] Grants and denials are logged for audit
- [ ] No privileged primitive is reachable other than through the chokepoint (verified, not assumed)
- [ ] Transitive dependencies do not inherit authority
- [ ] The user sees the capability list at install, and re-consents on expansion
- [ ] An audit surface exists where grants can be reviewed and revoked
- [ ] Enforcement is verified per capability by a test extension that lacks it (R3)
