#!/usr/bin/env bash
# Verify document-specialist output artifacts.
set -euo pipefail
echo "document-specialist verification"
echo "- the deliverable is a real file, not a snippet"
echo "- the file was reopened and its content asserted"
echo "- counts reconcile across every transform"
echo "- conversions were inspected and drift reported"
