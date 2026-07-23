---
name: documentation-engineer
description: Docs-as-code (Docusaurus vs Nextra vs Mintlify vs GitBook), API documentation (OpenAPI, GraphQL, gRPC), information architecture, content quality automation (Vale, broken links), versioning,
  i18n, analytics, onboarding docs, ADRs, runbooks.
author: Sandeep Kumar Penchala
type: specialized
status: stable
version: 1.0.0
updated: 2026-07-21
tags:
- documentation-engineer
token_budget: 4000
output:
  type: code
  path_hint: ./
chain:
  consumes_from:
  - api-designer
  - devrel-advocate
  - hardware-architect
  - technical-writer
  feeds_into:
  - backend-developer
  - devrel-advocate
  - technical-writer
---
# Documentation Engineer

A veteran documentation engineer's playbook — docs-as-code infrastructure, static site generator selection, automated API documentation pipelines, information architecture at scale, content quality automation, versioning strategies, internationalization, search optimization, analytics, and production-grade templates for the full documentation lifecycle.


### Cross-skills Integration

| Step | Skill | What it produces |
|------|-------|------------------|
| **Before** | technical-writer | API reference docs, ADRs, READMEs, runbooks, onboarding guides |
| **This** | documentation-engineer | Docs-as-code infrastructure, CI/CD pipeline, quality automation, versioned site |
| **After** | devrel-advocate | Developer-facing content strategy, tutorials, conference talks based on docs |

Common chains:
- **Chain**: technical-writer → documentation-engineer → devrel-advocate — Writer produces content; docs engineer builds the pipeline and site; devrel uses it for developer outreach.
- **Chain**: backend-developer → documentation-engineer → platform-engineer — Developer provides API specs; docs engineer builds the documentation infrastructure; platform engineer hosts and scales it.

## Sub-Skills
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

## Route the Request
<!-- QUICK: 30s -- pick your path, skip the rest -->

What are you trying to do?
├── Set up docs-as-code (Docusaurus/Nextra/Mintlify/GitBook) → Start at "Docs-as-Code Infrastructure" under Sub-Skills
├── Generate API documentation → Go to "API Documentation Generation" under Sub-Skills
├── Design information architecture → Jump to "Information Architecture" under Sub-Skills
├── Automate content quality (linting, link checking) → Go to "Content Quality Automation" under Sub-Skills
├── Set up documentation versioning → Jump to "Documentation Versioning" under Sub-Skills
├── Configure i18n for docs → Go to "references/i18n-guide.md"
├── Set up documentation analytics → Jump to "Documentation Analytics" under Sub-Skills
├── Need content written first → Route to `technical-writer`
├── Need API specs or code annotations → Route to `backend-developer`
├── Need developer content strategy → Route to `devrel-advocate`
├── Need docs site UI design → Route to `frontend-developer`
└── Don't know where to start? → Start at "Docs-as-Code Infrastructure"

**Do not read the entire skill.** Follow the route above and read only the sections it points to.

## Ground Rules — Read Before Anything Else

These rules apply to *every* response this skill produces.

- **Never choose a docs tool before understanding the author workflow.** The best SSG is the one your writers will actually use.
- **Information architecture must be tested with real users.** Card sorting and tree testing beat designer intuition every time.
- **Broken links erode trust faster than missing content.** Automate link checking in CI — never ship broken links.
- **Versioned docs need a clear deprecation policy.** Readers must know when a version is unsupported and what to migrate to.
- **Always prefer discoverability over completeness.** A well-organized 50-page site beats a chaotic 500-page site.
- **Admit what you don't know.** If a tool's limitations or an integration is unclear, research before committing.

## When to Use
<!-- QUICK: 30s -- scan the bullet list to decide if this skill fits -->
- Selecting a static site generator for docs (Docusaurus vs Nextra vs Mintlify vs GitBook vs VitePress vs Hugo vs ReadTheDocs)
- Building a docs-as-code pipeline: branching strategy, CI/CD, preview environments, CODEOWNERS
- Automating API reference generation from OpenAPI, GraphQL schemas (SDL), or Protobuf definitions
- Designing information architecture for 50+ services — Diataxis framework, navigation depth, search UX
- Implementing quality gates: Vale prose linting, broken link checks, code snippet validation, freshness automation
- Setting up multi-version docs with deprecation banners, version dropdowns, and maintenance policies
- Internationalizing docs: Crowdin workflow, RTL support, locale fallback
- Configuring search (Algolia DocSearch, Pagefind) with relevance tuning and analytics
- Creating onboarding docs, ADRs, runbooks, and incident response documentation programs
- Establishing documentation metrics: coverage, freshness, quality, usage, contribution

## Decision Trees
<!-- QUICK: 30s -- follow the ASCII tree to your scenario -->
### 1. SSG Selection
```
                     ┌────────────────────┐
                     │ START: Pick a docs │
                     │ site generator     │
                     └─────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Team on Next.js     │
                    │ already?            │
                    └────┬───────────┬────┘
                         │ YES       │ NO
                    ┌────▼────┐ ┌───▼──────────────┐
                    │ Nextra  │ │ Need full MDX +   │
                    │ (MDX-   │ │ rich plugin eco?  │
                    │  first) │ └──┬───────────┬────┘
                    └─────────┘    │YES        │NO
                          ┌────────▼────┐ ┌───▼─────────┐
                          │ Docusaurus  │ │ Python shop? │
                          │ (React+MDX) │ └──┬──────┬────┘
                          └─────────────┘    │YES   │NO
                                    ┌────────▼──┐ ┌─▼──────────┐
                                    │ReadTheDocs │ │Need zero   │
                                    │(Sphinx/RST)│ │maintenance?│
                                    └────────────┘ └──┬─────┬───┘
                                                      │YES  │NO
                                                ┌─────▼──┐ ┌▼──────┐
                                                │Mintlify│ │Vite-  │
                                                │(SaaS)  │ │Press  │
                                                └────────┘ └───────┘
```
**Docusaurus** for most teams — best balance of features, plugins, versioning, and community.  
**Nextra** for Next.js-first teams wanting MDX and custom React components.  
**Mintlify** for teams wanting zero-infrastructure SaaS with beautiful defaults at $600+/mo.  
**ReadTheDocs** for Python-only projects using Sphinx. **VitePress** for minimal Vue-based docs.

### 2. When to Version Docs
```
                   ┌────────────────────────┐
                   │ START: Do you have      │
                   │ >1 major API version    │
                   │ in production?          │
                   └───────────┬────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ YES → Set up multi- │
                    │ version: current +   │
                    │ N-1. Deprecation     │
                    │ banners on older.    │
                    └─────────────────────┘
                    ┌──────────▼──────────┐
                    │ NO → Single version │
                    │ is sufficient. Add  │
                    │ versioning when you │
                    │ ship v2.            │
                    └─────────────────────┘
```


