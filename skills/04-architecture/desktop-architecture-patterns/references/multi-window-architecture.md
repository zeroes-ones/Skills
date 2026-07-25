# Multi-Window Architecture — Patterns for Desktop Applications

## Overview

Multi-window architecture is one of the most complex aspects of desktop development. Unlike web apps where "pages" are ephemeral views, desktop windows have independent lifecycles, OS-level management, and persistent identity. Getting this wrong results in data loss, state corruption, and broken user workflows.

---

## Window Lifecycle State Machine

```
                    ┌──────────┐
                    │  NONE    │
                    └────┬─────┘
                         │ new BrowserWindow()
                    ┌────▼─────┐
            ┌──────►│ CREATED  │
            │       └────┬─────┘
            │            │ win.show()
            │       ┌────▼─────┐
            │       │  SHOWN   │◄──────────────┐
            │       └────┬─────┘               │
            │            │                     │
            │   ┌────────┼────────┐            │
            │   │        │        │            │
            │   ▼        ▼        ▼            │
            │ ┌────┐ ┌──────┐ ┌────────┐      │
            │ │MIN │ │FOCUS │ │BLURRED │      │
            │ │IMIZE│ │ED    │ │        │──────┘
            │ └──┬─┘ └──┬───┘ └────────┘  restore
            │    │       │
            │    │       │ win.close()
            │    │  ┌────▼─────┐
            │    │  │ CLOSING   │──► preventDefault() ──┐
            │    │  └────┬─────┘                       │
            │    │       │ allow close                  │
            │    │  ┌────▼─────┐                       │
            └────┼──┤  CLOSED  │◄──────────────────────┘
                 │  └────┬─────┘
                 │       │ auto-destroy
                 │  ┌────▼─────┐
                 └──┤ DESTROYED│
                    └──────────┘
```

**Platform-specific behaviors:**
- **macOS:** `window-all-closed` does NOT quit app; `Cmd+Q` sends `before-quit` → `will-quit`
- **Windows:** `window-all-closed` quits app by default; Alt+F4 closes focused window
- **Linux:** Behavior varies by DE; GNOME treats last-window-close same as Windows

---

## Window Ownership Models

### Parent-Child Hierarchy

```
┌──────────────────────────────┐
│      MainWindow (parent)      │
│                               │
│  ┌─────────────────────────┐ │
│  │ SettingsDialog (modal)   │ │
│  │ parent: MainWindow       │ │
│  └─────────────────────────┘ │
│                               │
│  ┌─────────────────────────┐ │
│  │ InspectorPanel (child)   │ │
│  │ parent: MainWindow       │ │
│  │ modal: false             │ │
│  └─────────────────────────┘ │
└──────────────────────────────┘
```

**Rules for parent-child windows:**
1. Child closes when parent closes (OS enforces this)
2. Modal children block parent interaction (macOS: sheet; Windows: modal dialog)
3. Child position relative to parent (platform convention)
4. `parent.window.getChildWindows()` for management

### Independent Windows

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Document A  │  │  Document B  │  │  Settings    │
│  (independent)│  │  (independent)│  │  (independent)│
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └────────┬────────┴────────┬────────┘
                │                 │
          ┌─────▼─────────────────▼─────┐
          │     Main Process Store       │
          │   (shared state via IPC)     │
          └─────────────────────────────┘
```

**Rules for independent windows:**
1. Each has its own renderer process (crash isolation)
2. Shared state ONLY via main process — never direct renderer-to-renderer IPC
3. Window identity via UUID assigned at creation
4. Registry of active windows in main process for lifecycle queries

---

## State Synchronization Between Windows

### Central Store Pattern

```typescript
// Main process — single source of truth
class WindowRegistry {
  private windows = new Map<string, WindowState>();
  private store = new AppStore(); // Redux/Zustand store

  registerWindow(id: string, initialState: WindowState) {
    this.windows.set(id, initialState);
  }

  dispatch(action: Action, sourceWindowId: string) {
    const newState = this.store.reduce(this.store.getState(), action);

    // Broadcast to ALL windows except source
    for (const [id, win] of this.windows) {
      if (id !== sourceWindowId) {
        win.webContents.send('state-sync', {
          action,
          newState: this.scopeState(newState, id) // Scoped to window's concern
        });
      }
    }
  }
}
```

### Scoped State Pattern

Not every window needs the full state tree. Scope state to what each window actually renders:

```typescript
// Window A (Document Editor): needs documents, currentDocument, undoStack
// Window B (Project Explorer): needs projectTree, activeBranch
// Window C (Search): needs searchIndex, recentQueries

function scopeState(fullState: AppState, windowId: string): Partial<AppState> {
  const windowRole = getWindowRole(windowId);
  switch (windowRole) {
    case 'editor': return pick(fullState, ['documents', 'currentDocument', 'undoStack']);
    case 'explorer': return pick(fullState, ['projectTree', 'activeBranch']);
    case 'search': return pick(fullState, ['searchIndex', 'recentQueries']);
    default: return fullState;
  }
}
```

---

## Window Coordination Patterns

### Pattern 1: "Open in New Window"

```typescript
// Renderer requests new window
const newWindowId = await ipcRenderer.invoke('window:open', {
  type: 'document',
  context: { documentId: 'doc-123', scrollPosition: 450 },
  position: 'cascade' // offset from parent, or 'center', or {x, y}
});

