# Evidence Documentation

## Purpose
Create an auditable record of verification that survives team turnover and memory decay.

## Minimum Evidence Bar
Every closed issue or merged PR must include:

1. **Before evidence**: Screenshot, log, or test output showing the bug BEFORE the fix.
   - Must include timestamp and environment identifier.
   - Must match the EXACT reproduction case from the bug report.

2. **After evidence**: Screenshot, log, or test output showing correct behavior AFTER the fix.
   - Must show the same scenario as the "before" evidence.
   - Must clearly demonstrate the expected behavior.

3. **Test suite evidence**: Output from the regression test suite showing all tests passing.
   - Include the test command used and the pass/fail summary.
   - Link to the CI run if available.

## Documentation Format
```markdown
**Verified on [DATE] against reproduction case [LINK].**

BEFORE (reproduced):
[embedded screenshot or code block with failure output]

AFTER (verified fixed):
[embedded screenshot or code block with success output]

Regression suite: [N] tests passing, [M] failing. [CI link]
```

## Gate
No evidence = no verification. No verification = no closure.
