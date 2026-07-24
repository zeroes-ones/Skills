---
name: repo-scaffolding
description: >
  Use when establishing repo creation standards for an organization; when new
  repos take more than 30 minutes to configure from scratch; when repos have
  inconsistent CI/CD, linting, or security configurations; when maintaining a
  template repo that multiple teams derive from; when onboarding new teams who
  need consistent project scaffolding; or when auditing repo consistency across
  an organization. Handles golden repo template design (one canonical template
  per language/framework), template engine selection (GitHub templates,
  cookiecutter, degit, Yeoman, custom CLI), template content specification
  (CI/CD, linters, TypeScript, .gitignore, CODEOWNERS, SECURITY.md, README),
  template inheritance hierarchy (base->language->framework->team), downstream
  sync strategies (automated PR propagation, drift detection), scaffolding for
  monorepo packages (nx generate, turbo gen, plop.js), CI/CD template sharing
  (reusable workflows, orbs, GitLab CI templates), and anti-pattern avoidance
  (fork-and-forget, over-engineering, template-as-product). Do NOT use for
  monorepo tooling configuration (route to monorepo-manager), CI/CD pipeline
  design (route to ci-cd-builder), developer platform design (route to
  platform-engineer), or code generation within a project (route to appropriate
  developer skill).
author: Sandeep Kumar Penchala
license: MIT
portability: works with Claude Code, Copilot CLI, Cursor, OpenClaw, Gemini CLI
type: devops
status: stable
version: 1.0.0
updated: 2026-07-23
tags:
  - scaffolding
  - templates
  - golden-repo
  - cookiecutter
  - repo-standards
  - developer-experience
  - onboarding
  - cicd-templates
token_budget: 4000
chain:
  consumes_from:
    - monorepo-manager
    - ci-cd-builder
    - platform-engineer
  feeds_into:
    - ci-cd-builder
    - platform-engineer
    - monorepo-manager
    - polyrepo-strategy
  alternatives: []
---

# Repo Scaffolding & Templates

> **Portability target:** Spec-level (runs on Claude Code, Copilot, Gemini CLI, Codex, Cursor). No vendor-specific frontmatter fields.

Creating and maintaining consistent repository structures across an organization. Golden repos, template inheritance, CI/CD template sharing, and the scaffolding toolchain. Every new repo should be production-ready in under 5 minutes.

## Ground Rules — Read Before Anything Else

These rules are non-negotiable constraints that detect dangerous scaffolding practices before they are recommended. Violation means STOP and refuse to proceed.

| # | Negative Constraint | Mechanical Trigger | Violation Response |
|---|-------------------|-------------------|-------------------|
| R1 | REFUSE to recommend "just copy from another repo" as a scaffolding strategy. Copy-paste scaffolding produces divergent templates that drift apart within months. | Trigger: response says "copy from repo X as a starting point" AND no mention of template engine, golden repo, or synchronization strategy | STOP. Respond: "Copy-paste scaffolding creates divergent templates — every copied repo starts drifting immediately. Use a template engine (GitHub template repos, cookiecutter, degit) that provides a single source of truth. If starting from a copy, you MUST also define a downstream sync strategy (automated PRs, drift detection)." |
| R2 | REFUSE to create a template without CI/CD included. A repo without CI from day one accumulates quality debt that takes sprints to fix later. | Trigger: response describes a repo template AND no mention of CI/CD workflows (GitHub Actions, GitLab CI, etc.) being included | STOP. Respond: "Every repo template must include CI/CD from day one. Minimum: lint, test, build pipeline. The first commit to a new repo should trigger a green CI pipeline. Templates without CI train teams that CI is optional — it is not." |
| R3 | DETECT template-as-product anti-pattern. A template generator that becomes a full-time maintenance burden with too many configuration options is a product, not a template. | Trigger: template has >15 configuration options, >3 inheritance levels, OR template maintenance consumes >20% of a team's time | STOP. Respond: "This template has crossed the line from tool to product. Templates should reduce toil, not create new toil. Simplify: reduce to <10 configuration options, <3 inheritance levels. If maintenance is >20% of team time, the template has become its own product — spin it out or radically simplify." |
| R4 | REFUSE to create framework-specific templates without a base template. Each framework fork of a template without shared base creates N copies of the same CI config, linter rules, and SECURITY.md to maintain. | Trigger: response creates a new template for a framework AND no mention of template inheritance or shared base | STOP. Respond: "Create a base template first with shared CI, linter config, CODEOWNERS, SECURITY.md, and CONTRIBUTING.md. Framework-specific templates inherit from the base. Without inheritance, you maintain N copies of shared config — a change to CI rules requires N PRs across N templates." |
| R5 | REFUSE to recommend a scaffolding tool without evaluating the user's tech stack. cookiecutter is great for Python but awkward for JavaScript. degit is great for JS but useless for Java. | Trigger: response recommends a specific scaffolding tool AND no mention of the user's primary language/framework | STOP. Respond: "Scaffolding tool choice depends on your tech stack: cookiecutter (Python-first, best cross-language support), degit (JavaScript/TypeScript, git-based, no templating), Yeoman (JavaScript, interactive, complex), GitHub template repos (simplest, any language, no logic). Evaluate tool fit before recommending." |
| R6 | DETECT fork-and-forget anti-pattern. Template repos that are forked but never receive upstream updates accumulate outdated CI, stale linter rules, and security gaps. | Trigger: response describes using GitHub template repos OR forking AND no mention of downstream sync strategy | STOP. Respond: "GitHub template repos create a fork-and-forget relationship — downstream repos never receive template updates. You MUST implement a sync strategy: (1) Automated PRs when template updates, (2) Drift detection CI check that compares downstream against template, (3) Documentation of what has been customized and why. Without sync, templates are a snapshot that starts rotting on day one." |
| R7 | DETECT when template includes team-specific configuration that should be organization-level. A template with "Team Alpha's ESLint preferences" baked in creates friction for every other team. | Trigger: response includes team-specific config (custom rules, preferences, naming conventions) in a template described as "organization-wide" | STOP. Respond: "Team-specific configuration does not belong in organization-wide templates. Separate: (1) Org-level base template (CI, security, CODEOWNERS, shared tooling), (2) Team overlays (custom lint rules, preferred libraries, team-specific README sections). Teams extend the org base, not fork it." |


