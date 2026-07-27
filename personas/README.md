# Agent Personas — The "Who" Layer

Personas define agent roles with tool restrictions, default skills, and orchestration rules. They sit between slash commands (the *when*) and skills (the *how*).

## Architecture

```
Layer 1: Skills     (how) → SKILL.md files — 210 skills across 28 domains
Layer 2: Personas   (who) → persona definitions — role-based tool restrictions
Layer 3: Commands   (when) → slash commands — user-facing routing to persona+skill combos
```

## Available Personas

### code-reviewer
- **Role**: Read-only code reviewer
- **Allowed tools**: Read, Grep, Glob
- **Prohibited tools**: Edit, Write, Bash (mutating)
- **Default skills**: code-reviewer, code-simplification
- **Orchestration**: Parallelizable

### security-auditor
- **Role**: Read-only security auditor
- **Allowed tools**: Read, Grep, Glob
- **Prohibited tools**: Edit, Write, Bash (mutating)
- **Default skills**: security-reviewer, security-engineer
- **Orchestration**: Parallelizable

### test-engineer
- **Role**: Test-first developer
- **Allowed tools**: Read, Grep, Glob, Edit, Write (tests only)
- **Prohibited tools**: Edit/Write on source files
- **Default skills**: tdd-guide, qa-engineer
- **Orchestration**: Parallelizable

### web-perf-auditor
- **Role**: Read-only performance auditor
- **Allowed tools**: Read, Grep, Glob, Network tools
- **Prohibited tools**: Edit, Write
- **Default skills**: performance-engineer
- **Orchestration**: Parallelizable

## Core Rules

1. **Personas cannot invoke other personas** — the user or slash command is the orchestrator
2. **Parallel fan-out is the only endorsed multi-persona pattern** — spawn personas in parallel, merge results
3. **Personas are stateless** — each invocation is independent
4. **Tool restrictions are enforced** — a persona cannot bypass its prohibited_tools list

## Parallel Fan-Out Pattern

```
/ship → spawns [code-reviewer, security-auditor, test-engineer] in parallel
     → merge results
     → if all pass → deploy
     → if any fail → report and block
```

## Adding a New Persona

1. Define the persona in `personas/<name>.md`
2. Specify `allowed_tools` and `prohibited_tools`
3. Assign `default_skills` — skills loaded automatically
4. Set `parallelizable: true` if fan-out safe
5. Create a slash command in `.claude/commands/` that routes to the persona
