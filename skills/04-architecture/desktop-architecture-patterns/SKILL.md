---
name: desktop-architecture-patterns
description: "Desktop application architecture patterns covering MVVM, MVP, MVC, Redux-style, event-driven, and platform-specific patterns for Windows, macOS, and Linux. Use when designing desktop app architecture, choosing between web-based (Electron/Tauri) vs native desktop approaches, implementing multi-window management, designing system tray and background service architectures, planning auto-update and installer pipelines, or structuring desktop apps with IPC. Handles desktop-specific concerns: OS integration patterns, file system access architecture, hardware acceleration decisions, and cross-platform desktop strategies. Do NOT use for mobile architecture, web architecture, or game engine architecture."
author: Sandeep Kumar Penchala
license: MIT
version: 1.0.0
updated: 2026-07-24
tags: [desktop, architecture, mvvm, electron, tauri, wpf, patterns, cross-platform]
token_budget: 4500
chain:
  consumes_from:
    - system-architect
    - desktop-developer
    - macos-developer
    - frontend-developer
  feeds_into:
    - desktop-developer
    - macos-developer
    - frontend-developer
---
> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor).

# Desktop Architecture Patterns — Scalable Desktop Application Design

---
<!-- QUICK: 30s -->

## Route the Request
<!-- STANDARD: 3min -->


## Auto-Route (No User Input Required)
<!-- STANDARD: 3min -->
| # | Condition | Action |
|---|-----------|--------|
| A1 | User mentions MVVM, MVP, MVC, Redux-style, or event-driven | This is your skill. Jump to that pattern's dedicated section. |
| A2 | User asks "Electron vs Tauri vs native?" | Jump to **Decision Trees** for the cross-platform selection matrix. |
| A3 | User mentions IPC, inter-process communication, main/renderer | Jump to **Section 7 (IPC Architecture)**. |
| A4 | User mentions auto-update, installer, distribution | Jump to **Section 9 (Auto-Update Architecture)**. |
| A5 | User mentions multi-window, window management | Jump to **Section 6 (Multi-Window Architecture)**. |
| A6 | User mentions system tray, background services, daemon | Jump to **Section 8 (System Tray & Background Services)**. |

## The Expert's Mindset
<!-- STANDARD: 3min -->

You are a desktop architect who has shipped productivity applications, creative tools, and system utilities to millions of users across Windows, macOS, and Linux. You understand that desktop architecture is fundamentally about OS integration depth — how intimately your app knows the host operating system determines its perceived quality. You default to Electron/Tauri for rapid cross-platform delivery, native (WPF/WinUI/SwiftUI) when OS integration is the competitive advantage. You know that the system tray is the most under-designed surface in desktop apps and that a bad auto-updater loses more users than any other single bug.

## Operating at Different Levels
<!-- STANDARD: 3min -->

| Level | Scope | Deliverable |
|-------|-------|-------------|
| **L2 (Practitioner)** | Implement a single desktop feature with correct IPC separation | Working feature with main/renderer separation, correct permission model, and error handling |
| **L3 (Senior)** | Design architecture for a full desktop application (10+ windows, system tray, auto-update) | Architecture decision record. IPC protocol design. Multi-window state management. Distribution pipeline |
| **L4 (Staff)** | Define desktop architecture standards across product portfolio | Desktop platform team playbook. Cross-app component library. Shared IPC protocol. Auto-update infrastructure as shared service |
| **L5 (Principal)** | Pioneer desktop platform innovation, influence OS vendors | Novel desktop paradigms. OS-level integration standards. Industry adoption |

## When to Use
<!-- STANDARD: 3min -->

- Choosing between Electron, Tauri, WPF, WinUI, SwiftUI, or Qt for a new desktop application
- Designing multi-window desktop applications with cross-window state and communication
- Implementing IPC (Inter-Process Communication) between main process and renderer processes
- Designing system tray applications and background services that survive user logout
- Planning auto-update and installer pipelines for Windows (MSIX), macOS (DMG/pkg), and Linux (AppImage/deb)
- Architecting desktop apps that need deep OS integration (file system access, hardware acceleration, native menus)
- Evaluating web-based vs native desktop approaches for performance, bundle size, and OS integration trade-offs

## Core Workflow
<!-- STANDARD: 3min -->

**(STANDARD)**

Desktop architecture follows a 4-phase decision process:


## Phase 1 (~10 min): Platform & Technology Selection
<!-- STANDARD: 3min -->
Evaluate: target OS(es), OS integration depth required, team skills (web vs native), performance requirements, bundle size constraints, distribution complexity. Use the technology selection matrix in Section 16.


## Phase 2 (~15 min): Process Architecture Design
<!-- STANDARD: 3min -->
Decide: single-process vs multi-process. Define main process responsibilities (window management, native APIs, auto-update). Define renderer responsibilities (UI, business logic). Design IPC protocol: channel-based (Electron), command-based (Tauri), or native message passing.


## Phase 3 (~20 min): Window & State Management
<!-- STANDARD: 3min -->
Design: primary window lifecycle, secondary windows (settings, about, modal dialogs), cross-window state synchronization. Decide on state management pattern: Redux/Zustand for Electron, provider/notifier for native, or custom event bus.


## Phase 4 (~15 min): Distribution & Update Architecture
<!-- STANDARD: 3min -->
Design installer strategy per platform. Implement auto-update: check on launch + periodic check (every 4 hours). Handle update rollback on launch failure. Sign binaries: code signing cert for Windows, notarization for macOS.

## Error Recovery
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

**(STANDARD)**

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Best Practices
<!-- STANDARD: 3min -->

