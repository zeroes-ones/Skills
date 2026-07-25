# Sandbox Execution — Reference

> **Runtime tool:** `scripts/sandbox-exec.sh`
> **Security coverage:** Context-window injection defense + untrusted code execution
> **Integrated with:** ai-security (Phase 0 + Decision Tree 7), supply-chain-security (provenance → trust tier)

## Overview

`sandbox-exec.sh` provides a 3-mode security boundary for agent operations:

| Mode | Command | Use When |
|------|---------|----------|
| **Scan** | `--scan <project-path>` | About to read files from a cloned/third-party repo; want to detect injection patterns before loading into context |
| **Sanitize** | `--sanitize <file>` | Need to clean a specific file of instruction-hijacking patterns before agent reads it |
| **Execute** | `--command '<cmd>' --project <path> [--allow-network]` | Need to run untrusted code (third-party scripts, user-provided commands, npm/pip package tests) |

## 27 Injection Patterns Tracked

### Instruction Overrides (7 patterns)
- `IGNORE (PREVIOUS|ALL) (INSTRUCTIONS|RULES|CONSTRAINTS)`
- `DISREGARD (PREVIOUS|ALL) (INSTRUCTIONS|RULES|CONSTRAINTS)`
- `FORGET (PREVIOUS|ALL) (INSTRUCTIONS|RULES)`
- `OVERRIDE (SYSTEM|AGENT) (PROMPT|INSTRUCTIONS)`
- `YOU ARE NOW`
- `NEW (SYSTEM|AGENT) (PROMPT|INSTRUCTIONS)`
- `YOUR (NEW|ONLY) (ROLE|JOB|TASK) IS`

### System Prompt Extraction (4 patterns)
- `REPEAT (THE|YOUR) (SYSTEM|INITIAL) (PROMPT|INSTRUCTIONS)`
- `PRINT (THE|YOUR) (SYSTEM|INITIAL) (PROMPT|INSTRUCTIONS)`
- `WHAT (IS|ARE) YOUR (SYSTEM|INITIAL) (PROMPT|INSTRUCTIONS)`
- `OUTPUT YOUR (SYSTEM|BASE) PROMPT`

### Tool/Execution Hijacking (3 patterns)
- `EXECUTE (THIS|THE FOLLOWING) (COMMAND|CODE)`
- `RUN (THIS|THE FOLLOWING) (COMMAND|SCRIPT|CODE) WITHOUT (ASKING|CONFIRMATION)`
- `curl.*\|.*(bash|sh|python)`
- `\$\(.*rm -rf.*\)`

### Data Exfiltration (3 patterns)
- `SEND.*(TO|AT).*(http|https)://`
- `curl.*http.*\$\{?[A-Z_]+\}?`
- `ENV\|ENVIRONMENT\|SECRET\|TOKEN\|PASSWORD\|CREDENTIAL`

### Instruction Embedding (7 patterns)
- `\[SYSTEM\]:`
- `\[INST\]:`
- `<\|\|_start\|>`
- `<\|\|_end\|>`
- `<<SYS>>`
- `<system>`
- `Human:.*Assistant:`

### Token Smuggling (3 patterns)
- `(IGNORE|DISREGARD).*ABOVE.*(INSTRUCTION|RULE)`
- `IMPORTANT:.*IGNORE`
- `CRITICAL:.*OVERRIDE`

## Trust Tier Classification

| Tier | Definition | Sanitization | Execution | Example |
|------|-----------|-------------|-----------|---------|
| **TRUSTED** | Your org's repos, files you authored, verified publishers with SLSA L3+ | None needed | Standard execution | Your company's monorepo, official npm packages from known maintainers |
| **UNKNOWN** | Public repos without verified maintainers, community packages, user-provided files | Required: strip all injection patterns, wrap in untrusted-content preamble | Sandbox with network BLOCKED | Random GitHub repo, new npm package (<100 stars), user-uploaded script |
| **UNTRUSTED** | Known malicious sources, pastebin links, anonymous gists, packages flagged by security tools | Do not load into primary context. Read via sandboxed subprocess, capture structure only | NEVER execute in primary process. Inform user of risk. | Pastebin script, "free破解版" package, anonymous gist |

## Execution Isolation

| Platform | Isolation Mechanism | Read-Only Source | Network Isolation |
|----------|-------------------|-----------------|-------------------|
| **macOS** | `cp -R` to temp + `chmod -R u-w` | Read-only filesystem (simulated) | `env -u HTTP_PROXY -u HTTPS_PROXY` strips proxy/env vars |
| **Linux** | `unshare -r -m -p [-n] --fork` | Copy + namespace isolation | `-n` flag creates network namespace (no network) |

## File Size & Safety Limits

- **Max file size:** 10MB (configurable via `--max-file-size`)
- **Binary files skipped:** `file` command detects binary/data/archive/image/audio/video
- **Build artifacts skipped:** `node_modules/`, `.git/`, `.next/`, `dist/`, `build/`, `.venv/`, `__pycache__/`
- **Audit log:** Every file access, pattern match, and execution step logged to `$SANDBOX_ROOT/audit.log`

## Output Verification Checklist

After sandbox execution, verify:

- [ ] Exit code is expected (non-zero → investigate before trusting output)
- [ ] stderr is clean (no suspicious patterns: network requests, file writes outside /tmp, credential access)
- [ ] stdout matches expected format (truncated output shown for review)
- [ ] No files written to the project directory (all output in `$SANDBOX_ROOT/output/`)
- [ ] Audit log reviewed for any ALERT-level findings during pre-scan

## Integration Points

| Integration | How |
|-------------|-----|
| **ai-security → Phase 0** | Before loading any external file, run `--scan` on the source directory |
| **ai-security → Decision Tree 7** | Full sandboxed execution workflow: classify → scan → execute → verify |
| **supply-chain-security** | Provenance verification feeds trust tier: SLSA L3+ with Sigstore → TRUSTED |
| **code-reviewer** | Can invoke sandbox to safely test PR code from external contributors |
| **ci-cd-builder** | Runs build/test commands from cloned repos in sandbox before allowing merge |
| **pre-commit hook** | `scripts/validate-skills.sh` can call `--scan` on modified skill files |

## Security Model

```
┌─────────────────────────────────────────────────┐
│              PRIMARY AGENT PROCESS               │
│  (trusted — has access to env vars, SSH, creds)  │
└────────────────────┬────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌─────────────────┐    ┌─────────────────────┐
│  SANDBOX SCAN   │    │  SANDBOX EXECUTION   │
│  (read-only)    │    │  (isolated process)   │
│                 │    │                       │
│  • Scans files  │    │  • No primary env     │
│  • Detects      │    │  • Read-only source   │
│    patterns     │    │  • Network blocked    │
│  • Never writes │    │  • Output to /tmp     │
│  • Audit log    │    │  • Audit log          │
└─────────────────┘    └─────────────────────┘
```

**The boundary is absolute:** untrusted code never runs in the primary agent process. No environment variables, SSH keys, cloud credentials, or file system access leak across the sandbox boundary.
