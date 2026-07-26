## Phase 1B: Business Telemetry Impact Scan

Execute after Phase 1 (Blast Radius Analysis) when any of these are detected:
- dbt project files (`dbt_project.yml`, `models/**/*.sql`)
- Analytics event schemas (Mixpanel, Amplitude, PostHog, Segment, Rudderstack)
- Customer support troubleshooting runbooks referencing API behavior
- Marketing automation triggers dependent on event properties
- Data science notebook schemas or dashboard SQL queries

### Step 1: dbt Model Dependency Scan (~15 min)

```
1. FIND ALL dbt PROJECTS IN SCOPE
   |-- Search across org repos: rg "dbt_project.yml" --glob "**/dbt_project.yml"
   |-- For each project, list all models: rg "model" **/dbt_project.yml
   |-- Identify which models reference the affected table/column

2. COLUMN-LEVEL LINEAGE
   |-- For each affected column: rg "column_name" **/models/**/*.sql
   |-- Classify each reference:
   |   |-- Direct SELECT: `SELECT column_name FROM source` → WILL BREAK
   |   |-- Derived/transformed: `column_name * 1.1 AS adjusted` → WILL BREAK
   |   |-- Used in WHERE/JOIN: `WHERE column_name IS NOT NULL` → WILL BREAK
   |   |-- Commented/documentation: `-- uses column_name` → LOW IMPACT
   |-- Count: total dbt model references = _____

3. DOWNSTREAM DASHBOARD IMPACT
   |-- For each affected dbt model: who consumes this model?
   |   |-- BI tools (Looker, Tableau, Metabase, PowerBI) — check model name in BI config
   |   |-- Reverse ETL (Hightouch, Census) — check sync configs
   |   |-- Embedded analytics — check application code
   |   |-- Internal reports — check scheduled jobs, email reports
   |-- Document: "Model `dim_customers` feeds 3 Looker dashboards used by Sales VP weekly"

4. MITIGATION
   |-- Option A: Create new column alongside old (Expand-Contract pattern)
   |   |-- Phase 1: Add new_column to source table, write to both
   |   |-- Phase 2: Update dbt models to read from new_column
   |   |-- Phase 3: Deprecate old_column after all models migrated
   |   |-- Phase 4: Remove old_column after 30 days zero reads
   |-- Option B: Version the dbt model
   |   |-- Create `dim_customers_v2` alongside `dim_customers`
   |   |-- Consumers migrate at their own pace
   |   |-- Deprecate v1 when zero consumers remain
   |-- Option C: DBT snapshot/SCD before change
   |   |-- Capture current state as SCD Type 2
   |   |-- Historical dashboards continue working with old data

⚠️ **War story:** A team changed `orders.status` from VARCHAR to ENUM in Postgres. The migration was
clean — zero application errors. But 3 dbt models had `SELECT status FROM orders` with downstream
Looker dashboards. The ENUM change made `status` values sort differently in Looker. The Sales VP's
"Orders by Status" dashboard showed garbled data for 2 weeks before anyone noticed. The data was
correct in the database — it was the analytics pipeline that silently broke. Cost: $25K in lost
pipeline time and 3 emergency data fix sprints.
```

### Step 2: Analytics Event Schema Scan (~10 min)

```
1. IDENTIFY ANALYTICS PLATFORM
   |-- Search for SDK imports: rg "(mixpanel|amplitude|posthog|segment|rudderstack)" --glob "*.{js,ts,py,java,go,rb}"
   |-- Search for tracking configs: rg "track\|identify\|page\|group\|alias" --glob "*.{js,ts,py}"
   |-- Check for analytics middleware/wrappers: custom tracking libraries

2. EVENT PROPERTY DEPENDENCY MAP
   |-- For each `track('event_name', { properties })` call containing the affected field:
   |   |-- Event name: ________
   |   |-- Property name: ________ (the field being changed/removed)
   |   |-- Property type: string / number / boolean / object
   |-- If changing property TYPE: 🛑 STOP. Analytics platforms enforce schema types.
   |   |-- Changing `user_id` from string to number = all historical data orphaned
   |   |-- Changing `amount` from number to string = all funnels/revenue reports break
   |-- If adding/removing property: 🟡 Smaller blast radius, but still affects:
   |   |-- Cohorts defined on that property
   |   |-- Funnels filtering by that property
   |   |-- Dashboards with breakdowns by that property
   |   |-- Marketing automation triggered by property values (Braze, Customer.io, HubSpot)

3. DOCUMENT CONSUMERS
   |-- Who uses this event property? (Check analytics platform UI)
   |   |-- Product analytics dashboards: _____
   |   |-- Marketing automation workflows: _____
   |   |-- A/B test configurations: _____
   |   |-- Data warehouse syncs (Segment Reverse ETL, etc.): _____

⚠️ **War story:** A team renamed `plan_type` to `subscription_tier` in their tracking code. The rename
took 15 minutes in the codebase. But 47 Mixpanel dashboards, 12 Braze marketing automations, and
an A/B test with 50K users were all keyed on `plan_type`. The rename created a NEW property
`subscription_tier` while `plan_type` went to zero. Dashboards showed "No data" for 3 days.
Marketing sent "Your trial is ending" emails to paying customers because the `plan_type = 'trial'`
filter matched zero users (all data was now under `subscription_tier`). Cost: $12K in incorrect
marketing sends + 8 hours emergency dashboard rewiring.
```

