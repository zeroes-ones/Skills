# Desktop Security Architecture — Threat Model & Defense Patterns

## Overview

Desktop applications have the largest attack surface of any application type: they run with user-level OS privileges, have direct file system access, and often handle sensitive credentials. This reference covers the threat model, defense-in-depth patterns, and platform-specific security controls for desktop apps.

---

## Threat Model

### Attack Surface Map

```
┌──────────────────────────────────────────────────────────────┐
│                     ATTACK SURFACE                           │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  RENDERER    │  │  IPC CHANNEL │  │  NATIVE LAYER    │   │
│  │              │  │              │  │                  │   │
│  │ • XSS        │  │ • Message    │  │ • DLL hijacking  │   │
│  │ • Prototype  │  │   spoofing   │  │ • Symlink races  │   │
│  │   pollution  │  │ • Reentrancy │  │ • TOCTOU         │   │
│  │ • Dependency │  │ • Type       │  │ • Unquoted       │   │
│  │   chain      │  │   confusion  │  │   service paths  │   │
│  │ • CSP bypass │  │ • Buffer     │  │ • Named pipe     │   │
│  │              │  │   overflow   │  │   squatting      │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  STORAGE     │  │  NETWORK     │  │  AUTO-UPDATE     │   │
│  │              │  │              │  │                  │   │
│  │ • Plaintext  │  │ • MITM       │  │ • Unsigned       │   │
│  │   secrets    │  │ • Cert       │  │   updates        │   │
│  │ • SQLite     │  │   pinning    │  │ • No rollback    │   │
│  │   without    │  │   bypass     │  │   verification   │   │
│  │   encryption │  │ • WebSocket  │  │ • HTTP update    │   │
│  │ • Temp files │  │   hijacking  │  │   channel        │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

## Defense Layer 1: Renderer Sandbox

### Electron Hardening Checklist

```typescript
// main.ts — SECURITY BASELINE
const mainWindow = new BrowserWindow({
  webPreferences: {
    // MANDATORY
    sandbox: true,                    // macOS App Store requirement
    contextIsolation: true,           // No renderer access to Node.js
    nodeIntegration: false,           // Absolute requirement
    nodeIntegrationInWorker: false,   // No Node in Web Workers either

    // RECOMMENDED
    webSecurity: true,                // Same-origin policy enforced
    allowRunningInsecureContent: false,
    experimentalFeatures: false,      // Disable experimental Chromium features

    // Preload script (contextBridge only)
    preload: path.join(__dirname, 'preload.js'),
  }
});

// Disable remote module (deprecated, dangerous)
app.commandLine.appendSwitch('disable-electron-site-instance-overrides');

// Disable opening arbitrary URLs
mainWindow.webContents.setWindowOpenHandler(({ url }) => {
  // Only allow app-internal URLs
  if (url.startsWith('app://')) return { action: 'allow' };
  // External URLs open in system browser
  shell.openExternal(url);
  return { action: 'deny' };
});

// Prevent navigation to external origins
mainWindow.webContents.on('will-navigate', (event, url) => {
  if (!url.startsWith('app://')) {
    event.preventDefault();
  }
});
```

### Content Security Policy (CSP)

```typescript
// Strict CSP — allowlist approach
session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
  callback({
    responseHeaders: {
      ...details.responseHeaders,
      'Content-Security-Policy': [
        [
          "default-src 'self'",
          "script-src 'self'",                    // No inline scripts, no eval
          "style-src 'self' 'unsafe-inline'",     // Allow inline styles (unavoidable)
          "img-src 'self' data: blob:",           // Allow data URIs for images
          "font-src 'self'",
          "connect-src 'self' https://api.example.com",  // Only your API
          "frame-src 'none'",                     // No iframes
          "object-src 'none'",                    // No plugins
        ].join('; ')
      ]
    }
  });
});
```

### Tauri CSP

```json
// tauri.conf.json
{
  "tauri": {
    "security": {
      "csp": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self' https://api.example.com"
    }
  }
}
```

---

## Defense Layer 2: IPC Security

### Input Validation (Never Trust Renderer)

```typescript
import { z } from 'zod';

// Shared schemas — validates ALL IPC input
const SaveDocumentSchema = z.object({
  id: z.string().uuid(),
  title: z.string().min(1).max(500).trim(),
  content: z.string().max(10_000_000), // 10MB limit
  tags: z.array(z.string().max(50)).max(20).optional(),
  metadata: z.record(z.string(), z.unknown()).optional(),
});

// Handler with validation
ipcMain.handle('documents:save', async (event, rawInput) => {
    throw new IPCError('VALIDATION_FAILED', parsed.error.format());
  }

    throw new IPCError('RATE_LIMITED', 'Too many requests');
  }

  }

  // Step 5: Execute
  return documentService.save(sanitized);
});
```

### Rate Limiter

```typescript
class IPCRateLimiter {
  private counters = new Map<string, { count: number; resetAt: number }>();

  check(clientId: string, channel: string, maxRequests: number, windowMs: number): boolean {
    const key = `${clientId}:${channel}`;
    const now = Date.now();
    let entry = this.counters.get(key);

    if (!entry || now > entry.resetAt) {
      entry = { count: 0, resetAt: now + windowMs };
      this.counters.set(key, entry);
    }

    entry.count++;
    return entry.count <= maxRequests;
  }
}
```

// Validate that contextIsolation is actually enabled
    // ... typed API
  });
---
## Defense Layer 3: Secret Management
### OS Keychain Integration

```typescript
// Using safeStorage (Electron 28+) — encrypts with OS-level key
import { safeStorage } from 'electron';

class SecureStore {
  private storagePath: string;

