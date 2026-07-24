# Cross-Agent Directory Conventions

## Root: `~/.agents/`

All agent-related artifacts live under a single root directory. This keeps the
workspace clean and provides a predictable location for cross-agent handoffs.

```
~/.agents/
├── skills/              # Skill definitions and configurations
│   ├── active/          # Currently loaded skills (symlinks or copies)
│   ├── cache/           # Cached skill bundles
│   └── versions.lock    # Pinned skill versions
├── state/               # Cross-agent state artifacts
│   ├── handoffs/        # Serialized handoff payloads
│   │   └── {pipeline_id}/
│   │       ├── 001-system-architect→backend-developer.json
│   │       ├── 002-backend-developer→devops-engineer.json
│   │       └── 003-backend-developer→security-engineer.json
│   ├── ledgers/         # Decision gate ledgers
│   │   └── {pipeline_id}.json
│   └── contracts/       # Signed handoff contracts
│       └── {pipeline_id}/
│           └── {origin}→{target}.md
├── artifacts/           # Shared output files
│   ├── adrs/            # Architecture Decision Records
│   ├── specs/           # API specs, data models
│   ├── configs/         # Generated configuration files
│   └── diagrams/        # Architecture diagrams (Mermaid, PlantUML)
├── logs/                # Agent execution logs
│   └── {skill-name}/
│       └── {pipeline_id}.log
└── tmp/                 # Temporary working files (auto-cleaned)
```

## Conventions

1. **Pipeline ID as namespace:** All artifacts for a pipeline run share the same
   `pipeline_id` directory.
2. **Sequential numbering:** Handoff files are numbered `NNN-origin→target.json`
   to preserve pipeline order.
3. **Immutable history:** Once written, handoff files are append-only. New decisions
   go in new handoff files, not by editing old ones.
4. **Cleanup policy:** `tmp/` is cleaned after pipeline completion. `state/` and
   `artifacts/` persist for audit trail.
5. **Symlink isolation:** Agent working directories should NOT reference each
   other's internal state directly. All cross-agent communication goes through
   `~/.agents/state/handoffs/`.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENTS_HOME` | `~/.agents` | Root of agent directory tree |
| `AGENTS_STATE_DIR` | `$AGENTS_HOME/state` | Handoff and ledger storage |
| `AGENTS_ARTIFACTS_DIR` | `$AGENTS_HOME/artifacts` | Shared output files |
| `PIPELINE_ID` | (auto-generated UUID) | Current pipeline identifier |
| `PIPELINE_STAGE` | (set by orchestrator) | Current stage index |
