#!/usr/bin/env bash
# Verify fintech-ui-designer output artifacts.
set -euo pipefail
echo "fintech-ui-designer verification"
echo "- every value carries its unit/label and a timestamp where live"
echo "- no state is encoded by colour alone"
echo "- destructive actions require explicit confirmation"
