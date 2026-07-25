## 8. System Tray & Background Services

```
┌─────────────────────────────────────────┐
│          SYSTEM TRAY ICON               │
│  ┌───────────────────────────────────┐ │
│  │  Show/Hide Windows                │ │
│  │  Quick Actions (context menu)     │ │
│  │  Status Indicators                │ │
│  └───────────┬───────────────────────┘ │
│              │                          │
│  ┌───────────▼───────────────────────┐ │
│  │    BACKGROUND SERVICE PROCESS     │ │
│  │  ┌─────────┐  ┌────────────────┐  │ │
│  │  │ Watcher │  │ Sync Scheduler │  │ │
│  │  │ (fs,    │  │ (periodic      │  │ │
│  │  │  network│  │  operations)   │  │ │
│  │  └─────────┘  └────────────────┘  │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Platform differences:**
- Windows: System tray + Notification Area (always visible by default)
- macOS: Menu bar app (`NSStatusBar`) + `LSUIElement` for background-only
- Linux: `StatusNotifier` (KDE) / `AppIndicator` (Ubuntu) — fragmented ecosystem

See: [reference/system-tray-background-services.md](reference/system-tray-background-services.md)

---
