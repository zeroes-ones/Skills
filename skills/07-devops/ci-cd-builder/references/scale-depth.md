# Scale Depth: Solo → Small → Medium → Enterprise

### Solo (1 person, 0-100 users)
- **What changes**: CI/CD = `git push` to Vercel/Netlify/Railway. No pipeline definition needed. Deploy on push to main. Rollback = `git revert` + push.
- **What to skip**: Custom CI pipeline. Test stages. Build caching. Environment promotion. Secrets management. Preview deployments. Artifact management.
- **Coordination**: You push, platform deploys. Done.

### Small Team (2-10 people, 100-10K users)
- **What changes**: GitHub Actions or GitLab CI. Stages: lint → test → build → deploy. Caching for dependencies. Environment separation (staging + production). Secrets via CI secrets manager. Preview deployments per PR. Notifications on failure.
- **What to skip**: Matrix builds. Blue-green/canary deployments. Progressive delivery. SLSA provenance. SBOM generation. Multi-cloud pipelines.
- **Coordination**: Pipeline changes reviewed in PR. Deploy announcements in Slack. Weekly pipeline health check.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Full pipeline: lint → test → build → scan → deploy → verify. Matrix builds for multi-platform. Blue-green or canary deployments. Security scanning (SAST + dependency + container). Path filters in monorepo. Environment promotion (dev → staging → prod). Artifact promotion (build once, deploy many). Concurrency groups.
- **What to skip**: Multi-cloud pipelines. Progressive delivery (canary analysis automated). Full SLSA Level 3. SBOM for every build.
- **Coordination**: Pipeline team or DevOps owner. Bi-weekly pipeline review. Deploy calendar for coordinated releases.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Pipeline platform team. Self-service pipeline templates. Multi-cloud deployment pipelines. Progressive delivery with automated rollback. Full security gates (SAST + DAST + SCA + IAC scan + image scan). SLSA Level 3 provenance. SBOM generation. Compliance gates (SOC 2, PCI DSS). Pipeline metrics (DORA: deployment frequency, lead time, change failure rate, MTTR). Pipeline cost optimization.
- **What's full production**: Internal developer platform. Pipeline catalog. Automated canary analysis. Deployment analytics. Pipeline as product.
- **Coordination**: Pipeline platform team weekly. Monthly pipeline review board. Quarterly DORA metrics review.

### Transition Triggers
- **Solo → Small**: Second developer. Need automated tests before deploy.
- **Small → Medium**: 3+ teams. Deploy coordination overhead. First security incident from deployed code.
- **Medium → Enterprise**: 10+ teams. Compliance requirements. >50 deploys/day.
