#!/usr/bin/env bash
# KMP version anchor — print the installed Kotlin/Gradle toolchain for the current project.
# Run from a KMP project root (or pass a path):
#   bash scripts/version-anchor.sh [project-root]
# Ground Rule R1: anchor to installed versions before writing any KMP code.
set -euo pipefail

ROOT="${1:-$(pwd)}"

echo "=== KMP Version Anchor ==="
echo "  project:  $ROOT"

if [ -f "$ROOT/gradlew" ]; then
    (cd "$ROOT" && ./gradlew --version 2>/dev/null | grep -E "Gradle|Kotlin|JVM:" | head -5) || echo "  WARNING: gradlew failed — check the wrapper" >&2
else
    echo "  WARNING: no gradlew at $ROOT" >&2
fi

if [ -f "$ROOT/gradle/libs.versions.toml" ]; then
    echo ""
    echo "  version catalog (gradle/libs.versions.toml):"
    grep -E "^[a-z]|kotlin|compose|ktor|sqldelight|coroutines|serialization" "$ROOT/gradle/libs.versions.toml" | head -30 || true
fi

echo ""
echo "  Next: check Kotlin/Native <-> Xcode compatibility before any iOS work; run the full CI matrix after upgrades."
