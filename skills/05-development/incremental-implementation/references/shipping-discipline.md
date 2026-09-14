# Shipping Discipline

Every commit leaves the branch deployable. That constraint is what makes incremental delivery safe.

## The rules

1. **Green at every commit.** A red commit is a stopped line.
2. **One logical change per commit.** Bundling makes rollback impossible.
3. **Rollback-friendly.** Each change can be reverted without unwinding unrelated work.
4. **Deployable default.** Anything user-visible sits behind a flag.
5. **Reversible migrations.** Expand → migrate → contract; never a destructive change in one step.

## The commit-as-save-point pattern

A commit is a place you can return to. If the work after it is wrong, reverting costs one operation
rather than an archaeology exercise.

## Failure modes of shipping discipline

- **Big-bang merge.** A long-lived branch that lands as one large change; rollback now means
  unwinding everything.
- **Red commits merged forward.** The failure is inherited by everyone who pulls.
- **Irreversible migration.** A dropped column ships before the data is proven unneeded.
- **Untested rollback.** The revert path is assumed to work and has never been run.
- **Flag debt.** Removed-code tasks are never emitted, so the temporary becomes permanent.
