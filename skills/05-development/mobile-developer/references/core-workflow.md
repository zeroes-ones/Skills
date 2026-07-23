# Core Workflow — Full Implementation

<!-- QUICK: 30s -- scan phase titles to understand the process -->
### Phase 0 (~15 min): Native vs Cross-Platform Decision Framework
<!-- DEEP: 10+min -->

Before writing a single line of code, select the right technology for the job. The wrong choice can cost months of rework.

**Choose Native (Swift/SwiftUI + Kotlin/Jetpack Compose) when:**
- GPU-intensive rendering is required (games, AR/VR, real-time video processing, Metal/Vulkan access)
- Complex, chained animations must run at 60fps on low-end devices — cross-platform animation bridges add 2-8ms overhead per frame
- Heavy hardware integration: Bluetooth LE peripheral mode, NFC with custom APDUs, Camera2/Core Image pipelines, Core Motion sensor fusion at 100Hz+
- Platform-specific UX is a competitive advantage (e.g., fitness app using HealthKit, banking app needing per-platform trust signals)
- Team has dedicated iOS and Android engineers — dual-platform codebases diverge naturally; fighting a cross-platform abstraction layer adds friction, not velocity

**Choose React Native when:**
- App is content-heavy with standard UI patterns: feeds, lists, forms, CRUD, dashboards
- Team has React/TypeScript expertise — reuse 60-80% of code; the remaining 20-40% is platform-specific (navigation feel, haptics, permissions, native modules)
- Time-to-market is critical: single codebase for MVP, prove product-market fit, then optimize native modules incrementally
- OTA updates are needed: CodePush/expo-updates let you ship JS bundle changes without app store review (Apple allows this for non-native changes per guideline 4.7)
- Anti-pattern: Don't use React Native for apps requiring complex gesture handling (3+ simultaneous gesture recognizers), background audio processing, or per-frame video manipulation — the JS-Native bridge bottleneck still applies even with JSI/Fabric

**Choose Flutter when:**
- Pixel-perfect custom UI that must look identical on iOS and Android — Flutter's Skia/Impeller rendering engine draws every pixel; no platform UI component mapping
- Complex custom animations: Flutter's animation framework provides 60fps out of the box with no bridge overhead (all rendering is on the GPU thread)
- Team lacks web/React background — Dart is easier to learn than React's hooks/JSX paradigm for developers coming from Java/Kotlin/Swift
- Target includes desktop (macOS, Windows, Linux) or web alongside mobile — single Flutter codebase for all four platforms
- Anti-pattern: Avoid Flutter for apps that must feel deeply "platform-native" (heavy OS integration, complex share sheets, platform-specific text selection behavior) — Flutter's custom rendering means platform conventions must be manually recreated

**Performance comparison (real-world benchmarks on mid-range device, iPhone 12 / Pixel 6 equivalent):**

| Metric | Native (Swift/Kotlin) | React Native (Fabric) | Flutter (Impeller) | PWA |
|--------|----------------------|----------------------|--------------------|-----|
| Cold start (ms) | 300-600 | 800-1500 | 600-1000 | 1500-3000 |
| 60fps scrolling | Guaranteed | OK with FlatList/FlashList | Guaranteed | Variable |
| Binary size (MB) | 15-30 | 20-40 (Expo: +10) | 15-25 | 0 (browser) |
| Memory baseline (MB) | 30-60 | 60-120 | 40-80 | 50-150 |
| Native API access | Complete | Via native modules | Via platform channels | Limited |

### Phase 1 (~15 min): Project Scaffolding & Architecture

**Clean Architecture Layers (applies to all frameworks):**
- **Presentation layer**: Screens, widgets, UI components. Depends on Domain layer. Contains no business logic — only UI state transformation and event delegation.
- **Domain layer**: Use cases, entities, repository interfaces. Pure Dart/Swift/Kotlin/TypeScript — zero framework imports. This layer is the source of truth for what the app *does*.
- **Data layer**: Repository implementations, data sources (remote API, local DB, cache), DTOs with mappers to domain entities. Handles serialization, error mapping, pagination.

**React Native + Expo (recommended for 90% of RN projects):**
```bash
npx create-expo-app@latest --template tabs  # expo-router with tab navigation
```
- Use Expo SDK managed workflow. Eject to bare workflow (expo prebuild) ONLY when: you need a native module not in Expo's module ecosystem, custom Metal/Vulkan rendering, or Bluetooth LE peripheral mode.
- TypeScript strict mode: `strict: true` in tsconfig. Zero `any` types in domain/data layers.
- Folder structure (feature-based, scalable to 50+ screens):
  ```
  src/
    app/              # expo-router file-based routes
    features/
      auth/
        screens/      # LoginScreen, SignupScreen, ForgotPasswordScreen
        components/   # AuthForm, SocialLoginButton, BiometricPrompt
        hooks/        # useAuth, useBiometric
        services/     # authService.ts (API calls)
        types.ts      # LoginRequest, AuthToken, User
        __tests__/    # unit + integration
    shared/
      components/     # Button, TextInput, Card, BottomSheet — design system
      hooks/          # useNetworkStatus, useDebounce, useAppState
      utils/          # formatDate, haptics, platformSelect
      types/          # shared domain types
    services/         # apiClient, secureStorage, analytics
  ```


**What good looks like:** App builds and runs on both iOS and Android from a single codebase commit. All screens render correctly on the smallest and largest supported device sizes (iPhone SE to Pro Max, Pixel to Galaxy Ultra). No red boxes, crash logs, or ANR reports in the last 100 test sessions. App store review passes on first submission — no guideline violations. Launch-to-interaction time < 2s on a mid-range device (Pixel 6 / iPhone 12).

