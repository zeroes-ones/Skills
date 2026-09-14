# Bypass Detection

A contract shared by more than one implementation can be:
* **fully used** — every implementation reaches every operation through the seam
* **not used at all** — the contract is documentation
* **partially used** — some implementations reach some operations directly

The third case is the dangerous one, because the contract looks exercised. The green implementation
is quoted as evidence that the seam works, and the evidence is worth nothing: that implementation
never travelled the seam for the operation that is broken.

## The grid

Build an operations × implementations matrix. Every cell gets one of three values:

```
                    iOS                Android            Test double
create/save         BYPASS             through contract   through contract
read/hasSession     through contract   through contract   through contract
delete/clear        through contract   through contract   through contract
```

Fill it by grepping each implementation for direct access to the storage or service the contract
abstracts — the keychain, shared preferences, the HTTP client, the database handle, the SDK client.
A cell is `BYPASS` when the implementation performs that operation without going through the
contract, even if it also has a contract-based path it does not use.

Blank cells are not permitted. A cell is `N/A (one implementation)` or it is a finding.

## Reading the grid

| Pattern | Meaning | Action |
|---|---|---|
| All cells `through contract` | The contract is genuinely enforced | Proceed; the grid is your evidence |
| One row is `BYPASS` on one implementation | That implementation is the only one where the contract's omission is fatal | Route it through the seam, then re-run it |
| One operation is `BYPASS` everywhere | The contract cannot express it at all | Completeness defect (see `completeness-vs-consistency.md`) |
| `N/A` because there is one implementation | The bypass question is unanswerable today | Record `N/A`, and re-run the grid when the second implementation lands |
| A cell is blank | The audit is incomplete | Not a finding — an unfinished review |

## The re-run that makes the audit honest

After routing a bypassing implementation through the seam, **re-run that implementation**. Two
outcomes, both informative:

* **It fails.** It had the same latent defect and never showed it. Its previous pass is now
  reclassified: *passing without exercising the seam*. This is the common case, and it is why a
  platform's green suite should never be accepted as evidence about a shared contract.
* **It passes.** The divergence was in the failing implementation only. The contract is now
  enforced everywhere, and the earlier passing run has been upgraded from uninformative to genuine
  evidence.

Do not skip this step. The whole value of the grid is that it converts "platform A is fine" into a
claim with a path attached.

## Partial seams are worse than absent ones

An absent seam is visible. A partial seam is not:

* The contract exists, so reviewers assume it is the integration point.
* Some paths use it, so the contract's tests pass.
* The bypassing path has no test tied to the contract, so the contract's guarantees are asserted
  only where they happen to hold.
* Any change to the contract is validated against the paths that use it, and silently misses the
  paths that do not.

This is why the grid, not the interface text, is the artefact. It answers a question the interface
cannot: *where is this contract actually load-bearing?*

## Where bypasses come from

They are rarely deliberate. The four origins, in rough order of frequency:

1. **A platform requirement the contract has no slot for.** A system SDK that presents UI needs an
   activity context; the singleton holding the contract was injected with an application context.
   The contract had no way to express "this operation needs a lifecycle-tracked context", so the
   implementation reached around it.
2. **An older path that predates the contract.** The iOS path wrote the keychain directly before the
   port existed, and nobody removed the direct write when the port was introduced.
3. **A performance or concurrency reason.** The write needed one atomic `commit()` rather than two
   `apply()` calls, and the contract's `save` took the two values separately, so the implementation
   bypassed it to get atomicity. The fix is a contract change, not a local exception.
4. **An unowned operation.** Nobody could express it, so somebody solved it where they stood.
   This is the completeness defect appearing as a bypass.

Origin 3 is a signal about the contract's granularity, and origin 4 is a signal about its
completeness. Neither is an argument for permitting the bypass.

## Rules

* **Two implementations make the audit mandatory; one makes it vacuous.** Record `N/A`, do not skip.
* **The grid is the deliverable.** A prose sentence saying "both platforms use the port" is not
  checkable and is how the bypass survived review.
* **Bypass counts as a finding even when the bypassing code is correct.** The defect is that the
  contract is not the integration point, not that the direct call is broken.
* **Re-run every implementation you re-route.** An implementation that passes through the seam is
  evidence; one that passes without it is decoration.
* **When the bypass is a platform requirement, widen the contract rather than documenting the
  exception.** An exemption with no slot in the contract becomes a second, undocumented contract.
