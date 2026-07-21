# Code Reviewer - Best Practices

Per-language best practices with BEFORE (bad) and AFTER (good) code examples.

---

## Python

### 1. Type Hints
```python
# BAD: No type hints
def process_order(order, user, discount):
    total = sum(item.price for item in order.items)
    return total * (1 - discount) if user.is_vip else total

# GOOD: Type hints enable static analysis and better IDE support
from decimal import Decimal
def process_order(order: Order, user: User, discount: Decimal) -> Decimal:
    total = sum((item.price for item in order.items), start=Decimal('0'))
    return total * (1 - discount) if user.is_vip else total
```

### 2. Context Managers
```python
# BAD: Manual resource management
f = open('data.json')
try:
    data = json.load(f)
finally:
    f.close()

conn = sqlite3.connect('db.sqlite')
try:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
finally:
    conn.close()

# GOOD: Context managers ensure cleanup
with open('data.json') as f:
    data = json.load(f)

with sqlite3.connect('db.sqlite') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')

# Custom context manager
from contextlib import contextmanager
@contextmanager
def timer():
    start = time.perf_counter()
    yield
    print(f'Elapsed: {time.perf_counter() - start:.2f}s')
```

### 3. List Comprehensions & Generators
```python
# BAD: Inefficient list building
squares = []
for i in range(100):
    squares.append(i * i)

filtered = []
for item in items:
    if item.active and item.price > 10:
        filtered.append(item.name)

# GOOD: List comprehensions are faster and more readable
squares = [i * i for i in range(100)]
filtered = [item.name for item in items if item.active and item.price > 10]

# BAD: Materializing full list in memory
result = [expensive_op(x) for x in huge_list]  # OOM risk

# GOOD: Generator for lazy evaluation
result = (expensive_op(x) for x in huge_list)   # Evaluated on demand
```

### 4. Async/Await Patterns
```python
# BAD: Sequential I/O
async def fetch_all(urls):
    results = []
    for url in urls:
        results.append(await fetch(url))  # One at a time
    return results

# GOOD: Concurrent I/O
async def fetch_all(urls):
    tasks = [fetch(url) for url in urls]
    return await asyncio.gather(*tasks)  # All at once

# BAD: async without timeout
async def get_data():
    return await http_client.get('https://api.example.com/data')

# GOOD: Always set timeouts
async def get_data():
    return await asyncio.wait_for(
        http_client.get('https://api.example.com/data'),
        timeout=30.0
    )
```

### 5. PEP 8 Conventions
```python
# BAD: Inconsistent spacing, long lines
def doStuff ( x,y,z ):
    return x+y+z

class user_service:
    def Get_All_Users(self): pass

# GOOD: PEP 8
def do_stuff(x: int, y: int, z: int) -> int:
    return x + y + z

class UserService:
    def get_all_users(self) -> list[User]:
        pass
```

### 6. Dataclasses & Pydantic Models
```python
# BAD: Boilerplate class
class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age
    def __repr__(self):
        return f'User(name={self.name}, email={self.email}, age={self.age})'
    def __eq__(self, other):
        return (self.name, self.email, self.age) == (other.name, other.email, other.age)

# GOOD: Dataclass eliminates boilerplate
from dataclasses import dataclass
@dataclass(frozen=True)
class User:
    name: str
    email: str
    age: int

# GOOD: Pydantic for validation at boundaries
from pydantic import BaseModel, EmailStr, Field
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)
```

---

## JavaScript / TypeScript

### 1. React Patterns — Hooks
```jsx
// BAD: Class component with lifecycle duplication
class UserProfile extends React.Component {
    componentDidMount() { this.loadUser(this.props.userId); }
    componentDidUpdate(prevProps) {
        if (prevProps.userId !== this.props.userId) this.loadUser(this.props.userId);
    }
}

// GOOD: useEffect with dependency array
function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    useEffect(() => { loadUser(userId).then(setUser); }, [userId]);
    return user ? <div>{user.name}</div> : <Spinner />;
}
```

### 2. React Patterns — Memoization
```jsx
// BAD: Unnecessary re-renders and recalculations
function ExpensiveList({ items, filter }) {
    const filtered = items.filter(item => item.category === filter);
    const sorted = filtered.sort((a, b) => a.name.localeCompare(b.name));
    return sorted.map(item => <ListItem key={item.id} item={item} />);
}

// GOOD: useMemo for expensive derivations, React.memo for components
function ExpensiveList({ items, filter }) {
    const processed = useMemo(() => {
        return items
            .filter(item => item.category === filter)
            .sort((a, b) => a.name.localeCompare(b.name));
    }, [items, filter]);
    return processed.map(item => <ListItem key={item.id} item={item} />);
}
const ListItem = React.memo(function ListItem({ item }) {
    return <div>{item.name}</div>;
});
```

### 3. Immutability
```javascript
// BAD: Mutating state
function addItem(state, item) {
    state.items.push(item);  // Mutation!
    return state;
}

// GOOD: Immutable updates
function addItem(state, item) {
    return { ...state, items: [...state.items, item] };
}

// BAD: Deep mutation
user.address.city = 'New York';

// GOOD: Immutable deep update
const updatedUser = {
    ...user,
    address: { ...user.address, city: 'New York' }
};
// Or use Immer: produce(user, draft => { draft.address.city = 'New York'; });
```