1. **Isolate main and renderer processes with context isolation enabled from day one.** `contextIsolation: true` and `nodeIntegration: false` are non-negotiable in Electron. Without them, any XSS in any npm dependency (average Electron app has 1,200+) grants full Node.js access to the attacker. In Tauri, the Rust backend is isolated by design — never expose raw command execution to the frontend. Desktop security breaches from missing context isolation average $500K+ in liability.

2. **Design IPC as typed contracts, not ad-hoc string channels.** Every IPC invocation should have a type-safe request/response contract. Use `ipcMain.handle`/`ipcRenderer.invoke` (Electron) or Tauri commands with typed parameters. Validate all inputs in the main process. Never trust renderer-sent data — the renderer is a sandbox but not a trusted one. IPC without validation is the desktop equivalent of exposed REST endpoints without authentication.

3. **Multi-window architecture must define window ownership and lifecycle before the first secondary window is created.** Each window must have a clear owner (parent-child or sibling). Child windows must close when the parent closes. Window state (position, size, fullscreen) must restore on relaunch. Cross-window state synchronization must be single-source-of-truth — typically in the main process. Retrofitting multi-window after single-window assumptions are baked in is a 6-8 week rewrite.

4. **System tray and background services are not optional — they define desktop apps.** Users expect minimize-to-tray, system notifications, and background operation. On macOS, apps stay alive after the last window closes by convention. On Windows, the system tray is the primary way users interact with long-running apps. Implement tray with context menu, notification handling, and app-quit from tray option. Test on all target platforms — tray behavior differs significantly across OSes.

5. **Auto-update must be architected before v1 ships, not after.** Choose between electron-updater/Squirrel (Electron), Tauri updater, Sparkle (macOS native). Implement: silent background download, apply-on-restart, staged rollouts (5% → 25% → 100%), kill switch for bad releases, rollback on launch failure, and certificate pinning for update servers. Without auto-update, v1.0 bugs live forever — 62% of desktop users never manually update.

6. **DPI scaling must be handled at the architecture level, not patched in CSS.** Windows at 125%/150%/175%, macOS Retina @2x/@3x, Linux fractional scaling (Wayland). Declare DPI awareness in the platform manifest. Use vector assets (SVG) exclusively. Test on every DPI tier. A blurry UI at 150% scaling generates App Store rejections and $25K+ accessibility compliance exposure.

7. **Never block the main thread with synchronous I/O or heavy computation.** A single `fs.readFileSync` on a 50MB file freezes the entire app for 400ms+ — all IPC, window events, and menu actions stop. Use async I/O (`fs.promises`), worker threads, or stream-based reads. Offload CPU-intensive work to worker threads or native addons. Profile main thread responsiveness in CI — target <16ms per tick.

8. **Platform abstraction layers are cheaper than platform-specific codebases.** Define a `Platform` interface with implementations for each target OS. Abstract: window management, file dialogs, notifications, system tray, auto-start, file associations, and updater. The abstraction layer is 10-15% overhead on initial development but saves 200%+ on maintenance compared to maintaining separate Windows, macOS, and Linux codebases.

9. **Secrets must use OS-level secure storage, never LocalStorage or plaintext configs.** Electron's `safeStorage` API encrypts with OS keychain. On Tauri, use the `tauri-plugin-store` with encrypted storage. On native, use Keychain Services (macOS), Credential Manager (Windows), or libsecret (Linux). Tokens in LocalStorage are plaintext to any user with DevTools (F12) — that's every user.

10. **Test on real hardware across all target OS versions, not just CI VMs.** GPU rendering bugs, DPI scaling issues, file permission quirks, and antivirus interference only manifest on real machines. Maintain a test matrix: Windows 10, Windows 11, macOS latest and -1, Ubuntu LTS. CI covers logic; real hardware covers integration. The cost of one missed platform-specific crash in production exceeds the cost of a test device fleet.

## Verification Guardrails
<!-- STANDARD: 3min -->

Run these checks before declaring work complete. ALL must pass.

| # | Guardrail | Check |
|---|-----------|-------|
| V1 | Output matches specification | Compare generated output against the requirements stated at the start. Every explicit requirement must have a corresponding deliverable. |
| V2 | No broken references or links | All file references must resolve. Run `grep -oP '\]\([^)]+\)' [output] | while read link; do [ -f "$link" ] || echo "BROKEN: $link"; done`. |
| V3 | All validations pass where applicable | Run any existing test suite or verification script. `bash scripts/validate-skills.sh` if in this repository. |
| V4 | No placeholder or TODO content remains | `grep -ri 'TODO\|FIXME\|PLACEHOLDER' [output]` must return empty. |
| V5 | Error states handled | Verify error paths produce clear messages, not silent failures or stack traces. |
| V6 | Edge cases considered | Empty input, max/min values, concurrent access, boundary conditions handled or documented as out-of-scope. |
| V7 | Performance within budget | If constraints specified, verify compliance. If not, verify no unbounded loops or quadratic blowup. |
| V8 | Anti-patterns from Anti-Patterns section avoided | Re-read Anti-Patterns section. Verify none of the listed anti-patterns appear in the output. |

## Production Checklist
<!-- STANDARD: 3min -->

**(STANDARD)**

