# Template Engines

> Comparison matrix and selection guide for repo scaffolding tools.

## Comparison Matrix

| Engine | Language | Post-Create Updates | Template Variables | Learning Curve | Best For |
|--------|----------|-------------------|--------------------|----------------|----------|
| GitHub Templates | Any | No | No | Minimal | First template, small orgs |
| Cookiecutter | Python | No | Jinja2 | Low | Python-heavy orgs |
| Copier | Python | Yes (built-in) | Jinja2 | Medium | Python orgs needing sync |
| Degit | JS/TS | No | No | Low | Custom CLI building block |
| Yeoman | JS/TS | No | EJS | High | Legacy Node.js projects |
| Custom CLI | Any | Custom | Custom | High | Large polyglot orgs |

## Selection Flow

1. Is this your first template? -> GitHub Templates
2. Need template variables? -> Cookiecutter or Copier
3. Need downstream updates? -> Copier or Custom CLI
4. Polyglot org with 50+ repos? -> Custom CLI
5. Monorepo? -> nx generate, turbo gen, or plop.js (see monorepo-scaffolding.md)

## Migration Paths

* GitHub Template -> Cookiecutter: Convert repo to cookiecutter template, add cookiecutter.json
* Cookiecutter -> Copier: Create copier.yaml, migrate hooks to Copier API
* Any -> Custom CLI: Extract template content, wrap in CLI with string replacement
