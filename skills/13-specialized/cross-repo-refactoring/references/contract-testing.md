# Cross-Repo Contract Testing

## Pact Workflow

### Consumer Side

```typescript
// consumer.pact.spec.ts
import { Pact } from '@pact-foundation/pact';

const provider = new Pact({
  consumer: 'payment-service',
  provider: 'user-service',
});

describe('User Service Contract', () => {
  it('returns user by ID', async () => {
    await provider.addInteraction({
      state: 'user 123 exists',
      uponReceiving: 'a GET request for user 123',
      withRequest: {
        method: 'GET',
        path: '/api/users/123',
      },
      willRespondWith: {
        status: 200,
        body: {
          id: 123,
          name: 'Alice',
          email: 'alice@example.com',
        },
      },
    });

    const user = await userClient.getUser(123);
    expect(user.name).toBe('Alice');
  });
});
```

### Provider Side

```typescript
// provider.pact.spec.ts — Verifies provider satisfies all consumer contracts
import { Verifier } from '@pact-foundation/pact';

new Verifier().verifyProvider({
  provider: 'user-service',
  providerBaseUrl: 'http://localhost:8080',
  pactBrokerUrl: 'https://pact-broker.example.com',
});
```

## Can I Deploy? Check

The Pact Broker's `can-i-deploy` endpoint checks if deploying a new provider version would break any consumer contracts.

```bash
pact-broker can-i-deploy   --pacticipant user-service   --version 2.5.0   --to-environment production
```

## Lightweight Alternatives

- OpenAPI schema compatibility check in CI
- CI job that runs consumer test suites against provider staging
- ProtoBuf backwards compatibility lint (buf breaking)
- Shared API client library with versioned releases
