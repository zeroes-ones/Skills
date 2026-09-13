# The Update Model

<!-- DEEP: 5+min -- remediation paths, exposure windows, and the rehearsal procedure -->

## Why this file exists

This is the R2 deliverable. The linkage decision is the *consequence*; the update model is the
*decision*. If you can answer "a critical vulnerability was just published in this dependency — what
happens next, and how long until users are protected?", you have an update model. If you cannot, you
have a guess with a build flag attached.

## The five update models

| Model | Mechanism | Exposure window driven by |
|---|---|---|
| **Platform-patched** | the OS or runtime ships the library; users update the OS | the platform vendor's release cadence |
| **Package-patched** | a distribution/package manager ships the library | the distribution's cadence, or your pinning policy |
| **Self-patched, dynamic** | you ship the shared library; consumers load the new one | your release cadence, once per library |
| **Self-patched, static** | the library is in your binary; every consumer rebuilds | your release cadence × every consumer |
| **Bundled set** | one release ships a tested set; the whole set is replaced | your release cadence, and you must re-verify the set |

Each is legitimate. The failure is not choosing one — it is not *knowing* which one you chose.

## The exposure window, defined precisely

```text
exposure_window = t_patch_available → t_users_protected

  t_patch_available : the upstream fix exists
  + t_integrate     : you take the fix and build
  + t_test          : your verification (regression, security, perf)
  + t_release       : your release train / store review / package publish
  + t_rollout       : staged rollout to full adoption
  = t_users_protected
```

Measure it once, for real, and record the number. An unmeasured exposure window is the thing that
turns a routine patch into an emergency.

**Where the terms differ by model:**

| Term | Static | Dynamic (your library) | Platform-patched | Sidecar / service |
|---|---|---|---|---|
| `t_integrate` | rebuild every consumer | rebuild one library | none | rebuild one image/service |
| `t_test` | every consumer's suite | the library's suite | the platform's | the service's |
| `t_release` | every consumer's release train + review | one library release | the OS update path | one deploy |
| `t_rollout` | per-consumer adoption | per-library adoption | OS adoption (slow, involuntary) | your deploy |

**The counter-intuitive row:** platform-patched looks best on paper but has the *worst* rollout term,
because you do not control OS adoption. That is why a product may still vendor a library it could
otherwise take from the platform.

## The rehearsal

R2 and Decision Tree 4 require the path to have been **executed once**. Reading the steps is not a
rehearsal.

```text
Rehearsal procedure (do this once per critical dependency, then annually):

1. Pick a dependency with real security relevance.
2. Take a real (or realistic) patch to it.
3. Execute the full path on each shipping platform:
     integrate → build → test → package/review → stage → rollout
4. Record each stage's elapsed time.
5. Note anything that had to be improvised.
6. Fix the improvisations (missing pipeline step, unclear ownership, absent rollback).
7. Re-run and compare.
8. Publish the exposure window, per platform, with the date measured.
```

**What rehearsals reliably uncover:** an untested build target, a release process that needs a human
nobody named, a store review that turns hours into days, and a dependency that is actually two
dependencies in different forms. None of these is visible from the build configuration.

## Deciding the model, per dependency

```text
Is the dependency security-relevant?
├── No → the model matters less; still record it
└── Yes ↓
    Can the platform supply it (a system library with a patch channel)?
    ├── Yes → PLATFORM-PATCHED, if you actually load the system copy
    │         → verify: no vendored copy is shadowing it in the load path
    │         → accept: you do not control OS adoption speed
    └── No ↓
        How many independently-shipped consumers must you patch?
        ├── One, released in lockstep → STATIC, with a stated cadence
        └── Many or independent ↓
            Must users be protected without rebuilding consumers?
            ├── Yes → DYNAMIC (self-patched), and maintain the ABI so updates load
            └── No  → STATIC is defensible; publish the exposure window so the
                      acceptance is explicit rather than incidental
    Then, always:
    ├── Is the exposure window acceptable for THIS dependency's blast radius?
    │   ├── Yes → record the acceptance and the measured window
    │   └── No  → change the model, or reduce the blast radius
    └── Who owns executing the path? Named, not "the team"
```

## The blast-radius question

The exposure window matters proportionally to what the dependency can expose. Pair them:

| Dependency kind | Typical blast radius | What a long window costs |
|---|---|---|
| TLS/crypto primitives | total — confidentiality of all traffic | unacceptable; the window is the risk |
| Authentication/authorisation | account takeover | high |
| Parser for untrusted input | remote code execution | high |
| Serialisation/format library | data corruption or RCE | high |
| HTTP/network client | request forgery, SSRF enablers | medium-high |
| Compression | decompression bombs, DoS | medium |
| Logging | mostly availability | low-medium |
| UI toolkit | rarely security-relevant | low |
| Test-only dependency | none in production | not applicable |

**Use this to prioritise the rehearsal.** A static linkage decision for a logging library is not a
finding. The same decision for a TLS library is.

## When static linkage with a long window is defensible

The honest justifications, each of which must be written down:

| Justification | What must accompany it |
|---|---|
| The dependency has no meaningful security surface | state the assessment, and re-check when it gains one |
| The platform provides no shared copy for this target | state the target constraint |
| The product is a single-tenant internal tool with a controlled rollout | state the rollout control |
| The distribution channel forbids shipping additional binaries | state the channel rule |
| The exposure window is short in practice because the release train is fast | **measure it**, do not assert it |

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| The update model discovered during an incident | the incident sets the timeline, not you |
| "We'll rebuild quickly if we need to" | unmeasured; the rehearsal contradicts it |
| A vendored copy shadowing the system library | you think it is platform-patched and it is not |
| A static dependency nobody classified as security-relevant | mis-triaged blast radius |
| No named owner for executing the path | the path executes late and improvised |
| Rehearsing only the build, not the release | the release train is usually the long pole |
| One exposure window for all platforms | store review and package publish differ by orders of magnitude |

## Checklist

- [ ] Every dependency has a recorded update model, not an implied one
- [ ] Security-relevant dependencies are classified by blast radius
- [ ] The exposure window is measured per platform, with the date recorded
- [ ] The path has been rehearsed end to end, including the release stage
- [ ] Improvisations found in the rehearsal have been fixed
- [ ] A named owner exists for executing the path
- [ ] No vendored copy shadows a platform-patched library
- [ ] Each acceptance of a long window is written down with its justification
- [ ] The remediation path is recorded where a new engineer will find it (R2)
