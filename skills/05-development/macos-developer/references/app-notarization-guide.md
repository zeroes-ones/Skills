# macOS App Notarization Guide

<!-- STANDARD: 3min -- end-to-end notarization pipeline for direct distribution -->

## What Notarization Does

Notarization is Apple's automated malware scanning service. It checks your app for:
- Malicious content (known malware signatures)
- Code signing integrity (all binaries signed, no tampering)
- Hardened Runtime compliance (if enabled)
- Sandbox violations (if sandboxed)

After notarization, Gatekeeper allows your app to launch without the "unidentified developer" warning. **Users no longer need to right-click > Open.**

---

## Prerequisites

1. **Apple Developer Program membership** ($99/year)
2. **Developer ID Application certificate** in your keychain (`security find-identity -v -p basic`)
3. **App-specific password** for your Apple ID (appleid.apple.com → Sign-In and Security → App-Specific Passwords)
4. **Xcode 13+** (for `notarytool`; replaces deprecated `altool`)

### Store Credentials

```bash
# Store notarization credentials in keychain (do this ONCE)
xcrun notarytool store-credentials "NOTARY_PROFILE" \
  --apple-id "dev@example.com" \
  --team-id "YOUR_TEAM_ID" \
  --password "@keychain:AC_PASSWORD"
```

---

## The Full Notarization Pipeline

### Step 1: Archive the App

```bash
xcodebuild archive \
  -project YourApp.xcodeproj \
  -scheme YourApp \
  -configuration Release \
  -archivePath build/YourApp.xcarchive \
  CODE_SIGN_IDENTITY="Developer ID Application: Your Name (TEAMID)" \
  DEVELOPMENT_TEAM=YOUR_TEAM_ID \
  OTHER_CODE_SIGN_FLAGS="--options=runtime --timestamp"
```

### Step 2: Export the .app Bundle

```bash
# Create a copy for notarization (don't modify the archive directly)
cp -R build/YourApp.xcarchive/Products/Applications/YourApp.app build/YourApp.app
```

### Step 3: Verify Code Signing

```bash
# Verify the app is properly signed
codesign -dvvv build/YourApp.app

# Look for:
#   Authority=Developer ID Application: Your Name (TEAMID)
#   TeamIdentifier=YOUR_TEAM_ID
#   flags=0x10000(runtime)   <- CRITICAL: Hardened Runtime must be enabled

# Verify all nested binaries are signed
codesign --verify --deep --strict --verbose=2 build/YourApp.app
```

### Step 4: Create a ZIP for Submission

```bash
# notarytool requires a ZIP, PKG, or DMG — not a .app bundle
ditto -c -k --keepParent build/YourApp.app build/YourApp.zip
```

### Step 5: Submit for Notarization

```bash
xcrun notarytool submit build/YourApp.zip \
  --keychain-profile "NOTARY_PROFILE" \
  --wait
```

Expected output:
```
Processing complete
  id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
  status: Accepted
```

### Step 6: Staple the Ticket

Notarization creates a ticket on Apple's servers. **Stapling** embeds that ticket in your app so Gatekeeper can verify it offline.

```bash
xcrun stapler staple build/YourApp.app
# Output: "Processing: /path/to/YourApp.app"
#         "The staple and validate action worked!"
```

### Step 7: Verify Gatekeeper Acceptance

```bash
spctl -a -v build/YourApp.app
# Expected: "build/YourApp.app: accepted"
#           "source=Notarized Developer ID"

# Also check:
stapler validate build/YourApp.app
```

### Step 8: Package for Distribution

```bash
# Create a DMG with the stapled app
hdiutil create -volname "YourApp" \
  -srcfolder build/YourApp.app \
  -ov -format UDZO \
  build/YourApp.dmg

# Sign the DMG itself
codesign --sign "Developer ID Application: Your Name (TEAMID)" \
  --timestamp build/YourApp.dmg

# Notarize the DMG too (users download the DMG, not the .zip)
xcrun notarytool submit build/YourApp.dmg \
  --keychain-profile "NOTARY_PROFILE" \
  --wait
xcrun stapler staple build/YourApp.dmg
```

