## Core Workflow

<!-- QUICK: 30s -- scan phase titles to understand the process -->

### Phase 1 (~20 min): Framework Selection & Architecture
1. **Run the framework decision tree** (see Decision Trees). Document: target platforms, performance budget (RAM, CPU, disk), team skills (JS/Rust/C#/C++), and app type (document editor, chat, system utility, game launcher).
2. **Project scaffold**: Framework CLI — `npm init electron-app@latest`, `npm create tauri-app@latest`, `dotnet new maui`, or CMake-based Qt project.
3. **IPC architecture**: Define IPC channels and message schemas BEFORE writing handlers. Each channel: name, direction (main↔renderer), payload schema, error responses. Document in `ipc-contract.md`.
4. **Security baseline**: Electron: `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`, structured `contextBridge` API. Tauri: command allowlist, capability-based permissions. WPF: ClickOnce security. MAUI: entitlement restrictions.
5. **Build pipeline skeleton**: GitHub Actions with matrix (macos-13, macos-14, windows-2022, ubuntu-22.04). Code signing configured (certificates as secrets, never committed).

### Phase 2 (~30 min): Window & Process Architecture
1. **Main process design**: Lifespan — `app.whenReady()`, `app.on('window-all-closed')`, `app.on('before-quit')`. Platform-specific quit: macOS keeps app alive after last window closes; Windows/Linux quit.
2. **Window creation**: `BrowserWindow` with size, position, min/max constraints. Persist window state via `electron-window-state`. Restore on next launch.
3. **Renderer bootstrap**: SPA (React/Vue/Svelte) loaded from local file (`loadFile`) or dev server (`loadURL`). CSP via `session.defaultSession.webRequest.onHeadersReceived`.
4. **Preload script**: Structured `contextBridge.exposeInMainWorld('electronAPI', { ... })` with typed methods. Validate inputs before IPC. No `require('electron')` in renderer.
5. **Tray/menu bar**: Platform-specific — macOS menu bar app (no dock icon), Windows system tray with context menu, Linux `libappindicator`. Handle click, right-click, notification badges.

### Phase 3 (~35 min): Core Feature Implementation
<!-- DEEP: 10+min -->
1. **IPC handlers**: `ipcMain.handle('channel', async (event, ...args) => { ... })` for request-response. `ipcMain.on` for events. Validate all arguments with Zod/schema. Return structured errors: `{ error?: { code, message }, data }`.
2. **File system**: Use `dialog.showOpenDialog()` / `showSaveDialog()` — never construct paths from renderer input. Use `app.getPath('userData')` for app storage. Respect sandbox restrictions.
3. **Native dialogs**: `dialog.showMessageBox()`, `dialog.showErrorBox()`. Platform-native. Avoid custom HTML dialogs that break keyboard nav and screen readers.
4. **OS integration**: Notifications (`Notification` API or Tauri plugin), file associations (register in builder config), custom protocols (`app.setAsDefaultProtocolClient('myapp')`), global shortcuts (`globalShortcut.register`).
5. **Offline/PWA patterns**: Cache static assets. Queue operations when offline, replay on reconnect. `navigator.onLine` is unreliable — ping backend or check DNS.
6. **Crash reporting**: `crashReporter.start()` with submitURL to Sentry. Include: app version, OS version, Electron/Tauri version, GPU info, last 50 log lines. Minidumps for native crashes.

### Phase 4 (~25 min): Auto-Update Pipeline
1. **Provider selection**: `electron-updater` with S3, GitHub Releases, or generic HTTP. Tauri updater with custom endpoint. Sparkle (macOS native) for non-Electron apps.
2. **Update server**: Static JSON manifest: `latest.yml` (Windows), `latest-mac.yml` (macOS), `latest-linux.yml` (Linux). Contains: version, files (with SHA512), path, release date, release notes URL.
3. **Client integration**: Check on app start (debounce 15s after launch). Download in background with progress. Notify user when ready. Support "Install on quit" and "Install now and restart."
4. **Failure handling**: Signature verification fails → delete download, retry later. Disk full → notify user, don't retry silently. Download interrupted → resume from byte offset. New version crashes on launch → auto-rollback.
5. **Differential updates**: Ship only changed files. `electron-updater` supports blockmap-based diffs. Reduces update from 180MB to 5-30MB.

### Phase 5 (~30 min): Installer & Distribution
1. **electron-builder config**: Targets: `nsis` (Windows), `dmg` + `zip` (macOS), `AppImage` + `deb` (Linux). Per-platform: install directory, shortcuts, file associations, uninstaller.
2. **Code signing**: macOS: `CSC_LINK` (base64 p12), `CSC_KEY_PASSWORD`, `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD`, `APPLE_TEAM_ID`. Notarize with `notarytool`. Windows: `CSC_LINK`, `CSC_KEY_PASSWORD`. EV certificate for instant SmartScreen trust.
3. **Notarization**: Staple ticket (`xcrun stapler staple`). Verify with `spctl -a -v`. Gatekeeper requires notarization outside Mac App Store.
4. **CI/CD**: GitHub Actions matrix: `macos-13` (x64), `macos-14` (arm64), `windows-2022`, `ubuntu-22.04`. Signing secrets in GitHub Secrets. Upload artifacts to release.
5. **Distribution channels**: Direct download (GitHub Releases), Mac App Store (sandboxed), Microsoft Store (MSIX), Snap/Flatpak (Linux), enterprise MDM (Intune/Jamf).

### Phase 6 (~20 min): Testing
1. **Unit tests**: Vitest/Jest for main process logic. Spectron/Playwright for renderer. Tauri: Rust `#[cfg(test)]` for backend.
2. **Integration tests**: IPC handler tests — mock `ipcMain`, send messages, assert responses. File system tests with temp dirs. Auto-update tests with local HTTP server.
3. **E2E tests**: Playwright with `electron.launch()`. Test: launch, window creation, menu interactions, file dialogs, tray, quit/reopen, update flow. Run against built artifacts.
4. **Cross-platform matrix**: Run E2E on macOS, Windows, Linux in CI. GPU differences cause platform-specific rendering bugs. Test with `--disable-gpu` on all platforms.
5. **Performance**: Measure cold start, warm start, memory after idle (5 min), memory under load, CPU idle, disk I/O. Set budgets and alert on regression.

### Framework-Specific Code Patterns

**Electron Preload Security Pattern (TypeScript)**:

```typescript
// preload.ts — The ONLY file importing from 'electron'
// NEVER expose ipcRenderer directly. Expose typed, validated functions.
import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  getAppVersion: (): Promise<string> =>
    ipcRenderer.invoke('app:get-version'),

  openFile: async (): Promise<{ filePath: string; content: string } | null> => {
    const result = await ipcRenderer.invoke('dialog:open-file');
    if (result?.canceled || !result?.filePaths?.[0]) return null;
    const content = await ipcRenderer.invoke('fs:read-file', result.filePaths[0]);
    return { filePath: result.filePaths[0], content };
  },

  // NEVER expose generic IPC: ipcRenderer, ipcRenderer.on, ipcRenderer.send
  // Each function is a specific, validated IPC channel
});
```

**Tauri Command with Validation (Rust)**:

```rust
// src-tauri/src/commands.rs
use tauri::State;
use std::sync::Mutex;

#[tauri::command]
fn read_config(key: String, config: State<'_, Mutex<AppConfig>>) -> Result<String, String> {
    // Validate input — never trust frontend-provided strings blindly
    if key.len() > 128 || !key.chars().all(|c| c.is_alphanumeric() || c == '_') {
        return Err(format!("Invalid config key: {key}"));
    }
    let cfg = config.lock().map_err(|e| e.to_string())?;
    cfg.get(&key).cloned().ok_or_else(|| format!("Key not found: {key}"))
}
```

**WPF MVVM ViewModel (C#)**:

```csharp
// MainViewModel.cs — INotifyPropertyChanged for data binding
public class MainViewModel : INotifyPropertyChanged
{
    private string _status = "Ready";
    public string Status
    {
        get => _status;
        set { _status = value; OnPropertyChanged(); }
    }

    public ICommand LoadDataCommand { get; }

    public MainViewModel()
    {
        LoadDataCommand = new RelayCommand(async () =>
        {
            Status = "Loading...";
            await Task.Run(() => LoadData()); // Off UI thread
            Status = "Ready";
        });
    }

    public event PropertyChangedEventHandler? PropertyChanged;
    protected void OnPropertyChanged([CallerMemberName] string? name = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}
```

**electron-builder Configuration (JSON)**:

```json
{
  "appId": "com.company.myapp",
  "productName": "MyApp",
  "directories": { "output": "dist" },
  "mac": {
    "category": "public.app-category.productivity",
    "hardenedRuntime": true,
    "entitlements": "build/entitlements.mac.plist",
    "notarize": { "teamId": "YOUR_TEAM_ID" }
  },
  "win": {
    "target": [{ "target": "nsis", "arch": ["x64", "arm64"] }],
    "sign": "./scripts/sign-windows.cmd"
  },
  "nsis": { "oneClick": false, "allowToChangeInstallationDirectory": true }
}
```

**WPF XAML Window with Data Binding (XML)**:

```xml
<!-- MainWindow.xaml -->
<Window x:Class="MyApp.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="MyApp" Height="450" Width="800"
        DataContext="{Binding MainViewModel, Source={StaticResource Locator}}">
    <Grid>
        <TextBlock Text="{Binding Status}" HorizontalAlignment="Center" VerticalAlignment="Center"/>
        <Button Content="Load Data" Command="{Binding LoadDataCommand}" VerticalAlignment="Bottom"/>
    </Grid>
</Window>
```

**CI Sign & Notarize (Bash)**:

```bash
#!/usr/bin/env bash
set -euo pipefail

# macOS code sign + notarize
if [[ "$(uname)" == "Darwin" ]]; then
  # Sign all native binaries
  find dist/mac-arm64/MyApp.app -type f -name '*.dylib' -o -name '*.node' | while read -r file; do
    codesign --force --options runtime --sign "$APPLE_DEVELOPER_ID" "$file"
  done
  codesign --force --options runtime --sign "$APPLE_DEVELOPER_ID" dist/mac-arm64/MyApp.app

  # Notarize and staple
  ditto -c -k --keepParent dist/mac-arm64/MyApp.app dist/MyApp.zip
  xcrun notarytool submit dist/MyApp.zip --apple-id "$APPLE_ID" --team-id "$APPLE_TEAM_ID" \
    --password "$APPLE_APP_PASSWORD" --wait
  xcrun stapler staple dist/mac-arm64/MyApp.app
  spctl -a -v dist/mac-arm64/MyApp.app
fi

# Windows Authenticode signing
if [[ "$(uname -o 2>/dev/null)" == "Msys" || "$RUNNER_OS" == "Windows" ]]; then
  signtool sign /fd SHA256 /a /f certificate.pfx /p "$CSC_KEY_PASSWORD" dist/MyApp.exe
  signtool verify /pa dist/MyApp.exe
fi
```