### 4. Error Boundaries
```jsx
// BAD: No error boundary — entire app crashes
function App() {
    return <ComplexWidget />;  // If this throws, whole app goes white screen
}

// GOOD: Error boundary prevents cascade failure
class ErrorBoundary extends React.Component {
    state = { hasError: false, error: null };
    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }
    componentDidCatch(error, info) {
        logError(error, info);
    }
    render() {
        if (this.state.hasError) return <ErrorFallback error={this.state.error} />;
        return this.props.children;
    }
}
function App() {
    return <ErrorBoundary><ComplexWidget /></ErrorBoundary>;
}
```

### 5. Async Patterns
```javascript
// BAD: Callback hell
function loadDashboard(userId, callback) {
    getUser(userId, (err, user) => {
        if (err) return callback(err);
        getOrders(user.id, (err, orders) => {
            if (err) return callback(err);
            getAnalytics(user.id, (err, analytics) => {
                if (err) return callback(err);
                callback(null, { user, orders, analytics });
            });
        });
    });
}

// GOOD: async/await with Promise.all for concurrency
async function loadDashboard(userId) {
    const user = await getUser(userId);
    const [orders, analytics] = await Promise.all([
        getOrders(user.id),
        getAnalytics(user.id),
    ]);
    return { user, orders, analytics };
}
```

### 6. TypeScript — Discriminated Unions
```typescript
// BAD: Ambiguous type
type Response = {
    status: string;
    data?: User[];
    error?: string;
};

// GOOD: Discriminated union
type Response =
    | { status: 'success'; data: User[] }
    | { status: 'error'; error: string }
    | { status: 'loading' };

function handleResponse(res: Response) {
    switch (res.status) {
        case 'success': return res.data.length;  // TypeScript knows data exists
        case 'error': return res.error;           // TypeScript knows error exists
        case 'loading': return '...';
    }
}
```

---

## Go

### 1. Error Handling
```go
// BAD: Ignoring errors
func ReadConfig(path string) *Config {
    data, _ := os.ReadFile(path)  // Error silently ignored
    var cfg Config
    json.Unmarshal(data, &cfg)    // Error silently ignored
    return &cfg
}

// GOOD: Explicit error handling with context
func ReadConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("reading config %s: %w", path, err)
    }
    var cfg Config
    if err := json.Unmarshal(data, &cfg); err != nil {
        return nil, fmt.Errorf("parsing config %s: %w", path, err)
    }
    return &cfg, nil
}
```

### 2. Defer Patterns
```go
// BAD: Manual cleanup — error-prone
func ProcessFile(name string) error {
    f, err := os.Open(name)
    if err != nil {
        return err
    }
    data, err := io.ReadAll(f)
    f.Close()  // What if io.ReadAll fails? File leaks.
    if err != nil {
        return err
    }
    return handle(data)
}

// GOOD: defer ensures cleanup
func ProcessFile(name string) (err error) {
    f, err := os.Open(name)
    if err != nil {
        return err
    }
    defer f.Close()
    data, err := io.ReadAll(f)
    if err != nil {
        return err
    }
    return handle(data)
}
```

### 3. Interface Segregation
```go
// BAD: Fat interface
type UserRepository interface {
    Create(user User) error
    GetByID(id string) (*User, error)
    Update(user User) error
    Delete(id string) error
    List(page, limit int) ([]User, error)
    Search(query string) ([]User, error)
    Export(format string) ([]byte, error)
}

// GOOD: Small, focused interfaces
type UserReader interface {
    GetByID(id string) (*User, error)
}
type UserWriter interface {
    Create(user User) error
    Update(user User) error
}
type UserRepository interface {
    UserReader
    UserWriter
    Delete(id string) error
}
```

### 4. Goroutine Lifecycle
```go
// BAD: Leaked goroutine — no way to stop
func StartWorker() {
    go func() {
        for {
            data := fetchData()
            process(data)
            time.Sleep(5 * time.Second)
        }
    }()
}

// GOOD: Context-based cancellation
func StartWorker(ctx context.Context) {
    go func() {
        ticker := time.NewTicker(5 * time.Second)
        defer ticker.Stop()
        for {
            select {
            case <-ctx.Done():
                log.Println("worker shutting down:", ctx.Err())
                return
            case <-ticker.C:
                data, err := fetchDataWithContext(ctx)
                if err != nil {
                    continue
                }
                process(data)
            }
        }
    }()
}
```

### 5. Zero Value & Constructors
```go
// BAD: Partial initialization
type Server struct {
    Addr    string
    Timeout time.Duration
    MaxConn int
}
s := Server{Addr: ":8080"}  // Timeout is 0, MaxConn is 0 — dangerous defaults

// GOOD: Constructor with sensible defaults
func NewServer(addr string) *Server {
    return &Server{
        Addr:    addr,
        Timeout: 30 * time.Second,
        MaxConn: 1000,
    }
}
```

---

## Java

