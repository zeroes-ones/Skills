# Version Negotiation

<!-- STANDARD: 3min -- the declaration, the supported range, and mismatch behaviour -->

## Why negotiation is required

The host and its extensions release on **different schedules, controlled by different people**. The host
must therefore decide what to do with every combination of versions that can meet, and every outcome
must be defined rather than discovered.

This is R2's enforceable half: the tier table is the promise, and negotiation is how the promise is
honoured at runtime.

## The declaration

Every extension declares what it targets. Minimum viable set:

| Field | Purpose | Without it |
|---|---|---|
| `id` | identity, for diagnostics and revocation | an unidentifiable extension is undiagnosable |
| `version` | the extension's own version, for support | you cannot tell which build a user has |
| `targets.hostApi` | the contract range it was built against | the host cannot validate it |
| `capabilities` | what it requests | the capability model has nothing to enforce |

```json
{
  "id": "com.example.my-extension",
  "version": "2.1.0",
  "targets": { "hostApi": ">=3.0 <4.0" },
  "capabilities": ["content.read", "network.outbound"]
}
```

**The range form matters.** A single version is brittle — it refuses everything except an exact match,
including compatible releases. A range expresses what the extension actually needs.

## The mismatch matrix

| Case | Outcome | Rationale |
|---|---|---|
| Host version ∈ extension's range | **LOAD** | the normal case |
| Extension range entirely below the host's minimum | **REFUSE** with actionable message | it targets a contract that no longer exists |
| Extension range entirely above the host's maximum | **REFUSE** | the host predates the contract it needs |
| Ranges overlap but neither contains the other | **LOAD** at the top of the overlap, record the assumption | the overlap is the negotiated contract |
| Host supports the range, but a requested capability is deprecated | **LOAD + WARN** | it works now; it will not soon |
| A requested capability is unavailable | **LOAD DEGRADED**, or REFUSE — decide and state which | partial function may still be useful |
| Extension declares no range | **REFUSE** (or load as EXPERIMENTAL-only) | the host cannot know what was assumed |
| Host API is EXPERIMENTAL and the extension targets it | **LOAD**, with the experimental status surfaced | the extension opted in |

**Every row must have a defined outcome in the implementation, not just in this document.** The failure
R2 prevents is a mismatch that resolves silently to *something*.

## Refusal must be actionable

```
❌ "Incompatible extension"
❌ "Extension failed to load"

✅ "My Extension requires host API 2.x.
    This version provides 3.2, which is not compatible.
    Update My Extension to 2.1.0 or later, or check for a host update."
```

Three elements: the requirement, the host's version, and the next action. A refusal missing any of them
produces a support ticket rather than a resolution.

## Degradation versus refusal

The choice, per capability:

```text
Is the extension still valuable without the missing capability?
├── Yes → LOAD DEGRADED
│   ├── Disable the features that need it
│   ├── Tell the USER what is unavailable, in plain language
│   ├── Tell the EXTENSION which capabilities are absent, so it can adapt
│   └── Log it, so support can see why behaviour differs
└── No → REFUSE, with the actionable message above
```

**Degrade honestly or refuse cleanly. Never degrade silently** — silent degradation means the extension
believes it has a capability it does not, which produces mysterious failures the user cannot interpret.

## Where negotiation happens

| Point | Why there |
|---|---|
| **Install** | refuse before the user forms an expectation |
| **Update** | the most common moment for a mismatch to appear, in either direction |
| **Load** | the last gate; a mismatch introduced by an environment change |
| **Call** | a capability revoked or a deprecated point used — the only per-operation check |

**The load-time check is not sufficient on its own** if capabilities can be revoked or deprecated while
an extension runs. Design the call-time check for capability availability, and keep version negotiation
at install/update/load.

## Host-side version reporting

The host must expose its version, so an extension can adapt rather than fail:

```text
host.apiVersion          → "3.2"
host.capabilities        → the available capability set
host.deprecatedUsage     → what this extension is using that is deprecated
```

**The last one is unusual and valuable**: it lets an extension warn its own users about an impending
break, which distributes the migration communication rather than centralising it.

## Communicating a break

| Channel | Content |
|---|---|
| The refusal/refusal message | requirement, host version, next action |
| The extension developer's log/console | the full technical detail, once per run |
| The host's warnings surface | a list of extensions at risk, so users can act before it breaks |
| Deprecation notices in the docs | the replacement and the removal version |
| Direct communication for high-impact extensions | a platform break is an ecosystem event |

**The host's warnings surface is the one most often missing.** Telling the user *before* the break —
"this extension will stop working in the next version" — converts a break into a planned migration.

## Testing negotiation

```text
Build a matrix of extension versions × host versions, and assert the outcome for each:

| ext 1.0 (targets 1.x) | ext 2.0 (targets 2.x) | ext 3.0 (targets 3.x) |
host 1.x   LOAD               REFUSE                 REFUSE
host 2.x   REFUSE             LOAD                   REFUSE
host 3.x   REFUSE             REFUSE                 LOAD
host 3.x   + degradation case → LOAD DEGRADED, with the user told

Every cell must be asserted by a test, not by reading the matrix.
```

The degraded case belongs in the matrix too; it is the one that is silently wrong in most implementations.

## Checklist

- [ ] Every extension declares id, version, target range and capabilities
- [ ] The target range is a range, not a single version
- [ ] Every mismatch case has a defined, tested outcome (R2)
- [ ] Refusal messages name the requirement, the host version and the next action
- [ ] Degradation is designed where honest, and is never silent
- [ ] The host exposes its version and capability set to extensions
- [ ] Deprecated usage is reported to the extension, so it can warn its users
- [ ] The host surfaces at-risk extensions to users before a break
- [ ] A version matrix is tested, including the degradation case
- [ ] Direct communication is planned for high-impact ecosystem breaks
