# Universal Binary Builds — Apple Silicon + Intel

<!-- STANDARD: 3min -- configure Xcode and CI for arm64 + x86_64 -->

## What Is a Universal Binary?

A Universal Binary (also called "Universal 2") contains executable code compiled for both:
- **arm64** — Apple Silicon (M1, M2, M3, M4 series)
- **x86_64** — Intel Macs (Core i5/i7/i9, Xeon)

When a user launches the app, macOS loads only the architecture slice that matches their processor. The other slice is never loaded into memory.

As of 2026, ~5-15% of active Macs are still Intel-based, concentrated in enterprise fleets and Mac Pro workstations.

---

## Build Configuration

### Xcode Project Settings

| Setting | Value | Notes |
|---|---|---|
| `ARCHS` (Architectures) | `arm64 x86_64` | Build for both architectures |
| `ONLY_ACTIVE_ARCH` | `YES` for Debug, `NO` for Release | Debug builds only for your dev machine; Release builds for both |
| `EXCLUDED_ARCHS` | **DO NOT SET** for Release | NEVER exclude arm64 from Release builds |
| `VALID_ARCHS` | `arm64 x86_64` | Limit to supported architectures |

### .xcconfig File (Recommended)

```bash
// Release.xcconfig
ARCHS = arm64 x86_64
ONLY_ACTIVE_ARCH = NO
MACOSX_DEPLOYMENT_TARGET = 13.0

// Debug.xcconfig
ARCHS = $(NATIVE_ARCH)
ONLY_ACTIVE_ARCH = YES
MACOSX_DEPLOYMENT_TARGET = 13.0
```

### Swift Package Manager

```swift
// Package.swift
let package = Package(
    name: "YourPackage",
    platforms: [
        .macOS(.v13)
    ],
    targets: [
        .target(
            name: "YourTarget",
            // SPM builds Universal by default. No special config needed.
        )
    ]
)
```

---

## Building from Command Line

```bash
# Build Universal Binary for Release
xcodebuild -project YourApp.xcodeproj \
  -scheme YourApp \
  -configuration Release \
  -archivePath build/YourApp.xcarchive \
  ARCHS="arm64 x86_64" \
  ONLY_ACTIVE_ARCH=NO \
  archive

# Verify the result
lipo -archs build/YourApp.xcarchive/Products/Applications/YourApp.app/Contents/MacOS/YourApp
# Expected: arm64 x86_64
```

---

## Verifying Universal Binary

### Check Main Executable
```bash
lipo -info /path/to/YourApp.app/Contents/MacOS/YourApp
# Output: Architectures in the fat file: ... are: arm64 x86_64
```

### Check All Embedded Frameworks
```bash
# Find all Mach-O binaries in the app bundle
find /path/to/YourApp.app -type f -exec file {} \; | grep Mach-O

# Verify each contains required architectures
for bin in $(find /path/to/YourApp.app -type f -exec file {} \; | grep 'Mach-O' | cut -d: -f1); do
  ARCHS=$(lipo -archs "$bin")
  if [[ "$ARCHS" != *"arm64"* ]] || [[ "$ARCHS" != *"x86_64"* ]]; then
    echo "WARNING: $bin has architectures: $ARCHS"
  fi
done
```

### Thin a Universal Binary (for debugging)
```bash
# Extract just arm64 for testing on Apple Silicon
lipo /path/to/YourApp.app/Contents/MacOS/YourApp \
  -extract arm64 \
  -output /tmp/YourApp_arm64

# Extract just x86_64 for testing under Rosetta
lipo /path/to/YourApp.app/Contents/MacOS/YourApp \
  -extract x86_64 \
  -output /tmp/YourApp_x86_64
```

---

## Common Issues

### Issue 1: "Building for macOS, but the linked framework 'Foo.framework' was built for iOS"

**Cause**: A dependency only has iOS slices, not macOS slices.
**Fix**: Ensure all third-party frameworks include macOS slices. Use `lipo -info` on every framework in your dependency chain.

### Issue 2: "ld: warning: ignoring file ... building for macOS-arm64 but attempting to link with file built for macOS-x86_64"

**Cause**: A precompiled static library doesn't include the arm64 slice.
**Fix**: Rebuild the library as Universal, or use `lipo -create` to combine arm64 and x86_64 `.a` files.

### Issue 3: App Store Connect rejects with "ITMS-90207: Invalid Bundle. The bundle ... does not support the minimum OS version"

**Cause**: One embedded binary targets a higher deployment target than the main app.
**Fix**: Check `LC_VERSION_MIN_MACOSX` in every binary:
```bash
otool -l /path/to/binary | grep -A3 LC_VERSION_MIN_MACOSX
```