- [ ] **[DAP1]** Context isolation enabled (`contextIsolation: true`, `nodeIntegration: false`) — verified in electron-builder config and runtime check
- [ ] **[DAP2]** All IPC channels typed with request/response contracts — zero `ipcRenderer.send` calls without a corresponding `ipcMain.handle` with input validation
- [ ] **[DAP3]** Multi-window ownership model documented: parent-child relationships, lifecycle hooks, cross-window state sync via main process
- [ ] **[DAP4]** System tray implemented with context menu, notification permission request, and platform-specific behavior verified on Windows + macOS
- [ ] **[DAP5]** Auto-update pipeline: silent background download, apply-on-restart, staged rollout capability, kill switch, rollback on launch failure, certificate pinning
- [ ] **[DAP6]** DPI awareness declared in platform manifest; SVG-only icon strategy; UI tested at 100%, 125%, 150%, 175%, 200% scaling
- [ ] **[DAP7]** Main thread profiled: zero synchronous I/O outside startup, <16ms per tick, heavy computation in worker threads
- [ ] **[DAP8]** Platform abstraction layer with documented interfaces for: window management, file dialogs, notifications, system tray, auto-start, file associations
- [ ] **[DAP9]** Secrets stored via OS secure storage (`safeStorage`/Keychain/Credential Manager/libsecret) — zero tokens in LocalStorage or plaintext config
- [ ] **[DAP10]** Code signing configured: EV cert for Windows, Apple Developer ID + notarization for macOS, GPG for Linux — verified in CI pipeline
- [ ] **[DAP11]** Crash reporting with symbolication across platforms; crash rate <0.5% of sessions; top 5 crashes resolved within 7 days
- [ ] **[DAP12]** E2E tests pass on real hardware: Windows 10, Windows 11, macOS latest, macOS -1, Ubuntu LTS — CI covers unit/integration, hardware covers platform-specific

## Cross-Skill Coordination
<!-- STANDARD: 3min -->

| Upstream Skill | What You Receive | When |
|---|---|---|
| `system-architect` | Overall system architecture, backend API contracts, security requirements | Before desktop architecture design — ensures alignment |
| `desktop-developer` | Implementation feedback on architecture ergonomics | During architecture selection |
| `security-reviewer` | Threat model for desktop-specific vectors (code injection, DLL hijacking, IPC spoofing) | Before finalizing IPC and process architecture |

| Downstream Skill | What You Provide | When |
|---|---|---|
| `desktop-developer` | Architecture playbook, IPC protocol spec, module structure | After architecture is finalized |
| `macos-developer` | macOS-specific patterns: sandboxing, XPC, notarization, MenuBar apps | When targeting macOS |
| `devops-engineer` | CI/CD for multi-platform builds, code signing pipeline, auto-update CDN | Before distribution pipeline setup |

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.


## How the State Log Works
<!-- STANDARD: 3min -->
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:

   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "desktop-architecture-patterns",
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


## State Log Schema
<!-- STANDARD: 3min -->

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


## Anti-Drift Check
<!-- STANDARD: 3min -->
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## What Good Looks Like
<!-- STANDARD: 3min -->

> The desktop app installs in under 15 seconds, launches in under 2 seconds, and stays under 150MB of RAM at idle. Auto-update downloads in the background and applies on next restart — users are never prompted during active work. All IPC calls are typed and validated — zero "could not communicate with main process" errors in the last 10K sessions. The app works identically on Windows 10, Windows 11, macOS Ventura+, and Ubuntu 22.04+ from a single codebase. The system tray icon provides at-a-glance status and quick actions without opening the full window.

## Deliberate Practice
<!-- STANDARD: 3min -->

| Exercise | Skill Targeted | Success Metric |
|----------|---------------|----------------|
| Implement the same calculator app in Electron, Tauri, and SwiftUI | Cross-platform comparison, technology trade-offs | Identify 5+ concrete differences in bundle size, memory, startup time, and OS integration depth |
| Design a multi-window IDE-like app with 4 window types (editor, output, settings, about) | Multi-window architecture, cross-window state | All windows stay in sync. Closing the main window handles children correctly. Window positions restore on relaunch |
| Build a complete auto-update pipeline with staged rollouts and kill switch | Distribution architecture | Update downloads silently. Rollback on launch failure < 5 seconds. Kill switch blocks update within 1 minute of activation |

## Proactive Triggers
<!-- STANDARD: 3min -->

| Trigger | Action | Rationale |
|---|---|---|
| `shell.openExternal()` or `shell.openPath()` with user-supplied input | Block merge — must sanitize and validate before opening | Unvalidated shell commands are RCE vectors on desktop. Always validate paths against allowlist and sanitize shell arguments |
| Bundle size increases by 20%+ in a single PR | Flag — investigate what was added. Desktop users care about download size | A 50MB → 60MB increase may seem small, but it compounds. Desktop apps that exceed 150MB see 30%+ drop in download-to-install conversion |
| Auto-update check fails silently in production for 24+ hours | Escalate to P1 — users are running outdated, potentially vulnerable versions | Desktop apps have no forced update mechanism like web apps. Silent update failures mean security patches never reach users |
| IPC channel adds synchronous blocking call | Reject — all IPC calls must be async with timeout | Synchronous IPC blocks the renderer's main thread, freezing the UI. A single sync IPC call in the renderer process makes the app feel broken |

## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Choosing Electron without considering memory budget on target hardware | $150K-$400K in poor user reviews and uninstalls from 500MB+ memory usage | Profile memory on target hardware (4GB RAM machines). Consider Tauri for memory-constrained use cases |
| No IPC timeout handling leading to frozen UI | $100K-$300K in frozen UI incidents when backend process hangs | Every IPC call must have a timeout and error handler. Test with intentionally slow responses |
| Ignoring auto-update architecture from day 1 | $200K-$500K in stranded users running unpatched vulnerable versions | Implement auto-update (electron-updater, Sparkle, WinGet) before first release. Test update path in CI |
| Single-thread UI blocking during I/O operations | $80K-$200K in crash reports from unresponsive UI during file/network access | Move all file I/O, network calls, and DB queries off the main thread. Use web workers, async IPC, or background processes |

## References
<!-- STANDARD: 3min -->

Detailed reference material loaded on demand:

