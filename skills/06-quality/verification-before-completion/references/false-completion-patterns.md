# False Completion Patterns

## Purpose
Identify recurring patterns where work is marked "done" without actual verification. Learn to recognize these patterns before they recur.

## Pattern Catalog

### Pattern 1: The "Obvious Fix" Close
**Signature**: Issue closed within minutes of a commit with no verification comment.
**Reality**: The developer assumed the fix was correct because it was "simple." No reproduction, no test.
**Detection**: `time(issue.closed) - time(commit.pushed) < 15 minutes` AND `closing_comment.length < 50 chars`

### Pattern 2: The "Works for Me" Dismissal
**Signature**: Issue closed with "Cannot reproduce" but no investigation into environment differences.
**Reality**: The bug is environment-specific. It still exists for the reporter.
**Detection**: Closing comment contains "works for me" or "cannot reproduce" AND no follow-up questions asked.

### Pattern 3: The "Sprint-End Sweep"
**Signature**: Multiple issues moved to "Done" on the last day of a sprint without linked verification.
**Reality**: Status updated to meet sprint metrics, not because verification happened.
**Detection**: `count(status_change_to_done on sprint_last_day) > average * 3`

### Pattern 4: The "CI Green = Done" Fallacy
**Signature**: Issue closed with only a CI link as evidence, no reproduction case re-run.
**Reality**: CI passing means existing tests pass. It doesn't mean the specific bug is fixed.
**Detection**: Closing comment contains CI link but no "BEFORE/AFTER" evidence.

### Pattern 5: The "Silent Close"
**Signature**: Issue closed with no comment at all, or only "Fixed in [commit]."
**Reality**: No verification whatsoever. The issue may or may not be fixed.
**Detection**: Issue status = closed AND closing_comment is null or only contains a commit hash.
