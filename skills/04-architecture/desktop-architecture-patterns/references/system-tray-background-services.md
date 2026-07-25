# System Tray & Background Services — Architecture Patterns

## Overview

System tray applications and background services are the "always-on" face of desktop apps. They must run with minimal resources, survive OS sleep/wake cycles, and integrate seamlessly with platform notification systems. Getting this wrong results in excessive battery drain, OS-level kill events, and frustrated users who can't find your app.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────┐
│                  SYSTEM TRAY                      │
│  ┌────────────────────────────────────────────┐  │
│  │  Icon (16x16 / 22x22 platform-specific)    │  │
│  │  Context Menu (right-click)                │  │
│  │  Left-click Action (toggle visibility)     │  │
│  │  Tooltip (status text)                     │  │
│  └────────────────┬───────────────────────────┘  │
│                   │                               │
│  ┌────────────────▼───────────────────────────┐  │
│  │          BACKGROUND SERVICE                 │  │
│  │  ┌───────────┐  ┌──────────┐  ┌──────────┐ │  │
│  │  │ Scheduler │  │ Watchers │  │ Sync     │ │  │
│  │  │ (cron-    │  │ (fs,     │  │ Engine   │ │  │
│  │  │  style)   │  │  network)│  │ (periodic│ │  │
│  │  └───────────┘  └──────────┘  └──────────┘ │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

---

## Platform Implementations

### Electron System Tray

```typescript
import { Tray, Menu, nativeImage, app } from 'electron';

let tray: Tray | null = null;

app.whenReady().then(() => {
  // Create tray — must be 16x16 (Windows), 22x22 (macOS template), or provide @2x/@3x
  const icon = nativeImage.createFromPath(
    path.join(__dirname, 'assets', process.platform === 'darwin' ? 'trayTemplate.png' : 'tray.ico')
  );
  tray = new Tray(icon.resize({ width: 16, height: 16 }));

  // macOS: Template images auto-adapt to dark/light mode
  if (process.platform === 'darwin') {
    icon.setTemplateImage(true);
  }

  tray.setToolTip('MyApp — Synced');
  tray.setContextMenu(Menu.buildFromTemplate([
    { label: 'Show Window', click: () => mainWindow?.show() },
    { label: 'Sync Now', click: () => syncService.syncNow() },
    { type: 'separator' },
    {
      label: 'Status: Connected',
      enabled: false
    },
    { type: 'separator' },
    { label: 'Quit', click: () => app.quit() }
  ]));

  // Left-click behavior
  tray.on('click', () => {
    if (mainWindow?.isVisible()) {
      mainWindow.focus();
    } else {
      mainWindow?.show();
    }
  });
});

// Prevent app from quitting when window closes
app.on('window-all-closed', (event) => {
  if (process.platform !== 'darwin') {
    // On Windows/Linux, keep running in tray
    event.preventDefault();
  }
});
```

**Critical: Windows tray restoration on Explorer restart:**
```typescript
// Windows Explorer restart kills tray icons — must re-create
app.on('ready', () => {
  createTray();
  // Re-create tray if it gets destroyed (Explorer restart on Windows)
  tray?.on('balloon-click', () => { /* handled by OS */ });
});

if (process.platform === 'win32') {
  setInterval(() => {
    if (tray?.isDestroyed()) {
      createTray();
    }
  }, 10_000);
}
```


## Background Service Patterns

### Pattern 1: Periodic Sync Scheduler

```typescript
class SyncScheduler {
  private timer: NodeJS.Timeout | null = null;
  private isRunning = false;

  constructor(
    private intervalMs: number,
    private task: () => Promise<void>,
    private onError: (err: Error) => void
  ) {}

  start() {
    // Immediate first run
    this.runTask();
    // Then periodic
    this.timer = setInterval(() => this.runTask(), this.intervalMs);
  }

  private async runTask() {
    if (this.isRunning) return; // Skip if previous run still in progress
    this.isRunning = true;
    try {
      await this.task();
    } catch (err) {
      this.onError(err as Error);
    } finally {
      this.isRunning = false;
    }
  }

  stop() {
    if (this.timer) clearInterval(this.timer);
  }

  changeInterval(newMs: number) {
    this.stop();
    this.intervalMs = newMs;
    this.start();
  }
}
```

### Pattern 2: File System Watcher Service

```typescript
import { watch } from 'chokidar';

class FileWatcherService {
  private watchers = new Map<string, FSWatcher>();

  watchDirectory(dirPath: string, onChanged: (path: string) => void) {
    const watcher = watch(dirPath, {
      ignored: /(^|[/\\])\./,  // Ignore dotfiles
      persistent: true,
      ignoreInitial: true,     // Don't fire for existing files
      awaitWriteFinish: {
        stabilityThreshold: 500, // Wait 500ms after last write
        pollInterval: 100
      }
    });

    watcher.on('change', onChanged);
    watcher.on('error', (err) => console.error('Watcher error:', err));

    this.watchers.set(dirPath, watcher);
    return () => { watcher.close(); this.watchers.delete(dirPath); };
  }

  dispose() {
    for (const [path, watcher] of this.watchers) {
      watcher.close();
    }
    this.watchers.clear();
  }
}
```

### Pattern 3: Network Reachability Monitor

```typescript
class NetworkMonitor {
  private isOnline = true;
  private listeners: Set<(online: boolean) => void> = new Set();

  constructor() {
    // Electron online/offline events
    const { net } = require('electron');
    net.on('online', () => this.setOnline(true));
    net.on('offline', () => this.setOnline(false));

    // Also check on wake from sleep
    const { powerMonitor } = require('electron');
    powerMonitor.on('resume', () => {
      this.setOnline(net.isOnline());
    });
  }

  get online() { return this.isOnline; }

  onChange(cb: (online: boolean) => void) {
    this.listeners.add(cb);
    return () => this.listeners.delete(cb);
  }

  private setOnline(value: boolean) {
    if (this.isOnline === value) return;
    this.isOnline = value;
    for (const cb of this.listeners) cb(value);
  }
}
```

---

## Power Management Integration

```typescript
import { powerMonitor, powerSaveBlocker } from 'electron';

// Prevent system sleep during critical operations
let blockerId: number | null = null;

async function performCriticalSync() {
  // Prevent sleep during sync
  blockerId = powerSaveBlocker.start('prevent-app-suspension');

  try {
    await syncService.fullSync();
  } finally {
    if (blockerId !== null) {
      powerSaveBlocker.stop(blockerId);
      blockerId = null;
    }
  }
}

// Pause non-critical operations when on battery
powerMonitor.on('on-battery', () => {
  syncScheduler.changeInterval(5 * 60 * 1000); // Every 5 min on battery
  fileWatcherService.dispose();                 // Stop watching
});

powerMonitor.on('on-ac', () => {
  syncScheduler.changeInterval(30 * 1000);      // Every 30s on AC
  fileWatcherService.watchDirectory(userDir, handleChange);
});

// Handle sleep/wake
powerMonitor.on('suspend', () => {
  syncScheduler.stop();
  db.close(); // Release locks before sleep
});

powerMonitor.on('resume', () => {
  db.open();
  syncScheduler.start();
  syncService.syncNow(); // Sync immediately on wake
});
```

---

## Notification Architecture

```
┌─────────────────────┐
│   Background Service │
│                     │
│  Event Detected     │
│       │             │
│       ▼             │
│  Notification       │     ┌──────────────────┐
│  Manager            │────►│ OS Notification  │
│  ┌───────────────┐  │     │ Center           │
│  │ Rate Limiter  │  │     └────────┬─────────┘
│  │ Coalescer     │  │              │ click
│  │ Sound Policy  │  │     ┌────────▼─────────┐
│  └───────────────┘  │     │ Main Window       │
└─────────────────────┘     └──────────────────┘
```

```typescript
import { Notification } from 'electron';

```

---

## Tauri Background Services

```rust
fn setup_background(app: &tauri::AppHandle) {
    let handle = app.clone();

    tauri::async_runtime::spawn(async move {
        let mut ticker = interval(Duration::from_secs(30));

        loop {
            ticker.tick().await;

            // Perform background work
            if let Err(e) = sync_engine::sync(&handle).await {
                eprintln!("Sync error: {}", e);
            }

            // Update tray tooltip
            let status = if sync_engine::is_connected(&handle) {
                "Connected"
            } else {
                "Offline"
            };
            let _ = handle.tray_handle().set_tooltip(&format!("MyApp — {}", status));
        }
    });
}
```

---

## Anti-Patterns

| Anti-Pattern | Impact | Fix |
|--------------|--------|-----|
| No tray re-creation on Explorer restart (Windows) | Tray icon disappears, app unreachable | Re-create tray on timer or listen for `app.on('ready')` |
| Blocking UI thread in tray click handler | Tray menu freezes, app appears hung | Async operations only in click handlers |
| Background sync without power monitoring | Drains laptop battery in 2 hours | Throttle on battery, pause watchers, use `powerSaveBlocker` only when essential |
| Notifications without rate limiting | 500 notifications in 10 seconds — user uninstalls | Per-category cooldown, coalescing |
| Spinning event loop when idle | 1-2% CPU constantly for "do-nothing" tray app | Use event-driven triggers, not polling; sleep between checks |

---

## Platform Quick Reference

| Feature | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Tray icon size | 16x16 ICO | 18x18/36x36 PNG (template) | 22x22 PNG (varies by DE) |
| Background-only | `skipTaskbar: true` | `LSUIElement = YES` | `skipTaskbar: true` |
| Auto-start | Registry `HKCU\...\Run` | LaunchAgent plist | `~/.config/autostart/*.desktop` |
| Sleep detection | `powerMonitor` | `powerMonitor` + `NSWorkspace` | `powerMonitor` (limited) |
| Notification API | `Notification` (native) | `UserNotification` | `Notification` (via libnotify) |

---

## References

- [Electron Tray Docs](https://www.electronjs.org/docs/latest/api/tray)
- [Electron Power Monitor](https://www.electronjs.org/docs/latest/api/power-monitor)
- [macOS LSUIElement](https://developer.apple.com/documentation/bundleresources/information_property_list/lsuielement)
- See also: [desktop-ipc-architecture.md](desktop-ipc-architecture.md)
