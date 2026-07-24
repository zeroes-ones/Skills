---
name: desktop-installer-packaging
description: Complete guide to packaging desktop applications — NSIS, WiX, MSIX, DMG, AppImage, Flatpak, snap, code signing, notarization, and store submission across Windows, macOS, and Linux.
author: Sandeep Kumar Penchala
---

# Desktop Installer Packaging

The installer is the first experience every user has with your application. A confusing installer with unsigned binaries triggers OS security warnings that cause 60%+ of potential users to abandon. This reference covers installer packaging for all major platforms with code signing and distribution.

---

## 1. Universal Packaging Requirements

| Platform | Signing Required | Notarization | Store Option | Enterprise |
|----------|-----------------|--------------|--------------|------------|
| Windows | Authenticode (EV recommended) | N/A | Microsoft Store (MSIX) | MSI via Intune/GPO |
| macOS | Apple Developer ID | Required (notarytool) | Mac App Store | MDM (Jamf) |
| Linux | GPG (optional, recommended) | N/A | Snap Store, Flathub | Custom repos |

## 2. Windows: NSIS (electron-builder)

### 2.1 Configuration

```yaml
# electron-builder.yml
win:
  target:
    - target: nsis
      arch:
        - x64
        - arm64
  icon: build/icon.ico
  certificateFile: certs/code-signing.pfx
  certificatePassword: ${CSC_KEY_PASSWORD}
  signingHashAlgorithms:
    - sha256

nsis:
  oneClick: false
  perMachine: true
  allowToChangeInstallationDirectory: true
  createDesktopShortcut: true
  createStartMenuShortcut: true
  shortcutName: MyApp
  installerIcon: build/icon.ico
  uninstallerIcon: build/icon.ico
  installerHeaderIcon: build/icon.ico
  license: LICENSE.txt
  include: build/installer.nsh
```

### 2.2 Custom NSIS Script

```nsis
; build/installer.nsh
!macro customInstall
  ; Register file associations
  WriteRegStr HKCR ".myapp" "" "MyApp.Project"
  WriteRegStr HKCR "MyApp.Project" "" "MyApp Project File"
  WriteRegStr HKCR "MyApp.Project\DefaultIcon" "" "$INSTDIR\MyApp.exe,1"
  WriteRegStr HKCR "MyApp.Project\shell\open\command" "" '"$INSTDIR\MyApp.exe" "%1"'

  ; Register custom protocol
  WriteRegStr HKCR "myapp" "" "URL:MyApp Protocol"
  WriteRegStr HKCR "myapp" "URL Protocol" ""
  WriteRegStr HKCR "myapp\shell\open\command" "" '"$INSTDIR\MyApp.exe" "%1"'

  ; Install VC++ redistributable if needed
  ExecWait '"$INSTDIR\vc_redist.x64.exe" /quiet /norestart'
!macroend

!macro customUninstall
  DeleteRegKey HKCR ".myapp"
  DeleteRegKey HKCR "MyApp.Project"
  DeleteRegKey HKCR "myapp"
!macroend
```

### 2.3 Windows Code Signing

```bash
# Sign with EV certificate (CI)
signtool sign /fd SHA256 \
  /f certs/code-signing.pfx \
  /p $env:CSC_KEY_PASSWORD \
  /tr http://timestamp.digicert.com \
  /td SHA256 \
  /v \
  dist/MyApp-Setup.exe

# Verify signature
signtool verify /pa /v dist/MyApp-Setup.exe

# Dual sign (SHA1 + SHA256) for Windows 7 compatibility
signtool sign /fd SHA1 /f cert.pfx /p pass /t http://timestamp.digicert.com dist/app.exe
signtool sign /fd SHA256 /f cert.pfx /p pass /tr http://timestamp.digicert.com /td SHA256 /as dist/app.exe
```

## 3. Windows: WiX Toolset (.msi)

### 3.1 WiX for Enterprise Deployment

WiX produces `.msi` installers compatible with Group Policy deployment:

