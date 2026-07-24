# Play Store Deployment — Android Developer Reference

> **Parent skill:** [android-developer](../SKILL.md) | **Load condition:** When preparing app for Play Store submission or debugging release issues

## Play App Signing

Google's signing model has two keys: your **upload key** (you sign AABs submitted to Play) and Google's **app signing key** (Google signs distributed APKs). You can reset the upload key. You can NEVER recover the app signing key — losing it means unpublishing and starting fresh with a new package name.

```kotlin
// app/build.gradle.kts — signing config from CI env vars, NEVER commit keystore
android {
    signingConfigs {
        create("release") {
            storeFile = rootProject.file("upload-keystore.jks")
            storePassword = System.getenv("KEYSTORE_PASSWORD") ?: ""
            keyAlias = System.getenv("KEY_ALIAS") ?: ""
            keyPassword = System.getenv("KEY_PASSWORD") ?: ""
        }
    }
}
```

**Critical post-setup verification:**
```bash
# Compare upload key SHA-1 with Play Console → App Signing → Upload key certificate
keytool -list -v -keystore upload-keystore.jks | grep SHA1
```

**Disaster recovery protocol:**
1. Backup upload keystore to password manager + encrypted drive
2. Store `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD` in CI secrets (GitHub Secrets, GitLab CI Variables)
3. If upload key is lost: generate new upload key, contact Google support for reset. Only possible if enrolled in Play App Signing.
4. If NOT enrolled in Play App Signing and lose key = app permanently dead. Unpublish, new package name, lose all users.

## AAB vs APK — Always Use AAB

```bash
# Generate App Bundle (AAB) — Google splits per-device APKs automatically
./gradlew bundleRelease
# Output: app/build/outputs/bundle/release/app-release.aab

# Generate universal APK (for testing only — never submit to Play)
./gradlew assembleRelease
```

AAB benefits: Google Play generates optimized APKs per device (ABI, density, language), reducing download size 15-35%. Dynamic feature modules and asset delivery only work with AAB.

## Build Types & Signing Configs

```kotlin
// app/build.gradle.kts
android {
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.app"
        minSdk = 26
        targetSdk = 35
        versionCode = 42
        versionName = "2.1.0"
    }

    buildTypes {
        debug {
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
            isMinifyEnabled = false
            signingConfig = signingConfigs.getByName("debug")
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro",
            )
            signingConfig = signingConfigs.getByName("release")
            ndk { abiFilters += listOf("arm64-v8a") }  // Drop x86 for release
        }
    }
}
```

## Release Tracks

| Track | Purpose | Typical Cadence |
|-------|---------|-----------------|
| **Internal** | Team testing. Available <1 min. | Every CI push |
| **Alpha (Closed)** | External testers (<100). | Weekly |
| **Beta (Open)** | Public opt-in beta. | Bi-weekly |
| **Production** | All users. Staged rollout. | Per sprint/monthly |

### Staged Rollout Strategy

```
10% → monitor crash rate 6-24h → 25% → monitor 12-24h → 50% → monitor 24h → 100%
```

**Halt criteria:**
- Crash rate exceeds 0.5% (Play Console threshold)
- ANR rate exceeds 0.47%
- Critical user-reported bug in feedback channel
- Revenue drop >5%

```bash
# Pull crash stats during rollout via Google Play Developer API
gcloud play androidpublisher reviews list --package-name com.example.app
```

## In-App Review API

```kotlin
// Max once per 30 days (Google-enforced). Never show custom review prompt.
// implementation("com.google.android.play:review-ktx:2.0.1")
class ReviewManager(private val activity: Activity) {

    fun requestReview() {
        val manager = ReviewManagerFactory.create(activity)
        manager.requestReviewFlow().addOnCompleteListener { request ->
            if (request.isSuccessful) {
                manager.launchReviewFlow(activity, request.result)
                    .addOnCompleteListener { /* Review dialog shown or dismissed */ }
            }
            // If !isSuccessful: quota exceeded (30-day limit), device incompatible, or
            // user already reviewed this version. Silently no-op — never show fallback.
        }
    }
}

// Trigger points (pick ONE):
// - After user completes a meaningful action (e.g., 5th purchase, 3rd session in week)
// - After user dismisses an interstitial naturally (don't interrupt workflow)
// - NEVER on app open, during onboarding, or after a crash
```

## Billing 7.x — Subscriptions & One-Time Purchases

