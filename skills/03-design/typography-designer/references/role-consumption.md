# Role Consumption

<!-- DEEP: 5+min -- how a type role is written at the call site, per platform -->

> **Verification note.** The language mechanisms below are grounded in the Swift evolution
> proposals and the Kotlin and Material 3 documentation, cited inline. Confirm the mechanism
> against the language version you target before relying on it — the leading-dot form in
> particular has a version floor.

## The problem

A type system with clean roles can still be verbose at every call site:

```kotlin
Text(post.title,     style = MaterialTheme.typography.titleLarge)
Text(post.author,    style = MaterialTheme.typography.bodySmall)
Text(post.timestamp, style = MaterialTheme.typography.bodySmall)
```

Three text nodes, three repetitions of the theme object and the role name. Each repetition is a
coupling: a theme change, a re-naming, or a switch of type family touches every file that names a role.

The question this file answers: **how do you write less, without losing the role?**

## The critical finding: the platforms are asymmetric

**Swift can write `.barTitle`. Kotlin cannot.**

| Platform | Can `.barTitle` work? | Why |
|---|---|---|
| **Swift / iOS** | **Yes** | an implicit member expression, when the contextual type is inferable |
| **Kotlin / Android** | **No** | extension properties require an explicit receiver; there is no leading-dot form |

The Swift mechanism, verbatim from the proposal that introduced the chained form:

> "anywhere that a contextual type `T` can be inferred, writing `.member1.member2.(...).memberN`
> will behave as if the user had written `T.member1.member2.(...).memberN`"
>
> *(Source: SE-0287, "Extend implicit member syntax to cover chains of member references", Implemented Swift 5.4.)*

The Kotlin constraint, verbatim from the language documentation:

> "Extensions are always called on a receiver. The receiver has to have the same type as the class
> or interface being extended. To use an extension, prefix it with the receiver followed by a `.`
> and the function or property name."
>
> *(Source: Kotlin documentation, "Extensions".)*

**The design consequence, and the reason this belongs in a cross-platform skill:** a policy that
prescribes `.barTitle` as the standard ships **invalid code on Android**, which is roughly half of a
typical mobile product. The rule cannot be "use `.barTitle`". It must be **"use the shortest form the
platform legally allows."**

## The three tiers, best first

### Tier 1 — do not name the role at all

The genuinely "write less" answer, and it beats any shorthand. Both platforms propagate a text style
down a subtree, so the role is declared **once at a container** and the leaves are anonymous.

**Android (Compose):**

```kotlin
// The role is named ONCE, at the container
ProvideTextStyle(MaterialTheme.typography.titleLarge) {
    PostHeader()          // children inherit it; no role named inside
}
```

`ProvideTextStyle` is documented as setting "the current value of `LocalTextStyle`, merging the given
style with the current style values for any missing attributes." *(Source: Material 3 API reference.)*

**iOS (SwiftUI):**

```swift
// The role is named ONCE, at the container
VStack { PostHeader() }
    .environment(\.font, .title2)      // children inherit; .title2 is legal here
```

**The metric that follows from this:** a screen with 30 text nodes should name **zero** roles in the
leaves. If it names thirty, the container is the missing piece — not the syntax.

### Tier 2 — the shortest legal form

For the cases where an explicit role at a leaf is genuinely right (a heading inside a body container,
a caption inside a label context):

| Platform | Form | Legal because | Cost |
|---|---|---|---|
| iOS | `.barTitle` | implicit member expression (SE-0287) | one line of extension code, once |
| Android | `barTitle` | a top-level `@Composable` property, imported | **shorter than iOS** — no leading dot |
| Android | `AppType.barTitle` | when an import would collide | one extra qualifier |
| Web | `var(--type-bar-title)` | custom property | already the shortest form |

**Note the inversion:** the shortest form is on **Android**, not iOS. `Text(style = barTitle)` is
shorter than `Text("x").font(.barTitle)` — and it is legal, because a top-level property needs no
receiver at the call site (the receiver is the module, resolved by the import).

### Tier 3 — never repeat the long form

`MaterialTheme.typography.titleLarge` at every call site, or `.font(.system(size: 22, weight: .semibold))`,
is the defect this file exists to prevent. It couples every text node to the theme object **and** to
the role name.

## How each tier is implemented

### iOS: the role extension

```swift
// AppType.swift — written ONCE
import SwiftUI

extension Font {
    static var barTitle:   Font { .system(.title2, design: .serif) }
    static var barBody:    Font { .system(.body,   design: .serif) }
    static var barCaption: Font { .system(.caption) }
}
```

Then `.barTitle` works anywhere the contextual type is `Font` — which is the parameter type of
`Text.font(_:)`. The mechanism is the implicit member expression, and the type safety comes from the
compile-time type: an invalid role does not compile, because there is no such member.

**Version floor:** the *chained* implicit-member form needs Swift 5.4 (SE-0287). A single-member
`.barTitle` works earlier. If you must support an older toolchain, use Tier 1 instead of Tier 2.

### iOS: dynamic member lookup, when roles are data

Where role names come from a configuration file or a theme payload, `@dynamicMemberLookup` provides
dot syntax resolved "in a **completely type safe** way" *(Source: SE-0195, Implemented Swift 4.2)*:

