---
name: electron-architecture-patterns
description: Production-grade Electron architecture — process model, preload security, CSP configuration, crash reporting, OS integration, and performance optimization patterns for desktop applications.
author: Sandeep Kumar Penchala
---

# Electron Architecture Patterns

A definitive reference for architecting secure, performant, and maintainable Electron applications. Covers the process model, security boundaries, preload patterns, Content Security Policy, crash reporting, OS integration, and performance optimization.

---

## 1. Process Model Deep Dive

### 1.1 The Three-Process Architecture

```
┌────────────────────────────────────────────────┐
│                 MAIN PROCESS                     │
│  • Node.js runtime (full OS access)              │
│  • Creates and manages BrowserWindows            │
│  • app lifecycle (ready, quit, activate)        │
│  • ipcMain handlers                              │
│  • Menu, Tray, Notifications, globalShortcut    │
│  • autoUpdater, crashReporter                    │
│  • Runs: exactly ONE instance                     │
└──────────────┬─────────────────────────────────┘
               │ IPC (via contextBridge)
┌──────────────▼─────────────────────────────────┐
│              RENDERER PROCESS                    │
│  • Chromium rendering engine                     │
│  • NO Node.js (nodeIntegration: false)          │
│  • Sandboxed (sandbox: true)                     │
│  • Can only access APIs exposed via preload     │
│  • Runs: ONE per BrowserWindow/BrowserView      │
│  • Web APIs: DOM, canvas, WebGL, fetch          │
└──────────────┬─────────────────────────────────┘
               │ MessagePort / SharedArrayBuffer
┌──────────────▼─────────────────────────────────┐
│           UTILITY PROCESS (optional)              │
│  • child_process.fork() or utilityProcess       │
│  • CPU-intensive work (image processing, PDF)   │
│  • Crash isolation — doesn't take down app      │
│  • No renderer access — pure computation        │
└────────────────────────────────────────────────┘
```

### 1.2 Main Process Responsibilities

The main process is the **only** process with OS privileges. It must:

- Create and destroy windows (`new BrowserWindow()`, `win.close()`)
- Manage the application lifecycle (`app.whenReady()`, `app.on('window-all-closed')`, `app.on('before-quit')`)
- Handle IPC requests from renderers (`ipcMain.handle()`)
- Push events to renderers (`webContents.send()`)
- Access system APIs: file dialogs, notifications, tray, menu, global shortcuts
- Manage auto-updates (`autoUpdater.checkForUpdates()`)
- Report crashes (`crashReporter.start()`)

```typescript
// main.ts — canonical main process entry point
import { app, BrowserWindow, ipcMain } from 'electron';
import { join } from 'path';

let mainWindow: BrowserWindow | null = null;

function createWindow(): void {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      preload: join(__dirname, 'preload.js'),
      sandbox: true,
      contextIsolation: true,
      nodeIntegration: false,
      webSecurity: true,
    },
  });

  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// Safety net for unhandled rejections in IPC handlers
process.on('unhandledRejection', (reason) => {
  console.error('Unhandled rejection in main process:', reason);
  // Send to crash reporter
});
```

### 1.3 Renderer Process Constraints

The renderer runs in a **sandboxed** Chromium environment. It has:

- **NO** `require()` — cannot load Node.js modules
- **NO** `fs`, `child_process`, or `os` modules
- **NO** direct access to Electron APIs (`ipcRenderer`, `remote`, `shell`)
- **YES** access to standard web APIs: `fetch`, `WebSocket`, `localStorage`, `IndexedDB`, `WebGL`, `Canvas`
- **YES** access to APIs exposed via `contextBridge.exposeInMainWorld()`

## 2. Preload Security Patterns

### 2.1 Canonical Preload Shape

The preload script is the ONLY file that imports from `electron`. It acts as a security gateway:

