# Windows-Native & Linux-Native Desktop Depth (WinUI/Win32, GTK/Qt)

> Deep-dive reference loaded on demand by `desktop-developer`. The cross-platform toolkits
> (Electron/Tauri/MAUI/Qt) get you 80% of desktop users fast — but when real users demand
> native behavior (Windows 11 Snap Layouts, native title bars, Linux DE integration, per-OS
> accessibility), you drop to platform-native UI. Think like an engineer who has shipped to
> 100M Windows seats AND a Linux enterprise fleet: native is a promise about behavior and
> integration, not a badge of purity.

## 0. When to Go Native vs Stay Cross-Platform

```
What does the product actually need?
├── Broad reach, fast iteration, web tech available
│   └── Electron or Tauri — native shell, web UI. Most SaaS desktop apps live here.
├── Windows-enterprise or Windows-only market (finance, healthcare, utilities)
│   └── WinUI 3 (modern) or WPF (legacy interop). Native Windows behavior wins deals.
├── Deep OS integration (Shell, taskbar, notifications, file associations, accessibility)
│   ├── Windows → WinUI 3 / Win32 (P/Invoke where needed)
│   ├── macOS → AppKit/SwiftUI (see macos-developer)
│   └── Linux → GTK4 (GNOME) or Qt (KDE/cross-DE) — target the DE your users run
├── One codebase for Windows + Linux + macOS with native-ish feel
│   └── Qt (C++/QML) or .NET MAUI (Windows-first) — native widgets, one codebase
└── Embedded/kiosk or driver-adjacent Windows → Win32 (C/C++) directly
```

## 1. Windows Native — WinUI 3

### Project & architecture
- **WinUI 3** = Windows App SDK: XAML, Fluent design, modern controls. Use for NEW Windows
  apps. **WPF** = .NET Framework/.NET native-windowed XAML with the deepest ecosystem for
  enterprise/legacy. **Win32** (C/C++) = shell extensions, low-level, driver-adjacent work.
- Architecture: MVVM with `CommunityToolkit.Mvvm`; `Microsoft.UI.Xaml` for WinUI; keep
  business logic in a netstandard/.NET library shared with tests (no UI dependency).
- **Deployment**: MSIX packaging (Store/Sideload) for modern; MSI/EXE bootstrappers
  (WiX/Inno) for enterprise. MSIX = clean install/update/uninstall; enterprise often needs
  MSI for GPO/Intune. Support both from one build.

### Windows-specific behavior users actually notice
- **Title bar & windowing:** `AppWindow`/`Window` customization; Snap Layouts integration
  (Windows 11) — honor `WM_GETMINMAXINFO` and DPI awareness (per-monitor v2). Handle
  multiple monitors with different scales — blurry text on a 2nd monitor kills trust.
- **Taskbar:** thumbnail buttons, progress state (`SetProgressState`), jump lists, icon
  badges — the OS chrome is part of your app's UX.
- **Notifications:** Windows toast (`Microsoft.Windows.AppNotifications`); toast actions;
  notification history. Don't build your own tray-only notifications.
- **File associations & shell:** register via manifest (MSIX) or registry (MSI); drag-drop
  from Explorer; Explorer context menus (packaged COM).
- **Accessibility:** WinUI/WPF have solid UIA support when you use real controls and set
  `AutomationProperties`. Narrator + keyboard-only must work; this is a procurement gate in
  government/enterprise.

## 2. Windows Native — Win32 essentials (when you need the metal)

- **Message loop & window procs** are the substrate everything else wraps. For UI apps prefer
  WinUI/WPF; reach for Win32 for: shell extensions, global hotkeys, low-level input, tray
  icons with precise control, and interop (P/Invoke from .NET or via COM).
- **DPI:** declare per-monitor-v2 in the manifest; handle `WM_DPICHANGED`; never mix
  system-DPI assumptions with per-monitor reality.
