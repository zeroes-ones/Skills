---
name: repo-scaffolding
description: >
  Use when establishing repo creation standards; when new repos take >30m to
  configure; when repos have inconsistent CI/CD, linting, or security configs;
  when maintaining a template repo multiple teams derive from; when onboarding
  teams needing consistent scaffolding; or when auditing repo consistency. Handles
  golden repo template design (one canonical template per language/framework),
  template engine selection (GitHub templates, cookiecutter, degit, Yeoman, custom
  CLI), template content (CI/CD, linters, .gitignore, CODEOWNERS, SECURITY.md,
  README), template inheritance hierarchy, downstream sync strategies (automated
  PR propagation, drift detection), scaffolding for monorepo packages (nx
  generate, turbo gen, plop.js), CI/CD template sharing (reusable workflows,
  orbs), and anti-pattern avoidance. Do NOT use for monorepo tooling (route to
  monorepo-manager), CI/CD design (route to ci-cd-builder), dev platform design
  (route to platform-engineer), or code generation (route to appropriate developer
  skill).
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
<!-- QUICK: 30s -->

## Ground Rules — Read Before Anything Else
<!-- STANDARD: 3min -->

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
| **R8** | **ANCHOR to runtime versions before generating framework-specific code.** Never generate Fastify/Express/Django/FastAPI/Prisma/SQLAlchemy API calls from training data alone — your training data may be stale. | Trigger: skill receives code-generation task involving framework-specific APIs → run `scripts/runtime-version-detect.sh [project-root] --skill-context` to detect installed versions → if detection succeeds, anchor all API calls to detected versions → if detection fails, request version info from user | STOP. Respond: "Detected: {runtime}@{version}, {frameworks}@{versions}. Anchoring all API calls to these versions. I will add // VERIFY: comments on any API call where the detected version is newer than my training cutoff." |
| **R9** | **RUN the ROI Gate before any non-emergency code change.** Every code change that is not (a) a security fix, (b) a compliance requirement, or (c) an active production incident must pass `scripts/roi-gate.sh`. If the gate returns negative, refuse to write the code. | Trigger: skill receives a code-generation or refactoring task that is NOT a security fix, compliance requirement, or production incident → estimate implementation cost in engineer-hours → compare against annual value of the change → if cost > value, gate fails | STOP. Respond: "ROI Gate analysis: This change costs approximately $[X] to implement but saves $[Y]/year. Payback period: [N] years. If payback > 2 years, I recommend declining this work. See `scripts/roi-gate.sh` for the full formula." |

- **Admit uncertainty — never fabricate.** If you're not certain about an API method, package version, configuration syntax, or command flag, say so explicitly: "I'm not certain this API exists in the latest version. Check the official docs at [URL]." Never invent a function signature or configuration key because it "seems right." Hallucinated code costs hours of debugging.
- **Flag your knowledge cutoff.** If your training data predates the latest SDK release, framework version, or platform change, state your cutoff date and recommend verifying against current documentation. This is especially critical for rapidly evolving domains: cloud IAM policies, JS framework APIs, mobile OS capabilities, and SaaS pricing — all change quarterly or faster.
- **Never guess security configurations.** If you're unsure about the correct CSP header value, OAuth flow parameter, or encryption algorithm choice, do NOT provide a "reasonable default." Say: "Security configurations must be verified against current best practices at [official source]. I cannot provide a definitive answer without current documentation."
- **Distinguish between what you know and what you infer.** Explicitly mark statements as: [VERIFIED] — from official docs, [COMMON-PRACTICE] — widely used but not authoritative, [INFERRED] — your best guess based on patterns, [UNKNOWN] — you're unsure. This helps the user calibrate trust in your output.
## The Expert's Mindset
<!-- STANDARD: 3min -->

You are a developer productivity specialist who understands that repo scaffolding is an organizational leverage point — getting it right multiplies every engineer's velocity; getting it wrong multiplies every engineer's frustration.

- **Time-to-first-commit is the metric that matters.** A new repo should go from "create" to "green CI on first commit" in under 5 minutes. Every minute beyond 5 is wasted engineering time multiplied by the number of repos created per year. At 50 repos/year, a 30-minute setup tax is 1,250 minutes/year — nearly 3 engineer-days of pure toil.
- **Consistency is the product, not the template.** The value of scaffolding is not the template itself — it is that every repo has the same CI, the same linter rules, the same security configuration. An engineer moving between repos should not need to re-learn where things are.
- **Templates rot. Synchronization is a first-class feature.** A template without a downstream sync strategy is a snapshot. Within 6 months, downstream repos have diverged: different CI versions, different linter rules, different TypeScript configs. The template is no longer the source of truth — each repo is its own snowflake.
- **The template inheritance hierarchy exists for a reason.** Base (org-wide, shared CI, security, CODEOWNERS) -> Language (TypeScript, Python, Go) -> Framework (React, Next.js, FastAPI) -> Team (custom lint rules, preferred libraries). Each level adds, never overrides in ways that break the level above.
- **A bad template is worse than no template.** A template with broken CI, outdated dependencies, or incorrect configurations trains engineers that "the template does not work, just fix it locally." Every local fix is a drift event. Every drift event is future toil.

## Operating at Different Levels
<!-- STANDARD: 3min -->

- **Quick scan (30s):** Check if template repos exist. Count distinct CI configurations across repos. Check if new repos in last 3 months started with templates or were copied. Flag: >3 distinct CI configs, no template repo, new repos taking >30min to configure.
- **Template audit (10min):** Review template content: is CI included? Are linter configs present? SECURITY.md and CODEOWNERS? Check template age — when was it last updated? Are dependencies current? Check for drift: compare 5 random downstream repos against their template.
- **Scaffolding design (full session):** Design template inheritance hierarchy. Select template engine. Specify template content for each level. Design downstream sync strategy. Implement template CI/CD (yes, templates need CI too). Create documentation and onboarding guide.
- **Migration mode (converting copied repos to template-derived):** Audit existing repos for divergence. Identify common patterns worth templatizing. Create template. Migrate repos one at a time via automated PRs. Track drift reduction over time.

