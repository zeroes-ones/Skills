---
name: desktop-developer
description: Cross-platform desktop application development with Electron, Tauri, .NET MAUI, Qt, WPF, and native desktop frameworks. Use when building desktop applications for Windows/macOS/Linux, choosing desktop frameworks, implementing system tray/menu bar apps, designing auto-update pipelines, packaging desktop installers, or integrating with OS-level APIs. Handles desktop architecture patterns, IPC mechanisms, native module integration, window management, and cross-platform distribution strategies. Do NOT use for mobile development, web applications, or CLI tools.
author: Sandeep Kumar Penchala
license: MIT
portability: spec-level
type: development
status: stable
version: 1.0.0
updated: 2026-07-24
tags: [desktop, electron, tauri, wpf, qt, cross-platform, native]
token_budget: 4500
chain:
  consumes_from:
    - frontend-developer
    - backend-developer
    - system-architect
    - security-reviewer
  feeds_into:
    - qa-engineer
    - performance-engineer
    - devops-engineer
---
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

# Desktop App Developer — Cross-Platform Desktop Application Engineering

## Route the Request

<!-- QUICK: 30s -- auto-route first, then intent-route -->

### Auto-Route (No User Input Required)
Evaluate these file-system conditions in order. First match wins — jump immediately.

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("electron-builder.yml\|electron-builder.json")` OR `file_contains("package.json", "\"electron\"")` | This is your skill. Jump to **Decision Trees** — Electron vs Tauri comparison. |
| A2 | `file_exists("tauri.conf.json")` OR `file_contains("Cargo.toml", "tauri")` | This is your skill. Jump to **references/tauri-security-model.md** for Tauri-specific security patterns. |
| A3 | `file_exists("*.csproj")` AND `file_contains("*.csproj", "Microsoft.NET.Sdk\|WinExe\|Maui")` | This is your skill. Jump to **Decision Trees** — .NET MAUI vs WPF. |
| A4 | `file_contains("CMakeLists.txt", "Qt\|find_package.*Qt")` OR `file_contains("*.pro", "QT\s*\+=")` | This is your skill. Jump to **Core Workflow** — Phase 3 (native desktop development). |
| A5 | `file_contains("*.xaml", "Window\|Application")` AND `file_exists("*.csproj")` | This is your skill. Jump to **Decision Trees** — WPF architecture patterns. |
| A6 | `file_contains("*", "contextBridge\|ipcMain\|ipcRenderer")` OR `file_contains("*.ts", "preload")` | Jump to **references/desktop-ipc-patterns.md** — IPC design patterns. |
| A7 | `file_contains("*", "autoUpdater\|electron-updater\|nugget\|sparkle")` OR `file_contains("*", "app-update.yml\|latest.yml")` | Jump to **references/auto-update-strategies.md** — auto-update implementation. |
| A8 | `file_exists("*.nuspec\|*.wixproj\|*.dmg\|setup.iss")` OR `file_contains("package.json", "\"nsis\"\|\"dmg\"\|\"appx\"")` | Jump to **references/desktop-installer-packaging.md** — installer configuration. |

### Intent Route (Ask the User)
If no auto-route matched, use this intent tree:

```
What are you trying to do?
├── Build a new desktop app → Start at "Decision Trees" — framework selection
├── Add system tray / menu bar app → Jump to "references/desktop-window-management.md" — tray section
├── Design IPC between renderer and native code → Jump to "references/desktop-ipc-patterns.md"
├── Implement auto-update pipeline → Jump to "references/auto-update-strategies.md"
├── Package installer for distribution → Jump to "references/desktop-installer-packaging.md"
├── Integrate native C++/Rust/Swift module → Jump to "references/native-module-integration.md"
├── Manage multi-window application → Jump to "references/desktop-window-management.md"
├── Set up cross-platform CI/CD builds → Go to "Core Workflow" — Phase 5
├── Write cross-platform tests → Jump to "references/cross-platform-testing.md"
├── Add OS-level integrations (notifications, file associations, protocols) → Go to "references/electron-architecture-patterns.md" — OS Integration section
├── Need security review of IPC surface → Invoke security-reviewer skill
├── Need UI/UX design patterns → Invoke ui-ux-designer skill
└── Don't know which framework to choose? → Share target platforms, performance requirements, team skills, and app type
```

Do not read the entire skill. Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that detect desktop development mistakes before they are made. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|---------------------|
| R1 | REFUSE executing native code or shell commands with unsanitized input from the renderer process | Trigger: IPC handler receives user-supplied input (file paths, URLs, shell arguments) and passes it directly to `exec()`, `spawn()`, `shell.openPath()`, or `NSWorkspace.openURL()` without an allowlist or validation | STOP. Respond: "This IPC handler passes unsanitized renderer input to a shell or system API: [specific call]. The renderer is attacker-controlled territory — any XSS becomes arbitrary code execution on the user's machine. Validate ALL IPC inputs against a strict allowlist. Never construct shell commands from renderer-provided strings." |
| R2 | REFUSE shipping unsigned binaries on macOS and Windows | Trigger: Build configuration has no `certificateFile`, `certificatePassword`, Apple notarization is skipped, or Windows signing is disabled to "speed up the build" | STOP. Respond: "Unsigned desktop binaries trigger macOS Gatekeeper ('cannot be verified') and Windows SmartScreen red warnings. 60%+ of users abandon at this point. Configure code signing: Apple Developer ID certificate + notarization with notarytool, Windows Authenticode with EV certificate. Every release build must be signed — unsigned builds are not release candidates." |
| R3 | DETECT synchronous IPC calls on the main thread for I/O operations | Trigger: `ipcMain.on()` handler performs `fs.readFileSync()`, synchronous database queries, or network requests without delegating; or `ipcRenderer.sendSync()` used for data retrieval | STOP. Respond: "Synchronous I/O on the main process blocks ALL renderer windows and the event loop. A 200ms operation means your entire app is unresponsive for 200ms. Use `ipcMain.handle()` with async operations. `ipcRenderer.sendSync()` is only for trivial synchronous property access (<1ms)." |
| R4 | REFUSE bundling credentials, API keys, or signing secrets in the application package | Trigger: `.env` files with production secrets in build artifacts, API keys in source that ship in `.asar`/binary, OAuth client secrets embedded in the app instead of PKCE flow | STOP. Respond: "Desktop apps are distributed binaries — everything in the package is extractable within seconds. Use OAuth 2.0 PKCE (Proof Key for Code Exchange) — no client secret required. API keys must come from a per-user authenticated backend. Environment variables in `.env` are build-time only, never shipped." |
| R5 | DETECT untested auto-update path with no rollback strategy | Trigger: Auto-update configured but no tests for: download failure mid-stream, signature verification failure, disk-full during extraction, app launch after partial update, or rollback mechanism | STOP. Respond: "Auto-update without failure testing and rollback is a bricking mechanism. If the new version crashes on launch, users are locked out with no recovery path except manual reinstall. Implement: atomic swap with backup, signature verification before swap, health-check on launch with auto-rollback if the new version crashes within 30s, and CI tests for every failure mode." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset

<!-- DEEP: 10+min — how masters think, not just what they do -->

### The Mental Model Shift
Competent desktop developers make windows appear and respond to clicks. Masters understand that **the desktop is a hostile distributed system where every OS version, display configuration, accessibility setting, and power state is a unique runtime environment.** Unlike web servers in controlled containers, your desktop app runs on machines with antivirus software hooking syscalls, GPU drivers from 2018, 125% display scaling on a 4K monitor, and 87% disk utilization. Your app must survive all of this.

### Cognitive Biases That Kill Desktop Apps
| Bias | How It Manifests | Antidote |
|-------|------------------|----------|
| **Browser parity delusion** | Assuming Electron's Chromium renders identically to Chrome. Chromium version lag, GPU blacklisting, and OS compositor differences mean your UI breaks on specific hardware configurations | Test on real hardware: integrated GPU (Intel UHD), discrete GPU (NVIDIA/AMD), HiDPI displays, and VMs without GPU acceleration. Chromium's `--disable-gpu` flag is how ~8% of users experience your app. |
| **File-system optimism** | Assuming `fs.writeFile` always succeeds. Disk full, permission denied, antivirus lock, network drive timeout, and cloud-sync conflicts are all normal desktop conditions | Every file operation must handle: `ENOSPC` (disk full), `EACCES` (permissions), `EBUSY` (locked), `ENOENT` (parent deleted). Retry with exponential backoff for transient locks. |
| **Single-window thinking** | Designing for one window and discovering users open 15. Window management is the #1 desktop bug source: z-order fights, memory leaks from zombie windows, focus stealing | Design for multi-window from commit 1. Every BrowserWindow needs: unique ID, listener cleanup on `closed`, no assumption of focus, `blur`/`focus` handlers that don't affect sibling windows. |

### What Desktop Masters Know That Others Don't
- **The GPU is not guaranteed.** Chromium's GPU process crashes on specific driver/OS combinations, falling back to software rendering. CSS animations become 5 FPS. Test with `--disable-gpu` — this is how ~8% of users experience your app.
- **The file system lies.** `fs.watch` doesn't work on network drives (SMB/NFS). `fs.stat` on an actively-written file returns intermediate sizes. Windows locks open files; macOS doesn't. Writing to `%APPDATA%` during OneDrive sync causes permission errors. Desktop file I/O is a distributed systems problem.
- **Power states kill assumptions.** Your app must survive: sleep (suspend-to-RAM), hibernate (suspend-to-disk), lid close, battery critical, and fast user switching. Network connections drop on sleep. Timers drift. The renderer process may resume before the GPU process — handle `canvas.getContext('webgl')` returning `null` for 2 seconds after wake.
- **The renderer is not a browser tab.** Users don't "close a tab" — they close your entire app. Renderer-only state (Redux store, React state) is gone. Critical data must hit disk BEFORE `beforeunload` (which gives you ~1 second). Use `app.on('before-quit')` on the main process for last-chance persistence.
- **Installation path is an input, not a constant.** `C:\Program Files\`, `/Applications/`, `/opt/`, and `~/.local/share/` have different permission models, AV scanning behaviors, and path-length limits. Windows has a 260-char `MAX_PATH` unless the app manifest opts in to long paths.

### When to Break Your Own Rules
- **Skip code signing for internal enterprise apps distributed via MDM.** If deployed via Intune, Jamf, or Workspace ONE to managed devices, enterprise certificates and MDM policies bypass Gatekeeper/SmartScreen.
- **Use Electron for internal tools with <50 users.** The 180MB download and 400MB RAM are acceptable when the alternative is 2 weeks of build-system setup for Qt/C++. Fast iteration beats binary size for internal tools.
- **Ignore HiDPI for kiosk/embedded apps on fixed hardware.** If your app runs on a specific 1920×1080 industrial touchscreen forever, skip `@2x` assets. But document this assumption — the hardware will be replaced someday.

## Operating at Different Levels

Desktop spans web technologies (Electron), system languages (Tauri/Rust, Qt/C++), and managed runtimes (.NET MAUI/WPF). Level manifests in how deeply you understand the OS integration layer.

| Level | Desktop Output Characteristics |
|---|---|
| **L1 — Apprentice** | Builds single-window Electron apps from tutorials. Uses `nodeIntegration: true` "because it's easier." Doesn't understand why antivirus flags their app. |
| **L2 — Practitioner** | Delivers cross-platform apps with proper IPC, code signing, and auto-update. Ships installers via CI/CD. Handles basic OS integration (file associations, notifications). |
| **L3 — Senior** | Makes framework decisions with explicit trade-off rationale. Designs IPC surface with security boundaries. Handles multi-window, power-state, and GPU-fallback scenarios. Owns CI/CD across macOS/Windows/Linux. |
| **L4 — Staff** | Defines desktop architecture patterns for the org: IPC standards, native module guidelines, cross-platform abstraction layers, crash-reporting pipelines. Builds internal tooling that makes desktop dev as productive as web. |
| **L5 — Principal** | Creates desktop frameworks or methodologies adopted across the industry. Contributes to Electron, Tauri, or platform-native frameworks. Defines new paradigms for desktop-web convergence. |

**Usage**: Say "as an L3 desktop developer, design the multi-window architecture for..." Default: **L2** (production-ready, proper security boundaries).

## When to Use

<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Building cross-platform desktop applications with Electron, Tauri, .NET MAUI, Qt, or WPF
- Choosing between desktop frameworks based on performance, team skills, and target platforms
- Implementing system tray / menu bar applications with background processes
- Designing IPC (Inter-Process Communication) between renderer and native system code
- Configuring auto-update pipelines with differential updates and rollback
- Packaging desktop installers: NSIS, WiX, DMG, AppImage, MSIX, Flatpak
- Integrating native C++/Rust/Swift modules with the desktop shell
- Managing multi-window applications with z-order, focus, and lifecycle
- Implementing OS-level integrations: notifications, file associations, custom URL protocols, global shortcuts
- Setting up cross-platform CI/CD builds with code signing and notarization
- Debugging GPU-related rendering issues, power-state bugs, or antivirus false positives
- Migrating from Electron to Tauri for reduced bundle size and memory footprint
- Implementing accessibility (screen readers, keyboard navigation) in desktop webviews

## Core Workflow
<!-- COMPRESSED: Full 188 lines extracted to references/core-workflow.md -->

<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~20 min): Framework Selection & Architecture
1. **Run the framework decision tree** (see Decision Trees). Document: target platforms, performance budget (RAM, CPU, disk), team skills (JS/Rust/C#/C++), and app type (document editor, chat, system utility, game launcher).
2. **Project scaffold**: Framework CLI — `npm init electron-app@latest`, `npm create tauri-app@latest`, `dotnet new maui`, or CMake-based Qt project.
...
> 📎 **Full content (188 lines):** [references/core-workflow.md](references/core-workflow.md)

## Decision Trees

<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->

### Electron vs Tauri vs .NET MAUI vs Qt vs WPF

```
                    ┌──────────────────────────────────────────┐
                    │ START: Which desktop framework?          │
                    └──────────────────┬───────────────────────┘
                                       │
          ┌────────────────────────────▼────────────────────────────┐
          │ Target platforms?                                        │
          └──┬──────────┬──────────┬──────────┬──────────┬──────────┘
             │          │          │          │          │
       Win+Mac+Linux  Windows  Win+Mac+Linux Windows  Win+Mac+Linux
       + mobile                 + mobile               + embedded
             │          │          │          │          │
             ▼          ▼          ▼          ▼          ▼
    ┌─────────────┐ ┌─────────┐ ┌──────────┐ ┌──────┐ ┌──────────┐
    │ Can team    │ │ .NET    │ │ .NET     │ │ WPF  │ │ Qt/C++   │
    │ write Rust? │ │ MAUI or │ │ MAUI     │ │ or   │ │ or       │
    └──┬──────┬───┘ │ WPF     │ │ (limited │ │ WinUI│ │ Qt/Python│
       │YES   │NO   └─────────┘ │ Linux)   │ │      │ └──────────┘
       ▼      ▼                 └──────────┘ └──────┘
  ┌────────┐ ┌──────────────────────────────┐
  │ Tauri  │ │ Bundle/RAM critical?         │
  │ ~5MB   │ │ (sub-50MB, <100MB RAM)?      │
  │ binary │ └──┬───────────────────────┬───┘
  │ + Rust │    │ YES                   │ NO
  │ backend│    ▼                       ▼
  └────────┘ ┌──────────────────┐ ┌──────────────┐
              │ Tauri (if team   │ │ Electron     │
              │ can learn Rust)  │ │ ~180MB       │
              │ OR Electron with │ │ ~200-400MB   │
              │ strict security  │ │ Full web     │
              └──────────────────┘ └──────────────┘