- **Interop patterns:** HWND hosting (host Win32 in WinUI via `DesktopWindowXamlSource`, or
  WinUI in Win32 via `XamlIsland`), COM for Office/Shell, and keep a thin native layer with
  the bulk of logic in managed code (testable, safe).

## 3. Linux Native — GTK vs Qt

### Choose by desktop environment, not by preference
- **GNOME-first users** → **GTK4** (`gtk4-rs` for Rust, PyGObject for Python, C). Libadwaita
  (`libadwaita`) gives GNOME-native look with `AdwApplication`, adaptive breakpoints.
- **KDE / cross-DE users** → **Qt** (C++/QML, PySide6, or Qt for Python). Qt looks native
  enough everywhere and is the pragmatic choice for a Linux app that must run on many DEs.
- **Enterprise Linux fleet** (RHEL/Ubuntu LTS with a pinned DE) → match the DE: GTK for
  GNOME shops, Qt for KDE shops. Do not ship a "generic" toolkit that matches neither.

### Linux integration that separates native from "it runs"
- **Desktop file & icons:** proper `.desktop` entry, icon theme compliance, `%U` file
  handling, `.desktop` actions.
- **Notifications:** `org.freedesktop.Notifications` via libnotify/`notify-send`; actions
  and persistence.
- **App indicators/tray:** StatusNotifier (SNI) — many DEs removed legacy XEmbed tray;
  test on the DE your users actually run.
- **Sandboxing:** Flatpak with a proper manifest (permissions, portals) for distribution;
  portals for file dialogs, screenshots, and settings — don't bypass with host calls.
- **Fractional scaling & Wayland:** test on Wayland (XWayland fallback is not "Wayland
  support"); handle fractional scaling, `wlr-layer-shell`/window rules where needed.
- **Accessibility:** AT-SPI via `at-spi2` — GTK4/Qt5+ support it when real widgets are used;
  verify with Orca on your target DE.

## 4. Cross-cutting native desktop checklist

- [ ] **Installer & update**: MSIX/MSI (Windows), Flatpak/AppImage/deb/rpm (Linux), with an
      auto-update path (see references/auto-update-strategies.md).
- [ ] **Signing**: Authenticode (Windows — drivers/enterprise gate on it), GPG/Flatpak
      signing (Linux). Unsigned Windows apps trigger SmartScreen friction.
- [ ] **Per-monitor DPI + fractional scaling** verified on real hardware (Windows + Wayland).
- [ ] **Accessibility**: Narrator/Orca + keyboard-only pass; real controls, not custom
      painted ones without automation peers.
- [ ] **Shell integration**: taskbar/tray/notifications/file associations behave natively.
- [ ] **Telemetry/crash**: native crash reporting (WER/Crashpad) — managed-only logging misses
      native crashes.
- [ ] **Test matrix**: Windows 10/11 + ARM64 Windows; Ubuntu LTS + Fedora + the DE your
      enterprise runs; CI on all three.

## War stories

- **The "runs everywhere" app that ran nowhere well:** A cross-platform toolkit app shipped
  to a Windows enterprise — blurry on the second monitor, no Snap Layouts, SmartScreen
  warning on every install. The deal stalled in procurement. Rebuild of the shell on WinUI 3
  with MSIX + Authenticode signing cleared it in one cycle. Lesson: in enterprise Windows,
  native behavior and signing are procurement requirements, not polish.
- **The Linux app that ignored the DE:** A Qt app "worked" on GNOME but looked and behaved
  like a KDE refugee — wrong theming, tray icon missing, notifications broken. Users
  uninstalled. Porting the shell to GTK4/libadwaita for the GNOME fleet fixed adoption.
  Lesson: on Linux, match the DE your users actually run; there is no generic native.
- **The Wayland surprise:** An Electron-era app "worked fine" until the company moved to
  Wayland-only GNOME — screen sharing and window rules broke. Lesson: test on Wayland, not
  just X11; XWayland compatibility is not Wayland support.
