# Golden Repo Pattern

> One canonical template per language/framework that all new repos derive from.

## Overview

The golden repo pattern is the simplest and most effective template strategy: maintain one repository that serves as the definitive template for a specific language/framework combination. Every new repo of that type is created from this golden repo, ensuring consistency across the organization.

## Structure

```
template-python-service/
  .github/
    workflows/
      ci.yml              # CI pipeline: lint, test, build
      security-scan.yml    # SAST, dependency scanning
  SECURITY.md              # Security policy and reporting
  CODEOWNERS               # Default code owners
  .gitignore               # Python-specific gitignore
  LICENSE                  # Org standard license
  README.md                # Template README with setup instructions
  pyproject.toml            # Python project config (ruff, pytest, mypy)
  src/
    __init__.py             # Package init
    main.py                 # Hello-world entry point
  tests/
    __init__.py
    test_main.py            # Passing test
  .env.example              # Documented environment variables
  renovate.json             # Dependency update configuration
```

## When to Use

* Small to medium organizations (<20 repos)
* Limited language/framework diversity (<5 stacks)
* Teams want simplicity over flexibility

## Governance

* **Owner:** Platform team or designated template maintainer
* **Update cadence:** Monthly for dependencies, quarterly for structural changes
* **Review process:** Any PR to the golden repo requires 2 approvals
* **Testing:** Automated scaffold + CI test runs on every PR
