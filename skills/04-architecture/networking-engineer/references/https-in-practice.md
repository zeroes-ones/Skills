# How HTTPS Works — TLS Under the Hood

> Original explainer for interview prep and learning. [research-source: title-only]

## What HTTPS is

HTTPS = HTTP over **TLS** (the modern name for SSL). TLS provides three guarantees: **confidentiality** (traffic encrypted), **integrity** (tamper-evident), and **authentication** (you're talking to the real server, not an impostor). It runs on top of TCP (port 443) and below HTTP — HTTP itself is unchanged.

## The TLS handshake (know the shape, not just the name)

1. **ClientHello** — client sends supported TLS version, cipher suites, and a random nonce.
2. **ServerHello** — server picks version + cipher suite, sends its own nonce and its **certificate** (public key + identity, signed by a CA).
3. **Certificate verification (client side)** — client checks the cert chains to a trusted root CA, is unexpired, matches the hostname, and isn't revoked. This is the authentication step.
4. **Key exchange** — client and server derive a shared session key. Modern TLS uses **(EC)DHE**: both sides contribute ephemeral key material, so the session key is fresh per connection (**forward secrecy** — past traffic can't be decrypted if a long-term key later leaks).
5. **Finished + encrypted application data** — both sides confirm, then HTTP flows over the encrypted channel.

TLS 1.3 simplified this to a **1-RTT** handshake (0-RTT with session resumption, at a replay cost) and removed weak legacy options. "RTT" matters: the handshake adds round trips before the first byte.

## Why certificates exist

The public key alone proves nothing — an attacker could present their own. A **certificate** binds a public key to a domain, signed by a **Certificate Authority (CA)** that the client already trusts (root store). **Let's Encrypt** made issuance free and automated via the ACME protocol, which is why HTTPS is now the default everywhere. The weak points: a compromised/mis-issuing CA (mitigated by Certificate Transparency logs + CAA records) and **certificate revocation** being slow to propagate.

## The pieces interviewers probe

| Topic | What to say |
|---|---|
| **Symmetric vs asymmetric crypto** | TLS uses asymmetric crypto only for the handshake (auth + key exchange); bulk data uses fast symmetric encryption (AES-GCM/ChaCha20) with the session key |
| **Forward secrecy** | Ephemeral (EC)DHE per session → compromising a server's long-term key can't decrypt recorded past traffic |
| **Cipher suites** | e.g., `TLS_AES_256_GCM_SHA384` — key exchange, auth, bulk cipher, MAC; 1.3 removed RSA key exchange (no forward secrecy) and CBC |
| **Perfect vs practical** | Client validates: chain to root, hostname match (SNI), expiry, revocation (OCSP/CRL); pinning is fragile — avoid |
| **mTLS** | Server *and* client present certs — used for service-to-service auth, not browsers |
| **TLS termination** | LB/proxy terminates TLS and forwards plaintext internally; fine inside a trusted network, but then the proxy holds the keys — decide the trust boundary |
| **Session resumption / 0-RTT** | Faster reconnects; 0-RTT can replay — only for idempotent requests |

## Performance notes (the "HTTPS is slow" myth)

- Handshake overhead is real but small: TLS 1.3 ≈ 1 RTT, amortized by session resumption and **HTTP/2 + HTTP/3** (which multiplex and run over QUIC/UDP).
- Real costs to watch: **certificate management** (auto-renew, monitor expiry — expired certs are a top cause of outages), OCSP/CRL checks, and TLS termination CPU (cheap with AES-NI).
- **HSTS** tells browsers to always use HTTPS — prevents downgrade. Add it once HTTPS is solid.

## Interview answer skeleton

"HTTPS is HTTP over TLS. The handshake authenticates the server via a CA-signed certificate and derives a fresh session key with ephemeral Diffie-Hellman for forward secrecy, then all data flows under symmetric encryption. In design I terminate TLS at the edge/proxy, manage certificates with automated renewal and expiry monitoring, use HSTS, and pick TLS 1.3 with modern AEAD ciphers."

## Anti-patterns

- ❌ Disabling cert verification "in dev" and shipping it (a classic MITM hole).
- ❌ Long-lived RSA key exchange ciphers with no forward secrecy.
- ❌ Letting certificates expire — automate renewal and alert on the date.
- ❌ Terminating TLS in the app server when a proxy would centralize cert management (unless the trust boundary requires end-to-end).
- ❌ Self-signed certs everywhere without a private CA + client trust story.

## Deliberate-practice drills

1. **Handshake drill:** `openssl s_client -connect example.com:443` and narrate the certificate chain + negotiated cipher.
2. **Cipher drill:** explain why `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` provides forward secrecy but `TLS_RSA_...` doesn't.
3. **Design drill:** terminate TLS for 50 microservices — where, whose keys, how certs renew, how mTLS fits.
4. **Failure drill:** the cert expired at 2 AM — walk detection, mitigation (renew + HSTS impact), and the automation that prevents recurrence.
5. **Interview drill:** "is HTTPS slow?" — answer with RTT math, resumption, HTTP/2/3.

## References
- See also: dns-deep-dive.md (this repo)
- `cryptography` SKILL.md — primitives, key management, cert lifecycle (ACME/OCSP)
- `networking-engineer` SKILL.md — L7 termination, zero trust
- `secure-api-design` SKILL.md — mTLS and API transport security
