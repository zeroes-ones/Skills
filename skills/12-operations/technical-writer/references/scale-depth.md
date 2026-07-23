# Scale Depth

### Solo (1 person, 0-100 users)
Developer writing docs alongside code. Docs as Markdown in the repo, served via GitHub Pages, Mintlify, or Docusaurus free tier. README + CONTRIBUTING + basic API reference (manually written). No dedicated documentation site beyond repo. No style guide, no CI for docs. Update docs when something breaks. Cost: $0-100/month. Overkill: dedicated docs platform (GitBook/ReadMe), OpenAPI auto-generation, docs-as-code pipeline, dedicated technical writer.

### Small (2-10 people, 100-10K users)
Developer with docs focus or part-time technical writer. Docs-as-code: Markdown in repo, CI validates links, site via Docusaurus/Mintlify/ReadMe. API reference from OpenAPI spec (Redoc/Swagger UI). Style guide (Google Developer Style Guide or custom). Changelog: keepachangelog.com format. Onboarding guide maintained. Cost: $200-1K/month. Overkill: dedicated docs engineer, localization, content testing platform.

### Medium (10-50 people, 10K-1M users)
Dedicated technical writer or small docs team (1-2). Full docs platform: GitBook, ReadMe, or custom. Diátaxis framework. API reference auto-generated + conceptual guides. Automated link checking, spell checking, readability scoring in CI. Content testing: user feedback surveys, search analytics, page-level NPS. Style guide enforced via Vale linter. Cost: $2K-10K/month.

### Enterprise (50+ people, 10K+ users)
Docs team (3-10+). Enterprise docs platform with SSO, analytics, versioning. Multi-product documentation with consistent IA. Localization pipeline for 3+ languages. Docs product management: roadmap, user research, content design. API docs: SDK generation from OpenAPI, interactive API explorer. Docs metrics: CSAT, self-service resolution rate, time-to-answer. Cost: $20K-200K+/month.

### Transition Triggers
| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | >3 contributors find docs confusing, or product has paying customers | Adopt docs-as-code; add docs CI; implement style guide; auto-generate API reference |
| Small → Medium | >50 docs pages, multiple products, or >100 support tickets/month traceable to docs gaps | Hire dedicated writer; implement Diátaxis; add content testing |
| Medium → Enterprise | 3+ languages needed, >100K monthly docs users, or docs-driven revenue (PLG) | Build docs team; implement localization; add docs product management; enterprise platform |


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | backend-developer | API implementations, OpenAPI specs, RFC documents |
| **This** | technical-writer | API reference docs, ADRs, READMEs, runbooks, onboarding guides |
| **After** | documentation-engineer | Published documentation site, CI/CD pipeline, quality automation |

Common chains:
- **Chain**: backend-developer → technical-writer → documentation-engineer — API code becomes polished documentation; docs engineer integrates it into the site and CI pipeline.
- **Chain**: qa-engineer → technical-writer → devrel-advocate — QA-discovered edge cases inform runbooks and troubleshooting guides; devrel uses them for developer outreach.
