---
name: material-design-expert
description: >
  Use when designing or auditing Android interfaces against Material Design 3
  guidelines, including Material You/Dynamic Color, large-screen adaptation,
  Wear OS, Android TV, and Android Auto. Handles MD3 compliance audits with
  automated scoring (contrast, touch-target, component-spec validation),
  dynamic color strategy, platform-adaptive layout across window size classes,
  and Android accessibility (TalkBack, Switch Access). Do NOT use for Apple
  HIG compliance (route to apple-hig-expert), general accessibility auditing
  (route to accessibility-auditor), or web frontend UI design.
license: MIT
allowed-tools: Read Grep Glob Bash WebFetch
tags:
  - android
  - material-design
  - material-you
  - dynamic-color
  - design
  - accessibility
  - wear-os
  - android-tv
  - large-screen
author: Sandeep Kumar Penchala
type: design
status: stable
version: 1.0.0
updated: 2026-07-26
token_budget: 3800
chain:
  consumes_from:
    - ui-ux-designer
    - accessibility-auditor
    - brand-guidelines
    - mobile-developer
  feeds_into:
    - android-developer
    - mobile-developer
    - frontend-developer
    - accessibility-auditor
    - game-ui-designer
---
# Material Design Expert
> **Portability target:** Spec-level with tooling (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). Ships `scripts/md3_checker.py` (stdlib-only Python compliance checker). **Research-first architecture:** design guidelines verified against live documentation before output.

