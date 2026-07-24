---
name: auto-update-strategies
description: Production auto-update implementation for Electron, Tauri, .NET, and native desktop apps — differential updates, staged rollouts, rollback mechanisms, code signing verification, and CI/CD integration.
author: Sandeep Kumar Penchala
---

# Auto-Update Strategies

Auto-update is not a feature — it's the only patch distribution channel you control. Without it, every bug lives forever on every installed copy. This reference covers auto-update implementation for Electron, Tauri, .NET/WPF, and native macOS (Sparkle).

---

## 1. Universal Auto-Update Requirements

Every auto-update implementation must satisfy these requirements, regardless of framework:

| Requirement | Why | Failure Mode |
|---|---|---|
| Atomic swap | Prevents partial updates that corrupt the app | User has a broken app that won't launch |
| Signature verification | Prevents supply-chain attacks via compromised update server | Attacker can push malware to all users |
| Rollback on failure | New version crashes on launch → revert to previous | User locked out, must manually reinstall |
| HTTPS manifest | Prevents MITM tampering of update metadata | Attacker can redirect to malicious binary |
| Staged rollouts | Canary releases catch bugs before 100% rollout | Bug affects entire user base simultaneously |
| Differential updates | Reduces bandwidth for users on metered connections | 180MB download every patch cycle |
| Health telemetry | Knows if updates are actually being applied | "Update available" but nobody can install it |

## 2. Electron: electron-updater

### 2.1 Architecture

```
┌──────────────┐    HTTPS     ┌─────────────────┐
│  Electron    │◄────────────►│  Update Server   │
│  App         │   manifest   │  (S3 / GitHub)   │
│              │   + binary   │                  │
│ autoUpdater  │              │  latest.yml      │
│              │              │  MyApp-2.0.0.exe │
│              │              │  MyApp-2.0.0.dmg │
└──────────────┘              └─────────────────┘
```

### 2.2 Provider Configuration

```typescript
// main.ts
import { autoUpdater } from 'electron-updater';
import { app } from 'electron';

// S3 provider (recommended for production)
autoUpdater.setFeedURL({
  provider: 's3',
  bucket: 'myapp-updates',
  region: 'us-east-1',
  path: '/',
});

// GitHub Releases provider (good for open source)
autoUpdater.setFeedURL({
  provider: 'github',
  owner: 'myorg',
  repo: 'myapp',
  private: true,
  token: process.env.GH_TOKEN, // Only for private repos
});

// Generic HTTP provider (self-hosted)
autoUpdater.setFeedURL({
  provider: 'generic',
  url: 'https://updates.myapp.com/',
  channel: 'stable',
});
```

### 2.3 Update Lifecycle

```typescript
app.whenReady().then(() => {
  // Check for updates 15 seconds after launch (don't block startup)
  setTimeout(() => {
    autoUpdater.checkForUpdatesAndNotify();
  }, 15000);

  // Check every 4 hours
  setInterval(() => {
    autoUpdater.checkForUpdatesAndNotify();
  }, 4 * 60 * 60 * 1000);
});

// Update events
autoUpdater.on('checking-for-update', () => {
  mainWindow?.webContents.send('update:checking');
});

autoUpdater.on('update-available', (info) => {
  mainWindow?.webContents.send('update:available', {
    version: info.version,
    releaseDate: info.releaseDate,
    releaseNotes: info.releaseNotes,
  });
});

autoUpdater.on('download-progress', (progress) => {
  mainWindow?.webContents.send('update:progress', {
    percent: progress.percent,
    bytesPerSecond: progress.bytesPerSecond,
  });
});

autoUpdater.on('update-downloaded', (info) => {
  mainWindow?.webContents.send('update:downloaded', info);
});

autoUpdater.on('error', (error) => {
  console.error('Update error:', error);
  mainWindow?.webContents.send('update:error', error.message);
});
```

### 2.4 Update Manifest Format

```yaml
# latest.yml (Windows)
version: 2.0.0
files:
  - url: MyApp-Setup-2.0.0.exe
    sha512: abc123def456...
    size: 89000000
path: MyApp-Setup-2.0.0.exe
sha512: abc123def456...
releaseDate: '2026-07-24T00:00:00.000Z'

# latest-mac.yml (macOS)
version: 2.0.0
files:
  - url: MyApp-2.0.0-mac.zip
    sha512: def789abc012...
    size: 95000000
path: MyApp-2.0.0-mac.zip
sha512: def789abc012...
releaseDate: '2026-07-24T00:00:00.000Z'
```

