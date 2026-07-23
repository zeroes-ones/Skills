# Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: Fullstack = Next.js (pages or app router) or Remix. One codebase. Database via ORM (Prisma/Drizzle). Auth = NextAuth/Clerk. Deploy to Vercel. No monorepo. No CI/CD. Manual testing.
- **What to skip**: Monorepo. Docker. Separate frontend/backend. Message queues. Redis. Microservices. E2E tests. Feature flags. Structured logging. Type sharing packages.
- **Coordination**: You own everything. Ship fast.

### Small Team (2-10 people, 100-10K users)
- **What changes**: Monorepo (Turborepo) with shared types/validation. Fullstack framework (Next.js/Remix). CI/CD with lint + type-check + test + deploy. Database migrations in CI. Basic error handling. Structured logging. E2E test for critical flow. Feature flags for risky changes.
- **What to skip**: Separate frontend/backend services. Message queues (inline async is fine). Redis (unless caching needed). Multiple deployment targets.
- **Coordination**: PR review. API contract in shared types package. Weekly fullstack sync.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Monorepo with multiple apps/packages. Separate services for compute-heavy work. Message queues for async processing. Redis for caching. Full E2E test suite. Feature flags with gradual rollout. Error monitoring (Sentry). Observability with correlation IDs. Database migration rollback plans.
- **What to skip**: Microservices (>3 services). Kubernetes (Vercel/ECS is enough). Multi-region.
- **Coordination**: Weekly fullstack guild. Architecture RFC for new services. Cross-team type contract review.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Platform team owning shared infra. Microservices for domain boundaries. Full observability (traces + metrics + logs). SLOs with error budgets. Canary deployments. A/B testing infrastructure. Feature flag platform (LaunchDarkly). Multi-region deployment. Compliance audit trails. Database sharding as needed.
- **What's full production**: Internal developer platform. Service catalog. Automated dependency updates. Contract testing. Developer experience metrics.
- **Coordination**: Platform team weekly. Architecture review board. Cross-team service contract sync. Quarterly capacity planning.

### Transition Triggers
- **Solo → Small**: Second fullstack developer. Monolith becomes hard to reason about for one person.
- **Small → Medium**: Need to separate concerns (compute-heavy work blocking request lifecycle). >1K req/s.
- **Medium → Enterprise**: 5+ teams in monorepo. Multi-region or compliance requirements. >10K req/s.