```xml
<!-- installer.wxs -->
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" Name="MyApp" Language="1033" Version="2.0.0"
           Manufacturer="MyCompany" UpgradeCode="GUID-HERE">
    <Package InstallerVersion="500" Compressed="yes"
             InstallScope="perMachine"
             Comments="MyApp Installer" />

    <MajorUpgrade DowngradeErrorMessage="A newer version is already installed." />

    <MediaTemplate EmbedCab="yes" />

    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFiles64Folder">
        <Directory Id="APPLICATIONFOLDER" Name="MyApp">
          <Component Id="MainExecutable" Guid="*">
            <File Id="MyAppExe" Source="MyApp.exe" KeyPath="yes" />
          </Component>
          <Component Id="AppShortcut" Guid="*">
            <Shortcut Id="StartMenuShortcut" Name="MyApp"
                      Directory="ProgramMenuFolder"
                      WorkingDirectory="APPLICATIONFOLDER"
                      Advertise="yes" />
            <Shortcut Id="DesktopShortcut" Name="MyApp"
                      Directory="DesktopFolder"
                      WorkingDirectory="APPLICATIONFOLDER"
                      Advertise="yes" />
            <RegistryValue Root="HKCU"
                           Key="Software\MyCompany\MyApp"
                           Name="installed" Value="1" Type="integer"
                           KeyPath="yes" />
          </Component>
        </Directory>
      </Directory>
    </Directory>

    <Feature Id="Complete" Level="1">
      <ComponentRef Id="MainExecutable" />
      <ComponentRef Id="AppShortcut" />
    </Feature>
  </Product>
</Wix>
```

### 3.2 Building MSI

```bash
# Compile WiX source
candle installer.wxs -out installer.wixobj

# Link to MSI
light installer.wixobj -out MyApp.msi -ext WixUIExtension

# Sign MSI
signtool sign /fd SHA256 /f cert.pfx /p pass /tr http://timestamp.digicert.com /td SHA256 MyApp.msi
```

## 4. Windows: MSIX (Microsoft Store)

```xml
<!-- AppxManifest.xml -->
<?xml version="1.0" encoding="utf-8"?>
<Package xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
         xmlns:desktop="http://schemas.microsoft.com/appx/manifest/desktop/windows10">
  <Identity Name="MyCompany.MyApp" Publisher="CN=PublisherName"
            Version="2.0.0.0" ProcessorArchitecture="x64" />
  <Properties>
    <DisplayName>MyApp</DisplayName>
    <PublisherDisplayName>MyCompany</PublisherDisplayName>
    <Logo>Assets\StoreLogo.png</Logo>
  </Properties>
  <Applications>
    <Application Id="MyApp" Executable="MyApp.exe"
                 EntryPoint="Windows.FullTrustApplication">
      <desktop:Extension Category="windows.startupTask"
                         Executable="MyApp.exe"
                         EntryPoint="Windows.FullTrustApplication" />
    </Application>
  </Applications>
</Package>
```

## 5. macOS: DMG + Notarization

### 5.1 DMG Configuration

```yaml
# electron-builder.yml
mac:
  target:
    - target: dmg
      arch:
        - x64
        - arm64
    - target: zip
      arch:
        - x64
        - arm64
  icon: build/icon.icns
  category: public.app-category.productivity
  entitlements: build/entitlements.mac.plist
  entitlementsInherit: build/entitlements.mac.plist
  hardenedRuntime: true
  gatekeeperAssess: false

dmg:
  title: MyApp ${version}
  icon: build/icon.icns
  background: build/dmg-background.png
  contents:
    - x: 130
      y: 220
    - x: 410
      y: 220
      type: link
      path: /Applications
  window:
    width: 540
    height: 380
```

### 5.2 Entitlements

```xml
<!-- build/entitlements.mac.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>com.apple.security.cs.allow-jit</key>
  <true/>
  <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
  <true/>
  <key>com.apple.security.cs.disable-library-validation</key>
  <true/>
  <key>com.apple.security.device.audio-input</key>
  <true/>
  <key>com.apple.security.network.client</key>
  <true/>
  <key>com.apple.security.files.user-selected.read-write</key>
  <true/>
</dict>
</plist>
```

