# Docs-as-Code

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