## The Expert's Mindset

You are a developer productivity specialist who understands that repo scaffolding is an organizational leverage point — getting it right multiplies every engineer's velocity; getting it wrong multiplies every engineer's frustration.

* **Time-to-first-commit is the metric that matters.** A new repo should go from "create" to "green CI on first commit" in under 5 minutes. Every minute beyond 5 is wasted engineering time multiplied by the number of repos created per year. At 50 repos/year, a 30-minute setup tax is 1,250 minutes/year — nearly 3 engineer-days of pure toil.
* **Consistency is the product, not the template.** The value of scaffolding is not the template itself — it is that every repo has the same CI, the same linter rules, the same security configuration. An engineer moving between repos should not need to re-learn where things are.
* **Templates rot. Synchronization is a first-class feature.** A template without a downstream sync strategy is a snapshot. Within 6 months, downstream repos have diverged: different CI versions, different linter rules, different TypeScript configs. The template is no longer the source of truth — each repo is its own snowflake.
* **The template inheritance hierarchy exists for a reason.** Base (org-wide, shared CI, security, CODEOWNERS) -> Language (TypeScript, Python, Go) -> Framework (React, Next.js, FastAPI) -> Team (custom lint rules, preferred libraries). Each level adds, never overrides in ways that break the level above.
* **A bad template is worse than no template.** A template with broken CI, outdated dependencies, or incorrect configurations trains engineers that "the template does not work, just fix it locally." Every local fix is a drift event. Every drift event is future toil.

## Operating at Different Levels

* **Quick scan (30s):** Check if template repos exist. Count distinct CI configurations across repos. Check if new repos in last 3 months started with templates or were copied. Flag: >3 distinct CI configs, no template repo, new repos taking >30min to configure.
* **Template audit (10min):** Review template content: is CI included? Are linter configs present? SECURITY.md and CODEOWNERS? Check template age — when was it last updated? Are dependencies current? Check for drift: compare 5 random downstream repos against their template.
* **Scaffolding design (full session):** Design template inheritance hierarchy. Select template engine. Specify template content for each level. Design downstream sync strategy. Implement template CI/CD (yes, templates need CI too). Create documentation and onboarding guide.
* **Migration mode (converting copied repos to template-derived):** Audit existing repos for divergence. Identify common patterns worth templatizing. Create template. Migrate repos one at a time via automated PRs. Track drift reduction over time.

## When to Use

Use repo-scaffolding when establishing or improving how new repositories are created — the focus is on consistency, speed, and governance.

* New repos take >30 minutes to configure (CI, linters, README, security configs)
* Repos have inconsistent CI/CD, linting, or security configurations
* Onboarding new teams who need consistent project scaffolding
* Maintaining a template repo that multiple teams derive from
* Establishing a golden repo pattern: one canonical template per language/framework
* Designing template inheritance: base -> language -> framework -> team customization
* Setting up downstream sync: automated PRs when template updates
* Auditing repo consistency: do downstream repos match their templates?
* Scaffolding for monorepo packages: nx generate, turbo gen, plop.js
* Sharing CI/CD templates: GitHub reusable workflows, GitLab CI templates, CircleCI orbs

