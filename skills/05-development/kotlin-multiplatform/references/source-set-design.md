# Source-Set Design — Hierarchy Template, commonMain Discipline

## The Source-Set Map

```
shared/
├── commonMain/     # genuinely shared: domain models, validation, use cases, DTOs
├── androidMain/    # Android actuals, Android-specific integrations
├── iosMain/        # iOS actuals, iOS-specific integrations
└── commonTest/     # shared tests that run on EVERY target
```

## The Hierarchy Template

The default hierarchy template creates intermediate source sets so you can share code between groups of targets (e.g., all Apple targets) without dumping it into commonMain. Design the hierarchy deliberately:

- **commonMain** — truly universal logic.
- **appleMain** (if present) — shared across iOS/macOS/watchOS targets.
- **androidMain / iosMain** — platform halves for expect/actual.

## commonMain Discipline

| Allowed in commonMain | NOT allowed |
|----------------------|-------------|
| Pure Kotlin logic (models, validation, use cases) | `java.*` imports |
| kotlinx libraries (coroutines, serialization, datetime) | UIKit / Android framework APIs |
| Multiplatform libraries (Ktor client, SQLDelight) | Platform file/date/random APIs (use expect/actual or kotlinx) |
| `expect` declarations | Platform-specific singleton patterns |

## The expect/actual Contract

- Every `expect` is a promise both platforms honor; keep the surface **small and stable**.
- Signatures must match exactly across actuals (the compiler enforces it — visibility, type params, and modifiers included).
- Prefer libraries over expects: Ktor/SQLDelight/kotlinx cover most needs; expects are for genuine platform capabilities (Keychain, network status, device info, secure storage).

## Inventory Sheet

Document for every expect:

| expect | commonMain type | androidMain actual | iosMain actual | Stable? |
|--------|-----------------|--------------------|----------------|---------|
| KeychainStore | `expect class` | EncryptedSharedPreferences | Keychain/SSKeychain | yes |

## Common Mistakes

- Expect added, actual forgotten → compile error on one target (Error Decoder row 1).
- Convenience expects multiply → every change ripples to both platforms.
- Platform code in commonMain → iOS build breaks (Anti-Pattern row 1).
