# Desktop IPC Architecture — Inter-Process Communication Patterns

## Overview

IPC is the backbone of modern desktop applications. Every message crossing the renderer-main process boundary is a serialization point, a potential bottleneck, and a security boundary. This reference covers IPC patterns for Electron, Tauri, and native desktop applications.

---

## IPC Security Model

### The Golden Rule

```
RENDERER ──[untrusted]──► PRELOAD ──[validated]──► MAIN ──[authorized]──► SYSTEM
```

The renderer process is **always** compromised. Design every IPC channel as if the renderer is attacker-controlled — because it is.

### Electron Security Baseline

```typescript
// main process — webPreferences
const mainWindow = new BrowserWindow({
  webPreferences: {
    sandbox: true,                    // macOS App Store requirement
    contextIsolation: true,           // MANDATORY — no renderer-to-Node access
    nodeIntegration: false,           // MANDATORY — Node.js in renderer = RCE
    preload: path.join(__dirname, 'preload.js'),
    webSecurity: true,                // Same-origin policy
    allowRunningInsecureContent: false,
  }
});

// Content Security Policy
mainWindow.webContents.session.webRequest.onHeadersReceived((details, callback) => {
  callback({
    responseHeaders: {
      ...details.responseHeaders,
      'Content-Security-Policy': [
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
      ]
    }
  });
});
```

### contextBridge — The Only Bridge

```typescript
// preload.js — EXPOSED API
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('appAPI', {
  // Request-response pattern
  getDocuments: () => ipcRenderer.invoke('documents:list'),
  saveDocument: (doc: Document) => ipcRenderer.invoke('documents:save', doc),

  // Event subscription
  onDocumentChanged: (callback: (doc: Document) => void) => {
    const handler = (_event: any, doc: Document) => callback(doc);
    ipcRenderer.on('documents:changed', handler);
    return () => ipcRenderer.removeListener('documents:changed', handler);
  },

  // One-way fire-and-forget
  logEvent: (event: AnalyticsEvent) => ipcRenderer.send('analytics:track', event),
});

// NEVER do this:
// contextBridge.exposeInMainWorld('danger', { exec: require('child_process').exec });
```

---

## IPC Patterns

### Pattern 1: Request-Response (invoke/handle)

```typescript
// Main process — handler registration
ipcMain.handle('documents:save', async (event, doc: Document) => {
  // Validate — never trust renderer data
  if (!isValidDocument(doc)) {
    throw new IPCError('INVALID_DOCUMENT', 'Document schema validation failed');
  }

  // Authorize — which window sent this?
  const windowId = BrowserWindow.fromWebContents(event.sender)?.id;
  if (!windowId || !windowRegistry.has(windowId)) {
    throw new IPCError('UNAUTHORIZED', 'Unknown window');
  }

  // Execute
  const result = await documentService.save(doc);

  // Notify other windows
  windowRegistry.broadcast('documents:changed', doc, windowId);

  return result;
});

// Renderer — typed client
const result = await window.appAPI.saveDocument(doc); // typed, validated
```

### Pattern 2: Event Streaming

```typescript
// Main process — streaming large data
ipcMain.handle('export:start', async (event, params) => {
  const rows = await db.query('SELECT * FROM huge_table');

  // Break into chunks — never send 50MB in one IPC message
  const CHUNK_SIZE = 1000;
  for (let i = 0; i < rows.length; i += CHUNK_SIZE) {
    const chunk = rows.slice(i, i + CHUNK_SIZE);
    event.sender.send('export:chunk', { index: i / CHUNK_SIZE, data: chunk });
    await sleep(0); // Yield to event loop — don't flood IPC
  }
  event.sender.send('export:complete', { total: rows.length });
  return { status: 'started' };
});
```

### Pattern 3: Transferable Objects (Zero-Copy)

