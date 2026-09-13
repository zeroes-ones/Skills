# Anti-Patterns

<!-- STANDARD: 3min -- the visibility anti-pattern catalogue with detection heuristics -->

## 1. Surface by exclusion

**Symptom:** a library whose API is "everything not marked private"; the documented surface is much smaller than the real one.
**Cause:** the default modifier was never inverted (R2).
**Detection:** count public declarations against the documented surface.

```bash
# ratio of public to non-public declarations (language-specific)
grep -rc "public " src/**/*.java 2>/dev/null | awk -F: '{s+=$2} END {print "public:", s}'
grep -rc "private " src/**/*.java 2>/dev/null | awk -F: '{s+=$2} END {print "private:", s}'
```

**Fix:** invert the default; publish an explicit list.

## 2. Speculative widening

**Symptom:** public declarations with no consumer outside their own module.
**Cause:** "someone might need it" (R1).
**Detection:** search for references from outside the declaring module.

**Fix:** narrow to the most restrictive that compiles; widen when a real consumer appears.

## 3. Public mutable field

**Symptom:** a changed field breaks callers; a field rename is a breaking change.
**Cause:** the representation was published (R3).
**Detection:**

```bash
grep -rnE "public\s+\w+\s+\w+\s*[;=]" src/ | grep -v final | head
```

**Fix:** a private field and an accessor (or `internal(set)` / `private set`).

## 4. Non-enforcing privacy

**Symptom:** a secret readable at runtime, or reachable from another language.
**Cause:** TypeScript `private` (erased), Kotlin `internal` (Java-permeable), Python `_name` (convention) (R4).
**Detection:** flag every such modifier where the value is sensitive.

```bash
grep -rnE "private\s+\w*(token|secret|key|password)" src/**/*.ts | head   # TS: needs #field
grep -rn "internal " src/**/*.kt | head                                   # Kotlin: Java-permeable
```

**Fix:** the enforcing mechanism (`#field`, a module boundary, a process).

## 5. Test-driven widening

**Symptom:** a declaration is public with "for the tests" as the only reason.
**Cause:** the test mechanism was not used (R5).
**Detection:** public declarations whose only external reference is a test file.

**Fix:** `@testable` / `InternalsVisibleTo` / the test source set / same-package tests.

## 6. Accidental subclassability

**Symptom:** a third-party subclass breaks on an upgrade.
**Cause:** a public class was subclassable by default (Java, C#, Kotlin pre-`final` habits) (R6).
**Detection:** is every publicly subclassable class intended as an extension point?

**Fix:** `final` / `sealed` by default; `open` deliberately, with a documented contract.

## 7. `protected` misread

**Symptom:** a member is reachable from unrelated classes in the same package.
**Cause:** Java's `protected` includes the package (and TS's can be widened by a subclass).
**Detection:** check whether the intended scope was "subclasses only".

**Fix:** compose, or use a private hook behind a public final method.

## 8. Everything public in a single-module app

**Symptom:** an app with one module where every class is public.
**Cause:** the default was never questioned (R1).
**Detection:** count `public` in a single-module project.

**Fix:** `internal` everywhere; there is no public surface.

## 9. Transitive exposure

**Symptom:** a public function returns a type that was meant to be internal.
**Cause:** visibility propagates through signatures — every language enforces it.
**Detection:** the build may already fail here; check whether the fix was to widen the type.

**Fix:** narrow the function, or ask whether the type should be public at all.

## 10. Interface treated as an internal seam

**Symptom:** an "internal" interface is reachable by every consumer.
**Cause:** Java/Kotlin/C# interface members are implicitly public (Java cannot narrow them).
**Detection:** is every interface part of the intended surface?

**Fix:** an unexported abstract class, a module that does not export the package, or Go-style unexported interfaces.

## 11. Keyword translation across languages

**Symptom:** a ported design has different boundaries than the original.
**Cause:** `internal` was mapped to `internal` literally.
**Detection:** compare the ported units (module vs package vs crate vs assembly vs library).

**Fix:** map by promise, not by keyword (see `language-models.md`).

## 12. Package split changes visibility

**Symptom:** refactoring a package into several silently changes what is reachable.
**Cause:** package-private access was relied on across what is now a boundary.
**Detection:** diff the visibility graph before and after a package restructure.

**Fix:** treat a package split as a visibility change, and review it as one.

## 13. Removal without deprecation

**Symptom:** a downstream consumer breaks with no warning.
**Cause:** a public declaration was removed directly (R2).
**Detection:** was there an announce → warn → window → remove sequence?

**Fix:** deprecate first, with a window and a warning mechanism.

## 14. `export *` / blanket re-export

**Symptom:** the surface includes everything a barrel file happens to import.
**Cause:** convenience re-exporting (R2).
**Detection:**

```bash
grep -rn "export \*" src/ | head
```

**Fix:** name each export explicitly.

## 15. `InternalsVisibleTo` shipped or over-broad

**Symptom:** a test grant reaches a release artifact, or grants a wildcard.
**Cause:** the attribute was added without a build-configuration check (R5).
**Detection:** is it excluded from release, and does it name one assembly?

**Fix:** name one assembly; verify the release build excludes it; never treat it as a security control.

## Detection sweep

```bash
SRC="${1:-src}"

echo "== public vs private ratio (surface by exclusion?) =="
pub=$(grep -rIoE "\bpublic\b" "$SRC" 2>/dev/null | wc -l | tr -d ' ')
priv=$(grep -rIoE "\bprivate\b" "$SRC" 2>/dev/null | wc -l | tr -d ' ')
echo "  public: $pub   private: $priv"

echo "== public mutable fields =="
grep -rnE "public\s+\w+\s+\w+\s*(;|=)" "$SRC" 2>/dev/null | grep -vE "final|const|readonly" | head -5 || echo "  none"

echo "== non-enforcing privacy (TS private on sensitive names) =="
grep -rnE "private\s+\w*(token|secret|key|password|credential)" "$SRC" 2>/dev/null | head -5 || echo "  none"

echo "== test-driven widening hints =="
grep -rn "for tests\|for the tests\|visible for testing" "$SRC" 2>/dev/null | head -3 || echo "  none"

echo "== blanket re-exports =="
grep -rn "export \*" "$SRC" 2>/dev/null | head -3 || echo "  none"

echo "== C# InternalsVisibleTo =="
grep -rn "InternalsVisibleTo" "$SRC" 2>/dev/null | head -3 || echo "  none"

echo "== Java modules: is there an exports list? =="
find . -name "module-info.java" 2>/dev/null | head -3 || echo "  no modules"
```

Interpretation: **a public/private ratio far above 1** suggests the surface is defined by exclusion. **A public mutable field** is the R3 defect. **A TS `private` on a token** is the R4 security defect. **A blanket `export *`** means the surface grows with every import.
