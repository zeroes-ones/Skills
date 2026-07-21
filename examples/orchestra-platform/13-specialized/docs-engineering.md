# Documentation Engineering

## Platform

Docusaurus 3.2 deployed at `docs.orchestra.dev`. Static site built with `docusaurus build`, output hosted on S3 with CloudFront CDN (same distribution as the marketing site, path pattern `/docs/*`). Custom Docusaurus theme extends the Orchestra design system: purple primary, Inter font, dark mode toggle that syncs with the user's OS preference. Search powered by Algolia DocSearch (free for open-source, applied under the "developer platform" exception with 4,200 indexed pages).

## Docs-as-Code Workflow

All documentation lives in `orchestra-docs` GitHub repository. Authoring flow: write in Markdown → open PR → CI runs quality gates → peer review → merge to `main` → GitHub Actions builds Docusaurus → deploys to S3 → CloudFront cache invalidation (`/docs/*` path). Average time from PR open to docs live: 18 minutes. Contributors: 8 engineers + 2 technical writers.

## Content Quality Gates

CI pipeline enforces three quality gates before merge:

- **Vale Prose Linting**: Custom Vale style guide (`vale-orchestra`) enforces: sentence length ≤ 35 words, no passive voice in procedures, no "simply" or "just" (ableist language), consistent capitalization of product names (Orchestra, not orchestra), heading case (sentence case for H2+, title case for H1). 14 style rules. All violations must be resolved or explicitly waived with a `<!-- vale off -->` comment.
- **Broken Link Checker**: `lychee` scans all internal and external links on every PR. Internal links (relative paths within Docusaurus) are validated against the file tree. External links are checked with a 10-second timeout and retry. Broken external links block merge (with a 72-hour grace period for transient outages).
- **Code Example Policy**: Every documentation page must contain at least 1 fenced code block. Enforced via a custom script that counts triple-backtick blocks. Exemptions: glossary pages, release notes, and legal pages (listed in an allowlist).

## Versioned Documentation

Docusaurus versioning configured for `v1.0` (current stable), `v1.1` (in development, deployed as "next" from the `develop` branch), and `v0.9` (previous stable, maintained for 3 months after v1.0 release). Version dropdown in the docs navbar lets users switch between versions. Deprecation banner appears on v0.9 pages: "You're viewing docs for v0.9. v1.0 includes SSO support and the Plugin SDK."

## Internationalization

English is the primary documentation language. German translation pipeline established via Crowdin: `main` branch pushed to Crowdin → professional translators (verified technical translators with DevOps domain knowledge) → translated PR opened automatically → reviewed by a German-speaking engineer → merged. Current coverage: quickstart (100%), API reference (45%), plugin SDK (15%). Target: 80% of top-20 pages translated by Q1 2027.

## Analytics

Plausible Analytics (privacy-focused, no cookies) tracks documentation usage. July 2026 metrics: 3,200 unique visitors, 12,400 page views, average time on page 3m 42s. Top 5 pages: quickstart (1,200 UV), template-api-reference (870 UV), plugin-sdk-quickstart (640 UV), architecture-overview (520 UV), troubleshooting-deployments (490 UV). Bounce rate: 32% — below the 45% SaaS documentation benchmark.
