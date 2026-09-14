# Round-Trip Assertions

A round-trip assertion is the artefact that closes a completeness finding. It is the only test that
depends on the operation the contract was missing, and therefore the only test that fails when the
operation is dropped again.

## The pattern

```
write  →  read back present  →  clear  →  read back absent
```

Four steps, in one test, asserting the two state transitions. It is deliberately the smallest
assertion that requires the operation to exist:

| If the operation is missing | Where the test fails |
|---|---|
| No `save` | The write step cannot be written — the assertion is unconstructible, which is the finding |
| `save` writes nothing | `read back present` fails |
| `save` writes non-atomically | A concurrent read may see half the value; the presence assertion is flaky, which is itself the finding |
| `clear` does not clear | `read back absent` fails |

The observed instance, named for the behaviour rather than the method: *"a written session is
reported, and a cleared one is not"* — asserting exactly the round trip the interface now guarantees
(write → `hasSession` true → clear → false), and failing if `save` is dropped from the port, which
is the exact shape of the original defect.

## Name it after the behaviour, not the method

A method-named test (`testSaveSession`) asserts that a method exists. A behaviour-named test
(`a written session is reported, and a cleared one is not`) asserts what the system does. When the
contract is later refactored, the behaviour name survives the rename and the method name does not.

The stronger form is to name the test after the **defect it guards** and cross-reference it:

| Test | The defect it guards |
|---|---|
| `a written session is reported, and a cleared one is not` | the port that had no `save`, so a session never persisted |
| `a signed-out launch ignores a completed local position` | opening the tab bar for a user with no credentials |
| `completion wins over a stale recorded step` | dragging a finished user back into onboarding |
| `a mismatched confirmation is reported on the confirmation field` | sending the user to edit the password box |

Each row makes regression archaeology trivial: when the test fails, the defect it guards is already
written down.

## Per-language and per-storage variants

The assertion is storage-agnostic; the *atomicity* requirement is not.

| Storage | Write mechanism | Atomicity note |
|---|---|---|
| Keychain (iOS) | `kSecClassGenericPassword` with an accessibility class | Choose the accessibility class deliberately — one that permits a background read is different from one that requires unlock |
| Encrypted preferences (Android) | One `commit()` for the whole value pair | Two `apply()` calls can be killed between them, leaving a half-written pair that the presence check then reports inconsistently |
| Browser storage | `localStorage.setItem` / IndexedDB transaction | IndexedDB gives you a transaction; `localStorage` does not |
| SQL / NoSQL | Transaction or a single document write | Two rows written separately is the same half-write problem |
| In-memory | Direct assignment | Atomicity is free; persistence is the missing property, so the assertion must run against the real store |
| Files | Write-temp-then-rename | A plain write leaves a truncated file on crash |

The rule across all of them: **a value with two parts must be written in one operation.** A presence
check that can see half a value is a presence check that will eventually report the wrong thing.

## The removal check

Passing is not the finish line. The assertion is finished when you have watched it fail:

```
1. Add the operation to the contract and implement it.
2. Write the round trip.
3. Run it. It passes.
4. Remove the operation locally (do not commit).
5. Run it again. It must FAIL.
6. Restore the operation and re-run. It passes.
```

Step 5 distinguishes a test of the contract from a test of the storage. An assertion that passes
with and without the operation is exercising the fake, or a default, or nothing.

This is the same discipline as proving a gate fires, applied one level down. If the assertion cannot
be made to fail at step 5, the question becomes a verifier-design question — which check *can* see
this defect class — and belongs with `verifier-design`.

## Where the assertion lives

Three valid homes, in order of preference:

1. **Beside the port, run against every implementation.** This is the strongest placement: a
   contract test that runs on each implementation catches a bypass, because a bypassing
   implementation runs the contract test against storage it is not using through the seam.
2. **In the shared domain test suite, run on every platform.** A shared domain rule has one suite
   per implementation. If the rule changes, both suites change in the same commit, or one is left
   asserting the old behaviour and looks exactly like a real regression.
3. **Beside the storage adapter.** Weakest: it tests the adapter the contract already names, and it
   will not notice a second implementation that bypasses the contract.

Placement 1 or 2, always. Placement 3 is where the assertion ends up when nobody thought about it,
and it is the placement that keeps the original defect alive.

## Rules

* **One test per contract operation that another component depends on.** Not one per method — one per
  operation the system needs.
* **Name it after the behaviour, cross-reference the defect it guards.** A method name does not
  survive refactoring; a defect reference does.
* **Run the removal check before trusting the pass.** Watch it fail once.
* **Write two-part values in one operation.** A presence check that can see half a value reports the
  wrong answer.
* **Put the assertion where every implementation runs it.** An adapter-local test cannot see a
  bypass.