```

**When Tauri:** Binary size <10MB required. Memory budget <100MB. Security-sensitive (Rust's memory safety). Team has or can learn Rust. Target: Win/Mac/Linux + mobile in future.  
**When Electron:** Team is JS/TS only. Complex rendering (WebGL, rich text). Rapid development with web UI libraries. User base has modern hardware. Time-to-market is primary constraint.  
**When .NET MAUI:** Cross-platform Win+Mac (+mobile). Team is C#/.NET. Need native controls (not web-based). Enterprise ecosystem (Azure AD).  
**When WPF:** Windows-only. Team is C#/XAML. Deep Windows integration (registry, COM, Win32). Legacy enterprise app modernization.  
**When Qt:** Cross-platform native C++ performance. Embedded/kiosk/IoT. Complex custom rendering (CAD, video editing, scientific visualization). Team has C++ expertise.

### Native vs Web-Based Renderer

```
                    ┌──────────────────────────────────────┐
                    │ START: Native UI or WebView?         │
                    └──────────────────┬───────────────────┘
                                       │
          ┌────────────────────────────▼────────────────────────────┐
          │ Need: (a) pixel-perfect OS look, (b) <50ms input        │
          │ latency, or (c) native screen reader support?           │
          └──┬──────────────────────────────────────────────────┬───┘
             │ YES to any                                        │ NO
             ▼                                                   ▼
    ┌──────────────────┐                           ┌──────────────────────┐
    │ Native renderer  │                           │ Team has existing    │
    │ (.NET MAUI, WPF, │                           │ React/Vue web app?   │
    │ Qt, AppKit,      │                           └──┬───────────────┬───┘
    │ WinUI)           │                              │ YES           │ NO
    └──────────────────┘                              ▼               ▼
                                           ┌──────────────┐ ┌──────────────┐
                                           │ WebView      │ │ Native if     │
                                           │ (Electron,   │ │ performance   │
                                           │ Tauri, MAUI  │ │ matters       │
                                           │ Hybrid)      │ └──────────────┘
                                           └──────────────┘
