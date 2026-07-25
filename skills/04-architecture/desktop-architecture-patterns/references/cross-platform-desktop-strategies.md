# Cross-Platform Desktop Strategies — Architecture & Decision Framework

## Overview

Cross-platform desktop development is a spectrum from "write once, run anywhere" to platform-native excellence. The right strategy balances development cost, user experience, and maintenance burden. This reference provides frameworks for making these decisions and implementing effective platform abstraction.

---

## The Cross-Platform Spectrum

```
┌────────────────────────────────────────────────────────────────┐
│  Shared Code ─────────────────────────────────────► Native     │
│                                                                │
│  Web-based        Hybrid          Native-Core      True Native │
│  ┌─────────┐   ┌─────────┐    ┌──────────┐    ┌──────────┐    │
│  │Electron │   │ Tauri    │    │ React     │    │ WinUI 3  │    │
│  │100% web │   │ Web UI + │    │ Native    │    │ (Win)    │    │
│  │         │   │ backend  │    │ Shell     │    │ (Mac)    │    │
│  └─────────┘   └─────────┘    └──────────┘    │ GTK4     │    │
│                                                │ (Linux)  │    │
│  80-95% shared  70-85% shared  50-70% shared   └──────────┘    │
│                                               0-10% shared     │
└────────────────────────────────────────────────────────────────┘
```

---

## Platform Abstraction Layer (PAL) Pattern

### Architecture

```
┌──────────────────────────────────────────────────────┐
│              APPLICATION LAYER                        │
│  ┌──────────────────────────────────────────────┐    │
│  │  Business logic, state management, routing    │    │
│  │  ZERO platform imports                        │    │
│  └────────────────────┬─────────────────────────┘    │
├───────────────────────┼──────────────────────────────┤
│           PLATFORM ABSTRACTION LAYER                  │
│  ┌────────┐  ┌──────────┐  ┌──────────┐             │
│  │Windows │  │  macOS   │  │  Linux   │             │
│  │Adapter │  │ Adapter  │  │ Adapter  │             │
│  └───┬────┘  └────┬─────┘  └────┬─────┘             │
└──────┼────────────┼─────────────┼───────────────────┘
       │            │             │
│           OS NATIVE LAYER                             │
└──────────────────────────────────────────────────────┘
```

### Interface Definition

```typescript
// platform/interface.ts — shared contract
export interface PlatformAdapter {
  readonly name: 'win32' | 'darwin' | 'linux';
  readonly version: string;

  // File system
  getAppDataDir(): string;
  getDocumentsDir(): string;
  getTempDir(): string;

  // Notifications
  showNotification(opts: NotificationOptions): Promise<string>;
  requestNotificationPermission(): Promise<boolean>;

  // Window management
  setProgressBar(windowId: string, progress: number): void;
  setBadgeCount(count: number): void;
  flashWindow(windowId: string): void;

  // Auto-start
  setAutoStart(enabled: boolean): Promise<void>;
  isAutoStartEnabled(): Promise<boolean>;

  // File associations
  registerFileAssociation(ext: string, mimeType: string): Promise<void>;

  // Deep links / protocol handlers
  registerProtocol(protocol: string): Promise<void>;

  // Power management
  getPowerState(): Promise<PowerState>;

  // Cleanup
  dispose(): void;
}
```

### Platform Implementations