---

## Common Notarization Failures

### Error: "The binary is not signed with a Developer ID certificate"

**Cause**: App signed with "Apple Development" or "Mac Developer" cert instead of "Developer ID Application."
**Fix**: `CODE_SIGN_IDENTITY="Developer ID Application: Your Name (TEAMID)"`

### Error: "The binary uses an SDK older than 10.9"

**Cause**: App linked against a pre-10.9 SDK. Notarization requires macOS 10.9+ SDK.
**Fix**: Set `MACOSX_DEPLOYMENT_TARGET = 10.13` or later in your xcconfig.

### Error: "The executable does not have the Hardened Runtime capability"

**Cause**: Missing `com.apple.security.hardened-runtime` entitlement or `--options=runtime` flag during signing.
**Fix**: Add the entitlement to your `.entitlements` file AND pass `OTHER_CODE_SIGN_FLAGS="--options=runtime --timestamp"` during archive.

### Error: "The signature algorithm must be SHA-256"

**Cause**: Binary signed with SHA-1 instead of SHA-256.
**Fix**: Add `OTHER_CODE_SIGN_FLAGS="--digest-algorithm=sha256"` or ensure Xcode 13+ is used (defaults to SHA-256).

### Error: "The executable contains bitcode but the Hardened Runtime is not enabled"

**Cause**: Bitcode enabled in build settings but Hardened Runtime missing.
**Fix**: Either disable bitcode (`ENABLE_BITCODE = NO`) or enable Hardened Runtime.

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Notarize
on:
  push:
    tags: ['v*']
jobs:
  notarize:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      - name: Import signing certificate
        env:
          DEV_ID_CERT: \${{ secrets.DEVELOPER_ID_CERT_BASE64 }}
          DEV_ID_PASS: \${{ secrets.DEVELOPER_ID_CERT_PASSWORD }}
        run: |
          echo "\$DEV_ID_CERT" | base64 --decode > dev_id.p12
          security import dev_id.p12 -k ~/Library/Keychains/login.keychain-db -P "\$DEV_ID_PASS" -T /usr/bin/codesign
          security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k "" ~/Library/Keychains/login.keychain-db
      - name: Archive and Notarize
        env:
          NOTARY_PASSWORD: \${{ secrets.NOTARY_PASSWORD }}
        run: |
          xcodebuild archive -project YourApp.xcodeproj -scheme YourApp \
            -archivePath build/YourApp.xcarchive \
            CODE_SIGN_IDENTITY="Developer ID Application" \
            OTHER_CODE_SIGN_FLAGS="--options=runtime --timestamp"
          ditto -c -k --keepParent build/YourApp.xcarchive/Products/Applications/YourApp.app build/YourApp.zip
          xcrun notarytool submit build/YourApp.zip \
            --apple-id "dev@example.com" --team-id "TEAMID" \
            --password "\$NOTARY_PASSWORD" --wait
          xcrun stapler staple build/YourApp.xcarchive/Products/Applications/YourApp.app
```

### Fastlane Integration

```ruby
lane :notarize do
  build_mac_app(
    scheme: "YourApp",
    codesigning_identity: "Developer ID Application",
    export_method: "developer-id"
  )
  notarize(
    package: "YourApp.pkg",
    apple_id: ENV["NOTARY_APPLE_ID"],
    team_id: ENV["NOTARY_TEAM_ID"]
  )
end
```

---

## Notarization Timing

| Phase | Typical Duration |
|---|---|
| ZIP creation | 10-60 seconds (depends on app size) |
| Upload to Apple | 30-120 seconds |
| Notarization scan | 1-5 minutes (Apple automated scan) |
| Staple ticket | < 1 second |
| **Total pipeline** | **3-7 minutes** |

If notarization takes >15 minutes, check your network connection or Apple's system status.