```

**When Native UI:** Accessibility critical (gov, healthcare). Sub-frame input latency (music, video editing, drawing). Pixel-perfect OS integration required.  
**When WebView:** Team is web developers. Rapid iteration with hot reload. Information-dense but not latency-sensitive UI (dashboards, chat, docs). Code sharing with web app.

### Auto-Update Strategies

```
                    ┌──────────────────────────────────────┐
                    │ START: Auto-update strategy?         │
                    └──────────────────┬───────────────────┘
                                       │
          ┌────────────────────────────▼────────────────────────────┐
          │ Framework?                                                │
          └──┬──────────────┬──────────────┬──────────────┬──────────┘
             │              │              │              │
        Electron         Tauri         .NET MAUI/WPF   Qt/Native
             │              │              │              │
             ▼              ▼              ▼              ▼
   ┌─────────────────┐ ┌──────────────┐ ┌──────────┐ ┌──────────┐
   │ electron-updater │ │ Tauri updater│ │ ClickOnce│ │ Sparkle  │
   │ + S3/GitHub/     │ │ + custom     │ │ or MSIX  │ │ (macOS)  │
   │ static server    │ │ endpoint     │ │ App      │ │ + WinSpark│
   └──┬───────────────┘ └──┬───────────┘ │ Installer│ │ (Windows)│
      │                    │             └──┬───────┘ └──┬───────┘
      ▼                    ▼                ▼             ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ Common requirements: differential updates, rollback on      │
   │ failure, staged rollouts (5%→25%→100%), HTTPS manifest,     │
   │ signature verification before applying update               │
   └─────────────────────────────────────────────────────────────┘