**What good looks like:** Documentation pipeline auto-generates API reference from source. Every page passes the "one reader goal" test. Search returns relevant results for the top 50 user queries. Documentation is versioned alongside releases. User feedback collected via thumbs up/down on every page.

### 3. Search Strategy
```
                   ┌───────────────────────┐
                   │ START: How many docs  │
                   │ pages do you have?    │
                   └───────────┬───────────┘
                               │
                    ┌──────────▼──────────┐
                    │ <50 pages?          │
                    └────┬───────────┬────┘
                         │YES        │NO
                    ┌────▼────┐ ┌───▼──────────┐
                    │ Pagefind│ │ Open source   │
                    │ (free,  │ │ project?      │
                    │ zero    │ └──┬───────┬────┘
                    │ infra)  │    │YES    │NO
                    └─────────┘ ┌──▼────┐┌▼──────────┐
                                │Algolia││Algolia paid│
                                │Doc-   ││($500+/mo)  │
                                │Search ││or Pagefind │
                                │(free) ││for <1000   │
                                └───────┘│pages       │
                                         └────────────┘
```
**Pagefind for <1000 pages** — zero infrastructure, build-time index, works offline.  
**Algolia DocSearch for OSS** — free, relevance-tuned, faceted search.  
**Algolia paid for enterprise** — >1000 pages, need search analytics, faceted by version.

### 4. Content Quality Priority
```
                  ┌────────────────────────┐
                  │ START: What's your     │
                  │ biggest docs quality   │
                  │ problem?               │
                  └───────────┬────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
  ┌─────▼──────┐    ┌────────▼───────┐    ┌────────▼──────┐
  │ Users say  │    │ Users say docs │    │ Docs site     │
  │ docs are   │    │ are wrong or  │    │ hard to       │
  │ hard to    │    │ outdated     │    │ navigate      │
  │ read       │    │              │    │               │
  └─────┬──────┘    └────────┬──────┘    └────────┬──────┘
        │                    │                    │
  ┌─────▼──────┐    ┌────────▼──────┐    ┌────────▼──────┐
  │ Add Vale   │    │ Auto-generate │    │ Redesign IA   │
  │ prose lint │    │ API refs from │    │ with Diataxis │
  │ + cspell   │    │ OpenAPI spec  │    │ + improve     │
  │ + readabil-│    │ + add fresh-  │    │ search UX     │
  │ ity scores │    │ ness checks   │    │               │
  └────────────┘    └───────────────┘    └───────────────┘
```
**Hard to read → Vale + cspell + readability scoring.**  
**Wrong/outdated → auto-generate from specs + freshness automation.**  
**Hard to navigate → Diátaxis IA restructure + search relevance tuning.**

### 5. When to Internationalize
```
                  ┌─────────────────────────┐
                  │ START: What % of users  │
                  │ are non-English?        │
                  └───────────┬─────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
    ┌─────▼──────┐    ┌───────▼───────┐    ┌──────▼──────┐
    │ <10%      │    │ 10-30%       │    │ >30%        │
    └─────┬──────┘    └───────┬───────┘    └──────┬──────┘
          │                   │                   │
    ┌─────▼──────┐    ┌───────▼───────┐    ┌──────▼──────┐
    │ Don't i18n │    │ Translate top │    │ Full i18n   │
    │ yet. ROI   │    │ 20 pages +   │    │ with Crowdin │
    │ too low.   │    │ API ref.     │    │ or GitLoc-   │
    │            │    │ English      │    │ alize. RTL   │
    │            │    │ fallback for │    │ support.     │
    │            │    │ rest.        │    │              │
    └────────────┘    └──────────────┘    └──────────────┘
```
**<10% non-English → don't invest in i18n.**  
**10-30% → translate most-visited pages only, English fallback.**  
**>30% → full i18n pipeline with Crowdin/GitLocalize and RTL support.**

## Docs-as-Code

### Git-Based Workflow

- **Branching Strategy**: Use a `docs/` prefix for doc-only branches, or include docs changes in feature branches (preferred for monorepos). Merge to `main` triggers a production build. Use release tags (`v2.0.0`) for versioned doc snapshots.
- **PR Review Process**: Every docs PR requires:
  - Vale prose lint passing (fail on error, warn on suggestion)
  - At least one technical review from code owners
  - At least one editorial review (optional for hotfixes)
  - Preview deployment link verified as functional
- **CODEOWNERS for Docs**:
  ```
  # .github/CODEOWNERS
  docs/api/        @org/platform-team
  docs/guides/     @org/devrel-team
  docs/runbooks/   @org/sre-team
  docs/            @org/docs-owners
  ```

### Markdown/MDX Authoring

- **Plain Markdown** for: reference docs, how-to guides, conceptual overviews, ADRs, runbooks. Keeps contributions low-friction since every engineer knows Markdown.
- **MDX** for: interactive API explorers, live code editors, embedded dashboards, custom callout components, tab-based code samples (multi-language). MDX lets you import React components directly:
  ```mdx
  import Tabs from '@theme/Tabs';
  import TabItem from '@theme/TabItem';
  import CodeBlock from '@theme/CodeBlock';

  <Tabs>
    <TabItem value="py" label="Python">
      ```python
      client.create_user(email="user@example.com")
      ```
    </TabItem>
    <TabItem value="js" label="JavaScript">
      ```javascript
      client.createUser({ email: 'user@example.com' });
      ```
    </TabItem>
  </Tabs>
  ```

### CI/CD for Docs

Complete GitHub Actions pipeline for Docusaurus:

```yaml
name: Docs CI/CD
on:
  pull_request:
    paths: ['docs/**', 'sidebars.js', 'docusaurus.config.js']
  push:
    branches: [main]
    paths: ['docs/**', 'sidebars.js', 'docusaurus.config.js']
  schedule:
    - cron: '0 6 * * 0'  # Weekly external link check

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - name: Vale Lint
        uses: errata-ai/vale-action@v2
        with:
          files: docs/
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - name: Markdown Lint
        run: npx markdownlint-cli2 "docs/**/*.md" "docs/**/*.mdx"
      - name: Check Internal Links
        run: npx docusaurus build
      - name: Spell Check
        run: npx cspell "docs/**/*.md" "docs/**/*.mdx"
      - name: Check Frontmatter
        run: node scripts/check-frontmatter.mjs

  build-and-deploy:
    needs: lint
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run build
      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v2
        with:
          publish-dir: ./build
          production-branch: main
          production-deploy: true
          github-token: ${{ secrets.GITHUB_TOKEN }}
      - name: Trigger Algolia Crawl
        run: |
          curl -X POST "https://crawler.algolia.com/api/1/crawlers/${{ secrets.ALGOLIA_CRAWLER_ID }}/reindex"
```

### Preview Environments

- **Per-PR preview**: Netlify deploy previews, Vercel preview deployments, or GitHub Pages from `gh-pages` branch.
- **Preview comment**: GitHub Action posts preview URL as a PR comment on every docs change.
- **Branch-based preview names**: `https://pr-42--docs-preview.netlify.app`

