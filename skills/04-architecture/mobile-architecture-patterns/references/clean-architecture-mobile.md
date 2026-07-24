# Clean Architecture on Mobile — Reference Implementation

> Complete Clean Architecture implementation for iOS and Android with multi-module structure, dependency inversion, and platform-agnostic domain logic.

---

## Layer Dependency Rule

```
┌──────────────────────────────────────────────────────────────┐
│ PRESENTATION LAYER                                           │
│ iOS: SwiftUI Views + ViewModels (Swift, imports SwiftUI)     │
│ Android: Compose Screens + ViewModels (Kotlin, imports Compose)│
├──────────────────────────────────────────────────────────────┤
│ DOMAIN LAYER (Pure, no platform imports)                     │
│ Entities, UseCases, Repository Interfaces                    │
│ ZERO dependencies on UIKit, SwiftUI, Android SDK             │
├──────────────────────────────────────────────────────────────┤
│ DATA LAYER (Platform-specific implementations)               │
│ Repository Implementations, API Clients, Database DAOs       │
│ Implements Domain interfaces, imports platform frameworks    │
└──────────────────────────────────────────────────────────────┘

Dependencies point INWARD. Domain ← Data (via interfaces). Presentation ← Domain.
```

---

## iOS Implementation

### Domain Layer — Pure Swift

```swift
// Domain/Entities/User.swift
public struct User: Equatable, Sendable {
    public let id: String
    public let email: String
    public let displayName: String
    public let avatarURL: URL?
    public let createdAt: Date

    public init(id: String, email: String, displayName: String,
                avatarURL: URL?, createdAt: Date) {
        self.id = id
        self.email = email
        self.displayName = displayName
        self.avatarURL = avatarURL
        self.createdAt = createdAt
    }
}

// Domain/UseCases/GetUserProfileUseCase.swift
public protocol GetUserProfileUseCase {
    func execute(userId: String) async throws -> User
}

public final class GetUserProfileUseCaseImpl: GetUserProfileUseCase {
    private let repository: UserRepository

    public init(repository: UserRepository) {
        self.repository = repository
    }

    public func execute(userId: String) async throws -> User {
        guard !userId.isEmpty else {
            throw DomainError.invalidInput("User ID cannot be empty")
        }
        let user = try await repository.getUser(byId: userId)
        return user
    }
}

// Domain/Repositories/UserRepository.swift
public protocol UserRepository {
    func getUser(byId id: String) async throws -> User
    func updateUser(_ user: User) async throws -> User
    func deleteUser(id: String) async throws
}

// Domain/Errors/DomainError.swift
public enum DomainError: LocalizedError {
    case invalidInput(String)
    case notFound(String)
    case unauthorized
    case networkError(Error)

    public var errorDescription: String? {
        switch self {
        case .invalidInput(let msg): return msg
        case .notFound(let id): return "User \(id) not found"
        case .unauthorized: return "Session expired"
        case .networkError(let error): return error.localizedDescription
        }
    }
}
```

### Data Layer