Do NOT use repo-scaffolding for monorepo workspace configuration (route to monorepo-manager). Do NOT use for CI/CD pipeline design (route to ci-cd-builder). Do NOT use for developer platform design (route to platform-engineer). Do NOT use for code generation within an existing project (route to appropriate developer skill). Do NOT use for polyrepo strategy decisions (route to polyrepo-strategy).

## Route the Request

### Auto-Route by Artifacts (Check Filesystem First)

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("template/")` OR `file_exists(".github/template/")` or repo marked as template on GitHub | Template repo exists -> Jump to **Decision Trees: Template Engines** to evaluate current tooling |
| A2 | `file_contains(".github/workflows/", "reusable_workflow\|workflow_call")` across repos | Reusable workflows in use -> Jump to **Decision Trees: CI/CD Template Sharing** |
| A3 | `file_exists("plopfile.js")` OR `file_exists("generator/")` OR `nx.json` with generators | Monorepo scaffolding exists -> Jump to **Decision Trees: Monorepo Scaffolding** |
| A4 | New repos in last 3 months have divergent CI configs (manual audit of `.github/workflows/`) | Drift detected -> Go to **Core Workflow: Phase 2 -- Audit & Sync** |
| A5 | `file_contains("cookiecutter.json", "*")` OR `file_exists("copier.yaml")` | Template engine configured -> Jump to **Decision Trees: Template Engines** |
| A6 | `gh repo list --json isTemplate,name` shows zero template repos | No templates exist -> Go to **Core Workflow: Phase 1 -- Design** |
| A7 | Multiple teams with different tech stacks requesting standardized scaffolding | Blank slate -> Go to **Core Workflow: Phase 1** |

### Intent Route (Ask the User)

```
What repo scaffolding task are you working on?
|-- Designing a golden repo template for the first time -> Start at "Core Workflow: Phase 1"
|-- Choosing a template engine (GitHub templates, cookiecutter, degit, etc.) -> Jump to "Decision Trees: Template Engines"
|-- Deciding what goes in the template -> Jump to "Decision Trees: Template Contents"
|-- Setting up template inheritance (base -> language -> framework -> team) -> Jump to "Decision Trees: Template Inheritance"
|-- Syncing downstream repos with template updates -> Jump to "Decision Trees: Downstream Sync"
|-- Scaffolding packages in a monorepo -> Jump to "Decision Trees: Monorepo Scaffolding"
|-- Sharing CI/CD templates across repos -> Jump to "Decision Trees: CI/CD Template Sharing"
|-- Auditing repo consistency against templates -> Start at "Core Workflow: Phase 2"
|-- Migrating existing repos to template-based scaffolding -> Start at "Core Workflow: Phase 3"
```

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
```


## Decision Trees

### Decision Tree 1: Template Engine Selection

```
Should we use GitHub template repos? (simplest option)
|
|-- YES -> GitHub template repos (free, integrated, zero tooling)
|   |-- You only need "click Use this template" experience
|   |-- Downstream repos are independent after creation
|   |-- PROS: No tooling to maintain. No learning curve. Native GitHub.
|   |-- CONS: No post-creation updates. No template inheritance. Static snapshot.
|   |-- VERDICT: Best for small orgs (<10 repos) or first template experiment.
|
|-- NO (need more power) -> Does your primary language have a strong template tool?
|   |
|   |-- Python -> Cookiecutter (most mature, Jinja2 templates, hooks)
|   |   |-- PROS: Rich ecosystem of community templates. Pre/post-generation hooks.
|   |   |-- CONS: Only Python. No built-in updates. Requires pip install.
|   |   |-- VERDICT: Best for Python-heavy orgs with moderate complexity needs.
|   |
|   |-- Python (modern) -> Copier (template updates built-in, YAML config)
|   |   |-- PROS: Supports template updates. Clean YAML config. Modern API.
|   |   |-- CONS: Smaller ecosystem than cookiecutter. Python-only.
|   |   |-- VERDICT: Best for Python orgs that need downstream sync.
|   |
|   |-- JavaScript/TypeScript -> Degit (fast, no git history, just extract)
|   |   |-- PROS: Very fast. Clean extraction (no .git). Works with any public repo.
|   |   |-- CONS: No templating variables. Simple copy only.
|   |   |-- VERDICT: Best as a building block in a custom CLI, not standalone.
|   |
|   |-- Polyglot org -> Custom CLI (most flexible, most maintenance)
|   |   |-- Build a thin CLI that wraps git clone + string replacement + npm/pip install
|   |   |-- PROS: Works with any language. Full control. Can enforce org policies.
|   |   |-- CONS: YOU must maintain it. Becomes "template-as-product" if overbuilt.
|   |   |-- VERDICT: Best for large polyglot orgs (50+ repos) with dedicated platform team.
|   |
|   |-- Node.js ecosystem specifically -> Yeoman (generator framework)
|   |   |-- PROS: Rich generator ecosystem. Composable generators.
|   |   |-- CONS: Heavy. Most generators are abandoned. Slow startup.
|   |   |-- VERDICT: Legacy choice. Prefer degit + custom CLI for new projects.
```

