# Production Checklist — Creator Economy Builder

<!-- QUICK: 30s -- binary pass/fail items -->

- [ ] Design document reviewed and approved by stakeholders
- [ ] All decision trees in SKILL.md have been walked through for this implementation
- [ ] Error handling covers all code paths (happy path + error states + edge cases)
- [ ] Input validation at every boundary (API, CLI, file, user input)
- [ ] Authentication and authorization enforced on all protected routes/operations
- [ ] Secrets externalized -- no hardcoded credentials, API keys, or tokens
- [ ] Database migrations are backward-compatible and tested with rollback
- [ ] Logging includes correlation IDs for request tracing across services
- [ ] Health check endpoint returns accurate status of all dependencies
- [ ] Rate limiting applied to public endpoints
- [ ] CORS configured restrictively (not wildcard * in production)
- [ ] Content Security Policy headers set
- [ ] Performance tested under expected peak load
- [ ] Accessibility baseline met (keyboard nav, screen reader labels, color contrast)
- [ ] Mobile-responsive if user-facing (tested on actual devices)
- [ ] Analytics/telemetry instrumented for key user journeys
- [ ] Error messages are user-friendly (no stack traces, no internal paths)
- [ ] Documentation updated (README, API docs, runbooks)
- [ ] Rollback plan documented and tested
- [ ] Code review completed by at least one other developer
