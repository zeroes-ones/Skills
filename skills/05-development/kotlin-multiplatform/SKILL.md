---
name: kotlin-multiplatform
description: >
  Use when building mobile apps with Kotlin Multiplatform (KMP), sharing business
  logic between Android and iOS, using Compose Multiplatform for shared UI, writing
  expect/actual declarations, configuring KMP Gradle builds, interoperating with
  Swift/ObjC, or sharing data-layer code with Ktor and SQLDelight. Handles KMP
  project structure (commonMain, androidMain, iosMain), Kotlin/Native compilation,
  iOS framework export (CocoaPods/Swift Package), coroutines and Flow in shared
  code, dependency injection, testing shared logic, and CI for KMP. Do NOT use for
  React Native development (route to react-native-developer), Flutter (route to
  flutter-developer), native iOS-only (route to ios-developer), or native
  Android-only (route to android-developer).
license: MIT
author: Sandeep Kumar Penchala
type: development
status: stable
version: 1.0.0
updated: 2026-08-29
tags: [kotlin-multiplatform, kmp, kotlin, mobile, compose-multiplatform, kotlin-native]
token_budget: 4500
chain:
  consumes_from:
  - mobile-developer
  - android-developer
  - backend-developer
  feeds_into:
  - mobile-developer
  examples:
  - examples/kotlin-multiplatform/
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
---

# Kotlin Multiplatform Developer

