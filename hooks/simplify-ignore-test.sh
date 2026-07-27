#!/usr/bin/env bash
# Test for simplify-ignore hook.
set -euo pipefail

TEST_INPUT='
func keep_this() { return 1; }
// simplify-ignore-start
func dont_touch_this() { return secret; }
// simplify-ignore-end
func also_keep() { return 2; }
'

RESULT=$(echo "$TEST_INPUT" | bash hooks/simplify-ignore.sh)

# Verify protected block is replaced with placeholder
if echo "$RESULT" | grep -q "dont_touch_this"; then
  echo "FAIL: simplify-ignore.sh did not protect the block"
  exit 1
fi

# Verify non-protected code is preserved
if ! echo "$RESULT" | grep -q "keep_this"; then
  echo "FAIL: simplify-ignore.sh removed non-protected code"
  exit 1
fi

if ! echo "$RESULT" | grep -q "also_keep"; then
  echo "FAIL: simplify-ignore.sh removed non-protected code"
  exit 1
fi

# Verify placeholder exists
if ! echo "$RESULT" | grep -q "BLOCK_.*_PROTECTED"; then
  echo "FAIL: simplify-ignore.sh did not insert placeholder"
  exit 1
fi

echo "PASS: simplify-ignore.sh correctly protects marked blocks"
