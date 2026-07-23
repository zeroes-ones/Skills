# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
1. **Automate setup, not docs:** If dev setup takes >30 min, fix the setup script — beautiful docs don't help if code won't run. One `./scripts/setup.sh` beats 50 pages of onboarding docs.
2. **Slack questions are your docs backlog:** Every repeated Slack answer belongs in docs. Search Slack for your top 10 answered questions — write those pages first.
3. **Generate API refs, never hand-write:** OpenAPI/SDL spec is the source of truth. Hand-written API docs go stale on the next deploy. Use Redoc or Scalar for rendering.
4. **Search before structure:** Users search, they don't browse. Tune Pagefind/Algolia relevance before reorganizing information architecture. Measure "search exit rate" (searches with no click-through).
5. **Vale in CI from day 1:** Style guide consistency is free if enforced automatically. One `.vale.ini` + custom terminology rules prevent bikeshedding over tone.
6. **Version only when you must:** Multi-version docs add maintenance burden. Until you have a v2 in production with users, don't version. When you do, keep current + N-1 only.
7. **Freshness automation is a feature:** A stale doc is worse than no doc. Flag pages >6 months without update. Escalate at 12 months. Set CODEOWNERS so every page has a human responsible.
8. **Quickstart is the most important page:** If a new user can't succeed in <5 minutes, they leave. Time-to-first-success is your #1 docs KPI. Test it on a fresh machine monthly.
9. **"Was this helpful?" on every page:** Binary feedback with optional text. Alert on pages with >50% "no" rate in last 30 days. This is your real-time quality signal.
10. **Eat your own dogfood:** Docs engineers must follow the same workflow they prescribe. If your team won't use the docs-as-code pipeline, no one else will.