### 5.3 Notarization

```bash
# Submit for notarization
xcrun notarytool submit MyApp.dmg \
  --apple-id "$APPLE_ID" \
  --team-id "$APPLE_TEAM_ID" \
  --password "$APPLE_APP_SPECIFIC_PASSWORD" \
  --wait

# Check notarization status
xcrun notarytool log <submission-id> \
  --apple-id "$APPLE_ID" \
  --team-id "$APPLE_TEAM_ID" \
  --password "$APPLE_APP_SPECIFIC_PASSWORD"

# Staple notarization ticket to app
xcrun stapler staple MyApp.dmg

# Verify
spctl -a -v MyApp.dmg
# Should print: "MyApp.dmg: accepted"
```

## 6. Linux: AppImage, deb, rpm, Flatpak, snap

### 6.1 AppImage

```yaml
# electron-builder.yml
linux:
  target:
    - target: AppImage
      arch:
        - x64
        - arm64
    - target: deb
      arch:
        - x64
    - target: rpm
      arch:
        - x64
  icon: build/icon.png
  category: Utility
  maintainer: support@myapp.com
```

### 6.2 Flatpak Manifest

```yaml
# com.myapp.MyApp.yml
app-id: com.myapp.MyApp
runtime: org.freedesktop.Platform
runtime-version: '23.08'
sdk: org.freedesktop.Sdk
command: myapp
finish-args:
  - --socket=x11
  - --socket=wayland
  - --share=ipc
  - --share=network
  - --filesystem=home
modules:
  - name: myapp
    buildsystem: simple
    build-commands:
      - cp -R * /app/
    sources:
      - type: file
        path: MyApp-2.0.0.tar.gz
```

### 6.3 GPG Signing (Linux)

```bash
# Sign .deb package
dpkg-sig --sign builder MyApp_2.0.0_amd64.deb

# Sign .rpm package
rpm --addsign MyApp-2.0.0.x86_64.rpm

# Sign AppImage with GPG
gpg --detach-sign --armor MyApp-2.0.0.AppImage
```

## 7. CI/CD Integration

### 7.1 GitHub Actions — Multi-Platform Build

```yaml
name: Build & Sign
on:
  push:
    tags: ['v*']

jobs:
  build:
    strategy:
      matrix:
        os: [macos-13, macos-14, windows-2022, ubuntu-22.04]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci

      - name: Build & Package
        run: npm run build
        env:
          CSC_LINK: ${{ secrets.CSC_LINK }}
          CSC_KEY_PASSWORD: ${{ secrets.CSC_KEY_PASSWORD }}
          APPLE_ID: ${{ secrets.APPLE_ID }}
          APPLE_APP_SPECIFIC_PASSWORD: ${{ secrets.APPLE_APP_SPECIFIC_PASSWORD }}
          APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}

      - name: Verify Signatures
        if: runner.os == 'Windows'
        run: signtool verify /pa dist/*.exe
        if: runner.os == 'macOS'
        run: |
          spctl -a -v dist/*.app
          pkgutil --check-signature dist/*.pkg

      - name: Upload Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.os }}
          path: dist/*
```

## 8. Distribution Checklist

- [ ] Windows: NSIS .exe built and Authenticode signed (EV certificate)
- [ ] Windows: WiX .msi built for enterprise GPO deployment
- [ ] Windows: Verified with `signtool verify /pa`
- [ ] macOS: .dmg built and notarized
- [ ] macOS: Notarization stapled (`xcrun stapler staple`)
- [ ] macOS: Verified with `spctl -a -v`
- [ ] Linux: .AppImage, .deb, .rpm built
- [ ] Linux: GPG signatures for all packages
- [ ] All installers tested on clean VM (fresh OS install, no dev tools)
- [ ] File associations work after install
- [ ] Uninstaller cleans up all files and registry entries
- [ ] Silent install works (`/S` for NSIS, `installer -q` for MSI)
