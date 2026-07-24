# Certificate Lifecycle Reference

## ACME Protocol (RFC 8555)

### Client Implementations
- **certbot** (EFF): most widely used, plugin architecture for Apache/nginx
- **lego** (Go): library + CLI, supports DNS-01 for wildcard certs
- **Caddy**: built-in auto-HTTPS with ACME (zero-config TLS)
- **cert-manager** (Kubernetes): native Kubernetes CRDs, Issuer/ClusterIssuer

### Challenge Types
- **HTTP-01**: serves token at `/.well-known/acme-challenge/<token>` on port 80
- **DNS-01**: TXT record `_acme-challenge.<domain>` — required for wildcard certs
- **TLS-ALPN-01**: TLS handshake on port 443 with special ALPN protocol

### Rate Limits (Let's Encrypt)
- 50 certificates per registered domain per week
- 5 duplicate certificates per week (same set of hostnames)
- 20 certificates per week per account (new domain additions)
- 300 pending authorizations per account

## Certificate Lifetime Strategy

| Strategy | Lifetime | Renewal | Use Case |
|----------|---------|---------|----------|
| Short-lived | 24 hours | Automated hourly | Internal mTLS (SPIFFE/SPIRE) |
| ACME standard | 90 days | Auto-renew at 60 days (30-day window) | Public-facing web services |
| Long-lived | 1 year | Manual or automated at 11 months | Internal PKI with CRL distribution |
| Extended validation | 1-2 years | Manual, stricter validation | EV certificates (declining value) |

## Certificate Type Selection

### Wildcard (*.example.com)
- **Pros**: covers all first-level subdomains dynamically
- **Cons**: single private key compromise = all subdomains breached
- **Rule**: use only with HSM/TPM-protected private keys and strictly scoped subdomains

### SAN (Subject Alternative Name)
- **Pros**: explicit domain enumeration, limited blast radius
- **Cons**: must know all domains at issuance time
- **Rule**: preferred for known, static domain lists

## Revocation Mechanisms

### OCSP (Online Certificate Status Protocol)
- Real-time certificate status check
- Privacy concern: CA learns which sites user visits
- OCSP Must-Staple eliminates client OCSP queries

### CRL (Certificate Revocation List)
- Periodic published list of revoked certificate serial numbers
- Larger overhead (can be megabytes for large CAs)
- CRLite (Mozilla): compressed, efficiently queryable CRL aggregation
