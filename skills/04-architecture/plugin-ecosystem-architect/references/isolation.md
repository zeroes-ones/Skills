# Isolation

<!-- DEEP: 5+min -- in-process, sandboxed, and separate-process isolation per extension class -->

> **Verification note.** Sandbox runtimes, their capability models and their performance
> characteristics change between versions. Confirm current support and behaviour against the runtime's
> own documentation for the version you intend to ship.

## The decision, stated plainly

**Policy is not isolation (R5).** Running untrusted code in-process means one extension's defect is a
remote code execution in your product, and its crash is your outage. Isolation is a mechanism: a
sandboxed runtime, a separate process, or a verifiable absence of privileged primitives.

## The options

| Option | Isolation | Performance | Author experience | Fits |
|---|---|---|---|---|
| **Data only** (no code) | n/a | n/a | declare, don't code | theme, config, layout, content |
| **In-process native** | none | fastest | best (native tools) | first-party or fully vetted code |
| **Embedded interpreter** | moderate | good | good | user automation, scripting |
| **Sandboxed runtime** (e.g. WASM) | strong, structural | moderate (marshalling) | new toolchain | untrusted third-party code |
| **Separate process** | strongest | IPC cost | moderate | heavy work, crash containment, language mismatch |

## Why the sandboxed runtime is structurally stronger

With a sandboxed runtime, the capability set *is* the import set:

```text
Extension declares capabilities: [content.read, network.outbound]

Host constructs the runtime instance with imports:
  content_read(...)      ← provided
  network_fetch(...)     → provided
  filesystem_open(...)   ← NOT PROVIDED — the function does not exist in the instance

An extension attempting a filesystem call has nothing to call. The capability is
absent by construction, not by policy check.
```

This is why enforcement and sandboxing are usually chosen together: the capability model's chokepoint
becomes the runtime's import graph, and bypassing it is impossible rather than forbidden.

WASM's own documented use cases include "server-side compute of untrusted code" and "portable and
secure" distribution, which is precisely this role. *(Source: webassembly.org use-cases.)*

**The costs are real:** marshalling at the boundary, a different toolchain for authors, and a bounded
capability set that may not cover everything a native extension could do.

## Why a separate process is sometimes better

| Advantage | Detail |
|---|---|
| Crash containment | the extension dies; the host survives |
| Memory isolation | no shared address space; no cross-extension interference |
| Language freedom | the extension may be written in anything |
| Resource limits | CPU, memory and file descriptors are enforceable per process |
| Debuggability | standard process tooling applies |

**Costs:** IPC serialisation, process lifecycle management, and harder synchronous call patterns. It
fits work that is heavy, blocky, or likely to misbehave.

## Choosing per extension class

The rule from Decision Tree 3: **decide per class, not once for the platform.** A theme is data; a
build step runs code with real consequences.

```text
Class                    Isolation              Why
─────────────────────────────────────────────────────────────────────────
theme / appearance       data-only              no code executes
content provider         sandboxed runtime      untrusted code, contained capability set
build / transform step   separate process       heavy work, crash containment matters
integration / connector  sandboxed runtime      network access must be capability-gated
automation / scripting   embedded interpreter   user-authored, moderately trusted
first-party native       in-process             trusted, performance-critical (state it)
```

**One model for all classes is always wrong** — either too slow for the light classes or too weak for
the heavy ones.

## The in-process case, and what it requires

In-process is legitimate — for first-party code, or for a class where the platform deliberately accepts
full trust. If you choose it for anything third-party, three conditions must hold:

1. **No privileged primitive is reachable.** The extension cannot obtain a raw handle, socket, or host
   pointer by any route, including reflection, FFI, or a transitive dependency.
2. **The capability chokepoint is genuinely unavoidable** (see `capability-model.md`).
3. **A crash is contained** — panic isolation, or an explicit acceptance that an extension crash is a
   host crash.

**Condition 1 is the hard one**, and it is why in-process native extension models in practice end up
granting near-full trust. If you cannot verify condition 1 by test, you do not have it.

## Resource limits

Isolation from *capabilities* is one axis; isolation from *resource exhaustion* is another. A malicious
or buggy extension can harm by consuming.

| Resource | Limit | Enforced by |
|---|---|---|
| CPU time | per invocation or per window | the sandbox runtime, or the process scheduler |
| Memory | a ceiling per extension | the runtime, or OS limits per process |
| Wall-clock | a timeout on every host-to-extension call | the host |
| Output size | a maximum for data returned | the marshalling boundary |
| Concurrent invocations | a cap per extension | the host |

**The call-timeout is the one most often missing.** A host that calls into an extension synchronously
with no timeout has given that extension control of its own responsiveness.

## Failure containment

| Failure | In-process | Sandboxed | Separate process |
|---|---|---|---|
| Extension panics | host may crash | contained; the instance is discarded | the process dies; host unaffected |
| Extension loops forever | host hangs | timeout + terminate | timeout + kill |
| Extension leaks memory | host leaks | bounded by the instance | bounded by the process |
| Extension corrupts data | host memory | only its own instance state | only its own process |
| Extension is malicious | full host authority (if unenforced) | capability-bounded | capability-bounded + OS-bounded |

**The design requirement:** every failure must have a containment story, and the story must be *tested*
by deliberately causing that failure.

## Testing isolation

```text
For each extension class, write a hostile test extension that:
  1. Attempts an unrequested capability            → must fail at the chokepoint
  2. Attempts to reach a raw primitive             → must be impossible
  3. Loops forever                                 → must be terminated by the timeout
  4. Allocates without bound                       → must hit the memory limit
  5. Panics / crashes                              → must be contained
  6. Returns enormous output                       → must be bounded
  7. Attempts to observe another extension's state → must be impossible
Run this suite per class, and re-run it when the isolation mechanism or version changes.
```

An isolation model that has never been attacked is an assumption. The hostile test extension is how the
assumption becomes a verification.

## Checklist

- [ ] The isolation mechanism is named per extension class, not chosen once for the platform (R5)
- [ ] Untrusted code is never in-process without a verified absence of privileged primitives
- [ ] Sandboxed runtimes are used where structural capability enforcement is required
- [ ] Separate processes are used where crash containment or heavy work requires it
- [ ] Resource limits exist: CPU, memory, wall-clock, output size, concurrency
- [ ] Every host-to-extension call has a timeout
- [ ] Every failure mode has a containment story that has been tested
- [ ] A hostile test extension suite exists and runs per class
- [ ] The isolation decision and its performance cost are recorded, not assumed
