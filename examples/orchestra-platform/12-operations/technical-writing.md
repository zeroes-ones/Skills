# Technical Writing

## API Documentation

All Go services expose OpenAPI 3.1 specifications generated from code annotations using `swaggo/swag`. Specifications are validated in CI against the OpenAPI schema and must include a `description` and at least one `example` for every endpoint, parameter, and response body. Aggregated API docs are published at `docs.orchestra.dev/api` using Redoc (chosen over Swagger UI for its superior search, three-panel layout, and code sample generation). Redoc renders all 47 endpoints across 5 services with curl, Go, Python, and Node.js code samples auto-generated from the OpenAPI schema.

## Architecture Decision Records (ADRs)

Architecture Decision Records published at `docs.orchestra.dev/adr`. Each ADR follows the Michael Nygard format: Title, Status (proposed/accepted/deprecated/superseded), Context (the problem and constraints), Decision (what we chose and why), Consequences (what becomes easier and harder). 17 ADRs published to date covering key decisions: "ADR-001: Use Go for Backend Services" (performance + single binary deployment), "ADR-004: BFF Pattern with Next.js" (security + type sharing), "ADR-009: Expand-Contract for Database Migrations" (zero-downtime deploys), "ADR-014: mTLS via Istio" (zero-trust networking). ADRs are version-controlled alongside code in `docs/adr/` and rendered by Docusaurus.

## Onboarding Guide

The 5-step quickstart at `docs.orchestra.dev/quickstart` is the most-visited documentation page (1,200 unique visitors/month). Steps: (1) Sign up at orchestra.dev/signup — 30 seconds, (2) Create a team and invite members — 1 minute, (3) Pick a template from the catalog — 2 minutes, (4) Configure and deploy your first service — 4 minutes, (5) Invite team members to collaborate — 1 minute. Each step includes a screenshot and a "Troubleshooting" callout for common issues. Completion tracking via Rudderstack events: 68% of quickstart visitors reach step 5 (deployment success).

## Changelog

Published at `docs.orchestra.dev/changelog` following the keepachangelog.com format (Added, Changed, Deprecated, Removed, Fixed, Security sections). Every release (bi-weekly) includes a changelog entry. Entries link to relevant GitHub issues, PRs, and documentation updates. RSS feed available for automated changelog monitoring. Example entry for v0.9.0: 4 Added (Template Wizard, Plugin Config UI, Admin Dashboard, German locale), 2 Changed (improved catalog search performance, updated color contrast for WCAG compliance), 3 Fixed (BUG-412, BUG-415, BUG-418).

## Runbook Templates

Standardized runbook templates stored in the operations repo (`runbooks/`). Templates cover: Incident Response (step-by-step for detection, triage, mitigation, resolution, postmortem), Deployment (pre-deployment checklist, canary rollout, monitoring, rollback procedure), Rollback (feature flag disable, database migration revert, DNS failback, communication steps). Each runbook has a "Last Tested" date — runbooks older than 90 days without a test trigger a P3 Linear ticket for a dry-run exercise. All runbooks are executable via the `orc` CLI where possible (e.g., `orc deploy rollback --service my-service --version v1.2.0` wraps the manual steps documented in the runbook).
