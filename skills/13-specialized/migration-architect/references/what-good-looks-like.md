# What Good Looks Like — Full Quality Standard

When migration architecture is executed flawlessly, every migration has a phased plan with rollback checkpoints at each phase, data integrity is verified with row counts, checksums, and business-level reconciliation before cutover, feature flags gate every new code path so rollback takes seconds not hours, replication lag is monitored and never exceeds thresholds, the pre-mortem's top three failure modes have automated triggers, and the cutover window is measured in minutes — the business continues operating without detecting the migration happened.

> This is the full aspirational quality standard. The compressed version in SKILL.md is optimized for model token budgets.
