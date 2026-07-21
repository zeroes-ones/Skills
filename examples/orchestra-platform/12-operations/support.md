# Customer Support

## Support Channels

**Intercom**: Embedded chat widget on `orchestra.dev` and the web app. Staffed during business hours (9am–6pm ET, Mon–Fri) by the Customer Success team (2 agents). After hours: chatbot deflects to knowledge base articles with an option to leave a message for next-business-day follow-up. Email-to-ticket via `support@orchestra.dev` creates an Intercom conversation with the same SLA tracking.

**Linear**: Bug tracking and feature request management. Support agents triage verified bugs into Linear with severity labels (P1–P4, matching incident response severity). Feature requests tagged `source:support` for weekly product review. Linear-GitHub integration auto-closes issues when PRs merge.

**PagerDuty**: On-call escalation for P1 incidents. Intercom conversations can be escalated to PagerDuty by support agents with a single click. See incident response plan for full escalation procedure.

## Knowledge Base

Self-service knowledge base at `help.orchestra.dev` powered by Help Scout Docs. 42 articles at launch organized in 5 categories:

- **Getting Started** (8 articles): Account setup, creating your first service, inviting team members, understanding the dashboard, billing overview.
- **Templates** (10 articles): Template types explained, configuring environment variables, resource limits, troubleshooting failed executions, best practices for golden path design.
- **Plugins** (9 articles): Plugin marketplace overview, installing plugins, plugin configuration reference, building custom plugins (SDK quickstart), publishing to the marketplace.
- **Troubleshooting** (8 articles): Common error messages, debugging deployments, API authentication issues, connectivity problems, checking service logs.
- **Billing & Account** (7 articles): Plan comparison, upgrading/downgrading, invoice download, adding payment methods, account deletion, data export.

Articles include step-by-step instructions with screenshots (updated quarterly), code snippets with copy buttons, and related article links at the bottom. Average help center deflection rate: 34% (visitors who search and don't open a chat).

## SLA Tiers

| Plan | Response Time | Coverage | Channels |
|------|--------------|----------|----------|
| Enterprise ($2,500+/mo) | 1 hour | 24/7/365 | Chat, Email, Phone (critical only) |
| Pro ($500/mo) | 4 hours | Business hours (9am–6pm ET) | Chat, Email |
| Starter ($50/mo) | 24 hours | Best-effort, business hours | Email only |

SLA measured from ticket creation to first human response (not auto-responder). Enterprise SLA compliance: 97.3% in July (1 breach due to PagerDuty misconfiguration, resolved within 2 hours).

## Feedback Loop

All support interactions tagged with categories (templates, plugins, billing, bug, feature-request, docs-gap). Weekly product meeting (Wednesdays, 2pm) includes a "Voice of Customer" agenda item: top 3 support themes, new feature requests with >3 votes, and docs gaps identified. Decisions tracked in Linear with `source:support` label. Monthly trend report shared with the full company at all-hands: ticket volume (avg 78/week, growing 15% MoM), CSAT score (4.6/5.0), median resolution time (2.3 hours), top 5 article searches.
