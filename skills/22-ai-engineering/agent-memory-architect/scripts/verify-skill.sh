#!/usr/bin/env bash
# Verify agent-memory-architect output artifacts.
set -euo pipefail
echo "agent-memory-architect verification"
echo "- a read path exists and is exercised (not write-only)"
echo "- injected memory carries a context-only label"
echo "- every entry has provenance: source, timestamp, workflow, run id"
echo "- consolidation counts outcomes; it does not re-summarise"
echo "- the store is bounded and eviction is scheduled"
echo "- retrieval is capped in tokens with a stated truncation rule"
