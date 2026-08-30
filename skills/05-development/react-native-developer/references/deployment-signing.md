# RN Deployment & Signing — EAS, Fastlane, Store Submission

## Expo (EAS) Path

```bash
eas build --platform ios --profile production   # builds + signs with EAS credentials
eas build --platform android --profile production
eas submit --platform ios --latest              # upload to TestFlight / App Store Connect
eas submit --platform android --latest          # upload to Play Console
```

- Credentials (certificates, provisioning profiles, keystores) live in EAS; back them up via `eas credentials`.
- `eas update` creates OTA bundles per channel (see `ota-release-policy.md`).

## Bare (Fastlane) Path

```ruby
# fastlane/Fastfile
lane :release do
  match(type: "appstore")            # certificates + provisioning from match repo
  build_app(scheme: "App")
  pilot                            # TestFlight upload (iOS)
  supply                          # Play Console upload (Android)
end
```

- `fastlane match` stores signing assets encrypted in git; never commit raw `.p12`/keystores.
- Signing is per-platform: iOS provisioning profiles + certificates; Android keystore + Play App Signing.

## Store Submission Checklist

- [ ] App icon + splash generated from config (adaptive icon for Android)
- [ ] Privacy policy URL (required by both stores for data collection)
- [ ] Test account credentials in submission notes
- [ ] Screenshots for required device sizes
- [ ] Content rating questionnaire completed
- [ ] OTA policy documented in submission notes (if relevant)
- [ ] App Store 3.3.2 compliance verified (no executable-code download)

## CI/CD

- EAS: `eas build` triggers from git; secrets via EAS secrets.
- Bare: Fastlane lanes in GitHub Actions/other CI; match for signing; E2E (Detox/Maestro) in the pipeline before release.
- Release gate in CI: unit + E2E green, performance budgets met, version bump validated.

## Common Signing Failures

| Symptom | Fix |
|---------|-----|
| "No valid provisioning profile" | `match` renew; check the bundle ID matches the app ID |
| "Provisioning profile doesn't include this device" | Add device to the profile (dev), or use a distribution profile for release |
| Play "upload key mismatch" | Sign with the same upload key registered in Play Console; keep it backed up |
| EAS "credentials not found" | `eas credentials` to configure; verify the Apple team ID and bundle ID |
