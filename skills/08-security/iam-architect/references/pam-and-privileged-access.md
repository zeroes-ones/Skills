# Privileged Access Management (PAM)

## Just-in-Time (JIT) Elevation Workflow

1. User requests elevation: selects target role, provides justification, sets requested duration
2. Auto-approval for standard roles (<=4 hours, business hours only)
3. Manager approval for sensitive roles (>4 hours, out-of-hours, production access)
4. Security lead approval for break-glass, database admin, infrastructure admin
5. Elevation granted with hard TTL: 1-4 hours standard, 30 minutes break-glass
6. Session recording begins immediately upon elevation
7. Auto-revocation at TTL expiry + 5-minute grace period for active operations
8. Full audit log: who, what role, when, why, what was accessed, session recording reference

## Session Recording Architecture

Privileged User -> Bastion Host (recording proxy) -> Target System
                           |
                    Screen recording + keystroke logging
                           |
                    Encrypted, immutable storage (WORM)
                           |
                    SIEM integration for anomaly detection + random audit sampling

### Retention Policy
- Standard privileged sessions: 90 days
- Production database access: 1 year
- Break-glass sessions: 3 years minimum
- Sessions flagged for audit review: retain until reviewed + 90 days

## Break-Glass Procedure Design

1. **When to invoke**: Auth system down, PAM unavailable, or emergency incident response requiring immediate admin.
2. **Two-person rule**: Break-glass requires two authorized personnel simultaneously -- no single person can invoke.
3. **Credential vaulting**: Shamir's Secret Sharing (3 of 5 shares to reconstruct). Shares distributed across security leadership team.
4. **Post-use protocol**: Automatic credential rotation within 5 minutes. Full audit review within 24 hours. All shares redistributed to new key material.

## Standing Privilege Elimination

Inventory every user with admin/root/superuser access. For each:
- Is this privilege used daily? -> Convert to JIT with auto-approval during business hours
- Used weekly? -> JIT with manager approval, 4-hour TTL
- Used monthly or less? -> JIT with security lead approval, 1-hour TTL
- Never used in past 90 days? -> Remove immediately, re-evaluate on next access request
