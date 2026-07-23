# Scale Depth

<!-- QUICK: 30s -- find your team size column -->
### Solo (1 person) → Small (2-10) → Medium (10-50) → Enterprise (50+)

| Dimension | Solo | Small | Medium | Enterprise |
|-----------|------|-------|--------|------------|
| **Docs Infrastructure** | README.md in repo | Docusaurus on Vercel (free) | Docs-as-code CI/CD with previews | Multi-site, multi-repo, SSO-gated docs |
| **API Reference** | curl examples in README | Auto-generated from OpenAPI | Interactive API explorer (Scalar/Stoplight) | SDK docs + multi-language samples |
| **Search** | Ctrl+F | Pagefind (free) | Algolia DocSearch | Algolia paid with search analytics |
| **Quality** | Manual review | Vale + markdownlint in CI | Full quality gates + readability scores | Automated freshness, ownership, contribution tracking |
| **Versioning** | None needed | Git tags for releases | Multi-version with deprecation banners | Version maintenance policy + SLA |
| **i18n** | English only | English only | Top pages translated | Full i18n pipeline with Crowdin |
| **Metrics** | None | Page views | Feedback widget + analytics | Docs-as-product dashboard |
| **Team** | Developer writes docs | Rotating docs duty | 1 dedicated writer | Docs team (2-4) with specialization |

### Transition Triggers

| From → To | Trigger | What to Change |
|-----------|---------|----------------|
| Solo → Small | >3 regular contributors | Set up Docusaurus/VitePress, add search, start style guide |
| Small → Medium | >50 docs pages, users asking for versioned docs | Add CI/CD quality gates, multi-version setup, auto-generated API refs |
| Medium → Enterprise | >500 docs pages, non-English user base >10% | Dedicated docs team, i18n pipeline, docs-as-product KPIs, ownership model |