```typescript
// platform/win32.ts
class WindowsAdapter implements PlatformAdapter {
  readonly name = 'win32' as const;
  readonly version = process.getSystemVersion() || '';

  getAppDataDir(): string {
    return path.join(process.env.APPDATA || '', 'MyApp');
  }

  setAutoStart(enabled: boolean): Promise<void> {
    const key = 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run';
    // Registry manipulation via node-regedit or native addon
    return enabled
      ? this.setRegistryValue(key, 'MyApp', process.execPath)
      : this.deleteRegistryValue(key, 'MyApp');
  }

  setProgressBar(windowId: string, progress: number): void {
    const win = BrowserWindow.fromId(parseInt(windowId));
    win?.setProgressBar(progress);
  }

  flashWindow(windowId: string): void {
    const win = BrowserWindow.fromId(parseInt(windowId));
    win?.flashFrame(true);
  }
}

// platform/darwin.ts
class MacOSAdapter implements PlatformAdapter {
  readonly name = 'darwin' as const;
  readonly version = process.getSystemVersion() || '';

  getAppDataDir(): string {
    return path.join(
      process.env.HOME || '',
      'Library',
      'Application Support',
      'MyApp'
    );
  }

  setAutoStart(enabled: boolean): Promise<void> {
    const plistPath = path.join(
      process.env.HOME || '',
      'Library', 'LaunchAgents',
      'com.myapp.helper.plist'
    );
    // Write or delete LaunchAgent plist
    return enabled
      ? fs.promises.writeFile(plistPath, this.generatePlist())
      : fs.promises.unlink(plistPath).catch(() => {}); // Ignore if doesn't exist
  }

  setBadgeCount(count: number): void {
    app.dock.setBadge(count > 0 ? count.toString() : '');
  }
}

// platform/linux.ts
class LinuxAdapter implements PlatformAdapter {
  readonly name = 'linux' as const;
  readonly version = '';

  getAppDataDir(): string {
    const xdg = process.env.XDG_DATA_HOME;
    if (xdg) return path.join(xdg, 'MyApp');
    return path.join(process.env.HOME || '', '.local', 'share', 'MyApp');
  }

  setAutoStart(enabled: boolean): Promise<void> {
    const autostartDir = path.join(
      process.env.XDG_CONFIG_HOME || path.join(process.env.HOME || '', '.config'),
      'autostart'
    );
    const desktopFile = path.join(autostartDir, 'myapp.desktop');
    return enabled
      ? fs.promises.writeFile(desktopFile, this.generateDesktopEntry())
      : fs.promises.unlink(desktopFile).catch(() => {});
  }
}
```

### Factory

```typescript
// platform/factory.ts
export function createPlatformAdapter(): PlatformAdapter {
  switch (process.platform) {
    case 'win32': return new WindowsAdapter();
    case 'darwin': return new MacOSAdapter();
    case 'linux': return new LinuxAdapter();
    default:
      throw new Error(`Unsupported platform: ${process.platform}`);
  }
}

// Singleton
let instance: PlatformAdapter;
export function getPlatform(): PlatformAdapter {
  if (!instance) instance = createPlatformAdapter();
  return instance;
}
```

---

## Build Matrix

### Electron

| Target | Build Tool | Output | Code Signing |
|--------|-----------|--------|--------------|
| Windows (x64) | electron-builder | NSIS/MSI/AppX | EV Code Signing |
| macOS (x64+arm64) | electron-builder | DMG/PKG | Apple notarization |
| Linux (x64) | electron-builder | AppImage/deb/rpm | GPG (optional) |

```yaml
# electron-builder.yml
appId: com.example.myapp
productName: MyApp

mac:
  category: public.app-category.productivity
  hardenedRuntime: true
  entitlements: build/entitlements.mac.plist
  entitlementsInherit: build/entitlements.mac.plist
  target:
    - target: dmg
      arch: [x64, arm64]
    - target: zip
      arch: [x64, arm64]

win:
  target:
    - target: nsis
      arch: [x64]
    - target: msi
      arch: [x64]
  signingHashAlgorithms: [sha256]
  certificateFile: cert.pfx

linux:
  target:
    - target: AppImage
      arch: [x64]
    - target: deb
      arch: [x64]
    - target: rpm
      arch: [x64]
  category: Office
```

### Tauri

```json
{
  "tauri": {
    "bundle": {
      "targets": ["nsis", "dmg", "appimage", "deb"],
      "icon": [
        "icons/32x32.png",
        "icons/128x128.png",
        "icons/128x128@2x.png",
        "icons/icon.icns",
        "icons/icon.ico"
      ]
    }
  }
}
```

---

## Platform-Specific Code Organization

### Option 1: Platform Files (Recommended)

