# Contract Testing at Repo Boundaries

Consumer-driven contract testing ensures that changes in one repo do not silently break consumers in other repos. Contracts are the polyrepo equivalent of compile-time type checking across repo boundaries.

## Consumer-Driven Contracts

Each consumer defines a contract: "I expect the provider's API to respond with this shape, these fields, and these status codes." The provider runs all consumer contracts in its CI pipeline.

### Workflow

1. Consumer team writes a contract test (e.g., using Pact framework).
2. Contract is published to a shared broker (Pact Broker or Git-based).
3. Provider CI pulls all consumer contracts and verifies them against the current code.
4. If a provider change breaks a contract, CI fails before merge.

### Benefits

- Provider knows exactly which consumers will break.
- Consumers know exactly what they depend on.
- Breaking changes are caught at design time, not in integration tests.

## Implementation Options

- **Pact:** Most mature. Pact Broker for contract sharing. Supports HTTP, gRPC, message queues.
- **Spring Cloud Contract:** JVM-focused. Provider-side contract definition.
- **Custom:** Git-based contract storage. Simple but less tooling support.

## When to Use Contract Testing

- Service-to-service API dependencies across repo boundaries.
- When provider team does not know all consumers.
- When breaking changes must be caught before merge, not after deploy.

## When NOT to Use

- Same-team services in a monorepo (compile-time checks are sufficient).
- Stable, rarely-changing APIs with few consumers.
- Teams without capacity to maintain contracts.