```

**When electron-updater:** Electron app. S3 as update server (cheap, reliable, CDN). Supports NSIS, DMG, AppImage. Differential updates via blockmap.  
**When Sparkle:** Non-Electron native macOS app. Used by 90%+ of Mac apps. Appcasts over RSS with DSA/EdDSA signatures.  
**When ClickOnce:** .NET/WPF Windows app in enterprise. Integrated with AD/Group Policy.  
**When Tauri updater:** Tauri app. Static JSON endpoint. Rust-native verification and extraction.

### IPC Mechanism Selection

```
                    ┌──────────────────────────────────────┐
                    │ START: IPC pattern?                  │
                    └──────────────────┬───────────────────┘
                                       │
          ┌────────────────────────────▼────────────────────────────┐
          │ Communication pattern?                                    │
          └──┬──────────────────┬──────────────────┬─────────────────┘
             │                  │                  │
    Request-Response     Fire-and-Forget      Streaming/Bulk
             │                  │                  │
             ▼                  ▼                  ▼
   ┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
   │ ipcMain.handle() │ │ ipcMain.on() │ │ MessagePort /    │
   │ + invoke()       │ │ / webContents│ │ SharedArrayBuffer│
   │ Promise-based    │ │ .send()      │ │ / stream pipe    │
   │                  │ │ Event-based  │ │                  │
   │ File reads,      │ │ Notifications│ │ Large files,     │
   │ config, DB,      │ │ status, logs │ │ real-time data   │
   │ settings         │ │              │ │                  │
   └──────────────────┘ └──────────────┘ └──────────────────┘
   
   Tauri equivalent:
   ┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
   │ #[tauri::command]│ │ emit()/      │ │ File system APIs │
   │ fn → Result<T,E> │ │ listen()     │ │ (direct paths)   │
   └──────────────────┘ └──────────────┘ └──────────────────┘
```

**When request-response:** Operations returning data/confirmation. Use `ipcMain.handle` + `ipcRenderer.invoke` (Electron) or `#[tauri::command]` (Tauri). Always validate input, return typed output.  
**When fire-and-forget:** Events, status updates, log entries. Use `webContents.send` (main→renderer) or `ipcRenderer.send`. Risk: queue overflow if receiver is slow.  
**When streaming:** File transfers >10MB, real-time feeds, WebRTC. Use MessagePort for zero-copy or SharedArrayBuffer for shared memory. Avoid serializing large buffers through IPC — doubles memory.

### Installer Packaging

```
                    ┌──────────────────────────────────────┐
                    │ START: How to package?               │
                    └──────────────────┬───────────────────┘
                                       │
          ┌────────────────────────────▼────────────────────────────┐
          │ Target platform?                                          │
          └──┬──────────────────────┬──────────────────┬─────────────┘
             │                      │                  │
          Windows                macOS              Linux
             │                      │                  │
             ▼                      ▼                  ▼
   ┌──────────────────┐  ┌──────────────────┐ ┌──────────────────┐
   │ Channel?         │  │ Channel?         │  │ Distribution?    │
   └──┬────┬────┬─────┘  └──┬────┬─────────┘  └──┬────┬──────────┘
      │    │    │           │    │               │    │
   Direct Store Ent.    Direct Store Ent.    Deb/RPM  Snap/Flatpak
      │    │    │           │    │               │    │
      ▼    ▼    ▼           ▼    ▼               ▼    ▼
   NSIS  MSIX MSI/Int.   DMG   MAS/MDM      pkg mgr  AppImage
```

