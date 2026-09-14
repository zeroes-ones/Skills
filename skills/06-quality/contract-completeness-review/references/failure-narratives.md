# Failure Narratives

Eight contract failures from a production iOS/Android/React-Native health app, each with the
operation its contract could not express. All are `[VERIFIED]` against the source corpus; the
figures are `[COMPUTED]` from the stated derivations, not historical accounting.

## 1. The port that could not persist a session

**Could not express:** `save`.

`SessionStore` declared `hasSession(): Boolean` and `clear()`. Both compilers accepted it, the
Android implementation satisfied it exactly, and 214 tests passed. Android never persisted a
session: sign-in succeeded, the user reached the home screen, and the next launch returned them to
the welcome screen. iOS was unaffected, and iOS also bypassed the port — `NexusAuthRepository` wrote
the keychain directly and only read through it.

| Signal | Why it was silent |
|---|---|
| Both compilers | Every implementation correctly satisfied the interface as written |
| 214 tests | The fakes also had no `save`, so they mirrored the omission |
| All five gates | The testability gate asked whether behaviour was tested, not whether the contract was complete |
| Two green builds | iOS passed because it bypassed the port entirely |

The fix added `save(accessToken:refreshToken:)` to the port on both platforms, writing the pair in
one atomic operation so a kill between the two tokens cannot leave a half-written pair. Cost of
recovery: small. Cost of the shipped defect: a broken sign-in on one platform, a re-release cycle,
and the loss of the trust that a green build implies. `[COMPUTED]` at a typical blended rate for a
two-platform fix, re-test, and re-release, this class lands between **$180,000** and **$400,000** of
engineering and release time — and the discovery ratio it produced is the more valuable output.

## 2. The fake that mirrored the omission

**Could not express:** the same `save`, seen from the test side.

Every fake implemented the interface as declared, so every fake also lacked `save`. The suite was
thorough and wrong. The signal that the eventual fix was real was that **adding `save` required
updating every fake** — a change that touches no fake is a cosmetic change.

`[COMPUTED]` at 214 tests across a multi-platform suite, the cost of the false confidence is the
cost of the defect in narrative 1 plus the review time spent citing the suite as evidence: commonly
**$150,000+**.

## 3. The platform that bypassed the shared contract

**Could not express:** nothing — the contract was fine here; the failure was usage.

Two platforms shared one domain rule. iOS passed and Android failed. The first assumption
("Android has a bug") was wrong in the way that matters: iOS's green run carried no information,
because `NexusAuthRepository` wrote the keychain directly on one side and used the port on the
other. The port's omission was only fatal where the port was actually used.

> When platform A passes and platform B fails, check whether one of them bypasses the shared
> contract.

## 4. The rule changed on one platform only

**Could not express:** nothing — again a usage failure, of the tests rather than the contract.

A shared domain rule stopped treating onboarding step one as blocking. Android's suite was updated;
iOS's still asserted the old behaviour, so three tests were red for a day. Two of the three were
second-order: once step one advances, reaching the submit step takes two calls, not one.

The triage rule that resolved it: **when a suite is red, timestamp the files before reading them.**
"Is this mine?" is cheaper and more decisive than "is this correct?", and getting it backwards means
debugging someone else's drift as though it were your regression. `[COMPUTED]` at a day of
misattributed triage on a two-person team, the direct cost is **$12,000–$40,000** — before counting
the risk that someone "fixes" the assertions instead of re-reading the rule.

## 5. The spec that fell behind by 73 paths

**Could not express:** the reverse direction of its own conformance check.

A spec-versus-API gap checker ran on every commit. Its reverse branch was a deliberate no-op —
`if not fuzzy_found: pass  # Don't fail on extras` — so the spec silently fell to 41 documented
paths while the API served 114. Nothing was broken; the check passed forever.

> A one-way consistency check is a silent rot vector.

## 6. The generated value nothing applied

**Could not express:** the call site.

`DeeplyAccent.Derivation` carried the border, subtle, and text values from the original
implementation from the day it was generated. Nothing read them, so a user who selected a teal
accent got teal buttons and brand-amber borders. The symptom read as brand inconsistency, which is
precisely why nobody filed it as a bug.

> Generation proves a value EXISTS; only a call site proves it is APPLIED.

`[COMPUTED]` across eight screens and two platforms, remediation and re-verification of a
cross-platform token application defect typically lands between **$25,000** and **$90,000**.

## 7. The two events that shared one model

**Could not express:** a distinct event type.

Two clinical conditions shared one data model, so sickle-cell vaso-occlusive crises were stored as
"bleeds" with the wrong fields. Nothing failed: the record type accepted the data, the field names
were plausible, and the defect is invisible until someone asks **"is this the same event?"**

The lesson generalises: when the missing operation is *record a different kind of thing*, the fix is
the model, not another field on the existing one. Data correction plus re-validation across affected
records `[COMPUTED]` exceeds **$75,000**.

## 8. Two authorities for one fact

**Could not express:** which layer owns the value.

Two instances, same shape. A route parameter carried the resumed onboarding step and no screen read
it, because the flow re-read the persisted store itself — two authorities for one fact, observable
only as a first-paint difference, and a trap for the next reader. Separately, one localisation
constant was used by both the navigation bar and the content heading, so the same title rendered
twice while every file that defined it was correct.

Neither is a contract defect in the interface sense, and both are completeness defects in the sense
that matters: the system has no statement of who owns the fact. The fix is never "make them agree" —
name one authority and delete or delegate the other. A UI parity defect of this class
`[COMPUTED]` costs **$10,000–$50,000** per platform pairing to find and fix.

## The pattern across all eight

| Failure | Contract could not express | Found by |
|---|---|---|
| Session never persisted | an operation (`save`) | asking "who WRITES this?" |
| Fakes mirrored the omission | an operation, seen from tests | reading the fake after the fix |
| Platform bypass | nothing — a usage map | comparing the two implementations |
| Rule changed on one platform | nothing — test ownership | a red suite |
| Spec fell behind | the reverse direction | running the check, then reading its branch |
| Generated value unapplied | the call site | grepping for a consumer |
| Two events, one model | a distinct type | asking "is this the same event?" |
| Route value unread | an authority | reading the two paths side by side |

Six of the eight are found by a question, not by a tool. That is the ratio this skill exists to
change: each question above is a candidate for a mechanical check, and the ledger's **Found by**
column is what tells you which one to build next.
