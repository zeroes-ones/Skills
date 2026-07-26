# distribution-channels

Reference documentation for the automation-engineer skill — every distribution channel with authentication, CI pipeline snippets, CLI invocations, common failure modes, and recovery procedures.

## App Store Connect (Apple — iOS, iPadOS, watchOS, tvOS, macOS, visionOS)

**Authentication:**
```bash
# App Store Connect API key (preferred for CI)
fastlane spaceauth -u user@example.com      # generate session cookie (legacy)
app_store_connect_api_key(
  key_id: "ABC1234567",
  issuer_id: "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
  key_filepath: "./AuthKey_ABC1234567.p8",
  duration: 1200,  # token TTL in seconds (max 20 min)
  in_house: false
)
```

**fastlane deliver — metadata & screenshots:**
```ruby
lane :deliver_metadata do
  deliver(
    username: "user@example.com",
    app_identifier: "com.example.app",
    force: true,
    overwrite_screenshots: true,
    skip_binary_upload: true,
    phased_release: true,
    automatic_release: false
  )
end
```

**TestFlight upload with fastlane pilot:**
```ruby
lane :testflight do
  build_app(scheme: "MyApp")
  upload_to_testflight(
    skip_waiting_for_build_processing: false,
    apple_id: "1234567890",
    distribute_external: true,
    groups: ["Beta Testers", "Internal QA"],
    changelog: read_changelog,
    notify_external_testers: true
  )
end
```

**CI pipeline (GitHub Actions — App Store):**
```yaml
- name: Deploy to TestFlight
  env:
    APP_STORE_CONNECT_API_KEY_KEY_ID: ${{ secrets.ASC_KEY_ID }}
    APP_STORE_CONNECT_API_KEY_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
    APP_STORE_CONNECT_API_KEY_KEY: ${{ secrets.ASC_KEY_P8 }}
    MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
  run: bundle exec fastlane testflight
```

**Common failure modes & recovery:**
| Failure | Cause | Recovery |
|---------|-------|----------|
| `ITC.apps.tf.build.processing.failed` | Binary rejected by Apple processing | Check email for specifics, fix plist/entitlements, re-upload |
| `ERROR: No provisioning profile found` | Match hasn't synced or profile expired | `fastlane match nuke development && fastlane match development` |
| `90238: Invalid Bundle` | Wrong deployment target or missing entitlement | Validate `Info.plist` minimum version, check entitlements file |
| `API key expired` | Token TTL exceeded | Regenerate via `app_store_connect_api_key` with fresh token |
| `ITC.apps.tf.build.preview.invalid` | Screenshot dimensions wrong | Run `fastlane frameit` to generate correct sizes per device |

## Google Play Console (Android — phone, tablet, Wear OS, TV, Automotive)

**Authentication:**
```bash
# Service account JSON key (download from Google Cloud Console)
# Enable "Google Play Android Developer API" in GCP project
# Invite service account email to Play Console with "Admin" role
export SUPPLY_JSON_KEY="/path/to/service-account.json"
```

**fastlane supply — upload & rollout:**
```ruby
lane :deploy_play do
  gradle(task: "bundleRelease")
  supply(
    track: "production",
    release_status: "completed",   # "draft" to hold for manual review
    rollout: "0.25",               # staged rollout: 25%, null = full
    version_name: "2.4.0",
    aab: "app/build/outputs/bundle/release/app-release.aab",
    validate_only: false,
    skip_upload_apk: true,         # AAB only
    skip_upload_images: true,
    skip_upload_screenshots: true
  )
end
```

**Promoting between tracks:**
```ruby
supply(
  track: "internal",        # internal / alpha / beta / production
  track_promote_to: "beta",
  version_code: 123         # promote specific version
)
```

**Staged rollout management:**
```bash
# fastlane
bundle exec fastlane supply --track production --rollout 0.50  # increase to 50%

# Direct API (google-play-android-developer v3)
curl -X PUT "https://androidpublisher.googleapis.com/androidpublisher/v3/applications/com.example.app/edits/${EDIT_ID}/tracks/production" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -d '{"track":"production","releases":[{"versionCodes":["123"],"userFraction":0.50}]}'
```