**When NSIS:** Direct Windows distribution. Widest compatibility (Win7+). Customizable UI. Supports install directory, shortcuts, file associations, uninstaller.  
**When DMG:** Direct macOS distribution. Must be notarized. Include `/Applications` shortcut. Background image, license.  
**When AppImage:** Linux portable. Single file, no install needed. Works on any distro.  
**When MSIX:** Windows Store. Sandboxed, clean install/uninstall. Automatic Store updates. Limited filesystem access.

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
| `frontend-developer` | Component architecture, state management patterns, design tokens, UI routing conventions | Before building renderer UI — ensures consistency with web app patterns |
| `backend-developer` | API contracts, authentication flows, data models, caching strategies | Before integrating backend APIs in the desktop client |
| `system-architect` | Process topology decisions, framework evaluations, cross-cutting concerns | Before finalizing framework choice and IPC architecture |
| `security-reviewer` | Preload audit, CSP review, IPC surface analysis, signing configuration review | Before shipping — IPC is the security boundary |
| `ui-ux-designer` | Window chrome patterns, responsive layouts, platform-specific UI conventions | Before implementing window management and layout |

| Downstream Skill | What You Provide | Impact of Delay |
|---|---|---|
| `devops-engineer` | Build matrix (3 platforms), signing config, notarization steps, installer targets, update server endpoint | DevOps can't build CI/CD pipeline without understanding the full build matrix and signing requirements |
| `qa-engineer` | E2E test scenarios, platform test matrix, GPU configuration variants, power-state test cases, auto-update test plan | QA can't design comprehensive desktop tests without knowing platform-specific failure modes |
| `performance-engineer` | Cold/warm startup metrics, memory baseline, GPU rendering paths, IPC latency budget | Performance can't set budgets without understanding desktop-specific bottlenecks |

### Communication Triggers

| Trigger | Notify | Why |
|---|---|---|
| Framework change (Electron→Tauri or vice versa) | All developers, DevOps, QA | Complete build pipeline rewrite, new signing requirements, different test tooling |
| New IPC channel added | Security Reviewer | Every IPC channel expands the attack surface |
| Code signing certificate expiring in <30 days | DevOps, Release Manager | Unsigned builds block all distribution channels |
| New OS version released (macOS 15, Windows 12) | QA, All developers | API deprecations, new notarization requirements, permission model changes |
| Auto-update pipeline change | DevOps, QA | Broken updates brick existing installs |

### Escalation Path

```
IPC security vulnerability discovered? → Security Reviewer → System Architect
Code signing certificate expired? → DevOps Engineer → Release Manager
Auto-update bricking users? → DevOps Engineer → All (incident response)
Framework choice contested? → System Architect → CTO Advisor
App rejected from Mac App Store? → Release Manager → Legal Advisor
```

## Proactive Triggers

<!-- DEEP: 10+min — patterns that demand immediate intervention -->

| Trigger | Action | Why |
|---------|--------|-----|
| `nodeIntegration: true` or `contextIsolation: false` found in any Electron config | BLOCK: "This configuration exposes full Node.js APIs to every web page loaded in the renderer. Any XSS vulnerability becomes arbitrary code execution with the user's full OS privileges. Replace with contextBridge + preload. nodeIntegration must be false, contextIsolation must be true, sandbox must be true." | The most dangerous configuration in desktop development. A single XSS in a third-party dependency loaded in the renderer gives an attacker `require('child_process').exec('rm -rf /')`. This configuration is responsible for >80% of critical Electron CVEs. |
| `ipcRenderer.sendSync()` used for data retrieval | FLAG: "sendSync blocks the renderer process until the main process responds. If the main process is busy (disk I/O, GPU operation), ALL renderer windows freeze. Replace with ipcMain.handle + ipcRenderer.invoke for async request-response. sendSync is only acceptable for trivial property access returning in <1ms." | Synchronous IPC is the #1 cause of "the app feels sluggish" complaints. A single sendSync call during a disk write freezes the entire UI for the duration of the I/O operation — typically 10-200ms, enough for users to perceive stutter. |
| Team building a Tauri app without a capabilities file (v2) | ALERT: "Tauri v2 uses capability-based permissions. Without explicit capabilities, commands that access the file system, network, or system APIs will fail at runtime. Define exactly which plugins and commands each window can invoke in capabilities/default.json. Follow least-privilege: a settings window does not need file-system access." | Tauri's permission model is what makes it secure. Running without capabilities means either nothing works (commands fail silently) or everything is permitted (no security boundary). Both outcomes are unacceptable in production. |
| Auto-update configured but never tested end-to-end with a signed build | BLOCK: "Auto-update has different code paths for signed vs unsigned, dev vs production, and different platforms. An auto-update pipeline that passes in dev but fails in production (wrong manifest URL, signature mismatch, missing platform entry in latest.yml) will silently fail — users never receive updates and you never know. Test the full pipeline: build a signed artifact, upload to a staging update server, install on a clean VM, verify the update is detected and applied." | Untested auto-update is the #1 cause of "version fragmentation hell." Users on v1.0.0 report bugs you fixed in v1.0.3 because they never received the update. Your support team wastes hours debugging already-fixed issues. Test the full pipeline before your first public release. |
| WPF ViewModel updating UI-bound properties from a background thread | FLAG: "WPF data binding marshals PropertyChanged events to the UI thread, but only if the property change was raised on the UI thread. If a background Task sets a bound property, the UI update silently fails — the data changes in memory but the screen shows stale values. Always use Application.Current.Dispatcher.Invoke or Dispatcher.InvokeAsync when updating ViewModel properties from background threads." | Silent data-binding failures are the hardest WPF bugs to detect. The data is correct in memory, the ViewModel shows the right value, but the user sees stale information. These bugs survive code review because the code looks correct — the threading violation is invisible. |
| Desktop app being built without any offline capability | WARN: "Desktop apps encounter network interruptions that web apps don't: laptop lid close, WiFi dead zones, VPN disconnects, hotel captive portals. If your app crashes or shows a white screen without internet, users perceive it as broken. At minimum: cache the last-known-good state, show a 'You're offline' banner with the cached data, and queue mutations for replay on reconnect." | Desktop users have a different relationship with connectivity than web users. A web user hitting a 500 page refreshes. A desktop user whose app shows a white screen uninstalls. Offline resilience is not a feature — it's a baseline expectation for software that lives on the user's machine. |
| Crash reporter configured but not capturing native crashes (C++ panics, Rust panics, segfaults) | ALERT: "JavaScript crash reporters (Sentry JS SDK, window.onerror) only capture renderer-process JS exceptions. Native crashes — Rust unwraps, C++ segfaults, GPU process crashes — produce no JavaScript stack trace and are silently lost. Configure crashReporter.start() in Electron's main process or Sentry Native SDK for Tauri/WPF. Without native crash reporting, your crash rate dashboard shows 0.01% when the real rate is 3%." | Native crashes are the most common type in desktop apps (GPU driver bugs, filesystem permission errors, antivirus hook conflicts) but the least reported. Teams celebrate "99.9% crash-free" metrics while users experience daily native crashes that were never captured. |

