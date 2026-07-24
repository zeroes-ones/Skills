# Open Banking & PSD2/PSD3 Security

FAPI profiles, Strong Customer Authentication (SCA), eIDAS
certificates, and TPP management for open banking APIs.

## FAPI Security Profile Mapping

Financial-grade API (FAPI) — RFC 7521 + OAuth 2.0 + OIDC extensions for banking.

### FAPI 1.0 Baseline (mandatory minimum)
| Requirement | Implementation |
|-------------|----------------|
| Authorization code flow | Only auth code grant, no implicit or ROPC |
| PKCE (RFC 7636) | `code_challenge` = SHA-256(`code_verifier`); required even with client secret |
| Redirect URI validation | Exact match, no wildcards, HTTPS only |
| Client authentication | `private_key_jwt` or `mutual_tls` (not client_secret_basic/post) |
| State parameter | Unguessable random value, bind to browser session |
| Token binding | Access token bound to TLS connection (MTLS) |

### FAPI 1.0 Advanced (Read/Write APIs — payments)
All Baseline requirements PLUS:
- Request Object (JWT): signed JWT containing authorization request parameters
- PAR (Pushed Authorization Request): POST to PAR endpoint, get `request_uri`, use in auth request (prevents browser-tamperable parameters)
- JARM: JWT-secured authorization response (protects response parameters from modification)
- Detached signature: `response_type=code id_token` (hybrid flow) for non-repudiation
- SCA required: user interaction at authorization endpoint must include authentication
- Refreshing consent: refresh token only if original consent still valid

### FAPI 2.0 (Current, simplified)
- DPoP (Demonstration of Proof-of-Possession): sender-constrained access tokens
- PAR is mandatory (not optional as in FAPI 1.0 Advanced)
- Rich Authorization Request (RAR): granular scopes with typed parameters
- Grant management: OAuth 2.0 Grant Management for consent lifecycle
- Simplified: no hybrid flow, no request objects (PAR replaces), no detached signatures

## Strong Customer Authentication (SCA)

PSD2 Article 97: payment service providers must apply SCA when:
1. Payer accesses payment account online
2. Payer initiates electronic payment
3. Payer carries out any action that may imply fraud risk

### Authentication Factors (at least TWO independent categories)

| Category | Examples | Considerations |
|----------|----------|----------------|
| **Knowledge** (something only user knows) | Password, PIN, secret question answer, knowledge-based challenge | Must be revocable, not shared across services |
| **Possession** (something only user has) | Hardware token, software token (TOTP), registered device, SMS OTP (deprecated per NIST), smart card, secure element | Must prove possession, not just knowledge of device ID |
| **Inherence** (something user is) | Fingerprint, face ID, iris scan, voice print, behavioral biometrics (keystroke, gait) | Must have liveness detection, spoof-proof |

### SCA Exemptions
- Low-value: <€30 per transaction, cumulative <€100 or 5 consecutive since last SCA
- Trusted beneficiary: payer whitelisted merchant (requires first-time SCA)
- Recurring: same payee, same amount (first payment needs SCA)
- Corporate payments: dedicated payment processes (not consumer-facing)
- Transaction Risk Analysis (TRA): acquirer's fraud rate <0.13% (€100), <0.06% (€250), <0.01% (€500)

## eIDAS Certificate Management

### QWAC (Qualified Website Authentication Certificate)
- Required per PSD2: QWAC for TPP-facing interface
- Issued by Qualified Trust Service Provider (QTSP) on EU Trusted List
- Certificate must contain: PSD2 authorization number, role (AISP/PISP/PISP+AISP), competent authority
- Format: X.509 v3 with `qcStatements` extension containing PSD2-specific OID
- Revocation: OCSP with 24-hour max staleness, CRL
- Rotation: before expiry, maintain overlap for zero-downtime MTLS

### QSealC (Qualified Electronic Seal Certificate)
- Used to digitally sign: payment initiation requests, account information responses
- Non-repudiation: proves response came from ASPSP (not tampered in transit)
- Signature format: JSON Web Signature (JWS) detached or CAdES

## TPP Management

### Registration
1. TPP registers with National Competent Authority (NCA) — gets PSD2 license + authorization number
2. TPP obtains eIDAS QWAC from QTSP with PSD2 authorization details embedded
3. TPP registers with each ASPSP's developer portal (per PSD2, ASPSP must provide access)
4. TPP obtains OAuth 2.0 client credentials per ASPSP (client_id per ASPSP)

### Revocation
```
Revocation triggers:
- NCA revokes PSD2 authorization → QTSP revokes QWAC within 24h
- ASPSP detects fraud/misuse → revoke client credentials immediately
- TPP fails to renew QWAC → grace period 72h then access suspended
- Customer revokes consent → TPP access token invalidated immediately

Technical implementation:
- OCSP stapling: every TPP connection MTLS handshake validates QWAC status
- JWT access token introspection (RFC 7662): validate OAuth token per request
- Webhook to NCA registry: monitor for authorization status changes
```