### 2.5 Staged Rollouts

```typescript
// electron-builder.yml
publish:
  provider: s3
  bucket: myapp-updates
  updaterCacheDirName: myapp-updater

// Staged rollout via electron-updater
// Set in latest.yml:
//   stagingPercentage: 5   ← only 5% of users get this update

// In code:
autoUpdater.allowPrerelease = false; // Beta channel
autoUpdater.allowDowngrade = false;  // Never downgrade
autoUpdater.autoDownload = true;     // Download in background
autoUpdater.autoInstallOnAppQuit = true;
```

### 2.6 Rollback Implementation

```typescript
import { app } from 'electron';
import { execSync } from 'child_process';
import { existsSync } from 'fs';
import { join } from 'path';

function checkAppHealth(): boolean {
  // Basic health check: can we create a window?
  try {
    const { BrowserWindow } = require('electron');
    const win = new BrowserWindow({ show: false });
    win.destroy();
    return true;
  } catch {
    return false;
  }
}

function rollbackToPreviousVersion(): void {
  const backupDir = join(app.getPath('userData'), 'previous-version');
  if (!existsSync(backupDir)) {
    console.error('No backup available for rollback');
    return;
  }

  // Restore previous version
  // Platform-specific restoration logic
  if (process.platform === 'win32') {
    execSync(`robocopy "${backupDir}" "${path.dirname(app.getPath('exe'))}" /E /IS /IT`);
  } else if (process.platform === 'darwin') {
    execSync(`cp -R "${backupDir}/" "${path.dirname(app.getPath('exe'))}/"`);
  }

  app.relaunch();
  app.exit();
}

// On launch, check if this is a fresh update
const updateFlag = join(app.getPath('userData'), '.just-updated');
if (existsSync(updateFlag)) {
  // Remove flag
  fs.unlinkSync(updateFlag);

  // Health check
  setTimeout(() => {
    if (!checkAppHealth()) {
      rollbackToPreviousVersion();
    }
  }, 30000); // 30s grace period
}
```

## 3. Tauri: tauri-plugin-updater

### 3.1 Configuration

```json
// tauri.conf.json
{
  "plugins": {
    "updater": {
      "active": true,
      "endpoints": [
        "https://updates.myapp.com/{{target}}/{{arch}}/{{current_version}}"
      ],
      "dialog": true,
      "pubkey": "YOUR_PUBLIC_KEY_HERE",
      "windows": {
        "installMode": "passive"
      }
    }
  }
}
```

### 3.2 Update Server Response Format

```json
{
  "version": "2.0.0",
  "notes": "Bug fixes and performance improvements.",
  "pub_date": "2026-07-24T00:00:00Z",
  "platforms": {
    "darwin-x86_64": {
      "signature": "base64_encoded_ed25519_signature",
      "url": "https://updates.myapp.com/MyApp_2.0.0_x64.app.tar.gz"
    },
    "darwin-aarch64": {
      "signature": "base64_encoded_ed25519_signature",
      "url": "https://updates.myapp.com/MyApp_2.0.0_aarch64.app.tar.gz"
    },
    "windows-x86_64": {
      "signature": "base64_encoded_ed25519_signature",
      "url": "https://updates.myapp.com/MyApp_2.0.0_x64.msi"
    },
    "linux-x86_64": {
      "signature": "base64_encoded_ed25519_signature",
      "url": "https://updates.myapp.com/MyApp_2.0.0_amd64.AppImage"
    }
  }
}
```

### 3.3 Key Generation

```bash
# Generate signing key pair
cargo tauri signer generate -w ~/.tauri/myapp.key

# The public key goes in tauri.conf.json > plugins.updater.pubkey
```

## 4. macOS Native: Sparkle

### 4.1 Architecture

Sparkle is the industry standard for macOS auto-update. Used by 90%+ of Mac apps including VSCode, Slack, and 1Password.

```xml
<!-- appcast.xml — served over HTTPS -->
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:sparkle="http://www.andymatuschak.org/xml-namespaces/sparkle">
  <channel>
    <title>MyApp Updates</title>
    <item>
      <title>Version 2.0.0</title>
      <sparkle:releaseNotesLink>https://myapp.com/releases/2.0.0.html</sparkle:releaseNotesLink>
      <pubDate>Wed, 24 Jul 2026 00:00:00 +0000</pubDate>
      <enclosure
        url="https://updates.myapp.com/MyApp-2.0.0.zip"
        sparkle:version="2.0.0"
        sparkle:shortVersionString="2.0"
        sparkle:edSignature="base64_encoded_ed25519_signature"
        length="95000000"
        type="application/octet-stream" />
      <sparkle:minimumSystemVersion>13.0</sparkle:minimumSystemVersion>
    </item>
  </channel>
</rss>
```

