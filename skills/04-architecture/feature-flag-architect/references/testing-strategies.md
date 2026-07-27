# Testing with Feature Flags

## The Core Problem: Combinatorial Explosion

N binary flags = 2^N possible states. At 5 flags, you need 32 test suites. At 10 flags, 1,024. This is untestable.

### The Solution Layer Cake

```
Layer 1: Unit test each flag branch independently (always)
Layer 2: Integration test each flag ON and OFF (always)
Layer 3: Pairwise interaction testing (when flags interact)
Layer 4: Full-combination testing (never — use monitoring instead)
```

## Layer 1: Unit Testing Both Flag States

Every code block guarded by a flag must be tested for both states:

```typescript
describe("CheckoutService", () => {
  describe("when checkout.new_flow.v2 is OFF", () => {
    it("uses legacy checkout flow", () => {
      flags.setEnabled("checkout.new_flow.v2", false);
      const order = checkoutService.process(cart);
      expect(order.flow).toBe("legacy");
    });
  });

  describe("when checkout.new_flow.v2 is ON", () => {
    it("uses new checkout flow", () => {
      flags.setEnabled("checkout.new_flow.v2", true);
      const order = checkoutService.process(cart);
      expect(order.flow).toBe("v2");
    });
  });
});
```

**CI gate: Any flag-guarded code block without both-state tests → PR BLOCKED.**

## Layer 2: Flag Transition Testing

Test what happens when a flag changes state at runtime:

```typescript
describe("Flag transition", () => {
  it("survives ON→OFF transition without errors", () => {
    flags.setEnabled("checkout.new_flow.v2", true);
    const order1 = checkoutService.process(cart); // v2 flow
    flags.setEnabled("checkout.new_flow.v2", false);
    const order2 = checkoutService.process(cart); // legacy flow
    expect(order1.flow).toBe("v2");
    expect(order2.flow).toBe("legacy");
    // No errors in Sentry
  });

  it("OFF→ON transition works mid-session", () => {
    const session = startCheckoutSession();
    flags.setEnabled("checkout.new_flow.v2", true);
    session.continue(); // should not crash
  });
});
```

## Layer 3: Pairwise Interaction Testing

When flags A and B both affect the same code path, test all *pairs* of states (not all combinations):

```
Flags: A (checkout_v2), B (fraud_check), C (express_shipping)
8 combinations (2^3), but only 4 pairwise tests needed:
1. A=OFF, B=OFF (covers C=OFF by default)
2. A=ON,  B=OFF (covers C=OFF by default)
3. A=OFF, B=ON  (with C=ON)
4. A=ON,  B=ON  (with C=ON)
```

**CI gate: When a code path touches N flags (N > 2), require at least N+1 pairwise tests.**

## Flag Interaction Budget

Service-level rule: maximum 3 flags may interact in the same code path. If 4 flags interact, refactor to reduce interactions before adding more tests.

```python
# BAD: 4 flags interacting in one function
def process_checkout(cart, flags):
    if flags.is_enabled("new_flow"):
        if flags.is_enabled("fraud_check"):
            if flags.is_enabled("express"):
                if flags.is_enabled("loyalty_discount"):
                    return checkout_v4(cart)  # 16 states, untestable

# BETTER: Decompose into independent services
def process_checkout(cart, flow, fraud, shipping, loyalty):
    return flow(cart) \
        .pipe(fraud) \
        .pipe(shipping) \
        .pipe(loyalty)
    # Each component tested independently; composition tested pairwise
```

## Kill Switch Testing (Quarterly Drill)

Every ops toggle must be tested in production once per quarter:

```
1. Schedule non-peak window (Tuesday 3 AM UTC-4).
2. Announce drill 24 hours in advance.
3. At drill time:
   a. Toggle kill switch OFF.
   b. Verify old code path activates within 5 seconds.
   c. Monitor error rate, latency for 2 minutes.
   d. Toggle kill switch back ON.
   e. Verify new code path resumes within 5 seconds.
4. File drill report: duration, errors, latency spikes.
5. If kill switch fails: P1 incident, fix within 24 hours.
```

## Per-Platform Testing Matrix

| Platform | Unit Test Tool | Flag Mock | Integration/E2E | Special Concern |
|----------|---------------|-----------|-----------------|-----------------|
| Backend (Go) | `go test` + testify | Mock `flag.Client` interface | Integration test with real SDK in Docker | Flag evaluation latency under load |
| Backend (Node) | Jest/Vitest | Mock `launchdarkly-node` | Supertest with flag middleware | Async flag initialization race |
| Web (React) | Jest + React Testing Library | Mock `useFlag` hook | Cypress/Playwright with flag overrides | SSR hydration mismatch |
| iOS | XCTest | Mock `RemoteConfig` | XCUITest with launch arguments for flags | 12-hour cache behavior |
| Android | JUnit + MockK | Mock `FirebaseRemoteConfig` | Espresso with test flag provider | OEM background kill |
| Desktop | Jest/Vitest | Mock flag client | Playwright/Spectron with flag injection | Multi-window flag sync |

## CI Enforcement Rules

```yaml
# .github/workflows/flag-checks.yml (conceptual)
flag-policy:
  rules:
    - name: stale-flag-detection
      check: "Every flag at 100% > 30 days must have a CLOSED removal ticket"
      action: FAIL_PR

    - name: both-state-test-coverage
      check: "Every flag-guarded code block must have at least one test for ON and one for OFF"
      action: FAIL_PR

    - name: flag-metadata-required
      check: "Every flag must have: owner, type, removal_date, rollout_plan"
      action: FAIL_PR with missing metadata report

    - name: interaction-budget
      check: "No code path may reference more than 3 feature flags"
      action: WARN_PR (BLOCK for paths with 5+ flags)

    - name: kill-switch-drill-schedule
      check: "Every ops toggle must have a drill in the last 90 days"
      action: WARN_PR (reminder to schedule drill)
```
