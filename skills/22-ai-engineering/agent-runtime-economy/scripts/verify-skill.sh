#!/usr/bin/env bash
# Verify agent-runtime-economy output artifacts.
set -euo pipefail
echo "agent-runtime-economy verification"
echo "- the ambient floor is measured, not estimated"
echo "- token, turn, and time budgets are declared with a rationale"
echo "- a measurable stop rule exists"
echo "- routing accuracy is measured against a held-out set"
echo "- every structural choice is compared to a single-call baseline"
echo "- every cost figure is paired with a success metric"
