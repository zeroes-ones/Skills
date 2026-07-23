# Scale Depth: Solo → Small → Medium → Enterprise

<!-- STANDARD: 3min -->

### Solo (1 developer, MVP)
**Description:** Single API, < 20 endpoints, no existing tests.
**Approach:** Run route detection. Generate smoke tests for every endpoint (auth × 2 + happy path). Target 60% coverage. Don't over-engineer — the API will change rapidly.
**Time investment:** 2-4 hours for full baseline coverage.

### Small Team (2-10 developers, active development)
**Description:** Growing API, 20-100 endpoints, some tests exist but coverage is spotty.
**Approach:** Run route-to-test gap analysis. Prioritize P0 endpoints (auth, payments, core business logic). Add validation matrices for new endpoints. Integrate coverage gate into CI. Generate regression test suite for pre-release.
**Time investment:** 1-2 days to close P0 gaps. Ongoing: 15 min per new endpoint.

### Medium Team (10-50 developers, multiple services)
**Description:** Multiple APIs, 100-500 endpoints, dedicated QA team, CI/CD pipeline.
**Approach:** Standardize test structure across services. Add mutation testing to P0 endpoints. Contract testing between services (Pact or similar). Performance test suite for critical paths. Test data factories as shared library. Coverage dashboards per service.
**Time investment:** 1-2 weeks to standardize. Ongoing: automated in CI.

### Enterprise (50+ developers, microservices, compliance requirements)
**Description:** 500+ endpoints across 10+ services, regulatory compliance (SOC 2, HIPAA, PCI), multiple teams.
**Approach:** Centralized test infrastructure team. Cross-service integration tests with synthetic data. Compliance-specific test suites (PHI access audit, encryption verification, data retention). Chaos testing for API resilience. Automated test generation from OpenAPI specs on every deploy. Coverage and mutation score SLAs per service.
**Time investment:** Ongoing investment. Dedicated test infrastructure team.