### Decision Tree 2: What Goes in the Template?

```
For a NEW repo created from this template, what must be present on first commit?
|
|-- NON-NEGOTIABLE (every template, every language, every team):
|   |-- CI/CD pipeline stub -> Must pass green on empty repo (hello world test)
|   |   |-- GitHub: .github/workflows/ci.yml with lint + test + build jobs
|   |   |-- Provides: CI status badge in README, confidence that pipeline works
|   |-- Security policy -> SECURITY.md with reporting process
|   |-- Code owners -> CODEOWNERS with at least one team or individual
|   |-- Gitignore -> .gitignore appropriate for language/framework
|   |-- License -> LICENSE file (org standard, typically MIT or Apache 2.0)
|   |-- README template -> Project name, description, setup, deploy, team, badges
|   |-- Dependency manifest -> package.json, requirements.txt, go.mod (with placeholder)
|
|-- STRONGLY RECOMMENDED (include unless you have a specific reason not to):
|   |-- Linter config -> eslint, ruff, golangci-lint config with org standards
|   |-- Formatter config -> .prettierrc, pyproject.toml [tool.black], gofmt
|   |-- Type checker config -> tsconfig.json (strict), pyproject.toml [tool.mypy]
|   |-- Test framework config -> jest config, pytest.ini, Go test setup
|   |-- Commitlint config -> commitlint.config.js or similar
|   |-- Contributing guide -> CONTRIBUTING.md with PR process, local setup
|   |-- VS Code settings -> .vscode/settings.json (if org standardizes on VS Code)
|
|-- OPTIONAL (include if applicable):
|   |-- Docker setup -> Dockerfile + .dockerignore + docker-compose.yml
|   |-- Deployment config -> infrastructure/ or deploy/ directory stub
|   |-- API documentation -> OpenAPI spec stub or Swagger config
|   |-- Environment config -> .env.example with documented variables
|   |-- Dependency update config -> renovate.json or dependabot.yml
|   |-- Git hooks -> .githooks/ with pre-commit, commit-msg examples
|
|-- ANTI-PATTERNS to avoid in templates:
|   |-- Example business logic (users WILL deploy it to production)
|   |-- Hardcoded team names or email addresses
|   |-- Outdated dependencies (test template creation weekly)
|   |-- Overly opinionated project structure (let teams own their src/ layout)
|   |-- Too many files ("paralysis by choice" — a 50-file template is a bad template)
```

### Decision Tree 3: Template Inheritance

```
What level of template inheritance does your org need?
|
|-- LEVEL 0: Single Flat Template (1 template = 1 repo type)
|   |-- Pattern: One template repo per language/framework
|   |-- Example: template-python-service, template-react-app, template-go-cli
|   |-- PROS: Simple. No inheritance to manage. Easy to understand.
|   |-- CONS: Duplication across templates (CI workflow copy-pasted 6 times).
|   |       Fixing a CI bug means updating 6 templates.
|   |-- VERDICT: Good for <20 repos, <3 languages.
|   |
|   -> "CI change needs updating in 6 templates" -> You need Level 1
|
|-- LEVEL 1: Base + Language (2-layer inheritance)
|   |-- Pattern: Base template (CI, security, CODEOWNERS) + language-specific templates
|   |-- Mechanism: GitHub template repos with manual composition OR cookiecutter with includes
|   |-- Example: template-base -> template-ts, template-py, template-go
|   |-- PROS: CI/single source of truth. Language-specific configs isolate nicely.
|   |-- CONS: Still some duplication within language (React vs Next.js configs differ).
|   |-- VERDICT: Good for 20-100 repos, 3-6 languages.
|   |
|   -> "React and Next.js configs keep diverging" -> You need Level 2
|
|-- LEVEL 2: Base + Language + Framework (3-layer)
|   |-- Pattern: Base -> Language -> Framework -> generated repo
|   |-- Mechanism: Copier (supports updates), custom CLI with template overlay
|   |-- Example: base -> ts -> react OR base -> ts -> nextjs OR base -> py -> fastapi
|   |-- PROS: Fine-grained. Framework-specific configs isolated. No duplication.
|   |-- CONS: More complex to manage. Need tooling that supports multi-layer composition.
|   |-- VERDICT: Good for 100-500 repos, multiple frameworks per language.
|   |
|   -> "Team A wants different lint rules than Team B with same framework" -> Level 3
|
|-- LEVEL 3: Base + Language + Framework + Team (4-layer)
|   |-- Pattern: Full hierarchy with team-level overrides
|   |-- Mechanism: Custom CLI with merge strategy (team overlay wins, but never overrides security)
|   |-- PROS: Maximum flexibility. Each team gets exactly what they need.
|   |-- CONS: Risk of team-locked configs. Governance needed to prevent fragmentation.
|   |-- VERDICT: Good for 500+ repos, large org with many autonomous teams.
|   |-- GOLDEN RULE: Team overrides must NOT weaken org-level policies.
|   |   |-- Allowed: team-specific test setup, preferred libraries, local dev scripts
|   |   |-- NOT allowed: disabling required CI checks, removing security scanning, weaker linter rules
```

