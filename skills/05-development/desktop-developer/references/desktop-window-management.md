---
name: desktop-window-management
description: Production window management for desktop applications — multi-window architecture, frameless windows, DPI scaling, system tray, menu bar, focus management, and platform-specific window behaviors across Electron, Tauri, and WPF.
author: Sandeep Kumar Penchala
---

# Desktop Window Management

Window management is the most visible aspect of desktop application quality. Users notice immediately when windows flash, lose focus, render at the wrong DPI, or fail to restore their previous state. This reference covers window management across Electron, Tauri, and WPF.

---

## 1. Window Architecture Patterns

### 1.1 Single-Window

```
┌──────────────────────────────────────┐
│  Menu Bar                            │
├──────────────────────────────────────┤
│                                      │
│        Main Content Area             │
│                                      │
├──────────────────────────────────────┤
│  Status Bar                          │
└──────────────────────────────────────┘
```

Suitable for: Simple tools, settings panels, utilities with one primary view.

### 1.2 Multi-Window with Parent

```
┌─ Main Window ────────────────────────┐
│                                      │
│    ┌─ Settings ──────────────────┐   │
│    │                             │   │
│    └─────────────────────────────┘   │
│                                      │
└──────────────────────────────────────┘
```

Suitable for: Editors, IDEs, creative tools, apps with modal workflows.

### 1.3 Tray + Hidden Window

```
┌─────────────────┐
│  System Tray    │  ← Icon always visible
│  ┌───┐          │
│  │ 🏠 │          │  Click → show popup window
│  └───┘          │
└─────────────────┘
```

Suitable for: Clipboard managers, screenshot tools, VPN clients, music controllers.

## 2. Electron Window Management

### 2.1 Window State Persistence

```typescript
import windowStateKeeper from 'electron-window-state';

function createMainWindow(): BrowserWindow {
  // Load previous window state (position, size, maximized)
  const mainWindowState = windowStateKeeper({
    defaultWidth: 1200,
    defaultHeight: 800,
    file: 'main-window-state.json',
  });

  const win = new BrowserWindow({
    x: mainWindowState.x,
    y: mainWindowState.y,
    width: mainWindowState.width,
    height: mainWindowState.height,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      preload: join(__dirname, 'preload.js'),
      sandbox: true,
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  // Track changes
  mainWindowState.manage(win);

  return win;
}
```

### 2.2 Multi-Window Management

```typescript
// main.ts — window registry pattern
class WindowManager {
  private windows = new Map<string, BrowserWindow>();

  createWindow(id: string, options: Electron.BrowserWindowConstructorOptions): BrowserWindow {
    if (this.windows.has(id)) {
      const existing = this.windows.get(id)!;
      existing.focus();
      return existing;
    }

    const win = new BrowserWindow({
      ...options,
      parent: options.parent, // Attach to parent window
    });

    // Clean up on close
    win.on('closed', () => {
      this.windows.delete(id);
    });

    this.windows.set(id, win);
    return win;
  }

  getWindow(id: string): BrowserWindow | undefined {
    return this.windows.get(id);
  }

  closeAll(): void {
    for (const [id, win] of this.windows) {
      win.close();
    }
    this.windows.clear();
  }
}

export const windowManager = new WindowManager();

// Usage
ipcMain.handle('window:openSettings', () => {
  const mainWin = BrowserWindow.getFocusedWindow();
  windowManager.createWindow('settings', {
    width: 600, height: 500,
    parent: mainWin ?? undefined,
    modal: true,
    resizable: false,
  });
  return { success: true };
});
```

### 2.3 Frameless Window with Custom Title Bar

```typescript
const win = new BrowserWindow({
  titleBarStyle: 'hidden',          // macOS: hides title bar, keeps traffic lights
  // OR
  frame: false,                     // All platforms: completely frameless
  titleBarOverlay: {                // Windows/Linux: overlay controls
    color: '#2f3241',
    symbolColor: '#74b1be',
    height: 40,
  },
  webPreferences: { /* ... */ },
});
```

```css
/* Custom drag region in renderer */
.title-bar {
  -webkit-app-region: drag;
  height: 40px;
  display: flex;
  align-items: center;
  padding: 0 12px;
}

.title-bar button {
  -webkit-app-region: no-drag; /* Allow clicks on buttons */
}
```

### 2.4 System Tray