```typescript
// Renderer — transferring large ArrayBuffer
const buffer = new ArrayBuffer(50 * 1024 * 1024); // 50MB
const uint8 = new Uint8Array(buffer);
// ... fill buffer with camera data ...

// Transfer (not copy) — buffer becomes detached in renderer
await ipcRenderer.invoke('video:frame', { frame: uint8.buffer }, [uint8.buffer]);
// uint8.buffer.byteLength === 0 now — ownership transferred
```

### Pattern 4: MessagePort for High-Throughput Channels

```typescript
// Main process
ipcMain.handle('stream:open', (event) => {
  const { port1, port2 } = new MessageChannelMain();

  // port1 stays in main, process data
  port1.on('message', (event) => {
    const { data } = event;
    processRealtimeData(data);
    port1.postMessage({ ack: data.sequence });
  });

  // port2 sent to renderer via IPC
  event.sender.postMessage('stream:port', null, [port2]);
});
```

---

## Tauri IPC Architecture

### Command Pattern

```rust
// Rust backend — command registration
#[tauri::command]
async fn save_document(
    app: tauri::AppHandle,
    doc: Document,
) -> Result<DocumentId, String> {
    // Validate
    if doc.title.is_empty() {
        return Err("Title cannot be empty".into());
    }

    // Authorize via app handle
    let state = app.state::<AppState>();
    let id = state.db.save(&doc).await.map_err(|e| e.to_string())?;

    // Emit event to all windows
    app.emit_all("document:saved", id.clone()).unwrap();

    Ok(id)
}

// Registration
fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![save_document])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

```typescript
// Frontend — typed invoke
import { invoke } from '@tauri-apps/api/core';

const id = await invoke<DocumentId>('save_document', { doc: { title: 'My Doc' } });
```

### Tauri Event System

```typescript
// Listen for backend events
import { listen } from '@tauri-apps/api/event';

const unlisten = await listen<DocumentId>('document:saved', (event) => {
  console.log('Document saved:', event.payload);
});

// Cleanup
unlisten();
```

### Tauri IPC Performance Considerations

| Operation | Serialization | Overhead | Use Case |
|-----------|---------------|----------|----------|
| `invoke` | JSON (serde) | ~1ms per call | Standard CRUD, config |
| Custom protocol | Binary (user-defined) | ~0.1ms | Large file streaming |
| Event system | JSON (serde) | ~0.5ms | Real-time notifications |
| File drop | OS-provided path | ~0ms | Drag-and-drop files |

---

## Native Desktop IPC

### Windows: Named Pipes

```
┌─────────────────┐                    ┌─────────────────┐
│   Main Process   │                    │  Helper Service  │
│                  │  \\.\pipe\myapp\   │                  │
│  CreateNamedPipe ├────────────────────►  ConnectNamedPipe │
│                  │◄────────────────────┤                  │
│  ReadFile/       │   Named Pipe        │  WriteFile/      │
│  WriteFile       │   (duplex, 64KB)    │  ReadFile        │
└─────────────────┘                    └─────────────────┘
```

```cpp
// C++ Windows example
HANDLE hPipe = CreateNamedPipe(
    L"\\\\.\\pipe\\MyApp\\ElevatedService",
    PIPE_ACCESS_DUPLEX,
    PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
    PIPE_UNLIMITED_INSTANCES,
    65536, 65536, 0, NULL
);
```

### macOS: XPC Services

```
┌──────────────────┐          ┌──────────────────────┐
│   Main App        │          │  XPC Service          │
│   (com.myapp)     │  XPC     │  (com.myapp.helper)   │
│                   │◄────────►│                       │
│  NSXPCConnection  │          │  NSXPCListener         │
└──────────────────┘          └──────────────────────┘
```

**Benefits of XPC:**
- Automatic privilege separation (service runs in its own sandbox)
- launchd lifecycle management (on-demand launch, idle exit)
- Crash isolation — service crash doesn't kill main app
- First-class support in App Sandbox

### Linux: D-Bus + Unix Domain Sockets

```
┌──────────────────┐          ┌──────────────────────┐
│   Application     │  D-Bus   │  Desktop Environment  │
│                   │◄────────►│  (notifications,      │
│  GDBusConnection  │          │   mpris, file manager) │
└──────────────────┘          └──────────────────────┘
```

---

## IPC Validation and Error Handling

### Typed IPC Layer

```typescript
// schema.ts — shared between main and preload
import { z } from 'zod';

