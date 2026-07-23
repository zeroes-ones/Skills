# When Kubernetes is Overkill

```
Team < 5 engineers? → Overkill. Use docker-compose or managed PaaS.
< 5 services? → Overkill. docker-compose + a small VM.
< 100 req/s total? → Overkill. A single VM handles this easily.
Monthly infra budget < $500? → Overkill. K8s control plane alone costs $73/month (EKS).
No multi-service orchestration needed? → Overkill. docker-compose is enough.

Check 2+ boxes? DON'T use Kubernetes. Use one of:
- docker-compose (single VM, 0-5 services, < $100/month)
- ECS Fargate (managed containers, no K8s ops)
- Cloud Run (serverless containers, zero ops)
- Railway/Render/Fly.io (PaaS, heroku-like, < 5 services)
```
