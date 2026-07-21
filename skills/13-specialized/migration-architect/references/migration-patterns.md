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