### 4.2 Delta Updates with Sparkle

Sparkle supports delta updates via `sparkle:deltaFrom`:

```xml
<enclosure url="https://updates.myapp.com/MyApp-2.0.0.zip"
           sparkle:version="2.0.0"
           sparkle:edSignature="..."
           length="95000000" />

<!-- Delta from 1.9.0 to 2.0.0 -->
<enclosure url="https://updates.myapp.com/MyApp-1.9.0-2.0.0.delta"
           sparkle:version="2.0.0"
           sparkle:deltaFrom="1.9.0"
           sparkle:edSignature="..."
           length="15000000" />
```

## 5. Windows: Squirrel.Windows / ClickOnce

### 5.1 Squirrel.Windows

```csharp
// .NET app using Squirrel.Windows
using Squirrel;

public static async Task CheckForUpdates()
{
    using var manager = new UpdateManager(
        "https://updates.myapp.com",
        "MyApp",
        FrameworkVersion.Net60);

    var updateInfo = await manager.CheckForUpdate();
    if (updateInfo.ReleasesToApply.Any())
    {
        await manager.UpdateApp();
        // App will restart automatically
    }
}
```

### 5.2 Microsoft Store (MSIX) Auto-Update

MSIX-packaged apps distributed through the Microsoft Store get automatic updates managed by the Store infrastructure:

```xml
<!-- AppxManifest.xml — update settings -->
<UpdateSettings>
  <AutoUpdate>
    <OnLaunch>true</OnLaunch>
  </AutoUpdate>
</UpdateSettings>
```

## 6. CI/CD Integration

### 6.1 GitHub Actions — Update Manifest Generation

```yaml
# .github/workflows/release.yml
- name: Generate update manifests
  run: |
    # Generate latest.yml for Windows
    node scripts/generate-manifest.js \
      --platform windows \
      --version ${{ github.ref_name }} \
      --file dist/MyApp-Setup-${{ github.ref_name }}.exe

    # Upload to S3
    aws s3 cp dist/ s3://myapp-updates/ --recursive
    aws s3 cp latest.yml s3://myapp-updates/latest.yml
    aws s3 cp latest-mac.yml s3://myapp-updates/latest-mac.yml
```

### 6.2 Verification in CI

```yaml
- name: Verify update manifests
  run: |
    # Check manifest is valid JSON/YAML
    python3 -c "import yaml; yaml.safe_load(open('latest.yml'))"

    # Verify binaries referenced in manifest exist
    for file in $(grep -oP 'url:\s+\K.*' latest.yml); do
      aws s3 ls "s3://myapp-updates/$file" || echo "MISSING: $file"
    done

    # Verify SHA512
    aws s3 cp "s3://myapp-updates/$(grep url latest.yml | head -1 | cut -d' ' -f2)" /tmp/verify.exe
    EXPECTED=$(grep sha512 latest.yml | head -1 | cut -d' ' -f2)
    ACTUAL=$(sha512sum /tmp/verify.exe | cut -d' ' -f1)
    [ "$EXPECTED" = "$ACTUAL" ] || echo "SHA512 MISMATCH"
```

## 7. Testing Auto-Update

### 7.1 Local Testing

```bash
# 1. Build version 1.0.0
npm run build && electron-builder --publish=never

# 2. Serve updates locally
npx http-server dist/updates -p 8080 --cors

# 3. Configure app to use local update server
# autoUpdater.setFeedURL('http://localhost:8080/')

# 4. Increment version to 2.0.0 in package.json

# 5. Rebuild, copy artifacts to updates/ directory

# 6. Launch v1.0.0 app — should detect v2.0.0 update
```

### 7.2 Failure Mode Testing

| Test | How | Expected Behavior |
|------|-----|-------------------|
| Server unreachable | Kill update server | App continues normally, no error shown to user |
| Corrupt download | Serve truncated binary | Signature verification fails, delete and retry |
| Disk full | Fill disk before update | Notify user, don't retry, log error |
| New version crashes | Deploy crashing build to test channel | Auto-rollback to previous version within 30s |
| Network drop mid-download | Kill network during download | Resume from byte offset on next check |
