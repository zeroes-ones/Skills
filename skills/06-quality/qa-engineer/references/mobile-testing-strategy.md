# Mobile Testing Strategy

## The Fragmentation Problem

Unlike web (1-3 browsers) or backend (homogeneous runtime), mobile apps must run on 10,000+ device models with different:
- Screen sizes and pixel densities
- OS versions (iOS 16-19, Android 12-16 in active use)
- RAM (2GB budget phones → 12GB flagships)
- GPU capabilities
- Network conditions (5G ↔ 2G Edge)
- Manufacturer skins (Samsung One UI, Xiaomi MIUI, etc.)

## Device Selection Matrix — What to Test On

### Tier 1: Primary Test Targets (every PR, every release)

| Platform | Device | OS | RAM | Rationale |
|----------|--------|----|-----|-----------|
| iOS | iPhone SE (latest) | Latest - 1 | 4GB | Small screen, modest RAM — stress tests layout and memory |
| iOS | Pro Max model (latest - 1 gen) | Latest | 8GB | Large screen, Dynamic Island — tests safe areas |
| Android | Pixel a-series (latest) | Latest - 1 | 6GB | Stock Android, mid-range — reference baseline |
| Android | Samsung Galaxy A series | 2 versions back | 4GB | Most popular global device class; One UI skin |

**Rule: At least 1 budget device + 1 flagship device per platform in primary set.**

### Tier 2: Release Gate (every release)

Add 4-6 more devices covering:
- iOS: iPad (tablet layout), oldest supported iOS version
- Android: Foldable (Samsung Fold/Flip), tablet, oldest supported Android
- One low-end device (< $200, 2GB RAM, Android Go)

### Tier 3: Full Matrix (quarterly, before major launches)