```kotlin
// implementation("com.android.billingclient:billing-ktx:7.1.1")
@HiltViewModel
class BillingViewModel @Inject constructor(
    private val billingClient: BillingClient,
) : ViewModel() {

    private val _purchases = MutableStateFlow<List<Purchase>>(emptyList())
    val purchases: StateFlow<List<Purchase>> = _purchases.asStateFlow()

    init {
        billingClient.startConnection(object : BillingClientStateListener {
            override fun onBillingSetupFinished(result: BillingResult) {
                if (result.responseCode == BillingResponseCode.OK) {
                    queryPurchases()
                }
            }
            override fun onBillingServiceDisconnected() { /* Retry connection */ }
        })
    }

    fun purchaseProduct(activity: Activity, productDetails: ProductDetails) {
        val flowParams = BillingFlowParams.newBuilder()
            .setProductDetailsParamsList(listOf(
                BillingFlowParams.ProductDetailsParams.newBuilder()
                    .setProductDetails(productDetails)
                    .setOfferToken(productDetails.subscriptionOfferDetails?.firstOrNull()?.offerToken ?: "")
                    .build()
            ))
            .build()
        billingClient.launchBillingFlow(activity, flowParams)
    }

    private fun queryPurchases() {
        // Query active subscriptions
        billingClient.queryPurchasesAsync(QueryPurchasesParams.newBuilder()
            .setProductType(BillingClient.ProductType.SUBS).build()
        ) { result, purchases ->
            if (result.responseCode == BillingResponseCode.OK) {
                _purchases.value = purchases
            }
        }
    }
}

// CRITICAL: Acknowledge all purchases within 3 days or Google auto-refunds.
// Handle PENDING state (slow payment methods in India, Brazil, etc.):
fun handlePurchase(purchase: Purchase) {
    if (purchase.purchaseState == Purchase.PurchaseState.PURCHASED) {
        if (!purchase.isAcknowledged) {
            billingClient.acknowledgePurchase(AcknowledgePurchaseParams.newBuilder()
                .setPurchaseToken(purchase.purchaseToken).build()
            ) { result -> /* Grant entitlement */ }
        }
    } else if (purchase.purchaseState == Purchase.PurchaseState.PENDING) {
        // Show "Payment processing..." UI. Do NOT grant entitlement yet.
        // Google retries for up to 24 hours. Listen for PurchaseStateUpdated.
    }
}
```

## Pre-Submission Checklist

