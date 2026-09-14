# The Writer/Reader Audit

One question finds the class of defect that every other check is blind to:

> **Who WRITES this?**

Ask it of any state whose presence or value something else depends on reading. The question is
cheap, mechanical, and it is the check that located the most serious defect in the source corpus —
a port that could only ask and forget.

## The procedure

For each piece of shared state:

1. **Name the state.** Not the variable — the fact. "Whether the device currently holds a valid
   session", not `sessionState`.
2. **Name every reader.** A screen, a job, a middleware, a health check. Include indirect readers:
   a routing decision that reads it at launch is a reader.
3. **Name every writer.** The function that first creates the value and every function that updates
   it. A constructor default is not a writer; an initialiser that sets `isLoading = true` and is
   never subsequently changed is the absence of one.
4. **Name the seam each reader and each writer uses.** A seam is the interface, port, or module
   boundary the operation travels through. `writes directly to Keychain` is a seam name, and it is
   the finding.
5. **Compare.** A read whose writer is unnamed, or whose writer uses a different seam from the
   reader, is a finding.

## Output shape

| State | Reader (seam) | Writer (seam) | Verdict |
|---|---|---|---|
| Valid session present | `AppEntry.resolve` via `SessionStore` | *(none — the port has no `save`)* | **Incomplete contract** |
| Valid session present (iOS) | `AppEntry.resolve` via `SessionStore` | `NexusAuthRepository` via `KeychainTokenStore` **directly** | **Bypass** |
| Onboarding position | `RootScreen` via route parameter | `OnboardingFlow` re-reads the store itself | **Two authorities** |
| Loading resolved | `HomeViewModel.state` | *(none — `on(intent: .load)` is never called)* | **Missing writer, no error** |

The fourth row is worth dwelling on: a view model whose state starts at `isLoading = true` and has
no writer will spin forever. No compiler complains, because the state is validly initialised; no
timeout fires, because no request was ever made. The writer/reader audit names it in one pass,
while "find the bug" does not.

## A state lifecycle needs its operations in the same contract

The asymmetry that produces this defect is always the same shape: a lifecycle has four or five
operations and the contract exposes a suffix of them.

| Operation | Typical member | Usually present? | Consequence of absence |
|---|---|---|---|
| Create | `save`, `set`, `put`, `insert` | **No** — this is the one that goes missing | The value is never created; the reader sees the initial state forever |
| Read | `get`, `has`, `exists`, `load` | Yes | — |
| Update | `save`, `set`, `refresh` | Usually folded into create | Silent divergence between in-memory and stored value |
| Delete | `clear`, `remove`, `delete`, `logout` | Yes | — |
| Observe | `observe`, `changes`, `subscribe` | Sometimes | Polling everywhere, or a stale UI |

The pattern is not random. **Reads and deletes are visible in the UI, so they get built first and
get built into the contract. Creation and update are absorbed by whichever layer happens to own the
storage, which is usually outside the seam.** A port written after the screens were built will
describe a store that can be asked about and emptied, because that is what the screens needed to
render.

## Asymmetric-operation catalogue

Every row below was observed or is the direct generalisation of an observed case.

| Contract member present | Missing opposite | What the name promised | What it delivers |
|---|---|---|---|
| `hasSession()` | `save(session)` | A store owns a session | A predicate with a delete |
| `getCurrentUser()` | `setCurrentUser(user)` | A current user is tracked | A read of something nobody sets |
| `isAuthenticated()` | `authenticate(...)` | Authentication state | Derived truth with no origin |
| `isFeatureEnabled(flag)` | flag provisioning | Feature state | An answer about a fact that is never written |
| `listComponents()` | `register(component)` | A registry holds components | An enumeration of an empty set |
| `findByTenant(id)` | tenant-scoped write | Tenant-scoped data | Reads constrained to a scope nothing enforces on write |
| `canPerform(action)` | the action's own capability check | Authorization | A gate the client derives and the server never enforces |

The last row is the one to escalate rather than fix locally: a contract that cannot express a
capability check cannot enforce it, and the absence is security-relevant. Escalate to
`security-reviewer` — a capability derived on the client and enforced nowhere is an authorization
hole wearing a contract shape.

## Two authorities for one fact

The writer/reader audit also catches the inverse defect: **more than one writer, or a reader that
does not read the thing the writer wrote.**

* A route parameter carries the resumed onboarding step, and no screen reads it, because the flow
  re-reads the store itself. There are two authorities for one fact. Neither is wrong alone, the
  divergence is observable only as a first-paint difference, and the route value is a trap for the
  next reader.
* A single localisation constant is used by both the navigation bar and the content heading, so the
  same title renders twice. Every file that defines it is correct. The defect is a duplicate use of
  one authority across two layers.

The fix is never "make them agree" — agreement is what an unowned fact does when it drifts. Name one
authority, and delete or delegate the other.

## Rules

* **A store that reads must also write, or it is a query and not a store.** The name is part of the
  contract: `SessionStore` advertised ownership of the value and delivered ownership of the
  question.
* **An initialiser default is not a writer.** `isLoading = true` with no transition is the same
  class of defect as a missing `save`, and it is harder to see because the state is not wrong, it is
  frozen.
* **A writer outside the seam is a bypass, not an answer.** "Something sets it" is not a writer
  unless you can name the function and the seam. See `bypass-detection.md`.
* **Count the writers.** Two is a defect. One is a finding only if it is outside the contract that
  the readers use.
