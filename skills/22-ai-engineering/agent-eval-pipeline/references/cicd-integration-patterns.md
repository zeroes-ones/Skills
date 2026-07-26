# CI/CD Integration Patterns for Agent Evals

## GitHub Actions Example
```yaml
name: Agent Eval Suite
on:
  pull_request:
    paths: ['skills/**/SKILL.md']
  push:
    branches: [main]

jobs:
  static-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: bash scripts/validate-skills.sh

  unit-evals:
    needs: static-checks
    runs-on: ubuntu-latest
    strategy:
      matrix:
        skill: ${{ fromJSON(needs.discover-skills.outputs.changed) }}
    steps:
      - run: python scripts/run-evals.py --level unit --skill ${{ matrix.skill }}

  integration-evals:
    needs: unit-evals
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - run: python scripts/run-evals.py --level integration
```

## Quality Gates
| Stage | Gate | Block Condition |
|-------|------|-----------------|
| PR | Static checks | Any failure |
| PR | Unit evals | > 1 test case regression |
| Merge | Integration | > 5% metric regression |
| Release | Full suite | Any critical security fail |
| Post-deploy | Sampling | > 2σ drift on any metric |
