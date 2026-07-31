# Error Decoder

<!-- DEEP: 5min -- each entry includes a diagnostic grep pattern and step-by-step recovery loop for automation -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Launch messaging rejected by Legal/Regulatory -- "unsubstantiated clinical claims" | Claims made without evidence citations. "Improves outcomes" without specifying which study, what outcome, what population. | **Detect:** Missing study/citation terms in messaging containing improvement claims

**Fix:** Add specific citations for every clinical claim. Create claims-evidence matrix mapping every claim to a specific study.

**Auto-recovery:** 1. Extract claims inventory. 2. Match each against evidence database. 3. If unmatched, search literature. 4. Inject citation. 5. Re-submit for regulatory review. | Every clinical claim needs a citation, not just a reasonable belief. The detection pattern catches claims without evidence and the auto-recovery loop enforces literature-supported messaging. |
| Sales team ignores battle cards -- "they are outdated, I do not trust them" | Battle cards >90 days old. Competitive landscape changed and cards were not updated. Sales found an error and lost trust. | **Detect:** Stale battle card detection via date comparison

**Fix:** Cut to 2 pages max. Update within 48 hours of any competitive event. Co-create with top 3 reps. Add "last verified" timestamp.

**Auto-recovery:** 1. Check battle card staleness. 2. Refresh stale cards with competitive intel. 3. Update with top rep co-authors. 4. Validate with sales. 5. Deploy with notification. | Trust lost by one outdated battle card takes months to rebuild. The detection pattern catches stale cards and the auto-recovery loop forces rapid refresh with sales co-authors. |
| Win rate declining -- "we keep losing to Competitor X but nobody knows exactly why" | Competitive gap opened (feature, pricing, clinical evidence), messaging went stale, or market shifted. No win/loss analysis program. | **Detect:** Win rate declining over 2+ quarters AND competitive positioning present in messaging

**Fix:** Run urgent win/loss analysis on last 20 deals. Identify top 3 loss reasons. Update battle cards and messaging with counter-positioning.

**Auto-recovery:** 1. Run win-loss analyzer. 2. Extract themes. 3. Build counter-positioning for each theme. 4. Update battle cards. 5. Deploy sales training. | A declining win rate without win/loss analysis is guessing, not strategizing. The detection pattern catches sustained decline and the auto-recovery loop forces systematic analysis. |
| Enterprise prospect flags during procurement review: "You advertised SSO but it is not available" -- deal stalls | PMM messaged a roadmap feature as if GA. Marketing claims exceeded product reality. Procurement legal review caught the gap. | **Detect:** Features marked non-GA appearing in marketing materials

**Fix:** Immediately update all materials: mark roadmap features as "[COMING Q3 2026]" not "available." Create claims-reality matrix. PMM must attend sales calls.

**Auto-recovery:** 1. Audit all non-GA features in marketing. 2. Auto-annotate with roadmap status. 3. Verify zero false claims. 4. Schedule PMM sales calls. 5. Communicate correction to affected deals. | Marketing roadmap features as if GA creates legal liability and lost trust. The detection pattern catches GA=false features in marketing and the auto-recovery loop annotates and corrects. |
| Launch falls flat -- low pipeline, no analyst coverage, sales unprepared | Messaging not tested with target audience, sales not trained, demand-gen not aligned to launch timing. Go decision made despite red flags. | **Detect:** Low messaging/sales/demand readiness scores near launch date

**Fix:** Halt launch activities. Run messaging comprehension test with >=10 target buyers (>=80% recall). Mandate sales certification. Align campaigns to revised launch date.

**Auto-recovery:** 1. Run launch health check. 2. If any pillar <70%, pause. 3. Fix messaging with audience testing. 4. Deploy sales certification. 5. Align demand-gen campaigns. | A launch that clears all readiness gates but falls flat means the gates are wrong. The detection pattern catches readiness gaps and the auto-recovery loop enforces audience testing and sales certification before launch. |
| Analyst report misrepresents product -- "competitor X is the leader, we are a niche player" | Insufficient briefing: wrong analyst contacted, no evidence package, no customer references. Briefing was reactive, not proactive. | **Detect:** Missing last briefing date in analyst relations

**Fix:** Schedule corrective briefing within 2 weeks. Prepare evidence package with clinical outcomes, customer case studies (3+), integration depth. Offer 3 customer references.

**Auto-recovery:** 1. Identify misrepresentations. 2. Build evidence package. 3. Schedule corrective briefing. 4. Present evidence with customer references. 5. Establish quarterly touchpoint. | Analyst reports are written from briefings you gave, not from your product. The detection pattern catches stale analyst relationships and the auto-recovery loop builds a proactive briefing program. |
