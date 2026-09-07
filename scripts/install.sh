#!/usr/bin/env bash
#=============================================================================
# Skills Library — Global Install
# Author: Sandeep Kumar Penchala
#
# One-time setup. Clones the skills library to a canonical location and
# creates global symlinks so every project can access all 298 skills.
#
# Usage: curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash
#    or: ./scripts/install.sh
#=============================================================================
set -euo pipefail

SKILLS_HOME="${SKILLS_HOME:-$HOME/.zeroes-ones/skills}"
REPO_URL="${REPO_URL:-https://github.com/zeroes-ones/Skills.git}"
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Zeroes & Ones — Skills Library Global Installer${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Step 1: Clone or update the repository
if [ -d "$SKILLS_HOME" ]; then
    echo -e "${YELLOW}[1/4]${NC} Updating existing skills library..."
    cd "$SKILLS_HOME"
    git pull --ff-only origin main 2>/dev/null || git pull origin main
else
    echo -e "${YELLOW}[1/4]${NC} Cloning skills library to ${SKILLS_HOME}..."
    mkdir -p "$(dirname "$SKILLS_HOME")"
    git clone --depth 1 "$REPO_URL" "$SKILLS_HOME"
fi
echo -e "      ${GREEN}✓${NC} Skills library at ${SKILLS_HOME}"

# Step 2: Set up global agent symlinks
echo -e "${YELLOW}[2/4]${NC} Creating global agent symlinks..."

# Format: agent_name:target_dir (colon-separated).
# `skills-flat` is linked (one-level <name>/SKILL.md discovery view of all 298 skills),
# never the nested skills/<domain>/<name> store — native scanners only look one level deep.
AGENT_LIST="agents:$HOME/.agents/skills claude:$HOME/.claude/skills copilot:$HOME/.copilot/skills github:$HOME/.github/skills cursor:$HOME/.cursor/skills codex:$HOME/.codex/skills gemini:$HOME/.gemini/skills windsurf:$HOME/.windsurf/skills cline:$HOME/.cline/skills opencode:$HOME/.opencode/skills"

agents_configured=""
for entry in $AGENT_LIST; do
    agent="${entry%%:*}"
    target="${entry#*:}"
    if [ -L "$target" ]; then
        echo -e "      ${GREEN}✓${NC} $agent already linked"
        agents_configured="$agents_configured $agent"
    elif [ -e "$target" ] && [ -n "$(ls -A "$target" 2>/dev/null)" ]; then
        echo -e "      ${YELLOW}○${NC} $agent dir exists with content (keep user skills, skip)"
    elif [ -d "$(dirname "$target")" ] || mkdir -p "$(dirname "$target")" 2>/dev/null; then
        rm -rf "$target" 2>/dev/null || true
        ln -sf "$SKILLS_HOME/skills-flat" "$target"
        echo -e "      ${GREEN}✓${NC} $agent → $target"
        agents_configured="$agents_configured $agent"
    else
        echo -e "      ${YELLOW}○${NC} $agent not installed (skip)"
    fi
done

# Step 3: Create convenience commands
echo -e "${YELLOW}[3/4]${NC} Creating convenience commands..."

mkdir -p "$HOME/.local/bin"

# skills-init — per-project activation. Installed from the repo's canonical
# scripts/init-project.sh (single source of truth; also the `skills-init` npm
# bin). Dual-mode: all 298 skills by default, or --solo/--grow subsets.
install -m 755 "$SKILLS_HOME/scripts/init-project.sh" "$HOME/.local/bin/skills-init"
echo -e "      ${GREEN}✓${NC} skills-init → $HOME/.local/bin/skills-init (default: all 298; --solo/--grow subsets)"

# skills-update — pull latest library, then refresh the commands so fixes to
# scripts/init-project.sh propagate to already-installed machines.
cat > "$HOME/.local/bin/skills-update" << 'UPDATESCRIPT'
#!/usr/bin/env bash
SKILLS_HOME="${SKILLS_HOME:-$HOME/.zeroes-ones/skills}"
cd "$SKILLS_HOME" || { echo "Skills library not found at $SKILLS_HOME"; exit 1; }
echo "Updating skills library..."
git pull origin main
if [ -f "scripts/init-project.sh" ]; then
    install -m 755 "scripts/init-project.sh" "$HOME/.local/bin/skills-init" 2>/dev/null || true
    echo "✓ Refreshed skills-init command."
fi
echo "✓ Skills updated — linked projects use the latest (symlinks auto-resolve)."
UPDATESCRIPT
chmod +x "$HOME/.local/bin/skills-update"
echo -e "      ${GREEN}✓${NC} skills-update → $HOME/.local/bin/skills-update"

# Step 4: Verify
echo -e "${YELLOW}[4/4]${NC} Verifying installation..."
skill_count=$(find "$SKILLS_HOME/skills" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
echo -e "      ${GREEN}✓${NC} $skill_count skills available"

if [ -n "$agents_configured" ]; then
    echo -e "      ${GREEN}✓${NC} Agents configured:$agents_configured"
fi

# PATH reminder
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo -e "${YELLOW}⚠${NC}  Add to your shell profile (~/.zshrc or ~/.bashrc):"
    echo -e "   ${BLUE}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Installation complete!${NC}"
echo ""
echo -e "  In any project, run:  ${BLUE}skills-init${NC}"
echo -e "  To update all skills: ${BLUE}skills-update${NC}"
echo -e "  Bootstrap guide:      ${BLUE}less \$HOME/.zeroes-ones/skills/PROJECT-BOOTSTRAP.md${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