```swift
// Data/Repositories/UserRepositoryImpl.swift
import Foundation

final class UserRepositoryImpl: UserRepository {
    private let remoteDataSource: UserRemoteDataSource
    private let localDataSource: UserLocalDataSource
    private let connectivityChecker: ConnectivityChecking

    init(remote: UserRemoteDataSource, local: UserLocalDataSource,
         connectivity: ConnectivityChecking) {
        self.remoteDataSource = remote
        self.localDataSource = local
        self.connectivityChecker = connectivity
    }

    func getUser(byId id: String) async throws -> User {
        if connectivityChecker.isOnline {
            do {
                let remoteDTO = try await remoteDataSource.fetchUser(id: id)
                let user = remoteDTO.toDomain()
                try? await localDataSource.saveUser(remoteDTO)
                return user
            } catch {
                // Fallback to cache on network failure
                if let cached = try? await localDataSource.getUser(id: id) {
                    return cached.toDomain()
                }
                throw DomainError.networkError(error)
            }
        }
        // Offline: read from local DB
        guard let localDTO = try? await localDataSource.getUser(id: id) else {
            throw DomainError.notFound(id)
        }
        return localDTO.toDomain()
    }

    func updateUser(_ user: User) async throws -> User {
        let remoteDTO = try await remoteDataSource.updateUser(user.toDTO())
        try? await localDataSource.saveUser(remoteDTO)
        return remoteDTO.toDomain()
    }

    func deleteUser(id: String) async throws {
        try await remoteDataSource.deleteUser(id: id)
        try? await localDataSource.deleteUser(id: id)
    }
}

// Data/DataSources/UserRemoteDataSource.swift
protocol UserRemoteDataSource {
    func fetchUser(id: String) async throws -> UserDTO
    func updateUser(_ dto: UserDTO) async throws -> UserDTO
    func deleteUser(id: String) async throws
}

struct UserDTO: Codable {
    let id: String
    let email: String
    let displayName: String
    let avatarURL: String?
    let createdAt: String // ISO 8601

    func toDomain() -> User {
        User(id: id, email: email, displayName: displayName,
             avatarURL: avatarURL.flatMap(URL.init),
             createdAt: ISO8601DateFormatter().date(from: createdAt) ?? .distantPast)
    }
}

extension User {
    func toDTO() -> UserDTO {
        UserDTO(id: id, email: email, displayName: displayName,
                avatarURL: avatarURL?.absoluteString,
                createdAt: ISO8601DateFormatter().string(from: createdAt))
    }
}
```

### Presentation Layer

```swift
// Presentation/Profile/ProfileViewModel.swift
@MainActor
final class ProfileViewModel: ObservableObject {
    @Published var userName: String = ""
    @Published var userEmail: String = ""
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?

    private let getUserProfile: GetUserProfileUseCase
    private let userId: String

    init(getUserProfile: GetUserProfileUseCase, userId: String) {
        self.getUserProfile = getUserProfile
        self.userId = userId
    }

    func loadProfile() async {
        isLoading = true
        errorMessage = nil
        do {
            let user = try await getUserProfile.execute(userId: userId)
            userName = user.displayName
            userEmail = user.email
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }
}
```

---

## Android Implementation

### Domain Layer — Pure Kotlin

```kotlin
// domain/src/main/kotlin/com/example/domain/entity/User.kt
data class User(
    val id: String,
    val email: String,
    val displayName: String,
    val avatarUrl: String?,
    val createdAt: Instant
)

// domain/src/main/kotlin/com/example/domain/usecase/GetUserProfileUseCase.kt
class GetUserProfileUseCase @Inject constructor(
    private val userRepository: UserRepository
) {
    suspend operator fun invoke(userId: String): Result<User> {
        if (userId.isBlank()) {
            return Result.failure(IllegalArgumentException("User ID required"))
        }
        return try {
            val user = userRepository.getUser(userId)
            Result.success(user)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

// domain/src/main/kotlin/com/example/domain/repository/UserRepository.kt
interface UserRepository {
    suspend fun getUser(id: String): User
    suspend fun updateUser(user: User): User
    suspend fun deleteUser(id: String)
}

// domain/src/main/kotlin/com/example/domain/error/DomainError.kt
sealed class DomainError(message: String) : Exception(message) {
    class NotFound(id: String) : DomainError("Resource $id not found")
    class Unauthorized : DomainError("Session expired")
    class NetworkError(cause: Throwable) : DomainError(cause.message ?: "Network error")
}
```

### Data Layer

