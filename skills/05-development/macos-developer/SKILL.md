---
name: macos-developer
description: Native macOS application development with SwiftUI, AppKit, Swift, Xcode, Catalyst, and Apple platform technologies. Use when building native macOS applications, designing macOS UI with SwiftUI/AppKit, implementing macOS-specific features (Menu Bar apps, Preferences windows, NSToolbar, NSTableView, drag-and-drop), configuring sandboxing and hardened runtime entitlements, notarizing apps for distribution, or building Universal Binaries for Apple Silicon + Intel. Handles macOS architecture patterns, Metal integration, XPC services, and macOS-specific performance optimization. Do NOT use for iOS development, cross-platform desktop with Electron/Tauri, or Windows/Linux native apps.
author: Sandeep Kumar Penchala
license: MIT
version: 1.0.0
updated: 2026-07-24
tags:
- macos
- swift
- swiftui
- appkit
- apple
- catalyst
- desktop
- native
token_budget: 4500
chain:
  consumes_from:
  - desktop-developer
  - desktop-architecture-patterns
  - ui-ux-designer
  - backend-developer
  - system-architect
  feeds_into:
  - qa-engineer
  - security-reviewer
  - performance-engineer
---
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

# macOS Developer — Native macOS Application Engineering

Build production-grade native macOS applications with deep expertise across SwiftUI, AppKit, Swift, and the full Apple platform stack. This is the internal playbook for Apple-platform engineering — every section contains concrete, actionable implementation patterns, not generic advice. Covers the full lifecycle: UI framework selection (SwiftUI vs AppKit vs Catalyst) with tradeoff matrices, sandboxing and hardened runtime entitlements, code signing and notarization, Universal Binary builds for Apple Silicon + Intel, Menu Bar app architecture, XPC service patterns, Metal GPU integration, accessibility compliance, and macOS-specific performance optimization.

