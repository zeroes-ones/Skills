#!/usr/bin/env bash
# Simplify-Ignore Hook — Protects code blocks from accidental modification during code simplification.
# Blocks are demarcated with:
#   // simplify-ignore-start → content protected → // simplify-ignore-end
# This PreToolUse Read hook replaces block contents with BLOCK_<hash> placeholders.
set -euo pipefail

INPUT=$(cat)

# Replace simplify-ignore blocks with hashed placeholders
# This prevents the agent from reading (and thus modifying) protected blocks
awk '
/simplify-ignore-start/ { in_block=1; block_num++; print "// BLOCK_" block_num "_PROTECTED"; next }
/simplify-ignore-end/   { in_block=0; next }
!in_block               { print }
' <<< "$INPUT"
