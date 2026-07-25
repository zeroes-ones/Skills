## Core Workflow

### Phase 0: Clarify the Bug

Before touching any code, complete this template:

```
BUG TRIAGE TEMPLATE
===================
What is the exact error? [copy-paste error message + stack trace]
What was expected to happen? [specific expected behavior]
What actually happened? [specific observed behavior]
When did it start? [timestamp, deployment, commit]
What is the impact? [users affected, revenue impact, data loss]
Can you reproduce it? [YES / NO / SOMETIMES]
What are the reproduction steps? [1. 2. 3.]
What is the environment? [OS, browser, server version, database version]
```

If any field is blank, STOP. Ask the reporter to fill it in before proceeding. Debugging without this information is guessing.

### Phase 1: Reproduce

Reproduction is the foundation. Without it, you are navigating without a map.

```
Step 1: Reproduce manually
  Follow the reproduction steps exactly. If you cannot reproduce, the bug report is incomplete.

Step 2: Write a failing test
  describe('bug #1234: login fails with special characters', () => {
    it('should accept email with plus sign', () => {
      expect(() => login('user+tag@example.com', 'password'))
        .not.toThrow();
    });
  });

Step 3: Confirm the test fails for the reported reason
  npm test -- -t 'bug #1234'
  # Expected: test FAILS (red) -- proving the bug exists
  # If test PASSES (green) -- your reproduction is wrong
```

### Phase 2: Localize

Narrow the problem space. Binary search is the most efficient method.

```
Method A: git bisect (find the breaking commit)
  git bisect start
  git bisect bad HEAD          # current broken state
  git bisect good <last_known_good_commit>
  # Git checks out midpoint. Test. Mark good/bad. Repeat.
  # In log2(N) steps, you find the exact commit.
  git bisect log > bisect_log.txt

Method B: Binary search on code (comment-out method)
  # For a 200-line function that throws an error:
  # Comment out lines 100-200. Does error still occur?
  # YES → bug is in lines 1-100.  NO → bug is in lines 100-200.
  # Repeat, halving each time. Find exact line in log2(200) ≈ 8 iterations.

Method C: Log injection
  # When you cannot modify code (production), add targeted structured logs:
  logger.info('checkpoint-A', { userId, cartTotal, timestamp });
  # Query logs: which checkpoint was the last one reached before the error?
  # Bug is between the last successful checkpoint and the error.
```

ASCII diagram:
```
┌─────────────────────────────────────────────────┐
│              DEBUGGING WORKFLOW                  │
├─────────────────────────────────────────────────┤
│  Phase 0: Clarify (fill triage template)        │
│     │                                           │
│     ▼                                           │
│  Phase 1: Reproduce (write failing test)        │
│     │                                           │
│     ▼                                           │
│  Phase 2: Localize (bisect / binary search)     │
│     │                                           │
│     ▼                                           │
│  Phase 3: Reduce (minimal reproduction)         │
│     │                                           │
│     ▼                                           │
│  Phase 4: Fix Root Cause (5 Whys)               │
│     │                                           │
│     ▼                                           │
│  Phase 5: Guard (regression test)               │
│     │                                           │
│     ▼                                           │
│  Phase 6: Verify (production-like environment)   │
└─────────────────────────────────────────────────┘
```

### Phase 3: Reduce to Minimal Reproduction

Strip away everything unnecessary. The smaller the repro, the faster the fix.

```
Before reduction:
  - 500-line component
  - 3 API calls
  - 2 database queries
  - User must be logged in with specific permissions
  - Input: 50-field form submission

After reduction:
  - 15-line function: the single transform that fails
  - 0 API calls (mocked)
  - 0 database queries (hardcoded data)
  - No auth required
  - Input: the single field value that triggers the bug
```

The delta debugging algorithm: systematically remove elements from the input/state until you find the minimal set that still triggers the bug.

### Phase 4: Fix Root Cause

Apply the 5 Whys. Never fix at the symptom layer.

```
Symptom: TypeError: Cannot read property 'name' of undefined
│
├── Why? user parameter is undefined
│   └── Why? getUser() returned null
│       └── Why? Database query returned no rows
│           └── Why? User record was deleted by cleanup job
│               └── Why? Cleanup job had wrong date filter
│                   └── ROOT CAUSE: Date filter off-by-one error
│
├── SYMPTOM FIX (WRONG): Add `if (user) return;` at the top
└── ROOT CAUSE FIX (CORRECT): Fix date filter in cleanup job + add guard in getUser()
```

### Phase 5: Guard with Regression Test

The bug-fix test must be specific enough to catch the exact failure mode.

```
// GOOD regression test: specific to the bug
it('handles user record deleted between auth and profile fetch', async () => {
  await db.insertUser({ id: 1, name: 'Alice' });
  const token = await auth.login('alice', 'password');
  await db.deleteUser(1); // simulate race condition
  await expect(profile.getProfile(token))
    .rejects.toThrow('UserNotFoundError'); // expect graceful error, not crash
});

// BAD regression test: too generic
it('profile fetch works', async () => {
  const profile = await profile.getProfile(validToken);
  expect(profile).toBeDefined();
});
```

### Phase 6: Verify

Before closing the bug, verify in conditions as close to production as possible.

- [ ] Fix passes the regression test
- [ ] Fix passes ALL existing tests (no regressions introduced)
- [ ] Fix tested with production-like data (same nulls, edge cases, data volumes)
- [ ] Fix tested under load (if the bug was load-related)
- [ ] Fix deployed to canary/staging and monitored for 15+ minutes
- [ ] Rollback plan documented (can the fix be safely reverted?)