## Route the Request

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("*.xcodeproj")` OR `file_exists("Package.swift")` OR `file_contains("*.swift", "@main\\|NSApplicationMain\\|@NSApplicationMain")` | This is your skill. Jump to **Core Workflow** — Phase 1. |
| A2 | `file_contains("*.entitlements", "com.apple.security")` OR `file_contains("*.plist", "com.apple.security.app-sandbox")` | Jump to **Decision Trees** — Sandboxing Strategy. |
| A3 | `file_contains("*.swift", "NSStatusBar\\|MenuBarExtra\\|NSMenu\\|statusItem")` | Jump to **Decision Trees** — Menu Bar App architecture. |
| A4 | `file_contains("*.swift", "MTLDevice\\|MTLBuffer\\|MTLRenderPipeline\\|Metal")` | Jump to **references/metal-on-macos.md** — Metal integration. |
| A5 | `file_contains("*.swift", "NSXPCConnection\\|XPCService\\|xpc_connection")` | Jump to **references/xpc-services-patterns.md** — XPC patterns. |
| A6 | `file_exists("*.xcarchive")` OR `file_contains("*.sh", "notarytool\\|xcrun notarytool\\|altool")` | Jump to **Decision Trees** — Distribution Channel. |
| A7 | `file_contains("*.swift", "NSAccessibility\\|accessibilityLabel\\|AXCustomContent")` | Jump to **references/macos-accessibility.md** — Accessibility implementation. |
| A8 | `file_contains("project.pbxproj", "ONLY_ACTIVE_ARCH")` OR `file_contains("*.xcconfig", "EXCLUDED_ARCHS")` | Jump to **references/universal-binary-builds.md** — Universal Binary configuration. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
|-- Build a new native macOS app from scratch -> Jump to "Core Workflow" - Phase 1 (Project Setup)
|-- Choose between SwiftUI and AppKit for my UI -> Go to "Decision Trees" - SwiftUI vs AppKit vs Catalyst
|-- Set up sandboxing and entitlements -> Jump to "Decision Trees" - Sandboxing Strategy
|-- Notarize my app for distribution outside the App Store -> Go to "references/app-notarization-guide.md"
|-- Build a Menu Bar / status bar app -> Jump to "references/macos-menu-bar-apps.md"
|-- Build Universal Binary for Apple Silicon + Intel -> Jump to "references/universal-binary-builds.md"
|-- Implement XPC services for privilege separation -> Jump to "references/xpc-services-patterns.md"
|-- Add Metal GPU compute or rendering -> Jump to "references/metal-on-macos.md"
|-- Ensure VoiceOver and accessibility compliance -> Jump to "references/macos-accessibility.md"
|-- Architect a document-based app -> Jump to "Decision Trees" - Document-Based vs Single-Window
|-- Need UI design help -> Invoke ui-ux-designer skill instead
|-- Need backend API for my macOS app -> Invoke backend-developer skill instead
|-- Need code review -> Invoke code-reviewer skill instead
|-- Need security audit -> Invoke security-reviewer skill instead
|-- Not sure? -> Describe the problem in plain language and I'll route you
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules are **negative constraints** — they define what you MUST NOT do, with mechanical triggers that detect violations before execution.

| # | Negative Constraint | Mechanical Trigger (detect before executing) | Violation Response |
|---|-------------------|---------------------------------------------|-------------------|
| **R1** | **NEVER ship without sandboxing — App Store rejection is guaranteed.** Every macOS app distributed through the App Store MUST have the `com.apple.security.app-sandbox` entitlement set to `true`. Direct-distribution apps through notarization still require the Hardened Runtime. | Trigger: `.entitlements` file is missing `com.apple.security.app-sandbox` OR `com.apple.security.hardened-runtime` is absent | STOP. Respond: "This app will be rejected from the App Store or blocked by Gatekeeper. Add `com.apple.security.app-sandbox = true` to your entitlements file for App Store distribution, or enable the Hardened Runtime capability in Xcode. See references/macos-sandboxing-entitlements.md." |
| **R2** | **REFUSE to write UI code without confirming the target macOS version.** SwiftUI APIs available in macOS 14 are not available in macOS 12. AppKit deprecations in macOS 14 can break entire view hierarchies. | Trigger: generating SwiftUI or AppKit code without `@available(macOS X)` annotations OR without explicit deployment target confirmation | STOP. Ask: "What's your minimum deployment target? (macOS 12 Monterey, macOS 13 Ventura, macOS 14 Sonoma, macOS 15 Sequoia). This determines which APIs are available." Then wrap all version-specific code in `@available(macOS X, *)` guards. |
| **R3** | **REFUSE to let NSView/NSWindow updates happen off the main thread.** AppKit is not thread-safe. Updating UI from a background queue causes heisenbugs: flickering, crashes in `CALayer`, and races that only reproduce under load. | Trigger: generated code calls `.layer?`, `.addSubview()`, `.frame =`, `.needsDisplay = true`, or `.setFrame()` inside `DispatchQueue.global().async`, `Task.detached`, or Combine `.receive(on: background)` | STOP. Wrap all UI mutations in `DispatchQueue.main.async { ... }` or use `@MainActor`. Add assertion: `assert(Thread.isMainThread, "UI update off main thread")` in debug builds. |
| **R4** | **REFUSE to hardcode file paths outside the sandbox container.** Sandboxed apps cannot access `~/Documents`, `/tmp`, `/usr/local`, or arbitrary paths. Every file access MUST go through Powerbox (`NSOpenPanel`/`NSSavePanel`) or use sandbox-compliant directories. | Trigger: generated code contains `FileManager.default.fileExists(atPath: "/Users/"` OR `URL(fileURLWithPath: "/")` OR paths to `~` with absolute expansion | STOP. Replace with: `FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask).first!` or `NSOpenPanel` for user-chosen files. Hardcoded absolute paths will crash in the sandbox. |
| **R5** | **DETECT and WARN about missing code signing identity in release builds.** Unsigned or ad-hoc signed apps are blocked by Gatekeeper and fail notarization. Every archive build MUST use a Developer ID Application certificate. | Trigger: `xcodebuild archive` command is generated without `CODE_SIGN_IDENTITY` or `DEVELOPMENT_TEAM` parameters in release configuration | WARN: Add `-codeSignIdentity "Developer ID Application: Your Team"` to the build command. Apps without valid code signing will not pass notarization or Gatekeeper checks. |


- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

### The Mental Model Shift
Competent macOS developers make apps that look right. Masters make apps that **feel native.** The shift: stop thinking about what the framework makes easy and start thinking about what the platform expects. A macOS app that uses standard controls, respects System Preferences (Appearance, Accent Color, Reduce Motion), and integrates with Spotlight, Services, and Quick Look is automatically trusted by users. An app that reinvents every widget — no matter how beautiful — feels foreign and hostile.

### Cognitive Biases That Kill macOS Apps
| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **iOS-first thinking** | Porting an iOS SwiftUI app to macOS without adapting navigation (TabView -> sidebar), window management, or keyboard shortcuts. The result is a giant iPhone app floating in a window — no menu bar integration, no multi-window support, no drag-and-drop. | Design for macOS first if macOS is a target. If porting from iOS, budget 40% extra for platform adaptation: `NavigationSplitView` instead of `TabView`, `NSMenu` + `commands` modifier, `NSDocument` for document-based apps. |
| **AppKit nostalgia** | Choosing AppKit "because SwiftUI isn't mature enough" without measuring: 80% of macOS UI can be built in SwiftUI today, with AppKit bridging for the remaining 20% (`NSTableView` with 100K rows, custom `NSToolbar` items). Writing the entire app in AppKit because 20% needs it costs 2x development time. | Use SwiftUI as the default. Escape to AppKit/`NSViewRepresentable`/`NSViewControllerRepresentable` only when you hit a documented limitation. Profile the decision — don't default to AppKit from muscle memory. |
| **Cross-platform lowest common denominator** | Choosing Catalyst or Electron so the app "runs everywhere" — then discovering Catalyst doesn't support menu bar apps, drag-and-drop behaves differently, and Electron uses 400MB RAM for a calculator. | If macOS is a primary platform, build natively. Catalyst is acceptable for simple iOS ports; Electron only for internal tools where RAM budget doesn't matter. Every abstraction layer costs platform fidelity. |

### What macOS Masters Know That Others Don't
- **The run loop is your performance budget.** AppKit processes events on the main run loop in `NSDefaultRunLoopMode`. If your code blocks the main thread for >16ms (one frame at 60fps), scrolling hitches, buttons feel laggy, and the spinning beachball appears. Profile with Instruments' Time Profiler, not `print(Date())`.
- **Code signing is a chain, not a checkbox.** The signature covers your binary, embedded frameworks, the `_CodeSignature` directory, and resource files. Modify any file after signing — even a `.plist` — and the signature breaks. Gatekeeper will reject the app. Always sign after archiving, never before.
- **Entitlements are deny-by-default in the sandbox.** If an entitlement isn't explicitly listed and set to `true`, the capability is denied. This includes file access, network access, USB, Bluetooth, camera, microphone, and printing. Every capability you need must be declared.
- **Every refactor must remove dead AppKit bridging code — not just reorganize it.** When you migrate from AppKit to SwiftUI, actively delete the old `NSView` subclasses, the `NSViewController` wrappers, and the now-unused delegate methods. A refactor's diff should be net-negative in lines. Dead bridging code adds compile time, binary size, and confusion.

### When to Break Your Own Rules
- **Skip sandboxing for command-line tools distributed via Homebrew.** CLI tools run outside the sandbox by definition. Sandboxing is for `.app` bundles that users launch from Finder.
- **Use force-unwrapping for `NSApplication.shared` and `NSApp`** — these are guaranteed to exist after `NSApplicationMain` runs. Pedantic nil-checking is noise.
- **Hardcode deployment target in `xcconfig` files, not in multiple `project.pbxproj` build settings.** A single source of truth for `MACOSX_DEPLOYMENT_TARGET` prevents drift between Debug and Release.

## Operating at Different Levels

The same macOS development task produces fundamentally different output depending on the practitioner's level. Invoke this skill with your target level to calibrate depth and scope.

| Level | macOS Developer Output Characteristics |
|---|---|
| **L1 — Apprentice** | Step-by-step SwiftUI view implementation with explanations. Uses standard controls, basic `@State`, follows HIG. "Here's the Settings view, here's how `@AppStorage` persists preferences." |
| **L2 — Practitioner** | Production-ready window with all states (loading, empty, error, multi-window), keyboard shortcuts, accessibility labels. Independent delivery to App Store or notarized distribution. |
| **L3 — Senior** | Architecture decisions: SwiftUI vs AppKit split, XPC boundary design, sandbox entitlements strategy, document architecture (NSDocument vs custom). Trade-off analysis with rationale. |
| **L4 — Staff** | Multi-app macOS ecosystem design: shared frameworks, XPC service architecture, build system for Universal Binaries across teams, CI/CD for notarization pipeline. "This is how all our Mac apps should handle updates, licensing, and crash reporting." |
| **L5 — Principal** | Novel macOS patterns adopted across the industry. Framework-level extensions to SwiftUI/AppKit. "Here's a new window management pattern for this class of desktop application." |

**Usage**: Say "as an L3 macOS developer, design the architecture for..." or "give me an L2 implementation of this document window" to calibrate. Default: **L2** (production-ready, independent execution).

## When to Use

- Building a new native macOS application from scratch with SwiftUI or AppKit
- Choosing between SwiftUI, AppKit, and Catalyst for your macOS UI layer — with concrete tradeoffs and decision matrices
- Designing sandbox entitlements and hardened runtime configuration for App Store or direct distribution
- Notarizing a macOS app for distribution outside the App Store via `notarytool` or the notarization pipeline
- Building Universal Binaries that run natively on both Apple Silicon (arm64) and Intel (x86_64)
- Implementing Menu Bar / status bar apps with `NSStatusBar` or SwiftUI `MenuBarExtra`
- Architecting XPC services for privilege separation, crash isolation, or inter-process communication
- Integrating Metal for GPU compute, custom rendering, or Core Image processing pipelines
- Ensuring macOS accessibility compliance: VoiceOver, Full Keyboard Access, Reduce Motion, Increase Contrast
- Designing document-based apps with `NSDocument`, autosave, versions, and the macOS document model
- Implementing drag-and-drop, Services menu integration, Quick Look previews, or Spotlight indexing
- Setting up Sparkle or in-app update mechanisms for direct-distribution apps

## Core Workflow

<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~15 min): Project Setup & Architecture
1. **Minimum deployment target**: Set `MACOSX_DEPLOYMENT_TARGET` in an `.xcconfig` file (single source of truth). Default to macOS 13 Ventura for new projects in 2026.
2. **Framework decision**: Run through the SwiftUI vs AppKit decision tree (below). Document the decision and its rationale in the project README.
3. **Project structure**: Feature-based, not layer-based. `Sources/Features/YourFeature/` contains views, models, ViewModels, and services together. Shared code in `Sources/Core/`.
4. **App entry point**: SwiftUI `@main App` with `WindowGroup` or `DocumentGroup`. AppKit: `NSApplicationDelegate` with explicit activation policy.
5. **Entitlements file**: Create `YourApp.entitlements` with `com.apple.security.app-sandbox = true` (App Store) or `com.apple.security.hardened-runtime = true` (direct). Add only the entitlements you actually use.

### Phase 2 (~30 min): UI Implementation
1. **SwiftUI path**: `NavigationSplitView` for sidebar apps, `WindowGroup` for multi-window, `Settings` scene for Preferences. Use `@Environment(\\.colorScheme)` and `@AppStorage` for system integration.
2. **AppKit path**: `NSWindowController` + `NSViewController` for each window. Use `NSStackView` over manual Auto Layout. `NSTableView` with cell reuse for data grids.
3. **Menu bar**: Every app gets standard menus: App Name (About, Preferences, Hide, Quit), File (New, Open, Save, Close), Edit (Undo, Cut, Copy, Paste), Window (Minimize, Zoom, Bring All to Front). SwiftUI: `commands` modifier. AppKit: `NSApplication.shared.mainMenu`.
4. **Keyboard shortcuts**: ⌘, for Preferences, ⌘W for Close Window, ⌘M to minimize, ⌘H to hide. Use `KeyboardShortcut` in SwiftUI, `NSMenuItem.keyEquivalent` in AppKit.

### Phase 3 (~20 min): Sandboxing & Security
1. **Map every capability to an entitlement**: File access, network (client + server), USB, Bluetooth, camera, microphone, printing, location — each is opt-in.
2. **Replace `Process()`/`NSTask` with `NSXPCConnection`**: XPC services are sandbox-compatible. Embedded XPC services live in `Contents/XPCServices/`.
3. **File access via Powerbox**: `NSOpenPanel` and `NSSavePanel` for user-chosen files. Security-scoped bookmarks (`NSURL.bookmarkData`) to persist access across launches.
4. **Validate third-party library entitlements**: Every linked framework that accesses hardware or files must declare its own entitlements or inherit from the host app.

### Phase 4 (~25 min): Code Signing & Notarization
1. **Signing order**: Frameworks first (deepest dependency up), then XPC services, then the main executable, then the app bundle.
2. **Verify signing**: `codesign -dvvv YourApp.app` — check Authority chain, TeamIdentifier, and that `runtime` flag is present.
3. **Notarize**: `xcrun notarytool submit YourApp.zip --apple-id "dev@example.com" --team-id TEAMID --password "@keychain:NOTARY_PASSWORD" --wait`
4. **Staple ticket**: `xcrun stapler staple YourApp.app` — embeds the notarization ticket so Gatekeeper can verify offline.
5. **Verify**: `spctl -a -v YourApp.app` reports `accepted`.

### Phase 5 (~20 min): Distribution Packaging
1. **App Store**: Archive → Validate → Upload via Xcode Organizer or `xcrun altool --upload-app`. Fill in App Store Connect metadata: description, screenshots (1280x800, 144 DPI minimum), privacy policy URL, and content ratings.
2. **Direct DMG**: Create DMG with `hdiutil create -format UDZO -srcfolder YourApp.app YourApp.dmg`. Sign the DMG with your Developer ID. Include a symlink to `/Applications` for drag-and-drop installation. Set a custom background image and icon layout with AppleScript or `create-dmg`.
3. **Sparkle updates**: Generate appcast XML, sign each update with EdDSA using `sign_update`, host at a secure URL. Configure `SUFeedURL` in `Info.plist`. Implement phased rollouts for staged production releases.
4. **Crash reporting**: Integrate a crash reporter (Crashlytics, Sentry, or custom `NSUncaughtExceptionHandler`). Symbolicate dSYMs automatically in CI. Mask personally identifiable information in crash logs before upload.
5. **CI/CD pipeline**: Automate the full build-sign-notarize-package pipeline. Use Fastlane `notarize` action or a custom shell script. Store signing certificates and notarization credentials in CI/CD secrets — never in the repository. Run `spctl` and `lipo` validation as pipeline gates.

### Phase 6 (~15 min): macOS Integration Polish
1. **Services menu**: Register your app as a service provider via `Info.plist` `NSServices` entries. Handle `NSPasteboard` data for text, images, and URLs.
2. **Quick Look**: Implement `QLPreviewingController` for in-app previews. Register a Quick Look generator for custom file types via a `.qlgenerator` bundle.
3. **Spotlight**: Index your app's documents with `CSSearchableIndex` or `NSMetadataQuery`. Provide a Core Spotlight importer for custom document types.
4. **Touch Bar / Magic Keyboard**: Support `NSTouchBar` for MacBook Pro users. Map critical actions to the Touch Bar with fallback keyboard shortcuts.
5. **Handoff & Universal Clipboard**: Use `NSUserActivity` to enable Handoff between Mac and iOS. Mark activities with `isEligibleForHandoff = true`.

## Decision Trees

### SwiftUI vs AppKit vs Catalyst — Framework Selection

```
START: Building a macOS app?
|
+-- Is it a Menu Bar / status bar app?
|   +-- YES -> SwiftUI `MenuBarExtra` (macOS 13+) or AppKit `NSStatusBar` (macOS 12 and earlier)
|   +-- NO -> Continue
|
+-- Do you need 60fps scrolling with 10,000+ rows in a data grid?
|   +-- YES -> AppKit `NSTableView` with cell reuse. SwiftUI `List` / `Table` will choke.
|   +-- NO -> Continue
|
+-- Are you porting an existing iPad app to macOS?
|   +-- YES -> Catalyst (Mac Catalyst). Share 90% of code. Restrict expectations.
|   +-- NO -> Continue
|
+-- Does your app need custom drawing, Core Animation layers, or Metal interop inside views?
|   +-- YES -> AppKit `NSView` with `CALayer` or `MTKView`. SwiftUI bridging available but adds complexity.
|   +-- NO -> Continue
|
+-- Do you need deep integration with macOS services (Spaces, Mission Control, Accessibility API, CGEvent)?
|   +-- YES -> AppKit. These APIs are C/Objective-C and require manual bridging.
|   +-- NO -> SwiftUI (default). Covers 80%+ of app UI with dramatically less code.
```

**Default**: SwiftUI for new apps. Escape to AppKit via `NSViewRepresentable` / `NSViewControllerRepresentable` for the 20% SwiftUI can't handle. Catalyst only for iPad-first apps that need a Mac presence. See **references/swiftui-appkit-selection-guide.md** for the full matrix.

### Sandboxing Strategy

```
START: Distribution channel?
|
+-- App Store?
|   +-- App Sandbox (com.apple.security.app-sandbox = true) REQUIRED
|   +-- Network: add com.apple.security.network.client/server entitlements
|   +-- File access: com.apple.security.files.user-selected.read-write + Powerbox
|   +-- USB/Bluetooth/Camera/Mic: each needs explicit entitlement
|
+-- Direct distribution (notarized DMG/ZIP)?
|   +-- Hardened Runtime (com.apple.security.hardened-runtime) REQUIRED
|   +-- App Sandbox is optional but recommended for security
|   +-- Additional entitlements depend on capabilities needed
|
+-- Both (App Store + direct)?
|   +-- Build two configurations: one with sandbox + App Store cert, one with hardened runtime + Developer ID
|   +-- Share 95% of entitlements between configs
```

See **references/macos-sandboxing-entitlements.md** for the complete entitlement catalog.

### Distribution Channel — App Store vs Direct Notarization

```
START: Revenue model and update cadence?
|
+-- Paid app (one-time purchase)?
|   +-- App Store: easier discovery, Apple handles payments (30% cut on first-year subscriptions, 15% thereafter)
|   +-- Direct: Paddle/Stripe integration, full revenue, but you handle payment infrastructure
|
+-- Subscription app with frequent updates?
|   +-- App Store: Apple handles subscription management, renewals, family sharing
|   +-- Direct: Sparkle for updates, more control over release timing, no review delays
|
+-- Free/open-source app?
|   +-- App Store: broadest reach, zero infrastructure cost
|   +-- Direct (Homebrew cask): developer audience, no review process
|
+-- App requires entitlements NOT available in sandbox?
|   +-- Direct distribution ONLY. App Store requires sandbox, which blocks certain system-level access
|
+-- Do you need control over update timing (bypass App Review)?
|   +-- Direct with Sparkle. App Store reviews take 24-48h typically.
```

See **references/app-notarization-guide.md** for the full notarization pipeline.

### Universal Binary vs Apple Silicon Only

```
START: What's your user base?
|
+-- Consumer app on App Store?
|   +-- Universal Binary (arm64 + x86_64). ~5-15% of App Store users still on Intel Macs in 2026.
|
+-- Internal enterprise tool where IT controls hardware?
|   +-- Apple Silicon only if all deployed Macs are M-series. Verify first. Smaller binary.
|
+-- Pro app targeting video/3D/development (high-end users)?
|   +-- Universal Binary. Pro users are on latest hardware AND older Intel Mac Pros. Don't alienate them.
|
+-- Binary size matter (app > 200MB)?
|   +-- Universal thins at install via App Thinning. Ship Universal, let App Store deliver arch-specific slices.
```

See **references/universal-binary-builds.md** for build settings and CI configuration.

### Document-Based vs Single-Window Architecture

```
START: What does your app create/edit?
|
+-- Files the user thinks of as "documents" (text, images, video, spreadsheets)?
|   +-- `NSDocument` / `DocumentGroup` (SwiftUI). Free: autosave, vers

