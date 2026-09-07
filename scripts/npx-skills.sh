#!/usr/bin/env bash
#=============================================================================
# npx @zeroes-ones/skills — dispatcher entry point
#
# npm runs the bin whose name matches the package short name, so this script
# makes the documented `npx @zeroes-ones/skills init` command resolve. Each
# subcommand delegates to the same canonical script exposed as the individual
# skills-* bins (single source of truth).
#
#   init      activate skills in the current project (all 297 by default,
#             or --solo / --grow subsets) — bootstraps ~/.zeroes-ones/skills
#             on first use if the shell installer was never run
#   update    install or update the ~/.zeroes-ones/skills library + global
#             agent symlinks + convenience commands (same as scripts/install.sh)
#   validate  run the skills governance validator (dev tool)
#   lint      run the markdown linter (dev tool)
#=============================================================================
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cmd="${1:-}"
if [ $# -gt 0 ]; then shift; fi

case "$cmd" in
    init)      exec "$DIR/init-project.sh" "$@" ;;
    update)    exec "$DIR/install.sh" "$@" ;;
    validate)  exec "$DIR/validate-skills.sh" "$@" ;;
    lint)      exec "$DIR/lint.sh" "$@" ;;
    ""|--help|-h)
        echo "Usage: npx @zeroes-ones/skills <command> [args]"
        echo ""
        echo "  init       activate skills in the current project (all 297, or --solo/--grow)"
        echo "  update     install/update the ~/.zeroes-ones/skills library + global agent symlinks"
        echo "  validate   run the skills governance validator (dev tool)"
        echo "  lint       run the markdown linter (dev tool)"
        exit 0 ;;
    *)
        echo "Unknown command: $cmd (try: init | update | validate | lint)" >&2
        exit 2 ;;
esac