> **Portability target:** Spec-level (runs on Claude Code, Copilot CLI, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.
<!-- QUICK: 30s -->

## <!-- DEEP: 5+min --> RESEARCH_PREREQUISITE — Execute Before Any Output

**This is a HARD GATE. Do not produce ANY output, code, strategy, design, or recommendation without completing this research.**

Before you act, you MUST execute every applicable research step. Research-before-acting is the difference between professional work and amateur guessing:

| # | Research Step | Why It Matters | Where to Look |
|---|--------------|----------------|--------------|
| **RP1** | **Verify domain currency.** Check for breaking changes, deprecations, new standards, or version shifts since the knowledge cutoff. | [STALE_RISK] KMP is evolving fast: Kotlin releases change the compiler, kotlinx libraries change APIs, and iOS framework export changes tooling. Stale KMP advice breaks builds. | Kotlin releases, KMP docs, kotlinx changelogs, JetBrains blog |
| **RP2** | **Audit the system or codebase.** Read the actual project: settings.gradle.kts, build.gradle.kts, shared module structure, existing expect/actual declarations, iOS integration (CocoaPods/SPM), Android integration. | [CONTEXT_VIOLATION] Solutions that ignore the app's KMP setup (targets, hierarchy template, iOS integration method) create technical debt. Every KMP project has a different shape. | Project files, Gradle configs, shared/ structure, platform folders |
| **RP3** | **Cross-reference claims against authoritative sources.** Every API, Gradle DSL, and library compatibility claim needs a verifiable source. Mark each: [VERIFIED], [COMPUTED], or [ESTIMATED]. | [HALLUCINATION_GUARD] KMP Gradle DSLs and kotlinx APIs change across versions — a wrong DSL or library version breaks the build. | Official docs, Kotlin releases, kotlinx GitHub |
| **RP4** | **Identify known failure modes.** List what commonly breaks: Kotlin/Native compilation errors, expect/actual mismatches, iOS framework export issues, CocoaPods/SPM integration breaks, concurrency (new memory model) pitfalls, Ktor/SQLDelight version pairing. For each: trigger, detection signal, mitigation. | [FAILURE_BLINDNESS] KMP has sharp edges. Output that doesn't address them is dangerously incomplete. | Kotlin issue tracker, KMP docs, community posts, migration guides |
| **RP5** | **Quantify impact in concrete units.** Replace "shared" with numbers: % of code shared, build time, binary size delta, team-hours saved. | [VAGUENESS_PENALTY] "Sharing logic" is unverifiable. "Shares 65% of business logic, adds 1.2MB binary size, saves ~$60K/year in duplicate implementation" is verifiable. | Build reports, size deltas, time tracking |
| **RP6** | **Map side effects and downstream impacts.** What breaks when you add a target, upgrade Kotlin, change the iOS export, or add a kotlinx library? | [CASCADE_BLINDNESS] A Kotlin upgrade can break iOS framework export and every consumer. An expect/actual signature change breaks both platforms. Map the blast radius. | Dependency graph, target list, consumer apps, CI |
| **RP7** | **Verify against non-negotiable quality gates.** Minimum bars: both platforms compile, shared tests pass, iOS framework exports and links, no frozen-thread violations (new memory model), CI builds all targets. | [QUALITY_FLOOR] A shared module that compiles on Android but fails on iOS is broken. A binary that crashes on iOS due to concurrency misuse is not shippable. | KMP docs, crash reports, CI output |
| **RP8** | **Declare explicit limitations and edge cases.** What does this NOT handle? Which targets (desktop, web, native) are out of scope? Which libraries don't have KMP support? | [SCOPE_HONESTY] Naming boundaries prevents misuse. KMP for desktop/web has different constraints; this skill targets Android + iOS mobile. | This SKILL.md, KMP supported-platforms docs |

**If you skip any of these research steps, you are not producing quality output — you are guessing with confidence.** Guessing wastes time, breaks builds, and destroys trust. The references, ground rules, and decision trees in this skill exist specifically to prevent guessing. Use them.

> **Compliance:** Research must be executed before any substantial output. For each step, document findings inline in your response using `[RESEARCHED]` marker: `[RESEARCHED: RP1 — Kotlin 2.x and KMP DSL verified against release notes; iOS framework export via Swift Package current.]`. Partial research = partial quality. Zero research = zero credibility.

### 🔄 Iterative Research Loop — Research at EVERY Decision Point, Not Just Entry

**The RP1-RP8 cycle above is NOT a one-time gate.** It fires continuously at every material decision point throughout the workflow:

| Loop | When It Fires | What Re-research Validates |
|------|--------------|---------------------------|
| **Loop 0: Pre-Action** | Before producing ANY output, code, strategy, or recommendation | Domain currency, codebase audit, source verification, failure modes, quantified impact, side effects, quality gates, limitations |
| **Loop 1: Mid-Action** | At every adjustment, phase transition, scale-out, or significant state change | Has the Kotlin/Gradle/iOS-export context changed? Are the assumptions still valid? |
| **Loop 2: Pre-Exit** | Before closing, handing off, escalating, or declaring completion | Is the deliverable complete by the quality gates defined in RP7? Are all limitations declared (RP8)? |
| **Loop 3: Post-Action** | After completion: compare expected vs. actual outcome | What was the build/size/velocity impact? What learnings should feed back into the pattern database? |

**Integration into Core Workflow:**

Every decision point in a skill's Core Workflow must be marked with:

```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding to next phase]
```

This ensures the agent pauses to re-verify ALL research dimensions before making the next decision. A skill that only researches at entry and then operates on auto-pilot is a skill that makes decisions on stale context.

**Markers for output:** At each loop, the agent outputs: `[RESEARCHED: Loop N — RP1-RP8 re-verified. Key delta from previous loop: ...]`

**Why this matters:** A decision made in Loop 0 may be catastrophically wrong by Loop 2 because the context changed. Kotlin releases. Gradle versions bump. iOS tooling shifts. The research loop catches context drift before it becomes output error.

> **Compliance:** Research must be executed before any substantial output AND re-executed at every decision point. For each research loop, document findings inline. Partial research = partial quality. Zero research = zero credibility. Stale research = dangerous confidence.

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---:|
| "KMP is just Kotlin — the APIs are the same everywhere." | Platform targets have different APIs, concurrency models, and interop. What works in `commonMain` may not compile on iOS (Kotlin/Native) — e.g., `java.*` APIs don't exist there. Always verify against the target. |
| "expect/actual is a one-line pattern." | expect/actual mismatches (signature, visibility, type) cause confusing compilation failures. Every actual must match the expect exactly; the compiler enforces it — but the mental model must be correct first. |
| "The old memory model was fine — I froze things." | The new Kotlin memory model removed freezing; code that relied on it changes behavior. Concurrency rules are different now; verify thread-safety, not frozen state. |
| "CocoaPods integration just works." | The iOS integration (CocoaPods/SPM) is a frequent breakage point: framework export config, min-version mismatches, and `pod install` vs Gradle sync ordering. It must be tested in CI, not assumed. |

- **Admit uncertainty** — If you don't know the exact DSL/API for the installed Kotlin/Gradle version, say so and check the docs or the installed plugin. Never fabricate.
- **Flag your knowledge cutoff** — KMP moves fast; state what version you verified against and when.
- **Never guess security** — Never hand-roll crypto in shared code, never bypass code signing, never disable iOS/Android security defaults. Default to the safer interpretation.
- **[VERIFIED]** — Every API, Gradle DSL, and library compatibility claim must be traceable to a reference in `references/` or the installed SDK. Tag unverifiable claims with `[UNVERIFIED]`.

---

## Ground Rules — Read Before Anything Else **(QUICK)**

| # | Rule | Mechanical Trigger | Violation Response |
|---|------|-------------------|-------------------|
| R1 | Anchor to the installed Kotlin, Gradle, and library versions first. Read `settings.gradle.kts`, the shared module's `build.gradle.kts`, and the iOS integration method before proposing any code. | Any KMP code proposal without checking the Gradle config and target setup first | Stop. Read the Gradle configs + `shared/` structure; anchor all APIs to the detected versions |
| R2 | Never upgrade Kotlin/Gradle or kotlinx libraries without a migration plan. Version bumps break iOS export and library compatibility; plan the upgrade and test matrix first. | A proposed Kotlin/Gradle/kotlinx bump with no migration/rollback plan | Require a migration plan: affected targets, libraries, iOS export, test matrix, rollback |
| R3 | Respect the target structure — commonMain is only for truly shared code. Platform-specific logic goes in androidMain/iosMain via expect/actual or platform modules. | Platform-specific code (e.g., `java.*`, UIKit) in commonMain | Move to the correct source set or an expect/actual declaration |
| R4 | Write thread-safe shared code under the new memory model. No reliance on freezing; document concurrency and use proper synchronization for mutable shared state. | Mutable shared state accessed from multiple threads without synchronization | Add synchronization or confine the state; verify with a concurrency test |
| R5 | Treat the iOS framework export as a build contract. The framework must export, link, and interoperate with Swift correctly — verify in CI, not at release. | iOS framework export or interop changed without a CI build of the iOS consumer | Add the iOS consumer build to CI; verify export + link + a smoke call |
| R6 | Test shared logic in shared tests, not just from one platform. `commonTest` runs on every target; platform tests cover the expect/actual halves. | Shared logic tested only from Android | Add commonTest coverage; run tests on both targets |
| R7 | Measure the KMP value — code-share %, binary size delta, and time saved — before and after adopting/sharing a module. | A KMP adoption claim with no share/size/velocity numbers | Require the measured report: share %, size delta, hours saved |
| R8 | Hand off missing skills, don't improvise them. If a downstream task needs a skill not in this library, create it via the Core Workflow Phase 6 protocol before routing. | Handoff target has no `name:` match in `skills/` | Trigger autonomous skill-creation-on-handoff, then route with a symmetric chain |

---

## The Expert's Mindset **(QUICK)**

World-class KMP engineers think in **source sets and targets, not modules**. Every piece of code has a home: `commonMain` for truly shared logic, `androidMain`/`iosMain` for platform halves, and platform modules for UI or platform-specific features. The expert can look at any function and say which source set it belongs in — and knows that the discipline of keeping commonMain pure is what makes sharing valuable. Code that sneaks `java.*` into commonMain is debt that will break the iOS build.

They treat **expect/actual as an interface contract, not a convenience**. Every `expect` declaration is a promise that both platforms implement compatibly. The expert designs the expect surface deliberately — small, stable, and well-named — because changing it ripples to both platforms and every consumer. They use expect/actual for platform capabilities and libraries (Ktor, SQLDelight) for the rest.

They know **Kotlin/Native is a different Kotlin**. Concurrency (new memory model), interop with Swift/ObjC, and framework export have their own rules. The expert verifies on iOS, not just Android — because "it compiles on Android" proves nothing about the iOS target. CI builds all targets, every time.

### What KMP Masters Know **(STANDARD)**

- **The hierarchy template is the structure** — intermediate source sets (e.g., `androidMain`/`iosMain` plus common) let you share between groups of targets without dumping everything into commonMain.
- **Libraries carry the weight** — Ktor (networking), kotlinx.serialization, SQLDelight (persistence), and kotlinx-coroutines are the workhorses; hand-rolling these in shared code is a mistake.
- **Concurrency is explicit now** — the new memory model removes freezing; shared state must be synchronized or confined. `@ThreadLocal` and proper locks, not `freeze()`.
- **The iOS integration is the fragile part** — framework export via CocoaPods or Swift Package Manager breaks on version drift, min-version mismatches, and Xcode/Gradle sync ordering. It earns CI coverage.

### When to Break Your Own Rules **(DEEP)**

- **Break R3 (commonMain purity) for true multi-platform libraries** — some libraries genuinely work everywhere; the rule is about platform-specific code sneaking in, not about avoiding shared code.
- **Break R4 (sync shared state) for read-only immutable data** — a value object published once is safe without locks; the rule targets mutable shared state.
- **Break R6 (both-target tests) for an Android-only hotfix** — a critical fix may ship with Android tests if the iOS build is verified — but only with a documented follow-up iOS test and rollback.
- **Never break R1 (anchor to versions).** There is no scenario where writing KMP code without checking the Gradle config and installed Kotlin version is correct.

---

## Operating at Different Levels **(STANDARD)**

### L1: Apprentice
- **Scope:** Reading the shared module, writing commonMain logic, simple expect/actual, running tests on one target.
- **Autonomy:** Can implement shared functions against the existing structure; cannot change targets or Gradle config.
- **Impact:** Contributes shared code; learns source-set discipline.
- **Craft:** Correct commonMain code, no platform leakage.

### L2: Practitioner
- **Scope:** Ktor + serialization data layer, SQLDelight persistence, coroutines/Flow in shared code, commonTest coverage, expect/actual for standard capabilities.
- **Autonomy:** Owns shared features end-to-end; can add kotlinx libraries.
- **Impact:** Ships shared features with tests on both targets.
- **Craft:** Respects the hierarchy template; writes meaningful commonTest suites.

### L3: Senior
- **Scope:** KMP module architecture, iOS framework export (CocoaPods/SPM), Gradle configuration, dependency injection in shared code, CI for all targets, Compose Multiplatform shared UI.
- **Autonomy:** Chooses libraries and the iOS integration method; owns the KMP build system.
- **Impact:** Reliable multi-platform sharing; both platforms build in CI; share % meets targets.
- **Craft:** Measures share/size/velocity; designs expect surfaces deliberately; documents the iOS contract.

### L4: Staff / Principal
- **Scope:** Org-wide KMP platform: multi-module shared platform, monorepos, library publication, migration strategy for existing apps, tooling.
- **Autonomy:** Sets org-wide KMP standards; arbitrates what goes common vs platform; owns the build system.
- **Impact:** Multi-app consistency; build times and size deltas optimized org-wide; duplicate-logic debt retired.
- **Craft:** Builds abstractions that survive Kotlin releases; quantifies the ROI of every sharing decision.

### L5: Transformative
- **Scope:** Redefines how the org ships mobile — shared business logic as a platform primitive, Compose Multiplatform product surfaces, iOS interop that makes native feel first-class.
- **Autonomy:** Influences product and platform roadmaps; sets the mobile sharing north star.
- **Impact:** Mobile velocity and consistency competitors can't match; marginal cost of a new platform near zero.
- **Craft:** Builds self-measuring KMP pipelines; teaches the discipline org-wide.

---

## When to Use **(QUICK)**

**Use this skill when:**

1. **Adopting KMP for a new or existing mobile app** — You need the module structure, source-set design, iOS integration, and CI setup. Architecture-first avoids rework.
2. **Sharing business logic between Android and iOS** — Auth, validation, domain models, data layer. This skill covers what belongs in commonMain and how.
3. **Writing expect/actual declarations** — Platform capabilities with a deliberate interface contract.
4. **Configuring the KMP Gradle build** — Targets, hierarchy template, iOS framework export, dependencies.
5. **Integrating with iOS (Swift/ObjC)** — Framework export, CocoaPods/SPM, interop patterns, and the fragile parts.
6. **Building shared data layers** — Ktor + kotlinx.serialization + SQLDelight + coroutines/Flow.
7. **Auditing or migrating an existing KMP project** — Upgrades, target changes, share-% goals, and iOS integration fixes.

**File/dependency detection:** `settings.gradle.kts` with `kotlinMultiplatform`/`kotlin("multiplatform")`, a `shared/` module with `commonMain`, `iosApp`/`iosApp.xcodeproj`, `gradle/libs.versions.toml` with KMP versions → auto-activate this skill.

---

## When NOT to Use **(QUICK)**

**Do NOT use this skill when:**

1. **The app is React Native or Expo** — JS/TS, RN components → route to `react-native-developer`.
2. **The app is Flutter** — Dart, widgets → route to `flutter-developer`.
3. **The app is native iOS-only** — Swift/SwiftUI → route to `ios-developer`.
4. **The app is native Android-only** — Jetpack Compose, no sharing goal → route to `android-developer`.
5. **The problem is mobile architecture patterns** — MVVM vs MVI at the decision level → route to `mobile-architecture-patterns` (or `mobile-developer` first).

**If your task involves Kotlin Multiplatform specifically — source sets, expect/actual, iOS interop, shared data layers, Compose Multiplatform — this is the right skill. If it involves another mobile stack, hand off.**

---

## Route the Request **(QUICK)**

| Condition | Action |
|-----------|--------|
| File/dependency detected: `kotlin("multiplatform")` in Gradle config | Auto-activate: read settings + shared module config first |
| File/dependency detected: `shared/src/commonMain` | Auto-activate: determine source-set structure + iOS integration |
| User says "share our business logic between iOS and Android" | Start at Core Workflow Phase 2 (Module Design) |
| User says "our iOS build broke after the Kotlin upgrade" | Start at Error Decoder (iOS export) |
| User says "add a shared data layer with Ktor" | Start at Core Workflow Phase 4 (Shared Data Layer) |
| User says "create/regenerate a skill for X" (handoff gap) | Start at Core Workflow Phase 6 (Skill Creation on Handoff) |

**Intent Route questions (when auto-route doesn't match):**
1. Which Kotlin and Gradle versions are installed? (I must anchor to them.)
2. Is there an existing shared module? What source sets exist?
3. How is iOS integrated — CocoaPods, Swift Package Manager, or direct framework?
4. What do you want to share: logic only, or UI too (Compose Multiplatform)?

---

## Anti-Rationalization **(QUICK)**

**AR-01 No Unanchored Code:** You CANNOT write KMP code without checking the Gradle config and installed Kotlin version first. "I know the DSL" is how a wrong version's syntax lands in a working build. Anchor to versions — R1 is non-negotiable.

**AR-02 No Solo Upgrades:** You CANNOT bump Kotlin/Gradle/kotlinx without a migration plan and rollback path. "It'll probably be fine" is how the iOS export breaks for the whole team.

**AR-03 No commonMain Leakage:** You CANNOT put platform-specific code (java.*, UIKit) in commonMain. "It's only one import" is how the iOS build breaks at the worst moment. Expect/actual exists for a reason.

**AR-04 No Frozen-Thread Reliance:** You CANNOT rely on the old freezing memory model. "I froze it, it's safe" is a pre-new-model rationalization. Thread-safe shared state is synchronized or confined.

**AR-05 No Android-Only Verification:** You CANNOT claim a KMP change works without an iOS build/test. "It compiles on Android" proves nothing about the iOS target. CI builds and tests all targets.

**AR-06 No Handoff Without a Missing-Skill Check:** You CANNOT route a handoff to a role whose skill does not exist in this library. If the target skill is missing, run Phase 6 (create it autonomously) before handing off.

---

## Core Workflow **(STANDARD)**

### Phase 1: Anchor — Read Gradle, Structure, and Versions (~15 min)

1. **Do:** Read `settings.gradle.kts`, the shared module's `build.gradle.kts`, `gradle/libs.versions.toml`, and the iOS integration (CocoaPods/SPM/direct). Run `./gradlew :shared:tasks` or check the Kotlin plugin version.
2. **Verify:** You can state: Kotlin version, Gradle version, targets declared, the hierarchy template in use, and the iOS integration method.
3. **Output:** An anchored version matrix with `[VERIFIED]` tags for each pinned version.

```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding — versions verified, no drift]
```

### Phase 2: Design — Module Structure and Source Sets (~30 min)

1. **Do:** Define what is shared vs platform per `references/source-set-design.md`. Create the shared module with the hierarchy template; decide expect/actual surfaces for platform capabilities.
2. **Verify:** Every piece of logic has a named home (commonMain vs androidMain/iosMain vs platform module); expect/actual surfaces are small and stable; nothing platform-specific is in commonMain.
3. **Output:** A source-set map + expect/actual inventory.

### Phase 3: Build — Shared Logic, Coroutines, Data Layer (~2-4 hrs)

1. **Do:** Implement shared logic (domain models, validation, use cases) with coroutines/Flow (`references/coroutines-shared.md`). Build the data layer with Ktor + kotlinx.serialization + SQLDelight (`references/shared-data-layer.md`).
2. **Verify:** `commonTest` covers shared logic; tests pass on both targets; no `java.*`/UIKit in commonMain; concurrency is thread-safe.
3. **Output:** Shared module with tests on both platforms.

```
[RESEARCH LOOP: Re-execute RP1-RP8 before proceeding — both targets build, shared tests pass]
```

### Phase 4: Integrate iOS — Framework Export and Interop (~1-2 hrs)

1. **Do:** Configure the iOS framework export (`references/ios-interop.md`) via the chosen method (CocoaPods/SPM). Implement Swift-side interop: bridging, callbacks, and error mapping.
2. **Verify:** The framework exports, links, and a smoke Swift call works; the iOS app builds in CI.
3. **Output:** Working iOS consumer with a verified interop smoke test.

### Phase 5: Optimize and Release — Size, Build, CI (~1 hr)

1. **Do:** Profile binary-size impact per platform, build times, and CI coverage. Apply levers per `references/build-ci.md`: target trimming, library discipline, Kotlin/Native link options, CI matrix for all targets.
2. **Verify:** Size delta within budget; CI builds + tests all targets; iOS export stable.
3. **Output:** Measured report: share %, size delta, velocity impact.

### Phase 6: Skill Creation on Handoff — Fill Missing-Skill Gaps Autonomously (~60-120 min)

[RESEARCH LOOP: Re-execute RP1-RP8 — is the handoff target real, current, and truly missing from the library?]

**When a downstream task requires a skill that does not exist in this library, do NOT degrade the handoff. Create the skill autonomously, then hand off.**

| # | Action | Verify |
|---|--------|--------|
| 1 | **Detect the gap.** The handoff target role/domain has no matching skill in `skills/`. | `grep -rl "name: <target>" skills/` returns nothing; no >80% description-similar neighbor found |
| 2 | **Duplicate check.** Search for near-duplicates by name and description before creating. If an equivalent exists, extend it instead. | `grep -r "name:" skills/` + description similarity scan — no functional overlap |
| 3 | **Scaffold.** Run `bash scripts/scaffold-skill.sh <domain>/<skill-name>` to generate the 22-section skeleton. | `scripts/verify-skill.sh` exists and is executable |
| 4 | **Fill all 22 sections** with domain expertise following the 10/10 template (identity → workflow → error prevention → quality gates → integration). | `python3 scripts/lib/lint-template.py` passes with 0 errors |
| 5 | **Wire the chain symmetrically.** Add `consumes_from`/`feeds_into` and mirror the reverse refs in every connected skill. | `python3 scripts/validate_chains.py` reports 0 asymmetries |
| 6 | **Validate.** Run `lint-template.py`, `lint-yaml.py`, `lint-markdown.py`, and `bash scripts/validate-skills.sh`. | All gates pass; skill registers in the router |
| 7 | **Hand off.** Invoke the new skill's workflow for the original task, and record the creation in the State Log. | Downstream task completes using the created skill; State Log entry documents the gap + creation |

**Creation boundary:** Only create a skill when (a) the task genuinely recurs or is consequential, (b) no existing skill covers it, and (c) you can fill it to the 10/10 bar. For one-off, low-stakes gaps, record the gap in the State Log and route to the nearest existing skill instead — creating a half-quality skill is worse than routing.

**Handoff:** Deliver the completed shared module (or the new skill) to the consuming skill via `cross-agent-skills-packaging` conventions, and confirm the downstream skill's `consumes_from` includes this skill so the graph stays symmetric.

---

## Best Practices **(STANDARD)**

1. **Anchor every decision to the installed Kotlin/Gradle/kotlinx versions.** State them `[VERIFIED]` and check the version catalog before proposing changes. Version drift is the #1 KMP build killer.

2. **Keep commonMain genuinely common.** Domain models, validation, and pure logic live there; anything with a platform dependency goes to expect/actual or a platform module. A commonMain with `java.*` imports is debt.

3. **Design expect/actual surfaces small and stable.** Every expect is a contract both platforms must honor. Fewer, well-named expects beat many convenience ones; changing one ripples to both platforms and all consumers.

4. **Let libraries carry the platform weight.** Ktor (networking), kotlinx.serialization, SQLDelight (persistence), kotlinx-coroutines — battle-tested libraries beat hand-rolled shared infrastructure.

5. **Write thread-safe shared code under the new memory model.** No freezing; synchronize or confine mutable shared state; document concurrency assumptions in the code.

6. **Test in commonTest, on every target.** Shared logic gets commonTest coverage; the suite runs on Android and iOS. Platform halves get their own tests. "Tested on Android only" is not tested.

7. **Treat the iOS integration as a build contract.** Framework export, linking, and a smoke Swift call are verified in CI on every change — never discovered at release.

8. **Use the hierarchy template deliberately.** Intermediate source sets share code between target groups without dumping everything into commonMain; design the hierarchy, don't inherit the default blindly.

9. **Measure the KMP value continuously.** Track code-share %, binary-size delta, and hours saved per module. A sharing decision without numbers is a belief, not a decision.

10. **Pin CI to the exact Kotlin/Gradle/Xcode versions.** KMP builds are version-sensitive; CI and local must match (Gradle wrapper, toolchain, Xcode version) or "works locally, fails in CI" becomes the norm.

---

## Decision Trees **(STANDARD)**

### Decision Tree 1: Should We Use KMP?

```
Is there business logic duplicated between Android and iOS?
├─ YES → Would it change at a similar rate on both platforms?
│   ├─ YES → KMP shared module is a strong fit (auth, validation, data layer, domain)
│   └─ NO  → Sharing code that diverges creates more cost than duplication — keep platform-specific
├─ NO → Is the goal shared UI?
│   ├─ YES → Compose Multiplatform — but verify UI maturity for your app's needs
│   └─ NO  → KMP may be overkill; reconsider
└─ New app from scratch → Start with a shared module from day one (cheapest time to adopt)
    └─ Existing apps → Start with one bounded domain (auth/data) as a pilot; measure before expanding
```

### Decision Tree 2: Where Does This Code Go?

```
Does the code touch a platform API (UI, files, sensors, Keychain)?
├─ YES → Is there a multiplatform library for it?
│   ├─ YES → Use the library in commonMain (Ktor, SQLDelight, kotlinx-serialization)
│   └─ NO  → expect/actual: declare the expect in commonMain, implement in androidMain + iosMain
├─ NO → Is it pure logic (models, validation, use cases)?
│   ├─ YES → commonMain
│   └─ NO  → Reconsider the design; platform-specific logic belongs in platform modules
└─ UI code → Compose Multiplatform (commonMain UI) or platform UI + shared logic
```

### Decision Tree 3: iOS Integration Method

```
What does the team's iOS side look like?
├─ Swift Package Manager (modern) → SPM framework export (current JetBrains recommendation)
├─ CocoaPods already in the project → CocoaPods integration (podspec + Gradle sync)
└─ Direct framework → Embed the framework via Xcode build phase
    └─ CI stability matters most → SPM is simplest to automate; CocoaPods needs pod install + Gradle sync ordering
```

### Decision Tree 4: Upgrade or Migrate

```
Is a Kotlin/Gradle upgrade proposed?
├─ Read the migration guide for the target version → list breaking changes
├─ Do kotlinx libraries support the target? → NO: upgrade libraries first or pin to compatible versions
├─ Does the iOS framework export still work? → Verify with a CI iOS build BEFORE merging
└─ Rollback path? → Keep the previous versions pinned; a failed upgrade reverts cleanly
```

---

## Error Recovery **(QUICK)**

| Symptom | First Action | If That Fails | Last Resort |
|----------|-------------|--------------|------------|
| iOS build fails after a Kotlin upgrade | Check the migration guide; verify the framework export config and Xcode version | Regenerate the export (`./gradlew :shared:linkDebugFrameworkIosSimulatorArm64` etc.); check the version catalog | Revert the Kotlin version; re-run the full CI matrix |
| "expect declaration has no actual" | Check the actual declarations exist in all required source sets and match the expect signature exactly | Add/align the missing actual; check visibility and type parameters | Re-verify the expect surface design; reduce the surface if needed |
| iOS app crashes on a shared call | Check thread-safety of the shared state (new memory model); check Swift interop types | Synchronize/confine the state; fix the Swift bridging (nullability, callbacks) | Roll back the shared call; isolate the module; add a concurrency test |
| CocoaPods/Gradle sync mismatch | `pod install` after Gradle sync (or vice versa per the docs); check min-version alignment | Clean both (`pod deintegrate`, `./gradlew clean`); re-integrate | Switch integration method (SPM) with a migration plan |
| CommonTest fails only on iOS | Check for platform-specific behavior in shared code (e.g., file/date handling) | Add the iOS-specific fix in the actual or a platform source set | Abstract the behavior behind expect/actual; re-run both targets |

**Hard failure boundary:** After 3 failed recovery attempts, escalate to human. Do not loop.

---

## Error Decoder **(STANDARD)**

| Symptom | Root Cause | Fix | Lesson |
|----------|-----------|-----|--------|
| "expect declaration has no actual implementation" on iOS | An expect added to commonMain without the iosMain actual, or the actual doesn't match the expect signature exactly. | Add the iosMain actual matching the expect signature; verify visibility and type params; run `./gradlew :shared:compileKotlinIosSimulatorArm64`. | expect/actual is a contract the compiler enforces — but only if you write both halves. Design the surface small so both are cheap to maintain. |
| iOS framework export breaks after a Kotlin bump | The Kotlin/Native toolchain or export config is incompatible with the new version or the Xcode version. | Check the migration guide; regenerate the export; align Xcode and Kotlin versions; verify in CI. | The iOS export is the fragile seam of KMP. It earns a CI build on every change, not a release-time discovery. |
| Shared call crashes on iOS but works on Android | New-memory-model violation (mutable shared state across threads) or Swift interop type mismatch (nullability, callbacks). | Synchronize or confine the state; fix the Swift bridging; add a concurrency test in commonTest. | "Works on Android" proves nothing about the iOS target. Concurrency and interop are platform behaviors that must be tested on both. |
| CocoaPods "target has frameworks with conflicting names" | The podspec/framework name conflicts with an existing framework, or the pod install ran out of sync with Gradle. | Rename the framework; clean and re-integrate (`pod deintegrate` + `pod install` after `./gradlew syncFramework`). | The iOS integration is a build contract with ordering rules. Document the sync order and run it in CI. |
| Binary size jumped after adding a shared module | Kotlin/Native links the whole runtime; naive target config or unused code inflates the binary. | Trim targets; enable link options (dead-code elimination); audit libraries; measure per-target size deltas. | Sharing logic has a size tax. Measure the delta per module and keep it within budget — the tax is real. |
| Shared tests pass but the app misbehaves | Platform halves (expect/actual) behave differently in the real app than in tests. | Add platform tests for the actuals; integration-test the real flow on both platforms. | commonTest proves shared logic; platform tests prove the actuals. Both are release gates. |

---

## Cross-Skill Coordination **(STANDARD)**

### Upstream (What This Skill Needs)

| Upstream Skill | Artifact Needed | What You'll Use It For |
|---------------|----------------|----------------------|
| `mobile-developer` | Native-vs-cross-platform decision + offline-first guidance | Choosing the sharing strategy before KMP-specific work |
| `android-developer` | Kotlin/Compose patterns, Android integration | The Android half of the shared module (androidMain) |
| `backend-developer` | API contracts, data models | Designing the shared data layer (Ktor client, DTOs) |

### Downstream (What This Skill Produces)

| Downstream Skill | Deliverable | What They'll Do With It |
|-----------------|------------|------------------------|
| `mobile-developer` | Shared module + source-set map | Integrate with the broader mobile strategy (offline-first, performance, security) |
| `ios-developer` | Exported iOS framework + interop docs | Consume the shared framework from Swift with correct bridging |
| `android-developer` | Shared module consumed from Android | Integrate the shared logic into the Android app |
| `backend-developer` | Shared DTOs + client contracts | Keep the API contract aligned with the shared data layer |

**Skill Creation on Handoff (autonomous):**

| Situation | Trigger | Action |
|-----------|---------|--------|
| Downstream task needs a skill that does not exist in the library | No `name:` match + no >80% description-similar neighbor in `skills/` | Run Core Workflow Phase 6 — scaffold, fill 22 sections, validate, wire symmetric chain, then hand off |
| A generated skill must be packaged for cross-agent reuse | Skill must run on Claude Code, Copilot, Gemini CLI, Cursor | Route to `cross-agent-skills-packaging` for portability testing + packaging |
| Complex multi-step handoff between agent roles | Handoff involves state, unresolved questions, or 3+ skills | Route to `agent-handoff-protocol` for the structured handoff ledger |
| A skill must be created or recreated from scratch at 10/10 quality | "create/regenerate skill for X" request | Route to `dynamic-skill-creator` (full discovery + generation protocol) |

---

## Proactive Triggers **(STANDARD)**

- **Kotlin or Gradle upgrade available** → Surface the migration plan and iOS-export impact before anyone upgrades ad hoc. 🔴
- **Platform-specific code appears in commonMain** → Flag as iOS-build debt before it breaks. 🔴
- **A kotlinx library is unversioned or mismatched** → Flag the version catalog mismatch before it breaks a build. 🟡
- **iOS framework export not in CI** → Block: the iOS seam must be verified on every change. 🔴
- **Shared tests run on one target only** → Intervene: commonTest must run on both platforms. 🟠
- **Binary-size delta over budget** → Alert before a release ships with the regression. 🟡

---

## State Log **(QUICK)**

| Turn | Action | Decision | Risk Accepted | Mitigation |
|------|--------|----------|---------------|-----------|
| 1 | Anchored versions | Adopted Kotlin 2.x / Gradle 8.x matrix | kotlinx compat drift | Version catalog + `libs.versions.toml` pinning |
| 2 | Module design | Shared auth + data layer in a pilot module | iOS export risk | CI iOS build + interop smoke test |
| 3 | expect/actual surface | 4 expects: keychain, network-status, date, ids | Surface change ripples | Small, stable expects; documented contract |
| 4 | iOS integration | SPM framework export | CocoaPods team legacy | Migration plan + CI verification |
| 5 | Skill gap detected | Created `<new-skill>` via Phase 6 | New skill is v1.0 | Full validation + symmetric chain wiring |
| N | ... | ... | ... | ... |

**Anti-Drift Check:** Before each response, verify:
1. Did the last action match the plan?
2. Are we still within the version matrix and source-set design?
3. Has any new information (Kotlin release, iOS tooling, crash data) invalidated prior decisions?

---

## What Good Looks Like **(QUICK)**

A KMP deliverable reads like a platform design, not a code dump. It opens with the anchored version matrix `[VERIFIED]` — Kotlin, Gradle, kotlinx, Xcode — and the source-set map showing exactly what lives in commonMain vs platform. expect/actual surfaces are enumerated as contracts. The data layer uses Ktor + SQLDelight with commonTest coverage on both targets; the iOS framework exports, links, and passes a smoke Swift call in CI. The report ends with measured share %, binary-size delta, and velocity impact.

**Signs of Excellence:**
- Versions anchored; version catalog is the source of truth.
- commonMain is genuinely common; expect surfaces are small and stable.
- Both targets build and test in CI; iOS export is a build contract.
- Sharing value measured in share %, size delta, and hours saved.

**Signs of Dysfunction:**
- `java.*` imports in commonMain.
- Shared logic tested only from Android.
- iOS export discovered broken at release.
- A sharing decision made with no numbers.

---

## Deliberate Practice **(STANDARD)**

```mermaid
graph TD
    A[Anchor versions] --> B[Design source sets]
    B --> C[Implement shared logic]
    C --> D[Test on both targets]
    D --> E[Verify iOS export + interop]
    E --> F[Measure share/size/velocity]
    F --> G[Feed learning into version matrix]
    G --> A
```

| Level | Routine | Time | Success Metric |
|-------|---------|------|---------------|
| Novice | Build a shared module with one expect/actual; run tests on both targets | 4 hours | commonTest green on Android + iOS; no commonMain leakage |
| Intermediate | Add a Ktor + SQLDelight data layer with serialization; commonTest coverage | 6 hours | Data layer tested on both targets; size delta measured |
| Advanced | Configure iOS framework export (SPM) + Swift smoke call; fix an interop bug | 6 hours | Export links; smoke call passes; CI builds the iOS consumer |
| Expert | Design a multi-module KMP platform with measured share/size/velocity ROI | 1-2 days | Share % and size deltas documented; org standards set |

---

## Anti-Patterns **(STANDARD)**

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| ❌ **java.\* in commonMain** — platform-specific imports sneak into shared code; the iOS build breaks at the worst moment. | ✅ **Source-set discipline** — anything platform-specific goes to expect/actual or a platform module; CI compiles every source set. |
| ❌ **The monolithic expect surface** — dozens of convenience expects that ripple to both platforms every time one changes. | ✅ **Small, stable expects** — a few deliberate contracts; libraries (Ktor, SQLDelight) carry the rest. |
| ❌ **Freezing for thread safety** — relying on the old memory model's `freeze()`; code misbehaves under the new model. | ✅ **Explicit concurrency** — synchronize or confine mutable shared state; test concurrency in commonTest. |
| ❌ **Android-only verification** — "it compiles on Android" shipped as "it works." | ✅ **Both-target CI** — build + test all targets and the iOS consumer on every change. |
| ❌ **Solo Kotlin upgrade** — bumping Kotlin/Gradle without a migration plan; iOS export breaks the team. | ✅ **Planned upgrades** — migration guide, library compat, iOS-export CI check, rollback path. |
| ❌ **Sharing code that diverges** — forcing shared code where iOS/Android requirements differ, creating more cost than duplication. | ✅ **Bounded sharing** — share domains that change at a similar rate; measure; pilot before expanding. |

### 1. commonMain Leakage Breaks iOS ($15K/build outage)

A team adds a `java.text.SimpleDateFormat` import to commonMain "just for this one date format." The iOS build fails for the whole team for 2 days while the import is hunted down and abstracted. 6 engineers × 2 days × $150/hr: **$14,400** in lost velocity, ~**$15,000** with recovery. Fix: R3 — platform code in commonMain is a build break; CI compiles every source set; expect/actual for platform capabilities.

### 2. Android-Only Testing Ships an iOS Crash ($18K/incident)

Shared auth logic passes commonTest on Android but the iOS actual (Keychain access) has a threading bug under the new memory model. The iOS app crashes for 8% of users at login. Emergency hotfix, support surge, rating drop: **$18,000/incident.** Fix: R5/R6 — commonTest runs on both targets; the iOS actual gets a platform test; CI verifies the iOS consumer.

### 3. Solo Kotlin Upgrade Breaks iOS Export ($12K/build outage)

A `kotlin("multiplatform")` version bump without checking the migration guide breaks the iOS framework export. CI red for 3 days while the team backtracks. 5 engineers × 3 days × $150/hr: **$18,000** lost velocity, ~**$12,000** after partial recovery. Fix: R2 — upgrades are planned migrations with an iOS-export CI gate and rollback.

### 4. Binary-Size Tax Unbudgeted ($10K/year)

A shared module adds 8MB to the iOS binary because targets weren't trimmed and libraries weren't audited. Store and user complaints about size; the team spends a sprint reducing it. **$10,000/year** in engineering and review. Fix: measure size deltas per module (Best Practice 9); trim targets and libraries; keep the tax within budget.

### 5. Freezing Reliance Under the New Memory Model ($20K/incident)

Shared state "protected" with `freeze()` under the old model behaves differently after the migration — a background Flow mutates state concurrently and crashes intermittently in production. Two weeks of intermittent-crash debugging across teams: **$20,000/incident.** Fix: R4 — explicit synchronization/confined state; concurrency tests in commonTest; no reliance on freezing.

---

## Production Checklist **(STANDARD)**

- [ ] **CR1: Version matrix anchored and verified** — Verification: Kotlin/Gradle/kotlinx/Xcode versions documented `[VERIFIED]`; version catalog is the source of truth
- [ ] **CR2: Source-set map defined** — Verification: every piece of logic has a named home; no platform-specific code in commonMain (CI-enforced)
- [ ] **CR3: expect/actual surface small and stable** — Verification: expect inventory documented; both platform actuals exist and match signatures
- [ ] **CR4: Both targets compile** — Verification: `./gradlew :shared:compileKotlinAndroid` + iOS target compilation succeed on a clean checkout
- [ ] **CR5: commonTest passes on both targets** — Verification: shared test suite green on Android and iOS
- [ ] **CR6: iOS framework exports and links** — Verification: framework export builds; Swift smoke call passes; iOS consumer compiles in CI
- [ ] **CR7: Concurrency is thread-safe** — Verification: no reliance on freezing; mutable shared state synchronized/confined; concurrency tests pass
- [ ] **CR8: Data layer uses battle-tested libraries** — Verification: Ktor/kotlinx.serialization/SQLDelight (or equivalent) — no hand-rolled shared infrastructure
- [ ] **CR9: Binary-size delta within budget** — Verification: per-target size deltas measured and committed; the sharing tax is accounted for
- [ ] **CR10: CI builds and tests all targets** — Verification: CI matrix covers Android + iOS targets and the iOS consumer
- [ ] **CR11: Sharing value measured** — Verification: code-share %, size delta, and hours saved reported per module
- [ ] **CR12: iOS integration method documented** — Verification: CocoaPods/SPM choice + sync order documented; min versions aligned
- [ ] **CR13: Crash-free sessions ≥ 99% (both platforms)** — Verification: crash rate monitored per version; regressions gated
- [ ] **CR14: Handoff skill gaps resolved** — Verification: any required downstream skill missing from `skills/` was created via Phase 6 or the gap is recorded in the State Log

---

## Gotchas **(QUICK)**

| Gotcha | Cost | Fix |
|--------|------|-----|
| `java.*` in commonMain breaks the iOS build | $10K-$20K per build outage | Source-set discipline + CI compile of every source set |
| Android-only testing ships an iOS concurrency crash | $10K-$30K/incident | commonTest on both targets; platform tests for actuals; concurrency tests |
| Solo Kotlin upgrade breaks the iOS export | $10K-$20K per outage | Planned upgrades with an iOS-export CI gate and rollback |
| Unbudgeted binary-size tax from shared modules | $5K-$15K/year | Measure per-target size deltas; trim targets and libraries |
| CocoaPods/Gradle sync ordering mismatch | $5K-$10K per incident | Document the sync order; run it in CI; consider SPM |

---

## Verification **(STANDARD)**

| # | Complete when... | Verify |
|---|---|---|
| ☐ | Complete when the version matrix is anchored: Kotlin, Gradle, kotlinx, and Xcode versions stated `[VERIFIED]` | Verify `./gradlew --version` + Kotlin plugin version + version catalog match the documented matrix |
| ☐ | Complete when the source-set map is defined: every piece of logic has a named home; commonMain has no platform-specific code | Verify the source-set doc; CI compiles every source set (platform leakage fails the build) |
| ☐ | Complete when both targets compile and commonTest passes on both: Android + iOS builds green | Verify CI runs both targets; shared tests green on both platforms |
| ☐ | Complete when the iOS framework exports, links, and a Swift smoke call passes | Verify the export build + smoke call in CI; iOS consumer compiles |
| ☐ | Complete when concurrency is thread-safe under the new memory model: no freezing reliance; synchronized/confined shared state | Verify concurrency tests pass; code review confirms no freezing patterns |
| ☐ | Complete when the sharing value is measured: share %, size delta, and hours saved reported | Verify the measured report exists; size deltas committed |
| ☐ | Complete when handoff skill gaps are resolved: any downstream task requiring a missing skill was created via Phase 6 or logged | Verify `python3 scripts/validate_chains.py` reports 0 asymmetries for created skills; State Log has the gap entry |

---

## Verification Guardrails **(STANDARD)**

### Pre-Generation
- [ ] Confirm the installed Kotlin/Gradle/kotlinx versions and target structure are captured — never write unanchored code
- [ ] Confirm the iOS integration method and sync order are known before any change touching it
- [ ] Confirm what will be shared vs platform is decided before writing code

### Post-Generation
- [ ] Re-run both-target builds and shared tests; confirm no new failures
- [ ] Confirm the iOS export and a Swift smoke call still pass
- [ ] Confirm all cross-skill chain references are symmetric and handoff gaps are either created or logged

---

## References **(QUICK)**

- [Source-Set Design](../references/source-set-design.md) — Hierarchy template, commonMain discipline, expect/actual inventory
- [iOS Interop](../references/ios-interop.md) — Framework export, CocoaPods/SPM, Swift bridging
- [Shared Data Layer](../references/shared-data-layer.md) — Ktor, kotlinx.serialization, SQLDelight patterns
- [Coroutines in Shared Code](../references/coroutines-shared.md) — Flow, scopes, and concurrency in commonMain
- [Concurrency Under the New Memory Model](../references/concurrency-memory-model.md) — Thread-safety without freezing
- [Build & CI](../references/build-ci.md) — Gradle config, targets, CI matrix, size control
- [Testing Shared Logic](../references/testing-shared-logic.md) — commonTest setup and platform test strategy
- [Version Matrix Reference](../references/version-matrix.md) — Kotlin/Gradle/kotlinx compatibility and upgrade protocol
- [Compose Multiplatform](../references/compose-multiplatform.md) — Shared UI strategy and maturity guidance

---

> **Skill version:** 1.0.0 | **Token budget:** 4500 | **Generated:** 2026-08-29