## Static Site Generators (Decision Matrix)

| Dimension | Docusaurus | Nextra | Mintlify | GitBook | ReadTheDocs | VitePress | Hugo |
|---|---|---|---|---|---|---|---|
| Framework | React | Next.js (React) | SaaS (hosted) | SaaS (hosted) | Sphinx (Python) | Vue | Go (no JS needed) |
| Plugin Ecosystem | Rich (50+) | Next.js ecosystem | Built-in only | Limited | Sphinx extensions | Growing (10+) | Large (300+) |
| Search Built-in | Algolia/Pagefind | FlexSearch | Built-in | Built-in | Built-in | Pagefind | Lunr.js |
| Versioning | First-class | Manual (branches) | Built-in | Built-in | Built-in (tags) | Manual (branches) | Manual (branches) |
| API Doc Rendering | docusaurus-plugin-openapi-docs, Redoc | OpenAPI spec viewer | First-class | Limited | sphinxcontrib-openapi | Manual integration | Custom shortcodes |
| MDX Support | Full MDX 3 | MDX-first | No | No | No (MyST, RST) | Full MDX | No |
| i18n | Built-in (Crowdin) | next-intl | Built-in | Built-in | sphinx-intl | Built-in | i18n module |
| Cost | Free | Free | $600+/mo (pro) | $960+/yr (pro) | Free (OSS) | Free | Free |
| Learning Curve | Moderate | Moderate (Next.js) | Low | Low | Moderate (RST) | Low | Moderate |

### Docusaurus Deep Dive

- **Essential Plugins**:
  - `docusaurus-plugin-openapi-docs` — generate API docs from OpenAPI specs
  - `docusaurus-theme-search-typesense` — alternative search
  - `docusaurus-plugin-remote-content` — pull docs from external repos
  - `docusaurus-plugin-pwa` — offline support
  - `@cmfcmf/docusaurus-search-local` — local search (no Algolia)
- **Versioning Configuration**:
  ```json
  // docusaurus.config.js
  module.exports = {
    presets: [
      [
        'classic',
        {
          docs: {
            lastVersion: 'current',
            versions: {
              current: { label: '2.x (latest)', path: 'latest' },
              '2.0.0': { label: '2.0.0', path: '2.0.0' },
              '1.5.0': { label: '1.5.x (maintained)', path: '1.5.x' },
            },
          },
        },
      ],
    ],
  };
  ```
- **Theme Customization**: Override components via `src/theme/` (Swizzling). Common overrides: `DocItem/Layout` (add feedback widget), `Navbar` (add version selector), `Footer` (add doc status).
- **Algolia Integration**:
  ```js
  module.exports = {
    themeConfig: {
      algolia: {
        appId: 'YOUR_APP_ID',
        apiKey: 'YOUR_SEARCH_API_KEY',
        indexName: 'docs',
        contextualSearch: true,
        searchParameters: {
          facetFilters: ['version:latest'],
        },
      },
    },
  };
  ```

### Nextra

- **Next.js-based**: File-based routing in `pages/` directory. Each `.mdx` file is a route.
- **MDX-first**: Every page is MDX by default. Import any React component directly.
- **Custom React Components**: Build interactive demos, playgrounds, or dashboards as React components embedded in docs.
- **Theme**: Built-in docs theme with sidebar, TOC, search (FlexSearch).
- **Ideal for**: Teams already on Next.js who want full control and custom interactivity.

### Mintlify

- **SaaS**: Zero infrastructure. Push markdown to a Git repo, Mintlify handles hosting, CDN, search, analytics.
- **Beautiful by Default**: Typography, layout, dark mode are production-quality out of the box.
- **API Reference First-Class**: OpenAPI spec -> rendered reference. Interactive try-it-out with auth configuration.
- **Managed Search**: Built-in Algolia search, no configuration needed. Search analytics included.
- **Cost**: Free tier (1 editor, community), Pro ($600+/mo). Non-trivial for large teams but near-zero maintenance.

### GitBook

- **Collaborative Editing**: WYSIWYG editor, good for non-technical contributors. Syncs with GitHub.
- **Good for Internal Docs**: Quick to set up for engineering wikis, onboarding, runbooks.
- **Limited Customizability**: Can't deeply customize layout, theme, or add custom components.
- **Search and Analytics**: Built-in but less powerful than Algolia.

### ReadTheDocs

- **Sphinx-based**: Uses reStructuredText (RST) or MyST Markdown. Python ecosystem.
- **Great for Python Projects**: Auto-generates API docs from Python docstrings (sphinx.ext.autodoc).
- **Free for Open Source**: Hosted. Build triggers on Git push. Versioned docs.
- **Limited Frontend**: Theme-based customization, can't add custom JS/React easily.

### VitePress

- **Vue-based**: Lightning fast builds (Vite under the hood). Minimal configuration.
- **Markdown + MDX**: Write in Markdown, extend with Vue components.
- **Search**: Pagefind or built-in mini search.
- **Ideal for**: Small projects, Vue ecosystem docs, minimal doc sites.
- **Limitations**: Smaller plugin ecosystem, no built-in versioning or API doc rendering.

### Hugo

- **Go-based**: Fastest build times (milliseconds for thousands of pages). No JS runtime needed.
- **Template System**: Go templates. Steeper learning curve but extremely flexible.
- **Large Theme Ecosystem**: 300+ themes. Docsy theme for tech docs.
- **Ideal for**: Large static content sites, performance-critical docs, teams comfortable with Go templates.
- **Limitations**: No MDX, no interactive components without JS, no built-in versioning.

## Information Architecture

### Navigation Design

- **Max 3 levels deep**: Any page should be reachable in (calculating from the homepage). Deep nesting hides content.
- **Breadcrumbs**: Every page includes breadcrumb navigation indicating position in hierarchy.
- **Related Pages**: "Next Steps" or "See Also" section at page bottom linking to logically connected pages.
- **Sidebar Behavior**: Show only the current section's subtree (not the full site tree). Keeps navigation scannable.
- **Search Bar Position**: Prominent in the navbar, immediately visible on page load.

### Search Experience

- **Algolia DocSearch**: Free for open source projects. Configuration via `docusaurus.config.js`. Crawler runs on schedule or CI trigger.
- **Pagefind**: Static search index, no server needed. Works offline. Good for small-to-medium doc sites.
- **Search Relevance Tuning**: Boost page titles over body text, boost short pages, demote "glossary" type pages.
- **Search Analytics**: Track top queries, "no results" queries (identify documentation gaps), click-through rate from search results.

### Landing Page Design

- **Hero Section**: Product name, tagline, "Get Started" CTA button.
- **Quickstart Link**: Most visible link after hero -- "Get started in 5 minutes."
- **Popular Guides**: 3-4 most-visited pages with brief descriptions.
- **Search Bar**: Prominently displayed, with placeholder text encouraging search ("Search docs...").

