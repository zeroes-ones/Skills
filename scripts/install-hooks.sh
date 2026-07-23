#!/usr/bin/env bash
# Install git hooks for this repository.
# Run once: bash scripts/install-hooks.sh
# Hooks validate skills on commit (fast) and push (full suite).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Installing git hooks for Skills repository..."

git config core.hooksPath .githooks

# Make hooks executable
chmod +x "$REPO_ROOT/.githooks/pre-commit"
chmod +x "$REPO_ROOT/.githooks/pre-push"

echo "✅ Git hooks installed:"
echo "   pre-commit: Fast frontmatter + link checks on changed SKILL.md files"
echo "   pre-push:   Full validate-skills.sh governance gate"
echo ""
echo "To uninstall: git config --unset core.hooksPath"