**Flutter (using very_good_cli):**
```bash
very_good create my_app --org com.company --platforms ios,android
```
- Layered architecture: `lib/features/<feature>/` with `data/`, `domain/`, `presentation/` subdirectories
- Dependency injection: use `get_it` + `injectable` (code generation) for a compile-time-safe service locator; avoid `provider` for DI — it's a state management solution, not a DI container
- Environment configuration: `flutter_dotenv` with `.env.development`, `.env.staging`, `.env.production`. Use Dart define flags (`--dart-define=ENVIRONMENT=staging`) for compile-time constants; env files for runtime config only.

**Monorepo structure (when sharing code with web/backend):**
```
packages/
  api-client/        # Shared API types, fetch wrapper, error types
  ui/                # Shared design tokens, if cross-platform component library
  utils/             # Date formatting, validation, constants
apps/
  mobile/            # React Native / Flutter mobile app
  web/               # Next.js web app (if applicable)
```
Use `turborepo` for task orchestration — it caches build outputs and only rebuilds changed packages.

### Phase 2 (~30 min): Navigation & Deep Linking

**Architecture decision: file-based vs programmatic routing**
- **File-based** (expo-router, go_router with ShellRoute): best for standard navigation patterns; co-location of routes with screens; automatic type generation
- **Programmatic** (React Navigation imperative, Navigator 2.0): when navigation depends on complex runtime state (multi-step wizards that branch, role-based navigation trees, deep link handling with conditional redirects)

**Navigation patterns — when to use each:**
| Pattern | Use case | Anti-pattern |
|---------|----------|--------------|
| Tab Bar (bottom) | 3-5 top-level destinations, flat hierarchy | Don't nest tab bars (bottom tabs + top tabs in same flow = confusing) |
| Stack (push/pop) | Hierarchical drill-down, forms, detail screens | Don't go deeper than 5 levels — use modal for sub-flows |
| Drawer | 5+ destinations, secondary navigation, settings | Not for primary navigation on phones; OK on tablets |
| Modal | Focused task, create/edit flows, alerts requiring action | Don't stack modals — max 1 modal deep |

**Deep linking — production-grade configuration:**
```typescript
// expo-router deep link configuration (app.json)
{
  "scheme": "myapp",
  "associatedDomains": ["applinks:myapp.com"],  // iOS universal links
  "intentFilters": [{                            // Android app links
    "action": "VIEW",
    "autoVerify": true,
    "data": [{ "scheme": "https", "host": "myapp.com" }]
  }]
}
```
- Map every route to a URL path: `product/:id` → `myapp://product/123`
- Deferred deep links: use Branch/AppFlyer for install attribution — user clicks link, installs app, opens to target screen on first launch
- Test deep links: `xcrun simctl openurl booted "myapp://product/123"` (iOS), `adb shell am start -W -a android.intent.action.VIEW -d "myapp://product/123"` (Android)

**Authentication flow (zero-flash pattern):**
1. On app launch, show native splash screen (not a JS/Flutter loading screen — uses launch screen storyboard/xib)
2. Check stored auth token while splash is showing
3. If token exists: validate with server (non-blocking), navigate to main app
4. If no token: navigate to auth stack
5. Hide splash ONLY after navigation target is determined — this prevents the "flash of wrong screen"
6. On logout: clear all cached data, navigate to auth stack with `reset` (no back button to main app)

### Phase 3 (~20 min): State Management & Offline-First Data Layer

**State management taxonomy — choose the right tool for each state category:**

| State Type | React Native | Flutter | Characteristics |
|------------|-------------|---------|-----------------|
| Server state | TanStack Query | Riverpod + AsyncValue | Cached, eventually consistent, paginated |
| Client/global | Zustand | Riverpod StateNotifier | Shared across screens, persisted |
| Form state | React Hook Form + Zod | flutter_form_builder + formz | Ephemeral, validation-heavy |
| UI ephemeral | useState/useReducer | StatefulWidget/ValueNotifier | Single component, discarded on unmount |
| Navigation state | expo-router (built-in) | go_router (built-in) | URL-derived, type-safe params |
| Persistent/local DB | WatermelonDB, MMKV | Isar, Drift | Source of truth for offline-first |

**Offline-first architecture — the definitive approach:**

The golden rule: **local database is the source of truth; the server is a backup.** Never code as if the network is always available.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  UI Layer   │ ←──→│ Domain Layer │ ←──→│  Repository │
│ (screens)   │     │ (use cases)  │     │   (facade)  │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                          ┌────┴────┐
                                    ┌─────┴────┐ ┌──┴──────────┐
                                    │ Local DB │ │ Remote API   │
                                    │ (primary)│ │ (secondary)  │
                                    └──────────┘ └──────────────┘
                                          │              │
                                          └── Sync ──────┘
```

**Sync strategy selection:**

| Strategy | When to use | Conflict handling | Example |
|----------|------------|-------------------|---------|
| Last-write-wins (LWW) | Single-user apps, non-collaborative data | Timestamp comparison | Note-taking app, settings sync |
| CRDT (Conflict-free Replicated Data Types) | Multi-user collaboration, offline editing | Automatic merge via CRDT semantics | Google Docs-style editor, shared task lists |
| Operational Transform (OT) | Real-time collaboration with central server | Server-mediated transformation | Google Docs (original), text editors |
| Delta sync | Large datasets, batch updates | Server as authority, client replays missing deltas | Calendar sync, email sync |

**Sync queue implementation pattern (React Native example):**
```typescript
// 1. User performs mutation → written to local DB immediately + queued
async function updateTodo(todo: Todo) {
  await localDB.update('todos', todo);              // optimistic local update
  await syncQueue.enqueue('UPDATE_TODO', todo);     // queue for server
}