```typescript
// preload.ts
import { contextBridge, ipcRenderer } from 'electron';

export interface ElectronAPI {
  // File operations
  saveFile: (content: string, defaultName?: string) => Promise<{ success: boolean; path?: string; error?: string }>;
  openFile: () => Promise<{ success: boolean; content?: string; path?: string; error?: string }>;

  // App info
  getAppVersion: () => Promise<string>;
  getPlatform: () => string;

  // Update events (main → renderer)
  onUpdateAvailable: (callback: (info: UpdateInfo) => void) => () => void;
  onUpdateDownloaded: (callback: (info: UpdateInfo) => void) => () => void;

  // Window controls
  minimizeWindow: () => void;
  maximizeWindow: () => void;
  closeWindow: () => void;
}

interface UpdateInfo {
  version: string;
  releaseDate: string;
  releaseNotes: string;
}

contextBridge.exposeInMainWorld('electronAPI', {
  saveFile: (content: string, defaultName?: string) =>
    ipcRenderer.invoke('file:save', content, defaultName),

  openFile: () =>
    ipcRenderer.invoke('file:open'),

  getAppVersion: () =>
    ipcRenderer.invoke('app:getVersion'),

  getPlatform: () => process.platform,

  onUpdateAvailable: (callback: (info: UpdateInfo) => void) => {
    const handler = (_event: Electron.IpcRendererEvent, info: UpdateInfo) => callback(info);
    ipcRenderer.on('update:available', handler);
    return () => ipcRenderer.removeListener('update:available', handler);
  },

  onUpdateDownloaded: (callback: (info: UpdateInfo) => void) => {
    const handler = (_event: Electron.IpcRendererEvent, info: UpdateInfo) => callback(info);
    ipcRenderer.on('update:downloaded', handler);
    return () => ipcRenderer.removeListener('update:downloaded', handler);
  },

  minimizeWindow: () => ipcRenderer.invoke('window:minimize'),
  maximizeWindow: () => ipcRenderer.invoke('window:maximize'),
  closeWindow: () => ipcRenderer.invoke('window:close'),
} satisfies ElectronAPI);
```

### 2.2 Security Rules for Preload Scripts

1. **Only expose what the renderer NEEDS.** Every function in the API is an attack surface entry point.
2. **Validate ALL inputs** before forwarding to IPC. Use Zod or manual type guards.
3. **Never expose raw `ipcRenderer`.** Always wrap in typed functions with validation.
4. **Return cleanup functions for event listeners.** Prevents memory leaks when components unmount.
5. **Never expose `shell.openExternal` with unsanitized URLs.** Validate URL protocols: only allow `https:` and `mailto:`.

### 2.3 Type-Safe Renderer Usage

```typescript
// renderer/src/hooks/useElectronAPI.ts
declare global {
  interface Window {
    electronAPI: import('../../preload').ElectronAPI;
  }
}

export function useSaveFile() {
  return async (content: string, defaultName?: string) => {
    try {
      const result = await window.electronAPI.saveFile(content, defaultName);
      if (!result.success) {
        throw new Error(result.error ?? 'Save failed');
      }
      return result.path;
    } catch (err) {
      console.error('Save failed:', err);
      throw err;
    }
  };
}
```

## 3. Content Security Policy (CSP)

### 3.1 Production CSP Configuration

```typescript
// main.ts — set CSP headers
app.whenReady().then(() => {
  session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        'Content-Security-Policy': [
          [
            "default-src 'self'",
            "script-src 'self'",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data: https:",
            "font-src 'self' data:",
            "connect-src 'self' https://api.example.com",
            "frame-src 'none'",
            "object-src 'none'",
          ].join('; '),
        ],
      },
    });
  });
});
```

### 3.2 CSP Testing

```bash
# Verify CSP in DevTools Console
# Open DevTools → Network tab → find index.html response → check CSP header

# Or automate in CI:
curl -I http://localhost:5173 2>/dev/null | grep -i content-security-policy
```

**Warning signs in CSP:**
- `script-src 'unsafe-eval'` — allows `eval()` which is dangerous
- `script-src 'unsafe-inline'` — allows inline `<script>` tags, bypassing CSP
- Missing `object-src 'none'` — allows Flash/ActiveX objects

## 4. Crash Reporting

### 4.1 Configuration

