# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Documentation Audit & Strategy

1. **Documentation Inventory** — Catalog all existing docs: repository READMEs, wiki pages, `/docs` directories, API specs (OpenAPI, GraphQL), ADRs, runbooks, onboarding materials, blog posts with technical content, internal Google Docs/Notion pages. For each: audience, freshness (last updated), accuracy (% still correct), discoverability (how do people find it?).
2. **Audience & Needs Mapping** — Identify documentation personas:
   - **New Developer**: setup guide, architecture overview, first contribution walkthrough, coding standards.
   - **Experienced Developer**: API reference, advanced configuration, <!-- DEEP: 10+min -->
debugging guide, performance tuning.
   - **Operator/SRE**: deployment guide, runbooks, monitoring setup, disaster recovery, scaling.
   - **Product/Support**: feature documentation, changelog, known issues, FAQ.
   - **External User** (for public APIs/products): getting started, SDK guides, API reference, tutorials.
   - Map each existing doc to a persona and a user journey stage (discover, learn, build, troubleshoot).
3. **Gap Analysis** — Cross-reference inventory with persona needs. Common gaps: no architecture overview (new developers get lost), no runbooks (operators escalate to developers), API reference exists but no usage examples (developers read source code), docs exist but are undiscoverable (no search, poor IA).
4. **Docs-as-Code Strategy** — Define toolchain:
   - **Source format**: Markdown (with frontmatter for metadata), MDX (Markdown + JSX for interactive docs), AsciiDoc (for complex technical docs).
   - **Static site generator**: Docusaurus (React-based, great for OSS), VitePress (Vue-based, fast, simple), Mintlify (hosted, beautiful, API-first), Nextra (Next.js-based).
   - **Versioning**: docs versioned alongside code releases (Git tags → doc versions). Maintain docs for current + N-1 versions.
   - **CI/CD**: docs built and deployed on merge to main; preview deployments per PR.
   - **Linting**: Vale or textlint for style guide enforcement; markdownlint for formatting.
5. **Deliverable: Documentation Strategy Document** — Inventory, persona map, gap analysis, prioritized backlog of docs to create/update, toolchain decision, IA proposal for doc site.

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): Core Documentation Types

1. **README** — Every repository's landing page. Structure:
   - **Title & Badge Bar**: build status, coverage, version, license, downloads.
   - **One-line description**: what the project does, who it's for.
   - **Quick Start** (the most important section): install, minimal working example, expected output. Must work in under 5 minutes.
   - **Motivation**: why does this exist? What problem does it solve? When should I use it versus alternatives?
   - **Documentation Link**: point to full docs site, not a wall of text here.
   - **Contributing**: link to CONTRIBUTING.md; code of conduct; how to set up dev environment.
   - **License**: SPDX identifier and link to LICENSE file.
2. **API Reference Documentation** —
   - **Source of truth**: OpenAPI 3.x specification (`openapi.yaml` or `openapi.json`). Keep it in the repo; generate docs from it, never write API docs manually.
   - **OpenAPI best practices**: describe every endpoint with `summary` and `description`; add `example` to every request body and response schema; use `$ref` for reusable schemas; tag endpoints by resource; document error responses (400, 401, 403, 404, 429, 500) consistently.
   - **Generated reference**: use Redoc, Swagger UI, or Scalar for rendered API docs.
   - **Supplement with guides**: API reference answers "what endpoints exist?" but not "how do I accomplish X?". Add: authentication guide, rate limiting guide, pagination guide, error handling guide, webhook guide, SDK usage examples.
3. **Architecture Decision Records (ADRs)** — Lightweight documentation for significant technical decisions:
   - **Template**: Title (verb phrase: "Use PostgreSQL as primary database"), Status (proposed, accepted, deprecated, superseded), Context (problem statement, constraints, assumptions), Decision (what we decided and why), Alternatives Considered (each with pros/cons), Consequences (positive, negative, and neutral — what becomes easier/harder).
   - **Storage**: `docs/adr/` directory with sequential numbering: `0001-use-postgresql.md`, `0002-adopt-kubernetes.md`.
   - **When to write an ADR**: choosing a new technology, changing a major architectural pattern, deprecating a system, making a decision with multiple viable options that future developers will question.
   - **Tooling**: `adr-tools` CLI for creating and managing ADRs; `adr-log` for generating an index.
4. **Runbooks** — Operational procedures for predictable, safe incident response:
   - **Template**: Title, Applicability (which systems/services), Severity (when to use this runbook), Prerequisites (access, tools), Steps (numbered, with exact commands — copy-pasteable), Verification (how to confirm the fix worked), Rollback (how to undo if it made things worse), Escalation (who to contact if this runbook doesn't resolve).
   - **Key runbooks to have**: database failover, traffic spike mitigation, certificate expiration, disk full, memory leak restart procedure, secret rotation, deployment rollback.
   - **Keep runbooks in the repo** next to the code they operate on — `service/runbooks/`. They should be reviewed during code review.
5. **Onboarding Guide** — Target: new developer productive within 1 week.
   - **Sections**: Development environment setup (automated — one script if possible), repository tour (key directories explained), architecture overview (diagram + 1-page explanation), development workflow (branch → code → test → PR → review → merge → deploy), how to find work (backlog, labeling conventions), team norms (meetings, communication), who's who (team member roles and areas of expertise).
6. **Changelogs** — Document what changed, for whom, and migration steps:
   - **Automated**: use Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `perf:`, `test:`, `ci:`, `build:`) + `standard-version` or `semantic-release` to auto-generate CHANGELOG.md grouped by type.
   - **Manual curation**: for user-facing changelogs, write in feature language, not commit language. "Added support for SAML SSO" not "implemented SAML provider in auth module." Include migration guide (steps the user must take to adopt the change) and deprecation notices with timeline.
   - **Keep a BREAKING CHANGES section**: `BREAKING CHANGE: the 'api_key' config field is now 'credentials.api_key'. Migration: rename in config file.`

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Operations & Maintenance

1. **Documentation Site IA (Information Architecture)** — Structure by persona or by activity:
   - Persona-based: "For Developers" / "For Operators" / "For Integrators".
   - Activity-based: "Getting Started" / "Guides" / "API Reference" / "Operations" / "Contributing".
   - Universal elements: search (Algolia, Pagefind, or built-in — search is the #1 requested feature), table of contents on every page, breadcrumbs, dark mode, feedback widget ("Was this page helpful?").
2. **Documentation Review Process** — Treat docs like code:
   - Docs PR alongside code PR — never "I'll document it later."
   - Reviewer checklist: is it accurate? (test the code examples), is it discoverable? (linked from relevant pages), is it complete? (covers error cases, not just happy path), does it follow the style guide?
   - Docs test in CI: build the site, check no broken links (internal or external), lint prose with Vale, validate OpenAPI spec, verify code examples compile/run.
3. **Keeping Docs Fresh** — Rotation mechanisms:
   - **Docs on-call**: each sprint, one developer is responsible for reviewing docs touched by that sprint's work.
   - **Freshness check automation**: script that identifies docs not updated in >6 months, flags in a GitHub issue for review.
   - **User feedback loop**: "Was this page helpful? Yes/No" widget. If "No," ask what was missing. Route feedback to the owning team.
   - **Deprecation banners**: when a feature is deprecated, add a banner at the top of every related doc page with the deprecation timeline and migration path. Archive deprecated docs after the retention period.
