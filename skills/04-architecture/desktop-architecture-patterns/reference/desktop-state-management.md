# Desktop State Management — Architecture Patterns

## Overview

Desktop state management differs fundamentally from web and mobile: state persists across process boundaries, multiple windows share state, and users expect to close and reopen the app exactly where they left off. This reference covers state architecture patterns for Electron, Tauri, and native desktop apps.

---

## State Architecture

```
┌──────────────────────────────────────────────────┐
│                 STATE LAYERS                      │
├──────────────────────────────────────────────────┤
│  L1: EPHEMERAL STATE                              │
│  • UI focus, scroll position, animation state     │
│  • Lives in renderer memory                       │
│  • Lost on window close — acceptable              │
├──────────────────────────────────────────────────┤
│  L2: SESSION STATE                                │
│  • Open documents, undo stack, tab state          │
│  • Persisted to disk periodically (SQLite WAL)    │
│  • Restored on app/window reopen                  │
├──────────────────────────────────────────────────┤
│  L3: PERSISTENT STATE                             │
│  • User preferences, project config, recent files │
│  • Written immediately on change                  │
│  • Survives crashes, OS restarts                  │
├──────────────────────────────────────────────────┤
│  L4: SECRETS                                      │
│  • Tokens, passwords, encryption keys             │
│  • OS keychain only — never in app memory longer  │
│    than necessary                                 │
│  • Wiped from memory after use                    │
└──────────────────────────────────────────────────┘
```

---

## Redux-Style Architecture (Electron)

### Store Design

```typescript
// store/types.ts
interface AppState {
  documents: DocumentsState;
  ui: UIState;
  user: UserState;
  sync: SyncState;
}

interface DocumentsState {
  byId: Record<string, Document>;
  allIds: string[];
  activeDocumentId: string | null;
  undoStack: UndoEntry[][]; // Per-document undo stacks
  redoStack: UndoEntry[][];
  isDirty: Record<string, boolean>;
  lastModified: Record<string, number>;
}

interface UIState {
  theme: 'light' | 'dark' | 'system';
  sidebarWidth: number;
  sidebarVisible: boolean;
  activePanel: 'explorer' | 'search' | 'extensions' | 'none';
  windowStates: Record<string, WindowState>;
}

interface SyncState {
  status: 'idle' | 'syncing' | 'error' | 'offline';
  lastSyncAt: number | null;
  pendingChanges: number;
  conflictIds: string[];
}
```

### Main Process Store (Single Source of Truth)

```typescript
// main/store.ts
import { createStore, applyMiddleware } from 'redux';
import createSagaMiddleware from 'redux-saga';

const sagaMiddleware = createSagaMiddleware();

const store = createStore(
  rootReducer,
  applyMiddleware(
    sagaMiddleware,
    persistenceMiddleware,   // Auto-save to SQLite
    ipcForwardMiddleware,    // Broadcast actions to renderers
    analyticsMiddleware      // Track state changes
  )
);

// Persistence middleware
const persistenceMiddleware: Middleware = store => next => action => {
  const result = next(action);
  const state = store.getState();

  // Determine what needs persisting based on action type
  if (action.type.startsWith('documents/')) {
    persistDocuments(state.documents);
  }
  if (action.type.startsWith('user/')) {
    persistUserPreferences(state.user);
  }

  return result;
};

// IPC forward middleware — notify renderers of state changes
const ipcForwardMiddleware: Middleware = store => next => action => {
  const result = next(action);
  const state = store.getState();

  // Scope state per window and broadcast
  for (const [windowId, winState] of Object.entries(state.ui.windowStates)) {
    const scoped = scopeState(state, windowId);
    browserWindows.get(windowId)?.webContents.send('state:update', scoped);
  }

  return result;
};
```
```typescript
// Actions are the source of truth for undo, not snapshots
interface UndoableAction {
  type: string;
  payload: unknown;
  undo: () => void;   // Reverse function
  redo: () => void;   // Forward function
  timestamp: number;
  groupKey?: string;   // For grouping rapid-fire edits
}

class UndoManager {
  private undoStack: UndoableAction[] = [];
  private redoStack: UndoableAction[] = [];
  private maxSize = 1000;

  execute(action: UndoableAction) {
    action.redo();
    this.undoStack.push(action);
    this.redoStack = []; // New action invalidates redo

    // Group rapid-fire edits within 500ms
    const last = this.undoStack[this.undoStack.length - 1];
    if (last?.groupKey && last.groupKey === action.groupKey &&
        action.timestamp - last.timestamp < 500) {
      // Merge into last action's undo/redo
    }

    if (this.undoStack.length > this.maxSize) {
      this.undoStack.shift();
    }
  }

  undo(): boolean {
    const action = this.undoStack.pop();
    if (!action) return false;
    action.undo();
    this.redoStack.push(action);
    return true;
  }

  redo(): boolean {
    const action = this.redoStack.pop();
    if (!action) return false;
    action.redo();
    this.undoStack.push(action);
    return true;
  }
}
```

