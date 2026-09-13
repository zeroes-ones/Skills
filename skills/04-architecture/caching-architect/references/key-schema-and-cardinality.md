# Key Schema and Cardinality — the key is a capacity and security decision

> Every dimension added to the key for correctness multiplies the key space, and every dimension
> omitted from the key is a correctness or data-leak bug. This file works both directions (R2).

---

## Key cardinality, and why the key schema is a capacity decision

```
keys ≈ distinct combinations of the separator dimensions
     = |tenant| × |locale| × |scope| × |entities| × |versions|

100 tenants × 5 locales × 2 scopes × 1,000,000 entities × 2 versions
  = 2,000,000,000 distinct keys
```

Every dimension added to the key for correctness multiplies the key space and therefore the memory.
The schema decision and the sizing decision are the same decision; this is why R2 asks for the
components *and* why cache sizing escalates to `capacity-planning-engineer` rather than being tuned
by feel (R6).

---

## The key must separate on every dimension the value depends on

The two failures this rule prevents, stated as properties to test:

- **Missing correctness dimension.** A key built from an identifier that is unique but whose *value*
  depends on a tenant override will serve one tenant's value to every other. The key must separate
  on every dimension the **value** depends on, not every dimension the **identifier** happens to be
  unique on.
- **Missing security dimension.** A key that omits the authorization scope is a cross-tenant
  data-leak vector. Keys are a security boundary, and the collision test is written against tenants
  and scopes, not against entity ids.

---

## The collision test

Prove two tenants (or scopes) cannot map to the same key. This is a property test, not an example:

```
for tenant_a, tenant_b in sample where tenant_a != tenant_b:
    for every other dimension combination D:
        assert key(tenant_a, D) != key(tenant_b, D)
```

The test fails the moment a dimension is dropped from the schema — which is the only way this bug
can be introduced.
