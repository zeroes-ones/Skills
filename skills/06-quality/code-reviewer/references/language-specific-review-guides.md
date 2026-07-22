---
name: language-specific-review-guides
description: Anti-pattern detection with before/after code examples for Python, TypeScript, Go, and Rust code reviews. Covers mutable defaults, any vs unknown, goroutine leaks, unsafe blocks, and more.
author: Sandeep Kumar Penchala
---

# Language-Specific Code Review Guides

Definitive anti-pattern reference for code reviews across four languages. Each section identifies common pitfalls with detection patterns, before/after fix examples, and severity grading. Use this as a companion to the Code Reviewer skill.

---

## Python

### 1. Mutable Default Arguments

**Detection:** `grep -rn "def .*=[\s]*\[" --include="*.py" | grep -v "None\|Optional"`

**Before (Vulnerable):**
```python
# BUG: Default list is created ONCE at function definition time.
# All calls share the same list object.
def add_item(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items

add_item("a")  # Returns ["a"]
add_item("b")  # Returns ["a", "b"] — shares the mutated list!
```

**After (Fixed):**
```python
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items

add_item("a")  # Returns ["a"]
add_item("b")  # Returns ["b"] — correct independent lists
```

**Severity:** High. Causes subtle, hard-to-diagnose bugs in multi-call scenarios.

---

### 2. Bare Except Clauses

**Detection:** `grep -rn "except:" --include="*.py" | grep -v "except ([A-Z]\|Exception\|ValueError"`

**Before (Vulnerable):**
```python
try:
    result = process_data(file_path)
except:  # Catches EVERYTHING: KeyboardInterrupt, SystemExit, MemoryError
    logger.error("Processing failed")  # Swallows critical signals!
```

**After (Fixed):**
```python
try:
    result = process_data(file_path)
except FileNotFoundError:
    logger.warning("File not found: %s", file_path)
    raise  # Re-raise if caller should handle it
except (ValueError, TypeError) as e:
    logger.error("Invalid data: %s", e)
    raise ProcessingError(f"Failed to process {file_path}") from e
# SystemExit and KeyboardInterrupt pass through — correctly
```

**Severity:** Critical. Can prevent graceful shutdown and mask critical errors.

---

### 3. Context Manager Misuse

**Before (Vulnerable):**
```python
# Resource leak — file not guaranteed to close on error
f = open("data.json")
data = json.load(f)
f.close()  # Never reached if json.load raises!

# Manual transaction management with leak risk
conn = get_db_connection()
conn.execute("UPDATE users SET status = 'active'")
# If next line raises, transaction is never committed or rolled back!
conn.commit()
```

**After (Fixed):**
```python
# Context manager guarantees cleanup
with open("data.json") as f:
    data = json.load(f)
# File closed even if json.load raises

# Transaction context manager
from contextlib import contextmanager

@contextmanager
def transaction(conn):
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise

with transaction(get_db_connection()) as conn:
    conn.execute("UPDATE users SET status = 'active'")
```

**Severity:** High. Resource leaks under error conditions.

---

### 4. Async Patterns — Common Mistakes

**Blocking the event loop:**
```python
# Before: Blocking I/O in async context
async def fetch_data():
    data = requests.get("https://api.example.com")  # Blocking!
    return data.json()

# After: Async HTTP client
import aiohttp

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com") as resp:
            return await resp.json()
```

**Missing `asyncio.gather` (sequential where parallel is possible):**
```python
# Before: Sequential — total time = sum of all requests
async def load_dashboard(user_id):
    user = await db.fetch_user(user_id)         # 100ms
    orders = await db.fetch_orders(user_id)     # 200ms
    notifications = await db.fetch_notifs(user_id)  # 150ms
    return user, orders, notifications          # Total: 450ms

# After: Concurrent — total time = max of all requests
async def load_dashboard(user_id):
    user, orders, notifications = await asyncio.gather(
        db.fetch_user(user_id),
        db.fetch_orders(user_id),
        db.fetch_notifications(user_id),
    )
    return user, orders, notifications          # Total: 200ms
```

