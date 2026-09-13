# Platform Families

<!-- STANDARD: 3min -- Apple, Android, Windows, web and cross-platform families in brief -->

> **Verification note.** This file describes the *shape* of each platform family's conventions so
> decisions can be reasoned about. It deliberately does not state current numeric dimensions,
> control names or API names as fact, because platforms revise their guidance every release
> cycle. Before implementing, confirm specifics against the platform's current documentation for
> the targeted SDK version (see the Anti-Hallucination section of `SKILL.md`).

## The shape of each family

| Family | Convention philosophy | Expresses brand through | Non-negotiable |
|---|---|---|---|
| Apple | Content-forward, deference to the content, system-provided affordances | Type, colour, imagery, custom controls at the edges | Navigation model, back gesture, system dialogues |
| Android | Material-based, dynamic, themable, explicit system integration | Material theming, custom components within the system | Back handling, system intents, permission flow |
| Windows | Keyboard-and-pointer parity, window management, information density | Fluent theming and custom chrome | Window behaviour, menu/shortcut expectations |
| Web | User-agent freedom, progressive enhancement, addressability | Almost everything visual | Keyboard access, focus, reflow, standards semantics |
| Cross-platform (Flutter / RN / KMP / MAUI) | Framework widget set, optionally bridged to native | Whatever the framework renders | Per-platform accessibility, navigation and system integration |

## Apple family (iOS, iPadOS, watchOS, visionOS, tvOS)

**The organising idea:** the system provides a great deal, and the app defers to it. Navigation,
transitions, gestures, typography and controls all have platform-native expressions, and the app
expresses itself through content, colour and imagery.

**What is platform-governed (do not override):**
- The navigation model (stack, tab, split) and its visual expression
- The back affordance and its gesture
- Standard control behaviour and system affordances (share, permission, biometrics)
- Text styles and the user's text-size setting

**What the product governs:**
- Content presentation, imagery, illustration
- Colour and brand expression within the system's structure
- Custom controls where the platform has no equivalent

**Form-factor notes:** iPadOS adds split view, pointer and keyboard, so a phone layout is not
sufficient (R2). watchOS has a one-task-per-screen budget. tvOS is focus-driven with no pointer.
visionOS introduces spatial placement, gaze and comfort constraints. Depth for all of these
belongs to `apple-hig-expert`; this skill decides *which* conventions bind.

## Android family (phone, foldable, tablet, Wear, Auto, TV)

**The organising idea:** a themable design system with explicit system integration. Material
provides a component and token system, and the platform expects apps to participate in system
behaviour (intents, back, permissions, dynamic colour).

**What is platform-governed:**
- Back navigation semantics, including gesture and predictive back behaviour
- System intents and inter-app behaviour (share, open, deep link)
- Permission flow and its system dialogues
- Dynamic colour and theming participation

**What the product governs:**
- Brand theming within the Material structure
- Custom components where Material has no equivalent
- Information architecture and content

**Form-factor notes:** foldables change size *at runtime*, which makes device-name breakpoints
actively wrong; design against available size and state. Wear is a glance surface with a
one-task budget and its own input (dial/crown, swipe, voice). Auto and TV are focus- and
glance-driven with strict attention constraints. Material 3 component depth belongs to
`material-design-expert`.

## Windows / desktop

**The organising idea:** pointer and keyboard are first-class, windows are first-class, and
information density is expected. A desktop app is not a phone app with a bigger viewport.

**What is platform-governed:**
- Window behaviour: resize, maximise, snap, multi-window, state restoration
- Menu and context-menu conventions, keyboard shortcuts
- Pointer semantics: hover, cursor changes, drag and drop
- System integration: notifications, file associations, taskbar/dock

**What the product governs:**
- Information architecture, density, custom chrome and theming

**The common failure** is porting a touch navigation model — bottom tabs, a back gesture, a
hamburger — onto a windowed surface with a pointer and a keyboard. Users on desktop expect
shortcuts and multi-window, and they will find the absence of each a missing feature rather
than a design choice.

## Web

**The organising idea:** the web is the least prescriptive platform and therefore the one where
brand governs most, *except* for the parts that are standards or accessibility obligations.

**What is platform-governed:**
- Keyboard access and focus model (WCAG 2.1.1, 2.4.7)
- Reflow and resize (WCAG 1.4.4, 1.4.10)
- Addressability: URL state, back/forward behaviour, deep linking
- Standards semantics: headings, landmarks, form semantics

**What the product governs:**
- Layout, visual language, component design, motion

**The web-specific trap:** browser back is the user's back button and also a navigation model.
An SPA that breaks back/forward behaviour violates a platform convention as surely as an app
that removes the Android back gesture.

## Cross-platform frameworks

| Framework | Default rendering | Native-widget path | Governance caveat |
|---|---|---|---|
| Flutter | Self-drawn widgets (one renderer everywhere) | Platform-adaptive widgets and community platform libraries | The default widget set is *not* a platform convention; shipping it to a platform-targeted app is a recorded trade, not compliance |
| React Native | Native primitives, framework components | Native modules and platform-specific components | Closer to native by default, but navigation and gestures still need per-platform handling |
| Kotlin Multiplatform | Compose UI or native UI per platform | Native UI in the platform layer; Compose shared | With shared Compose UI the same trade applies; with native UI, platform conventions are free |
| .NET MAUI | XAML controls mapped to native | Native handler customisation | Mapping is good but not complete; verify navigation and gestures per platform |

**The rule for every framework:** the framework's default widget is a starting point. Whether it
constitutes platform conformance is a *decision* (Decision Tree 2), and if the answer is "we
accept the deviation", it belongs in the deviation log.

## Choosing the family scope

```text
Which families ship?
├── One mobile family only        → learn that family deeply; this skill still applies for
│                                    form factors (tablet, foldable, watch)
├── Two mobile families           → the matrix is the core artefact (R1)
├── Mobile + web                  → resolve the shared information architecture, then per-family
│                                    conventions; watch the navigation conflict
├── Mobile + web + desktop        → the widest conflict surface; desktop expectations are the
│                                    most often missed
└── Any of the above + wearable/TV/spatial
                                  → run Decision Tree 4 per reduced surface before layout
```

## What is genuinely shared across families

Being the same *only* where it is safe is the discipline. These are safe:

- Domain model, business logic and validation
- Content and copy (subject to length, not convention)
- Information architecture (the *what*, not the *how*)
- Data and networking layers
- Brand identity: colour, imagery, voice, illustration

These are not safe to share:

- Navigation model and back affordance
- Gesture meanings
- Control behaviour and hit-target expectations
- Input handling (pointer, keyboard, remote, gaze, stylus)
- Motion timing and reduced-motion behaviour
- System integration and permission flows
- Accessibility handling and the platform's accessibility API surface
