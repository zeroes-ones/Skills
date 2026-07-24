# Submodule Disaster Recovery Playbook

## Disaster 1: Detached HEAD After Update

Symptoms: `git status` in submodule shows "HEAD detached at"
Root cause: Submodule not configured to track a branch

```bash
# Temporary fix
cd path/to/submodule
git checkout main

# Permanent fix
git config -f ../.gitmodules submodule.path/to/submodule.branch main
git submodule update --remote -- path/to/submodule
```

## Disaster 2: Merge Conflict in Submodule Pointer

Symptoms: `git merge` shows conflict on submodule path
Root cause: Two branches updated submodule to different commit SHAs

```bash
# Accept one side
git checkout --theirs -- path/to/submodule
# OR
git checkout --ours -- path/to/submodule

# Stage the resolution
git add path/to/submodule

# Verify the chosen SHA
cd path/to/submodule && git log -1 --oneline
```

## Disaster 3: "No url found for submodule path"

Symptoms: `git submodule update` fails with URL error
Root cause: .gitmodules missing, corrupt, or .git/config out of sync

```bash
# Sync .git/config from .gitmodules
git submodule sync --recursive

# If .gitmodules is corrupted, restore from known-good branch
git checkout main -- .gitmodules

# Then re-initialize
git submodule update --init --recursive
```

## Disaster 4: Submodule Points to Non-Existent Commit

Symptoms: "fatal: reference is not a tree" when checking out submodule
Root cause: Upstream repo was force-pushed, pinned SHA no longer exists

```bash
cd path/to/submodule
git fetch origin
git log origin/main --oneline | head -20
# Manually identify the equivalent commit in new history
git checkout <new-commit-sha>
cd ../..
git add path/to/submodule
git commit -m "Update submodule pointer after upstream rewrite"
```

## Prevention Checklist

- Never force-push to repos used as submodules
- Configure branch tracking: `branch = main` in .gitmodules
- Add CI health check: `git submodule status --recursive`
- Monthly audit: verify all pinned SHAs are reachable