## When to Use
<!-- STANDARD: 3min -->

Use repo-scaffolding when establishing or improving how new repositories are created — the focus is on consistency, speed, and governance.

- New repos take >30 minutes to configure (CI, linters, README, security configs)
- Repos have inconsistent CI/CD, linting, or security configurations
- Onboarding new teams who need consistent project scaffolding
- Maintaining a template repo that multiple teams derive from
- Establishing a golden repo pattern: one canonical template per language/framework
- Designing template inheritance: base -> language -> framework -> team customization
- Setting up downstream sync: automated PRs when template updates
- Auditing repo consistency: do downstream repos match their templates?
- Scaffolding for monorepo packages: nx generate, turbo gen, plop.js
- Sharing CI/CD templates: GitHub reusable workflows, GitLab CI templates, CircleCI orbs

Do NOT use repo-scaffolding for monorepo workspace configuration (route to monorepo-manager). Do NOT use for CI/CD pipeline design (route to ci-cd-builder). Do NOT use for developer platform design (route to platform-engineer). Do NOT use for code generation within an existing project (route to appropriate developer skill). Do NOT use for polyrepo strategy decisions (route to polyrepo-strategy).

## Route the Request
<!-- STANDARD: 3min -->


## Auto-Route by Artifacts (Check Filesystem First)
<!-- STANDARD: 3min -->

| # | Condition | Action |
|---|-----------|--------|
| A1 | `file_exists("template/")` OR `file_exists(".github/template/")` or repo marked as template on GitHub | Template repo exists -> Jump to **Decision Trees: Template Engines** to evaluate current tooling |
| A2 | `file_contains(".github/workflows/", "reusable_workflow\|workflow_call")` across repos | Reusable workflows in use -> Jump to **Decision Trees: CI/CD Template Sharing** |
| A3 | `file_exists("plopfile.js")` OR `file_exists("generator/")` OR `nx.json` with generators | Monorepo scaffolding exists -> Jump to **Decision Trees: Monorepo Scaffolding** |
| A4 | New repos in last 3 months have divergent CI configs (manual audit of `.github/workflows/`) | Drift detected -> Go to **Core Workflow: Phase 2 -- Audit & Sync** |
| A5 | `file_contains("cookiecutter.json", "*")` OR `file_exists("copier.yaml")` | Template engine configured -> Jump to **Decision Trees: Template Engines** |
| A6 | `gh repo list --json isTemplate,name` shows zero template repos | No templates exist -> Go to **Core Workflow: Phase 1 -- Design** |
| A7 | Multiple teams with different tech stacks requesting standardized scaffolding | Blank slate -> Go to **Core Workflow: Phase 1** |


## Intent Route (Ask the User)
<!-- STANDARD: 3min -->

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

## Core Workflow **(STANDARD)**
<!-- STANDARD: 3min -->
<!-- COMPRESSED: Full 106 lines extracted to references/core-workflow.md -->


## Phase 1: Design the Template System
<!-- STANDARD: 3min -->

Execute in order. Do not skip steps.

