# Submodule Lifecycle Management

## Adding a Submodule

```bash
# Add submodule with branch tracking
git submodule add -b main https://github.com/org/shared-lib.git libs/shared-lib

# This creates:
# - .gitmodules entry with path, url, and branch
# - .git/modules/libs/shared-lib/ (the submodule's git data)
# - libs/shared-lib/ (working tree at pinned commit)

# Commit the submodule pointer
git add .gitmodules libs/shared-lib
git commit -m "Add shared-lib as submodule"
```

## Updating a Submodule

```bash
# Update to latest commit on tracking branch
git submodule update --remote -- libs/shared-lib

# Update to a specific tag
cd libs/shared-lib
git fetch --tags
git checkout v2.1.0
cd ../..
git add libs/shared-lib
git commit -m "Pin shared-lib to v2.1.0"
```

## Removing a Submodule (Complete)

```bash
# The correct removal sequence — do not skip steps
git submodule deinit -f libs/shared-lib
rm -rf .git/modules/libs/shared-lib
git rm -f libs/shared-lib
# Edit .gitmodules to remove the [submodule "libs/shared-lib"] section
git add .gitmodules
git commit -m "Remove shared-lib submodule"
```

## Cloning with Submodules

```bash
git clone --recurse-submodules https://github.com/org/parent-repo.git
# Or after a normal clone:
git submodule update --init --recursive
```
