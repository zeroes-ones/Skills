# fastlane-reference

Comprehensive fastlane patterns for mobile CI/CD automation. Covers iOS and Android lanes with error handling, code signing, store submission, and notification integration.

## Prerequisites

- Ruby 3.0+ (system Ruby or rbenv/rvm)
- Bundler: `gem install bundler`
- fastlane: `gem install fastlane` or add to Gemfile

```ruby
# Gemfile
source "https://rubygems.org"
gem "fastlane"
gem "cocoapods"
```

```bash
bundle install
bundle exec fastlane init
```

## iOS: Complete Fastfile

```ruby
default_platform(:ios)

platform :ios do
  before_all do |lane|
    ENV["FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD"] = ENV["APPLE_APP_SPECIFIC_PASSWORD"]
    setup_ci if is_ci?
  end

  desc "Run tests"
  lane :test do
    run_tests(
      scheme: "MyApp",
      devices: ["iPhone 15 Pro"],
      deployment_target_version: "17.0"
    )
  end

  desc "Build and upload to TestFlight"
  lane :beta do
    ensure_git_status_clean
    match(type: "appstore", readonly: true)
    increment_build_number(
      build_number: latest_testflight_build_number + 1
    )
    gym(
      scheme: "MyApp",
      export_method: "app-store",
      clean: true,
      include_bitcode: false
    )
    pilot(
      skip_waiting_for_build_processing: true,
      distribute_external: true,
      notify_external_testers: true
    )
    slack(
      message: "New TestFlight build #{lane_context[SharedValues::BUILD_NUMBER]} uploaded",
      success: true
    )
  rescue => e
    slack(
      message: "TestFlight upload failed: #{e.message}",
      success: false
    )
    raise e
  end

  desc "Submit to App Store review"
  lane :release do
    ensure_git_status_clean
    match(type: "appstore", readonly: true)
    increment_build_number(
      build_number: latest_testflight_build_number + 1
    )
    gym(
      scheme: "MyApp",
      export_method: "app-store",
      clean: true
    )
    deliver(
      force: true,
      submit_for_review: true,
      automatic_release: false,
      phased_release: true,
      precheck_include_in_app_purchases: false
    )
    slack(
      message: "App submitted for review — build #{lane_context[SharedValues::BUILD_NUMBER]}",
      success: true
    )
  rescue => e
    slack(
      message: "App Store submission failed: #{e.message}",
      success: false
    )
    raise e
  end

  desc "Generate and upload screenshots"
  lane :screenshots do
    capture_screenshots(
      scheme: "MyAppUITests",
      devices: ["iPhone 15 Pro", "iPhone 15 Pro Max", "iPad Pro (12.9-inch) (6th generation)"]
    )
    frame_screenshots
    deliver(
      skip_binary_upload: true,
      skip_metadata: false,
      overwrite_screenshots: true
    )
  end
end
```

## Android: Complete Fastfile

```ruby
default_platform(:android)

platform :android do
  desc "Run unit tests"
  lane :test do
    gradle(task: "test")
  end

  desc "Build and upload to internal track"
  lane :internal do
    gradle(
      task: "bundleRelease",
      properties: {
        "android.injected.signing.store.file" => ENV["KEYSTORE_FILE"],
        "android.injected.signing.store.password" => ENV["KEYSTORE_PASSWORD"],
        "android.injected.signing.key.alias" => ENV["KEY_ALIAS"],
        "android.injected.signing.key.password" => ENV["KEY_PASSWORD"]
      }
    )
    upload_to_play_store(
      track: "internal",
      release_status: "completed",
      aab: "app/build/outputs/bundle/release/app-release.aab"
    )
  end

  desc "Staged rollout to production"
  lane :release do
    gradle(
      task: "bundleRelease",
      properties: {
        "android.injected.signing.store.file" => ENV["KEYSTORE_FILE"],
        "android.injected.signing.store.password" => ENV["KEYSTORE_PASSWORD"],
        "android.injected.signing.key.alias" => ENV["KEY_ALIAS"],
        "android.injected.signing.key.password" => ENV["KEY_PASSWORD"]
      }
    )
    upload_to_play_store(
      track: "production",
      release_status: "inProgress",
      rollout: "0.1",
      aab: "app/build/outputs/bundle/release/app-release.aab"
    )
    slack(message: "Play Store staged rollout started at 10%", success: true)
  rescue => e
    slack(message: "Play Store upload failed: #{e.message}", success: false)
    raise e
  end

  desc "Promote staged rollout"
  lane :promote_rollout do
    upload_to_play_store(
      track: "production",
      rollout: "1.0",
      release_status: "completed"
    )
  end
end
```

## Match (Code Signing)

```ruby
# Matchfile
git_url("git@github.com:org/certificates.git")
storage_mode("git")
type("appstore")
app_identifier("com.myorg.myapp")
username("ci@myorg.com")
team_id("ABCDEF1234")
```

```bash
# Initial setup
fastlane match appstore
fastlane match development
fastlane match adhoc

# Rotate expired certs
fastlane match nuke appstore
fastlane match appstore --force
```

## CI Environment Setup

```bash
# macOS CI runner prerequisites
brew install fastlane
bundle install

# Set required env vars
export APPLE_APP_SPECIFIC_PASSWORD="$APP_STORE_PASSWORD"
export MATCH_PASSWORD="$MATCH_REPO_PASSWORD"
export FASTLANE_SESSION="$FASTLANE_SESSION_TOKEN"  # from `fastlane spaceauth`
```

## Error Handling Patterns

| Pattern | When to Use | Example |
|---------|------------|---------|
| `rescue` + re-raise | Lane must fail visibly in CI | `rescue => e; notify_failure(e); raise e` |
| Retry with backoff | Transient network/app store errors | `retry_count = 3` in action options |
| `ensure` block | Clean up keychain, temp files | `unlock_keychain` in ensure |
| `is_ci?` guard | CI-specific behavior only | `setup_ci if is_ci?` |
| `UI.error` + exit | Non-critical lane, graceful exit | `UI.error("Skip"); next` |

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| "No code signing identity found" | Expired cert, wrong team | `fastlane match nuke` + regenerate |
| "Authentication failed" | Expired session token | `fastlane spaceauth -u ci@org.com` |
| "No provisioning profile" | New device, new app ID | `fastlane match appstore --force` |
| "Invalid Binary" | Simulator build, wrong arch | Check `ONLY_ACTIVE_ARCH=NO` and `VALID_ARCHS` |
| "ITC.apps.tf.violatesPolicy" | Screenshot/metadata issue | Run `fastlane deliver download_metadata` to diff |

## GitHub Actions Integration

```yaml
- name: Run fastlane beta
  run: bundle exec fastlane beta
  env:
    APPLE_APP_SPECIFIC_PASSWORD: ${{ secrets.APPLE_APP_SPECIFIC_PASSWORD }}
    MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
    FASTLANE_SESSION: ${{ secrets.FASTLANE_SESSION }}
    KEYSTORE_FILE: ${{ secrets.KEYSTORE_FILE }}
    KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
    KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
    KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
```
