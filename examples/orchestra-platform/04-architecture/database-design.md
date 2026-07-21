# Database Design

## Schema — Services Domain (7 Tables)

**services**: Core entity. Columns: `id` (UUID, PK), `org_id` (UUID, FK → organizations), `name` (VARCHAR 255), `description` (TEXT), `service_type` (ENUM: api, web, cron, pipeline, plugin), `health_status` (ENUM: healthy, degraded, down), `created_at`, `updated_at`, `deleted_at` (soft delete).

**service_versions**: Immutable version history. Columns: `id` (UUID, PK), `service_id` (UUID, FK), `version` (SEMVER VARCHAR 32), `config_snapshot` (JSONB), `deployed_by` (UUID, FK → users), `deployed_at`, `rollback_target` (BOOLEAN).

**service_owners**: Many-to-many relationship. Columns: `service_id` (UUID, FK), `user_id` (UUID, FK), `role` (ENUM: owner, maintainer, viewer), `assigned_at`. Composite PK on (service_id, user_id).

**templates**: Scaffolding blueprints. Columns: `id` (UUID, PK), `org_id` (UUID, FK), `name`, `type`, `source_repo` (VARCHAR 512), `version`, `variables_schema` (JSONB), `is_public` (BOOLEAN), `created_at`.

**template_executions**: Audit log of template usage. Columns: `id` (UUID, PK), `template_id` (UUID, FK), `user_id` (UUID, FK), `parameters` (JSONB), `status` (ENUM: running, success, failed), `result_service_id` (UUID, FK → services), `started_at`, `completed_at`, `error_log` (TEXT, nullable).

**plugins**: Marketplace entities. Columns: `id` (UUID, PK), `name`, `description`, `author` (VARCHAR 255), `version`, `entrypoint` (VARCHAR 512), `icon_url`, `download_count` (INTEGER), `created_at`.

**plugin_configs**: Per-organization plugin settings. Columns: `id` (UUID, PK), `plugin_id` (UUID, FK), `org_id` (UUID, FK), `config` (JSONB), `enabled` (BOOLEAN), `updated_at`. UNIQUE constraint on (plugin_id, org_id).

## Indexing Strategy

- **Composite indexes**: `idx_services_org_type ON services(org_id, service_type)` — primary query pattern for catalog filtering. `idx_template_executions_template_time ON template_executions(template_id, created_at DESC)` — execution history lookups. `idx_plugin_configs_org ON plugin_configs(org_id, enabled)` — active plugin listing.
- **Partial indexes**: `idx_services_active ON services(org_id) WHERE deleted_at IS NULL` — excludes soft-deleted rows from 90% of queries.
- **GIN indexes**: `idx_service_versions_config ON service_versions USING GIN(config_snapshot)` — JSONB query support for config diffing.

## Migration Plan

Using `golang-migrate` v4.17 with sequential up/down SQL files in `migrations/`. Naming convention: `{timestamp}_{description}.up.sql` and `{timestamp}_{description}.down.sql`. CI pipeline runs `migrate up` against a temporary database to validate migrations before merge. Production migrations run via a Kubernetes Job with `--deployment-lock` to prevent concurrent execution.

## Data Retention Policy

- **services** + **service_versions**: Retain indefinitely (core business data).
- **template_executions**: 90 days hot storage (indexed), archive to S3 as gzipped JSON after 90 days, auto-purge from primary after 365 days.
- **plugin_configs**: Retain while organization is active, purge 30 days after org deletion.
- **Soft-deleted records**: Hard-delete after 180 days via nightly cron job.
