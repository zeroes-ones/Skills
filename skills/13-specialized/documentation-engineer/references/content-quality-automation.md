# Content Quality Automation

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
