# Static Site Generators (Decision Matrix)

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
