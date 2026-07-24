# App Store Submission Reference

## Pre-Submission Checklist

```bash
# 1. Archive with Release configuration
xcodebuild archive \
  -workspace App.xcworkspace \
  -scheme App \
  -configuration Release \
  -archivePath ./build/App.xcarchive

# 2. Validate archive
xcodebuild -exportArchive \
  -archivePath ./build/App.xcarchive \
  -exportPath ./build/App \
  -exportOptionsPlist ExportOptions.plist \
  -allowProvisioningUpdates
```

## ExportOptions.plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "…">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>teamID</key>
    <string>YOUR_TEAM_ID</string>
    <key>uploadBitcode</key>
    <false/>
    <key>manageAppVersionAndBuildNumber</key>
    <true/>
</dict>
</plist>
```

## Common Rejections (with $ Impact)
- **4.2 Minimum Functionality** (~$15K delay cost): App too simple; add meaningful features
- **2.1 App Completeness** (~$10K): Crashes on launch; test on oldest supported device
- **5.1.1 Data Collection** (~$8K legal risk): Missing privacy manifest; add PrivacyInfo.xcprivacy
- **3.1.1 In-App Purchase** (~$20K revenue loss): Using third-party payment; must use StoreKit 2

## TestFlight Distribution
- Internal: Up to 100 testers, no review required
- External: Up to 10,000 testers, Beta App Review required for first build