// 2. Sync worker processes queue when online
syncQueue.onConnectivityChange(async (online) => {
  if (online) {
    const pending = await syncQueue.getPending();    // FIFO order
    for (const item of pending) {
      try {
        await apiClient.sync(item);
        await syncQueue.markComplete(item.id);
      } catch (error) {
        if (isConflict(error)) {
          await resolveConflict(item, error.serverVersion);
        } else {
          await syncQueue.markFailed(item.id, error);
        }
      }
    }
  }
});
```

**Local database selection:**
- **WatermelonDB** (React Native): Lazy-loading SQLite. Only loads records when accessed — survives 10,000+ records without memory pressure. Best for relational data.
- **MMKV** (React Native): Synchronous key-value storage, 30x faster than AsyncStorage. Use for tokens, settings, small objects. NOT for relational queries.
- **Isar** (Flutter): NoSQL with links (relationships), full-text search, ACID transactions. Best all-rounder for Flutter local storage.
- **Drift** (Flutter): Type-safe SQLite wrapper with reactive queries. Use when you need complex SQL joins and migrations.

**Production-grade sync queue — priority levels, backoff, and dead letters:**

The simple FIFO queue above works for demos. Production needs priority ordering, exponential backoff with jitter, and a dead letter queue for permanently failed operations.

```typescript
type SyncPriority = 'critical' | 'high' | 'normal' | 'background';
type SyncStatus = 'pending' | 'in_flight' | 'completed' | 'dead_letter';

interface SyncItem {
  id: string;
  type: 'CREATE' | 'UPDATE' | 'DELETE';
  entity: string;           // table or collection name
  payload: Record<string, unknown>;
  priority: SyncPriority;
  retries: number;          // 0–5
  maxRetries: number;       // default 5
  lastError?: string;
  createdAt: number;        // epoch ms
  nextRetryAt: number;      // epoch ms
  status: SyncStatus;
  localVersion: number;     // monotonic counter for conflict detection
}

class SyncQueue {
  private queue: SyncItem[] = [];
  private processing = false;

  /** Enqueue with priority-based insertion. Critical items (life-saving data
   *  like bleed logs) jump to the front. Background items (analytics) wait. */
  async enqueue(item: Omit<SyncItem, 'id' | 'retries' | 'status' | 'localVersion'>): Promise<void> {
    const syncItem: SyncItem = {
      ...item,
      id: uuid(),
      retries: 0,
      status: 'pending',
      localVersion: await this.getLocalVersion(item.entity),
      nextRetryAt: Date.now(),
    };
    // Insert at correct priority position
    const priorities: SyncPriority[] = ['critical', 'high', 'normal', 'background'];
    const insertIdx = this.queue.findIndex(
      q => priorities.indexOf(q.priority) > priorities.indexOf(syncItem.priority)
    );
    if (insertIdx === -1) this.queue.push(syncItem);
    else this.queue.splice(insertIdx, 0, syncItem);

    await this.persist(); // save queue to MMKV — survives app kill
  }

  /** Process queue with exponential backoff + jitter. Called when online. */
  async processAll(): Promise<void> {
    if (this.processing) return;
    this.processing = true;

    while (this.queue.some(q => q.status === 'pending' && q.nextRetryAt <= Date.now())) {
      const item = this.queue.find(q => q.status === 'pending' && q.nextRetryAt <= Date.now())!;
      item.status = 'in_flight';

      try {
        await this.dispatch(item);
        item.status = 'completed';
        this.queue = this.queue.filter(q => q.id !== item.id);
      } catch (error) {
        item.retries++;
        item.lastError = String(error);

        if (item.retries >= item.maxRetries) {
          // Dead letter — permanently failed. Alert the user for critical items.
          item.status = 'dead_letter';
          if (item.priority === 'critical') {
            this.notifyUser('Sync failed', `Could not save ${item.entity}`);
          }
        } else {
          // Exponential backoff: 2^n * base_delay with 20% jitter
          const baseDelay = item.priority === 'critical' ? 1_000 : 5_000;
          const delay = Math.min(
            Math.pow(2, item.retries) * baseDelay * (0.8 + Math.random() * 0.4),
            5 * 60 * 1000  // cap at 5 minutes
          );
          item.nextRetryAt = Date.now() + delay;
          item.status = 'pending';
        }
      }
      await this.persist();
    }
    this.processing = false;
  }
}
```

**Conflict resolution — three-way merge for offline mutations:**

```typescript
interface ConflictResolution<T> {
  /** Three-way merge using base (last known server state), local, and remote versions.
   *  This is the industry standard — Git uses the same algorithm. */
  resolve(params: {
    baseVersion: T;      // what the server had when we last synced
    localVersion: T;     // what we changed offline
    remoteVersion: T;    // what the server now has (someone else's change)
    strategy: 'last-write-wins' | 'client-wins' | 'server-wins' | 'field-merge';
    fieldRules?: Record<string, 'client' | 'server'>;  // per-field authority for field-merge
  }): T;
}

// Health app example: bleed log entry
function resolveBleedLogConflict(params: {
  baseVersion: BleedLogEntry;
  localVersion: BleedLogEntry;
  remoteVersion: BleedLogEntry;
}): BleedLogEntry {
  const { base, local, remote } = params;

  // If remote hasn't changed since base → use local (no conflict)
  if (remote.updatedAt === base.updatedAt) return local;

  // If local hasn't changed since base → use remote (no conflict)
  if (local.updatedAt === base.updatedAt) return remote;

  // Both changed → field-level merge based on medical safety rules
  return {
    ...remote,
    // User's symptom report always wins (subjective, can't be overridden)
    symptoms: local.symptoms,
    // Severity: take the higher value (safety-first — never downgrade severity)
    severity: Math.max(local.severity, remote.severity),
    // Treatment notes: merge both (don't lose information)
    treatmentNotes: `${remote.treatmentNotes}\n---Additional entry---\n${local.treatmentNotes}`,
    // Administrative fields: server wins (timestamps, flags set by backend)
    updatedAt: remote.updatedAt,
    reviewedBy: remote.reviewedBy,
  };
}
```

**Offline mutations — temporary IDs and sync ordering:**

When creating records offline, generate a temporary client-side ID. On first successful sync, the server returns the permanent ID. All child records must reference the parent by its temporary ID until the parent is synced.

```typescript
// 1. Create parent (bleed log entry) — temporary ID
const tempBleedId = `temp_${uuid()}`;
await localDB.insert('bleed_logs', { id: tempBleedId, ...data, _synced: false });
await syncQueue.enqueue({ type: 'CREATE', entity: 'bleed_logs', payload: { id: tempBleedId, ...data }, priority: 'critical' });