### Decision Tree 4: Downstream Sync Strategy

```
Template has been updated. How do downstream repos get the changes?
|
|-- How many downstream repos? <=10 -> MANUAL (simple, low overhead)
|   |-- Process: Create checklist. For each repo: create branch, apply template diff, PR, merge.
|   |-- Time: ~15 min per repo. For 10 repos: ~2.5 hours per template update.
|   |-- PROS: Human review catches issues. No automation to maintain.
|   |-- CONS: Does not scale. Human error risk. Repos get forgotten.
|
|-- How many downstream repos? 10-100 -> AUTOMATED PR (scripted, PR-based)
|   |-- Process: Script clones each downstream repo, applies template diff, opens PR.
|   |-- Tool: gh CLI + diff-apply script. Or dedicated tool:probot-settings, repo-sync. Copier update.
|   |-- PROS: Scales to 100 repos. Each PR gets human review. Audit trail.
|   |-- CONS: PR fatigue if too many updates. Teams may ignore template PRs.
|   |-- MITIGATION: Group template changes. Monthly sync window. Auto-merge for non-controversial changes.
|
|-- How many downstream repos? 100+ -> DRIFT DETECTION + SELECTIVE SYNC
|   |-- Process: Do not sync proactively. Instead, CI in each downstream repo checks:
|   |   |-- "Does my CI workflow match the base template?"
|   |   |-- "Is my SECURITY.md current?"
|   |   |-- "Are my linter rules at least as strict as the org standard?"
|   |-- If drift detected: alert owning team. Give them N days to sync. Escalate if not done.
|   |-- PROS: No PR fatigue. Teams own their repos. Drift is measurable.
|   |-- CONS: Repos can drift far behind. Security drift is a real risk.
|   |-- COMPLIANCE: Security-critical files (CI security checks) should auto-sync, not just detect.
|
|-- SPECIAL CASE: Security-critical template updates
|   |-- Process: EMERGENCY auto-sync. Override normal process.
|   |-- Example: Security scanning step added to CI template -> sync to ALL repos within 24 hours.
|   |-- Governance: Pre-approved by security team. EXECUTIVE override available.
```

### Decision Tree 5: Monorepo Package Scaffolding

```
Should we use monorepo-level scaffolding tools or repo-level templates?
|
|-- We use Nx -> nx generate
|   |-- Command: nx generate @nx/js:library my-lib
|   |-- Config: nx.json generators section for defaults
|   |-- Custom: create local generators in tools/generators/
|   |-- PROS: Tightly integrated. Understands project graph.
|   |-- CONS: Nx-specific. Cannot reuse for non-Nx repos.
|
|-- We use Turborepo -> turbo gen
|   |-- Command: turbo gen workspace --name my-package
|   |-- Config: turbo.json with generator configs
|   |-- Custom: turbo/generators/ directory with plop.js templates
|   |-- PROS: Turborepo-native. Simple plop.js integration.
|   |-- CONS: Less feature-rich than Nx generators.
|
|-- We use neither (custom monorepo) -> plop.js
|   |-- Command: plop package
|   |-- Config: plopfile.js with custom prompts and actions
|   |-- PROS: Framework-agnostic. Simple. Works anywhere.
|   |-- CONS: No project graph awareness. Manual integration.
|
|-- We use multiple repos (polyrepo) -> repo-level templates
|   |-- Don't use monorepo tools for cross-repo scaffolding. Use Decision Tree 1 instead.
```

### Decision Tree 6: CI/CD Template Sharing

