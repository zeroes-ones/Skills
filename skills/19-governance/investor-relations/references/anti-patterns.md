# Anti-Patterns

<!-- QUICK: 30s -- machine-detectable anti-patterns with auto-prevention -->

| ❌ Anti-Pattern | ✅ Do This Instead | 🔍 Detect (grep/lint) | 🛡️ Auto-Prevent |
|---|---|---|---|
| Fundraising at 6 months runway with decelerating growth | Start at 12+ months runway while growth is accelerating | `file_contains("*", "runway.*[3-6] months")` AND `file_contains("*", "(declining|slowing|decelerating).*growth")` | STOP. Require 12+ month runway projection before any fundraising advice. |
| Sending generic pitch deck to 50 investors | Customize first 3 slides per investor: why this firm, this partner, now | `grep -rl "\.pptx" \| xargs grep -l "pitch deck"` with no `investor-tailoring.md` | WARN. Generate per-investor tailoring brief before distribution. |
| Accepting term sheet on valuation headline alone | Build full comparison: liq pref, participation, board, anti-dilution | `file_contains("*", "signed.*term sheet")` AND NOT `file_exists("*term-sheet-comparison*")` | STOP. Generate term sheet comparison matrix before signature. |
| Cap table via Excel beyond 10 equity holders | Migrate to Carta/Pulley; reconcile monthly; counsel audit | `file_exists("*.xlsx")` AND `file_contains("*.xlsx", "(option pool|warrant|convertible note)")` AND `wc -l shareholders.csv > 10` | REFUSE cap table operations on Excel. Escalate to Carta/Pulley. |
| Treating all investors equally in comms | Tier: active (weekly), warm (bi-weekly), passive (monthly), disengaged (quarterly) | `file_contains("*", "send.*update.*all.*investors")` AND NOT `file_contains("*", "(tier|segment).*investor")` | WARN. Generate investor tier list and cadence schedule. |
| Data room as unstructured Dropbox folder | 14-folder data room, indexed, counsel-reviewed, Docsend access control | `file_exists("data-room/")` AND NOT `file_exists("data-room/00-index.md")` | STOP. Build structured data room with index before investor access. |
| Disclosing bad news first time during diligence | Pre-disclose material challenges before term sheet | `file_mtime("*.md")` during diligence AND `grep "first time disclos"` in investor comms | STOP. Generate pre-disclosure memo for all material risks. |
| Skipping investor updates "nothing to report" | Send monthly regardless — silence = suspicion | `file_mtime("investor-update*.md") > 60d` | ALERT. Auto-generate "steady progress" investor update. |
