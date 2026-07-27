# /code-simplify — Simplify code while preserving behavior

Apply Chesterton's Fence principle: understand why code exists before removing it. Make incremental, behavior-preserving simplifications, each verified by tests.

**When to use**: When code is overly complex, has dead paths, or accumulates unnecessary abstractions. Do NOT use on code marked with `simplify-ignore` blocks.

**Workflow**:
1. Invoke `code-simplification` skill
2. Identify 5 categories of simplification: dead code, over-abstraction, complexity, duplication, inconsistency
3. Each change: simplify → test → verify behavior preserved → commit
4. Use `hooks/simplify-ignore.sh` to protect marked blocks
5. Output: Simplified, tested code with net-negative diff

**What it produces**: Cleaner code with fewer lines, fewer abstractions, and preserved behavior. Every change verified by existing tests.