### Step 3: Customer Support Documentation Scan (~5 min)

```
1. FIND SUPPORT DOCS REFERENCING THE AFFECTED BEHAVIOR
   |-- Search internal wiki/knowledge base: rg "affected_field\|old_behavior" --glob "*.md"
   |-- Search runbooks/playbooks: rg "affected_field" --glob "**/runbooks/**"
   |-- Search auto-remediation scripts: rg "affected_field" --glob "*.{sh,py,js}"
   |-- Search Zendesk/Intercom macros referencing the field

2. IMPACT ASSESSMENT
   |-- Support agent troubleshooting steps: "Check the user's plan_type in the admin panel"
   |   |-- If field is renamed: support docs become confusing (old name no longer exists)
   |   |-- If field is removed: support docs reference non-existent UI
   |-- Auto-remediation scripts: `curl /api/v1/users?plan_type=enterprise`
   |   |-- If endpoint changes: script silently fails, incidents go unresolved longer
   |-- Customer-facing documentation: API docs, help center articles, error message copy

3. MITIGATION
   |-- Before change: update all support docs, runbooks, and scripts
   |-- Coordinate with support team: announce change 2 weeks before it ships
   |-- Add redirect/alias: if `plan_type` → `subscription_tier`, accept both in API for 6 months
```

### Step 4: Marketing Automation Impact Scan (~5 min)

```
1. FIND MARKETING TRIGGERS ON AFFECTED EVENTS
   |-- Search for marketing platform configs: rg "(braze|customer.io|hubspot|market|iterable|klaviyo)"
   |-- Check for webhook triggers: rg "webhook.*affected_field\|trigger.*affected_field"
   |-- Check for email template personalization: `{{ user.plan_type }}`, `{{ event.plan_type }}`

2. IMPACT ASSESSMENT
   |-- Lifecycle emails: "Welcome to the {{ plan_type }} plan!"
   |   |-- If plan_type changes → emails show wrong plan name or empty string
   |-- Triggered campaigns: "Users on enterprise plan who haven't logged in for 7 days"
   |   |-- If plan_type renamed → zero users match → campaign silently stops
   |-- Lead scoring: `plan_type = 'enterprise'` → +50 points
   |   |-- If renamed → enterprise leads lose their score → sales pipeline drops

⚠️ **War story:** A team changed their pricing model, renaming `plan_type: 'growth'` to `plan_type: 'pro'`.
The tracking code was updated in all 4 services. But the Braze integration had a hardcoded filter:
`plan_type != 'growth'`. After the rename, NO users had `plan_type = 'growth'`, so ALL users matched
the filter. A "We miss you, come back!" re-engagement campaign sent to 100% of the user base instead
of the intended 15% churned segment. 850K emails sent in 30 minutes before the campaign was killed.
```

### Phase 1B Output: Combined Impact Matrix

| Impact Domain | Affected Artifacts | Severity | Mitigation Timeline |
|---|---|---|---|
| dbt Models | [N] models referencing [column] | 🔴 HIGH | 2-4 weeks (model migration) |
| Analytics Events | [N] dashboards, [N] automations | 🔴 HIGH | 1-3 weeks (schema migration) |
| Support Docs | [N] runbooks, [N] macros | 🟡 MEDIUM | 1-2 weeks (doc updates) |
| Marketing Automation | [N] campaigns, [N] triggers | 🔴 HIGH | 1-2 weeks (campaign rewiring) |
| Data Science Notebooks | [N] notebooks, [N] scheduled jobs | 🟡 MEDIUM | 1-2 weeks (notebook updates) |

**Decision Gate:** If ANY domain has 🔴 HIGH severity → apply Expand-Contract pattern (Phase 2: Comet-Style Migration).
Do NOT "break and fix forward" when business telemetry is involved. A silent data pipeline failure can
persist for weeks before detection, corrupting decisions made on bad data. The cost of Expand-Contract
is always less than the cost of corrupted business analytics.