- **Production Checklist**: See [checklist.md](references/checklist.md)
- **Technology Comparison Matrix**: See [technology-comparison.md](references/technology-comparison.md)
- **Best Practices**: See [best-practices.md](references/best-practices.md)

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->


## 1.1 Non-Negotiables
<!-- STANDARD: 3min -->

1. **NEVER run heavy computation on the main/render thread.** A single 200ms synchronous operation freezes the entire UI, costing $50K+ in user churn per release for mid-market SaaS products. Offload to worker threads, background services, or child processes — no exceptions.

2. **NEVER block the UI thread with synchronous I/O.** File reads, database writes, network calls — all must be async. Even `fs.readFileSync` in Electron's main process blocks IPC handling. Cost of a single freeze: 15-25% reduction in NPS scores within one quarter.

3. **ALWAYS separate process concerns.** Renderer, main, and backend services must run in isolated processes. A crash in one must never cascade. IPC boundaries are your contract — treat them like network boundaries with serialization, validation, and error handling.

4. **NEVER trust renderer-originated data in the main process.** All IPC messages from renderer to main must be validated. Electron's `contextBridge` + `webPreferences.contextIsolation=true` is mandatory, not optional. A single unsanitized message can lead to RCE — average breach cost for desktop apps: $4.2M (IBM Cost of Data Breach 2024).

5. **ALWAYS handle window lifecycle explicitly.** `before-quit`, `will-quit`, `window-all-closed`, platform-specific close behavior (macOS Cmd+Q vs window close) — every transition must be modeled. Miss one and you ship data-loss bugs, costing $80K+ in support escalations and hotfix cycles.

6. **NEVER hardcode platform paths.** `%APPDATA%` on Windows, `~/Library/Application Support` on macOS, `$XDG_DATA_HOME` on Linux. Use `env-paths` or equivalent. Platform path bugs create irrecoverable data-states — average remediation cost: $45K per incident.


## 1.2 Architecture First Principles
<!-- STANDARD: 3min -->

- **Process isolation beats shared memory.** Every desktop app operates in a hostile OS environment. Antivirus hooks, accessibility tools, other apps — all can inject into your process space. Isolate critical logic.
- **The installer is part of your architecture.** Code signing, elevation requirements, file associations, protocol handlers — these are architectural decisions, not packaging afterthoughts.
- **Offline-first by default.** Desktop users have unreliable connectivity. Local SQLite/WAL, CRDT-based sync, and conflict-free merge strategies are required. "We'll add offline later" costs 3-5x more in retrofits.
- **Auto-update is a security feature, not a convenience.** Unpatched desktop apps with 90-day-old versions are the #1 attack vector. If your update mechanism isn't bulletproof, you don't have a product — you have liability.

- **ANCHOR to runtime versions before generating framework-specific code.** Never generate framework-specific API calls from training data alone — your training data may be stale. Run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions. If detection succeeds, anchor all API calls to detected versions; if detection fails, request version info from user. | Trigger: code-generation task involving framework-specific APIs | STOP: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring API calls to these versions."
- **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: code-generation/refactoring task not a security fix, compliance requirement, or production incident | STOP: "ROI Gate analysis: estimate cost vs annual value. See `scripts/roi-gate.sh`."

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.

---

## Decision Trees
<!-- STANDARD: 3min -->

**(QUICK)**

### Decision Tree 5: How Do I Choose an Auto-Update Strategy?

        ┌── INPUT: Desktop app needs update delivery
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
App store           Independent         Enterprise
distribution        updater (Squirrel,  MSI/DEB with
(Mac App Store,     Sparkle, electron-  group policy
Microsoft Store)    updater)            management
   │                 │                  │
   ▼                 ▼                  ▼
Best for: consumer  Best for: B2B       Best for: IT-
apps; zero infra;   tools; control      managed fleets;
review process      release cadence;    silent installs;
required            delta updates       no auto-update

### Decision Tree 6: How Do I Choose IPC Architecture?

        ┌── INPUT: Multi-process desktop app needs IPC
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
Main↔Renderer       Service process     Native IPC
(Electron-style)    ↔UI process         (Unix sockets,
                    (background tasks)   named pipes)
   │                 │                  │
   ▼                 ▼                  ▼
Best for: web-      Best for: long-     Best for: native
based UI; JSON      running tasks;      apps; high-
serialization;      crash isolation;    throughput;
contextBridge       gRPC or DBus        low latency

### Decision Tree 7: How Do I Design System Tray Behavior?

        ┌── INPUT: Desktop app needs background presence
        │
   ┌────┴────────────┬──────────────────┐
   │                 │                  │
   ▼                 ▼                  ▼
Close to tray       Minimize to tray    Separate tray
(hide on close)     (keep running)      + window process
   │                 │                  │
   ▼                 ▼                  ▼
Best for: always-   Best for: music,    Best for: resource
on tools; restore   chat, monitoring;   isolation; tray
from tray icon      quick restore       survives window
                                        crash
   │                 │                  │
   ▼                 ▼                  ▼
macOS: hide();      Cross-platform:     Main + tray
Windows: notifyIcon tray.show() +       helper process;
                    window.hide()       IPC for actions


## 2.1 Electron vs Tauri vs Native
<!-- STANDARD: 3min -->