### Snapshot-Based Undo (Text Editors)

```typescript
// For text editors where actions are too granular
interface Snapshot {
  documentId: string;
  content: string;
  cursorPosition: { line: number; column: number };
  timestamp: number;
}

class SnapshotUndoManager {
  private snapshots = new Map<string, Snapshot[]>();
  private currentIndex = new Map<string, number>();
  private readonly MAX_SNAPSHOTS = 500;
  private readonly MIN_INTERVAL_MS = 300;

  private lastSnapshot = new Map<string, number>();

  capture(documentId: string, content: string, cursor: { line: number; column: number }) {
    // Throttle: at most one snapshot every 300ms per document
    const last = this.lastSnapshot.get(documentId) || 0;
    if (Date.now() - last < this.MIN_INTERVAL_MS) return;

    const stack = this.snapshots.get(documentId) || [];
    const idx = this.currentIndex.get(documentId) || -1;

    // Discard redo stack
    stack.length = idx + 1;

    stack.push({ documentId, content, cursorPosition: cursor, timestamp: Date.now() });
    this.currentIndex.set(documentId, idx + 1);
    this.lastSnapshot.set(documentId, Date.now());

    // Limit stack size
    if (stack.length > this.MAX_SNAPSHOTS) {
      stack.shift();
      this.currentIndex.set(documentId, (this.currentIndex.get(documentId) || 0) - 1);
    }

    this.snapshots.set(documentId, stack);
  }

  undo(documentId: string): Snapshot | null {
    const idx = this.currentIndex.get(documentId) || -1;
    if (idx <= 0) return null;
    this.currentIndex.set(documentId, idx - 1);
    return this.snapshots.get(documentId)![idx - 1];
  }

  redo(documentId: string): Snapshot | null {
    const stack = this.snapshots.get(documentId);
    if (!stack) return null;
    const idx = this.currentIndex.get(documentId) || -1;
    if (idx >= stack.length - 1) return null;
    this.currentIndex.set(documentId, idx + 1);
}
```

---

## Cross-Window State Sync

### Conflict Resolution: Last-Write-Wins with Meld

