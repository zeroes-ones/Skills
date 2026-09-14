# Completeness vs. Consistency

Two questions get asked about a contract. They sound similar, they are answered by different
evidence, and only one of them has a natural failure signal.

| Question | Formally | Evidence that answers it | Natural failure signal |
|---|---|---|---|
| **Consistency** | Does every implementation satisfy the contract as written? | Compilers, interface conformance checks, generated mocks, contract tests | A red build. Loud, immediate, impossible to ignore |
| **Completeness** | Can the contract express every operation the system performs? | An operation inventory derived from call sites, jobs, and required state | **None.** An incomplete contract is satisfied by every implementation |

That asymmetry is the entire reason this skill exists. Consistency reviews happen because they are
mechanically enforced: the compiler runs whether or not anyone asked. Completeness reviews do not
happen, because nothing fails when you skip them.

## The proof case

A domain port named `SessionStore` declared two members:

```kotlin
interface SessionStore {
    suspend fun hasSession(): Boolean   // can ask...
    suspend fun clear()                 // ...and forget
}
```

Both platforms compiled. The Android implementation satisfied the interface exactly — it could be
asked whether a session existed, and it could forget one. Nothing in the interface could create one.

The result: sign-in succeeded, the user reached the home screen, and the next launch found no
session and returned them to the welcome screen.

| Signal that stayed green | Why it was silent |
|---|---|
| Both compilers | Every implementation correctly satisfied the interface as written |
| 214 tests | The fakes also had no `save`, so they faithfully mirrored the omission |
| All five project gates | The testability gate asked whether behaviour was **tested**, not whether the contract was **complete** |
| Two platforms building green | iOS passed because it **bypassed the port entirely**, writing the keychain directly |

The four signals are not four weak checks. They are four checks that share one assumption: that the
contract is the specification. No consistency check can falsify that assumption, because the check
is built from it.

## The relationship to Goodhart's law

Consistency checks are a measure that has become the target. Teams measure contract health by
conformance — does it compile, does the adapter pass the port's contract test — and that measure is
genuinely useful, so it is optimised. An interface with no mutating member maximises conformance: it
is trivially satisfiable by every implementation, including a no-op.

Completeness is the intent the conformance measure can betray. The check that guards it is
deliberately low-tech: enumerate what the system must do, then ask whether the contract can say it.

## The two checks in practice

### Consistency (the check everyone has)

```
for each implementation of Contract C:
    assert implementation satisfies every member of C
```

This fails loudly when an implementation drifts. Keep it.

### Completeness (the check almost nobody has)

```
required = operations the system performs on the datum C describes
    derived from: call sites, persisted state, scheduled jobs, user-visible flows

expressible = members of C

findings = required - expressible
for each finding:
    name the operation, not the symptom
    name the implementations affected
    name the seam each affected implementation actually uses
```

This never fails on its own. It has to be scheduled, and its output is a list of operations rather
than a red mark. That is why it belongs in review rather than in CI: it requires someone to decide
what the system is supposed to be able to do.

## Why "both compilers pass" is not the argument

A compiler enforces the contract against its implementations. It has no view of the behaviour the
contract was meant to permit. Three consequences follow, and each is a real class of defect:

1. **A contract can be narrower than the work.** `hasSession` + `clear` is a valid interface for a
   read-and-forget store, and an invalid one for a session that must be persisted. The compiler
   accepts both readings because it does not read.
2. **An implementation can be wider than the contract.** Code that reaches the storage directly is
   not checked against the contract at all, so it can implement the missing operation correctly and
   still leave the contract incomplete. This is the bypass case — see `bypass-detection.md`.
3. **A test double can be exactly as narrow as the contract.** Generated mocks are derived from the
   interface, so a suite over an incomplete contract is a suite of assertions that the world is
   consistent with an incomplete contract — see `mirroring-fakes.md`.

## Deciding which review you are in

Ask what the reviewer actually checked:

* "All implementations satisfy the interface" → consistency review. Correct, useful, and silent
  about whether the interface is right.
* "The interface can express every operation the system performs" → completeness review.
* "There is no way to write the missing call" → completeness defect, and the most important kind,
  because it is the one that has no call site to point at.

## Rules

* **Derive the required set from behaviour, never from the interface.** The interface is the
  comparison target. Reading it produces a set identical to itself, which always diffs clean.
* **Say which review you ran, and say what it cannot see.** "Consistency: all implementations pass;
  completeness: not assessed" is an honest result. "The contract is fine" is not.
* **Treat the absence of a call site as ambiguous.** Either nobody needed the operation, or nobody
  could write it. Only the second is a defect, and you cannot tell them apart from the interface.
