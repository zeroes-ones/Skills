# Access Modifiers — Flutter / Dart

> Full model: `access-modifiers` → `references/dart-and-mobile.md`.

Dart has **no access modifiers at all**. Privacy is a single convention — a leading underscore — and
it is scoped to the **library**, which in practice is one file. Everything else is public.

## The two levels

| Form | Visible in |
|---|---|
| `name` | everywhere |
| `_name` | the declaring **library** (normally one file) |

That is the whole model. There is no `internal`, no `protected`, no package-private, and no test
friend mechanism.

## Guidance specific to Flutter

**1. The library is the file, so `_` does not share across files.** Two files cannot share a private
member unless they are `part` of the same library — and using `part` to share privates is widely
discouraged, because it couples the files into a single unit and defeats incremental compilation.
Where two files must share an internal helper, the honest options are: make it public, or extract both
into one library.

**2. There is no "package-internal".** A package is not a visibility unit in Dart. A `lib/src/`
convention exists for "implementation, not the public entry point" — the analyzer and the docs treat
`lib/src/` as private by convention, and consumers are expected to import `lib/<package>.dart` rather
than reaching into `src/`. That convention is the closest Dart gets, and it is a convention, not a
boundary.

```text
lib/
├── my_package.dart        ← the public entry point (import this)
└── src/                   ← implementation; importing it is discouraged
    └── internal_thing.dart
```

**3. `@visibleForTesting` and friends are analyzer hints.** The `meta` package provides annotations
the analyzer enforces as warnings:

| Annotation | Meaning |
|---|---|
| `@visibleForTesting` | warn if used outside a test |
| `@internal` | warn if used outside this package |
| `@protected` | warn if used outside a subclass |
| `@mustCallSuper` | warn if an override does not call super |

These are the closest Dart gets to the modifiers other languages have, and they are **declaration for
the analyzer** — useful in review, and honest about being a hint.

**4. The test-visibility limitation is real, and it should be stated rather than worked around.**
Dart has no friend mechanism, so a `_`-private member in one file is genuinely unreachable from a test
in another file. The options, in order of preference:

1. **Test the public behaviour** — usually the better test anyway, and the Flutter widget-test
   harness makes this natural.
2. **Put the test in the same library** (`part`, or a test inside the same file) — couples the test to
   the file.
3. **Widen** — refused (R5); in Dart it also means the widening has no mechanism to hide it again.

State the limitation. Widening silently to make a test compile is the failure this skill exists to
prevent.

**5. Flutter's own conventions are worth following.** Framework-internal state is typically held in
private fields behind a `State` class, exposed to the widget tree through the build method rather than
through accessors. `_`-prefixed fields in a `StatefulWidget`'s `State` are private to that file, which
is usually exactly the intent.

**6. On Dart, "public" is the default and the whole surface is public unless underscored.** So a
package's published surface is *everything not starting with an underscore* — which makes the inverted
default (R2) more important here than anywhere: there is no modifier to narrow later, only a rename.

## The Flutter checklist

- [ ] `_` privacy understood as **library-scoped** (normally one file), not class- or package-scoped
- [ ] Cross-file sharing of an internal helper solved by extraction, not by `part`
- [ ] `lib/src/` used as the implementation convention, with `lib/<package>.dart` as the entry point
- [ ] `@visibleForTesting` / `@internal` / `@protected` recognized as analyzer hints, not boundaries
- [ ] The no-test-mechanism limitation stated where it applies, rather than widening (R5)
- [ ] Read-only state exposed through a getter over a `_` field, not a public mutable field
- [ ] The published surface reviewed as "everything not underscored" — an explicit list, not a default
- [ ] No secret placed in Dart on the assumption `_` protects it (Dart ships to the device)
