# Linkage Forms

<!-- STANDARD: 3min -- the unit-form catalogue and the four constraints that select a form -->

## The three axes, stated separately

Most linkage arguments collapse three independent decisions into one. Keep them apart:

| Axis | Question | Options |
|---|---|---|
| **Resolution time** | When does a symbol become an address? | build · load · first call · runtime |
| **Unit form** | What shape is the reusable thing? | header-only · static archive · shared object · framework · plugin · sidecar · network service · WASM module · source package |
| **Process presence** | How much exists at launch? | not loaded · loaded eagerly · loaded on demand · separate process |

A choice on one axis does not determine the others. You can have a shared object loaded on demand
with lazy binding, or a static archive resolved at build time, or a WASM module loaded at runtime
in a separate execution context.

## The unit forms

| Form | Resolved at | Cost | Use when |
|---|---|---|---|
| **Header-only** | build (inlined) | code duplication in every consumer; slow compiles | small, template-driven, generic code |
| **Static archive** (`.a`, `.lib`) | build | large executables; each consumer carries its own copy | one consumer; minimal targets; no shared runtime |
| **Shared object** (`.so`, `.dylib`, `.dll`) | load | loader work; version and path management | multiple consumers; patchable dependencies |
| **Framework / bundle** | load | bundle structure; platform conventions | platform-integrated libraries (Apple frameworks, .NET assemblies) |
| **Plugin / extension** | runtime | ABI contract; sandboxing; lifecycle | third-party extensibility; optional capability |
| **Sidecar process** | runtime (separate process) | IPC cost; process management | isolation, language mismatch, crash containment |
| **Network service** | runtime (remote) | latency; failure modes; operations | independent scaling and deployment |
| **WASM module** | runtime (sandbox) | boundary/marshalling cost; toolchain constraints | untrusted code; portable, sandboxed extension |
| **Source package** | build (compiled by the consumer) | consumer needs a toolchain; no binary ABI risk | language-ecosystem distribution (crates, modules, packages) |

Note the last row: a **source package** has no ABI problem at all, because there is no binary
boundary. That is why language package managers default to it — and why the ABI discussion only
starts when you ship a binary.

## The four constraints that select a form

Every form choice should be traceable to these four. If a constraint is unknown, the choice is a
guess.

| # | Constraint | The question it answers | It decides |
|---|---|---|---|
| C1 | **Update model** | How does a fix in this unit reach users? | static vs dynamic; whether a plugin boundary is warranted |
| C2 | **Launch / memory budget** | What may this cost at startup and in resident memory? | eager vs lazy load; sidecar vs in-process |
| C3 | **Distribution target** | What does the channel permit to be shipped and loaded? | whether runtime loading is available at all |
| C4 | **Licence** | Does the licence permit this form of distribution? | whether a form is legally available (see `dependency-governance`) |

**C3 is the one teams forget.** A distribution channel may forbid loading code that did not ship
with the app, or forbid bundling a runtime. That constraint removes options regardless of their
engineering merit — which is why R6 requires confirming it before choosing.

**C4 is the one that surprises late.** Some licences distinguish between linking forms, or forbid
modification (which subsetting or static incorporation may constitute). Confirm it during
selection, not at release.

## The form decision, condensed

```text
1. More than one independently-released consumer?
   ├── No  → static is usually right (record the update model anyway)
   └── Yes → continue
2. Must a fix reach consumers without rebuilding them?
   ├── Yes → dynamic (or a plugin, if the boundary is also an extension point)
   └── No  → static is defensible if the remediation latency is stated and accepted
3. Is the unit optional, untrusted, or language-mismatched?
   ├── Yes → plugin (in-process), sidecar (isolated), or WASM (sandboxed)
   └── No  → in-process shared object
4. Does the target have no shared runtime?
   └── Yes → static, and state the constraint
5. Does the distribution channel forbid any of the above?
   └── Yes → that option is removed; re-choose from the rest
```

## What "form" commits you to

| Form | The commitment |
|---|---|
| Header-only | Every consumer recompiles; a change is a source change everywhere |
| Static archive | Every consumer rebuilds and re-ships for a fix |
| Shared object | You maintain an ABI and a version boundary; fixes can ship once |
| Framework | The platform's bundle conventions and signing/entitlement model apply |
| Plugin | You maintain an ABI for third parties and a lifecycle for load and failure |
| Sidecar | You run a process and its IPC; failures are isolated but observable |
| Network service | You operate it; versioning becomes a wire contract (see `api-designer`) |
| WASM | You respect a sandbox boundary and a different toolchain |
| Source package | The consumer owns the build; your risk is API breakage, not ABI |

## Common mistakes

| Mistake | Why it fails |
|---|---|
| Choosing a form by ecosystem habit | Go, Rust and C ecosystems default differently; a habit is not a constraint |
| Treating "dynamic" as one thing | A system-provided library, a bundled shared object and a plugin have different update models |
| Ignoring the second consumer | The first consumer makes it a component; the second makes it a contract |
| Choosing the form before knowing the channel | A forbidden form is not a decision |
| Assuming a shared object is always smaller in memory | Shared pages help; per-process state and loader overhead do not disappear |
| Overlooking the build-graph consequence | A dynamic boundary changes the build target matrix (see `build-system-design`) |

## Recording the decision

Per unit, record — this is the artefact R1 requires:

| Field | Example |
|---|---|
| Unit | `libcrypto-shim` |
| Form | shared object |
| C1 update model | platform-patchable; exposure window = OS vendor latency |
| C2 launch budget | loaded eagerly; contributes < 5 ms to cold start `[ESTIMATED]` |
| C3 distribution | bundled with the app; runtime loading of add-ons not permitted by the channel |
| C4 licence | permits redistribution and linking as chosen |
| ABI policy | soname major bump on incompatibility; 14 exported symbols |
| Remediation rehearsal | executed 2026-08; 3 h from patched source to staged rollout |
