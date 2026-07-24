# Breaking Change Propagation

Multi-step process for safely making breaking changes when consumers live in independent repositories. In polyrepo, you cannot atomically update all consumers — you need a migration window.

## The 5-Step Propagation Process

### Step 1: Assess Blast Radius

- Identify all consumer repos using dependency graph, grep, or package registry dependents
- Classify: active consumers (deployed this quarter) vs dormant (no recent deploys)
- For each active consumer: owner team, release cadence, criticality

### Step 2: Design Migration Path

- Add new interface alongside old. Never remove old first.
- Mark old as `@deprecated` with migration guide and hard deadline.
- Deadline formula: longest consumer release cycle × 2 (minimum 30 days).
- Provide codemod or automated migration script if feasible.

### Step 3: Communicate

- Notify all consumer teams: what is changing, why, how to migrate, deadline.
- Create tracking issues in consumer repos or a centralized migration tracker.
- Office hours for complex migrations.

### Step 4: Monitor Adoption

- Track % consumers migrated vs. deadline.
- At 50% of deadline: if <50% migrated, escalate to engineering leadership.
- At deadline: if active consumers remain, extend deadline. Do not force-break.

### Step 5: Remove Old Interface

- Only after ALL active consumers migrated + 1 release cycle buffer.
- Archive with comment documenting removal date and migration completion.
- Post-mortem if migration exceeded planned timeline by >50%.

## Anti-Patterns

- **"We will update consumers ourselves."** You lack consumer context. You will miss edge cases.
- **"Just bump the major version and let them deal with it."** Destroys trust. Consumers will pin old versions indefinitely.
- **No deprecation window.** Surprise breakage erodes confidence in shared dependencies.
