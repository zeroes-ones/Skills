# build-ecosystem

Reference documentation for the automation-engineer skill — every build platform with CLI invocations, signing, packaging, CI matrix strategies, and caching patterns.

## iOS

**xcodebuild CLI:**
```bash
xcodebuild -project MyApp.xcodeproj -scheme MyApp -sdk iphoneos \
  -configuration Release -archivePath ./build/MyApp.xcarchive archive

xcodebuild -exportArchive -archivePath ./build/MyApp.xcarchive \
  -exportPath ./build/ipa -exportOptionsPlist ExportOptions.plist
```

**Export method plist (`ExportOptions.plist`):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>teamID</key>
    <string>TEAM123456</string>
    <key>signingStyle</key>
    <string>automatic</string>
</dict>
</plist>
```

**fastlane gym:**
```ruby
lane :build do
  match(type: "appstore", readonly: is_ci)
  gym(
    scheme: "MyApp",
    export_method: "app-store",
    output_directory: "./build",
    include_bitcode: false,
    xcargs: "-allowProvisioningUpdates"
  )
end
```

**Code signing with Match:**
```bash
fastlane match appstore --readonly   # CI: readonly, uses shared certs/profiles
fastlane match nuke appstore         # Reset all certs/profiles
```
Match stores encrypted certs/profiles in a private git repo. CI pulls them read-only via `MATCH_PASSWORD` secret.

**macOS notarization:**
```bash
xcrun notarytool submit MyApp.dmg --apple-id "$APPLE_ID" --team-id "$TEAM_ID" \
  --password "$APP_SPECIFIC_PASSWORD" --wait