```typescript
interface StateChange {
  windowId: string;
  key: string;
  value: unknown;
  timestamp: number;
  vectorClock: Record<string, number>; // Lamport-style vector clock
}

class StateSynchronizer {
  private vectorClock: Record<string, number> = {};
  private pendingChanges: StateChange[] = [];

  applyLocal(key: string, value: unknown) {
    this.vectorClock[this.windowId] = (this.vectorClock[this.windowId] || 0) + 1;

    const change: StateChange = {
      windowId: this.windowId,
      key, value,
      timestamp: Date.now(),
      vectorClock: { ...this.vectorClock }
    };

    // Apply locally immediately (optimistic)
    this.localState[key] = value;

    // Send to main process for broadcast
    ipcRenderer.send('state:change', change);
  }

  receiveRemote(change: StateChange) {
    // Update vector clock
    for (const [wid, clock] of Object.entries(change.vectorClock)) {
      this.vectorClock[wid] = Math.max(this.vectorClock[wid] || 0, clock);
    }

    // Check for conflicts
    const existing = this.localState[change.key];
    if (existing && !this.isConcurrent(change, this.lastLocalChange[change.key])) {
      // No conflict — apply directly
      this.localState[change.key] = change.value;
    } else {
      // Conflict — use timestamp as tiebreaker (LWW)
      this.pendingChanges.push(change);
      this.resolveConflicts();
    }
  }

  private isConcurrent(a: StateChange, b?: StateChange): boolean {
    if (!b) return false;
    const aAfterB = Object.keys(a.vectorClock).some(
      wid => (a.vectorClock[wid] || 0) > (b.vectorClock[wid] || 0)
    );
    const bAfterA = Object.keys(b.vectorClock).some(
      wid => (b.vectorClock[wid] || 0) > (a.vectorClock[wid] || 0)
    );
    return aAfterB && bAfterA; // Concurrent if neither happened-before the other
  }
}
```

---

## Persistence Strategy

```typescript
import Database from 'better-sqlite3';

class StatePersistence {
  private db: Database.Database;

  constructor(dbPath: string) {
    this.db = new Database(dbPath);
    this.db.pragma('journal_mode = WAL');
    this.db.pragma('synchronous = NORMAL');
    this.db.pragma('foreign_keys = ON');

    this.db.exec(`
      CREATE TABLE IF NOT EXISTS state (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        updated_at INTEGER NOT NULL
      );

      CREATE INDEX IF NOT EXISTS idx_state_updated
      ON state(updated_at);
    `);
  }

  // Scheduled persistence — not on every keystroke
  private pendingWrites = new Map<string, string>();
  private flushTimeout: NodeJS.Timeout | null = null;
  private readonly FLUSH_INTERVAL = 500; // 500ms debounce

  scheduleWrite(key: string, value: unknown) {
    this.pendingWrites.set(key, JSON.stringify(value));

    if (!this.flushTimeout) {
      this.flushTimeout = setTimeout(() => this.flush(), this.FLUSH_INTERVAL);
    }
  }

  private flush() {
    const insert = this.db.prepare(`
      INSERT INTO state (key, value, updated_at) VALUES (?, ?, ?)
      ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at
    `);

    const transaction = this.db.transaction(() => {
      const now = Date.now();
      for (const [key, value] of this.pendingWrites) {
        insert.run(key, value, now);
      }
    });

    transaction();
    this.pendingWrites.clear();
    this.flushTimeout = null;
  }

  read(key: string): unknown | null {
    const row = this.db.prepare('SELECT value FROM state WHERE key = ?').get(key) as any;
    return row ? JSON.parse(row.value) : null;
  }

  readAll(): Record<string, unknown> {
    const rows = this.db.prepare('SELECT key, value FROM state').all() as any[];
    return Object.fromEntries(rows.map((r: any) => [r.key, JSON.parse(r.value)]));
  }

  close() {
    this.flush(); // Ensure pending writes committed
    this.db.close();
  }
}
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Storing state only in renderer memory | Lost on crash, refresh, window close | Periodic persistence to main process |
| Writing to disk on every keystroke | I/O saturation, battery drain | Debounced writes (300-500ms) |
| Single global store with no scoping | Every window receives full state on any change | Scoped selectors per window |
| Snapshot undo for huge documents (100MB+) | Memory exhaustion from duplicate content | Action-based undo with patches |
| No state migration on app update | Old state format crashes new version | Versioned state schemas with migration functions |

---

## References

- [Redux Toolkit](https://redux-toolkit.js.org/)
- [Zustand](https://docs.pmnd.rs/zustand)
- [better-sqlite3](https://github.com/WiseLibs/better-sqlite3)
- See also: [multi-window-architecture.md](multi-window-architecture.md), [desktop-ipc-architecture.md](desktop-ipc-architecture.md)