```kotlin
// data/src/main/kotlin/com/example/data/repository/UserRepositoryImpl.kt
class UserRepositoryImpl @Inject constructor(
    private val remoteDataSource: UserRemoteDataSource,
    private val localDataSource: UserLocalDataSource,
    private val connectivityChecker: ConnectivityChecker
) : UserRepository {

    override suspend fun getUser(id: String): User {
        return if (connectivityChecker.isOnline()) {
            try {
                val remoteUser = remoteDataSource.fetchUser(id)
                localDataSource.saveUser(remoteUser)
                remoteUser.toDomain()
            } catch (e: Exception) {
                localDataSource.getUser(id)?.toDomain()
                    ?: throw DomainError.NetworkError(e)
            }
        } else {
            localDataSource.getUser(id)?.toDomain()
                ?: throw DomainError.NotFound(id)
        }
    }

    override suspend fun updateUser(user: User): User {
        val dto = user.toDto()
        val updated = remoteDataSource.updateUser(dto)
        localDataSource.saveUser(updated)
        return updated.toDomain()
    }

    override suspend fun deleteUser(id: String) {
        remoteDataSource.deleteUser(id)
        localDataSource.deleteUser(id)
    }
}

// data/src/main/kotlin/com/example/data/datasource/UserRemoteDataSource.kt
interface UserRemoteDataSource {
    suspend fun fetchUser(id: String): UserDto
    suspend fun updateUser(dto: UserDto): UserDto
    suspend fun deleteUser(id: String)
}

// data/src/main/kotlin/com/example/data/dto/UserDto.kt
@Entity(tableName = "users")
data class UserDto(
    @PrimaryKey val id: String,
    val email: String,
    val displayName: String,
    val avatarUrl: String?,
    val createdAt: String
)

fun UserDto.toDomain() = User(
    id = id, email = email, displayName = displayName,
    avatarUrl = avatarUrl,
    createdAt = Instant.parse(createdAt)
)

fun User.toDto() = UserDto(
    id = id, email = email, displayName = displayName,
    avatarUrl = avatarUrl,
    createdAt = createdAt.toString()
)
```

### Presentation Layer

```kotlin
// presentation/src/main/kotlin/com/example/presentation/profile/ProfileViewModel.kt
@HiltViewModel
class ProfileViewModel @Inject constructor(
    private val getUserProfile: GetUserProfileUseCase,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val userId: String = savedStateHandle["userId"]!!

    private val _uiState = MutableStateFlow(ProfileUiState())
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()

    init { loadProfile() }

    fun loadProfile() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            getUserProfile(userId)
                .onSuccess { user ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            userName = user.displayName,
                            userEmail = user.email
                        )
                    }
                }
                .onFailure { error ->
                    _uiState.update {
                        it.copy(isLoading = false, error = error.message)
                    }
                }
        }
    }
}

data class ProfileUiState(
    val userName: String = "",
    val userEmail: String = "",
    val isLoading: Boolean = false,
    val error: String? = null
)
```

---

## Multi-Module Project Structure

### iOS (SPM / Xcode Workspace)

```
MyApp/
├── Domain/                       # Swift Package, no platform deps
│   ├── Entities/
│   ├── UseCases/
│   └── RepositoryInterfaces/
├── Data/                         # Swift Package
│   ├── Repositories/
│   ├── DataSources/
│   │   ├── Remote/
│   │   └── Local/
│   └── DTOs/
├── Core/                         # Shared utilities
│   ├── DI/
│   └── Extensions/
└── Presentation/                 # App target
    ├── Screens/
    ├── ViewModels/
    └── Navigation/
```

### Android (Gradle Multi-Module)

```
app/
├── :domain                       # Pure Kotlin, no Android deps
│   └── src/main/kotlin/...
├── :data                         # Implements domain interfaces
│   ├── :data:remote              # Retrofit, OkHttp
│   └── :data:local               # Room
├── :core
│   ├── :core:di                  # Hilt modules
│   ├── :core:model               # Shared models
│   └── :core:navigation          # Navigation contracts
└── :feature
    ├── :feature:profile
    ├── :feature:settings
    └── :feature:auth
```

---

## Key Rules

1. **Domain module compiles without ANY platform dependency.** Run `swift build --target Domain` / `./gradlew :domain:compileKotlin` to verify.
2. **Data module implements Domain interfaces, never the reverse.** Domain defines the contract. Data fulfills it.
3. **DTOs never cross into Domain.** Always map DTO → Entity at the Repository boundary.
4. **UseCases are the ONLY entry point to Domain.** ViewModels never call Repositories directly.
5. **Every layer is independently testable.** Domain tests run in milliseconds (pure logic). Data tests use fakes. Presentation tests use mocked UseCases.
6. **Offline-first is built into the Repository pattern, not bolted on.** The Repository always reads cache, refreshes from network opportunistically.
