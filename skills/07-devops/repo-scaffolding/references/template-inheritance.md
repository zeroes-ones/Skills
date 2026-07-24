# Template Inheritance

> The 4-layer hierarchy: Base -> Language -> Framework -> Team.

## Layer Definitions

### Level 0: Org Base Template
* **Audience:** Every repo in the organization
* **Content:** CI workflow skeleton, SECURITY.md, CODEOWNERS, .gitignore, LICENSE
* **Override rule:** Downstream can ADD but never REMOVE files from this layer
* **Example:** Adding a .dockerignore is fine; removing SECURITY.md is not

### Level 1: Language Template (extends Base)
* **Audience:** All repos in a specific language
* **Content:** Language configs (tsconfig, pyproject.toml, go.mod), linter, formatter, test framework
* **Override rule:** Can add language-specific configs but cannot weaken base security rules

### Level 2: Framework Template (extends Language)
* **Audience:** Repos using a specific framework
* **Content:** Framework configs, directory structure, sample code
* **Override rule:** Can add framework-specific tooling but cannot remove language-level lint rules

### Level 3: Team Overlay (extends Framework, optional)
* **Audience:** A specific team
* **Content:** Team-preferred libraries, custom scripts, local dev tooling
* **Override rule:** MUST NOT weaken any rule from Levels 0-2. Security team can veto.

## Implementation Pattern

```yaml
# copier.yaml example for multi-layer inheritance
_base:
  source: github.com/org/template-base
  version: v2.0.0

_language:
  source: github.com/org/template-typescript
  version: v1.5.0

_framework:
  source: github.com/org/template-nextjs
  version: v1.2.0
```
