# Interface Minimization

## Philosophy

Every public method is a tax on every developer who reads the codebase. The goal of interface minimization is to reduce that tax to the absolute minimum while preserving all necessary behavior.

## Techniques

### 1. Combine Methods
**Before:** `setHost(host)`, `setPort(port)`, `setTimeout(ms)` — three methods, three learning costs.
**After:** `configure(ConnectionOptions options)` — one method, one learning cost. Callers create an options object.

### 2. Default Parameters
**Before:** `connect()`, `connect(host)`, `connect(host, port)` — three overloads.
**After:** `connect(host = "localhost", port = 8080)` — one method with defaults.

### 3. Narrow Return Types
**Before:** `getUsers(): HashMap<String, User>` — exposes implementation (HashMap).
**After:** `getUsers(): List<User>` — returns interface type. Callers don't need to know it's a HashMap.

### 4. Hide Implementation Classes
**Before:** `new SqlUserRepository(connectionString)` — caller knows about SQL.
**After:** `UserRepository.create(connectionString)` — factory method hides implementation. Caller only knows the interface.

### 5. Method Justification Checklist
For each public method, answer:
- Is it called by external production code? (Not tests, not internal callers)
- Does it represent a single, coherent operation?
- Could callers achieve the same result without this method?
- Would deleting this method break a real use case?

If the answer to question 1 is NO, make it private. If the answer to question 3 is YES, delete it.

### 6. Reduce Parameter Count
Every parameter is interface cost. If a method has >3 parameters, consider:
- Grouping related parameters into an options/config object
- Splitting the method into smaller, more focused methods
- Using the builder pattern for complex construction