// 2. Create child (treatment) — references temp parent ID
await localDB.insert('treatments', { id: `temp_${uuid()}`, bleedLogId: tempBleedId, ...treatmentData, _synced: false });
await syncQueue.enqueue({ type: 'CREATE', entity: 'treatments', payload: { bleedLogId: tempBleedId, ...treatmentData }, priority: 'critical' });

// 3. Sync worker enforces ordering: CREATE parents before children
// On successful parent sync, remap temp IDs to real IDs:
const idMapping = new Map<string, string>(); // tempId → realId
idMapping.set(tempBleedId, serverResponse.id);
// Update all queued child items referencing tempBleedId
for (const item of syncQueue.getByParent(tempBleedId)) {
  item.payload.bleedLogId = serverResponse.id;
}
```

**Network state machine — graceful degradation by connection quality:**

```typescript
type NetworkState = 'online-fast' | 'online-slow' | 'online-metered' | 'offline';
type NetworkStrategy = 'sync-all' | 'sync-critical-only' | 'queue-only' | 'read-cache-only';

const strategyForState: Record<NetworkState, NetworkStrategy> = {
  'online-fast': 'sync-all',            // full sync, fetch fresh data, upload all
  'online-slow': 'sync-critical-only',  // only bleed logs + meds, defer analytics/images
  'online-metered': 'queue-only',       // don't download images/video, queue writes
  'offline': 'read-cache-only',         // local DB only, show stale-data banner
};

// Connectivity detection with quality assessment
const useNetworkMonitor = () => {
  const [state, setState] = useState<NetworkState>('offline');

  useEffect(() => {
    const check = async () => {
      const netInfo = await NetInfo.fetch();
      if (!netInfo.isConnected) return setState('offline');
      if (netInfo.details?.isConnectionExpensive) return setState('online-metered');

      // Measure latency with a HEAD request to health endpoint
      const start = Date.now();
      try {
        await fetch(`${API_BASE}/health`, { method: 'HEAD' });
        const latency = Date.now() - start;
        setState(latency < 500 ? 'online-fast' : 'online-slow');
      } catch {
        setState('offline');
      }
    };
    check();
    return NetInfo.addEventListener(check);
  }, []);

  return state;
};
```

**Delta sync with sequence numbers — minimize transferred data:**

```typescript
interface DeltaSyncState {
  lastSequence: number;       // last server sequence number we've seen
  lastFullSync: number;       // epoch ms of last complete sync
}