```

Is your team primarily web/frontend developers?
├── YES → Is bundle size < 15MB critical?
│   ├── YES → Is memory usage < 100MB critical at idle?
│   │   ├── YES → Can you afford platform-specific codebases?
│   │   │   ├── YES → **Native** (WinUI 3, SwiftUI, GTK4)
│   │   │   └── NO → **Tauri** (Rust backend, minimal footprint)
│   │   └── NO → **Tauri** (50-80MB idle, Rust performance)
│   └── NO → Do you need Chromium-level rendering (PDF, complex CSS, WebGL)?
│       ├── YES → **Electron** (VSCode, Figma, Discord path)
│       └── NO → **Tauri** (uses system WebView, 5-15MB bundles)
└── NO → Is cross-platform deployment required?
    ├── YES → **Tauri** (best native-feel per platform)
    └── NO → **Native** (WinUI 3 / SwiftUI+AppKit / GTK4+Adwaita)

```

**Cost of wrong choice:** Electron when Tauri would suffice → $120K/yr in excess memory/CPU on user machines (support load). Tauri when Electron is needed → $200K+ rewriting rendering pipeline for complex browser features.


## 2.2 MVVM vs MVP vs Redux-Style for Desktop
<!-- STANDARD: 3min -->

```

Does your app have complex, interactive forms with bidirectional data binding?
├── YES → Does the framework support native data binding (WPF, WinUI, SwiftUI)?
│   ├── YES → **MVVM** — the framework wiring is battle-tested
│   └── NO → **MVP** — manual binding with presenter mediation
└── NO → Is your state highly relational with undo/redo, time-travel, or collaborative state?
    ├── YES → **Redux-style** (unidirectional data flow, single store, pure reducers)
    └── NO → How many distinct windows/views share state?
        ├── 1-3 → **MVP** — simpler, less ceremony
        └── 4+ → **Redux-style** — centralized store prevents sync chaos

```


## 2.3 Multi-Window vs Single-Window with Tabs/Views
<!-- STANDARD: 3min -->

```

Does the user need to compare content side-by-side?
├── YES → **Multi-window** — OS-level window management is irreplaceable
└── NO → Does the app have > 5 distinct functional areas?
    ├── YES → Does each area operate on independent data contexts?
    │   ├── YES → **Multi-window** — independent crash isolation
    │   └── NO → **Single-window with tabs** — browser-like navigation
    └── NO → **Single-window with navigation** — simpler lifecycle

```


## 2.4 SQLite vs File-Based Storage
<!-- STANDARD: 3min -->

```

Is your data structured with > 1000 records or relational queries?
├── YES → **SQLite with WAL mode** — proven at terabyte scale
└── NO → Is the data inherently document-oriented (JSON, Markdown)?
    ├── YES → Do you need concurrent access from multiple processes?
    │   ├── YES → **SQLite** — locking is solved, file-based isn't
    │   └── NO → **File-based** (JSON/YAML per document)
    └── NO → **SQLite** — future-proofs against schema evolution

```


## 2.5 Auto-Update Strategy
<!-- STANDARD: 3min -->

```

Is your app on an app store (Mac App Store, Microsoft Store)?
├── YES → **Store-managed updates** — zero infrastructure cost
└── NO → Is delta update size critical (users on metered connections)?
    ├── YES → **Tauri updater / Electron-builder with NSIS/AppImage delta**
    └── NO → How critical is update reliability?
        ├── Mission-critical (IDE, security tool) → **Squirrel** (Windows) / **Sparkle 2** (macOS)
        └── Standard → **electron-updater / Tauri updater** — simple, well-tested

```


## 2.6 IPC Mechanism
<!-- STANDARD: 3min -->

```

Are you using Electron/Tauri?
├── Electron → contextBridge + ipcRenderer/ipcMain (structured clone algorithm)
│   ├── High throughput (>100 msg/s) → MessagePort (transferable streams)
│   └── Standard → invoke/handle pattern (request-response)
├── Tauri → invoke (command pattern, JSON serialized)
│   ├── Binary data → Tauri file drop / custom protocol
│   └── Streaming → Tauri event system (listen/emit)
└── Native → Platform IPC
    ├── Windows → Named pipes (duplex, 64KB default buffer)
    ├── macOS → XPC Services (privilege separation, launchd-managed)
    └── Linux → Unix domain sockets (D-Bus for desktop integration)

```

---

## 3. Anti-Patterns
<!-- STANDARD: 3min -->

| # | Gotcha | Impact | Mitigation | Mechanical Trigger (detect before executing) | Violation Response |
|---|--------|--------|------------|---|
| 1 | **Blocking the main thread with synchronous file I/O.** A single `fs.readFileSync` on a 50MB file blocks Electron's main process for 400ms+. All IPC, window events, and menu actions freeze. | $90K/yr in support tickets for "app freezes randomly." | Use `fs.promises`, worker threads, or stream-based reads. Never sync I/O outside startup. | | |

| 2 | **Storing sensitive data in LocalStorage/SessionStorage.** Electron's `webContents` can be DevTools-inspected. Tokens, keys, credentials in LocalStorage are plaintext to any user with F12. | $1.2M average breach cost for credential exfiltration via desktop app. | `safeStorage` API for secrets, OS keychain (`keytar`/`electron-secure-defaults`), encrypt-at-rest with `libsodium`. | | |

| 3 | **Assuming `window-all-closed` quits on macOS.** macOS convention: apps stay alive after last window closes. Calling `app.quit()` here breaks every macOS user's expectation. | $35K in App Store 1-star reviews, rejected from Mac App Store for HIG violation. | Platform-check: `if (process.platform !== 'darwin') { app.quit(); }` | | |

| 4 | **Not handling `will-quit` for cleanup.** Temp files, database WAL checkpoints, pending sync operations — all lost. SQLite needs `sqlite3_close` or WAL corruption on force-quit. | $60K per major version in data-corruption support escalations. | Register `app.on('will-quit', async () => { await db.close(); await cleanup(); })` | | |

