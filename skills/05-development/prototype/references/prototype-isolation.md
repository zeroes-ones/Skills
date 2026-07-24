# Prototype Isolation: Keeping Experimental Code Separate

## Isolation Methods

### Method A: Git Worktree (Preferred)
```bash
# Create detached worktree for prototype
git worktree add --detach ../proto-YYYY-MM-DD-[topic]

# Work in isolated directory
cd ../proto-YYYY-MM-DD-[topic]

# Dispose when done
cd ../main-repo
git worktree remove ../proto-YYYY-MM-DD-[topic]
```

### Method B: Temp Directory
```bash
# Create isolated directory
mkdir -p ~/prototypes/proto-YYYY-MM-DD-[topic]
cd ~/prototypes/proto-YYYY-MM-DD-[topic]

# Work in isolated directory
# ...

# Dispose when done
cd ~/main-project
rm -rf ~/prototypes/proto-YYYY-MM-DD-[topic]
```

### Method C: Docker Container
Use only when the prototype requires specific system dependencies. Overkill for most prototypes.

## Verification
After creating isolation: `git status` in main repo must show NO changes and NO untracked prototype files.

## Anti-Patterns
- Prototyping in a subdirectory of the main repo ("prototypes/" folder)
- Prototyping in a branch of the main repo (branch survives disposal)
- Copying prototype files into the main repo and deleting the original
