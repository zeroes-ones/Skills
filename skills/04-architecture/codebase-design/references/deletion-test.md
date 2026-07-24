# Deletion Test

## Protocol

The deletion test asks one question: **"If I delete this module entirely, what breaks?"**

### Step-by-Step

1. **Identify the module** — class, file, or package under evaluation
2. **Delete it** (mentally or in a branch)
3. **Compile/run** — what fails?
4. **Classify the result:**

| Result | Verdict | Action |
|--------|---------|--------|
| Nothing breaks (no callers) | Dead code | Delete permanently |
| Only tests break | Test-only artifact | Reassess — is the module only here for testing convenience? |
| Callers break but can be trivially updated (rename, re-import) | Pass-through | Delete — update callers to use dependency directly |
| Callers break and need significant rewrite | Real module | Keep — module provides genuine behavior |

### Pass-Through Detection

A module is a pass-through if ALL of its public methods satisfy:
- Method body is ≤2 lines
- Body is a single delegation call to another module
- No transformation, validation, or decision logic

```java
// Pass-through: DELETE THIS MODULE
public void save(User user) {
    repository.save(user);  // Single delegation, no behavior
}

// Not a pass-through: KEEP
public void register(User user) {
    validate(user);              // Behavior: validation
    user.setCreatedAt(now());    // Behavior: timestamp
    repository.save(user);       // Delegation
    emailService.sendWelcome();  // Behavior: side effect
}
```

### Trivial Wrapper Detection

A module is a trivial wrapper if its public methods are all getters/setters for configuration or data transfer with zero behavior logic. These are not modules — they're data structures. Treat them as such.
