# MVP Migration Patterns for 1-3 Dev Teams

> **Audience:** Small teams (1-3 devs) needing to migrate databases, schemas, or platforms without a dedicated migration team, DBA, or SRE.  
> **Principle:** Every migration pattern here assumes you're on-call for the app AND the migration. Keep it simple enough to debug at 2 AM.

---

## The Strangler Fig for Startups

The Strangler Fig pattern (Martin Fowler) is the safest way to migrate anything with a small team. You don't "cut over" — you gradually replace.

```
Phase 1: NEW alongside OLD  (everyone uses OLD. NEW is built, idle.)
Phase 2: DUAL WRITE         (write to both. Read from OLD.)
Phase 3: BACKFILL           (copy historical data from OLD → NEW.)
Phase 4: DUAL READ + VERIFY (read from both, compare. Route 1% to NEW.)
Phase 5: SWITCH READ        (read from NEW. OLD is fallback.)
Phase 6: RETIRE OLD         (delete OLD. Keep backup for 30 days.)
```

**Key property:** You can STOP at any phase and the system works. You can ROLL BACK from any phase by going to the previous phase. This is critical for small teams — you can't afford a migration that requires 8 hours of recovery.

---

## Pattern A: Schema Change with 0 Downtime (1-2 day effort)

**Example:** Rename `users.email` to `users.primary_email`. Live app. Paying users.

```
Phase 1: EXPAND (30 min)
  ALTER TABLE users ADD COLUMN primary_email VARCHAR(255);
  -- Application: write to BOTH email and primary_email
  -- Application: read from email (primary_email is not trusted yet)

Phase 2: BACKFILL (1-4 hours, run in background)
  -- Batch script: UPDATE users SET primary_email = email WHERE primary_email IS NULL LIMIT 1000;
  -- Run until all rows have primary_email populated
  -- Resumable: re-running same batch is idempotent

Phase 3: VERIFY (15 min)
  SELECT COUNT(*) FROM users WHERE primary_email IS NULL;  -- Should be 0
  -- Spot-check 100 random rows: email == primary_email

Phase 4: SWITCH READ (deploy app change)
  -- Application: read from primary_email
  -- Keep writing to BOTH

Phase 5: RETIRE OLD (wait 1-2 weeks, then deploy)
  -- Application: stop writing to email
  ALTER TABLE users DROP COLUMN email;
```

**Tooling needed:** A batch update script (30 lines of Python/Node) + your existing deploy pipeline.  
**Rollback:** At any phase, revert the app code to the previous phase. The column still exists.

---

## Pattern B: Database Platform Migration (2-6 weeks effort)

**Example:** MySQL → PostgreSQL. 50GB database. Live app.

```
Week 1: SETUP
  - Provision new PostgreSQL instance (same region as app servers)
  - Set up pgloader or custom ETL script
  - Create schema in PostgreSQL (mapped from MySQL types)
  - Test: import a snapshot, verify row counts, spot-check data

Week 2: DUAL WRITE
  - Application: write to BOTH MySQL and PostgreSQL on every mutation
  - Queue-based: app → SQS/Kafka → worker writes to PG
  - OR inline: try PG write, catch error, log (don't block the request)
  - Monitor: PG write failures, latency added by dual-write

Week 3: BACKFILL
  - Run batch migration: SELECT * FROM mysql LIMIT 10000 OFFSET N → INSERT INTO pg
  - Process in chunks of 5K-10K rows
  - Track progress: last_processed_id in a checkpoint table
  - Run during low-traffic hours if it adds load
  - Verify: row counts match, spot-check 1000 rows for data integrity

Week 4: VERIFY + SHADOW READ
  - Read from PG alongside MySQL for 1% of requests
  - Compare responses. Log differences.
  - Fix discrepancies. Re-backfill affected rows.
  - Gradually increase to 10% → 50% → 100% shadow reads
  - Once 100% shadow reads match for 48 hours → proceed

Week 5: SWITCHOVER
  - Deploy: primary reads from PG, keep dual-write to MySQL
  - Monitor error rates, latency, data consistency
  - Keep MySQL as fallback (can revert in minutes by deploy rollback)

Week 6: RETIRE MYSQL
  - After 2 weeks of PG-only with no incidents
  - Stop dual-write. Remove MySQL connection config.
  - Keep MySQL instance (stopped) for 30 days as emergency fallback
  - Then terminate
```

**Tooling needed:** pgloader (free) or custom Python ETL (200-300 lines), checkpoint table, verification queries.  
**Cost:** New PG instance ($15-50/mo during migration) + engineering time (2-6 weeks part-time).

---

## Pattern C: Safe Data Backfill (1-3 day effort)

**Example:** Add `organization_id` to every `project` row based on the project's owner. 5M rows.

