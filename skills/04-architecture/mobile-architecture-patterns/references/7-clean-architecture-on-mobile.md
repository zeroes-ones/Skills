## 7. Clean Architecture on Mobile

Clean Architecture on mobile adds domain and data layers around the presentation layer. The key constraint: **dependencies point inward.** Domain knows nothing about data sources. Presentation knows nothing about APIs.

### Layer Diagram

```
┌─────────────────────────────────────────────────────┐
│  PRESENTATION (iOS: SwiftUI/UIKit, Android: Compose) │
│  ViewModels, Views, Coordinators                    │
├─────────────────────────────────────────────────────┤
│  DOMAIN (Pure Kotlin/Swift, no platform imports)     │
│  Entities, UseCases, Repository Interfaces          │
├─────────────────────────────────────────────────────┤
│  DATA (Platform-specific implementations)            │
│  Repository Impl, API (Retrofit/URLSession),         │
│  Database (Room/Core Data), DataSources             │
└─────────────────────────────────────────────────────┘
```

### Dependency Rule

- Domain has zero dependencies on platform frameworks
- Data depends on Domain (implements repository interfaces)
- Presentation depends on Domain (calls use cases)

Full implementation in `references/clean-architecture-mobile.md`.

---
