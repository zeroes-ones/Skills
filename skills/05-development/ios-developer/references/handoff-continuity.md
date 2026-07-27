# Handoff & Continuity — Cross-Device UX Patterns

## Core Concepts

Apple's Continuity framework connects user experiences across devices:
- **Handoff**: Transfer an activity from one device to another (start on iPhone, continue on Mac)
- **Universal Clipboard**: Copy on one device, paste on another
- **Continuity Camera**: Use iPhone camera as Mac webcam
- **Universal Control**: Single keyboard/mouse across Mac and iPad
- **Sidecar**: iPad as secondary Mac display

For developers, the implementation surface is: `NSUserActivity`, Universal Links, and iCloud KVS.

---

## NSUserActivity: The Handoff API

### Creating an Activity

```swift
// When user enters a context worth continuing
let activity = NSUserActivity(activityType: "com.yourcompany.checkout.viewing")
activity.title = "Viewing Checkout Cart"
activity.isEligibleForHandoff = true
activity.userInfo = [
    "cartId": cart.id.uuidString,
    "step": "shipping_address"
]
// Fallback for non-Apple devices or when Handoff unavailable
activity.webpageURL = URL(string: "https://yourapp.com/checkout/\(cart.id)?step=shipping")
// Required for Handoff — persist only the minimal state
activity.needsSave = true
activity.becomeCurrent()
```

### Receiving an Activity

```swift
// In SceneDelegate or AppDelegate
func scene(_ scene: UIScene, continue userActivity: NSUserActivity) {
    guard userActivity.activityType == "com.yourcompany.checkout.viewing",
          let cartId = userActivity.userInfo?["cartId"] as? String else {
        return
    }
    // Restore the exact state: navigate to checkout, load cart, scroll to step
    navigationCoordinator.restoreCheckout(cartId: cartId, step: userActivity.userInfo?["step"] as? String)
}
```

### Activity Type Conventions

| Pattern | Example | Usage |
|---------|---------|-------|
| `com.company.feature.viewing` | `com.checkout.cart.viewing` | Read-only context (browsing, viewing) |
| `com.company.feature.editing` | `com.checkout.order.editing` | Mutating context (editing, composing) |
| `com.company.feature.navigating` | `com.checkout.map.navigating` | Active navigation (turn-by-turn, tracking) |

---

## Universal Links — Deep Linking to In-App Content

Universal Links connect web URLs to in-app screens. They serve dual purpose: Handoff fallback AND external deep links.

### Configuration

```swift
// 1. apple-app-site-association (hosted at https://yourapp.com/.well-known/)
{
  "applinks": {
    "details": [
      {
        "appID": "TEAMID.com.yourcompany.yourapp",
        "paths": ["/checkout/*", "/product/*", "/order/*"]
      }
    ]
  }
}

// 2. Associated Domains in Xcode
// Capabilities → Associated Domains → applinks:yourapp.com

// 3. Handle in SceneDelegate
func scene(_ scene: UIScene, continue userActivity: NSUserActivity) {
    guard userActivity.activityType == NSUserActivityTypeBrowsingWeb,
          let url = userActivity.webpageURL,
          let components = URLComponents(url: url, resolvingAgainstBaseURL: true) else {
        return
    }

    switch components.path {
    case let path where path.hasPrefix("/checkout/"):
        let cartId = path.components(separatedBy: "/").last ?? ""
        navigationCoordinator.navigateToCheckout(cartId: cartId)
    case let path where path.hasPrefix("/product/"):
        let productId = path.components(separatedBy: "/").last ?? ""
        navigationCoordinator.navigateToProduct(productId: productId)
    default:
        break
    }
}
```

---

## Scene-Based State Restoration

iOS 13+ introduced scene-based state restoration. Use `NSUserActivity` for per-scene restoration:

```swift
// Save scene state
func stateRestorationActivity(for scene: UIScene) -> NSUserActivity? {
    let activity = NSUserActivity(activityType: "com.yourcompany.restoration")
    activity.userInfo = navigationCoordinator.stateRestorationInfo()
    return activity
}

// Restore scene state
func scene(_ scene: UIScene, restoreInteractionStateWith stateRestorationActivity: NSUserActivity) {
    if let info = stateRestorationActivity.userInfo {
        navigationCoordinator.restoreState(from: info)
    }
}
```

---

## Handoff with Feature Flags

When a feature is behind a flag, Handoff must respect flag state across devices:

