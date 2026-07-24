# Source Identification

Techniques for identifying the primary source of a change: git blame, log searching, PR/issue linking, and author context.

## Primary Identification Methods

### git blame
```bash
git blame -L <start>,<end> <file>
```
Shows the last commit that touched each line. Use to identify which commit introduced the conflicting code.

### git log with path filtering
```bash
git log --oneline --follow -p -- <file>
```
Traces the full history of changes to the file, including renames.

### PR/Issue Linking
GitHub merge commits contain PR numbers. Conventional commits often reference issues. Parse the commit message for `#NNNN` patterns.

### Author Context
If source is unclear, the commit author is the best person to ask. Record their name and the commit hash for follow-up.

## Fallback Chain

1. Try git blame → 2. Try git log with path filtering → 3. Check PR/issue references → 4. Note author for human follow-up
