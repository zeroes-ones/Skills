# Injection Prevention — Reference

## SQL Injection — The Pattern That Must Never Appear

### Vulnerable (String Concatenation):
```python
# NEVER: string interpolation creates SQL injection
cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
cursor.execute("SELECT * FROM users WHERE name = '" + name + "'")
```

### Secure (Parameterized Queries):
```python
# ALWAYS: parameterized queries
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
```

### Dynamic Table/Column/Group BY Names (Rare Case):
```python
# Allowlist approach for truly dynamic identifiers
ALLOWED_COLUMNS = {'id', 'name', 'email', 'created_at'}
ALLOWED_DIRECTIONS = {'ASC', 'DESC'}

def get_users(order_by: str, direction: str):
    if order_by not in ALLOWED_COLUMNS:
        raise ValueError(f"Invalid column: {order_by}")
    if direction.upper() not in ALLOWED_DIRECTIONS:
        raise ValueError(f"Invalid direction: {direction}")
    # Safe: values are guaranteed to be in the allowlist
    cursor.execute(f"SELECT * FROM users ORDER BY {order_by} {direction}")
```

## ORM Escape Hatch Audit

ORMs do NOT prevent SQL injection in native/raw queries. Audit these methods:

| ORM | Vulnerable Methods | Safe Alternative |
|-----|-------------------|------------------|
| Sequelize | `sequelize.query(userInput)` | `sequelize.query('SELECT * FROM users WHERE id = ?', {replacements: [id]})` |
| Prisma | `prisma.$queryRaw`      `prisma.$executeRaw` | `prisma.$queryRaw\`SELECT * FROM users WHERE id = ${id}\`` (tagged template) |
| GORM | `db.Raw(userInput)` | `db.Raw("SELECT * FROM users WHERE id = ?", id)` |
| SQLAlchemy | `session.execute(text(userInput))` | `session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": id})` |
| Django ORM | `Model.objects.raw(userInput)` | `Model.objects.raw("SELECT * FROM users WHERE id = %s", [id])` |

## NoSQL Injection Patterns

### MongoDB — Vulnerable:
```javascript
// Attacker sends: {"username": {"$ne": null}, "password": {"$ne": null}}
db.users.find({username: req.body.username, password: req.body.password})
// This matches ALL users with non-null username AND password!
```

### MongoDB — Secure:
```javascript
// Use $eq operator to force exact match
db.users.find({
  username: {$eq: req.body.username},
  password: {$eq: req.body.password}
})
```

### MongoDB — Additional Defenses:
- Never use `$where` operator — evaluates arbitrary JavaScript
- Never use `mapReduce` with user input
- Sanitize keys: reject any key starting with `$` in user-supplied objects
- Use `mongo-sanitize` or equivalent library to strip operator characters

## SSTI (Server-Side Template Injection)

### Go
```go
// SAFE: html/template auto-escapes
import "html/template"
tmpl.Execute(w, userInput)  // Output is HTML-escaped

// DANGEROUS: text/template does NOT escape
import "text/template"
// Only use for non-HTML output (emails, plain text)
```

### Python (Jinja2/Django)
```python
# SAFE: Auto-escaped by default
render_template('page.html', user_input=user_input)

# DANGEROUS: render_template_string with user input
render_template_string(user_input)  # SSTI vector!

# DANGEROUS: autoescape disabled
{% autoescape false %}{{ user_input }}{% endautoescape %}
```

### Node.js (EJS)
```html
<!-- SAFE: Escaped interpolation -->
<%= userInput %>

<!-- DANGEROUS: Unescaped interpolation -->
<%- userInput %>
```

## Command Injection
```python
# DANGEROUS: Shell injection via os.system
os.system(f"ping -c 1 {user_host}")  # Attacker: "google.com; rm -rf /"

# SAFE: Argument arrays prevent shell interpretation
subprocess.run(["ping", "-c", "1", user_host])
```
