# Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep / lint) |
|---|---|---|
| Collecting IOCs without TTP context — feeds full of IPs with no adversary attribution | Every IOC must have a confidence score, first/last seen timestamps, and mapped threat actor | Check feeds for missing `created_by_ref` and `confidence` STIX fields |
| Running threat hunts without hypotheses — "just looking around" in logs | Generate specific hypotheses from intelligence gaps: "If APT29 used this TTP, what would we see in our logs?" | Audit hunt documentation for formal hypothesis statements |
| Sharing intelligence without Traffic Light Protocol (TLP) markings | Every STIX object must have TLP:RED/AMBER/GREEN/CLEAR based on sensitivity | Validate STIX bundles against TLP marking completeness |
| Equating IOC feeds with threat intelligence — confusing data with analysis | IOC feeds are data; intelligence requires human analysis with context, confidence, and business relevance | Count feed-to-report conversion rate; flag if >100 IOCs for every finished intelligence product |
| Trusting OSINT without source verification — single-source intel is rumor | Triangulate every claim across at least 3 independent sources before publishing | Flag intelligence products with <3 source references |