```swift
func scene(_ scene: UIScene, continue userActivity: NSUserActivity) {
    // If the activity targets a feature behind a flag
    if userActivity.activityType == "com.yourcompany.checkout.new_flow.viewing" {
        guard featureFlags.isEnabled("checkout.new_flow.v2") else {
            // Fall back to legacy flow; don't lose the user's session
            navigationCoordinator.navigateToLegacyCheckout(cartId: userActivity.userInfo?["cartId"] as? String)
            return
        }
        navigationCoordinator.navigateToNewCheckout(cartId: userActivity.userInfo?["cartId"] as? String)
    }
}
```

**Critical rule:** Never show a blank screen or error when receiving a Handoff activity for a feature that's disabled on this device. Always fall back to the closest available experience.

---

## Continuity Camera — System Integration

Continuity Camera is handled by the system (no API needed), but you can respond to it:

```swift
// Detect when Continuity Camera is available
import AVFoundation

let discoverySession = AVCaptureDevice.DiscoverySession(
    deviceTypes: [.continuityCamera],
    mediaType: .video,
    position: .unspecified
)

for device in discoverySession.devices {
    print("Continuity Camera available: \(device.localizedName)")
}
```

---

## iCloud Key-Value Store — Synchronizing Small State

For sharing small state across devices (user preferences, last-viewed screen):

```swift
// Store
NSUbiquitousKeyValueStore.default.set(cartId, forKey: "lastCheckoutCartId")
NSUbiquitousKeyValueStore.default.synchronize()

// Retrieve (with notification for changes)
NotificationCenter.default.addObserver(
    forName: NSUbiquitousKeyValueStore.didChangeExternallyNotification,
    object: NSUbiquitousKeyValueStore.default,
    queue: .main
) { notification in
    if let reason = notification.userInfo?[NSUbiquitousKeyValueStoreChangeReasonKey] as? Int {
        // Handle external change (server change, initial sync, quota exceeded)
    }
}
```

**Limits:** 1MB total, 1024 keys max, 4KB per value. For larger state, use CloudKit or a custom server.

---

## Testing Handoff

### Manual Testing Checklist

| Test | Steps | Expected |
|------|-------|----------|
| iPhone → Mac | Open app on iPhone, navigate to checkout. Check Mac Dock — Handoff icon appears. Click it. | App opens on Mac at the same checkout screen |
| Mac → iPhone | Open app on Mac, edit a document. Swipe up on iPhone Lock Screen — Handoff icon appears. | App opens on iPhone with the same document in editing state |
| iPad → iPhone | Same as above | Context transfers correctly |
| Feature flag OFF on receiving device | Send Handoff activity for feature behind a flag. Receiving device has flag OFF. | App opens to closest equivalent experience (legacy flow), not blank screen |
| Airplane mode | Start activity, enable Airplane Mode, try to Handoff | Activity times out gracefully; no crash |
| App not installed | Send Handoff to device without app | `webpageURL` fallback opens in Safari |
| Large userInfo | Send activity with > 3KB userInfo | Activity gracefully degrades — essential state transmitted |

### Test Environment

- Test on physical devices (Simulator doesn't support Handoff reliably)
- Same iCloud account on all devices
- Bluetooth enabled on all devices
- Both devices on same Wi-Fi network (Handoff uses Bluetooth LE + Wi-Fi Direct)
- Handoff enabled: Settings → General → AirPlay & Handoff → Handoff

---

## Common Failure Modes

| Failure | Cause | Fix |
|---------|-------|-----|
| Handoff icon doesn't appear on receiving device | Activity not marked `isEligibleForHandoff` or never called `becomeCurrent()` | Verify both are called on the main thread |
| Handoff opens to wrong screen | `userInfo` missing navigation state or scene delegate not parsing it | Add navigation restoration debug logging |
| Handoff times out / never completes | State too large (userInfo > 3KB blocks transmission) | Store large state server-side; send only ID |
| App crashes on Handoff receive | Receiving app cannot parse userInfo (schema mismatch) | Add version field to userInfo; migrate old schemas |
| webPageURL not working | AASA file missing or not served at `/.well-known/` | Verify: `curl -H "Authorization: Bearer unused" https://yourapp.com/.well-known/apple-app-site-association` returns valid JSON |
| iCloud KVS not syncing | Entitlement missing or NSUbiquitousKeyValueStore not enabled | Verify iCloud capability with Key-value storage checked in Xcode |
