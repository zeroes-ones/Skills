# API Authorization Models — Reference

## Model Comparison

| Dimension | RBAC (Role-Based) | ABAC (Attribute-Based) | ReBAC (Relationship-Based) |
|-----------|-------------------|------------------------|----------------------------|
| Decision logic | User → Role → Permission | Subject + Resource + Environment → Decision | Actor --[Relation]--> Object |
| Policy complexity | Low (flat role list) | High (boolean logic over attributes) | Medium (graph traversal) |
| Policy changes | Requires role reassignment | Attribute changes auto-update access | Relationship changes auto-update access |
| Query complexity | `SELECT * WHERE user.role = 'admin'` | Policy evaluation per resource (slow) | Graph traversal with set logic |
| Best examples | Admin, Editor, Viewer roles | "User can read documents in their department during business hours" | "User can edit documents shared with their team" |
| Implementation | Built into most frameworks | OPA/Rego, Cedar, AWS Verified Permissions | OpenFGA, SpiceDB, Google Zanzibar |

## OPA/Rego Policy Examples

### Simple RBAC Policy
```rego
package api.authz

default allow = false

allow {
    input.user.role == "admin"
}

allow {
    input.user.role == "editor"
    input.action == "read"
}

allow {
    input.user.role == "viewer"
    input.action == "read"
}
```

### Resource-Level ABAC Policy
```rego
package api.authz

default allow = false

allow {
    # User can access their own resources
    input.user.id == input.resource.owner_id
}

allow {
    # Admins can access any resource in their tenant
    input.user.role == "admin"
    input.user.tenant_id == input.resource.tenant_id
}

allow {
    # Managers can access their direct reports' resources
    input.user.id in input.resource.manager_chain
    input.action == "read"
}
```

### Tenant Isolation Policy
```rego
package api.authz

default allow = false

# Every access MUST be scoped to the user's tenant
allow {
    input.user.tenant_id == input.resource.tenant_id
    # Additional conditions apply...
}
```

## Permission Model Decision Tree

When choosing an authorization model, evaluate these factors:
1. **Number of roles:** < 20 distinct roles → RBAC is sufficient. > 50 roles → ABAC or ReBAC.
2. **Attribute complexity:** Do you need time-based, location-based, or risk-based conditions? → ABAC.
3. **Relationship complexity:** Social graphs, org hierarchies, document sharing? → ReBAC.
4. **Policy change frequency:** Rare changes → RBAC. Frequent, dynamic changes → ABAC or ReBAC.
5. **Performance requirements:** RBAC adds ~1ms. ABAC/ReBAC add 10-50ms per evaluation.

## Policy-as-Code Best Practices

- Version control all policies alongside application code
- Test policies with `opa test` in CI pipeline
- Use policy bundles (OPA) or policy stores (Cedar) for distribution
- Decision log: log every allow/deny with full input context
- Fail closed: `default allow = false` — deny if policy evaluation errors
- Separate policy from enforcement: policy engine evaluates, middleware enforces
