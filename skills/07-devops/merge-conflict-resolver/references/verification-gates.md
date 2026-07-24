# Verification Gates

Per-hunk and per-phase verification gates: build checks, test selection, semantic validation, and CI pipeline integration.

## Per-Hunk Gates

1. **Compile check**: Build the affected module. Must succeed before proceeding.
2. **Unit test check**: Run tests for the affected module. All must pass.
3. **Lint check**: Run linter on the resolved file. No new warnings.

## Per-Phase Gates

After all hunks in a file are resolved:
- Full module build
- Full module test suite
- Integration tests if module has upstream/downstream dependencies

## Final Gates

After all conflicts resolved:
- Full project build
- Full test suite
- Conflict marker scan (grep for `<<<<<<<` across all tracked files)
- Resolution log completeness check

## CI Pipeline Integration

If available, run the full CI pipeline locally: `act` for GitHub Actions, `gitlab-runner exec` for GitLab CI, or equivalent.
