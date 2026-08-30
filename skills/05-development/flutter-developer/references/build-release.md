# Build & Release — AOT, Tree-Shaking, Codemagic/Fastlane

## Release Build Config

```bash
flutter build apk --release --split-per-abi --tree-shake-icons \
  --obfuscate --split-debug-info=build/symbols
flutter build ios --release --obfuscate --split-debug-info=build/symbols
```

- **AOT** — release builds compile to native code; debug/JIT is for development only.
- **Tree-shake icons** — removes unused Material/Cupertino icons.
- **Obfuscate + split-debug-info** — smaller binary, separable symbols (upload to Crashlytics/Sentry).
- **Report sizes** — `--report-sizes` / `flutter build appbundle` size output for the size gate.

## CI/CD — Codemagic (managed) or Fastlane (custom)

**Codemagic:** YAML workflow — `flutter test` → integration tests → build APK/IPA → publish to stores. Secrets via environment groups.

**Fastlane:**

```ruby
lane :release do
  run_tests
  build_app(scheme: "App")
  pilot          # TestFlight (iOS)
  supply         # Play Console (Android)
end
```

- Signing: iOS certificates/provisioning via `match`; Android keystore via encrypted secrets. Never commit signing material.
- Secrets in the credential store, never the repo.

## Store Submission

- [ ] Icons/splash from pubspec or native config
- [ ] Privacy policy URL (both stores)
- [ ] Test accounts in submission notes
- [ ] Screenshots for required device sizes
- [ ] Content rating questionnaire
- [ ] Version bump + changelog
- [ ] Crash-free baseline from the previous version

## Release Gate (CI)

1. `flutter analyze` clean
2. `flutter test` green (no skips)
3. Integration tests green on both platforms
4. Size report within budget
5. Signing verified
6. Crash-free sessions ≥ 99% baseline

## Common Release Failures

| Symptom | Fix |
|---------|-----|
| App rejected: "uses private API" | Audit plugins for private API usage; check the rejected binary's symbols |
| "Missing expected icon" / metadata | Complete store assets (adaptive icon, screenshots) |
| Upload key mismatch (Play) | Sign with the same upload key registered in Play Console |
| TestFlight "missing compliance" | Complete export compliance (encryption) in App Store Connect |
