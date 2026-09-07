#!/usr/bin/env bash
# build-flat-index.sh — generate a flat, agent-discoverable view of every skill.
#
# Agent skill scanners expect <skills-dir>/<name>/SKILL.md at exactly one level of
# nesting. The library stores skills two levels deep (skills/<domain>/<name>/), which
# hides all 297 skills from native discovery. This script materialises
#   skills-flat/<name> -> ../skills/<domain>/<name>
# (symlinked whole skill dirs, so references/ scripts/ examples/ resolve unchanged),
# keeping the canonical store nested and the discovery view flat.
#
# Usage: scripts/build-flat-index.sh
set -euo pipefail
cd "$(dirname "$0")/.."

ROOT="$(pwd)"
FLAT="$ROOT/skills-flat"

# Fresh rebuild each run (idempotent).
rm -rf "$FLAT"
mkdir -p "$FLAT"

count=0
for skill_dir in "$ROOT"/skills/*/*/; do
    [ -f "$skill_dir/SKILL.md" ] || continue
    name="$(basename "$skill_dir")"
    rel="$(python3 - "$ROOT" "$skill_dir" <<'PY'
import os, sys
root, d = sys.argv[1], sys.argv[2].rstrip('/')
print(os.path.relpath(d, start=os.path.join(root, "skills-flat")))
PY
)"
    ln -s "$rel" "$FLAT/$name"
    count=$((count + 1))
done

echo "skills-flat: $count skills linked"
[ "$count" -gt 0 ]
