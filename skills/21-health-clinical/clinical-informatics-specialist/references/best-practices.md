# Best Practices

<!-- DEEP: 10+min -->
<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Profile before you implement.** Write the FHIR StructureDefinition and validate it against the FHIR validator before writing any integration code. A validated profile catches 80% of interoperability issues at design time.
- **Use USCDI as your minimum data baseline.** USCDI v4 defines the minimum data classes required for nationwide interoperability. Start there, then extend with domain-specific profiles (e.g., Hemophilia IG, mCODE for oncology).
- **Map once, use everywhere.** Build a centralized terminology service with canonical mappings (SNOMED ↔ ICD-10-CM ↔ local codes). Every downstream system queries the terminology service — never duplicate mapping logic.
- **Consent is not a checkbox.** Consent is a FHIR Consent resource with computable provisions that downstream systems enforce programmatically. A checkbox in a UI without a backend Consent resource is a compliance gap.
- **PRO measures degrade without monitoring.** Track PRO completion rates, floor/ceiling effects, and response patterns. A PRO instrument with <60% completion rate or >20% ceiling effect is not producing valid data.
- **De-identification is not anonymous re-identification.** Expert Determination under HIPAA requires a qualified statistician to certify re-identification risk is very small. Safe Harbor (18 identifiers removed) is safer but may strip clinically useful data. Choose method based on use case.
- **Test with real clinical data shapes, not synthetic data.** Synthetic FHIR data misses edge cases — missing required fields, codes outside ValueSets, contradictory clinical statements. Use de-identified real data for integration testing.
- **Version everything.** FHIR profiles, terminology ValueSets, consent policies, PRO instruments, mapping tables — all versioned. A pipeline processing data from 2024 with 2026 terminology codes produces garbage.
