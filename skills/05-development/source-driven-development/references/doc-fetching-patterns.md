# Documentation Fetching Patterns

## Pattern A: Static Doc Sites (curl)

```bash
# Direct curl — works for SSR docs and sites that serve raw HTML
curl -sL "https://docs.example.com/api/v2/users/create" | head -200

# With custom headers for sites that block curl user-agent
curl -sL -H "User-Agent: Mozilla/5.0" "https://nodejs.org/api/fs.html#fsreadfilepath-options-callback"

# Extract specific section using CSS selector (requires pup or similar)
curl -sL "https://react.dev/reference/react/useEffect" | pup 'article json{}' | jq '.'
```

## Pattern B: Package Registries (npm, PyPI, crates.io)

```bash
# npm registry metadata (includes README, version history)
curl -sL "https://registry.npmjs.org/react" | jq '.["dist-tags"]'

# PyPI JSON API
curl -sL "https://pypi.org/pypi/requests/json" | jq '.info.version'

# Go module proxy
curl -sL "https://proxy.golang.org/github.com/gin-gonic/gin/@v/v1.9.1.mod"
```

## Pattern C: GitHub Source (gh CLI)

```bash
# Fetch specific file at a tag
gh api repos/owner/repo/contents/src/api/users.ts?ref=v2.3.0 --jq '.content' | base64 -d

# Read release notes
gh release view v2.3.0 --repo owner/repo --json body,name,tagName

# Compare tags for migration impact
gh api repos/owner/repo/compare/v1.0.0...v2.0.0 --jq '.files[].filename'
```

## Pattern D: Web Fetch Tool

```
# Use the web_fetch tool for JS-heavy sites or clean extraction
web_fetch("https://tanstack.com/query/v5/docs/reference/useQuery", max_length=5000)

# For paginated content
web_fetch("https://docs.example.com/api/v2/endpoints?page=2", start_index=5000)
```

## Pattern E: Caniuse / Node.green API

```bash
# caniuse data for a feature
curl -sL "https://api.caniuse.com/v2/feature/fetch" | jq '.data.stats'

# Node.green (scrape — no public API) — use web_fetch instead
web_fetch("https://node.green/#ES2023-array-find-from-last")
```

## Pattern F: MDN Browser Compat Data (npm package)

```bash
npm install @mdn/browser-compat-data
node -e "const bcd = require('@mdn/browser-compat-data'); console.log(JSON.stringify(bcd.api.AbortController, null, 2))"
```

## Verification After Fetch

Always validate:
1. Does the URL include a version identifier?
2. Is the "last updated" date acceptable relative to the installed version?
3. Does the fetched content contain the specific API signature you need?
4. If fetching source code, is it at the exact tag/SHA in your lockfile?