## What Good Looks Like

> The app launches on a clean Windows VM without SmartScreen warnings, checks for updates, and shows the UI in under 2 seconds. Every IPC channel is documented with input validation and error responses. The preload script is the only file importing ipcRenderer. The installer runs silently in CI/CD and produces a signed, notarized artifact.

### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | system-architect | Framework evaluation, process topology, IPC architecture decisions |
| **Before** | ui-ux-designer | Window chrome design, responsive layout specs, platform-specific interaction patterns |
| **This** | desktop-developer | Cross-platform app: processes, IPC, OS integration, auto-update, installers, CI/CD |
| **After** | code-reviewer | Security audit of preload+IPC, GPU rendering review, platform compatibility check |
| **After** | qa-engineer | E2E tests on all platforms, auto-update tests, power-state tests, GPU-fallback tests |

Common chains:
- **New desktop product**: system-architect → desktop-developer → code-reviewer → qa-engineer
- **Web-to-desktop port**: frontend-developer → desktop-developer → security-reviewer → devops-engineer
- **Electron-to-Tauri migration**: desktop-developer (assessment) → backend-developer (Rust API rewrite) → desktop-developer (integration) → performance-engineer

## Deliberate Practice

<!-- DEEP: 10+min — how to improve, not just what you do -->

### The Desktop Improvement Loop
1. **Build the same app on 3 frameworks** — Electron, Tauri, and either WPF or Qt. Compare: startup time, bundle size, RAM at idle, RAM under load, lines of code, security surface.
2. **Simulate every failure mode** — Disk full during save, GPU crash during animation, sleep during file write, network drop during update download. Your app should degrade gracefully in every scenario.
3. **Measure from the user's perspective** — Time from double-click to interactive UI. Time from "Check for Updates" click to "Restart to Update" button. Installer download size. RAM usage after 8 hours of use.

### Practice Routines
| Skill Level | Practice | Frequency | Expected Result |
|-------------|----------|-----------|-----------------|
| Novice → Competent | Build a system tray app (clipboard manager, snippet tool) with Electron + auto-update + NSIS installer. Ship it to 5 friends on different OSes. Fix every bug they report. | Monthly | Can independently ship a production-quality desktop app with proper IPC, signing, and updates |
| Competent → Expert | Port an Electron app to Tauri. Measure and document: bundle size reduction, memory reduction, security surface reduction, developer experience differences. | Quarterly | Can make evidence-based framework decisions and lead migrations |
| Expert → Master | Build a desktop app that integrates a native C++/Rust library via N-API/FFI. Implement: async off-main-thread execution, graceful degradation if the library fails to load, cross-platform compilation in CI. | Quarterly | Can extend any desktop framework with native code without compromising stability |

### The One Thing
**Ship a desktop app with auto-update, code signing, and crash reporting to 10 real users every quarter.** Nothing exposes gaps like real users on real hardware. Their antivirus will flag your unsigned build. Their HiDPI display will break your layout. Their corporate proxy will block your update server. You cannot simulate these — you must experience them.

## Gotchas

> **NEVER enable `nodeIntegration: true` in production.** This is the single most dangerous Electron misconfiguration — it grants any XSS in your renderer full OS shell access. Audit: `grep -rn 'nodeIntegration.*true'` must return zero results in production configs.

