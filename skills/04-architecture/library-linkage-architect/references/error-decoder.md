# Error Decoder — Long Form

<!-- DEEP: 5+min -- the symptom catalogue in long form, with causes and fixes -->

The compressed table lives in `SKILL.md`. This file carries the full diagnosis.

## 1. A CVE in a dependency forces an emergency rebuild

**Symptom:** an advisory lands and within hours the team is rebuilding not just the dependency but
every product that embeds it. Release schedules slip; someone asks whether the fix can wait.

**Mechanism:** static linkage bound the fix to the product's release cycle. The remediation path was
never named, so it was never measured, and the first execution of it happens under pressure.

**Diagnosis:** answer three questions — how many consumer binaries contain the vulnerable library?
How long does each take from patched source to protected users? Who executes that?

**Fix:** convert to dynamic linkage where the platform or a package channel can patch once, or accept
static and publish the measured exposure window as an explicit decision. Rehearse the path so the
second execution is not improvised.

**Recurrence guard:** every dependency carries an update model and a rehearsed window (R2, CR2).

## 2. Two libraries load and one calls the wrong function

**Symptom:** behaviour is subtly wrong, with no error and no crash log. Two features interact in a way
that makes no sense from the source.

**Mechanism:** a flat symbol namespace plus a generic exported name. The loader bound the first
definition it found, and the second library's callers got it.

**Diagnosis:** dump the exported symbols of everything in the process and look for duplicates.

```bash
nm -D --defined-only liba.so libb.so | awk '{print $3}' | sort | uniq -d
```

**Fix:** hidden visibility by default, prefixed exported names, a collision test over the real
co-load set.

**Recurrence guard:** the collision test is a pipeline gate (CR7).

## 3. A caller crashes after a "compatible" library upgrade

**Symptom:** the library released a patch version with a new field, the build was green, and a
consumer corrupts memory or reads garbage.

**Mechanism:** the caller allocates the struct, so adding a field moved data outside the caller's
allocation — or overlapped the following field. The compiler accepted both sides, because they were
compiled against different headers.

**Diagnosis:** compare the struct layout between versions; look for a public struct the caller
constructs.

**Fix:** make the type opaque with accessors, or reserve space. Add an ABI diff so the next such
change fails the build.

**Recurrence guard:** opaque boundaries plus an automated ABI check (CR4, CR9).

## 4. The application will not start after a dependency update

**Symptom:** the loader reports a missing library; nothing starts. Or worse, an older library is
found silently and the app misbehaves.

**Mechanism:** a soname or search-path change moved resolution. The name the loader uses changed, and
the build worked because the developer's environment differed from the target's.

**Diagnosis:** trace resolution on the target (`LD_DEBUG=libs`, or the platform equivalent), and
compare with the build environment.

**Fix:** version the soname deliberately and only on a real incompatibility; pin the search path with
`rpath` rather than relying on the environment; add a load test to the pipeline.

**Recurrence guard:** a load test on the real target per release (CR8).

## 5. A plugin cannot be replaced without restarting the host

**Symptom:** updating a plugin requires a full restart; users lose session state; the update flow is
unpopular.

**Mechanism:** the design assumed `dlclose` unloads reliably. In practice the reference count does not
reach zero (callbacks registered, TLS in use, another load referencing it), or the library refuses to
unload.

**Diagnosis:** after `dlclose`, check whether the library is still resident (`RTLD_NOLOAD` probes for
this).

**Fix:** load a versioned unit under a new path and route new work to it, accepting bounded resident
versions. Record the accepted risk if unload is genuinely required.

**Recurrence guard:** the unload decision is recorded per load site (CR12).

## 6. The executable is enormous and starts slowly

**Symptom:** binary size in the hundreds of megabytes; cold start dominated by paging and
initialisation. Container images are large; deploys are slow.

**Mechanism:** everything statically linked. Apple's guidance is explicit: "Linking many static
libraries into an app produces large app executable files. Applications with large executables suffer
from slow launch times and large memory footprints."

**Diagnosis:** measure the binary size and the load/start time; attribute the size to specific
units.

**Fix:** move optional, non-launch-critical units to dynamic linkage and load on demand. Hand the
measurement to `app-launch-performance-engineer` before and after.

**Recurrence guard:** binary size and load time are tracked per release.

## 7. A tool cannot run in a minimal container

**Symptom:** the static binary does not run in a scratch or distroless image; the dynamic one works
where glibc exists, and neither works everywhere.

**Mechanism:** the two forms have opposite requirements. Static needs no runtime but may need target
libraries for some features; dynamic needs the loader and the exact libraries present.

