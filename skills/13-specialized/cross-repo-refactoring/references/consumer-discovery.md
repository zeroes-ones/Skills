# Consumer Discovery: Finding Everyone Who Depends on Your API

## GitHub Code Search

```bash
# Search across all org repos
gh search code "oldFunction" --owner=my-org --language=typescript

# Search for imports specifically
gh search code "import { oldFunction } from" --owner=my-org

# Search for REST endpoint usage
gh search code "/api/v1/deprecated-endpoint" --owner=my-org
```

## Registry Analytics

### npm
```bash
npm view @org/package deprecated --json
npm view @org/package versions --json
```

### Maven Central
Check download statistics and dependency graphs in your artifact repository (Nexus, Artifactory).

### PyPI
```bash
pip install pypistats
pypistats recent @org/package
```

## Runtime Telemetry

```typescript
// Instrument deprecated API with consumer-aware counter
app.use('/api/v1/old-endpoint', (req, res, next) => {
  metrics.increment('deprecated_api_usage', {
    api: 'old-endpoint',
    consumer: req.headers['x-service-name'] || 'unknown',
    version: req.headers['x-service-version'] || 'unknown'
  });
  next();
});
```

## Consumer Inventory Template

| Repo | Maintainer | Call Sites | Deploy Cadence | Last Deploy | Migration Difficulty |
|------|-----------|------------|----------------|-------------|---------------------|
| repo-a | @alice | 45 | Daily | 2026-07-22 | Low (simple pattern) |
| repo-b | @bob | 12 | Weekly | 2026-07-15 | Medium (wrapper exists) |
| repo-c | UNMAINTAINED | 8 | Never | 2025-11-03 | High (no maintainer) |
