# Offline-First Mobile Architecture — Reference

> Local database as source of truth with bidirectional sync engine. Users never see a "No Internet" screen. Every screen renders from cache.

---

## Architecture Principles

```
                    ┌──────────────────────────┐
                    │         UI LAYER         │
                    │  Reads from local DB     │
                    │  NEVER calls API directly│
                    └────────────┬─────────────┘
                                 │ observes
                    ┌────────────▼─────────────┐
                    │      LOCAL DATABASE      │
                    │  (Room / Core Data /     │
                    │   GRDB / SQLDelight)     │
                    │                          │
                    │  SINGLE SOURCE OF TRUTH  │
                    └────────┬─────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
    ┌─────────▼────────┐       ┌───────────▼──────────┐
    │   SYNC ENGINE    │       │   CONFLICT RESOLUTION│
    │                  │       │                       │
    │ - Pull: API→DB   │       │  - LWW (last-write-  │
    │ - Push: DB→API   │       │    wins)              │
    │ - Retry with     │       │  - CRDT for           │
    │   exponential    │       │    collaborative      │
    │   backoff        │       │  - Merge strategies   │
    │ - Queue local    │       │    per entity type    │
    │   writes         │       │                       │
    └──────────────────┘       └───────────────────────┘
```

---

## iOS Implementation (GRDB.swift)

### Database Schema

```swift
import GRDB

struct DatabaseMigrator {
    static func migrate(_ db: Database) throws {
        try db.create(table: "product") { t in
            t.column("id", .text).primaryKey()
            t.column("name", .text).notNull()
            t.column("price", .double).notNull()
            t.column("isInStock", .boolean).notNull()
            t.column("imagePath", .text)
            t.column("lastSyncedAt", .datetime).notNull()
            t.column("localModifiedAt", .datetime)
            t.column("syncStatus", .text).notNull()
                .defaults(to: SyncStatus.pending.rawValue)
        }
    }
}

enum SyncStatus: String, Codable {
    case synced
    case pending    // Modified locally, needs push
    case pendingDelete  // Deleted locally, needs push
    case conflicted
}
```

### Database Record

```swift
struct ProductRecord: Codable, FetchableRecord, PersistableRecord {
    var id: String
    var name: String
    var price: Double
    var isInStock: Bool
    var imagePath: String?
    var lastSyncedAt: Date
    var localModifiedAt: Date?
    var syncStatus: SyncStatus

    static let databaseTableName = "product"

    func toDomain() -> Product {
        Product(id: id, name: name, price: price,
                inStock: isInStock, imagePath: imagePath)
    }
}

extension Product {
    func toRecord(syncStatus: SyncStatus = .pending,
                  modifiedAt: Date = Date()) -> ProductRecord {
        ProductRecord(id: id, name: name, price: price,
                      isInStock: inStock, imagePath: imagePath,
                      lastSyncedAt: Date(),
                      localModifiedAt: modifiedAt,
                      syncStatus: syncStatus)
    }
}
```

### Repository with offline-first strategy

```swift
final class ProductRepositoryImpl: ProductRepository {
    private let db: DatabaseQueue
    private let api: ProductAPI
    private let connectivityChecker: ConnectivityChecking

    func getProducts(category: String) async throws -> [Product] {
        // Always read from local DB
        let records: [ProductRecord] = try await db.read { db in
            try ProductRecord
                .filter(Column("category") == category)
                .fetchAll(db)
        }

        if records.isEmpty || shouldRefreshCache(records) {
            // Silently fetch from API in background
            Task.detached(priority: .background) { [weak self] in
                try? await self?.syncProducts(category: category)
            }
        }

        return records.map { $0.toDomain() }
    }

    private func shouldRefreshCache(_ records: [ProductRecord]) -> Bool {
        guard let oldest = records.min(by: { $0.lastSyncedAt < $1.lastSyncedAt })
        else { return true }
        return Date().timeIntervalSince(oldest.lastSyncedAt) > 300 // 5 min TTL
    }

    func syncProducts(category: String) async throws {
        guard connectivityChecker.isOnline else { return }

        // 1. Push pending local changes
        let pending: [ProductRecord] = try await db.read { db in
            try ProductRecord
                .filter(Column("syncStatus") != SyncStatus.synced.rawValue)
                .fetchAll(db)
        }

        for record in pending {
            switch record.syncStatus {
            case .pendingDelete:
                try await api.deleteProduct(id: record.id)
                try await db.write { db in
                    try record.delete(db)
                }
            case .pending:
                let dto = ProductDTO(from: record)
                let updatedDTO = try await api.updateProduct(dto)
                try await db.write { db in
                    var updated = ProductRecord(from: updatedDTO)
                    updated.syncStatus = .synced
                    try updated.save(db)
                }
            default: break
            }
        }

        // 2. Pull fresh data
        let remote = try await api.fetchProducts(category: category)
        try await db.write { db in
            for dto in remote {
                var record = ProductRecord(from: dto)
                record.syncStatus = .synced
                try record.save(db)
            }
        }
    }
}
```

---

## Android Implementation (Room + WorkManager)

### Room Database

```kotlin
@Entity(tableName = "products")
data class ProductEntity(
    @PrimaryKey val id: String,
    val name: String,
    val price: Double,
    val isInStock: Boolean,
    val imagePath: String?,
    val lastSyncedAt: Long,
    val localModifiedAt: Long?,
    val syncStatus: SyncStatus
)

enum class SyncStatus { SYNCED, PENDING, PENDING_DELETE }

@Dao
interface ProductDao {
    @Query("SELECT * FROM products WHERE syncStatus != 'SYNCED'")
    suspend fun getPendingSync(): List<ProductEntity>

    @Query("SELECT * FROM products")
    fun observeAll(): Flow<List<ProductEntity>>

    @Upsert
    suspend fun upsertAll(products: List<ProductEntity>)

    @Query("DELETE FROM products WHERE id = :id")
    suspend fun deleteById(id: String)
}

@Database(entities = [ProductEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun productDao(): ProductDao
}
```

