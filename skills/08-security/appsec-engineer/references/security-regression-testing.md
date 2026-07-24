# Security Regression Testing

## Test Pyramid for Security

```
          /\
         /  \       Manual Pen Test (pre-release, major features)
        /    \      Security BDD Scenarios (automated, in CI)
       /------\     Fuzzing (automated, nightly, high-risk endpoints)
      /        \    DAST Scans (automated, staging environment)
     /----------\   Security Unit Tests (automated, every PR)
    /            \  SAST + Secret Scanning (automated, pre-commit + PR)
```

## Security BDD Scenarios (Gherkin Format)

Write security test cases in Gherkin to make them readable by developers, QA, and security engineers:

```gherkin
Feature: Authentication Security
  Scenario: Session fixation prevention on login
    Given a user visits the login page
    And a session cookie "session_id=attacker_known_value" is set
    When the user successfully authenticates
    Then the session ID should be regenerated to a new value
    And the old session ID should be invalidated

  Scenario: Account lockout after repeated failed attempts
    Given a user account "alice@example.com" exists
    When 5 failed login attempts occur within 10 minutes
    Then the account should be locked for 30 minutes
    And a security alert should be triggered

Feature: Authorization Security
  Scenario: IDOR prevention on user profile endpoint
    Given user "alice" is authenticated
    When alice requests GET /api/users/bob/profile
    Then the response should be 403 Forbidden
    And alice should not see bob's profile data

  Scenario: Privilege escalation prevention
    Given user "alice" has role "editor"
    When alice sends PATCH /api/users/alice with {"role": "admin"}
    Then the response should be 403 Forbidden
    And alice's role should remain "editor"
```

## Fuzzing Integration

Fuzzing sends malformed, unexpected, or random data to find crashes and undefined behavior:

- Tool selection: libFuzzer (C/C++), go-fuzz (Go), Jazzer (Java/JVM), atheris (Python), jsfuzz (JavaScript)
- Target selection: parsers, serializers, protocol handlers, file format readers, compression algorithms
- Fuzzing corpus: Start with valid inputs, let the fuzzer mutate from there
- CI integration: Run fuzzers on main branch nightly for 30 minutes minimum
- Crash triage: Every crash creates a ticket, priority based on exploitability (can arbitrary code execution be achieved?)

## Mutation Testing for Authorization Controls

Mutation testing intentionally introduces bugs to verify that tests catch them:

1. Write authorization test suite (BDD scenarios above)
2. Run mutation testing tool that modifies auth checks:
   - Removes authorization check entirely (should fail)
   - Replaces role check with "always true" (should fail)
   - Changes permission check from strict to lenient (should fail)
3. Mutation score = % of mutations that were caught by tests
4. Target: 100% mutation score for Tier 1 authZ code (auth, admin, payments)

## DAST Security Test Cases

Beyond automated scanning, define manual DAST test cases for critical flows:

### Authentication Flow
- Brute force: 10 rapid login attempts -- should be rate-limited or locked
- Password reset: Request reset for non-existent email -- should not reveal if account exists
- MFA bypass: Attempt to access MFA-protected endpoint directly without completing MFA

### Authorization Flow
- Horizontal privilege escalation: User A tries to access User B's resources
- Vertical privilege escalation: Editor tries admin-only endpoints
- Context-dependent: User tries to access resource outside their department/project

### Input Validation
- SQL injection: ' OR '1'='1 in every parameter -- should not affect query logic
- XSS: <script>alert(1)</script> in every input -- should be encoded in output
- File upload: Upload executable file (.php, .jsp, .exe) -- should be rejected server-side
