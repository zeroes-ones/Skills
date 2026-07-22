#!/usr/bin/env bash
#=============================================================================
# Skills Library — Global Install
# Author: Sandeep Kumar Penchala
#
# One-time setup. Clones the skills library to a canonical location and 
# creates global symlinks so every project can access all 56 skills.
#
# Usage: curl -sSL https://raw.githubusercontent.com/zeroes-ones/Skills/main/scripts/install.sh | bash
#    or: ./scripts/install.sh
#=============================================================================
set -euo pipefail

SKILLS_HOME="${SKILLS_HOME:-$HOME/.zeroes-ones/skills}"
REPO_URL="https://github.com/zeroes-ones/Skills.git"
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

# Format: agent_name:target_dir (colon-separated)
AGENT_LIST="claude:$HOME/.claude/skills copilot:$HOME/.copilot/skills cursor:$HOME/.cursor/skills openclaw:$HOME/.openclaw/workspace/skills"

agents_configured=""
for entry in $AGENT_LIST; do
    agent="${entry%%:*}"
    target="${entry#*:}"
    if [ -L "$target" ]; then
        echo -e "      ${GREEN}✓${NC} $agent already linked"
        agents_configured="$agents_configured $agent"
    elif [ -d "$(dirname "$target")" ] || mkdir -p "$(dirname "$target")" 2>/dev/null; then
        rm -rf "$target" 2>/dev/null || true
        ln -sf "$SKILLS_HOME/skills" "$target"
        echo -e "      ${GREEN}✓${NC} $agent → $target"
        agents_configured="$agents_configured $agent"
    else
        echo -e "      ${YELLOW}○${NC} $agent not installed (skip)"
    fi
done

# Step 3: Create convenience command
echo -e "${YELLOW}[3/4]${NC} Creating convenience commands..."

# skills-init command for per-project setup
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/skills-init" << 'INITSCRIPT'
#!/usr/bin/env bash
# Run this inside any project directory to activate all skills
SKILLS_HOME="${SKILLS_HOME:-$HOME/.zeroes-ones/skills}"
PROJECT="${1:-.}"

cd "$PROJECT" || { echo "Cannot access $PROJECT"; exit 1; }
echo "Activating skills in $(pwd)..."

# Format: agent_name:target_dir (colon-separated)
AGENT_LIST="claude:.claude/skills copilot:.copilot/skills cursor:.cursor/skills openclaw:.openclaw/workspace/skills"

for entry in $AGENT_LIST; do
    agent="${entry%%:*}"
    target="${entry#*:}"
    parent=$(dirname "$target")
    if [ -d "$parent" ] || mkdir -p "$parent" 2>/dev/null; then
        rm -rf "$target" 2>/dev/null || true
        ln -sf "$SKILLS_HOME/skills" "$target"
        echo "  ✓ $agent → $target"
        # Add to .gitignore
        grep -q "^$target$" .gitignore 2>/dev/null || echo "$target" >> .gitignore
    fi
done

# Also symlink bootstrap guide
ln -sf "$SKILLS_HOME/PROJECT-BOOTSTRAP.md" .skills-bootstrap.md 2>/dev/null || true
echo ""
echo "✓ Skills activated. Use /{skill-name} to invoke any skill."
echo "  See .skills-bootstrap.md for the lifecycle navigation guide."
INITSCRIPT
chmod +x "$HOME/.local/bin/skills-init"
echo -e "      ${GREEN}✓${NC} skills-init → $HOME/.local/bin/skills-init"

# skills-update command for pulling latest
cat > "$HOME/.local/bin/skills-update" << 'UPDATESCRIPT'
#!/usr/bin/env bash
SKILLS_HOME="${SKILLS_HOME:-$HOME/.zeroes-ones/skills}"
cd "$SKILLS_HOME" || exit 1
echo "Updating skills library..."
git pull origin main
echo "✓ All projects now use updated skills (symlinks auto-resolve)."
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
