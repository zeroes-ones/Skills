# Developer Experience

<!-- STANDARD: 3min -- onboarding, local development, testing, debugging, publishing -->

## Why DX is a ground rule

R6 exists because **ecosystems are won or lost in the developer's first hour**. Not in the API design,
not in the documentation site, and not in the launch announcement — in whether a developer can get
something working, see it fail informatively, and ship it, before their attention runs out.

A platform with a beautiful contract and no local development story produces a launch and no ecosystem.
That is a predictable outcome, not bad luck.

## The first-hour path

```text
0:00  read one page and understand what the platform is for
0:05  install the tooling (one command)
0:10  scaffold a working extension from a template
0:15  run it against the host locally
0:25  hit an error, and get a message that names the cause
0:35  fix it, using the docs the error linked to
0:45  run the extension's own tests
0:55  package it and see it load
1:00  something working exists
```

**Every step must be timed and measured.** If a step takes longer than this budget, that is the finding —
not a documentation gap to note, but a deliverable to fix.

## The deliverables

| Deliverable | Minimum | Why |
|---|---|---|
| **A template / scaffold** | one command creates a working extension | the empty-file problem stops most first attempts |
| **A local host** | run the host with the extension loaded, without a full install path | iteration speed decides whether anyone continues |
| **A test harness** | exercise extension points without the whole product | untestable extensions are abandoned extension |
| **Structured errors** | errors name the cause and link to the fix | the single highest-value DX item |
| **A debug path** | breakpoints / logs / inspector for extension code | otherwise every bug is a guessing game |
| **A packaging command** | build, validate, sign | publishing friction is a filter on the ecosystem |
| **Local validation** | catch manifest and capability errors before publishing | publishing then failing is a demoralising loop |
| **Documentation with runnable examples** | copy-pasteable, verified | prose without code is not a tutorial |

## Structured errors are the leverage

The highest-return DX investment, because it converts every mistake into a self-service fix:

```
❌ "Extension failed to load"
✅ "Extension 'com.example.foo' targets host API 2.x, but this host provides 3.2.
    The extension was built for an older contract.
    → Migrating to host API 3.x: <link>
    → Or install a compatible host version: <link>"
```

Three properties:

1. **Names the cause**, in the developer's terms.
2. **Names the next action**, not just the problem.
3. **Links to the specific fix**, not to the documentation home page.

**Implement this at the host's error sites, not in the docs.** A developer hitting an error will read
the error; they will not search the docs for it.

## Local development

| Requirement | Why |
|---|---|
| Load an unpackaged extension from a directory | packaging on every iteration kills velocity |
| Hot reload, or a fast restart | the loop length is the DX metric |
| The same host build developers ship against | version skew between dev and production is a DX defect |
| A way to run against test data | a real account is not always available |
| The capability model active locally | an extension that works locally and fails on install is a trap |

**The last row is subtle and important.** If local development runs with all capabilities granted, the
developer discovers the capability model only at install time. Enforce capabilities locally too.

## Testing

| Level | What the platform provides |
|---|---|
| Unit | the extension's own tests, with the host's API mocked or stubbed by the platform |
| Integration | run the extension against a local host instance |
| Contract | verify the extension against the declared target range |
| Capability | verify the extension does not exceed what it requested |

The **contract test** is the platform's responsibility, because only the platform knows the contract.
Shipping a way to run an extension against multiple host API versions is how a developer avoids shipping
a break.

## Debugging

| Need | Provide |
|---|---|
| See what the host called | a log of extension-point invocations, with arguments |
| See what the extension returned | same, for results and errors |
| Break on an extension point | a debug hook, or a documented attach path |
| See capability denials | the chokepoint's audit log, surfaced to the developer |
| Reproduce a user's problem | a diagnostic bundle including extension id/version/capabilities |

**The capability-denial log is DX-specific and often missing.** A developer whose extension silently
cannot do something needs to see the denial, or they will spend hours on a bug that is a policy.

## Publishing

| Step | Friction to remove |
|---|---|
| Build | one command, reproducible |
| Validate | manifest, capabilities, target range — before submitting |
| Sign | automatic, with the key managed by the tooling |
| Submit | an API, not a form, for repeatable releases |
| See status | a queue state and a reason for any rejection |
| Update | the same path, without re-review where the model allows |

Automated validation before submission is the highest-value item: it converts a review rejection into a
local error, which is the difference between a frustrating loop and a fast one.

## Measuring DX

| Metric | Target |
|---|---|
| Time from start to a working extension | within the first-hour budget |
| Time from change to seeing it locally | a few seconds, not a rebuild cycle |
| Time to publish, first time | minutes after the work is done |
| % of errors with an actionable message and a link | approaching 100% |
| % of submissions passing validation first time | high, and rising |
| Developer-reported friction, in their words | read it, and act on it |

Measure the first three with a stopwatch on a real developer. The numbers are usually worse than
assumed, and that is the point.

## The abandonment signals

| Signal | Meaning |
|---|---|
| Developers scaffold and stop | the template produces something that does not run |
| Questions cluster on the same step | that step is broken, not the developer |
| Extensions work locally, fail on install | the local environment does not enforce the real constraints |
| Support load is high for simple problems | errors are not actionable |
| Few updates after the first release | publishing is painful, or the contract is too unstable |
| Long forum threads ending in workarounds | the platform, not the developer |

Each is a DX defect with a specific fix, and each is measurable before the ecosystem fails.

## Checklist

- [ ] A scaffold creates a working extension in one command
- [ ] A local host runs the extension without a full install path
- [ ] A test harness exists, including a contract test against the target range
- [ ] Errors name the cause, the next action, and link to the specific fix
- [ ] A debugging path exists for extension code
- [ ] Capabilities are enforced locally, so the model is discovered before install
- [ ] Packaging and signing are one command
- [ ] Local validation catches manifest and capability errors before submission
- [ ] Documentation examples are runnable and verified
- [ ] Time-to-first-working-extension is measured, against a stated budget (R6)
