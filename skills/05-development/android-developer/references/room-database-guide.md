# Room Database Guide — Android Developer Reference

> **Parent skill:** [android-developer](../SKILL.md) | **Load condition:** When defining Room entities, DAOs, or database migrations

## Entity Definition

```kotlin
@Entity(
    tableName = "users",
    indices = [
        Index(value = ["email"], unique = true),
        Index(value = ["team_id"]),  // Foreign key columns always indexed
    ],
    foreignKeys = [ForeignKey(
        entity = TeamEntity::class,
        parentColumns = ["id"],
        childColumns = ["team_id"],
        onDelete = ForeignKey.CASCADE,
    )],
)
data class UserEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "display_name") val displayName: String,
    @ColumnInfo(name = "email") val email: String,
    @ColumnInfo(name = "team_id") val teamId: String,
    @ColumnInfo(name = "avatar_url") val avatarUrl: String = "",
    @ColumnInfo(name = "created_at", defaultValue = "CURRENT_TIMESTAMP") val createdAt: Long = 0,
)
```

### Embedded Types & @Relation

```kotlin
// Embedded: flatten fields into parent table columns
data class Address(
    val street: String,
    val city: String,
    val zipCode: String,
)

@Entity(tableName = "profiles")
data class ProfileEntity(
    @PrimaryKey val userId: String,
    @Embedded val address: Address,  // Flattens to street, city, zipCode columns
)

// @Relation: define one-to-many / one-to-one relationships for query results
data class TeamWithUsers(
    @Embedded val team: TeamEntity,
    @Relation(parentColumn = "id", entityColumn = "team_id")
    val users: List<UserEntity>,
)

data class UserWithProfile(
    @Embedded val user: UserEntity,
    @Relation(parentColumn = "id", entityColumn = "userId")
    val profile: ProfileEntity?,
)
```

## Type Converters

```kotlin
class Converters {
    @TypeConverter
    fun fromTimestamp(value: Long?): Date? = value?.let { Date(it) }

    @TypeConverter
    fun dateToTimestamp(date: Date?): Long? = date?.time

    @TypeConverter
    fun fromStringList(value: String): List<String> = Gson().fromJson(value, object : TypeToken<List<String>>() {}.type)

    @TypeConverter
    fun stringListToString(list: List<String>): String = Gson().toJson(list)

    @TypeConverter
    fun fromEnumToString(status: OrderStatus): String = status.name

    @TypeConverter
    fun stringToEnum(value: String): OrderStatus = OrderStatus.valueOf(value)
}

@Database(entities = [UserEntity::class], version = 1, exportSchema = true)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() { /* ... */ }
```

## DAO Patterns

```kotlin
@Dao
interface UserDao {
    // Observable Flow — emits on every table change (INSERT/UPDATE/DELETE)
    @Query("SELECT * FROM users WHERE team_id = :teamId ORDER BY created_at DESC")
    fun getUsersByTeam(teamId: String): Flow<List<UserEntity>>

    // One-shot suspend call — no observation needed
    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUserById(userId: String): UserEntity?

    // @Transaction for multi-table consistency
    @Transaction
    @Query("SELECT * FROM teams WHERE id = :teamId")
    fun getTeamWithUsers(teamId: String): Flow<TeamWithUsers>

    // @Upsert (Room 2.5+) — INSERT or REPLACE
    @Upsert
    suspend fun upsertUsers(users: List<UserEntity>)

    // @Insert with conflict strategy
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrReplace(user: UserEntity): Long

    // @Delete by entity — uses primary key
    @Delete
    suspend fun deleteUser(user: UserEntity): Int

    // Raw @Query delete with return count
    @Query("DELETE FROM users WHERE team_id = :teamId")
    suspend fun deleteUsersByTeam(teamId: String): Int

    // Paging 3 — PagingSource for paginated lists
    @Query("SELECT * FROM users WHERE team_id = :teamId ORDER BY created_at DESC")
    fun getPagedUsers(teamId: String): PagingSource<Int, UserEntity>

    // Multi-table JOIN with custom return type
    @Query("""
        SELECT u.id, u.display_name, u.email, t.name AS team_name
        FROM users u INNER JOIN teams t ON u.team_id = t.id
        WHERE u.team_id = :teamId
    """)
    fun getUsersWithTeamName(teamId: String): Flow<List<UserWithTeamName>>
}
```

## Database Class Setup

```kotlin
@Database(
    entities = [UserEntity::class, TeamEntity::class, ProfileEntity::class],
    version = 3,
    exportSchema = true,  // Schema JSON in VCS for migration tests
    autoMigrations = [
        AutoMigration(from = 1, to = 2),
        AutoMigration(from = 2, to = 3, spec = AppDatabase.Migration2To3::class),
    ],
)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    abstract fun teamDao(): TeamDao

    companion object {
        @Volatile private var INSTANCE: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                INSTANCE ?: Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "app_database.db",
                )
                    .addCallback(DatabaseCallback())
                    .addMigrations(MIGRATION_2_3)
                    .build()
                    .also { INSTANCE = it }
            }
        }
    }
}
```

## Migration Strategy