export const DocumentSchema = z.object({
  id: z.string().uuid(),
  title: z.string().min(1).max(500),
  content: z.string().max(10_000_000), // 10MB
  createdAt: z.string().datetime(),
  tags: z.array(z.string().max(50)).max(20),
});

export type Document = z.infer<typeof DocumentSchema>;

// IPC handler with validation
const IPC_SCHEMAS = {
  'documents:save': { input: DocumentSchema, output: z.object({ id: z.string() }) },
  'documents:list': { input: z.object({ limit: z.number().max(100) }), output: z.array(DocumentSchema) },
} as const;

function registerTypedHandler<K extends keyof typeof IPC_SCHEMAS>(
  channel: K,
  handler: (input: z.infer<typeof IPC_SCHEMAS[K]['input']>) => Promise<z.infer<typeof IPC_SCHEMAS[K]['output']>>
) {
  ipcMain.handle(channel, async (event, raw) => {
    const schema = IPC_SCHEMAS[channel];
    const parsed = schema.input.safeParse(raw);
    if (!parsed.success) {
      throw new IPCError('VALIDATION', parsed.error.message);
    }
    return handler(parsed.data);
  });
}
```

### Error Taxonomy

| Error Type | HTTP Analog | When |
|------------|-------------|------|
| `VALIDATION` | 400 | Input fails schema validation |
| `UNAUTHORIZED` | 403 | Window not in registry, expired session |
| `NOT_FOUND` | 404 | Resource doesn't exist |
| `CONFLICT` | 409 | Concurrent modification detected |
| `INTERNAL` | 500 | Unexpected error, retryable |
| `PERMISSION` | 403 | OS denied the operation (file permissions) |

---

## IPC Performance Benchmarks

| Pattern | Throughput | Latency (avg) | Memory per msg |
|---------|------------|---------------|----------------|
| `invoke/handle` (JSON, 1KB) | 5,000 msg/s | 0.2ms | 3KB (serialized + overhead) |
| `invoke/handle` (JSON, 1MB) | 20 msg/s | 50ms | 3MB (serialized + copy) |
| `postMessage` + transfer (1MB) | 1,000 msg/s | 1ms | 0MB (transferred) |
| MessagePort (1KB) | 50,000 msg/s | 0.02ms | 1KB |
| Tauri invoke (1KB) | 8,000 msg/s | 0.1ms | 1KB |

**Rule of thumb:** For > 100 msg/s or messages > 100KB, use transferables or streaming. Never send multi-megabyte payloads through `invoke/handle`.

---

## Anti-Patterns

| Anti-Pattern | Impact | Fix |
|--------------|--------|-----|
| `nodeIntegration: true` | Full RCE in renderer | `contextIsolation: true`, `nodeIntegration: false` |
| Passing functions via IPC | Functions can't be cloned; silent failure | Send data; define handlers on both sides |
| Sending `Buffer` without `.buffer` | Copies entire buffer instead of transferring | Use `.buffer` with transfer list |
| Flooding IPC without backpressure | Renderer event loop starvation, UI freeze | Batch messages, use MessagePort, implement queue |
| Catching all errors as generic | Debugging IPC failures is impossible | Typed errors with machine-readable codes |

---

## References

- [Electron IPC Docs](https://www.electronjs.org/docs/latest/tutorial/ipc)
- [Tauri IPC](https://tauri.app/v1/guides/features/command/)
- [Electron Security Guidelines](https://www.electronjs.org/docs/latest/tutorial/security)
- [XPC Services (Apple)](https://developer.apple.com/documentation/xpc)