**Severity:** Medium (sequential issue) / High (blocking event loop).

---

### 5. Type Hints — Common Gaps

**Before:**
```python
# Vague types
def process(items):  # No type annotation
    ...

def get_user(user_id) -> dict:  # dict is too vague
    ...

def handle(data: dict[str, Any]) -> None:  # Any defeats the purpose
    ...
```

**After:**
```python
from typing import TypedDict, Literal, Protocol

class User(TypedDict):
    id: str
    email: str
    role: Literal["admin", "editor", "viewer"]

def process(items: list[str]) -> None: ...

def get_user(user_id: str) -> User | None: ...

# Use Protocol for duck typing
class HasId(Protocol):
    id: str

def delete(entity: HasId) -> None: ...

# Use Final for constants, TypeGuard for type narrowing
```

**Severity:** Low (code quality, not bug-causing) but accumulates tech debt.

---

## TypeScript

### 1. `any` vs `unknown`

**Detection:** `grep -rn ": any\b\|as any\|<any>" --include="*.ts" --include="*.tsx"`

**Before (Vulnerable):**
```typescript
// any — completely disables type checking
function parseJSON(json: string): any {
    return JSON.parse(json);
}

const data = parseJSON(userInput);
data.nonExistent.method(); // No type error! Runtime crash!
```

**After (Fixed):**
```typescript
// unknown — forces validation before use
function parseJSON(json: string): unknown {
    return JSON.parse(json);
}

const raw = parseJSON(userInput);
// raw.method() — TypeScript error! Must narrow first.

if (typeof raw === 'object' && raw !== null && 'name' in raw) {
    // Type narrowed — safe to use
    console.log((raw as { name: string }).name);
}

// Better: use Zod for full validation
import { z } from 'zod';

const UserSchema = z.object({
    name: z.string(),
    email: z.string().email(),
});

function parseUser(json: string) {
    const raw: unknown = JSON.parse(json);
    return UserSchema.parse(raw); // Returns typed User or throws
}
```

**Severity:** Medium. `any` breaks the type system; `unknown` preserves safety.

---

### 2. Missing Discriminated Unions

**Before (messy):**
```typescript
type ApiState = {
    loading: boolean;
    data?: Data;
    error?: Error;
};

function render(state: ApiState) {
    if (state.loading) return <Spinner />;
    if (state.error) return <ErrorBanner error={state.error} />;
    // TypeScript doesn't know data is definitely defined here!
    return <DataView data={state.data!} />; // Non-null assertion — unsafe
}
```

**After (Discriminated Union):**
```typescript
type ApiState =
    | { status: 'idle' }
    | { status: 'loading' }
    | { status: 'success'; data: Data }
    | { status: 'error'; error: Error };

function render(state: ApiState) {
    switch (state.status) {
        case 'idle': return <EmptyState />;
        case 'loading': return <Spinner />;
        case 'success': return <DataView data={state.data} />; // data is guaranteed
        case 'error': return <ErrorBanner error={state.error} />; // error guaranteed
    }
    // Exhaustiveness check — TypeScript errors if we miss a case
    const _exhaustive: never = state;
}
```

**Severity:** Medium. Improves readability, eliminates runtime errors.

---

### 3. Null Checks & Optional Chaining

**Before:**
```typescript
// Deeply nested null checks
const city = user && user.address && user.address.city;

// Non-null assertion — risky!
const city = user!.address!.city!;

// Optional chaining done wrong
const city = user?.address.city; // Only user is guarded. If user exists but address doesn't, crash!
```

**After:**
```typescript
// Optional chaining — stops at first null/undefined
const city = user?.address?.city; // Safe: returns undefined if any link is missing

// Nullish coalescing for defaults
const cityName = user?.address?.city ?? 'Unknown';

// Pattern: early return with explicit null check
function getCity(user: User | null): string {
    if (!user?.address?.city) {
        throw new NotFoundError('City not available');
    }
    return user.address.city; // Type narrowed to string
}
```

