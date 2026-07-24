# Assertion Checklist

## Purpose
Distinguish strong assertions (prove correct behavior) from weak assertions (prove nothing useful). Weak assertions create false confidence.

## Strong Assertions (Use These)
- `expect(result.price).toBe(19.99)` — specific value match
- `expect(result.items).toHaveLength(3)` — structural assertion
- `expect(fn).toThrow(TypeError)` — specific error type
- `expect(mockFn).toHaveBeenCalledWith({ id: 42 })` — exact call verification
- `expect(response.status).toBe(201)` — specific status code

## Weak Assertions (Avoid Without Supplement)
- `expect(result).toBeTruthy()` — passes for `{}`, `[]`, `"false"`, `1`
- `expect(result).not.toBeNull()` — passes for wrong values
- `expect(result).toBeDefined()` — passes for `undefined`'s cousin `null`
- `expect(fn).not.toThrow()` — passes even if output is completely wrong
- `expect(result).toBeInstanceOf(Object)` — passes for literally any object

## Checklist
- [ ] Every test asserts a specific expected value, not just "truthy" or "not null"
- [ ] Error paths assert the specific error type and message
- [ ] Array assertions include length and content checks
- [ ] Mock/spy assertions verify exact arguments, not just "was called"
- [ ] Async tests use `await` or `done` callback — no false passes from unresolved promises

## Gate
A test suite where >10% of assertions are weak is not adequate verification.
