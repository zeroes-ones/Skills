# Orchestra Platform — From Idea to Spec

## Problem Statement

Developers at mid-market companies lose **5–10 hours per week** on infrastructure requests — spinning up new services, requesting CI/CD pipelines, managing environment configurations, rotating secrets, and tracking down service ownership. These requests typically flow through a bottlenecked platform engineer (or a DevOps team of one) who manually fulfills each ticket. The result: feature velocity drops, developer satisfaction tanks, and the platform engineer burns out within 18 months.

## Target User

**Primary persona:** Platform Engineering Lead (or senior DevOps engineer) at a 50–200 person engineering organization. They've been tasked with "building an internal platform" but have no dedicated team. They've looked at Backstage but can't justify the 3–6 months of setup and ongoing maintenance.

**Secondary persona:** Staff Engineer who just wants to create a new service, see what services exist, and know who owns what — without filing a Jira ticket.

## Core User Stories

- **As a developer,** I want to create a new service from a template (with CI/CD, monitoring, and a repo scaffolded) in under 15 minutes.
- **As a platform lead,** I want to see a live inventory of every service in my org — what it is, who owns it, and when it was last deployed.
- **As a developer,** I want to browse and install plugins (e.g., PagerDuty, LaunchDarkly) that add functionality without writing integration code.
- **As an engineering leader,** I want a dashboard that shows adoption metrics: template usage, service health, and team onboarding velocity.

## PRD Sections

### Problem
Engineering teams spend 30%+ of capacity on infrastructure toil. Internal platforms take 6+ months to build and require ongoing maintenance. Orchestra eliminates both problems.

### Users
Platform engineering leads, individual developers, engineering VPs at 50–200 dev organizations.

### Success Metrics
- **Time-to-first-service:** Median under 15 minutes from signup to a deployed "hello world" service
- **Template execution success rate:** > 95% (no manual intervention required)
- **Weekly active teams:** > 80% of registered teams use the platform at least once per week
- **Net Promoter Score:** > 40 at 90 days post-onboarding

### MVP Scope
1. **Service Catalog** — Register, search, and view services with ownership metadata. Import from GitHub, GitLab, and Bitbucket.
2. **Software Templates** — 5 built-in templates (Go microservice, Node.js API, Python worker, React SPA, infra module) plus a custom template builder.
3. **Plugin Framework** — 5 launch partner plugins (PagerDuty, Datadog, LaunchDarkly, Sentry, CircleCI). SDK and documentation for third-party developers.
4. **Admin Dashboard** — User management, org settings, template usage analytics, audit log preview.
5. **Billing** — Stripe integration for self-serve subscription management.

### Out of Scope (v1)
- Plugin marketplace (search, reviews, billing for developers) — planned v2
- SSO/SAML — Enterprise tier only; v1 uses Auth0 social login + email/password
- Multi-region deployment — AWS us-east-1 only for v1
- On-premises deployment — cloud-only for v1
- AI-powered service recommendations — v3 research item

### Timeline
- **Month 1–2:** Core platform (service catalog + template engine) — alpha with 5 design partners
- **Month 3–4:** Plugin framework + marketplace backend — private beta (20 orgs)
- **Month 5:** Admin dashboard, billing, polish — public beta
- **Month 6:** GA launch, content marketing push, conference debut

### Out of Scope
- Custom integrations beyond the plugin framework
- Managed CI/CD runners (customers bring their own CI)
- Incident management or on-call scheduling (partner plugins fill this gap)
