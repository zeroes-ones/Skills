# Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **Stack**: Python/FastAPI or Node.js/Express. Fastest path to working API.
- **Database**: SQLite for dev, managed Postgres (Render/Railway free tier) for prod.
- **Deploy**: Single server or PaaS (Railway, Render, Fly.io). Dockerfile + `git push`.
- **Skip**: Kubernetes, microservices, message queues, distributed tracing. All overkill.
- **Coordination**: None. You are the API designer, developer, and reviewer.

### Small Team (2-10 people, 100-10K users)
- **Add**: CI/CD pipeline (GitHub Actions), structured logging, basic monitoring (health checks + error alerts).
- **Database**: Managed Postgres with connection pooling (PgBouncer). Redis for caching and sessions.
- **API**: OpenAPI spec as contract between frontend and backend. API versioning policy.
- **Queue**: Redis or SQS for async tasks. Keep simple — one queue, one worker.
- **Skip**: Kubernetes (use PaaS or docker-compose), multi-service architecture, event sourcing.

### Medium Team (10-50 people, 10K-1M users)
- **Add**: Distributed tracing (OpenTelemetry), metrics dashboard (Grafana), SLO-based alerting.
- **Architecture**: Modular monolith or 2-3 services around clear bounded contexts.
- **Database**: Read replicas for read-heavy endpoints. Connection pooling per service.
- **Queue**: Dedicated message broker (RabbitMQ, SQS). Dead letter queues for failed jobs.
- **Testing**: Contract tests in CI. Load tests before major releases.

### Enterprise (50+ people, 1M+ users)
- **Architecture**: Microservices or service-oriented. Event-driven where appropriate.
- **Database**: Multi-region with sharding. Dedicated DBRE (Database Reliability Engineer).
- **Security**: API gateway with rate limiting, WAF, regular penetration testing.
- **Compliance**: SOC 2, GDPR, PCI DSS controls implemented. Audit logging everywhere.
- **Coordination**: Cross-team API governance. Shared infrastructure team.

### Transition Triggers
- Solo → Small: You're the bottleneck. Hire backend dev #2.
- Small → Medium: P95 latency > 200ms sustained. DB CPU > 60%. Team can't ship independently.
- Medium → Enterprise: 3+ teams need to coordinate per deploy. Compliance mandates separation of concerns.
