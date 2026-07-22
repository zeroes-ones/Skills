# Developer Relations Strategy

## Conference Talks

**KubeCon North America 2026** (November 12–15, Salt Lake City): Accepted talk — *"IDP in a Box: How Orchestra Automates 80% of Platform Engineering Toil"*. 30-minute session in the Platform Engineering track. Covers: golden path templates, plugin SDK, self-service infrastructure, and developer onboarding metrics. Target audience: 300+ platform engineers. Supporting materials: slide deck, live demo recording (backup if WiFi fails), 1-page takeaway PDF with links.

**PlatformCon 2026** (June 8–10, virtual): Proposed talk — *"Plugin Ecosystem Design: Lessons from Building an Extensible IDP"*. 20-minute lightning talk. Focuses on the technical decisions behind the plugin SDK: interface design, versioning strategy, sandboxing, and the plugin marketplace model. Decision notification expected August 2026.

**DevOpsDays Austin 2026** (October 5–6): Lightning talk — *"15 Minutes to Production: Developer Onboarding at Orchestra"*. Applied, awaiting selection.

## Workshop Program

*"Build Your IDP in 2 Hours"* — a hands-on workshop delivered at conferences and as a virtual event. Attendees bring a laptop and leave with a working internal developer platform. Format: 15-minute intro, 90 minutes of guided hands-on (deploy Orchestra locally via Docker Compose, create a golden path template, scaffold a service, configure a plugin), 15-minute Q&A. Run 4 times to date: average 53 attendees per session (range: 38–72). NPS score: 78. All workshop materials open-source at `github.com/orchestra-platform/idp-workshop`.

## Sample Repositories

Five example repos demonstrate real-world Orchestra integrations, all published under `github.com/orchestra-platform/examples/`:

1. **go-api-template**: Full Go REST API with Dockerfile, Helm chart, GitHub Actions CI, and Orchestra template definition.
2. **react-spa-template**: Next.js 14 app with TypeScript, Tailwind, testing setup, and Orchestra template definition.
3. **cron-job-template**: Go cron job with SQS dead-letter queue, PagerDuty alerting, and Prefect schedule.
4. **data-pipeline-template**: Airbyte connector + dbt models + Great Expectations suite with Terraform infra-as-code.
5. **custom-plugin**: Example Orchestra plugin (Slack Notifier) demonstrating the Plugin SDK, manifest format, and publishing workflow.

Each repo includes a README with architecture decisions, a 5-minute quickstart, and links to Orchestra documentation.

## Community Building

**Discord Server**: `discord.gg/orchestra-dev` — 512 members as of July 18, 2026 (launched May 2026). Channels: #general, #help, #plugins (showcase + support), #templates (sharing golden paths), #feedback, #jobs. Weekly "Office Hours" voice call (Thursdays, 2pm ET) with rotating team members. Moderation: 2 community managers + 3 volunteer moderators.

**Developer Newsletter**: Separate from the content newsletter, this monthly email shares community highlights: top Discord discussions, plugin of the month, contributor spotlights, upcoming events. 320 subscribers, 42% open rate.

## Metrics

- Workshop NPS: 78 (target: >70)
- Discord member growth: 40–60/week organic
- Sample repo stars: 142 (go-api), 98 (react-spa), 67 (cron-job), 45 (data-pipeline), 38 (custom-plugin)
- Conference talk CTA conversion: 12% of talk attendees start a free trial within 7 days
