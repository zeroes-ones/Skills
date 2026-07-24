---
name: tauri-security-model
description: Complete Tauri v2 security model reference — capability-based permissions, CSP configuration, command allowlisting, scope restrictions, IPC hardening, and platform security best practices.
author: Sandeep Kumar Penchala
---

# Tauri Security Model

Tauri's security model is fundamentally different from Electron's. Tauri uses a **capability-based permission system** where each window explicitly declares what it can access. There is no Node.js integration — the webview is truly sandboxed, and all system access goes through the Rust backend via explicitly registered commands.

---

## 1. Capability-Based Permissions (Tauri v2)

### 1.1 The Permission Model

Tauri v2 introduced a declarative capability system. Each window gets a `capabilities` JSON file that explicitly lists which plugins and commands it can invoke.

```
Window "main":
  capabilities/default.json:
    ✓ core:default          — window management, app info
    ✓ dialog:allow-save     — save file dialogs
    ✓ fs:allow-read-text    — read text files
    ✓ fs:allow-write-text   — write text files
    ✗ fs:allow-read-binary  — NOT granted
    ✗ shell:allow-execute   — NOT granted

Window "settings":
  capabilities/settings.json:
    ✓ core:default
    ✓ store:allow-get       — read from app store
    ✓ store:allow-set       — write to app store
    ✗ dialog:*              — NO file dialogs
    ✗ fs:*                  — NO filesystem access
```

### 1.2 Capabilities File Structure

```json
// src-tauri/capabilities/default.json
{
  "identifier": "default",
  "description": "Capabilities for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "dialog:allow-open",
    "dialog:allow-save",
    "fs:allow-read-text-file",
    "fs:allow-write-text-file",
    "fs:allow-exists",
    {
      "identifier": "fs:allow-read-text-file",
      "allow": [
        {
          "path": "$APPDATA/**"
        }
      ]
    },
    {
      "identifier": "http:default",
      "allow": [
        {
          "url": "https://api.myapp.com/**"
        }
      ]
    }
  ]
}
```

### 1.3 Scope-Based Restrictions

Tauri commands can be scoped to specific paths, URLs, or resources:

```json
// Permission scope examples
{
  "identifier": "fs:allow-read-text-file",
  "allow": [
    { "path": "$APPDATA/**" },        // Only app data directory
    { "path": "$DOCUMENT/**" }        // Only documents directory
  ]
}

{
  "identifier": "http:default",
  "allow": [
    { "url": "https://api.myapp.com/**" },  // Only our API
    { "url": "https://cdn.myapp.com/**" }   // Only our CDN
  ]
}

{
  "identifier": "shell:allow-execute",
  "allow": [
    { "name": "open", "cmd": "open", "args": true }  // Only macOS open command
  ]
}
```

### 1.4 Security Best Practices for Capabilities

1. **One capability file per window.** Don't share capabilities between main window and settings window.
2. **Least privilege.** A settings window doesn't need file dialog access. A print preview doesn't need HTTP access.
3. **Scope everything.** Never use `fs:allow-read-text-file` without a path scope. Always restrict to `$APPDATA/**` or specific directories.
4. **Review capabilities in CI.** Run `cargo tauri capability verify` as a CI check.

## 2. CSP Configuration

### 2.1 Tauri CSP Settings

```json
// tauri.conf.json
{
  "app": {
    "security": {
      "csp": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://api.myapp.com; frame-src 'none'; object-src 'none'"
    }
  }
}
```

### 2.2 CSP Differences from Electron

Tauri's CSP has some key differences from Electron's web CSP:

- Tauri CSP is **directly embedded** in the HTML file or configured in `tauri.conf.json`
- Tauri does **not** use `session.defaultSession.webRequest.onHeadersReceived`
- The `tauri://` protocol is whitelisted automatically for IPC with the Rust backend
- `connect-src` must include `ipc:` for Tauri v2 IPC (the new IPC bridge)

### 2.3 CSP Validation in CI

```bash
# Check CSP configuration
grep -A5 '"csp"' src-tauri/tauri.conf.json

# Ensure no unsafe-eval
grep -r 'unsafe-eval' src-tauri/tauri.conf.json && echo "ERROR: unsafe-eval in CSP" && exit 1

# Ensure no unsafe-inline scripts (styles are acceptable for most CSS-in-JS libs)
grep -r "script-src.*unsafe-inline" src-tauri/tauri.conf.json && echo "WARN: unsafe-inline scripts"
```

## 3. Command Allowlisting

### 3.1 Registering Commands

Only commands registered in `invoke_handler` are callable from the frontend:

