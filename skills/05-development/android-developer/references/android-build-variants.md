---
title: "Android Build Variants — Gradle Flavors, Build Types, and Signing"
author: Sandeep Kumar Penchala
date: 2026-07-24
---

## Build Variant Fundamentals

Android build variants are the cross-product of **build types** (debug, release) and **product flavors** (dev, staging, production). They allow different configurations, resources, and code for different deployment targets.

```
buildTypes × productFlavors = buildVariants

release × production = productionRelease
release × staging    = stagingRelease
debug   × production = productionDebug
debug   × staging    = stagingDebug
```

## Build Types (debug, release)

Build types define how the app is packaged and optimized. Every project has `debug` and `release` by default. Add custom types for additional packaging needs.

```kotlin
// app/build.gradle.kts
android {
    buildTypes {
        debug {
            applicationIdSuffix = ".debug"    // Different package name = installable alongside release
            isDebuggable = true
            isMinifyEnabled = false            // No R8 in debug — faster builds
            isShrinkResources = false
            buildConfigField("String", "BASE_URL", "\"https://dev-api.example.com\"")
            buildConfigField("Boolean", "ENABLE_LOGGING", "true")
        }
        release {
            isDebuggable = false
            isMinifyEnabled = true             // R8 enabled for release
            isShrinkResources = true           // Remove unused resources
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            buildConfigField("String", "BASE_URL", "\"https://api.example.com\"")
            buildConfigField("Boolean", "ENABLE_LOGGING", "false")
        }
        // Custom build type for QA testing — release optimizations + debug logging
        create("qa") {
            initWith(buildTypes.getByName("release"))
            isDebuggable = true
            applicationIdSuffix = ".qa"
            buildConfigField("String", "BASE_URL", "\"https://qa-api.example.com\"")
        }
    }
}
```

## Product Flavors — Multi-Environment

Product flavors define environment-specific configurations. Common flavors: `dev`, `staging`, `production`, or white-label flavors per client.

```kotlin
android {
    flavorDimensions += "environment"

    productFlavors {
        create("dev") {
            dimension = "environment"
            applicationIdSuffix = ".dev"
            versionNameSuffix = "-dev"
            buildConfigField("String", "API_BASE_URL", "\"https://dev-api.example.com\"")
            buildConfigField("String", "API_KEY", "\"dev_key_abc123\"")
            resValue("string", "app_name", "MyApp Dev")
        }
        create("staging") {
            dimension = "environment"
            applicationIdSuffix = ".staging"
            versionNameSuffix = "-staging"
            buildConfigField("String", "API_BASE_URL", "\"https://staging-api.example.com\"")
            buildConfigField("String", "API_KEY", "\"staging_key_def456\"")
            resValue("string", "app_name", "MyApp Staging")
        }
        create("production") {
            dimension = "environment"
            // No suffix — production is the base
            buildConfigField("String", "API_BASE_URL", "\"https://api.example.com\"")
            buildConfigField("String", "API_KEY", "\"prod_key_ghi789\"")
            resValue("string", "app_name", "MyApp")
        }
    }
}
```

## Multi-Dimension Flavors

Combine multiple flavor dimensions for complex configurations (environment × payment provider × theme):

```kotlin
android {
    flavorDimensions += listOf("environment", "payment")

    productFlavors {
        create("dev") { dimension = "environment"; /* ... */ }
        create("production") { dimension = "environment"; /* ... */ }

        create("stripe") { dimension = "payment"
            buildConfigField("String", "PAYMENT_PROVIDER", "\"stripe\"")
        }
        create("razorpay") { dimension = "payment"
            buildConfigField("String", "PAYMENT_PROVIDER", "\"razorpay\"")
        }
    }
    // Generates: devStripeDebug, devStripeRelease, productionStripeDebug, productionStripeRelease,
    //            devRazorpayDebug, devRazorpayRelease, productionRazorpayDebug, productionRazorpayRelease
}
```

## Flavor-Specific Resources

Flavor-specific source sets override the `main` source set at build time.

```
app/src/
├── main/           ← Shared code + resources
│   ├── java/
│   └── res/
├── dev/            ← Dev-only overrides
│   ├── java/       ← Dev-specific classes (mock implementations)
│   └── res/
│       └── values/
│           ├── strings.xml    ← "app_name": "MyApp Dev"
│           └── colors.xml     ← Dev-specific accent color (bright red to signal dev build)
├── staging/
│   └── res/values/strings.xml ← "app_name": "MyApp Staging"
└── production/
    └── res/values/strings.xml ← "app_name": "MyApp"
```

### Flavor-Specific Code