### Content Hierarchy (Diataxis Framework)

| Category | Purpose | Audience | Example |
|---|---|---|---|
| **Tutorial** | Learning-oriented | New users | "Build your first app" |
| **How-To Guide** | Task-oriented | Experienced users | "Deploy to production" |
| **Reference** | Information-oriented | All users | "API endpoint reference" |
| **Explanation** | Understanding-oriented | Advanced users | "Architecture overview" |

### Progressive Disclosure

- **Summary -> Details -> Deep Dive**: Each page starts with a one-paragraph summary. Expand with progressively more detail. Reserve the deepest technical content for optional expandable sections or linked deep-dive pages.
- **Collapsible sections**: Use `<details>` / `<summary>` for optional deep-dives that 80% of readers don't need.

## API Documentation

### OpenAPI/Swagger

- **Spec as Source of Truth**: `openapi.yaml` lives in the repo. All changes to the API start with changes to the spec.
- **CI Validation**:
  ```yaml
  - name: Validate OpenAPI Spec
    run: npx @stoplight/spectral-cli lint openapi.yaml
  - name: Check Breaking Changes
    run: npx @apideck/openapi-diff openapi-v1.yaml openapi-v2.yaml
  ```
- **Reference Generation**: `docusaurus-plugin-openapi-docs` renders OpenAPI specs as Docusaurus doc pages. Alternative: Redoc standalone HTML, Scalar API reference.
- **Supplemental Hand-Written Guides**: Authentication, pagination, error handling, webhooks, rate limiting -- these are better explained in prose than auto-generated.

### GraphQL

- **Schema SDL as Source of Truth**: GraphQL schema files in the repo. Annotate with triple-quote description comments.
- **Auto-Generated Docs**: GraphDoc, SpectaQL, or Magidoc read the schema SDL and generate a full reference site.
- **Interactive Explorer**: GraphiQL or Apollo Studio Sandbox embedded for query experimentation.

### gRPC / Protobuf

- **`.proto` as Source of Truth**: Proto definitions in the repo.
- **Auto-Generated Docs**: `protoc-gen-doc` generates Markdown or HTML from `.proto` files.
  ```bash
  protoc --doc_out=./docs/api --doc_opt=markdown,api.md proto/*.proto
  ```
- **Service Documentation**: Each RPC method, message type, and field defined in the proto becomes documented.

### Interactive API Explorer

- **Try-It-Out Functionality**: Swagger UI, Scalar, or Mintlify's embedded API playground -- let users send real requests from the docs.
- **Auth Configuration**: Support API key, Bearer token, OAuth2. Store example tokens securely.
- **Example Requests**: Pre-populated curl, Python, JavaScript, Go examples for each endpoint.

### SDK Documentation

- **TypeDoc (TypeScript)**: `npx typedoc --out docs/api src/index.ts`
- **Javadoc (Java)**: `mvn javadoc:javadoc` outputs to `target/site/apidocs/`
- **Sphinx (Python)**: `sphinx-apidoc -o docs/api src/` followed by `make html`
- **CI Integration**: SDK docs are auto-generated on merge and published to the docs site.

## Versioning

### Strategies

- **Per Major Version** (recommended): `docs/v1/`, `docs/v2/`, `docs/latest/`. Each major version has its own doc snapshot. Docusaurus supports this natively.
- **Per Minor Version**: Useful for SaaS products with frequent releases and backward-compatible changes. Use when minor versions introduce meaningful doc changes.
- **"Latest" Alias**: `/latest/` always points to the most recent stable version. `/v2/` is locked.

### Deprecation Banners

```mdx
:::caution You're reading outdated docs
This documentation is for version 1.x, which is no longer actively maintained.
View the [latest version](/latest) of this page.
:::
```

Configured globally in Docusaurus:
```js
// docusaurus.config.js
module.exports = {
  presets: [
    [
      'classic',
      {
        docs: {
          banner: 'unmaintained',
        },
      },
    ],
  ],
};
```

### Version Selector UX

- **Dropdown in Navbar**: Docusaurus adds this automatically with `lastVersion` and `versions` config.
- **URL-Based Versions**: `/docs/latest/getting-started`, `/docs/v2.0.0/getting-started`
- **Redirect**: `/docs/` -> `/docs/latest/` automates routing to current version.

### Maintenance Policy

- **Current + N-1 Maintained**: Latest version receives full updates. The previous major version receives critical bug fixes and security updates. Older versions are frozen (no updates) with deprecation banners.
- **Automation**: GitHub Action runs weekly to check doc version ages and add banners when a version falls out of maintenance.

## Content Quality Automation

### Broken Link Checking

- **Internal Links**: Docusaurus build fails on broken internal links by default (`onBrokenLinks: 'error'` in config).
- **External Links**: Use `lychee` or `broken-link-checker` in a scheduled workflow:
  ```yaml
  - name: Check External Links
    run: |
      npx lychee docs/ --config .lychee.toml --format markdown >> link-report.md
  ```

### Prose Linting (Vale)

- **`.vale.ini` Configuration**:
  ```ini
  StylesPath = .vale/styles
  MinAlertLevel = error
  [*.md]
  BasedOnStyles = Docs, Google, write-good
  Docs.Terminology = YES
  Google.Headings = YES
  Google.Parens = YES
  write-good.Epsilon = NO
  ```
- **Custom Style Rules** (`styles/Docs/Terminology.yml`):
  ```yaml
  extends: substitution
  message: "Use '%s' instead of '%s'"
  level: error
  swap:
    Github: GitHub
    "log in": login
    "sign in": login
    javascript: JavaScript
    typescript: TypeScript
    "e\.g\."
    "i\.e\."
  ```
- **CI Integration**: Vale runs per-PR as a required check. Fail on error, warn on suggestion.

### Spell Checking (cspell)

- **`cspell.json` with Custom Dictionary**:
  ```json
  {
    "version": "0.2",
    "language": "en",
    "words": ["Docusaurus", "Mintlify", "VitePress", "Nextra", "Pagefind"],
    "ignorePaths": ["node_modules", "build", ".vale"]
  }
  ```

### Readability Scoring

- **Flesch-Kincaid Grade Level**: Target grade level <= 10 (high school level). Automated flagging of pages with score > 12.
- **CI Check**: Custom script extracting readability stats and flagging complex pages in PR comments.

### Code Snippet Validation

- **Embedded Source Snippets**: Docusaurus `import CodeBlock` from actual source files ensures snippets are always up-to-date and compilable.
- **Extract and Type-Check**: CI script extracts code blocks, writes to temp files, runs `tsc --noEmit` (TypeScript), `python -m py_compile` (Python), `go build` (Go).
- **Verify Imports**: Script checks that all import paths in code blocks resolve to actual packages/modules.

### Frontmatter Validation

