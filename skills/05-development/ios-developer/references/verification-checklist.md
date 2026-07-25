## Verification Checklist

Before marking any iOS task complete:

- [ ] Builds from clean (`xcodebuild clean build`) with zero errors and zero warnings
- [ ] All four screen states (loading, loaded, empty, error) implemented and visible
- [ ] VoiceOver reads every interactive element with meaningful labels
- [ ] Dynamic Type from `xSmall` to `accessibilityExtraExtraExtraLarge` doesn't clip or truncate
- [ ] `PrivacyInfo.xcprivacy` exists and lists all required API reason categories
- [ ] No `try?` discarding errors — all failure paths handled with user-visible feedback
- [ ] No `!` force-unwrap on optionals from external sources (network, database, user defaults)
- [ ] All closures capture `[weak self]` unless lifetime is provably shorter
- [ ] Core Data / SwiftData operations respect thread confinement
- [ ] `.gitignore` excludes `xcuserdata/`, `*.xcworkspace/xcuserdata/`, `DerivedData/`
- [ ] `Info.plist` includes `NSCameraUsageDescription`, `NSPhotoLibraryUsageDescription`, etc., for any requested permissions
- [ ] Instruments > Leaks shows zero leaks after 5-minute navigation cycle
- [ ] TestFlight archive validates with `xcodebuild -exportArchive`
- [ ] `@available` guards wrap any API newer than `IPHONEOS_DEPLOYMENT_TARGET`

---
