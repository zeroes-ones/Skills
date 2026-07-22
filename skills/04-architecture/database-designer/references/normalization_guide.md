# Database Normalization Guide

## Normal Forms

### 1NF (First Normal Form)
- Each cell contains a single value (atomic)
- Each row is unique (primary key exists)
- No repeating groups

```
❌ Violation:
| id | name  | phones              |
| 1  | Alice | 555-0100, 555-0200  |

✅ 1NF:
| id | name  | phone     |
| 1  | Alice | 555-0100  |
| 2  | Alice | 555-0200  |
```

### 2NF (Second Normal Form)
- Satisfies 1NF
- No partial dependencies (non-key columns depend on the ENTIRE primary key)

```
❌ Violation — composite key (order_id, product_id):
| order_id | product_id | product_name | quantity |
product_name depends only on product_id, not the full key

✅ 2NF — split into orders_items + products:
orders_items(order_id, product_id, quantity)
products(product_id, product_name)
```

### 3NF (Third Normal Form)
- Satisfies 2NF
- No transitive dependencies (non-key columns don't depend on other non-key columns)

```
❌ Violation:
| employee_id | name  | dept_id | dept_name |
dept_name depends on dept_id, not directly on employee_id

✅ 3NF — split into employees + departments:
employees(employee_id, name, dept_id)
departments(dept_id, dept_name)
```

### BCNF (Boyce-Codd Normal Form)
- Strict version of 3NF
- Every determinant must be a candidate key
- Rarely needed in practice

## When to Denormalize

Denormalization is acceptable when:
1. **Read-heavy workloads** — query performance outweighs write complexity
2. **Precomputed aggregates** — dashboards, reporting tables
3. **Embedded documents** — MongoDB pattern where related data is always accessed together
4. **CQRS read models** — optimized read side separate from normalized write side

Always document why you denormalized and how consistency is maintained.

## Common Design Mistakes

1. **Over-normalization** — splitting data that's always queried together
2. **Under-normalization** — massive tables with repeated data
3. **Missing foreign keys** — no referential integrity
4. **Wrong data types** — VARCHAR for everything, no constraints
5. **No timestamps** — missing `created_at` and `updated_at` on every table
6. **EAV pattern abuse** — Entity-Attribute-Value as a primary design pattern
7. **No soft deletes** — permanent destructive deletes