**In-app reviews API automation note:** Review prompts are client-side, not distributable via CI. Use Remote Config or Firebase to toggle the prompt window.

**CI pipeline (GitHub Actions — Play Store):**
```yaml
- name: Deploy to Play Store
  env:
    SUPPLY_JSON_KEY_DATA: ${{ secrets.PLAY_STORE_SERVICE_ACCOUNT_JSON }}
  run: |
    echo "$SUPPLY_JSON_KEY_DATA" > /tmp/play-store-key.json
    bundle exec fastlane deploy_play
```

**Common failure modes & recovery:**
| Failure | Cause | Recovery |
|---------|-------|----------|
| `googleapiclient.errors.HttpError 403` | Service account lacks permissions | Re-invite service account email to Play Console with Admin |
| `versionCode 123 already exists` | Duplicate version code in AAB | Increment `versionCode` in `build.gradle.kts`, rebuild |
| `APK signature scheme v2/v3 missing` | Unsigned or incorrectly signed | Verify `signingConfig signingConfigs.release` in build.gradle |
| `rollout halted` | User crash rate threshold exceeded | Fix crash, upload new AAB with higher versionCode, resume |

## Chrome Web Store

**Authentication — OAuth2 setup:**
```bash
npm install -g chrome-webstore-upload-cli

# 1. Go to https://console.cloud.google.com/apis/credentials
# 2. Create OAuth 2.0 Client ID (Desktop app)
# 3. Enable "Chrome Web Store API"
# 4. Run:
chrome-webstore-upload-cli refresh-token \
  --client-id $CLIENT_ID \
  --client-secret $CLIENT_SECRET
# Paste the auth code from browser — outputs refresh_token
```

**Upload and publish:**
```bash
export EXTENSION_ID="abcdefghijklmnopqrstuvwxyz123456"
export CLIENT_ID="123456789012-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com"
export CLIENT_SECRET="GOCSPX-xxxxxxxxxxxxxxxxxxxx"
export REFRESH_TOKEN="1//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Upload new version
chrome-webstore-upload-cli upload \
  --source extension.zip \
  --extension-id $EXTENSION_ID \
  --client-id $CLIENT_ID \
  --client-secret $CLIENT_SECRET \
  --refresh-token $REFRESH_TOKEN

# Publish (draft → published)
chrome-webstore-upload-cli publish \
  --extension-id $EXTENSION_ID \
  --client-id $CLIENT_ID \
  --client-secret $CLIENT_SECRET \
  --refresh-token $REFRESH_TOKEN
```

**Manifest v3 minimum (`manifest.json`):**
```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0.0",
  "description": "Description (max 132 chars)",
  "permissions": ["storage"],
  "host_permissions": ["https://*.example.com/*"],
  "action": {
    "default_popup": "popup.html",
    "default_icon": { "16": "icon16.png", "48": "icon48.png", "128": "icon128.png" }
  },
  "background": { "service_worker": "background.js" }
}
```

**CI pipeline (GitHub Actions):**
```yaml
- name: Publish to Chrome Web Store
  run: |
    npm ci
    npm run build
    cd dist && zip -r ../extension.zip .
    npx chrome-webstore-upload-cli upload --source ../extension.zip \
      --extension-id ${{ secrets.CHROME_EXTENSION_ID }} \
      --client-id ${{ secrets.CHROME_CLIENT_ID }} \
      --client-secret ${{ secrets.CHROME_CLIENT_SECRET }} \
      --refresh-token ${{ secrets.CHROME_REFRESH_TOKEN }}
    npx chrome-webstore-upload-cli publish \
      --extension-id ${{ secrets.CHROME_EXTENSION_ID }} \
      --client-id ${{ secrets.CHROME_CLIENT_ID }} \
      --client-secret ${{ secrets.CHROME_CLIENT_SECRET }} \
      --refresh-token ${{ secrets.CHROME_REFRESH_TOKEN }}
```