```typescript
// main.ts
import { crashReporter } from 'electron';

crashReporter.start({
  submitURL: 'https://sentry.example.com/api/minidump/?sentry_key=YOUR_KEY',
  uploadToServer: true,
  compress: true,
  globalExtra: {
    appVersion: app.getVersion(),
    platform: process.platform,
    arch: process.arch,
    osVersion: os.release(),
  },
});
```

### 4.2 Capturing Renderer Crashes

```typescript
app.on('render-process-gone', (event, webContents, details) => {
  console.error('Renderer process crashed:', {
    reason: details.reason, // 'crashed' | 'killed' | 'oom' | 'clean-exit' | 'abnormal-exit'
    exitCode: details.exitCode,
  });

  // Show recovery UI
  const win = BrowserWindow.fromWebContents(webContents);
  if (win) {
    win.loadFile('crash-recovery.html');
  }
});
```

## 5. OS Integration

### 5.1 Custom Protocol Handler

```typescript
// main.ts
if (process.defaultApp) {
  if (process.argv.length >= 2) {
    app.setAsDefaultProtocolClient('myapp', process.execPath, [
      path.resolve(process.argv[1]),
    ]);
  }
} else {
  app.setAsDefaultProtocolClient('myapp');
}

// Handle protocol activation
app.on('open-url', (event, url) => {
  event.preventDefault();
  // Parse url: myapp://path/to/resource?param=value
  const parsed = new URL(url);
  mainWindow?.webContents.send('protocol:activated', {
    path: parsed.pathname,
    params: Object.fromEntries(parsed.searchParams),
  });
});
```

### 5.2 File Associations

```json
// electron-builder.yml
fileAssociations:
  - ext: .myapp
    name: MyApp Project
    description: MyApp project file
    role: Editor
  - ext: .mydata
    name: MyApp Data
    role: Viewer

// macOS specific
mac:
  extendInfo:
    CFBundleDocumentTypes:
      - CFBundleTypeName: MyApp Project
        CFBundleTypeRole: Editor
        LSHandlerRank: Owner
        LSItemContentTypes:
          - com.myapp.project
```

### 5.3 Global Shortcuts

```typescript
import { globalShortcut } from 'electron';

app.whenReady().then(() => {
  const registered = globalShortcut.register('CommandOrControl+Shift+M', () => {
    mainWindow?.show();
    mainWindow?.focus();
  });

  if (!registered) {
    console.error('Global shortcut registration failed');
  }
});

app.on('will-quit', () => {
  globalShortcut.unregisterAll();
});
```

## 6. Performance Optimization

### 6.1 Startup Performance Budget

| Metric | Target | Critical |
|--------|--------|----------|
| Cold start (first launch) | < 3s | > 5s unacceptable |
| Warm start | < 1.5s | > 2.5s unacceptable |
| Time to interactive | < 2s | > 4s unacceptable |

### 6.2 Memory Management

```typescript
// Aggressive garbage collection hint
app.on('browser-window-blur', () => {
  if (global.gc) {
    global.gc();
  }
});

// Run with --expose-gc in development
// electron --js-flags="--expose-gc" main.js
```

### 6.3 Lazy Loading Heavy Modules

```typescript
// Instead of:
import sharp from 'sharp'; // 30MB native module loaded at startup

// Do:
async function processImage(path: string) {
  const sharp = await import('sharp');
  return sharp(path).resize(800).toBuffer();
}
```

## 7. Security Audit Checklist

- [ ] `nodeIntegration: false` on all BrowserWindows
- [ ] `contextIsolation: true` on all BrowserWindows
- [ ] `sandbox: true` on all BrowserWindows
- [ ] No `remote` module usage (deprecated, removed in Electron 14+)
- [ ] `webSecurity: true` (default, never disable)
- [ ] `allowRunningInsecureContent: false` (default)
- [ ] CSP header present and restrictive
- [ ] All `shell.openExternal()` calls validate URL protocol
- [ ] No `webview` tag usage (use `BrowserView` instead)
- [ ] `webPreferences.additionalArguments` is empty
- [ ] Preload script is the only file importing `ipcRenderer`