1. **`targetSdkVersion 35`** — required within 1 year of Android 15 release (August 2025)
2. **Privacy policy URL** in Play Console AND in-app settings — mandatory if collecting personal data
3. **Data safety form** completed — declare ALL data types collected/shared (location, contacts, identifiers, financial)
4. **IARC content rating** questionnaire — fill out honestly or face removal
5. **`android:debuggable="false"`** — Play rejects debuggable APKs/AABs. Verify: `aapt dump badging app-release.aab | grep debuggable`
6. **Permissions Declaration Form** required for: `ACCESS_BACKGROUND_LOCATION`, `QUERY_ALL_PACKAGES`, `MANAGE_EXTERNAL_STORAGE`, `REQUEST_INSTALL_PACKAGES`, `BIND_ACCESSIBILITY_SERVICE`, `BIND_NOTIFICATION_LISTENER_SERVICE`
7. **Screenshots**: 2 phone (6.5" 16:9 or 20:9), 7" tablet (if tablet-supported), 10" tablet (if tablet-supported)
8. **Upload key SHA-1** verified against Play Console → App Signing
9. **Managed publishing** enabled to control release timing
10. **Feature graphic** (1024×500px PNG/JPG, <1MB) for store listing

### Permissions Declaration Details

```xml
<!-- These require Play Console declaration + Google review: -->
<uses-permission android:name="android.permission.ACCESS_BACKGROUND_LOCATION" />
<!-- Requires: prominent disclosure dialog BEFORE system permission dialog -->
<!-- Requires: in-app video demo showing location feature -->

<uses-permission android:name="android.permission.QUERY_ALL_PACKAGES" />
<!-- Requires: justification why you need to see ALL installed packages -->
<!-- Acceptable: device search, file management, accessibility, browser -->
<!-- Rejected: advertising, analytics without clear user benefit -->

<uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE" />
<!-- Requires: core functionality justification (file manager, document editor) -->
<!-- Rejected: just to cache media files — use MediaStore or app-specific storage -->

<uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />
<!-- Requires: app is a browser, file manager, or enterprise device management -->
<!-- Rejected for most apps — update workflow should use Play Store updates -->
```

## Store Listing Best Practices

```markdown
# App Title (30 characters)
App Name: Core Purpose

# Short Description (80 characters)
One-line value proposition. Include primary keyword.

# Full Description (4000 characters)
1. Opening hook (2-3 sentences) — problem you solve
2. Key features as bullet points (5-7)
3. Social proof: "Trusted by X users", awards, press mentions
4. Call to action: "Download now and start..."
5. NO promotional fluff — be concrete about what the app DOES

# Graphic Assets
- Icon: 512×512px PNG, no alpha, <1MB. Adaptive icon with foreground + background layers.
- Feature graphic: 1024×500px. No text on left 25% (overlapped by icon on Play Store).
- Phone screenshots: 1080×1920px (or any 16:9). Show UI with device frame.
- Promo video (optional): YouTube URL, 30s-2min, show real app UI.
```

## Pre-Launch Report

Play Console automatically runs your app on test devices (Firebase Test Lab) before release:
- **Stability**: Crashing on any device blocks release
- **Performance**: Slow rendering flagged with per-device details
- **Accessibility**: `contentDescription` missing, touch target too small, contrast violations
- **Security**: SSL/TLS issues, cleartext HTTP, WebView vulnerabilities
- **Permissions**: Unused permissions flagged
- **Background Location**: Must have `android:foregroundServiceType="location"` in manifest

```bash
# Review pre-launch report in Play Console or via API:
# Play Console → Release → Pre-launch report → View details
```

## Common Rejections & Fixes

| Rejection | Cause | Fix |
|-----------|-------|-----|
| **"Impersonation"** | App name/icon too similar to another brand | Completely unique branding. No "for X" naming. |
| **"Minimum functionality"** | App doesn't do enough — static website wrapper, single wallpaper | Add unique functionality, user accounts, data persistence. |
| **"Background location"** | No prominent disclosure before system dialog | Custom dialog explaining why, in-app video, submit to Play Console. |
| **"All files access"** | `MANAGE_EXTERNAL_STORAGE` without core file management | Use MediaStore, SAF, or app-specific storage. Submit video justification. |
| **"Misleading claims"** | Screenshots show features not in the app | Screenshots must be actual app screens. No mockups. |
| **"WebView spam"** | App is just a WebView wrapping a website | Add native functionality (offline, notifications, camera, location). |
| **"Copycat"** | Repackaging another app's APK with minor changes | Original codebase, unique features, different value proposition. |

## Android Vitals Monitoring

Critical thresholds on Play Console → Android Vitals:

| Metric | Bad Behavior Threshold | Action |
|--------|----------------------|--------|
| **ANR rate** | >0.47% | Bad-behavior badge, search rank penalty |
| **Crash rate** | >1.09% | Bad-behavior badge for user-perceived crashes |
| **Slow rendering** | >15% of frames >16ms | User-perceived jank, poor rating correlation |
| **Frozen frames** | >0.1% of frames >700ms | Severe UX impact — users perceive app as frozen |
| **Stuck wake locks** | >0.1% of sessions >1h | Battery drain — 1★ review risk |
| **Excessive wakeups** | >10 wakeups/hour in background | Doze-violation — Play Store policy violation |

```kotlin
// Monitor in-app with Firebase Crashlytics
// implementation(platform("com.google.firebase:firebase-bom:33.0.0"))
// implementation("com.google.firebase:firebase-crashlytics-ktx")
// implementation("com.google.firebase:firebase-analytics-ktx")

// Custom keys for debugging release builds
FirebaseCrashlytics.getInstance().setCustomKey("build_variant", BuildConfig.FLAVOR)
FirebaseCrashlytics.getInstance().setCustomKey("device_ram_mb", Runtime.getRuntime().maxMemory() / 1024 / 1024)
```

## Managed Publishing Workflow

```bash
# CI workflow (GitHub Actions example):
jobs:
  deploy-play-store:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build AAB
        run: ./gradlew bundleRelease
      - name: Upload to Play Console (Internal track)
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.PLAY_STORE_SERVICE_ACCOUNT }}
          packageName: com.example.app
          releaseFile: app/build/outputs/bundle/release/app-release.aab
          track: internal
          status: completed  # Auto-publish to internal track
          # For production: track: production, status: draft (managed publishing)
```

**Managed publishing flow:**
1. Upload AAB to production track with `status: draft`
2. Review pre-launch report for crashes and a11y violations
3. Manually click "Start rollout to production" in Play Console
4. Monitor Android Vitals during rollout
5. If issues detected → "Halt rollout" button preserves current split
6. Upload fix as new release → rollout resumes where it left off
