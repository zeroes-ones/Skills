# Repository Structure

### Structural Patterns

| Pattern | Layout | When to Use |
|---------|--------|-------------|
| **Package-first** | `packages/*` | Small–medium repos, simple ownership. Turborepo's default model. |
| **Domain-first** | `teams/core/`, `teams/billing/`, `teams/shared/` | Large orgs with clear team ownership. Each team owns their domain subtree. |
| **Hybrid (most common)** | `apps/*`, `packages/*`, `tools/*` | Teams of all sizes. Separates deployables (apps) from libraries (packages) from tooling (tools). |

### Hybrid Structure — Deep Dive

```
my-monorepo/
├── apps/
│   ├── web/                # Next.js app
│   │   └── package.json    # "name": "@myorg/web"
│   ├── api/                # Express/Fastify API
│   │   └── package.json    # "name": "@myorg/api"
│   └── mobile/             # React Native app
│       └── package.json
├── packages/
│   ├── ui/                 # Shared UI component library
│   │   └── package.json    # "name": "@myorg/ui"
│   ├── utils/              # Shared utility functions
│   │   └── package.json    # "name": "@myorg/utils"
│   ├── types/              # Shared TypeScript types/interfaces
│   │   └── package.json    # "name": "@myorg/types"
│   └── config/
│       ├── typescript-config/
│       ├── eslint-config/
│       ├── prettier-config/
│       └── jest-config/
├── tools/
│   ├── generators/         # Plop or custom code generators
│   └── scripts/            # CI helper scripts
├── pnpm-workspace.yaml
├── turbo.json
├── package.json            # Root — only dev tooling
└── .github/workflows/
```

### Package Entry Points — The `exports` Field

Do NOT rely on `main` + `module` alone. Use the `exports` field for proper encapsulation:

```jsonc
// packages/ui/package.json
{
  "name": "@myorg/ui",
  "type": "module",
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    },
    "./button": {
      "import": "./dist/button/index.mjs",
      "require": "./dist/button/index.js",
      "types": "./dist/button/index.d.ts"
    },
    "./styles.css": "./dist/styles.css"
  },
  // Anything NOT in exports is private — consumers cannot deep-import it
  "files": ["dist"],
  "publishConfig": {
    "access": "public"
  }
}
```

### Barrel Exports — Public API Surface

```typescript
// packages/ui/src/index.ts — public barrel
export { Button } from './button';
export { Card } from './card';
export { ThemeProvider } from './theme';
// NOT exported: internal hooks, utils, types — these are implementation details

// packages/ui/src/index.test.ts — barrel test ensures nothing is broken
import * as publicApi from './index';
describe('@myorg/ui public API', () => {
  it('should export Button', () => expect(publicApi.Button).toBeDefined());
  it('should export Card', () => expect(publicApi.Card).toBeDefined());
});
```

### Shared Config Packages

```jsonc
// packages/config/typescript-config/package.json
{
  "name": "@myorg/typescript-config",
  "version": "0.0.0",
  "private": true,
  "files": ["./base.json", "./nextjs.json", "./react-library.json"]
}
```

- **`@myorg/typescript-config/base.json`**: `strict: true`, `exactOptionalPropertyTypes: true`, `noUncheckedIndexedAccess: true`
- **`@myorg/typescript-config/nextjs.json`**: extends `base.json`, adds `"module": "ESNext"`, `"jsx": "preserve"`
- **`@myorg/eslint-config`**: extends `eslint-config-next`, `eslint-config-prettier`, with `@nx/enforce-module-boundaries` rule
- **`@myorg/prettier-config`**: single `module.exports = { semi: true, singleQuote: true, trailingComma: 'all' }`
- **`@myorg/jest-config`**: `jest-preset.js` exporting `{ testEnvironment: 'node', transform: { '^.+\\.ts$': 'ts-jest' } }`

All packages extend these:

```jsonc
// apps/web/package.json
{
  "prettier": "@myorg/prettier-config",
  "jest": { "preset": "@myorg/jest-config" }
}
// tsconfig.json
{
  "extends": "@myorg/typescript-config/nextjs.json"
}
// .eslintrc.js
module.exports = {
  root: true,
  extends: ["@myorg/eslint-config/next"]
};
```

### Internal Libraries vs Published Packages

| Category | Private | Published | Example |
|----------|---------|-----------|---------|
| **Shared config** | ✅ private | ❌ | `@myorg/typescript-config` |
| **Internal types** | ✅ private | ❌ | `@myorg/types` |
| **Shared utils** | ✅ private (or published) | depends | `@myorg/utils` — publish if other orgs use it |
| **UI components** | ⚠️ start private, publish when mature | ✅ eventually | `@myorg/ui` → `@acme/ui` |
| **SaaS platform libs** | ✅ private | ❌ | Business logic, API client wrappers |

**Rule**: Keep a package private until an external consumer explicitly needs it. Publishing prematurely creates a maintenance contract. Use `"private": true` and `"publishConfig": { "access": "restricted" }` for internal-only packages.
