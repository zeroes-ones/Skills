# Consent Management

Event-sourced consent architecture with cryptographic proof chain
implementation. GDPR-compliant consent is not a boolean — it is a
verifiable state machine recording who consented to what, when, and
under which privacy notice.

## Consent Data Model (Event-Sourced)

```
Table: consent_events (append-only, immutable)
  subject_id: UUID      — the data subject
  purpose_id: STRING    — "marketing_email", "analytics_tracking", "third_party_sharing"
  event_type: ENUM      — 'granted', 'withdrawn', 'expired', 'updated'
  notice_version: STRING— privacy notice version at time of consent
  notice_text_hash: STR — SHA-256 of full notice text shown to user
  timestamp: TIMESTAMP  — when the action occurred
  proof_hash: STRING    — SHA-256(subject_id + purpose_id + notice_text + timestamp + nonce)
  nonce: UUID           — prevents hash collision, ensures uniqueness
  ip_address: STRING    — (optional, jurisdiction-dependent) for geo-evidence
  user_agent: STRING    — session context for audit trail
```

## Consent Proof Chain

The `proof_hash` creates a tamper-evident chain:
1. At consent time, generate nonce, compute proof_hash
2. Store the full record with proof_hash
3. During audit, recompute proof_hash and verify against stored value
4. If stored hash != recomputed hash → tampering detected

## Withdrawal Architecture

```
Consent withdrawal flow:
1. User requests withdrawal via privacy dashboard
2. INSERT consent_events: event_type='withdrawn'
3. Publish event to message queue: {subject_id, purpose_id, 'withdrawn'}
4. All downstream services consume event and delete/halt processing
5. Services acknowledge completion within 24h SLA
6. Reconciliation job verifies all services processed withdrawal
7. Admin dashboard shows per-service withdrawal status
```

## Re-Consent Triggers (When to Re-Ask)

- New processing purpose not covered by existing consent
- New third-party recipient not disclosed in original notice
- Material change to processing (new technology, merged datasets)
- Merger/acquisition (new controller = new consent basis)
- Consent older than 24 months (some DPAs expect periodic refresh)
- Legal basis change (switching from legitimate interest to consent)

## CCPA Opt-Out Implementation

```
Opt-out technical requirements:
- "Do Not Sell or Share My Personal Information" link on every page
- Global Privacy Control (GPC) signal detected via Sec-GPC HTTP header
- Opt-out preference stored server-side, respected for 12 months minimum
- Opt-out propagates to all downstream data recipients
- No re-requesting opt-in for 12 months after opt-out
```

## Cookie Consent Architecture (ePrivacy + GDPR)

```
Strictly necessary cookies (no consent required):
- Session cookie (session_id)
- CSRF token (csrf_token)
- Load balancer affinity (lb_affinity)
- Authentication token (auth_token)

Non-essential cookies (prior consent required):
- Analytics (utm_source, _ga, _gid)
- Advertising (ad_id, _fbp)
- Personalization (theme_pref, language_pref)
- Social media (social_share_id)

Consent implementation:
1. Cookie wall is PROHIBITED — access cannot be conditional on consent
2. Pre-ticked boxes are PROHIBITED — must be affirmative action
3. "Accept All" and "Reject All" must be equally prominent
4. Granular per-category toggles, not just all-or-nothing
5. Consent proof stored server-side with timestamp for audit
```