Add 10+ devices via device farm (Firebase Test Lab, BrowserStack, Sauce Labs):
- Top 10 devices by active user base
- Top 5 OEM skins (Samsung, Xiaomi, OPPO, vivo, OnePlus)
- Minimum spec device (enforced by app's minSDK/minimum deployment target)

---

## Emulator vs Real Device

| Factor | Emulator/Simulator | Real Device |
|--------|-------------------|-------------|
| Speed | Fast (seconds to launch) | Slow (minutes to provision in device farm) |
| Cost | Free (included in SDK) | $0.05-$5.00 per test run |
| Sensor accuracy | Simulated (may differ from reality) | Real hardware |
| Push notifications | Simulator: unreliable. Emulator: FCM works | Full FCM/APNs support |
| Biometrics | Simulated (no real fingerprint/face) | Real hardware |
| Network simulation | Full control (latency, packet loss, bandwidth) | Limited (WiFi/LTE only) |
| Battery/thermal | N/A | Real behavior |
| GPU rendering | Software rendering (may differ) | Real GPU |
| **Use for** | Unit tests, widget tests, quick iteration | E2E tests, performance, biometrics, release validation |

**Strategy:** Emulators in CI for PRs. Real devices for nightly regression and pre-release. 80% of tests on emulators, 20% on real devices.

---

## Testing Layers for Mobile

### Layer 1: Unit Tests (milliseconds, every build)

```kotlin
// Android: JUnit + MockK
@Test
fun `checkout total includes tax when tax flag enabled`() {
    every { featureFlags.isEnabled("checkout.tax_calculation") } returns true
    val total = checkoutViewModel.calculateTotal(cart)
    assertEquals(11.00, total) // $10 + 10% tax
}
```

```swift
// iOS: XCTest
func testCheckoutTotalIncludesTaxWhenFlagEnabled() {
    featureFlags.setEnabled("checkout.tax_calculation", true)
    let total = viewModel.calculateTotal(for: cart)
    XCTAssertEqual(total, 11.00)
}
```

### Layer 2: Widget/Component Tests (seconds, every PR)

```kotlin
// Compose Testing
@Test
fun `checkout screen shows tax line when flag enabled`() {
    composeTestRule.setContent {
        CheckoutScreen(viewModel = viewModel)
    }
    composeTestRule.onNodeWithTag("tax_line").assertIsDisplayed()
}
```

### Layer 3: Integration Tests (seconds, every PR)

Test ViewModel + Repository + API layer together. Mock the server, use real flag evaluation.

### Layer 4: E2E Tests (minutes, nightly + pre-release)

```kotlin
// Espresso
@Test
fun completeCheckoutFlow() {
    onView(withId(R.id.product_search)).perform(typeText("widget"), pressImeActionButton())
    onView(withId(R.id.add_to_cart)).perform(click())
    onView(withId(R.id.checkout)).perform(click())
    onView(withId(R.id.payment_button)).perform(click())
    onView(withId(R.id.order_confirmation)).check(matches(isDisplayed()))
}
```

```swift
// XCUITest
func testCompleteCheckoutFlow() {
    let app = XCUIApplication()
    app.textFields["product_search"].tap()
    app.textFields["product_search"].typeText("widget\n")
    app.buttons["add_to_cart"].tap()
    app.buttons["checkout"].tap()
    app.buttons["payment_button"].tap()
    XCTAssertTrue(app.staticTexts["order_confirmation"].exists)
}
```

### Layer 5: Screenshot/Snapshot Testing (pre-release)

Compare screenshots against baselines across device sizes:
- Tools: `paparazzi` (Android, no device needed), `snapshot-testing` (iOS)
- Store baselines in repo
- Diff threshold: 1% pixel difference triggers failure

### Layer 6: Accessibility Automated Testing

```kotlin
// Android: Espresso + AccessibilityChecks
AccessibilityChecks.enable()
// Every Espresso interaction automatically checks:
// - TalkBack focus order
// - Contrast ratio (if combined with contrast checking)
// - Touch target size
```

```swift
// iOS: XCUITest + Accessibility Inspector
let app = XCUIApplication()
// Set accessibility testing mode
app.launchArguments = ["-UIAccessibilityEnabled", "YES"]
// Verify all interactive elements are accessible
XCTAssertTrue(app.buttons["add_to_cart"].isAccessibilityElement)
```

---

## Network Condition Testing

Mobile apps must function across a wide range of network conditions:

| Condition | Downlink | Uplink | Latency | Test Scenario |
|-----------|----------|--------|---------|---------------|
| 5G | 100 Mbps | 50 Mbps | 5ms | Baseline — everything works |
| 4G LTE | 20 Mbps | 10 Mbps | 50ms | All features work, images load in < 2s |
| 3G | 1.5 Mbps | 0.5 Mbps | 300ms | Features work, loading spinners visible |
| 2G Edge | 100 Kbps | 50 Kbps | 800ms | Timeout at 30s, show offline message |
| Offline | 0 | 0 | N/A | Show cached data, queue operations |
| Packet Loss 5% | Any | Any | Any | Retry logic engages, no crashes |
| DNS Failure | Any | Any | N/A | Graceful degradation, cached IP fallback |

**Tooling:**
- Android: `NetworkProfiler` in Android Studio, or `Charles Proxy`
- iOS: Network Link Conditioner (System Preferences)
- Device Farm: BrowserStack network throttling profiles
- CI: `tc` (traffic control) on Android emulators

---

## Performance Testing on Budget Devices

| Metric | Budget Target | Flagship Target | Test Method |
|--------|-------------|-----------------|-------------|
| Cold start | < 3 seconds | < 1 second | ADB `am start -W` or XCUITest launch measurement |
| Hot start | < 1 second | < 500ms | Re-launch timing |
| Screen transition | < 200ms | < 100ms | Systrace / Instruments Time Profiler |
| Scroll jank | 0 dropped frames / 100 scrolls | 0 dropped frames | GPU profiling overlay |
| Memory peak | < 200MB | < 400MB | Memory Profiler / Allocations Instrument |
| Battery drain | < 5% per hour idle | < 2% per hour idle | Battery Historian / Energy Log |

**Critical rule:** If it doesn't run on the budget device, it doesn't ship. Test on budget hardware FIRST, not as an afterthought.

---

## CI Integration for Mobile Testing

```yaml
# conceptual CI pipeline for mobile
mobile-qa-pipeline:
  triggers:
    - pull_request
    - nightly

  stages:
    - stage: unit
      parallel: true
      matrix:
        android: [Pixel 9 Emulator]
        ios: [iPhone 16 Simulator]
      script: ./gradlew test or xcodebuild test
      timeout: 10 minutes

    - stage: integration
      depends_on: unit
      script: ./gradlew connectedCheck or xcodebuild test (with host app)
      timeout: 15 minutes

    - stage: e2e-smoke
      depends_on: integration
      condition: pull_request
      devices: [primary device set (4 devices)]
      script: run smoke tests on device farm
      timeout: 20 minutes

    - stage: e2e-full
      depends_on: integration
      condition: nightly OR release_branch
      devices: [full device matrix (12+ devices)]
      script: run full E2E suite on device farm
      timeout: 60 minutes

    - stage: screenshot-validation
      depends_on: e2e-full
      condition: release_branch
      script: compare screenshots against baselines
      timeout: 30 minutes
```

---

## Common Mobile Testing Anti-Patterns

| Anti-Pattern | Why It's Dangerous | Fix |
|-------------|-------------------|-----|
| Testing only on latest flagship | Catches < 5% of user device issues | Tier-based device selection above |
| No network condition testing | "Works on WiFi" ≠ "Works on subway" | Network condition matrix in CI |
| No budget device testing | Crashes on 60% of Android devices | Tier 1 includes budget device |
| Screenshot tests without baseline in repo | Untracked visual regressions | Store baselines in Git LFS |
| E2E tests that depend on real APIs | Flaky, slow, hard to debug | Mock server (WireMock, Mockoon) with recorded responses |
| No accessibility automation in e2e | 15% of users may be excluded | Enable AccessibilityChecks in every E2E run |
| "We'll test on real devices before launch" | 90% of bugs found too late to fix | Real devices in nightly regression |
| All tests on one OS version | Misses OS-specific regressions (especially iOS major version updates) | Test current and current-1 OS versions |
