#!/usr/bin/env bash
#=============================================================================
# Skills Library — Per-Project Init
# Author: Sandeep Kumar Penchala
#
# Run inside any project to symlink all 56 skills into that project.
# Skills are loaded from ~/.zeroes-ones/skills/ (set by install.sh).
#
# Usage: ./scripts/init-project.sh [project-path]
#    or: skills-init [project-path]  (after global install)
#=============================================================================
set -euo pipefail

SKILLS_HOME="${SKILLS_HOME:-$HOME/.zeroes-ones/skills}"
PROJECT="${1:-.}"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

if [ ! -d "$SKILLS_HOME/skills" ]; then
    echo -e "${YELLOW}Skills library not found at $SKILLS_HOME${NC}"
    echo -e "Run first: ${BLUE}curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash${NC}"
    exit 1
fi

cd "$PROJECT" || { echo "Cannot access $PROJECT"; exit 1; }
echo -e "${BLUE}Activating 56 skills in $(pwd)...${NC}"
echo ""

# Agent-specific skill directories
# Format: agent_name:target_dir (colon-separated)
AGENT_LIST="claude:.claude/skills copilot:.copilot/skills cursor:.cursor/skills openclaw:.openclaw/workspace/skills gemini:.gemini/skills"

initialized=0
for entry in $AGENT_LIST; do
    agent="${entry%%:*}"
    target="${entry#*:}"
    parent=$(dirname "$target")

    # Try to create parent dir (means agent is used in this project)
    if [ -d "$parent" ] || mkdir -p "$parent" 2>/dev/null; then
        rm -rf "$target" 2>/dev/null || true
        ln -sf "$SKILLS_HOME/skills" "$target"
        echo -e "  ${GREEN}✓${NC} $agent → $target"
        initialized=$((initialized + 1))

        # Add to .gitignore
        if [ -f .gitignore ]; then
            grep -q "^$target\$" .gitignore 2>/dev/null || echo "$target" >> .gitignore
        else
            echo "$target" > .gitignore
        fi
    fi
done

# Also symlink key docs
for doc in PROJECT-BOOTSTRAP.md TECH-STACK-DECISIONS.md COORDINATION-MATRIX.md; do
    if [ -f "$SKILLS_HOME/$doc" ]; then
        ln -sf "$SKILLS_HOME/$doc" ".$doc" 2>/dev/null || true
        echo -e "  ${GREEN}✓${NC} doc → .$doc"
    fi
done

echo ""
if [ $initialized -gt 0 ]; then
    echo -e "${GREEN}✓ Skills activated for $initialized agent(s).${NC}"
    echo -e "  Invoke any skill: ${BLUE}/{skill-name}${NC}"
    echo -e "  Lifecycle guide: ${BLUE}less .PROJECT-BOOTSTRAP.md${NC}"
    echo -e "  Update later:    ${BLUE}skills-update${NC}"
else
    echo -e "${YELLOW}○ No agent directories found. Create one first:${NC}"
    echo -e "  mkdir -p .claude/ && touch .claude/settings.json"
    echo -e "  Then run this script again."
fi
