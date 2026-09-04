# Additional Resources — data-governance-officer

> Deep knowledge loaded on demand. Policy templates, quality dimensions, and reference material.

## Policy Templates (one page each, adapt to your org)

### Data Ownership Policy
- Every dataset has one accountable owner (person) + one steward.
- Owner approves schema/definition changes; steward maintains metadata and quality.
- Owner review cadence: quarterly confirmation that the dataset still matches reality.

### Canonical Metric Definition Template
| Field | Example |
|-------|---------|
| Metric name | Monthly Recurring Revenue (MRR) |
| Business definition | Recurring subscription revenue recognized monthly, excluding one-time fees |
| Technical definition | `SUM(revenue) WHERE type='subscription' AND status='active' GROUP BY month` |
| Owner | Head of Finance |
| Review date | Quarterly |
| Decision record | v2: excluded setup fees (2026-03); v1: included all revenue (2025-09) |

### Data Quality Dimensions & Example Checks
| Dimension | Question | Example check |
|-----------|----------|---------------|
| Freshness | Is it current? | max(updated_at) within 24h |
| Completeness | Are rows/fields missing? | null-rate per critical column < 2% |
| Accuracy | Does it match source of truth? | row count within ±5% of source table |
| Consistency | Same as other systems? | totals match the finance system within tolerance |
| Validity | Fits schema and rules? | no duplicate keys; enum values in allowed set |

### Retention Schedule Skeleton
| Data class | Legal minimum | Business retention | Deletion mechanism | Owner |
|-----------|---------------|--------------------|--------------------|-------|
| PII (customer) | Varies by jurisdiction | Defined + documented | Hard delete + backup purge | Data owner |
| Financial records | 7 years (typical) | Match legal | Archive, then delete | Finance |
| Logs | 30-90 days (typical) | Defined per purpose | TTL/rotation | Ops |

## War Stories

- **The catalog that became fiction:** A data team stood up an enterprise catalog, populated it once, and never automated refresh. Two quarters later it described a warehouse that no longer existed. Teams stopped trusting it and started a second, private catalog — fragmenting the "single source" further. Lesson: automate metadata scanning or the catalog rots; a stale catalog is worse than none because it's trusted until it isn't.
- **The definition that cost a quarter:** Two teams reported "active users" differently for six months. The board deck and the product dashboard disagreed in a public review. Nobody owned the definition; each team was "right" by their own measure. Lesson: definition conflicts are governance incidents — convene, pick one, publish the loser as deprecated.
- **The 95% that was 40%:** A governance lead reported 95% catalog coverage. An audit measured 40% — the number had been estimated, not measured. The governance program lost credibility with the board in one meeting. Lesson: every governance metric must be reproducible from a metadata query.

## Reference Material

- GDPR (Art. 5, 17, 30), CCPA/CPRA, HIPAA — retention and data-subject obligations
- DAMA-DMBOK — data management body of knowledge (governance, quality, metadata)
- DCAM (EDM Council) — data management capability assessment model
- OpenMetadata / DataHub / Atlan docs — catalog + lineage tooling patterns
- dbt test + elementary — warehouse-native quality monitoring
