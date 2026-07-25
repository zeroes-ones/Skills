## Core Workflow

The five-phase adversarial review cycle. Each phase produces an artifact that feeds the next. No phase may be skipped.

```
                            ┌──────────┐
                            │  CLAIM   │ ← Extract every non-trivial assumption
                            └────┬─────┘
                                 │ claims.md
                                 ▼
                            ┌──────────┐
                            │ EXTRACT  │ ← Anchor each claim to code/evidence
                            └────┬─────┘
                                 │ anchored_claims.md
                                 ▼
                   ┌────────────────────────┐
                   │        DOUBT           │ ← For each claim: "This is wrong if..."
                   │  ┌──────┐  ┌─────────┐ │
                   │  │Cycle 1│→│Cycle 2  │→│→ Max 3 cycles
                   │  └──────┘  └─────────┘ │
                   └───────────┬────────────┘
                               │ doubt_log.md
                               ▼
                   ┌────────────────────────┐
                   │      RECONCILE         │ ← Resolve, accept, or escalate
                   │  ┌────────┐ ┌────────┐ │
                   │  │Resolved│ │Residual│ │
                   │  └────────┘ └────────┘ │
                   └───────────┬────────────┘
                               │ RECONCILE.md
                               ▼
                            ┌──────────┐
                            │   STOP   │ ← Hard stop. Residual doubt is documented.
                            └──────────┘
```

### Phase 1: CLAIM — Extract Every Non-Trivial Assumption

Read the code as if the author is trying to deceive you. Every line that makes an assertion about behavior, data, timing, or correctness IS a claim.

**What qualifies as a claim:**
- Behavior assertions: "This function returns sorted results" (Is it? Under all inputs?)
- Invariant assertions: "This value is never null here" (Prove it.)
- Security assertions: "Only authenticated users reach this handler" (Where's the middleware?)
- Performance assertions: "This query runs in O(n)" (What's n at scale?)
- Correctness assertions: "This matches the spec" (Which spec? Which version?)

```
Example: Extracting claims from an auth middleware

function requireAuth(req, res, next) {          // CLAIM-001: Every route after this
  const token = req.headers.authorization;      // middleware has a valid token.
  if (!token) return res.status(401);           // CLAIM-002: Absence of token → 401.
  const decoded = jwt.verify(token, SECRET);    // CLAIM-003: jwt.verify rejects
  req.user = decoded;                           // expired/invalid tokens.
  next();                                       // CLAIM-004: decoded payload is
}                                               // safe to attach as req.user.
                                                // CLAIM-005: next() is always
                                                // called after successful auth.
```

**Output artifact:** `claims.md` with each claim labeled `CLAIM-NNN`, the code location (file:line), and the extracted assertion in one sentence.

### Phase 2: EXTRACT — Anchor Every Claim

For each claim, find the evidence that would PROVE or DISPROVE it. A claim without a test is a confession, not a claim.

```
Example: Anchoring CLAIM-002

CLAIM-002: Absence of token → 401.
  Evidence FOR:
    - auth.test.ts:45 — sends request without Authorization header, expects 401 ✓
    - auth.test.ts:52 — sends request with empty Authorization header, expects 401 ✓
  Evidence AGAINST:
    - No test for Authorization header with value "null" (string) ❌
    - No test for Authorization header with value "undefined" (string) ❌
    - No test for malformed Bearer prefix ("Bearer" vs "bearer" vs empty scheme) ❌
```

**Output artifact:** `anchored_claims.md` — same claims, now with evidence columns (FOR/AGAINST) and at least one testable condition per claim.

### Phase 3: DOUBT — Adversarial Challenge (Max 3 Cycles)

For each anchored claim, adopt the mindset: **"This claim is false. Find the proof."**

Each doubt cycle MUST follow this structure:
```
DOUBT-[claim_id]-[cycle]: "Claim X would be WRONG if [condition]."
  TEST: [concrete check that verifies condition]
  EVIDENCE: [grep/run/test result]
  SEVERITY: [CRITICAL|HIGH|MEDIUM|LOW] — if condition is met, what's the blast radius?
```

```
Example: Doubt cycle on CLAIM-002

CYCLE 1:
  DOUBT-C002-1: "CLAIM-002 would be WRONG if the Authorization header
                 can contain the literal string 'null' when JS null
                 is coerced to a string."
  TEST: curl -H "Authorization: null" https://api/secure-endpoint
  EVIDENCE: Returns 401 ✓ (express does not coerce null to "null" header)
  SEVERITY: HIGH (would allow unauthenticated access)
  DISPOSITION: CLAIM HOLDS for this condition.

CYCLE 2:
  DOUBT-C002-2: "CLAIM-002 would be WRONG if jwt.verify throws
                 instead of returning null on invalid token."
  TEST: grep -n "try.*catch\|\.catch" auth.js
  EVIDENCE: No try/catch around jwt.verify — unhandled rejection! ❌
  SEVERITY: CRITICAL (crash loop on any invalid token)
  DISPOSITION: CLAIM FAILS. jwt.verify throws JsonWebTokenError.
                → RECONCILE required.
```

**Cycle limit:** Maximum 3 cycles per claim. After cycle 3, residual doubt is documented and accepted.

### Phase 4: RECONCILE — Resolve, Accept, or Escalate

Every doubt that does not resolve to "CLAIM HOLDS" must be reconciled. Three outcomes:

```
RECONCILE-[claim_id]:
  RESOLVED:   [Code fix applied, test added → claim now holds]
  ACCEPTED:   [Risk accepted with documented rationale and monitoring plan]
  ESCALATED:  [Cross-model review requested — see cross-model-escalation.md]
```

```
Example: Reconciling DOUBT-C002-2

RECONCILE-C002:
  STATUS: RESOLVED
  DOUBT: jwt.verify throws instead of returning null
  FIX: Wrapped jwt.verify in try/catch with explicit JsonWebTokenError handling
  TEST_ADDED: auth.test.ts:78 — sends token with invalid signature, expects 401 not 500
  VERIFIED_BY: CI run #2847 — auth test suite passes with new test
  DATE: 2026-07-23
  REVIEWER: cross-model (GPT-4o verified fix completeness)
```

### Phase 5: STOP — Hard Stop and Residual Doubt Acceptance

After reconciliation, the cycle STOPS. No further doubt on reconciled claims.

**Stop criteria checklist:**
- [ ] All claims have completed at least 1 doubt cycle
- [ ] All CRITICAL/HIGH severity doubts are RESOLVED (not ACCEPTED)
- [ ] No claim has exceeded 3 doubt cycles
- [ ] RECONCILE.md contains entries for every non-HOLDS doubt
- [ ] Residual risk inventory is complete with monitoring plan
- [ ] Cross-model escalation considered for any CRITICAL doubt that required cycle 3

```
Example: STOP artifact

STOP REPORT — 2026-07-23 — PR #847 (Auth Middleware Refactor)
  CLAIMS EXTRACTED:  12
  DOUBT CYCLES RUN:  28 (across 12 claims)
  CLAIMS HOLDING:    8
  RECONCILED:        4 (3 RESOLVED, 1 ACCEPTED, 0 ESCALATED)
  RESIDUAL RISK:     1 — CLAIM-009 (rate limiting assumes single-instance;
                      accepted with monitoring alert on >1000 req/s per IP)
  STOP DECISION:     CLEAR TO MERGE with residual risk monitoring active.
```
