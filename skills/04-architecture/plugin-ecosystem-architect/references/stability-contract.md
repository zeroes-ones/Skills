# Stability Contract

<!-- DEEP: 5+min -- tiers, deprecation windows, and the version-negotiation rule -->

## What the contract says

A stability contract answers three questions for an extension developer:

1. **What will not break?** — the tier of each point.
2. **For how long?** — the deprecation window.
3. **How will I be told?** — the migration path and the warning mechanism.

Anything less leaves the developer guessing, and guessing developers write defensive code or leave.

## The tier table, published

```markdown
## Extension API stability

| Surface                | Tier        | Promise                                      |
|------------------------|-------------|----------------------------------------------|
| content.load/save      | STABLE      | No break without a major version + migration |
| content.query          | STABLE      | As above                                     |
| build.transform        | STABLE      | As above                                     |
| events.on(event, cb)   | STABLE      | As above                                     |
| events.filter.*        | EXPERIMENTAL| May change with notice; opt in               |
| ai.prompt              | EXPERIMENTAL| May change with notice                       |
| internal.*             | INTERNAL    | No promise; not for extensions               |
```

Publishing this table is the contract. Without it, "stable" means whatever the last person believed.

## Deprecation, done properly

A deprecation is a promise with a timeline. The full sequence:

```text
1. ANNOUNCE      the point is deprecated; name the replacement and the removal version
2. WARN IN HOST  extensions using it generate a visible warning, with a doc link
3. KEEP WORKING  the old point continues to function for the whole window
4. MIGRATE       provide a migration note; a codemod if the shape allows
5. REMOVE        only at the announced version, after the window has elapsed
```

**The four failures in this sequence, all common:**

| Failure | Effect |
|---|---|
| Removing without a window | Integrations break with no notice; the trust event is disproportionate |
| Announcing without a warning mechanism | Developers do not see it; the removal is still a surprise |
| Warning but breaking early | The window was a statement, not a commitment |
| Never removing | Dead surface accumulates; the deprecation was theatre |

**Window length:** long enough that a small maintainer can act — typically one major release cycle at
minimum, and longer for a public ecosystem where many maintainers work part-time. State the rule, then
honour it.

## The version-negotiation rule

Extensions release on their own schedule. The host must therefore decide what to do with every mismatch.

### The declaration

Every extension declares what it targets:

```json
{
  "id": "com.example.my-extension",
  "version": "2.1.0",
  "targets": { "hostApi": ">=3.0 <4.0" },
  "capabilities": ["content.read", "content.write"]
}
```

Three fields are load-bearing: **identity** (for diagnostics and revocation), **version** (for
support), and **targets** (for negotiation). Capabilities are covered in `capability-model.md`.

### The mismatch matrix

Every cell needs a defined outcome. This is R2's enforceable half.

| Case | Host behaviour | Why |
|---|---|---|
| Extension targets a range the host satisfies | **LOAD** | normal |
| Extension targets older than the host's minimum | **REFUSE**, with an actionable message naming the required version | it cannot work against the current contract |
| Extension targets newer than the host | **REFUSE** | the host cannot know a contract it predates |
| Overlapping but not exact | **LOAD**, record which contract was assumed | the overlap is the contract |
| Host supports the range but a used capability is deprecated | **LOAD + WARN** | working, but heading for a break |
| Capability no longer available | **LOAD DEGRADED** — disable the affected features, tell the user | partial function beats refusal, if honest |

**The "load degraded" row is the one teams omit.** An extension that needs one removed capability may
still be valuable without it. Degrading explicitly — with a user-visible statement — is usually better
than refusing, provided the extension can be told which features are unavailable.

### Refusal must be actionable

```
❌ "Extension incompatible."
✅ "This extension requires host API 2.x; this app provides 3.2.
    Update My Extension to 2.1.0 or later to continue."
```

The message names the requirement, the host's version, and what the user can do. A refusal without a
next step is a support ticket.

## Degradation design

Where a host can degrade, it should design for it:

| Situation | Degradation |
|---|---|
| Optional capability gone | Disable the feature; keep the rest; state it |
| Event shape changed | Adapt in the host where the mapping is unambiguous |
| Extension predates a new required capability | Offer the fallback path, or refuse with a clear reason |
| Extension uses a deprecated point | Load, warn in the log, and surface it to the developer |

**The principle:** degrade in the direction of *less function, honestly stated*, never in the direction
of *silent wrong behaviour*.

## Compatibility shims

A shim is legitimate and bounded: a host-side adapter implementing the old contract over the new one.

| Use a shim when | Do not use a shim when |
|---|---|
| The change is mechanical (renamed field, moved function) | The change is semantic (different guarantees) |
| The old point is deprecated but still needed by many | Almost nobody uses it — just remove it |
| The shim is small and testable | The shim grows to re-implement the old system |

**The trap:** a shim that quietly becomes the permanent implementation of a deprecated contract. Give it
a removal version and an owner.

## Rehearsing a break

Before shipping anything that breaks a contract, run this:

```text
1. Write (or take) a real extension against the CURRENT contract.
2. Apply the breaking change to the host.
3. Load the old extension against the new host.
4. Confirm the failure mode matches the contract:
     - refusal with an actionable message, or
     - degradation as designed, or
     - a shim that works
5. Confirm what a developer sees: the message, the log, the docs link.
6. Fix anything that failed.
7. Record the rehearsal, and repeat it before the next breaking release.
```

Step 4 is where designs fail: the contract said "refuse cleanly" and the reality is a crash.

## What the contract must not promise

| Over-promise | Why it is a mistake |
|---|---|
| "Never breaks" | Impossible for a platform that needs to evolve; the first break destroys trust |
| "Stable" without a tier on every point | Unenforceable; there is no list to check |
| Behavioural stability of a deprecated point | Old contract, new internals — guarantee only what you can |
| A deprecation window you cannot resource | A broken promise is worse than a short one |

**Under-promise and honour it.** A platform that promises little and keeps every promise develops a
better reputation than one that promises permanence and breaks twice.

## Checklist

- [ ] Every extension point has a published stability tier (R2)
- [ ] Every extension declares identity, version and target range
- [ ] Every mismatch case in the matrix has a defined outcome
- [ ] Refusal messages are actionable: requirement, host version, next step
- [ ] Degradation is designed where it is honest, and never silent
- [ ] The deprecation sequence is followed, including the warning mechanism
- [ ] The window is stated and honoured, and removals happen at the announced version
- [ ] A compatibility shim has an owner and a removal version
- [ ] A break has been rehearsed with a real extension, end to end
- [ ] The contract promises only what the team can resource