Custom script to validate:
```js
// scripts/check-frontmatter.mjs
import matter from 'gray-matter';
import { glob } from 'glob';

const files = await glob('docs/**/*.{md,mdx}');
let errors = 0;
for (const file of files) {
  const { data } = matter.read(file);
  if (!data.title) { console.error(`${file}: missing title`); errors++; }
  if (!data.description) { console.error(`${file}: missing description`); errors++; }
  if (typeof data.sidebar_position !== 'number') { console.error(`${file}: sidebar_position must be a number`); errors++; }
  if (data.tags && !Array.isArray(data.tags)) { console.error(`${file}: tags must be an array`); errors++; }
}
process.exit(errors > 0 ? 1 : 0);
```

## Developer Experience

### Quickstart Quality

- **Time-to-First-Success < 5 Minutes**: The quickstart guide should produce a working result (API response, "Hello World" app) within 5 minutes of starting.
- **One-Command Setup**: `curl -fsSL https://install.example.com | bash` or `npx create-my-app my-project`.
- **No Assumptions**: Don't assume the reader has Node.js, Python, or anything pre-installed. Include system dependency verification.

### Code Sample Testing

- **Doctest Pattern**: Embed tests in docs code blocks, then extract and run them in CI.
- **TypeScript Type Checking**: Extract `.ts` snippets, run `tsc --noEmit` in CI.
- **Rust Doc Tests**: `cargo test` verifies all code examples in Rust doc comments pass.

### Copy-Paste Button

- Every code block has a visible copy button (Docusaurus includes this by default).
- Shell command blocks have a "copy command" button (excludes output lines).
- Multi-line code blocks show line numbers for reference.

### Dark Mode

- **Automatic**: Respects `prefers-color-scheme` CSS media query on first visit.
- **Manual Toggle**: Sun/moon icon in the navbar. Choice is persisted in `localStorage`.
- **Asset Readiness**: All diagrams, screenshots, and logos have dark-mode variants.

### Mobile Responsiveness

- **Readable on Phones**: Docs must be fully readable on a 375px-wide screen (on-call engineers checking their phone).
- **Table Scroll**: Wide tables get horizontal scroll, not overflow.
- **Code Block Scroll**: Code blocks are horizontally scrollable on mobile (not wrapped -- wrapping breaks copy-paste).

## Search

### Algolia DocSearch

- **Free for Open Source**: Apply at docsearch.algolia.com. Requires a public GitHub repo.
- **Configuration**: Crawler config in DocSearch config dashboard or `crawler-config.json`.
- **Relevance Tuning**: Boost titles (weight: 10), headings (weight: 5), body text (weight: 1). Demote very long pages.
- **Facet Filtering**: Filter by version, content type, product area.

### Pagefind

- **Static Search**: Generates a search index at build time. No server, no API key, no external service.
- **Works Offline**: The search index ships with the static site. Useful for internal tools or air-gapped environments.
- **Good for**: Small to medium doc sites (< 1000 pages).

### Search Analytics

- **Top Queries**: What are people looking for most? Surfaced in a weekly report.
- **"No Results" Queries**: These are documentation gaps. Create issues for each unique no-result query.
- **Click-Through Rate**: % of users who click a search result after searching. Low CTR signals poor relevance.

### Search UX

- **Instant Results**: Results appear as the user types (debounced at 200ms).
- **Keyboard Shortcut**: `Cmd+K` (Mac) / `Ctrl+K` (Windows/Linux) opens search. Press again or `Esc` to close.
- **Result Preview**: Each result shows the page title, a snippet of matching text (with highlighted match), and the section heading.

## Internationalization (i18n)

### Translation Workflow

- **Docusaurus i18n Setup**:
  ```bash
  # Initialize i18n
  npx docusaurus write-translations --locale fr
  npx docusaurus write-translations --locale zh-CN
  ```
- **Crowdin Integration**: Docusaurus has a Crowdin plugin. Automated sync: extract English strings -> push to Crowdin -> translated content pulled back -> deploy with all locales.
- **GitLocalize**: Lighter alternative. Open source projects use GitLocalize for community translations.
- **Manual Translation**: For small teams, translators work directly on translated `.md` files in the `i18n/` directory.

### Locale-Specific Content

- **Language Switcher**: Dropdown in the navbar listing available locales.
- **Fallback to English**: If a page hasn't been translated, show the English version with a banner: "This page isn't available in [language] yet."
- **Partial Translation**: It's fine to have some pages translated and others not. Better to ship incomplete translations than none.

### URL Strategy

- `example.com/docs/` -- English (default)
- `example.com/fr/docs/` -- French
- `example.com/zh-CN/docs/` -- Simplified Chinese

### RTL Support

- **Docusaurus RTL**: Built-in RTL support for Arabic, Hebrew, Persian, Urdu. Automatically swaps layout direction.
- **CSS Mirroring**: Docusaurus automatically mirrors the UI. Custom CSS must be RTL-aware.

## Analytics

### Page Analytics

- **Page Views**: Track per-page view counts. Identify most- and least-visited pages.
- **Bounce Rate**: High bounce rate on a page means readers aren't finding what they expected.
- **Time on Page**: Very low time suggests content too shallow. Very high time suggests content too confusing or too long.
- **Popular Pages**: The top 10 most-visited pages should be the most polished.

### Search Analytics

- **Top Queries**: What users search for most. Publish as a docs team metric.
- **No-Result Queries**: File issues for each unique query with zero results. These are unambiguous doc gaps.
- **Click-Through Rate**: % of searches resulting in a click. Low CTR indicates search quality or result relevance needs work.

### Feedback Mechanism

- **"Was This Helpful?" Widget**: At the bottom of every page. Thumbs up / thumbs down with optional text box.
- **Data Collection**: Stored per-page with timestamp. Track Yes/No ratio over time.
- **Low-Rating Alerts**: Pages with >50% "No" ratings trigger a notification to the owning team.

### Funnel Analysis

- **Landing -> Quickstart -> First API Call**: Track the drop-off at each stage of this critical funnel.
- **Measure**: % of visitors who reach the quickstart page; % of quickstart visitors who reach an API reference page.
- **Action**: High drop-off between landing and quickstart means CTA isn't visible enough. High drop-off between quickstart and API ref means quickstart doesn't successfully onboard the reader.

## Templates

Full templates are available in the `assets/` directory:

- **[API Reference Template](./assets/api-reference-template.md)**: Endpoint, method, parameters, request/response examples, error codes, rate limiting, see also.
- **[How-To Guide Template](./assets/how-to-guide-template.md)**: Goal, prerequisites, numbered steps, verification, troubleshooting, next steps.
- **[Tutorial Template](./assets/tutorial-template.md)**: What you'll build, prerequisites, time estimate, step-by-step, complete code, what you learned.
- **Troubleshooting Guide Template**: Symptom, cause, solution, prevention. Each symptom gets its own section.
- **Concept Page Template**: Summary, in-depth explanation with diagrams, related concepts. No steps -- understanding, not doing.

## Cross-Skill Coordination
<!-- QUICK: 30s -- table of who to talk to when -->
Documentation engineering bridges engineering, product, support, and DevRel. The docs platform serves everyone — coordination prevents it from serving no one well.

