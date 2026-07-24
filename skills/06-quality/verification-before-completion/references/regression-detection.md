# Regression Detection

## Purpose
Prove a bug fix doesn't break existing functionality. The fix is incomplete if it introduces regressions.

## Scope Selection
1. **Direct scope**: Run the test suite for the module containing the fix.
2. **Dependency scope**: Identify all files that import from the changed file.
   ```bash
   grep -r "from '\.\/changed-file'" --include="*.ts" --include="*.js" src/
   ```
   Run the test suites for every dependent module.
3. **Shared utility scope**: If the change is in a shared utility or library, run the FULL project test suite.
4. **Integration scope**: Run integration/E2E tests that exercise the affected code path.

## Execution
- Run tests in the same order as CI to catch ordering-dependent failures
- Run with the same flags CI uses (e.g., `--runInBand` for Jest, `--fail-fast` for Mocha)
- Check for new warnings, deprecation notices, or console errors — not just test failures

## Regression Patterns
- **Silent breakage**: Test passes but behavior is different (caught by strong assertions only)
- **Ordering-dependent**: Tests pass in isolation but fail in a specific order
- **Environment-dependent**: Tests pass locally but fail in CI (Node version, OS, locale)
- **Data-dependent**: Tests pass with fresh data but fail with production-like data volumes

## Gate
Any new test failure after the fix is a regression and blocks status transition.
