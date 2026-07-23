# Sub-Skills

<!-- QUICK: 30s -- table of deeper dives by topic -->
When the agent identifies a specific docs engineering need, drill into the relevant sub-skill. Each sub-skill has dedicated references, templates, and CI configurations.

| Sub-Skill | What It Covers | Key Reference |
|-----------|---------------|----------------|
| **Docs-as-Code Infrastructure** | Repository structure, CI/CD pipeline (GitHub Actions for Docusaurus/VitePress), preview environments, SSG selection (7 generators compared), diagram pipeline (Mermaid/PlantUML/Structurizr) | `references/docs-as-code-guide.md` (complete implementation) |
| **API Documentation Generation** | OpenAPI → Redoc/Scalar/Swagger, GraphQL SDL → GraphDoc/SpectaQL, Protobuf → protoc-gen-doc, SDK docs (TypeDoc/Javadoc/Sphinx), CI validation (Spectral linting) | Section below: "API Documentation" |
| **Information Architecture** | Diátaxis framework (tutorials, how-to, reference, explanation), navigation depth limits, breadcrumbs, search UX (Algolia/Pagefind), landing page design | Section below: "Information Architecture" |
| **Content Quality Automation** | Vale prose linting, markdownlint, broken link checking (lychee), spell checking (cspell), code snippet type-checking, frontmatter validation, freshness (stale flagging) | Section below: "Content Quality Automation" |
| **Documentation Versioning** | Multi-version strategy (current + N-1), deprecation banners, version dropdown UX, maintenance policies, archiving old versions | Section below: "Versioning" |
| **Templates & Content Design** | API reference template, how-to guide template, tutorial template, troubleshooting guide template, concept page template — production-grade templates in `assets/` | `assets/api-reference-template.md`, `assets/how-to-guide-template.md`, `assets/tutorial-template.md` |
| **Documentation Analytics** | Page analytics (views, bounce rate), search analytics (top queries, no-result queries), "Was this helpful?" feedback widgets, funnel analysis | Section below: "Analytics" |

> **Token-saving rule:** Setting up a docs site? Load "Docs-as-Code Infrastructure" + the SSG decision matrix. Writing an API reference page? Load the API template from `assets/api-reference-template.md` (364 lines) — it's self-contained. Don't load i18n when you're just fixing a broken link.
