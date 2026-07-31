# Error Decoder

<!-- DEEP: 5min -- each entry includes a diagnostic grep pattern and step-by-step recovery loop for automation -->

| Symptom | Root Cause | Fix | Lesson |
|---------|-----------|-----|--------|
| Clinical reviewer rejects illustration -- "this anatomy is incorrect" | Anatomical inaccuracy: illustrator used memory or non-medical reference. Wrong vessel placement, incorrect staging, outdated classification. | **Detect:** `grep -cP "Netter\|Gray's\|Thieme\|Sobotta\|anatomical.reference" *.svg *.md` -> 0

**Fix:** Verify against latest edition of anatomical reference. Cross-reference 2 independent sources. Re-submit with citation trail. Add reviewer sign-off metadata.

**Auto-recovery:** 1. List all clinical SVGs without anatomical references. 2. For each, check for citation. 3. Insert citation block. 4. Re-submit with clinical reviewer. | Anatomical accuracy requires citations, not memory. The detection pattern catches illustrations without anatomical references and the auto-recovery loop enforces a citation trail before clinical review. |
| Patients misunderstand visual -- "I do not know what this is showing" | Too much detail, no visual-first design, text-dependent. Assumed audience has clinical training. No patient testing before publish. | **Detect:** `grep -cP "comprehension\|patient.test\|usability" *.md` -> 0 AND file_contains "patient\|education\|brochure"

**Fix:** Simplify to core concept. Remove non-essential anatomical detail. Test with 5 patients from target demographic. Iterate until >80% can explain the concept in 10 seconds without reading labels.

**Auto-recovery:** 1. Check readability grade level. 2. Recruit patient testers. 3. Deploy comprehension test. 4. If <80%, simplify and re-test. 5. Escalate if still <80% after 3 iterations. | If a patient cannot explain the visual in 10 seconds, the illustration has failed. The detection pattern catches missing usability testing and the auto-recovery loop enforces patient comprehension testing. |
| Accessibility audit fails -- color-only differentiation, low contrast, missing alt text | Color palette designed without CVD testing. Red/green differentiation for critical structures. No pattern or label backup. | **Detect:** Color-blindness terms missing from docs AND multi-color SVGs present

**Fix:** Run Coblis/Color Oracle simulation. Add pattern overlays (hatching=danger, dots=safe), text labels on all color-coded elements, descriptive alt text with anatomical context. Increase contrast to >=4.5:1 (WCAG AA).

**Auto-recovery:** 1. Run CVD simulator. 2. If users cannot distinguish categories, add pattern overlays. 3. Generate alt text. 4. Check contrast >=4.5. 5. Boost contrast if needed while preserving hue. | Color-only differentiation excludes 8% of male viewers. The detection pattern catches missing CVD testing and the auto-recovery loop adds pattern overlays and alt text as fallbacks. |
| Translation workflow breaks -- text baked into raster images, labels cannot be extracted | Text was flattened into PNG/JPEG or rasterized within SVG. No text elements with data-i18n-key. Every language requires full re-illustration. | **Detect:** SVG files contain embedded raster images AND translation/localization files exist

**Fix:** Rebuild illustration with text as separate SVG text layer. Assign data-i18n-key to each text element. Store translations in JSON/Markdown key-value pairs.

**Auto-recovery:** 1. Run SVG text audit. 2. For rasterized illustrations, rebuild text layer. 3. Assign i18n keys. 4. Test with locale render. 5. Validate text-only comparison. | Text baked into images is untranslatable. The detection pattern catches rasterized text and the auto-recovery loop rebuilds with separate text layers and i18n key infrastructure. |
| Motion content causes photosensitive reactions -- animation triggers seizures in susceptible viewers | Flash rate exceeds 3/sec between high-contrast color alternations. No prefers-reduced-motion query. No static alternative. | **Detect:** Flash/blink/strobe terms in animation timeline AND missing prefers-reduced-motion CSS

**Fix:** Reduce flash rate to <=3/sec. Add CSS prefers-reduced-motion rule. Provide static keyframe alternative. Test with PEAT (Photosensitive Epilepsy Analysis Tool).

**Auto-recovery:** 1. Check flash rate. 2. Analyze timeline. 3. Auto-reduce to safe intervals. 4. Add CSS motion rules. 5. Add static fallback. | Photosensitive reactions are preventable with proper testing. The detection pattern catches risky flash rates and the auto-recovery loop enforces safety constraints and provides static alternatives. |
| Fetal illustration rejected by OB/GYN reviewer -- "wrong developmental stage for stated gestational age" | Gestational age convention mismatch: US uses weeks from LMP, Europe uses weeks from fertilization (2-week offset). No audience specification. | **Detect:** Fetal/embryo/prenatal SVGs without gestational age metadata

**Fix:** Confirm convention (LMP vs fertilization). Verify fetal morphology against Carnegie stages or standard embryology references. Specify audience and convention in metadata.

**Auto-recovery:** 1. List all prenatal illustrations. 2. Check metadata for gestationalAgeConvention. 3. Verify morphology. 4. Auto-annotate with convention and week. 5. Re-submit with convention documented. | Gestational age conventions vary by region and can differ by 2 weeks. The detection pattern catches missing gestational metadata and the auto-recovery loop forces convention documentation and morphology verification. |