| 5 | **Ignoring DPI scaling in native apps.** Windows at 125%/150%/175% scaling, macOS Retina @2x/@3x, Linux fractional scaling (Wayland). Without manifest entries and vector assets, UI is illegible. | $25K in accessibility compliance fines and refunds. | Declare DPI awareness in manifest, use vector icons (SVG), test at every DPI tier. | | |

| 6 | **Spawning child processes without spawn-detached cleanup.** Orphaned processes consume memory, hold file locks, and prevent clean uninstall. | $15K/yr in user complaints about "app won't update/uninstall." | Use `detached: true` with `process.kill()` on quit, register cleanup in OS uninstall scripts. | | |

| 7 | **No graceful degradation when GPU process crashes.** Electron's GPU process crash kills WebGL/Canvas. Without fallback to software rendering, the app becomes a blank white window until restart. | $40K in user churn for creative/professional tools. | Listen for `gpu-process-crashed`, switch to software rendering, notify user with recovery action. | | |

| 8 | **Hardcoding update server URLs without certificate pinning.** MITM at coffee shop WiFi → malicious update delivered → full system compromise. | $500K+ liability if your app is the attack vector for enterprise breaches. | Certificate pinning in update client, signed updates with Ed25519, verify signatures before applying. | | |

--- | |

## 4. Anti-Rationalization
<!-- STANDARD: 3min -->

This table lists the excuses teams give for skipping architectural rigor — and why those excuses don't survive scrutiny.

| Statement | Reality |
|-----------|---------|
| *"We'll add security later — right now we need to ship."* | Desktop apps that ship without `contextIsolation` and `nodeIntegration: false` are permanently exploitable. Users don't update. The version you ship today is the version on 40% of machines in 2 years. There is no "later." |
| *"IPC overhead doesn't matter — it's all local."* | Structured clone algorithm in Electron serializes all data crossing process boundaries. Passing a 10MB ArrayBuffer via IPC without transferables copies it in memory. At 60fps rendering with live data, that's 600MB/s of needless allocation. IPC is real overhead — measure it. |
| *"We don't need auto-update — users will get it from the website."* | 62% of desktop users never manually update. Your crash reports show bugs you fixed 6 months ago. Every unpatched install is a support ticket waiting to happen and, for security fixes, a potential CVE disclosure. |
| *"Just use `nodeIntegration: true` — it's simpler for development."* | This is the desktop equivalent of `eval(userInput)`. It exposes the full Node.js runtime to any XSS in any dependency (of which the average Electron app has 1,200+). The 30 minutes saved in development costs $10K/hour in incident response when exploited. |
| *"Multi-window architecture is premature — we'll refactor later."* | Window management touches IPC, state sync, lifecycle, menu state, and OS integration. Retrofitting multi-window support after single-window assumptions are baked into the state layer is a 6-8 week rewrite. Architectural decisions at the window level are effectively irreversible after 3 months of development. |

---

## 5. Core Desktop Architecture Patterns
<!-- STANDARD: 3min -->
<!-- COMPRESSED: Full 91 lines extracted to references/5-core-desktop-architecture-patterns.md -->


## 5.1 MVVM (Model-View-ViewModel)
<!-- STANDARD: 3min -->

The dominant pattern for data-binding-native frameworks (WPF, WinUI 3, SwiftUI, Avalonia).

```

...
> 📎 **Full content (91 lines):** [references/5-core-desktop-architecture-patterns.md](references/5-core-desktop-architecture-patterns.md)

## 6. Multi-Window Architecture
<!-- STANDARD: 3min -->


## 6.1 Window Ownership Model
<!-- STANDARD: 3min -->

```

┌──────────────────────────────────────────┐
│              MAIN PROCESS                 │
│  ┌────────┐  ┌────────┐  ┌────────────┐ │
│  │Window 1│  │Window 2│  │Window N    │ │
│  │(parent)│  │(child) │  │(independent)│ │
│  └───┬────┘  └───▲────┘  └────────────┘ │
│      │           │                       │
│      │  IPC sync │                       │
│      └───────────┘                       │
└──────────────────────────────────────────┘

```

**Critical rules:**
- Each window = isolated `BrowserWindow`/`WebView`/`NSWindow` instance
- Shared state via main-process store, never via global variables in renderer
- Window lifecycle events: `created` → `shown` → `focused` → `blurred` → `minimized` → `closed` → `destroyed`
- Parent-child window relationships for modality (macOS sheets, Windows modal dialogs)

See: [reference/multi-window-architecture.md](reference/multi-window-architecture.md)

---

## 7. IPC Architecture
<!-- STANDARD: 3min -->

```

┌──────────────────────────────────────────────────┐
│                  MAIN PROCESS                     │
│  ┌─────────────┐  ┌──────────┐  ┌──────────────┐│
│  │ IPC Router  │  │ Services │  │ Native APIs  ││
│  │ (validate,  │──│ (business│──│ (file system, ││
│  │  authorize, │  │  logic)  │  │  OS keychain) ││
│  │  route)     │  └──────────┘  └──────────────┘│
│  └──────▲──────┘                                 │
└─────────│────────────────────────────────────────┘
          │ contextBridge / preload
┌─────────│────────────────────────────────────────┐
│         ▼               RENDERER PROCESS         │
│  ┌─────────────┐  ┌────────────────┐            │
│  │ IPC Client  │──│ UI Components  │            │
│  │ (typed API) │  │ (React/Vue/    │            │
│  │             │  │  Svelte)       │            │
│  └─────────────┘  └────────────────┘            │
└──────────────────────────────────────────────────┘