### Repository

```kotlin
class ProductRepository @Inject constructor(
    private val productDao: ProductDao,
    private val productApi: ProductApi,
    private val connectivityChecker: ConnectivityChecker
) {
    fun observeProducts(): Flow<List<Product>> {
        return productDao.observeAll().map { entities ->
            entities.map { it.toDomain() }
        }
    }

    suspend fun refreshProducts(category: String) {
        if (!connectivityChecker.isOnline()) return

        try {
            val remoteProducts = productApi.fetchProducts(category)
            val entities = remoteProducts.map { it.toEntity(syncStatus = SyncStatus.SYNCED) }
            productDao.upsertAll(entities)
        } catch (e: Exception) {
            // Cache is already showing stale data — no need to propagate error
            if (productDao.observeAll().first().isEmpty()) {
                throw e // Only throw if cache is empty (first launch)
            }
        }
    }

    suspend fun updateProduct(product: Product) {
        // Write locally immediately
        val entity = product.toEntity(
            syncStatus = SyncStatus.PENDING,
            localModifiedAt = System.currentTimeMillis()
        )
        productDao.upsertAll(listOf(entity))
        // Sync will happen via WorkManager
    }
}
```

### Sync Worker

```kotlin
@HiltWorker
class SyncWorker @AssistedInject constructor(
    @Assisted context: Context,
    @Assisted params: WorkerParameters,
    private val productDao: ProductDao,
    private val productApi: ProductApi
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        val pending = productDao.getPendingSync()
        if (pending.isEmpty()) return Result.success()

        return try {
            for (entity in pending) {
                when (entity.syncStatus) {
                    SyncStatus.PENDING_DELETE -> {
                        productApi.deleteProduct(entity.id)
                        productDao.deleteById(entity.id)
                    }
                    SyncStatus.PENDING -> {
                        val updated = productApi.updateProduct(entity.toDto())
                        productDao.upsertAll(listOf(updated.toEntity(SyncStatus.SYNCED)))
                    }
                    SyncStatus.SYNCED -> {}
                }
            }
            Result.success()
        } catch (e: Exception) {
            if (runAttemptCount < 5) Result.retry() else Result.failure()
        }
    }

    companion object {
        fun enqueue(context: Context) {
            val constraints = Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .build()

            val request = PeriodicWorkRequestBuilder<SyncWorker>(15, TimeUnit.MINUTES)
                .setConstraints(constraints)
                .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 30, TimeUnit.SECONDS)
                .build()

            WorkManager.getInstance(context)
                .enqueueUniquePeriodicWork(
                    "sync_products",
                    ExistingPeriodicWorkPolicy.KEEP,
                    request
                )
        }
    }
}
```

---

## Conflict Resolution Strategies

| Scenario | Strategy | Example |
|---|---|---|
| Single-user app, device-agnostic | **Last-Write-Wins (LWW)** | Compare `localModifiedAt` vs `serverModifiedAt`. Keep newest. |
| Multi-user, same entity | **Server-authoritative** | Server merges or rejects. Client accepts server state. |
| Collaborative editing | **CRDT (Conflict-free Replicated Data Types)** | Use Automerge or Yjs for document-level sync. |
| Shopping cart | **Merge (union of items)** | Combine local + server items. Deduplicate by product ID. |
| User profile fields | **Field-level LWW** | Track `modifiedAt` per field. Merge newest value per field. |

### LWW Implementation

```kotlin
fun resolveConflict(local: ProductEntity, remote: ProductEntity): ProductEntity {
    return when {
        local.localModifiedAt == null -> remote
        remote.localModifiedAt == null -> local
        local.localModifiedAt!! > remote.localModifiedAt!! -> local
        else -> remote
    }
}
```

---

## Offline Queue Pattern

```kotlin
// Queue local operations for later sync

sealed class PendingOperation {
    data class Create(val entity: ProductEntity) : PendingOperation()
    data class Update(val entity: ProductEntity) : PendingOperation()
    data class Delete(val id: String) : PendingOperation()
}

@Dao
interface PendingOperationDao {
    @Query("SELECT * FROM pending_operations ORDER BY createdAt ASC")
    suspend fun getAll(): List<PendingOperationEntity>

    @Insert
    suspend fun insert(op: PendingOperationEntity)

    @Delete
    suspend fun delete(op: PendingOperationEntity)
}

// When user performs action while offline:
// 1. Apply change locally (optimistic update)
// 2. Enqueue PendingOperation
// 3. SyncWorker processes queue when online
// 4. UI already reflects the change — no user friction
```

---

## Testing Offline Scenarios

```kotlin
@Test
fun `getProducts returns cached data when offline`() = runTest {
    // Pre-populate cache
    val cachedEntity = ProductEntity(id = "1", name = "Cached Product", ...)
    productDao.upsertAll(listOf(cachedEntity))

    // Simulate offline
    connectivityChecker.setOnline(false)

    val products = productRepository.observeProducts().first()
    assertThat(products).hasSize(1)
    assertThat(products[0].name).isEqualTo("Cached Product")
}

@Test
fun `getProducts throws when cache is empty and offline`() = runTest {
    connectivityChecker.setOnline(false)

    val error = assertFailsWith<Exception> {
        productRepository.refreshProducts("electronics")
    }
    assertThat(error).hasMessageThat().contains("No cached data")
}
```