ions, window restoration, duplicate, and the title bar proxy icon for free. Use it.
|   +-- Utilities/tools (settings window, single-window data browser)? -> Single-window. No document lifecycle needed.
|
+-- Does the user open multiple files simultaneously?
|   +-- YES -> Document-based. Each file opens in its own window. Standard macOS expectation.
|   +-- NO -> Single-window with tabs (NSTabView / TabView). Single-file tools like image compressors, code formatters.
|
+-- Is undo/redo per-file important?
|   +-- YES -> NSDocument. Built-in NSUndoManager per document, dirty-state tracking, "Save" prompt on close.
|   +-- NO -> Single-window with manual state management.
```

### XPC Service vs Bundled Helper Tool

```
START: Need privilege separation or crash isolation?
|
+-- Component needs to run with different privileges than the main app?
|   +-- YES -> XPC Service (within app bundle). e.g., a privileged helper that performs system-level operations.
|   +-- NO -> Continue.
|
+-- Component is crash-prone (parsing untrusted data, third-party plugin)?
|   +-- YES -> XPC Service. Crash in the XPC process doesn't bring down the main app. Restart the service automatically.
|   +-- NO -> Continue.
|
+-- Component needs to stay alive when the app is not running?
|   +-- YES -> Launch Agent/Daemon (standalone executable, not embedded in app bundle).
|   +-- NO -> Continue.
|
+-- Just separating concerns for code organization?
|   +-- Use Swift Package Manager modules instead. XPC adds IPC overhead, code signing complexity, and launch latency.
```

See **references/xpc-services-patterns.md** for implementation patterns.


## Error Recovery

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Cross-Skill Coordination

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `ui-ux-designer` | Design system, interaction patterns, component specs, typography scale, color tokens, spacing grid | Before implementing any UI; ensures macOS HIG compliance and native feel |
| `system-architect` | Service boundaries, data flow architecture, technology stack decisions, IPC strategy | Before choosing XPC boundaries, persistence layer, or networking stack |
| `backend-developer` | REST/GraphQL API endpoints, authentication tokens, WebSocket push channels | Before implementing networking layer in the macOS client |
| `desktop-developer` | Cross-platform desktop patterns, Electron/Tauri alternatives assessment, platform selection rationale | Before committing to native macOS vs cross-platform approach |
| `desktop-architecture-patterns` | MVVM/MVC/MVP pattern guidance, state management patterns for desktop apps, offline-first strategies | Before designing the app architecture layer |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `qa-engineer` | Build artifacts, test signing identities, XCTest/XCUITest targets, accessibility audit paths, test plan | QA can't begin integration testing without signed builds |
| `security-reviewer` | Entitlements files, sandbox configuration, XPC boundary definitions, code signing setup, hardened runtime flags | Security review is incomplete without understanding the sandbox and privilege model |
| `performance-engineer` | Instruments trace templates, frame-rate benchmarks, memory pressure baselines, launch time measurements | Performance work is guesswork without baseline metrics from the app |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| Entitlement change (adding network, USB, Bluetooth access) | Security Engineer | Sandbox expansion changes the threat model — each new entitlement is a new attack surface |
| Minimum deployment target bump (dropping macOS 12 support) | QA Engineer, Product Manager | Drops support for ~5-15% of Intel Macs — coordinate with product roadmap |
| New XPC service added to app bundle | Security Engineer, DevOps | Each XPC service needs its own code signing identity, sandbox profile, and notarization |
| Switching from AppKit to SwiftUI for a major component | UI/UX Designer, QA | UI behavior changes — keyboard navigation, accessibility tree, and appearance differ between frameworks |
| Notarization failure | DevOps, Release Manager | Blocks distribution — requires immediate triage of code signing, entitlement, or binary issues |

### Escalation Path

```
Blocked by code signing / cert issues? -> DevOps Engineer -> Security Engineer -> Apple Developer Support
App Store rejection (sandbox/entitlement violation)? -> Security Engineer -> Compliance Officer
SwiftUI API limitation blocking feature? -> Staff macOS Developer -> Principal (framework contribution path)
Metal/GPU performance bottleneck? -> Performance Engineer -> GPU Architecture Specialist
Accessibility compliance issue? -> Accessibility Auditor -> Legal Advisor (ADA compliance)
```

## Proactive Triggers

| Trigger | Response |
|---------|----------|
| "App rejected from App Store: 'ITMS-90296: App sandbox not enabled'" | Enable sandbox: set `com.apple.security.app-sandbox = true` in entitlements. Remove use of `posix_spawn`, `NSTask` (use `NSXPCConnection` instead), and direct file access outside container. Use Powerbox (`NSOpenPanel`/`NSSavePanel`) for user-chosen files. Re-archive and resubmit. |
| "Notarization fails with 'The binary is not signed with a Developer ID certificate'" | Verify signing identity: `codesign -dvvv /path/to/YourApp.app`. Look for `Authority=Developer ID Application: Team Name (TEAMID)`. If missing, import the Developer ID certificate into your keychain, set `CODE_SIGN_IDENTITY = "Developer ID Application"` in build settings, and re-archive. Ad-hoc signing (dash `-`) will always fail notarization. |
| "Menu bar app icon doesn't appear / is invisible in Dark Mode" | The status bar icon (`NSImage`) must have `isTemplate = true` so AppKit inverts it for Dark Mode and the menu bar highlight. If you're using a color icon, set `isTemplate = false` and provide both light and dark variants. For SwiftUI `MenuBarExtra`, use `Image(systemName:)` (template by default) or provide PDF-based images with the template rendering mode. |
| "Sparkle update check fails: 'The update is improperly signed'" | Sparkle uses EdDSA (Ed25519) signatures. Generate keys: `./bin/generate_keys`. The `SUPublicEDKey` in `Info.plist` must match the private key used to sign the appcast. The appcast XML must include the `<sparkle:edSignature>` element. Re-signing the update with `sign_update` tool after every build. |
| "App launches to blank window on Apple Silicon when built as x86_64 only" | The app is running under Rosetta 2 translation. While it works, performance degrades 20-40%. Build as Universal Binary (`arm64 x86_64` in `ARCHS`). Do NOT set `EXCLUDED_ARCHS[sdk=macosx*] = arm64` in Release configuration — this strips Apple Silicon from release builds. |
| "SwiftUI List shows empty rows or stale data with Core Data @FetchRequest" | `@FetchRequest` is tied to the view's identity. If the view struct is recreated, the fetch is re-executed. Use `@SectionedFetchRequest` for grouped data. Set `nsPredicate` and `sortDescriptors` as constants (not computed properties) — changing them recreates the fetch request and resets scroll position. |
| "Drag-and-drop works in debug but fails in Release / App Store build" | Release builds have `com.apple.security.app-sandbox` enabled. File promises and drop destinations that rely on direct file access fail. Use `NSItemProvider` with sandbox-compatible UTI types. Register for `NSFilenamesPboardType` only if `com.apple.security.files.user-selected.read-write` is in entitlements. |


## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "macos-developer",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }
   ```