**Diagnosis:** run the artefact in the actual minimal image, not on the build host.

**Fix:** use static for truly minimal targets (state the constraint), or adopt a base image with the
runtime and pin the library versions.

**Recurrence guard:** each shipping target's runtime availability is recorded (CR3, CR13).

## 8. First-use latency spikes with no startup cost

**Symptom:** startup looks excellent in CI; users report stutter the first time they open a feature.
It never reproduces on the second open.

**Mechanism:** lazy binding spread symbol resolution into first call. The resolution exists either
way; it just happens where the user notices it.

**Diagnosis:** measure first-call latency on the specific interactive path, not only startup.

**Fix:** eager binding for that library or that binary, so the cost lands in startup predictably.

**Recurrence guard:** binding mode is chosen and recorded per library (CR11).

## 9. A forked child hangs intermittently

**Symptom:** the child process hangs under load; the parent is fine; it never reproduces in testing.

**Mechanism:** the child inherited the parent's mutex states, including a lock held at fork time, with
no thread in the child to release it. Only async-signal-safe calls are permitted in the child before
`exec`.

**Diagnosis:** look for library initialisation before the fork that takes an internal lock, and for
non-async-signal-safe calls in the child.

**Fix:** do nothing before `fork()` that is not required; use `pthread_atfork` handlers where
unavoidable as a workaround, not a design.

**Recurrence guard:** the pre-launch safety checklist is applied whenever a library is added
(CR12-adjacent; see `process-safety.md`).

## 10. A second consumer cannot use the library without recompiling

**Symptom:** the library "works", but every change is a source change for consumers; there is no
binary compatibility story.

**Mechanism:** no ABI policy. With one consumer the library is a component; on the second it becomes a
contract, and the contract was never written.

**Diagnosis:** is there a declared public surface, a versioning rule, and a breaking-change list?

**Fix:** declare the ABI, set visibility, keep symbols stable within a major version, and provide a
deprecation window.

**Recurrence guard:** the ABI policy is a release checklist item (CR4).

## 11. An incompatible plugin crashes instead of failing cleanly

**Symptom:** an old plugin is loaded by a new host and the host crashes.

**Mechanism:** no version probe. The host called an API function directly, whose signature or
behaviour had changed.

**Diagnosis:** does every load site call a version function before anything else?

**Fix:** export and call `plugin_abi_version()` first; refuse a mismatch with a clear message.

**Recurrence guard:** the version probe is part of the ABI contract (CR4, `plugin-abi.md`).

## 12. A platform review rejects the artefact

**Symptom:** a release is blocked because the app loads code, bundles a runtime, or uses a
non-permitted interface.

**Mechanism:** the channel's constraint was never checked; the design was chosen on engineering
grounds alone (R6).

**Diagnosis:** is there a recorded platform-constraint answer per target, with a date and a source?

**Fix:** confirm the rules per target before choosing a form; redesign within the permitted set where
necessary.

**Recurrence guard:** the constraint record is part of the linkage decision (CR13).

## 13. A static initialiser fails in a small fraction of launches

**Symptom:** rare launch-time failures, environment-dependent, invisible in testing.

**Mechanism:** a static initialiser touched the filesystem, network or environment before it was
ready, and the ordering between translation units is unspecified.

**Diagnosis:** grep for global objects whose constructors do I/O; launch with a minimal environment.

**Fix:** explicit initialisation from `main`, or lazy once-guarded access; make each initialiser
independently valid.

**Recurrence guard:** the pre-launch safety checklist (CR3-adjacent; see `process-safety.md`).

## 14. A dependency's licence turns out to forbid the chosen form

**Symptom:** legal review blocks a release because the licence does not permit the linking or
distribution model in use.

**Mechanism:** licence terms were checked for *use* and not for *distribution form* (C4). Some
licences distinguish, and modification (which static incorporation or subsetting may constitute) is
sometimes forbidden.

**Diagnosis:** re-read the licence against the actual form: static incorporation, dynamic linking,
redistribution, modification.

**Fix:** change the form, or obtain a different grant, or replace the dependency.

**Recurrence guard:** the licence is confirmed as part of form selection, with `dependency-governance`
(CR3).

## The triage rule

Three of these symptoms — undeclared boundaries, unstated update models, and absent ABI policy — are
detectable in minutes with a symbol dump and three questions, and they account for most linkage
failures that reach production. Run the detection sweep in `anti-patterns.md` first; escalate to the
deeper diagnosis only when the sweep is clean.