async function deltaSync(state: DeltaSyncState): Promise<DeltaSyncState> {
  // 1. Pull: ask server for changes since our last known sequence
  const response = await apiClient.get('/sync/pull', {
    params: { since: state.lastSequence, limit: 500 }
  });
  // Server returns: { changes: [...], newSequence: 1042, hasMore: false }

  // 2. Apply server changes to local DB in order
  for (const change of response.changes) {
    await applyChangeToLocalDB(change);
    state.lastSequence = Math.max(state.lastSequence, change.sequence);
  }

  // 3. Push: send our pending changes to server
  const pendingLocal = await syncQueue.getPending();
  const pushResponse = await apiClient.post('/sync/push', {
    changes: pendingLocal,
    baseSequence: state.lastSequence,  // server checks for conflicts
  });

  // 4. Handle push conflicts
  for (const conflict of pushResponse.conflicts) {
    const resolved = resolveConflict(conflict);
    await localDB.update(conflict.entity, resolved);
  }

  // 5. Periodically do a full reconciliation (e.g., every 24h or on WiFi)
  if (Date.now() - state.lastFullSync > 24 * 60 * 60 * 1000) {
    const fullData = await apiClient.get('/sync/full');
    await localDB.replaceAll(fullData);
    state.lastFullSync = Date.now();
    state.lastSequence = fullData.sequence;
  }

  return state;
}
```

**TTL-based cache invalidation policy by data type:**

| Data Type | Cache TTL | Stale-While-Revalidate | Strategy |
|-----------|-----------|----------------------|----------|
| User profile | 1 hour | Yes (show cached, refresh bg) | `staleTime: 60 * 60 * 1000` |
| Forum posts list | 5 min | Yes | Invalidate on pull-to-refresh |
| Forum post detail | 30 sec | No (show loader for fresh data) | Real-time via WebSocket push |
| Bleed log entries | Immediate | No (health data — never stale) | `staleTime: 0, cacheTime: 0` |
| Medication list | 1 hour | Yes | Invalidate on user edit |
| Notification preferences | 24 hours | Yes | User rarely changes these |
| Static content (FAQs) | 7 days | Yes | Hard reload on app update |
| Pod/condition data | 1 hour | Yes | Invalidate on pod membership change |

### Phase 4 (~15 min): Push Notifications

**Provider architecture:**
```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Backend │ →──│   FCM    │ →──│  Android  │
│  Server  │    │  (Google)│    │  Device   │
│          │    └──────────┘    └──────────┘
│          │    ┌──────────┐    ┌──────────┐
│          │ →──│   APNs   │ →──│   iOS    │
│          │    │  (Apple) │    │  Device   │
└──────────┘    └──────────┘    └──────────┘
```

**Critical implementation details:**
- APNs tokens rotate. Always register for token updates on each app launch — do NOT assume a stored token is valid. iOS may issue a new token after app reinstall, device restore, or OS update.
- FCM tokens also change. Subscribe to `onTokenRefresh` callback.
- Store the platform and token together: `{ platform: 'ios', token: '...', lastUpdated: Date }`. Backend needs to know which push service to route through.
- Never send sensitive data in the notification payload itself — push services (Apple/Google) log these. Put only a reference ID in `data`, fetch actual content from your API on notification tap.

**Notification priority taxonomy:**
| Priority | Android | iOS | Use case |
|----------|---------|-----|----------|
| High (10) | `priority: high` | `apns-priority: 10` | Time-sensitive: chat messages, OTP codes, ride updates |
| Normal (5) | `priority: normal` | `apns-priority: 5` | Standard: social updates, content alerts, reminders |
| Background | Silent FCM | `content-available: 1` | Data sync trigger, no user-visible notification |

**APNS device token lifecycle — the full picture:**
- **Registration**: On app launch, call `registerForRemoteNotifications()`. iOS returns a device token via `application(_:didRegisterForRemoteNotificationsWithDeviceToken:)`. This token is unique to the device + app combination and changes across reinstalls, device restores, and major OS updates.
- **Refresh detection**: iOS may issue a new token without user interaction. Always compare the received token against the last stored token. If different, send to backend immediately — old token will fail silently, causing undelivered notifications.
- **Invalidation**: The delegate method `application(_:didFailToRegisterForRemoteNotificationsWithError:)` fires when registration fails. Common causes: no network, no provisioning profile entitlement, simulator (push doesn't work on simulator — test on device).
- **Multi-device handling**: A user with iPhone + iPad + Apple Watch gets different APNs tokens per device. Your backend must store an array of `{ deviceId, platform, token, lastActive }` per user. When sending, broadcast to all or target by last-active device.
- **APNs auth**: Use token-based authentication (JWT with p8 key) — it never expires, unlike certificate-based auth which requires annual renewal. One p8 key covers all your team's apps.

**Notification Service Extension (iOS) — modify push before display:**

```swift
// NotificationService.swift — runs in a separate process, ~30s execution window
// Use cases: decrypt end-to-end encrypted push payload, download rich media attachment
class NotificationService: UNNotificationServiceExtension {
    override func didReceive(_ request: UNNotificationRequest,
        withContentHandler contentHandler: @escaping (UNNotificationContent) -> Void) {

        guard let bestAttempt = request.content.mutableCopy() as? UNMutableNotificationContent else {
            contentHandler(request.content); return
        }

        // 1. Decrypt E2E-encrypted payload (e.g., chat message body)
        if let encryptedBody = bestAttempt.userInfo["encrypted_body"] as? String {
            bestAttempt.body = decryptPayload(encryptedBody) ?? "New message"
        }

        // 2. Download rich media attachment (image, video thumbnail)
        if let imageUrl = bestAttempt.userInfo["image_url"] as? String {
            downloadAttachment(from: imageUrl) { attachment in
                if let attachment = attachment {
                    bestAttempt.attachments = [attachment]
                }
                contentHandler(bestAttempt)
            }
        } else {
            contentHandler(bestAttempt)
        }
    }
}
```

**Notification Content Extension (iOS) — custom notification UI:**
- Provides a custom `UIViewController` displayed when the user 3D-touches or long-presses a notification. Use for: interactive charts, message threads, calendar event previews. Not for: replacing standard notification look entirely (Apple rejects this).
- Register in Info.plist with `UNNotificationExtensionCategory` matching the notification category identifier.
- Limited interaction — no keyboard input, no scrolling `UITableView`. Use `UNNotificationContentExtension` protocol methods for media playback controls or quick action buttons.

**Android notification channels deep-dive:**

```kotlin
// Create channel on app startup — Android 8.0+ requires channels for ALL notifications
// If no channel matches, notification is silently dropped on API 26+
val channel = NotificationChannel(
    "chat_messages",            // id: immutable once created
    "Chat Messages",            // name: user-visible in system settings
    NotificationManager.IMPORTANCE_HIGH // importance: controls sound, heads-up, interruption
).apply {
    description = "Incoming chat messages from your conversations"
    enableVibration(true)
    vibrationPattern = longArrayOf(0, 200, 100, 200) // custom pattern
    setShowBadge(true)          // show dot on app icon
    lockscreenVisibility = Notification.VISIBILITY_PRIVATE // hide content on lock screen
}

