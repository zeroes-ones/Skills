# Reproduction Verification Guide

## Purpose
Ensure every bug fix is verified against the EXACT reproduction case from the original bug report. Generic testing is not verification.

## Process
1. **Locate** the reproduction steps in the bug report. Look for sections labeled "Steps to Reproduce," "STR," "Reproduction," or numbered lists.
2. **Execute** every step exactly as written. Do not skip, combine, abbreviate, or "optimize" steps. The reporter's steps are the specification.
3. **Document** the failure state: screenshot, log output, or test failure with timestamp and environment details.
4. **Apply** the fix and re-execute the exact same steps. Document the success state.
5. **Attach** both failure and success evidence to the issue or PR before closing.

## Common Pitfalls
- "Optimizing" steps (e.g., skipping "clear cache" because "that shouldn't matter")
- Using different input data than the reporter used
- Testing in a different environment (browser, OS, dependency versions)
- Accepting "close enough" output that doesn't match expected behavior

## Gate
Cannot close any issue without before-and-after evidence from the exact reproduction case.