**Common failure modes & recovery:**
| Failure | Cause | Recovery |
|---------|-------|----------|
| `invalid_grant` | Refresh token expired/revoked | Re-run `refresh-token` to obtain new refresh token |
| `PKG_INVALID` | ZIP structure wrong | Ensure manifest.json is in ZIP root, not a subfolder |
| `MANIFEST_PERMISSION_WARNING` | New sensitive permission added | Must publish manually first time; subsequent updates automated |
| Review takes > 3 days | Queue backlog | No automation remedy; track via Chrome Web Store Developer Dashboard |

## VS Code Marketplace

**Authentication — Personal Access Token (PAT):**
```bash
# 1. Go to https://dev.azure.com → User Settings → Personal Access Tokens
# 2. Create PAT with "Marketplace (Publish)" scope, org = "All accessible organizations"
# 3. Export:
export VSCE_PAT="your-pat-here"
```

**vsce publish:**
```bash
npm install -g @vscode/vsce

# Version bump and publish
vsce publish patch     # minor, major also accepted
vsce publish --pre-release   # pre-release channel

# Package without publishing
vsce package

# Publish with ovsx (Open VSX Registry) as well
npx ovsx publish -p $OVSX_TOKEN
```

**Extension manifest minimum (`package.json`):**
```json
{
  "name": "my-extension",
  "displayName": "My Extension",
  "version": "1.0.0",
  "publisher": "my-publisher-id",
  "engines": { "vscode": "^1.85.0" },
  "categories": ["Other"],
  "activationEvents": [],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [{ "command": "myExtension.helloWorld", "title": "Hello World" }]
  }
}
```

**CI pipeline (GitHub Actions):**
```yaml
- name: Publish to VS Code Marketplace
  run: |
    npm ci
    npm run compile
    npx @vscode/vsce publish patch -p ${{ secrets.VSCE_PAT }}
    npx ovsx publish -p ${{ secrets.OVSX_TOKEN }}
```

**Pre-release flow:**
```bash
vsce publish minor --pre-release   # 1.1.0 → 1.2.0-pre.1
vsce publish --pre-release         # 1.2.0-pre.1 → 1.2.0-pre.2
vsce publish patch                 # 1.2.0-pre.2 → 1.2.0 (promotes to stable)
```

**Common failure modes & recovery:**
| Failure | Cause | Recovery |
|---------|-------|----------|
| `401 Unauthorized` | PAT expired or wrong scope | Regenerate PAT with "Marketplace (Publish)" scope |
| `409 Conflict: version already exists` | Duplicate version | Increment semver, must be strictly higher |
| `Missing publisher` | `publisher` field empty or not registered | Create publisher at marketplace.visualstudio.com/manage |

## Firefox Add-ons (AMO)

**Authentication — AMO API keys:**
```bash
# 1. Go to https://addons.mozilla.org/en-US/developers/addon/api/key/
# 2. Generate JWT issuer and secret
export WEB_EXT_API_KEY="user:12345:789"
export WEB_EXT_API_SECRET="deadbeef..."
```

**web-ext CLI:**
```bash
npm install -g web-ext

# Build and sign
web-ext sign \
  --api-key $WEB_EXT_API_KEY \
  --api-secret $WEB_EXT_API_SECRET \
  --channel=listed \         # "listed" (public) or "unlisted" (direct link only)
  --source-dir ./dist \
  --artifacts-dir ./web-ext-artifacts

# Lint before signing
web-ext lint --source-dir ./dist
```

**CI pipeline (GitHub Actions):**
```yaml
- name: Sign Firefox Add-on
  run: |
    npm ci && npm run build
    npx web-ext sign \
      --api-key ${{ secrets.FIREFOX_API_KEY }} \
      --api-secret ${{ secrets.FIREFOX_API_SECRET }} \
      --channel=listed \
      --source-dir ./dist
```