```
src/
├── app/
│   └── main.ts              # Platform-agnostic logic
├── platform/
│   ├── interface.ts          # Shared PlatformAdapter interface
│   ├── factory.ts            # Platform detection + instantiation
│   ├── win32/
│   │   ├── adapter.ts
│   │   ├── registry.ts
│   │   └── taskbar.ts
│   ├── darwin/
│   │   ├── adapter.ts
│   │   ├── dock.ts
│   │   └── menu.ts
│   └── linux/
│       ├── adapter.ts
│       ├── dbus.ts
│       └── autostart.ts
```


## UI Adaptation Strategies

### Electron: CSS Platform Detection

```css
/* Platform-specific styling */
.app-container {
  /* Common styles */
}

/* macOS: traffic light inset padding */
.platform-darwin .app-container {
  padding-top: 28px;
}

/* Windows: title bar height */
.platform-win32 .app-container {
  padding-top: 32px;
  /* Segoe UI font stack */
  font-family: 'Segoe UI', system-ui, sans-serif;
}

/* Linux: varies by DE — use system font */
.platform-linux .app-container {
  font-family: system-ui, sans-serif;
}
```

### Tauri: Platform Guards

```rust
#[tauri::command]
fn get_default_path() -> String {
    #[cfg(target_os = "windows")]
    { std::env::var("APPDATA").unwrap_or_default() }

    #[cfg(target_os = "macos")]
    { format!("{}/Library/Application Support", std::env::var("HOME").unwrap()) }

    #[cfg(target_os = "linux")]
    { format!("{}/.local/share", std::env::var("HOME").unwrap()) }
}
```

---

## Testing Across Platforms

### CI Matrix (GitHub Actions)

```yaml
strategy:
  matrix:
    os: [ubuntu-24.04, macos-14, windows-2025]
    include:
      - os: ubuntu-24.04
        test-command: xvfb-run npm test
      - os: macos-14
        test-command: npm test
      - os: windows-2025
        test-command: npm test

runs-on: ${{ matrix.os }}
```

**Platform-specific test concerns:**
- File path separators (`\` vs `/`)
- Line endings (CRLF vs LF)
- Environment variable names
- DPI scaling rendering tests
- System font rendering differences
- Permission models (sandbox on macOS, UAC on Windows)

---

## Decision Framework

| Factor | Electron | Tauri | React Native Desktop | Native (per-platform) |
|--------|----------|-------|---------------------|----------------------|
| Bundle size | 80-150 MB | 5-15 MB | 20-50 MB | 10-50 MB |
| Memory (idle) | 100-200 MB | 30-60 MB | 60-120 MB | 40-100 MB |
| Dev team skill | Web (JS/TS) | Web + Rust | React Native | Platform-specific |
| Native feel | Good (Chromium) | Very good (WebView) | Good (native widgets) | Excellent |
| OS API access | Full (via Node) | Full (via Rust) | Good (via bridges) | Complete |
| Build complexity | Low | Medium | Medium | High (3 codebases) |
| Hot reload | Yes (HMR) | Yes (Vite) | Yes (Metro) | Platform-dependent |
| App store ready | macOS (with care) | macOS (simpler) | Yes | Yes |
| Best for | Internal tools, IDEs | Consumer apps | Mobile-first desktop | Platform-exclusive |

---

## Anti-Patterns

| Anti-Pattern | Impact | Fix |
|--------------|--------|-----|
| `if (process.platform === 'win32')` scattered everywhere | Unmaintainable — 200+ conditionals across codebase | Platform Adapter pattern with single factory |
| Platform-specific code in renderer | Bloated bundles on all platforms | Tree-shake platform code or put in preload |
| Assuming `/` as path separator on Windows | File operations break | Use `path.join()`, `path.resolve()` always |
| Hardcoding platform assumptions in business logic | Logic breaks on new platform | Isolate platform concerns behind interface |
| Not testing on all platforms until release week | Showstopper bugs discovered too late | CI runs on all platforms on every PR |

---

## References

- [Electron Build Tools](https://www.electronjs.org/docs/latest/tutorial/application-distribution)