// Main process creates and registers
ipcMain.handle('window:open', async (event, params) => {
  const id = crypto.randomUUID();
  const win = new BrowserWindow({
    width: 1200, height: 800,
    webPreferences: { preload: PATH_PRELOAD, contextIsolation: true }
  });
  registry.registerWindow(id, { type: params.type, context: params.context });
  await win.loadURL(`app://editor?windowId=${id}&documentId=${params.context.documentId}`);
  return id;
});
```

### Pattern 2: "Focus or Create"

```typescript
ipcMain.handle('window:focusOrCreate', async (event, params) => {
  const existing = registry.findWindow(w =>
    w.type === params.type && w.context.documentId === params.context.documentId
  );
  if (existing) {
    existing.win.focus();
    return existing.id;
  }
  // Create new window as above
});
```

### Pattern 3: "Broadcast to All"

```typescript
// Main process
ipcMain.on('theme:change', (event, theme) => {
  registry.broadcast('theme:changed', theme);
});

// All renderers receive and apply
ipcRenderer.on('theme:changed', (event, theme) => {
  applyTheme(theme);
});
```

---

## Window Restoration (Session Persistence)

```typescript
interface WindowSession {
  id: string;
  type: string;
  bounds: { x: number; y: number; width: number; height: number };
  isMaximized: boolean;
  context: Record<string, unknown>; // type-specific: documentId, scroll, etc.
}

// On app quit
app.on('before-quit', async () => {
  const session: WindowSession[] = [];
  for (const [id, state] of registry.all()) {
    const bounds = state.win.getBounds();
    session.push({
      id, type: state.type,
      bounds,
      isMaximized: state.win.isMaximized(),
      context: state.context
    });
  }
  await fs.promises.writeFile(SESSION_PATH, JSON.stringify(session));
});

// On app start
app.on('ready', async () => {
  const session: WindowSession[] = JSON.parse(
    await fs.promises.readFile(SESSION_PATH, 'utf-8')
  );
  for (const s of session) {
    const win = new BrowserWindow({ ...s.bounds });
    if (s.isMaximized) win.maximize();
    await win.loadURL(`app://${s.type}?restore=${JSON.stringify(s.context)}`);
  }
});
```

---

## Platform-Specific Window Behaviors

### macOS

```typescript
// Frameless window with native traffic lights
new BrowserWindow({
  titleBarStyle: 'hiddenInset', // Traffic lights inset into content
  vibrancy: 'under-window',     // macOS blur effect
  transparent: true,
});

// NSWindow tabbing (macOS 10.12+)
win.setRepresentedFilename('/path/to/document.pdf'); // Proxy icon in titlebar
win.setDocumentEdited(true); // Dot in close button
```

### Windows

```typescript
// Snap layouts (Windows 11)
// Automatically supported by BrowserWindow; test at common sizes:
// 50% snap: 683px @ 1366px screen
// 33% snap: 455px @ 1366px screen

// Taskbar thumbnail buttons
win.setThumbarButtons([
  { icon: playIcon, click: () => win.webContents.send('media:play') },
  { icon: pauseIcon, click: () => win.webContents.send('media:pause') }
]);

// Taskbar progress
win.setProgressBar(0.75); // 75% progress overlay on taskbar icon
```

### Linux

```typescript
// Wayland vs X11 detection
const isWayland = process.env.XDG_SESSION_TYPE === 'wayland';

// Window positioning workaround (Wayland doesn't allow setBounds for security)
if (!isWayland) {
  win.setBounds({ x: 100, y: 100, width: 1200, height: 800 });
}

// CSD (Client-Side Decorations) for GNOME
new BrowserWindow({
  frame: true, // Let the WM handle decorations (SSD on KDE, CSD on GNOME)
});
```

---

## Memory Management for Multi-Window Apps

```
┌─────────────────────────────────────────────┐
│  Window Count    →    Memory Strategy        │
├─────────────────────────────────────────────┤
│  1-3 windows     →    Full state per window  │
│  4-10 windows    →    Shared store + scoped  │
│  10+ windows     →    Virtualized state +    │
│                       LRU window cache       │
└─────────────────────────────────────────────┘
```

**Background window throttling:**
```typescript
win.on('blur', () => {
  win.webContents.setBackgroundThrottling(true); // Reduce timers to 1Hz
});
win.on('focus', () => {
  win.webContents.setBackgroundThrottling(false);
});
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Renderer-to-renderer IPC | No crash isolation; hard to debug | Route all cross-window communication through main process |
| Global mutable window registry | Race conditions on create/destroy | UUID-keyed Map with synchronized access |
| Restoring windows at exact positions | Window may be off-screen on different monitor setup | Clamp bounds to `screen.getPrimaryDisplay().workArea` |
| Creating windows in response to IPC without debounce | 100 windows from a stuck keyboard repeat | Debounce 300ms on window creation from user input |
| Not handling `render-process-gone` | Zombie windows — dead renderer, live BrowserWindow | Listen and destroy: `win.on('render-process-gone', () => win.destroy())` |

---

## References

- [Electron BrowserWindow Docs](https://www.electronjs.org/docs/latest/api/browser-window)
- [SwiftUI WindowGroup (macOS)](https://developer.apple.com/documentation/swiftui/windowgroup)
- See also: [desktop-state-management.md](desktop-state-management.md), [desktop-ipc-architecture.md](desktop-ipc-architecture.md)
