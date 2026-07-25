## 13. Performance Architecture

### 13.1 Thread/Process Model

```
┌────────────────────────────────────────────────┐
│                  MAIN PROCESS                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │
│  │ IPC Hub  │  │ Menu/    │  │ Native       │ │
│  │          │  │ Tray     │  │ Addons (NAPI)│ │
│  └──────────┘  └──────────┘  └──────────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │
│  │ Worker 1 │  │ Worker 2 │  │ Worker N     │ │
│  │ (CPU)    │  │ (I/O)    │  │ (Specialized)│ │
│  └──────────┘  └──────────┘  └──────────────┘ │
└────────────────────────────────────────────────┘
```

- **CPU-bound work** → Worker threads (Node.js `worker_threads`) or Web Workers
- **I/O-bound work** → Async I/O in main process (libuv handles it natively)
- **GPU-bound work** → Renderer process (WebGL, Canvas, CSS animations)

### 13.2 Memory Budget

| App Type | Idle Memory | Active Memory | Bundle Size |
|----------|-------------|---------------|-------------|
| Tauri | 30-50 MB | 80-150 MB | 5-15 MB |
| Electron (optimized) | 80-120 MB | 200-400 MB | 50-120 MB |
| Electron (unoptimized) | 200-400 MB | 800+ MB | 150-300 MB |
| SwiftUI | 40-80 MB | 120-200 MB | 10-30 MB |
| WinUI 3 | 50-100 MB | 150-300 MB | 20-50 MB |

---
