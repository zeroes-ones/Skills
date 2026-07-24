# MFA and WebAuthn

## Factor Strength Comparison

| Factor | Phish Resistance | Cost | UX Friction | Compromise Resistance |
|--------|-----------------|------|-------------|----------------------|
| WebAuthn/FIDO2 Hardware Token (YubiKey) | 99%+ | $25-55/token | Medium | Origin-bound, private key never leaves device |
| WebAuthn Platform Authenticator (Passkey) | 99%+ | $0 | Low | Synced across ecosystem, biometric-protected |
| TOTP (Authenticator App) | 50% | $0 | Low | Phishable -- user can be tricked into entering code on fake site |
| Push Notification (Duo, Okta) | 70% | $3-9/user/mo | Very Low | MFA fatigue attacks -- user may approve malicious request |
| SMS / Voice Call | 30% | $0.05-0.10/msg | Medium | SIM swap, SS7 interception, carrier social engineering |
| Email OTP | 20% | $0 | Medium | Email account compromise bypasses MFA entirely |

## WebAuthn Deployment Checklist

### Registration (Attestation)
- Require User Verification (UV) for high-value accounts -- biometric or device PIN
- Store credential ID + public key (CBOR-encoded COSE key) in user profile
- Set userVerification: "required" for privileged accounts, "preferred" for standard
- Allow multiple credentials per user (minimum 2 -- one primary, one backup)
- Attestation conveyance: "none" is acceptable for most deployments (privacy-preserving)

### Authentication (Assertion)
- Validate rpId against origin (same domain or registered subdomain)
- Validate challenge: cryptographically random, single-use, expires in 5 minutes
- Increment and store sign count for cloned credential detection
- Verify userHandle matches the authenticated user

## Passkey Migration Strategy

Phase 1 (Month 1-2): Enable WebAuthn as OPTIONAL second factor alongside existing TOTP.
Phase 2 (Month 3): Promote WebAuthn via in-app banner, email campaign, security checkup prompts.
Phase 3 (Month 4-6): Target 50% enrollment among active users. Deprecate SMS for enrolled users.
Phase 4 (Month 7-9): WebAuthn becomes PRIMARY factor. TOTP as fallback. SMS restricted to recovery only.
Phase 5 (Month 10-12): Target 80%+ enrollment. Disable SMS entirely for accounts with WebAuthn enrolled.

## Recovery Design
- Backup codes: 10 single-use codes, 16+ alphanumeric characters, shown once at MFA enrollment
- Recovery email: Time-limited link (15 minutes) sent to verified recovery email address
- Hardware token backup: Require enrollment of 2+ hardware tokens for high-privilege accounts
- Account recovery workflow: Identity verification + 24-hour waiting period before MFA reset