```rust
// src-tauri/src/main.rs
#[tauri::command]
fn get_user_data(app: tauri::AppHandle) -> Result<UserData, String> {
    let path = app.path().app_data_dir()
        .map_err(|e| e.to_string())?
        .join("user.json");
    let data = std::fs::read_to_string(&path)
        .map_err(|e| format!("Read error: {}", e))?;
    serde_json::from_str(&data)
        .map_err(|e| format!("Parse error: {}", e))
}

#[tauri::command]
async fn fetch_api_data(url: String) -> Result<serde_json::Value, String> {
    // Validate URL is within allowed scope
    if !url.starts_with("https://api.myapp.com/") {
        return Err("URL not in allowed scope".into());
    }
    reqwest::get(&url)
        .await
        .map_err(|e| e.to_string())?
        .json()
        .await
        .map_err(|e| e.to_string())
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            get_user_data,
            fetch_api_data,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### 3.2 Command Security Rules

1. **Validate ALL arguments within the command body.** Never trust frontend input.
2. **Restrict URL/Path arguments** to known scopes. Validate against allowlists, not blocklists.
3. **Return `Result<T, String>` with descriptive errors.** Never panic or unwrap in commands.
4. **Use `async` commands for I/O.** Blocking commands freeze the Rust event loop.
5. **Never expose arbitrary shell execution.** If `shell:allow-execute` is granted, restrict command names to a known-safe list.

### 3.3 Frontend Invocation with Type Safety

```typescript
// src/lib/commands.ts
import { invoke } from '@tauri-apps/api/core';

interface UserData {
  name: string;
  preferences: Record<string, unknown>;
}

export async function getUserData(): Promise<UserData> {
  try {
    return await invoke<UserData>('get_user_data');
  } catch (error) {
    console.error('Failed to get user data:', error);
    throw new Error(typeof error === 'string' ? error : 'Unknown error');
  }
}

export async function fetchApiData(endpoint: string): Promise<unknown> {
  const url = `https://api.myapp.com/${endpoint}`;
  return invoke('fetch_api_data', { url });
}
```

## 4. Filesystem Security

### 4.1 Path Resolution

Tauri provides safe path resolution through the `app.path()` API:

```rust
use tauri::Manager;

#[tauri::command]
fn read_config(app: tauri::AppHandle) -> Result<Config, String> {
    // Safe: resolves to OS-appropriate app config directory
    let config_dir = app.path().app_config_dir()
        .map_err(|e| e.to_string())?;

    // Safe: joins within the resolved path
    let config_path = config_dir.join("settings.json");

    // Read file
    let data = std::fs::read_to_string(&config_path)
        .map_err(|e| format!("Cannot read: {}", e))?;

    serde_json::from_str(&data)
        .map_err(|e| format!("Invalid JSON: {}", e))
}
```

### 4.2 Path Traversal Prevention

```rust
// DANGEROUS: allows path traversal
fn dangerous_read(user_path: String) {
    let path = std::path::Path::new(&user_path);
    std::fs::read_to_string(path); // Could read /etc/passwd!
}

// Safe: resolves relative to a base directory
fn safe_read(app: tauri::AppHandle, relative_path: String) -> Result<String, String> {
    let base = app.path().app_data_dir().map_err(|e| e.to_string())?;
    let resolved = base.join(&relative_path);

    // Canonicalize and verify it's still under base
    let canonical = resolved.canonicalize().map_err(|e| e.to_string())?;
    let base_canonical = base.canonicalize().map_err(|e| e.to_string())?;

    if !canonical.starts_with(&base_canonical) {
        return Err("Path traversal detected".into());
    }

    std::fs::read_to_string(&canonical)
        .map_err(|e| format!("Read error: {}", e))
}
```

## 5. Network Security

### 5.1 HTTP Scope Restrictions

```json
// capabilities/default.json
{
  "identifier": "http:default",
  "allow": [
    {
      "url": "https://api.myapp.com/**"       // Production API
    },
    {
      "url": "https://staging-api.myapp.com/**"  // Staging API
    }
  ],
  "deny": [
    {
      "url": "http://**"  // Block all HTTP (non-TLS)
    }
  ]
}
```

### 5.2 Certificate Pinning (Advanced)

Tauri apps can implement certificate pinning via a custom HTTP client:

```rust
use reqwest::Certificate;

#[tauri::command]
async fn secure_request() -> Result<String, String> {
    let cert = Certificate::from_pem(include_bytes!("../cert.pem"))
        .map_err(|e| e.to_string())?;

    let client = reqwest::Client::builder()
        .add_root_certificate(cert)
        .https_only(true)
        .build()
        .map_err(|e| e.to_string())?;

    client.get("https://api.myapp.com/data")
        .send()
        .await
        .map_err(|e| e.to_string())?
        .text()
        .await
        .map_err(|e| e.to_string())
}
```

## 6. Security Audit Checklist

- [ ] Capabilities file exists (`src-tauri/capabilities/default.json`)
- [ ] Permissions follow least privilege per window
- [ ] All `fs:` permissions are scoped to specific paths (`$APPDATA/**`)
- [ ] All `http:` permissions are scoped to specific URLs
- [ ] No `shell:allow-execute` without command name restrictions
- [ ] CSP configured in `tauri.conf.json > app.security.csp`
- [ ] CSP does not contain `unsafe-eval`
- [ ] All `#[tauri::command]` functions validate arguments
- [ ] No command uses `unwrap()` or `panic!()` — all return `Result<T, String>`
- [ ] Path traversal protection on all file operations accepting user input
- [ ] HTTPS enforced for all network requests
