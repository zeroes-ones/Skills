# Xcode Build Settings Reference

## Critical Build Settings

```bash
# Debug vs Release differentiation
SWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG  # Debug only
SWIFT_OPTIMIZATION_LEVEL = -Osize            # Release: smallest binary
SWIFT_COMPILATION_MODE = wholemodule          # Release: slower compile, faster runtime

# Warnings as errors (add to project.pbxproj or xcconfig)
SWIFT_TREAT_WARNINGS_AS_ERRORS = YES
GCC_TREAT_WARNINGS_AS_ERRORS = YES

# Deployment target
IPHONEOS_DEPLOYMENT_TARGET = 16.0  # Support N-2 strategy
```

## xcconfig for Environment-Specific Builds

```
// Debug.xcconfig
SWIFT_ACTIVE_COMPILATION_CONDITIONS = $(inherited) DEBUG
BUNDLE_ID_SUFFIX = .debug
DISPLAY_NAME_SUFFIX =  Dev
OTHER_SWIFT_FLAGS = $(inherited) -DDEBUG

// Release.xcconfig
SWIFT_ACTIVE_COMPILATION_CONDITIONS = $(inherited) RELEASE
OTHER_SWIFT_FLAGS = $(inherited)
```

## Privacy Manifest (PrivacyInfo.xcprivacy) — Required April 2024+

```xml
<key>NSPrivacyTracking</key>
<false/>
<key>NSPrivacyCollectedDataTypes</key>
<array>
    <dict>
        <key>NSPrivacyCollectedDataType</key>
        <string>NSPrivacyCollectedDataTypeCrashData</string>
        <key>NSPrivacyCollectedDataTypeLinkedToUser</key>
        <false/>
        <key>NSPrivacyCollectedDataTypePurpose</key>
        <array><string>NSPrivacyCollectedDataTypePurposeAppFunctionality</string></array>
    </dict>
</array>
```
