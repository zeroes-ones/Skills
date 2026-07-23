# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
| Sub-Skill | When to Use | Context |
|-----------|-------------|---------|
| `cross-platform-selection` | Choosing between React Native (Expo), Flutter, Swift/Kotlin native, or PWA | Performance requirements, team skills, time-to-market, platform-specific API needs, long-term maintenance cost |
| `navigation-architecture` | Designing tab/stack/drawer navigation with deep linking and universal links | React Navigation/GoRouter, `apple-app-site-association`, `assetlinks.json`, deferred deep links |
| `offline-first` | Building apps for unreliable connectivity, field workers, or data-entry-heavy workflows | WatermelonDB/Isar local DB, sync queue with conflict resolution (CRDT, LWW), network status monitoring |
| `push-notifications` | Implementing FCM/APNs with deep-link routing, rich media, and analytics | Token registration/refresh, notification channels (Android), provisional auth (iOS), foreground handling |
| `mobile-security` | Certificate pinning, Keychain/Keystore, biometric auth, root/jailbreak detection | SSL pinning with TrustKit/okhttp, secure enclave storage, code obfuscation (ProGuard/R8), runtime integrity checks |
| `performance-optimization` | Cold start < 1.5s, 60fps scrolling, memory < 50MB on low-end devices | Hermes engine tuning, FlatList/RecyclerView optimization, image caching tiers, main thread offloading |
| `app-store-deployment` | TestFlight, App Store Connect, Google Play Console, over-the-air updates (CodePush) | Store metadata (privacy labels, screenshots), phased rollout, app review guidelines, EAS Submit |
| `platform-design-compliance` | iOS HIG and Material Design 3 conformance: touch targets, safe areas, typography | 44pt/48dp touch targets, Dynamic Type/font scaling, Dark Mode, SafeArea/WindowInsets, platform-specific gestures |