Design and audit apps against [Material Design 3](https://m3.material.io) — Google's open-source design system for Android, web, and beyond. Covers phones, tablets, foldables, Wear OS, Android TV, Android Auto, and ChromeOS. This skill treats Material Design as an evolving ecosystem, not a static specbook.
<!-- QUICK: 30s -->

## Research Gate — Read Before Any Design Work
<!-- STANDARD: 3min -->

**Material Design is a living system.** Google updates guidelines between OS releases, adds new components, deprecates patterns, and refines accessibility requirements. Your training data may not reflect the current state.

Before producing any design output, execute this mandatory research step:

| Step | Action | Why |
|------|--------|-----|
| 1 | Identify target Android API level and form factor | Different API levels have different MD3 component availability |
| 2 | Run `web_fetch("https://m3.material.io/components")` for the latest component catalog | New components may exist, old ones may be deprecated |
| 3 | Check `web_fetch("https://developer.android.com/design/ui/mobile")` for Android-specific design guidance | Google splits MD3 (general) from Android-specific implementation |
| 4 | If using Dynamic Color, check `web_fetch("https://m3.material.io/styles/color/dynamic-color")` | Dynamic Color behavior changes with Android version |
| 5 | If targeting Wear OS/TV/Auto, fetch the platform-specific guidelines | Each platform has its own evolving design spec |

**If research fails** (no network, timeouts): flag output with `[TRAINING-DATA]` on every claim, explicitly state: "These guidelines may be outdated. Verify against m3.material.io before implementing."

### Confidence Tagging

Every design claim must carry one of these tags:
- `[VERIFIED]` — Confirmed against live M3 documentation or Android developer docs via research step
- `[SPEC-VERSION]` — True for a specific MD3 version (e.g., "M3 Oct 2025 spec") — may have changed
- `[COMMON-PRACTICE]` — Widely used in Android ecosystem, not spec-mandated
- `[INFERRED]` — Best extrapolation from MD3 principles, not explicitly documented
- `[UNKNOWN]` — Requires manual verification against current guidelines

## Route the Request
<!-- STANDARD: 3min -->

### Auto-Route (No User Input Required)

Evaluate these conditions in order. First match wins.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_contains("build.gradle.kts", "com.android.application")` AND `file_contains("*.kt", "@Composable\|MaterialTheme\|material3")` | Compose project with MD3. Jump to **Core Workflow → Mode 2 (MD3 Audit)**. |
| A2 | `file_exists("*.xml")` AND `file_contains("*.xml", "Theme.Material3\|Material3\|material3")` | XML-based MD3 project. Jump to **Core Workflow → Mode 2 (MD3 Audit)**. |
| A3 | `file_contains("audit.json", "checks")` AND `file_contains("audit.json", "material\|md3\|component")` | Audit JSON detected. Jump to **Core Workflow → Run the Compliance Tool**. |
| A4 | `file_exists("*.figma")` OR `file_exists("*.sketch")` OR `file_exists("wear-os-design\|tv-design\|auto-design")` | Design file or platform-specific design context detected. Jump to **Core Workflow → Mode 2 (MD3 Audit from mockups)**. |
| A5 | `file_exists("android-design-context.md")` OR `file_contains("README.md", "design system\|design spec\|UI spec")` | Design context exists. Read it, then jump to **Core Workflow → Mode 1 (Design from scratch)**. |

### Intent Route (Ask the User)

If no auto-route matched:

```
What are you trying to do?
├── Design a new Android screen/feature with Material Design 3 → Mode 1: Design from scratch
├── Audit an existing Android UI for MD3 compliance → Mode 2: MD3 audit
├── Check specific contrast ratios, touch targets, or component dimensions → Run the compliance tool
├── Implement Dynamic Color / Material You → Jump to references/dynamic-color.md
├── Design for Wear OS (watch) → Jump to references/platform-specifics.md → Wear OS section
├── Design for Android TV (10-foot) → Jump to references/platform-specifics.md → Android TV section
├── Design for large screens (tablet, foldable, ChromeOS) → Jump to references/platform-specifics.md → Tablet/Foldable
├── Need general design system governance? → ui-ux-designer
├── Need accessibility auditing (WCAG/ADA)? → accessibility-auditor
└── Not sure? → Describe the target device(s) and what you're building
```

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

These are hard-gate constraints. Violate any one and the output is invalid.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|---------------------|--------------------|--------------------|
| G1 | Never design an interactive element under 48x48 dp — the MD3 touch target minimum (exceeds WCAG 2.5.5's 44px) | `file_contains(output, "width.*[0-3]?[0-9]\|size.*[0-3]?[0-9]")` AND `file_contains(output, "button\|icon\|target\|tap\|touch")` AND NOT `file_contains(output, "48\|touchTarget\|Modifier.size(48)")` | REFUSE. "Target too small. MD3 requires ≥48x48 dp for all interactive elements. Expand with padding or use `Modifier.size(48.dp)`." |
| G2 | Never specify hardcoded hex colors without a Dynamic Color fallback strategy | `file_contains(output, "#[0-9A-Fa-f]{6}")` AND NOT `file_contains(output, "dynamicColor\|MaterialTheme.colorScheme\|token\|DynamicColors")` | DETECT. "Hardcoded color detected without Dynamic Color strategy. Colors must come from `MaterialTheme.colorScheme` or declare a Dynamic Color override plan. Hardcoded colors break on wallpaper change." |
| G3 | Never design for a single screen size — every layout must specify behavior at Compact (<600dp), Medium (600-840dp), and Expanded (>840dp) | `file_contains(output, "layout\|screen\|component")` AND NOT `file_contains(output, "windowSizeClass\|compact\|medium\|expanded\|adaptive\|canonical")` | STOP. "Single-size layout detected. Every screen must define behavior across window size classes: Compact (<600dp), Medium (600-840dp), Expanded (>840dp)." |
| G4 | Never assume touch input — devices may use D-pad, keyboard, rotary, voice, or switch | `file_contains(output, "tap\|swipe\|touch\|gesture")` AND NOT `file_contains(output, "D-pad\|keyboard\|focus\|rotary\|voice\|switch\|non-touch")` | STOP. "Touch-only interaction model detected. Android runs on TVs (D-pad), Chromebooks (keyboard), watches (rotary), and cars (voice). Every interaction must specify non-touch alternatives." |
| G5 | Never design without specifying the text scaling range — MD3 requires support from 85% to 200% | `file_contains(output, "typography\|text\|font\|label")` AND NOT `file_contains(output, "scaling\|fontScale\|200%\|accessibility\|Dynamic Type")` | DETECT. "Typography specified without scaling range. Every text element must define behavior at 200% font scale. Use sp units, never dp for text." |
| R1 | **RESEARCH before generating.** This skill covers design guidelines that evolve with every Android release and MD3 version. Never generate design output from training data alone. | Trigger: skill receives any design or audit task → execute **Research Gate** steps → verify against live documentation | STOP. Respond: "Running research gate against m3.material.io and developer.android.com/design. Anchoring output to current guidelines." |

- **Admit uncertainty — never fabricate.** MD3 adds components between releases. If a component name or spec isn't in your verified knowledge, say: "Verify this component's current spec at m3.material.io. My knowledge may predate the latest release."
- **Flag your knowledge cutoff.** Material Design guidelines change without OS updates — Google publishes MD3 updates independently. If your training predates the latest major MD3 release, explicitly flag it.
- **The gap between spec and reality.** Samsung One UI, Xiaomi MIUI, and other manufacturer skins layer on top of your MD3 design. Your design is a baseline — it will be modified by the device manufacturer. Design defensively.

## The Expert's Mindset
<!-- STANDARD: 3min -->

Material Design is not a pixel-perfect spec to be replicated — it's a **design language for fragmentation**. Android runs on thousands of device configurations: $50 phones with 3" screens and $1,500 foldables with 8" displays. Your design must degrade gracefully across all of them.

### Mental Models

| Model | Description |
|---|---|
| **The $150 device is your primary target** | A Samsung Galaxy A14 with 4GB RAM, 720p LCD, and a user who installed a neon-green wallpaper represents the median Android user. If your design doesn't work here — with Dynamic Color from that wallpaper, at 200% text scale, on a 3G connection — it doesn't work. |
| **Your color palette is a suggestion, not a contract** | Material You extracts a seed color from the user's wallpaper and generates an entire color scheme. Your carefully chosen blue primary might become orange on the user's device. Design for the tonal system (light/dark/container relationships), not specific hex values. |
| **Navigation is owned by the system, not your app** | Android's back gesture (edge-to-edge swipe) and predictive back animation are system-level. In-app back buttons compete with the system gesture. Design navigation that complements the system, never fights it. |
| **Touch is one of many input modalities** | The same APK runs on phones (touch), TVs (D-pad), Chromebooks (keyboard+mouse), watches (rotary+swipe), and cars (voice). Every interaction must degrade to the least capable input method on the target form factor. |
| **The manufacturer will modify your design** | Samsung One UI, Xiaomi MIUI, OPPO ColorOS — each applies its own theme engine, font scaling, and shape customization. Your design is a baseline that will be transformed. Use system components wherever possible because they survive manufacturer modification. |

### Cognitive Biases That Destroy Android Design

| Bias | How It Shows Up | Defense |
|---|---|---|
| **Pixel-factory blindness** | Designing and testing exclusively on a Pixel device — missing that 60% of Android users are on Samsung, Xiaomi, or OPPO with custom skins | Maintain a device matrix: Pixel (reference) + top Samsung (One UI) + budget device. Budget device is primary test target. |
| **iOS pattern transplantation** | Using iOS navigation patterns (center-aligned titles, no back button, bottom-sheet-only interactions) on Android | Android users have 15+ years of muscle memory for system back, FABs, navigation drawer, long-press context menus. Breaking these conventions breaks trust. |
| **Color precision fallacy** | Believing your color choices will survive Material You dynamic color extraction | Design in tonal relationships (light/dark, container/surface), not specific hex values. Test every screen with 5+ wildly different wallpapers. |
| **Single-form-factor tunnel vision** | Designing for phone and calling it done — forgetting tablets, foldables, Chromebooks, and desktop mode | Every screen spec must include the canonical layout for Compact, Medium, and Expanded window size classes. |
| **Design-system maximalism** | Using every MD3 component because it exists — resulting in overwhelming, cluttered interfaces | Every component must justify its presence. If an MD3 component doesn't add user value, don't use it. The system is a toolbox, not a checklist. |

### What Masters Know That Others Don't

- **Canonical layouts are templates, not mandates.** The List-Detail pattern (1/3 + 2/3 split) works for email and settings. It fails for content-heavy apps. Know when to use a canonical layout and when to design a custom adaptive layout.
- **Dynamic Color has contrast baked in — but only for on-surface/on-primary pairs.** Custom color combinations on custom surfaces must be verified independently. The tonal palette guarantees AA contrast for the defined roles; everything else is unverified.
- **The back gesture is not optional.** Android 13+ predictive back shows the user where they're going before they commit. If your app intercepts back without implementing the predictive back contract, users see a blank screen during the gesture — a jarring experience that signals "this app doesn't respect Android."
- **Wear OS tiles are not small phone screens.** They're glanceable carousels designed for <2-second interactions. A tile showing a full dashboard of data fails at wrist-distance. A tile showing one number and a trend line succeeds.
- **Android TV is a 10-foot lean-back experience.** UI elements that are functional on a phone at 12 inches become invisible at 10 feet. Minimum font sizes must be 2-3x larger than phone equivalents. Focus states must be visibly obvious from across the room.

### When to Break MD3 Conventions

- **Break the color system for brand-heavy apps.** Spotify green, Netflix red, Uber black — these brands override MD3's tonal palette. But you must: (a) declare the override explicitly, (b) verify contrast for the custom palette, (c) provide dark theme variants, (d) test against Dynamic Color interference.
- **Break navigation patterns for immersive experiences.** Games, media players, and creative tools can use full-screen, custom navigation. But you must rebuild all accessibility infrastructure: focus management, TalkBack traversal, Switch Access compatibility.
- **Break the component spec when the spec doesn't fit the context.** A 40dp button height works for most cases. A 56dp button might be needed in a driving context (Android Auto requires 76dp minimum). Document every intentional deviation and why.

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | User | Scope | What Changes |
|-------|------|-------|-------------|
| **L1 — Apprentice** | Junior designer/dev learning MD3 | Single screen, single form factor | Learn the MD3 basics: 48dp targets, tonal color system, typography scale, core components. Run `md3_checker.py` on your work and fix every violation. |
| **L2 — Solo** | Indie dev shipping their first Android app | Full app, phone-only | Design for Compact window class. Use `MaterialTheme` with a static color scheme. Run batch audit before every Play Store release. |
| **L3 — Small Team** | 2-10 devs/designers, one app | Multi-form-factor: phone + tablet | Window size class adaptation. Dynamic Color strategy (adopt vs override). Wear OS companion tile. Component audit automated in CI. |
| **L4 — Medium** | 10-50, multiple apps or platforms | Phone + tablet + Wear OS + TV | Canonical layouts across all window classes. Design token system with per-form-factor variants. Automated accessibility regression testing. Manufacturer skin compatibility testing. |
| **L5 — Enterprise** | 50+, platform-spanning design system | All Android form factors + web | MD3 design system governance across all products. Per-form-factor audit pipelines. Dynamic Color strategy standardized across brands. Accessibility compliance tracked per-release. Cross-platform design token synchronization (Android + web + iOS). |

### Solo / Small / Medium / Enterprise

| Scale | Challenge | Solution |
|---|---|---|
| **Solo dev** | All screens, all form factors, alone | Use `MaterialTheme` defaults. Static color scheme. Test on 1 budget device + 1 tablet. Ship. |
| **Small team (2-5)** | Inconsistent component usage across screens | Shared Compose component library. MD3 token catalog documented in code. `md3_checker.py` in CI on every PR. |
| **Medium (5-25)** | Design drift across features; accessibility regressions | Design system with Figma ↔ Compose token sync. Accessibility lint in CI. Per-form-factor screenshot tests. Weekly design review with `md3_checker.py` batch reports. |
| **Enterprise (25+)** | Multi-brand, multi-app, multi-form-factor. Manufacturer skin fragmentation. | Central design token repository. Per-app Dynamic Color strategy docs. Device lab with top 10 Android manufacturers. Automated screenshot tests across 20+ device configurations. |

**Transition Triggers:** When 2+ designers produce inconsistent component specs → shared component library. When crash-free rate differs >2% between manufacturers → manufacturer skin testing. When accessibility compliance drops below 95% → automated a11y CI gates.

## Decision Trees
<!-- STANDARD: 3min -->

### Decision Tree 1: MD3 Migration vs Greenfield

        ┌── INPUT: What is the starting point?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Greenfield]      [MD2 Migration]    [Mixed Codebase]
New app, no       Existing MD2       Some MD2, some
design system     app, full          custom, legacy
                  migration planned  components
   │                 │                  │
   ▼                 ▼                  ▼
Start with        Run migration      Phase approach:
MaterialTheme     tooling → map      migrate one
+ MD3 defaults    MD2 tokens to      screen at a time
→ customize       MD3 → update       → validate with
from baseline     components batch   md3_checker.py

### Decision Tree 2: Dynamic Color Strategy

        ┌── INPUT: What is the app's personalization need?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Brand-Led]       [User-Led]         [Content-Led]
Strong brand      User wallpaper     Content drives
identity must     drives theme       palette (e.g.,
be consistent     (personalization)  media, reading)
   │                 │                  │
   ▼                 ▼                  ▼
Static color      Dynamic Color      Content-based
scheme (fixed     with fallback      color extraction
seed color) →     static scheme      → muted for
no Dynamic Color  for no-wallpaper   readability
                  devices

### Decision Tree 3: Form Factor Adaptation

        ┌── INPUT: What devices are targeted?
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
[Phone Only]      [Phone + Tablet]   [All Android]
Compact window    Compact + Medium   Phone, tablet,
size class        + Expanded         watch, TV, auto
   │                 │                  │
   ▼                 ▼                  ▼
Single layout     Adaptive layouts   Canonical layouts
with bottom nav   per size class:    per device type
→ test on 3       compact=bottom     → read platform-
screen sizes      nav, medium=rail   specifics.md for
                  expanded=drawer    each form factor

## Core Workflow
<!-- STANDARD: 3min -->

### Mode 1: Design from Scratch

**Goal:** Produce MD3-compliant screen designs that work across window size classes.

**Phase 0 — Research Gate (5 min)**
1. Determine target API level and form factor(s)
2. Execute Research Gate steps: fetch current MD3 component catalog, Dynamic Color guidelines, and platform-specific docs
3. Tag all subsequent output with confidence levels

**Phase 1 — Window Size Class & Layout (5 min)**
1. Identify target window size classes: Compact (<600dp), Medium (600-840dp), Expanded (>840dp)
2. Select canonical layout per class:
   - Compact: Single-pane, bottom navigation, FAB
   - Medium: List-Detail (1/3 + 2/3) or Navigation Rail
   - Expanded: List-Detail or Supporting Pane with permanent Navigation Drawer
3. Define how the layout transforms at each breakpoint — never "responsive by accident"
4. Read `references/platform-specifics.md` for form-factor-specific patterns

**Phase 2 — Color & Theming (5 min)**
1. Decide Dynamic Color strategy:
   - **Adopt**: Use `MaterialTheme` with `dynamicColor = true` (utility apps, tools)
   - **Override**: Use static `ColorScheme` with brand colors + Dynamic Color for surfaces only
   - **Reject**: Static scheme entirely (games, brand-heavy apps)
2. Define light and dark theme variants for every color role
3. Verify all color pairs pass `md3_checker.py contrast` at 4.5:1 (normal) or 3:1 (large text)
4. Test with 3 wildly different wallpaper scenarios if using Dynamic Color
5. Read `references/dynamic-color.md` for implementation patterns

**Phase 3 — Typography & Scaling (5 min)**
1. Set MD3 type scale: Display → Headline → Title → Body → Label
2. Define behavior at 200% font scale: truncation strategy, reflow, or scroll
3. Use `sp` units everywhere — never `dp` for text
4. Body text minimum: 16sp (accessibility baseline + MD3 default `bodyLarge`)
5. Verify no text clipping at 200% scale on the smallest target screen

**Phase 4 — Components & Interaction (10 min)**
1. Select MD3 components: Filled/Tonal/Outlined/Text buttons, cards, chips, dialogs, etc.
2. Verify component dimensions against `md3_checker.py component` — every component must match spec or document intentional deviation
3. Define interaction states: enabled, hovered, focused, pressed, disabled, dragged
4. Define non-touch interaction: focus order (D-pad/keyboard), rotary behavior (watch), voice commands (Auto)
5. Specify motion: duration (50-700ms per MD3), easing curve (Standard/Emphasized/Decelerated/Accelerated), reduce-motion fallback

**Phase 5 — Accessibility Verification (5 min)**
1. Add `contentDescription` to every meaningful element
2. Define TalkBack traversal order and heading hierarchy
3. Verify touch targets ≥48dp on all interactive elements
4. Test at 200% font scale, extreme color blindness simulations, and reduced motion
5. Read `references/accessibility.md` for platform-specific patterns

### Mode 2: MD3 Audit

**Goal:** Score an existing design or implementation against MD3 guidelines.

**Phase 1 — Gather (5 min)**
1. Identify the target API level and form factor
2. Collect all screens/mockups to audit
3. Build the audit batch JSON (see `templates/md3-audit-template.json`)
4. Execute Research Gate if guidelines may have changed since the design was created

**Phase 2 — Automated Check (2 min)**

```bash
python3 scripts/md3_checker.py batch audit.json

```

**Phase 3 — Manual Review (15 min)**
For each screen, verify what the tool cannot measure:
- Dynamic Color response to 5+ wallpaper scenarios
- Text scaling from 85% to 200% without clipping
- Focus management for keyboard and D-pad navigation
- TalkBack content descriptions and traversal order
- Predictive back gesture compatibility
- Manufacturer skin compatibility (Samsung One UI, Xiaomi MIUI)
- Non-touch input: D-pad, rotary, voice, switch
- Window size class transitions (Compact → Medium → Expanded)

**Phase 4 — Scoring & Report (5 min)**
1. Merge automated + manual findings
2. Assign severity: Critical (contrast fail on primary CTA, unreachable via keyboard), Major (missing contentDescription, window-size-class blind spot), Minor (non-standard animation duration, component spec deviation with valid reason)
3. Score: 100 − (10 × critical) − (5 × major) − (2 × minor)
4. Deliver report: bottom line first, fixes organized by effort

## Run the Compliance Tool
<!-- STANDARD: 3min -->

`scripts/md3_checker.py` (stdlib-only, no dependencies):

```bash
# Contrast ratio: WCAG formula, 4.5:1 threshold for normal text
python3 scripts/md3_checker.py contrast "#8E8E93" "#FFFFFF"
# → [FAILED] Contrast 3.26 < 4.5. Fix: darken foreground or use MD3 on-surface token

# Contrast for large text (3:1 threshold)
python3 scripts/md3_checker.py contrast "#8E8E93" "#FFFFFF" --large-text
# → [PASSED] Contrast 3.26 ≥ 3.0

# Touch target: 48x48 dp MD3 minimum
python3 scripts/md3_checker.py touch-target 40 40
# → [FAILED] Target 40x40 dp < 48x48 dp. Expand to 48x48 dp.

# Component spec: validate against MD3 spec table (24 components)
python3 scripts/md3_checker.py component button-filled height 36
# → [FAILED] button-filled height: 36dp does not match spec (40dp). Adjust to 40dp.

# Batch audit: JSON → scorecard (starts at 100, -10 per violation)
python3 scripts/md3_checker.py batch audit.json --compact
# → {"score": 80, "violations": ["Contrast 3.26 fails for caption", "button-filled height 36≠40dp"]}
```

Batch input shape (`audit.json`):

```json
{
  "checks": [
    {"type": "contrast", "name": "caption-on-surface", "fg": "#8E8E93", "bg": "#FFFFFF"},
    {"type": "contrast", "name": "heading-on-primary", "fg": "#FFFFFF", "bg": "#1A73E8", "large_text": true},
    {"type": "touch-target", "name": "close-icon", "w": 24, "h": 24},
    {"type": "component", "name": "primary-btn", "element": "button-filled", "property": "height", "actual": 36},
    {"type": "component", "name": "dialog-corners", "element": "dialog", "property": "corner-radius", "actual": 12}
  ]
}

```

**Scorecard rubric:**
- **90-100** → Ship. Minor issues only, or documented intentional deviations.
- **70-80** → Fix before release. At least one critical or several major issues.
- **<70** → Systematic rework. Multiple critical violations across screens.

Checks the tool **cannot** measure (assessed manually):
- TalkBack content descriptions and traversal order
- Dynamic Color behavior with varied wallpapers
- Text scaling from 85% to 200%
- Focus management for non-touch navigation
- Predictive back gesture compatibility
- Manufacturer skin transformations
- Window size class transition behavior
- Reduce-motion animation fallback

## Proactive Triggers
<!-- STANDARD: 3min -->

Surface these WITHOUT being asked:

| Trigger | Action | Why |
|---------|--------|-----|
| `file_contains(code, "#[0-9A-Fa-f]{6}")` on Android code | Flag: hardcoded colors detected. Ask about Dynamic Color strategy. | Hardcoded colors survive wallpaper changes. Must use `MaterialTheme.colorScheme` or declare override. |
| `file_contains(code, "Modifier\\.size\\(([0-9]|[1-3][0-9]|4[0-7])\\.dp\\)")` on clickable | Flag: sub-48dp touch target on interactive element. | MD3 minimum is 48dp. Expand with padding or wrap in larger touch area. |
| `file_contains(code, "fontSize.*\\.dp")` NOT `file_contains(code, "\\.sp")` | Flag: text sized in dp instead of sp. | dp ignores system font scale. Use sp to respect user's accessibility setting. |
| `file_contains(code, "Modifier\\.fillMaxWidth\|Modifier\\.fillMaxSize")` AND NOT `file_contains(code, "windowSizeClass\|WindowWidthSizeClass\|BoxWithConstraints")` | Flag: full-width layout without adaptive breakpoints. | Filling max width on a tablet creates unusable stretched layouts. Add window size class gate. |
| `file_contains(code, "clickable\|onClick\|onTap")` AND NOT `file_contains(code, "contentDescription\|semantics\|accessibilityLabel")` | Flag: interactive element without accessibility label. | TalkBack users cannot identify unlabeled interactive elements. |
| `file_contains(code, "AnimatedVisibility\|animate\|animation")` AND NOT `file_contains(code, "reducedMotion\|AnimationConstants\|LookaheadScope")` | Flag: animation without reduced-motion fallback. | 12% of users have motion sensitivity. Must disable or reduce animations when system setting is enabled. |

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

### Upstream (Consumes From)

| Upstream Skill | What We Need | When |
|----------------|-------------|------|
| `ui-ux-designer` | Design system tokens, component specs, interaction patterns | Before designing any component — use the existing design system as foundation |
| `accessibility-auditor` | WCAG 2.2 audit results, accessibility baseline | Before an MD3 audit — incorporate existing accessibility findings |
| `brand-guidelines` | Brand colors, typography preferences, Dynamic Color override strategy | Before designing — determine whether to adopt, override, or reject Dynamic Color |
| `mobile-developer` | Cross-platform mobile design context, Material Design cheatsheet reference | Before designing — understand how Android fits in the broader mobile strategy |

### Downstream (Feeds Into)

| Skill | What We Provide | When |
|-------|----------------|------|
| `android-developer` | MD3-compliant UI specs, color token mappings, accessibility specs, window size class layouts | After design or audit complete — developer picks up verified designs |
| `mobile-developer` | Platform-specific MD3 patterns, Android vs iOS design reconciliation | After multi-platform design — developer reconciles platform differences |
| `frontend-developer` | MD3 patterns applicable to web (Material Web) and cross-platform consistency | When web app shares design language with Android app |
| `accessibility-auditor` | Android-specific accessibility findings (TalkBack, text scaling, non-touch input) | After MD3 audit — feed platform-specific a11y issues into broader WCAG audit |
| `game-ui-designer` | TV UI patterns, D-pad navigation, 10-foot design principles | When designing game menus for Android TV / console-style interfaces |

## What Good Looks Like
<!-- STANDARD: 3min -->

> **MD3 score 100/100 — all checks pass.**
>
> 1. All contrast ratios ≥4.5:1 (normal text) and ≥3:1 (large text). 🟢 tool-verified.
> 2. All interactive elements ≥48x48 dp touch targets. 🟢 tool-verified.
> 3. All component dimensions match MD3 spec or have documented intentional deviations. 🟢 tool-verified.
> 4. Layouts specify behavior at Compact, Medium, and Expanded window classes. 🟢 manual review.
> 5. Dynamic Color strategy declared (adopt/override/reject) and tested with 5+ wallpapers. 🟡 device-tested.
> 6. Typography works from 85% to 200% text scale without clipping. 🟡 device-tested.
> 7. Every element is reachable via D-pad, keyboard, and TalkBack with logical traversal order. 🟡 device-tested.
> 8. Predictive back gesture shows correct destination preview, not blank screen. 🟡 device-tested on Android 14+.
> 9. Animations disabled when reduce-motion system setting is active. 🟡 device-tested.
> 10. Design tested on at least one non-Pixel device (Samsung One UI or budget device). 🟡 device-tested.

## Deliberate Practice
<!-- STANDARD: 3min -->

1. **Design the same screen for 3 form factors.** Take a feature (e.g., "search results") and design it for Compact (phone), Medium (tablet portrait), and Expanded (tablet landscape/desktop). How does the canonical layout change? What becomes visible in the supporting pane that was hidden behind navigation?
2. **Test Dynamic Color with extreme wallpapers.** Generate 5 color schemes from wallpapers: sunset (warm oranges), forest (deep greens), snow (white/blue), neon (saturated pink/cyan), and monochrome (grayscale). Does your design maintain hierarchy and contrast across all five?
3. **Navigate your design with keyboard only.** Tab through every interactive element. Can you reach everything? Is the focus order logical? Do focus indicators have sufficient contrast? Now do the same with Switch Access scanning.
4. **Shrink and stretch.** Take a phone screen and stretch it to 840dp wide. Does the layout gracefully adapt or does it break? Take a tablet layout and compress it to 360dp. Does content become unreachable?

## References
<!-- STANDARD: 3min -->

- `references/platform-specifics.md` — Form-factor-specific patterns: phone, tablet/foldable, Wear OS, Android TV, Android Auto, ChromeOS
- `references/dynamic-color.md` — Material You pipeline, HCT color space, tonal palette generation, implementation patterns
- `references/accessibility.md` — TalkBack, Switch Access, Voice Access, text scaling, reduce motion, captions, testing tools
- `templates/md3-audit-template.json` — Batch audit JSON template
- [Material Design 3 (official)](https://m3.material.io)
- [Android Design Guidelines](https://developer.android.com/design)
- [Material Design Components (Android)](https://m3.material.io/develop/android)
- [Android Accessibility](https://developer.android.com/guide/topics/ui/accessibility)

## When to Use
<!-- STANDARD: 3min -->

| Condition | Use This Skill | Use Instead |
|-----------|---------------|-------------|
| Designing Android app UI with Material Design 3 | ✅ Apply MD3 component specs, Dynamic Color, window size classes | — |
| Auditing existing Android app for MD3 compliance | ✅ Run `md3_checker.py` automated audit with research gate | — |
| Implementing Dynamic Color / Material You | ✅ HCT color space, tonal palette generation, wallpaper-based theming | — |
| Designing for Wear OS, Android TV, or Android Auto | ✅ Platform-specific MD3 patterns and component adaptations | — |
| Designing for large screens (tablets, foldables, ChromeOS) | ✅ Window size classes, canonical layouts (List-Detail, Supporting Pane) | — |
| Auditing iOS app for HIG compliance | ❌ | `apple-hig-expert` |
| General WCAG 2.2 accessibility audit (non-Android) | ❌ | `accessibility-auditor` |
| Web frontend UI design (non-Material Web) | ❌ | `ui-ux-designer` or `frontend-developer` |
| Game UI design for Android TV | ✅ D-pad navigation, 10-foot design principles, TV layout patterns | — |

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Design looks correct on Pixel but broken on Samsung — One UI overrides shape, font, and color | $25K-$75K in device-specific bug fixes; 34% of Android users are on Samsung devices — a broken Samsung experience alienates 1/3 of users | Use system components (`MaterialTheme`) exclusively. Never custom-draw elements that bypass the theme engine. Test on at least one non-Pixel device (Samsung, OnePlus, Xiaomi) before release |
| Missing window size class handling — single-column layout stretched to 10-inch tablet looks broken | $30K-$100K in tablet/foldable redesign; Google Play may feature-reject apps without large-screen optimization | Add `WindowWidthSizeClass` checks. Canonical layouts: List-Detail for Expanded, Supporting Pane for Medium. Test at 360dp, 600dp, and 840dp widths |
| Dynamic Color adoption without brand color override — brand colors become unrecognizable on certain wallpapers | $20K-$60K in brand identity erosion; marketing team escalates when app icon/launch screen doesn't match in-app colors | Override `primary` role with brand color. Keep Dynamic Color for containers and surfaces. Declare strategy explicitly: adopt/override/reject with documented rationale |
| Content unreachable at 200% text scale — TalkBack and Switch Access users cannot complete workflows | $30K-$150K in accessibility lawsuit exposure; Google Play Store accessibility filtering may reduce discoverability | Test typography at 85% and 200% system font scale. No text truncation, overlap, or layout breakage. Scrollable containers for content that exceeds viewport |
| D-pad/Keyboard navigation landing on invisible or off-screen elements — TV and ChromeOS users stuck | $25K-$80K in TV app rejection or refund request rate; Wear OS rotary input and TV D-pad are primary interaction methods | Focus must never land on invisible or off-screen elements. Set `focusable = false` on hidden items. Test non-touch navigation on all target form factors |
| Predictive back gesture shows blank screen — app feels unpolished on Android 14+ | $15K-$50K in UX rework; back gesture is the most-used navigation action — a blank screen breaks user trust | Implement `OnBackInvokedCallback` with destination preview. Register during `onViewCreated`. Test with predictive back enabled in Developer Options |
| TalkBack reads content in wrong order — Compose layout order ≠ semantic order | $20K-$60K in accessibility remediation; screen reader users abandon apps with broken navigation | Use `Modifier.semantics { isTraversalGroup = true }` on containers. Explicit `contentDescription` ordering. Test with TalkBack gesture navigation through every screen |
| Touch targets below 48×48dp — users with motor impairments cannot reliably tap controls | $25K-$75K in accessibility remediation; regulatory non-compliance under EN 301 549 in EU markets | Minimum 48×48dp hit area on every interactive element. Use `.padding()` or `Modifier.size()` to expand small icon tap regions. Verify via `md3_checker.py --touch-targets` |

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| `md3_checker.py` contrast passes but manual review on device fails | Checked against flat `surface` color, but actual background is a gradient or image | Use MD3 tokens on their designated surfaces. Custom color pairs must be tested on the actual composited background. |
| Design looks correct on Pixel, broken on Samsung | Samsung One UI overrides shape, font, and color | Use system components (`MaterialTheme`) — they survive manufacturer transformation. Avoid custom-drawn elements that bypass the theme engine. |
| Layout breaks on tablet — single column stretched to 10 inches | Missing window size class handling | Add `WindowWidthSizeClass` checks. Use canonical layouts (List-Detail, Supporting Pane) for Medium/Expanded classes. |
| Dynamic Color makes brand colors unrecognizable | Full adoption of Dynamic Color without brand color override | Override `primary` role with brand color. Keep Dynamic Color for containers and surfaces. |
| TalkBack reads content in wrong order | Compose layout order ≠ semantic order | Use `Modifier.semantics { isTraversalGroup = true }` and explicit `contentDescription` ordering. |
| Predictive back shows blank screen | App intercepts back without implementing `OnBackInvokedCallback` | Implement `OnBackInvokedDispatcher` with destination preview. Register the callback during `onViewCreated`. |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Decision | Status | Timestamp |
|----------|--------|-----------|
| (none yet) | — | — |

## Best Practices

1. **Do pin your Material Design version and run the research gate before every design session** — MD3 is a living spec that changes between Android releases. A component API valid in October 2025 may be deprecated by April 2026. Run `web_fetch("https://m3.material.io/components")` before producing output, and tag every claim with a confidence level: `[VERIFIED]`, `[SPEC-VERSION]`, `[INFERRED]`. Shipping a design built on stale training data costs $15,000-$40,000 in rework when developers discover the component doesn't exist in the current library.
2. **Prefer Dynamic Color adoption with explicit brand overrides over static color schemes** — Material You's tonal palette system generates accessible, harmonious color schemes automatically from a single seed color. Rejecting Dynamic Color means manually maintaining 40+ color tokens across light and dark themes — a $5,000-$10,000/year maintenance burden. If brand colors are non-negotiable, declare explicit overrides for specific roles (primary, secondary) while letting Dynamic Color handle neutral, surface, and error tones.
3. **Always test typography at 85% and 200% system font scale** — Android's font scale setting ranges from 0.85x to 2.0x. Text truncation, overlap, or layout breakage at either extreme means your layout is not truly adaptive. A screen that works at 100% but breaks at 200% fails WCAG 1.4.4 (Resize Text) and excludes users with visual impairments. Test by toggling font scale in Settings → Accessibility → Font size on a real device — emulators lie about text rendering.
4. **Never use fixed-pixel layouts for Android — design with window size classes (Compact, Medium, Expanded)** — Android runs on phones (360dp), foldables (600-840dp), tablets (840+dp), ChromeOS (1200+dp), and desktop mode. A layout designed at 360dp that breaks at 840dp means your app gets a 2-star Play Store rating on tablets. Cost of retrofitting large-screen support post-launch: $20,000-$60,000 vs. $3,000-$8,000 if designed upfront with adaptive layouts.
5. **Measure TalkBack completion rate** — Can a blind user navigate every screen and complete the primary task (e.g., book a flight, send a message) using only TalkBack? Target: 100% task completion on critical paths. Instrument user testing with screen-reader users; every `contentDescription` gap, missing `semantics { isTraversalGroup = true }`, or incorrect traversal order is a regression. An inaccessible critical path costs $50,000-$250,000 in ADA litigation and Play Store delisting risk.

## Production Checklist

Before deploying or delivering work from this skill, verify:

| # | Check | Verify |
|---|-------|--------|
| ☐ | Research Gate executed — all design claims verified against current m3.material.io documentation; output carries confidence tags | Run `web_fetch("https://m3.material.io/components")`; grep output for `[VERIFIED]`, `[SPEC-VERSION]`, `[INFERRED]` tags on every design assertion |
| ☐ | All interactive elements meet MD3 minimum touch target (48×48dp) with adequate spacing between tappable regions | Run `md3_checker.py` or Layout Inspector; flag any touch target below 48dp in either dimension |
| ☐ | Window size class behavior specified for Compact, Medium, and Expanded breakpoints with canonical layouts per class | Verify each screen renders correctly at all three size classes on physical devices or emulator; List-Detail for Expanded, single-column for Compact |
| ☐ | Dynamic Color strategy explicitly declared (adopt/reject/override) with brand color handling and rationale documented | Check that `dynamicColorScheme` is used OR a documented override strategy explains why brand colors deviate |
| ☐ | Color contrast meets WCAG AA minimums (4.5:1 normal text, 3:1 large text) across all color roles in both light and dark themes | Run `md3_checker.py --contrast` or Android Accessibility Scanner; flag every ratio below threshold |
| ☐ | Typography tested at 85% and 200% system font scale — no text truncation, overlap, or layout breakage | Toggle font scale in Settings → Accessibility → Font size on physical device; every screen must remain usable at both extremes |
| ☐ | TalkBack announces every meaningful element with correct `contentDescription`; traversal order matches visual order; `semantics { isTraversalGroup = true }` set on containers | Navigate every screen via TalkBack gesture navigation; verify `contentDescription` on all interactive and informative elements |
| ☐ | Rollback plan is documented and tested | Verify: APK/AAB rollback to previous version doesn't corrupt user data; Dynamic Color tokens persist across rollback; Play Store staged rollout at 10% with rollback trigger on crash rate > 0.5% |

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|---|---|
| ☐ | Complete when all interactive elements meet MD3 minimum touch target (48×48dp) with adequate spacing between tappable regions | Verify via `md3_checker.py` or layout inspector; flag any touch target below 48dp in either dimension |
| ☐ | Complete when window size class behavior is specified for Compact, Medium, and Expanded breakpoints with canonical layouts per class | Verify each screen renders correctly at all three size classes; List-Detail for Expanded, single-column for Compact |
| ☐ | Complete when Dynamic Color strategy is explicitly declared (adopt/reject/override) with brand color handling documented | Verify that either `dynamicColorScheme` is used OR a documented override strategy explains why brand colors cannot be dynamic |
| ☐ | Complete when all component dimensions match MD3 spec tolerances (or deviations are explicitly documented with rationale) | Verify via `md3_checker.py --components` that padding, corner radii, and elevation values match the spec for each component type |
| ☐ | Complete when color contrast meets WCAG AA minimums (4.5:1 normal text, 3:1 large text) across all color roles and both light/dark themes | Verify via `md3_checker.py --contrast` or Android Accessibility Scanner; flag every ratio below threshold |
| ☐ | Complete when typography is tested at 85% and 200% system font scale with no text truncation, overlap, or layout breakage | Verify by toggling font scale in Android Settings → Accessibility → Font size; every screen must remain usable at both extremes |
| ☐ | Complete when TalkBack announces every meaningful element with correct contentDescription, traversal order matches visual order | Verify via TalkBack gesture navigation through every screen; check that `semantics { isTraversalGroup = true }` is set on containers |
| ☐ | Complete when non-touch navigation is fully defined: D-pad for TV, rotary for Wear OS, keyboard for ChromeOS, switch access for accessibility | Verify by testing directional navigation on each target form factor; focus must never land on invisible or off-screen elements |
| ☐ | Complete when predictive back gesture compatibility is confirmed: OnBackInvokedCallback registered, destination preview renders for in-app navigation | Verify by enabling predictive back in Developer Options and performing back gesture from every screen edge |
| ☐ | Complete when all MD3 claims carry confidence tags: [VERIFIED], [SPEC-VERSION], [COMMON-PRACTICE], [INFERRED], or [UNKNOWN] | Verify via grep that every design assertion in output has exactly one confidence tag adjacent to it |

## Verification Guardrails
<!-- STANDARD: 3min -->
- [ ] Research Gate executed against current m3.material.io documentation
- [ ] All contrast ratios verified by `md3_checker.py` or manual WCAG calculation
- [ ] All interactive elements ≥48x48 dp
- [ ] All component dimensions match MD3 spec (or deviations documented)
- [ ] Window size class behavior specified for Compact, Medium, and Expanded
- [ ] Dynamic Color strategy explicitly declared (adopt/override/reject)
- [ ] Typography tested at 85% and 200% system font scale
- [ ] Non-touch navigation defined: D-pad, keyboard, rotary, voice
- [ ] TalkBack content descriptions on all meaningful elements
- [ ] Predictive back gesture compatibility confirmed
- [ ] Reduce-motion fallback specified for all animations
- [ ] Confidence tagged on every claim: `[VERIFIED]` / `[SPEC-VERSION]` / `[COMMON-PRACTICE]` / `[INFERRED]` / `[UNKNOWN]`

## Anti-Hallucination
<!-- STANDARD: 3min -->

* Never guess security. If work touches auth, payments, or PII, route to security-reviewer.
This skill covers Material Design 3 guidelines that evolve independently of Android OS releases. MD3 updates are published continuously at m3.material.io. Never treat training data as current — always execute the Research Gate.

- `[VERIFIED]` — Confirmed against live m3.material.io or developer.android.com/design
- `[SPEC-VERSION]` — True for a specific MD3 version snapshot — may have changed since
- `[COMMON-PRACTICE]` — Widely used in Android ecosystem, not formally specified
- `[INFERRED]` — Reasonable extrapolation from MD3 principles
- `[UNKNOWN]` — Requires verification against current documentation
