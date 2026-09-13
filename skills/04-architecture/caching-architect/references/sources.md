# Sources — provenance for the claims in this skill

> Every claim in SKILL.md and these reference files traces to a source below, tagged by strength.
> Where a source is weaker (vendor engineering blog, folklore), it is marked — the mechanisms are
> well-established; the specific percentages in any workload must be measured on that workload (R6).
> Estimated figures are marked as such and must not be quoted as measured.

---

## Sources

| Claim | Source | Strength |
|-------|--------|----------|
| Cache invalidation is a correctness concern, not only performance | Established practice; the "two hard problems" framing is folklore, the underlying difficulty is not | Established, widely reproduced |
| Probabilistic early expiry reduces stampedes without coordination | The XFetch formulation, Vattani, Chierichetti, Lowenstein (2015); widely implemented (e.g. cache libraries' early-recompute options) | Peer-reviewed mechanism |
| `stale-while-revalidate` as a cache directive | RFC 5861 (HTTP Cache-Control extensions) | IETF standard |
| Thundering herd / cache stampede is the characteristic cold-start failure | Standard reliability practice, cf. AWS and Google SRE material | Established practice |
| A cache key omitting a security dimension is a data-leak vector | OWASP guidance on cache and session handling; incident literature | Established practice |
| Cache behaviour is scale-dependent (eviction, cardinality, TTL rounding) | Standard capacity and cache literature | Established practice |
| Redis eviction policies and CDN invalidation APIs differ per version | Vendor documentation, version-specific | Must be re-checked against the installed version — see Anti-Hallucination in SKILL.md |
| Incident-cost ranges quoted in SKILL.md ($10k–$75k, $50k–$500k, $100k–$1M+) | Directional estimates synthesised from incident-response cost reporting | **Estimated** — order-of-magnitude, not audited; never quote as measured |

**Explicitly not claimed.** That a cache can be made perfectly coherent (it cannot — a copy is a
copy), that a specific hit rate is "good", or that any single defence removes the need for the
origin to shed load. The aim is a *declared and owned* staleness budget, not zero staleness.