  constructor() {
    this.storagePath = path.join(app.getPath('userData'), 'encrypted-store.json');
  }

  async set(key: string, value: string): Promise<void> {
    if (!safeStorage.isEncryptionAvailable()) {
      throw new Error('OS encryption not available');
    }

    const encrypted = safeStorage.encryptString(value);
    const store = await this.readStore();

    store[key] = encrypted.toString('base64');
    await fs.promises.writeFile(this.storagePath, JSON.stringify(store), { mode: 0o600 });
  }

  async get(key: string): Promise<string | null> {
    if (!safeStorage.isEncryptionAvailable()) return null;

    const store = await this.readStore();
    const encrypted = store[key];
    if (!encrypted) return null;

    return safeStorage.decryptString(Buffer.from(encrypted, 'base64'));
  }

  async delete(key: string): Promise<void> {
    const store = await this.readStore();
    delete store[key];
    await fs.promises.writeFile(this.storagePath, JSON.stringify(store), { mode: 0o600 });
  }

  async clear(): Promise<void> {
    await fs.promises.writeFile(this.storagePath, '{}', { mode: 0o600 });
  }

  private async readStore(): Promise<Record<string, string>> {
    try {
      const data = await fs.promises.readFile(this.storagePath, 'utf-8');
      return JSON.parse(data);
    } catch {
      return {};
    }
  }
}
```


| Platform | Requirement | Certificate Type | Validation |
|----------|-------------|-----------------|------------|
| Windows | EV Code Signing | Extended Validation (HSM-backed) | SmartScreen reputation |
| macOS | Developer ID + Notarization | Apple Developer (2-year expiry) | Gatekeeper + notary service |
| Linux | GPG (Flatpak) / AppImage signature | GPG key | Package manager verification |

### macOS Notarization Pipeline

```bash
# 1. Code sign with hardened runtime
codesign --deep --force --options runtime \
  --entitlements entitlements.plist \
  --sign "Developer ID Application: My Company (TEAMID)" \
  MyApp.app

# 2. Create ZIP for notarization
ditto -c -k --keepParent MyApp.app MyApp.zip

# 3. Submit for notarization
xcrun notarytool submit MyApp.zip \
  --apple-id "dev@company.com" \
  --team-id "TEAMID" \
  --password "@keychain:AC_PASSWORD" \
  --wait

# 4. Staple the notarization ticket
xcrun stapler staple MyApp.app
```

## Defense Layer 5: Network Security

### Certificate Pinning

```typescript
app.on('ready', () => {
  session.defaultSession.setCertificateVerifyProc((request, callback) => {
    const { hostname, certificate } = request;

    // Pin API endpoints
    const PINNED_HOSTS: Record<string, string[]> = {
      'api.example.com': ['SHA256:AA:BB:CC:DD:EE:FF:...'],
      'updates.example.com': ['SHA256:11:22:33:44:55:66:...'],
    };

    if (PINNED_HOSTS[hostname]) {
      const matches = PINNED_HOSTS[hostname].includes(certificate.fingerprint);
      if (!matches) {
        callback(-2); // CERT_STATUS_AUTHORITY_INVALID
        return;
      }
    }

    callback(0); // Trust for non-pinned hosts
  });
});
```

### Secure Protocol Handlers

```typescript
// Deep link handling — NEVER trust the payload
app.setAsDefaultProtocolClient('myapp');

app.on('open-url', (event, url) => {
  event.preventDefault();
  const parsed = new URL(url);

  // Validate protocol
  if (parsed.protocol !== 'myapp:') {
    logger.warn('Invalid protocol:', parsed.protocol);
    return;
  }

  // Validate path
  const ALLOWED_PATHS = ['/open', '/auth-callback', '/import'];
  if (!ALLOWED_PATHS.includes(parsed.pathname)) {
    logger.warn('Blocked path:', parsed.pathname);
    return;
  }

  // Sanitize query parameters
  const params = Object.fromEntries(parsed.searchParams);
  // ... validate each param against schema ...

  handleDeepLink(parsed.pathname, params);
});
```

---

## Security Testing Checklist

```yaml
# .github/workflows/security.yml
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
      - uses: Electronegativity/action@v1
        with:
          path: ./src
      - uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          scanners: vuln,secret,misconfig
```

---

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|--------------|------|-----|
| `nodeIntegration: true` for "easier development" | RCE in renderer from any XSS | `contextIsolation: true`, never enable nodeIntegration |
| `webSecurity: false` for CORS during development | Disables same-origin policy entirely | Configure CORS on API server, use proxy in dev |
| Storing tokens in localStorage | Plaintext accessible from DevTools | OS keychain via safeStorage |
| No input validation on IPC handlers | Prototype pollution, type confusion attacks | Zod/Yup schema validation on every handler |
| `shell.openExternal(userProvidedUrl)` without sanitization | Arbitrary command execution | Validate URL protocol (allowlist: https only) |
| CSP with `'unsafe-eval'` | Enables code injection via eval() | Remove eval usage or isolate to sandboxed context |
| Hardcoded secrets in source | Secrets in git history, distribution bundles | Environment variables, build-time injection, keychain |

---

## References

- [Electron Security Guidelines](https://www.electronjs.org/docs/latest/tutorial/security)
- [Electronegativity (Security Linter)](https://github.com/doyensec/electronegativity)
- [OWASP Desktop App Security](https://cheatsheetseries.owasp.org/cheatsheets/Desktop_App_Security_Cheat_Sheet.html)
- [Apple Hardened Runtime](https://developer.apple.com/documentation/security/hardened_runtime)
- [Microsoft Windows Security](https://learn.microsoft.com/en-us/windows/security/)
