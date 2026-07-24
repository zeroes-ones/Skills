# Monorepo Scaffolding

> Package generation with nx generate, turbo gen, plop.js, and custom generators.

## Nx Generators

```bash
# Built-in generators
nx generate @nx/js:library my-lib --directory=packages/my-lib
nx generate @nx/react:component MyComponent --directory=libs/ui/src

# Custom generator config in nx.json
{
  "generators": {
    "@nx/js:library": {
      "bundler": "swc",
      "unitTestRunner": "jest"
    }
  }
}

# Local workspace generators in tools/generators/
nx generate @org/generators:microservice --name=user-service
```

## Turborepo Generators

```bash
# turbo gen with plop.js
# turbo/generators/plopfile.js
turbo gen workspace --name my-package
```

## Plop.js

```javascript
// plopfile.js
module.exports = function (plop) {
  plop.setGenerator('package', {
    description: 'Create a new package',
    prompts: [
      { type: 'input', name: 'name', message: 'Package name' },
      { type: 'list', name: 'type', choices: ['library', 'service', 'app'] }
    ],
    actions: [
      { type: 'addMany', destination: 'packages/{{name}}', templateFiles: 'templates/package/**' }
    ]
  });
};
```

## Integration Points

* Workspace registration: new package must be added to workspace config (tsconfig paths, nx.json)
* CI integration: new package should auto-trigger appropriate CI jobs
* Dependency management: shared dependencies versioned at workspace root
