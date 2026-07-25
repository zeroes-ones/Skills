## Anti-Patterns

| ❌ Anti-Pattern | ✅ Do This Instead |
|----------------|-------------------|
| Tracking everything "just in case" — 500+ events, no taxonomy | Define 20-30 core events that map to the user journey. Every event must answer a product question. |
| Reporting "average" retention — single number across all users | Report by cohort (acquisition week/month). Averages hide declining new-user retention behind stable old-user retention. |
| Running A/A tests repeatedly — "verifying the system" | One A/A test at setup validates randomization. After that, trust your platform. Repeated A/A tests waste traffic and find false positives by chance. |
| Optimizing for clicks/engagement without measuring downstream value | Clicks -> core action conversion. "Engagement went up" means nothing if users are clicking but not converting. Measure the full chain. |
| Calling a metric "North Star" but changing it every quarter | North Star is stable for years. If you are changing it quarterly, you have not found it. Input metrics change; North Star does not. |
| Building dashboards before defining what decisions they drive | Decision-first dashboard design: "When metric X crosses threshold Y, we do Z." If you cannot complete that sentence, skip the dashboard. |
| Segmenting by demographics when behavior segments are 10x more predictive | Power users vs casual users > Male vs Female. Behavior segmentation > demographic segmentation. Always. |
| Stopping an experiment at "almost significant" (p=0.06) | p=0.06 means 6% chance the result is noise. Wait for target N or call it inconclusive. "Almost significant" is not significant. |