```kotlin
// main/java/com/app/di/NetworkModule.kt — common interface
interface AnalyticsTracker { fun track(event: String) }

// dev/java/com/app/di/AnalyticsModule.kt — dev implementation
class DevAnalyticsTracker @Inject constructor() : AnalyticsTracker {
    override fun track(event: String) { Log.d("Analytics", event) }
}

// production/java/com/app/di/AnalyticsModule.kt — production implementation
class ProdAnalyticsTracker @Inject constructor(
    private val firebaseAnalytics: FirebaseAnalytics
) : AnalyticsTracker {
    override fun track(event: String) { firebaseAnalytics.logEvent(event, null) }
}

// Binding in Hilt module (main source set — shared)
@Module @InstallIn(SingletonComponent::class)
abstract class AnalyticsModule {
    @Binds abstract fun bindAnalytics(tracker: ProdAnalyticsTracker): AnalyticsTracker
    // Dev source set provides its own @Binds to override in dev builds
}
```

## App Signing Configuration

Android requires all APKs/AABs to be digitally signed. Google Play's App Signing model separates your upload key from Google's app signing key.

```kotlin
android {
    signingConfigs {
        create("release") {
            // Load from local.properties (never committed to VCS)
            val keystoreProperties = Properties().apply {
                load(rootProject.file("local.properties").inputStream())
            }
            storeFile = file(keystoreProperties["RELEASE_STORE_FILE"] as String)
            storePassword = keystoreProperties["RELEASE_STORE_PASSWORD"] as String
            keyAlias = keystoreProperties["RELEASE_KEY_ALIAS"] as String
            keyPassword = keystoreProperties["RELEASE_KEY_PASSWORD"] as String
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            // ...
        }
    }
}
```

### local.properties (Never Commit!)

```properties
RELEASE_STORE_FILE=../keystore/release.jks
RELEASE_STORE_PASSWORD=super_secret_store_password
RELEASE_KEY_ALIAS=myapp_release
RELEASE_KEY_PASSWORD=super_secret_key_password
```

## BuildConfig vs Manifest Placeholders

```kotlin
android {
    defaultConfig {
        // BuildConfig fields: accessible as BuildConfig.FIELD_NAME in Kotlin
        buildConfigField("String", "API_VERSION", "\"v1\"")
        buildConfigField("int", "DB_VERSION", "3")
        buildConfigField("boolean", "FEATURE_NEW_UI", "true")

        // Manifest placeholders: used in AndroidManifest.xml
        manifestPlaceholders["appLabel"] = "MyApp"
        manifestPlaceholders["deepLinkScheme"] = "myapp"
    }
}
```

```xml
<!-- AndroidManifest.xml -->
<application android:label="${appLabel}">
    <activity android:name=".MainActivity">
        <intent-filter>
            <data android:scheme="${deepLinkScheme}" />
        </intent-filter>
    </activity>
</application>
```

## Gradle Convention Plugins

For multi-module projects, convention plugins eliminate copy-pasted `android { }` blocks.

```kotlin
// buildSrc/src/main/kotlin/android-library.gradle.kts
plugins {
    id("com.android.library")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.kapt") // or ksp
}

android {
    compileSdk = 34
    defaultConfig {
        minSdk = 26
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { compose = true }
    composeOptions { kotlinCompilerExtensionVersion = "1.5.8" }
}

// Usage in any module:
// plugins { id("android-library") }
```

## Source Sets Per Variant

Access variant-specific source directories:

```kotlin
android {
    sourceSets {
        // Dev flavor source set
        getByName("dev") {
            java.srcDirs("src/dev/java")
            res.srcDirs("src/dev/res")
            manifest.srcFile("src/dev/AndroidManifest.xml")
        }
        // Release build type source set
        getByName("release") {
            java.srcDirs("src/release/java")
        }
    }
}
```

## Variant Filtering

Exclude unwanted variant combinations to reduce build matrix:

```kotlin
android {
    variantFilter {
        val names = flavors.map { it.name } + buildType.name
        val variant = names.joinToString(separator = "").lowercase()

        // Exclude dev + release (dev builds are always debug)
        if (variant.contains("dev") && variant.contains("release")) {
            ignore = true
        }
    }
}
```

## Testing Across Variants

```kotlin
// Run specific variant tests
// ./gradlew testDevDebugUnitTest
// ./gradlew connectedProductionReleaseAndroidTest

// Test-only dependencies
dependencies {
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.8.0")

    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation("androidx.compose.ui:ui-test-junit4:1.6.0")

    // Dev-specific dependencies
    "devImplementation"("com.squareup.leakcanary:leakcanary-android:2.13")  // Only in dev builds
    "stagingImplementation"("com.facebook.stetho:stetho:1.6.0")            // Only in staging
}

// CI Pipeline: Assemble all release variants
// ./gradlew assembleProductionRelease assembleStagingRelease
```
