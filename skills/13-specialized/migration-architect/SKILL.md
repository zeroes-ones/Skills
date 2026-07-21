---
name: migration-architect
description: Database migration strategies (expand-contract, blue-green, parallel run), cloud migration (6 R's), framework/language migration patterns, rollback strategy, stakeholder management, migration testing.
author: Sandeep Kumar Penchala
---

# Migration Architect

A veteran's playbook for planning and executing every type of production migration — database schema changes, platform swaps, language rewrites, framework upgrades, and cloud transitions — with zero downtime, military-grade rollback capability, and stakeholder trust.

This is not a theory document. Every section contains specific code, commands, scripts, and decision trees you can use tomorrow.

## Sub-Skills

When the agent encounters a specific migration type, drill into the relevant sub-skill rather than reading the full 1600+ line SKILL.md. Each sub-skill has dedicated patterns, scripts, and rollback plans.

| Sub-Skill | What It Covers | When to Load |
|-----------|---------------|--------------|
| **Database Schema Migration** | Expand-contract phases, online schema change tools (gh-ost, pgroll), `CREATE INDEX CONCURRENTLY`, backward-compatible schema evolution rules | Changing table structure in production |
| **Data Migration** | Batch processing with checkpointing, CDC (Debezium/Kafka), dual-write consistency verification, streaming data pipelines | Backfilling or transforming >100K rows |
| **Cloud Migration** | 6 R's framework (Rehost/Replatform/Repurchase/Refactor/Retire/Retain), wave planning, TCO analysis, AWS DMS/Application Migration Service | Moving infrastructure between providers or on-prem → cloud |
| **Framework & Library Migration** | Dependency graph analysis, adapter/wrapper pattern, gradual replacement with feature flags, real-world migration recipes (jQuery→React, REST→GraphQL, Express→Fastify) | Upgrading or swapping a major dependency |
| **Language Migration** | Strangler fig at module boundary, interop patterns (sidecar, gRPC, shared queue), when it makes business sense vs rewrite | Porting Python→Go, Ruby→Elixir, JS→TS, Java→Kotlin |
| **Rollback Engineering** | Per-phase rollback plans, feature flag kill switches, reverse data sync (new→old), bake period design, automated rollback triggers | Any migration where rollback risk is non-trivial |
| **Migration Testing** | Parallel run verification (old vs new output diff), canary deployment with metric comparison, data integrity reconciliation, load test before/after comparison | Validating correctness before cutting over |

> **Token-saving rule:** A migration of a 5GB Postgres database doesn't need the cloud migration or language migration sub-skills. Load only what's relevant. Each section is self-contained with its own scripts, patterns, and checklists.

---

## 1. Assessment & Scoping

### Inventory Gathering

Before you touch a single migration tool, know every surface area:

**Systems inventory:**
```bash
# Internal — crawl service registry, CMDB, or k8s namespaces
kubectl get deployments --all-namespaces -o wide

# Also crawl: cron jobs, CI pipelines referencing prod, config maps with DB URLs
kubectl get cronjobs --all-namespaces
kubectl get configmaps --all-namespaces | grep -iE 'database|connection|endpoint|host'
```

**Database inventory — discover every data store with read/write access:**
```sql
-- Run this (or equivalent) against each DB to gauge surface area
SELECT table_schema,
       table_name,
       (pg_total_relation_size(quote_ident(table_schema) || '.' || quote_ident(table_name))) / 1024 / 1024 AS size_mb,
       (SELECT reltuples::bigint FROM pg_class WHERE oid = (quote_ident(table_schema) || '.' || quote_ident(table_name))::regclass) AS estimated_rows
FROM information_schema.tables
WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY size_mb DESC;
```

**Service dependency inventory (for each service):**
- Every database connection string it uses (prod, read-replica, cache, queue)
- Every port it listens on
- Every external system it calls (internal API, 3rd-party SaaS, FTP, S3 bucket)
- File descriptors, temp directories, hardcoded IPs, environment-specific logic
- Cron jobs, scheduled tasks, dead-letter queues, DLQ consumers

### Complexity Scoring

Score each migration target on a 1–5 scale. Total score > 12 → this is high-risk, requires staged rollout.

| Factor | 1 (Low) | 3 (Medium) | 5 (High) |
|--------|---------|------------|---------|
| Row count | < 100K | 100K–10M | > 10M |
| Write throughput | < 100 writes/min | 100–10K/min | > 10K/min |
| Consumers (services) | 1–2 | 3–7 | 8+ |
| Schema coupling | No shared tables | Shared tables with other services | Shared tables + shared sequences + triggers |
| Risk (data loss) | Non-critical | Important but re-derivable | Financial/PHI/compliance |
| Rollback effort | Simple revert | Multiple services revert | Data sync-in-reverse required |

```python
# complexity_scorer.py — embed this in your playbook
def score_migration(rows: int, writes_per_min: int, consumers: int, has_shared_schema: bool, data_critical: bool) -> str:
    s = 0
    if rows > 10_000_000: s += 5
    elif rows > 100_000: s += 3
    else: s += 1
    if writes_per_min > 10_000: s += 5
    elif writes_per_min > 100: s += 3
    else: s += 1
    if consumers >= 8: s += 5
    elif consumers >= 3: s += 3
    else: s += 1
    if has_shared_schema: s += 3
    if data_critical: s += 3
    if s >= 12: return "HIGH — staged rollout, multiple pre-prod validations, extended bake"
    if s >= 8: return "MEDIUM — standard expand-contract, 48h bake, dedicated runbook"
    return "LOW — standard migration, 24h bake"
```

### Dependency Mapping

**Upstream/downstream map:** for each migration target, list everything that feeds into it and everything it feeds into.

**Hidden dependencies — the three that bite you every time:**

1. **Shared databases:** Service A and B read/write the same `orders` table. You migrate A's schema — B breaks silently because it still uses old column names. *Fix: assign table ownership to one service before migrating, create read-only views for consumers.*
2. **Hardcoded endpoints:** The configmap says `DB_HOST=db-primary.internal`. But the monitoring stack, the backup scripts, the ETL pipeline, and the legacy reporting cron all have `db-primary.internal` compiled in or in a forgotten `.env` on an old VM. *Fix: grep every repo, every cron box, every CI secret store for the hostname before migration.*
3. **Sequences and auto-increment IDs:** You migrate table A to a new DB, but the sequence generators are shared between tables in the old DB. New inserts on table B (still in old DB) create IDs that conflict with history. *Fix: decouple sequences before migration.*

### Risk Identification

| Risk Category | What to Check | Mitigation |
|---|---|---|
| **Data loss** | Is any row transformed but transformation is lossy? (BigDecimal → float, varchar truncation) | Snapshot before every phase. Test round-trip. |
| **Downtime** | Does any step require exclusive locks that block reads? | Use online schema tools (gh-ost, pgroll, CONCURRENTLY). |
| **Performance regression** | Does the new query path have same or better index coverage? | `EXPLAIN ANALYZE` old vs new before cutover. |
| **Compatibility** | Does the change break older API clients that haven't upgraded? | Versioned API. Deprecation headers. Feature-flag new behavior. |

### Build vs Buy Decision

| Scenario | Build Custom Script | Buy Managed Service |
|---|---|---|
| Simple column rename with expand-contract | ✓ — 50 lines of Python, no external infra | × — overkill |
| 2TB PostgreSQL → Aurora MySQL | × — months of edge cases (type mapping, trigger migration) | ✓ — AWS DMS handles CDC, type mapping, resumability |
| Custom ETL with complex business logic | ✓ — off-the-shelf tools can't express your domain rules | × — DMS transformations are limited |
| PCI/HIPAA data migration | × — need audit trail, encryption, rollback cert | ✓ — DMS with CloudTrail, or Stripe Sigma for financial data |
| FinTech — migrating payment processing from Provider A → B | ✓ + managed — custom mapping for payment states + managed CDC for transaction replay | Hybrid — custom for domain logic, managed for raw replication |

**Verdict:** For anything that touches customer money, compliance data, or has >50 tables with foreign-key chains — buy or hybrid. For internal tools, small schemas (<10 tables), or quick iterations — build.

---

## 2. Migration Patterns

### Lift-and-Shift (Rehost)

**When:** You need to move fast, risk tolerance is low, and you don't want to refactor.

**What:** Move the entire workload as-is — same OS, same DB, same config — just on new infrastructure.

```yaml
# docker-compose lift-and-shift example: postgres 13 → postgres 13 on new host
services:
  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_DB: legacy_db
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - /data/pg13_data_restore:/var/lib/postgresql/data
    ports:
      - "5432:5432"
```

```bash
# Lift-and-shift data move
pg_dump -h old-db.internal -U app_user -Fc legacy_db > /tmp/legacy_db.dump
pg_restore -h new-db.internal -U app_user -j 4 --no-owner --dbname=legacy_db /tmp/legacy_db.dump

# Update DNS/app config to point to new host
# Keep old DB up for 7-day rollback window
```

**Risks:** You preserve all the tech debt. Performance characteristics change (new hardware). Replication lag during switchover.

### Refactor-and-Migrate

**When:** The old system needs cleanup and you're going through the pain of migration anyway.

**What:** Improve the architecture during migration — break up the monolith, normalize the schema, adopt new patterns.

**Real example — migrating from a monolithic `items` table with a polymorphic `type` column to separate tables:**

```python
# Phase 1: Expand — create new tables alongside old
# migration_001_expand.py (run via Alembic)
"""
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE,
    page_count INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE electronics (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    warranty_months INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

# Phase 2: Migrate — dual-write and backfill
# backfill_items.py
import psycopg2
import time

BATCH_SIZE = 1000

conn = psycopg2.connect("dbname=shop")
cur = conn.cursor()

last_id = 0
while True:
    cur.execute("""
        SELECT id, title, type,
               attributes->>'author' AS author,
               attributes->>'isbn' AS isbn,
               attributes->>'brand' AS brand,
               attributes->>'model' AS model
        FROM items
        WHERE id > %s
        ORDER BY id
        LIMIT %s
    """, (last_id, BATCH_SIZE))
    rows = cur.fetchall()
    if not rows:
        break

    for row in rows:
        if row[2] == 'book':
            cur.execute("""
                INSERT INTO books (id, title, author, isbn)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (row[0], row[1], row[3], row[4]))
        elif row[2] == 'electronics':
            cur.execute("""
                INSERT INTO electronics (id, title, brand, model)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (row[0], row[1], row[5], row[6]))

    conn.commit()
    last_id = rows[-1][0]
    time.sleep(0.05)  # throttle

cur.close()
conn.close()
```

**Trade-off:** Higher risk, longer timeline. But you won't be doing this again next year.

### Strangler Fig

**Best for:** Large monoliths, high-risk replacements, systems where the old version is actively maintained while the new version is built.

**How it works:**

```
        ┌─────────────┐
        │  API Gateway │
        └──────┬──────┘
               │
        ┌──────┴──────┐
        │   Router    │
        │(feature flag│
        │ per route)  │
        └──────┬──────┘
               │
     ┌─────────┴──────────┐
     ▼                    ▼
┌──────────┐      ┌──────────┐
│ Legacy   │      │ New      │
│ System   │      │ Service  │
│ (old)    │      │ (new)    │
└──────────┘      └──────────┘
```

**Implementation with feature flags:**

```javascript
// router.js — strangler fig routing
const featureFlags = require('./feature-flags');

async function handleRequest(req, res) {
  const route = req.path;

  if (featureFlags.isEnabled('orders:new') && route.startsWith('/orders')) {
    return proxyToNewService(req, res);  // new system
  }

  if (featureFlags.isEnabled('users:50pct')) {
    const userId = req.user.id;
    if (hash(userId) < 0.5) {
      return proxyToNewService(req, res);  // 50% traffic
    }
  }

  return proxyToLegacy(req, res);  // old system
}
```

**Critical rule:** Migrate one domain boundary at a time. Don't strangler a third of the monolith — strangler one Bounded Context (orders, users, payments) completely, then move to the next.

### Parallel Run

**Best for:** Financial systems, critical data processing where correctness is paramount.

**Run old and new simultaneously. Compare outputs. Don't cut over until results match for N days.**

```python
# parallel_run_verifier.py
# Compares order totals from old and new systems
import json
from datetime import datetime, timedelta

def verify_parallel_run(orders_file_old: str, orders_file_new: str, tolerance: float = 0.01):
    """Compare order-by-order totals between old and new systems."""
    with open(orders_file_old) as f:
        old_orders = {o['order_id']: o for o in json.load(f)}
    with open(orders_file_new) as f:
        new_orders = {o['order_id']: o for o in json.load(f)}

    mismatches = []
    for oid, old in old_orders.items():
        if oid not in new_orders:
            mismatches.append({'order_id': oid, 'issue': 'missing_in_new'})
            continue
        new = new_orders[oid]
        if abs(old['total'] - new['total']) > tolerance:
            mismatches.append({
                'order_id': oid,
                'old_total': old['total'],
                'new_total': new['total'],
                'diff': old['total'] - new['total']
            })

    if mismatches:
        print(f"PARALLEL RUN FAILED: {len(mismatches)} mismatches out of {len(old_orders)} orders")
        for m in mismatches[:10]:
            print(json.dumps(m, indent=2))
        return False
    else:
        print(f"PARALLEL RUN PASSED: {len(old_orders)} orders match within tolerance")
        return True

if __name__ == '__main__':
    verify_parallel_run('orders_old_2026-07-20.json', 'orders_new_2026-07-20.json')
```

**Run cadence:** compare hourly during first day, daily during first week, weekly after that. Cut over after N consecutive successful comparisons (your call — 7 days for low-risk, 30 days for financial).

### Blue-Green Cutover

**Best for:** Deployments, platform migrations, database migrations where you want instant switch and instant rollback.

```yaml
# docker-compose blue-green setup
services:
  app-blue:
    image: myapp:${BLUE_TAG:-v1.0.0}
    ports:
      - "8081:8080"
    environment:
      - DATABASE_URL=postgres://user:pass@db-blue:5432/app
    depends_on: [db-blue]

  app-green:
    image: myapp:${GREEN_TAG:-v2.0.0}
    ports:
      - "8082:8080"
    environment:
      - DATABASE_URL=postgres://user:pass@db-green:5432/app
    depends_on: [db-green]

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx-blue-green.conf:/etc/nginx/conf.d/default.conf
    ports:
      - "443:443"
```

```nginx
# nginx-blue-green.conf — active environment controlled by upstream name
upstream backend {
    server app-blue:8080;  # switch to app-green:8080 on cutover
}

server {
    listen 443 ssl;
    location / {
        proxy_pass http://backend;
    }
}
```

**Cutover script:**
```bash
#!/bin/bash
# cutover-to-green.sh
# 1. Warm the green environment
curl -s -o /dev/null -w "%{http_code}" http://app-green:8080/health

# 2. Final data sync (if DB migration)
pg_dump -h db-blue -U app app_db | psql -h db-green -U app app_db

# 3. Switch traffic
sed -i 's/app-blue:8080/app-green:8080/' nginx-blue-green.conf
nginx -s reload

# 4. Verify
if curl -s http://localhost/health | grep -q "OK"; then
  echo "Green cutover successful"
else
  echo "Green unhealthy — rolling back"
  sed -i 's/app-green:8080/app-blue:8080/' nginx-blue-green.conf
  nginx -s reload
fi
```

### Decision Matrix

| Pattern | Risk | Downtime | Complexity | Timeline | Best for |
|---|---|---|---|---|---|
| Lift-and-shift | Low | Minimal (1 restart) | Low | Shortest | Emergency moves, cloud migrations, compliance deadlines |
| Refactor-and-migrate | Medium-High | Depends on approach | High | Longest | Systems already needing overhaul |
| Strangler fig | Low | Zero | High | Long | Large monoliths, high-risk replacements |
| Parallel run | Very Low | Zero | Medium | Medium | Financial systems, critical data processing |
| Blue-green | Low | Near-zero | Medium | Short-Medium | Platform swaps, deployments, DB platform changes |
| Expand-contract | Low | Zero | Medium | Medium | Schema changes, column renames, type changes |

---

## 3. Database Migration (Deep Dive)

### Expand-Contract Pattern — Detailed Phases with Code

**The single most important migration pattern. Every production DB migration should use this unless you have a strong reason not to.**

**Phase 1 — Expand: Add new schema alongside old.**

```sql
-- Expand: add new column `email_verified` alongside old design
-- Old schema: users has phone_verified (boolean)
-- New schema: verify both email and phone
-- Step 1: Add nullable column
ALTER TABLE users ADD COLUMN email_verified BOOLEAN;
ALTER TABLE users ADD COLUMN email_verified_at TIMESTAMPTZ;
```

**Phase 2 — Migrate: Dual-write + backfill.**

```python
# Application code: write to both old and new
class UserService:
    def verify_user(self, user_id: int, method: str):
        with db.transaction():
            if method == 'email':
                # Write to new columns
                db.execute("UPDATE users SET email_verified = TRUE, email_verified_at = NOW() WHERE id = %s", user_id)
                # Also write to old column (backward compat)
                db.execute("UPDATE users SET phone_verified = TRUE WHERE id = %s", user_id)
            elif method == 'phone':
                db.execute("UPDATE users SET phone_verified = TRUE WHERE id = %s", user_id)
```

```python
# backfill_users.py — batch backfill historically verified users
# Run after expand, before contract
import psycopg2
import time

conn = psycopg2.connect("dbname=mydb")
cur = conn.cursor()

BATCH = 500
last_id = 0

while True:
    cur.execute("""
        UPDATE users
        SET email_verified = TRUE,
            email_verified_at = updated_at
        WHERE id > %s
          AND phone_verified = TRUE
          AND email_verified IS NULL
        ORDER BY id
        LIMIT %s
        RETURNING id
    """, (last_id, BATCH))
    affected = cur.fetchall()
    conn.commit()

    if not affected:
        break
    last_id = affected[-1][0]
    time.sleep(0.1)  # throttle

print(f"Backfill complete. Last ID: {last_id}")
```

**Phase 3 — Contract: Switch reads, then remove old.**

```python
# Application code: after backfill, deploy code that reads from new column
class UserService:
    def is_user_verified(self, user_id: int) -> bool:
        result = db.query("SELECT email_verified FROM users WHERE id = %s", user_id)
        return bool(result[0]['email_verified'])  # reads from new column

# After confirming no code reads phone_verified:
-- Contract: drop the old column
ALTER TABLE users DROP COLUMN phone_verified;
```

### Schema Evolution Rules

| Action | Safe? | Notes |
|---|---|---|
| Add nullable column | ✓ Safe | No existing rows affected. Reads that don't SELECT * are unaffected. |
| Add table | ✓ Safe | No existing consumers reference it. |
| Add index (CONCURRENTLY) | ✓ Safe | No lock on the table. Takes longer but non-blocking. |
| Add index (non-CONCURRENTLY) | ✗ Risky | Blocks writes on the table. For small tables (< 1M rows) OK. For large tables, use CONCURRENTLY. |
| Add NOT NULL column w/ default | ✓ Safe | In Postgres 11+, adding a column with DEFAULT no longer rewrites the table. Still avoid this. |
| Add NOT NULL column w/o default | ✗ Requires pattern | Add nullable → backfill → ALTER SET NOT NULL |
| Change column data type | ✗ Requires pattern | Add new column with new type → dual-write → backfill → switch reads → drop old |
| Rename column | ✗ Requires pattern | Add column with new name → dual-write → backfill → switch reads → drop old column |
| Remove column | ✗ Requires verification | Confirm zero deployed code reads it. Use access logs or static analysis. |
| Remove table | ✗ Requires verification | Confirm zero deployed code references it. Use database access logging. |
| Change primary key | ✗ High-risk | Extremely difficult online. Consider adding a new unique constraint + index instead. |
| Split table | ✗ Requires pattern | Create new tables → dual-write → backfill → switch reads → drop old table |
| Merge tables | ✗ High-risk | Create merged table → dual-write → backfill → switch reads → drop old tables |

### Data Migration: Batch vs Streaming vs Dual-Write

**Batch processing — for one-time backfills:**

```python
# batch_migrate.py — production-grade batch processor
import psycopg2
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BatchMigrator:
    def __init__(self, conn_string: str, batch_size: int = 1000, throttle_s: float = 0.05):
        self.conn_string = conn_string
        self.batch_size = batch_size
        self.throttle_s = throttle_s
        self.checkpoint_table = "migration_checkpoints"

    def migrate(self, source_query: str, target_query: str, extract_fn, checkpoint_key: str):
        conn = psycopg2.connect(self.conn_string)
        cur = conn.cursor()

        # Ensure checkpoint table exists
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.checkpoint_table} (
                key TEXT PRIMARY KEY,
                last_id BIGINT,
                updated_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        conn.commit()

        # Resume from checkpoint
        cur.execute("SELECT last_id FROM migration_checkpoints WHERE key = %s", (checkpoint_key,))
        row = cur.fetchone()
        last_id = row[0] if row else 0
        start_time = datetime.now()

        processed = 0
        while True:
            cur.execute(source_query, (last_id, self.batch_size))
            rows = cur.fetchall()
            if not rows:
                break

            for row in rows:
                target_data = extract_fn(row)
                cur.execute(target_query, target_data)

            last_id = rows[-1][0]
            processed += len(rows)

            # Update checkpoint
            cur.execute("""
                INSERT INTO migration_checkpoints (key, last_id, updated_at)
                VALUES (%s, %s, NOW())
                ON CONFLICT (key) DO UPDATE SET last_id = EXCLUDED.last_id, updated_at = EXCLUDED.updated_at
            """, (checkpoint_key, last_id))
            conn.commit()

            elapsed = (datetime.now() - start_time).total_seconds()
            rate = processed / elapsed if elapsed > 0 else 0
            logger.info(f"Processed {processed} rows | Rate: {rate:.0f} rows/sec | Last ID: {last_id}")

            time.sleep(self.throttle_s)

        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"Migration complete: {processed} rows in {elapsed:.0f}s ({processed/elapsed:.0f} rows/sec)")
        cur.close()
        conn.close()
```

**Streaming (CDC with Debezium/Kafka) — for zero-downtime continuous sync:**

```json
// debezium-connector.json — Debezium PostgreSQL connector config
{
  "name": "cdc-migration-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "old-db.internal",
    "database.port": "5432",
    "database.user": "cdc_user",
    "database.password": "${CDC_PASSWORD}",
    "database.dbname": "legacy_db",
    "database.server.name": "legacy",
    "plugin.name": "pgoutput",
    "table.include.list": "public.orders,public.users,public.products",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "slot.name": "migration_slot",
    "slot.max.retries": 5,
    "publication.name": "migration_pub",
    "publication.autocreate.mode": "filtered",
    "tombstones.on.delete": "false"
  }
}
```

```python
# cdc_consumer.py — consume CDC events and write to new DB
from kafka import KafkaConsumer
import json
import psycopg2

consumer = KafkaConsumer(
    'legacy.public.orders',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

new_conn = psycopg2.connect("dbname=new_db")
new_cur = new_conn.cursor()

for msg in consumer:
    event = msg.value
    op = event.get('__op')  # 'c' = create, 'u' = update, 'd' = delete
    after = event.get('after', {})

    if op == 'd':
        new_cur.execute("DELETE FROM orders WHERE id = %s", (after.get('id'),))
    elif op in ('c', 'u'):
        new_cur.execute("""
            INSERT INTO orders (id, user_id, total, status, created_at)
            VALUES (%(id)s, %(user_id)s, %(total)s, %(status)s, %(created_at)s)
            ON CONFLICT (id) DO UPDATE SET
                user_id = EXCLUDED.user_id,
                total = EXCLUDED.total,
                status = EXCLUDED.status
        """, after)
    new_conn.commit()
```

**Dual-write consistency — the hardest problem in migration:**

```python
# Verify dual-write consistency (sample-based)
# Run periodically during dual-write phase
import psycopg2
import random

def verify_dual_write_consistency(sample_pct: float = 0.01):
    old = psycopg2.connect("dbname=old_db")
    new = psycopg2.connect("dbname=new_db")
    old_cur = old.cursor()
    new_cur = new.cursor()

    # Get row count
    old_cur.execute("SELECT COUNT(*) FROM orders")
    n = old_cur.fetchone()[0]

    sample_size = int(n * sample_pct)
    sampled_ids = set()
    old_cur.execute("SELECT id FROM orders ORDER BY RANDOM() LIMIT %s", (sample_size,))
    for row in old_cur:
        sampled_ids.add(row[0])

    mismatches = 0
    for oid in sampled_ids:
        old_cur.execute("SELECT total, status FROM orders WHERE id = %s", (oid,))
        new_cur.execute("SELECT total, status FROM orders WHERE id = %s", (oid,))
        old_row = old_cur.fetchone()
        new_row = new_cur.fetchone()
        if not new_row:
            mismatches += 1
            continue
        if old_row != new_row:
            mismatches += 1

    if mismatches == 0:
        print(f"✓ Dual-write consistent on sample of {sample_size} rows")
    else:
        print(f"✗ Dual-write mismatch on {mismatches}/{sample_size} rows — investigate immediately")

    old.close()
    new.close()
```

### Migration Frameworks Comparison

| Feature | Flyway | Liquibase | Alembic | Prisma Migrate | golang-migrate | atlas | goose |
|---|---|---|---|---|---|---|---|
| Language | Java (JVM langs) | Java (JVM langs) | Python | TypeScript/Node | Go | Go | Go |
| Migration format | SQL + Java | XML/YAML/JSON/SQL | Python (autogen from models) | Declarative (schema.prisma) | SQL | Declarative HCL + SQL | SQL + Go |
| Auto-generation | No | No | Yes (from SQLAlchemy models) | Yes (from Prisma schema) | No | Yes (from DB or HCL) | No |
| Checksums | ✓ | ✓ | ✓ | ✓ (lint) | ✗ | ✓ | ✗ |
| Down migrations | ✓ | ✓ | ✓ | ✗ (prisma db execute) | ✓ | ✓ | ✓ |
| Online schema | No | No | No | No | No | Yes (with pgroll) | No |
| Multi-DB support | PostgreSQL, MySQL, SQLite, SQL Server, Oracle, DB2, etc. | Same + MongoDB | PostgreSQL, MySQL, SQLite, MSSQL, etc. | PostgreSQL, MySQL, SQLite, SQL Server, MongoDB, CockroachDB | PostgreSQL, MySQL, SQLite, SQL Server, etc. | PostgreSQL, MySQL, SQLite, MariaDB | PostgreSQL, MySQL, SQLite, etc. |
| CI/CLI | Flyway CLI, Maven, Gradle | Liquibase CLI, Maven, Gradle | Alembic CLI | Prisma CLI | CLI | Atlas CLI | goose CLI |
| Best for | Java shops, enterprise | Enterprise with compliance/audit | Python/SQLAlchemy projects | TypeScript/Prisma shops | Go projects | Any project needing schema management | Go projects |
| Locking | Schema version table lock | Lock table | No built-in lock | Shadow DB validation | Advisory lock | Advisory lock | No built-in lock |

### Online Schema Change Tools

| Tool | DB | Mechanism | Locking | Best for |
|---|---|---|---|---|
| **gh-ost** | MySQL | Triggerless — reads binlog, applies to ghost table | Minimal | Large MySQL tables, high write volume |
| **pt-online-schema-change** | MySQL | Triggers — creates ghost table, applies changes via triggers | Brief table-level lock at start and end | MySQL tables where gh-ost can't be used (no binlog_format=ROW) |
| **pgroll** | PostgreSQL | Shadow tables + triggers + concurrent index | Minimal | PostgreSQL, zero-downtime schema changes |
| **CONCURRENTLY** | PostgreSQL | Index built in background | No lock on writes | Adding/changing indexes only, not column changes |
| **pg_repack** | PostgreSQL | Online table rebuild | Minimal lock at the end (swapping tables) | Reclaiming bloat, reordering rows |

**pgroll example — add column with zero downtime:**
```bash
pgroll init --dsn "postgres://user:pass@localhost:5432/mydb"
pgroll add-column users email_verified boolean --default false
pgroll migrate users --complete
```

### Consistency Verification

```sql
-- 1. Row count comparison
SELECT 'old_db' AS source, COUNT(*) AS row_count FROM orders
UNION ALL
SELECT 'new_db' AS source, COUNT(*) AS row_count FROM new_db.public.orders;

-- 2. Checksum comparison (full table hash)
SELECT MD5(array_agg(id || '-' || total || '-' || status || '-' || created_at)::text) AS checksum FROM orders;

-- 3. Per-row sampling with hashed comparison
WITH sampled AS (
    SELECT id, MD5(id || '-' || COALESCE(total, 0) || '-' || COALESCE(status, '') || '-' || COALESCE(created_at::text, '')) AS row_hash
    FROM orders
    WHERE id % 100 = 0  -- sample every 100th row
)
SELECT COUNT(*) AS mismatches
FROM sampled s
JOIN new_db.public.orders n ON s.id = n.id
WHERE s.row_hash != MD5(n.id || '-' || COALESCE(n.total, 0) || '-' || COALESCE(n.status, '') || '-' || COALESCE(n.created_at::text, ''));

-- 4. Orphan detection: rows in old but not in new
SELECT COUNT(*) AS orphans_in_old
FROM orders o
LEFT JOIN new_db.public.orders n ON o.id = n.id
WHERE n.id IS NULL;
```

---

## 4. Framework/Library Migration

### Dependency Analysis

```bash
# Build a dependency graph before any library migration
# For Node/TypeScript:
npx madge --image dependency-graph.svg src/

# For Python:
pip install pipdeptree
pipdeptree --graph-output svg > dependency-graph.svg

# For Java:
# Use JDeps or Gradle's dependency graph

# Find all usages of the old library in your codebase
# Example: migrating from moment.js to date-fns
grep -r "moment(" src/ --include="*.ts" --include="*.tsx" | wc -l
grep -r "import.*moment" src/ --include="*.ts" --include="*.tsx" | wc -l
grep -r "from 'moment'" src/ --include="*.ts" --include="*.tsx" > moment_imports.txt
```

### Adapter Pattern

Wrap the old library in an abstraction layer before swapping implementations. This isolates the rest of your code from the change.

```typescript
// Phase 1: Define an abstraction
interface DateFormatter {
  format(date: Date, pattern: string): string;
  parse(dateString: string, pattern: string): Date;
  diff(date1: Date, date2: Date, unit: 'days' | 'hours' | 'minutes'): number;
}

// Phase 2: Implement with OLD library
class MomentDateFormatter implements DateFormatter {
  format(date: Date, pattern: string): string {
    return moment(date).format(pattern);
  }
  parse(dateString: string, pattern: string): Date {
    return moment(dateString, pattern).toDate();
  }
  diff(date1: Date, date2: Date, unit: 'days' | 'hours' | 'minutes'): number {
    return moment(date1).diff(moment(date2), unit);
  }
}

// Phase 3: Replace implementation with NEW library
class DateFnsDateFormatter implements DateFormatter {
  format(date: Date, pattern: string): string {
    return format(date, pattern);  // date-fns
  }
  parse(dateString: string, pattern: string): Date {
    return parse(dateString, pattern, new Date());
  }
  diff(date1: Date, date2: Date, unit: 'days' | 'hours' | 'minutes'): number {
    return differenceInDays(date1, date2);  // date-fns
  }
}

// Phase 4: Swap in the DI container
// Before: container.register('DateFormatter', MomentDateFormatter);
// After:  container.register('DateFormatter', DateFnsDateFormatter);
```

### Gradual Replacement with Feature Flags

```typescript
// middleware.ts — per-route library selection
import { Router } from 'express';
import { FeatureFlagService } from './feature-flags';

const router = Router();
const ff = new FeatureFlagService();

// REST → GraphQL migration: strangler per endpoint
router.all('/api/v1/orders', async (req, res) => {
  if (ff.isEnabled('orders:graphql')) {
    return graphqlHandler(req, res);     // new GraphQL endpoint
  }
  return restHandler(req, res);          // old REST endpoint
});

// Per-component migration (React example)
// OldComponent.tsx uses LegacyTable, NewComponent.tsx uses ModernTable
function OrdersPage() {
  const { flags } = useFeatureFlags();

  return (
    <div>
      {flags.newTable ? <ModernTable /> : <LegacyTable />}
    </div>
  );
}
```

### Real-World Examples

| From | To | Strategy | Pain Points | Timeline |
|---|---|---|---|---|
| **jQuery** | **React** | Strangler — wrap one component at a time | jQuery manipulates DOM outside React's awareness. Need to isolate jQuery-managed subtrees. | 6–18 months |
| **AngularJS** | **React/Vue** | Strangler — ng-upgrade or micro-frontend | Two-way binding vs one-way data flow. Digest cycle timing. | 12–24 months |
| **REST** | **GraphQL** | Gateway pattern — add GraphQL proxy in front of existing REST endpoints | N+1 under GraphQL wasn't visible under REST. BFF (Backend for Frontend) needed. | 3–6 months |
| **Express** | **Fastify** | Per-route migration with shared middleware | Middleware compatibility. Different plugin systems. | 2–4 weeks |
| **Redux** | **Zustand/Valtio** | Package-based strangler — migrate one slice at a time | Both state stores need to be active during transition. Sync layer between them. | 2–8 weeks |

---

## 5. Language Migration

### When It Makes Sense

| Reason | Old | New | Example |
|---|---|---|---|
| Scaling throughput limits | Python (GIL-bound) | Go | API gateway processing 50K req/s |
| Team expertise shift | Ruby (shrinking Ruby talent) | Kotlin/Go | Team attrition or hiring challenge |
| Ecosystem limitations | PHP (declining package ecosystem) | TypeScript/Node | New integrations need modern SDKs |
| Concurrency needs | Ruby/GIL or Node (event loop) | Elixir/Erlang (BEAM) | Real-time features, WebSockets |
| Memory safety | C/C++ | Rust | Security-critical components |
| Type safety | JavaScript | TypeScript | Large team, complex codebase |
| Operational simplicity | Java (heavy JVM) | Go (single binary) | Container images, cold starts |

### Interop Patterns

**Sidecar pattern — run old and new side by side, communicate over gRPC:**

```protobuf
// migration.proto — shared contract between old & new
service OrderProcessor {
  rpc ProcessOrder(ProcessOrderRequest) returns (ProcessOrderResponse);
}

message ProcessOrderRequest {
  string order_id = 1;
  string customer_id = 2;
  repeated LineItem items = 3;
}

message ProcessOrderResponse {
  bool success = 1;
  string order_reference = 2;
  string error_message = 3;
}
```

```yaml
# docker-compose — sidecar interop between old (Python) and new (Go)
services:
  app-python:
    image: app:python-legacy
    ports: ["8000:8000"]
    depends_on: [db]

  app-go:
    image: app:go-new
    ports: ["8001:8001", "50051:50051"]  # HTTP + gRPC
    depends_on: [db]
    environment:
      GRPC_PORT: 50051

  sidecar-router:
    image: envoyproxy/envoy:v1.26
    volumes:
      - ./envoy-sidecar.yaml:/etc/envoy/envoy.yaml
    ports: ["8080:8080"]
    depends_on: [app-python, app-go]
```

**Shared message queue — old and new process events from the same topic:**

```mermaid
sequenceDiagram
    participant Client
    participant Old as Legacy System (Python)
    participant New as New System (Go)
    participant Queue as Message Queue (Kafka/RabbitMQ)
    participant DB as Database

    Client->>Old: Submit order
    Old->>DB: Write order
    Old->>Queue: Emit order.created event
    New->>Queue: Consume order.created event
    New->>New: Process order (new logic)
    New->>DB: Update order status (new schema)
```

### Strangler at Module Boundary

Port one module at a time. Route traffic between old and new at the module boundary.

```go
// router.go — route between old and new per module
package main

type ModuleRouter struct {
    legacy  *LegacyProcessor
    modern  *ModernProcessor
}

func (r *ModuleRouter) ProcessOrder(ctx context.Context, req *OrderRequest) (*OrderResponse, error) {
    // Only the "pricing" module has been ported to Go
    // Everything else still runs on the legacy Python service
    if req.Path == "/pricing/calculate" {
        return r.modern.CalculatePricing(ctx, req)  // Go implementation
    }
    return r.legacy.Forward(ctx, req)  // Proxy to legacy Python
}
```

### Real-World Language Migration Approaches

| Migration | Strategy | Key Challenges | Success Signal |
|---|---|---|---|
| **Python → Go** | Sidecar + strangler at service boundary | Latency diff, error handling patterns, goroutine vs asyncio | Target service handles 2x throughput at 50% latency |
| **Ruby → Elixir** | Shared message queue + strangler per bounded context | Actor model mental shift, GenServer patterns, OTP supervision | WebSocket connections go from 10K to 100K per node |
| **JavaScript → TypeScript** | Gradual — `// @ts-check` → `--allowJs` → rename `.js` to `.ts` | Third-party .d.ts quality, `any` propagation | 0 `any` types in strict mode |
| **Java → Kotlin** | Coexistence — both compile to JVM, interop naturally | Null safety migration, Java interop types, annotation processing | New code 100% Kotlin, old Java slowly replaced |

```typescript
// Phase-by-phase JS → TS migration
// Phase 1: Enable type checking on .js files
// tsconfig.json
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": true,  // JSDoc becomes the type system
    "noEmit": true
  }
}

// Phase 2: Add JSDoc types incrementally
/** @param {number} a @param {number} b @returns {number} */
function add(a, b) { return a + b; }

// Phase 3: Rename .js to .ts one file at a time
// Works because --allowJs lets TS and JS mix
// Phase 4: Enable strict mode once coverage is sufficient
```

---

## 6. Cloud Migration

### The 6 R's Framework

| R | Description | Effort | Benefit | When |
|---|---|---|---|---|
| **Rehost** (Lift-and-shift) | Move as-is to cloud VM/container | Low | Immediate cost savings (no data center), quick wins | Tight deadlines, compliance mandates, low-risk apps |
| **Replatform** (Lift-tinker-shift) | Minor cloud optimizations (RDS instead of self-managed Postgres, S3 instead of NFS) | Low-Medium | Better performance, reduced operations, no full rewrite | Apps that need some cloud benefit without full rewrite |
| **Repurchase** | Move to SaaS (Salesforce, Workday, Stripe) instead of custom | Variable | Offload maintenance, get features for free | Non-core functions (HR, billing, CRM) |
| **Refactor** (Rebuild cloud-native) | Rewrite for cloud-native (microservices, serverless) | High | Best long-term agility, cost optimization, scalability | Core systems with runway, high business value |
| **Retire** | Decommission — nothing to migrate | Zero | Cost savings, reduced attack surface, less to maintain | Any system without users or business justification |
| **Retain** | Keep on-prem or as-is | None | No risk, no cost, no change | Systems with high migration cost vs low benefit, or regulatory restriction |

**Decision tree:**
```
Is the system still used?
├─ No → Retire
└─ Yes → Is the system core to competitive advantage?
    ├─ No → Does it have a SaaS equivalent?
    │   ├─ Yes → Repurchase
    │   └─ No → Rehost or Replatform
    └─ Yes → Does it need cloud-native features (auto-scale, serverless)?
        ├─ Yes → Refactor
        └─ No → Replatform
```

### Well-Architected Migration Assessment

Before any migration, score the current system against the five pillars:

| Pillar | Assessment Questions | Target |
|---|---|---|
| **Security** | Is data encrypted at rest and in transit? IAM least-privilege? Secrets management? | 100% of data encrypted. Access controlled by policy, not by network. |
| **Reliability** | Is there a backup/restore process tested monthly? Multi-AZ? Auto-scaling? | RPO < 1h, RTO < 4h. No single points of failure. |
| **Performance** | Are there latency SLOs? Can you scale vertically/horizontally? Is there a load testing baseline? | P99 latency < 200ms. Auto-scaling rules defined. |
| **Cost** | Current TCO (hardware, licenses, power, people for maintenance)? | Target: 20–40% TCO reduction over 3 years. |
| **Operational excellence** | Deployments automated? Monitoring? Incident response? Runbooks? | Deployments fully automated. PagerDuty contacts current. |

### Migration Planning: Wave Sequencing

```yaml
# migration-waves.yaml
waves:
  - wave: 1
    name: "Foundation"
    systems: [network, vpn, auth, monitoring]
    dependencies: []
    estimated_duration: "2 weeks"

  - wave: 2
    name: "Stateless Tier"
    systems: [web-servers, api-gateway, cdn]
    dependencies: [wave-1]
    estimated_duration: "1 week"

  - wave: 3
    name: "Stateful Tier — Read Replicas"
    systems: [reporting-db-reader-analytics]
    dependencies: [wave-1]
    estimated_duration: "1 week"

  - wave: 4
    name: "Stateful Tier — Primary Database"
    systems: [postgres-primary]
    dependencies: [wave-3]
    estimated_duration: "Weekend cutover + 7-day bake"
    rollback: true

  - wave: 5
    name: "Decommission"
    systems: [old-vpcs, old-nfs-shares, old-monitoring]
    dependencies: [wave-4]
    estimated_duration: "1 week"
    requires_confirmation: true
```

**Parallel vs sequential migrations:**
- **Parallel** (multiple systems at once): faster overall timeline, higher risk, needs separate teams. Only for systems with no dependency chain.
- **Sequential** (one wave at a time): safer, easier to debug, but takes longer. Recommended for all stateful migrations.

### AWS-Specific Tools

| Tool | Use Case | Limitations |
|---|---|---|
| **AWS Application Migration Service (MGN)** | Automated lift-and-shift. Replicates entire server (OS, apps, config) to AWS. Test before cutover. | Doesn't refactor — you get the same OS, same patching burden. Requires agent on source. |
| **AWS Database Migration Service (DMS)** | Database platform migrations. Supports homogeneous (Postgres → Aurora Postgres) and heterogeneous (Oracle → Aurora MySQL). Full load + CDC. | No DDL replication (schema changes must be applied manually). Type mapping needs validation. |
| **AWS VM Import/Export** | Import on-prem VM images to EC2. Good for one-off migrations. | Manual process. No continuous replication. |

### Cost Estimation & TCO Comparison

```python
# tco_comparison.py — rough TCO calculator
def tco_estimate(
    vcpus: int,
    ram_gb: int,
    storage_tb: float,
    monthly_traffic_tb: float,
    years: int = 3
) -> dict:
    on_prem = {
        'hardware': vcpus * 1500 + storage_tb * 1000,            # one-time server cost
        'power_cooling': (vcpus * 12 + ram_gb * 2) * 12 * years, # $/year
        'staff': 15000 * 12 * years,                               # sysadmin fraction
        'licensing': 2000 * years,                                 # OS/DB licenses
    }
    on_prem['total'] = sum(on_prem.values())

    cloud = {
        'compute': vcpus * 25 * 730 * years,                      # EC2/RDS per month
        'storage': storage_tb * 120 * 12 * years,                 # EBS or S3
        'data_transfer': monthly_traffic_tb * 90 * 12 * years,    # egress
        'services': 1000 * 12 * years,                             # monitoring, backup, etc.
    }
    # Reserved instance discount (1-year)
    cloud['compute'] *= 0.6
    cloud['total'] = sum(cloud.values())

    return {
        'on_premise': {k: f"${v:,.0f}" for k, v in on_prem.items()},
        'cloud': {k: f"${v:,.0f}" for k, v in cloud.items()},
        'savings': f"${on_prem['total'] - cloud['total']:,.0f}" if cloud['total'] < on_prem['total'] else f"-${cloud['total'] - on_prem['total']:,.0f} (increase)"
    }

print(tco_estimate(vcpus=8, ram_gb=32, storage_tb=2, monthly_traffic_tb=1))
```

---

## 7. Testing During Migration

### Parallel Run Verification

```python
# parallel_run_comparator.py — diff old vs new at scale
# Run this every N minutes during parallel run phase
import hashlib
import json
import psycopg2
from datetime import datetime

def compute_row_hash(row: tuple) -> str:
    """Compute a stable hash for a row, ignoring columns we don't control."""
    stable = [str(v) if v is not None else 'NULL' for v in row]
    return hashlib.md5('|'.join(stable).encode()).hexdigest()

def compare_old_new(params: dict):
    """Compare a batch of records between old and new systems."""
    old = psycopg2.connect(params['old_dsn'])
    new = psycopg2.connect(params['new_dsn'])

    old_cur = old.cursor()
    new_cur = new.cursor()

    # Get latest checkpoint
    checkpoint = params.get('last_checked_id', 0)
    batch = params.get('batch_size', 1000)

    old_cur.execute("""
        SELECT id, order_total, status, shipping_address, created_at
        FROM orders WHERE id > %s ORDER BY id LIMIT %s
    """, (checkpoint, batch))
    old_rows = old_cur.fetchall()

    if not old_rows:
        old.close()
        new.close()
        return {'status': 'complete', 'checked': 0, 'mismatches': []}

    max_id = old_rows[-1][0]
    new_cur.execute("""
        SELECT id, order_total, status, shipping_address, created_at
        FROM orders WHERE id > %s AND id <= %s ORDER BY id
    """, (checkpoint, max_id))
    new_rows_map = {r[0]: r for r in new_cur.fetchall()}

    mismatches = []
    for old_row in old_rows:
        oid = old_row[0]
        new_row = new_rows_map.get(oid)
        if new_row is None:
            mismatches.append({'id': oid, 'error': 'missing_in_new'})
            continue
        if compute_row_hash(old_row) != compute_row_hash(new_row):
            mismatches.append({'id': oid, 'error': 'value_mismatch'})

    old.close()
    new.close()

    return {
        'status': 'in_progress',
        'last_checked_id': max_id,
        'checked': len(old_rows),
        'mismatches': mismatches
    }
```

### Canary Comparison

```yaml
# canary-deployment.yaml — Kubernetes canary for migration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-new
spec:
  replicas: 1  # Start with 1 canary pod
  selector:
    matchLabels:
      app: app
      version: new
  template:
    metadata:
      labels:
        app: app
        version: new
    spec:
      containers:
        - name: app
          image: myapp:new-version
          env:
            - name: DATABASE_URL
              value: postgres://user:pass@new-db.internal:5432/app
          readinessProbe:
            httpGet:
              path: /health
              port: 8080

---
# Service splits 5% traffic to canary
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: app
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "5"
  name: app-canary
spec:
  rules:
    - http:
        paths:
          - backend:
              service:
                name: app
                port:
                  number: 8080
            path: /
            pathType: Prefix
```

### Data Integrity Checks — Automated Reconciliation

```sql
-- reconciliation_report.sql — run daily post-migration
SELECT
    'row_count_check' AS check_name,
    CASE WHEN (SELECT COUNT(*) FROM old_db.orders) = (SELECT COUNT(*) FROM new_db.orders)
         THEN 'PASS' ELSE 'FAIL' END AS result,
    (SELECT COUNT(*) FROM old_db.orders) AS old_count,
    (SELECT COUNT(*) FROM new_db.orders) AS new_count
UNION ALL
SELECT
    'checksum_check' AS check_name,
    CASE WHEN (SELECT MD5(array_agg(id || order_total || status)::text) FROM old_db.orders ORDER BY id)
           = (SELECT MD5(array_agg(id || order_total || status)::text) FROM new_db.orders ORDER BY id)
         THEN 'PASS' ELSE 'FAIL' END AS result,
    0, 0
UNION ALL
SELECT
    'orphan_check' AS check_name,
    CASE WHEN (SELECT COUNT(*) FROM old_db.orders o LEFT JOIN new_db.orders n ON o.id = n.id WHERE n.id IS NULL) = 0
         THEN 'PASS' ELSE 'FAIL' END AS result,
    (SELECT COUNT(*) FROM old_db.orders o LEFT JOIN new_db.orders n ON o.id = n.id WHERE n.id IS NULL) AS old_only,
    (SELECT COUNT(*) FROM new_db.orders n LEFT JOIN old_db.orders o ON n.id = o.id WHERE o.id IS NULL) AS new_only;
```

### Performance Regression Testing

```python
# load_test_compare.py — compare old vs new with locust
# Run this before cutover to validate performance parity or improvement
"""
locust command:
  locust -f load_test_compare.py --host=http://old-system.internal --headless -u 100 -r 10 --run-time 5m --csv old_results
  locust -f load_test_compare.py --host=http://new-system.internal --headless -u 100 -r 10 --run-time 5m --csv new_results
"""

from locust import HttpUser, task, between

class MigrationComparisonUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def get_orders(self):
        self.client.get("/api/v1/orders")

    @task(2)
    def get_order_detail(self):
        self.client.get(f"/api/v1/orders/{self._random_order_id()}")

    @task(1)
    def create_order(self):
        self.client.post("/api/v1/orders", json={
            "user_id": 42,
            "items": [{"product_id": 1, "quantity": 2}]
        })

    def _random_order_id(self):
        import random
        return random.randint(1, 10000)
```

```bash
# Compare results
echo "=== OLD SYSTEM ==="
awk -F',' 'NR>1 && $1=="Aggregated" {print "P50:", $8, "P95:", $9, "P99:", $10, "Error%:", $14}' old_results_stats.csv

echo "=== NEW SYSTEM ==="
awk -F',' 'NR>1 && $1=="Aggregated" {print "P50:", $8, "P95:", $9, "P99:", $10, "Error%:", $14}' new_results_stats.csv
```

**Pass criteria:** New system's P99 latency ≤ Old system's P99 latency × 1.1. Error rate < 0.1%. Zero 5xx errors.

---

## 8. Rollback Strategy (Military-Grade)

### Core Principle

```
Every migration phase must have a tested rollback.
If you can't roll back a phase, you can't move forward.
```

### Per-Phase Rollback Plans

| Phase | Rollback Action | Duration | Data Risk | Tested? |
|---|---|---|---|---|
| **Expand** (add columns) | `ALTER TABLE DROP COLUMN new_col` | 1–5 min | None (old data untouched) | ✓ |
| **Backfill** (populate new columns) | Run reverse backfill (new → old) OR leave new columns populated (acceptable waste) | 10–60 min | Low (old data still authoritative) | ✓ |
| **Dual-write start** | Deploy app code that writes only to old schema | 2 min (feature flag flip) | None if old write always worked | ✓ |
| **Switch reads to new** | Feature flag: read from old source | Instant (FF flip) | Medium — if dual-write was off, new may have stale data | ✓ |
| **Contract** (drop old columns) | Restore from backup + replay write-ahead log | 1–4 hours | High — potential data loss since backup | ✓ (restore drill) |
| **Dual-write stop** | Deploy app code that writes only to new | 2 min | Low — old columns are still populated, but may have missed writes | ✓ |
| **Decommission old system** | Clone new-to-old if backup exists | 4–24 hours | Very high — last-mile risk. Only do after extended bake. | N/A (no rollback — irreversible) |

### Feature Flags for Quick Disable

```typescript
// feature-flags.ts — migration-specific feature flags
interface MigrationFlags {
  ordersUseNewDb: boolean;       // if false, reads/writes go to old DB
  ordersDualWrite: boolean;      // if true, writes go to both
  ordersReadFromNew: boolean;    // if true, reads come from new DB
}

// Environment variable source (lowest ceremony, works without infra)
const flags: MigrationFlags = {
  ordersUseNewDb: process.env.FF_ORDERS_USE_NEW_DB === 'true',
  ordersDualWrite: process.env.FF_ORDERS_DUAL_WRITE === 'true',
  ordersReadFromNew: process.env.FF_ORDERS_READ_FROM_NEW === 'true',
};

// In Kubernetes:
// kubectl set env deployment/app FF_ORDERS_READ_FROM_NEW=false
```

```yaml
# For LaunchDarkly users:
# launchdarkly-migration-flag.yaml
flags:
  - key: orders-db-migration
    variations:
      - legacy
      - dual-write
      - new-read
      - new-only
    targeting:
      - variation: legacy
        rules: [{ clause: { contextKind: "user", attribute: "email", op: "endsWith", values: [ "@test.com" ] } }]
    default: legacy
```

### Data Sync Reversal

If you're writing to a new DB and need to roll back — how do you get data from the new DB back to the old one?

```python
# sync_reverse.py — sync data from new DB back to old DB during rollback
import psycopg2

OLD_DSN = "postgres://user:pass@old-db:5432/prod"
NEW_DSN = "postgres://user:pass@new-db:5432/prod"

def reverse_sync_orders():
    old = psycopg2.connect(OLD_DSN)
    new = psycopg2.connect(NEW_DSN)
    old_cur = old.cursor()
    new_cur = new.cursor()

    # Get all IDs in new that were created/updated during migration window
    new_cur.execute("""
        SELECT id, total, status, shipping_address, updated_at
        FROM orders
        WHERE updated_at > '2026-07-20 00:00:00+00'
        ORDER BY id
    """)

    count = 0
    for row in new_cur:
        old_cur.execute("""
            UPDATE orders
            SET total = %s, status = %s, shipping_address = %s, updated_at = %s
            WHERE id = %s
        """, (row[1], row[2], row[3], row[4], row[0]))
        count += 1

        if count % 500 == 0:
            old.commit()
            print(f"Reversed {count} orders")

    old.commit()
    print(f"Reverse sync complete: {count} orders synced back to old DB")
    old.close()
    new.close()
```

### Bake Period

| Migration Type | Minimum Bake | What to Monitor |
|---|---|---|
| Schema change (add column) | 24 hours | Error rates, data integrity, reads returning null |
| Data type change | 48 hours | Data truncation, rounding errors, null propagation |
| DB platform migration (PG → Aurora) | 7 days | Replication lag, performance, connection handling |
| Framework/library swap | 2 weeks | Feature parity, edge cases, performance under all load patterns |
| Language rewrite | 4 weeks | Correctness, memory usage, latency, error handling |
| Cloud migration (full platform) | 4 weeks | Cost, performance, availability, incident response |
| Financial system migration | 30+ days | Every reconciliation check must pass for N consecutive days |

### Rollback Decision Triggers

```python
# rollback_monitor.py — decide whether to rollback automatically
def should_rollback(metrics: dict, thresholds: dict) -> tuple[bool, list[str]]:
    """
    triggers is a dict of metric_name -> (current_value, threshold_value, comparator_fn)
    """
    triggers = []
    for name, config in thresholds.items():
        current = metrics.get(name)
        if current is None:
            continue
        threshold_value = config['threshold']
        comparator = config.get('comparator', 'gt')

        if (comparator == 'gt' and current > threshold_value) or \
           (comparator == 'lt' and current < threshold_value) or \
           (comparator == 'gte' and current >= threshold_value) or \
           (comparator == 'lte' and current <= threshold_value):
            triggers.append(f"{name}: {current} {comparator} {threshold_value}")

    return (len(triggers) > 0, triggers)


# Rollback thresholds for a typical DB migration
ROLLBACK_THRESHOLDS = {
    'error_rate_pct':        {'threshold': 0.5,   'comparator': 'gt'},     # > 0.5% error rate
    'p99_latency_ms':        {'threshold': 1000,  'comparator': 'gt'},     # > 1s P99
    'replication_lag_sec':   {'threshold': 60,    'comparator': 'gt'},     # > 60s lag
    'db_connections':        {'threshold': 200,   'comparator': 'gt'},     # > 200 connections
    'data_integrity_fail':   {'threshold': 0,     'comparator': 'gt'},     # any integrity failures
}
```

---

## 9. Stakeholder Management

### Migration Timeline Communication

```
Subject: Migration Window — Orders Service to New Database — July 27–28

Hi team,

We are migrating the Orders service to the new PostgreSQL cluster this weekend.

PHASE 1 — Friday 8 PM: Expand schema (add new columns). 5 min. No downtime.
PHASE 2 — Saturday 2 AM: Backfill historical data. ~2 hours. Read-only perf impact ~5%.
PHASE 3 — Saturday 10 AM: Switch reads to new. Feature-flagged. Instant rollback. No expected impact.
PHASE 4 — Sunday 12 PM: Switch writes to new. Feature-flagged. Instant rollback.
PHASE 5 — Sunday 6 PM: Remove old schema. 5 min. Will be retained for 7-day rollback.

Go/No-Go: Friday 3 PM — I'll confirm Phase 1 readiness.

Rollback: At any phase, flip a feature flag. Max 30 seconds to full rollback.

Monitoring: #migration-orders channel. Dashboard: [link]

Post-migration bake: 7 days before we decommission old DB.

Questions? Reply in thread.
```

### Business Continuity Assurance — Template

```
MIGRATION CONTINUITY ASSURANCE

1. Customer Impact: ZERO. All phases use expand-contract or blue-green patterns.
   No maintenance windows. No read-only mode.

2. Rollback: Every phase has a tested rollback under 30 seconds.
   Rollback tested in staging on [DATE] — results: PASS.

3. Data Safety: Pre-migration backup verified as restorable.
   Dual-write from Phase 2 ensures both old and new have consistent data.

4. Timeline: Migration spans [DATES]. Each phase is 5 min to 2 hours.
   Full rollback available at any point.

5. Testing: Full dry run on production-scale snapshot on [DATE].
   Load test results: [link]. Reconciliation results: [link].

6. Communication: Updates every 30 min during migration in #migration channel.
   Final confirmation email after successful bake period.

Signed: [ARCHITECT NAME], Migration Lead
```

### Success Metrics

| Metric | Target | Measurement |
|---|---|---|
| Latency (P50, P95, P99) | ≤ old system | Datadog/Grafana percentiles |
| Error rate (4xx + 5xx) | < 0.1% | API monitoring |
| Data integrity | 100% consistent | Reconciliation checks |
| Cost (if cloud migration) | ≤ pre-migration TCO | Cloud cost explorer |
| Developer satisfaction | > 7/10 (survey) | Post-migration retro survey |
| Rollback time | < 30 seconds | Timestamp flag flip → traffic restored |
| Bake period incidents | 0 critical, < 3 minor | Incident tracker |

### Communication Cadence

| Phase | Frequency | Audience | Format |
|---|---|---|---|
| Assessment | Weekly | Engineering team | Slack update |
| Preparation | Weekly | Engineering + PM | Brief standup |
| Pre-cutoff | Daily (last 3 days) | Full team + stakeholders | Standup + email |
| During migration | Every 30 min | Full team + on-call | Slack #migration channel |
| During cutover window | Every 5 min | Migration lead + SRE | Direct call/chat |
| Post-migration (bake) | Daily | Engineering team | Slack update |
| Post-migration (retro) | Once | Full team + stakeholders | Meeting + document |

---

## Cross-Skill Coordination

Migration architecture is inherently cross-functional — it spans databases, application code, infrastructure, and QA. A migration without coordination is a production incident waiting to happen.

| Coordinate With | When | What to Share/Ask |
|-----------------|------|-------------------|
| **Backend Developers** | Schema changes, data access layer changes, API versioning | Migration sequence, dual-write requirements, backward compatibility rules |
| **DBA / Database Team** | Schema migration, index changes, query performance | DDL review, lock duration estimates, replication lag impact, rollback plan |
| **DevOps / Infrastructure** | Deployment orchestration, environment management, backup/restore | Migration deployment order, blue-green coordination, backup verification |
| **System Architect** | Architecture changes, service boundaries, data ownership | Data ownership shifts, service decomposition impact, eventual consistency model |
| **QA Engineer** | Migration testing, data integrity verification, regression testing | Test environments, data comparison scripts, rollback test scenarios |
| **Security Reviewer** | Data migration security, sensitive data handling, encryption | Data at rest/in transit during migration, access control for migration tools |
| **Project Manager** | Migration timeline, stakeholder communication, resource coordination | Migration milestones, risk register, rollback decision authority |
| **Performance Engineer** | Migration impact on production performance, load during backfill | Backfill throttling, read/write load analysis, connection pool impact |
| **CTO Advisor** | Build vs buy migration tooling, architecture decisions | Tooling investment, migration strategy approval, risk acceptance |
| **Product Strategist** | User-facing migration impact, downtime communication, feature flags | User impact assessment, maintenance window communication, feature flag coordination |

### Communication Triggers — When to Proactively Notify

| Trigger | Notify | Why |
|---------|--------|-----|
| Migration script ready for production execution | Project Manager, DevOps, Backend Developers, DBA | Execution window scheduling; all stakeholders on standby |
| Data integrity check fails (row count mismatch, checksum mismatch) | DBA, Backend Developers, QA | Stop migration; root cause analysis; potentially pause backfill |
| Migration causes production latency increase >20% | Performance Engineer, DevOps, Project Manager | Throttle or pause; production impact unacceptable |
| Rollback plan activated for any reason | Project Manager, All Coordinated Teams | Incident declared; all teams execute rollback checklist |
| Schema change requires application downtime (cannot be done online) | Product Strategist, Project Manager, DevOps | Schedule maintenance window; user communication required |
| Backfill estimated completion shifts by >50% | Project Manager, Backend Developers | Replan cutover date; stakeholder expectation reset |
| Cross-team dependency for migration not met (e.g., API not ready, service not deployed) | Project Manager, Affected Team Lead | Blocking dependency; escalation for prioritization |
| Migration complete — verification passing, dual-write retired | All Coordinated Teams, Product Strategist, CTO Advisor | Migration closure; celebration; post-migration monitoring period begins |

### Escalation Path

| Situation | Escalate To | Rationale |
|-----------|------------|-----------|
| Data corruption detected post-migration (>10 rows or any customer-impacting) | **CTO Advisor** + VP Engineering + Incident Commander | Production incident; may require restore from backup |
| Migration blocked by external vendor/API limitation indefinitely | **CTO Advisor** + Product Strategist + Project Manager | Strategy pivot; may require architectural workaround or vendor change |
| Rollback fails during attempted execution | **CTO Advisor** + DevOps Lead + DBA | Critical incident; restore from backup may be only option |
| Migration cost/time exceeds original estimate by >100% | **CTO Advisor** + Project Manager + Stakeholders | Re-baseline; build vs buy vs maintain re-evaluation |
| Compliance/regulatory issue discovered in migrated data | **Legal Advisor** + Security Reviewer + Regulatory Specialist | Regulatory exposure; may require data remediation or disclosure |

## 10. Production Checklist

- [ ] **Inventory complete:** all databases, services, cron jobs, consumers, and dependencies documented with row counts, throughput estimates, and coupling scores
- [ ] **Migration pattern selected** with documented rationale and scored using the decision matrix (expand-contract, strangler, parallel run, blue-green, rehost, refactor)
- [ ] **Complexity scored** using the 1–5 scoring system; high-score migrations have staged rollout plans
- [ ] **Hidden dependencies found:** shared databases, hardcoded endpoints, shared sequences; mitigation plan documented
- [ ] **Dependency graph built** (upstream + downstream) and shared with all affected teams; each consumer has been individually contacted and confirmed awareness
- [ ] **Build vs buy decision** made and documented; managed services (DMS, MGN, gh-ost, pgroll) evaluated where appropriate
- [ ] **Schema changes are backward-compatible** at every intermediate phase; no breaking changes without expand-contract
- [ ] **Migration framework selected** (Flyway, Alembic, Prisma, golang-migrate, atlas, goose) with versioned, checksummed, reviewable migrations
- [ ] **Up and Down scripts** exist for every schema change; Down scripts tested in staging
- [ ] **CI pipeline validates:** migrations apply cleanly on a fresh database, no drift from production schema, Down scripts tested, data-loss operations require explicit confirmation
- [ ] **Data migration scripts** use batch processing with checkpoint-based resumability, idempotency guarantees, and configurable throttling (sleep between batches)
- [ ] **CDC replication tested** (if using Debezium/Kafka for streaming): binlog replication slot created, consumer lag monitored, JSON deserialization verified
- [ ] **Dual-write consistency verification** script written and tested; periodic sampling compares old vs new row-by-row
- [ ] **Reconciliation queries** written: row count comparison, full-table checksum, per-row sampling with hashed comparison, orphan detection
- [ ] **Performance tested** on a production-scale snapshot: duration, database load, replication lag impact, query plan comparison, lock contention analysis
- [ ] **Load test executed** on both old and new systems; P50/P95/P99 latencies compared; error rates confirmed below threshold
- [ ] **Rollback plan documented per phase** with exact commands/scripts, estimated duration, data risk, and verification steps
- [ ] **Rollback tested in staging** — full up-and-down cycle verified for every phase
- [ ] **Feature flags implemented** for dual-write/dual-read toggling with instant rollback capability (≤ 30 seconds per flag flip)
- [ ] **Rollback decision triggers defined** with numeric thresholds (error rate > 0.5%, P99 latency > 1s, replication lag > 60s)
- [ ] **Reverse sync script written** (for rolling back data from new → old during dual-write phase)
- [ ] **Pre-migration backup completed** and verified as restorable (tested on a separate environment)
- [ ] **Monitoring dashboards configured:** replication lag, lock contention, error rates, migration progress, latency percentiles (P50/P95/P99), connection count
- [ ] **Alarms configured:** replication lag > threshold, error rate spike, migration checkpoint stall > 10 min
- [ ] **Bake period defined** (minimum 24 hours for simple schema changes, 7 days for platform migrations, 30 days for financial systems)
- [ ] **Communication plan executed:** stakeholders, support team, on-call informed of migration window and phases
- [ ] **Go/no-go decision process defined** — who decides, based on what metrics, at what checkpoints
- [ ] **Post-migration cleanup** planned: old schema removal, feature flag removal, dual-write code removal, old system decommission
- [ ] **Postmortem scheduled** and template prepared: what went well, what went wrong, what to improve

---

## MVP vs Growth vs Scale

| Phase | Team Size | Priority | Migration Approach |
|-------|-----------|----------|-------------------|
| **MVP (0→1)** | 1-3 devs | Ship with whatever DB works | Single database. No migration tooling beyond raw SQL or ORM auto-migrate. `CREATE TABLE` in dev, export DDL for prod. If you need to change schema: dump → modify → restore (acceptable with 0 users). |
| **Growth (1→10)** | 3-15 devs, 1 backend specialist | Predictable, reversible schema changes | Versioned migrations (Flyway/Alembic/Prisma). Expand-contract for schema changes. CI validates migrations. Data migrations: batch scripts, resumable, throttled. Tested on staging with prod-scale data. |
| **Scale (10→N)** | 15+ devs, dedicated DB/infra team | Zero-downtime everything | Online schema change tools (gh-ost, pgroll). Blue-green database deployments. Automated migration testing in CI (apply up + test + roll back + test). Data migration pipelines with monitoring and auto-pause. |

**MVP migration rule:** `ALTER TABLE ADD COLUMN` is fine with 100 rows. Don't build a zero-downtime migration framework for a 10MB database. You don't have users to disrupt. Upgrade when: (a) you have paying users, (b) migrations take >30 seconds, (c) a failed migration would be a customer-visible incident.

## Cost-Effective Decision Table

| Decision | Free/Cheap Option | Paid Upgrade | When to Upgrade |
|----------|------------------|--------------|-----------------|
| Migration framework | ORM built-in (ActiveRecord, Prisma, SQLAlchemy auto-migrate) | Flyway Teams ($3K/yr) or Liquibase Pro | Need dry-run validation, undo scripts, or enterprise DB support (Oracle, DB2) |
| Online schema changes | PostgreSQL: `CREATE INDEX CONCURRENTLY` (built-in). MySQL: `gh-ost` (free OSS) | — | Free OSS tools cover 95% of needs |
| Data migration (backfill) | Custom Python/Node script with batching + checkpointing (1-2 days to write) | Data pipeline tool (Airbyte, Fivetran) | Backfill spans 10+ tables with complex transformations or needs scheduling |
| Schema drift detection | `pg_dump --schema-only` diff or manual comparison | Skeema ($250/mo) or Atlas ($295/mo) | >50 tables or multiple environments that drift frequently |
| Migration testing | CI job: apply migration to prod clone, verify | Database Lab Engine (Postgres, OSS) or Snaplet | Need instant (<1s) database clones for fast CI feedback |
| Rollback planning | Manual: write down script per phase | Atlas (declarative schema, auto-generates rollback) | >20 migrations/month or team >5 people |

**Annual migration tool budget by phase:** MVP: $0 (ORM built-in). Growth: $0-1K (OSS tools). Scale: $0-10K (OSS tools + CI infra).

## Scalability Decision Tree

```
Are your migrations taking >30 seconds to apply in production?
├── YES → Evaluate: is it a schema change (ALTER on large table) or data backfill?
│   ├── Schema change → Use online schema change: gh-ost (MySQL) or CREATE INDEX CONCURRENTLY (PG).
│   └── Data backfill → Batch it. Process in chunks of 1K-10K rows with sleep between.
└── NO → Migration time is acceptable. No tooling change needed.

Do you have paying users who would notice >1 second of downtime?
├── YES → Every schema change must be backward-compatible at each phase. Use expand-contract.
└── NO → Acceptable to have brief maintenance windows. Simple migrations are fine.

Do you need to roll back a migration more than once per quarter?
├── YES → Invest in automated rollback testing. Run up → test → down → test in CI.
└── NO → Manual rollback plan per migration is sufficient. Document it.

Is your database >100GB?
├── YES → All schema changes need online tools. Plan for hours, not minutes.
│   Test on a production-scale clone before executing against production.
└── NO → Standard migrations are fine. Clone entire DB for testing is fast.

Are you migrating database platforms (MySQL → PostgreSQL, on-prem → cloud)?
├── YES → This is a major project. Blue-green migration. 2-6 month timeline. Dedicated plan.
└── NO → Schema/data evolution within the same platform. Iterative approach.
```

## When NOT to Use This Skill (Overkill)

- **Pre-launch with 0 users**: You can dump, modify, and restore your database in minutes. Zero-downtime migration patterns are solving a problem you don't have.
- **Database is <1GB and migrations take <5 seconds**: `ALTER TABLE` during a maintenance window is fine. Don't build an online schema change pipeline.
- **Solo developer**: Expand-contract requires dual-write code paths, feature flags, and multi-phase deploys. That's operational overhead for a team of 1. Simple migrations work.
- **Read-only or append-only database**: If you never alter existing tables (only create new ones and append data), migration patterns for schema changes aren't needed.
- **Prototype/throwaway project**: Don't version migrations for a project you'll delete in 2 weeks. Raw SQL is fine.

## Token-Efficient Workflow

```
# Step 1: Migration readiness check
python3 scripts/migration_check.py --db-url $DATABASE_URL --output json
# Returns: {"size_gb": 2.5, "table_count": 42, "largest_table_rows": 1500000,
#           "has_replicas": true, "replication_lag_ms": 50, "active_connections": 80}

# Step 2: Decision tree → choose migration pattern
# largest_table_rows > 1M → Online schema change (gh-ost/pgroll). Don't ALTER directly.
# size_gb > 50 → Test on prod-scale clone first. Expect migration to take hours.
# has_replicas + lag > 1000ms → Throttle migration to reduce lag. Monitor closely.

# Step 3: Validation with exit codes
# Verify migration applies cleanly
npm run migrate:up -- --dry-run  # Exit code 0 = clean apply

# Verify migration rolls back
npm run migrate:down -- --dry-run  # Exit code 0 = clean rollback

# Verify no schema drift
python3 scripts/check_schema_drift.py --source migrations/ --target $DATABASE_URL
# Exit code 0 = no drift, 1 = drift detected

# Step 4: During migration — monitor replication lag
python3 scripts/monitor_replication.py --threshold-ms 2000 --output json
# Exit code 0 = lag below threshold, 1 = threshold exceeded (pause migration)
```

**Principle:** `migration_check.py` analyzes database metadata, outputs JSON. Agent applies decision tree to select pattern. Validation uses exit codes (dry-run, drift check). Monitoring script checks replication lag programmatically during execution.

## References

### Patterns & Theory
- [Parallel Change / Expand-Contract (Martin Fowler)](https://martinfowler.com/bliki/ParallelChange.html)
- [Blue-Green Deployment (Martin Fowler)](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [Strangler Fig Pattern (Martin Fowler)](https://martinfowler.com/bliki/StranglerFigApplication.html)
- [The 6 R's of Cloud Migration (Gartner/AWS)](https://aws.amazon.com/blogs/enterprise-strategy/6-strategies-for-migrating-applications-to-the-cloud/)

### Database Migration Tools
- [gh-ost — GitHub's Online Schema Migration for MySQL](https://github.com/github/gh-ost)
- [pt-online-schema-change — Percona Toolkit](https://docs.percona.com/percona-toolkit/pt-online-schema-change.html)
- [pgroll — Zero-Downtime Schema Changes for PostgreSQL](https://github.com/xataio/pgroll)
- [pg_repack — Online Table Rebuild for PostgreSQL](https://github.com/reorg/pg_repack)
- [Flyway — Database Migrations](https://flywaydb.org/)
- [Liquibase — Database Schema Change Management](https://www.liquibase.com/)
- [Alembic — Database Migration Tool for SQLAlchemy](https://alembic.sqlalchemy.org/)
- [Prisma Migrate — Declarative Database Migrations](https://www.prisma.io/docs/orm/prisma-migrate)
- [golang-migrate — Database Migrations in Go](https://github.com/golang-migrate/migrate)
- [atlas — Declarative Schema Management](https://atlasgo.io/)
- [goose — Database Migrations in Go](https://github.com/pressly/goose)

### Cloud Migration
- [AWS Application Migration Service (MGN)](https://aws.amazon.com/application-migration-service/)
- [AWS Database Migration Service (DMS)](https://aws.amazon.com/dms/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS VM Import/Export](https://aws.amazon.com/ec2/vm-import/)
- [Google Cloud Migration Services](https://cloud.google.com/migration)
- [Azure Migrate](https://azure.microsoft.com/en-us/products/azure-migrate/)

### Data Streaming & CDC
- [Debezium — Change Data Capture Platform](https://debezium.io/)
- [Apache Kafka — Event Streaming Platform](https://kafka.apache.org/)
- [Kafka Connect — Scalable Streaming Integrations](https://kafka.apache.org/documentation/#connect)

### Feature Flags & Rollback
- [LaunchDarkly — Feature Management](https://launchdarkly.com/)
- [Feature Flags (Martin Fowler)](https://martinfowler.com/articles/feature-toggles.html)

### Testing & Verification
- [Locust — Load Testing Framework](https://locust.io/)
- [k6 — Modern Load Testing](https://k6.io/)
- [Apache JMeter — Performance Testing](https://jmeter.apache.org/)