notificationManager.createNotificationChannel(channel)
```

**Importance levels — pick the right one:**

| Level | Behavior | Use Case |
|-------|----------|----------|
| `IMPORTANCE_HIGH` | Heads-up popup, sound, vibration | Chat messages, ride arrival, security alerts |
| `IMPORTANCE_DEFAULT` | Sound, no popup | Social updates, content alerts |
| `IMPORTANCE_LOW` | No sound, status bar only | Weather updates, sync status |
| `IMPORTANCE_MIN` | No sound, no visual interruption | Background data sync confirmations |
| `IMPORTANCE_NONE` | Blocked entirely | Deprecated channel migration placeholder |

**Channel groups:** Group related channels so users can manage them together in system settings. E.g., group "Messages" with sub-channels: "Direct Messages" + "Group Messages" + "Message Reactions."

**Silent/background notification best practices:**
- **iOS `content-available: 1`**: Set `apns-priority: 5` (not 10). The payload MUST NOT include `alert`, `sound`, or `badge` — or iOS may throttle it. iOS delivers at most 2-3 silent pushes per hour when the app is not in the foreground, and may coalesce them.
- **Android data payloads**: Omit `notification` key entirely; include only `data`. The app receives the payload in `onMessageReceived` and decides whether to post a local notification. This bypasses the system tray for true background processing.
- **Rate limits**: APNs silently throttles excessive background pushes. FCM collapses messages with the same `collapse_key`. Always include a collapse key for messages that replace previous ones (e.g., "new like on post" — only the latest matters).
- **User-facing rate limit**: More than 4-5 notifications/day from non-messaging apps leads to the user disabling notifications. Respect the user's attention.

**Push notification reliability — detecting and diagnosing failures:**
- **APNs feedback service**: APNs returns status codes (`410 Unregistered` = token invalid, remove it from your database). Poll the feedback service or use the HTTP/2 stream to get real-time delivery failures.
- **FCM delivery diagnostics**: FCM provides delivery receipt via `send_to_device` response (`success`, `failure`, `canonical_ids`). A `NotRegistered` error means the token is stale — delete it. A `canonical_id` in the response means the token was refreshed — update your database.
- **Handling expired tokens**: If a push send returns `410` (APNs) or `NotRegistered` (FCM), remove the token from your database immediately. Sending to invalid tokens wastes quota and may trigger rate limiting by Apple/Google.
- **End-to-end test**: Maintain a backend endpoint that sends a silent notification to a test device on demand. Run this test in CI on every deploy to verify the push pipeline: backend → APNs/FCM → device. A broken push pipeline produces zero user-facing errors — just silently undelivered notifications.

### Phase 5 (~25 min): Platform Design Systems

**iOS Human Interface Guidelines — non-negotiable rules:**
- **Touch targets**: minimum 44×44pt. No exception. Apple rejects apps with tappable elements smaller than this.
- **Safe Areas**: Always respect safe area insets (top notch/island, bottom home indicator). Use `SafeAreaView` (RN) or `SafeArea` (Flutter) — never hardcode padding values.
- **Typography**: Use the system font (SF Pro). Support Dynamic Type — all text must scale when user changes accessibility text size. Test with largest accessibility text size; layouts must not break.
- **Navigation**: Tab bars at bottom for top-level destinations (3-5 items). Use hierarchical navigation with back chevron for drill-down. Modals for focused tasks — always provide clear dismiss action.
- **Gestures**: Standard gestures only unless you have a strong reason. Swipe-back from left edge is sacred on iOS — don't override it globally.
- **Dark Mode**: EVERY screen must support Dark Mode. Use semantic colors (label, secondaryLabel, systemBackground) that adapt automatically.
- **Haptics**: Use `UIImpactFeedbackGenerator` for confirmations, selections, and errors. Tiny detail — massive perceived quality difference. `light` for selection, `medium` for confirmation, `heavy` for errors, `rigid` for toggle switches.

**Android Material Design 3 — non-negotiable rules:**
- **Touch targets**: minimum 48dp. The extra 4dp over iOS accounts for Android's larger default finger size assumption.
- **Edge-to-edge**: Apps MUST draw behind the status bar and navigation bar (Android 15+ enforces this). Use `WindowInsets` APIs — never hardcode status bar height.
- **Material You (Monet)**: Support dynamic color on Android 12+. User-chosen wallpaper colors flow through your app via `android:colorPrimary` and M3 color roles.
- **Predictive back gesture** (Android 14+): Users expect to see a preview of the destination screen during a back swipe. Implement `OnBackPressedCallback` with `setEnabled(false)` to opt into the system back animation.
- **Typography**: Use Material type scale tokens (`displayLarge` through `labelSmall`). Roboto is default; Google Sans for brand moments only.
- **Navigation Bar**: Bottom for phones, Navigation Rail (side) for tablets/landscape. Use `NavigationBar` composable or BottomNavigationView (views).

For complete platform design system details, see `references/ios-hig-cheatsheet.md` and `references/material-design-cheatsheet.md`.

### Phase 6 (~25 min): Performance Optimization

Performance is the #1 reason users delete apps. A 2-second delay in startup increases abandonment by 20%.

**Cold start time target: < 1.5 seconds to interactive (measured from user tap to first frame render + data visible)**

| Optimization | Framework | Impact |
|-------------|-----------|--------|
| Native splash screen (not JS splash) | All | -200-500ms perceived |
| Lazy init non-critical SDKs (analytics after 1s delay) | All | -100-300ms |
| Hermes engine (React Native) | RN | -200-400ms TTI |
| Dart AOT compilation (default in release) | Flutter | Already optimized |
| Minimize main isolate/Dart entry point work | Flutter | -100-200ms |
| Deferred component loading | RN/Flutter | -500KB+ binary |

**List performance — 60fps scrolling is non-negotiable:**
- **React Native**: Use `FlashList` (Shopify) instead of `FlatList` — it's 5-10x faster for large lists by recycling views more aggressively. Estimated item size + `getItemType` for heterogeneous lists.
- **Flutter**: Use `ListView.builder` — never `ListView(children: [...])` for lists over 20 items. `itemExtent` for fixed-height items (avoids layout pass per item).
- **Both**: Paginate with cursor-based pagination. Load 20-30 items per page. Implement `onEndReached` with threshold (0.5 = trigger when half a screen away from end). Guard against double-fires with a loading ref/lock.

**Image optimization:**
- Always resize server-side to exact display dimensions × device pixel ratio. A 4000×3000 photo displayed at 375×250 wastes 99.7% of decoded memory.
- Progressive JPEGs: show low-res (10-20KB) immediately, swap to full-res on load. Prevents white flash.
- Memory cache: 1/4 of available RAM (not disk RAM — runtime memory). Disk cache: 200MB max, LRU eviction.
- Libraries: `expo-image` (React Native, built on Glide/SDWebImage), `cached_network_image` (Flutter).

**Animation performance — never block the UI thread:**
- React Native: Always use `useNativeDriver: true` for `Animated` API. Animations without native driver run on the JS thread — any JS work (state update, API response parsing, navigation transition) causes frame drops.
- Flutter: Most animations are GPU-driven by default. For complex custom painters, use `RepaintBoundary` to isolate repaint areas and avoid full-screen repaints.

For deep performance optimization guides, see `references/performance-optimization.md`.

### Phase 7 (~25 min): Security

Mobile security is defense-in-depth. Assume the device is compromised — never trust the client.

| Layer | Technique | Framework |
|-------|-----------|-----------|
| Transport | Certificate pinning (pinned to leaf or intermediate CA) | react-native-ssl-pinning, flutter_trusted_device |
| Storage | iOS Keychain / Android Keystore for secrets; EncryptedSharedPreferences for tokens | expo-secure-store, flutter_secure_storage |
| Code | ProGuard/R8 (Android), code obfuscation | Built into Android build; react-native-obfuscating-transformer |
| Integrity | Root/jailbreak detection, SafetyNet/Play Integrity | react-native-device-info, flutter_jailbreak_detection |
| Auth | Biometric + device credential fallback; never store PIN | expo-local-authentication, local_auth |
| Network | ATS (App Transport Security) enforced; no HTTP except localhost dev | Info.plist NSAppTransportSecurity (never disable in prod) |

**Hard rules:**
- Never store API keys, client secrets, or symmetric encryption keys in the app binary. Extract strings from any IPA/APK with `strings` command in seconds. Use backend-to-backend communication for secrets.
- Certificate pinning adds ~50KB to binary. Rotate pins every 90 days. Have a backup pin — if you only pin one cert and it expires, your app is bricked until an update is approved (3-7 days for App Store).
- Biometric auth is convenience, not security. Always fall back to server-validated credential after biometric gate. Biometrics can be compelled legally; a password cannot (5th Amendment, US).

### Phase 8 (~30 min): Deployment & CI/CD

**Build pipeline — the gold standard flow:**
```
Push to main → CI triggers:
  1. Lint (ESLint/dart analyze)          ~30s
  2. Type-check (tsc --noEmit)           ~45s
  3. Unit tests (Jest/flutter test)      ~2min
  4. Build dev binary (simulator)        ~5min
  5. Integration tests (Detox/Maestro)   ~8min
  6. Build staging binary                ~10min
  7. Upload to TestFlight/Play Internal  ~3min
  Total: ~30min to staging distribution

