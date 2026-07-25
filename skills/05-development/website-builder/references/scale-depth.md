## Operating at Different Levels

| Level | Website Output Characteristics | Stack Evolution |
|-------|-------------------------------|-----------------|
| **Solo (1 person, $0-5/mo)** | Static site, markdown content, no database, no user accounts. Deployed to Cloudflare Pages or GitHub Pages. Zero maintenance. | Astro/Hugo/11ty + Git-based CMS. Plausible self-hosted analytics. Upptime for monitoring. Domain from Cloudflare Registrar. |
| **Small (2-5 people, $20-100/mo)** | Hybrid site — mostly static with a few dynamic pages (blog comments, newsletter signup, contact form). Headless CMS for non-dev editors. | Astro/Next.js hybrid + Decap CMS/Tina CMS. Vercel/Netlify Pro hosting. Sanity free tier. Resend for transactional email. Sentry free tier for error tracking. |
| **Medium (5-20 people, $100-500/mo)** | Full web app — user auth, database, API, payments, real-time features. Multi-environment (dev → staging → production). Feature flags. | Next.js/Remix + Supabase/PlanetScale. Vercel Pro/Enterprise. Headless CMS (Sanity paid). Stripe for payments. Sentry Team. Better Uptime. CI/CD with GitHub Actions. |
| **Enterprise (20+ people, $500-5,000+/mo)** | Multi-tenant SaaS, global CDN, multi-region deployment, SOC 2 compliance, SSO, audit logging, custom analytics pipeline, dedicated support. | Next.js/Remix on AWS (ECS/EKS or Amplify). Enterprise CMS (Contentful/Contentstack). Auth0/Okta for SSO. DataDog/New Relic for observability. LaunchDarkly for feature flags. Incident response on-call rotation. |
