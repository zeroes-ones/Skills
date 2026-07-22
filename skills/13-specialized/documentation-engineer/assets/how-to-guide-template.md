---
title: How to Deploy a Service to Production
description: Step-by-step guide for deploying a Docker containerized service to the production Kubernetes cluster.
sidebar_position: 2
tags: [deploy, production, kubernetes, docker]
---

# How to Deploy a Service to Production

> **Goal**: Deploy a Docker containerized service to the production Kubernetes cluster using the CI/CD pipeline, verify the deployment is healthy, and roll back if something goes wrong.

---

## Prerequisites

Before starting, ensure you have:

- [ ] **GitHub account** with write access to the service repository
- [ ] **kubectl** installed locally (`v1.28+`) — [Install guide](https://kubernetes.io/docs/tasks/tools/)
- [ ] **Docker** installed locally (`v24+`) — [Install guide](https://docs.docker.com/get-docker/)
- [ ] **Production cluster access** configured in `~/.kube/config` — see [Cluster Access Setup](../guides/cluster-access)
- [ ] **Docker Hub** or **ECR** credentials configured — see [Container Registry Setup](../guides/container-registry)
- [ ] **Service repository** cloned:
  ```bash
  git clone git@github.com:myorg/my-service.git
  cd my-service
  ```

> **Estimated time**: 15 minutes

---

## Step 1: Create a Release Branch

Create a new branch from `main` with your changes:

```bash
git checkout main
git pull origin main
git checkout -b release/v1.2.3
```

> **Expected output**:
> ```
> Switched to a new branch 'release/v1.2.3'
> ```

---

## Step 2: Bump the Version

Update the version tag in `package.json` (or your project's version file):

```bash
# For Node.js projects
npm version patch  # bumps 1.2.2 -> 1.2.3

# For Python projects
# Edit pyproject.toml or setup.cfg manually
```

Commit the version bump:

```bash
git add package.json
git commit -m "chore: bump version to 1.2.3"
```

---

## Step 3: Push and Open a Pull Request

Push the branch and create a PR targeting `main`:

```bash
git push -u origin release/v1.2.3
```

Open a PR in GitHub with:
- **Title**: `release: v1.2.3 — Add user authentication`
- **Description**: Link to changelog, list of changes since last release

> **Expected output**: CI pipeline triggers automatically. Verify all checks pass (lint, test, build, security scan).

---

## Step 4: Wait for CI to Build and Tag

Once the PR is merged to `main`, the CI pipeline automatically:

1. Builds the Docker image: `my-service:1.2.3`
2. Pushes the image to the container registry
3. Creates a Git tag: `v1.2.3`
4. Triggers the deployment workflow

Monitor the CI pipeline:
```bash
# Check if the tag was created
git fetch --tags
git tag -l 'v*' | tail -5
```

> **Expected output**:
> ```
> v1.2.1
> v1.2.2
> v1.2.3
> ```

---

## Step 5: Deploy to Staging

The deployment workflow deploys to staging first. Monitor progress:

```bash
# Watch the staging rollout
kubectl -n staging rollout status deployment/my-service --watch
```

> **Expected output**:
> ```
> Waiting for deployment "my-service" rollout to finish: 0 of 3 updated replicas are available...
> deployment "my-service" successfully rolled out
> ```

Verify the staging deployment:
```bash
# Check pod status
kubectl -n staging get pods -l app=my-service

# Check the health endpoint
curl -s https://staging.my-service.internal/health | jq .
```

> **Expected health response**:
> ```json
> {
>   "status": "healthy",
>   "version": "1.2.3",
>   "uptime_seconds": 120
> }
> ```

---

## Step 6: Deploy to Production

Once staging is verified, promote to production via the deployment dashboard or CLI:

```bash
# Using the deployment CLI tool
deployctl promote my-service --version 1.2.3 --environment production
```

Or if using ArgoCD / Flux:
```bash
# Update the manifest in the gitops repo
git clone git@github.com:myorg/gitops.git
cd gitops
sed -i 's/tag: v1.2.2/tag: v1.2.3/' environments/production/my-service/kustomization.yaml
git add .
git commit -m "promote my-service to v1.2.3"
git push
```

---

## Step 7: Verify the Production Deployment

Monitor the production rollout:

```bash
# Watch the production rollout
kubectl -n production rollout status deployment/my-service --watch
```

Run smoke tests:

```bash
# Basic health check
curl -s https://api.example.com/health | jq .

# End-to-end test
curl -s -o /dev/null -w "%{http_code}" https://api.example.com/api/v1/status

# Check error rate in the last 5 minutes
kubectl -n production logs -l app=my-service --tail=100 | grep -c "ERROR"
```

> **Expected**: HTTP 200 on health endpoint, HTTP 200 on status endpoint, zero errors.

---

## Verification Checklist

- [ ] Staging deployment rolled out successfully (all pods healthy)
- [ ] Staging smoke tests pass (health endpoint returns 200)
- [ ] Production deployment rolled out successfully (0 downtime)
- [ ] Production health endpoint returns `{"status": "healthy"}`
- [ ] Error rate is zero or within normal baseline
- [ ] Monitoring dashboard shows no alerts
- [ ] Release notes published in team Slack channel

---

## Troubleshooting

### Pods stuck in `Pending` or `CrashLoopBackOff`

**Symptom**: New pods are not becoming `Ready` after deployment.

**Causes**:
- Insufficient cluster resources (CPU/memory)
- Image pull failure (registry credentials expired)
- Configuration error (missing environment variable)

**Solutions**:
```bash
# Check pod events
kubectl -n production describe pod -l app=my-service

# Check pod logs
kubectl -n production logs -l app=my-service --tail=50

# Common fix: ensure the image tag exists
docker pull myregistry.io/my-service:1.2.3
```

### Rollback doesn't complete

**Symptom**: `kubectl rollout undo` reports success but pods still show old version.

**Solution**:
```bash
# Check rollout history
kubectl -n production rollout history deployment/my-service

# Roll back to a specific revision
kubectl -n production rollout undo deployment/my-service --to-revision=10

# Verify the rollback
kubectl -n production rollout status deployment/my-service
```

### Health check fails after deployment

**Symptom**: Health endpoint returns 503 or times out.

**Solutions**:
```bash
# Check if the service is listening on the correct port
kubectl -n production exec -it deployment/my-service -- netstat -tlnp

# Verify config map was updated correctly
kubectl -n production get configmap my-service-config -o yaml

# Restart the deployment with the previous config
kubectl -n production rollout undo deployment/my-service
```

---

## Next Steps

Now that your service is deployed to production:

- **[Set Up Monitoring](./set-up-monitoring)** — Configure dashboards and alerts for your service
- **[Configure Auto-Scaling](./configure-auto-scaling)** — Enable HPA for automatic scaling based on CPU/memory
- **[Write a Runbook](../runbooks/my-service)** — Document operational procedures for your service
- **[Set Up Blue/Green Deployments](./blue-green-deployment)** — Implement zero-downtime deployments
- **[Review Deployment Best Practices](./deployment-best-practices)** — Security and performance optimization checklist
