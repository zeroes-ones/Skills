# Session Management Security

## Cookie Configuration Reference

### Minimal Secure Cookie
```
Set-Cookie: session_id=<128-bit-random>; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=3600
```

### Maximum Security Cookie (high-value sessions)
```
Set-Cookie: __Host-session_id=<128-bit-random>; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=900
```
- __Host- prefix: Browser enforces Secure + Path=/ + no Domain attribute
- Strict mode: No cross-site requests -- breaks OAuth redirects, use only post-authentication

## Session Fixation Prevention

1. User visits login page (no session, or pre-auth session with minimal privileges)
2. User submits valid credentials
3. Server validates credentials successfully
4. **Server REGENERATES session ID** (critical step -- this is fixation prevention)
5. Server copies any pre-auth state to new session
6. Server destroys old session
7. User receives new session cookie with new ID

**Test:** Before login, set document.cookie="session_id=KNOWN_VALUE". After login, verify session_id has changed to a new value.

## Session Invalidation Triggers

| Trigger | Action | Rationale |
|---------|--------|-----------|
| Password change | Invalidate ALL sessions for that user | Old sessions may have been created by attacker with compromised password |
| Role/permission change | Invalidate ALL sessions for that user | Old sessions have cached permissions -- prevent privilege escalation |
| Email change (unverified) | Invalidate ALL sessions | Account takeover indicator -- verify the change was authorized |
| MFA enrollment/removal | Invalidate ALL sessions | Security posture change -- re-authenticate with new requirements |
| User deactivation/termination | Invalidate ALL sessions + blocklist session IDs | Immediate access termination required |
| Concurrent session limit exceeded | Terminate oldest session | Prevent session hoarding and credential sharing |

## Session Hijacking Detection Signals

- IP subnet change mid-session (flag, don't block -- mobile switches WiFi/cellular)
- User-Agent change mid-session (flag -- not just browser updates, investigate)
- Impossible travel: session used from NYC then Tokyo 10 minutes later -> terminate + alert
- Geolocation anomaly: session jump >1000km in <minimum travel time -> step-up MFA
