# macOS Sandboxing & Entitlements — The Complete Reference

<!-- STANDARD: 3min -- every entitlement, when to use it, and what breaks without it -->

## The Two Distribution Paths

| Path | Requires | Enforced By | Benefits |
|---|---|---|---|
| **App Store** | App Sandbox (`com.apple.security.app-sandbox`) | App Review + macOS | User trust, automatic updates, no Gatekeeper warnings |
| **Direct Distribution** | Hardened Runtime (`com.apple.security.hardened-runtime`) | Gatekeeper + Notarization | No App Review delays, full revenue, entitlements not available in sandbox |

**Critical**: You CANNOT ship an App Store app without sandboxing. You SHOULD use Hardened Runtime for direct distribution (it's technically optional but Gatekeeper treats unsigned/unhardened apps as malware-risk).

---

## App Sandbox Entitlements — The Full Catalog

### File Access

| Entitlement Key | Grants | When to Use |
|---|---|---|
| `com.apple.security.app-sandbox` | Enables sandbox (REQUIRED for App Store) | Always for App Store |
| `com.apple.security.files.user-selected.read-only` | Read files user picks via `NSOpenPanel` | Import features, opening documents not created by your app |
| `com.apple.security.files.user-selected.read-write` | Read/write files user picks | Document editors, export features |
| `com.apple.security.files.downloads.read-only` | Read from ~/Downloads | Import from downloads |
| `com.apple.security.files.downloads.read-write` | Read/write ~/Downloads | Save to downloads |
| `com.apple.security.files.pictures.read-write` | Read/write ~/Pictures | Photo apps, screenshot tools |
| `com.apple.security.files.music.read-write` | Read/write ~/Music | Audio apps |
| `com.apple.security.files.movies.read-write` | Read/write ~/Movies | Video apps |
| `com.apple.security.temporary-exception.files.home-relative-path.read-write` | Access to a specific path relative to home (e.g., `/.myapp/`) | Temporary entitlement for legacy paths — strongly discouraged, requires App Review justification |
| `com.apple.security.temporary-exception.files.absolute-path.read-write` | Access to a specific absolute path | EVEN MORE discouraged. Only for enterprise apps, never for App Store. |

### Network Access

| Entitlement Key | Grants | When to Use |
|---|---|---|
| `com.apple.security.network.client` | Outbound TCP/UDP connections | Every app that accesses the internet (HTTP, WebSocket, custom protocol) |
| `com.apple.security.network.server` | Inbound TCP/UDP connections (listen on a port) | P2P apps, local servers, Bonjour services, WebSocket servers |

### Hardware Access

| Entitlement Key | Grants | When to Use |
|---|---|---|
| `com.apple.security.device.camera` | Camera access | Video conferencing, photo capture |
| `com.apple.security.device.microphone` | Microphone access | Audio recording, VoIP |
| `com.apple.security.device.usb` | USB device access | Hardware tools, device sync |
| `com.apple.security.device.bluetooth` | Bluetooth access | BLE peripherals, headphones, game controllers |
| `com.apple.security.device.audio-input` | Audio input access (line-in, aggregate devices) | Professional audio tools |
| `com.apple.security.device.printing` | Printer access | Any app that prints |

### Personal Data

| Entitlement Key | Grants | When to Use |
|---|---|---|
| `com.apple.security.personal-information.location` | Core Location access | Maps, weather, location-aware features |
| `com.apple.security.personal-information.addressbook` | Contacts access | CRM, email clients, caller ID |
| `com.apple.security.personal-information.calendars` | Calendar access | Calendar apps, scheduling tools |
| `com.apple.security.personal-information.photos-library` | Full Photos library access | Photo management apps |

---

## Hardened Runtime Entitlements

Used for direct distribution (notarized apps). These are ResourceFlags set via `codesign`, not plist keys.

| Entitlement Key | Effect | When to Use |
|---|---|---|
| `com.apple.security.cs.disable-library-validation` | Allow loading unsigned/third-party plug-ins via `dlopen` | Apps with plugin systems (audio units, Photoshop plugins, scripting extensions) |
| `com.apple.security.cs.disable-executable-page-protection` | Allow writable+executable memory (`mmap` PROT_WRITE \| PROT_EXEC) | JIT compilers, JavaScript engines, emulators. NEVER use unless absolutely required. |
| `com.apple.security.cs.debugger` | Allow attaching a debugger | Development builds only. REMOVE from Release builds. |
| `com.apple.security.cs.allow-jit` | Allow `MAP_JIT` for just-in-time compilation | WebKit, JavaScriptCore, custom JIT engines |
| `com.apple.security.cs.allow-unsigned-executable-memory` | Allow executing memory not from a signed binary | Plugin hosts, scripting engines |
| `com.apple.security.cs.disable-root-restrictions` | Remove root access restrictions | System utilities that genuinely need root |
| `com.apple.security.cs.allow-dyld-environment-variables` | Honor `DYLD_*` environment variables | Development builds only. NEVER in production — allows code injection. |

---

## Entitlement File Template

### App Store Distribution

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- REQUIRED: Enable sandbox -->
    <key>com.apple.security.app-sandbox</key>
    <true/>

    <!-- Network: outbound connections (HTTP, sockets) -->
    <key>com.apple.security.network.client</key>
    <true/>

    <!-- File access: user-chosen files for import/export -->
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>

    <!-- File access: Downloads folder -->
    <key>com.apple.security.files.downloads.read-write</key>
    <true/>

    <!-- App Groups: shared container with extensions -->
    <key>com.apple.security.application-groups</key>
    <array>
        <string>$(TeamIdentifierPrefix)com.yourcompany.yourapp</string>
    </array>
</dict>
</plist>
```

### Direct Distribution (Notarized)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- REQUIRED: Enable Hardened Runtime -->
    <key>com.apple.security.hardened-runtime</key>
    <true/>

    <!-- Network: outbound connections -->
    <key>com.apple.security.network.client</key>
    <true/>

    <!-- Optional: Allow third-party plugins -->
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>

    <!-- Optional: Shared app group -->
    <key>com.apple.security.application-groups</key>
    <array>
        <string>$(TeamIdentifierPrefix)com.yourcompany.yourapp</string>
    </array>
</dict>
</plist>
```

---

## Common Sandboxing Pitfalls

### Pitfall 1: `Process()` / `NSTask` in Sandbox
```
ERROR: "posix_spawn: Operation not permitted"
```
**Why**: The sandbox prohibits launching arbitrary executables via `posix_spawn` or `NSTask`.
**Fix**: Use `NSXPCConnection` to communicate with an XPC Service embedded in your app bundle.

### Pitfall 2: Hardcoded Absolute Paths
```
ERROR: "The file 'Documents' couldn't be opened because you don't have permission to view it."
```
**Why**: The sandbox has its own container. `~/Documents` is NOT your container's Documents.
**Fix**: Use `FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)` or `NSOpenPanel`.

### Pitfall 3: Missing Network Client Entitlement
```
ERROR: "nw_connection_create failed: Operation not permitted"
```
**Why**: Sandbox denies ALL network access by default — both client and server.
**Fix**: Add `com.apple.security.network.client`.

### Pitfall 4: Security-Scoped Bookmarks Expire
```swift
// WRONG: URL access lost after app restart
let url = openPanel.url // Only valid for this session

// RIGHT: Create a security-scoped bookmark
let bookmarkData = try openPanel.url!.bookmarkData(
    options: .withSecurityScope,
    includingResourceValuesForKeys: nil,
    relativeTo: nil
)
UserDefaults.standard.set(bookmarkData, forKey: "savedFile")
// On next launch:
var isStale = false
let url = try URL(
    resolvingBookmarkData: bookmarkData,
    options: .withSecurityScope,
    relativeTo: nil,
    bookmarkDataIsStale: &isStale
)
if isStale {
    // Recreate bookmark
}
url.startAccessingSecurityScopedResource()
defer { url.stopAccessingSecurityScopedResource() }
```

### Pitfall 5: Debug vs Release Entitlement Mismatch
Debug builds in Xcode auto-include `com.apple.security.get-task-allow` (allows debugger attachment) and bypass some sandbox restrictions. Your code works in Xcode but crashes in Release. **Always test with Release configuration before distribution.**

---

## Verifying Entitlements

```bash
# Check entitlements embedded in binary
codesign -d --entitlements :- /path/to/YourApp.app 2>/dev/null | plutil -p -

# Check if sandbox is active at runtime
# In your app:
print("Sandbox: \(ProcessInfo.processInfo.environment["APP_SANDBOX_CONTAINER_ID"] ?? "none")")

# Check Hardened Runtime flags
codesign -dvvv /path/to/YourApp.app 2>&1 | grep -A5 "flags"
```