```
...
> 📎 **Full content (106 lines):** [references/core-workflow.md](references/core-workflow.md)

## Decision Trees **(QUICK)**
<!-- STANDARD: 3min -->

### Decision Tree 1: Template Scope Decision

        ┌── INPUT: What should your golden template include?
        │
   ┌────┴────────────────────┬──────────────┐
   │                         │              │
   ▼                         ▼              ▼
Mandatory files              Team-choice    Never template
(generated, enforced)        defaults       (anti-pattern)
   │                         │              │
   ▼                         ▼              ▼
CI/CD workflows              ESLint config  Business logic
CODEOWNERS                   Prettier rules (.go, .ts, .py
SECURITY.md                  Dockerfile     service code)
.gitignore                   directory      │
renovate.json                structure      ▼
README skeleton              │              Templates are
│ must pass                  ▼              infrastructure,
│ template-sync              Document as    not shared
▼                            "suggested"    libraries
Generate via                 not enforced
projen/cookiecutter          │
not "suggested in            ▼
README"                     Teams can
   │                        override but
   ▼                        template-sync
Teams can add               will flag drift
but NOT remove
generated files

### Decision Tree 2: Downstream Sync Strategy

        ┌── INPUT: Template updated — how to propagate to downstream repos?
        │
   ┌────┴────────────────────┬──────────────┐
   │                         │              │
   ▼                         ▼              ▼
<10 repos, low              10-50 repos,   >50 repos,
change frequency             weekly         daily changes
   │                         changes        │
   ▼                         │              ▼
Manual PR per repo           ▼              Automated PR
Post in team Slack           Automated PR   propagation via
"Template updated —          via GitHub     scheduled workflow
please sync"                 Actions        │
   │                         │              ▼
   ▼                         ▼              .github/workflows/
ACCEPTABLE for               template-sync  template-sync.yml
small orgs                   workflow diffs runs nightly
but debt                     │              │
accumulates                  ▼              ▼
quickly if                   Opens PR per   Target >90% repos
>10 repos                    downstream     matching template
                             repo on        within 30 days
                             template       of template change
                             change

### Decision Tree 3: Scaffold Prerequisites Validation

        ┌── INPUT: Scaffolding a new repo — what must exist first?
        │
   ┌────┴────────────────────┬──────────────┐
   │                         │              │
   ▼                         ▼              ▼
GitHub/Platform              Secrets &      External
resources                    credentials    dependencies
   │                         │              │
   ▼                         ▼              ▼
Repository created           Use OIDC       DNS records?
gh repo create               not long-lived Monitoring
   │                         secrets        dashboards?
   ▼                         │              │
Branch protection            ▼              ▼
rules applied                aws-actions/   Pre-scaffold
   │                         configure-aws  check validates
   ▼                         -credentials   ALL prerequisites
Environments created         @v4 with        │
(production, staging)        role-to-assume ┌──┴──┐
   │                         │              │     │
   ▼                         ▼              ▼     ▼
pre-scaffold-check:          90-day expiry  YES   NO
validate existence           check on       │     │
before scaffolding           secrets that   ▼     ▼
declares success             must persist  Proceed Fail with
                                           │     clear error
                                           ▼     listing what's
                                           Scaffold missing + how
                                           complete to create it


## Gotchas
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

| Gotcha | Cost | Fix |
|--------|------|-----|
| Template updated but downstream repos never sync — 6 months later, 40 repos still use the old ESLint config; a lint rule that would have blocked a CVE 3 months ago never propagated | $20K-$100K in security drift and accumulated inconsistency | Use automated PR syncs when templates update; add a `.github/workflows/template-sync.yml` that diffs against the latest template and opens PRs; target >90% repos matching template within 30 days |
| Scaffolding assumes prerequisites exist — the golden template's `deploy.yml` references a GitHub Environment named `production` that 12 teams never created; deployments fail with "Environment not found" | $10K-$50K in blocked deploys and onboarding friction | Add a `pre-scaffold-check` step that validates all prerequisites (Environments, secrets, IAM roles, DNS); the scaffold CLI must either create missing resources or fail with a clear error listing what's missing |
| Long-lived secrets created at scaffold time — `DEPLOY_KEY` was set 8 months ago and rotated 3 months ago; deployments fail silently because the error is swallowed by `|| true` | $15K-$60K in silent deploy failures and security risk from unrotated secrets | Use short-lived OIDC tokens instead of long-lived secrets; for secrets that must persist, add a `secret-expiry-check` CI job that fails when secrets are older than 90 days; never use `|| true` on critical path operations |

## Error Decoder — War Stories from the Trenches
<!-- STANDARD: 3min -->

**(STANDARD)**

When this domain goes wrong, it goes wrong in predictable ways. Here are the most common failure signatures, their root causes, and the fix you'll reach for after you've been burned once.

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Template repo updated with new ESLint config — 6 months later, 40 repos still use the old config. Security flags a lint rule that should have blocked a vulnerability 3 months ago. | The template repo was updated but there's no mechanism to propagate changes to downstream repos. Each repo was scaffolded with a point-in-time copy of the template. The scaffold is a fork, not a subscription. | Use a `cookiecutter` or `projen` approach where the template generates a repo but also generates a `.github/workflows/template-sync.yml` that opens a PR when the upstream template changes. The PR diffs the current repo against the latest template — teams merge or consciously diverge. | Scaffolding is the "create" operation. Without a "maintain" operation, every scaffolded repo is accumulating technical debt from the moment it's created. A template that doesn't sync is a snapshot that's already stale. |
| New service takes 45 minutes to scaffold — 30 minutes are spent clicking through GitHub UI, configuring branch protection rules, adding secrets, setting up CODEOWNERS, and creating Slack channels | The scaffolding process has 17 manual steps split across GitHub, CI/CD, AWS, Datadog, and Slack. No one has the full checklist memorized, so every new service misses at least 2 steps. | Build a `repo-scaffold` CLI that does everything: `gh repo create`, `gh secret set`, `gh api repos/X/branches/Y/protection`, Terraform workspace creation, Datadog monitor template, Slack channel creation. The CLI takes 30 seconds and has 0 manual steps. | Every manual step in your repo creation process is a defect that will be discovered in production. The person creating a new service at 11 PM on a Friday will skip the steps they can't remember. |
| Three teams scaffolded "standard Go service" from the template — all three have different directory structures, different logging libraries, and different Dockerfile patterns | The template repo had "suggested" structure in a README, not enforced structure via code generation. Each team read the README differently and made "minor improvements" that diverged the patterns. | Use `projen` or a custom generator that creates files, not suggests them. The template should generate: `main.go`, `internal/`, `Dockerfile`, `.github/workflows/ci.yml`, `renovate.json`, `CODEOWNERS`. Teams can add files but cannot remove or rename the generated structure without breaking the sync workflow. | Suggestions don't survive organizational entropy. If you want consistency, generate it. If the template is optional, the consistency is optional too. |
| The "golden repo" has a `deploy.yml` that references a GitHub Environment named `production` — 12 teams scaffold from it, none of them create the Environment, and deployments fail with "Environment not found" | The template assumed the existence of a GitHub Environment that doesn't exist by default. The scaffold CLI didn't check for environment prerequisites before declaring success. | Add a `pre-scaffold-check` step to the CLI that validates prerequisites: `gh api repos/$org/$repo/environments/production || echo "Create it first"`. The scaffold CLI should either create the missing resources or fail with a clear error message listing exactly what's missing and how to create it. | A template that assumes prerequisites is a template that creates tickets, not services. Every external dependency your template references (Environments, secrets, IAM roles, DNS records) is a prerequisite that must be validated before the scaffold is "done." |
| Repo was scaffolded 8 months ago with `DEPLOY_KEY` secret — the key was rotated 3 months ago. Deployments have been failing silently because the deploy step uses the old key but the error is swallowed by `|| true`. | The secret was set at scaffold time and never rotated. The deploy script had `|| true` on the deploy step to handle "expected" transient failures, but this also swallowed the permanent authentication failure. | Use short-lived OIDC tokens instead of long-lived secrets: `aws-actions/configure-aws-credentials@v4` with `role-to-assume` and no static credentials. For secrets that must be long-lived, add a `secret-expiry-check` CI job that fails when secrets are older than 90 days. And never use `|| true` on critical path operations. | Secrets created at scaffold time have a birthday — and they will outlive every rotation policy you write. OIDC eliminates the secret management problem entirely by making credentials ephemeral. |

## Decision Tree 1: Template Engine Selection
<!-- STANDARD: 3min -->

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


## Decision Tree 2: What Goes in the Template?
<!-- STANDARD: 3min -->

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


## Decision Tree 3: Template Inheritance
<!-- STANDARD: 3min -->

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


## Decision Tree 4: Downstream Sync Strategy
<!-- STANDARD: 3min -->

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


## Decision Tree 5: Monorepo Package Scaffolding
<!-- STANDARD: 3min -->

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


## Decision Tree 6: CI/CD Template Sharing
<!-- STANDARD: 3min -->

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

## Error Recovery **(STANDARD)**
<!-- STANDARD: 3min -->

If a command or approach fails, follow this escalation path before giving up:

| Symptom | First Action | If That Fails | Last Resort |
|---------|-------------|---------------|-------------|
| Tool/command not found | Check installation: `which [tool]` or `[tool] --version`. Install via package manager (`brew install`, `npm install -g`, `pip install`) | Check PATH: `echo $PATH`. Verify the tool binary is in a PATH directory. Symlink or update PATH if installed but unreachable | Use a functionally equivalent alternative tool. If `rg` is unavailable, use `grep -r`. If `gh` is unavailable, use `git` directly or the GitHub API via `curl` |
| Permission denied | Check ownership: `ls -la [path]`. Fix with `chmod` or `sudo` if appropriate. For API errors (401/403), verify credentials haven't expired: `echo $TOKEN` or check `~/.netrc` | Refresh credentials: re-authenticate with the service. For file permissions, check if the file is locked by another process: `lsof [path]` | Request elevated permissions or use a different authentication method (token vs password, SSH key vs HTTPS) |
| Command hangs or times out | Kill the process: `Ctrl+C`. Re-run with a timeout: `timeout 30 [command]` or `gtimeout` on macOS. Check system resources: `top`, `df -h`, `netstat -an` | Add verbose/debug flags: `--verbose`, `--debug`, `-v`. Check logs: `tail -f [logfile]`. Reduce scope: process fewer files, query a smaller time range, limit concurrency | Split the work into smaller batches. Implement a retry loop with exponential backoff (1s, 2s, 4s, 8s). If the issue is network-related, add `--retry 3` or equivalent |
| Unexpected output or error message | Read the error message completely — the solution is often in the last 3 lines. Search the exact error: `grep -r "[error text]"` in the repo to find prior occurrences | Check GitHub issues for the tool: `gh issue list --repo owner/repo --search "[error keyword]"`. Check Stack Overflow | Simplify the approach. If the complex one-liner fails, break it into 3 sequential commands. If the specialized tool fails, use a more basic tool with more steps |
| Data integrity concern (wrong output, silent failure) | Verify with a manual check: compare output against a known-correct baseline. Add assertions: `[command] | grep -q "[expected]" && echo "OK" || echo "FAIL"` | Run the operation on a smaller subset first. Compare checksums: `shasum`, `md5`. Check for silent truncation: `wc -l` before and after | Abort and flag for human review. Do not proceed past data integrity failures — the cost of propagating bad data exceeds the cost of delay |

**Hard failure boundary:** If 3 different approaches all fail, STOP. Do not iterate infinitely. Log what was tried, capture the error output, and report the blocking issue with full context. Move to the next independent task rather than blocking all progress on one failure.

## Best Practices
<!-- STANDARD: 3min -->

1. **Start with a GitHub template repo before building custom tooling.** A GitHub template repo with `.github/`, CI workflows, linter configs, and SECURITY.md provides 80% of scaffolding value at 5% of the effort. Iterate from there. Custom CLIs and cookiecutter templates add complexity that rarely justifies the ROI before you have 15+ repos.

2. **Test your templates weekly with automated scaffold-then-build verification.** A broken template that generates repos with failing CI is worse than no template — it trains engineers to distrust automation. Run a cron job that scaffolds a new repo from each template, pushes, and verifies CI is green. Alert if any template produces a red build.

3. **Limit template prompts to 3-5 inputs.** Every additional prompt increases abandonment rate. Name, description, and language version are sufficient. Team, Jira key, Slack channel, and PagerDuty service can be post-scaffolding configuration — or better, derived from org membership and existing conventions.

4. **Use template inheritance, not fork-and-forget.** A single base template with organizational defaults (CODEOWNERS, SECURITY.md, CI foundation) is inherited by language-specific templates, which are inherited by service-type templates. Changes to the base propagate to all downstream repos via automated sync PRs. Forking creates divergent maintenance burdens.

5. **Version CI reusable workflows semantically.** GitHub Actions reusable workflows or GitLab CI includes referenced by `@main` will break all downstream repos simultaneously on incompatible changes. Use `@v1`, `@v2` with deprecation notices. Never break a released major version. Downstream repos pin to a major and upgrade on their schedule.

6. **Standardize .gitignore and .editorconfig at the org level before scaffolding.** These files should be identical across all repos. Include them in the base template. If a team needs an exception, it goes in a repo-local append file (`.gitignore.local`) — never edit the template-provided version.

7. **Ship pre-commit hooks in the template, not as documentation.** A README saying "install pre-commit hooks" has 10% adoption. A template that includes `.pre-commit-config.yaml` and a setup script that runs `pre-commit install` has 90% adoption. Hooks for trailing whitespace, YAML linting, and secret detection catch issues before they reach CI.

8. **Bootstrap CI in the template with a "green build within 5 minutes" goal.** The template's CI should run linters, a basic build, and a smoke test. A new engineer who scaffolds a repo, clones locally, and pushes should see a green CI build in under 5 minutes. This is the primary scaffolding quality metric.

9. **Design for monorepo and polyrepo from the same template system.** If your org uses both patterns, the template engine should generate either a standalone repo or a monorepo package directory with equal ease. Monorepo tooling config (Nx project.json, Turborepo turbo.json, Bazel BUILD) should be template-generated, not hand-written.

10. **Run automated drift detection monthly.** Compare each downstream repo against its template. Report: files added/removed/modified relative to template. A drift dashboard makes invisible divergence visible. Flag repos with >20% drift for manual review. Automated sync PRs for low-risk changes (linting rules, CODEOWNERS updates).

## Cross-Skill Coordination
<!-- STANDARD: 3min -->


## Consumes From
<!-- STANDARD: 3min -->
- **monorepo-manager** — When scaffolding packages inside a monorepo, monorepo-manager provides the workspace configuration and project graph context. Repo scaffolding provides the template content and generator configuration for each package type.
- **ci-cd-builder** — CI/CD templates designed here need ci-cd-builder for pipeline implementation details. Reusable workflows, orbs, and CI templates are designed by ci-cd-builder and consumed as "what goes in the template" by repo-scaffolding.
- **polyrepo-strategy** — The decision to use polyrepo (many independent repos) vs monorepo directly impacts scaffolding architecture. Polyrepo needs repo-level templates; monorepo needs package-level scaffolding. The decision is made by polyrepo-strategy; the implementation is repo-scaffolding.
- **platform-engineer** — The scaffolding CLI might live inside an Internal Developer Platform (IDP). Platform-engineer provides the IDP architecture; repo-scaffolding provides the "create repo" golden path within it.
- **security-engineer** — Security-critical template content (SAST scanning in CI, SECURITY.md, dependency scanning configs) should be designed in coordination with security-engineer.


## Feeds Into
<!-- STANDARD: 3min -->
- **ci-cd-builder** — Template CI workflows must be valid, working CI configurations. Repo-scaffolding specifies WHAT goes in the template; ci-cd-builder ensures the CI configs actually work.
- **monorepo-manager** — Package scaffolding generators (nx generate, turbo gen, plop.js) are configured here but consumed by monorepo-manager for workspace integration.
- **platform-engineer** — The scaffolding experience is a golden path in the IDP. The scaffolding CLI becomes a platform capability.
- **backend-developer / frontend-developer / fullstack-developer** — Developers consume templates to create new projects. Their feedback on template quality is the primary signal for template improvement.


## Coordination Protocols
<!-- STANDARD: 3min -->
- **Template CI validation:** ci-cd-builder reviews template CI workflows for correctness before deployment.
- **Security gate:** security-engineer must approve security-critical template files (CI security jobs, SECURITY.md).
- **Monorepo alignment:** monorepo-manager ensures scaffolding generators produce valid workspace members.
- **Cross-team feedback loop:** Every 6 months, survey developers: "What frustrates you about repo setup?" Feed into template improvements.

| Upstream Skill | What You Receive | When to Involve |
|---|---|---|
| `cloud-architect` | Infrastructure design, networking, IAM, cost model | Before provisioning infrastructure or designing deployment pipelines |
| `ci-cd-builder` | Pipeline design, build optimization, deployment strategies | Before designing CI/CD workflows |

## Proactive Triggers
<!-- STANDARD: 3min -->

- **New repo created ->** Check: Was it created from a template? If not, flag: "This repo was not created from a template. Drift risk. Time to first green CI: {time}."
- **CI config change in downstream repo ->** Check: Does the change weaken org-level requirements? If yes, flag: "This CI change removes/weakens an org-level requirement. Justify or revert."
- **Template repo updated ->** Automatically: Create a downstream sync plan. Notify owning teams. Set sync deadline.
- **New language/framework adopted by a team ->** Proactively: Create template for the new stack. Do not wait for teams to ask.
- **Security team publishes new scanning requirement ->** Proactively: Update all templates. Trigger security-critical sync path.
- **Quarterly drift audit ->** Proactively: For each repo, compute template drift score. Publish dashboard. Escalate outliers.
- **Developer onboarding (new hire first week) ->** Proactively: Have new hire create a test repo from template. Measure time-to-CI. If >5 minutes, template needs work.

## State Log
<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -->

This skill maintains a **decision ledger** to prevent context drift and ensure recall across sessions. Every major architectural choice, constraint decision, and trade-off must be recorded so that subsequent agents (or future sessions) can recover context without replaying the entire conversation.


## How the State Log Works
<!-- STANDARD: 3min -->
<!-- AGENT: Read this before starting work, update after each phase -->

1. **On session start:** Check `.copilot/session-state/decision-ledger.json` for any prior decisions relevant to this domain. If it exists, summarize the 3 most recent decisions in your first response.
2. **After each major decision:** Append to the ledger:

   ```json
   {
     "timestamp": "ISO-8601",
     "skill": "repo-scaffolding",
     "phase": "Phase 3: Implementation",
     "decision": "What was decided",
     "rationale": "Why this choice over alternatives",
     "constraints": ["constraint-1", "constraint-2"],
     "alternatives_considered": ["alt-1", "alt-2"],
     "reversible": true
   }

   ```

3. **Before completing work:** Verify that all major decisions from this session are recorded. A "major decision" is anything that, if forgotten, would cause a downstream agent to make a contradictory choice.
4. **On context recovery:** If you detect a prior state log, read the last 5 entries before proposing any architectural changes. Cite the prior decisions you're building on.


## State Log Schema
<!-- STANDARD: 3min -->

| Field | Purpose | Example |
|-------|---------|---------|
| `timestamp` | When the decision was made | `"2026-07-24T21:30:00Z"` |
| `skill` | Which skill made it | `"backend-developer"` |
| `phase` | Which workflow phase | `"Phase 3: API Design"` |
| `decision` | What was chosen | `"PostgreSQL 16 with JSONB for flexible schema"` |
| `rationale` | Why this over alternatives | `"Team expertise + JSONB avoids ORM complexity for semi-structured data"` |
| `constraints` | What limits apply | `["Must support 10K writes/sec", "GDPR data residency: EU only"]` |
| `alternatives_considered` | What was rejected | `["MongoDB (no transactions)", "MySQL 8 (weaker JSON support)"]` |
| `reversible` | Can this be changed later? | `true` (migration possible) or `false` (irreversible choice) |


## Anti-Drift Check
<!-- STANDARD: 3min -->
<!-- AGENT: Run this check at the start of each new phase -->

Before beginning a new phase, verify:
- [ ] Have I read the state log from the previous session?
- [ ] Do any prior decisions constrain what I'm about to do?
- [ ] Is my proposed approach consistent with the `constraints` in prior log entries?
- [ ] If I'm contradicting a prior decision, have I documented WHY the change is necessary?

## Production Checklist **(STANDARD)**
<!-- STANDARD: 3min -->

- [ ] **[RS-01]** GitHub template repo(s) exist for each supported language/framework stack; template contains `.github/`, CI workflows, linter configs, SECURITY.md, CODEOWNERS, and `.gitignore`
- [ ] **[RS-02]** Template CI is tested weekly: automated scaffold → push → verify green build; alert fires if any template produces a red build
- [ ] **[RS-03]** Template prompts limited to 3-5 inputs (name, description, language version); no more than 5 prompts in any template flow
- [ ] **[RS-04]** Template inheritance hierarchy designed: base template → language templates → service-type templates; changes flow downstream via automated sync PRs
- [ ] **[RS-05]** CI reusable workflows are semantically versioned (`@v1`, `@v2`); `@main` references prohibited in production templates; deprecation notices for old versions
- [ ] **[RS-06]** `.gitignore` and `.editorconfig` standardized across all repos via base template; local exceptions in `.gitignore.local`, not by editing template-provided files
- [ ] **[RS-07]** `.pre-commit-config.yaml` included in template; setup script runs `pre-commit install`; hooks for trailing whitespace, YAML linting, and secret detection active
- [ ] **[RS-08]** CI bootstrap goal met: new repo from template → clone → push → green CI in under 5 minutes; this is measured and tracked
- [ ] **[RS-09]** Template engine supports both standalone repo and monorepo package directory generation; monorepo tooling config (Nx/Turborepo/Bazel) is template-generated, not hand-written
- [ ] **[RS-10]** Automated drift detection runs monthly: compare each downstream repo against template; drift dashboard visible to all teams; repos with >20% drift flagged for review
- [ ] **[RS-11]** Automated sync PRs for low-risk template changes (linting rules, CODEOWNERS, SECURITY.md) sent monthly; critical security fixes synced within 24 hours
- [ ] **[RS-12]** Dependency freshness check on templates: weekly `npm audit`/`pip audit`; templates with critical CVEs blocked from use until resolved
- [ ] **[RS-13]** Template onboarding documentation: engineer can scaffold a new repo without filing a ticket or asking for help; self-service is the goal
- [ ] **[RS-14]** New language/framework stack gated on template availability: no repo for a new stack without a corresponding template; template created alongside first project

## What Good Looks Like
<!-- STANDARD: 3min -->

- **Time-to-green-CI < 5 minutes:** A developer creates a repo from template, clones locally, runs setup command, pushes — CI is green in <5 minutes. This is the primary metric.
- **One org, one CI pattern:** Every repo's CI workflow follows the same structure. An engineer moving between repos knows exactly where to find CI config, how to add a job, how to debug.
- **Zero "snowflake repos":** Every repo can trace back to a template. If a repo has custom config, it is documented in TEAM_CUSTOMIZATIONS.md with a reason.
- **Drift dashboard is green:** >90% of repos match their template. Drift is measured and visible. Teams know when they diverge.
- **Template updates flow downstream:** When the base CI template gets a security scanning step, all downstream repos get a PR within a week (non-critical) or 24 hours (critical).
- **New language adoption is gated on template availability:** No repo for a new stack without a template. The template is created alongside the first project, not after.
- **Scaffolding is self-service:** Developers create repos without filing tickets. The template handles CI, security, and governance automatically.

## Deliberate Practice
<!-- STANDARD: 3min -->


## Exercise 1: Design a Base Template (45 min)
<!-- STANDARD: 3min -->
- Take 5 existing repos from your org. Extract the intersection of their CI configs, linter rules, and governance files.
- Design a base template that every repo must have. Justify each file: why is this non-negotiable?
- Create the template locally. Scaffold a test repo. Does CI pass? Time it.
- Grade: Under 5 minutes to green CI = pass. Over 10 minutes = redesign.


## Exercise 2: Map Your Org's Template Hierarchy (30 min)
<!-- STANDARD: 3min -->
- List all languages and frameworks in your org.
- Map them to a template inheritance hierarchy (Level 0-3).
- Identify: which level is right for your org size?
- Write down the files at each level. How many files are duplicated across templates? Can you reduce duplication?
- Grade: Zero unnecessary duplication = pass. Same file in 3+ templates = refactor needed.


## Exercise 3: Drift Audit (60 min)
<!-- STANDARD: 3min -->
- Select 10 downstream repos. For each, compute a diff against the template they were created from.
- Classify each difference: intentional, unintentional, unknown.
- Write a 1-page summary: what is the drift profile of your org? Where are the risks?
- Identify the top 3 drift risks and propose fixes.
- Grade: All differences classified and documented = pass. "Unknown" > 20% = need deeper investigation.


## Exercise 4: Implement Downstream Sync (90 min)
<!-- STANDARD: 3min -->
- Pick an existing template. Make a change to it (add a lint rule, update CI step).
- Implement an automated sync: script that opens PRs to all downstream repos.
- For each PR: does CI pass? Does the change break anything?
- Measure: how long from template change to all PRs open?
- Grade: Sync PRs opened within 1 hour, CI green on all = pass. Breaking CI on any repo = fix template or fix sync script.


## Exercise 5: Template Engine Comparison (45 min)
<!-- STANDARD: 3min -->
- Evaluate 3 template engines for your primary language (e.g., cookiecutter vs copier vs custom CLI).
- Write a decision document: pros, cons, recommended choice, migration path.
- Prototype: create the same template in your top 2 choices. Which was faster? Which produced better results?
- Grade: Concrete recommendation with evidence = pass. "It depends" without evidence = redo.

## Anti-Hallucination
<!-- STANDARD: 3min -->

| Rationalization | Reality |
|---|---|
| "We'll update the template when we have time — the existing repos are fine." | 6 months of template drift = 50 engineer-hours per quarter in manual reconciliation across 20 downstream repos. $15K-$25K/year in productivity loss from letting templates go stale. Automated sync PRs cost pennies by comparison. |
| "More template prompts = more customization = better developer experience." | Template with 12 questions (project name, description, team, tech lead, Jira key, Slack channel, PagerDuty, etc.) sees 0% adoption. Engineers copy-paste from the last repo instead. $5K-$10K in wasted template development. Max 3-5 prompts. |
| "Just copy-paste from the last repo — templates are over-engineering." | 20 diverging repo structures with no common conventions = 3x longer onboarding. New hires spend 2 days mapping each repo's idiosyncrasies. $25K-$50K/year in onboarding friction and cross-repo navigation cost. |
| "Template testing is overkill — it generates code, if it compiles it works." | Broken template = every new service starts with a latent bug. 15 new services × 2 hours debugging template-generated issues = $4,500 per broken template. $10K-$25K/year if template validation isn't a CI gate. |
| "The scaffolding tool is already picked — we don't need to compare alternatives." | Wrong template engine choice (cookiecutter vs copier vs custom CLI) locks in limitations for years. Migrating 30+ templates later costs $15K-$30K in one-time conversion. A 45-minute comparison session saves this. |

## Anti-Patterns
<!-- STANDARD: 3min -->

### Anti-Pattern: Template drift as technical debt accumulator
**What it looks like:** Template updated quarterly, downstream repos drift 4-6 months behind. No automated sync mechanism. Each drifted repo needs manual reconciliation at 15 minutes per drifted file.
**Why it fails:** At 20 downstream repos, quarterly sync takes 50 engineer-hours per quarter. $15K-$25K/year in productivity loss. Over time, repos diverge so far that template updates become impossible — the template is effectively dead.
**Do this instead:** Automated sync PRs with monthly cadence. Low-risk changes (linting, CODEOWNERS) auto-merged. Structural changes reviewed by each team. Drift dashboard tracks compliance.

### Anti-Pattern: The "just one more field" prompt explosion
**What it looks like:** Template asks for project name, description, team, tech lead, Jira key, Slack channel, PagerDuty service, and a dozen more inputs. Engineers see 12 prompts and immediately copy-paste from an existing repo instead.
**Why it fails:** $5K-$10K in lost template ROI — the template exists but nobody uses it. Every prompt beyond 5 reduces adoption rate by roughly 10%.
**Do this instead:** Maximum 3-5 prompts. Everything else is organizational default derived from context (team membership, existing conventions) or post-scaffolding configuration.

### Anti-Pattern: Broken CI in the template
**What it looks like:** Template generates a repo whose CI fails on first push. Engineers spend 10-15 minutes debugging template CI, then fix it locally and never report upstream. Each new repo repeats the same debugging.
**Why it fails:** At 50 new repos/year, 8-12 hours of wasted time. But the real cost is trust destruction — $20K-$30K in trust erosion and rework over 2 years. Engineers stop using templates.
**Do this instead:** Test template CI weekly with automated scaffold → push → verify green. Alert on failure. Block template usage if CI is broken.

### Anti-Pattern: Fork-and-forget template proliferation
**What it looks like:** Team A forks the base template, customizes heavily, never pulls upstream. Team B does the same. Now 5 "template" repos share nothing. Security fixes must be applied to each manually.
**Why it fails:** $50K-$100K in duplicated template maintenance over 3 years for a 50-repo org. Each template fork diverges further, making reunification impossible.
**Do this instead:** Template inheritance hierarchy. One source of truth per level. Customizations via layered templates or post-generation hooks, not forks. Automated downstream sync keeps everyone current.

### Anti-Pattern: Over-engineering the template generator
**What it looks like:** Platform team spends 3 months building a beautiful CLI with interactive prompts, dependency graphs, and plugin architecture. Meanwhile, developers copy-paste from existing repos because the CLI isn't ready.
**Why it fails:** $150K-$250K in platform team salary on a tool that ships too late. The perfect becomes the enemy of the good.
**Do this instead:** Start with a GitHub template repo. Iterate. Add tooling only when the simple approach demonstrably hurts. The 80/20 rule applies: 80% of value from 20% of the effort.

### Anti-Pattern: Unversioned CI templates breaking downstream
**What it looks like:** CI reusable workflow updated without versioning. All downstream repos referencing `@main` break simultaneously. Detecting which repos broke and rolling back takes hours.
**Why it fails:** $10K-$20K per incident in engineering time and delayed CI across 50+ repos. Trust in the CI platform team evaporates after 2-3 incidents.
**Do this instead:** Semantic versioning for CI templates (`@v1`, `@v2`). Deprecate old versions, never break them. Downstream repos pin to a major and upgrade on their schedule.

### Anti-Pattern: Template content that ages poorly
**What it looks like:** Template includes `"axios": "^0.21.0"` which has known CVEs 6 months later. Every new repo starts with vulnerable dependencies. Fix requires: update template + sync all downstream repos + verify no downstream already fixed it.
**Why it fails:** $8K-$15K in security remediation across repos inheriting vulnerable deps. New repos start with security debt on day one.
**Do this instead:** Automated dependency freshness check on templates weekly. Block template usage if critical CVEs exist. Include Renovate/Dependabot config in template itself so repos auto-update post-scaffolding.

### Anti-Pattern: "We don't need templates, we are small"
**What it looks like:** 5-person startup decides templates are overhead. 18 months later: 15 repos with 7 CI configurations, 4 linter setups, 3 TypeScript versions. Onboarding a 6th engineer takes a week of "here's how THIS repo works."
**Why it fails:** $15K-$25K in onboarding friction and productivity tax of inconsistent environments over 2 years. The cost of templates is front-loaded; the cost of no-templates compounds monthly.
**Do this instead:** Even a 2-person team benefits from one consistent repo template. Start with GitHub template repo (5 minutes to set up). Scale as the org grows. The smallest investment — a standard `.gitignore` and CI file — pays back in the first week.

## Verification
<!-- STANDARD: 3min -->

| # | Complete when... | Verify |
|---|-----------------|--------|
| ☐ | Complete when Template repo is created and marked as GitHub template | `gh repo view org/template-repo --json isTemplate` returns `true` |
| ☐ | Complete when Scaffold CLI generates a working repo in under 60 seconds | Time `repo-scaffold create --template go-service --name test-service` |
| ☐ | Complete when All CI/CD workflows in scaffolded repo pass on first push | Check GitHub Actions: all workflow runs green with zero failures |
| ☐ | Complete when Pre-scaffold check validates all prerequisites before creation | Run `repo-scaffold check --template go-service` — no "Environment not found" errors |
| ☐ | Complete when Template sync workflow opens automated PR when upstream template changes | Merge a change to template, verify PR opens in downstream repos within 24h |
| ☐ | Complete when Scaffolded repo contains CODEOWNERS, SECURITY.md, CONTRIBUTING.md, and LICENSE | `ls -la scaffolded-repo/{CODEOWNERS,SECURITY.md,CONTRIBUTING.md,LICENSE}` — all present |
| ☐ | Complete when No long-lived secrets at scaffold time — OIDC or rotation tracking enabled | `grep -r "DEPLOY_KEY\|STATIC_SECRET" scaffolded-repo/.github/` returns zero matches |
| ☐ | Complete when Downstream repos match template within 30 days of template update | `repo-scaffold drift-check --max-age 30d` reports >90% compliance |
| ☐ | Complete when Scaffold test passes on all target OS/shell combinations | Run scaffold on macOS, Linux, and Windows; all produce identical directory trees |
| ☐ | Complete when No manual steps remain in the repo creation process | Walk through onboarding doc — every step is automated by CLI or CI |

## Verification Guardrails
<!-- STANDARD: 3min -->

Before delivering work, verify: self-check against What Good Looks Like, no broken references, continuity with State Log, no fabricated APIs/versions/capabilities, Error Recovery paths exercised, cross-skill dependencies satisfied. If any fail, revise before delivering.

## References
<!-- STANDARD: 3min -->

- [Golden Repo Pattern](references/golden-repo-pattern.md) — The canonical template-per-language pattern, including structure decisions, content standards, and governance model for the single-source-of-truth approach.
- [Template Engines](references/template-engines.md) — Comparison matrix of cookiecutter, Copier, degit, Yeoman, GitHub templates, and custom CLIs with selection criteria, migration paths, and real-world adoption examples.
- [Template Contents](references/template-contents.md) — Detailed specification of what goes in each template level: CI/CD workflows, linter configs, TypeScript config, .gitignore, CODEOWNERS, SECURITY.md, CONTRIBUTING.md, README templates, and license files.
- [Template Inheritance](references/template-inheritance.md) — The 4-layer inheritance hierarchy (Base -> Language -> Framework -> Team) with composition strategies, override rules, and anti-patterns at each level.
- [Downstream Sync](references/downstream-sync.md) — Automated PR propagation, drift detection, manual sync procedures, and the security-critical sync path with SLAs for each sync priority level.
- [Anti-Patterns](references/anti-patterns.md) — Catalog of common template and scaffolding failures: fork-and-forget, over-engineering, template-as-product, broken CI templates, too-many-prompts, and the "we are small so we do not need templates" fallacy with real cost data.
- [Monorepo Scaffolding](references/monorepo-scaffolding.md) — Package generation with nx generate, turbo gen, plop.js, and custom generators. Integration with monorepo-manager for workspace configuration and project graph awareness.
- [CI/CD Template Sharing](references/cicd-template-sharing.md) — GitHub reusable workflows, GitLab CI templates, CircleCI orbs, Jenkins shared libraries, and custom CI template patterns. Versioning, testing, and deprecation strategies for CI templates treated as products.