3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.

### State Log Schema

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |

### Anti-Drift Check
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like

> Every window handles all states (loading, empty, error, content). The app integrates with macOS system services: the menu bar has standard items (About, Preferences, Hide, Quit), keyboard shortcuts follow HIG (⌘, for Preferences, ⌘W for Close), and every interactive element is navigable via Full Keyboard Access. The app builds as a Universal Binary, is sandboxed or hardened-runtime enabled, passes notarization, and launches in under 400ms cold. VoiceOver reads every label, every role, and every value change. The app respects Reduce Motion, Increase Contrast, and Dark Mode — automatically. Window restoration works: close and reopen the app, and every window returns to its previous position, size, and scroll offset.

### Production-Grade macOS App Indicators

A production-grade macOS app can be identified by these specific, testable characteristics:

| Dimension | Minimum Bar | Gold Standard |
|---|---|---|
| **Launch** | Cold launch < 400ms | Cold launch < 200ms, warm launch < 50ms |
| **Scrolling** | 60fps in `NSTableView`/`List` with 1,000 items | 60fps with 100,000 items using cell reuse and prefetching |
| **Memory** | < 100MB idle, < 300MB under load | < 50MB idle, < 150MB under load, no unbounded growth after 24h |
| **Notarization** | Passes `spctl -a -v` | Passes notarization in < 5 min, CI pipeline is fully automated |
| **Accessibility** | All controls have labels and roles | Full VoiceOver workflow: every task completable without sight |
| **Dark Mode** | No hardcoded colors break readability | Asset catalog with dark variants, custom views respect system appearance |
| **Multi-window** | Multiple windows open and close | Window restoration, tab support, full-screen split-view compatible |
| **Updates** | Users can download new version | Sparkle delta updates, phased rollout, signed appcast, silent background updates |

