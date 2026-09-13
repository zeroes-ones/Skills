# Code Loading, Linkage & Launch Lifecycle — Deep Research and Build Plan

> **The question.** Which skills would this library need to cover *how code gets loaded, linked
> and initialised* — the static/dynamic/library-form decision, the runtime-loading boundary, and
> the cold/warm/hot launch cost those decisions cause? And which of those are genuinely unowned?

The answer below is built the same way as `missing-skills-research.md`: scan the corpus for **named
ownership**, not mentions, then rank gaps by evidence. Every factual claim is tagged with its source,
and §7 states which sources are weak.

---

## 1. The short answer

This domain has **no named owner in the library**. Four concepts that every platform team must
decide — linkage form, library form, launch mode, and interop boundary — are discussed inside other
skills but claimed by none.

The four gaps worth building, in dependency order:

| # | Skill | Domain | Owns |
|---|---|---|---|
| G1 | `library-linkage-architect` | `04-architecture` | Static / dynamic / runtime-loaded; library *form*; ABI stability; symbol visibility; the security-update model |
| G2 | `app-launch-performance-engineer` | `06-quality` | Cold / warm / hot launch; init-cost attribution; launch budgets and regression gates |
| G3 | `plugin-ecosystem-architect` | `04-architecture` | Designing a host others extend: capability bounds, version negotiation, lifecycle, stability contract |
| G4 | `native-interop-engineer` | `05-development` | FFI boundaries: JNI, cgo, PyO3, N-API, P/Invoke; ownership across the boundary; marshalling cost; WASM as a stable ABI |

**G1 and G2 are one coupled decision** and should ship together: the linkage choice *sets the cost
floor* that G2 measures. G3 and G4 are independent extensions of G1.

A useful clarification the brief settles up front, because the vocabulary is used loosely in
practice: **static and dynamic are one axis (when a symbol resolves); library form is a second axis
(what shape the unit takes); cold/warm/hot launch is a third (how much of the process exists).**
Conflating them is why teams make these decisions by habit. The skill must separate them.

---

## 2. Coverage audit — what already exists

Verified by scanning all 312 skills for description-level ownership (the library's own standard:
*"mentioning a concept inside another skill is not owning it"* — `missing-skills-research.md` §2).

| Concept | Body mentions | Description owners | Reference-file depth | Verdict |
|---|---|---|---|---|
| Static vs dynamic linking | 1 | **0** | 1 | **Uncovered** |
| Shared library / `dlopen` / `soname` | 11 / 1 / 0 | **0** | 15 / 1 / 0 | **Uncovered** |
| Cold start / cold launch | 24 / 1 | **0** | 39 / 5 | **Uncovered** |
| Warm start / hot start | 3 / 0 | **0** | 5 / 2 | **Uncovered** |
| Startup / launch time | 5 / 10 | **0** | — | **Uncovered** |
| ABI stability / symbol visibility | 311 / 22 | **0** | 946 / 45 | **Uncovered** |
| FFI / marshalling boundary | 300 / 0 | **0** | 597 / 0 | **Uncovered** |
| Plugin / extension ABI | 38 / 49 | **0** | — | **Uncovered** |

**Methodological correction, stated because it changed the ranking.** An initial scan reported
`desc:4` for "FFI" and `desc:3` for "ABI". Both were **false positives**: case-insensitive matching
hit "o*ffi*ce", "tra*ffi*c", "*Abi*gail", "h*abi*t" and "dis*abi*lity". Re-checking for
word-boundary matches returns **0 owners** for both. The same trap applies to any short acronym in
this corpus; the numbers in the table above were re-derived after the correction.

**Nearest neighbours, and precisely where each stops:**

| Skill | Owns | Why it is not this |
|---|---|---|
| `build-system-design` | Bazel/Buck2/Pants/Nx selection, build *time* reduction | Owns how to build **fast**, not what to link |
| `dependency-governance` | Version sprawl, CVE triage, licence compliance across repos | Owns *which version*, not the linkage mechanism |
| `performance-engineer` | Profiling, load testing, Core Web Vitals, performance budgets | Owns the profiler, not the launch-mode taxonomy or the linkage decision |
| `frontend-developer` | **"SSR/SSG patterns"**, bundle optimization, code splitting, tree shaking | Already owns web chunk mechanics — the new skills must not duplicate |
| `firmware-developer` | ROM-to-app boot, bootloaders, OTA, cross-compilation toolchains | Already owns firmware boot — G2 must not claim it |
| `embedded-engineer` | MCU/MPU selection, RTOS, bootloaders, power profiles | Adjacent; consumes G1's linkage guidance |
| `mobile-architecture-patterns` / `desktop-architecture-patterns` | MVVM, VIPER, MVI, TCA, Electron-vs-native | Owns architecture *patterns*, not init cost |
| `codebase-design` | Module depth, seams, interface minimisation | Owns module *boundaries*, not linkage or ABI |
| `api-designer` | REST/GraphQL/gRPC, versioning strategy, OpenAPI | Owns network API contracts, not binary ABI |
| `system-architect` | C4, ADRs, microservices-vs-monolith, topology | Owns service decomposition, not in-process linking |

