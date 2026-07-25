## Decision Trees

### 1. SwiftUI vs UIKit

```
Building a new screen on iOS
├── Minimum deployment target ≥ iOS 16?
│   ├── YES → Does it need UIKit-only features?
│   │   ├── YES (MKMapView, WKWebView, UIImagePicker, PDFKit, rich text editing)
│   │   │   └── Use UIViewControllerRepresentable wrapping UIKit
│   │   └── NO  → Use SwiftUI with NavigationStack
│   └── NO (iOS 15 or lower)
│       ├── Complex collection views, custom layouts, or pixel-perfect control
│       │   └── Use UIKit (UICollectionView with compositional layout)
│       └── Simple forms, lists, or settings
│           └── Use SwiftUI (back-deploy most modifiers to iOS 15)
└── Need to integrate with existing UIKit codebase?
    ├── YES → Wrap SwiftUI in UIHostingController; UIKit owns navigation
    └── NO  → Pure SwiftUI with NavigationStack
```

### 2. Architecture Pattern

```
Choosing architecture for an iOS app
├── Solo developer or team of 2-3?
│   └── MVVM (ObservableObject + @Published or @Observable macro on iOS 17+)
│       Pros: Simple, Apple-aligned, great SwiftUI binding
│       Cons: No strict unidirectional flow; can get messy at scale
├── Team of 4-10, complex state, needs testability?
│   ├── TCA (The Composable Architecture by Point-Free)
│   │   Pros: Strict unidirectional flow, exhaustive testing, excellent debugging
│   │   Cons: Learning curve, boilerplate, dependency on third-party framework
│   └── MVVM + UseCases + Coordinators
│       Pros: Familiar, separates concerns without framework lock-in
│       Cons: Requires discipline to keep ViewModels thin
├── Large enterprise with many modules?
│   └── VIPER or Clean Swift
│       Pros: Maximum separation, module-level independence
│       Cons: Massive boilerplate, slow to iterate
└── Prototyping or hackathon?
    └── MVC (just get it working; refactor later)
```

### 3. Concurrency Choice

```
Handling async work
├── Simple network call, single result?
│   └── async/await with URLSession.shared.data(from:)
├── Stream of values over time?
│   ├── iOS 17+ → AsyncSequence (AsyncStream, AsyncThrowingStream)
│   └── iOS 13-16 → Combine (AnyPublisher, @Published)
├── Need background task that survives app suspension?
│   └── BGTaskScheduler (BGAppRefreshTask / BGProcessingTask)
├── Heavy computation, don't block main thread?
│   └── Task.detached(priority: .background) { ... } with actor isolation
├── Shared mutable state across concurrency domains?
│   └── actor with Sendable-conforming types
└── Legacy codebase with DispatchQueue?
    └── Bridge with Continuation: withCheckedContinuation / withCheckedThrowingContinuation
```

### 4. Data Persistence

```
Choosing persistence layer
├── iOS 17+ only, SwiftUI app?
│   └── SwiftData (@Model, @Query, @Environment(\\.modelContext))
│       Pros: Zero-setup, Swift-native, automatic iCloud sync opt-in
│       Cons: Immature, limited query expressiveness, migration story evolving
├── iOS 13-16, or need fine-grained control?
│   ├── Core Data + NSPersistentCloudKitContainer
│   │   Pros: Mature, powerful, CloudKit sync built-in
│   │   Cons: Verbose, concurrency pitfalls, migration complexity
│   └── GRDB (SQLite wrapper)
│       Pros: Raw SQL when needed, observation with ValueObservation, fast
│       Cons: Third-party, no built-in CloudKit sync
├── Real-time sync, collaborative features?
│   └── CloudKit (CKContainer, CKDatabase) directly
│       Pros: Apple-managed, free tier generous, private database per user
│       Cons: No server-side logic, eventual consistency
├── Key-value settings, preferences?
│   └── @AppStorage or UserDefaults
└── Secure storage (tokens, credentials)?
    └── Keychain (via Security framework or SwiftKeychainWrapper)
```

### 5. App Distribution

```
Distributing your app
├── Development/testing phase?
│   ├── Simulator → Just build and run (⌘R)
│   ├── Physical device → Xcode auto-signing with Personal Team or Developer account
│   └── Internal testers (≤100) → TestFlight Internal (no review, instant)
├── Beta testing?
│   └── TestFlight External (≤10,000 testers)
│       ├── First build → Requires Beta App Review (~24-48 hours)
│       └── Subsequent builds → No review unless significant changes
├── Production release?
│   └── App Store Connect submission
│       ├── Passes App Review (~24 hours typical, up to 5 days)
│       ├── Options: Manual release, phased release (7 days), auto-release
│       └── Must pass: no crashes, complete metadata, privacy labels, export compliance
└── Enterprise/Internal distribution?
    ├── Apple Business Manager + MDM → For employees
    └── Enterprise Program (in-house) → For internal-only apps (no App Store)
```

### 6. Animation Performance

```
Animation jank detected
├── Running on simulator? → Test on device first; simulator ≠ device GPU
├── Check Instruments > Core Animation template
│   ├── FPS consistently <55? → Too much work on main thread
│   │   └── Profile with Time Profiler; offload heavy work
│   ├── "Hitches" detected? → Inconsistent frame pacing
│   └── "Impact" > 10ms? → Identify the slow phase
├── Using implicit animations (.animation modifier)?
│   └── Prefer withAnimation { } block for explicit control
├── Animating layout (offset, frame)?
│   └── Use .drawingGroup() to rasterize, or Canvas for custom drawing
├── Animating many views simultaneously?
│   └── Reduce to animating a single container; use matchedGeometryEffect for transitions
├── Shadows or blurs during animation?
│   └── Cache shadow path: view.layer.shadowPath = UIBezierPath(…).cgPath
└── List/ScrollView during animation?
    └── Avoid GeometryReader inside scrolling lists; use .scrollPosition(id:) instead
```

---
