# Platform Engineering

## Backstage Developer Portal

Backstage v1.29 deployed as the internal developer portal, customized with the Orchestra brand theme (purple primary, Inter font family, Orchestra logo in the sidebar). The Software Catalog is populated via a custom `OrchestraEntityProvider` that syncs services, templates, and plugins from the Orchestra API every 5 minutes. TechDocs enabled for all internal services — documentation auto-published on push to `main` via a GitHub Actions plugin.

## Golden Path Templates

Five Backstage scaffolder templates provide self-service infrastructure creation:

1. **New Go Service**: Scaffolds a Go 1.22 service with `cmd/`, `internal/`, `pkg/` layout, Dockerfile, Helm chart, and GitHub Actions CI pipeline. Provisions an ECR repository, IAM role (IRSA), and a Kubernetes namespace. Average creation time: 4 minutes.

2. **New React App**: Next.js 14 project with TypeScript, Tailwind, shadcn/ui, ESLint + Prettier configs, and Vercel deployment config. Includes Storybook setup and component test scaffolding.

3. **New Cron Job**: Go binary with cron scheduling library, dead-letter queue integration (SQS), alerting via PagerDuty webhook, and a runbook template in the repo README.

4. **New Data Pipeline**: Airbyte connector configuration, dbt model scaffolding with example SQL, Great Expectations suite template, and scheduled execution via Prefect.

5. **New Plugin**: Orchestra plugin SDK project with `Plugin` interface implementation, manifest file, GitHub release workflow, and automated publishing to the internal plugin registry.

## Self-Service Infrastructure

Backstage scaffolder integrates with Terraform Cloud via the `terraform` action. Each golden path template triggers a Terraform run that provisions cloud resources using shared modules from `terraform-orchestra-modules` (private GitHub repo). Modules include: `eks-service` (namespace + service account + IRSA role), `rds-database` (Aurora instance with encryption + backup), `s3-bucket` (with versioning + lifecycle policies), and `cloudfront-distribution` (with WAF association).

## Developer CLI — `orc`

The `orc` CLI is distributed via Homebrew (`brew install orchestra/tap/orc`). Commands:

- `orc catalog list --org acme --filter type=api` — list services with filters
- `orc template create --name my-service --type go-api --port 8080` — interactive template wizard
- `orc plugin install prometheus-exporter --org acme` — install and configure a plugin
- `orc logs --service my-service --follow --tail 100` — stream structured logs from Loki
- `orc deploy --service my-service --env staging` — trigger a deployment pipeline

Authentication via `orc login` opens a browser OAuth flow with Auth0, storing a refresh token in the system keychain (macOS Keychain, GNOME Keyring on Linux).

## Developer Onboarding

New engineers complete onboarding in **15 minutes** from laptop setup to first service creation. Process: install `orc` CLI → `orc login` → select golden path template → fill 5 fields (name, team, language, port, description) → wait 4 minutes → service deployed with DNS, monitoring, and CI/CD pipeline ready. Onboarding measured: 23 new hires onboarded, median time-to-first-deployment 13.4 minutes.
