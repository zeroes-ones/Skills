#!/usr/bin/env bash
#=============================================================================
# Skills Library — Per-Project Init (Dual-Mode Activation)
# Author: Sandeep Kumar Penchala
#
# Run inside any project to symlink skills into that project. Two modes:
#   * default (no flag) — all 298 skills from the flat layer (~/.zeroes-ones/
#     skills/skills-flat), one level deep so every agent discovers them
#   * tiered — --solo (8 essential) / --grow (18) subsets, by skill name
# Usage: skills-init [--solo|--grow|--full|--status] [project-path]
#=============================================================================
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/zeroes-ones/Skills.git}"
DEFAULT_STORE="$HOME/.zeroes-ones/skills"
SKILLS_HOME="${SKILLS_HOME:-}"
SKILLS_SRC=""                 # nested skills/<domain>/<name> store (for counts/fallback)
FLAT_SRC=""                   # flat <name>/SKILL.md discovery layer (what agents link to)
TIER_FILE=".skills-tier"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ---- Tier Definitions (flat names — see skills-flat/) ----
# Solo: Essential 8 skills for personal projects
SOLO_SKILLS="ceo-strategist product-manager fullstack-developer code-reviewer qa-engineer security-reviewer ci-cd-builder gdpr-privacy"

# Grow: Add 10 more as project gains users/collaborators (total 18)
GROW_SKILLS="$SOLO_SKILLS business-strategist ux-researcher ui-ux-designer accessibility-auditor system-architect api-designer database-designer backend-developer devops-engineer security-engineer"

# Format: agent_name:target_dir — project scope uses the same flat discovery
# layer and agent set as scripts/install.sh (global install).
AGENT_LIST="agents:.agents/skills claude:.claude/skills copilot:.copilot/skills github:.github/skills cursor:.cursor/skills codex:.codex/skills gemini:.gemini/skills windsurf:.windsurf/skills cline:.cline/skills opencode:.opencode/skills"

FULL_COUNT=298

tier_info() {
    case "$1" in
        solo) echo "solo|8|$SOLO_SKILLS" ;;
        grow) echo "grow|18|$GROW_SKILLS" ;;
        *)    echo "full|$FULL_COUNT|" ;;
    esac
}

bootstrap_store() {
    # Auto-bootstrap the canonical store when SKILLS_HOME is unset and the
    # default location is missing (standalone `npx @zeroes-ones/skills init`).
    if [ -n "$SKILLS_HOME" ]; then
        echo -e "${YELLOW}Skills library not found at $SKILLS_HOME${NC}" >&2
        echo -e "Run first: ${BLUE}curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash${NC}" >&2
        exit 1
    fi
    echo -e "${YELLOW}Skills store not found at $DEFAULT_STORE — cloning once (first run only)...${NC}"
    command -v git >/dev/null 2>&1 || {
        echo -e "${YELLOW}git not found. Install git or run the installer:${NC}" >&2
        echo -e "  ${BLUE}curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash${NC}" >&2
        exit 1
    }
    mkdir -p "$(dirname "$DEFAULT_STORE")"
    git clone --depth 1 "$REPO_URL" "$DEFAULT_STORE"
    SKILLS_HOME="$DEFAULT_STORE"
}

resolve_store() {
    if [ -n "$SKILLS_HOME" ]; then
        if [ ! -d "$SKILLS_HOME" ]; then
            bootstrap_store   # errors out (explicit SKILLS_HOME respected)
            return
        fi
    elif [ -d "$DEFAULT_STORE" ]; then
        SKILLS_HOME="$DEFAULT_STORE"
    else
        bootstrap_store
    fi
    SKILLS_SRC="$SKILLS_HOME/skills"
    FLAT_SRC="$SKILLS_HOME/skills-flat"
    if [ ! -d "$FLAT_SRC" ]; then
        echo -e "${YELLOW}Flat discovery layer missing at $FLAT_SRC${NC}" >&2
        echo -e "Your store predates the flat layer — refresh it:  ${BLUE}skills-update${NC}" >&2
        exit 1
    fi
}