| # | Gotcha | Cost | Fix |
|---|--------|------|-----|
| 1 | **`nodeIntegration: true` in production Electron builds** — Enabling Node.js in the renderer means any XSS vulnerability in your web UI (from a compromised npm dependency, a malicious ad in an embedded webview, or a crafted user input rendered as HTML) gives the attacker access to `require('child_process')`, `require('fs')`, and every Node.js API. This transforms a web vulnerability into full remote code execution with the user's OS privileges. | **$100,000-$500,000** in incident response, CVE disclosure, forced updates, reputational damage, and potential regulatory fines (GDPR/CCPA) if user data is exfiltrated. | Always configure `nodeIntegration: false`, `contextIsolation: true`, `sandbox: true`. Expose only needed APIs via `contextBridge.exposeInMainWorld()` with input validation on every method. Audit with `grep -r 'nodeIntegration.*true'` in CI. |
| 2 | **Shipping unsigned Windows binaries** — Windows SmartScreen displays "Windows protected your PC" with a red banner and a tiny "More info" link. Analytics show 60-70% of non-technical users abandon at this screen. Even after bypass, your app is flagged as "unrecognized" in Task Manager, and antivirus engines assign a higher suspicion score. Reputation is per-certificate — your unsigned reputation doesn't transfer. | **$50,000-$200,000** in lost users, support tickets, and delayed enterprise deals that require signed binaries. | Acquire an EV code signing certificate (~$300-400/year). Sign in CI/CD. Build reputation gradually — new certificates still trigger SmartScreen for ~1-2 weeks until they accumulate enough installs. |
| 3 | **Auto-update silently failing because the manifest is unreachable** — The update server URL is behind a CDN that blocks specific regions, or the corporate proxy strips custom headers, or the DNS resolver fails on certain ISPs, or the TLS certificate doesn't include the intermediate chain on Windows. The app logs "Update check failed: ECONNREFUSED" to a file nobody reads. Users remain on vulnerable versions indefinitely. | **$30,000-$100,000** in support tickets for already-fixed bugs, security incidents from unpatched vulnerabilities, and engineering time debugging reports from outdated versions. | Implement update health telemetry — the app reports "last successful update check timestamp" on startup. Alert if >5% of users haven't checked successfully in 7 days. Use multiple fallback URLs. |
| 4 | **Main process crashes from unhandled Promise rejections** — `ipcMain.handle('channel', async () => { throw new Error('...') })` — the unhandled rejection crashes the main process (Electron < v20) or logs a warning with no recovery path. All renderer windows disappear. From the user's perspective, the app "just vanished." | **$20,000-$60,000** in crash-rate-driven app store rating decline (each 0.1-star drop costs ~5% conversion), user churn, and engineering time debugging crash reports with truncated stacks. | Every `ipcMain.handle` must wrap its body in try/catch. Return structured errors: `{ error: { code: 'FILE_NOT_FOUND', message: '...' } }`. Never let exceptions propagate uncaught. Use `process.on('unhandledRejection')` as a safety net with crash reporting. |
| 5 | **GPU process crashes on specific hardware causing white screens** — Chromium's GPU process crashes on: Intel HD Graphics 4000 with driver version 10.18.10.4358, NVIDIA Optimus laptops switching between integrated and discrete GPU, macOS VMs without Metal support, and Linux with Wayland+NVIDIA proprietary drivers. The renderer falls back to software rendering, but `canvas.getContext('webgl')` returns `null` — and your WebGL chart library throws `TypeError`, leaving a white rectangle. | **$15,000-$40,000** in 1-star reviews mentioning "white screen," support burden, and lost users on affected hardware (typically ~3-5% of install base). | Check `canvas.getContext('webgl')` on startup. If null, fall back to a 2D canvas or static image replacement. Test on real hardware with `--disable-gpu` flag. Implement a GPU crash count metric — if it exceeds threshold, auto-disable hardware acceleration. |
| 6 | **File-system race conditions with cloud-sync services** — OneDrive, Dropbox, and Google Drive place hooks on the filesystem that temporarily lock files during sync. Writing to `app.getPath('documents')` while OneDrive is syncing returns `EBUSY` on Windows. Reading a file while Dropbox is updating it returns partial content. `fs.watch` on a synced directory fires 3-4 events per actual change. | **$10,000-$25,000** in data corruption incidents, support tickets from users who "didn't do anything," and engineering time building retry logic after the fact. | Use atomic write patterns (write to temp file, fsync, rename). Retry `EBUSY` with exponential backoff (100ms, 200ms, 400ms, 800ms). Debounce `fs.watch` events by 500ms. Never assume a file is "done" just because it exists. |
| 7 | **DPI scaling breaks layout when moving windows between monitors** — A user drags your app from a 100% scaling 1080p monitor to a 200% scaling 4K monitor. If you used pixel-based sizes (`width: 800px`), the window is now half the physical size on the 4K display. If you used CSS `zoom` or `transform: scale()` for HiDPI, text is blurry because it's being bitmap-scaled instead of re-rendered at native resolution. | **$8,000-$20,000** in negative reviews, accessibility compliance issues (blurry text is an accessibility failure), and engineering time retrofitting DPI awareness post-launch. | Use relative units (`rem`, `em`, `%`) and viewport units. Set `ENABLE_PER_MONITOR_DPI_AWARE_V2` on Windows. Listen for `display-metrics-changed` events and re-render at native resolution. Never use bitmap-based scaling for HiDPI. |

## Anti-Rationalization — No Excuses

| Rationalization | Reality |
|---|---:|
| "We'll use Electron — it works everywhere and our web devs already know it. Tauri is too new." | Tauri has been stable since v1.0 (June 2022) and is in production at companies including Discord alternatives, VPN clients, and developer tools. "Too new" in 2026 means "I haven't evaluated it." The runtime cost of Electron (180MB+ download, 400MB+ RAM) is paid by every user, forever. One week of Rust learning for a 95% smaller binary is a trade-off your users deserve to have evaluated, not dismissed. |
| "Code signing is expensive and complicated. We'll add it after launch when we have revenue." | Unsigned Windows apps lose 60%+ of potential installs at the SmartScreen warning. Unsigned macOS apps require users to right-click → Open or disable Gatekeeper entirely. Your launch metrics will be 40% of what they should be. An EV code signing certificate costs $300-400/year. The lost revenue from abandoned installs in month 1 alone exceeds 10 years of certificate costs. |
| "Auto-update is a v2 feature. We need to ship first." | Without auto-update, v1.0.0 lives forever on every machine that installed it. When you discover a data-corrupting bug in v1.0.0, your only option is emailing users and hoping they manually download the fix. Response rate: <10%. The remaining 90% blame your app for the corruption and leave 1-star reviews. Auto-update is the only channel you control to fix bugs post-install. Building it after launch means building it while users suffer from unfixed bugs. |
| "We'll handle IPC by passing JSON objects through the bridge — just like REST." | The Electron IPC bridge serializes using the Structured Clone Algorithm, not JSON. `Date` objects survive. `Map` and `Set` survive. `ArrayBuffer` transfers zero-copy. But `Function`, `Symbol`, and `WeakMap` throw `DataCloneError`. Treating IPC as loose JSON means: (a) you miss zero-copy optimizations, (b) you're surprised when `new Date()` arrives as a string after manual `JSON.stringify`, and (c) you have no contract for what messages are valid. Define typed IPC channels with input validation — the bridge is a structured protocol, not a REST endpoint. |
| "The installer is just a wrapper. Users know how to install software." | The installer is the first product experience every user has. A confusing installer with unsigned binaries triggers Windows SmartScreen ("Windows protected your PC"), macOS Gatekeeper ("cannot be opened because the developer cannot be verified"), and Linux package manager warnings. 25% of users who see a SmartScreen warning never click "More info" to proceed. Another 35% proceed but have permanently reduced trust in your product. Code signing, silent install options, and clean uninstall are not polish — they are the prerequisite for users to trust your software enough to run it. |