**Severity:** High (non-null assertions in particular — runtime crashes).

---

### 4. Immutability Violations

**Before:**
```typescript
// Mutating function parameters
function addItem(cart: CartItem[], item: CartItem) {
    cart.push(item); // Mutates the caller's array!
    return cart;
}

// Mutating React state directly
function handleUpdate(user: User) {
    user.name = "New Name"; // Mutates state — won't trigger re-render
    setUser(user);
}
```

**After:**
```typescript
// Immutable update
function addItem(cart: readonly CartItem[], item: CartItem): CartItem[] {
    return [...cart, item];
}

// React: always create new objects
function handleUpdate(prevUser: User) {
    setUser({ ...prevUser, name: "New Name" });
}

// TypeScript utilities for immutability
type DeepReadonly<T> = { readonly [K in keyof T]: DeepReadonly<T[K]> };

function freeze<T>(obj: T): DeepReadonly<T> {
    return obj as DeepReadonly<T>;
}
```

**Severity:** Medium (bugs) / High (React — silent failures).

---

### 5. Effect Typing (Promise Handling)

**Before:**
```typescript
// Floating promise — unhandled
async function saveData() {
    db.save(data); // Returns Promise<void>, but not awaited!
    return "done"; // Returns BEFORE save completes
}

// Mixing async/callback patterns
async function init() {
    server.on('request', async (req) => {
        await handle(req); // Uncaught errors in async callback!
    });
}

// forEach with async — doesn't await!
[1, 2, 3].forEach(async (id) => {
    await processItem(id); // Runs in parallel, errors swallowed!
});
```

**After:**
```typescript
// Explicit promise handling
async function saveData() {
    await db.save(data); // Awaited
    return "done";
}

// Use Promise.all for parallel async
await Promise.all([1, 2, 3].map(id => processItem(id)));

// TypeScript's no-floating-promises rule (ESLint)
// @typescript-eslint/no-floating-promises: error

// void operator to explicitly ignore (with comment)
void db.audit('user_action'); // Fire-and-forget, intentional
```

**Severity:** High. Floating promises lead to unhandled rejections and data loss.

---

## Go

### 1. Error Handling Anti-patterns

**Before (Vulnerable):**
```go
// Swallowing errors
data, _ := ioutil.ReadFile("config.json")  // _ discards error!

// Generic error without context
if err != nil {
    return err  // Which operation failed? What input?
}

// Error in defer without checking
defer file.Close()  // Error from Close is silently ignored!
```

**After (Fixed):**
```go
// Always handle errors
data, err := os.ReadFile("config.json")
if err != nil {
    return fmt.Errorf("reading config file: %w", err)  // Wrap with context
}

// Error wrapping for debugging
if err != nil {
    return fmt.Errorf("fetching user %s from org %s: %w", userID, orgID, err)
}

// Named return for defer error handling
func processFile(path string) (err error) {
    f, err := os.Open(path)
    if err != nil {
        return fmt.Errorf("opening %s: %w", path, err)
    }
    defer func() {
        if closeErr := f.Close(); closeErr != nil && err == nil {
            err = fmt.Errorf("closing %s: %w", path, closeErr)
        }
    }()
    // ... use f
    return nil
}
```

**Severity:** High. Swallowed errors cause silent failures and data corruption.

---

### 2. Goroutine Leaks

**Detection:** Look for goroutines without context cancellation or done channels.

**Before (Leak):**
```go
func processItems(items []Item) {
    ch := make(chan Result)
    for _, item := range items {
        go func(item Item) {
            result, err := expensiveOperation(item)
            ch <- result  // BLOCKS FOREVER if no one reads!
        }(item)
    }
    // Only reads first result, then returns → 9 goroutines leaked
    first := <-ch
    fmt.Println(first)
}
```