show_status() {
    local tier="inactive"
    local count=0
    local target=""
    if [ -f "$TIER_FILE" ]; then
        tier=$(cat "$TIER_FILE")
    fi
    # Count SKILL.md reachable through the first configured agent dir present
    for entry in $AGENT_LIST; do
        target="${entry#*:}"
        if [ -L "$target" ] || [ -d "$target" ]; then
            count=$(find -L "$target" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
            break
        fi
    done
    echo -e "${BLUE}Skills status for ${CYAN}$(pwd)${NC}"
    echo ""
    if [ "$tier" = "inactive" ]; then
        echo -e "  Tier:    ${YELLOW}inactive${NC} (run skills-init to activate)"
    else
        echo -e "  Tier:    ${GREEN}$tier${NC} ($count skills linked)"
    fi
    echo ""
    echo -e "  ${CYAN}default/full${NC} → all 298 skills (team/company projects)"
    echo -e "  ${CYAN}grow${NC}         → 18 skills (project gaining traction)"
    echo -e "  ${CYAN}solo${NC}         → 8 essential skills (personal projects)"
    echo -e "  Run: ${BLUE}skills-init [--solo|--grow|--full]${NC} to switch tiers"
}

reset_target() {
    # Remove links THIS script created in a previous activation (mode switch),
    # so switching full -> solo/grow (or between tiers) actually replaces them.
    # Never touches user content: symlinks under our store are removed; real
    # files and foreign links are left alone.
    local target="$1" child real
    [ -n "$FLAT_SRC" ] || return 0   # safety: never glob-delete without a known store
    if [ -L "$target" ]; then
        rm -f "$target"
    elif [ -d "$target" ]; then
        for child in "$target"/*; do
            [ -L "$child" ] || continue
            real=$(readlink "$child")
            case "$real" in
                "$FLAT_SRC"*|"$SKILLS_SRC"*) rm -f "$child" ;;
            esac
        done
        rmdir "$target" 2>/dev/null || true
    fi
}

link_agent() {
    local agent="$1" target="$2" mode="$3" list="$4"
    local parent
    parent=$(dirname "$target")

    if [ "$FORCE_RESET" = "1" ]; then
        reset_target "$target"
    fi
    if [ -L "$target" ]; then
        echo -e "  ${GREEN}✓${NC} $agent already linked"
        return 0
    fi
    if [ -e "$target" ] && [ -n "$(ls -A "$target" 2>/dev/null)" ]; then
        echo -e "  ${YELLOW}○${NC} $agent dir exists with content (keep user skills, skip)"
        return 0
    fi
    if [ ! -d "$parent" ] && ! mkdir -p "$parent" 2>/dev/null; then
        echo -e "  ${YELLOW}○${NC} $agent not linked (cannot create $parent)"
        return 0
    fi

    rm -rf "$target" 2>/dev/null || true
    if [ "$mode" = "full" ]; then
        # One symlink to the flat layer — all skills, one level deep.
        ln -sfn "$FLAT_SRC" "$target"
    else
        # Tier subset: link individual flat skill dirs by name.
        mkdir -p "$target"
        local missing=0
        for name in $list; do
            if [ -d "$FLAT_SRC/$name" ]; then
                ln -sfn "$FLAT_SRC/$name" "$target/$name"
            else
                echo -e "  ${YELLOW}⚠${NC} unknown skill '$name' (not in $FLAT_SRC)" >&2
                missing=$((missing + 1))
            fi
        done
        [ "$missing" -gt 0 ] && return 1
    fi
    echo -e "  ${GREEN}✓${NC} $agent → $target"
    grep -q "^$target\$" .gitignore 2>/dev/null || echo "$target" >> .gitignore
    return 0
}

activate() {
    local mode="$1" list="$2" count="$3" linked=0 skipped=0 failed=0
    local label prev_tier=""
    if [ "$mode" = "full" ]; then
        label="all $count skills"
    else
        label="$mode tier ($count skills)"
    fi
    FORCE_RESET=0
    if [ -f "$TIER_FILE" ]; then
        prev_tier=$(cat "$TIER_FILE")
        # Mode change (full <-> solo/grow or solo <-> grow) replaces our links.
        if [ -n "$prev_tier" ] && [ "$prev_tier" != "$mode" ]; then
            FORCE_RESET=1
        fi
    fi
    echo -e "${BLUE}Activating ${CYAN}$label${BLUE} in $(pwd)...${NC}"
    echo ""

    for entry in $AGENT_LIST; do
        agent="${entry%%:*}"
        target="${entry#*:}"
        if link_agent "$agent" "$target" "$mode" "$list"; then
            linked=$((linked + 1))
        else
            skipped=$((skipped + 1))
        fi
    done

    echo "$mode" > "$TIER_FILE"

    # Project bootstrap pointer
    ln -sfn "$SKILLS_HOME/PROJECT-BOOTSTRAP.md" .skills-bootstrap.md 2>/dev/null || true

    echo ""
    if [ "$linked" -gt 0 ]; then
        echo -e "${GREEN}✓ Skills activated ($label) for $linked agent(s).${NC}"
        echo -e "  Invoke any skill:  ${BLUE}/{skill-name}${NC}"
        echo -e "  Check status:      ${BLUE}skills-init --status${NC}"
        if [ "$mode" = "solo" ]; then
            echo -e "  Ready to scale?    ${BLUE}skills-init --grow${NC}"
        elif [ "$mode" = "grow" ]; then
            echo -e "  Need everything?   ${BLUE}skills-init${NC} (all 298 skills)"
        fi
        echo -e "  Update later:      ${BLUE}skills-update${NC}"
    else
        echo -e "${YELLOW}○ No agent directory could be linked.${NC}"
    fi
    [ "$failed" -gt 0 ] && return 1
    return 0
}

install_principles() {
    # Opt-in (--principles): append the always-on operating principles
    # (hooks/always-on-principles.md) to the project's CLAUDE.md/AGENTS.md so
    # every session carries the rules even when the agent has no hook support.
    [ "$WRITE_PRINCIPLES" = "1" ] || return 0
    local src="$SKILLS_HOME/hooks/always-on-principles.md"
    if [ ! -f "$src" ]; then
        echo -e "  ${YELLOW}⚠${NC} principles file not found at $src (run skills-update)" >&2
        return 1
    fi
    local target=""
    for cand in CLAUDE.md AGENTS.md; do
        if [ -f "$cand" ]; then target="$cand"; break; fi
    done
    [ -n "$target" ] || target="CLAUDE.md"
    if grep -q "zeroes-ones operating principles" "$target" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Operating principles already present in $target (idempotent)"
        return 0
    fi
    {
        echo ""
        echo "<!-- BEGIN zeroes-ones operating principles -->"
        cat "$src"
        echo "<!-- END zeroes-ones operating principles -->"
    } >> "$target"
    echo -e "  ${GREEN}✓${NC} Operating principles appended to $target (always-on, ~280 tokens)"
    return 0
}

# ---- Main Entry ----
MODE="full"
PROJECT_ARG=""
WRITE_PRINCIPLES=0
while [ $# -gt 0 ]; do
    case "$1" in
        --solo)   MODE="solo"; shift ;;
        --grow)   MODE="grow"; shift ;;
        --full)   MODE="full"; shift ;;
        --principles) WRITE_PRINCIPLES=1; shift ;;
        --status)
            cd "${2:-.}" 2>/dev/null || true
            show_status
            exit 0 ;;
        --help|-h)
            echo "Usage: skills-init [--solo|--grow|--full|--principles|--status] [project-path]"
            echo ""
            echo "  (no flag)     all 298 skills — team/company projects (default)"
            echo "  --full        all 298 skills (explicit)"
            echo "  --grow        18 skills for projects gaining traction"
            echo "  --solo        8 essential skills for personal projects"
            echo "  --principles  append always-on operating principles to CLAUDE.md/AGENTS.md"
            echo "  --status      show current activation tier + skill count"
            exit 0 ;;
        *) PROJECT_ARG="$1"; shift ;;
    esac
done

resolve_store
cd "${PROJECT_ARG:-.}" || { echo -e "${YELLOW}Cannot access '$PROJECT_ARG'${NC}" >&2; exit 1; }

IFS='|' read -r MODE COUNT LIST <<< "$(tier_info "$MODE")"
activate "$MODE" "$LIST" "$COUNT"
install_principles
