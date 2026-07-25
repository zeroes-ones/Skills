## Gotchas

Real-world Apple platform traps and their business impact.

### 1. ATS Blocks HTTP Connections (~$50K)

**Symptom:** Network requests silently fail with `Error Domain=NSURLErrorDomain Code=-1022`.  
**Cause:** App Transport Security blocks plain HTTP connections.  
**Fix:** Add `NSAppTransportSecurity > NSAllowsArbitraryLoads` to `Info.plist` — but prefer per-domain exceptions:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSExceptionDomains</key>
    <dict>
        <key>api.staging.example.com</key>
        <dict>
            <key>NSExceptionAllowsInsecureHTTPLoads</key>
            <true/>
        </dict>
    </dict>
</dict>
```

**Impact:** $50K in delayed launch if discovered after App Store submission. Always test on a physical device — Simulator is more lenient with ATS.

### 2. Main Actor Isolation Warning Cascade (~$20K)

**Symptom:** `Expression requiring global actor 'MainActor' cannot appear in default-value expression of property '_viewModel'`.  
**Cause:** `@StateObject` / `@State` on a `@MainActor`-isolated type in a non-isolated View.  
**Fix:** Annotate the View with `@MainActor`:

```swift
@MainActor
struct ProductListView: View {
    @State private var viewModel = ProductListViewModel() // OK now
    // ...
}
```

**Impact:** A cascade of 40+ compiler errors from one missing annotation. $20K in wasted debugging time per large feature.

### 3. Retain Cycles in Closures (~$100K memory leak)

**Symptom:** ViewModel never deinitializes; `deinit` never called. Memory grows with each navigation cycle.  
**Cause:** Strong capture of `self` in escaping closures:

```swift
// WRONG — retains self forever
service.onUpdate = { self.products = $0 }

// RIGHT — weak capture
service.onUpdate = { [weak self] products in
    self?.products = products
}
```

**Impact:** Memory leak causing app termination by jetsam. $100K+ user churn when app reliably crashes after 10-15 navigation cycles.

### 4. unowned Crash in Asynchronous Context (~$75K)

**Symptom:** `Thread 1: EXC_BAD_ACCESS` or `Fatal error: Attempted to read an unowned reference but the object was already deallocated`.  
**Cause:** `[unowned self]` when `self` can deallocate before the closure executes:

```swift
// WRONG — imageLoader may outlive self
imageLoader.load { [unowned self] image in
    self.imageView.image = image // CRASH
}

// RIGHT
imageLoader.load { [weak self] image in
    self?.imageView?.image = image
}
```

**Rule:** `unowned` is safe ONLY when the captured object is guaranteed to outlive the closure — e.g., a parent capturing its child. In async contexts, always use `weak`.

**Impact:** $75K (crash rate spike → 2-star App Store rating → 30% conversion drop).

### 5. Core Data Thread Confinement (~$60K)

**Symptom:** `CoreData: error: Serious application error. An exception was caught from the delegate... NSManagedObjectContext is accessed from wrong thread`.  
**Cause:** Reading `NSManagedObject` properties on a thread other than its context's queue.  
**Fix:**

```swift
// WRONG — viewContext is main-queue only
DispatchQueue.global().async {
    let count = context.registeredObjects.count // CRASH
}

// RIGHT — use perform/performAndWait
context.perform {
    let count = context.registeredObjects.count
}

// EVEN BETTER — pass objectID across threads
let objectID = managedObject.objectID
Task.detached {
    let context = PersistenceController.shared.container.newBackgroundContext()
    let object = context.object(with: objectID)
    // Use object safely here
}
```

**Impact:** $60K — intermittent crashes impossible to reproduce, leading to negative reviews and support burden.

### 6. SwiftUI View Identity Breakage (~$40K)

**Symptom:** Animations break, `onAppear` fires unexpectedly, state resets.  
**Cause:** Using `id(_:)` unnecessarily, or relying on indices for `ForEach` with mutable data:

```swift
// WRONG — index-based identity; state lost on reorder
ForEach(0..<items.count, id: \.self) { index in
    ItemRow(item: items[index])
}

// RIGHT — stable identity from model
ForEach(items) { item in
    ItemRow(item: item)
}
```

**Impact:** $40K in UX debt. Users report "the app glitches when I scroll fast." Debugging SwiftUI identity issues can take days.

### 7. Xcode Previews Crash Silently (~$15K)

**Symptom:** Preview canvas shows "Preview Crashed" or hangs on spinner.  
**Cause (common):**

```swift
// Previews try to access Keychain, UserDefaults suite, or network
#Preview {
    ProductListView()
        .onAppear {
            // This fires in preview too!
            APIKeyManager.shared.configure() // 💥 crash
        }
}

// FIX — guard against preview environment
#Preview {
    ProductListView()
        .environment(\.isPreview, true)
}
```

Or use mock services in previews: `ProductListView(service: MockAPIService())`.

**Impact:** $15K per feature. Developers lose preview productivity and revert to simulator-only iteration.

### 8. Missing Entitlement Silently Breaks Feature (~$45K)

**Symptom:** Feature works on Simulator, fails on device with no clear error.  
**Example:** Push notifications silently fail without `aps-environment` entitlement. iCloud sync quietly doesn't work without `com.apple.developer.icloud-container-identifiers`.  
**Fix:** Verify entitlements in `App.entitlements`:

```xml
<key>aps-environment</key>
<string>development</string>
<key>com.apple.developer.icloud-container-identifiers</key>
<array>
    <string>iCloud.com.example.app</string>
</array>
```

**Impact:** $45K — feature flagged "complete" for weeks before device testing reveals it never worked.

---