### Issue 4: Archive is x86_64 only even though ARCHS is set

**Cause**: `EXCLUDED_ARCHS[sdk=macosx*] = arm64` in build settings (a common cargo-cult from early Apple Silicon transition issues).
**Fix**: Remove ALL `EXCLUDED_ARCHS` settings from Release configuration.

---

## Binary Size Considerations

| Configuration | Typical App Size |
|---|---|
| arm64 only | 8-15 MB |
| x86_64 only | 9-17 MB |
| Universal (arm64 + x86_64) | 17-30 MB |

App Thinning on the App Store automatically delivers only the architecture slice the user needs. Your uploaded archive is Universal (30MB), but users download only their architecture (15MB). Direct distribution via DMG doesn't get thinning — users download the full Universal binary.

### Reduce Binary Size
- Strip debug symbols: `STRIP_INSTALLED_PRODUCT = YES`, `STRIP_STYLE = all`
- Remove simulator slices from frameworks in the archive
- Enable `COMPRESS_PNG_FILES = YES`
- Use `SWIFT_COMPILATION_MODE = wholemodule` with `SWIFT_OPTIMIZATION_LEVEL = -Osize`

---

## Rosetta 2 Translation

If you ship an x86_64-only binary, Apple Silicon Macs run it via Rosetta 2 translation:
- **Performance**: 20-40% slower than native arm64
- **Startup**: First launch has ~1-2 second translation delay
- **Memory**: Translated code uses ~15% more memory
- **Compatibility**: Most apps work, but JIT, kernel extensions, and hypervisor frameworks do not translate

**Always prefer native arm64 over Rosetta.** Ship Universal unless you have a specific reason not to.

---

## Universal Binary with Third-Party Frameworks

### Sparkle (Update Framework)
Sparkle ships as a Universal Binary. No special handling needed.

### Firebase / Crashlytics
Some Firebase binaries are x86_64 only. Check with `lipo -info`:
```bash
for f in $(find Pods -name "*.framework" -type d); do
  BIN="$f/$(basename $f .framework)"
  if [ -f "$BIN" ]; then
    echo "$f: $(lipo -archs "$BIN")"
  fi
done
```

### Homebrew Libraries
Libraries installed via Homebrew are architecture-specific by default. For `/usr/local/lib/` (x86_64) and `/opt/homebrew/lib/` (arm64), you need to build fat libraries:
```bash
# Build universal static library from source
./configure CC="clang -arch arm64 -arch x86_64"
make
lipo -create libfoo_arm64.a libfoo_x86_64.a -output libfoo.a
```

---

## Debugging Rosetta Issues

If your Universal Binary crashes on Intel but works on Apple Silicon:
```bash
# Force the app to run under Rosetta (even if native x86_64 is available)
# Useful for debugging Intel-specific bugs on Apple Silicon
arch -x86_64 /path/to/YourApp.app/Contents/MacOS/YourApp

# Check what architecture a running process is
ps -eo pid,comm,args | grep YourApp
# Then:
lipo -info /path/to/YourApp.app/Contents/MacOS/YourApp
```

---

## CI Pipeline for Universal Build Validation

```bash
#!/bin/bash
# verify-universal.sh — run in CI after archive
set -e

APP_PATH="build/YourApp.xcarchive/Products/Applications/YourApp.app"
BINARY="$APP_PATH/Contents/MacOS/YourApp"

# 1. Check main binary architectures
ARCHS=$(lipo -archs "$BINARY")
if [[ "$ARCHS" != *"arm64"* ]] || [[ "$ARCHS" != *"x86_64"* ]]; then
    echo "FAIL: Missing architecture. Found: $ARCHS"
    exit 1
fi
echo "PASS: Universal binary contains arm64 and x86_64"

# 2. Check all embedded binaries
FAILED=0
for bin in $(find "$APP_PATH" -type f | xargs file | grep 'Mach-O' | cut -d: -f1); do
    BIN_ARCHS=$(lipo -archs "$bin")
    if [[ "$BIN_ARCHS" != *"arm64"* ]] || [[ "$BIN_ARCHS" != *"x86_64"* ]]; then
        echo "WARNING: $bin has: $BIN_ARCHS"
        FAILED=$((FAILED + 1))
    fi
done

if [ $FAILED -gt 0 ]; then
    echo "WARNING: $FAILED binaries are not Universal"
    # Non-fatal — third-party frameworks may be single-arch
fi

# 3. Verify minimum deployment target consistency
APP_TARGET=$(otool -l "$BINARY" | grep -A3 LC_VERSION_MIN_MACOSX | grep version | head -1 | awk '{print $2}')
echo "Deployment target: $APP_TARGET"

echo "Universal binary validation complete."
```