### Before You Ship — The macOS Litmus Test
1. Open your app. Press ⌘F5 to activate VoiceOver. Close your eyes. Can you complete the app's primary task?
2. Enable Full Keyboard Access (System Settings > Accessibility > Keyboard). Can you reach every control via Tab? Can you activate every button with Space? Can you close every dialog with Escape?
3. Switch to Dark Mode. Does every custom color, icon, and view render correctly? Are contrast ratios still 4.5:1 minimum?
4. Enable Reduce Motion. Do animations gracefully disable? Do you still get visual feedback for state changes?
5. Quit the app. Reopen it. Are your windows where you left them? Is your scroll position preserved? Is your unsaved work still there?
6. Archive, notarize, and staple. Install the app on a machine that has never run your development build. Does Gatekeeper allow it to open?

**Quality Gate Checklist:**
- [ ] App launches and passes Gatekeeper (no "unidentified developer" warning)
- [ ] App responds to Apple Events: `openDocument`, `reopen`, `print` — test via AppleScript
- [ ] Window restoration works: close the app, reopen — windows restore to previous positions and sizes
- [ ] Standard menu items present: App Name > About/Preferences/Services/Hide/Quit, all with ⌘ shortcuts
- [ ] Keyboard navigation: every interactive element reachable via Tab (Full Keyboard Access enabled)
- [ ] Undo/Redo works (⌘Z/⇧⌘Z) in every text field and document — `NSUndoManager` wired correctly
- [ ] Dark Mode: all colors, icons, and custom views adapt correctly — run `defaults write NSGlobalDomain AppleInterfaceStyle Dark`
- [ ] Accessibility: VoiceOver reads every control's label, role, and value — verified with Accessibility Inspector
- [ ] Universal Binary: `lipo -archs YourApp.app/Contents/MacOS/YourApp` shows `arm64 x86_64`
- [ ] Notarization: `spctl -a -v /path/to/YourApp.app` reports `accepted` with `source=Notarized Developer ID`
- [ ] No main-thread blocking: Instruments Time Profiler shows no hitch >16ms during scrolling and window resize
- [ ] Crash-free sessions: 99.9%+ in production crash reporting within 7 days of release