Tag release → Production build → Store submission
```

**Code signing — the part that breaks most teams:**
- iOS: Use Fastlane Match with a shared GitHub repo for certificates and provisioning profiles. One source of truth; no "it works on my machine" cert issues. Rotate annually (certificates expire after 1 year).
- Android: Generate upload keystore, store it in CI secrets (base64-encoded). Separate upload key (CI signing) from app signing key (Google-managed via Play Signing). Google Play Signing means even if your upload key is compromised, Google holds the actual app signing key.

**Over-the-air updates:**
- React Native: `expo-updates` — instant JS bundle push. Configure `fallbackToCacheTimeout: 0` (never fallback to embedded bundle if update download fails; the user already has a working version). Test OTA updates thoroughly — a bad push can crash ALL users instantly without app store rollback.
- Flutter: Shorebird — pushes Dart code changes. Still evolving; test extensively before production use.

**Store submission pitfalls that cause rejection:**
1. Missing privacy nutrition labels (Apple). List ALL data types your app collects, even if through third-party SDKs.
2. Requesting permissions without usage strings in Info.plist/AndroidManifest.
3. No "Delete Account" option inside the app (Apple requirement for apps with account creation since June 2022).
4. App crashes on launch on iPad if you only tested iPhone (Apple tests on both).
5. Using private APIs (Apple static analysis catches these). No `LSApplicationQueriesSchemes` beyond what you need.

### Phase 9 (~20 min): Testing Strategy

**Testing pyramid for mobile — adapted from web:**
```
        /\
       /E2E\      10% — Critical flows only (signup, checkout, core CRUD)
      /------\
     /  Inte- \    30% — Feature integration (screen with real API + DB)
    / gration  \
   /------------\
  /    Unit      \ 60% — Business logic, reducers, use cases, validators
 /----------------\
```

**Tools by layer:**
| Layer | React Native | Flutter |
|-------|-------------|---------|
| Unit | Jest + @testing-library/react-native | flutter test (built-in) |
| Widget/Component | @testing-library/react-native | flutter test with `pumpWidget` |
| Integration | Maestro (recommended — YAML-based, works on both platforms) | integration_test (built-in) |
| E2E | Detox (gray-box, Jest-based) or Maestro | patrol (successor to integration_test, more reliable) |
| Snapshot | jest-image-snapshot | golden_toolkit |
| Performance | React Native Performance Monitor, Flipper | Flutter DevTools timeline |

**Testing rules that prevent production incidents:**
- Every API-dependent screen must have a mock provider test that exercises loading, error, empty, and data states.
- Accessibility tests: run `accessibility()` checks in Maestro or manual VoiceOver/TalkBack pass. Every interactive element must have an accessibility label.
- Performance regression: measure cold start time and scroll FPS in CI. Fail the build if cold start exceeds 2s or average scroll FPS drops below 58.

### Phase 10 (~25 min): Streaming Clients & Real-Time Data

Real-time data on mobile is a fundamentally different beast from web. iOS and Android aggressively kill persistent connections when the app goes to background. The right pattern is the difference between a chat app that works and one that drains 30% battery per hour.

**Decision matrix — choose the right real-time transport:**

| Use Case | Transport | Why |
|----------|-----------|-----|
| Chat / messaging | WebSocket (primary) + Silent Push (wake) | Bidirectional low-latency; push wakes the app when WebSocket is killed |
| Live feed (sports scores, stock ticker) | SSE (primary) + Polling (fallback) | Server→client unidirectional; simpler than WebSocket; polling as degraded fallback |
| Data sync trigger (new content available) | Silent Push (`content-available: 1` / FCM data-only) | Minimal battery; app wakes briefly, fetches, goes back to sleep |
| Real-time health data (HR monitor, step counter) | BLE / Core Bluetooth | Persistent peripheral connection; not internet-based |
| Collaborative editing | WebSocket + CRDT merge | Bidirectional low-latency + conflict-free merge on reconnect |

**WebSocket client — production-grade implementation:**

```typescript
// Connection state machine: CONNECTING → CONNECTED → RECONNECTING → DISCONNECTED → SUSPENDED
type ConnectionState =
  | 'CONNECTING'
  | 'CONNECTED'
  | 'RECONNECTING'
  | 'DISCONNECTED'
  | 'SUSPENDED'; // app in background, OS killed socket