```python
# backfill_org_id.py — the standard MVP backfill pattern
import time
import os

BATCH_SIZE = 1000
SLEEP_MS = 100  # throttle to avoid DB overload
CHECKPOINT_FILE = '/tmp/backfill_checkpoint.txt'

def get_last_id():
    if os.path.exists(CHECKPOINT_FILE):
        return int(open(CHECKPOINT_FILE).read().strip())
    return 0

def save_checkpoint(last_id):
    with open(CHECKPOINT_FILE, 'w') as f:
        f.write(str(last_id))

def process_batch(db, start_id):
    """Idempotent batch: UPDATE projects SET org_id = (
        SELECT u.org_id FROM users u WHERE u.id = projects.owner_id
    ) WHERE id > %s AND id <= %s AND org_id IS NULL"""
    end_id = start_id + BATCH_SIZE
    db.execute("""
        UPDATE projects 
        SET org_id = (SELECT u.org_id FROM users u WHERE u.id = projects.owner_id)
        WHERE id > %s AND id <= %s AND org_id IS NULL
    """, (start_id, end_id))
    return end_id

def main():
    db = connect(os.environ['DATABASE_URL'])
    last_id = get_last_id()
    
    while True:
        last_id = process_batch(db, last_id)
        save_checkpoint(last_id)
        
        # Exit condition: no more rows to process
        remaining = db.query("SELECT COUNT(*) FROM projects WHERE org_id IS NULL")
        if remaining == 0:
            break
        
        time.sleep(SLEEP_MS / 1000)
    
    print("Backfill complete.")

if __name__ == '__main__':
    main()
```

**Key properties of this script:**
- **Resumable:** Checkpoint file → kill the script, re-run, continues from where it left off.
- **Idempotent:** `WHERE org_id IS NULL` → running the same batch twice does nothing.
- **Throttled:** `SLEEP_MS` → doesn't overwhelm the database.
- **Verifiable:** `SELECT COUNT(*) WHERE org_id IS NULL` → proves completion.

---

## Cost Comparison: Rewrite vs. Migrate vs. Maintain

| Approach | Initial Cost | Ongoing Cost | Risk | When to Choose |
|----------|-------------|-------------|------|---------------|
| **Maintain (do nothing)** | $0 | Tech debt compounds 15-30%/year | Medium (staying on outdated platform) | System works, no scaling issues, team knows it well |
| **Migrate (strangler fig)** | 2-6 weeks part-time (1 dev) | Lower post-migration | Low (phased, always reversible) | Same functionality, different platform/schema. Evolutionary. |
| **Rewrite** | 3-12 months (1-3 devs) | Lowest long-term | HIGH (parallel systems, feature parity) | Platform is fundamentally wrong, OR you're changing architecture (monolith → services), OR migrating would cost >50% of rewrite |
| **Buy/build new + sunset old** | 2-6 months | New license + lower ops | Medium | Off-the-shelf alternative exists, custom code is undifferentiated |

### Rule of Thumb for Small Teams

| Scenario | Recommendation |
|----------|---------------|
| Same functionality, different database/platform | **Migrate.** Strangler fig. 2-6 weeks. |
| Changing schema significantly (10+ tables restructured) | **Migrate** with expand-contract. Don't rewrite. |
| Changing architecture (monolith → 3 services) | **Extract 1 service first.** See if it helps. Don't plan all 3 at once. |
| Database is the wrong paradigm (SQL → document/ graph) | **Start with 1 bounded context.** See if the new DB solves the problem. |
| Codebase is unmaintainable spaghetti | **Rewrite is tempting but usually wrong.** Strangler-fig the worst modules one at a time. |
| You're the only developer and codebase is <5K lines | **Rewrite might be faster than migrating.** 5K lines is a month of work. Migrating might take the same time with more complexity. |

---

## Migration Readiness Checklist for Small Teams

```
Before ANY migration, verify:

[ ] Backup exists AND you've tested restoring it in the last 30 days
[ ] You know how to roll back the migration (and have tested it)
[ ] Migration script is resumable (can stop and restart without damage)
[ ] Migration script is idempotent (running the same batch twice = same result)
[ ] You have monitoring for: DB CPU, replication lag, app error rate, app latency
[ ] You've run the migration on a production-scale clone (same # rows, similar hardware)
[ ] You know the expected duration (±50%) from the clone test
[ ] You have a communication channel (#incidents or on-call) open during migration
[ ] You know who to escalate to if something goes wrong
[ ] The migration window does NOT overlap with: deployments, peak traffic, team PTO, weekends
```

---

## When a Small Team Should NOT Migrate

- **"It would be nice to use PostgreSQL" but MySQL works fine**: Platform preference is not a business justification. Migration cost (2-6 weeks) must have a clear ROI.
- **You have 0 users and are pre-launch**: Just launch on the new platform. Don't migrate an empty database. Delete it and start fresh.
- **The database is <100MB and you can afford 30 min downtime**: Dump → modify → restore. No need for zero-downtime patterns. Schedule a maintenance window. Tweet about it.
- **The migration would take longer than rewriting the affected module**: If rewriting is 2 weeks and migrating is 4 weeks, rewrite. But be honest about rewrite estimates (they're always 2-3x optimistic).
- **You're planning to pivot or sunset the product within 6 months**: Don't migrate a product you're about to kill. Maintain it. Minimal fixes. Redirect engineering time to the new thing.