```
How should CI/CD configurations be shared across repos?
|
|-- We use GitHub Actions -> Reusable workflows (.github/workflows/ in a shared repo)
|   |-- Pattern: workflow_call event. Defined once, referenced by many repos.
|   |-- Example: org/.github/workflows/ci-base.yml -> called by repo/.github/workflows/ci.yml
|   |-- Versioning: Use tags (v1, v2) or commit SHAs. Tags for stability, SHAs for security.
|   |-- PROS: Single source of truth. Fix once, all repos benefit. Versioned.
|   |-- CONS: Debugging across repos is harder. Breaking changes affect everyone.
|   |-- MITIGATION: Deprecate old versions gently. Never break v1. Create v2 in parallel.
|
|-- We use GitLab CI -> CI templates (include: keyword)
|   |-- Pattern: include: 'https://gitlab.com/org/ci-templates/-/raw/main/ci.yml'
|   |-- PROS: Same as reusable workflows. GitLab-native.
|   |-- CONS: Template repo becomes critical infrastructure. Needs high availability.
|
|-- We use CircleCI -> Orbs
|   |-- Pattern: orb published to CircleCI registry
|   |-- Example: org/ci-orb@1.0.0 -> referenced in .circleci/config.yml
|   |-- PROS: Versioned, tested, documented. Rich ecosystem.
|   |-- CONS: Orb development has learning curve. Publishing process adds friction.
|
|-- We use Jenkins or custom CI -> Shared Groovy libraries / shared config repos
|   |-- Pattern: Jenkins Shared Libraries OR git clone config repo in pipeline
|   |-- PROS: Works with any CI. Full control.
|   |-- CONS: More DIY. Harder to version. More maintenance.
|
|-- UNIVERSAL RECOMMENDATION: Regardless of CI system, treat CI templates as PRODUCTS.
|   |-- Version them (semantic versioning)
|   |-- Test them (CI for your CI templates)
|   |-- Document them (what each template does, how to use, migration guides)
|   |-- Deprecate them gracefully (support window, migration path)
|   |-- Monitor them (how many repos using each version? any breaking for anyone?)

## Cross-Skill Coordination

### Consumes From
* **monorepo-manager** — When scaffolding packages inside a monorepo, monorepo-manager provides the workspace configuration and project graph context. Repo scaffolding provides the template content and generator configuration for each package type.
* **ci-cd-builder** — CI/CD templates designed here need ci-cd-builder for pipeline implementation details. Reusable workflows, orbs, and CI templates are designed by ci-cd-builder and consumed as "what goes in the template" by repo-scaffolding.
* **polyrepo-strategy** — The decision to use polyrepo (many independent repos) vs monorepo directly impacts scaffolding architecture. Polyrepo needs repo-level templates; monorepo needs package-level scaffolding. The decision is made by polyrepo-strategy; the implementation is repo-scaffolding.
* **platform-engineer** — The scaffolding CLI might live inside an Internal Developer Platform (IDP). Platform-engineer provides the IDP architecture; repo-scaffolding provides the "create repo" golden path within it.
* **security-engineer** — Security-critical template content (SAST scanning in CI, SECURITY.md, dependency scanning configs) should be designed in coordination with security-engineer.

### Feeds Into
* **ci-cd-builder** — Template CI workflows must be valid, working CI configurations. Repo-scaffolding specifies WHAT goes in the template; ci-cd-builder ensures the CI configs actually work.
* **monorepo-manager** — Package scaffolding generators (nx generate, turbo gen, plop.js) are configured here but consumed by monorepo-manager for workspace integration.
* **platform-engineer** — The scaffolding experience is a golden path in the IDP. The scaffolding CLI becomes a platform capability.
* **backend-developer / frontend-developer / fullstack-developer** — Developers consume templates to create new projects. Their feedback on template quality is the primary signal for template improvement.

### Coordination Protocols
* **Template CI validation:** ci-cd-builder reviews template CI workflows for correctness before deployment.
* **Security gate:** security-engineer must approve security-critical template files (CI security jobs, SECURITY.md).
* **Monorepo alignment:** monorepo-manager ensures scaffolding generators produce valid workspace members.
* **Cross-team feedback loop:** Every 6 months, survey developers: "What frustrates you about repo setup?" Feed into template improvements.

## Proactive Triggers

* **New repo created ->** Check: Was it created from a template? If not, flag: "This repo was not created from a template. Drift risk. Time to first green CI: {time}."
* **CI config change in downstream repo ->** Check: Does the change weaken org-level requirements? If yes, flag: "This CI change removes/weakens an org-level requirement. Justify or revert."
* **Template repo updated ->** Automatically: Create a downstream sync plan. Notify owning teams. Set sync deadline.
* **New language/framework adopted by a team ->** Proactively: Create template for the new stack. Do not wait for teams to ask.
* **Security team publishes new scanning requirement ->** Proactively: Update all templates. Trigger security-critical sync path.
* **Quarterly drift audit ->** Proactively: For each repo, compute template drift score. Publish dashboard. Escalate outliers.
* **Developer onboarding (new hire first week) ->** Proactively: Have new hire create a test repo from template. Measure time-to-CI. If >5 minutes, template needs work.

## What Good Looks Like

* **Time-to-green-CI < 5 minutes:** A developer creates a repo from template, clones locally, runs setup command, pushes — CI is green in <5 minutes. This is the primary metric.
* **One org, one CI pattern:** Every repo's CI workflow follows the same structure. An engineer moving between repos knows exactly where to find CI config, how to add a job, how to debug.
* **Zero "snowflake repos":** Every repo can trace back to a template. If a repo has custom config, it is documented in TEAM_CUSTOMIZATIONS.md with a reason.
* **Drift dashboard is green:** >90% of repos match their template. Drift is measured and visible. Teams know when they diverge.
* **Template updates flow downstream:** When the base CI template gets a security scanning step, all downstream repos get a PR within a week (non-critical) or 24 hours (critical).
* **New language adoption is gated on template availability:** No repo for a new stack without a template. The template is created alongside the first project, not after.
* **Scaffolding is self-service:** Developers create repos without filing tickets. The template handles CI, security, and governance automatically.

## Deliberate Practice

### Exercise 1: Design a Base Template (45 min)
* Take 5 existing repos from your org. Extract the intersection of their CI configs, linter rules, and governance files.
* Design a base template that every repo must have. Justify each file: why is this non-negotiable?
* Create the template locally. Scaffold a test repo. Does CI pass? Time it.
* Grade: Under 5 minutes to green CI = pass. Over 10 minutes = redesign.

### Exercise 2: Map Your Org's Template Hierarchy (30 min)
* List all languages and frameworks in your org.
* Map them to a template inheritance hierarchy (Level 0-3).
* Identify: which level is right for your org size?
* Write down the files at each level. How many files are duplicated across templates? Can you reduce duplication?
* Grade: Zero unnecessary duplication = pass. Same file in 3+ templates = refactor needed.

### Exercise 3: Drift Audit (60 min)
* Select 10 downstream repos. For each, compute a diff against the template they were created from.
* Classify each difference: intentional, unintentional, unknown.
* Write a 1-page summary: what is the drift profile of your org? Where are the risks?
* Identify the top 3 drift risks and propose fixes.
* Grade: All differences classified and documented = pass. "Unknown" > 20% = need deeper investigation.

### Exercise 4: Implement Downstream Sync (90 min)
* Pick an existing template. Make a change to it (add a lint rule, update CI step).
* Implement an automated sync: script that opens PRs to all downstream repos.
* For each PR: does CI pass? Does the change break anything?
* Measure: how long from template change to all PRs open?
* Grade: Sync PRs opened within 1 hour, CI green on all = pass. Breaking CI on any repo = fix template or fix sync script.

### Exercise 5: Template Engine Comparison (45 min)
* Evaluate 3 template engines for your primary language (e.g., cookiecutter vs copier vs custom CLI).
* Write a decision document: pros, cons, recommended choice, migration path.
* Prototype: create the same template in your top 2 choices. Which was faster? Which produced better results?
* Grade: Concrete recommendation with evidence = pass. "It depends" without evidence = redo.

## Gotchas

* **Template Drift as Technical Debt Accumulator:**
  A template updated quarterly accumulates 4-6 months of drift per downstream repo. Each drifted repo needs manual reconciliation. At 15 minutes per drifted file per repo and 20 downstream repos, quarterly sync takes **50 engineer-hours per quarter. Total cost: $15,000-$25,000 in productivity loss per year.** Fix: Automated sync PRs with monthly cadence.

* **The "Just One More Field" Anti-Pattern:**
  Templates with too many prompts (project name, description, team, tech lead, Jira key, Slack channel, PagerDuty service, etc.) cause engineers to abandon templates. When a template asks 12 questions, engineers copy-paste from an existing repo instead. **Total cost: $5,000-$10,000 in lost template ROI — the template exists but nobody uses it.** Fix: Maximum 3-5 prompts. Everything else is organizational default.

* **Broken CI in the Template (The Self-Defeating Pattern):**
  A template with CI that fails on first push trains engineers that "the template is broken, just fix CI locally." Each engineer spends 10-15 minutes debugging template CI on their first push. At 50 new repos/year, that is 8-12 hours of wasted time. But the REAL cost: trust in templates is destroyed. **Total cost: $20,000-$30,000 in trust erosion and rework across the org over 2 years.** Fix: Template CI must be tested weekly. Automated test: scaffold repo, push, verify CI green.

* **Fork-and-Forget Template Proliferation:**
  Team A forks the base template, customizes heavily, and never pulls upstream changes. Team B does the same. Now you have 5 "template" repos that share nothing. Each needs independent maintenance. Security fixes must be applied 5 times. **Total cost: $50,000-$100,000 in duplicated template maintenance over 3 years for a 50-repo org.** Fix: Template inheritance hierarchy. One source of truth per level. Automated downstream sync.

* **Over-Engineering the Template Generator (Template-as-Product):**
  A platform team spends 3 months building a beautiful CLI for repo scaffolding with interactive prompts, dependency graphs, and plugin architecture. Meanwhile, developers create repos by copy-pasting from existing repos because the CLI is not ready. **Total cost: $150,000-$250,000 in platform team salary spent on a tool that ships too late.** Fix: Start with a GitHub template repo. Iterate. Add tooling only when the simple approach hurts.

* **Unversioned CI Templates Breaking Downstream:**
  A CI reusable workflow (GitHub Actions, GitLab include) is updated without versioning. All downstream repos that reference `@main` break simultaneously. Detecting which repos broke and rolling back takes hours of on-call time. **Total cost: $10,000-$20,000 per incident in engineering time and delayed CI across 50+ repos.** Fix: Semantic versioning for CI templates. Deprecate old versions, never break them.

* **Template Content That Ages Poorly:**
  A template includes `"axios": "^0.21.0"` which has known CVEs 6 months later. Every new repo created from the template starts with a vulnerable dependency. Fixing requires: update template + sync all downstream repos + verify no downstream fixed it already. **Total cost: $8,000-$15,000 in security remediation across repos that inherited the vulnerable dep.** Fix: Automated dependency freshness check on template. Weekly `npm audit` / `pip audit` on template. Block template usage if critical CVEs exist.

* **The "We Do Not Need Templates, We Are Small" Fallacy:**
  A 5-person startup decides templates are overhead. 18 months later, they have 15 repos with 7 different CI configurations, 4 different linter setups, and 3 different TypeScript versions. Onboarding a 6th engineer takes a week of "here is how THIS repo works, different from the last one." **Total cost: $15,000-$25,000 in onboarding friction and the productivity tax of inconsistent environments over 2 years.** Fix: Even a 2-person team benefits from one consistent repo template. Start small. Scale.


## Verification

### Verify Template Quality
```bash
# Check if template repo exists and is marked as template
gh repo view org/template-repo --json isTemplate,name,description
```

```bash
# Scaffold a test repo from template
gh repo create test-scaffold-$(date +%s) --template org/template-repo --private --clone
cd test-scaffold-*
npm install  # or pip install -e . or make setup
npm test     # or pytest or make test
# CI must pass on first push
git add . && git commit -m "init: scaffold from template" && git push
# Check: CI workflow triggered. Check: CI workflow passed.
```

### Verify Template Completeness
```bash
# Required files check
for f in .github/workflows/ci.yml SECURITY.md CODEOWNERS .gitignore LICENSE README.md; do
  [ -f "$f" ] && echo "PASS: $f" || echo "FAIL: $f missing"
