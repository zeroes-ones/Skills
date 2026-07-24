# XPC Services Patterns on macOS

<!-- STANDARD: 3min -- privilege separation and crash isolation with XPC -->

## What XPC Services Are

XPC (X-PC) is Apple's inter-process communication (IPC) framework. An XPC Service is a separate process bundled inside your app that communicates with the main app via message passing. XPC is the **only** sanctioned way to run code outside the sandbox container while staying inside the sandbox model.

Key properties:
- **Separate process**: Each XPC service runs in its own process with its own sandbox
- **Crash isolation**: An XPC service crash doesn't crash the main app
- **Privilege separation**: XPC services can have different entitlements than the main app
- **Automatic lifecycle**: The system launches the service on first connection, suspends it when idle, and terminates it when memory is low
- **No UI**: XPC services cannot show UI directly. They communicate data back to the main app.

---

## When to Use XPC Services

| Scenario | Use XPC? |
|---|---|
| Parsing untrusted data that could crash (PDF parsing, archive extraction) | **Yes** — crash in the service, not the main app |
| Network requests that could hang or fail | **Yes** — isolate network failures |
| Database operations that could corrupt state | **Yes** — data integrity boundary |
| Image/video processing (CPU/GPU intensive) | **Yes** — runs on a separate QoS queue |
| System-level operations requiring different entitlements | **Yes** — privileged XPC service |
| Simple data transformation (no crash risk) | **No** — XPC adds IPC overhead |
| UI updates | **No** — XPC can't update UI |

---

## Embedded XPC Service Architecture

```
YourApp.app/
├── Contents/
│   ├── MacOS/
│   │   └── YourApp              (main executable)
│   ├── XPCServices/
│   │   ├── DataProcessor.xpc/   (XPC service bundle)
│   │   │   └── Contents/
│   │   │       └── MacOS/
│   │   │           └── DataProcessor
│   │   └── NetworkService.xpc/
│   │       └── Contents/
│   │           └── MacOS/
│   │               └── NetworkService
│   └── Resources/
```

---

## Creating an XPC Service in Xcode

### Step 1: Add XPC Service Target
File → New → Target → macOS → XPC Service

### Step 2: Define the Protocol (Shared)

Create a shared Swift file included in both the main app and XPC service targets:

```swift
// DataProcessingProtocol.swift
import Foundation

@objc protocol DataProcessingProtocol {
    func processData(
        _ data: Data,
        withReply reply: @escaping (Data?, Error?) -> Void
    )
}
```

### Step 3: Implement the XPC Service

```swift
// DataProcessor.swift — in the XPC Service target
import Foundation

class DataProcessor: NSObject, DataProcessingProtocol {
    func processData(
        _ data: Data,
        withReply reply: @escaping (Data?, Error?) -> Void
    ) {
        // This runs in the XPC service's process.
        // If it crashes, the main app is unaffected.
        do {
            let result = try heavyProcessing(data)
            reply(result, nil)
        } catch {
            reply(nil, error)
        }
    }

    private func heavyProcessing(_ data: Data) throws -> Data {
        // CPU-intensive, potentially crash-prone work
        var result = Data()
        // ... processing ...
        return result
    }
}

// Service delegate
class ServiceDelegate: NSObject, NSXPCListenerDelegate {
    func listener(
        _ listener: NSXPCListener,
        shouldAcceptNewConnection newConnection: NSXPCConnection
    ) -> Bool {
        newConnection.exportedInterface = NSXPCInterface(
            with: DataProcessingProtocol.self
        )
        newConnection.exportedObject = DataProcessor()

        newConnection.invalidationHandler = {
            print("XPC connection invalidated")
        }

        newConnection.resume()
        return true
    }
}

// Entry point
let delegate = ServiceDelegate()
let listener = NSXPCListener.service()
listener.delegate = delegate
listener.resume()
```

### Step 4: Connect from the Main App

```swift
// Main app
import Foundation

final class XPCDataProcessor {
    private var connection: NSXPCConnection?

    func connect() {
        let connection = NSXPCConnection(
            serviceName: "com.yourcompany.yourapp.DataProcessor"
        )
        connection.remoteObjectInterface = NSXPCInterface(
            with: DataProcessingProtocol.self
        )

        connection.invalidationHandler = {
            print("XPC connection lost — will reconnect")
            // Reconnect logic
        }

        connection.interruptionHandler = {
            print("XPC connection interrupted")
        }

        connection.resume()
        self.connection = connection
    }

    func process(data: Data) async throws -> Data {
        guard let connection = connection else {
            throw XPCError.notConnected
        }

        let service = connection.remoteObjectProxyWithErrorHandler { error in
            print("XPC error: \(error)")
        } as! DataProcessingProtocol

        return try await withCheckedThrowingContinuation { continuation in
            service.processData(data) { result, error in
                if let error = error {
                    continuation.resume(throwing: error)
                } else if let result = result {
                    continuation.resume(returning: result)
                } else {
                    continuation.resume(
                        throwing: XPCError.noResult
                    )
                }
            }
        }
    }
}

enum XPCError: Error {
    case notConnected
    case noResult
}
```

---

## XPC Service Lifecycle

```
1. Main app creates NSXPCConnection
2. System launches XPC Service process (if not already running)
3. XPC Service's NSXPCListener accepts the connection
4. Communication begins
5. When main app suspends → XPC Service suspends
6. When memory pressure → System terminates idle XPC Services
7. On next connection → System relaunches the service
```

---

## Code Signing XPC Services

Each XPC Service must be signed with its own identity:

```bash
# Sign XPC services first, then the main app
codesign --force --sign "Developer ID Application: Your Name (TEAMID)" \
  --options runtime --timestamp \
  YourApp.app/Contents/XPCServices/DataProcessor.xpc

codesign --force --sign "Developer ID Application: Your Name (TEAMID)" \
  --options runtime --timestamp \
  YourApp.app/Contents/XPCServices/NetworkService.xpc

# Then sign the main app
codesign --force --sign "Developer ID Application: Your Name (TEAMID)" \
  --options runtime --timestamp \
  YourApp.app
```

XPC service entitlements are per-service. Each `.xpc` bundle gets its own `Info.plist` and entitlements.

---

## Performance Considerations

| Concern | Guidance |
|---|---|
| **Launch latency** | First XPC connection takes ~50-100ms to launch the service. Cache connections. |
| **IPC overhead** | Each message crosses a process boundary. Batch small messages. Use shared memory (`xpc_shmem`) for large data. |
| **Memory** | Each XPC service adds ~5-20MB baseline memory. Don't create dozens of services. |
| **Thread safety** | XPC messages arrive on a serial queue by default. Use `NSXPCConnection` with a concurrent queue if needed. |

---

## When NOT to Use XPC

- **Simple computed properties**: The IPC overhead isn't worth it.
- **UI code**: XPC can't show windows, views, or any UI.
- **File access that works fine in the sandbox**: Don't add complexity if the main app's sandbox already covers it.
- **In-process plugins**: If you control the plugin code and it's trusted, load it in-process with `Bundle.load()`.
