# Desktop Auto-Update Patterns — Architecture & Implementation

## Overview

Auto-update is not a feature — it is a security requirement and a user-retention mechanism. A desktop app without auto-update is a liability: unpatched versions remain on user machines for years, accumulating support costs and security exposure. This reference covers architecture patterns for self-hosted and store-managed update pipelines.

---

## Update Pipeline Architecture

```
┌────────────┐    check     ┌──────────────┐    fetch     ┌───────────────┐
│   Client   │──────────────►│ Update Server │──────────────►│  CDN / S3     │
│  (v1.0.0)  │  GET /update  │  (metadata)   │  redirect    │  (binaries)   │
│            │◄──────────────┤              │◄──────────────┤               │
└─────┬──────┘  {version,url,│              │  artifact     │               │
      │         hash,sig}    └──────────────┘               └───────────────┘
      │
      │  download + verify
      ▼
┌────────────┐    apply    ┌──────────────┐   restart   ┌───────────────┐
│  Staging   │─────────────►│  Replace      │────────────►│  App v1.0.1   │
│  Directory │              │  Executable    │            │  (running)    │
└────────────┘              └──────────────┘            └───────────────┘
```

---

## Security Requirements

### Update Manifest

```json
{
  "version": "1.0.1",
  "releaseDate": "2026-07-24T12:00:00Z",
  "platforms": {
    "darwin": {
      "url": "https://cdn.example.com/releases/1.0.1/mac.zip",
      "sha512": "abc123...",
      "signature": "ed25519:sig...",
      "size": 89456723
    },
    "win32": {
      "url": "https://cdn.example.com/releases/1.0.1/win.exe",
      "sha512": "def456...",
      "signature": "ed25519:sig...",
      "size": 102456789
    }
  },
  "minAppVersion": "1.0.0",
  "releaseNotes": "https://example.com/changelog#1.0.1",
  "mandatory": false
}
```

### Verification Pipeline

```typescript
import { createVerify } from 'crypto';

async function verifyUpdate(artifact: Buffer, signature: string): Promise<boolean> {
  // 1. Verify SHA-512 hash
  const expectedHash = updateManifest.platforms[process.platform].sha512;
  const actualHash = crypto.createHash('sha512').update(artifact).digest('hex');
  if (actualHash !== expectedHash) {
    throw new UpdateError('HASH_MISMATCH', 'Artifact integrity check failed');
  }

  // 2. Verify Ed25519 signature
  const publicKey = Buffer.from(PUBLIC_KEY_HEX, 'hex');
  const verifier = createVerify('sha512');
  verifier.update(artifact);
  verifier.end();

  const sigBuffer = Buffer.from(signature.replace('ed25519:', ''), 'hex');
  if (!verifier.verify({ key: publicKey, format: 'der', type: 'spki' }, sigBuffer)) {
    throw new UpdateError('SIGNATURE_INVALID', 'Artifact signature verification failed');
  }

  return true;
}
```

### Certificate Pinning

```typescript
import { net } from 'electron';

// Pin the update server certificate
net.session.defaultSession.setCertificateVerifyProc((request, callback) => {
  const { hostname, certificate } = request;

  if (hostname === 'updates.example.com') {
    const expectedFingerprint = 'SHA256:AA:BB:CC:...';
    const actualFingerprint = certificate.fingerprint;

    if (actualFingerprint !== expectedFingerprint) {
      callback(-2); // CERT_STATUS_AUTHORITY_INVALID
      return;
    }
  }

  callback(0); // Trust system store for all others
});
```

---

## Platform-Specific Update Mechanisms

### macOS: Sparkle 2

```
┌─────────────┐                  ┌──────────────────┐
│  App Bundle  │                  │  AppCast Server   │
│  ┌─────────┐ │  GET /appcast.xml │                  │
│  │Sparkle  │─┼──────────────────►│  appcast.xml      │
│  │Framework│ │◄──────────────────┤  (RSS 2.0 +      │
│  └─────────┘ │  XML              │   sparkle:        │
└─────────────┘                   │   namespace)      │
                                  └──────────────────┘
```

