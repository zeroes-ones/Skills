# docker-compose for MVP

```yaml
# Production-ready MVP stack: docker-compose on single $40/month VM
version: '3.8'
services:
  app:
    build: .
    ports: ['3000:3000']
    depends_on: [db, redis]
    restart: unless-stopped
  db:
    image: postgres:16-alpine
    volumes: [pgdata:/var/lib/postgresql/data]
    restart: unless-stopped
  redis:
    image: redis:7-alpine
    restart: unless-stopped
volumes:
  pgdata:
```
**Ceiling:** 1K-10K DAU, 50-200 req/s. Migrate to managed DB (RDS) first, then to K8s when you need auto-scaling.
