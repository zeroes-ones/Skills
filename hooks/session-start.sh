#!/usr/bin/env bash
# Session Start Hook — injects the always-on operating principles into every session.
# Claude Code delivers stdout as a system message to the agent at session start.
# Content lives in hooks/always-on-principles.md (single source of truth).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cat "$SCRIPT_DIR/always-on-principles.md"