function useWebSocket(url: string) {
  const [state, setState] = useState<ConnectionState>('DISCONNECTED');
  const wsRef = useRef<WebSocket | null>(null);
  const retryCount = useRef(0);
  const messageQueue = useRef<string[]>([]);

  const connect = useCallback(() => {
    setState('CONNECTING');
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      setState('CONNECTED');
      retryCount.current = 0;
      // Flush queued offline messages
      while (messageQueue.current.length > 0) {
        ws.send(messageQueue.current.shift()!);
      }
    };

    ws.onclose = (e) => {
      if (state === 'SUSPENDED') return; // don't reconnect if suspended
      setState('RECONNECTING');
      // Exponential backoff + jitter: prevents thundering herd
      const base = Math.min(1000 * 2 ** retryCount.current, 30000);
      const jitter = Math.random() * 1000;
      setTimeout(connect, base + jitter);
      retryCount.current++;
    };

    ws.onmessage = (event) => {
      // Dispatch to appropriate handler based on message type
      handleMessage(JSON.parse(event.data));
    };
  }, [url]);

  // Handle app background/foreground transitions
  useEffect(() => {
    const sub = AppState.addEventListener('change', (nextState) => {
      if (nextState === 'active' && wsRef.current?.readyState !== WebSocket.OPEN) {
        setState('RECONNECTING');
        connect();
      } else if (nextState === 'background') {
        setState('SUSPENDED');
        wsRef.current?.close(); // let OS reclaim socket — silent push will wake us
      }
    });
    return () => sub.remove();
  }, [connect]);

  // Offline message queuing: queue when disconnected, flush on reconnect
  const send = useCallback((data: string) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(data);
    } else {
      messageQueue.current.push(data);
    }
  }, []);

  return { state, send };
}
```

**Reconnection backoff reference table:**

| Attempt | Delay (max jitter) | Why |
|---------|-------------------|-----|
| 1st | 1-2s | Quick recovery from transient network flap |
| 2nd | 2-4s | Brief outage (tunnel, elevator) |
| 3rd | 4-8s | Cell tower handoff |
| 4th+ | 8-30s cap | Avoid battery drain; at this point, lean on silent push to wake |

**SSE consumption on mobile:**

```typescript
// EventSource polyfill — React Native lacks native EventSource; use a lib
import EventSource from 'react-native-sse';

function useLiveFeed(feedUrl: string) {
  const [events, setEvents] = useState<FeedEvent[]>([]);

  useEffect(() => {
    const es = new EventSource(feedUrl, {
      headers: { Authorization: `Bearer ${token}` },
      // Reconnect with backoff built into the polyfill; tune for mobile
      reconnectOnError: true,
      maxReconnectInterval: 15000,
    });

    es.addEventListener('update', (e) => {
      if (e.data) setEvents((prev) => [...prev, JSON.parse(e.data)]);
    });

    es.addEventListener('error', () => {
      // SSE connection lost — fall back to polling if persistent failure
      if (consecutiveFailures > 3) switchToPolling(feedUrl);
    });

    return () => es.close();
  }, [feedUrl]);
}
```

**Battery-efficient real-time — the golden rules:**

1. **Push-triggered fetch beats persistent WebSocket for most apps.** If your data updates every 30+ seconds, use silent push to tell the app "there's new data" and fetch on demand. A persistent WebSocket keeps the radio active — 10-20× more battery than an occasional push + fetch cycle.
2. **WebSocket only for sub-second latency requirements.** Chat, live trading, real-time collaboration. If 2-5 second delay is acceptable, silent push + fetch is always cheaper.
3. **Never hold a WebSocket open in the background.** iOS kills it within ~30 seconds; Android within a few minutes. Both platforms throttle background network. Close the WebSocket in `onBackground`, re-establish in `onForeground`. Use silent push to wake the app for important messages while in background.
4. **Batch and coalesce:** Don't send 50 individual WebSocket messages when the app returns from background — send one "sync since timestamp X" message and process the batch.

**Background modes — what survives and what doesn't:**

| Platform | Persistent connections | Silent push | Background fetch | BLE |
|----------|----------------------|-------------|-----------------|-----|
| iOS (foreground) | Yes | Yes | N/A | Yes |
| iOS (background, < 30s) | Yes (brief grace period) | Yes | Yes (opportunistic) | Yes (with capability) |
| iOS (background, > 30s) | Killed by OS | Yes (limited rate) | Yes (opportunistic, OS decides) | Yes (with capability) |
| Android (foreground) | Yes | Yes | N/A | Yes |
| Android (background) | Minutes, then killed | Yes (high-priority FCM) | Yes (WorkManager) | Yes (with foreground service) |

**What to remember:** iOS kills WebSocket connections aggressively — plan for it. Silent push is your reliable background wake mechanism on both platforms. For real-time data that must work in the background (fitness tracking, navigation), use platform-native background modes (BLE, location updates, audio) with a foreground service (Android) or capability entitlement (iOS).