**After (Fixed):**
```go
func processItems(ctx context.Context, items []Item) ([]Result, error) {
    ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
    defer cancel()

    results := make(chan Result, len(items))  // Buffered — no blocking
    errs := make(chan error, 1)

    g, ctx := errgroup.WithContext(ctx)
    for _, item := range items {
        item := item
        g.Go(func() error {
            result, err := expensiveOperation(ctx, item)
            if err != nil {
                return err
            }
            results <- result
            return nil
        })
    }

    // Close results when all goroutines finish
    go func() {
        g.Wait()
        close(results)
    }()

    if err := g.Wait(); err != nil {
        return nil, err
    }

    var all []Result
    for r := range results {
        all = append(all, r)
    }
    return all, nil
}
```

**Severity:** Critical. Goroutine leaks accumulate over time, eventually crashing the process with OOM.

---

### 3. Interface Pollution

**Before (Over-abstracted):**
```go
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*User, error)
    FindByEmail(ctx context.Context, email string) (*User, error)
    Create(ctx context.Context, user *User) error
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id string) error
    // 15 more methods...
}

type PostgresUserRepository struct {
    db *sql.DB
}

// 20 methods implemented... for ONE implementation.

// Consumer forced to depend on huge interface
func NewUserService(repo UserRepository) *UserService { ... }
```

**After (Interface Segregation):**
```go
// Small, focused interfaces — define where consumed
type UserFinder interface {
    FindByID(ctx context.Context, id string) (*User, error)
}

type UserCreator interface {
    Create(ctx context.Context, user *User) error
}

// Consumer defines what it needs — minimal interface
type Authenticator struct {
    finder UserFinder  // Only FindByID
}

func NewAuthenticator(finder UserFinder) *Authenticator {
    return &Authenticator{finder: finder}
}

// Implementor doesn't even need to know about the interface
func (r *PostgresStore) FindByID(ctx context.Context, id string) (*User, error) {
    // ...
}
```

**Severity:** Low (maintainability). Large interfaces make testing and refactoring painful.

---

### 4. Nil vs Empty Slice

**Before:**
```go
func getUsers() []User {
    // nil slice — len() == 0 but serializes as `null` in JSON
    return nil
}

func getOrders() []Order {
    // empty slice — len() == 0 but serializes as `[]` in JSON
    return []Order{}
}
```

**After (Intentional choice):**
```go
// API responses: prefer empty slice (clients expect array, not null)
func getUsers() []User {
    users, err := db.QueryUsers()
    if err != nil || len(users) == 0 {
        return []User{}  // JSON: [] — consistent array type
    }
    return users
}

// Internal: nil is fine as "no results" sentinel
func (s *Store) findOptional(key string) []string {
    return s.cache[key]  // nil if not found — callers check len()
}
```

**Severity:** Medium. Nil vs empty causes subtle JSON serialization bugs in APIs.

---

## Rust

### 1. Unsafe Block Abuse

**Before (Red flag):**
```rust
// unsafe for performance without proof of safety
pub fn sort_in_place<T: Ord>(data: &mut [T]) {
    unsafe {
        // Custom sort using raw pointer manipulation
        let ptr = data.as_mut_ptr();
        let len = data.len();
        // ... custom unsafe logic ...
    }
}

// FFI without safety abstraction
pub fn get_username(user_id: u32) -> String {
    unsafe {
        let ptr = ffi_get_username(user_id); // Raw pointer from C
        CStr::from_ptr(ptr).to_string_lossy().into_owned()
        // Who frees ptr? Is it valid? What about null?
    }
}
```

