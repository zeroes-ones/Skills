---
name: desktop-ipc-patterns
description: Comprehensive IPC design patterns for desktop applications — request/response, push events, streaming, error handling, typed contracts, and security boundaries across Electron, Tauri, and .NET desktop frameworks.
author: Sandeep Kumar Penchala
---

# Desktop IPC Patterns

Inter-Process Communication (IPC) is the most critical design decision in any desktop application. The IPC surface IS the security boundary between untrusted renderer code and privileged system operations. Poor IPC design leads to security vulnerabilities, performance degradation, and unmaintainable spaghetti code.

---

## 1. IPC Architecture Principles

### 1.1 The Four Rules of Desktop IPC

1. **The renderer is always untrusted.** Any code running in the renderer (JavaScript in Electron's Chromium, Rust WASM in Tauri's webview) can be modified by an attacker via XSS, dependency compromise, or devtools. Every IPC message must be treated as hostile input.
2. **Validate at the boundary, not at the handler.** Input validation must happen in the IPC layer before the handler sees the data. If validation is inside the handler, a new handler added by a developer who "just needs it to work" will bypass security.
3. **Errors must be structured and predictable.** Never throw across IPC. Return `{ success: boolean, data?: T, error?: { code: string, message: string } }`. The renderer must be able to distinguish "file not found" from "permission denied" from "network timeout."
4. **IPC is not REST.** The IPC bridge has different serialization rules (Structured Clone Algorithm, not JSON), different latency characteristics (sub-ms for simple messages), and different failure modes (process crash, not HTTP 500).

### 1.2 Serialization: Structured Clone vs JSON

The Electron IPC bridge uses the **Structured Clone Algorithm**, not `JSON.stringify`:

| Type | JSON | Structured Clone |
|------|------|-----------------|
| `string`, `number`, `boolean` | ✓ | ✓ |
| `null`, `undefined` | ✓ (except undefined) | ✓ |
| `Date` | String | ✓ (preserved as Date) |
| `Map`, `Set` | ✗ | ✓ |
| `ArrayBuffer`, `TypedArray` | ✗ | ✓ (zero-copy transfer possible) |
| `Error` | `{}` (lost) | ✓ (preserved) |
| `Function`, `Symbol` | ✗ | ✗ (throws DataCloneError) |
| `WeakMap`, `WeakSet` | ✗ | ✗ |
| Circular references | ✗ | ✗ |

**Key insight:** If you manually `JSON.stringify()` before IPC, you lose `Date` objects (become strings), `Map`/`Set` (become `{}`), and `ArrayBuffer` (becomes base64 string — 33% larger and copies memory). Let the bridge do its job.

## 2. IPC Pattern Catalog

### 2.1 Request-Response (RPC)

The most common pattern. Renderer sends a request, main process responds.

**Electron:**
```typescript
// preload.ts
contextBridge.exposeInMainWorld('api', {
  readFile: (path: string) => ipcRenderer.invoke('fs:readFile', path),
});

// main.ts
ipcMain.handle('fs:readFile', async (_event, path: string) => {
  // Validate path is within allowed directory
  if (!isPathAllowed(path)) {
    return { error: { code: 'PERMISSION_DENIED', message: 'Path not in allowed scope' } };
  }
  try {
    const content = await fs.readFile(path, 'utf-8');
    return { data: content };
  } catch (err) {
    return { error: { code: 'READ_ERROR', message: (err as Error).message } };
  }
});
```

**Tauri:**
```rust
#[tauri::command]
fn read_file(app: tauri::AppHandle, relative_path: String) -> Result<String, String> {
    let base = app.path().app_data_dir().map_err(|e| e.to_string())?;
    let path = base.join(&relative_path);
    // Path traversal check
    let canonical = path.canonicalize().map_err(|e| e.to_string())?;
    if !canonical.starts_with(&base) {
        return Err("Path traversal detected".into());
    }
    std::fs::read_to_string(&canonical).map_err(|e| format!("Read error: {}", e))
}
```

### 2.2 Push Events (Main → Renderer)

Main process pushes events to renderers without a prior request.

**Electron:**
```typescript
// main.ts — push to specific window
mainWindow.webContents.send('update:available', {
  version: '2.0.0',
  releaseDate: '2026-07-24',
});

// preload.ts — expose listener with cleanup
onUpdateAvailable: (callback: (info: UpdateInfo) => void) => {
  const handler = (_: any, info: UpdateInfo) => callback(info);
  ipcRenderer.on('update:available', handler);
  return () => ipcRenderer.removeListener('update:available', handler);
}
```

**Tauri:**
```rust
// Rust backend — emit event
app_handle.emit("update:available", UpdateInfo {
    version: "2.0.0".into(),
    release_date: "2026-07-24".into(),
}).map_err(|e| e.to_string())?;
```
```typescript
// Frontend listener
import { listen } from '@tauri-apps/api/event';
const unlisten = await listen<UpdateInfo>('update:available', (event) => {
  console.log('Update available:', event.payload.version);
});
```

### 2.3 Fire-and-Forget (Renderer → Main)

Renderer sends a message and doesn't wait for a response.

```typescript
// preload.ts
logEvent: (event: string, data: unknown) => {
  ipcRenderer.send('analytics:event', event, data);
}

// main.ts
ipcMain.on('analytics:event', (_event, name: string, data: unknown) => {
  analyticsBuffer.push({ name, data, timestamp: Date.now() });
  // Flush buffer periodically, don't slow down the renderer
});
```

