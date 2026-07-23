# Search

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
