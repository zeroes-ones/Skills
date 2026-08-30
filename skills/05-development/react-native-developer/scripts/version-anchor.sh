#!/usr/bin/env bash
# RN/Expo version anchor — print the installed version matrix for the current app.
# Run from a React Native / Expo project root (or pass a path):
#   bash scripts/version-anchor.sh [project-root]
# Ground Rule R1: anchor to installed versions before writing any RN code.
set -euo pipefail

ROOT="${1:-$(pwd)}"
PKG="$ROOT/package.json"

if [ ! -f "$PKG" ]; then
    echo "  ERROR: no package.json at $ROOT" >&2
    exit 2
fi

echo "=== RN/Expo Version Anchor ==="
echo "  project:  $ROOT"
if command -v node >/dev/null 2>&1 && [ -d "$ROOT/node_modules" ]; then
    for pkg in react-native expo react-native-reanimated react-native-gesture-handler react-native-screens @react-navigation/native; do
        v=$(node -p "try{require('$ROOT/node_modules/$pkg/package.json').version}catch(e){''}" 2>/dev/null || true)
        [ -n "$v" ] && echo "  $pkg: $v"
    done
else
    echo "  (node_modules not present — falling back to package.json ranges)"
    node -p "" 2>/dev/null || true
    grep -E '"(react-native|expo|react-native-reanimated|react-native-gesture-handler|react-native-screens)"' "$PKG" || true
fi

# New Architecture state
if [ -f "$ROOT/app.json" ]; then
    na=$(grep -o '"newArchEnabled"[^,]*' "$ROOT/app.json" || true)
    echo "  newArchEnabled: ${na:-not-set}"
fi
if [ -f "$ROOT/android/gradle.properties" ]; then
    na=$(grep -o 'newArchEnabled=.*' "$ROOT/android/gradle.properties" || true)
    echo "  gradle newArchEnabled: ${na:-not-set}"
fi

echo ""
echo "  Next: run 'npx expo install --check' (Expo) or 'npx react-native config' (bare) to verify drift,"
echo "  and the shared freshness check per the Library Freshness Policy:"
echo "    bash scripts/lib/library-version-check.sh . --strict"

# Shared freshness check (always-use-updated-libraries enforcement)
if [ -f "$(cd "$(dirname "$0")/../../.." && pwd)/scripts/lib/library-version-check.sh" ]; then
    echo ""
    bash "$(cd "$(dirname "$0")/../../.." && pwd)/scripts/lib/library-version-check.sh" "$ROOT" || true
fi
