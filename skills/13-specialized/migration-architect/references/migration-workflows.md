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
