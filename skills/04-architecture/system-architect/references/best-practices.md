# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Evolvable architecture**: Start with modular monolith; extract microservices only when bounded contexts are clear and independent scaling is needed.
- **Loose coupling, high cohesion**: Services communicate through well-defined APIs and events; avoid shared databases across services.
- **Design for failure**: Every dependency can fail — implement retries, circuit breakers, fallbacks, and dead-letter queues.
- **Observability from day one**: Distributed tracing (OpenTelemetry), structured logging, metrics (RED: Rate, Errors, Duration), health checks (liveness/readiness).
- **Infrastructure as Code**: Terraform/Pulumi/CloudFormation for all infrastructure; GitOps (ArgoCD/Flux) for deployment.
- **Security by design**: Defense in depth, zero-trust networking, least-privilege IAM, encryption at rest and in transit, secrets management (Vault/Secrets Manager).
- **Cost awareness**: Model cloud costs early (compute, data transfer, storage, managed services); architect for cost optimization (spot instances, auto-scaling, serverless where appropriate).
