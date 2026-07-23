# Versioning Cost Analysis

| Strategy | Implementation Cost | Maintenance Cost | Breaking Change Cost |
|----------|-------------------|-----------------|---------------------|
| **No versioning** | $0 | $0 | Full rewrite of all clients |
| **URL path (/v1/)** | Low (routing config) | Medium (N active versions × server cost) | Low (old version still works) |
| **Header versioning** | Medium (custom middleware) | Medium | High (clients must update headers) |
| **Query param (?v=1)** | Low | Medium | Low |
| **Content negotiation** | High (Accept header parsing) | Medium | High |
| **API Gateway routing** | High (gateway infra) | Low (route per version in gateway) | Low |

**Recommended:** URL path versioning (`/v1/`) for public APIs. Sunset vN 12 months after vN+1 release. Never run >2 versions simultaneously (cost grows linearly).

### Versioning Anti-Patterns
- **Versioning too early:** < 100 API consumers → don't version. Just change the API and notify.
- **Versioning everything:** Version only when breaking backward compatibility. Non-breaking additions don't need v2.
- **Keeping v1 forever:** Cost of maintaining v1 = hosting + bug fixes + security patches + support. Set a sunset date.