**Common failure modes & recovery:**
| Failure | Cause | Recovery |
|---------|-------|----------|
| `PKG_INVALID_MANIFEST` | Invalid manifest.json | Run `web-ext lint` locally, fix errors |
| `SIGNING_REJECTED` | Add-on violates AMO policies | Read rejection email, fix issues, bump version, re-submit |
| `JWT expired` | API key credentials stale | Regenerate at addons.mozilla.org |

## Microsoft Store

**MSIX packaging via WiX Toolset:**
```xml
<!-- Package.wxs -->
<Package Manufacturer="Contoso" Name="MyApp" Version="1.0.0.0">
  <MediaTemplate EmbedCab="yes" />
  <Directory Id="TARGETDIR" Name="SourceDir">
    <Directory Id="ProgramFiles64Folder">
      <Directory Id="INSTALLFOLDER" Name="MyApp">
        <Component Id="MainExecutable" Guid="PUT-GUID-HERE">
          <File Id="MyAppEXE" Source="MyApp.exe" KeyPath="yes" />
        </Component>
      </Directory>
    </Directory>
  </Directory>
</Package>
```

**Store submission API:**
```bash
# Authenticate via Azure AD app registration with Partner Center API access
az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
TOKEN=$(az account get-access-token --resource https://manage.devcenter.microsoft.com --query accessToken -o tsv)

# Create submission
curl -X POST "https://manage.devcenter.microsoft.com/v1.0/my/applications/$APP_ID/submissions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"

# Upload package
curl -X PUT "$UPLOAD_URL" \
  -H "x-ms-blob-type: BlockBlob" \
  --data-binary @MyApp.msix

# Commit submission
curl -X POST "$COMMIT_URL" \
  -H "Authorization: Bearer $TOKEN"
```

**CI pipeline (GitHub Actions):**
```yaml
- name: Build MSIX
  run: |
    dotnet publish -c Release -r win-x64 --self-contained
    candle.exe Package.wxs -ext WixUtilExtension
    light.exe Package.wixobj -ext WixUtilExtension -out MyApp.msix
- name: Submit to Microsoft Store
  run: |
    az login --service-principal -u ${{ secrets.AZURE_CLIENT_ID }} \
      -p ${{ secrets.AZURE_CLIENT_SECRET }} --tenant ${{ secrets.AZURE_TENANT_ID }}
    pwsh ./scripts/submit-store.ps1
```

**Common failure modes & recovery:**
| Failure | Cause | Recovery |
|---------|-------|----------|
| `Package acceptance validation error` | Missing capabilities declaration | Add required `<rescap:Capability>` entries, re-sign |
| `APPX_E_INVALID_SIP_SUBJECT` | Invalid Authenticode signature | Re-sign with valid code signing certificate |
| `Submission stuck "In certification"` | Manual review backlog | Wait; certification can take up to 3 business days |

## Steam (SteamPipe / SteamCMD)

**SteamPipe build configuration (`app_build_563560.vdf` / `depot_build_563561.vdf`):**
```
"AppBuild"
{
  "AppID" "563560"
  "Desc"  "Automated build"
  "BuildOutput" "steamworks_build_output"
  "ContentRoot" "..\game\build\release"
  "SetLive" "alpha"  // branch to set live on success
  "Depots"
  {
    "563561" "depot_build_563561.vdf"  // Windows depot
    "563562" "depot_build_563562.vdf"  // macOS depot
  }
}
```

**SteamCMD upload:**
```bash
# Install SteamCMD
# Linux:
steamcmd +quit
# macOS (via Homebrew):
brew install --cask steamcmd

# Run upload build
steamcmd +login "$STEAM_BUILDER_USER" "$STEAM_BUILDER_PASS" "$STEAM_GUARD_CODE" \
  +run_app_build "$(pwd)/scripts/app_build_563560.vdf" +quit

# Using steamctl (Python, modern alternative):
steamctl depot build --app 563560 --depot 563561 \
  --content-root ./game/build/release \
  --set-live alpha
```

**SteamPipe GUI setup (initial build config):** Use Steamworks partner site → SteamPipe → App Depots & Builds to create App and Depot IDs, configure depot file paths and encryption.

