## Core Workflow

### Phase 1: Design the Template System

Execute in order. Do not skip steps.

```
1. AUDIT EXISTING REPOS FOR COMMON PATTERNS
   |-- Review 10-20 existing repos. Extract common files:
   |   |-- CI/CD configs (.github/workflows, .gitlab-ci.yml, Jenkinsfile)
   |   |-- Linter configs (.eslintrc, .prettierrc, pyproject.toml, .golangci.yml)
   |   |-- TypeScript/Python/Java configs (tsconfig.json, pyproject.toml, pom.xml)
   |   |-- Git configs (.gitignore, .gitattributes)
   |   |-- Governance files (CODEOWNERS, SECURITY.md, CONTRIBUTING.md, LICENSE)
   |   |-- README template (project name, description, setup, deploy, team)
   |-- Identify the "minimum viable repo" — the files every repo MUST have
   |-- Identify variations: frontend vs backend, TypeScript vs Python, service vs library

2. DESIGN TEMPLATE INHERITANCE HIERARCHY
   |-- Level 0: Org Base Template
   |   |-- Content: CI/CD workflow skeleton, SECURITY.md, CODEOWNERS, .gitignore, LICENSE
   |   |-- Applies to: EVERY repo in the org. Non-negotiable.
   |-- Level 1: Language Template (extends Base)
   |   |-- TypeScript: tsconfig.json, eslint config, prettier config, jest config
   |   |-- Python: pyproject.toml, ruff config, pytest config, mypy config
   |   |-- Go: go.mod, .golangci.yml, Makefile
   |-- Level 2: Framework Template (extends Language)
   |   |-- React: vite.config.ts, tailwind config, testing-library setup
   |   |-- Next.js: next.config.js, middleware, app directory structure
   |   |-- FastAPI: main.py skeleton, route structure, pydantic models
   |-- Level 3: Team Overlay (extends Framework, optional)
   |   |-- Team-specific lint rules, preferred libraries, custom scripts
   |   |-- Must NOT override org-level security or CI requirements

3. SELECT TEMPLATE ENGINE
   |-- Decision factors: primary language, complexity needs, update mechanism
   |-- Options: GitHub template repos, cookiecutter, degit, Yeoman, custom CLI
   |-- See Decision Trees: Template Engines for detailed comparison

4. IMPLEMENT THE TEMPLATE
   |-- Create the base template first. Validate: can a new repo be created and pass CI in <5min?
   |-- Create language templates next. Test: create a TypeScript repo from template, does CI pass?
   |-- Create framework templates. Test: create a Next.js repo, run dev server, does it work?
   |-- Document: each template README explains what is included and how to customize.

5. DESIGN DOWNSTREAM SYNC STRATEGY
   |-- Option A: Automated PRs (preferred). When base template updates, PR to all downstream repos.
   |-- Option B: Scheduled drift detection. CI checks downstream against template. Alerts on drift.
   |-- Option C: Manual sync. Quarterly audit. Only for small orgs (<10 repos).
   |-- See Decision Trees: Downstream Sync for detailed strategies.
  Complete when: template inheritance hierarchy is designed with org base → language → framework → team overlay levels, template engine is selected with documented rationale, and a new repo created from template passes CI in under 5 minutes.
```

### Phase 2: Audit & Sync

```
1. DRIFT DETECTION
   |-- For each downstream repo, compute a diff against its template
   |-- Identify: intentional customizations vs unintentional drift
   |-- Flag: security-critical files that diverged (CI workflows, SECURITY.md)
   |-- Flag: CI configs that removed required security checks

2. DRIFT CLASSIFICATION
   |-- Intentional (approved): team-specific customizations, documented and justified
   |-- Unintentional (drift): CI version behind template, linter rules removed, SECURITY.md outdated
   |-- Unknown: change exists but no documentation — investigate with owning team

3. SYNC PROCESS
   |-- For unintentional drift: automated PR to align with template
   |-- For intentional customizations: document in TEAM_CUSTOMIZATIONS.md in repo root
   |-- For security-critical drift: escalate to engineering leadership
   |-- Sync cadence: monthly for all repos, weekly for critical repos

4. CONSISTENCY DASHBOARD
   |-- % repos matching template (target: >90%)
   |-- Average drift age (target: <30 days)
   |-- Number of repos with undocumented customizations (target: 0)
  Complete when: drift detection identifies all diverged repos, unintentional drift has automated PRs to realign, intentional customizations are documented in TEAM_CUSTOMIZATIONS.md, and consistency dashboard tracks the three targets.
```

### Phase 3: Migrate Existing Repos

```
1. ASSESS MIGRATION CANDIDATES
   |-- Repos <6 months old: high ROI, less accumulated custom config
   |-- Repos that are still actively maintained: worth migrating
   |-- Repos in maintenance mode: low priority, migrate only if security gaps exist
   |-- Archived repos: do not migrate

2. CREATE MIGRATION PR
   |-- Diff repo against target template
   |-- For each file: is the template version better? If yes, adopt. If repo version is intentional, skip.
   |-- NEVER overwrite business logic or application code — template covers config files only
   |-- PR description: what changed, why, what was intentionally kept

3. VALIDATE MIGRATION
   |-- CI must pass on migration PR
   |-- Dev server/application must start and function
   |-- Tests must pass (template changes should not break application tests)
   |-- Owning team must approve before merge

4. POST-MIGRATION
   |-- Add repo to downstream sync list
   |-- Document any permanent customizations in TEAM_CUSTOMIZATIONS.md
   |-- Monitor for 2 weeks: did migration introduce any issues?
  Complete when: migration PR is approved by owning team, CI passes on all migrated repos, and migrated repos are added to downstream sync with documented customizations.
```
