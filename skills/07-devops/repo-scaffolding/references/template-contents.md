# Template Contents

> Detailed specification of what belongs in each template level.

## Non-Negotiable Files (Every Template)

| File | Purpose | Validation |
|------|---------|------------|
| `.github/workflows/ci.yml` | CI pipeline: lint, test, build | Must pass on empty repo |
| `SECURITY.md` | Vulnerability reporting process | Must include contact method |
| `CODEOWNERS` | Default code owners | Must have at least one owner |
| `.gitignore` | Language-appropriate ignores | Must cover build artifacts, deps |
| `LICENSE` | Org-standard license | MIT or Apache 2.0 typical |
| `README.md` | Project readme template | Setup, deploy, team, badges |

## Language-Specific Additions

### TypeScript/JavaScript
- `tsconfig.json` (strict mode enabled)
- `eslint.config.js` or `.eslintrc.js`
- `.prettierrc`
- `jest.config.js` or `vitest.config.js`
- `package.json` with placeholder name/description

### Python
- `pyproject.toml` ([project], [tool.ruff], [tool.pytest], [tool.mypy])
- `Makefile` (setup, test, lint, format targets)

### Go
- `go.mod` (module placeholder)
- `.golangci.yml`
- `Makefile` (build, test, lint targets)

## Framework-Specific Additions

### React
- `vite.config.ts` or webpack config
- `tailwind.config.js` (if applicable)
- `src/App.tsx` (minimal component)
- Test setup (testing-library)

### Next.js
- `next.config.js`
- `app/layout.tsx`, `app/page.tsx`
- `middleware.ts` (empty stub)
