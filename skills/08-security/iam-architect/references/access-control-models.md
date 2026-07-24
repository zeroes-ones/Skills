# Access Control Models: RBAC, ABAC, ReBAC

## Model Comparison

| Dimension | RBAC | ABAC | ReBAC |
|-----------|------|------|-------|
| Decision basis | Role membership | User + resource + environment attributes | Relationship graph traversal |
| Granularity | Coarse (role-level) | Fine (attribute-level) | Fine (relationship-level) |
| Complexity (initial) | Low | Medium-High | Medium |
| Role explosion risk | High (>50 roles) | Low (attribute combinations scale) | Low (relationships naturally bounded) |
| Audit query speed | Fast | Medium (attribute lookup per request) | Medium (graph traversal, bounded by depth) |
| Best for | Internal tools, admin panels, CMS | Regulated industries, multi-tenant SaaS | Collaboration tools, social platforms |

## Role Explosion Prevention

When RBAC hits role explosion (>50 roles, >3 hierarchy levels), apply these patterns:

1. **Permission Groups**: Decouple permissions from roles. editor_read + editor_write + editor_publish = 3 groups, not 2^3 = 8 roles.
2. **ABAC Escape Hatch**: Roles define base access; attributes handle exceptions (e.g., role=editor + department=legal = can edit legal docs).
3. **ReBAC for Ownership**: Document access determined by document:owner@user:alice relationship, not document_owner role.

## Zanzibar Schema Design Pattern (SpiceDB/OpenFGA)

```
definition user {}

definition document {
    relation reader: user | group#member
    relation editor: user
    relation owner: user
    permission view = reader + editor + owner
    permission edit = editor + owner
    permission delete = owner
}

definition group {
    relation member: user
}
```

Key principles:
- Relations are between an object and a subject (or subject set)
- Permissions are computed from relations using union (+) and intersection (&)
- group#member means "member of this group" -- subjects can be users or subject sets
- Set max traversal depth (default 5) to prevent unbounded graph walks

## Policy Enforcement Architecture (PEP/PDP/PIP)

PEP (Policy Enforcement Point): API gateway, middleware, or sidecar proxy -- intercepts requests.
PDP (Policy Decision Point): OPA, Cedar, or custom engine -- evaluates policies against request context.
PIP (Policy Information Point): LDAP/AD (user attrs), CMDB (resource attrs), device manager -- retrieves attributes.
PAP (Policy Administration Point): Policy authoring, versioning, testing, deployment pipeline.

Decision caching: Cache PDP decisions for 30-60 seconds with forced invalidation on role/permission change.
Fail closed: If PDP is unreachable, deny access (never fail open).
