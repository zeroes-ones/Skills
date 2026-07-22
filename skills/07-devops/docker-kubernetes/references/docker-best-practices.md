# Docker Best Practices

> **Author:** Sandeep Kumar Penchala

Production-grade Docker patterns covering image optimization, security, Compose patterns, tagging, caching, secrets, and debugging. These practices support the docker-kubernetes skill's containerization and deployment workflows.

## Dockerfile Optimization

### Multi-Stage Builds

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
RUN npm run build

# Stage 2: Production (distroless — no shell, no package manager)
FROM gcr.io/distroless/nodejs20-debian12
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
USER nonroot
CMD ["dist/main.js"]
```

### Layer Caching Strategy

```dockerfile
# Layer ordering by change frequency (least → most frequent)
FROM node:20-alpine
WORKDIR /app

# 1. Dependencies (rarely changes) — cache this layer heavily
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# 2. Source code (changes often) — goes AFTER deps
COPY src/ ./src/
COPY tsconfig.json ./

# 3. Build output (every deploy)
RUN npm run build

# DO NOT DO: COPY . .  (invalidates entire cache on any file change)
# DO NOT DO: RUN npm install (no lockfile = non-deterministic)
```

### .dockerignore

```dockerignore
node_modules
.git
.gitignore
*.md
.env
.env.*
dist
coverage
.cache
Dockerfile
docker-compose*.yml
```

### Non-Root User

```dockerfile
# Create and switch to non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Or pre-created in base images:
USER node    # node:*-alpine images
USER 1001    # Distroless; numeric UID for K8s security context
```

## Image Size Reduction

| Base Image | Size | Shell | Package Manager | Best For |
|-----------|------|-------|----------------|----------|
| `node:20` | ~1 GB | Yes | apt | Not recommended |
| `node:20-slim` | ~250 MB | Yes | apt (minimal) | Dev/staging |
| `node:20-alpine` | ~120 MB | Yes | apk | Production default |
| `gcr.io/distroless/nodejs20` | ~130 MB | No | None | Maximum security |
| `alpine:3.20` | ~7 MB | Yes | apk | Custom builds |
| `scratch` | 0 MB | No | None | Static binaries only |

```
Size reduction checklist:
  1. Use slim/alpine variant
  2. Multi-stage builds (discard build tools)
  3. Combine RUN commands (fewer layers)
  4. Clean package manager cache: `apt-get clean && rm -rf /var/lib/apt/lists/*`
  5. Use --no-install-recommends with apt-get
  6. Strip debug symbols from compiled binaries
```

## Security Scanning

### Trivy in CI

```yaml
# .github/workflows/scan.yml
security-scan:
  steps:
    - uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'myapp:${{ github.sha }}'
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'HIGH,CRITICAL'
        exit-code: 1
    - uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: 'trivy-results.sarif'
```

### Docker Scout

```bash
# Quick comparison between images
docker scout compare node:20-alpine node:20-slim

# CI integration
docker scout cves myapp:latest --exit-code --severity critical
```

## Docker Compose Patterns

### Dev vs Prod Overrides

```yaml
# docker-compose.yml (base)
services:
  app:
    build: .
    ports: ["3000:3000"]
    environment:
      - NODE_ENV=production
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5
```

```yaml
# docker-compose.override.yml (dev — applied automatically)
services:
  app:
    build:
      target: development          # Use dev stage of Dockerfile
    volumes:
      - .:/app                     # Hot reload source
      - /app/node_modules          # Anonymous volume — preserve container node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev
```

### Health Checks

```yaml
# HTTP-based health check
healthcheck:
  test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/health"]
  interval: 10s
  timeout: 5s
  retries: 3
  start_period: 15s

# Process-based health check
healthcheck:
  test: ["CMD-SHELL", "pidof nginx || exit 1"]
  interval: 30s
```

## Image Tagging Strategy

| Tag | When to Use | Example | Pros | Cons |
|-----|------------|---------|------|------|
| Git SHA | Every CI build | `myapp:abc1234` | Immutable, traceable to commit | Not human-friendly |
| Semver | Releases | `myapp:1.2.3` | Human-friendly, semantic meaning | Must maintain versioning discipline |
| `latest` | Dev convenience only | `myapp:latest` | Easy to pull | Never use in production — non-deterministic |
| Branch name | Feature previews | `myapp:feat-payments` | Easy for dev/staging | Ephemeral; clean up |
| Date-based | Nightly builds | `myapp:2026-07-21` | Chronological ordering | No semantic meaning |

```
Production recommendation:
  docker build -t myapp:${GIT_SHA} -t myapp:${VERSION} .
  docker push myapp:${GIT_SHA}    # Deploy by SHA
  docker push myapp:${VERSION}    # Human-friendly alias
  # NEVER push latest to prod registry
```

## Build Caching with BuildKit

```bash
# Enable BuildKit (Docker 23+ enables by default)
export DOCKER_BUILDKIT=1

# Remote cache (OCI registry)
docker buildx build \
  --cache-from type=registry,ref=myregistry.com/myapp:cache \
  --cache-to   type=registry,ref=myregistry.com/myapp:cache,mode=max \
  -t myapp:latest .

# CI cache (GitHub Actions)
docker buildx build \
  --cache-from type=gha \
  --cache-to   type=gha,mode=max \
  -t myapp:$GITHUB_SHA .
```

## Secrets Management

```dockerfile
# NEVER DO THIS (secret becomes baked into layer):
# ENV DATABASE_URL=postgres://user:pass@host/db

# BuildKit secret mount (available during build, NOT in final image)
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci

# Usage: docker build --secret id=npmrc,src=$HOME/.npmrc .
```

```yaml
# Docker Compose secrets
services:
  app:
    secrets:
      - db_password
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## Container Debugging Cheat Sheet

```bash
# Inspect container
docker inspect myapp               # Full JSON metadata (env, mounts, network, labels)

# Logs
docker logs myapp                  # Recent logs
docker logs -f --tail 100 myapp   # Follow last 100 lines
docker logs --since 5m myapp      # Last 5 minutes

# Execute into container
docker exec -it myapp sh           # Shell (alpine)
docker exec -it myapp bash         # Shell (slim/standard)

# Resource usage
docker stats myapp                 # Live CPU/memory/network I/O
docker top myapp                   # Running processes inside container

# Filesystem
docker diff myapp                  # Files changed since container start

# Copy files to/from container
docker cp myapp:/app/logs ./logs   # Copy out
docker cp ./config.json myapp:/app/  # Copy in

# Debug with temporary container
docker run --rm -it --entrypoint sh myapp:latest   # Override entrypoint
docker run --rm -it --network host alpine wget -O- http://localhost:3000/health
```

These Docker best practices implement the docker-kubernetes skill's emphasis on production-grade containerization — multi-stage builds, non-root execution, security scanning, and proper tagging ensure every image is reproducible, minimal, and secure by default.
