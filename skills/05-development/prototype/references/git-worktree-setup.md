# Git Worktree Setup for Prototype Isolation

## Quick Start
```bash
# Create isolated worktree from current repo state
git worktree add --detach ../proto-$(date +%Y-%m-%d)-[topic]

# Navigate to the isolated directory
cd ../proto-$(date +%Y-%m-%d)-[topic]

# All changes here are isolated from the main working tree
# No .git directory sharing issues — each worktree has its own index

# When done, return to main repo and remove
cd /path/to/main-repo
git worktree remove ../proto-$(date +%Y-%m-%d)-[topic]
```

## Important Notes
- `--detach` prevents creating a branch. Prototype commits should not survive.
- Worktree shares the .git directory (objects, refs) but has its own index and HEAD.
- `git worktree list` shows all worktrees. Verify cleanup.

## Cleanup Verification
```bash
# Should show only the main working tree
git worktree list

# Verify prototype directory is gone
ls ../proto-* 2>&1 | grep "No such file"
```

## Handling Uncommitted Changes
If you accidentally have uncommitted changes in the main tree while creating a worktree:
- `git stash` in main tree first.
- Create worktree.
- `git stash pop` in main tree after worktree is ready.
