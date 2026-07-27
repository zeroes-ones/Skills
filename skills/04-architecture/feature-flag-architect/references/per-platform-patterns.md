# Feature Flag Implementation Patterns Per Platform

## Backend (Go/Node/Python/Java)

### Pattern 1: Branching by Abstraction (Recommended for major features)

```go
// interface definition
type CheckoutService interface {
    ProcessCheckout(cart Cart) (Order, error)
}

// old implementation
type LegacyCheckoutService struct {}
func (s *LegacyCheckoutService) ProcessCheckout(cart Cart) (Order, error) { ... }

// new implementation
type NewCheckoutService struct {}
func (s *NewCheckoutService) ProcessCheckout(cart Cart) (Order, error) { ... }

// flag-aware resolver (single point of flag evaluation)
type FlagAwareCheckoutService struct {
    legacy *LegacyCheckoutService
    new    *NewCheckoutService
    flags  FlagClient
}

func (s *FlagAwareCheckoutService) ProcessCheckout(cart Cart) (Order, error) {
    if s.flags.IsEnabled("checkout.new_flow.v2") {
        return s.new.ProcessCheckout(cart)
    }
    return s.legacy.ProcessCheckout(cart)
}
```

### Pattern 2: Decorator/Proxy (Recommended for additive behavior)

```python
class CheckoutService:
    def process(self, cart): ...

class FraudCheckDecorator:
    def __init__(self, inner: CheckoutService, flags: FlagClient):
        self.inner = inner
        self.flags = flags

    def process(self, cart):
        order = self.inner.process(cart)
        if self.flags.is_enabled("checkout.fraud_check.v1"):
            self.run_fraud_check(order)
        return order
```

### Pattern 3: Dependency Injection Composition Root

```java
@Configuration
public class CheckoutConfig {
    @Bean
    public CheckoutService checkoutService(FlagClient flags) {
        if (flags.isEnabled("checkout.new_flow.v2")) {
            return new NewCheckoutService();
        }
        return new LegacyCheckoutService();
    }
}
```

**Backend-specific concerns:**
- Evaluate flags per-request (not per-process) for correct targeting.
- Flag evaluation must be non-blocking with timeout (max 50ms) — use circuit breaker on flag SDK.
- Flag state changes propagate in < 200ms with streaming SDKs (LaunchDarkly), or polling interval (Flagsmith, Unleash).
- Database migrations guarded by flags: run migration first (backward-compatible), then enable flag, then clean up old schema when flag removed.

---

## Web Frontend (React/Vue/Svelte)

### Pattern 1: React with Provider + Hook

```tsx
// FlagProvider wraps the app
<FlagProvider client={flagsmith}>
  <App />
</FlagProvider>

// Hook for flag evaluation
function CheckoutPage() {
  const isNewFlow = useFlag("checkout.new_flow.v2");
  return isNewFlow ? <NewCheckoutFlow /> : <LegacyCheckoutFlow />;
}
```

### Pattern 2: No-Flash-of-Old-UI (SSR Hydration)

```tsx
// Server-side: evaluate flag, render correct component
export async function getServerSideProps(context) {
  const flags = await evaluateFlags(context.req);
  return { props: { isNewFlow: flags.isEnabled("checkout.new_flow.v2") } };
}

// Client-side: hydrate with server-returned state — no flash
function CheckoutPage({ isNewFlow }) {
  return isNewFlow ? <NewCheckoutFlow /> : <LegacyCheckoutFlow />;
}
```

### Pattern 3: CSS-Based Toggle (Zero-JS for layout changes)

```css
/* Flag class injected via attribute or CSS variable */
.checkout-layout[data-flag-new-checkout="true"] {
  grid-template-columns: 2fr 1fr;
}
.checkout-layout:not([data-flag-new-checkout="true"]) {
  grid-template-columns: 1fr;
}
```

**Web-specific concerns:**
- SSR hydration: evaluate flags server-side to avoid layout shift on client.
- CDN caching: flag-conditional content needs `Vary: X-Flag-State` header or cache-key variation.
- Polling interval: balance flag update freshness (100ms-5s) against CDN cache hit rate.
- Client-side flag evaluation must not block first paint — use async initialization with default fallback.

---

## iOS (Swift/SwiftUI)

### Pattern 1: Firebase Remote Config with SwiftUI

```swift
// Flag wrapper with offline-safe default
class FeatureFlags: ObservableObject {
    @Published var isNewCheckoutFlow = false
    private let remoteConfig = RemoteConfig.remoteConfig()

    init() {
        // 12-hour cache default; adjust for time-sensitive flags
        let settings = RemoteConfigSettings()
        settings.minimumFetchInterval = 43200 // 12 hours
        remoteConfig.configSettings = settings

        // Safe defaults (always safe offline and during review)
        remoteConfig.setDefaults([
            "checkout_new_flow_v2": false as NSObject
        ])
    }

    func fetch() async {
        do {
            let status = try await remoteConfig.fetchAndActivate()
            if status == .successFetchedFromRemote || status == .successUsingPreFetchedData {
                self.isNewCheckoutFlow = remoteConfig["checkout_new_flow_v2"].boolValue
            }
        } catch {
            // Defaults already set — app works offline and during review
        }
    }
}
```

