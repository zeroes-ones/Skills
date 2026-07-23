# Production Checklist

<!-- QUICK: 30s -- binary pass/fail items. Each has a mechanical validation command. -->

| ID | Checklist Item | Validation Command | Auto-Fix |
|----|---------------|-------------------|----------|
| **[S1]** | Semantic layer: every metric has one authoritative definition; no duplicate or conflicting definitions | `grep -rn "metric\|measure\|kpi" models/ --include="*.yml" \| awk -F: '{print $NF}' \| sort \| uniq -d` → must return 0 duplicates | Pre-commit: `scripts/check-metric-uniqueness.sh` — blocks if duplicate metric names found |
| **[S2]** | Governed self-serve tiers: Board (certified), Operational (managed), Exploratory (watermarked) | `grep -rn "governed\|certified\|exploratory\|board" config/ --include="*.yml" \| wc -l` → must be >= 3 | CI: `scripts/enforce-governance-tiers.sh` — applies tier template if missing |
| **[S3]** | Board metrics reconciliation: ARR, NRR, LTV/CAC, magic number — all defined with calculation methodology | `grep -rn "calculation\|methodology\|formula" metrics/ --include="*.yml" \| wc -l` → must match metric count | Lint: `scripts/check-metric-documentation.sh` — fails if any metric lacks `calculation` field |
| **[S4]** | Data freshness: SLAs per domain, dbt source freshness active, alerts on breach | `dbt source freshness --output json \| jq '.nodes[] \| select(.freshness.status == "error")'` → must return 0 | CI gate: `dbt source freshness` in pipeline — fails build if sources are stale |
| **[S5]** | Data modeling: star schemas with fact/dimension tables, SCD strategy documented per dimension | `grep -rn "SCD\|slowly_changing\|type_[0123]" models/ --include="*.sql" --include="*.yml"` → must match dimension table count | — |
| **[S6]** | dbt testing: not_null, unique, relationships, accepted_values on all key columns | `dbt test --output json \| jq '.results[] \| select(.status != "pass")'` → must return 0 failures | CI gate: `dbt test` in pipeline — fails build on test failures |
| **[S7]** | Incremental strategy: large fact tables use incremental materialization with unique_key | `grep -rn "materialized.*table\|materialized.*view" models/ --include="*.sql" \| grep -v "incremental" \| wc -l` → must be 0 for tables > 1M rows | Lint: `scripts/check-incremental-strategy.sh` — warns on full-refresh-only tables |
| **[S8]** | Dashboard freshness banner: all board/operational dashboards show data-as-of timestamp | `grep -rn "freshness\|last_updated\|data_as_of\|stale" dashboards/ --include="*.yml" \| wc -l` → must match dashboard count | CI: `scripts/require-freshness-banner.sh` — fails if dashboards lack freshness |
| **[S9]** | Embedded analytics: SSO, row-level security, rate limiting, tenant-isolated query pools | `grep -rn "tenant\|isolation\|row_level\|RLS" config/embedded/ --include="*.yml" \| wc -l` → must be >= 4 | CI: `scripts/check-embedded-isolation.sh` — fails if tenant isolation missing |
| **[S10]** | Data export compliance: exports logged (who/what/when), PHI never in raw exports, retention policy enforced | `grep -rn "export.*audit\|export.*log\|PHI.*export\|retention.*export" config/ --include="*.yml"` → must return > 0 | Pre-commit: `scripts/check-export-compliance.sh` — scans for PHI in export configs |
- [ ] **[BI13]**  Documentation: data dictionary published, metric definitions accessible, dashboard inventory maintained, lineage tracked
- [ ] **[BI14]**  Reconciliation: board metrics reconciled against source systems monthly; discrepancies investigated and documented
