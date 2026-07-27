# /ship — Prepare and execute production deployment

Run pre-launch checklist, stage rollouts, feature flag management, and launch-day monitoring. Uses parallel fan-out of `code-reviewer`, `security-auditor`, and `test-engineer` personas.

**When to use**: When a feature is ready for production deployment.

**Workflow**:
1. **Parallel fan-out**: Spawn `code-reviewer`, `security-auditor`, `test-engineer` personas simultaneously
2. **Merge results**: Aggregate findings from all three
3. **Gate check**: If all pass → proceed. If any fail → report and block deployment
4. Invoke `shipping-and-launch` skill for deployment execution
5. Staged rollout: canary 5% → monitor 10min → 25% → 10min → 100%
6. Output: Deployed feature with monitoring dashboards and rollback plan

**What it produces**: A deployed feature with canary monitoring, rollback procedures, launch-day runbook, and post-deployment verification.