### 2.4 Streaming / Bulk Data Transfer

For large data (>10MB), avoid serializing through IPC. Use shared memory or direct file paths.

**MessagePort (zero-copy):**
```typescript
// main.ts
const { port1, port2 } = new MessageChannelMain();
mainWindow.webContents.postMessage('stream:port', null, [port1]);

// Worker or utility process receives port2
port2.on('message', (event) => {
  // Process data chunks
});
port2.postMessage({ chunk: buffer });
```

**File path passing (preferred for >10MB):**
```typescript
// Instead of passing file content through IPC:
ipcMain.handle('process:largeFile', async (_event, filePath: string) => {
  // Process file directly on main process
  const result = await heavyProcessing(filePath);
  return { outputPath: resultPath }; // Return only path, not data
});
```

## 3. IPC Error Handling

### 3.1 Structured Error Envelope

```typescript
// Shared contract type
interface IPCResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: {
    code: IPCErrorCode;
    message: string;
    details?: unknown;
  };
}

type IPCErrorCode =
  | 'VALIDATION_ERROR'
  | 'PERMISSION_DENIED'
  | 'NOT_FOUND'
  | 'IO_ERROR'
  | 'TIMEOUT'
  | 'INTERNAL_ERROR';
```

### 3.2 Error Handling in Handlers

```typescript
// Consistent error pattern for every handler
ipcMain.handle('data:fetch', async (_event, id: string) => {
  // 1. Validate input
  if (typeof id !== 'string' || id.length === 0) {
    return { success: false, error: { code: 'VALIDATION_ERROR', message: 'id must be a non-empty string' } };
  }

  // 2. Check permissions
  if (!hasAccess(id)) {
    return { success: false, error: { code: 'PERMISSION_DENIED', message: 'Access denied' } };
  }

  // 3. Execute with error handling
  try {
    const data = await db.findById(id);
    if (!data) {
      return { success: false, error: { code: 'NOT_FOUND', message: `Entity ${id} not found` } };
    }
    return { success: true, data };
  } catch (err) {
    console.error('data:fetch failed:', err);
    return { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal error' } };
  }
});
```

## 4. IPC Channel Naming Conventions

Use namespaced channel names to organize IPC:

```
domain:action
────────────
file:open
file:save
file:delete
app:getVersion
app:quit
window:minimize
window:maximize
window:close
update:check
update:download
update:install
data:fetch
data:save
data:delete
notification:show
notification:click
```

## 5. IPC Testing

### 5.1 Handler Unit Tests

```typescript
// test/ipc/file-handlers.test.ts
import { ipcMain } from 'electron';
import { registerFileHandlers } from '../../src/main/ipc/file-handlers';

describe('file:save handler', () => {
  beforeEach(() => {
    registerFileHandlers();
  });

  it('rejects paths outside allowed directory', async () => {
    // Simulate IPC invocation
    const result = await invokeHandler('file:save', '/etc/passwd', 'content');
    expect(result.success).toBe(false);
    expect(result.error?.code).toBe('PERMISSION_DENIED');
  });
});

async function invokeHandler(channel: string, ...args: unknown[]) {
  return new Promise((resolve) => {
    // Access the registered handler
    const handler = (ipcMain as any)._events[channel]?.[0];
    handler({ sender: mockWebContents }, ...args).then(resolve);
  });
}
```

## 6. .NET WPF IPC Patterns

### 6.1 MVVM Command Binding

```csharp
// ViewModel communicates with services via commands
public class MainViewModel : BaseViewModel
{
    private readonly IFileService _fileService;

    public ICommand SaveCommand { get; }

    public MainViewModel(IFileService fileService)
    {
        _fileService = fileService;
        SaveCommand = new AsyncRelayCommand(SaveAsync, () => !IsSaving);
    }

    private async Task SaveAsync()
    {
        try
        {
            IsSaving = true;
            await _fileService.SaveAsync(FilePath, Content);
        }
        catch (IOException ex)
        {
            ErrorMessage = $"Save failed: {ex.Message}";
        }
        finally
        {
            IsSaving = false;
        }
    }
}
```

### 6.2 Cross-Process IPC (Named Pipes)

```csharp
// WPF apps use Named Pipes for single-instance enforcement
using var mutex = new Mutex(true, "MyApp.SingleInstance", out bool createdNew);
if (!createdNew)
{
    // Send args to existing instance via Named Pipe
    using var client = new NamedPipeClientStream(".", "MyApp.Pipe", PipeDirection.Out);
    client.Connect(1000);
    using var writer = new StreamWriter(client);
    writer.Write(Environment.CommandLine);
    return;
}
```

## 7. Performance Considerations

| IPC Pattern | Latency | Throughput | Use Case |
|---|---|---|---|
| `invoke`/`handle` (Electron) | ~0.1-0.5ms | ~10K msg/s | Most operations |
| `send`/`on` (Electron) | ~0.05-0.2ms | ~50K msg/s | Events, logs |
| `sendSync` (Electron) | Blocking | ~5K msg/s | Avoid; <1ms operations only |
| `#[tauri::command]` | ~0.01-0.1ms | ~100K msg/s | All operations |
| MessagePort (transfer) | ~0.001ms | ~1M msg/s | Large buffers |