**CI pipeline (GitHub Actions):**
```yaml
- name: Deploy to Steam
  env:
    STEAM_USERNAME: ${{ secrets.STEAM_BUILDER_USER }}
    STEAM_PASSWORD: ${{ secrets.STEAM_BUILDER_PASS }}
    STEAM_GUARD: ${{ secrets.STEAM_GUARD_CODE }}
  run: |
    steamcmd +login "$STEAM_USERNAME" "$STEAM_PASSWORD" "$STEAM_GUARD" \
      +run_app_build "$GITHUB_WORKSPACE/scripts/app_build_563560.vdf" +quit
```

**Common failure modes & recovery:**
| Failure | Cause | Recovery |
|---------|-------|----------|
| `RateLimitExceeded` | Too many build uploads | Back off and retry; 2 minute cooldown recommended |
| `InvalidPassword` / `SteamGuardRequired` | Shared secret incorrect | Use Steam TOTP shared secret from `$STEAM_GUARD_CODE` as mobile authenticator code |
| `BuildOutput directory not found` | Paths incorrect | Verify `BuildOutput` and `ContentRoot` paths are absolute or relative to script location |

## Epic Games Store

**EOS SDK build pipeline:**
```bash
# EOS uses BuildPatchTool for chunked uploads
BuildPatchTool \
  -mode=PatchGeneration \
  -OrganizationId="$EPIC_ORG_ID" \
  -ProductId="$EPIC_PRODUCT_ID" \
  -ArtifactId="$EPIC_ARTIFACT_ID" \
  -ClientId="$EPIC_CLIENT_ID" \
  -ClientSecret="$EPIC_CLIENT_SECRET" \
  -BuildRoot=./game/build/release \
  -CloudDir=./clouddir \
  -BuildVersion="1.2.0" \
  -AppLaunch="MyGame.exe" \
  -AppArgs=""

# Upload patch data
BuildPatchTool \
  -mode=BinaryPatchUpload \
  -OrganizationId="$EPIC_ORG_ID" \
  -ProductId="$EPIC_PRODUCT_ID" \
  -ArtifactId="$EPIC_ARTIFACT_ID" \
  -ClientId="$EPIC_CLIENT_ID" \
  -ClientSecret="$EPIC_CLIENT_SECRET" \
  -CloudDir=./clouddir \
  -BuildVersion="1.2.0"
```

**Epic Dev Portal setup:** Create Product → Artifacts & Binaries → obtain OrgID/ProductID/ArtifactID/Client credentials.

**Common failure modes & recovery:**
| Failure | Cause | Recovery |
|---------|-------|----------|
| `Chunk mismatch` | Partial previous upload | Delete CloudDir, regenerate patches, re-upload |
| `Authentication failed` | Client credentials revoked | Regenerate credentials in Dev Portal |

## Snap Store (Linux)

**snapcraft CLI:**
```bash
# Install snapcraft
sudo snap install snapcraft --classic

# Login (export credentials for CI)
snapcraft export-login snapcraft-creds.txt --snaps=my-snap-name --channels=edge,beta,candidate,stable --acls=package_access,package_push,package_update,package_release

# Build
snapcraft --use-lxd   # LXD container provides clean build environment

# Release to channels
snapcraft upload my-snap_1.0.0_amd64.snap --release=edge
snapcraft release my-snap-name 10 stable   # promote revision 10 to stable
```

**CI pipeline (GitHub Actions):**
```yaml
- name: Build and publish Snap
  env:
    SNAPCRAFT_STORE_CREDENTIALS: ${{ secrets.SNAPCRAFT_CREDS }}
  run: |
    sudo snap install snapcraft --classic
    snapcraft --use-lxd
    snapcraft upload *.snap --release=edge
```

**Channel progression:** `edge` (every commit) → `beta` (weekly) → `candidate` (pre-release QA) → `stable` (manual promotion).

