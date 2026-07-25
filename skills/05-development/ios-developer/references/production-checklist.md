## Production Checklist

Before any production release, verify ALL of:

1. [ ] **Code signing:** Archive succeeds with Distribution provisioning profile; no "Failed to codesign" errors
2. [ ] **Entitlements:** `aps-environment`, `com.apple.developer.icloud-container-identifiers`, and any custom entitlements match provisioning profile
3. [ ] **Privacy manifest:** `PrivacyInfo.xcprivacy` includes all required-reason API categories (UserDefaults, file timestamp, system boot time, disk space, active keyboard, etc.)
4. [ ] **ATS configuration:** No `NSAllowsArbitraryLoads` at top level without security review sign-off; per-domain exceptions preferred
5. [ ] **Launch screen:** `LaunchScreen.storyboard` exists; no blank black screen on cold launch
6. [ ] **App thinning:** Slicing enabled; `ENABLE_BITCODE` understanding (deprecated in Xcode 14+)
7. [ ] **Crash-free rate ≥ 99.5%:** Verified via Xcode Organizer or Crashlytics for last 7 days
8. [ ] **Network resilience:** All network calls have timeout + retry; no infinite spinners
9. [ ] **Background tasks:** `BGTaskScheduler` handlers complete within 30 seconds or call `expirationHandler`
10. [ ] **StoreKit 2:** IAP products fetched and displayed; `Transaction.updates` listener active; no hardcoded product IDs in production
11. [ ] **Deep links:** Universal Links configured in `apple-app-site-association`; URL scheme fallback registered
12. [ ] **App Store metadata:** Screenshots for all required sizes (6.7", 6.5", 5.5"); app description, keywords, and privacy labels complete
13. [ ] **Export compliance:** CCATS or ERN filed if using encryption beyond OS-provided (HTTPS, WPA)
14. [ ] **Accessibility:** Basic VoiceOver audit passes; no `accessibilityLabel` = "" on tappable elements
15. [ ] **Size budget:** App bundle <200 MB for cellular download; on-demand resources configured for assets exceeding threshold
