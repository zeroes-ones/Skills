# Boundary Justification

<!-- STANDARD: 3min -- when to cross a language boundary, and the alternatives -->

## The question the expert asks first

Not "how do we cross?" but **"must we?"** A language boundary is permanent: a second toolchain, a
second CI path, a safety surface that must be reviewed, and a place where the compiler stops checking
your invariants. It should be justified, not assumed.

This is R6.

## The four legitimate reasons

| Reason | What it means | How to verify it |
|---|---|---|
| **A library exists only in the other language** | the capability is not available in your language | check whether a native equivalent exists first |
| **Measured performance** | the other language is materially faster for this workload | **measure it** — the claim is the justification |
| **Organisational** | an existing team owns the code | state it; the cost is political and real |
| **Platform requirement** | an OS API, driver or plugin host demands it | no choice; document the constraint |

The second row is the one that fails most often: FFI is chosen for anticipated speed and delivers a
per-crossing cost that exceeds the gain.

## The alternatives, before FFI

| Alternative | When it wins |
|---|---|
| **A native library in your language** | usually available; check before assuming otherwise |
| **A service boundary** (sidecar, microservice) | the work is coarse-grained; isolation matters; language freedom matters |
| **A subprocess** | the work is batchy; crash containment matters; the interface is simple |
| **A managed rewrite** | the code is small, or the ecosystem has caught up |
| **A data format instead of a call** | the exchange is a file, a stream or a message |
| **A sandboxed runtime** (e.g. WASM) | you need portability and isolation more than raw speed |

**The service boundary is the most under-considered.** A subprocess or a service moves the boundary to a
process edge, where the failure modes are well-understood (timeouts, retries, serialisation) instead of
memory-unsafe ones. For coarse work it is almost always the safer choice.

## The cost of a boundary, itemised

| Cost | Detail |
|---|---|
| **Per-crossing overhead** | conversion, allocation, copy, guard acquisition — paid every call |
| **A second toolchain** | build system, CI, packaging, platform quirks |
| **A second dependency graph** | two ecosystems to keep patched (see `dependency-governance`) |
| **A safety surface** | every `unsafe` region is a review and a potential exploit primitive |
| **A debugging surface** | cross-language debugging is materially harder |
| **A permanence** | the boundary is hard to remove once shipped |
| **A staffing surface** | the team must hold competence in both languages |

## Measuring the performance claim

The claim must be measured, not assumed:

```text
1. Build a micro-harness that measures ONE crossing in isolation.
     - empty call (the ABI overhead floor)
     - typical call (real arguments, typical size)
     - the operation's actual work in pure language A
     - the operation's actual work in pure language B
2. Compare: does FFI + B beat pure A?
     - if the per-crossing cost exceeds the gain, FFI loses regardless of B's speed
3. Then measure end-to-end, because the boundary's share in a real workload may be small.
```

**The two numbers that decide it:** the *per-crossing cost* and the *crossings per operation*. A cheap
crossing called a million times is expensive; an expensive crossing called once is irrelevant.

## The decision

```text
Is the capability available natively?
├── Yes → do not cross. (Most common outcome.)
└── No ↓
    Is the work coarse-grained (batch, file, stream)?
    ├── Yes → consider a subprocess or service boundary FIRST
    │   └── Cheaper failure modes; language freedom; isolation
    └── No (fine-grained, latency-sensitive) ↓
        Is the performance claim measured?
        ├── No → measure it before deciding (R2, R6)
        └── Yes, and FFI wins ↓
            Is the boundary's blast radius acceptable?
            ├── Yes → cross, with the full contract (ownership, errors, threads)
            └── No  → reconsider; a memory-safety defect at the boundary may be an exploit
```

## When FFI is genuinely right

| Situation | Why FFI wins |
|---|---|
| A hardware or OS API with no binding | there is no alternative |
| A numerically intensive kernel called in a tight loop | per-crossing cost amortised over substantial work |
| A platform SDK required by the product | platform constraint |
| An existing, large, tested native library | rewriting it costs more than the boundary |
| A plugin host that requires native extensions | the host defines the boundary |

## When FFI is wrong, and what to do instead

| Situation | Better |
|---|---|
| "It might be faster" | benchmark first; often the same or worse |
| A few hundred calls a day | a subprocess or a CLI invocation |
| A coarse batch job | a service boundary |
| A small utility | rewrite it; the ecosystem may already have it |
| A one-off script | keep it in one language |
| A library you could vendor in your language | vendor that instead |

## Recording the decision

| Field | Example |
|---|---|
| Capability | image resampling kernel |
| Native alternative? | the pure-language version is 8× slower `[VERIFIED]` |
| Coarse or fine? | fine-grained — called per tile, thousands per image |
| Per-crossing cost | 0.9 µs empty, 4.1 µs typical `[VERIFIED]` |
| Work per crossing | 2.3 ms — the boundary is 0.18% of the call |
| Verdict | FFI justified; the boundary cost is negligible against the work |
| Boundary cost accepted | second toolchain (Rust), CI path per platform, one `unsafe` region |

The last row matters: the performance case is made, and the *non-performance* costs are still
acknowledged rather than ignored.

## Checklist

- [ ] A native equivalent was checked for and is genuinely unavailable
- [ ] The work's granularity is stated (coarse or fine)
- [ ] A subprocess or service boundary was considered and rejected with a reason
- [ ] Any performance claim is measured per crossing, and end to end
- [ ] The crossings-per-operation count is known
- [ ] The non-performance costs are acknowledged: toolchain, dependencies, safety, debugging, staffing
- [ ] The decision is recorded with its numbers, not just its conclusion
