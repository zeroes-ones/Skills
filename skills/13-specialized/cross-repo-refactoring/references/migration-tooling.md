# Migration Tooling: Codemods and Automated PRs

## Tool Selection Matrix

| Tool | Best For | Languages | Learning Curve |
|------|----------|-----------|---------------|
| jscodeshift | JS/TS AST transforms | JavaScript, TypeScript | Medium |
| comby | Structural search-replace | Any language | Low |
| ast-grep | AST-aware structural search | 20+ languages | Low-Medium |
| semgrep | Pattern-based search | 30+ languages | Low |

## jscodeshift Codemod Example

```javascript
// transform.js — Rename oldFunction to newFunction
export default function transformer(file, api) {
  const j = api.jscodeshift;
  const root = j(file.source);

  return root
    .find(j.CallExpression, {
      callee: { name: 'oldFunction' }
    })
    .replaceWith(path => {
      return j.callExpression(
        j.identifier('newFunction'),
        path.node.arguments
      );
    })
    .toSource();
}
```

## comby Example

```bash
# Rename function across all files
comby 'oldFunction(:[args])' 'newFunction(:[args])' .ts -in-place

# With type-aware pattern
comby 'import { oldFunction } from :[path]' 'import { newFunction } from :[path]' .ts -in-place
```

## Test Fixtures Pattern

```
__testfixtures__/
  input.js       # Code BEFORE codemod
  output.js      # Expected AFTER codemod
  negative.js    # Should NOT be transformed
  edge-case-1.js # Named arguments, default params
  edge-case-2.js # Nested calls, destructuring
```

## Automated PR Generation

```bash
#!/bin/bash
# Generate migration PRs for a list of repos
REPOS=("repo-a" "repo-b" "repo-c")
for repo in "${REPOS[@]}"; do
  git clone "https://github.com/org/${repo}.git" "work/${repo}"
  cd "work/${repo}"
  jscodeshift -t ../../transform.js src/
  git add -A && git commit -m "Migrate oldFunction -> newFunction"
  gh pr create --title "Migrate to newFunction" --body "Automated migration. See migration guide."
  cd ../..
done
```
