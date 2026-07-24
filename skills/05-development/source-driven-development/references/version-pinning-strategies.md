# Version Pinning Strategies

## The Golden Rule

**Read docs for the exact version you run. Run the exact version you document.**

## Pin by Ecosystem

### JavaScript/TypeScript (npm/yarn/pnpm)

```json
{
  "dependencies": {
    "react": "18.3.1",
    "next": "14.2.15"
  }
}
```
- **Remove `^` and `~`** from production dependencies. Use exact versions.
- Use `npm ls <pkg> --depth=0` to verify installed version matches docs.
- Add `engine-strict: true` in `.npmrc` to enforce `engines` field.

### Python (pip/Poetry/uv)

```txt
# requirements.txt — exact pins
fastapi==0.115.0
sqlalchemy==2.0.35
```
- Use `==` not `>=`. Pin transitive deps with `pip freeze`.
- Run `pip check` in CI to detect version conflicts.
- For Poetry: `poetry.lock` IS the pin — never delete it.

### Go

```go
require (
    github.com/gin-gonic/gin v1.9.1
)
```
- `go.sum` pins exact hashes. Commit it.
- Use `go list -m all` to audit dependency tree.
- `GONOSUMDB` and `GONOSUMCHECK` should never be set in CI.

### Rust (Cargo)

```toml
[dependencies]
tokio = { version = "=1.40.0", features = ["full"] }
```
- Use `=` prefix for exact pin. `Cargo.lock` IS the pin for binaries.
- Run `cargo update --dry-run` before every upgrade to preview impact.

## CI Version Verification

```yaml
# GitHub Actions: verify installed versions match documented versions
- name: Version Audit
  run: |
    npm ls react --depth=0 | grep "18.3.1" || (echo "React version mismatch! Docs assume 18.3.1" && exit 1)
    npm ls next --depth=0 | grep "14.2.15" || (echo "Next.js version mismatch!" && exit 1)
```

## Version-Citation Drift Check

```bash
#!/bin/bash
# Extract all cited versions from source files
grep -rohP 'Version:\s*\K[^]]+' src/ | sort -u > /tmp/cited-versions.txt

# Extract all installed versions from lockfile
npm ls --depth=0 --json | jq -r '.dependencies | to_entries[] | "\(.key)@\(.value.version)"' > /tmp/installed-versions.txt

# Diff them
diff <(sort /tmp/cited-versions.txt) <(sort /tmp/installed-versions.txt)
```

## When Pins Don't Match Docs

1. Docs are for a newer version → check changelog for backward compat. If safe, upgrade. If breaking, find older docs.
2. Docs are for an older version → you're ahead of docs. Find release notes for your version. Flag undocumented APIs.
3. No versioned docs exist → pin to a git tag. Cite source code at that tag.