## Verification

- [ ] Run security audit: `grep -rn 'nodeIntegration.*true\|contextIsolation.*false\|sandbox.*false'` returns zero results
- [ ] Run IPC audit: `grep -r 'ipcRenderer\.sendSync'` returns zero results
- [ ] Verify preload isolation: `grep -r "require('electron')" src/renderer/` returns zero results
- [ ] Build succeeds on all platforms: `npm run build:mac`, `npm run build:win`, `npm run build:linux`
- [ ] Installer runs silently: `start /wait MyAppSetup.exe /S` (Windows), `hdiutil attach MyApp.dmg` (macOS)
- [ ] Code signing verified: `signtool verify /pa dist/MyApp.exe`, `spctl -a -v dist/MyApp.app`
- [ ] Auto-update tested: deploy to staging update server, install old version, verify update detection and application
- [ ] E2E tests pass on all platforms in CI: `npm run test:e2e` across macos, windows, ubuntu runners
- [ ] Perform launch-budget: cold start < 3s, warm start < 1.5s, idle RAM < 200MB (Electron) / < 50MB (Tauri)
- [ ] Crash reporter captures both JS and native crashes: trigger test crash, verify it appears in Sentry dashboard

## Verification Guardrails

Before delivering work, the agent must verify:

- [ ] **Self-check against What Good Looks Like:** All deliverables meet the quality bar defined above
- [ ] **No broken references:** All file paths, URLs, and skill references resolve correctly
- [ ] **Continuity with State Log:** No prior decisions contradicted without documented rationale
- [ ] **Anti-hallucination check:** No fabricated APIs, version numbers, or capabilities asserted
- [ ] **Error Recovery paths exercised:** Failure modes documented and recovery steps tested
- [ ] **Cross-skill dependencies satisfied:** All upstream skill outputs consumed as documented

If any checkbox fails, revise before delivering. When all pass, add to the state log.

## References

Detailed reference material loaded on demand:

- **Electron Architecture Patterns**: See [references/electron-architecture-patterns.md](references/electron-architecture-patterns.md) — Process model, preload security, CSP, crash reporting, OS integration
- **Tauri Security Model**: See [references/tauri-security-model.md](references/tauri-security-model.md) — Capability permissions, CSP, command allowlisting, scope restrictions
- **Desktop IPC Patterns**: See [references/desktop-ipc-patterns.md](references/desktop-ipc-patterns.md) — Request/response, push events, streaming, error handling, typed contracts
- **Auto-Update Strategies**: See [references/auto-update-strategies.md](references/auto-update-strategies.md) — electron-updater, Tauri updater, Sparkle, Squirrel, differential updates, rollback
- **Desktop Installer Packaging**: See [references/desktop-installer-packaging.md](references/desktop-installer-packaging.md) — NSIS, WiX, MSIX, DMG, AppImage, Flatpak, snap, code signing, notarization
- **Native Module Integration**: See [references/native-module-integration.md](references/native-module-integration.md) — N-API, FFI, Rust bindings, C++ addons, prebuilds, cross-platform compilation
- **Desktop Window Management**: See [references/desktop-window-management.md](references/desktop-window-management.md) — Multi-window, frameless, DPI scaling, tray, menu bar, focus management
- **Cross-Platform Testing**: See [references/cross-platform-testing.md](references/cross-platform-testing.md) — Spectron, Playwright, platform matrix, GPU testing, power-state simulation

## Operating at Different Levels

| Scale | Challenge | Solution |
|---|---|---|
| 1-10 users | Dev setup works, manual installs acceptable | DMG + NSIS, no auto-update required |
| 10-100 | Version fragmentation begins | Add electron-updater with GitHub Releases provider |
| 100-1K | Support tickets for "won't install" | Add .msi for enterprise, .deb/.rpm for Linux |
| 1K-10K | CDN costs for updates, delta size matters | Differential updates, CDN with cache-control, staged rollouts (5%→25%→100%) |
| 10K-100K | Crash reports flood in, need telemetry | Sentry/Bugsnag native + JS, crash rate target <0.1%, automated crash triage |
| 100K+ | Store compliance, legal review, localization | Microsoft Store ingestion, Mac App Store sandbox, GDPR consent, 12-language installer |

## State Log

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.

### How the State Log Works
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:
   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "desktop-developer",
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

## Production Checklist

- [ ] `nodeIntegration: false`, `contextIsolation: true`, `sandbox: true` (Electron)
- [ ] Preload script is the ONLY file importing `ipcRenderer` from `electron`
- [ ] CSP header blocks `unsafe-eval` and `unsafe-inline` scripts
- [ ] All main-process I/O is async (promises, no sync calls)
- [ ] Tauri capabilities file restricts permissions per window (least privilege)
- [ ] Code signing certificate acquired and configured (EV for Windows)
- [ ] macOS app notarized and stapled (`spctl -a -v MyApp.app` passes)
- [ ] Auto-update tested on a signed, production-identical build from a clean VM
- [ ] Crash reporter configured (`crashReporter.start()` or Sentry native SDK)
- [ ] Window state (bounds, maximized) persisted and restored correctly per display
- [ ] Offline data path uses `app.getPath('userData')`, not CWD or relative paths
- [ ] `before-quit` handler cleans up DB connections, temp files, active timers
- [ ] Installer tested on clean VM (no dev tools, fresh OS install)
- [ ] File associations and custom protocol handlers registered and tested
- [ ] Multi-monitor DPI scaling handled (per-monitor v2 awareness on Windows)
- [ ] All IPC channels documented with input schemas and error responses
- [ ] E2E tests pass on all three platforms in CI