**Common failure modes & recovery:**
| Failure | Cause | Recovery |
|---------|-------|----------|
| `Store credentials expired` | Login token TTL (1 year) | Re-run `snapcraft export-login` |
| `Architecture mismatch` | Snap built for wrong arch | Use `--target-arch` or build on matching CI runner |

## Flathub (Linux)

**flatpak-builder:**
```bash
flatpak-builder --force-clean --repo=repo build-dir com.example.App.json
flatpak build-bundle repo com.example.App.flatpak com.example.App
flatpak build-update-repo repo
```

**CI pipeline (GitHub Actions) — external-data-checker:**
```yaml
- name: Update Flathub manifest
  run: |
    git clone https://github.com/flathub/com.example.App
    cd com.example.App
    # Update source URL/checksum in .json manifest
    python3 -c "
    import json, hashlib, urllib.request
    data = urllib.request.urlopen('$SOURCE_URL').read()
    sha = hashlib.sha256(data).hexdigest()
    print(f'New SHA256: {sha}')
    "
    # Commit and push — Flathub bot picks up changes
    git commit -am "Update to $VERSION"
    git push
```

**Common failure modes & recovery:**
| Failure | Cause | Recovery |
|---------|-------|----------|
| `Build timeout` | Flathub build infra timeout (1h) | Optimize build; consider pre-built binaries |
| `SDK runtime mismatch` | Freedesktop SDK version changed | Update `runtime-version` in manifest |

## Homebrew (macOS & Linux)

**Formula creation and publishing:**
```ruby
# /usr/local/Homebrew/Library/Taps/myorg/homebrew-tap/Formula/mytool.rb
class Mytool < Formula
  desc "A command-line tool"
  homepage "https://github.com/myorg/mytool"
  url "https://github.com/myorg/mytool/archive/refs/tags/v1.2.0.tar.gz"
  sha256 "abc123def456..."
  license "MIT"

  depends_on "go" => :build

  def install
    system "go", "build", "-o", bin/"mytool", "."
  end

  test do
    system "#{bin}/mytool", "--version"
  end
end
```

**Automated bump on release (GitHub Actions):**
```yaml
- name: Bump Homebrew formula
  run: |
    VERSION="${{ github.ref_name }}"
    URL="https://github.com/myorg/mytool/archive/refs/tags/${VERSION}.tar.gz"
    SHA256=$(curl -sL "$URL" | shasum -a 256 | cut -d' ' -f1)

    git clone "https://${{ secrets.HOMEBREW_TAP_TOKEN }}@github.com/myorg/homebrew-tap"
    cd homebrew-tap

    sed -i '' "s|url \".*\"|url \"${URL}\"|" Formula/mytool.rb
    sed -i '' "s|sha256 \".*\"|sha256 \"${SHA256}\"|" Formula/mytool.rb
    git commit -am "mytool ${VERSION}"
    git push
```

## Package Registries

### npm (Node.js)

```bash
npm set "//registry.npmjs.org/:_authToken" "$NPM_TOKEN"
npm publish --access public

# Scoped packages
npm publish --access public --scope=@myorg

# Verify with dry-run
npm publish --dry-run
```

**GitHub Actions:**
```yaml
- uses: actions/setup-node@v4
  with: { registry-url: "https://registry.npmjs.org" }
- run: npm ci && npm run build && npm publish
  env: { NODE_AUTH_TOKEN: "${{ secrets.NPM_TOKEN }}" }
```

### PyPI (Python)

```bash
pip install build twine
python -m build
twine upload dist/* -u __token__ -p "$PYPI_TOKEN"

# Test PyPI first
twine upload --repository testpypi dist/* -u __token__ -p "$PYPI_TEST_TOKEN"
```

**GitHub Actions — Trusted Publisher (OIDC, no token needed):**
```yaml
- uses: pypa/gh-action-pypi-publish@release/v1
  # No token needed — uses OIDC Trusted Publisher configured in PyPI project settings
```

### RubyGems (Ruby)