### Pattern 2: Strategy Pattern with DI

```swift
protocol CheckoutStrategy {
    func process(cart: Cart) async throws -> Order
}

class LegacyCheckoutStrategy: CheckoutStrategy { ... }
class NewCheckoutStrategy: CheckoutStrategy { ... }

class CheckoutViewModel: ObservableObject {
    private let strategy: CheckoutStrategy

    init(flags: FeatureFlags) {
        self.strategy = flags.isNewCheckoutFlow
            ? NewCheckoutStrategy()
            : LegacyCheckoutStrategy()
    }
}
```

**iOS-specific concerns:**
- App Store review creates 1-14 day flag evaluation lag. Default values must be safe for the ENTIRE review window.
- Firebase Remote Config has a 12-hour minimum fetch interval by default. Force a shorter interval during development.
- When a flag is disabled server-side, installed apps with cached flag=ON will continue showing the feature until they fetch.
- Use `NSUserActivity` for Handoff: if a flag controls a feature, ensure the Handoff activity reflects the flag state so continuity doesn't expose disabled features.

---

## Android (Kotlin/Compose)

### Pattern 1: Firebase Remote Config with Compose

```kotlin
// Flag repository with offline-safe defaults
class FeatureFlagRepository(private val remoteConfig: FirebaseRemoteConfig) {
    init {
        val configSettings = remoteConfigSettings {
            minimumFetchIntervalInSeconds = 43200 // 12 hours
        }
        remoteConfig.setConfigSettingsAsync(configSettings)
        remoteConfig.setDefaultsAsync(mapOf(
            "checkout_new_flow_v2" to false
        ))
    }

    suspend fun fetch() {
        remoteConfig.fetchAndActivate()
    }

    val isNewCheckoutFlow: Boolean
        get() = remoteConfig.getBoolean("checkout_new_flow_v2")
}

// Compose ViewModel
@HiltViewModel
class CheckoutViewModel @Inject constructor(
    private val flags: FeatureFlagRepository
) : ViewModel() {
    val checkoutStrategy: CheckoutStrategy = if (flags.isNewCheckoutFlow) {
        NewCheckoutStrategy()
    } else {
        LegacyCheckoutStrategy()
    }
}
```

### Pattern 2: In-App Updates for Flag Refresh

```kotlin
// Force flag fetch when critical flags change
suspend fun fetchCriticalFlags() {
    val result = remoteConfig.fetch(0) // 0 = no cache, force fetch
    if (result) {
        remoteConfig.activate()
    }
}
```

**Android-specific concerns:**
- Firebase Remote Config: 12-hour default cache, same as iOS.
- Play Store review: 1-7 days typically, still a flag evaluation lag.
- Manufacturer-specific behavior: some OEMs aggressively kill background processes, preventing flag fetch. Always cache last-known-good flag state.
- In-app updates API can prompt users to update when a flag requires a newer app version.
- Material Design 3 Dynamic Color: when flags control theme variants, coordinate with `material-design-expert` to ensure color contrast stays WCAG-compliant across both flag states.

---

## Desktop (Electron/Tauri/Native)

### Pattern: No Store Review Delay — Use Web Patterns

Desktop apps don't have app store review windows, so flag evaluation lag is minimal (seconds, not days). Use the web frontend patterns with the added benefit of:
- Direct disk access for flag state caching
- Background process for flag sync
- No CDN cache between app and flag server
- Instant kill switch (sub-second evaluation latency)

**Desktop-specific concerns:**
- Auto-update pipeline: flag changes can be bundled with app updates (no store review).
- Offline mode: desktop apps may be used offline for extended periods. Cache more aggressively.
- Multi-window: flag state must be synchronized across all windows via IPC.

---

## Universal Pattern: Flag Evaluation Timeout

Every flag evaluation MUST have a timeout. Never block application startup on flag evaluation.

```go
// Go: context with timeout
ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
defer cancel()
enabled, err := flags.IsEnabledWithContext(ctx, "checkout.new_flow.v2")
if err != nil {
    // Timeout or error → use safe default (OFF for release toggles)
    enabled = false
}
```

```typescript
// TypeScript/JavaScript: Promise.race with timeout
const TIMEOUT_MS = 50;
const enabled = await Promise.race([
  flags.isEnabled("checkout.new_flow.v2"),
  new Promise<boolean>((resolve) => setTimeout(() => resolve(false), TIMEOUT_MS))
]);
```