```

See: [reference/desktop-ipc-architecture.md](reference/desktop-ipc-architecture.md)

---

## 8. System Tray & Background Services
<!-- STANDARD: 3min -->
<!-- Full 31 lines extracted to references/8-system-tray-background-services.md -->

┌─────────────────────────────────────────┐
│          SYSTEM TRAY ICON               │
│  ┌───────────────────────────────────┐ │
│  │  Show/Hide Windows                │ │
...
> 📎 **[references/8-system-tray-background-services.md](references/8-system-tray-background-services.md)** — 31 lines of detailed guidance

## 9. Auto-Update Architecture
<!-- STANDARD: 3min -->

```

┌──────────┐   check   ┌─────────────┐   fetch   ┌──────────────┐
│   App    │──────────►│ Update      │──────────►│ CDN / S3 /   │
│ (current │           │ Client      │           │ Update Server│
│  version)│◄──────────┤ (background)│◄──────────┤              │
└────┬─────┘  metadata └──────┬──────┘  download └──────────────┘
     │                        │
     │  apply                 │ verify signature (Ed25519)
     ▼                        ▼
┌──────────┐   restart  ┌──────────────┐
│  Updated │◄───────────┤  Staged      │
│   App    │            │  Update      │
└──────────┘            └──────────────┘

```

**Required security properties:**
- Updates signed with Ed25519 — verify before applying
- Update metadata over HTTPS with certificate pinning
- Staged update directory (never overwrite running binary in-place)
- Rollback capability if new version fails to start
- Background download with progress and resume support

See: [reference/desktop-auto-update-patterns.md](reference/desktop-auto-update-patterns.md)

---

## 10. Desktop Security Architecture
<!-- STANDARD: 3min -->


## 10.1 Threat Model
<!-- STANDARD: 3min -->

```

┌──────────────────────────────────────────────┐
│               THREAT SURFACE                  │
│  ┌────────────┐  ┌──────────┐  ┌───────────┐ │
│  │ RENDERER   │  │ IPC      │  │ NATIVE    │ │
│  │ (XSS,      │  │ (message │  │ (DLL      │ │
│  │  prototype │  │  spoof,  │  │  hijack,  │ │
│  │  pollution)│  │  reentry)│  │  symlink) │ │
│  └────────────┘  └──────────┘  └───────────┘ │
└──────────────────────────────────────────────┘

```

See: [reference/desktop-security-architecture.md](reference/desktop-security-architecture.md)

---

## 11. Cross-Platform Desktop Strategies
<!-- STANDARD: 3min -->


## 11.1 Platform Abstraction Layer
<!-- STANDARD: 3min -->

```

┌──────────────────────────────────────┐
│        APPLICATION LOGIC              │
│  (framework-agnostic, pure business)  │
├──────────────────────────────────────┤
│     PLATFORM ABSTRACTION LAYER       │
│  ┌────────┐ ┌────────┐ ┌──────────┐ │
│  │Windows │ │ macOS  │ │  Linux   │ │
│  │Adapter │ │Adapter │ │ Adapter  │ │
│  └────────┘ └────────┘ └──────────┘ │
├──────────────────────────────────────┤
│         OS NATIVE APIs               │
└──────────────────────────────────────┘

```

See: [reference/cross-platform-desktop-strategies.md](reference/cross-platform-desktop-strategies.md)

---

## 12. Desktop State Management
<!-- STANDARD: 3min -->


## 12.1 State Categories
<!-- STANDARD: 3min -->

| Category | Location | Persistence | Sync Strategy |
|----------|----------|-------------|---------------|
| UI State (tabs, scroll) | Renderer memory | None | Per-window, lost on close |
| Session State (open files, undo) | Renderer + Main | SQLite WAL | IPC to main periodically |
| User Preferences | Main process | SQLite / JSON | Read on startup, write on change |
| Secrets (tokens, keys) | OS Keychain | OS-managed | Never in renderer memory |
| Application Cache | App data dir | Filesystem | LRU eviction, size-capped |

See: [reference/desktop-state-management.md](reference/desktop-state-management.md)

---

## 13. Performance Architecture
<!-- STANDARD: 3min -->
<!-- Full 34 lines extracted to references/13-performance-architecture.md -->


## 13.1 Thread/Process Model
<!-- STANDARD: 3min -->
┌────────────────────────────────────────────────┐
│                  MAIN PROCESS                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │
...
> 📎 **[references/13-performance-architecture.md](references/13-performance-architecture.md)** — 34 lines of detailed guidance

## 14. Installer & Distribution Architecture
<!-- STANDARD: 3min -->


## 14.1 Platform Matrix
<!-- STANDARD: 3min -->

| Platform | Format | Code Signing | Store Option |
|----------|--------|--------------|--------------|
| Windows | NSIS / MSI / MSIX | EV Code Signing Certificate | Microsoft Store |
| macOS | DMG / PKG | Apple Developer ID + Notarization | Mac App Store |
| Linux | AppImage / deb / rpm / Flatpak | GPG (optional) | Flathub / Snap Store |


## 14.2 Installation Concerns
<!-- STANDARD: 3min -->
- Per-user vs per-machine installation
- File associations and protocol handlers (registry on Windows, plist on macOS, `.desktop` on Linux)
- Auto-start registration (respect user choice, easy to disable)
- Clean uninstall (remove app data, registry entries, file associations)

---

## 15. Testing Architecture
<!-- STANDARD: 3min -->


## 15.1 Testing Pyramid for Desktop Apps
<!-- STANDARD: 3min -->

```

         ┌──────┐
         │ E2E  │  Playwright/Spectron (5%)
        ┌┴──────┴┐
        │  IPC   │  Integration: main+renderer (15%)
       ┌┴────────┴┐
       │  Unit    │  Business logic, reducers, presenters (80%)
       └──────────┘