**AppCast XML:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:sparkle="http://www.andymatuschak.org/xml-namespaces/sparkle">
  <channel>
    <title>MyApp Updates</title>
    <item>
      <title>Version 1.0.1</title>
      <sparkle:version>2026072401</sparkle:version>
      <sparkle:shortVersionString>1.0.1</sparkle:shortVersionString>
      <sparkle:minimumSystemVersion>13.0</sparkle:minimumSystemVersion>
      <enclosure
        url="https://cdn.example.com/MyApp-1.0.1.dmg"
        sparkle:edSignature="MEUCIQD..."
        sparkle:version="2026072401"
        length="45678901"
        type="application/octet-stream" />
    </item>
  </channel>
</rss>
```

**Sparkle 2 requirements:**
- EdDSA (Ed25519) signing — mandatory, replaces DSA
- App must be Developer ID signed and notarized
- Delta updates supported via `sparkle:deltaFrom` elements
- `SUEnableInstallerLauncherService` for sandboxed apps

### Windows: Squirrel.Windows

```
┌────────────┐                ┌──────────────┐
│  App       │  Squirrel       │  Update.exe  │
│  (running) │───────────────►│  (staging)    │
│            │                └──────┬───────┘
│            │                       │
│            │                       ▼
│            │                ┌──────────────┐
│            │◄───────────────│  RELEASES    │
│            │  delta .nupkg  │  file (NuGet) │
└────────────┘                └──────────────┘
```

**RELEASES file format:**
```
B54F3A2D8E1C6F9B7A0D3E5C8F2A4B6D8E0C1A3B  MyApp-1.0.1-full.nupkg  45678901
A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A9B0  MyApp-1.0.1-delta.nupkg  2345678
```

### Electron: electron-updater

```typescript
import { autoUpdater } from 'electron-updater';

// Configure
autoUpdater.setFeedURL({
  provider: 's3',
  bucket: 'myapp-releases',
  region: 'us-east-1',
  path: '/releases',
});

// Auto-download in background
autoUpdater.autoDownload = false; // Let user decide for large updates
autoUpdater.allowDowngrade = false;
autoUpdater.allowPrerelease = false;

// Event handlers
autoUpdater.on('checking-for-update', () => {
  tray.setToolTip('MyApp — Checking for updates...');
});

autoUpdater.on('update-available', (info) => {
  dialog.showMessageBox({
    type: 'info',
    title: 'Update Available',
    message: `Version ${info.version} is available (${(info.files[0].size / 1_000_000).toFixed(0)}MB). Download now?`,
    buttons: ['Download', 'Later']
  }).then(({ response }) => {
    if (response === 0) autoUpdater.downloadUpdate();
  });
});

autoUpdater.on('download-progress', (progress) => {
  mainWindow?.setProgressBar(progress.percent / 100);
  tray.setToolTip(`MyApp — Downloading ${Math.round(progress.percent)}%`);
});

autoUpdater.on('update-downloaded', () => {
  dialog.showMessageBox({
    type: 'info',
    title: 'Update Ready',
    message: 'Update downloaded. Restart now to apply?',
    buttons: ['Restart', 'Later']
  }).then(({ response }) => {
    if (response === 0) autoUpdater.quitAndInstall();
  });
});

autoUpdater.on('error', (error) => {
  logger.error('Update error', { error: error.message });
  tray.setToolTip('MyApp — Update failed');
});

// Check on startup (with delay to not slow down launch)
setTimeout(() => autoUpdater.checkForUpdates(), 10_000);

// Check every 4 hours
setInterval(() => autoUpdater.checkForUpdates(), 4 * 60 * 60 * 1000);
```

### Tauri Updater

```json
// tauri.conf.json
{
  "tauri": {
    "updater": {
      "active": true,
      "endpoints": [
        "https://releases.example.com/update/{{target}}/{{current_version}}"
      ],
      "dialog": true,
      "pubkey": "dW50cnVzdGVkIGNvbW1lbnQ6IG1pbmlzaWduIHB1YmxpYyBrZXk6IDE5QzE5..."
    }
  }
}
```

```typescript
import { checkUpdate, installUpdate } from '@tauri-apps/plugin-updater';
import { relaunch } from '@tauri-apps/plugin-process';

