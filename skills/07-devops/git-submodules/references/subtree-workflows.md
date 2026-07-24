# Git Subtree Workflows

## One-Way Sync (Inner Source to Outer Repo)

```bash
# Add subtree (one-time)
git subtree add --prefix=shared/lib https://github.com/org/lib.git main --squash

# Pull updates from upstream
git subtree pull --prefix=shared/lib https://github.com/org/lib.git main --squash

# Make local changes in shared/lib/ and commit normally
# Local changes survive subtree pulls (merged, not overwritten)
```

## Bidirectional Sync (Push Changes Back)

```bash
# Make changes in shared/lib/ within the parent repo
cd shared/lib
echo "// New feature" >> feature.ts
git add feature.ts
git commit -m "Add feature to shared lib"
cd ../..

# Push changes back to subtree remote
git subtree push --prefix=shared/lib https://github.com/org/lib.git main

# WARNING: This rewrites history of the subtree.
# When pulling from remote later, conflicts are likely.
# Use bidirectional subtree only when truly necessary.
```

## Splitting a Subtree into a New Repo

```bash
# Extract subtree history into a branch
git subtree split --prefix=shared/lib -b lib-extract

# Push to new remote
git remote add lib-origin https://github.com/org/new-lib.git
git push lib-origin lib-extract:main

# Clean up
git branch -D lib-extract
```

## When NOT to Use Subtree

- Bidirectional sharing with frequent updates (merge conflicts compound)
- More than 3 subtree prefixes (history gets unwieldy)
- Team unfamiliar with subtree (nobody knows how to recover from errors)
