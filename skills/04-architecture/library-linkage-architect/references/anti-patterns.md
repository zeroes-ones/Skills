# Anti-Patterns

<!-- STANDARD: 3min -- the linkage anti-pattern catalogue with detection heuristics -->

## 1. Default-by-template

**Symptom:** nobody can say why the library is static or dynamic; it was whatever the scaffold did.
**Cause:** linkage treated as a build detail rather than an architecture decision (R1).
**Detection:** ask three engineers; if the answers differ, there is no decision.

```bash
# Is there any recorded linkage decision anywhere?
find . -iname "*linkage*" -o -iname "*abi*policy*" -o -iname "*decision*record*" | head
```

**Fix:** record the form, the four constraints, and the reason per unit.

## 2. Unstated update model

**Symptom:** a CVE forces an unplanned rebuild across every consumer.
**Cause:** the remediation path was never named (R2).
**Detection:** ask "how does a fix in this dependency reach users?" — hesitation is the finding.

**Fix:** name the model, measure the exposure window, rehearse the path.

## 3. Everything exported

**Symptom:** a wrong function is called, or an internal helper becomes load-bearing for a consumer.
**Cause:** no visibility control (R5).
**Detection:**

```bash
# Count exported symbols; a large number for a small library is the signal
nm -D --defined-only libfoo.so 2>/dev/null | wc -l
```

**Fix:** hidden by default, an explicit export list, prefixed names, a collision test.

## 4. Public structs and published vtables

**Symptom:** a "compatible" upgrade corrupts callers.
**Cause:** the caller allocates the layout, so any addition is breaking (R3).
**Detection:** a public header exposing a struct the caller constructs, or a base class with virtual
methods, and no reserved space.

**Fix:** opaque types with accessors, or reserved fields/slots.

## 5. Compiles-equals-compatible

**Symptom:** an ABI break ships because the build was green.
**Cause:** no ABI diff; compatibility asserted by review.
**Detection:** is there a symbol-inventory file in the repo, and is it diffed in CI?

**Fix:** a committed export list, diffed per release, plus a structural ABI check where the consumer
count warrants it.

## 6. Reload-by-unload

**Symptom:** a plugin cannot be replaced without restarting the host.
**Cause:** the design assumed `dlclose` unloads reliably (R4).
**Detection:** a plugin lifecycle that mentions unload, with no statement of the risk.

**Fix:** version the unit and load a new path; accept bounded resident versions.

## 7. Untested second form

**Symptom:** the static build breaks the first time someone needs it.
**Cause:** two forms offered, one built in CI.
**Detection:** does the pipeline build every offered form?

**Fix:** build and test both, or ship one.

## 8. Vendored copy shadowing the system library

**Symptom:** the team believes the dependency is platform-patched; it is not.
**Cause:** a vendored copy earlier in the load path wins resolution.
**Detection:** trace what actually loads (`LD_DEBUG=libs` or the platform equivalent) rather than
reading the build file.

**Fix:** remove the vendored copy, or stop claiming platform patchability.

## 9. Lazy binding on a user-triggered path

**Symptom:** the first tap on a feature stutters; startup looks fine.
**Cause:** resolution cost deferred into first use, on the exact path the user notices.
**Detection:** measure first-call latency on interactive paths, not just startup.

**Fix:** eager binding for that library, or pre-warm the path.

## 10. Work before `fork()`

**Symptom:** intermittent child hangs.
**Cause:** a lock held across `fork()`, or a non-async-signal-safe call in the child.
**Detection:** is anything initialised before the fork that takes a lock or starts a thread?

**Fix:** do no work before `fork()`; only async-signal-safe calls in the child until `exec`.

## 11. Static initialiser depending on another

**Symptom:** a rare launch failure, only in some environments.
**Cause:** cross-unit initialisation order is unspecified.
**Detection:** grep for global objects with constructors that touch the filesystem, network or
environment.

**Fix:** explicit initialisation, or lazy once-guarded access.

## 12. Generic exported names

**Symptom:** a symbol collision with another library in the same process.
**Cause:** unprefixed `extern "C"` names (`init`, `close`, `read`).
**Detection:**

```bash
nm -D --defined-only libfoo.so 2>/dev/null | awk '{print $3}' \
  | grep -xE 'init|close|read|write|open|create|destroy|get|set|error|version|config'
```

**Fix:** prefix every exported symbol with the library name.

## 13. Runtime loading of mandatory code

**Symptom:** a crash when the load target is missing; nobody tested the absent case.
**Cause:** a required dependency implemented as an optional load.
**Detection:** for each load site, is the absence handled? If the product cannot function without it,
it is not optional.

**Fix:** link it at build time, or design and test the absent state.

## 14. No version probe

**Symptom:** an incompatible plugin crashes instead of failing cleanly.
**Cause:** the ABI version is not queried before use (R3).
**Detection:** `dlsym` calls that go straight for an API function rather than a version function.

**Fix:** export and call a version function first; refuse on mismatch.

## 15. Platform rule discovered late

**Symptom:** a design that depends on runtime loading or a bundled runtime is rejected at review.
**Cause:** the channel's constraint was never checked (R6).
**Detection:** is there a recorded platform-constraint answer per target, with a date?

**Fix:** confirm per target before choosing the form.

## Detection sweep

```bash
SRC="${1:-src}"

echo "== runtime loading sites =="
grep -rnE 'dlopen|LoadLibrary|dlsym|Library\.load|require\(.*\.node' "$SRC" 2>/dev/null | head || echo "  none"

echo "== version probe present for each load? =="
grep -rn 'abi_version\|_api_version\|api_version(' "$SRC" 2>/dev/null | head || echo "  NONE — no version probe found"

echo "== visibility control in the build =="
grep -rnE 'fvisibility|__declspec\(dllexport\)|version-script|export_dynamic' . --include='*.cmake' --include='CMakeLists.txt' --include='*.mk' --include='Makefile' --include='*.toml' 2>/dev/null | head || echo "  NONE — default (broad) export likely"

echo "== committed symbol inventory =="
find . -iname 'exported-symbols*' -o -iname 'abi-*.txt' -o -iname '*symbols*.map' 2>/dev/null | head || echo "  none"

echo "== ABI diff in the pipeline? =="
grep -rnE 'abi-compliance|abi-dumper|abi-diff|cargo-public-api|japicmp|revapi' .github/workflows/ 2>/dev/null | head || echo "  none"

echo "== unload references (check each is justified) =="
grep -rnE 'dlclose|FreeLibrary' "$SRC" 2>/dev/null | head || echo "  none"

echo "== generic exported names =="
# run against built artefacts, not source:
# nm -D --defined-only build/libfoo.so | awk '{print $3}' | grep -xE 'init|close|read|write|open'
echo "  (run against a built library)"

echo "== static initialisers touching the environment =="
grep -rnE '^\s*(static|const)\s+\w+\s+\w+\s*\{' "$SRC" 2>/dev/null | head || echo "  none obvious"

echo "== linkage/ABI decision record =="
find . -iname '*linkage*' -o -iname '*abi-policy*' 2>/dev/null | head || echo "  NONE — no recorded decision"
```

Interpretation: **no version probe**, **no visibility control** and **no recorded decision** are each
standalone findings in a shipped library — they are the three cheapest rules to apply and the three
most often skipped.