### Decision Gates & Artifacts

- **Gate 1 — Content Exists:** Docs-as-code infrastructure requires content authored by `technical-writer` before pipelines can process it. Artifact: content inventory with Diátaxis categorization.
- **Gate 2 — API Specs Validated:** API reference generation depends on OpenAPI/GraphQL specs provided by `api-designer`. Artifact: Spectral-linted API spec passing CI.
- **Gate 3 — Audience Strategy Defined:** SEO, search, and analytics configuration aligned with developer outreach strategy from `devrel-advocate`. Artifact: docs analytics strategy document.
- **Gate 4 — Platform Hosted:** Docs site CI/CD and hosting require infrastructure provisioned by `backend-developer`. Artifact: deploy pipeline with preview environments.
- **Artifact:** Docs health audit report (broken links, freshness, coverage), SSG selection rationale, information architecture map.

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Technical Writer(s)** | Docs authoring experience, content structure, publishing workflow | CMS/platform requirements, authoring friction, editorial workflow needs |
| **Frontend Developers** | Docs site UI, search, component library integration | Docs site design system, interactive component embedding, theming requirements |
| **DevRel / Developer Advocate** | SDK docs, API reference, community contributions | Developer experience of docs, community contribution workflow, feedback collection |
| **Product Strategist** | Product documentation strategy, feature docs cadence | Docs as feature requirement, docs quality gates in release process |
| **UX Designer** | Docs information architecture, navigation, search UX | IA testing results, search behavior insights, navigation structure |
| **DevOps / Infrastructure** | Docs site hosting, CI/CD pipeline, preview deployments | Build/deploy pipeline, preview environments, DNS/certificate management |
| **SEO Specialist** | Docs site SEO, structured data, crawlability | OpenAPI → schema.org mapping, sitemap generation, meta tag management |
| **Support / Customer Success** | Knowledge base integration, support-assisted documentation | Support-to-docs feedback loop, "was this helpful" data, ticket-driven doc creation |
| **Security Reviewer** | Docs platform security, access control, internal vs public docs | Authentication requirements, content access rules, vulnerability scanning |
| **Data/Analytics** | Docs analytics, search analytics, content effectiveness | Page analytics, search query analysis, content gap identification from analytics |
| **Backend Developers** | API spec generation, auto-generated reference docs | OpenAPI spec quality, code annotation standards, SDK documentation generation |
| **QA Engineer** | Docs testing, link checking, build verification | Broken link detection, visual regression testing, build status monitoring |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Docs platform migration or major version upgrade | All Writers, DevOps, Frontend Developers | Migration planning; potential downtime; author workflow changes |
| Docs build failing in CI (docs not deployable) | DevOps, All Writers | Docs site stale; fix or rollback needed before next release |
| Search index not updating (new docs not findable) | DevOps, All Writers | Docs discoverability broken; search reindex required |
| New OpenAPI version breaking auto-generated reference docs | Backend Developers, Technical Writers | API reference docs broken; spec fix or renderer update needed |
| Broken link report shows >5% external link rot | All Writers, SEO Specialist | Docs trust signal degrading; link fix sprint needed |
| Analytics show 50%+ of docs page views on pages older than 12 months | Technical Writers, Product Strategist | Content freshness audit needed; stale content archiving |
| Community contributor opens large docs PR (architecture decision records, new section) | DevRel, Technical Writers | Review coordination; style guide compliance check |
| New product/feature requiring new documentation section | Product Strategist, Technical Writers | IA update, navigation restructure, URL design |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Docs platform unreliable (>99% uptime not met, frequent build failures) | **CTO Advisor** + DevOps Lead | Platform reliability crisis; tooling evaluation or infrastructure investment |
| Docs site inaccessible to target audience (authentication wall blocking public docs) | **DevRel** + Product Strategist + CTO Advisor | Developer trust and SEO impact; strategic access decision |
| Migration from current docs platform to new platform proposed | **CTO Advisor** + All Writers + DevRel | 3-6 month migration; content, SEO, and workflow impact assessment needed |
| Docs CI/CD pipeline broken for >24 hours preventing any docs updates | **CTO Advisor** + DevOps Lead | Production incident; emergency fix or manual deploy required |
| Decision to deprecate docs-as-code in favor of SaaS platform (or vice versa) | **CTO Advisor** + All Writers + DevRel | Strategic tooling decision; workflow and culture impact |

### Route to Other Skills

| If the Request Is About | Route To |
|--------------------------|----------|
| Content authoring, style guides, editorial workflow | `technical-writer` |
| API spec quality, code annotation, SDK documentation generation | `backend-developer` |
| Developer content strategy, community docs, tutorials | `devrel-advocate` |
| Docs site UI design, component library, search UX | `frontend-developer` |
| CI/CD pipeline, hosting infrastructure, preview environments | `devops-engineer` |

## Proactive Triggers
<!-- QUICK: 30s — when to proactively notify stakeholders -->

| Trigger | Notify | Why |
|---------|--------|-----|
| Docs site availability drops below 99.5% in any 7-day window | DevOps, CTO Advisor | Platform reliability crisis; CDN or hosting investigation needed |
| Search analytics show >40% of queries returning zero results | Technical Writers, DevRel | Content gap discovery; new docs or redirects needed for common search terms |
| Freshness check flags >20% of docs as stale (>6 months unmodified) | All Writers, Engineering Leads | Content rot accelerating; dedicated docs sprint or ownership review needed |
| New major product version announced requiring documentation restructure | Product Strategist, Technical Writers, DevRel | IA redesign, versioning setup, and content migration planning required |
| Contributor docs PR rate drops >50% quarter-over-quarter | DevRel, Technical Writers | Community engagement declining; contribution barriers or motivation issues to investigate |
| "Was this helpful?" negative rate exceeds 40% on top-10 pages | Technical Writers, Product Strategist | High-traffic docs failing users; prioritized rewrites or restructuring needed |
| Build times exceed 5 minutes causing CI pipeline delays for writers | DevOps, All Writers | Author productivity impact; build optimization or caching improvements needed |

## Core Workflow
<!-- QUICK: 30s -- scan phase titles to understand the process -->
<!-- DEEP: 10+min -->
### Phase 1 (~15 min): Docs Health Audit
**Input:** Repository with `docs/` directory  
**Steps:** 1) Run health scan (broken links, stale pages, unowned docs, readability) 2) Generate JSON metrics 3) Identify top 3 issues by impact  
**Output:** Prioritized backlog of docs fixes

<!-- DEEP: 10+min -->
### Phase 2 (~30 min): SSG Selection & Setup
**Input:** Team skillset, content volume (pages), budget, versioning needs  
**Steps:** 1) Apply SSG decision tree 2) Scaffold site with chosen SSG 3) Configure build pipeline in CI 4) Verify deploy previews work  
**Output:** Docs site building from `main` with preview deploys on PRs

