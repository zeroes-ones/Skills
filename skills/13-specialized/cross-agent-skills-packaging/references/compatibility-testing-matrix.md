# Compatibility Testing Matrix

## Overview

Before claiming a skill is "cross-agent compatible," verify it across all target agent terminals. A skill that loads in Claude Code but fails silently in Copilot CLI is not cross-agent compatible — it's Claude-only with a misleading `portability` field.

## Test Framework

### Phase 1: Load Test (Each Agent)

| Test | Claude Code | Copilot CLI | Cursor | Codex | Gemini CLI | OpenCode | OpenClaw |
|------|------------|-------------|--------|-------|-----------|----------|----------|
| Skill appears in available skills list | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| No load errors in agent logs | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Frontmatter parsed correctly | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| All reference links resolve | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| PROCESS_TREE.md present (Claude only) | ☐ | N/A | N/A | N/A | N/A | N/A | N/A |

### Phase 2: Intent Routing Test

| Test | Expected Behavior |
|------|------------------|
| User asks "package this skill for cross-agent" | Skill activates via intent routing |
| User mentions "~/.agents/skills/" | Skill activates via auto-route |
| User asks about "symlink strategy" | Skill routes to Decision Tree #1 |
| User mentions "frontmatter conflict" | Skill routes to Decision Tree #2 |
| User mentions "manifest generation" | Skill routes to Decision Tree #3 |

### Phase 3: Decision Tree Execution Consistency

Verify each decision tree produces the same output across agents:

| Decision Tree | Claude Code | Copilot CLI | Cursor | Codex | Gemini CLI | OpenCode |
|---------------|------------|-------------|--------|-------|-----------|----------|
| Symlink vs Copy | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Frontmatter Normalization | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Agent Discovery Flow | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Conflict Resolution | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Manifest Generation | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

### Phase 4: Token Efficiency Benchmark

| Agent | Tokens Consumed (skill load) | Tokens Consumed (full execution) | Overhead vs Baseline |
|-------|------------------------------|----------------------------------|---------------------|
| Claude Code | | | |
| Copilot CLI | | | |
| Cursor | | | |
| Codex | | | |
| Gemini CLI | | | |
| OpenCode | | | |
| **Average** | | | |

### Phase 5: Edge Cases

| Edge Case | Pass/Fail | Notes |
|-----------|-----------|-------|
| Skill with no overrides (pure symlink) | | |
| Skill with per-agent overrides | | |
| Skill with broken symlink | | |
| Skill with circular dependency in chain | | |
| Skill with missing required field | | |
| Skill with vendor-specific frontmatter leakage | | |
| Skill with >10 reference files | | |
| Skill with nested directory structure | | |

## Automated Test Script

```bash
#!/usr/bin/env bash
# compatibility-test.sh — Test a skill across all configured agent terminals
SKILL_NAME="${1:?Usage: $0 <skill-name>}"
REPORT="compatibility-report-${SKILL_NAME}-$(date +%Y%m%d).json"
RESULTS='{"skill": "'$SKILL_NAME'", "timestamp": "'$(date -Iseconds)'", "results": {}}'

test_agent() {
  local agent="$1"
  local skill_dir="$HOME/.${agent}/skills/${SKILL_NAME}"
  
  if [ -L "$skill_dir" ] && [ -e "$skill_dir" ]; then
    echo "  [PASS] $agent: symlink exists and resolves"
    RESULTS=$(echo "$RESULTS" | jq ".results[\"$agent\"] = {symlink: \"ok\"}")
  elif [ -d "$skill_dir" ]; then
    echo "  [WARN] $agent: directory exists but is not a symlink"
    RESULTS=$(echo "$RESULTS" | jq ".results[\"$agent\"] = {symlink: \"copy-not-symlink\"}")
  else
    echo "  [FAIL] $agent: skill directory not found"
    RESULTS=$(echo "$RESULTS" | jq ".results[\"$agent\"] = {symlink: \"missing\"}")
    return
  fi

  # Check SKILL.md present
  if [ -f "$skill_dir/SKILL.md" ]; then
    echo "    [PASS] $agent: SKILL.md found"
  else
    echo "    [FAIL] $agent: SKILL.md missing"
    RESULTS=$(echo "$RESULTS" | jq ".results[\"$agent\"] += {skill_md: \"missing\"}")
  fi

  # Check frontmatter
  if head -1 "$skill_dir/SKILL.md" 2>/dev/null | grep -q "^---$"; then
    echo "    [PASS] $agent: YAML frontmatter detected"
  else
    echo "    [FAIL] $agent: No YAML frontmatter"
    RESULTS=$(echo "$RESULTS" | jq ".results[\"$agent\"] += {frontmatter: \"missing\"}")
  fi

  # Claude-specific: PROCESS_TREE.md
  if [ "$agent" = "claude" ]; then
    if [ -f "$skill_dir/PROCESS_TREE.md" ]; then
      echo "    [PASS] $agent: PROCESS_TREE.md present"
    else
      echo "    [FAIL] $agent: PROCESS_TREE.md MISSING (Claude Code won't detect skill)"
      RESULTS=$(echo "$RESULTS" | jq ".results[\"$agent\"] += {process_tree: \"missing\"}")
    fi
  fi
}

echo "=== Compatibility Test: $SKILL_NAME ==="
for agent in claude copilot cursor codex gemini opencode openclaw; do
  test_agent "$agent"
done

echo "$RESULTS" | jq '.' > "$REPORT"
echo ""
echo "Report saved to: $REPORT"
```

## Compatibility Report Matrix

The output is a JSON matrix:

```json
{
  "skill": "cross-agent-skills-packaging",
  "timestamp": "2026-07-24T12:00:00Z",
  "results": {
    "claude": {"symlink": "ok", "skill_md": "ok", "frontmatter": "ok", "process_tree": "ok"},
    "copilot": {"symlink": "ok", "skill_md": "ok", "frontmatter": "ok"},
    "cursor": {"symlink": "ok", "skill_md": "ok", "frontmatter": "ok"},
    "codex": {"symlink": "ok", "skill_md": "ok", "frontmatter": "ok"},
    "gemini": {"symlink": "ok", "skill_md": "ok", "frontmatter": "ok"},
    "opencode": {"symlink": "ok", "skill_md": "ok", "frontmatter": "ok"},
    "openclaw": {"symlink": "ok", "skill_md": "ok", "frontmatter": "ok"}
  },
  "summary": {
    "total": 7,
    "pass": 7,
    "fail": 0,
    "warn": 0,
    "overall": "COMPATIBLE"
  }
}
```

## CI Integration

Integrate compatibility testing into your CI pipeline:

```yaml
# .github/workflows/skill-compatibility.yml
name: Skill Compatibility Check
on:
  push:
    paths:
      - 'skills/**'
jobs:
  test-compatibility:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Test cross-agent compatibility
        run: |
          for skill in skills/*/SKILL.md; do
            skill_name=$(basename "$(dirname "$skill")")
            bash scripts/compatibility-test.sh "$skill_name"
          done
      - name: Upload compatibility report
        uses: actions/upload-artifact@v4
        with:
          name: compatibility-reports
          path: compatibility-report-*.json
```

## Gotcha: False Positives in Compatibility Testing

A skill that loads without errors in all agents may still produce incorrect results in one agent. Load testing is necessary but not sufficient. Always follow up with:
1. **Intent routing test:** Does the skill activate when the user asks a relevant question?
2. **Decision tree execution:** Does each decision tree produce the same output?
3. **Output validation:** Are the outputs semantically equivalent across agents?