async function checkForUpdates() {
  const update = await checkUpdate();
  if (update) {
    console.log(`Update available: ${update.version}`);
    await update.downloadAndInstall();
    await relaunch();
  }
}
```

---

## Delta Updates

### Binary Diff Strategy

```
┌──────────────┐         ┌──────────────┐
│  v1.0.0.app  │         │  v1.0.1.app  │
└──────┬───────┘         └──────┬───────┘
       │                        │
       └────────┬───────────────┘
                │
         ┌──────▼──────┐
         │  bsdiff /    │
         │  courgette   │
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │  delta.patch │  (10-30% of full update size)
         └─────────────┘
```

**Cost savings:**
| Update Size | Full Download | Delta Download | Savings |
|-------------|---------------|----------------|---------|
| 100 MB | 100 MB | 15-25 MB | 75-85% |
| 50 MB | 50 MB | 8-12 MB | 76-84% |
| 10 MB | 10 MB | 2-4 MB | 60-80% |

CDN bandwidth savings at 100K daily active users: $8K-$15K/month.

---

## Rollback Architecture

```typescript
class UpdateRollback {
  private backupDir: string;
  private currentVersion: string;

  async applyUpdate(updatePath: string): Promise<void> {
    // 1. Backup current version
    const backupPath = path.join(this.backupDir, `backup-${this.currentVersion}`);
    await fs.promises.cp(process.resourcesPath, backupPath, { recursive: true });

    try {
      // 2. Apply new version
      await this.extractUpdate(updatePath, process.resourcesPath);

      // 3. Write version marker
      await fs.promises.writeFile(
        path.join(process.resourcesPath, '.version'),
        updateManifest.version
      );

      // 4. Mark as successful on next start
      await fs.promises.writeFile(
        path.join(this.backupDir, '.last-successful'),
        'true'
      );
    } catch (err) {
      // 5. Rollback on any failure
      await fs.promises.rm(process.resourcesPath, { recursive: true });
      await fs.promises.cp(backupPath, process.resourcesPath, { recursive: true });
      throw new UpdateError('APPLY_FAILED', 'Update failed, rolled back');
    }
  }

  async checkAndRollback(): Promise<boolean> {
    const success = await fs.promises.access(
      path.join(this.backupDir, '.last-successful')
    ).then(() => true).catch(() => false);

    if (!success) {
      // App failed to start after update — rollback
      const backups = await fs.promises.readdir(this.backupDir);
      const latest = backups.filter(b => b.startsWith('backup-')).sort().pop();
      if (latest) {
        await fs.promises.rm(process.resourcesPath, { recursive: true });
        await fs.promises.cp(
          path.join(this.backupDir, latest),
          process.resourcesPath,
          { recursive: true }
        );
        return true; // Rollback applied
      }
    }
    return false;
  }
}
```

---

## Store-Managed Updates

| Store | Update Mechanism | Review Time | Revenue Share |
|-------|-----------------|-------------|---------------|
| Mac App Store | Automatic via App Store app | 24-48h | 15-30% |
| Microsoft Store | Automatic background | 1-3 business days | 12-15% |
| Flathub | Automatic via GNOME Software | Hours | 0% |
| Snap Store | Automatic (candidate/stable channels) | Hours | 0% |

**Store tradeoffs:**
- ✅ Zero infrastructure, built-in delta, user trust
- ❌ Review delays, sandboxing restrictions, revenue cut, can't force-update

---

## Anti-Patterns

| Anti-Pattern | Impact | Fix |
|--------------|--------|-----|
| HTTP (not HTTPS) for update metadata | MITM delivers malicious update | HTTPS + certificate pinning |
| No signature verification | Any CDN compromise = all users compromised | Ed25519 + SHA-512 verification |
| Overwriting running binary in-place | Crash, corruption, OS file lock errors | Stage in separate directory, replace on restart |
| Forcing restart without user consent | Loss of unsaved work, user rage, 1-star reviews | Dialog, save state, restart gracefully |
| Single update server, no CDN | DDoS or outage = no updates for anyone | CDN with multiple edge locations |
| No rollback mechanism | Bad update = bricked app until manual reinstall | Backup + rollback on startup failure detection |

---

## References

- [Sparkle 2 Documentation](https://sparkle-project.org/documentation/)
- [electron-updater](https://www.electron.build/auto-update)
- [Tauri Updater](https://tauri.app/plugin/updater/)
- [Squirrel.Windows](https://github.com/Squirrel/Squirrel.Windows)
- [bsdiff/courgette (Chromium)](https://chromium.googlesource.com/chromium/src/courgette/)
