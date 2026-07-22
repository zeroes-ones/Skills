#!/usr/bin/env bash
#=============================================================================
# Skills Library — Per-Project Init (Tiered Activation)
# Author: Sandeep Kumar Penchala
#
# Run inside any project to symlink skills into that project.
# Skills are loaded from ~/.zeroes-ones/skills/ (set by install.sh).
#
# Usage:
#   skills-init                  Full 56 skills (work/team projects)
#   skills-init --solo           8 essential skills (personal/solo projects)
#   skills-init --grow           18 skills (project gaining traction)
#   skills-init --status         Show current tier and skill count
#=============================================================================
set -euo pipefail

SKILLS_HOME="${SKILLS_HOME:-$HOME/.zeroes-ones/skills}"
SKILLS_SRC="$SKILLS_HOME/skills"
TIER_FILE=".skills-tier"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ---- Tier Definitions ----
# Solo: Essential 8 skills for personal projects
SOLO_SKILLS="01-strategy/ceo-strategist 02-product/product-manager 05-development/fullstack-developer 06-quality/code-reviewer 06-quality/qa-engineer 06-quality/security-reviewer 07-devops/ci-cd-builder 11-legal/gdpr-privacy"

# Grow: Add 10 more as project gains users/collaborators (total 18)
GROW_SKILLS="$SOLO_SKILLS 01-strategy/business-strategist 02-product/ux-researcher 03-design/ui-ux-designer 03-design/accessibility-auditor 04-architecture/system-architect 04-architecture/api-designer 04-architecture/database-designer 05-development/backend-developer 07-devops/devops-engineer 08-security/security-engineer"

show_status() {
    echo -e "${BLUE}Skills status for ${CYAN}$(pwd)${NC}"
    echo ""
    local tier="inactive"
    local count=0
    if [ -d ".claude/skills" ] || [ -L ".claude/skills" ]; then
        count=$(find -L .claude/skills -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
    fi
    if [ -f "$TIER_FILE" ]; then
        tier=$(cat "$TIER_FILE")
        echo -e "  Tier:    ${GREEN}$tier${NC} ($count skills linked)"
    else
        echo -e "  Tier:    ${YELLOW}inactive${NC} (run skills-init to activate)"
    fi
    echo ""
    echo -e "  ${CYAN}solo${NC}  → 8 essential skills (personal projects)"
    echo -e "  ${CYAN}grow${NC}  → 18 skills (project gaining traction)"
    echo -e "  ${CYAN}full${NC}  → 56 skills (team/company projects)"
}

link_skill() {
    local skill_path="$1"
    local target_base="$2"
    local src="$SKILLS_SRC/$skill_path"
    local dest="$target_base/$skill_path"
    if [ -d "$src" ]; then
        mkdir -p "$(dirname "$dest")"
        ln -sfn "$src" "$dest" 2>/dev/null || true
    fi
}

activate_tier() {
    local tier="$1"
    local skill_list=""
    local count=0

    case "$tier" in
        solo)  skill_list="$SOLO_SKILLS"; count=8 ;;
        grow)  skill_list="$GROW_SKILLS"; count=18 ;;
        full)  count=56 ;;
        *)     echo -e "${YELLOW}Unknown tier: $tier${NC}"; return 1 ;;
    esac

    echo -e "${BLUE}Activating ${CYAN}$tier${BLUE} tier ($count skills) in $(pwd)...${NC}"
    echo ""

    AGENT_LIST="claude:.claude/skills copilot:.copilot/skills cursor:.cursor/skills openclaw:.openclaw/workspace/skills gemini:.gemini/skills"

    initialized=0
    for entry in $AGENT_LIST; do
        agent="${entry%%:*}"
        target="${entry#*:}"
        parent=$(dirname "$target")

        if [ -d "$parent" ] || mkdir -p "$parent" 2>/dev/null; then
            rm -rf "$target" 2>/dev/null || true

            if [ "$tier" = "full" ]; then
                ln -sfn "$SKILLS_SRC" "$target"
            else
                mkdir -p "$target"
                for skill_path in $skill_list; do
                    link_skill "$skill_path" "$target"
                done
            fi

            echo -e "  ${GREEN}✓${NC} $agent → $target"
            initialized=$((initialized + 1))

            grep -q "^$target\$" .gitignore 2>/dev/null || echo "$target" >> .gitignore
        fi
    done

    echo "$tier" > "$TIER_FILE"

    for doc in PROJECT-BOOTSTRAP.md TECH-STACK-DECISIONS.md COORDINATION-MATRIX.md; do
        if [ -f "$SKILLS_HOME/$doc" ]; then
            ln -sfn "$SKILLS_HOME/$doc" ".$doc" 2>/dev/null || true
        fi
    done

    echo ""
    if [ $initialized -gt 0 ]; then
        echo -e "${GREEN}✓ Skills activated ($tier tier, $count skills) for $initialized agent(s).${NC}"
        echo -e "  Invoke any skill:  ${BLUE}/{skill-name}${NC}"
        echo -e "  Check status:      ${BLUE}skills-init --status${NC}"
        if [ "$tier" = "solo" ]; then
            echo -e "  Ready to scale?    ${BLUE}skills-init --grow${NC}"
        elif [ "$tier" = "grow" ]; then
            echo -e "  Need everything?   ${BLUE}skills-init${NC} (full 56 skills)"
        fi
        echo -e "  Update later:      ${BLUE}skills-update${NC}"
    else
        echo -e "${YELLOW}○ No agent directories found. Create one first:${NC}"
        echo -e "  mkdir -p .claude/ && touch .claude/settings.json"
    fi
}

# ---- Main Entry ----
if [ ! -d "$SKILLS_SRC" ]; then
    echo -e "${YELLOW}Skills library not found at $SKILLS_HOME${NC}"
    echo -e "Run first: ${BLUE}curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash${NC}"
    exit 1
fi

TIER="full"
PROJECT_ARG=""
while [ $# -gt 0 ]; do
    case "$1" in
        --solo)   TIER="solo"; shift ;;
        --grow)   TIER="grow"; shift ;;
        --full)   TIER="full"; shift ;;
        --status) 
            cd "${2:-.}" 2>/dev/null || true
            show_status
            exit 0 ;;
        --help|-h)
            echo "Usage: skills-init [--solo|--grow|--full|--status] [project-path]"
            echo ""
            echo "  --solo   8 essential skills for personal projects"
            echo "  --grow   18 skills for projects gaining traction"
            echo "  --full   56 skills for team/company projects (default)"
            echo "  --status Show current tier"
            exit 0 ;;
        *) PROJECT_ARG="$1"; shift ;;
    esac
done

cd "${PROJECT_ARG:-.}" || { echo "Cannot access $PROJECT_ARG"; exit 1; }
activate_tier "$TIER"