**After (Safe abstraction):**
```rust
// Use standard library — already optimized and safe
pub fn sort_in_place<T: Ord>(data: &mut [T]) {
    data.sort(); // Safe, optimized, maintained by Rust team
}

// FFI safety wrapper — unsafe block is minimal and proven
pub fn get_username(user_id: u32) -> Result<String, Error> {
    // SAFETY: ffi_get_username returns a null-terminated C string
    // allocated by the library. The caller must NOT free it.
    // Returns null if user_id is invalid.
    let ptr = unsafe { ffi_get_username(user_id) };
    if ptr.is_null() {
        return Err(Error::UserNotFound(user_id));
    }
    // SAFETY: ptr is non-null and points to a valid null-terminated C string.
    let c_str = unsafe { CStr::from_ptr(ptr) };
    Ok(c_str.to_string_lossy().into_owned())
}
```

**Severity:** Critical. Unsafe blocks must have explicit safety comments (SAFETY: ...).

---

### 2. Panic vs Result

**Before:**
```rust
// Library code panicking — crashes the entire program
pub fn parse_config(path: &str) -> Config {
    let content = std::fs::read_to_string(path)
        .expect("Failed to read config file"); // Panics!
    serde_json::from_str(&content)
        .expect("Invalid config JSON") // Panics!
}

// Indexing that can panic
fn get_item(items: &[Item], index: usize) -> &Item {
    &items[index] // Panics if index >= len!
}
```

**After:**
```rust
// Return Result — caller decides how to handle failure
pub fn parse_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(|e| ConfigError::ReadFailed(path.to_string(), e))?;
    let config = serde_json::from_str(&content)
        .map_err(|e| ConfigError::InvalidJson(e))?;
    Ok(config)
}

// Safe indexing with Option
fn get_item(items: &[Item], index: usize) -> Option<&Item> {
    items.get(index) // Returns None instead of panicking
}
```

**Severity:** High. Panics in library code prevent callers from recovering.

---

### 3. Clone Optimization

**Before (Inefficient):**
```rust
// Clone-heavy code — often unnecessary
fn process_data(data: &Data) -> Data {
    let mut processed = data.clone(); // Full clone
    processed.field = compute_new_value(data.clone()); // Another clone?
    processed
}

// Cloning in loops
for item in items.clone() { // Clones entire Vec
    process(item.clone()); // Clones each item
}
```

**After (Borrow-aware):**
```rust
// Borrow when possible
fn process_data(data: &Data) -> Data {
    Data {
        field: compute_new_value(data), // Uses reference, no clone
        ..data.clone() // Clone only the remaining fields
    }
}

// Iterate by reference
for item in &items {
    process(&item); // No clones
}

// Take ownership when consuming
fn consume_and_transform(items: Vec<Item>) -> Vec<Transformed> {
    items.into_iter().map(|item| transform(item)).collect()
}
```

**Severity:** Medium (performance).

---

### 4. Lifetime Annotation Confusion

**Before (Over-specified):**
```rust
// Lifetime annotations where elision would suffice
fn first_word<'a>(s: &'a str) -> &'a str {
    s.split_whitespace().next().unwrap_or("")
}

// Wrong lifetime leading to borrow issues
struct Container<'a> {
    data: &'a str,
    cache: RefCell<HashMap<String, &'a str>>, // Borrow checker nightmare
}
```

**After (Elision + Ownership):**
```rust
// Rust elides single-input lifetimes automatically
fn first_word(s: &str) -> &str {
    s.split_whitespace().next().unwrap_or("")
}

// Own data when possible — avoid lifetime plumbing
struct Container {
    data: String,  // Owned — no lifetime annotation needed
    cache: RefCell<HashMap<String, usize>>, // Store indices, not references
}
```

**Severity:** Low (ergonomics). Prefer ownership over complex lifetime annotations.

---

## References
- [Effective Python (2nd Edition)](https://effectivepython.com/) — Brett Slatkin
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/) — Basarat Ali Syed
- [Effective Go](https://go.dev/doc/effective_go)
- [The Rust Book](https://doc.rust-lang.org/book/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Common Rust Lifetime Misconceptions](https://github.com/pretzelhammer/rust-blog/blob/master/posts/common-rust-lifetime-misconceptions.md)
