# API Key Lifecycle Management

## Key Generation

### Format
Prefix + base64url random data (32+ bytes). Example: sk_live_<32_bytes_base64url_random>

- Prefix: 8-12 chars identifying environment and purpose (sk_live_, pk_test_, api_prod_)
- Random: secrets.token_urlsafe(32) -> 43 characters of base64url-encoded data
- Total length: 50-60 characters, 256 bits of entropy minimum

### Storage Rule
NEVER store raw API key in database. Store only: SHA-256(raw_key)
Show raw key to user exactly once at creation time.
Subsequent API responses: show only key prefix + last 4 characters for identification.
If the raw key is lost, the only option is rotation -- the server cannot recover it.

## Rotation Automation Pattern

```
Daily cron job:
  1. Query keys expiring in <7 days
  2. For each expiring key:
     a. Generate new key pair (store SHA-256 hash)
     b. Notify key owner via secure channel with new key
     c. Set new key active, old key expires in 7 days (overlap period)
     d. Log rotation event: old_key_id, new_key_id, timestamp, reason
  3. Daily cleanup: revoke keys past their expiry date
```

## HMAC Request Signing

For request integrity on high-value API operations (transfers, deletions, PII access):

1. Client constructs signing string:
   METHOD + "\n" + PATH + "\n" + TIMESTAMP + "\n" + SHA256(BODY)
2. Client computes: HMAC-SHA256(api_secret, signing_string)
3. Client sends headers: X-Signature, X-Timestamp
4. Server validates:
   - Timestamp within +/-5 minutes of server time (replay window)
   - Reconstruct signing string from request
   - Compute expected HMAC using stored secret
   - Compare signatures in constant time (crypto.timingSafeEqual)

## Revocation Architecture

- Instant: POST /keys/{id}/revoke -> marks revoked in DB, publishes to message bus
- Propagation: Resource servers subscribe to revocation events, update local cache within 60 seconds
- Fallback: If no event received in 120 seconds, call key status endpoint
- Blocklist: SHA-256 hashes of revoked keys with TTL matching original key expiry
- Cascade: If master/root key compromised, revoke ALL keys in that scope immediately