```typescript
import { Tray, Menu, nativeImage } from 'electron';

let tray: Tray | null = null;

app.whenReady().then(() => {
  const icon = nativeImage.createFromPath(join(__dirname, 'tray-icon.png'));
  tray = new Tray(icon.resize({ width: 16, height: 16 }));

  const contextMenu = Menu.buildFromTemplate([
    {
      label: 'Show App',
      click: () => mainWindow?.show(),
    },
    {
      label: 'Status: Connected',
      enabled: false,
    },
    { type: 'separator' },
    {
      label: 'Settings',
      click: () => { /* open settings */ },
    },
    {
      label: 'Quit',
      click: () => app.quit(),
    },
  ]);

  tray.setToolTip('MyApp — Connected');
  tray.setContextMenu(contextMenu);

  tray.on('click', () => {
    mainWindow?.isVisible() ? mainWindow.hide() : mainWindow.show();
  });
});
```

### 2.5 macOS Menu Bar App

```typescript
// Hide dock icon, show only in menu bar
app.dock?.hide();

// Or hide from dock entirely:
// In package.json: "LSUIElement": true

// Create a popover-style window
const win = new BrowserWindow({
  width: 320,
  height: 480,
  show: false,
  frame: false,
  resizable: false,
  skipTaskbar: true,
  alwaysOnTop: true,
  webPreferences: { /* ... */ },
});

tray.on('click', () => {
  // Position window under tray icon
  const trayBounds = tray.getBounds();
  const windowBounds = win.getBounds();

  const x = Math.round(trayBounds.x + trayBounds.width / 2 - windowBounds.width / 2);
  const y = Math.round(trayBounds.y + trayBounds.height);

  win.setPosition(x, y);
  win.isVisible() ? win.hide() : win.show();
});
```

## 3. DPI Scaling & Multi-Monitor

### 3.1 Per-Monitor DPI Awareness (Windows)

```typescript
// main.ts — Windows DPI awareness
if (process.platform === 'win32') {
  app.commandLine.appendSwitch('high-dpi-support', '1');
  app.commandLine.appendSwitch('force-device-scale-factor', '1');
}

// In the renderer, listen for DPI changes
window.matchMedia('screen and (resolution: 2dppx)').addEventListener('change', (e) => {
  console.log('DPI changed:', e.matches ? '2x' : '1x');
  // Re-render at new DPI
});
```

```css
/* Use CSS logical pixels — they auto-scale with DPI */
:root {
  /* Good: relative units */
  --spacing: 1rem;
  --sidebar-width: 16rem;

  /* Avoid: hardcoded pixels that break on HiDPI */
  /* --spacing: 16px; ← renders as 32px on 2x display */
}

/* Use SVG for icons — they scale to any DPI */
.icon {
  background-image: url('./icon.svg');
  width: 1.5rem;
  height: 1.5rem;
}
```

### 3.2 Display Change Handling

```typescript
import { screen } from 'electron';

screen.on('display-added', (event, newDisplay) => {
  console.log('New display:', newDisplay.scaleFactor, newDisplay.bounds);
  // Reposition windows if they're off-screen
  repositionOffScreenWindows();
});

screen.on('display-removed', () => {
  // Move windows to remaining display
  repositionOffScreenWindows();
});

screen.on('display-metrics-changed', () => {
  // DPI or resolution changed
  mainWindow?.webContents.send('dpi:changed');
});

function repositionOffScreenWindows(): void {
  const displays = screen.getAllDisplays();
  for (const win of BrowserWindow.getAllWindows()) {
    const bounds = win.getBounds();
    const isOnScreen = displays.some(d =>
      bounds.x >= d.bounds.x &&
      bounds.y >= d.bounds.y &&
      bounds.x + bounds.width <= d.bounds.x + d.bounds.width &&
      bounds.y + bounds.height <= d.bounds.y + d.bounds.height
    );

    if (!isOnScreen) {
      // Move to primary display
      const primaryDisplay = screen.getPrimaryDisplay();
      win.setPosition(
        primaryDisplay.workArea.x + 50,
        primaryDisplay.workArea.y + 50
      );
    }
  }
}
```

## 4. Tauri Window Management

### 4.1 Window Configuration

```json
// tauri.conf.json
{
  "app": {
    "windows": [
      {
        "label": "main",
        "title": "MyApp",
        "width": 1200,
        "height": 800,
        "minWidth": 800,
        "minHeight": 600,
        "resizable": true,
        "decorations": true,
        "center": true,
        "visible": true
      }
    ]
  }
}
```

### 4.2 Multi-Window in Tauri

```rust
// Rust backend — create windows programmatically
use tauri::Manager;

#[tauri::command]
fn open_settings(app: tauri::AppHandle) -> Result<(), String> {
    let settings_window = tauri::WebviewWindowBuilder::new(
        &app,
        "settings",
        tauri::WebviewUrl::App("settings.html".into()),
    )
    .title("Settings")
    .inner_size(600.0, 500.0)
    .resizable(false)
    .build()
    .map_err(|e| e.to_string())?;

    Ok(())
}
```

```typescript
// Frontend — invoke from renderer
import { invoke } from '@tauri-apps/api/core';
await invoke('open_settings');
```