```


## 15.2 Desktop-Specific Test Concerns
<!-- STANDARD: 3min -->
- Multi-window interaction tests
- System tray click → window show/hide
- Auto-update download → apply → restart cycle
- Graceful GPU crash recovery
- File association handling on each platform
- DPI scaling at every supported scale factor
- Accessibility tree validation (AX tree on macOS, UIA on Windows)

---

## 16. Quick Reference: Technology Selection Matrix
<!-- STANDARD: 3min -->

| Requirement | Recommended Stack | Why |
|-------------|-------------------|-----|
| Cross-platform, web dev team | Electron + React | Largest ecosystem, mature tooling |
| Cross-platform, small footprint | Tauri + Svelte | 5-15MB bundles, Rust performance |
| Windows-only, enterprise | WinUI 3 + .NET MVVM | Native Windows 11 integration |
| macOS-only, consumer | SwiftUI + AppKit fallback | HIG compliance, App Store ready |
| Linux-only, system tool | GTK4 + Rust | Adwaita theming, Flatpak distribution |
| Real-time collaboration | Electron + CRDT (Yjs) | Proven at scale (Notion, Linear) |
| Media/graphics intensive | Native (C++ + platform API) | Direct GPU access, no browser overhead |
| Internal enterprise tool | Electron + low-config | Speed to market, no store approval |

---

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "Electron is too bloated; we'll use a native framework per platform" | Maintaining 3 native codebases (Win32, Cocoa, GTK) costs 180-250% of a single cross-platform codebase; shipping velocity drops 3x and feature parity drifts within 2 releases |
| "Multi-window support? Our app only needs one window" | Users open settings, find/replace, or export as separate windows; hacking them in later means race conditions on shared state and zombie windows that crash on close |
| "Auto-update is a nice-to-have; we'll add it after v1" | Without auto-update, v1.0 bugs live forever on user machines; support tickets for already-fixed issues consume 30% of engineering time in the first year |
| "IPC performance doesn't matter; it's just passing small messages" | JSON serialization for IPC in a rendering-heavy app adds 2-5ms per frame; at 60fps, that burns 12-30% of your frame budget on serialization alone — visible as UI stutter |
| "System tray and background services can wait" | Users expect desktop apps to minimize to tray, show notifications, and run in the background; shipping without these means your app feels like a web page, not a desktop app |

## 17. Reference Files
<!-- STANDARD: 3min -->

| File | Content | Lines |
|------|---------|-------|
| [desktop-mvvm-patterns.md](reference/desktop-mvvm-patterns.md) | MVVM deep-dive across WPF, SwiftUI, Electron/MobX | ~350 |
| [multi-window-architecture.md](reference/multi-window-architecture.md) | Window lifecycle, ownership, state sync, modality | ~350 |
| [desktop-ipc-architecture.md](reference/desktop-ipc-architecture.md) | IPC patterns, contextBridge, typed APIs, streaming | ~350 |
| [system-tray-background-services.md](reference/system-tray-background-services.md) | Tray patterns, background services, platform specifics | ~300 |
| [desktop-auto-update-patterns.md](reference/desktop-auto-update-patterns.md) | Update architecture, Squirrel, Sparkle, delta updates | ~300 |
| [desktop-state-management.md](reference/desktop-state-management.md) | Redux, Zustand, multi-window sync, persistence | ~350 |
| [cross-platform-desktop-strategies.md](reference/cross-platform-desktop-strategies.md) | Platform abstraction, build matrix, platform-specific code | ~350 |
| [desktop-security-architecture.md](reference/desktop-security-architecture.md) | Threat model, sandboxing, CSP, code signing | ~350 |

---

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|-----------------|--------|
| ☐ | Complete when Every `ipcMain.handle` is wrapped in try/catch returning structured `{ data?, error? }` responses | `grep -r "ipcMain.handle" src/` — all handlers must have error wrapping; lint rule enforced in CI |
| ☐ | Complete when GPU crash recovery is implemented: `gpu-process-crashed` and `render-process-gone` events are handled with fallback to software rendering | Trigger GPU crash in test: verify app relaunches with `--disable-gpu` and renders correctly |
| ☐ | Complete when Auto-update pipeline tested end-to-end: download → staging → apply → restart cycle works on clean OS installs | Production dashboard tracks update success rate; alert fires if <95% of users successfully update |
| ☐ | Complete when Multi-window state is synchronized: window open/close lifecycle tested with no zombie windows or leaked IPC listeners | Open/close 10 windows in rapid sequence; verify `ipcRenderer.eventNames()` returns zero unexpected listeners |
| ☐ | Complete when Web security is enforced in production: `webSecurity: false` is absent from all production configs | `grep -r "webSecurity.*false"` returns empty in production builds; CSP validator passes in CI |
| ☐ | Complete when Memory budget enforced: app uses <150MB after 1 hour idle with no memory growth trend across releases | Profile with `webContents.getProcessMemoryInfo()` weekly; CI blocks releases with >20% memory growth |
| ☐ | Complete when Window state restoration works across: app quit, logout/login, system restart, and external display disconnect | Test matrix covers all four restoration scenarios on each target platform |
| ☐ | Complete when VC++ redistributables (Windows) or equivalent runtime dependencies are bundled with the installer | Test on clean OS VM (no dev tools); dependency walker scan in CI catches missing DLLs |
| ☐ | Complete when IPC response types are enforced: all main→renderer communication uses typed `IPCResponse<T>` with error checking on the renderer side | TypeScript compiler enforces response type; lint rule prevents destructuring without error check |
| ☐ | Complete when System tray and background service lifecycle is tested: minimize-to-tray, notification delivery, and wake-from-sleep all work correctly | Test matrix covers: tray minimize/restore, notification click, system sleep/wake, OS dark mode toggle |
