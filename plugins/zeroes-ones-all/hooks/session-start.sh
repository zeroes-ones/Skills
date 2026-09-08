#!/usr/bin/env bash
# SessionStart hook (Claude Code plugin) — injects the always-on operating
# principles into every session. Claude Code delivers stdout as a system
# message at session start. Content is the plugin-local copy of
# hooks/always-on-principles.md (kept in sync with the repo root source).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cat "$SCRIPT_DIR/always-on-principles.md"