### 1. SOLID — Single Responsibility
```java
// BAD: Class does too much
public class OrderProcessor {
    public void process(Order order) {
        validate(order);
        calculateTotal(order);
        saveToDatabase(order);
        sendConfirmationEmail(order);
        logAudit(order);
    }
}

// GOOD: Single responsibility per class
public class OrderProcessor {
    private final OrderValidator validator;
    private final OrderRepository repository;
    private final EmailService emailService;
    private final AuditLogger auditLogger;

    public void process(Order order) {
        validator.validate(order);
        order.calculateTotal();
        repository.save(order);
        emailService.sendConfirmation(order);
        auditLogger.log(order);
    }
}
```

### 2. Exception Handling
```java
// BAD: Catching generic exception, swallowing
try {
    processPayment(payment);
} catch (Exception e) {
    // Silent failure — no one knows payment failed
}

// GOOD: Specific exceptions, proper handling
try {
    processPayment(payment);
} catch (PaymentDeclinedException e) {
    payment.setStatus(Status.DECLINED);
    notificationService.notifyUser(payment.getUserId(), e.getMessage());
} catch (PaymentGatewayException e) {
    payment.setStatus(Status.RETRY);
    retryQueue.enqueue(payment);
    logger.error("Gateway error for payment {}", payment.getId(), e);
}
```

### 3. Streams API
```java
// BAD: Imperative loops
public List<String> getActiveAdminEmails() {
    List<String> emails = new ArrayList<>();
    for (User user : users) {
        if (user.isActive() && user.getRole() == Role.ADMIN) {
            emails.add(user.getEmail());
        }
    }
    return emails;
}

// GOOD: Declarative streams
public List<String> getActiveAdminEmails() {
    return users.stream()
        .filter(User::isActive)
        .filter(user -> user.getRole() == Role.ADMIN)
        .map(User::getEmail)
        .toList();  // Java 16+ — immutable
}
```

### 4. Immutability
```java
// BAD: Mutable, no encapsulation
public class User {
    public String name;
    public String email;
    public List<Order> orders = new ArrayList<>();
}

// GOOD: Immutable with builder
public final class User {
    private final String name;
    private final String email;
    private final List<Order> orders;

    private User(Builder builder) {
        this.name = builder.name;
        this.email = builder.email;
        this.orders = List.copyOf(builder.orders);  // Defensive copy
    }

    public String getName() { return name; }
    public String getEmail() { return email; }
    public List<Order> getOrders() { return orders; }  // Already immutable via List.copyOf

    public static class Builder {
        private String name;
        private String email;
        private List<Order> orders = List.of();
        public Builder name(String name) { this.name = name; return this; }
        public Builder email(String email) { this.email = email; return this; }
        public Builder orders(List<Order> orders) { this.orders = orders; return this; }
        public User build() {
            Objects.requireNonNull(name, "name");
            Objects.requireNonNull(email, "email");
            return new User(this);
        }
    }
}
```

### 5. Optional — Avoid Null
```java
// BAD: Null checks everywhere
public String getUserCity(String userId) {
    User user = userRepository.findById(userId);
    if (user != null) {
        Address address = user.getAddress();
        if (address != null) {
            return address.getCity();
        }
    }
    return "Unknown";
}

// GOOD: Optional for chain
public String getUserCity(String userId) {
    return userRepository.findById(userId)
        .map(User::getAddress)
        .map(Address::getCity)
        .orElse("Unknown");
}
```

### 6. Try-with-Resources
```java
// BAD: Manual resource management
public String readFile(String path) throws IOException {
    BufferedReader reader = new BufferedReader(new FileReader(path));
    try {
        return reader.lines().collect(Collectors.joining("\n"));
    } finally {
        reader.close();  // What if this throws?
    }
}

// GOOD: Try-with-resources (AutoCloseable)
public String readFile(String path) throws IOException {
    try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
        return reader.lines().collect(Collectors.joining("\n"));
    }
}
```

---

## Cross-Language Patterns

### All Languages — Early Returns
```python
# BAD: Deep nesting
def validate(data):
    if data is not None:
        if data.get('name'):
            if len(data['name']) > 0:
                return True
    return False

# GOOD: Early returns (guard clauses)
def validate(data):
    if data is None:
        return False
    if not data.get('name'):
        return False
    return len(data['name']) > 0
```

### All Languages — Constant Extraction
```javascript
// BAD: Magic values
if (response.status === 429) { /* ... */ }
setTimeout(retry, 5000);

// GOOD: Named constants
const TOO_MANY_REQUESTS = 429;
const RETRY_DELAY_MS = 5_000;
if (response.status === TOO_MANY_REQUESTS) { /* ... */ }
setTimeout(retry, RETRY_DELAY_MS);
```

### All Languages — Dependency Injection
```java
// BAD: Hardcoded dependency
public class OrderService {
    private final PaymentGateway gateway = new StripeGateway("sk_live_xxx");  // Hardcoded!
}

// GOOD: Injected dependency
public class OrderService {
    private final PaymentGateway gateway;
    public OrderService(PaymentGateway gateway) {  // Inject
        this.gateway = gateway;
    }
}
```