## Deliberate Practice

<!-- DEEP: 10+min — how to improve, not just what to do -->

### The macOS Developer Improvement Loop
1. **Profile with Instruments** — Run Time Profiler during a 30-second interaction session. Find every main-thread hitch >16ms. Run Allocations to find retain cycles and abandoned memory. Run Leaks to find memory that can't be reclaimed.
2. **Test on oldest supported hardware** — An M1 Max masks performance problems. Test scrolling, window resize, and animations on an Intel Mac or M1 base model. If it's smooth there, it's smooth everywhere. Test on the minimum supported macOS version — new APIs may be missing.
3. **Run the Accessibility Inspector** — Audit every window. Can VoiceOver navigate to every control? Are labels descriptive? Are value changes announced? Is the focus order logical? Test with Full Keyboard Access enabled.
4. **Notarize a build end-to-end** — From archive to `xcrun notarytool submit` to `stapler staple`. If this pipeline takes more than 5 minutes, optimize it. Every minute in the pipeline is a minute developers wait for feedback.
5. **Read App Store Review Guidelines** — Review the macOS-specific sections every WWDC cycle. Apple adds new rules, clarifies existing ones, and occasionally changes enforcement patterns. One guideline change can block your next release.

### Practice Routines
| Skill Level | Practice | Frequency | Expected Result |
|-------------|----------|-----------|-----------------|
| Novice → Competent | Build the same UI in SwiftUI and AppKit; compare line count, accessibility tree, keyboard handling, Dark Mode behavior | Monthly | Can articulate SwiftUI/AppKit tradeoffs from direct experience, not blog posts |
| Competent → Expert | Build a sandboxed app that uses XPC, does custom Metal rendering, and ships via notarization — all from `xcodebuild` CLI (no Xcode GUI) | Quarterly | Can set up a complete macOS CI/CD pipeline without the Xcode IDE |
| Expert → Master | Contribute an accessibility fix or Metal performance improvement to an open-source macOS app. Submit a SwiftUI feedback (FB) with a reproducible sample project. Reverse-engineer an AppKit control to understand its run-loop integration. | Quarterly | Understands the framework internals well enough to work around bugs and file actionable radars |
| Master → Principal | Prototype a new macOS interaction pattern (novel window management, custom input method, new accessibility paradigm). Write a proposal for Swift Evolution or Apple's Feedback Assistant that ships in a macOS release. | Annually | Shapes the platform, not just builds on it |

