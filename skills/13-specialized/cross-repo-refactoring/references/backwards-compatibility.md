# Backwards Compatibility Patterns

## Pattern 1: Add-Deprecate-Remove

The standard three-step pattern for function/class changes:

```typescript
// Step 1: ADD new API
function newFunction(name: string, options?: Options): Result {
  // New implementation
}

// Step 2: DEPRECATE old API (keep working)
/** @deprecated Use newFunction() instead. Will be removed in v3.0.0. */
function oldFunction(options?: Options, name: string): Result {
  console.warn('[DEPRECATED] oldFunction() called. Use newFunction().');
  metrics.increment('deprecated.oldFunction', { caller: getServiceName() });
  return newFunction(name, options);  // Delegate to new implementation
}

// Step 3: REMOVE old API (after all consumers migrated)
// Delete oldFunction entirely
```

## Pattern 2: API Versioning (URL-Based)

```
/api/v1/users  →  Old implementation (keep for backward compat)
/api/v2/users  →  New implementation
```

Return `Deprecation: true` and `Sunset: Sat, 01 Nov 2026 00:00:00 GMT` headers on v1 responses.

## Pattern 3: Feature Flags

```typescript
if (featureFlags.isEnabled('new-user-api', { userId })) {
  return newUserAPI(userId);
}
return oldUserAPI(userId);
```

## Pattern 4: Protobuf Field Deprecation

```protobuf
message User {
  string name = 1;
  string old_email = 2 [deprecated = true];
  string new_email = 3;
  reserved 2;  // After removing old_email
}
```

## Pattern 5: GraphQL @deprecated

```graphql
type User {
  name: String!
  oldField: String @deprecated(reason: "Use newField. Removal: 2026-12-31")
  newField: String!
}
```
