# Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| Docs site | Docusaurus or VitePress on Vercel (free) + markdown in repo | Mintlify ($150/mo starter) or ReadMe ($99/mo) | Need managed hosting, API-first docs, or non-dev team editing docs |
| API reference | Redoc (free OSS) or Swagger UI (free) rendered from OpenAPI spec | ReadMe or Mintlify (auto-sync from OpenAPI, better UX) | Need interactive API console, code samples in multiple languages, or analytics |
| Doc search | Pagefind (free, local search) or Lunr (free) | Algolia DocSearch (free for OSS, $500/mo+ otherwise) | >500 docs pages, need faceted search, or analytics on search queries |
| Diagramming | Mermaid (free, in-markdown) | Lucidchart ($7.95/user/mo) or Excalidraw (free) | Need collaborative whiteboarding or non-code-generated diagrams |
| Prose linting | Vale (free OSS) + markdownlint (free) | WriteGood or Grammarly Business ($15/user/mo) | Need AI-powered suggestions or non-dev writers who prefer GUI |
| Broken link checking | `lychee` or `broken-link-checker` (free CLI) | Drone or dedicated service | >1000 external links or need scheduled weekly checks with alerts |
| OpenAPI editor | Swagger Editor (free, web) or VS Code OpenAPI plugin | Stoplight Studio ($99/mo) or Postman Enterprise | Design-first API workflow with non-dev collaborators |
| Analytics on docs | Google Analytics 4 (free) or Plausible ($9/mo) | Algolia Analytics or custom | Need search query analytics or "was this helpful" aggregated reporting |

**Annual docs tool budget by phase:** MVP: $0. Growth: $0-3K. Scale: $10K-100K.
