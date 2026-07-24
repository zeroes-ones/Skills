# Instruments Profiling Reference

## Key Instruments Templates

| Template | Use For | Metric |
|----------|---------|--------|
| Time Profiler | CPU hotspots | % CPU per symbol |
| Allocations | Memory leaks & growth | Live bytes, persistent count |
| Leaks | Retain cycle detection | Leaked objects |
| SwiftUI | View body invocations | Body count, slow frames |
| Core Animation | FPS & hitches | Frame rate, hitch duration |
| Network | HTTP traffic | Latency, throughput |
| Energy Log | Battery drain | Energy impact score |

## Launch Arguments for Profiling

```bash
# In Xcode Scheme > Run > Arguments:
-MallocStackLogging 1              # Trace allocations to call site
-MallocScribble 1                  # Fill freed memory with 0x55
-NSDebugInvalidation 1             # Crash on zombie objects
-com.apple.CoreData.ConcurrencyDebug 1  # Assert Core Data thread safety
```

## Hang Detection (iOS 17+)

```swift
// Xcode Organizer shows hang rate per version
// Target: <1% hang rate for 99th percentile users

// In code: use os_signpost for custom spans
import os

let log = OSLog(subsystem: "com.app", category: .pointsOfInterest)
os_signpost(.begin, log: log, name: "Image Processing")
defer { os_signpost(.end, log: log, name: "Image Processing") }
```

## Common Profiles to Run Before Ship
1. **Leaks** — run for 5+ minutes covering all screens
2. **Time Profiler** — scroll-heavy screens, target <60ms/frame
3. **Allocations** — ensure memory returns to baseline after screen dismiss
