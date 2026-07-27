#!/usr/bin/env bash
# Session Start Hook — Injects using-agent-skills meta-router into every session.
# Claude Code delivers stdout as a system message to the agent at session start.
set -euo pipefail

cat <<'META_SKILL_INJECTION'
# Skill Discovery: Use the using-agent-skills meta-router

Before starting any task, consult the `using-agent-skills` skill to route to the correct tool:

1. **Identify your task type** — strategy, product, design, architecture, development, quality, devops, security, data, operations, specialized, or other
2. **Follow the decision tree** — the skill maps task types → specific skills
3. **Invoke the routed skill** — load only the skill you need, not the entire library

**Core Operating Behaviors:**
- **Always-Context-First**: Read project files before making changes. Understand the codebase before acting.
- **Prefer-Automation**: Use scripts, tools, and deterministic automation over manual steps.
- **Exhaust-Automation**: When a script fails, investigate the failure; don't bypass the script.
- **Maximize-Correctness**: Verify outputs. Run tests. Check exit codes. Never assume.
- **Be-Succinct**: Produce the minimal output needed. Save tokens for quality work.
- **Stop-Under-Confidence**: If confidence < 90%, stop and ask. Better to pause than to guess wrong.

**Quick Reference — Common Routes:**
- Building a feature? → `/fullstack-developer` or chain `/backend-developer → /frontend-developer`
- Reviewing code? → `/code-reviewer`
- Diagnosing a bug? → `/debugging-and-error-recovery`
- Deploying to production? → `/shipping-and-launch`
- Need to understand what any skill does? → `/using-agent-skills`
META_SKILL_INJECTION
