# Scalability Decision Tree

```
Is your software intended for medical purposes (diagnosis, treatment, prevention, monitoring)?
├── YES → It's potentially SaMD. Proceed to classification.
│   ├── Is it Class I (low risk, e.g., medical image storage)?
│   │   └── General controls, likely 510(k) exempt. Document decision. Ship.
│   ├── Is it Class II (moderate risk, e.g., diagnostic aid with clinician review)?
│   │   └── 510(k) required. Identify predicate device. Full design controls per 820.30.
│   └── Is it Class III (high risk, e.g., autonomous diagnosis)?
│       └── PMA required. Clinical evidence needed. This is a 2-4 year, $5M+ pathway.
└── NO → Not a medical device under FDA. Document the determination. Ship as general software.

Do you handle Protected Health Information (PHI)?
├── YES → Are you a Covered Entity or Business Associate?
│   ├── Covered Entity → Full HIPAA compliance (Privacy, Security, Breach rules).
│   └── Business Associate → Sign BAA. Implement Security Rule safeguards.
└── NO → HIPAA doesn't apply. Still follow good security practices.

Have you had an FDA inspection or notified body audit in the last 2 years?
├── YES → Were observations (483) or non-conformities issued?
│   ├── YES → CAPA required. Address within timeline. Failure = warning letter.
│   └── NO → Clean audit. Maintain QMS. Schedule next internal audit.
└── NO → Schedule a mock audit within 6 months. Don't wait for the real thing.

Is your software changing (new feature, new algorithm, new intended use)?
├── YES → Does the change significantly affect safety or effectiveness?
│   ├── YES → May need new 510(k) or notified body notification. Assess with consultant.
│   └── NO → Document in change control. No submission needed. Move forward.
└── NO → Maintain. Review annually.
```


**What good looks like:** Regulatory pathway document with requirements, timeline, and budget. Evidence binder prepared for submission (QMS, risk management, clinical evaluation, PMS). Regulatory submission accepted within first review cycle. Post-market surveillance plan active.