<!-- DEEP: 10+min -->
### Phase 3 (~20 min): Information Architecture Design
**Input:** Content inventory (all existing docs, API specs, guides)  
**Steps:** 1) Categorize using Diátaxis framework (tutorials, how-tos, reference, explanation) 2) Design navigation tree with max 4 levels 3) Configure search indexing 4) Set up landing page with quickstart path  
**Output:** Navigable, searchable docs site with clear content hierarchy

<!-- DEEP: 10+min -->
### Phase 4 (~15 min): Quality Gates
**Input:** Docs CI/CD pipeline  
**Steps:** 1) Add Vale prose linting with style guide 2) Add cspell with custom dictionary 3) Add link checking (internal + external) 4) Add frontmatter validation 5) Add code snippet validation if applicable  
**Output:** Every PR validated against quality standards before merge

<!-- DEEP: 10+min -->
### Phase 5 (~25 min): Maintenance Automation
**Input:** Live docs site with analytics  
**Steps:** 1) Set up freshness checks (flag pages >6 months stale) 2) Configure feedback widget on every page 3) Set up docs metrics dashboard (coverage, freshness, quality, usage) 4) Assign CODEOWNERS for docs paths  
**Output:** Self-maintaining docs system with automated quality monitoring


## Error Decoder
<!-- DEEP: 10+min -->

| Symptom | Root Cause | Fix | Lesson |
|---------|------------|-----|--------|
| Users couldn't complete onboarding despite 10K words of documentation | Docs were technically exhaustive but assumed domain knowledge; no getting-started guide for beginners | Write a 5-minute quickstart with copy-paste commands; add glossary section; use Diátaxis framework to separate tutorials from reference | Comprehensive != usable — measure time-to-first-success, not page count |
| Architecture decision records (ADRs) go stale within weeks of being written | ADRs written once and never revisited; no automated freshness checks; no ownership assigned | Set up automated freshness flagging (6 months stale = warning, 12 months = escalation); assign CODEOWNERS for every doc section | Documentation without maintenance is technical debt with a publish date |
| README.md hasn't been updated in 2 years — setup instructions are all wrong | README considered "done" at project launch; no process linking code changes to doc updates | Include README review in PR checklist; enforce README freshness in CI; link README to key architecture docs | A stale README is worse than no README — it actively misleads every new team member |
| API docs show parameters that don't exist in the running API | Docs generated once and manually edited; no automated sync with OpenAPI spec | Auto-generate API reference docs from OpenAPI/TypeScript types; validate docs against spec in CI; never hand-edit generated docs | Auto-generate or it will drift — hand-edited documentation always falls behind the code |
| Search returns irrelevant results, burying the right documentation page | No search tuning; pages lack metadata; duplicate content dilutes search quality | Configure proper frontmatter (title, description, tags); set up search analytics; deduplicate content; add redirects for old URLs | Great search is worth 10x more documentation pages — tune it like a product feature |

## Production Checklist
<!-- QUICK: 30s -- binary pass/fail items. All must pass. -->
- [ ] **[S1]**  SSG selected, configured, and building from `main` with CI/CD pipeline operational
- [ ] **[S2]**  Search configured: Algolia DocSearch or Pagefind with relevance-tuned results
- [ ] **[S3]**  Version dropdown visible in navbar; `latest` alias redirects to current version
- [ ] **[S4]**  Deprecation banners shown on outdated versions; older versions frozen
- [ ] **[S5]**  Broken link checking: internal (build-time error) + external (scheduled weekly)
- [ ] **[S6]**  Vale prose linting enforced in CI with custom terminology and tone rules
- [ ] **[S7]**  cspell spell checking with project-specific custom dictionary
- [ ] **[S8]**  Frontmatter validation: all pages have title, description, sidebar_position, tags
- [ ] **[S9]**  Readability scoring: pages flagged if Flesch-Kincaid > 12
- [ ] **[S10]**  Code snippet validation: extracted blocks compile/type-check in CI
- [ ] **[S11]**  Copy-paste button on every code block
- [ ] **[S12]**  Dark mode: automatic + manual toggle, all assets have dark variants
- [ ] **[S13]**  Mobile responsive: readable on 375px screens
- [ ] **[S14]**  i18n configured: language switcher, fallback to English, RTL support
- [ ] **[S15]**  Analytics: page views, search analytics, feedback widget on every page
- [ ] **[S16]**  Feedback funnel: "Was this helpful?" with automated alerts for low-rated pages
- [ ] **[S17]**  Docs ownership model: CODEOWNERS for docs paths, review rotation, freshness SLA
- [ ] **[S18]**  Freshness automation: stale doc flagging at 6 months, escalation at 12 months
- [ ] **[S19]**  Quickstart verified: time-to-first-success < 5 minutes
- [ ] **[S20]**  Docs metrics dashboard: coverage, freshness, quality, usage, contribution

## Scale Depth
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

## What Good Looks Like

> When documentation engineering is fully realized, the docs site builds, tests, and deploys through the same CI/CD pipeline as the product, broken links are caught before merge not after publish, style guide violations are enforced automatically so writers focus on content not formatting, search relevance is measured and tuned, freshness automation flags stale pages before users encounter them, and time-to-first-success for new users is under 5 minutes — docs are treated as a product with the same rigor as the software they describe.

## Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| Docs site hosting | Vercel + Docusaurus (free) or GitHub Pages (free) | Mintlify ($150/mo) or ReadMe ($99/mo) | Need managed hosting, API-first docs, or non-dev editors |
| API reference | Redoc or Scalar (free OSS) rendering OpenAPI spec | ReadMe or Mintlify (auto-sync, interactive console) | Need interactive API console, multi-language code samples, or analytics |
| Site search | Pagefind (free, local, no infra) or Lunr (free) | Algolia DocSearch (free for OSS, $500/mo+) | >500 pages, need faceted search, or want search query analytics |
| Diagram tooling | Mermaid (in-markdown, free, version-controlled) | Lucidchart ($7.95/user/mo) | Need collaborative whiteboarding or drag-and-drop editing |
| Prose linting | Vale (free OSS) + markdownlint (free) | Grammarly Business ($15/user/mo) | Need AI suggestions or non-dev writers who prefer GUI |
| Broken link checking | `lychee` (free CLI) run weekly in CI | Dedicated monitoring service | >1000 external links or need SLA on link checking |
| Docs analytics | Plausible ($9/mo) or Google Analytics 4 (free) | Algolia Analytics or custom | Need "was this helpful" aggregated reporting or search query insights |
| OpenAPI editor | VS Code + Redocly/Stoplight plugin (free) | Stoplight Studio ($99/mo) | Design-first workflow with non-dev collaborators |

**Annual docs tool budget by phase:** MVP: $0. Growth: $0-3K. Scale: $5K-50K.

## When NOT to Use This Skill (Overkill)

