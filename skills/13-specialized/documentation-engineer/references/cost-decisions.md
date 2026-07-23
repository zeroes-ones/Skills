# Cost-Effective Decision Table

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
