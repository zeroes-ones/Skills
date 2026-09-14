#!/usr/bin/env bash
# Verify implementation-planner output artifacts.
set -euo pipefail
echo "implementation-planner verification"
echo "- every task has acceptance criteria + a verification step"
echo "- every dependency is an explicit blocked_by edge"
echo "- the DAG is acyclic and the unblocked set is non-empty"
echo "- the critical path is stated"
echo "- every parallel wave records its collision surface"
