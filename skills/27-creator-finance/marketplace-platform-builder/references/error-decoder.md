# Error Decoder — Marketplace Platform Builder

<!-- DEEP: 5min -- each entry includes a console-string matcher for automatic recovery loops -->

| 🖥️ Console Match | Symptom | Root Cause | Fix | 🔄 Auto-Recovery Loop |
|---|---|---|---|---|
| TypeError: Cannot read properties of undefined | App crashes accessing nested data | Missing null check on API response or async data not loaded yet | Add optional chaining (?.) and nullish coalescing (??). Add loading state UI. | Lint: eslint-plugin-unicorn prefer-optional-chaining rule |
| CORS error: No Access-Control-Allow-Origin | API calls fail from browser but work in curl | Server CORS not configured for frontend origin | Configure CORS with explicit origin list (never * with credentials) | CI: verify CORS config. Block wildcard origins in production |
| FATAL: password authentication failed | DB connection refused after deployment | Credentials mismatch after rotating secrets | Verify env vars match secrets manager. Check connection string format. | Health check: include DB connectivity. Alert on failures |
| 413 Request Entity Too Large | File uploads or large payloads rejected | Server body size limit (often 1MB default) too small | Increase limit for upload routes. Stream large files instead of buffering. | Per-route body size limits. Log at 80% threshold |
| ECONNREFUSED 127.0.0.1:6379 | Redis/cache unavailable | Redis not running or wrong host:port | Start Redis. Verify config. Add connection retry with backoff. | Health check all deps. Circuit breaker for graceful degradation |
| npm ERR! ERESOLVE unable to resolve dependency tree | Install fails with version conflicts | Conflicting package version requirements | Use npm install --legacy-peer-deps. Align versions or use overrides. | CI: npm ci for deterministic builds. Commit lockfile |
| Error: listen EADDRINUSE :::3000 | Server won't start, port in use | Another process holding the port | lsof -i :3000 / kill -9 <PID>. Auto-increment port. | Start script: check port, offer to kill stale process |
| FATAL: sorry, too many clients already | DB connection pool exhausted | Connection leak in error paths | Audit: every pool.connect() needs release() in try/finally. | Auto-release middleware. Pool metrics in health check |
