# Mirroring Fakes

A test double is constructed from the contract. That is its purpose — it stands in for the
implementation so the test can run without the real dependency — and it is also why it cannot
falsify the contract.

> The fake and the interface share the omission, so the test agrees with the bug.

## The mechanism

```
contract  ──→ implementation A
   │      ──→ implementation B
   └──────→ fake, mock, stub, double      (derived from the contract)
                     ↓
              assertions that the system behaves consistently
              with a contract that cannot express the operation
```

Every assertion is true. The suite is thorough. Nothing is wrong with any individual test. The
system still does not do the thing, because the contract has no spelling for it and every test was
written against the contract.

## What the fake-update count tells you

The single most useful signal about whether a contract change is real:

| Fakes touched by the change | Meaning |
|---|---|
| Every fake updated | The contract genuinely changed shape — the new member is required, and every double had to satisfy it |
| Some fakes updated | The member is optional, defaulted, or only used on one path — ask why |
| No fake updated | The change was **cosmetic**. The operation is still inexpressible, or the member is declared and never used |

The source corpus records exactly this: adding the missing `save` to the port "required updating
every fake — which is the signal that the contract change was real rather than cosmetic." That
sentence is the whole check. It costs one command (`git diff --stat` over the mock directories) and
distinguishes a contract change from a comment.

## Fake taxonomy, ranked by evidential strength

| Kind | Derived from | Can falsify the contract? | Use it when |
|---|---|---|---|
| Generated mock | The interface, mechanically | **No** — it is the interface restated | The contract is stable and you are testing call ordering or error propagation |
| Hand-written stub | The interface, by a person | **No**, but a person may notice the gap while writing it | Early in a contract's life |
| Behaviour fake | The behaviour the system requires | **Partially** — it fails when the contract cannot produce the behaviour | Any contract younger than two releases, and any contract that anything depends on for a value |
| Recorded real interaction | Production traffic or a captured payload | **Yes, for what it recorded** | Whenever the wire format or storage format matters |
| Contract test against every implementation | The contract, run on each implementation | **No** — but it catches bypasses, because a bypassing implementation runs the test against nothing | Whenever there are two or more implementations |

Two entries deserve emphasis.

**Behaviour fakes are the only double that pushes back.** A behaviour fake asserts what the system
must be able to do — "a written session is reported, and a cleared one is not" — and then runs
against whatever the contract provides. If the contract cannot express the write, the behaviour
fake cannot be constructed, and that failure is the finding. The assertion that ships with the fix
is exactly this shape: write → `hasSession` true → clear → false, and it fails if `save` is dropped
from the port.

**Recorded real interactions are the only double that can falsify a *shape*.** A hand-written sample
encodes the same assumptions as the code it is written against, which is why a mock fixture proves
nothing about the real wire format. Decoding a captured live response is a different rung of the
ladder entirely.

## The removal check

The assertion is not finished when it passes. It is finished when you have watched it **fail**
without the fix:

```
1. Add the operation to the contract.
2. Write the round-trip assertion.
3. Confirm it passes.
4. Remove the operation (locally, uncommitted).
5. Confirm the assertion FAILS.
6. Restore the operation.
```

Step 5 is the check that the assertion tests the contract rather than the storage. An assertion that
passes with and without the operation is testing the fake.

> A check that shares an assumption with the code it validates cannot catch a bug in that
> assumption.

This is the same rule as proving a gate fires, applied one level down: the assertion must be shown
to be capable of failing before its pass means anything. If the assertion cannot be made to fail,
the contract is not what is being tested — escalate the verifier question to `verifier-design`.

## Rules

* **Never argue a contract's completeness from its doubles.** They are the contract restated.
* **Keep one behaviour fake per contract that anything depends on for a value.** Generated mocks are
  fine for the rest.
* **Count the fakes a contract change touches.** Zero means cosmetic; every one means real.
* **Run the removal check on every round-trip assertion.** Watch it fail before trusting it to pass.
* **Prefer a recorded real interaction over a hand-written one whenever a format is at stake.** The
  fixture is captured, not composed.
