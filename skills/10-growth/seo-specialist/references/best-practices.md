# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Indexability is job #1** — You can't rank what Google can't index. Sitemaps, robots.txt, HTTP status codes, and canonicals are the foundation.
- **Renderability matters** — Google renders JavaScript. If content depends on JS, verify it's in the rendered HTML (GSC URL Inspection → View Crawled Page).
- **E-E-A-T is not optional for YMYL** — Medical, financial, legal content without demonstrated expertise will not rank.
- **Schema validates → Schema monitors** — Validate at deployment, monitor in GSC weekly. Schema errors can compound.
- **Core Web Vitals are cumulative** — Fix the worst-performing page first. One 10-second page drags down your entire origin's CrUX score.
- **Hreflang must be bidirectional** — EN→DE requires DE→EN. Broken hreflang is worse than no hreflang.
- **Link building is about relevance, not volume** — 5 links from authoritative industry publications > 500 directory links.
- **Algorithm updates happen every 3-6 months** — Don't panic-react. Wait for the update to finish rolling out (usually 2 weeks), then analyze.