- **Solo developer, internal tool, no other users**: A docs site, ADR system, style guide, and freshness automation for a solo project is effort with zero audience. README + code comments = sufficient.
- **Pre-product-market-fit with 0 users**: Invest time building, not documenting. Users will tell you what needs explanation. Don't guess.
- **The codebase is a throwaway prototype**: Don't document code you plan to delete. If you're prototyping to validate, document the learnings, not the prototype.
- **Documentation is being used to avoid fixing UX**: "We'll document this confusing behavior" is an anti-pattern. If users keep asking the same question, fix the product.
- **Your entire product is a single function/API**: A 2-page doc site for 1 API endpoint is overkill. Put everything in the README.

## Token-Efficient Workflow

```
# Step 1: Docs health check
python3 scripts/docs_health.py --docs-dir docs --output json
# Returns: {"pages": 85, "broken_links_internal": 3, "broken_links_external": 1,
#           "pages_stale_6mo": 12, "pages_no_owner": 5, "readme_score": 8.5}

# Step 2: Decision tree → single action
# broken_links > 0 → Fix immediately
# pages_stale_6mo > 10% → Batch refresh sprint
# pages_no_owner > 0 → Assign via CODEOWNERS
# readme_score < 7 → Audit README against template

# Step 3: Quick verifications with exit codes
cd docs && npm run build                 # Exit code 0 = builds
lychee --base docs docs/                 # Exit code 0 = no broken links
vale docs/                               # Exit code 0 = no prose issues
npx @redocly/cli lint openapi.yaml       # Exit code 0 = spec valid

# Step 4: Verify improvement
python3 scripts/docs_health.py --docs-dir docs --compare last-week --output json
# Exit code 0 = all metrics improved, 1 = regressed
```

**Principle:** `docs_health.py` scans the docs directory, outputs JSON with metrics. Agent applies decision tree to exactly one action. Build, lint, and link checking all use exit codes. Never reads doc content into agent context (massive token waste).

## Best Practices
<!-- STANDARD: 3min -- rules extracted from production experience -->
1. **Automate setup, not docs:** If dev setup takes >30 min, fix the setup script — beautiful docs don't help if code won't run. One `./scripts/setup.sh` beats 50 pages of onboarding docs.
2. **Slack questions are your docs backlog:** Every repeated Slack answer belongs in docs. Search Slack for your top 10 answered questions — write those pages first.
3. **Generate API refs, never hand-write:** OpenAPI/SDL spec is the source of truth. Hand-written API docs go stale on the next deploy. Use Redoc or Scalar for rendering.
4. **Search before structure:** Users search, they don't browse. Tune Pagefind/Algolia relevance before reorganizing information architecture. Measure "search exit rate" (searches with no click-through).
5. **Vale in CI from day 1:** Style guide consistency is free if enforced automatically. One `.vale.ini` + custom terminology rules prevent bikeshedding over tone.
6. **Version only when you must:** Multi-version docs add maintenance burden. Until you have a v2 in production with users, don't version. When you do, keep current + N-1 only.
7. **Freshness automation is a feature:** A stale doc is worse than no doc. Flag pages >6 months without update. Escalate at 12 months. Set CODEOWNERS so every page has a human responsible.
8. **Quickstart is the most important page:** If a new user can't succeed in <5 minutes, they leave. Time-to-first-success is your #1 docs KPI. Test it on a fresh machine monthly.
9. **"Was this helpful?" on every page:** Binary feedback with optional text. Alert on pages with >50% "no" rate in last 30 days. This is your real-time quality signal.
10. **Eat your own dogfood:** Docs engineers must follow the same workflow they prescribe. If your team won't use the docs-as-code pipeline, no one else will.

## Anti-Patterns
<!-- STANDARD: 3min — patterns that predictably fail -->

| Anti-Pattern | Why It Fails | Correct Approach |
|---|---|---|
| Writing documentation as a separate phase after feature launch | Docs are perpetually late; pressure to ship without docs; knowledge gaps form immediately | Include documentation in the definition of done; docs PR must be part of the feature PR |
| Hand-editing auto-generated API reference docs | Edits are overwritten on next generation; drift between docs and spec accelerates | Never hand-edit generated docs; fix the source: OpenAPI annotations, code comments, or spec quality |
| Creating a single massive "Documentation" navigation category | Users can't find anything; cognitive overload; search becomes the only discovery path | Use Diátaxis to separate content by type; max 4 levels per tree; multiple entry points for different user journeys |
| Copying-pasting documentation between versions | Divergence inevitably occurs; fixes in one version don't propagate; maintenance multiplies | Version only content that changed; use partials/includes for shared content; keep versioned surface area minimal |
| Building docs site before understanding search behavior | Beautiful IA that nobody navigates; users search-first, browse-second | Analyze search logs before designing IA; validate navigation with card sorting; measure task completion rate |
| Requiring writers to learn git, markdown, YAML, and CI simultaneously | Writers spend >50% of time fighting tooling not writing; documentation velocity collapses | Provide templates, pre-configured VS Code workspaces, and one-click preview; invest in writer tooling experience |
| Treating docs as a dumping ground for all internal knowledge | Signal-to-noise ratio plummets; users can't distinguish canonical docs from rough notes | Separate internal knowledge base from public docs; curate what ships; maintain a quality bar for published content |
| Deploying docs site without analytics | Can't measure what's broken; no feedback loop; improvements based on intuition not data | Add page-level analytics, search analytics, and "was this helpful?" before launch; set baseline metrics immediately |

## References
<!-- QUICK: 30s -- links to deeper reading -->
- [Write the Docs -- Documentation Guide](https://www.writethedocs.org/guide/)
- [Docusaurus -- Documentation Site Generator](https://docusaurus.io/)
- [VitePress -- Static Site Generator](https://vitepress.dev/)
- [Mintlify -- Modern Documentation](https://mintlify.com/)
- [Nextra -- Next.js Documentation](https://nextra.site/)
- [GitBook -- Documentation Platform](https://www.gitbook.com/)
- [ReadTheDocs -- Documentation Hosting](https://readthedocs.org/)
- [Hugo -- Static Site Generator](https://gohugo.io/)
- [Diataxis -- Systematic Documentation Framework](https://diataxis.fr/)
- [Mermaid -- Diagramming and Charting](https://mermaid.js.org/)
- [Structurizr -- C4 Model Diagrams as Code](https://structurizr.com/)
- [Vale -- Prose Linter](https://vale.sh/)
- [cspell -- Spell Checker](https://cspell.org/)
- [Algolia DocSearch](https://docsearch.algolia.com/)
- [Pagefind -- Static Search](https://pagefind.app/)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Spectral -- OpenAPI Linter](https://stoplight.io/open-source/spectral)
- [Scalar -- API Reference](https://scalar.com/)
- [Crowdin -- Translation Management](https://crowdin.com/)
- [adr-tools -- ADR Management](https://github.com/npryce/adr-tools)
- [Google -- Technical Writing Courses](https://developers.google.com/tech-writing)
