# Dart and Mobile

<!-- STANDARD: 3min -- Dart's library-level _ privacy, and cross-platform mapping -->

> Grounded in the Dart language tour and library documentation. Confirm against the
> installed SDK version, as Dart's privacy rules are library-scoped and change slowly but
> do change.

## Dart: the underscore is library-scoped

Dart has **no access modifiers at all**. Privacy is a single convention: an identifier
beginning with `_` is private **to the library** — and in Dart a library is a file (or a
set with `part`).

| Form | Visible in |
|---|---|
| `name` | everywhere |
| `_name` | the declaring **library** (normally one file) |

```dart
// profile.dart — a library
class Profile {
  String _token = '';          // private to this file
  String get token => _token;  // the accessor is the boundary
  set token(String v) => _token = v;
}
```

Two facts worth internalising:

1. **The unit is the library, i.e. usually the file.** Two files cannot share a private
   member unless they are `part` of the same library — and using `part` to share privates
   is widely discouraged, because it couples the files into one unit.
2. **There is no `internal`, `protected`, or `package-private`.** So Dart's levels are
   exactly two: private-to-the-library, and public.

### Practical consequences

| Situation | Dart's answer |
|---|---|
| share a private across two files | make it public, or extract it into one library |
| "package-internal" API | not expressible — the package is not a visibility unit |
| subclass-only member | not expressible — Dart has no `protected` |
| test reaching a private | the test must be in the same library (`part`), or test the public surface |
| a member only for tests | there is no friend mechanism; the surface is what is testable |

**The test point is the one that bites.** Because Dart has no test-visibility mechanism,
a private member is genuinely untestable from a separate test file. The options are: test
the public behaviour (preferred), put the test in the same library (coupling), or widen —
which R5 refuses. State the limitation rather than widening silently.

### `@visibleForTesting` and analyzer hints

The `meta` package provides annotations that the **analyzer** enforces as hints:

```dart
import 'package:meta/meta.dart';

@visibleForTesting
void resetState() { }
```

`@visibleForTesting` warns when the member is used outside a test. It is an analyzer hint,
not a runtime boundary — useful in review, and honest about being a hint. Related hints
worth knowing: `@internal` (this package only), `@protected` (subclasses), `@mustCallSuper`.

**These are the closest Dart gets to the modifiers other languages have**, and they are
declarations for the analyzer. Treat them as documentation that a tool reads.

## Cross-platform mapping for mobile

| Concern | Swift (iOS) | Kotlin (Android) | Dart (Flutter) |
|---|---|---|---|
| this file only | `private` / `fileprivate` | `private` (file, at top level) | `_name` (library) |
| this module/unit only | `internal` | `internal` (module) | not expressible |
| package-internal | `package` | — | not expressible |
| subclasses only | — | `protected` | `@protected` hint only |
| anyone | `public` | `public` | the name |
| anyone + extend | `open` | `open` | no subclassing control |
| test visibility | `@testable` | test source set | none (same library only) |
| read-only from outside | `internal(set)` / `private(set)` | `private set` | getter, private setter field |
| JVM/JS permeability | — | **`internal` visible to Java** | — |

**The mapping rule:** map by promise, not by keyword. Kotlin's `internal` and Dart's `_` are
different scopes; Swift's `internal` and Kotlin's `internal` are different units (module in
both, but "module" means a framework target in one and a compilation unit in the other).

### The read-only idiom, in three languages

Every mobile language expresses "publicly readable, internally writable" — the shape R3
prefers:

```swift
public private(set) var count = 0            // Swift
```

```kotlin
var count: Int = 0
    private set                              // Kotlin
```

```dart
int _count = 0;
int get count => _count;                     // Dart
```

Use these instead of a public mutable property in every case.

## React Native / TypeScript-JavaScript

React Native spans two worlds and both have the erasure issue (R4):

| Layer | Concern |
|---|---|
| JS/TS side | `private` is erased — use `#field` for anything sensitive |
| native side | Swift/Kotlin rules apply to the native modules |
| the bridge | an exported native method is public to JS whatever the native modifier says |

**The bridge is the notable trap:** a natively `private` method exposed through a bridge
or a native module becomes callable from JavaScript. Check the export surface, not only the
modifier.

## The mobile checklist

- [ ] Dart's two levels understood: library-private and public — nothing else exists
- [ ] `_name` privacy not relied on across files (the unit is the library)
- [ ] `@visibleForTesting` / `@internal` / `@protected` recognized as analyzer hints, not boundaries
- [ ] The no-test-mechanism limitation stated where it applies, rather than widening (R5)
- [ ] Read-only accessors used instead of public mutable properties (R3)
- [ ] Cross-platform ports mapped by promise, not keyword
- [ ] On React Native, the bridge's exported surface checked separately from the native modifiers
- [ ] On the JVM/Android side, `internal`'s Java permeability kept in mind (R4)
