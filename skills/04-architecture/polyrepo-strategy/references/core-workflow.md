## Core Workflow

### Phase 1: Assess Current State & Make the Decision

Execute in order. Do not skip steps.

```
1. MAP TEAM TOPOLOGY TO REPO TOPOLOGY
   |-- List all teams (5-15 people each, aligned to business capability)
   |-- List all repos with primary owning team
   |-- Identify misalignments:
   |   |-- Multiple teams owning same repo = coupling hotspot
   |   |-- One team owning >7 repos = fragmentation risk
   |   |-- Orphan repos (no clear owner) = operational debt
   |-- Draw the Conway alignment: does repo boundary match team boundary?

2. MEASURE CROSS-REPO COUPLING
   |-- Analyze git history for cross-repo references over last 6 months
   |-- Calculate: (% of PRs touching multiple repos) / (total PRs)
   |-- Thresholds:
   |   |-- <10% cross-repo PRs: Repos are well-decoupled. Polyrepo works.
   |   |-- 10-30%: Borderline. Investigate whether coupling is necessary or accidental.
   |   |-- >30%: High coupling. Teams shipping together should consider shared repo.
   |-- Also measure: average time from PR open in Repo A to related PR merge in Repo B

3. EVALUATE RELEASE CADENCE ALIGNMENT
   |-- For each repo: what is the release frequency? (continuous, daily, weekly, monthly, quarterly)
   |-- If repos release on same cadence AND depend on each other: monorepo reduces coordination
   |-- If repos release independently AND rarely depend on each other: polyrepo enables autonomy
   |-- Hybrid signal: core libraries on monthly cadence, product services on daily cadence

4. SCORE THE DECISION MATRIX
   |-- Score each dimension 1-5 (1=strongly favors polyrepo, 5=strongly favors monorepo):
   |   |-- Team autonomy: do teams operate independently? (1=completely independent, 5=always coordinated)
   |   |-- Code sharing frequency: how often is shared code modified? (1=rarely, 5=daily)
   |   |-- Release coupling: must repos version together? (1=never, 5=always)
   |   |-- Security boundaries: different classification levels? (1=many boundaries, 5=single level)
   |   |-- Build times: would monorepo CI be acceptable? (1=unacceptable >30min, 5=fast <5min)
   |   |-- Tooling maturity: do you have monorepo tooling? (1=no tooling, 5=dedicated team)
   |-- Average score < 2.5: Polyrepo is the right default
   |-- Average score 2.5-3.5: Hybrid approach warranted
   |-- Average score > 3.5: Monorepo is the right default
```

### Phase 2: Audit Repo Health

```
1. IDENTIFY REPO SPRAWL
   |-- List all repos with last commit date
   |-- Flag: no commits in >6 months = candidate for archival
   |-- Flag: <5 commits in 12 months = low-activity, investigate
   |-- Flag: no clear owner (no CODEOWNERS, no team mapping) = orphan risk

2. AUDIT CI/CD CONSISTENCY
   |-- Compare .github/workflows/ across repos
   |-- Count unique CI configurations / total repos ratio
   |-- Flag: ratio >0.5 = highly fragmented (each repo has unique CI)
   |-- Target: ratio <0.2 (80%+ repos share canonical CI templates)

3. CHECK DEPENDENCY VERSION ALIGNMENT
   |-- For each shared dependency (framework, core lib), count distinct versions across repos
   |-- Flag: >3 versions of same framework = version sprawl
   |-- Flag: CVEs in shared dependencies across >5 repos = blast radius

4. MEASURE INNER SOURCE HEALTH
   |-- Cross-repo PR ratio: PRs from non-owning-team / total PRs
   |-- Flag: ratio <5% = siloed repos, no inner source culture
   |-- Flag: ratio >30% = may indicate unclear ownership
   |-- Average PR review time for cross-team contributions
```

### Phase 3: Establish Repo Governance

```
1. DEFINE REPO CREATION STANDARDS
   |-- When to create a new repo:
   |   |-- Independent deployable unit with its own release cadence
   |   |-- Different security/access boundary than existing repos
   |   |-- Separate team with no coordinated releases
   |   |-- Different language/framework than existing repos (divergent tooling)
   |-- When NOT to create a new repo:
   |   |-- "It feels cleaner" without operational justification
   |   |-- Same team, same release cadence as existing repo
   |   |-- Shared code that is tightly coupled to one consumer

2. DEFINE REPO LIFECYCLE
   |-- Creation: template-based scaffolding (see repo-scaffolding skill)
   |-- Active: maintained, CI passing, owner responsive
   |-- Maintenance: critical fixes only, no feature development
   |-- Deprecated: read-only, migration guide published, consumers notified
   |-- Archived: read-only, no new issues/PRs, redirect to replacement

3. ESTABLISH CROSS-REPO COORDINATION MECHANISMS
   |-- Repo-to-repo CI: repository_dispatch, workflow_dispatch with explicit contracts
   |-- Version policy: SemVer for shared libraries, lockstep ranges for frameworks
   |-- Contract testing: consumer-driven contracts between service repos
   |-- Breaking change process: deprecation window, migration guide, automated detection

4. IMPLEMENT OWNERSHIP MODEL
   |-- Every repo has CODEOWNERS with at least 2 maintainers
   |-- Escalation path for orphan repos (platform team as backstop)
   |-- Quarterly ownership review: are owners still active? team still exists?
```
