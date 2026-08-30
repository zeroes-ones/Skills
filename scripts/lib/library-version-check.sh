#!/usr/bin/env bash
# ==============================================================================
# Library Version Freshness Check — shared, repo-wide.
# ==============================================================================
# Canonical "always use updated libraries" enforcement for every skill that emits
# library/API references. Detects the project type in the target directory and
# runs the appropriate freshness checks, then reports installed vs latest and
# flags outdated dependencies.
#
# Policy: see scripts/references/library-freshness-policy.md (the single source
# of truth for what "updated" means, pinning rules, upgrade cadence, exceptions).
#
# Usage:
#   bash scripts/lib/library-version-check.sh [project-root] [--strict]
#     --strict  exit 1 if ANY outdated dependency is found (default: report only)
#
# Exit codes:
#   0 = project fresh (or no outdated deps found)
#   1 = outdated dependencies found (with --strict)
#   2 = project type not detected / cannot determine freshness
#
# Supported project types:
#   react-native / expo  -> package.json (+ expo) -> npx expo install --check, npm outdated
#   flutter              -> pubspec.yaml         -> flutter pub outdated
#   kmp / android-gradle -> settings.gradle.kts   -> gradle version catalog + dependency check
#   generic node         -> package.json          -> npm outdated
#
# Bash 3.2 compatible (macOS default) — no associative arrays, no bashisms.
# ==============================================================================
set -u

ROOT="${1:-$(pwd)}"
STRICT=false
for a in "$@"; do [ "$a" = "--strict" ] && STRICT=true; done

OUTDATED=0
UNKNOWN=0

note()  { echo "  [${1}] $2"; }
fresh() { echo "  [OK] $1"; }
flag()  { echo "  [OUTDATED] $1"; OUTDATED=$((OUTDATED + 1)); }
warn()  { echo "  [WARN] $1"; }

echo "=== Library Version Freshness Check ==="
echo "  project:  $ROOT"
echo "  policy:   scripts/references/library-freshness-policy.md"
echo ""

if [ ! -d "$ROOT" ]; then
    echo "  ERROR: no such directory: $ROOT" >&2
    exit 2
fi

# ── Detect project type ──────────────────────────────────────────────────────
TYPE=""
PKG="$ROOT/package.json"
PUBSPEC="$ROOT/pubspec.yaml"
SETTINGS="$ROOT/settings.gradle.kts"

if [ -f "$PKG" ]; then
    if grep -q '"react-native"\|"expo"' "$PKG" 2>/dev/null; then
        TYPE="react-native"
    else
        TYPE="node"
    fi
elif [ -f "$PUBSPEC" ] && grep -q "^flutter" "$PUBSPEC" 2>/dev/null; then
    TYPE="flutter"
elif [ -f "$SETTINGS" ] && grep -qi "kotlinMultiplatform\|multiplatform" "$SETTINGS" 2>/dev/null; then
    TYPE="kmp"
elif [ -f "$ROOT/build.gradle.kts" ] || [ -f "$ROOT/android/build.gradle.kts" ]; then
    TYPE="gradle"
fi

case "$TYPE" in
    react-native)
        echo "  type: React Native / Expo"
        echo ""
        # ── Expo SDK alignment ──
        if command -v npx >/dev/null 2>&1; then
            echo "  [1] npx expo install --check (Expo SDK alignment)"
            if (cd "$ROOT" && npx expo install --check 2>&1) | tee /tmp/lvc-expo.$$ | grep -qiE "expected|mismatch|outdated|update"; then
                flag "Expo SDK dependency drift detected — run 'npx expo install --fix' after review"
            else
                fresh "Expo dependencies aligned with the installed SDK"
            fi
        else
            warn "npx not available — cannot run 'expo install --check'"
        fi
        echo ""
        # ── npm outdated ──
        if command -v npm >/dev/null 2>&1; then
            echo "  [2] npm outdated (installed vs latest)"
            if (cd "$ROOT" && npm outdated 2>/dev/null) | tee /tmp/lvc-npm.$$ | grep -qE "Package|^[a-z@]"; then
                flag "npm dependencies behind latest — review and upgrade per policy"
            else
                fresh "npm dependencies current (or none outdated)"
            fi
        else
            warn "npm not available — cannot run 'npm outdated'"
        fi
        ;;
    node)
        echo "  type: Node.js (generic)"
        echo ""
        if command -v npm >/dev/null 2>&1; then
            echo "  [1] npm outdated (installed vs latest)"
            if (cd "$ROOT" && npm outdated 2>/dev/null) | tee /tmp/lvc-npm.$$ | grep -qE "Package|^[a-z@]"; then
                flag "npm dependencies behind latest — review and upgrade per policy"
            else
                fresh "npm dependencies current (or none outdated)"
            fi
        else
            warn "npm not available — cannot run 'npm outdated'"
        fi
        ;;
    flutter)
        echo "  type: Flutter / Dart"
        echo ""
        if command -v flutter >/dev/null 2>&1; then
            echo "  [1] flutter --version (SDK anchor)"
            (cd "$ROOT" && flutter --version 2>/dev/null | head -3) || warn "flutter --version failed"
            echo ""
            echo "  [2] flutter pub outdated (installed vs latest)"
            if (cd "$ROOT" && flutter pub outdated 2>&1) | tee /tmp/lvc-fp.$$ | grep -qE "PackageName|^[a-z_]"; then
                flag "pub dependencies behind latest — review and upgrade per policy"
            else
                fresh "pub dependencies current (or none outdated)"
            fi
        else
            warn "flutter not on PATH — cannot run 'flutter pub outdated'"
        fi
        ;;
    kmp|gradle)
        echo "  type: Kotlin Multiplatform / Gradle"
        echo ""
        echo "  [1] Version catalog (gradle/libs.versions.toml)"
        if [ -f "$ROOT/gradle/libs.versions.toml" ]; then
            grep -E "^[a-zA-Z]" "$ROOT/gradle/libs.versions.toml" | head -25 || true
            echo ""
            warn "Gradle/Kotlin freshness requires a network-backed resolver (e.g., Gradle Versions Plugin, renovate)."
            warn "Manually verify kotlinx/library versions against their release pages before upgrading."
        else
            warn "No version catalog found — check build.gradle.kts dependency declarations manually."
        fi
        ;;
    *)
        echo "  type: not detected"
        echo ""
        echo "  No supported project manifest found (package.json, pubspec.yaml, settings.gradle.kts)."
        echo "  Freshness cannot be determined — review dependencies manually per the policy."
        UNKNOWN=1
        ;;
esac

echo ""
echo "=== Summary ==="
if [ "$UNKNOWN" -eq 1 ]; then
    echo "  RESULT: UNKNOWN — project type not detected (exit 2)"
    exit 2
fi
if [ "$OUTDATED" -gt 0 ]; then
    echo "  RESULT: $OUTDATED outdated dependency group(s) found"
    if $STRICT; then
        echo "  → BLOCKING: fix per scripts/references/library-freshness-policy.md before emitting code"
        exit 1
    fi
    echo "  → ADVISORY: review and upgrade per the policy before shipping library references"
    exit 0
fi
echo "  RESULT: FRESH — dependencies are current"
exit 0