### 4.3 Tray in Tauri

```rust
use tauri::tray::{TrayIconBuilder, MouseButton, MouseButtonState, TrayIconEvent};

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let tray = TrayIconBuilder::new()
                .icon(app.default_window_icon().unwrap().clone())
                .tooltip("MyApp")
                .on_tray_icon_event(|tray, event| {
                    if let TrayIconEvent::Click {
                        button: MouseButton::Left,
                        button_state: MouseButtonState::Up,
                        ..
                    } = event
                    {
                        let app = tray.app_handle();
                        if let Some(window) = app.get_webview_window("main") {
                            let _ = window.show();
                            let _ = window.set_focus();
                        }
                    }
                })
                .build(app)?;

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error");
}
```

## 5. WPF Window Management

### 5.1 Window State Persistence

```csharp
public partial class MainWindow : Window
{
    private const string StateKey = "MainWindowState";

    public MainWindow()
    {
        InitializeComponent();
        this.SourceInitialized += OnSourceInitialized;
        this.Closing += OnClosing;
    }

    private void OnSourceInitialized(object sender, EventArgs e)
    {
        // Restore previous state
        var settings = Properties.Settings.Default;
        if (!string.IsNullOrEmpty(settings.WindowPlacement))
        {
            // Restore using WINDOWPLACEMENT structure
            var wp = JsonSerializer.Deserialize<WindowPlacement>(settings.WindowPlacement);
            // Apply placement...
        }
    }

    private void OnClosing(object sender, CancelEventArgs e)
    {
        // Save state
        var settings = Properties.Settings.Default;
        settings.WindowPlacement = JsonSerializer.Serialize(GetWindowPlacement());
        settings.Save();
    }
}
```

### 5.2 Multi-Window Owner Pattern

```csharp
private void OpenSettings_Click(object sender, RoutedEventArgs e)
{
    var settingsWindow = new SettingsWindow
    {
        Owner = this,  // Modal to main window
        WindowStartupLocation = WindowStartupLocation.CenterOwner
    };
    settingsWindow.ShowDialog(); // Modal — blocks main window
}
```

## 6. Focus & Z-Order Management

### 6.1 Preventing Focus Stealing

```typescript
// DON'T: steal focus on notification
const notifyWin = new BrowserWindow({ /* ... */ });
notifyWin.show(); // BAD: steals focus from user's current app

// DO: show without stealing focus
notifyWin.showInactive(); // Shows window but doesn't activate

// DO: use Notification API instead of a window
new Notification({ title: 'Update Ready', body: 'Restart to apply' }).show();
```

### 6.2 Always-On-Top Windows

```typescript
const floatingToolbar = new BrowserWindow({
  width: 300,
  height: 60,
  alwaysOnTop: true,        // Stays above other windows
  skipTaskbar: true,        // Not shown in taskbar
  frame: false,
  focusable: false,         // Doesn't steal keyboard focus
  transparent: true,
  resizable: false,
});
```

## 7. Power State Handling

```typescript
import { powerMonitor } from 'electron';

powerMonitor.on('suspend', () => {
  console.log('System going to sleep');
  // Persist critical state immediately
  saveAllDirtyDocuments();
  // Close WebSocket connections
  disconnectServices();
});

powerMonitor.on('resume', () => {
  console.log('System woke from sleep');
  // Reconnect services
  reconnectServices();
  // Check for updates (might have been missed)
  autoUpdater.checkForUpdates();
});

powerMonitor.on('on-battery', () => {
  // Reduce polling frequency
  reduceBackgroundActivity();
});

powerMonitor.on('on-ac', () => {
  // Resume normal activity
  restoreBackgroundActivity();
});

// Lock screen detection
powerMonitor.on('lock-screen', () => {
  // Hide sensitive information
  mainWindow?.webContents.send('screen:locked');
});

powerMonitor.on('unlock-screen', () => {
  mainWindow?.webContents.send('screen:unlocked');
});
```

## 8. Window Lifecycle Checklist

- [ ] Window state (position, size, maximized, fullscreen) persisted and restored
- [ ] Minimum/maximum window sizes enforced
- [ ] Multi-window: parent-child relationships maintained
- [ ] Windows repositioned if display configuration changes (monitor unplugged)
- [ ] Frameless windows have draggable regions (`-webkit-app-region: drag`)
- [ ] Tray icon provides context menu and click behavior
- [ ] macOS: app stays running when last window closes (standard behavior)
- [ ] Windows/Linux: app quits when last window closes
- [ ] DPI changes handled: icons re-rendered at native resolution
- [ ] Focus not stolen by background windows or notifications
- [ ] Power state transitions handled: sleep → persist, resume → reconnect