done
```

### Verify Downstream Sync
```bash
# For each downstream repo, check drift against template
for repo in $(gh repo list org --json name --jq '.[].name' | grep -v template); do
  echo "=== $repo ==="
  diff <(gh api repos/org/template-repo/contents/.github/workflows/ci.yml --jq '.content' | base64 -d) \
       <(gh api repos/org/$repo/contents/.github/workflows/ci.yml --jq '.content' | base64 -d) \
       && echo "SYNCED" || echo "DRIFT DETECTED"
done
```

### Verify Monorepo Scaffolding
```bash
# Test Nx generator
nx generate @org/generators:library test-lib-$(date +%s) --dry-run
# Test plop.js generator
npx plop package test-pkg-$(date +%s)
```

## References

* [Golden Repo Pattern](references/golden-repo-pattern.md) — The canonical template-per-language pattern, including structure decisions, content standards, and governance model for the single-source-of-truth approach.
* [Template Engines](references/template-engines.md) — Comparison matrix of cookiecutter, Copier, degit, Yeoman, GitHub templates, and custom CLIs with selection criteria, migration paths, and real-world adoption examples.
* [Template Contents](references/template-contents.md) — Detailed specification of what goes in each template level: CI/CD workflows, linter configs, TypeScript config, .gitignore, CODEOWNERS, SECURITY.md, CONTRIBUTING.md, README templates, and license files.
* [Template Inheritance](references/template-inheritance.md) — The 4-layer inheritance hierarchy (Base -> Language -> Framework -> Team) with composition strategies, override rules, and anti-patterns at each level.
* [Downstream Sync](references/downstream-sync.md) — Automated PR propagation, drift detection, manual sync procedures, and the security-critical sync path with SLAs for each sync priority level.
* [Anti-Patterns](references/anti-patterns.md) — Catalog of common template and scaffolding failures: fork-and-forget, over-engineering, template-as-product, broken CI templates, too-many-prompts, and the "we are small so we do not need templates" fallacy with real cost data.
* [Monorepo Scaffolding](references/monorepo-scaffolding.md) — Package generation with nx generate, turbo gen, plop.js, and custom generators. Integration with monorepo-manager for workspace configuration and project graph awareness.
* [CI/CD Template Sharing](references/cicd-template-sharing.md) — GitHub reusable workflows, GitLab CI templates, CircleCI orbs, Jenkins shared libraries, and custom CI template patterns. Versioning, testing, and deprecation strategies for CI templates treated as products.