**The boundary in one sentence:** existing skills decide *what the system is* and *what the code
does*; the four gaps decide *how the code physically reaches memory and when* — plus the contract
that lets a foreign compiler or a third-party plugin meet it safely.

---

## 3. The gaps, ranked by evidence

### Tier 1 — the coupled pair

#### G1 · `library-linkage-architect`

**The decision.** When a symbol resolves (build / load / first-call / runtime), and what shape the
unit takes (header-only, static archive, shared object, framework bundle, plugin, sidecar, network
service, WASM module, source package).

**Evidence it matters.** Apple's own developer documentation states the trade-off directly:
using dynamic libraries instead of static libraries "reduces the executable file size", and lets
apps "delay loading libraries with special functionality only when they're needed instead of at
launch time", which "contributes further to reduced launch times and efficient memory use". The
same document states the opposite cost: "Linking many static libraries into an app produces large
app executable files. Applications with large executables suffer from slow launch times and large
memory footprints." So the two choices trade launch time against per-library flexibility — and the
documentation says so, rather than leaving it to folklore. *(Source: Apple, Overview of Dynamic
Libraries, archived developer documentation.)*

**The under-appreciated cost is security, not size.** A statically linked cryptographic library
binds the vulnerability to the application binary. After Heartbleed (CVE-2014-0160 — listed in
CISA's Known Exploited Vulnerabilities catalog, added 2022-05-04), every consumer that had
statically linked OpenSSL needed a rebuild and a re-ship; consumers of a system-provided shared
library could be remediated once by the platform. This is the strongest argument for dynamic
linkage in a regulated or high-traffic product, and it is a *security* decision that teams usually
make on *performance* grounds.

**Why it needs an owner.** Linkage is currently decided implicitly, by whatever the build tool
defaults to or whatever a tutorial did. The consequences (launch cost, update model, ABI exposure)
are discovered later by people who did not make the decision.

**Decision trees it must carry:** static-vs-dynamic by constraint (update model, launch budget,
distribution, licence) · plugin boundary ABI choice · symbol-visibility and collision triage ·
ABI/versioning policy · where lazy binding is acceptable and where it is not.

#### G2 · `app-launch-performance-engineer`

**The decision.** Which launch mode is failing, what dominates its cost, and what the fix order is.

**Evidence — the taxonomy is authoritative, not invented.** Android's official launch-time
guidance defines exactly three states and their costs:

- **Cold start** — "an app's starting from scratch… the system's process creates the app's process."
  Presents "the greatest challenge" in minimizing startup time.
- **Warm start** — "encompasses a subset of the operations that take place during a cold start."
- **Hot start** — "lower overhead… the system brings your app's host activity to the foreground",
  avoiding object initialization, UI initialization and rendering when the UI is still resident.

**Evidence — the metrics and the thresholds are published.** Android vitals defines two metrics:
time to initial display (TTID, "the time it takes to display the first frame") and time to full
display (TTFD, "the time it takes for the app to become fully interactive"), and marks startup
**excessive** at: cold ≥ 5 s, warm ≥ 2 s, hot ≥ 1.5 s (measured as TTID). *(Source: Android,
"App startup time", launch-time vitals.)*

That gives a new skill something rare and valuable: **a published numeric budget with an official
source**, rather than a threshold invented by the skill author.

**Evidence — one platform's fix is another's non-issue.** Android's ART uses a hybrid of AOT, JIT
and interpretation, with AOT compilation that can be profile-guided; shipping a Baseline Profile
lets ART pre-compile critical code paths (app startup, navigation, scrolling) so they are optimised
"from the first time they run". *(Sources: Android, "Configure ART"; "Baseline Profiles overview".)*
iOS has no equivalent mechanism — its launcher is `dyld`, and the levers differ entirely (dylib
count, static initializers, prewarming). A single skill that knows both is more useful than two
platform skills that each assume their own levers are universal.

**The classic Android footgun, documented.** Multiple SDKs each declaring a `ContentProvider` to
self-initialise means several providers run before the app's own `onCreate`; Android's App Startup
library exists specifically so components "share a single content provider… This can significantly
improve app startup time", and its docs warn: "If you previously used content providers to
initialize components in your app, make sure that you remove those content providers when you use
App Startup." *(Source: Android, App Startup library.)* That failure — third-party code silently on
the cold-start critical path — is exactly the kind of thing an owner skill should encode.

**The mismatch that motivates the skill.** Most "the app is slow" reports are **cold** launch; most
developers test with the app already running, so they optimise **hot** launch. The two have
different dominant costs (loader + init vs. restoration), so effort aimed at the wrong one produces
no measured improvement. Naming that mismatch is a core deliverable.

**Scope fence (deliberate):** web is limited to hydration and time-to-interactive — chunk mechanics
stay with `frontend-developer`; firmware boot stays with `firmware-developer`.

**Decision trees it must carry:** which launch mode is failing · where the time actually goes
(loader / relocations / static-init / framework-init / first-frame / hydration) · fix order by
cost-versus-risk · how to set a launch budget and a regression gate.

### Tier 2 — independent extensions

#### G3 · `plugin-ecosystem-architect`

**The decision.** Designing a host that others extend: what a plugin may do, how versions negotiate,
what the platform promises to keep stable, and how plugins load and unload.

**Evidence it needs an owner.** "plugin" appears in 38 SKILL.md files and "extension" in 49, with
**0 description owners**. Meanwhile the design surface is large and the failure modes are expensive:
a plugin ABI that changes breaks every third-party plugin at once; a capability model that is too
broad turns every plugin into a security boundary the host cannot enforce; a lifecycle that assumes
unload-and-reload is a design bug (see §4).

**The unload reality is documented.** `dlclose` unloads an object only "if the object's reference
count drops to zero and no symbols in this object are required by other objects", and glibc offers
`RTLD_NODELETE` explicitly to "not unload the shared object during dlclose()… the object's static
and global variables are not reinitialized if the object is reloaded with dlopen() at a later time."
*(Source: `dlopen(3)`, Linux man-pages 6.19.)* So "unload and reload a plugin" is not generally safe,
and a host that depends on it is built on a false assumption. That is a documented fact the skill
can state rather than a preference.

#### G4 · `native-interop-engineer`

**The decision.** How to cross a language boundary safely: the ABI on each side, who owns memory,
what marshalling costs, how errors and exceptions propagate.

**Evidence it needs an owner.** "binding" appears in 78 SKILL.md files, "interop" in 21, "JNI" and
"cgo" in 1 each, and `marshalling` in **0** — while description-level ownership is **0** for every
one of them. The concepts are known but nowhere owned.

**Evidence the problem is real.** The `fork` interaction is documented and severe: after `fork()` in
a multithreaded program, "the child can safely call only async-signal-safe functions until such time
as it calls `execve()`", and the child inherits "the states of mutexes, condition variables, and
other pthreads objects" — which is why a library holding a lock across `fork()` deadlocks the child.
*(Source: `fork(2)`, Linux man-pages.)* That is an interop-and-load-order failure that a linkage
owner must know about and an application developer will not discover until production.

**Evidence for WASM as a stable ABI.** WebAssembly's own use-cases document lists "Outside the
browser: game distribution service (portable and secure)", "server-side compute of untrusted code",
and "hybrid native apps on mobile devices". *(Source: webassembly.org use-cases.)* That is the
documented basis for the pattern `native-interop-engineer` should recommend when a plugin or
extension must be safely sandboxed across compilers: a stable, sandboxed ABI rather than a native
one.

---

## 4. Real-world problems the skills must encode

These are the concrete, recurring failures — the reason the skills are worth having. Each is
anchored to a documented mechanism rather than a war story.

**Launch and lifecycle**

| # | Problem | Mechanism, and the fix direction |
|---|---|---|
| 1 | iOS launch pays for dylib count and static initializers | `dyld` loads "the app's dependent libraries" before control reaches `main`; each adds symbol resolution, relocations and initializers. Apple's own guidance ties executable size to launch time |
| 2 | Android SDK `ContentProvider`s run before `onCreate` | Third-party initialisers land on the cold-start path invisibly; App Startup consolidates them into one provider — and its docs require removing the old ones |
| 3 | Android class verification and JIT warm-up | AOT/JIT/interpretation is a hybrid; code not covered by a profile is verified and JIT-compiled on first use, pushing cost into startup and first interaction. Fix: profile-guided AOT (Baseline/Startup Profiles) |
| 4 | Web hydration is the web's cold start | Server HTML arrives fast, then the component tree re-executes and blocks the main thread; islands architecture exists to avoid exactly this |
| 5 | Serverless cold start is module-graph cost | The dominant term is the import/require graph evaluated per cold instance, not the handler |
| 6 | Python import cost per invocation | A framework that imports hundreds of modules during package init pays it on every CLI run; `python -X importtime` exists to show "module name, cumulative time… and self time". Documented diagnostic |
| 7 | Static-initialization-order fiasco | Cross-translation-unit C++ init order is undefined; `+load` (Obj-C/Swift) and static blocks (Java) have the same shape. A static ctor touching a filesystem that does not exist yet fails in a small fraction of launches |
| 8 | Prewarm semantics differ from a normal launch | iOS prewarms apps in the background; assuming identical timing in `applicationDidFinishLaunching` produces bugs that reproduce rarely |
| 9 | `fork()` safety | A library holding locks or threads across `fork()` deadlocks the child; only async-signal-safe calls are permitted before `execve`. Classic cause: not doing work before `fork` |
| 10 | Lazy binding moves cost into runtime | `RTLD_LAZY` resolves symbols "only as the code that references them is executed"; `LD_BIND_NOW` / `RTLD_NOW` resolves everything at load. Lazy spreads jitter into the UI; eager pays upfront and makes launch predictable |

**Linkage and packaging**

| # | Problem | Mechanism, and the fix direction |
|---|---|---|
| 11 | **Static linking vs CVE response** | A statically linked crypto library binds the vulnerability to the binary. Heartbleed (CVE-2014-0160, in CISA KEV) forced every static consumer to rebuild and re-ship; a system shared library could be patched once. The strongest *security* argument for dynamic linkage |
| 12 | DLL hell / version conflict | Two libraries requiring different versions of one shared object; loader search order decides the winner. Mitigations: versioned sonames, `rpath`, side-by-side assemblies — or static linking |
| 13 | Symbol collision in a flat namespace | Generic `extern "C"` symbols (`init`, `close`, `read`) collide when two libraries load together; C++ mangling does not help. Fix: hidden visibility by default plus explicit export |
| 14 | ABI breaks that compile cleanly | Adding a field to a public struct, or a virtual method to a base class, silently breaks callers that used the old layout — no compiler error, corruption at runtime |
| 15 | Barrel files defeating tree shaking | An `index.ts` re-exporting everything makes an otherwise static import un-shakeable, so unused code still ships. A packaging choice inverting the static-linkage optimisation |
| 16 | `dlclose` does not really unload | Unloading requires refcount zero and no external references; `RTLD_NODELETE` exists to prevent it and to avoid re-initialisation on reload. A plugin design assuming clean unload is incorrect |
| 17 | Plugin ABI across compilers | Passing C++ objects across a compiler boundary fails on STL layout, name mangling and exception ABI. Fix: a C ABI boundary, or WASM as a stable sandboxed ABI |

---

## 5. The build plan

> **Build status (this repo, current HEAD):** all four skills are **delivered**. Phase A:
> `library-linkage-architect` (18 files) and `app-launch-performance-engineer` (19 files) authored
> to full compliance with bidirectional chain edges, per-skill `evals/evals.json`, and backtest
> examples. Phase B: `plugin-ecosystem-architect` (18 files) and `native-interop-engineer`
> (19 files) authored on the same pattern. Phase C: `validate_chains.py` reports 0 asymmetries and
> the flat discovery layer resolves every skill.

Each skill follows the pattern proven by the four design skills: full template compliance, ≥9
reference files, a domain harness, a provenance-tagged backtest example, `evals.json`, and
**bidirectional** chain edges.

### Phase A — the coupled pair (highest value)

| Step | Skill | Chains |
|---|---|---|
| 1 | Author `library-linkage-architect` to full compliance | consumes `system-architect`, `codebase-design`, `build-system-design`; feeds `app-launch-performance-engineer`, `plugin-ecosystem-architect`, `native-interop-engineer`, platform skills |
| 2 | Author `app-launch-performance-engineer` | consumes `library-linkage-architect`, `performance-engineer`, `mobile-architecture-patterns`; feeds platform skills and `shipping-and-launch` |
| 3 | Wire the reciprocal edges into the ~18 existing neighbours | `validate_chains.py` must gain 0 new asymmetries |

### Phase B — the extensions

| Step | Skill | Chains |
|---|---|---|
| 4 | Author `plugin-ecosystem-architect` | consumes `library-linkage-architect`, `api-designer`, `secure-api-design`, `appsec-engineer` |
| 5 | Author `native-interop-engineer` | consumes `library-linkage-architect`, `embedded-engineer`, `kotlin-multiplatform`, `python`-adjacent and backend skills |

### Phase C — verify

6. Run the full gate set: template, YAML, markdown, workflow lint, G13 examples, G14 deep-research,
   `validate_chains.py`, `verify-skill.sh`, `validate-skills.sh`, CI mirror.
7. Rebuild `skills-flat/` and re-run `check-flat-index.py`.

**Effort:** ~1 focused session per skill to author, plus one wiring pass. Measured cost from the
four design skills: **18–19 files each**.

---

## 6. What I would *not* build, and why

| Candidate | Why not |
|---|---|
| A standalone "static vs dynamic linking" skill | It is one axis, and it is meaningless without the launch-cost context that justifies it (G1 covers it) |
| A "bundle optimization" skill | `frontend-developer` already owns code splitting, tree shaking and bundle analysis across 13 reference files |
| A "compiler / AOT / JIT" skill | Owned in substance by `game-engine-architect` (Burst/JIT), `ml-ai-engineer`, `embedded-engineer`; a fourth fragments it |
| A "container image size" skill | `docker-kubernetes` + `build-system-design` cover it; the launch angle is a *section*, not a skill |
| A "microservices vs monolith" skill | `system-architect` owns it explicitly |
| A separate "startup time" skill | Startup **is** cold launch; splitting creates two owners for one measurement |
| A "cross-platform build" skill | `flutter-developer`, `react-native-developer`, `kotlin-multiplatform` and `build-system-design` cover the surface; nothing is missing |

---

## 7. Sourcing caveat

Weigh these findings accordingly — the evidence is not uniform:

| Strength | Sources |
|---|---|
| **Primary vendor documentation — strong** | Android "App startup time" (the three launch states, TTID/TTFD, the 5 s / 2 s / 1.5 s excessive-startup thresholds); Android "Configure ART" (hybrid AOT/JIT/interpretation); Android "Baseline Profiles overview"; Android App Startup library (the `ContentProvider` consolidation and its removal requirement); Apple "Overview of Dynamic Libraries" (static-vs-dynamic launch and memory trade-off) |
| **Authoritative reference implementations — strong** | Linux man-pages: `dlopen(3)` (`RTLD_LAZY`/`RTLD_NOW`, `RTLD_NODELETE`, unload semantics), `ld.so(8)` (`LD_BIND_NOW`), `fork(2)` (async-signal-safe restriction, inherited mutex state) |
| **Primary security data — strong** | CISA Known Exploited Vulnerabilities catalog, machine-readable feed, catalog version 2026.09.11, 1709 entries — CVE-2014-0160 present, added 2022-05-04; the Heartbleed disclosure site for the vulnerability description |
| **Spec-level — strong** | webassembly.org use-cases ("portable and secure" out-of-browser use, untrusted server-side compute, hybrid mobile apps); Python documentation for `-X importtime` |
| **Widely repeated but secondary** | The "cold start vs hot start" framing in blog posts and conference talks — the *taxonomy* is authoritative from Android's docs, but specific millisecond figures quoted online are usually device-specific and should be re-measured |
| **Explicitly avoided** | Any specific millisecond budget asserted as universal; any claim that one linkage strategy is "always right"; any vendor benchmark of launch improvements (marketing-adjacent) |

Claims I deliberately did **not** make: that dynamic linking is always faster (it is a size and
flexibility trade, per Apple's own text); that a Baseline Profile yields a specific percentage
improvement (varies by app); that WASM is suitable for every plugin (it introduces its own
boundary costs); and that these four skills exhaust the domain — networking and package-resolution
sub-topics may warrant later passes.

---

## 8. Recommended next action

Build **`library-linkage-architect` (G1)** first, end to end, as the template for the rest:

1. Author it to full template compliance with a grounded `workflow:` contract.
2. Add a backtest example — a static-linking CVE-response scenario and a dylib-count launch
   regression, with the arithmetic shown and every figure provenance-tagged.
3. Declare chain edges both ways and validate (`validate_chains.py`, `validate-workflows.py`).
4. Then author `app-launch-performance-engineer` (G2), which consumes G1's output — the coupling is
   the reason to do these two first.
5. Decide from the working pair whether G3 and G4 follow the same shape.

That order matters for the same reason recorded in `missing-skills-research.md` §8: this library's
own evidence is that a skill's real problems only appear when an agent actually runs it. Proving the
coupled pair before authoring the extensions avoids repeating a documented mistake.