xcrun stapler staple MyApp.dmg  # staple the ticket for offline validation
```

## Android

**Gradle build:**
```bash
./gradlew assembleRelease                 # APK
./gradlew bundleRelease                   # Android App Bundle (AAB)
./gradlew testReleaseUnitTest             # unit tests
./gradlew connectedAndroidTest            # instrumentation tests
```

**Build variants (`app/build.gradle.kts`):**
```kotlin
android {
    buildTypes {
        release { isMinifyEnabled = true; proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro") }
        debug { applicationIdSuffix = ".debug"; isDebuggable = true }
    }
    flavorDimensions += "environment"
    productFlavors {
        create("staging") { applicationIdSuffix = ".staging"; dimension = "environment" }
        create("production") { dimension = "environment" }
    }
}
```

**APK signing:**
```bash
apksigner sign --ks keystore.jks --ks-key-alias upload --ks-pass env:KEYSTORE_PASS \
  --out app-release-signed.apk app-release-unsigned.apk

apksigner verify --verbose app-release-signed.apk
```

**fastlane supply (Google Play upload):**
```ruby
lane :deploy_play do
  gradle(task: "bundleRelease")
  supply(
    track: "production",
    release_status: "completed",
    aab: "app/build/outputs/bundle/release/app-release.aab",
    skip_upload_metadata: false,
    skip_upload_images: false,
    skip_upload_screenshots: false
  )
end
```

**CI snippet — Android matrix:**
```yaml
android-build:
  runs-on: ubuntu-latest
  strategy:
    matrix:
      variant: [stagingRelease, productionRelease]
  steps:
    - uses: actions/setup-java@v4
      with: { java-version: '17', distribution: 'temurin' }
    - uses: gradle/actions/setup-gradle@v4
      with: { cache-read-only: '${{ github.ref != ''refs/heads/main'' }}' }
    - run: ./gradlew assemble${{ matrix.variant }}
    - uses: actions/upload-artifact@v4
      with: { name: apk-${{ matrix.variant }}, path: app/build/outputs/apk/${{ matrix.variant }}/*.apk }
```

## Web

| Build Tool | Config | Key Feature |
|-----------|--------|-------------|
| Vite | `vite.config.ts` | ESM-native dev server, Rollup-based prod |
| webpack | `webpack.config.js` | Full control, mature ecosystem |
| Next.js | `next.config.js` | ISR, image optimization, Edge runtime |
| Turborepo | `turbo.json` | Monorepo task orchestration with caching |
| Nx | `nx.json` | Monorepo with dependency graph, affected detection |

**Vite build:**
```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: { output: { manualChunks: { vendor: ['react', 'react-dom'] } } },
    target: 'es2020',
    sourcemap: true,
  },
});
```

**Next.js output standalone:**
```javascript
// next.config.js
module.exports = { output: 'standalone' };
```
```bash
next build && cp -r public .next/standalone/public && cp -r .next/static .next/standalone/.next/static
```

**Turborepo monorepo pipeline:**
```json
// turbo.json
{
  "pipeline": {
    "build": { "dependsOn": ["^build"], "outputs": ["dist/**", ".next/**"] },
    "test": { "dependsOn": ["build"], "outputs": [] },
    "lint": { "outputs": [] },
    "dev": { "cache": false, "persistent": true }
  }
}
```

**Bundle analysis:**
```bash
npx vite-bundle-visualizer         # Vite
npx webpack-bundle-analyzer dist/stats.json  # webpack
ANALYZE=true next build            # Next.js with @next/bundle-analyzer
```

**Tree shaking enforcement:**
```javascript
// package.json — sideEffects flag for tree shaking
{ "sideEffects": ["*.css", "*.scss"] }
```

## macOS Desktop

**DMG packaging:**
```bash
# create-dmg
create-dmg --volname "MyApp" --volicon "icon.icns" \
  --window-pos 200 120 --window-size 800 400 \
  --icon-size 100 --icon "MyApp.app" 200 190 \
  --hide-extension "MyApp.app" --app-drop-link 600 185 \
  "MyApp-1.0.0.dmg" "build/Release/MyApp.app"
```

**Notarization (notarytool):**
```bash
xcrun notarytool submit MyApp.dmg --keychain-profile "AC_PASSWORD" --wait
xcrun stapler staple MyApp.dmg
```

**Sparkle auto-update (AppCast):**
```xml
<!-- appcast.xml -->
<item>
  <title>Version 2.0.0</title>
  <sparkle:version>200</sparkle:version>
  <sparkle:shortVersionString>2.0.0</sparkle:shortVersionString>
  <enclosure url="https://example.com/MyApp-2.0.0.dmg"
    sparkle:edSignature="..." length="12345678" type="application/octet-stream"/>
</item>
```
Use `generate_appcast` from Sparkle to create and sign appcast entries.

## Windows Desktop

**MSI via WiX Toolset:**
```xml
<!-- WiX .wxs fragment -->
<DirectoryRef Id="INSTALLFOLDER">
  <Component Id="MainExecutable" Guid="*">
    <File Id="MyAppExe" Source="build\MyApp.exe" KeyPath="yes" />
  </Component>
</DirectoryRef>
```
```bash
candle MyApp.wxs -out build/ && light build/MyApp.wixobj -out dist/MyApp.msi -ext WixUIExtension
```

**MSIX packaging:**
```bash
# Using MSIX Packaging Tool or makeappx.exe
makeappx pack /d build/MyApp /p MyApp.msix /l
```

**Squirrel auto-updater:**
```javascript
// electron-forge Squirrel.Windows config
module.exports = {
  makers: [{
    name: '@electron-forge/maker-squirrel',
    config: {
      remoteReleases: 'https://updates.example.com/',
      iconUrl: 'https://example.com/icon.ico',
    },
  }],
};
```

## Linux Desktop

**AppImage:**
```bash
# appimagetool
mkdir -p AppDir/usr/bin && cp myapp AppDir/usr/bin/
cp myapp.desktop AppDir/ && cp myapp.png AppDir/
appimagetool AppDir MyApp-x86_64.AppImage
```

**Snap (snapcraft):**
```yaml
# snap/snapcraft.yaml
name: myapp
version: '1.0.0'
base: core24
apps:
  myapp:
    command: bin/myapp
    plugs: [network, home, desktop]
parts:
  myapp:
    plugin: cmake
    source: .
    build-snaps: [gtk-common-themes]
```
```bash
snapcraft --use-lxd && snapcraft upload *.snap
```

**Flatpak (flatpak-builder):**
```json
// org.example.MyApp.json
{
  "app-id": "org.example.MyApp",
  "runtime": "org.gnome.Platform",
  "runtime-version": "46",
  "sdk": "org.gnome.Sdk",
  "command": "myapp",
  "finish-args": ["--socket=wayland", "--socket=fallback-x11", "--share=network"],
  "modules": [{
    "name": "myapp",
    "buildsystem": "meson",
    "sources": [{ "type": "archive", "url": "https://example.com/myapp-1.0.tar.gz" }]
  }]
}
```
```bash
flatpak-builder build-dir org.example.MyApp.json --force-clean
flatpak build-export repo build-dir && flatpak build-bundle repo myapp.flatpak org.example.MyApp
```

**.deb / .rpm via fpm:**
```bash
fpm -s dir -t deb -n myapp -v 1.0.0 \
  --prefix /usr/local bin/myapp=/usr/local/bin/myapp \
  --depends libssl3
```

## Electron

**electron-builder (recommended):**
```jsonc
// electron-builder.yml
appId: com.example.myapp
mac:
  category: public.app-category.developer-tools
  target: [dmg, zip]
  hardenedRuntime: true
  entitlements: build/entitlements.mac.plist
  notarize: { teamId: "TEAM123" }
win:
  target: [nsis, portable]
  certificateFile: build/cert.pfx
  certificatePassword: $WINDOWS_SIGN_PASSWORD
linux:
  target: [AppImage, deb, rpm]
  category: Development
publish:
  provider: github
```
```bash
npx electron-builder --mac --win --linux --publish always
```

**Code signing (macOS entitlements):**
```xml
<!-- entitlements.mac.plist -->
<key>com.apple.security.cs.allow-unsigned-executable-memory</key><true/>
<key>com.apple.security.cs.disable-library-validation</key><true/>
<key>com.apple.security.device.audio-input</key><true/>
```

**autoUpdater (electron-updater):**
```typescript
import { autoUpdater } from 'electron-updater';
autoUpdater.setFeedURL({ provider: 'github', owner: 'user', repo: 'myapp' });
autoUpdater.checkForUpdatesAndNotify();
```

## Tauri

**tauri-cli build:**
```bash
cargo install tauri-cli
cargo tauri build --target aarch64-apple-darwin  # macOS Apple Silicon
cargo tauri build --target x86_64-pc-windows-msvc # Windows
```

**Tauri config signing:**
```json
// tauri.conf.json
{
  "bundle": {
    "active": true,
    "targets": "all",
    "macOS": { "signingIdentity": "Apple Distribution: ..." },
    "windows": { "certificateThumbprint": "A1B2C3...", "digestAlgorithm": "sha256" }
  },
  "plugins": {
    "updater": {
      "endpoints": ["https://releases.example.com/{{target}}/{{current_version}}"],
      "pubkey": "dW50cnVzdGVkIGNvbW1lbnQ6IG1pbmlzaWdu..."
    }
  }
}
```

```bash
# Sign after build
tauri signer sign --private-key ~/.tauri/myapp.key --password env:TAURI_KEY_PASS generated-msi.msi
```

## Flutter

**Platform builds:**
```bash
flutter build ios --release --no-codesign      # iOS IPA (unsigned)
flutter build appbundle --release              # Android AAB
flutter build apk --release --split-per-abi    # Android split APKs
flutter build web --release --wasm             # Web with WASM
flutter build macos --release                  # macOS
flutter build windows --release                # Windows
flutter build linux --release                  # Linux
```

**fastlane integration:**
```ruby
lane :flutter_build do
  sh("flutter clean && flutter pub get")
  sh("flutter build ipa --release --export-method app-store")
  sh("flutter build appbundle --release")
end
```

**iOS code signing for Flutter:**
```bash
# Use Match via fastlane
fastlane match appstore --readonly
flutter build ios --release
```

## React Native

**Platform builds:**
```bash
# iOS
cd ios && xcodebuild -workspace MyApp.xcworkspace -scheme MyApp \
  -configuration Release -archivePath build/MyApp.xcarchive archive

# Android
cd android && ./gradlew assembleRelease
```

**Hermes compilation:**
```javascript
// android/app/build.gradle
project.ext.react = [
    enableHermes: true,  // Hermes bytecode precompilation
    hermesFlagsRelease: ["-O", "-output-source-map"],
]
```
```bash
npx react-native bundle --platform ios --dev false \
  --entry-file index.js --bundle-output ios/main.jsbundle \
  --assets-dest ios --hermes-engine
```

**fastlane for RN:**
```ruby
lane :build_both do
  ios_build && android_build
end
```

## Game Engines

**Unity CLI build:**
```bash
unity -quit -batchmode -nographics \
  -projectPath . \
  -buildTarget iOS \
  -executeMethod BuildCommand.PerformBuild \
  -logFile build.log

# BuildCommand.cs
static void PerformBuild() {
    BuildPipeline.BuildPlayer(GetScenes(), "Build/iOS",
        BuildTarget.iOS, BuildOptions.None);
}
```

**Unreal Automation Tool (UAT):**
```bash
RunUAT.bat BuildCookRun \
  -project=MyProject.uproject \
  -platform=Win64 -clientconfig=Shipping \
  -cook -stage -pak -archive -archivedirectory=Build/Win64
```

**Console certification checklist:**
- Platform-specific TRCs/XR (Technical Requirement Checklist / Xbox Requirements)
- Age rating submission (ESRB, PEGI, IARC)
- Platform compliance tests (lotcheck)
- Store metadata, screenshots, trailers per platform spec

## CI Pipeline YAML by Platform Category

**iOS + macOS CI matrix:**
```yaml
apple-build:
  strategy:
    matrix:
      scheme: [MyApp-iOS, MyApp-macOS]
      config: [Release, Debug]
  runs-on: macos-15
  steps:
    - uses: actions/checkout@v4
    - run: fastlane match appstore --readonly
      env: { MATCH_PASSWORD: '${{ secrets.MATCH_PASSWORD }}' }
    - run: xcodebuild -scheme ${{ matrix.scheme }} -configuration ${{ matrix.config }} build | xcbeautify
```

**Android CI:**
```yaml
android-build:
  strategy:
    matrix:
      variant: [stagingRelease, productionRelease, debug]
  runs-on: ubuntu-latest
  steps:
    - uses: actions/setup-java@v4
      with: { java-version: '17', distribution: 'temurin' }
    - uses: gradle/actions/setup-gradle@v4
    - run: ./gradlew assemble${{ matrix.variant }}
```

**Web CI:**
```yaml
web-build:
  strategy:
    matrix:
      framework: [vite, nextjs]
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with: { node-version: '20', cache: 'npm' }
    - run: npm ci
    - run: npm run build
    - uses: actions/upload-artifact@v4
      with: { name: web-${{ matrix.framework }}, path: dist/ }
```

**Linux desktop matrix:**
```yaml
linux-package:
  strategy:
    matrix:
      format: [appimage, deb, rpm, snap, flatpak]
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - if: matrix.format == 'appimage'
      run: appimagetool AppDir MyApp.AppImage
    - if: matrix.format == 'snap'
      run: snapcraft --use-lxd
    - if: matrix.format == 'flatpak'
      run: flatpak-builder build-dir org.example.MyApp.json
    - if: matrix.format == 'deb'
      run: fpm -s dir -t deb -n myapp -v 1.0.0 bin/=/usr/local/bin
    - if: matrix.format == 'rpm'
      run: fpm -s dir -t rpm -n myapp -v 1.0.0 bin/=/usr/local/bin
```

**Cross-platform matrix (Electron/Tauri):**
```yaml
cross-platform-build:
  strategy:
    matrix:
      include:
        - os: macos-15
          target: mac
          artifact: '*.dmg *.zip'
        - os: windows-latest
          target: win
          artifact: '*.exe *.msi'
        - os: ubuntu-latest
          target: linux
          artifact: '*.AppImage *.deb *.rpm'
  runs-on: ${{ matrix.os }}
  steps:
    - uses: actions/checkout@v4
    - if: matrix.os == 'macos-15'
      run: security unlock-keychain -p '${{ secrets.KEYCHAIN_PASS }}' login.keychain
    - run: npx electron-builder --${{ matrix.target }} --publish never
    - uses: actions/upload-artifact@v4
      with: { name: release-${{ matrix.target }}, path: dist/${{ matrix.artifact }} }
```

## Caching Strategies per Platform

**iOS (derived data + SPM + CocoaPods):**
```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/Library/Developer/Xcode/DerivedData
      ~/Library/Caches/org.swift.swiftpm
      Pods
    key: apple-${{ runner.os }}-${{ hashFiles('*.xcworkspace', 'Podfile.lock', 'Package.resolved') }}
```

**Android (Gradle):**
```yaml
- uses: gradle/actions/setup-gradle@v4
  with:
    cache-read-only: '${{ github.ref != ''refs/heads/main'' }}'
```

**Node.js (npm/pnpm/yarn):**
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # auto-detects package-lock
```

**Rust (Tauri, CLI tools):**
```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/registry
      ~/.cargo/git
      target
    key: cargo-${{ runner.os }}-${{ hashFiles('Cargo.lock') }}
```

**Flutter:**
```yaml
- uses: subosito/flutter-action@v2
  with: { flutter-version: '3.24', cache: true }
```

**Docker buildkit cache:**
```yaml
- uses: docker/setup-buildx-action@v3
- uses: docker/build-push-action@v6
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```