```bash
gem build mygem.gemspec
gem push mygem-1.0.0.gem --host https://rubygems.org

# CI: ~/.gem/credentials
mkdir -p ~/.gem
printf -- "---\n:rubygems_api_key: ${RUBYGEMS_API_KEY}\n" > ~/.gem/credentials
chmod 0600 ~/.gem/credentials
```

### Maven Central (Java/Kotlin)

```xml
<!-- pom.xml distributionManagement -->
<distributionManagement>
  <repository>
    <id>ossrh</id>
    <url>https://s01.oss.sonatype.org/service/local/staging/deploy/maven2/</url>
  </repository>
</distributionManagement>
```

```bash
# ~/.m2/settings.xml must contain OSSRH credentials with signing key
mvn deploy -P release
```

**GitHub Actions:**
```yaml
- uses: actions/setup-java@v4
  with: { java-version: "17", distribution: "temurin" }
- run: mvn deploy -P release --batch-mode
  env:
    OSSRH_USERNAME: ${{ secrets.OSSRH_USERNAME }}
    OSSRH_PASSWORD: ${{ secrets.OSSRH_PASSWORD }}
    GPG_PRIVATE_KEY: ${{ secrets.GPG_PRIVATE_KEY }}
    GPG_PASSPHRASE: ${{ secrets.GPG_PASSPHRASE }}
```

### CocoaPods (iOS/macOS)

```bash
pod trunk register user@example.com "Your Name" --description="CI bot"
pod lib lint MyPod.podspec   # validate locally
pod trunk push MyPod.podspec --allow-warnings
```

**GitHub Actions:**
```yaml
- run: pod trunk push MyPod.podspec --allow-warnings
  env: { COCOAPODS_TRUNK_TOKEN: "${{ secrets.COCOAPODS_TRUNK_TOKEN }}" }
```

### Swift Package Registry

```bash
# Swift packages use git tags natively — no separate registry push
git tag 1.0.0
git push origin 1.0.0

# The Package.swift manifest self-describes:
# swift package-registry publish <id> <version> is not yet GA for third-party registries
# For now: git tag + push is canonical distribution
```

### Docker Hub

```bash
docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"
docker build -t myorg/myimage:1.0.0 -t myorg/myimage:latest .
docker push myorg/myimage:1.0.0
docker push myorg/myimage:latest
```

**GitHub Actions:**
```yaml
- uses: docker/login-action@v3
  with: { username: "${{ secrets.DOCKER_USERNAME }}", password: "${{ secrets.DOCKER_PASSWORD }}" }
- uses: docker/build-push-action@v5
  with: { push: true, tags: "myorg/myimage:1.0.0,myorg/myimage:latest" }
```

### GitHub Container Registry (GHCR)

```bash
echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_ACTOR" --password-stdin
docker tag myimage ghcr.io/myorg/myimage:1.0.0
docker push ghcr.io/myorg/myimage:1.0.0
```

**GitHub Actions (OIDC, no token needed):**
```yaml
- uses: docker/login-action@v3
  with: { registry: ghcr.io, username: "${{ github.actor }}", password: "${{ secrets.GITHUB_TOKEN }}" }
- uses: docker/build-push-action@v5
  with: { push: true, tags: "ghcr.io/${{ github.repository }}:1.0.0" }
```

### Package registry common failure modes:

| Registry | Failure | Recovery |
|----------|---------|----------|
| npm | `402 Payment Required` / `You must sign up for private packages` | Add `--access public` flag or upgrade npm org plan |
| PyPI | `403 Invalid or non-existent authentication information` | Verify `__token__` username format with token; reissue token |
| RubyGems | `Repushing of gem is not allowed` | Gem version already exists — must bump semver, cannot overwrite |
| Maven | `401 Unauthorized` / `403 Forbidden` | GPG key not registered in key servers or OSSRH token expired |
| CocoaPods | `[!] You need to register a session first` | Run `pod trunk register` from CI machine or export `COCOAPODS_TRUNK_TOKEN` |
| Docker Hub | `denied: requested access to the resource is denied` | Image namespace must match Docker Hub org/user, not `library/` |