### The One Thing
**Build a macOS app that ships on the App Store and via direct notarization — same codebase, different build configs — every 6 months.** You'll learn code signing end-to-end, how entitlements differ between channels, how App Review interprets sandboxing rules differently from Gatekeeper, and why continuous integration is non-negotiable for macOS distribution. App Store Connect is a product requirement, not a deployment detail.

### The macOS-Specific Learning Path
Unlike iOS where UIKit/SwiftUI are the only game in town, macOS development requires understanding two complete UI paradigms that coexist: the modern, declarative SwiftUI and the 20-year-old, battle-hardened AppKit. A senior macOS developer can:
- Choose the right framework per component, not per app — SwiftUI for the settings window, AppKit for the high-performance timeline
- Bridge between them at the `NSView`/`NSViewController` level without leaking memory or breaking responder chain
- Debug run-loop issues that manifest as "hangs" in Instruments but look like normal code in the debugger
- Understand that `NSApplication.shared` is a singleton with 30+ years of accumulated state — and respect that state instead of fighting it

## Gotchas

- **Code signing with `--deep` flag.** `codesign --deep` recursively signs every binary in the bundle with the same identity, overwriting framework signatures from their original developers. This breaks notarization because the notary service expects frameworks to be signed by their original developers, then re-signed with your identity via the `--preserve-metadata` flag. Developers cargo-cult `--deep` from Stack Overflow and waste 4-8 hours debugging notarization failures that show no obvious error. **Total cost: $500-$2,000 in lost engineering time per notarization debugging session.** Fix: Sign in order — frameworks first, then the main binary. Use `codesign --force --options runtime --timestamp --sign "Developer ID Application: Team" --preserve-metadata=identifier,entitlements,flags YourApp.app`.

- **Sparkle update framework shipped without EdDSA signing.** The app downloads updates over HTTP or unsigned HTTPS without verifying the EdDSA signature in the appcast. An attacker who compromises the update server or performs a man-in-the-middle attack can push malicious binaries to every user. The app update mechanism — designed for security — becomes the primary attack vector because one line of configuration was skipped. **Total cost: $100,000-$2,000,000 in incident response, PR damage control, forced password resets for all users, and potential legal liability from compromised user machines.** Fix: Generate EdDSA keys with Sparkle's `generate_keys` tool. Add `SUPublicEDKey` to `Info.plist`. Sign every update binary with `sign_update`. Verify the `<sparkle:edSignature>` element is present in the appcast XML before publishing.

- **Hardened Runtime without `com.apple.security.cs.disable-library-validation` blocks all plug-ins.** The Hardened Runtime, by default, prevents loading unsigned or third-party libraries via `dlopen`. Every audio unit, Photoshop plugin, Finder Sync extension, or scriptable plugin silently fails to load. Users report "the plugin doesn't work" and you can't reproduce it on your development machine (which doesn't have the hardened runtime). The bug report count climbs while you search for a code bug that doesn't exist. **Total cost: $10,000-$50,000 in wasted debugging time and customer support load over the app's lifecycle.** Fix: If your app loads third-party plugins, add `com.apple.security.cs.disable-library-validation = true` but pair it with `com.apple.security.cs.disable-executable-page-protection = false` (never allow writable+executable memory unless absolutely required for JIT). Document which library paths are validated.

- **`@Environment(\.colorScheme)` in SwiftUI doesn't update for custom AppKit windows.** When you create an `NSWindow` programmatically and host a SwiftUI view via `NSHostingView`, the `colorScheme` environment value is set at view creation time and never updates when the system appearance changes. Your app stays in Light Mode when the user switches to Dark Mode until the window is closed and reopened. **Total cost: $5,000-$15,000 in negative App Store reviews and support tickets for an app that "doesn't support Dark Mode" despite 40+ hours invested in Dark Mode color assets.** Fix: Observe `NSApplication.shared.effectiveAppearance` via KVO or `NSApp.effectiveAppearance` notifications. Force-refresh the hosting view: `hostingView.rootView = ContentView().environment(\.colorScheme, newColorScheme)`. Or use `NSWindow` subclass with `effectiveAppearance` observation.

- **Sandboxed app using `NSTask` / `Process` to launch helper tools — works in Xcode, crashes in App Store build.** Xcode launches apps with a development provisioning profile that includes `com.apple.security.get-task-allow` and bypasses sandbox restrictions. The same code using `Process()` to launch an external executable crashes with `POSIX error 1: Operation not permitted` in the sandbox. Developers ship the crash because "it worked on my machine." **Total cost: $3,000-$8,000 in App Store rejection cycles (2-3 submissions each taking 24-48h review), emergency patch releases, and user refunds for a non-functional feature.** Fix: Replace all `Process()` / `NSTask` calls with `NSXPCConnection` to an XPC Service bundled in the app. XPC services are explicitly allowed in the sandbox. Use `SMJobBless` for privileged helpers that need root.