```swift
@dynamicMemberLookup
struct TypeRoles {
    let roles: [String: Font]
    subscript(dynamicMember key: String) -> Font {
        roles[key] ?? .body        // a safe default; never a crash
    }
}

// Usage reads identically to the static form
Text("Inbox").font(typeRoles.barTitle)
```

**When to use it:** only when the role set is genuinely dynamic (a server-driven theme, a white-label
app with per-tenant roles). For a fixed role set, the static extension in the previous section is
simpler, faster, and catches typos at compile time. Dynamic lookup moves a typo from a compile error
to a runtime default — a real trade, so state it.

### Android: the top-level property

```kotlin
// AppType.kt — written ONCE
package com.example.design

import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.text.TextStyle

val barTitle: TextStyle
    @Composable get() = MaterialTheme.typography.titleLarge

val barBody: TextStyle
    @Composable get() = MaterialTheme.typography.bodyMedium
```

Then `Text(post.title, style = barTitle)` — an import, no qualifier, no leading dot.

**Three details that matter:**

1. **`@Composable` on the getter, not the property declaration** — `MaterialTheme` is only readable in a
   composition, so the accessor must be composable.
2. **Do not mark the property `const` or `val ... = `** with an initialiser — that would read the theme
   once, outside the composition, and break on a theme change.
3. **The import is the "shorthand".** Kotlin's import is what removes the qualifier, which is why this
   form is shorter than the Swift equivalent.

### Android: when an import is not enough

Two cases need the qualifier:

```kotlin
import com.example.design.AppType

Text(post.title, style = AppType.barTitle)   // explicit, still short
```

Use it when a local symbol shadows a role name, or when readability benefits from the namespace. It is
one extra token, and it is honest about where the role comes from.

### Android: a container helper

For the Tier-1 pattern, a small wrapper makes the intent explicit:

```kotlin
@Composable
fun BarTypography(content: @Composable () -> Unit) =
    ProvideTextStyle(MaterialTheme.typography.titleLarge, content)

// Usage
BarTypography { PostHeader() }
```

This is worth having when the same container style recurs: it names the *context* rather than the
*role*, which is one level higher in the abstraction and survives a role re-mapping.

## The mapping, in one table

| Tier | iOS | Android | Roles named per screen |
|---|---|---|---|
| 1 | `.environment(\.font, .title2)` at a container | `ProvideTextStyle(...)` at a container | 0 in the leaves |
| 2 | `.barTitle` | `barTitle` (imported) | 1 per explicit leaf |
| 3 | `.font(.system(size:weight:))` inline | `MaterialTheme.typography.titleLarge` inline | 1 per leaf, coupled to the theme |

**Tier 3 is the anti-pattern.** It is what the skills currently demonstrate, and it is why the long
form appears everywhere.

## Enforcing it with lint

The discipline is checkable, which is what makes it a standard rather than a convention (see
`code-formatting-and-linting`):

```yaml
# A custom rule: forbid the long form at a call site
# Android: detekt / ktlint custom rule
#   pattern: "MaterialTheme.typography." outside the token file
#   message: "Use an AppType role instead: `barTitle`, not `MaterialTheme.typography.titleLarge`"
```

```yaml
# iOS: a custom swiftlint rule
custom_rules:
  no_inline_type_roles:
    name: "No inline type roles"
    regex: '\.font\(\.system\(size:'
    message: "Use a role from Font.swift: `.barTitle`, not an inline size."
    severity: warning          # warning first; error once the baseline is clean
```

**The rule, generalised:** *the type scale is named in the token file and nowhere else.* A grep that
finds a raw size or a theme-qualified role outside that file is a finding.

This is the cleanest possible lint rule for typography — it is a **pattern match with a clear
exception** (the token file), it has no false-positive ambiguity, and the finding tells the author the
exact replacement.

## Verification

```text
1. Grep the codebase for the long form:
     Android: grep -rn "MaterialTheme\.typography\." --include="*.kt" | grep -v "AppType.kt"
     iOS:     grep -rn "\.font(\.system(size:" --include="*.swift" | grep -v "Font.swift"
   → any hit outside the token file is a finding.

2. Count the roles named per screen:
   → a screen with more named roles than leaves has a missing container (Tier 1).

3. Confirm the shorthand exists and compiles:
     iOS:     a `.barTitle` reference where the contextual type is Font
     Android: `barTitle` imported, used as a `TextStyle`, with @Composable on the getter

4. Confirm a theme change does not require touching call sites:
   → change the role's value in the token file; no other file should need an edit.
```

Step 4 is the acceptance test. If changing a role's value requires editing call sites, the roles are
not tokens — they are decorations over a theme.

## Checklist

- [ ] The container declares the role once where a whole region shares a style (Tier 1)
- [ ] A shorthand exists for each platform in the shortest form that platform legally allows (Tier 2)
- [ ] The Android form is a top-level `@Composable` property with the annotation on the getter
- [ ] The iOS form is a `Font` extension, or `@dynamicMemberLookup` where roles are genuinely dynamic
- [ ] The long form appears in exactly one file per platform — the token file (Tier 3 excluded)
- [ ] A lint rule forbids the long form (or a raw size) outside the token file
- [ ] The dynamic-lookup trade is stated, where it is used (a typo becomes a runtime default)
- [ ] Changing a role's value requires editing no call site (verified)