```kotlin
// Manual migration
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE users ADD COLUMN avatar_url TEXT NOT NULL DEFAULT ''")
        db.execSQL("CREATE INDEX IF NOT EXISTS index_users_team_id ON users(team_id)")
    }
}

val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("""
            CREATE TABLE IF NOT EXISTS profiles (
                userId TEXT PRIMARY KEY NOT NULL,
                street TEXT NOT NULL DEFAULT '',
                city TEXT NOT NULL DEFAULT '',
                zipCode TEXT NOT NULL DEFAULT '',
                FOREIGN KEY(userId) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
    }
}

// AutoMigration with manual spec for non-trivial changes
@Database(
    autoMigrations = [
        AutoMigration(from = 2, to = 3, spec = AppDatabase.Migration2To3::class)
    ],
    /* ... */
)
abstract class AppDatabase : RoomDatabase() {
    @RenameColumn(tableName = "users", fromColumnName = "name", toColumnName = "display_name")
    class Migration2To3 : AutoMigrationSpec
}

// Destructive fallback (development only — NEVER in production)
// .fallbackToDestructiveMigration()
```

## Full-Text Search (FTS)

```kotlin
@Fts4(contentEntity = ProductEntity::class)
@Entity(tableName = "products_fts")
data class ProductFts(
    @ColumnInfo(name = "name") val name: String,
    @ColumnInfo(name = "description") val description: String,
)

@Dao
interface ProductDao {
    @Query("SELECT * FROM products WHERE products.id IN (SELECT rowid FROM products_fts WHERE products_fts MATCH :query)")
    fun searchProducts(query: String): Flow<List<ProductEntity>>
}
```

## Database Views

```kotlin
@DatabaseView(
    "SELECT users.id, users.display_name, COUNT(orders.id) AS order_count " +
    "FROM users LEFT JOIN orders ON users.id = orders.user_id " +
    "GROUP BY users.id",
    viewName = "user_order_summary",
)
data class UserOrderSummary(
    val id: String,
    val displayName: String,
    val orderCount: Int,
)

@Database(
    entities = [UserEntity::class, OrderEntity::class],
    views = [UserOrderSummary::class],
    version = 1,
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userOrderDao(): UserOrderSummaryDao
}

@Dao
interface UserOrderSummaryDao {
    @Query("SELECT * FROM user_order_summary ORDER BY order_count DESC")
    fun getTopUsers(): Flow<List<UserOrderSummary>>
}
```

## Testing DAOs

```kotlin
@RunWith(AndroidJUnit4::class)
class UserDaoTest {
    private lateinit var db: AppDatabase
    private lateinit var dao: UserDao

    @Before fun createDb() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        db = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java).build()
        dao = db.userDao()
    }

    @After fun closeDb() { db.close() }

    @Test fun `insert then retrieve by ID`() = runTest {
        val user = UserEntity("1", "Test User", "test@test.com", "t1")
        dao.upsertUsers(listOf(user))
        val result = dao.getUserById("1")
        assertThat(result?.displayName).isEqualTo("Test User")
    }

    @Test fun `upsert replaces existing`() = runTest {
        dao.upsertUsers(listOf(UserEntity("1", "Old", "old@test.com", "t1")))
        dao.upsertUsers(listOf(UserEntity("1", "New", "new@test.com", "t1")))
        assertThat(dao.getUserById("1")?.displayName).isEqualTo("New")
    }

    @Test fun `Flow emits updated values on insert`() = runTest {
        val users = dao.getUsersByTeam("t1")
        dao.upsertUsers(listOf(UserEntity("1", "Test", "test@test.com", "t1")))
        assertThat(users.first()).hasSize(1)
    }
}
```

## Testing Migrations

```kotlin
@RunWith(AndroidJUnit4::class)
class MigrationTest {
    @get:Rule val helper = MigrationTestHelper(
        InstrumentationRegistry.getInstrumentation(),
        AppDatabase::class.java,
    )

    @Test fun `migrate from 1 to 3`() {
        // Create DB at v1 with known data
        val db = helper.createDatabase(TEST_DB_NAME, 1).apply {
            execSQL("INSERT INTO users (id, name, email, team_id) VALUES ('1', 'Old', 'old@test.com', 't1')")
            close()
        }

        // Run migrations to v3
        val migrated = helper.runMigrationsAndValidate(TEST_DB_NAME, 3, true, MIGRATION_1_2, MIGRATION_2_3)

        // Verify data survived
        migrated.query("SELECT * FROM users WHERE id = '1'").use { cursor ->
            assertThat(cursor.moveToFirst()).isTrue()
            assertThat(cursor.getString(cursor.getColumnIndexOrThrow("display_name"))).isEqualTo("Old")
        }
        migrated.close()
    }
}
```

## Pre-Packaged Database

```kotlin
// Ship a pre-populated .db file in assets/databases/
Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
    .createFromAsset("databases/prepopulated.db")
    .build()

// Or from file:
Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
    .createFromFile(File("/path/to/prepopulated.db"))
    .build()

// WARNING: createFromAsset skips onCreate() callback. Use addCallback() for any post-creation logic.
```

## Database Callbacks

```kotlin
class DatabaseCallback : RoomDatabase.Callback() {
    override fun onCreate(db: SupportSQLiteDatabase) {
        super.onCreate(db)
        // Populate defaults (only runs on brand-new installs)
        CoroutineScope(Dispatchers.IO).launch {
            // Insert seed data through DAO
        }
    }

    override fun onOpen(db: SupportSQLiteDatabase) {
        super.onOpen(db)
        // Enable WAL mode for concurrent reads (set only once)
        db.execSQL("PRAGMA journal_mode=WAL")
        db.execSQL("PRAGMA foreign_keys=ON")
    }

    override fun onDestructiveMigration(db: SupportSQLiteDatabase) {
        super.onDestructiveMigration(db)
        // Log to Crashlytics — this should never happen in production
    }
}
```
