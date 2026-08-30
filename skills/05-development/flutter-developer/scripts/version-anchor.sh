#!/usr/bin/env bash
# Flutter/Dart version anchor — print the installed SDK + package drift for the current app.
# Run from a Flutter project root (or pass a path):
#   bash scripts/version-anchor.sh [project-root]
# Ground Rule R1: anchor to installed versions before writing any Flutter code.
set -euo pipefail

ROOT="${1:-$(pwd)}"
PUBSPEC="$ROOT/pubspec.yaml"

echo "=== Flutter/Dart Version Anchor ==="
echo "  project:  $ROOT"

if command -v flutter >/dev/null 2>&1; then
    flutter --version 2>/dev/null | head -3
else
    echo "  WARNING: flutter not on PATH — install the SDK or pass a project with it available" >&2
fi

if [ -f "$PUBSPEC" ]; then
    echo ""
    echo "  sdk / flutter constraints in pubspec:"
    grep -A2 "^environment:" "$PUBSPEC" || true
    echo ""
    echo "  top-level dependencies:"
    sed -n '/^dependencies:/,/^dev_dependencies:/p' "$PUBSPEC" | grep -E "^  [a-z_0-9]+:" | head -25 || true
fi

echo ""
echo "  Next: run 'flutter pub outdated' to surface drift and 'flutter analyze' as the static gate."
echo "  Then the shared freshness check per the Library Freshness Policy:"
echo "    bash scripts/lib/library-version-check.sh . --strict"

# Shared freshness check (always-use-updated-libraries enforcement)
if [ -f "$(cd "$(dirname "$0")/../../.." && pwd)/scripts/lib/library-version-check.sh" ]; then
    echo ""
    bash "$(cd "$(dirname "$0")/../../.." && pwd)/scripts/lib/library-version-check.sh" "$ROOT" || true
fi