- **`NSView.draw(_:)` override without calling `super.draw(_:)` — rendering breaks on newer macOS versions.** Developers override `draw(_:)` to do custom Core Graphics drawing but omit the `super.draw(_:)` call. The view draws correctly on the development macOS version, but Apple changes the superclass implementation in a macOS update to set up new layer properties or backing store configurations. Suddenly, the custom view renders as a black rectangle on macOS 15 after working perfectly on macOS 14. **Total cost: $8,000-$25,000 in emergency debugging, expedited App Store review requests, and user churn from a critical rendering bug in a point release.** Fix: Always call `super.draw(dirtyRect)` at the start of every `draw(_:)` override. If you intentionally skip it (e.g., for full-frame Metal rendering), document why and test on the latest macOS beta within 7 days of WWDC.

- **Missing `NSApp.setActivationPolicy(.regular)` for non-document-based apps.** Apps without a `CFBundleDocumentTypes` entry or `NSDocument` subclass default to `NSApplication.ActivationPolicy.prohibited` (accessory mode). The app's dock icon never appears, the app doesn't appear in the Command-Tab switcher, and menu bar items don't respond to clicks. Developers spend hours debugging NSApplication delegate methods and menu setup when the fix is one line in `applicationWillFinishLaunching`. **Total cost: $2,000-$5,000 in wasted debugging sessions and Stack Overflow bounties.** Fix: In `AppDelegate.applicationWillFinishLaunching(_:)`, call `NSApp.setActivationPolicy(.regular)` for standard apps, `.accessory` for menu bar-only apps, or `.prohibited` for daemons. This must be set before `NSApp.activate(ignoringOtherApps: true)`.

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---|
| "I'll add sandboxing after the core features work — it's just a plist flag." | Sandboxing is architecture, not configuration. Every file access path must go through Powerbox or sandbox-compliant directories. Retrofitting sandboxing onto a codebase that uses `Process()`, hardcoded absolute paths, and direct `NSFileManager` access is a rewrite, not a flag flip. Cost: 2-4 weeks of rework vs 2 days if architected from day one. |
| "SwiftUI isn't ready for production macOS apps — I'll write everything in AppKit." | SwiftUI on macOS 14+ covers 80%+ of typical app UI with 60% less code than AppKit equivalents. Writing a settings window in AppKit takes 200+ lines of NSViewController, NSTableView delegate/datasource, and Auto Layout. SwiftUI does it in 40 lines with `Form` + `@AppStorage`. The 20% that needs AppKit bridges cleanly via `NSViewRepresentable`. Don't pay the AppKit tax on the 80%. |
| "I don't need to test on Intel — everyone has Apple Silicon now." | As of 2026, ~5-15% of active Macs are still Intel, concentrated in enterprise fleets and high-end Mac Pro users — exactly the customers who pay for professional software. Intel Macs have different GPU families, different memory pressure characteristics, and Rosetta 2 introduces subtle timing differences. One Intel-only crash in your crash reporter is a 1-star review from a paying customer. |
| "Accessibility is nice-to-have — we'll add VoiceOver labels after the 1.0 launch." | macOS includes accessibility by default on every shipping Mac. VoiceOver turns on with ⌘F5. If your app is silent to VoiceOver on launch day, accessibility users can't use it. Adding labels post-launch is 3x the effort of adding them during development because you've forgotten what each custom control does. Accessibility is not a feature — it's the baseline. |
| "The app doesn't need notarization — my users can right-click > Open to bypass Gatekeeper." | Right-click bypass works for technically literate users. Every other user sees "App can't be opened because it is from an unidentified developer" and either deletes your app or emails support. Notarization takes 2-5 minutes per build in CI. Skipping it saves zero development time and costs you users. |

## Verification

- [ ] Run `xcodebuild -project YourApp.xcodeproj -scheme YourApp -destination 'platform=macOS' test` — all XCTest and XCUITest pass
- [ ] Run `swiftlint lint --strict` or `swift-format lint --strict --recursive .` — zero warnings
- [ ] Build Release archive: `xcodebuild archive -scheme YourApp -archivePath build/YourApp.xcarchive`
- [ ] Verify Universal Binary: `lipo -archs build/YourApp.xcarchive/Products/Applications/YourApp.app/Contents/MacOS/YourApp` outputs `arm64 x86_64`
- [ ] Verify code signing: `codesign -dvvv build/YourApp.xcarchive/Products/Applications/YourApp.app` shows valid Developer ID certificate
- [ ] Submit for notarization: `xcrun notarytool submit build/YourApp.xcarchive --apple-id "dev@example.com" --team-id TEAMID --password "@keychain:NOTARY_PASSWORD" --wait`
- [ ] Staple notarization ticket: `xcrun stapler staple build/YourApp.xcarchive/Products/Applications/YourApp.app`
- [ ] Verify Gatekeeper: `spctl -a -v build/YourApp.xcarchive/Products/Applications/YourApp.app` reports `accepted`
- [ ] Run Accessibility Inspector on every window: all controls have `accessibilityLabel`, `accessibilityRole`, keyboard focus reaches every element
- [ ] Test with Reduce Motion enabled: all animations respect `NSWorkspace.shared.accessibilityDisplayShouldReduceMotion`
- [ ] Test with Dark Mode: all custom colors, images, and views render correctly
- [ ] Cold-launch test: `defaults write com.yourcompany.yourapp NSQuitAlwaysKeepsWindows -bool false` then launch — under 400ms to first window

## References

Detailed reference material loaded on demand:

- **SwiftUI vs AppKit Selection Guide**: See [swiftui-appkit-selection-guide.md](references/swiftui-appkit-selection-guide.md)
- **Sandboxing & Entitlements**: See [macos-sandboxing-entitlements.md](references/macos-sandboxing-entitlements.md)
- **App Notarization Guide**: See [app-notarization-guide.md](references/app-notarization-guide.md)
- **Universal Binary Builds**: See [universal-binary-builds.md](references/universal-binary-builds.md)
- **Menu Bar Apps**: See [macos-menu-bar-apps.md](references/macos-menu-bar-apps.md)
- **XPC Services Patterns**: See [xpc-services-patterns.md](references/xpc-services-patterns.md)
- **Metal on macOS**: See [metal-on-macos.md](references/metal-on-macos.md)
- **macOS Accessibility**: See [macos-accessibility.md](references/macos-accessibility.md)
